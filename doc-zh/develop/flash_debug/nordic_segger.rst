:orphan:

.. _nordic_segger:

Nordic nRF5x Segger J-Link
##########################

概述
****

所有 Nordic nRF5x 开发套件、预览开发套件和加密狗都配备了调试 IC(Atmel ATSAM3U2C),
提供以下功能:

* Segger J-Link 固件和桌面工具
* nRF5x IC 的 SWD 调试
* 用于拖放式镜像烧录的海量存储设备
* 桥接到 nRF5x UART 外设的 USB CDC ACM 串口
* Segger RTT 控制台
* Segger Ozone 调试器

Segger J-Link 软件安装
**********************

要安装 J-Link 软件和文档包,请按照以下步骤操作:

#. 从 `J-Link Software and documentation pack`_ 网站下载适当的软件包
#. 根据您的平台,安装软件包或运行安装程序
#. 当连接启用 J-Link 的开发板(如 nRF5x DK、PDK 或加密狗)时,应该会出现一个
   对应 USB 海量存储设备的驱动器以及一个串口

nRF5x 命令行工具安装
********************

nRF5x 命令行工具允许您从命令行控制 nRF5x 设备,包括重置、擦除或编程闪存等。

要安装它们,请访问 `nRF5x Command-Line Tools`_ 并选择您的操作系统。

安装后,请确保 ``nrfjprog`` 在您的可执行路径中,以便能够从任何位置调用它。

.. _nordic_segger_flashing:

烧录
****

要在按照说明安装了 Segger J-Link 软件和 nRF5x 命令行工具后,使用编译的 Zephyr 镜像
对闪存进行编程,请按照以下步骤操作:

* 将 micro-USB 线缆连接到 nRF5x 开发板和您的计算机
* 擦除 nRF5x IC 中的闪存:

.. code-block:: console

   nrfjprog --eraseall -f nrf5<x>

其中 ``<x>`` 对于基于 nRF51 的开发板为 1,对于基于 nRF52 的开发板为 2

* 从您选择的示例文件夹烧录 Zephyr 镜像:

.. code-block:: console

   nrfjprog --program outdir/<board>/zephyr.hex -f nrf5<x>

其中:``<board>`` 是您在构建时在 BOARD 指令中使用的开发板名称(例如 nrf52dk/nrf52832),
``<x>`` 对于基于 nRF51 的开发板为 1,对于基于 nRF52 的开发板为 2

* 重置并启动 Zephyr:

.. code-block:: console

   nrfjprog --reset -f nrf5<x>

其中 ``<x>`` 对于基于 nRF51 的开发板为 1,对于基于 nRF52 的开发板为 2

USB CDC ACM 串口设置
*******************

**重要说明**:nRF5x 开发板上的 Segger J-Link 固件问题可能会导致某些机器上的
USB CDC ACM 串口出现数据丢失和/或损坏。要解决此问题,请按照 :ref:`nordic_segger_msd`
中所述禁用开发板上的海量存储设备。

Windows
=======

串口将显示为 ``COMxx``。只需检查设备管理器中的"端口(COM 和 LPT)"部分。

GNU/Linux
=========

串口将显示为 ``/dev/ttyACMx``。默认情况下,并非所有用户都可以访问该端口。
输入以下命令将您的用户添加到 dialout 组,以便授予其访问串口的权限。
请注意,需要重新登录才能使此更改生效。

.. code-block:: bash

   sudo usermod -a -G dialout `whoami`

最近版本的 `ModemManager send AT commands to TTY-like devices`_;这包括 Nordic
开发套件。这将阻止您使用串口几秒钟,如果您的应用程序从 UART 读取数据,
可能会导致应用程序行为异常。在运行应用程序之前,您可能需要通过运行以下命令
临时禁用 ModemManager:

.. code-block:: bash

   systemctl stop ModemManager.service
   systemctl disable ModemManager.service

您还可以通过编辑 udev 规则来 `blocklist Segger devices by editing udev rules`_,
使 ModemManager 忽略它们,运行:

.. code-block:: bash

   sudo sh -c 'echo "ATTRS{idVendor}==\"1366\", ENV{ID_MM_DEVICE_IGNORE}=\"1\" " \
     >> /etc/udev/rules.d/99-segger-modemmanager-blocklist.rules'
   sudo service udev restart

预计 ModemManager 1.8 和 Segger IMCU 的新固件将修复此问题。

Apple macOS (OS X)
==================

串口将显示为 ``/dev/tty.usbmodemXXXX``。

.. _nordic_segger_msd:

禁用海量存储设备功能
********************

