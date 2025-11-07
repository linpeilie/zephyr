.. _mdio_api:

管理数据输入/输出 (Management Data Input/Output, MDIO)
########################################################

概述 (Overview)
****************

MDIO 是一种常用于与以太网 PHY 设备通信的总线。许多以太网 MAC 控制器还提供硬件以通过 MDIO 总线与外设设备通信。

此 API 主要供 PHY 驱动程序使用,但也可以由用户固件使用。

API 参考 (API Reference)
*************************

.. doxygengroup:: mdio_interface
