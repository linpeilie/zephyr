.. _i2c_api:

集成电路间总线 (Inter-Integrated Circuit, I2C) 总线
####################################################

概述 (Overview)
****************

.. note::

   Zephyr I2C API 中使用的术语遵循 `NXP I2C Bus Specification Rev 7.0 <i2c-specification_>`_。这些术语自 2021 年 10 月 1 日发布以来与以前的版本有所不同。

`I2C`_ (Inter-Integrated Circuit,发音为"eye squared see")是一种常用的双信号共享外设接口总线。许多片上系统解决方案提供了在 I2C 总线上通信的控制器。总线上的设备可以以两种角色运行:作为启动事务并控制时钟的"控制器 (controller)",或作为响应事务命令的"目标 (target)"。给定 SoC 上的 I2C 控制器通常支持控制器角色,有些还将支持目标模式。Zephyr 为两种角色都提供了 API。

.. _i2c-controller-api:

I2C 控制器 API (I2C Controller API)
=====================================

当 I2C 外设控制总线时使用 Zephyr 的 I2C 控制器 API,特别是启动和停止条件以及时钟。这是最常见的模式,用于与传感器和串行存储器等 I2C 设备交互。

此 API 在所有树内 I2C 外设驱动程序中受支持,并被认为是稳定的。

.. _i2c-target-api:

I2C 目标 API (I2C Target API)
===============================

当 I2C 外设响应总线上不同控制器发起的事务时,使用 Zephyr 的 I2C 目标 API。它可能用于具有由其他设备(如主机处理器)控制的传感器角色的 Zephyr 应用程序。

此 API 在很少的树内 I2C 外设驱动程序中受支持。该 API 被认为是实验性的,因为它与控制器模式下支持的所有 I2C 外设的功能不兼容。


配置选项 (Configuration Options)
*********************************

相关配置选项:

* :kconfig:option:`CONFIG_I2C`

API 参考 (API Reference)
*************************

.. doxygengroup:: i2c_interface

.. _i2c-specification:
   https://www.nxp.com/docs/en/user-guide/UM10204.pdf

.. _I2C: i2c-specification_
