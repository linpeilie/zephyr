.. _bluetooth_mesh_blob:

BLOB 传输模型
####################

二进制大对象 (BLOB) 传输模型实现了蓝牙网状二进制大对象
传输模型规范版本 1.0，并提供通过蓝牙网状网络从单个源向许多目标节点发送大型二进制对象的功能。它是 :ref:`bluetooth_mesh_dfu` 的底层
传输方法，但也可用于其他对象传输
目的。该实现处于实验状态。

BLOB 传输模型支持传输最多 4 GB (2 \ :sup:`32`
字节)的连续二进制对象。BLOB 传输协议具有内置的数据包丢失恢复程序，并设置
检查点以确保所有目标在继续之前都已接收所有数据。不保证数据传输
顺序。

BLOB 传输受底层网状网络的传输速度和可靠性约束。
在理想条件下，BLOB 可以高达 1 kbps 的速率传输，允许 100 kB
BLOB 在 10-15 分钟内传输。然而，网络条件、传输能力和
其他限制因素可以轻易地将数据速率降低几个数量级。根据
应用程序和网络配置调整传输参数，以及
将其安排在网络流量较低的时段，将显著提高协议的速度
和可靠性。然而，在实际部署中不太可能实现接近理想速率的传输速率。

有两种 BLOB 传输模型：

.. toctree::
   :maxdepth: 1

   blob_srv
   blob_cli

BLOB 传输客户端在发送器节点上实例化，BLOB 传输服务器在接收器节点上实例化。

概念
********

BLOB 传输协议引入了几个新概念来实现 BLOB 传输。


BLOB
====

BLOB 是最多 4 GB 大小的二进制对象，可以包含应用程序希望通过
网状网络传输的任何数据。BLOB 是连续的数据对象，被划分为块和
数据块，以使传输可靠且易于处理。对 BLOB 的内容或
结构没有限制，应用程序可以自由定义任何编码或压缩。

BLOB 传输协议不提供任何内置的完整性检查、加密或
BLOB 数据认证。但是，蓝牙网状协议的底层加密
提供数据完整性检查，并使用
网络和应用级加密保护 BLOB 的内容免受第三方侵害。

块
------

二进制对象被划分为块，通常从几百字节到几千字节
大小。每个块单独传输，BLOB 传输客户端确保所有 BLOB
传输服务器已接收完整块，然后再继续下一个。块大小由传输的 ``block_size_log`` 参数确定，对于传输中的所有块都是相同的，除了最后一个可能较小。对于存储在闪存中的 BLOB，块大小通常是目标设备闪存页大小的倍数。

数据块
------

每个块被划分为数据块。数据块是 BLOB 传输中最小的数据单元，必须适合单个蓝牙网状接入消息（不包括操作码）（379 字节或更少）。传输数据块的机制取决于传输模式。

当在推 BLOB 传输模式下操作时，数据块作为未确认的数据包从
BLOB 传输客户端发送到所有目标 BLOB 传输服务器。一旦一个块中的所有数据块都发送了，BLOB 传输客户端会询问每个 BLOB 传输服务器是否缺少任何数据块，并重新发送它们。这将重复直到所有 BLOB 传输服务器都已接收所有数据块，或 BLOB传输客户端放弃。

当在拉 BLOB 传输模式下操作时，BLOB 传输服务器将一次从 BLOB 传输客户端请求少量数据块，并等待 BLOB 传输客户端发送它们，然后再请求更多数据块。这将重复直到所有数据块都已传输，或 BLOB传输服务器放弃。

在 :ref:`bluetooth_mesh_blob_transfer_modes` 部分了解有关传输模式的更多信息。

.. _bluetooth_mesh_blob_stream:

BLOB 流
============

在 BLOB 传输模型的 API 中，BLOB 数据处理与高级传输
处理分离。这种分离允许为不同
应用程序重用不同的 BLOB 存储和传输策略。虽然高级传输由应用程序直接控制，但 BLOB 数据本身通过 *BLOB 流* 访问。

BLOB 流类似于标准库文件流。通过打开、关闭、读取
和写入，BLOB 传输模型可以完全访问 BLOB 数据，无论它存储在闪存、
RAM 还是外设上。BLOB 流在使用前以访问模式（读取或写入）打开，BLOB 传输模型将使用 BLOB 流作为接口在块和数据块内移动 BLOB 数据。

交互
-----------

在读取或写入 BLOB 之前，通过调用其
:c:member:`open <bt_mesh_blob_io.open>` 回调打开流。当与 BLOB 传输服务器一起使用时，BLOB
流总是以写入模式打开，当与 BLOB 传输客户端一起使用时，总是打开
读取模式。

对于 BLOB 中的每个块，BLOB 传输模型首先调用
:c:member:`block_start <bt_mesh_blob_io.block_start>`。然后，根据访问模式，BLOB
流的 :c:member:`wr <bt_mesh_blob_io.wr>` 或 :c:member:`rd <bt_mesh_blob_io.rd>` 回调将
被重复调用以将数据移入或移出 BLOB。当模型完成处理块时，它
调用 :c:member:`block_end <bt_mesh_blob_io.block_end>`。当传输完成时，通过调用 :c:member:`close <bt_mesh_blob_io.close>` 关闭 BLOB 流。

实现
---------------

应用程序可以实现自己的 BLOB 流，或使用 Zephyr 提供的实现：

.. toctree::
   :maxdepth: 2

   blob_flash


传输能力
=====================

每个 BLOB 传输服务器可能具有不同的传输能力。每个设备的传输能力通过以下配置选项控制：

* :kconfig:option:`CONFIG_BT_MESH_BLOB_SIZE_MAX`
* :kconfig:option:`CONFIG_BT_MESH_BLOB_BLOCK_SIZE_MIN`
* :kconfig:option:`CONFIG_BT_MESH_BLOB_BLOCK_SIZE_MAX`
* :kconfig:option:`CONFIG_BT_MESH_BLOB_CHUNK_COUNT_MAX`

:kconfig:option:`CONFIG_BT_MESH_BLOB_CHUNK_COUNT_MAX` 选项也被 BLOB 传输
客户端使用，并影响 BLOB 传输客户端模型结构的内存消耗。

为了确保尽可能多的服务器能够接收传输，BLOB 传输客户端
可以在开始传输之前检索每个 BLOB 传输服务器的能力。客户端
将使用尽可能高的块和数据块大小传输 BLOB。

.. _bluetooth_mesh_blob_transfer_modes:

传输模式
==============

BLOB 可以使用两种传输模式传输：推 BLOB 传输模式和拉 BLOB 传输模式。在大多数情况下，应在推 BLOB 传输模式下进行传输。

在推 BLOB 传输模式下，发送速率由 BLOB 传输客户端控制，该客户端将在没有高级流控制的情况下推送每个块的所有数据块。推 BLOB 传输模式支持任意数量的目标节点，应为默认传输模式。

在拉 BLOB 传输模式下，BLOB 传输服务器将以其自身速率从 BLOB 传输客户端"拉取"数据块。拉 BLOB 传输模式可以与多个目标节点一起进行，并且旨在向作为 :ref:`bluetooth_mesh_lpn` 的目标节点传输 BLOB。当在拉 BLOB 传输模式下操作时，BLOB 传输服务器将从小批次请求 BLOB 传输客户端的数据块，并等待它们全部到达，然后再请求更多数据块。此过程重复直到 BLOB 传输服务器已接收一个块中的所有数据块。然后，BLOB传输客户端开始下一个块，BLOB传输服务器请求该块的所有数据块。


.. _bluetooth_mesh_blob_timeout:

传输超时
================

BLOB 传输的超时基于超时基数。客户端和服务器使用相同的超时基数值，但它们的超时计算方式不同。

BLOB 传输服务器使用以下公式计算 BLOB 传输超时::

  10 * (Timeout Base + 1) 秒


对于 BLOB 传输客户端，使用以下公式::

  (10000 * (Timeout Base + 2)) + (100 * TTL) 毫秒

其中 TTL 是传输中设置的生存时间值。

API 参考
*************

本节包含 BLOB 传输模型通用的类型和定义。

.. doxygengroup:: bt_mesh_blob
