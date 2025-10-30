.. _flash-debug-host-tools:

烧录和调试主机工具
########################

本指南描述了您可以在主机工作站上运行的软件工具,用于烧录和调试 Zephyr 应用程序。

Zephyr 的 west 工具为所有这些工具的 ``flash``、``debug``、``debugserver`` 和 ``attach`` 命令提供内置支持,前提是您的板硬件支持它们,并且您的 Zephyr 板目录的 :file:`board.cmake` 文件正确声明了该支持。有关这些命令的更多信息,请参阅 :ref:`west-build-flash-debug`。

.. _runner_blackmagicprobe:

Black Magic Probe
*****************

Black Magic Probe (BMP) 是一个开源调试硬件,将 GDB 调试服务器功能集成到固件中。
不需要 GDB 服务器程序,因此没有等效于主机工具的程序。

有关更多详细信息,包括使用说明和支持的目标,请参阅 :ref:`black-magic-probe`。

.. _atmel_sam_ba_bootloader:
.. _runner_bossac:

SAM Boot Assistant (SAM-BA)
***************************

Atmel SAM Boot Assistant (Atmel SAM-BA) 允许从 USB 或 UART 主机进行系统内编程 (ISP),无需任何外部编程接口。Zephyr 允许用户使用 :ref:`west <west-flashing>` 开发和编程具有 SAM-BA 支持的板。Zephyr 支持带有/不带有 ROM 引导加载程序的设备以及 Arduino 和 Adafruit 的扩展。在 Zephyr SDK 0.12.0 中引入了完整支持。

烧录板的典型命令是:

.. code-block:: console

	west flash [ -r bossac ] [ -p /dev/ttyX ] [ --erase ]

.. note::

    默认情况下,使用 bossac 烧录仅会擦除包含烧录应用程序的闪存页,而不影响其他页。如果您希望在烧录时擦除目标的整个闪存,请在烧录时传递 ``--erase`` 参数。

设备的烧录配置:

.. tabs::

    .. tab:: 带有 ROM 引导加载程序

        这些设备不需要任何特殊配置。构建应用程序后,只需运行 ``west flash`` 即可烧录板。

    .. tab:: 不带 ROM 引导加载程序

        对于这些设备,用户应该:

        1. 定义闪存分区以容纳引导加载程序和应用程序映像;有关详细信息,请参阅 :ref:`flash_map_api`。
        2. 将 :kconfig:option:`CONFIG_USE_DT_CODE_PARTITION` Kconfig 选项设置为 ``y`` 的板 :file:`.defconfig` 文件,以指示构建系统使用这些分区进行代码重定位。
           此选项也可以在 ``prj.conf`` 或任何其他 Kconfig 片段中设置。
        3. 在设备上构建和烧录 SAM-BA 引导加载程序。

    .. tab:: 带有兼容的 SAM-BA 引导加载程序

        对于这些设备,用户应该:

        1. 定义闪存分区以容纳引导加载程序和应用程序映像;有关详细信息,请参阅 :ref:`flash_map_api`。
        2. 将 :kconfig:option:`CONFIG_BOOTLOADER_BOSSA` Kconfig 选项设置为 ``y`` 的板 :file:`.defconfig` 文件。这将
           自动选择 :kconfig:option:`CONFIG_USE_DT_CODE_PARTITION` Kconfig 选项,该选项指示构建系统使用这些分区进行代码
           重定位。板 :file:`.defconfig` 文件应该将
           :kconfig:option:`CONFIG_BOOTLOADER_BOSSA_ARDUINO`、
           :kconfig:option:`CONFIG_BOOTLOADER_BOSSA_ADAFRUIT_UF2` 或
           :kconfig:option:`CONFIG_BOOTLOADER_BOSSA_LEGACY` Kconfig 选项设置为 ``y``
           以选择正确的兼容 SAM-BA 引导加载程序模式。
           这些选项也可以在 ``prj.conf`` 或任何其他 Kconfig 片段中设置。
        3. 在设备上构建和烧录 SAM-BA 引导加载程序。

.. note::

    :kconfig:option:`CONFIG_BOOTLOADER_BOSSA_LEGACY` Kconfig 选项应作为最后的手段使用。首先尝试使用不带 ROM 引导加载程序的设备进行配置。


典型的闪存布局和配置
--------------------------------------

对于驻留在闪存上的引导加载程序,设备树分区布局是强制性的。对于具有 ROM 引导加载程序的设备,当应用程序使用存储或其他非应用程序分区时,它们是强制性的。在这种特殊情况下,应省略引导分区,code_partition 应从偏移量 0 开始。始终需要定义大小以避免重叠的分区。

不带 ROM 引导加载程序的设备的典型闪存布局是:

.. code-block:: devicetree

	/ {
		chosen {
			zephyr,code-partition = &code_partition;
		};
	};

	&flash0 {
		partitions {
			compatible = "fixed-partitions";
			#address-cells = <1>;
			#size-cells = <1>;

			boot_partition: partition@0 {
				label = "sam-ba";
				reg = <0x00000000 0x2000>;
				read-only;
			};

			code_partition: partition@2000 {
				label = "code";
				reg = <0x2000 0x3a000>;
				read-only;
			};

			/*
			* 最后 16 KiB 保留给应用程序。
			* 如果启用,存储分区将由 FCB/LittleFS/NVS 使用。
			*/
			storage_partition: partition@3c000 {
				label = "storage";
				reg = <0x0003c000 0x00004000>;
			};
		};
	};

带有 ROM 引导加载程序和存储分区的设备的典型闪存布局是:

.. code-block:: devicetree

	/ {
		chosen {
			zephyr,code-partition = &code_partition;
		};
	};

	&flash0 {
		partitions {
			compatible = "fixed-partitions";
			#address-cells = <1>;
			#size-cells = <1>;

			code_partition: partition@0 {
				label = "code";
				reg = <0x0 0xF0000>;
				read-only;
			};

			/*
			* 最后 64 KiB 保留给应用程序。
			* 如果启用,存储分区将由 FCB/LittleFS/NVS 使用。
			*/
			storage_partition: partition@F0000 {
				label = "storage";
				reg = <0x000F0000 0x00100000>;
			};
		};
	};


启用 SAM-BA 运行器
----------------------

为了指示 Zephyr west 工具使用 SAM-BA 引导加载程序,:file:`board.cmake` 文件必须有
``include(${ZEPHYR_BASE}/boards/common/bossac.board.cmake)`` 条目。请注意,
Zephyr 工具接受更多条目来定义多个运行器。默认情况下,使用 ``west flash`` 命令时将选择第一个。
通过传递运行器选项可以使用其余选项,例如 ``west flash -r bossac``。


可以在 :ref:`boards` 文档中找到更多实现细节。
作为快速参考,请参阅这四个板文档页面:

  - :zephyr:board:`sam4e_xpro` (ROM 引导加载程序)
  - :zephyr:board:`adafruit_feather_m0_basic_proto` (Adafruit UF2 引导加载程序)
  - :zephyr:board:`arduino_nano_33_iot` (Arduino 引导加载程序)
  - :zephyr:board:`arduino_nano_33_ble` (Arduino 传统引导加载程序)

在 Windows Native 上启用 BOSSAC [实验性]
------------------------------------------------

Zephyr SDK 的 bossac 目前仅在 Linux 和 macOS 上受支持。可以通过使用 `BOSSA official releases`_ 中的 bossac 版本在 Windows 上实现支持。
使用默认选项安装后,必须将 :file:`bossac.exe` 添加到 Windows PATH。可以通过传递
``--bossac`` 选项来使用特定的 bossac 可执行文件,如下所示:

.. code-block:: console

    west flash -r bossac --bossac="C:\Program Files (x86)\BOSSA\bossac.exe" --bossac-port="COMx"

.. note::

   目前不支持 WSL。


.. _linkserver-debug-host-tools:
.. _runner_linkserver:

LinkServer 调试主机工具
****************************

Linkserver 是一个用于启动和管理 NXP 调试探针 GDB 服务器的实用工具,
Linkserver 是一个用于启动和管理 NXP 调试探针 GDB 服务器的实用工具,
它还提供命令行目标闪存编程功能。
Linkserver 可以与 `NXP MCUXpresso for Visual Studio Code`_ 实现一起使用,
也可以与基于 GNU 工具的自定义调试配置一起使用,或作为持续集成和测试的无头解决方案的一部分。LinkServer 可以与 MCU-Link、LPC-Link2、
基于 LPC11U35 的以及来自 NXP 的独立或板载 OpenSDA 调试探针一起使用。

NXP 建议使用 NXP 的 `MCUXpresso Installer`_ 安装 LinkServer。
此方法还将安装支持以下调试探针的工具,
包括 NXP 的 MCU-Link 和 LPCScrypt 工具。

LinkServer 与以下调试探针兼容:

- :ref:`lpclink2-cmsis-onboard-debug-probe`
- :ref:`mcu-link-cmsis-onboard-debug-probe`
- :ref:`opensda-daplink-onboard-debug-probe`

要将 LinkServer 与 West 命令一起使用,应将安装文件夹添加到
:envvar:`PATH` :ref:`环境变量 <env_vars>`。要添加的默认安装路径是:

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

         /usr/local/LinkServer

   .. group-tab:: macOS

      .. code-block:: console

         /Applications/LinkServer_<version>

   .. group-tab:: Windows

      .. code-block:: console

         c:\nxp\LinkServer_<version>

支持的 west 命令:

1. flash
#. debug
#. debugserver
#. attach

注意:


1. 可以使用 LinkServer 列出探针:

.. code-block:: console

   LinkServer probes

2. 如果主机连接了多个调试探针,请使用
   LinkServer west 运行器的 ``--probe`` 选项来传递探针索引。

.. code-block:: console

   west flash --runner=linkserver --probe=3

3. 可以使用 LinkServer 的 west 运行器的 '--override' 选项覆盖设备特定设置。可以多次使用。格式由
   LinkServer 规定,例如:

.. code-block:: console

   west flash --runner=linkserver --override /device/memory/5/flash-driver=MIMXRT500_SFDP_MXIC_OSPI_S.cfx

4. LinkServer 不会在复位处理程序处安装隐式断点。如果
   您想从应用程序开始处单步执行,您
   需要手动在 ``main`` 或复位处理程序处添加断点。

.. _jlink-debug-host-tools:
.. _runner_jlink:

J-Link 调试主机工具
***********************

Segger 为 Linux、macOS 和 Windows 操作系统提供了一套调试主机工具:

- J-Link GDB Server: GDB 远程调试
- J-Link Commander: 命令行控制和闪存编程
- RTT Viewer: RTT 终端输入和输出
- SystemView: 实时事件可视化和记录

这些调试主机工具与以下调试探针兼容:

- :ref:`lpclink2-jlink-onboard-debug-probe`
- :ref:`opensda-jlink-onboard-debug-probe`
- :ref:`mcu-link-jlink-onboard-debug-probe`
- :ref:`jlink-external-debug-probe`
- :ref:`stlink-v21-onboard-debug-probe`

检查您的 SoC 是否在 `J-Link Supported Devices`_ 中列出。

下载并安装 `J-Link Software and Documentation Pack`_ 以获取
J-Link GDB Server 和 Commander,并安装相关的 USB 设备驱动程序。RTT Viewer 和 SystemView 可以单独下载,但不是必需的。

请注意,J-Link GDB 服务器尚不支持 Zephyr RTOS 感知。

.. _openocd-debug-host-tools:
.. _runner_openocd:

OpenOCD 调试主机工具
************************

OpenOCD 是一个社区开源项目,为广泛的 SoC 提供 GDB 远程调试和闪存编程支持。Zephyr SDK 中包含了添加 Zephyr RTOS 感知的分支;否则请参阅 `Getting OpenOCD`_
以获取从官方存储库下载 OpenOCD 的选项。

这些调试主机工具与以下调试探针兼容:

- :ref:`opensda-daplink-onboard-debug-probe`
- :ref:`jlink-external-debug-probe`
- :ref:`stlink-v21-onboard-debug-probe`

检查您的 SoC 是否在 `OpenOCD Supported Devices`_ 中列出。

.. note:: 在 Linux 上,openocd 可通过 `Zephyr SDK
   <https://github.com/zephyrproject-rtos/sdk-ng/releases>`_ 获得。
   Windows 用户应使用以下步骤安装 openocd:

   - 从此处下载适用于 Windows 的 openocd: `OpenOCD Windows`_
   - 将 bin 和 share 目录复制到 ``C:\Program Files\OpenOCD\``
   - 将 ``C:\Program Files\OpenOCD\bin`` 添加到 'PATH' 环境变量

.. _pyocd-debug-host-tools:
.. _runner_pyocd:

pyOCD 调试主机工具
**********************

pyOCD 是来自 Arm 的开源项目,为 Arm Cortex-M SoC 提供 GDB 远程调试和闪存编程支持。它在 PyPi 上分发,并在您完成入门指南中的 :ref:`gs_python_deps` 步骤时安装。pyOCD 包括对 Zephyr RTOS 感知的支持。

这些调试主机工具与以下调试探针兼容:

- :ref:`lpclink2-cmsis-onboard-debug-probe`
- :ref:`mcu-link-cmsis-onboard-debug-probe`
- :ref:`opensda-daplink-onboard-debug-probe`
- :ref:`stlink-v21-onboard-debug-probe`

检查您的 SoC 是否在 `pyOCD Supported Devices`_ 中列出。

.. _lauterbach-trace32-debug-host-tools:
.. _runner_trace32:

Lauterbach TRACE32 调试主机工具
***********************************

`Lauterbach TRACE32`_ 是一系列微处理器开发工具、调试器和实时跟踪器的产品线,支持 JTAG、SWD、NEXUS 或 ETM,涵盖多种核心架构,包括 Arm Cortex-A/-R/-M、RISC-V、Xtensa 等。
Zephyr 允许用户使用 :ref:`west <west-flashing>` 开发和编程具有 Lauterbach TRACE32 支持的板。

该运行器包含 TRACE32 软件的包装器,并允许 Zephyr 板为支持的不同命令执行自定义启动脚本(Practice Script),包括从 CMake 传递额外参数的能力。
由使用此运行器的板来定义在每个命令上执行的操作。

安装 Lauterbach TRACE32 软件
-----------------------------------

从 `Lauterbach TRACE32 download website`_ 下载 Lauterbach TRACE32 软件
(需要注册),并按照 `Lauterbach TRACE32 Installation Guide`_ 中描述的安装步骤进行操作。

烧录和调试
----------------------

将 :ref:`环境变量 <env_vars>` :envvar:`T32_DIR` 设置为 TRACE32
系统目录。然后执行 ``west flash`` 或 ``west debug`` 命令以
烧录或调试 Zephyr 应用程序,如 :ref:`west-build-flash-debug` 中所述。
``debug`` 命令启动 TRACE32 GUI 以允许调试 Zephyr
应用程序,而 ``flash`` 命令隐藏 GUI 并在后台执行所有
操作。

默认情况下,``t32`` 运行器将使用位于 TRACE32 系统
目录中名为 ``config.t32`` 的默认配置文件启动 TRACE32。要使用不同的配置文件,请向运行器提供参数
``--config CONFIG``,例如:

.. code-block:: console

	west flash --config myconfig.t32

有关更多选项,请运行 ``west flash --context -r t32`` 以打印用法。

Zephyr RTOS 感知
---------------------

To enable Zephyr RTOS awareness follow the steps described in
`Lauterbach TRACE32 Zephyr OS Awareness Manual`_.

.. _nxp-s32-debug-host-tools:
.. _runner_nxp_s32dbg:

NXP S32 Debug Probe Host Tools
******************************

:ref:`nxp-s32-debug-probe` is designed to work in conjunction with
`NXP S32 Design Studio for S32 Platform`_.

Download (registration required) NXP S32 Design Studio for S32 Platform and
follow the `S32 Design Studio for S32 Platform Installation User Guide`_ to get
the necessary debug host tools and associated USB device drivers.

Note that Zephyr RTOS-awareness support for the NXP S32 GDB server depends on
the target device. Consult the product release notes for more information.

Supported west commands:

1. debug
#. debugserver
#. attach

Basic usage
-----------

Before starting, add NXP S32 Design Studio installation directory to the system
:ref:`PATH environment variable <env_vars>`. Alternatively, it can be passed to
the runner on each invocation via ``--s32ds-path`` as shown below:

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

         west debug --s32ds-path=/opt/NXP/S32DS.3.6

   .. group-tab:: Windows

      .. code-block:: console

         west debug --s32ds-path=C:\NXP\S32DS.3.6

If multiple S32 debug probes are connected to the host via USB, the runner will
ask the user to select one via command line prompt before continuing. The
connection string for the probe can be also specified when invoking the runner
via ``--dev-id=<connection-string>``. Consult NXP S32 debug probe user manual
for details on how to construct the connection string. For example, if using a
probe with serial ID ``00:04:9f:00:ca:fe``:

.. code-block:: console

   west debug --dev-id='s32dbg:00:04:9f:00:ca:fe'

It is possible to pass extra options to the debug host tools via ``--tool-opt``.
When executing ``debug`` or ``attach`` commands, the tool options will be passed
to the GDB client only. When executing ``debugserver``, the tool options will be
passed to the GDB server. For example, to load a Zephyr application to SRAM and
afterwards detach the debug session:

.. code-block:: console

   west debug --tool-opt='--batch'

Requirements
------------

- **S32 Design Studio version**: 3.6.0 or newer.
- **S32DebugProbe OS (firmware)**: 1.1.0 or newer.

S32 Debug Probe OS Upgrade Procedure
------------------------------------

Refer to the “Reprogramming S32 Debug Probe Firmware Images” chapter
in the `S32 Debug Probe User Guide`_ to upgrade the OS of the S32DebugProbe.

.. _runner_probe_rs:

probe-rs Debug Host Tools
*************************

probe-rs is an open-source embedded toolkit written in Rust. It provides
out-of-the-box support for a variety of debug probes, including CMSIS-DAP,
ST-Link, SEGGER J-Link, FTDI and built-in USB-JTAG interface on ESP32 devices.

Check `probe-rs Installation`_ for more setup details.

Check if your SoC is listed in `probe-rs Supported Devices`_.

.. _runner_rfp:

Renesas Flash Programmer (RFP) Host Tools
*****************************************

Renesas provides `Renesas Flash Programmer`_ as an official programming tool for Renesas boards
using the Renesas standard boot firmware. It is available as a GUI and CLI.

For boards configured with the ``rfp`` west runner, the RFP CLI can be easily used to flash Zephyr.

Supported west commands:

1. flash

Once downloaded, if ``rfp-cli`` is not placed somewhere in your system PATH, you can pass the location
to ``rfp-cli`` when flashing:

.. code-block:: console

   west flash --rfp-cli ~/Downloads/RFP_CLI_Linux_V31800_x64/linux-x64/rfp-cli

.. _stm32cubeclt-host-tools:
.. _runner_stlink_gdbserver:

STM32CubeCLT Flash & Debug Host Tools
*************************************

STMicroelectronics provides `STM32CubeCLT`_ as an official all-in-one toolset compatible with
Linux |reg|, macOS |reg| and Windows |reg|, allowing the use of STMicroelectronics proprietary
tools within third-party development environments.

It notably provides a GDB debugging server (the *ST-LINK GDB Server*) that can be used to debug
applications on STM32 boards thanks to on-board or external ST-LINK debug probes.

It is compatible with the following debug probes:

- :ref:`stlink-v21-onboard-debug-probe`
- Standalone `ST-LINK-V2`_, `ST-LINK-V3`_, and `STLINK-V3PWR`_ probes

Install STM32CubeCLT
--------------------

The easiest way to get the ST-LINK GDB Server is to install `STM32CubeCLT`_ from STMicroelectronics' website.
A valid email address is needed to receive the downloading link.

Basic usage
-----------

The ST-Link GDB Server can be used through the ``west attach``, ``west debug`` or ``west debugserver`` commands
to debug Zephyr applications.

.. code-block:: console

   west debug --runner stlink_gdbserver

.. note::

   The `STM32CubeProgrammer`_ version contained in the `STM32CubeCLT`_ installation can also be used to flash
   applications. To do so, the dedicated :ref:`STM32CubeProgrammer runner <runner_stm32cubeprogrammer>` should
   be used instead of ``stlink_gdbserver``, as done in the following example:

   .. code-block:: console

      west flash --runner stm32cubeprogrammer

.. _stm32cubeprog-flash-host-tools:
.. _runner_stm32cubeprogrammer:

STM32CubeProgrammer Flash Host Tools
************************************

STMicroelectronics provides `STM32CubeProgrammer`_ (STM32CubeProg) as an official programming tool
for STM32 boards on Linux |reg|, macOS |reg|, and Windows |reg| operating systems.

It provides an easy-to-use and efficient environment for reading, writing, and verifying device memory
through both the debug interface (JTAG and SWD) and the bootloader interface (UART and USB DFU, I2C, SPI, and CAN).

It offers a wide range of features to program STM32 internal memories (such as flash, RAM, and OTP)
as well as external memories.

It also allows option programming and upload, programming content verification, and programming automation
through scripting.

它以 GUI(图形用户界面)和 CLI(命令行界面)版本提供。

它与以下调试探针兼容:

- :ref:`stlink-v21-onboard-debug-probe`
- :ref:`jlink-external-debug-probe`
- 独立的 `ST-LINK-V2`_、`ST-LINK-V3`_ 和 `STLINK-V3PWR`_ 探针

安装 STM32CubeProgrammer
---------------------------

获取 `STM32CubeProgrammer`_ 的最简单方法是从 STMicroelectronics 网站下载它。
需要有效的电子邮件地址才能接收下载链接。

或者,它可以作为 `STM32CubeCLT`_ 一体化多操作系统命令行工具集的一部分安装,
该工具集还包括 GDB 调试器客户端和服务器。

