.. _debug-probes:

调试探针
############

*调试探针* 是一种特殊硬件,允许您控制在单独板上运行的 Zephyr 应用程序的执行。调试探针通常允许读取和写入寄存器和内存,并支持使用 GDB 等工具在主机工作站上对 Zephyr 应用程序进行断点调试。它们还可能支持其他调试软件和更高级的功能,如
:ref:`跟踪程序执行 <tracing>`。有关 Zephyr 支持的相关主机软件的详细信息,请参阅 :ref:`flash-debug-host-tools`。

调试探针通常通过 USB 连接到主机工作站;有时也可以通过 IP 网络或其他方式访问。它们通常使用 JTAG 或 SWD 协议连接到运行 Zephyr 的设备。调试探针可以是单独的硬件设备,也可以是集成到运行 Zephyr 的同一块板上的电路。

Zephyr 中支持的许多板都包含第二个微控制器,用作板载调试探针、USB 转串口适配器,有时还是拖放式烧录程序器。这消除了购买外部调试探针的需要,并提供了各种调试主机工具选项。

几个硬件供应商有自己品牌的板载调试探针实现:NXP 板可能使用
`OpenSDA <#opensda-onboard-debug-probe>`_、
`LPC-Link2 <#lpc-link2-onboard-debug-probe>`_ 或
`MCU-Link <#mcu-link-onboard-debug-probe>`_ 探针,具体取决于
调试探针固件运行的微控制器。
ST 板有 `ST-LINK 探针 <#stlink-v21-onboard-debug-probe>`_。每个
板载调试探针微控制器可以支持一种或多种类型的固件,
这些固件与各自的调试主机工具通信。例如,
OpenSDA 微控制器可以使用 DAPLink 固件进行编程,以与 pyOCD 或 OpenOCD 调试主机工具通信,或使用 J-Link 固件与 J-Link 调试主机工具通信。


+------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
|| *调试探针与主机工具*                     |                                                            主机工具                                                              |
+| *兼容性表*                               +--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                                          |  **J-Link Debug**  |    **OpenOCD**     |      **pyOCD**      |   **NXP S32DS**    | **NXP LinkServer** | **ST-LINK GDB Server** |
+----------------+-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **J-Link 外部**         |           ✓        |          ✓         |                     |                    |                    |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **LPC-Link2 CMSIS-DAP** |                    |                    |                     |                    |         ✓          |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **LPC-Link2 J-Link**    |           ✓        |                    |                     |                    |                    |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **MCU-Link CMSIS-DAP**  |                    |                    |                     |                    |         ✓          |                        |
|  调试探针      +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **MCU-Link J-Link**     |           ✓        |                    |                     |                    |                    |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **NXP S32 调试探针**    |                    |                    |                     |          ✓         |                    |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **OpenSDA DAPLink**     |                    |          ✓         |          ✓          |                    |         ✓          |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **OpenSDA J-Link**      |           ✓        |                    |                     |                    |                    |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **ST-LINK/V2-1**        |           ✓        |          ✓         | *部分 STM32 板*     |                    |                    |           ✓            |
+----------------+-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+


Zephyr 中支持的一些板不包含板载调试探针,因此需要外部调试探针。此外,包含板载调试探针的板通常也有 SWD 或 JTAG 引脚头,以启用使用外部调试探针。这可能有用的一个原因是板载调试探针可能有局限性,例如缺乏对高级调试器或高速跟踪的支持。您可能需要调整跳线以防止板载调试探针干扰外部调试探针。

.. _nxp-onboard-debug-probes:

NXP 板载调试探针
************************

NXP 板可能有几种板载调试探针之一。这些探针包括
:ref:`mcu-link-onboard-debug-probe`、:ref:`lpc-link2-onboard-debug-probe`
和 :ref:`opensda-onboard-debug-probe`。每个探针都作为评估板上的辅助微控制器实现。给定板上存在的特定调试探针类型可以根据调试微控制器 SOC 确定:

- LPC55S69: :ref:`mcu-link-onboard-debug-probe`
- LPC4322: :ref:`lpc-link2-onboard-debug-probe`
- MK20: :ref:`opensda-onboard-debug-probe`

例如,:zephyr:board:`frdm_k64f` 板有 MK20 调试微控制器,
因此该板使用 :ref:`opensda-onboard-debug-probe`。

.. _mcu-link-onboard-debug-probe:

MCU-Link 板载调试探针
****************************

MCU-Link 板载调试探针使用 LPC55S69 SOC。此探针支持以下固件:

- :ref:`mcu-link-cmsis-onboard-debug-probe` (默认固件)
- :ref:`mcu-link-jlink-onboard-debug-probe`

This probe is programmed using the MCU-Link host tools, which are installed
with the :ref:`linkserver-debug-host-tools`. NXP recommends using NXP's
`MCUXpresso Installer`_ to install the Linkserver tools.

.. _mcu-link-cmsis-onboard-debug-probe:

MCU-Link CMSIS-DAP Onboard Debug Probe
======================================

This is the default firmware installed on MCU-Link debug probes.  The CMSIS-DAP
debug probes allow debugging from any compatible toolchain, including IAR
EWARM, Keil MDK, NXP’s MCUXpresso IDE and MCUXpresso extension for VS Code. In
addition to debug probe functionality, the MCU-Link probes may also provide:

1. SWO trace end point: this virtual device is used by MCUXpresso to retrieve
   SWO trace data. See the MCUXpresso IDE documentation for more information.
#. Virtual COM (VCOM) port / UART bridge connected to the target processor
#. USB to UART, SPI and/or I2C interfaces (depending on MCU-Link
   type/implementation)
#. Energy measurements of the target MCU

This debug probe is compatible with the following debug host tools:

- :ref:`linkserver-debug-host-tools`

Once the MCU-Link host tools are installed, the following steps are
required to program the CMSIS-DAP firmware:

1. Make sure the MCU-Link utility is present on your host machine. This can
   be done by installing :ref:`linkserver-debug-host-tools`.

#. Put the MCU-Link microcontroller into DFU boot mode by attaching the DFU
   jumper then connecting to the USB debug port on the board.  This jumper may
   also be referred to as the ISP jumper, and will be connected to ``PIO0_5``
   on the LPC55S69.

#. Run the ``program_CMSIS`` script, found in the installed MCU-Link ``scripts``
   folder.

#. Remove the DFU jumper and power cycle the board.

.. _mcu-link-jlink-onboard-debug-probe:

MCU-Link JLink Onboard Debug Probe
==================================

This debug probe firmware provides a JLink compatible debug interface,
as well as a USB-Serial adapter. It is compatible with the following debug host
tools:

- :ref:`jlink-debug-host-tools`

These probes do not have JLink firmware installed by default, and must be
updated. Once the MCU-Link host tools are installed, the following steps are
required to program the JLink firmware:

1. Make sure the MCU-Link utility is present on your host machine. This can
   be done by installing :ref:`linkserver-debug-host-tools`.

#. Put the MCU-Link microcontroller into DFU boot mode by attaching the DFU
   jumper then connecting to the USB debug port on the board.  This jumper may
   also be referred to as the ISP jumper, and will be connected to ``PIO0_5``
   on the LPC55S69.

#. Run the ``program_JLINK`` script, found in the installed MCU-Link ``scripts``
   folder.

#. Remove the DFU jumper and power cycle the board.

.. _lpc-link2-onboard-debug-probe:

LPC-LINK2 Onboard Debug Probe
*****************************

The LPC-LINK2 onboard debug probe uses an LPC4322 SOC. This probe supports
the following firmwares:

- :ref:`lpclink2-cmsis-onboard-debug-probe`
- :ref:`lpclink2-jlink-onboard-debug-probe`
- :ref:`lpclink2-daplink-onboard-debug-probe` (default firmware)

This probe is programmed using the LPCScrypt host tools, which are installed
with the :ref:`linkserver-debug-host-tools`. NXP recommends using NXP's
`MCUXpresso Installer`_ to install the Linkserver tools.

.. _lpclink2-cmsis-onboard-debug-probe:

LPC-LINK2 CMSIS DAP Onboard Debug Probe
=======================================

The CMSIS-DAP debug probes allow debugging from any compatible toolchain,
including IAR EWARM, Keil MDK, as well as NXP’s MCUXpresso IDE and
MCUXpresso extension for VS Code.
As well as providing debug probe functionality, the LPC-Link2 probes also
provide:

1. SWO trace end point: this virtual device is used by MCUXpresso to retrieve
   SWO trace data. See the MCUXpresso IDE documentation for more information.
2. Virtual COM (VCOM) port / UART bridge connected to the target processor
3. LPCSIO bridge that provides communication to I2C and SPI slave devices

This debug probe firmware is compatible with the following debug host tools:

- :ref:`linkserver-debug-host-tools`

The probe may be updated to use CMSIS-DAP firmware with the following steps:

1. Make sure the LPCScrypt utility is present on your host machine. This can
   be done by installing :ref:`linkserver-debug-host-tools`.

#. Put the LPC-Link2 microcontroller into DFU boot mode by attaching the DFU
   jumper, then connecting to the USB debug port on the board. This
   jumper is connected to ``P2_6`` on the LPC4322 SOC.

#. Run the ``program_CMSIS`` script, found in the installed LPCScrypt ``scripts``
   folder.

#. Remove the DFU jumper and power cycle the board.

.. _lpclink2-jlink-onboard-debug-probe:

LPC-Link2 J-Link Onboard Debug Probe
====================================

.. note:: On some boards, the J-Link probe firmware will no longer power the
   board via the USB debug port. On these boards, an alternative method
   of powering the board must be used when this firmware is programmed.

This debug probe firmware provides a JLink compatible debug interface,
as well as a USB-Serial adapter. It is compatible with the following debug host
tools:

- :ref:`jlink-debug-host-tools`

The probe may be updated to use the J-Link firmware with the following steps:

.. note:: Verify the firmware supports your board by visiting `Firmware for LPCXpresso`_

1. Make sure the LPCScrypt utility is present on your host machine. This can
   be done by installing :ref:`linkserver-debug-host-tools`.

#. Put the LPC-Link2 microcontroller into DFU boot mode by attaching the DFU
   jumper, then connecting to the USB debug port on the board. This
   jumper is connected to ``P2_6`` on the LPC4322 SOC.

#. Run the ``program_JLINK`` script, found in the installed LPCScrypt ``scripts``
   folder.

#. Remove the DFU jumper and power cycle the board.

.. _lpclink2-daplink-onboard-debug-probe:

LPC-Link2 DAPLink Onboard Debug Probe
=====================================

The LPC-Link2 DAPLink firmware is the default firmware shipped on LPC-Link2
based boards, but is not the recommended firmware. Users should update to
the :ref:`lpclink2-cmsis-onboard-debug-probe` firmware following the
instructions provided above. For details on programming the DAPLink firmware,
see `NXP AN13206`_.

.. _opensda-onboard-debug-probe:

OpenSDA Onboard Debug Probe
***************************

The OpenSDA onboard debug probe is based on the NXP MK20 SOC. It features
drag and drop programming supports, and supports the following debug firmwares:

- :ref:`opensda-daplink-onboard-debug-probe` (default firmware)
- :ref:`opensda-jlink-onboard-debug-probe`

.. _opensda-daplink-onboard-debug-probe:

OpenSDA DAPLink 板载调试探针
===================================

此调试探针固件与以下调试主机工具兼容:

- :ref:`pyocd-debug-host-tools`
- :ref:`openocd-debug-host-tools`
- :ref:`linkserver-debug-host-tools`

此探针是通过使用 DAPLink OpenSDA 固件对 OpenSDA 微控制器进行编程来实现的。NXP 提供 `OpenSDA DAPLink Board-Specific Firmwares`_。

在编程固件之前安装调试主机工具。

与所有 OpenSDA 调试探针一样,编程固件的步骤是:

1. 通过在给板上电时按住复位按钮,使 OpenSDA 微控制器进入引导加载程序模式。请注意,此上下文中的"引导加载程序模式"适用于 OpenSDA 微控制器本身,而不是 Zephyr 应用程序的目标微控制器。

#. 给板上电后,释放复位按钮。将枚举一个名为 **BOOTLOADER** 或 **MAINTENANCE** 的 USB 大容量存储设备。如果枚举的设备名为 **BOOTLOADER**,请首先按照 `DAPLink Bootloader Update`_ 的说明将引导加载程序更新到最新版本。

#. 将 OpenSDA 固件二进制文件复制到 USB 大容量存储设备。

#. 重新给板供电,这次不按住复位按钮。您应该看到枚举三个 USB 设备:CDC 设备(串口)、HID 设备(调试端口)和大容量存储设备(拖放式烧录程序)。

.. _opensda-jlink-onboard-debug-probe:

OpenSDA J-Link 板载调试探针
==================================

此调试探针与以下调试主机工具兼容:

- :ref:`jlink-debug-host-tools`

此探针是通过使用 J-Link OpenSDA 固件对 OpenSDA 微控制器进行编程来实现的。Segger 提供 `OpenSDA J-Link Generic Firmwares`_ 和
`OpenSDA J-Link Board-Specific Firmwares`_,通常建议使用后者(如果可用)。i.MX RT 板需要特定于板的固件才能支持其外部闪存,而通用固件与所有 Kinetis 板兼容。

在编程固件之前安装调试主机工具。

与所有 OpenSDA 调试探针一样,编程固件的步骤是:

1. 通过在将 USB 插入板的 USB 调试端口时按住复位按钮,使 OpenSDA 微控制器进入引导加载程序模式。请注意,此上下文中的"引导加载程序模式"适用于 OpenSDA 微控制器本身,而不是 Zephyr 应用程序的目标微控制器。

#. 给板上电后,释放复位按钮。将枚举一个名为 **BOOTLOADER** 或 **MAINTENANCE** 的 USB 大容量存储设备。如果枚举的设备名为 **BOOTLOADER**,请首先按照 `DAPLink Bootloader Update`_ 的说明将引导加载程序更新到最新版本。

#. 将 OpenSDA 固件二进制文件复制到 USB 大容量存储设备。

#. 重新给板供电,这次不按住复位按钮。您应该看到枚举两个 USB 设备:CDC 设备(串口)和供应商特定设备(调试端口)。

.. _jlink-external-debug-probe:

J-Link 外部调试探针
***************************

`Segger J-Link`_ 是一系列外部调试探针,包括 J-Link EDU、J-Link PLUS、J-Link ULTRA+ 和 J-Link PRO,支持来自不同硬件架构和供应商的大量设备。

此调试探针与以下调试主机工具兼容:

- :ref:`jlink-debug-host-tools`
- :ref:`openocd-debug-host-tools`

在编程固件之前安装调试主机工具。

.. _stlink-v21-onboard-debug-probe:

ST-LINK/V2-1 板载调试探针
********************************

ST-LINK/V2-1 是内置在所有 Nucleo 和 Discovery 板中的串口和调试适配器。它在您的计算机(或其他 USB 主机)和嵌入式目标处理器之间提供桥接,可用于调试、闪存编程和串口通信,全部通过简单的 USB 电缆完成。

它与以下主机调试工具兼容:

- :ref:`openocd-debug-host-tools`
- :ref:`jlink-debug-host-tools`
- :ref:`stm32cubeclt-host-tools`

对于某些基于 STM32 的板,它还与以下兼容:

- :ref:`pyocd-debug-host-tools`

虽然它可以直接与 OpenOCD 一起使用,但需要一些烧录才能与 J-Link 一起使用。为此,SEGGER 提供了一个固件,可升级 Nucleo 和 Discovery 板上的 ST-LINK/V2-1。此固件使 ST-LINK/V2-1 与 J-LinkOB 兼容,允许用户利用大多数 J-Link 功能,如超快闪存下载和调试速度或免费使用的 GDBServer。

有关将 ST-LINK/V2-1 升级到 JLink 或恢复 ST-Link/V2-1 固件的更多信息,请访问:`Segger over ST-Link`_

使用 ST-Link 烧录和调试
============================

.. tabs::

    .. tab:: 使用 OpenOCD

        OpenOCD 在 ST-Link 上默认可用,并配置为默认的烧录和调试工具。烧录和调试可以如下完成:

          .. zephyr-app-commands::
             :zephyr-app: samples/hello_world
             :goals: flash

          .. zephyr-app-commands::
             :zephyr-app: samples/hello_world
             :goals: debug

    .. tab:: _`使用 Segger J-Link`

        一旦 STLink 使用 SEGGER FW 烧录,并且 J-Link GDB 服务器安装在您的主机上,您可以如下烧录和调试:

        使用 CMake 配合 ``-DBOARD_FLASH_RUNNER=jlink`` 将默认的 OpenOCD 运行器更改为 J-Link。或者,您可以在应用程序 ``CMakeList.txt`` 文件中添加以下行。

          .. code-block:: cmake

             set(BOARD_FLASH_RUNNER jlink)

        如果您使用 West(Zephyr 的元工具),可以使用 ``--runner``(或 ``-r``)选项修改默认运行器。

          .. code-block:: console

             west flash --runner jlink

        使用 ``jlink`` 将调试器附加到您的板并打开调试控制台。

          .. code-block:: console

             west debug --runner jlink

        有关 West 和可用选项的更多信息,请参阅 :ref:`west`。

        如果您将 Zephyr 应用程序配置为使用 `Segger RTT`_ 控制台,请打开 telnet:

          .. code-block:: console

             $ telnet localhost 19021
             Trying ::1...
             Trying 127.0.0.1...
             Connected to localhost.
             Escape character is '^]'.
             SEGGER J-Link V6.30f - Real time terminal output
             J-Link STLink V21 compiled Jun 26 2017 10:35:16 V1.0, SN=773895351
             Process: JLinkGDBServerCLExe
             Zephyr Shell, Zephyr version: 1.12.99
             Type 'help' for a list of available commands
             shell>

        如果您没有获得 RTT 输出,您可能需要禁用与 RTT 冲突的其他控制台,如果它们在您运行的特定示例或应用程序中默认启用,例如在 menuconfig 中禁用 UART_CONSOLE

