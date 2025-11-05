.. _bluetooth_mesh_sar_cfg:

分段和重组 (SAR)
#################################

分段和重组 (SAR) 提供了一种在网状网络中处理较大的上层传输层消息的方法，目的是增强蓝牙网状网络的吞吐量。下层传输层使用分段和重组机制。

下层传输层定义如何将上层传输层 PDU 分段并重组为多个下层传输 PDU，并将它们发送到对等设备的下层传输层。如果上层传输 PDU 适合，它将在单个下层传输 PDU 中发送。对于更长的数据包，如果不适合单个下层传输 PDU，下层传输层将执行分段，将上层传输 PDU 拆分为多个段。

接收设备上的下层传输层在将段向上传递到栈之前将段重组为单个上层传输 PDU。分段消息的传递由接收节点的下层传输层确认，而未分段消息的传递不会被确认。但是，当需要下层传输层确认时，适合一个下层传输 PDU 的上层传输 PDU 也可以作为单段分段消息发送。设置 ``send rel`` 标志（参见 :c:struct:`bt_mesh_msg_ctx`）以使用可靠的消息传输并确认单段分段消息。

传输层能够通过其 SAR 机制传输最多 32 个段，最大消息（PDU）大小为 384 个八位字节。要为蓝牙网状栈配置消息大小，请使用以下 Kconfig 选项：

* :kconfig:option:`CONFIG_BT_MESH_RX_SEG_MAX` 设置传入消息中的最大段数。
* :kconfig:option:`CONFIG_BT_MESH_TX_SEG_MAX` 设置传出消息中的最大段数。

Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_TX_SEG_MSG_COUNT` 和 :kconfig:option:`CONFIG_BT_MESH_RX_SEG_MSG_COUNT` 定义可以同时处理的传出和传入分段消息的数量。当将多个分段消息发送到同一目标时，消息被排队并一次发送一个。

传入和传出的分段消息共享用于分配其段的相同池。此池大小通过 :kconfig:option:`CONFIG_BT_MESH_SEG_BUFS` Kconfig 选项配置。传入和传出的消息都在事务开始时分配段。传出的分段消息一旦被接收器确认就逐个释放其段，而传入的消息首先在完全接收消息后才释放段。在定义缓冲区大小时请记住这一点。

SAR 不会对每个段的有效负载层有效负载施加额外的开销。

分段和重组 (SAR) 配置模型
******************************************************

通过蓝牙网状协议规范版本 1.1，可以使用 SAR 配置模型通过网状网络配置 SAR 行为，如间隔、计时器和重传计数器：

* :ref:`bluetooth_mesh_sar_cfg_cli`
* :ref:`bluetooth_mesh_sar_cfg_srv`

无论节点上是否存在 SAR 配置服务器，以下 SAR 行为都适用。

段的传输由段传输间隔（参见 `SAR Segment Interval Step`_ 状态）分隔。分段和重组可用的其他可配置时间间隔和延迟为：

* 单播重传之间的间隔（参见状态 `SAR Unicast Retransmissions Interval Step`_ 和 `SAR Unicast Retransmissions Interval Increment`_）。
* 多播重传之间的间隔（参见 `SAR Multicast Retransmissions Interval Step`_ 状态）。
* 段接收间隔（参见 `SAR Receiver Segment Interval Step`_ 状态）。
* 确认延迟增量（参见 `SAR Acknowledgment Delay Increment`_ 状态）。

当传输最后一个标记为未确认的段时，下层传输层启动重传计时器。SAR 单播重传计时器的初始值取决于消息的 TTL 字段值。如果 TTL 字段值大于 ``0``，则计时器的初始值根据以下公式设置：

.. math::

   unicast~retransmissions~interval~step + unicast~retransmissions~interval~increment \times (TTL - 1)


如果 TTL 字段值为 ``0``，则计时器的初始值设置为单播重传间隔步长。

SAR 多播重传计时器的初始值设置为多播重传间隔。

当下层传输层接收到消息段时，它启动 SAR 丢弃计时器。丢弃计时器指示下层传输层在丢弃该段所属的分段消息之前等待多长时间。SAR 丢弃计时器的初始值是 `SAR Discard Timeout`_ 状态指示的丢弃超时值。

SAR 确认计时器保存在为接收段发送段确认消息之前的时间。SAR 确认计时器的初始值使用以下公式计算：

.. math::

   min(SegN + 0.5 , acknowledgment~delay~increment) \times segment~reception~interval


``SegN`` 字段值标识上层传输 PDU 被分段成的段总数。

四个计数器与 SAR 行为相关：

* 两个单播重传计数（参见 `SAR Unicast Retransmissions Count`_ 状态和 `SAR Unicast Retransmissions Without Progress Count`_ 状态）
* 多播重传计数（参见 `SAR Multicast Retransmissions Count`_ 状态）
* 确认重传计数（参见 `SAR Acknowledgment Retransmissions Count`_ 状态）

如果传输中的段数高于 `SAR Segments Threshold`_ 状态的值，则使用 `SAR Acknowledgment Retransmissions Count`_ 状态的值重新传输段确认消息。

.. _bt_mesh_sar_cfg_states:

SAR 状态
**********

定义了两个与分段和重组相关的状态：

* SAR 发送器状态
* SAR 接收器状态

SAR 发送器状态是一个复合状态，控制分段消息的传输数量和时序。它包括以下状态：

* SAR Segment Interval Step
* SAR Unicast Retransmissions Count
* SAR Unicast Retransmissions Without Progress Count
* SAR Unicast Retransmissions Interval Step
* SAR Unicast Retransmissions Interval Increment
* SAR Multicast Retransmissions Count
* SAR Multicast Retransmissions Interval Step

SAR 接收器状态是一个复合状态，控制段确认传输的数量和时序以及分段消息重组的丢弃。它包括以下状态：

* SAR Segments Threshold
* SAR Discard Timeout
* SAR Acknowledgment Delay Increment
* SAR Acknowledgment Retransmissions Count
* SAR Receiver Segment Interval Step

SAR Segment Interval Step
=========================

SAR Segment Interval Step 状态保存一个值，控制分段消息的段传输之间的间隔。间隔以毫秒为单位测量。

使用 :kconfig:option:`CONFIG_BT_MESH_SAR_TX_SEG_INT_STEP` Kconfig 选项设置默认值。然后使用以下公式计算段传输间隔：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_TX\_SEG\_INT\_STEP} + 1) \times 10~\text{ms}


SAR Unicast Retransmissions Count
=================================

SAR Unicast Retransmissions Count 保存一个值，定义分段消息到单播目标的最大重传次数。使用
:kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_COUNT` Kconfig 选项为此状态设置默认值。

