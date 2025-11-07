.. _can_api:

CAN 控制器 (CAN Controller)
############################

.. contents::
    :local:
    :depth: 2

概述 (Overview)
****************

控制器局域网络是由 Bosch CAN 规范、Bosch CAN with Flexible Data-Rate 规范和
ISO 11898-1:2003 标准定义的双线串行总线。
CAN 最为人所知的是其在汽车领域的应用。然而，它也用于家庭和工业自动化以及其他产品。

.. warning::

   CAN 控制器只能在总线处于空闲(隐性)状态至少 11 个隐性位时才能初始化。
   因此，您必须确保 CAN RX 为高电平，至少在短时间内。这对于环回模式也是必需的。

ISO 11898-1:2003 中定义的位时序如下所示:

.. image:: timing.svg
   :width: 40%
   :align: center
   :alt: CAN 时序

单个位分为四个段。

* Sync_Seg: 节点在 Sync_Seg 的边沿进行同步。它的长度始终为一个时间量子。

* Prop_Seg: 总线的信号传播延迟以及收发器和节点的其他延迟。

* Phase_Seg1 和 Phase_Seg2: 定义采样点。位在 Phase_Seg1 结束时采样。

位速率由时间量子的时间和上面定义的值计算得出。
位的长度为 Sync_Seg 加 Prop_Seg 加 Phase_Seg1 加 Phase_Seg2 乘以单个时间量子的时间。
位速率是单个位长度的倒数。

位在采样点处采样。
采样点位于 Phase_Seg1 和 PhaseSeg2 之间，因此是用户需要选择的参数。
CiA 建议将采样点设置为位的 87.5%。

重新同步跳转宽度(SJW)定义了采样点可以移动的时间量子数量。
当需要重新同步时，采样点会移动。

时序参数(SJW、位速率和采样点，或位速率、Prop_Seg、Phase_Seg1 和 Phase_Seg2)
最初从设备树设置，并可以在运行时通过时序 API 进行更改。

CAN 使用所谓的标识符来识别帧，而不是使用地址来识别节点。
此标识符可以是 11 位宽(标准或基本帧)或扩展帧情况下的 29 位。
Zephyr CAN API 同时支持标准和扩展标识符。CAN 帧以显性的帧起始位开始。
之后是标识符。此阶段称为仲裁阶段。在仲裁阶段，允许写冲突。
它们通过显性位覆盖隐性位的事实来解决。
节点监视总线并注意到它们的传输何时被覆盖，在这种情况下，会中止传输。
这有效地使较低编号的标识符优先于较高编号的标识符。

过滤器用于白名单对特定节点感兴趣的标识符。不匹配任何过滤器的标识符将被忽略。
过滤器可以精确匹配或匹配标识符的指定部分。
这种方法称为掩码。
例如，对于标准标识符设置了 11 位或对于扩展标识符设置了 29 位的掩码必须完全匹配。
掩码中设置为零的位在匹配标识符时被忽略。
大多数 CAN 控制器在硬件中实现了有限数量的过滤器。
过滤器的数量在 Kconfig 中也受到限制以节省内存。

传输过程中可能会发生错误。如果节点检测到错误的帧，
它会用错误帧部分覆盖当前帧。
错误帧可以是错误被动或错误主动，具体取决于控制器的状态。
如果控制器处于错误主动状态，它会发送六个连续的显性位，
这违反了所有节点都能检测到的填充规则。发送方可能会在之后立即重新发送帧。

初始化的节点可以处于以下状态之一:

* 错误主动(Error-active)
* 错误被动(Error-passive)
* 总线关闭(Bus-off)

初始化后，节点处于错误主动状态。在此状态下，节点允许发送主动错误帧、ACK 和过载帧。
每个节点都有接收和发送错误计数器。
如果接收或发送错误计数器超过 127，节点将变为错误被动状态。
在此状态下，节点不再允许发送错误主动帧。
如果发送错误计数器进一步增加到 255，节点将变为总线关闭状态。
在此状态下，节点不允许向总线发送任何显性位。处于总线关闭状态的节点可以
在接收到 128 次 11 个并发隐性位后恢复。

您可以在这篇
`CAN 维基百科文章 <https://en.wikipedia.org/wiki/CAN_bus>`_ 中阅读更多关于 CAN 总线的信息。

Zephyr 支持以下 CAN 功能:

* 标准和扩展标识符
* 带掩码的过滤器
* 环回和静默模式
* 远程请求

发送 (Sending)
***************

以下代码片段展示了如何发送数据。

此基本示例发送一个标准标识符为 0x123 和八个字节数据的 CAN 帧。
当传递 NULL 作为回调时，如此示例所示，发送函数会阻塞，
直到帧被发送并被至少一个其他节点确认或发生错误。
超时仅在获取邮箱时生效。分配传输邮箱后，发送无法取消。

.. code-block:: C

  struct can_frame frame = {
          .flags = 0,
          .id = 0x123,
          .dlc = 8,
          .data = {1,2,3,4,5,6,7,8}
  };
  const struct device *const can_dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_canbus));
  int ret;

  ret = can_send(can_dev, &frame, K_MSEC(100), NULL, NULL);
  if (ret != 0) {
          LOG_ERR("Sending failed [%d]", ret);
  }


此示例展示了如何发送扩展标识符为 0x1234567 和两个字节数据的帧。
提供的回调在消息发送时或发生错误时被调用。将 :c:macro:`K_FOREVER` 传递给超时
会导致函数阻塞，直到将传输邮箱分配给帧或发生错误。
它不会像上面的示例那样阻塞直到消息被发送。

.. code-block:: C

  void tx_callback(const struct device *dev, int error, void *user_data)
  {
          char *sender = (char *)user_data;

          if (error != 0) {
                  LOG_ERR("Sending failed [%d]\nSender: %s\n", error, sender);
          }
  }

  int send_function(const struct device *can_dev)
  {
          struct can_frame frame = {
                  .flags = CAN_FRAME_IDE,
                  .id = 0x1234567,
                  .dlc = 2
          };

          frame.data[0] = 1;
          frame.data[1] = 2;

          return can_send(can_dev, &frame, K_FOREVER, tx_callback, "Sender 1");
  }

接收 (Receiving)
*****************

只有当帧匹配过滤器时才会被接收。
以下代码片段展示了如何通过添加过滤器来接收帧。

这里有一个用于 :c:func:`can_add_rx_filter` 的接收回调示例。
在添加过滤器时传递用户数据参数。

.. code-block:: C

  void rx_callback_function(const struct device *dev, struct can_frame *frame, void *user_data)
  {
          ... do something with the frame ...
  }

以下片段展示了如何添加带有回调函数的过滤器。
这是接收消息最有效但也是最关键的方式。
回调函数从中断上下文调用，这意味着回调函数应该尽可能短并且不能阻塞。
不允许从用户空间上下文添加回调函数。

此示例的过滤器配置为精确匹配标识符 0x123。

.. code-block:: C

  const struct can_filter my_filter = {
          .flags = 0U,
          .id = 0x123,
          .mask = CAN_STD_ID_MASK
  };
  int filter_id;
  const struct device *const can_dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_canbus));

  filter_id = can_add_rx_filter(can_dev, rx_callback_function, callback_arg, &my_filter);
  if (filter_id < 0) {
    LOG_ERR("Unable to add rx filter [%d]", filter_id);
  }

这里展示了 :c:func:`can_add_rx_filter_msgq` 的示例。
使用此函数，可以同步接收帧。此函数可以从用户空间上下文调用。
消息队列的大小应该与预期的积压一样大。

此示例的过滤器配置为精确匹配扩展标识符 0x1234567。

.. code-block:: C

  const struct can_filter my_filter = {
          .flags = CAN_FILTER_IDE,
          .id = 0x1234567,
          .mask = CAN_EXT_ID_MASK
  };
  CAN_MSGQ_DEFINE(my_can_msgq, 2);
  struct can_frame rx_frame;
  int filter_id;
  const struct device *const can_dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_canbus));

  filter_id = can_add_rx_filter_msgq(can_dev, &my_can_msgq, &my_filter);
  if (filter_id < 0) {
    LOG_ERR("Unable to add rx msgq [%d]", filter_id);
    return;
  }

  while (true) {
    k_msgq_get(&my_can_msgq, &rx_frame, K_FOREVER);
    ... do something with the frame ...
  }

:c:func:`can_remove_rx_filter` 移除给定的过滤器。

.. code-block:: C

  can_remove_rx_filter(can_dev, filter_id);

设置位速率 (Setting the bitrate)
**********************************

位速率和采样点最初在运行时设置。要从应用程序更改它，
可以使用 :c:func:`can_set_timing` API。:c:func:`can_calc_timing` 函数
可以根据位速率和千分之几的采样点计算时序。
以下示例将位速率设置为 250k 波特，采样点为 87.5%。

.. code-block:: C

  struct can_timing timing;
  const struct device *const can_dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_canbus));
  int ret;

  ret = can_calc_timing(can_dev, &timing, 250000, 875);
  if (ret > 0) {
    LOG_INF("Sample-Point error: %d", ret);
  }

  if (ret < 0) {
    LOG_ERR("Failed to calc a valid timing");
    return;
  }

  ret = can_stop(can_dev);
  if (ret != 0) {
    LOG_ERR("Failed to stop CAN controller");
  }

  ret = can_set_timing(can_dev, &timing);
  if (ret != 0) {
    LOG_ERR("Failed to set timing");
  }

  ret = can_start(can_dev);
  if (ret != 0) {
    LOG_ERR("Failed to start CAN controller");
  }

对于支持 CAN FD 的控制器，存在类似的 API 用于计算和设置数据阶段的时序。
请参阅 :c:func:`can_set_timing_data` 和 :c:func:`can_calc_timing_data`。

SocketCAN
*********

Zephyr 还支持 SocketCAN，这是 Zephyr CAN API 的 BSD socket 实现。
SocketCAN 将众所周知的 BSD Socket API 的便利性带到了控制器局域网络。
它与 Linux SocketCAN 实现兼容，许多其他高级 CAN 项目都建立在此基础上。
请注意，帧会路由到网络堆栈而不是直接传递，这会增加一些计算和内存开销。

示例 (Samples)
***************

我们有两个可立即构建的示例，展示了 Zephyr CAN API 的使用:
:zephyr:code-sample:`Zephyr CAN counter sample <can-counter>` 和
:zephyr:code-sample:`SocketCAN sample <socket-can>`。


CAN 控制器 API 参考 (CAN Controller API Reference)
***************************************************

.. doxygengroup:: can_controller