由于 Segger 的 J-Link 固件中的已知问题,根据您的操作系统和版本,如果您使用
大于 64 字节的数据包的 USB CDC ACM 串口,可能会遇到数据损坏或丢失。
这在 GNU/Linux 和 macOS(OS X)上都有观察到。

为避免这种情况,您可以通过打开以下工具来简单禁用海量存储设备:

* 在 GNU/Linux 或 macOS(OS X)上从终端运行 JLinkExe
* 在 Microsoft Windows 上运行"JLink Commander"应用程序

然后输入以下命令:

.. code-block:: bat

   MSDDisable

最后拔掉并重新插入开发板。海量存储设备应该不再出现,现在您应该能够通过虚拟串口
发送长数据包。有关 Segger 的更多信息,请参见 `Segger SAM3U Wiki`_。

RTT 控制台
**********

Segger 的 J-Link 支持 `Real-Time Tracing (RTT)`_,这是一项允许在目标(nRF5x 开发板)
和开发计算机之间建立终端连接(输入和输出)以进行日志记录和输入的技术。Zephyr 支持
nRF5x 目标上的 RTT,如果 UART(通过 USB CDC ACM)已经用于日志记录之外的目的
(例如 hci_uart 应用程序中的 HCI 流量),这将非常有用。要使用 RTT,您首先需要
通过在 ``.conf`` 文件中添加以下行来启用它:

.. code-block:: cfg

   CONFIG_USE_SEGGER_RTT=y
   CONFIG_RTT_CONSOLE=y

.. warning::

   还有一个 ``HAS_SEGGER_RTT`` 符号,表示该平台支持 SEGGER J-Link RTT。
   该符号由 SoC Kconfig 文件自动设置。不要将其与 ``USE_SEGGER_RTT`` 混淆。

   ``USE_SEGGER_RTT`` 依赖于 ``HAS_SEGGER_RTT``。

如果您没有得到 RTT 输出,您可能需要禁用与 RTT 冲突的其他控制台(如果它们在您正在
运行的特定示例或应用程序中默认启用)。例如,要禁用 UART 控制台,请将以下内容添加到
您的 ``.conf`` 文件中:

.. code-block:: cfg

   CONFIG_UART_CONSOLE=n

启用 RTT 编译和烧录后,您可以通过以下方式显示 RTT 控制台消息:

Windows
=======

* 打开"J-Link RTT Viewer"应用程序
* 选择以下选项:

  * Connection:USB
  * Target Device:从列表中选择您的 IC
  * Target Interface and Speed:SWD,4000 KHz
  * RTT Control Block:Auto Detection

GNU/Linux 和 macOS (OS X)
==========================

* 从终端打开 ``JLinkRTTLogger``
* 选择以下选项:

  * Device Name:使用您 IC 的完全限定设备名称
  * Target Interface:SWD
  * Interface Speed:4000 KHz
  * RTT Control Block address:auto-detection
  * RTT Channel name or index:0
  * Output file:文件名或 ``/dev/stdout`` 以直接显示在终端上

Python 查看器
=============

可以在 `pyrtt-viewer`_ GitHub 仓库中找到 Python RTT 查看器工具。

Segger Ozone
************

Segger J-Link 与 `Segger Ozone`_ 兼容,这是一个可视化调试器,可以在这里获取:

* `Segger Ozone Download`_

下载后,您可以安装它并按如下方式进行配置:

* Target Device:从列表中选择您的 IC
* Target Interface:SWD
* Target Interface Speed:4 MHz
* Host Interface:USB

配置完成后,您可以使用 File->Open 菜单打开构建文件夹中的 ``zephyr.elf`` 文件。

参考
****

.. target-notes::

.. _nRF5x Command-Line Tools: https://www.nordicsemi.com/Software-and-Tools/Development-Tools/nRF-Command-Line-Tools

.. _Segger SAM3U Wiki: https://wiki.segger.com/index.php?title=J-Link-OB_SAM3U
.. _Real-Time Tracing (RTT): https://www.segger.com/jlink-rtt.html
.. _pyrtt-viewer: https://github.com/thomasstenersen/pyrtt-viewer
.. _Segger Ozone: https://www.segger.com/ozone.html
.. _Segger Ozone Download: https://www.segger.com/downloads/jlink#Ozone

.. _ModemManager send AT commands to TTY-like devices: https://bugs.freedesktop.org/show_bug.cgi?id=85007
.. _blocklist Segger devices by editing udev rules: http://www.at91.com/linux4sam/bin/view/Linux4SAM/SoftwareTools#Device_or_resource_busy_dev_ttyA

.. _J-Link Software and documentation pack: https://www.segger.com/jlink-software.html
