.. _networking_with_qemu:

使用 QEMU 进行网络通信
####################

.. contents::
    :local:
    :depth: 2

本页介绍如何在（Linux）主机与运行在 QEMU 虚拟机中的 Zephyr 应用之间建立虚拟网络（适用于 Zephyr 的 qemu_x86、qemu_cortex_m3 等目标）。某些虚拟 ARM 开发板（例如 qemu_cortex_a53）仅支持一个 UART，此时更推荐使用 QEMU 以太网，详见 :ref:`networking_with_eth_qemu`。

本示例在 QEMU 中运行 Zephyr 源码中的 :zephyr:code-sample:`sockets-echo-server` 示例。QEMU 实例通过串口与 Linux 主机相连，使用 SLIP 在 Zephyr 应用与 Linux 之间传输数据（通过一系列虚拟连接）。

前置条件
*************

在 Linux 主机上获取 Zephyr 的 `net-tools`_ 项目。它通常随 Zephyr 标准安装位于 ``tools/net-tools`` 目录，或从其独立的 Git 仓库单独克隆并构建：

.. code-block:: console

   sudo apt install -y socat libpcap-dev
   git clone https://github.com/zephyrproject-rtos/net-tools
   cd net-tools
   make

.. note::

   如果出现与 AX_CHECK_COMPILE_FLAG 相关的错误，请在 Debian/Ubuntu 上安装 ``autoconf-archive`` 包。

基础设置
***********

接下来的步骤至少需要 4 个终端窗口：

* 终端 #1：常用的 Zephyr 开发终端，已完成环境初始化。
* 终端 #2、#3、#4：当前目录为 net-tools（``cd net-tools``）。

步骤 1 - 创建辅助 socket
=============================

在使用网络仿真的 QEMU 启动前，需要先创建一个用于仿真的 Unix socket。

在终端 #2 执行：

.. code-block:: console

   ./loop-socat.sh

步骤 2 - 启动 TAP 设备路由守护进程
========================================

在终端 #3 执行：


.. code-block:: console

   sudo ./loop-slip-tap.sh

对于需要 DNS 的应用，此时可能需要重启主机的 DNS 服务，详见 :ref:`networking_internet`。

步骤 3 - 在 QEMU 中启动应用
==========================

构建并启动 ``echo_server`` 示例应用。

在终端 #1 执行：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: qemu_x86
   :goals: run
   :compact:

如果 QEMU 报错提示 unix:/tmp/slip.sock，则说明你漏掉了上面的步骤 1。

步骤 4 - 在主机上运行工具
=========================

现在在终端 #4，你可以运行各种工具与 QEMU 中运行的应用进行通信。

可以先尝试 ping：

.. code-block:: console

   ping 192.0.2.1
   ping6 2001:db8::1

也可以使用 netcat（“nc”）通过 UDP 进行连接：

.. code-block:: console

   echo foobar | nc -6 -u 2001:db8::1 4242
   foobar

.. code-block:: console

   echo foobar | nc -u 192.0.2.1 4242
   foobar

如果 echo_server 以支持 TCP 的方式编译（现在示例中默认启用，即 CONFIG_NET_TCP=y）：

.. code-block:: console

   echo foobar | nc -6 -q2 2001:db8::1 4242
   foobar

.. note::

   使用 Ctrl+C 退出。

也可以使用 telnet 命令实现上述功能。

步骤 5 - 停止相关守护进程
================================

完成基于 QEMU 的网络测试后，建议停止前面步骤中启动的所有守护程序或辅助进程，
以避免可能的网络或路由问题（例如本地网络接口的地址冲突）。
例如：当你从 QEMU 测试切换到真实硬件测试，或将主机恢复为正常的 Wi‑Fi 使用时。

要停止守护进程，在对应的终端窗口按 Ctrl+C（需要同时停止 ``loop-slip-tap.sh`` 和 ``loop-socat.sh``）。

按 :kbd:`CTRL+A` :kbd:`x` 退出 QEMU。

.. _networking_internet:

在主机上设置 Zephyr 与 NAT/伪装以访问互联网
*****************************************************************

要让 Zephyr 应用访问互联网，主机上可能需要进行一些额外配置。
这些配置对运行在 QEMU 里的应用和运行在真实硬件上的应用都适用（假设开发板连接在开发主机上）。
如果开发板连接在独立路由器上，则通常不需要这些配置。

对于使用 IPv4 访问互联网的 Zephyr 应用，应通过 DHCP 或手动配置网关。
若应用启用“Settings”功能（使能 :kconfig:option:`CONFIG_NET_CONFIG_SETTINGS`），
可设置 :kconfig:option:`CONFIG_NET_CONFIG_MY_IPV4_GW` 为网关 IP；
若未使用“Settings”，可在运行时调用 :c:func:`net_if_ipv4_set_gw` 设置网关。
例如：``CONFIG_NET_CONFIG_MY_IPV4_GW="192.0.2.2"``

要让运行在 QEMU 中的自定义应用访问互联网，需要为 QEMU 的源地址设置 NAT（伪装）。
假设使用的地址为 ``192.0.2.1``，Zephyr 网络接口为 ``zeth``，以 root 身份运行如下命令：

.. code-block:: console

   iptables -t nat -A POSTROUTING -j MASQUERADE -s 192.0.2.1/24
   iptables -I FORWARD 1 -i zeth -j ACCEPT
   iptables -I FORWARD 1 -o zeth -m state --state RELATED,ESTABLISHED -j ACCEPT

此外，需要在主机上启用 IPv4 转发，并检查其他防火墙（iptables）规则不会干扰伪装。
启用 IPv4 转发可用（root 身份）执行：

.. code-block:: console

   sysctl -w net.ipv4.ip_forward=1

有些应用还需要 DNS 服务器。许多 Zephyr 提供的示例默认假设主机上可用 DNS 服务器
（IP 为 ``192.0.2.2``），在现代 Linux 发行版上通常至少运行一个 DNS 代理。
在 QEMU 场景下，可能需要重启主机的 DNS，使其能在新创建的 TAP 接口上提供服务。
例如在基于 Debian 的系统上：

.. code-block:: console

   service dnsmasq restart

不依赖主机 DNS 的替代方式是使用网络中的公共 DNS，例如 ``8.8.8.8``。
可以通过 :kconfig:option:`CONFIG_DNS_SERVER1` 进行配置。


两台 QEMU 虚拟机之间的网络连接
***************************************

与前面描述的“虚拟机到主机”设置不同，“虚拟机到虚拟机”的设置是自动完成的。
对于支持该模式的示例应用（如 echo_server 与 echo_client），需要两个用于 Zephyr 开发的终端窗口。

Terminal #1:
============

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: qemu_x86
   :goals: build
   :build-args: server
   :compact:

这将启动 QEMU，并等待来自客户端 QEMU 的连接。

Terminal #2:
============

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_client
   :host-os: unix
   :board: qemu_x86
   :goals: build
   :build-args: client
   :compact:

这将启动第二个 QEMU 实例，你应能在两个实例中看到收发数据的日志。

运行同一示例的多个 QEMU 虚拟机
********************************************

如果需要运行同一 Zephyr 示例应用的多个实例，且这些实例无需互相通信，
可以使用 ``QEMU_INSTANCE`` 参数。

为每个需要的实例手动启动 ``socat`` 和 ``tunslip6``（而不是使用 ``loop-xxx.sh`` 脚本）。
以下命令供参考，请将 MAIN 或 OTHER 替换为你的实例名。

Terminal #1:
============

.. code-block:: console

   socat PTY,link=/tmp/slip.devMAIN UNIX-LISTEN:/tmp/slip.sockMAIN &
   sudo $ZEPHYR_BASE/../tools/net-tools/tunslip6 -t tapMAIN -T -s /tmp/slip.devMAIN 2001:db8::1/64 &
   # Now run Zephyr
   make -Cbuild run QEMU_INSTANCE=MAIN

Terminal #2:
============

.. code-block:: console

   socat PTY,link=/tmp/slip.devOTHER UNIX-LISTEN:/tmp/slip.sockOTHER &
   sudo $ZEPHYR_BASE/../tools/net-tools/tunslip6 -t tapOTHER -T -s /tmp/slip.devOTHER 2001:db8::1/64 &
   make -Cbuild run QEMU_INSTANCE=OTHER

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools
