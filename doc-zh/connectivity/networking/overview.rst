.. _ip_stack_overview:

概述
########

.. contents::
    :local:
    :depth: 2

支持的功能
******************

网络 IP 协议栈是模块化的,可通过构建时配置选项进行高度配置。您可以通过仅启用
应用程序所需的网络功能来最小化系统内存消耗。如果不需要,几乎所有功能都可以禁用。

* **IPv6** 默认启用对 IPv6 的支持。可以根据网络需求启用或禁用各种 IPv6 子选项。

  * 开发人员可以设置同时活动的单播和多播 IPv6 地址的数量。
  * 设备的 IPv6 地址可以使用 SLAAC(无状态地址自动配置)静态或动态设置
    (`RFC 4862 <https://tools.ietf.org/html/rfc4862>`_)。
  * 系统还支持多个 IPv6 前缀,最大 IPv6 前缀计数可以在构建时配置。
  * 如果不需要,可以禁用 IPv6 邻居缓存,其大小可以在构建时配置。
  * 默认启用 IPv6 邻居发现支持
    (`RFC 4861 <https://tools.ietf.org/html/rfc4861>`_)。
  * 默认启用多播侦听器发现 v2 支持
    (`RFC 3810 <https://tools.ietf.org/html/rfc3810>`_)。
  * IPv6 头压缩(6lo)可用于 IEEE 802.15.4 网络的 IPv6 连接
    (`RFC 4944 <https://tools.ietf.org/html/rfc4944>`_)。

* **IPv4** 网络协议栈支持传统的 IPv4。它不能被 IEEE 802.15.4 使用,因为此网络
  技术仅支持 IPv6。IPv4 可以在基于以太网的网络中使用。默认情况下禁用 IPv4 支持。

  * 支持 DHCP(动态主机配置协议)客户端
    (`RFC 2131 <https://tools.ietf.org/html/rfc2131>`_)。
  * IPv4 地址也可以手动配置。默认支持静态 IPv4 地址。

* **双栈支持。** 网络协议栈允许开发人员配置系统同时使用 IPv6 和 IPv4。

* **UDP** 支持用户数据报协议
  (`RFC 768 <https://tools.ietf.org/html/rfc768>`_)。
  开发人员可以发送 UDP 数据报(客户端支持)或创建侦听器以接收发往特定端口的
  UDP 数据包(服务器端支持)。

* **TCP** 支持传输控制协议
  (`RFC 793 <https://tools.ietf.org/html/rfc793>`_)。应用程序可以使用服务器
  和客户端角色。可用于应用程序的 TCP 套接字数量可以在构建时配置。

* **BSD 套接字 API** 支持
  :ref:`BSD 套接字兼容 API <bsd_sockets_interface>` 的子集。
  支持阻塞和非阻塞数据报(UDP)和流(TCP)套接字。

* **安全套接字 API** 对套接字 API 的 TLS/DTLS 安全协议和配置选项的实验性支持。
  实现的安全函数由 mbedTLS 库提供。

* **MQTT** 支持消息队列遥测传输(ISO/IEC PRF 20922)。
  实现了 MQTT v3.1.1 的示例 :zephyr:code-sample:`mqtt-publisher` 客户端应用程序。

* **CoAP** 支持受约束应用协议
  (`RFC 7252 <https://tools.ietf.org/html/rfc7252>`_)。
  实现了 :zephyr:code-sample:`coap-client` 和 :zephyr:code-sample:`coap-server`
  示例应用程序。

* **LWM2M** 支持 OMA 轻量级 M2M 协议
  (`LwM2M 规范 1.0.2`_),通过"引导"、"客户端注册"、"设备管理和服务启用"
  以及"信息报告"接口。实现了所需的核心 LwM2M 对象以及多个 IPSO 智能对象。
  当使用 Kconfig 选项启用时,也以类似方式支持 (`LwM2M 规范 1.1.1`_)。
  :zephyr:code-sample:`lwm2m-client` 示例将该库作为示例实现。

* **HTTP** 支持超文本传输协议客户端和服务器。
  :ref:`http_client_interface` 库支持 HTTP/1.1 (`RFC 2616`_)。
  :ref:`http_server_interface` 库支持 HTTP/1.1 (`RFC 2616`_) 和
  HTTP/2 (`RFC 9113`_)。
  提供了 :zephyr:code-sample:`sockets-http-client` 和
  :zephyr:code-sample:`sockets-http-server` 示例。

