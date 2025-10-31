.. _network_monitoring:

监控网络流量
#######################

.. contents::
    :local:
    :depth: 2

在调试连接问题或为 Zephyr 开发新协议支持时，监控网络流量非常有用。
本页介绍如何搭建网络流量捕获路径，使用户可以在远程主机上使用 Wireshark 等工具查看 Zephyr 设备发送或接收的网络数据包。

另请参考 Zephyr 源码中的 :zephyr:code-sample:`net-capture` 示例，了解需要启用的配置选项。

主机配置
******************

本节说明如何在 Linux 主机上捕获 Zephyr 的收发网络流量。
类似的方法也适用于其他操作系统。

在 Linux 主机上获取 Zephyr 的 `net-tools`_ 项目。它通常随 Zephyr 标准安装位于 ``tools/net-tools`` 目录，
也可以从其独立的 Git 仓库单独克隆：

.. code-block:: console

   git clone https://github.com/zephyrproject-rtos/net-tools

``net-tools`` 项目提供了一个配置文件用于创建 IP‑to‑IP 隧道接口，以便我们将监控数据从 Zephyr 传输到主机。

在终端 #1 执行：

.. code-block:: console

   ./net-setup.sh -c zeth-tunnel.conf

该脚本会创建如下 IPIP 隧道接口：

.. csv-table::
   :header: "Interface name", "Description"
   :widths: auto

   "``zeth-ip6ip``", "IPv6-over-IPv4 tunnel"
   "``zeth-ipip``", "IPv4-over-IPv4 tunnel"
   "``zeth-ipip6``", "IPv4-over-IPv6 tunnel"
   "``zeth-ip6ip6``", "IPv6-over-IPv6 tunnel"

Zephyr 会将捕获的网络数据包发送至其中一个接口。
具体使用哪个接口取决于捕获配置。
随后可使用 Wireshark 监控对应的网络接口。

创建好隧道接口后，可以使用 ``net-tools`` 项目的 ``net-capture.py`` 脚本打印或保存捕获的网络报文。
``net-capture.py`` 提供了一个 UDP 监听器，既可以在屏幕上打印捕获的数据，也可以选择保存为 pcap 文件。

.. code-block:: console

   $ ./net-capture.py -i zeth-ip6ip -w capture.pcap
   [20210408Z14:33:08.959589] Ether / IP / ICMP 192.0.2.1 > 192.0.2.2 echo-request 0 / Raw
   [20210408Z14:33:08.976178] Ether / IP / ICMP 192.0.2.2 > 192.0.2.1 echo-reply 0 / Raw
   [20210408Z14:33:16.176303] Ether / IPv6 / ICMPv6 Echo Request (id: 0x9feb seq: 0x0)
   [20210408Z14:33:16.195326] Ether / IPv6 / ICMPv6 Echo Reply (id: 0x9feb seq: 0x0)
   [20210408Z14:33:21.194979] Ether / IPv6 / ICMPv6ND_NS / ICMPv6 Neighbor Discovery Option - Source Link-Layer Address 02:00:5e:00:53:3b
   [20210408Z14:33:21.217528] Ether / IPv6 / ICMPv6ND_NA / ICMPv6 Neighbor Discovery Option - Destination Link-Layer Address 00:00:5e:00:53:ff
   [20210408Z14:34:10.245408] Ether / IPv6 / UDP 2001:db8::2:47319 > 2001:db8::1:4242 / Raw
   [20210408Z14:34:10.266542] Ether / IPv6 / UDP 2001:db8::1:4242 > 2001:db8::2:47319 / Raw

``net-capture.py`` 支持如下命令行选项：

.. code-block:: console

   Listen captured network data from Zephyr and save it optionally to pcap file.
   ./net-capture.py \
	-i | --interface <network interface>
		Listen this interface for the data
	[-p | --port <UDP port>]
		UDP port (default is 4242) where the capture data is received
	[-q | --quiet]
		Do not print packet information
	[-t | --type <L2 type of the data>]
		Scapy L2 type name of the UDP payload, default is Ether
	[-w | --write <pcap file name>]
		Write the received data to file in PCAP format

除了使用 ``net-capture.py`` 脚本之外，也可以用 ``netcat`` 提供一个 UDP 监听器，
以避免主机向 Zephyr 发送端口不可达的报文：

.. code-block:: console

   nc -l -u 2001:db8:200::2 4242 > /dev/null

上述 IP 地址是内层隧道的端点，可根据 Zephyr 的配置进行调整。
Zephyr 会将包含已捕获网络报文的 UDP 数据发送到配置的 IP 隧道，因此需要像这样在主机侧终止网络连接。

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools

Zephyr 配置
********************

本示例使用 ``native_sim`` 开发板。也可以使用任何支持网络的其他开发板。

在终端 #3 执行：

.. zephyr-app-commands::
   :zephyr-app: samples/net/capture
   :host-os: unix
   :board: native_sim
   :gen-args: -DCONFIG_UART_NATIVE_PTY_AUTOATTACH_DEFAULT_CMD=\""gnome-terminal -- screen %s"\"
   :goals: build
   :compact:

要查看 Zephyr 控制台和 shell，可如下启动 Zephyr 实例：

.. code-block:: console

   build/zephyr/zephyr.exe -attach_uart

也可以使用其他任意应用，只需确保启用了合适的配置选项（参见 ``samples/net/capture/prj.conf`` 示例）。

如有需要，网络捕获可以实现自动配置，但目前 ``capture`` 示例未自动完成该操作。
用户需要使用 ``net-shell`` 来设置并启用监控。

首先需要完成网络数据包监控的设置。``net-shell`` 提供了 ``net capture setup`` 命令，语法如下：

.. code-block:: console

   net capture setup <remote-ip-addr> <local-ip-addr> <peer-ip-addr>
        <remote> is the (outer) endpoint IP address
        <local> is the (inner) local IP address
        <peer> is the (inner) peer IP address
        Local and Peer IP addresses can have UDP port number in them (optional)
        like 198.0.51.2:9000 or [2001:db8:100::2]:4242

在 Zephyr 控制台中执行：

.. code-block:: console

   net capture setup 192.0.2.2 2001:db8:200::1 2001:db8:200::2

该命令会创建隧道接口。其中 ``192.0.2.2`` 是隧道在远端终止的主机地址，该地址用于选择隧道接口所附着的本地网络接口。
``2001:db8:200::1`` 指定隧道的本地 IP 地址，``2001:db8:200::2`` 是接收捕获网络报文的对端 IP 地址。
UDP 报文的端口号也可在设置命令中给出，例如用于 IPv6‑over‑IPv4 隧道：

.. code-block:: console

   net capture setup 192.0.2.2 [2001:db8:200::1]:9999 [2001:db8:200::2]:9998

IPv4‑over‑IPv4 隧道示例如下：

.. code-block:: console

   net capture setup 192.0.2.2 198.51.100.1:9999 198.51.100.2:9998

如果省略端口号，则默认使用 ``4242`` UDP 端口。

可通过以下命令查看当前监控配置：

.. code-block:: console

   uart:~$ net capture
   Network packet capture disabled
                   Capture  Tunnel
   Device          iface    iface   Local                  Peer
   NET_CAPTURE0    -        1      [2001:db8:200::1]:4242  [2001:db8:200::2]:4242

上面将打印当前配置。由于此时仍未启用监控，``Capture iface`` 尚未设置。

接着按如下方式启用网络数据包监控：

.. code-block:: console

   net capture enable 2

这里的 ``2`` 指定我们希望捕获哪个网络接口的流量。在本示例中，``2`` 是 ``native_sim`` 的以太网接口。
请注意，本示例中我们把网络流量发送到与监控相同的接口。监控系统会避免再次捕获已被捕获的流量，以防止递归。
可以使用 ``net iface`` 查看可用的网络接口。
注意不能从隧道接口捕获流量，否则会导致递归环路。
如有需要，捕获到的网络流量也可以发送到其他网络接口。只需在 ``net capture setup`` 中正确设置 ``<remote-ip-addr>``，使 IP 隧道附着在期望的网络接口上。
可以再次通过以下命令检查捕获状态：

.. code-block:: console

   uart:~$ net capture
   Network packet capture enabled
                   Capture  Tunnel
   Device          iface    iface   Local                  Peer
   NET_CAPTURE0    2        1      [2001:db8:200::1]:4242  [2001:db8:200::2]:4242

启用监控后，系统会将捕获到的网络报文（无论是接收还是发送）发送至隧道接口以便进一步处理。

可按如下方式禁用监控：

.. code-block:: console

   net capture disable

这将关闭当前运行的监控。可按如下方式清除监控配置：

.. code-block:: console

   net capture cleanup

配置监控并非必须通过 ``net-shell``。如有需要，应用也可以直接调用 :ref:`network capture API <net_capture_interface>` 提供的接口。

Wireshark 配置
***********************

可以使用 `Wireshark <https://www.wireshark.org/>`_ 以更直观的方式监控捕获到的网络流量。

可以监控隧道接口或 ``zeth`` 接口。
若要在 UDP 报文内看到实际捕获的数据，请参考 `Wireshark decapsulate UDP`_ 的说明。

.. _Wireshark decapsulate UDP:
   https://osqa-ask.wireshark.org/questions/28138/decoding-ethernet-encapsulated-in-tcp-or-udp/