SAR Unicast Retransmissions Without Progress Count
==================================================

此状态保存一个值，定义分段消息到单播地址的最大重传次数，如果超时期间未收到确认或收到已确认段的确认，则将发送此重传次数。使用 Kconfig 选项
:kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_WITHOUT_PROG_COUNT` 设置最大重传次数。

SAR Unicast Retransmissions Interval Step
=========================================

此状态的值控制用于延迟分段消息到单播地址的未确认段重传的间隔步长。间隔步长以毫秒为单位测量。

使用 :kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_INT_STEP` Kconfig 选项设置默认值。然后使用此值通过以下公式计算间隔步长：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_TX\_UNICAST\_RETRANS\_INT\_STEP} + 1) \times 25~\text{ms}


SAR Unicast Retransmissions Interval Increment
==============================================

SAR Unicast Retransmissions Interval Increment 保存一个值，控制用于延迟分段消息到单播地址的未确认段重传的间隔增量。增量以毫秒为单位测量。

使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_INT_INC` 设置默认值。Kconfig 选项值通过以下公式用于计算增量：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_TX\_UNICAST\_RETRANS\_INT\_INC} + 1) \times 25~\text{ms}


SAR Multicast Retransmissions Count
===================================

此状态保存一个值，控制分段消息到多播地址的重传总数。使用 Kconfig 选项
:kconfig:option:`CONFIG_BT_MESH_SAR_TX_MULTICAST_RETRANS_COUNT` 设置重传总数。

SAR Multicast Retransmissions Interval Step
===========================================

此状态保存一个值，控制分段消息到多播地址的所有段重传之间的间隔。间隔以毫秒为单位测量。

使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_SAR_TX_MULTICAST_RETRANS_INT` 设置默认值，该值用于通过以下公式计算间隔：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_TX\_MULTICAST\_RETRANS\_INT} + 1) \times 25~\text{ms}


SAR Discard Timeout
===================

此状态的值定义下层传输层在接收分段消息的段之后、丢弃该分段消息之前等待的秒数。使用 Kconfig
选项 :kconfig:option:`CONFIG_BT_MESH_SAR_RX_DISCARD_TIMEOUT` 设置默认值。丢弃超时将使用以下公式计算：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_RX\_DISCARD\_TIMEOUT} + 1) \times 5~\text{seconds}


SAR Acknowledgment Delay Increment
==================================

此状态保存一个值，控制用于在接收新段后延迟确认消息传输的间隔的延迟增量。增量以段为单位测量。

使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_SAR_RX_ACK_DELAY_INC` 设置默认值。增量值计算为
:math:`\verb|CONFIG_BT_MESH_SAR_RX_ACK_DELAY_INC| + 1.5`。

SAR Segments Threshold
======================

SAR Segments Threshold 状态保存一个值，定义分段消息的段数阈值，用于确认重传。使用 Kconfig 选项
:kconfig:option:`CONFIG_BT_MESH_SAR_RX_SEG_THRESHOLD` 设置阈值。

当分段消息的段数高于此阈值时，栈还将额外重传每个确认消息，次数由
:kconfig:option:`CONFIG_BT_MESH_SAR_RX_ACK_RETRANS_COUNT` 的值给出。

SAR Acknowledgment Retransmissions Count
========================================

SAR Acknowledgment Retransmissions Count 状态控制下层传输层发送的段确认消息的重传次数。它给出当分段消息中的段大小高于 :kconfig:option:`CONFIG_BT_MESH_SAR_RX_SEG_THRESHOLD` 值时栈将额外发送的确认消息的重传总数。

使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_SAR_RX_ACK_RETRANS_COUNT` 为此状态设置默认值。段确认消息的最大传输次数为
:math:`\verb|CONFIG_BT_MESH_SAR_RX_ACK_RETRANS_COUNT| + 1`。

SAR Receiver Segment Interval Step
==================================

SAR Receiver Segment Interval Step 定义用于在接收新段后延迟确认消息传输的段接收间隔步长。间隔以毫秒为单位测量。

使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_SAR_RX_SEG_INT_STEP` 设置默认值并使用以下公式计算间隔：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_RX\_SEG\_INT\_STEP} + 1) \times 10~\text{ms}