* **DNS** 支持域名服务
  (`RFC 1035 <https://tools.ietf.org/html/rfc1035>`_) 客户端功能。
  应用程序可以使用 DNS API 从 DNS 服务器查询域名信息或 IP 地址。可以查询
  IPv4 (A) 和 IPv6 (AAAA) 记录。
  支持组播 DNS (mDNS) (`RFC 6762 <https://tools.ietf.org/html/rfc6762>`_)
  和链路本地组播名称解析
  (LLMNR) (`RFC 4795 <https://tools.ietf.org/html/rfc4795>`_)。

* **网络管理 API。** 应用程序可以使用网络管理 API 侦听核心协议栈生成的管理事件,
  例如将 IP 地址添加到设备、网络接口启动等。

* **Wi-Fi 管理 API。** 应用程序可以使用 Wi-Fi 管理 API 管理接口,例如连接到
  Wi-Fi 网络和扫描可用的 Wi-Fi 网络。

* **Wi-Fi 网络管理器 API。** Wi-Fi 网络管理器现在可以向 Wi-Fi 协议栈注册自己。
  然后,网络管理器可以实现 Wi-Fi 管理 API 并管理 Wi-Fi 接口。

* **多种网络技术。** Zephyr OS 可以配置为通过在 Kconfig 中启用它们来同时支持
  多种网络技术:例如,以太网、Wi-Fi 和 802.15.4 支持。请注意,这些技术之间不
  提供自动 IP 路由功能。应用程序可以根据需要将数据发送到所需的网络接口。

* **最小复制网络缓冲区管理。** 可以拥有最小复制网络数据路径。这意味着系统在
  将应用程序数据发送到网络时会尽量避免复制应用程序数据。

* **虚拟 LAN 支持。** 虚拟 LAN (VLAN) 允许将物理以太网网络划分为逻辑网络。
  有关更多详细信息,请参阅 :ref:`VLAN 支持 <vlan_interface>`。

* **网络流量分类。** 可以根据应用程序需求对发送和接收的网络数据包进行优先级排序。
  有关更多详细信息,请参阅 :ref:`流量分类 <traffic-class-support>`。

* **时间敏感网络。** 支持 gPTP(广义精确时间协议)。
  有关更多详细信息,请参阅 :ref:`gPTP 支持 <gptp_interface>`。

* **网络 shell。** 网络 shell 提供用于查明网络状态、启用/禁用功能以及发出
  ping 或 DNS 解析等命令的助手。net-shell 在开发网络软件时很有用。
  有关更多详细信息,请参阅 :ref:`网络 shell <net_shell>`。

此外,Zephyr OS v1.7 及更高版本支持这些网络技术(链路层):

* IEEE 802.15.4
* 蓝牙
* 以太网
* SLIP (串行线路上的 IP)。用于使用 QEMU 进行测试。它为主机系统(如 Linux)
  提供以太网接口,测试应用程序可以在 Linux 主机中运行并将网络数据发送到
  Zephyr OS 设备。

源树布局
******************

网络协议栈源代码树的组织如下:

``subsys/net/ip/``
  这是 IP 协议栈代码所在的位置。

``subsys/net/l2/``
  这是 IP 协议栈第 2 层代码所在的位置。这包括对以太网、IEEE 802.15.4 和
  Wi-Fi 的通用支持。

``subsys/net/lib/``
  应用层协议(DNS、MQTT 等)和其他协议栈组件(BSD 套接字等)。

``include/net/``
  公共 API 头文件。这些是应用程序需要包含的头文件,以使用 IP 网络功能。

``samples/net/``
  网络示例代码。这是开始网络应用程序开发的良好参考。

``tests/net/``
  测试应用程序。这些应用程序用于验证 IP 协议栈的功能,但不是示例代码的
  最佳来源(请参阅 ``samples/net``)。

.. _LwM2M 规范 1.0.2:
   https://www.openmobilealliance.org/release/LightweightM2M/V1_0_2-20180209-A/OMA-TS-LightweightM2M-V1_0_2-20180209-A.pdf

.. _LwM2M 规范 1.1.1:
   https://www.openmobilealliance.org/release/LightweightM2M/V1_1_1-20190617-A/

.. _RFC 2616:
   https://tools.ietf.org/html/rfc2616

.. _RFC 9113:
   https://tools.ietf.org/html/rfc9113
