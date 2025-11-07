.. _gnss_api:

GNSS (全球导航卫星系统, Global Navigation Satellite System)
############################################################

概述 (Overview)
****************

GNSS 是一个通用术语,涵盖用于导航的卫星系统,如 GPS (Global Positioning System, 全球定位系统)。GNSS 服务通常通过 GNSS 调制解调器访问,该调制解调器接收和处理 GNSS 信号以确定其位置,或更具体地说,其天线位置。它们通常还提供精确的时间同步机制,通常称为 PPS (Pulse-Per-Second, 每秒脉冲)。

子系统支持 (Subsystem Support)
********************************

GNSS 子系统基于 :ref:`modem`。GNSS 子系统涵盖从向调制解调器发送和接收命令到解析、创建和处理 NMEA0183 消息的所有内容。

为基于 NMEA0183 的其他 GNSS 调制解调器添加支持仅需要为特定 GNSS 调制解调器实现电源管理和配置即可。

为使用其他协议和/或总线(而不是通常的 NMEA0183 over UART)的 GNSS 调制解调器添加支持是可能的,但需要驱动程序开发人员做更多的工作。

配置选项 (Configuration Options)
*********************************

相关配置选项:

* :kconfig:option:`CONFIG_GNSS`
* :kconfig:option:`CONFIG_GNSS_SATELLITES`
* :kconfig:option:`CONFIG_GNSS_DUMP_TO_LOG`

导航参考 (Navigation Reference)
********************************

.. doxygengroup:: navigation

GNSS API 参考 (GNSS API Reference)
***********************************

.. doxygengroup:: gnss_interface
