.. _emulators:

Zephyr 设备仿真器/模拟器
#########################

概述
====

Zephyr 代码库包含一组设备仿真器/模拟器。它们是与嵌入式软件一同构建的软组件，
在系统中以某类设备的形式对外呈现。

这些设备仿真器/模拟器可在任何具备足够 RAM 与 Flash 的目标上构建，
尽管其中一些额外功能可能仅在部分目标上可用。

.. note::

   | Zephyr 还包含并使用了许多其它类型的模拟器/仿真器，例如 CPU 与平台模拟器、
     射频模拟器，以及允许在开发主机上运行嵌入式代码的若干构建目标。
   | 部分通信控制器/驱动也包含环回模式或环回设备。
   | 本页不涵盖以上内容。

.. note::
   针对特定平台的驱动（如 :ref:`native_sim specific drivers <native_sim_peripherals>`），
   通过连接宿主机 API 来模拟外设类别的，不在本页范围内。


可用仿真器
==========

**ADC 仿真器**
  * 伪造的 ADC 驱动，可用于测试更高层的 ADC 设备 API。
  * 主要 Kconfig 选项：:kconfig:option:`CONFIG_ADC_EMUL`
  * 设备树绑定：:dtcompatible:`zephyr,adc-emul`

**DMA 仿真器**
  * 模拟的 DMA 控制器
  * 主要 Kconfig 选项：:kconfig:option:`CONFIG_DMA_EMUL`
  * 设备树绑定：:dtcompatible:`zephyr,dma-emul`

**EEPROM 仿真器**
  * 在某个 Flash 分区上模拟 EEPROM
  * 主要 Kconfig 选项：:kconfig:option:`CONFIG_EEPROM_EMULATOR`
  * 设备树绑定：:dtcompatible:`zephyr,emu-eeprom`

.. _emul_eeprom_simu_brief:

**EEPROM 模拟器**
  * 在 RAM 上模拟 EEPROM
  * 主要 Kconfig 选项：:kconfig:option:`CONFIG_EEPROM_SIMULATOR`
  * 设备树绑定：:dtcompatible:`zephyr,sim-eeprom`
  * 说明：对于 :zephyr:board:`native 目标 <native_sim>`，也可将内容保存在宿主机文件系统文件中。

**外部总线及其外设仿真器**
  * :ref:`文档 <bus_emul>`
  * 支持模拟 I2C、SPI 等外部总线及其挂接的外设。

.. _emul_flash_simu_brief:

**Flash 模拟器**
  * 在 RAM 上模拟 Flash
  * 主要 Kconfig 选项：:kconfig:option:`CONFIG_FLASH_SIMULATOR`
  * 设备树绑定：:dtcompatible:`zephyr,sim-flash`
  * 说明：对于 native 目标，也可将内容保存在宿主机文件系统文件中，参见
    :ref:`native_sim 的 Flash 模拟器 <nsim_per_flash_simu>`。

**GPIO 仿真器**
  * 可由软件驱动的 GPIO 控制器仿真
  * 主要 Kconfig 选项：:kconfig:option:`CONFIG_GPIO_EMUL`
  * 设备树绑定：:dtcompatible:`zephyr,gpio-emul`

**I2C 仿真器**
  * I2C 总线仿真，见 :ref:`总线仿真器 <bus_emul>`。
  * 主要 Kconfig 选项：:kconfig:option:`CONFIG_I2C_EMUL`
  * 设备树绑定：:dtcompatible:`zephyr,i2c-emul-controller`

**RTC 仿真器**
  * RTC 外设仿真，见 :ref:`RTC 仿真设备章节 <rtc_api_emul_dev>`
  * 主要 Kconfig 选项：:kconfig:option:`CONFIG_RTC_EMUL`
  * 设备树绑定：:dtcompatible:`zephyr,rtc-emul`

**SPI 仿真器**
  * SPI 总线仿真，见 :ref:`总线仿真器 <bus_emul>`。
  * 主要 Kconfig 选项：:kconfig:option:`CONFIG_SPI_EMUL`
  * 设备树绑定：:dtcompatible:`zephyr,spi-emul-controller`

**MSPI 仿真器**
  * MSPI 总线仿真，见 :ref:`总线仿真器 <bus_emul>`。
  * 主要 Kconfig 选项：:kconfig:option:`CONFIG_MSPI_EMUL`
  * 设备树绑定：:dtcompatible:`zephyr,mspi-emul-controller`

**UART 仿真器**
  * UART 总线仿真，见 :ref:`总线仿真器 <bus_emul>`。
  * 主要 Kconfig 选项：:kconfig:option:`CONFIG_UART_EMUL`
  * 设备树绑定：:dtcompatible:`zephyr,uart-emul`
