.. _networking_with_multiple_instances:

Networking with multiple Zephyr instances
#########################################

.. contents::
    :local:
    :depth: 2

本页介绍如何在多个 Zephyr 实例之间建立虚拟网络。Zephyr 实例可以运行在 QEMU 中，
也可以是 native_sim 开发板进程。Linux 主机可用于在这些系统之间转发网络流量。

前置条件
*************

在 Linux 主机上获取 Zephyr 的 `net-tools`_ 项目。它通常随 Zephyr 标准安装位于 ``tools/net-tools`` 目录，
也可以从其独立的 Git 仓库单独克隆：

.. code-block:: console

   git clone https://github.com/zephyrproject-rtos/net-tools

基础设置
***********

接下来的步骤建议同时打开 5 个终端窗口：

* 终端 #1 与 #2：当前目录为 net-tools（``cd net-tools``）
* 终端 #3：在 Linux 主机上进行网桥配置
* 终端 #4 与 #5：日常 Zephyr 开发环境（已完成环境初始化）

由于配置 Zephyr 网络的方式不止一种，下面的示例选用带 ``e1000`` 网卡的 ``qemu_x86`` 开发板
以及 native_sim 开发板以简化说明。你也可以按需选择其他 QEMU 开发板与驱动，详见
:ref:`networking_with_eth_qemu`。此外，也可以使用两个或多个 native_sim 实例并将它们互联。


步骤 1 - 创建配置文件
===================================

在启动具备网络功能的 QEMU 之前，需要先在主机为每个 Zephyr 实例创建网络接口。
默认的接口创建方式仅适用于“单个 Zephyr 实例连接 Linux 主机”的情形，此处不适用。

针对 Zephyr 实例 #1，在 ``net-tools`` 项目目录（或任意合适目录）创建 ``zephyr1.conf`` 文件。

.. code-block:: console

   # Configuration file for setting IP addresses for a network interface.
   INTERFACE="$1"
   HWADDR="00:00:5e:00:53:11"
   IPV6_ADDR_1="2001:db8:100::2"
   IPV6_ROUTE_1="2001:db8:100::/64"
   IPV4_ADDR_1="198.51.100.2/24"
   IPV4_ROUTE_1="198.51.100.0/24"
   ip link set dev $INTERFACE up
   ip link set dev $INTERFACE address $HWADDR
   ip -6 address add $IPV6_ADDR_1 dev $INTERFACE nodad
   ip -6 route add $IPV6_ROUTE_1 dev $INTERFACE
   ip address add $IPV4_ADDR_1 dev $INTERFACE
   ip route add $IPV4_ROUTE_1 dev $INTERFACE > /dev/null 2>&1

针对 Zephyr 实例 #2，在 ``net-tools`` 项目目录（或任意合适目录）创建 ``zephyr2.conf`` 文件。

.. code-block:: console

   # Configuration file for setting IP addresses for a network interface.
   INTERFACE="$1"
   HWADDR="00:00:5e:00:53:22"
   IPV6_ADDR_1="2001:db8:200::2"
   IPV6_ROUTE_1="2001:db8:200::/64"
   IPV4_ADDR_1="203.0.113.2/24"
   IPV4_ROUTE_1="203.0.113.0/24"
   ip link set dev $INTERFACE up
   ip link set dev $INTERFACE address $HWADDR
   ip -6 address add $IPV6_ADDR_1 dev $INTERFACE nodad
   ip -6 route add $IPV6_ROUTE_1 dev $INTERFACE
   ip address add $IPV4_ADDR_1 dev $INTERFACE
   ip route add $IPV4_ROUTE_1 dev $INTERFACE > /dev/null 2>&1


步骤 2 - 创建以太网接口
===================================

以下 ``net-setup.sh`` 命令需在 net-tools 目录下执行（``cd net-tools``）。

在终端 #1 执行：

.. code-block:: console

   ./net-setup.sh -c zephyr1.conf -i zeth.1

在终端 #2 执行：

.. code-block:: console

   ./net-setup.sh -c zephyr2.conf -i zeth.2


步骤 3 - 配置网络桥接
===============================

在终端 #3 执行：

.. code-block:: console

   sudo brctl addbr zeth-br
   sudo brctl addif zeth-br zeth.1
   sudo brctl addif zeth-br zeth.2
   sudo ifconfig zeth-br up


步骤 4 - 启动 Zephyr 实例
===============================

本示例分别启动 :zephyr:code-sample:`sockets-echo-server` 与
:zephyr:code-sample:`sockets-echo-client` 示例应用。你也可以按需替换为其他应用。

在终端 #4，若使用 QEMU，执行：

.. code-block:: console

   west build -d build/server -b qemu_x86 -t run \
      samples/net/sockets/echo_server -- \
      -DEXTRA_CONF_FILE=overlay-e1000.conf \
      -DCONFIG_NET_CONFIG_MY_IPV4_ADDR=\"198.51.100.1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV4_ADDR=\"203.0.113.1\" \
      -DCONFIG_NET_CONFIG_MY_IPV6_ADDR=\"2001:db8:100::1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV6_ADDR=\"2001:db8:200::1\" \
      -DCONFIG_NET_CONFIG_MY_IPV4_GW=\"203.0.113.1\" \
      -DCONFIG_ETH_QEMU_IFACE_NAME=\"zeth.1\" \
      -DCONFIG_ETH_QEMU_EXTRA_ARGS=\"mac=00:00:5e:00:53:01\"

或若使用 native_sim 开发板，执行：

.. code-block:: console

   west build -d build/server -b native_sim -t run \
      samples/net/sockets/echo_server -- \
      -DCONFIG_NET_CONFIG_MY_IPV4_ADDR=\"198.51.100.1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV4_ADDR=\"203.0.113.1\" \
      -DCONFIG_NET_CONFIG_MY_IPV6_ADDR=\"2001:db8:100::1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV6_ADDR=\"2001:db8:200::1\" \
      -DCONFIG_NET_CONFIG_MY_IPV4_GW=\"203.0.113.1\" \
      -DCONFIG_ETH_NATIVE_TAP_DRV_NAME=\"zeth.1\" \
      -DCONFIG_ETH_NATIVE_TAP_MAC_ADDR=\"00:00:5e:00:53:01\" \
      -DCONFIG_ETH_NATIVE_TAP_RANDOM_MAC=n


在终端 #5，若使用 QEMU，执行：

.. code-block:: console

   west build -d build/client -b qemu_x86 -t run \
      samples/net/sockets/echo_client -- \
      -DEXTRA_CONF_FILE=overlay-e1000.conf \
      -DCONFIG_NET_CONFIG_MY_IPV4_ADDR=\"203.0.113.1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV4_ADDR=\"198.51.100.1\" \
      -DCONFIG_NET_CONFIG_MY_IPV6_ADDR=\"2001:db8:200::1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV6_ADDR=\"2001:db8:100::1\" \
      -DCONFIG_NET_CONFIG_MY_IPV4_GW=\"198.51.100.1\" \
      -DCONFIG_ETH_QEMU_IFACE_NAME=\"zeth.2\" \
      -DCONFIG_ETH_QEMU_EXTRA_ARGS=\"mac=00:00:5e:00:53:02\"

或若使用 native_sim 开发板，执行：

.. code-block:: console

   west build -d build/client -b native_sim -t run \
      samples/net/sockets/echo_client -- \
      -DCONFIG_NET_CONFIG_MY_IPV4_ADDR=\"203.0.113.1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV4_ADDR=\"198.51.100.1\" \
      -DCONFIG_NET_CONFIG_MY_IPV6_ADDR=\"2001:db8:200::1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV6_ADDR=\"2001:db8:100::1\" \
      -DCONFIG_NET_CONFIG_MY_IPV4_GW=\"198.51.100.1\" \
      -DCONFIG_ETH_NATIVE_TAP_DRV_NAME=\"zeth.2\" \
      -DCONFIG_ETH_NATIVE_TAP_MAC_ADDR=\"00:00:5e:00:53:02\" \
      -DCONFIG_ETH_NATIVE_TAP_RANDOM_MAC=n


如果主机上启用了防火墙，请放通 ``zeth.1``、``zeth.2`` 与 ``zeth-br`` 接口之间的流量。

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools
