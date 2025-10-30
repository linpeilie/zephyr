.. _bluetooth-arch:

协议栈架构
##################

概述
********

本页面描述了 Zephyr 蓝牙协议栈的软件架构。

.. note::
   Zephyr 主要支持低功耗蓝牙(Bluetooth Low Energy,LE),即蓝牙规范的低功耗版本。
   Zephyr 对 BR/EDR Host 的部分功能也有有限支持。

.. _bluetooth-layers:

低功耗蓝牙层
===================

完整的低功耗蓝牙协议栈由 3 个主要层组成:

* **主机(Host)**: 此层位于应用程序下方,由多个(非实时)网络和传输协议组成,
  使应用程序能够以标准和可互操作的方式与对等设备通信。
* **控制器(Controller)**: 控制器实现链路层(LE LL),这是一个低级实时协议,
  与无线电硬件配合,提供标准可互操作的空中通信。LL 调度数据包的接收和传输,
  保证数据的传递,并处理所有 LL 控制过程。
* **无线电硬件(Radio Hardware)**: 硬件实现所需的模拟和数字基带功能块,
  使链路层固件能够在 2.4GHz 频段中发送和接收。

.. _bluetooth-hci:

主机控制器接口
=========================

`蓝牙规范`_ 描述了主机必须与控制器通信的格式。这称为主机控制器接口(HCI)协议。
HCI 可以通过不同的物理传输实现,如 UART、SPI 或 USB。该协议定义了主机可以发送给
控制器的命令以及可以期望返回的事件,还定义了需要通过空中传输的用户和协议数据的
格式。HCI 确保不同的主机和控制器实现可以以标准方式通信,使得可以组合来自不同
供应商的主机和控制器。

.. _bluetooth-configs:

配置
==============

协议的三个独立层和标准化接口使得可以在不同平台上实现主机和控制器。通常使用
以下两种配置:

* **单芯片配置**: 在此配置中,单个微控制器实现所有三层和应用程序本身。这也可以
  称为片上系统(SoC)实现。在这种情况下,蓝牙主机和蓝牙控制器直接通过 RAM 中的
  函数调用和队列进行通信。蓝牙规范没有指定如何在这种单芯片配置中实现 HCI,
  因此 HCI 命令、事件和数据在两者之间的流动方式可以是特定于实现的。此配置非常
  适合需要小占用空间和尽可能低功耗的应用程序和设计,因为一切都在单个 IC 上运行。
* **双芯片配置**: 此配置使用两个独立的 IC,一个运行应用程序和主机,另一个运行
  控制器和无线电硬件。这有时也称为连接芯片配置。此配置允许在使用 Zephyr OS
  作为控制器时有更广泛的主机组合。由于 HCI 确保主机和控制器实现之间的互操作性,
  当然包括 Zephyr 自己的蓝牙主机和控制器,Zephyr 控制器的用户可以选择使用在
  他们喜欢的任何平台上运行的任何主机。例如,主机可以是在任何能够支持 Linux 的
  处理器上运行的 Linux 蓝牙主机协议栈(BlueZ)。主机处理器当然也可以运行 Zephyr
  和 Zephyr OS 蓝牙主机。相反,将运行 Zephyr 主机的 IC 与不运行 Zephyr 的
  外部控制器结合也是受支持的。

.. _bluetooth-build-types:

构建类型
===========

作为 RTOS 的 Zephyr 软件栈具有高度可配置性,特别是蓝牙子系统可以在构建过程中
以多种方式配置,以仅包含所需的功能和层,从而减少 RAM 和 ROM 占用以及功耗。
以下是可以从 Zephyr 项目代码库生成的不同启用蓝牙的构建的简短列表:

* **仅控制器构建**: 当作为蓝牙控制器构建时,Zephyr 包括链路层和一个特殊应用程序。
  此应用程序根据为 HCI 选择的物理传输而不同:

  * :zephyr:code-sample:`bluetooth_hci_uart`
  * :zephyr:code-sample:`bluetooth_hci_usb`
  * :zephyr:code-sample:`bluetooth_hci_spi`

  此应用程序充当 UART、SPI 或 USB 外设与控制器子系统之间的桥梁,侦听 HCI 命令,
  发送应用程序数据并响应事件和接收的数据。此类型的构建设置以下 Kconfig 选项值:

  * :kconfig:option:`CONFIG_BT` ``=y``
  * :kconfig:option:`CONFIG_BT_HCI` ``=y``
  * :kconfig:option:`CONFIG_BT_HCI_RAW` ``=y``

  控制器本身也需要启用,通常通过确保相应的设备树节点已启用。

* **仅主机构建**: Zephyr OS 主机构建将包含应用程序和蓝牙主机,以及 HCI 驱动程序
  (UART 或 SPI)以与外部控制器芯片接口。此类型的构建设置以下 Kconfig 选项值:

  * :kconfig:option:`CONFIG_BT` ``=y``
  * :kconfig:option:`CONFIG_BT_HCI` ``=y``

  此外,如果平台也支持本地控制器,则需要禁用它,通常通过禁用相应的设备树节点。
  这与启用其他某些 HCI 驱动程序的设备树节点一起完成,并确保 ``zephyr,bt-hci``
  设备树选择属性指向它。

  位于 ``samples/bluetooth`` 中的所有示例,除了用于仅控制器构建的示例外,
  都可以构建为仅主机

* **组合构建**: 这包括应用程序、主机和控制器,专用于单芯片(SoC)配置。
  此类型的构建设置以下 Kconfig 选项值:

  * :kconfig:option:`CONFIG_BT` ``=y``
  * :kconfig:option:`CONFIG_BT_HCI` ``=y``

  控制器本身也需要启用,通常通过确保相应的设备树节点已启用。

  位于 ``samples/bluetooth`` 中的所有示例,除了用于仅控制器构建的示例外,
  都可以构建为组合

下图显示了使用 Zephyr 组合构建(包含蓝牙主机和控制器的构建,编程到芯片上的
同一固件映像中)时的 SoC 或单芯片配置:

.. figure:: img/ble_cfg_single.png
   :align: center
   :alt: 单芯片上的蓝牙组合构建

   单芯片配置上的组合构建

使用连接或双芯片配置时,可能有几种主机和控制器组合,其中一些如下所示:

.. figure:: img/ble_cfg_dual.png
   :align: center
   :alt: 蓝牙双芯片配置构建

   双芯片配置上的仅主机和仅控制器构建

当使用 Zephyr 主机(图像左侧)时,必须使用不同的配置构建两个 Zephyr OS 实例,
生成两个单独的映像,必须分别编程到每个芯片中。主机构建映像包含应用程序、
蓝牙主机和选定的 HCI 驱动程序(UART 或 SPI),而控制器构建运行
:zephyr:code-sample:`bluetooth_hci_uart` 或 :zephyr:code-sample:`bluetooth_hci_spi`
应用程序,以提供蓝牙控制器的接口。

此配置不限于使用 Zephyr OS 主机,如图像右侧所示。实际上,可以采用许多现有的
GNU/Linux 发行版之一,其中大多数包括 Linux 自己的蓝牙主机(BlueZ),通过 UART
或 USB 将其连接到 Zephyr OS 控制器构建的一个或多个实例。BlueZ 作为主机同时
支持多个控制器,适用于需要多个蓝牙无线电同时运行但共享同一主机协议栈的应用程序。

源树布局
******************

协议栈在源树中的拆分如下:

``subsys/bluetooth/host``
  :ref:`主机协议栈 <bluetooth_le_host>`。这是 HCI 命令和事件处理以及连接跟踪
  发生的地方。核心协议(如 L2CAP、ATT 和 SMP)的实现也在这里。

``subsys/bluetooth/controller``
  :ref:`低功耗蓝牙控制器 <bluetooth-ctlr-arch>` 实现。实现 HCI 的控制器端、
  链路层以及对无线电收发器的访问。

``include/bluetooth/``
  :ref:`公共 API <bluetooth_api>` 头文件。这些是应用程序需要包含的头文件,
  以便使用蓝牙功能。

``drivers/bluetooth/``
  HCI 传输驱动程序。每种 HCI 传输都需要自己的驱动程序。例如,两种常见类型的
  UART 传输协议(3-Wire 和 5-Wire)有各自的驱动程序。

``samples/bluetooth/``
  :zephyr:code-sample-category:`蓝牙示例代码 <bluetooth>`。这是开始蓝牙应用程序
  开发的良好参考。

``tests/bluetooth/``
  测试应用程序。这些应用程序用于验证蓝牙协议栈的功能,但不一定是示例代码的
  最佳来源(请参阅 ``samples/bluetooth``)。

``doc/connectivity/bluetooth/``
  额外文档,例如 PICS 文档。

.. _蓝牙规范: https://www.bluetooth.com/specifications/bluetooth-core-specification
