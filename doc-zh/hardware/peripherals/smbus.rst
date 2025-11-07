.. _smbus_api:

系统管理总线 (System Management Bus, SMBus)
#############################################

.. contents::
    :local:
    :depth: 2

概述 (Overview)
****************

系统管理总线 (SMBus, System Management Bus) 源自 I2C,用于与主板上的设备通信。系统可以使用 SMBus 与主板上的外设通信,而无需使用专用控制线。SMBus 外设可以提供各种制造商信息、报告错误、接受控制参数等。

总线上的设备可以以三种角色运行:作为启动事务并控制时钟的控制器 (Controller)、响应事务命令的外设 (Peripheral),或作为主机 (Host),这是一种专用控制器,为系统的 CPU 提供主要接口。Zephyr 具有控制器角色的 API。

SMBus 外设设备可以通过两种方法启动与控制器的通信:

* **主机通知协议 (Host Notify protocol)**:支持主机通知协议的外设设备充当控制器来执行通知。它将三字节消息写入特殊地址 "SMBus Host (0x08)",其中包含自己的地址和两字节的相关数据。
* **SMBALERT# 信号**:外设设备使用特殊信号 SMBALERT# 来请求控制器的注意。控制器需要从特殊的 "SMBus Alert Response Address (ARA) (0x0c)" 读取一个字节。外设设备用包含其自己地址的数据字节响应。

目前,该 API 基于 `SMBus Specification`_ 版本 2.0

.. note::
   有关此 API 中使用的术语的信息,请参阅 :ref:`coding_guideline_inclusive_language`。

.. _smbus-controller-api:

SMBus 控制器 API (SMBus Controller API)
*****************************************

当 SMBus 设备控制总线时使用 Zephyr 的 SMBus 控制器 API,特别是启动和停止条件以及时钟。这是用于与 SMBus 外设交互的最常见模式。

配置选项 (Configuration Options)
*********************************

相关配置选项:

* :kconfig:option:`CONFIG_SMBUS`

API 参考 (API Reference)
*************************

.. doxygengroup:: smbus_interface

.. _SMBus Specification: https://smbus.org/specs/smbus20.pdf
