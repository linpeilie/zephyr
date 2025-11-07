.. _tcpc_api:

USB Type-C 端口控制器 (USB Type-C Port Controller, TCPC)
##########################################################

概述 (Overview)
****************

`TCPC <tcpc-specification_>`_ (USB Type-C Port Controller, USB Type-C 端口控制器)
TCPC 是一种用于简化 USB-C 系统实现的设备,通过提供以下三个功能:

* VBUS 和 VCONN 控制 `USB Type-C <usb-type-c-specification_>`_:
  TCPC 可以为源设备提供控制 VBUS 供电的机制,为接收设备提供控制 VBUS 吸收的机制。为控制 VCONN 提供了类似的机制。

* CC 控制和感测:
  TCPC 实现用于控制 CC 引脚上拉和下拉电阻的逻辑。它还提供了一种感测和报告 CC 引脚上存在哪些电阻的方法。

* 电力传输消息接收和传输 `USB Power Delivery <usb-pd-specification_>`_:
  TCPC 发送和接收在 TCPM 中构造的消息,并将它们放在 CC 线上。

.. _tcpc-api:

TCPC API
========

TCPC 设备驱动程序充当 TCPC 设备和应用程序软件之间的联络;这是通过设备驱动程序提供的 Zephyr API 来实现的,该 API 用于与 TCPC 设备通信并控制它。

配置选项 (Configuration Options)
*********************************

相关配置选项:

* :kconfig:option:`CONFIG_USBC_TCPC_DRIVER`

API 参考 (API Reference)
*************************

.. doxygengroup:: usb_type_c
.. doxygengroup:: usb_type_c_port_controller_api
.. doxygengroup:: usb_power_delivery

.. _tcpc-specification:
   https://www.usb.org/document-library/usb-type-cr-port-controller-interface-specification

.. _usb-type-c-specification:
   https://www.usb.org/document-library/usb-type-cr-cable-and-connector-specification-revision-21

.. _usb-pd-specification:
   https://www.usb.org/document-library/usb-power-delivery
