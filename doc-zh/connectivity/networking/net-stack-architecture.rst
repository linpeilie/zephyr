.. _network_stack_architecture:

网络协议栈架构
##########################

.. toctree::
   :maxdepth: 1
   :hidden:

   net_pkt_processing_stats.rst

Zephyr 网络协议栈是专为 Zephyr OS 设计的原生网络协议栈。它由多层组成,每一层
都旨在向其他层提供特定服务。网络协议栈功能可通过 Kconfig 选项进行高度配置。

.. contents::
    :local:
    :depth: 2

网络协议栈的高级概述
****************************************

.. figure:: zephyr_netstack_overview.svg
    :alt: 网络协议栈架构概述
    :figclass: align-center

    网络协议栈概述

网络协议栈是分层的,由以下部分组成:

* **网络应用程序。** 网络应用程序可以使用提供的应用层协议库,也可以直接访问
  :ref:`BSD 套接字 API <bsd_sockets_interface>` 来创建网络连接、发送或接收数据
  以及关闭连接。应用程序还可以使用 :ref:`网络管理 API <net_mgmt_interface>`
  配置网络并设置相关参数,例如网络链路选项、开始扫描(如果适用)、侦听网络配置
  事件等。:ref:`网络接口 API <net_if_interface>` 可用于为网络接口设置 IP 地址、
  关闭网络接口等。

* **网络协议。** 这提供了各种协议的实现,例如

  * 应用层网络协议,如 CoAP、LWM2M 和 MQTT。
    有关它们的信息,请参阅 :ref:`应用协议章节 <net_protocols>`。
  * 核心网络协议,如 IPv6、IPv4、UDP、TCP、ICMPv4 和 ICMPv6。
    您可以使用 :ref:`BSD 套接字 API <bsd_sockets_interface>` 访问这些协议。

* **网络接口抽象。** 这提供了所有网络接口中常见的功能,例如关闭网络接口等。
  系统中可以有多个网络接口。
  有关更多详细信息,请参阅 :ref:`网络接口概述 <net_if_interface>`。

* **L2 网络技术。** 这为向实际网络设备发送和从实际网络设备接收数据提供了
  通用 API。
  有关更多详细信息,请参阅 :ref:`L2 概述 <net_l2_interface>`。
  这些网络技术包括 :ref:`以太网 <ethernet_interface>`、
  :ref:`IEEE 802.15.4 <ieee802154_interface>`、
  :ref:`蓝牙 <bluetooth_api>`、:ref:`CANBUS <can_api>` 等。
  其中一些技术支持 IPv6 头压缩(6Lo),
  有关详细信息,请参阅 `RFC 6282 <https://tools.ietf.org/html/rfc6282>`_。
  例如,IPv4 的 `ARP <https://tools.ietf.org/html/rfc826>`_ 由
  :ref:`以太网组件 <ethernet_interface>` 完成。

* **网络设备驱动程序。** 实际的低级设备驱动程序处理网络数据包的物理发送或接收。

网络数据流
*****************

应用程序通常由一个或多个执行应用程序逻辑的 :ref:`线程 <threads_v2>` 组成。
使用 :ref:`BSD 套接字 API <bsd_sockets_interface>` 时,将发生以下情况。

.. figure:: zephyr_netstack_overview-rx_sequence.svg
    :alt: 网络 RX 数据流
    :figclass: align-center

    网络 RX 数据流

数据接收 (RX)
-------------------

1. 设备驱动程序接收网络数据包。

2. 设备驱动程序分配足够的网络缓冲区来存储接收的数据。网络数据包被放置在
   适当的 RX 队列中(由 :ref:`k_fifo <fifos_v2>` 实现)。默认情况下,系统中
   只有一个接收队列,但可以拥有多达 8 个接收队列。这些队列将以不同的优先级
   处理传入的数据包。有关更多详细信息,请参阅 :ref:`traffic-class-support`。
   接收队列还用作分离数据处理管道(下半部)的方式,因为设备驱动程序在中断
   上下文中运行,必须尽可能快地进行处理。

3. 然后将网络数据包传递给正确的 L2 驱动程序。L2 驱动程序可以检查数据包是否
   正确并根据需要进行修改,例如剥离 L2 头和帧校验序列等。

4. 数据包由网络接口处理。如果通过 :kconfig:option:`CONFIG_NET_STATISTICS`
   启用,则收集网络统计信息。

5. 然后将数据包传递给 L3 处理。如果数据包基于 IP,则 L3 层检查数据包是否为
   正确的 IPv6 或 IPv4 数据包。

6. 然后,套接字处理程序找到网络数据包所属的活动套接字,并将其放入该套接字的
   队列中,以便将网络代码与应用程序分离。通常,应用程序在用户空间上下文中运行,
   网络协议栈在内核上下文中运行。

7. 然后,应用程序将接收数据并可以根据需要进行处理。应用程序应该使用
   :ref:`BSD 套接字 API <bsd_sockets_interface>` 创建一个将接收数据的套接字。


.. figure:: zephyr_netstack_overview-tx_sequence.svg
    :alt: 网络 TX 数据流
    :figclass: align-center

    网络 TX 数据流

数据发送 (TX)
-----------------

1. 应用程序应在发送数据时使用 :ref:`BSD 套接字 API <bsd_sockets_interface>`。

2. 准备应用程序数据以发送到内核空间,然后复制到内部 net_buf 结构。

3. 根据套接字类型,在数据前面添加协议头。例如,如果套接字是 UDP 套接字,
   则构造 UDP 头并将其放在数据前面。

4. 为 UDP 或 TCP 数据包在网络数据包中添加 IP 头。

5. 网络协议栈将检查网络接口是否正确设置为网络数据包,并且还将确保在数据排队
   发送之前启用网络接口。

6. 然后对网络数据包进行分类并放入适当的传输队列(由 :ref:`k_fifo <fifos_v2>`
   实现)。默认情况下,系统中只有一个传输队列,但可以拥有多达 8 个传输队列。
   这些队列将以不同的优先级处理发送的数据包。有关更多详细信息,请参阅
   :ref:`traffic-class-support`。
   在传输数据包分类之后,正确的 L2 层模块检查数据包。L2 模块将对数据进行
   额外检查,还将为网络数据包创建任何 L2 头。如果一切正常,则将数据提供给
   网络设备驱动程序以发送出去。

7. 设备驱动程序将数据包发送到网络。

请注意,在 TX 和 RX 数据路径中,队列(:ref:`k_fifo <fifos_v2>`)形成分离点,
在这些分离点数据从一个 :ref:`线程 <threads_v2>` 传递到另一个线程。
这些 :ref:`线程 <threads_v2>` 可能在不同的上下文
(:ref:`内核 <kernel_api>` 与 :ref:`用户空间 <usermode_api>`)中运行,
并具有不同的 :ref:`优先级 <scheduling_v2>`。


网络数据包处理统计
************************************

有关网络处理统计信息的信息,请参阅 :ref:`此处 <net_pkt_processing_stats>`。
