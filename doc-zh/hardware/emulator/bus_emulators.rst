.. _bus_emul:

外部总线和总线连接外设模拟器 (External Bus and Bus Connected Peripherals Emulators)
####################################################################################

概述 (Overview)
================

Zephyr 支持一个简单的模拟器框架，用于支持外部外设驱动程序的测试，无需真实硬件。

模拟器用于模拟外部硬件设备，以支持各种子系统的测试。例如，可以为 I2C 指南针编写一个模拟器，使其出现在 I2C 总线上，并且可以像真实硬件设备一样使用。

模拟器通常实现用于测试的特殊功能。例如，如果 I2C 总线速度过高，指南针可能支持返回伪数据，或者如果尚未完成校准，则可能返回无效测量值。这允许测试高级代码是否可以正确处理这些情况。因此，如果模拟了所有故障条件，测试覆盖率可以达到 100%。

概念 (Concept)
===============

下图在顶部显示了应用程序代码/高级测试。这是我们想要运行的最终应用程序。

.. figure:: img/arch.svg
   :align: center
   :alt: 模拟器架构，显示测试、模拟器和驱动程序

下面是外设驱动程序，例如 AT24 EEPROM 驱动程序。我们可以使用通过模拟 I2C 控制器/模拟器连接的模拟驱动程序测试外设驱动程序，该模拟器将 I2C 流量从 AT24 驱动程序传递到 AT24 模拟器。

另外，我们可以使用 API 测试在真实硬件上测试 STM32 和 NXP I2C 驱动程序。这些需要某种连接到总线的设备，但有了这个，我们可以验证大部分驱动程序功能。

将两者结合在一起，我们可以完全在 native_sim 上测试应用程序和外设代码。由于我们知道真实硬件上的 I2C 驱动程序可以工作，我们应该期望应用程序和外设驱动程序也可以在真实硬件上工作。

使用上述框架，我们可以在 native_sim 上测试整个应用程序(例如嵌入式控制器)，对所有非芯片驱动程序使用模拟器。

使用这种方法，我们可以:

* 为每个驱动程序(绿色)编写单独的测试，涵盖所有故障模式、错误条件等。

* 确保驱动程序(绿色)的 100% 测试覆盖率

* 为驱动程序组合编写测试，例如由通过 I2C 总线通信的 I2C GPIO 扩展器驱动程序提供的 GPIO，其中 GPIO 控制充电器。
  所有这些都可以在模拟环境或真实硬件上工作。

* 编写一个复杂的应用程序，将所有这些部分联系在一起，并在 native_sim 上运行。我们可以在主机上开发，使用源代码级调试等。

* 通过添加 Kconfig 和设备树片段，将应用程序传输到提供所需功能(例如 I2C、足够的 GPIO)的任何开发板。

创建设备驱动程序模拟器 (Creating a Device Driver Emulator)
=============================================================

模拟器子系统以 :ref:`device_model_api` 为模型。您使用 :c:func:`EMUL_DT_DEFINE()` 或 :c:func:`EMUL_DT_INST_DEFINE()` API 之一创建模拟器实例。

外设设备的模拟器重用与真实设备驱动程序相同的设备树节点。这意味着您的模拟器使用与真实驱动程序相同的 ``compat`` 值定义 ``DT_DRV_COMPAT``。

.. code-block:: C

  /* From drivers/sensor/bm160/bm160.c */
  #define DT_DRV_COMPAT bosch_bmi160

  /* From drivers/sensor/bmi160/emul_bmi160.c */
  #define DT_DRV_COMPAT bosch_bmi160

``EMUL_DT_DEFINE()`` 函数接受两种 API 类型:

  #. ``bus_api`` - 这指向模拟器连接到的上游总线的 API。``bus_api`` 参数是必需的。支持的模拟总线类型包括 I2C、SPI、eSPI 和 MSPI。
  #. ``_backend_api`` - 这指向模拟器的设备类特定后端 API。``_backend_api`` 参数是可选的。

下图演示了使用 BC1.2 充电检测器驱动程序作为模型设备类的 ``bus_api`` 和 ``_backend_api`` 的逻辑组织。

.. figure:: img/device_class_emulator.svg
   :align: center
   :alt: 设备类示例，演示 BC1.2 充电检测器。

真实代码以绿色显示，而模拟器代码以黄色显示。

``bus_api`` 将 BC1.2 模拟器连接到 ``native_sim`` I2C 控制器。真实的 BC1.2 驱动程序保持不变，并且完全像系统中存在物理 I2C 控制器一样运行。``native_sim`` I2C 控制器使用 ``bus_api`` 启动对模拟器的寄存器读写操作。

``_backend_api`` 提供了一种机制，使测试能够在带外操纵模拟器。每个设备类定义自己的 API 函数。后端 API 函数专注于高级行为，不为特定模拟器提供钩子。

在 BC1.2 充电检测器的情况下，后端 API 提供了模拟将充电器连接和断开到模拟 BC1.2 设备的功能。每个模拟器负责更新正确的供应商特定寄存器并可能发出中断信号。

示例测试流程:

  #. 测试使用 Zephyr BC1.2 驱动程序 API 注册 BC1.2 检测回调。
  #. 测试使用 BC1.2 模拟器后端连接充电器。
  #. 测试验证 B1.2 检测回调使用正确的充电器类型调用。
  #. 测试使用 BC1.2 模拟器后端断开充电器。

使用这种架构，同一个测试可以用于同一驱动程序类中的所有支持的驱动程序。

可用的模拟器 (Available Emulators)
====================================

Zephyr 包括以下模拟器:

* I2C 模拟器驱动程序，允许驱动程序连接到模拟器，以便在无法访问真实硬件的情况下执行测试

* SPI 模拟器驱动程序，对 SPI 执行相同的操作

* eSPI 模拟器驱动程序，对 eSPI 执行相同的操作。该模拟器正在开发以支持更多功能。

* MSPI 模拟器驱动程序，允许驱动程序连接到模拟器，以便在无法访问真实硬件的情况下执行测试。

I2C 模拟功能 (I2C Emulation features)
--------------------------------------

在 I2C 模拟总线的绑定中，有一个用于基于地址转发的自定义属性。给定以下设备树节点:

.. code-block:: devicetree

   i2c0: i2c@100 {
     status = "okay";
     compatible = "zephyr,i2c-emul-controller";
     clock-frequency = <I2C_BITRATE_STANDARD>;
     #address-cells = <1>;
     #size-cells = <0>;
     #forward-cells = <1>;
     reg = <0x100 4>;
     forwards = <&i2c1 0x20>;
   };

最后一个属性 ``forwards`` 指示发送到地址 ``0x20`` 的任何读/写请求应使用相同的地址发送到 ``i2c1``。这允许我们在同一镜像上测试通信的控制器端和目标端。

.. note::
   ``#forward-cells`` 属性应始终为 1。``forwards`` 属性中的每个条目由 phandle 后跟地址组成。在上面的示例中，``<&i2c1 0x20>`` 将把在端口 ``0x20`` 上对 ``i2c0`` 进行的所有读/写操作转发到同一端口上的 ``i2c1``。由于模拟控制器不使用其他单元，因此单元数应保持为 1。

示例 (Samples)
==============

以下是 Zephyr 中存在的一些示例:

#. Bosch BMI160 传感器驱动程序通过 I2C 和 SPI 连接到模拟器:

   .. zephyr-app-commands::
      :zephyr-app: tests/drivers/sensor/bmi160
      :board: native_sim
      :goals: build

#. 可以使用第二个 EEPROM 构建相同的测试，该 EEPROM 是通过 I2C 连接到模拟器的 Atmel AT24 EEPROM 驱动程序:

   .. zephyr-app-commands::
      :zephyr-app: tests/drivers/eeprom/api
      :board: native_sim
      :goals: build
      :gen-args: -DDTC_OVERLAY_FILE=at2x_emul.overlay -DEXTRA_CONF_FILE=at2x_emul.conf

API 参考 (API Reference)
=========================

.. doxygengroup:: io_emulators
