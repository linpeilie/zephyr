.. _led_api:

发光二极管 (Light-Emitting Diode, LED)
########################################

概述 (Overview)
****************

LED API 提供对发光二极管的访问,包括单个和灯带形式。

配置选项 (Configuration Options)
*********************************

相关配置选项:

* :kconfig:option:`CONFIG_LED`
* :kconfig:option:`CONFIG_LED_STRIP`

API 参考 (API Reference)
*************************

LED
===

.. doxygengroup:: led_interface

LED 灯带 (LED Strip)
=====================

.. doxygengroup:: led_strip_interface
