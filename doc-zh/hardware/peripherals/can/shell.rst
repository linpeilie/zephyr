.. _can_shell:

CAN Shell
#########

.. contents::
    :local:
    :depth: 1

概述 (Overview)
****************

CAN shell 为 :ref:`shell <shell_api>` 模块提供了一个带有一组子命令的 ``can`` 命令。
它允许通过交互式界面测试和探索 :ref:`can_api` 驱动程序 API，
而无需编写专用应用程序。CAN shell 也可以在现有应用程序中启用，
以帮助交互式调试 CAN 问题。

CAN shell 提供对大多数 CAN 控制器功能的访问，
包括检查、配置、发送和接收 CAN 帧以及总线恢复。

为了启用 CAN shell，必须启用以下 :ref:`Kconfig <kconfig>` 选项:

* :kconfig:option:`CONFIG_SHELL`
* :kconfig:option:`CONFIG_CAN`
* :kconfig:option:`CONFIG_CAN_SHELL`

以下 :ref:`Kconfig <kconfig>` 选项启用 ``can`` 命令的其他子命令和功能:

* :kconfig:option:`CONFIG_CAN_FD_MODE` 启用 CAN FD 特定的子命令
  (例如用于设置 CAN FD 数据阶段的时序)。
* :kconfig:option:`CONFIG_CAN_RX_TIMESTAMP` 启用接收到的 CAN 帧的时间戳打印。
* :kconfig:option:`CONFIG_CAN_STATS` 启用在 ``can show`` 子命令中打印 CAN 控制器的各种统计信息。
  这依赖于同时启用 :kconfig:option:`CONFIG_STATS`。
* :kconfig:option:`CONFIG_CAN_MANUAL_RECOVERY_MODE` 启用 ``can recover`` 子命令。

例如，为 :zephyr:board:`frdm_k64f` 构建 :zephyr:code-sample:`hello_world` 示例，
并启用 CAN shell 和 CAN 统计信息:

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :board: frdm_k64f
   :gen-args: -DCONFIG_SHELL=y -DCONFIG_CAN=y -DCONFIG_CAN_SHELL=y -DCONFIG_STATS=y -DCONFIG_CAN_STATS=y
   :goals: build

有关如何连接和与 shell 交互的一般说明，请参阅 :ref:`shell <shell_api>` 文档。
CAN shell 带有内置帮助(除非禁用 :kconfig:option:`CONFIG_SHELL_HELP`)。
可以通过向 ``can`` 命令或其任何子命令传递 ``-h`` 或 ``--help`` 来打印内置帮助消息。
所有子命令也支持其参数的制表符补全。

.. tip::
   所有 CAN shell 子命令都将 CAN 控制器的名称作为第一个参数，
   这也支持制表符补全。当启用 :kconfig:option:`CONFIG_DEVICE_SHELL` 时，
   可以使用 ``device list`` shell 命令获取所有可用设备的列表。
   下面的示例都使用设备名称 ``can@0``。

检查 (Inspection)
******************

可以使用 ``can show`` 子命令检查给定 CAN 控制器的属性，如下所示。
属性包括核心 CAN 时钟速率、支持的最大位速率、支持的 RX 过滤器数量、
能力、当前模式、当前状态、错误计数器、时序限制等:

.. code-block:: console

   uart:~$ can show can@0
   core clock:      144000000 Hz
   max bitrate:     5000000 bps
   max std filters: 15
   max ext filters: 15
   capabilities:    normal loopback listen-only fd
   mode:            normal
   state:           stopped
   rx errors:       0
   tx errors:       0
   timing:          sjw 1..128, prop_seg 0..0, phase_seg1 2..256, phase_seg2 2..128, prescaler 1..512
   timing data:     sjw 1..16, prop_seg 0..0, phase_seg1 1..32, phase_seg2 1..16, prescaler 1..32
   transceiver:     passive/none
   statistics:
     bit errors:    0
       bit0 errors: 0
       bit1 errors: 0
     stuff errors:  0
     crc errors:    0
     form errors:   0
     ack errors:    0
     rx overruns:   0

.. note::
   仅当启用 :kconfig:option:`CONFIG_CAN_STATS` 时才会打印统计信息。

配置 (Configuration)
*********************

CAN shell 允许配置 CAN 控制器模式和时序，以及启动和停止 CAN 帧的处理。

.. note::
   只有在 CAN 控制器停止时才能更改 CAN 控制器模式和时序，
   这是启动时的初始设置。初始 CAN 控制器模式设置为 ``normal``，
   初始时序根据 ``bitrate``、``sample-point``、``bitrate-data`` 和
   ``sample-point-data`` :ref:`devicetree` 属性设置。

时序 (Timing)
==============

可以使用 ``can bitrate`` 子命令配置经典 CAN 位速率/CAN FD 仲裁阶段位速率，如下所示。
位速率以每秒比特数指定。

.. code-block:: console

   uart:~$ can bitrate can@0 125000
   setting bitrate to 125000 bps

如果启用了 :kconfig:option:`CONFIG_CAN_FD_MODE`，
可以使用 ``can dbitrate`` 子命令配置数据阶段位速率，如下所示。
位速率以每秒比特数指定。

.. code-block:: console

   uart:~$ can dbitrate can@0 1000000
   setting data bitrate to 1000000 bps

这两个子命令都允许将可选的采样点(以千分之几为单位)和
重新同步跳转宽度(SJW，以时间量子为单位)指定为位置参数。
有关更多详细信息，请参阅子命令的交互式帮助。

也可以使用 ``can timing`` 和 ``can dtiming`` 子命令配置原始位时序。
有关所需参数的详细信息，请参阅这些子命令的交互式帮助输出。

模式 (Mode)
============

CAN shell 允许使用 ``can mode`` 子命令设置 CAN 控制器的模式。
下面显示了启用环回模式的示例。

.. code-block:: console

   uart:~$ can mode can@0 loopback
   setting mode 0x00000001

该子命令接受在同一命令行上给出的多个模式
(例如 ``can mode can@0 fd loopback`` 用于设置 CAN FD 和环回模式)。
供应商特定的模式可以用十六进制指定。

启动和停止 (Starting and Stopping)
====================================

根据需要配置时序和模式后，可以使用 ``can start`` 子命令启动 CAN 控制器，如下所示。
这将启用 CAN 帧的接收和传输。

.. code-block:: console

   uart:~$ can start can@0
   starting can@0

在重新配置时序或模式之前，需要使用 ``can stop`` 子命令停止 CAN 控制器，如下所示:

.. code-block:: console

   uart:~$ can stop can@0
   stopping can@0

接收 (Receiving)
*****************

为了接收 CAN 帧，需要配置一个或多个 CAN RX 过滤器。
使用 ``can filter add`` 子命令添加 CAN RX 过滤器，如下所示。
该子命令接受十六进制格式的 CAN ID，以及可选的 CAN ID 掩码(也是十六进制格式)，
用于设置要匹配的 CAN ID 中的位。有关支持的参数的更多详细信息，
请参阅此子命令的交互式帮助输出。

.. code-block:: console

   uart:~$ can filter add can@0 010
   adding filter with standard (11-bit) CAN ID 0x010, CAN ID mask 0x7ff, data frames 1, RTR frames 0, CAN FD frames 0
   filter ID: 0

返回的过滤器 ID(上例中为 0)将在删除 CAN RX 过滤器时使用。

匹配添加的过滤器的接收到的 CAN 帧将打印到 shell。下面显示了几个示例:

.. code-block:: console

   # Dev Flags    ID   Size  Data bytes
   can0  --       010   [8]  01 02 03 04 05 06 07 08
   can0  B-       010  [08]  01 02 03 04 05 06 07 08
   can0  BP       010  [03]  01 aa bb
   can0  --  00000010   [0]
   can0  --       010   [1]  20
   can0  --       010   [8]  remote transmission request

列的含义如下:

* Dev

  * 接收帧的设备名称。

* Flags

  * ``B``: 帧设置了 CAN FD 波特率切换(BRS)标志。
  * ``P``: 帧设置了 CAN FD 错误状态指示器(ESI)标志。发送节点处于错误被动状态。
  * ``-``: 未设置标志。

* ID

  * ``010``: 十六进制格式的标准(11 位)CAN ID，此处为 10h。
  * ``00000010``: 十六进制格式的扩展(29 位)CAN ID，此处为 10h。

* Size

  * ``[8]``: 十进制格式的帧数据字节数，此处为具有 8 个数据字节的经典 CAN 帧。
  * ``[08]``: 十进制格式的帧数据字节数，此处为具有 8 个数据字节的 CAN FD 帧。

* Data bytes

  * ``01 02 03 04 05 06 07 08``: 十六进制格式的帧数据字节，此处为从 1 到 8 的数字。
  * ``remote transmission request``: 该帧是远程传输请求(RTR)帧，因此不携带数据字节。

.. tip::
   如果启用了 :kconfig:option:`CONFIG_CAN_RX_TIMESTAMP`，
   每行都将在前面加上来自 CAN 控制器中自由运行的时间戳计数器的时间戳。

可以使用 ``can filter remove`` 子命令再次删除配置的 CAN RX 过滤器，如下所示。
过滤器 ID 是 ``can filter add`` 子命令返回的 ID(下例中为 0)。

.. code-block:: console

   uart:~$ can filter remove can@0 0
   removing filter with ID 0

发送 (Sending)
***************

可以使用 ``can send`` 子命令将 CAN 帧排队等待传输，如下所示。
该子命令接受十六进制格式的 CAN ID，以及可选的多个数据字节(也以十六进制指定)。
有关支持的参数的更多详细信息，请参阅此子命令的交互式帮助输出。

.. code-block:: console

   uart:~$ can send can@0 010 1 2 3 4 5 6 7 8
   enqueuing CAN frame #2 with standard (11-bit) CAN ID 0x010, RTR 0, CAN FD 0, BRS 0, DLC 8
   CAN frame #2 successfully sent

总线恢复 (Bus Recovery)
************************

``can recover`` 子命令可用于启动从 CAN 总线关闭事件中的手动恢复，如下所示:

.. code-block:: console

   uart:~$ can recover can@0
   recovering, no timeout

该子命令接受以毫秒为单位的可选总线恢复超时。如果未指定超时，
该命令将无限期等待总线恢复成功。

.. note::
   ``recover`` 子命令仅在启用 :kconfig:option:`CONFIG_CAN_MANUAL_RECOVERY_MODE` 时可用。
