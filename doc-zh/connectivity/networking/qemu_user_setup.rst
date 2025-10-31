.. _networking_with_user_qemu:

使用 QEMU User 网络（SLIRP）
#############################

.. contents::
    :local:
    :depth: 2

本页作为使用 QEMU SLIRP 与 Zephyr 结合的入门指南。

简介
*************

SLIRP 是一种网络后端，它在 QEMU 内部提供完整的 TCP/IP 协议栈，并基于该协议栈实现一个虚拟的 NAT 网络。
由于不依赖宿主机环境，SLIRP 的设置非常简单。

默认情况下，QEMU 使用 ``10.0.2.X/24`` 网络，并在 ``10.0.2.2`` 运行网关。
所有发往宿主网络的流量都将经过该网关，并依据 QEMU 命令行参数进行过滤。
该网关同时充当所有来宾系统的 DHCP 服务器，使其自动分配从 ``10.0.2.15`` 开始的 IP 地址。

关于 User Networking 的更多细节参见：
https://wiki.qemu.org/Documentation/Networking#User_Networking_.28SLIRP.29

在 Zephyr 中使用 SLIRP
************************

要在 Zephyr 中使用 SLIRP，需要启用相应的 Kconfig 选项以开启 User Networking：

.. code-block:: cfg

   CONFIG_NET_QEMU_USER=y

启用该配置后，所有 QEMU 启动都会使用 SLIRP。
在默认配置下，Zephyr 仅启用 User Networking，而不会传递任何附加参数。
这意味着来宾系统只能与 QEMU 网关通信，任何发往宿主机的数据都会被 QEMU 丢弃。

通常，QEMU User Networking 可以接收许多参数，包括：

* 宿主/来宾端口转发的信息（必须提供，以创建宿主与来宾之间的通信通道）。
* 要使用的网络信息（当不希望使用默认的 ``10.0.2.X`` 网络时很有用）。
* 指示 QEMU 在用户指定的 IP 地址上启动 DHCP 服务器。
* ID 及其他信息。

由于这些信息会随具体使用场景而变化，很难给出适用于所有情况的默认值。
因此，Zephyr 的实现将这部分留给用户，期望用户根据需求提供参数。
为此，提供了一个可由用户填写的 Kconfig 字符串：

.. code-block:: cfg

   CONFIG_NET_QEMU_USER_EXTRA_ARGS="net=192.168.0.0/24,hostfwd=tcp::8080-:8080"

该选项会按原样附加到 QEMU 命令行。因此该命令行的任何问题只会由 QEMU 报告。
上述示例将：

* 让 QEMU 使用 ``192.168.0.0/24`` 网络而非默认网络。
* 启用端口转发：将宿主机 8080 端口收到的 TCP 数据转发到来宾 8080 端口，反之亦然。

限制
*************

如果除在来宾中访问网页之外没有其他特定网络需求，User Networking（slirp）是一个不错的选择。
但它也有多项限制：

* 开销较大，性能较差。
* 宿主或外部网络无法直接访问来宾。
* 通常 ICMP 流量不可用（无法在来宾中使用 ping）。
* 由于端口映射需要在启动 QEMU 前定义，使用动态端口的客户端无法与外部网络通信。
* SLIRP 实现存在一个会过滤来宾所有 IPv6 报文的缺陷，详见 https://bugs.launchpad.net/qemu/+bug/1724590 ，因此在 User Networking 下 IPv6 无法工作。
