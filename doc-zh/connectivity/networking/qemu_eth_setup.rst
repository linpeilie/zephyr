.. _networking_with_eth_qemu:

使用 QEMU 以太网进行网络通信
#############################

.. contents::
    :local:
    :depth: 2

本页介绍如何在（Linux）主机与运行在 QEMU 中的 Zephyr 应用之间建立虚拟网络。

本示例在 QEMU 中运行 Zephyr 源码中的 :zephyr:code-sample:`sockets-echo-server` 示例。
Zephyr 实例通过一个 tuntap 设备连接到 Linux 主机，该设备在 Linux 中被建模为以太网网络接口。

前置条件
*************

在 Linux 主机上获取 Zephyr 的 `net-tools`_ 项目。它通常随 Zephyr 标准安装位于 ``tools/net-tools`` 目录，
也可以从其独立的 Git 仓库单独克隆：

.. code-block:: console

   git clone https://github.com/zephyrproject-rtos/net-tools


基础设置
***********

接下来的步骤建议同时打开两个终端窗口：

* 终端 #1：当前目录为 net-tools（``cd net-tools``）
* 终端 #2：常用的 Zephyr 开发终端，已完成环境初始化。

配置 Zephyr 实例时，需要为 QEMU 连接选择正确的以太网驱动：

* 对于 ``qemu_x86``：选择 ``Intel(R) PRO/1000 Gigabit Ethernet driver``（在 Zephyr 源码中驱动名为 ``e1000``）。
* 对于 ``qemu_cortex_m3``：选择 ``TI Stellaris MCU family ethernet driver``（驱动名为 ``stellaris``）。
* 对于 ``mps2_an385``：选择 ``SMSC911x/9220 Ethernet driver``（驱动名为 ``smsc911x``）。
* 对于 ``qemu_cortex_a53``：默认已选择 ``Intel(R) PRO/1000 Gigabit Ethernet driver``。
* 另外，:zephyr:code-sample:`sockets-echo-server` 示例为 ``qemu_x86_64`` 的 VIRTIO 网卡提供了覆盖文件。

步骤 1 - 创建以太网接口
==================================

在启动具备网络功能的 QEMU 之前，需要先在主机上创建一个网络接口。

在终端 #1 执行：

.. code-block:: console

   ./net-setup.sh

你可以调整 ``net-setup.sh`` 脚本的行为。运行如下命令查看可用选项：

.. code-block:: console

   ./net-setup.sh --help


步骤 2 - 在 QEMU 开发板中启动应用
================================

构建并启动 :zephyr:code-sample:`sockets-echo-server` 示例应用。
此处以 qemu_x86 开发板为例。

在终端 #2 执行：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: qemu_x86
   :gen-args: -DEXTRA_CONF_FILE=overlay-e1000.conf
   :goals: run
   :compact:

或者，如果打算在 qemu_x86_64 上使用 VIRTIO 网卡：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: qemu_x86_64
   :gen-args: -DDTC_OVERLAY_FILE=virtnet.overlay -DEXTRA_CONF_FILE=overlay-virtnet.conf
   :goals: run
   :compact:

按 :kbd:`CTRL+A` :kbd:`x` 退出 QEMU。

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools
