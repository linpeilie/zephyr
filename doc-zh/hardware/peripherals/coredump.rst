.. _coredump_device_api:

核心转储设备 (Coredump Device)
################################

概述 (Overview)
****************

核心转储设备是一个具有两种类型的伪设备驱动程序。COREDUMP_TYPE_MEMCPY 类型公开设备树绑定,用于将内存地址/大小值包含在任何转储中。驱动程序公开一个 API 以在运行时添加/删除转储内存区域。COREDUMP_TYPE_CALLBACK 设备在 memory-regions 数组中恰好需要一个大小为 0 和所需大小的条目。驱动程序将静态分配所需大小的内存,并提供 API 以注册回调函数,以便在转储发生时填充该内存。

配置选项 (Configuration Options)
*********************************

相关配置选项:

* :kconfig:option:`CONFIG_COREDUMP_DEVICE`

API 参考 (API Reference)
*************************

.. doxygengroup:: coredump_device_interface
