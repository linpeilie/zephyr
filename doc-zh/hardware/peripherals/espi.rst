.. _espi_api:

增强型串行外设接口 (Enhanced Serial Peripheral Interface, eSPI) 总线
######################################################################

概述 (Overview)
****************

eSPI (增强型串行外设接口, enhanced serial peripheral interface) 是一种基于 SPI 的串行总线。它还具有四线接口(接收、发送、时钟和目标选择)和三种配置:单 IO、双 IO 和四 IO。

技术进步包括更低的电压信号电平 (1.8V vs. 3.3V)、更少的引脚数,频率是原来的两倍 (66MHz vs. 33MHz)。由于其增强功能,eSPI 用于取代 LPC (lower pin count, 低引脚数) 接口、SPI、SMBus 和边带信号。

有关其他详细信息,请参阅 `eSPI 接口规范`_。


API 参考 (API Reference)
*************************

.. doxygengroup:: espi_interface

.. _eSPI 接口规范:
    https://downloadmirror.intel.com/27055/327432%20espi_base_specification%20R1-5.pdf