更新或恢复 ST-Link 固件
======================================

可以使用 `STM32CubeProgrammer Tool`_ 更新 ST-Link 固件。
当遇到烧录问题时,这通常很有用,例如在使用 twister 的设备测试选项时。

安装后,您可以使用以下命令更新附加板的 ST-Link 固件

  .. code-block:: console

     s java -jar ~/STMicroelectronics/STM32Cube/STM32CubeProgrammer/Drivers/FirmwareUpgrade/STLinkUpgrade.jar -sn <board_uid>

其中 board_uid 可以使用 twister 的 generate-hardware-map 选项获得。有关 twister 和可用选项的更多信息,请参阅
:ref:`twister_script`。

.. _nxp-s32-debug-probe:

NXP S32 调试探针
*******************

`NXP S32 Debug Probe`_ 通过标准调试端口实现 NXP S32 目标系统调试,同时通过 USB 连接到开发人员的工作站或通过以太网远程连接。

NXP S32 调试探针旨在与 NXP S32 Design Studio (S32DS) 和 NXP 汽车微控制器和处理器配合使用。在编程固件之前,按照 :ref:`nxp-s32-debug-host-tools` 中的说明安装调试主机工具。

.. _black-magic-probe:

Black Magic Probe
*****************

Black Magic Probe 是一种开源调试硬件,旨在与 `Black Magic Debug`_ 固件一起使用。
该固件集成了 GDB Server,因此您可以直接从 ``gdb`` 连接到目标设备。

一些基于 STM32F103 的板可以运行 `Black Magic Debug`_ 固件。
请参阅 `Black Magic Debug supported hardware`_。

.. _LPCScrypt:
   https://www.nxp.com/lpcscrypt

.. _Firmware for LPCXpresso:
   https://www.segger.com/products/debug-probes/j-link/models/other-j-links/lpcxpresso-on-board/

.. _OpenSDA DAPLink Board-Specific Firmwares:
   https://www.nxp.com/opensda

.. _OpenSDA J-Link Generic Firmwares:
   https://www.segger.com/downloads/jlink/#JLinkOpenSDAGenericFirmwares

.. _OpenSDA J-Link Board-Specific Firmwares:
   https://www.segger.com/downloads/jlink/#JLinkOpenSDABoardSpecificFirmwares

.. _Segger J-Link:
   https://www.segger.com/products/debug-probes/j-link/

.. _Segger over ST-Link:
   https://www.segger.com/products/debug-probes/j-link/models/other-j-links/st-link-on-board/

.. _Segger RTT:
    https://www.segger.com/jlink-rtt.html

.. _STM32CubeProgrammer Tool:
    https://www.st.com/en/development-tools/stm32cubeprog.html

.. _MCUXpresso Installer:
	https://www.nxp.com/lgfiles/updates/mcuxpresso/MCUXpressoInstaller.exe

.. _NXP S32 Debug Probe:
   https://www.nxp.com/design/software/automotive-software-and-tools/s32-debug-probe:S32-DP

.. _NXP AN13206:
   https://www.nxp.com/docs/en/application-note/AN13206.pdf

.. _DAPLink Bootloader Update:
   https://os.mbed.com/blog/entry/DAPLink-bootloader-update/

.. _Black Magic Debug:
   https://black-magic.org/index.html

.. _Black Magic Debug supported hardware:
   https://black-magic.org/hardware.html