如果您的系统上安装了 STM32CubeIDE,那么 STM32CubeProg 已经存在。

基本用法
-----------

`STM32CubeProgrammer`_ 被设置为 Zephyr 支持的所有活动 STM32 板的默认 west 运行器。
它可以通过 ``west flash`` 命令用于烧录 Zephyr 应用程序。

.. code-block:: console

   west flash --runner stm32cubeprogrammer

有关通过 GUI 或 CLI 的高级用法,请查看 `STM32CubeProgrammer User Manual`_。

.. _runner_uf2:

UF2 上传器
************

uf2 运行器支持使用 UF2 (USB Flashing Format) 烧录某些板。
UF2 是一种用户友好的文件格式,旨在通过 USB 大容量存储设备进行拖放编程。

它依赖于目标设备进入特殊的引导加载程序模式,在该模式下,它作为
USB 大容量存储设备出现在主机上。
进入此模式后,可以通过将 ``.uf2`` 文件复制到
挂载的卷来上传应用程序映像。

.. code-block:: console

   west flash --runner uf2

如果未自动检测到 UF2 卷,您可能需要使用 ``--device`` 选项手动指定挂载点:

有关 UF2 格式及其工具的更多信息,请参阅 `USB Flashing Format (UF2)`_。

.. _J-Link Software and Documentation Pack:
   https://www.segger.com/downloads/jlink/#J-LinkSoftwareAndDocumentationPack

.. _J-Link Supported Devices:
   https://www.segger.com/downloads/supported-devices.php

.. _Getting OpenOCD:
   https://openocd.org/pages/getting-openocd.html

.. _OpenOCD Supported Devices:
   https://github.com/zephyrproject-rtos/openocd/tree/latest/tcl/target

.. _pyOCD Supported Devices:
   https://github.com/pyocd/pyOCD/tree/main/pyocd/target/builtin

.. _OpenOCD Windows:
    https://gnutoolchains.com/arm-eabi/openocd/

.. _Lauterbach TRACE32:
    https://www.lauterbach.com/

.. _Lauterbach TRACE32 download website:
   https://www.lauterbach.com/download_trace32.html

.. _Lauterbach TRACE32 Installation Guide:
   https://www2.lauterbach.com/pdf/installation.pdf

.. _Lauterbach TRACE32 Zephyr OS Awareness Manual:
	https://www2.lauterbach.com/pdf/rtos_zephyr.pdf

.. _BOSSA official releases:
	https://github.com/shumatech/BOSSA/releases

.. _NXP MCUXpresso for Visual Studio Code:
	https://www.nxp.com/design/software/development-software/mcuxpresso-software-and-tools-/mcuxpresso-for-visual-studio-code:MCUXPRESSO-VSC

.. _MCUXpresso Installer:
	https://github.com/nxp-mcuxpresso/vscode-for-mcux/wiki/Dependency-Installation

.. _NXP S32 Design Studio for S32 Platform:
   https://www.nxp.com/design/software/development-software/s32-design-studio-ide/s32-design-studio-for-s32-platform:S32DS-S32PLATFORM

.. _Renesas Flash Programmer:
   https://www.renesas.com/en/software-tool/renesas-flash-programmer-programming-gui

.. _S32 Design Studio for S32 Platform Installation User Guide:
   https://www.nxp.com/webapp/Download?colCode=S32DSIG

.. _S32 Debug Probe User Guide:
   https://www.nxp.com/docs/en/user-guide/S32DBGUG.pdf

.. _probe-rs Installation:
   https://probe.rs/docs/getting-started/installation/

.. _probe-rs Supported Devices:
   https://probe.rs/targets/

.. _STM32CubeCLT:
   https://www.st.com/en/development-tools/stm32cubeclt.html

.. _STM32CubeProgrammer:
   https://www.st.com/en/development-tools/stm32cubeprog.html

.. _STM32CubeProgrammer User Manual:
   https://www.st.com/resource/en/user_manual/um2237-stm32cubeprogrammer-software-description-stmicroelectronics.pdf

.. _ST-LINK-V2:
   https://www.st.com/en/development-tools/st-link-v2.html

.. _ST-LINK-V3:
   https://www.st.com/en/development-tools/stlink-v3set.html

.. _STLINK-V3PWR:
   https://www.st.com/en/development-tools/stlink-v3pwr.html

.. _USB Flashing Format (UF2):
   https://github.com/microsoft/uf2
