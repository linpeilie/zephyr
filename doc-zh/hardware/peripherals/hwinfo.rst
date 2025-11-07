.. _hwinfo_api:

硬件信息 (Hardware Information)
################################

概述 (Overview)
****************

硬件信息 API 提供对硬件信息的访问,例如设备标识符和复位原因标志。

复位原因标志可用于确定设备为何复位;例如由于看门狗超时或电源循环。不同的设备支持不同的标志子集。使用 :c:func:`hwinfo_get_supported_reset_cause` 检索该设备支持的标志。

配置选项 (Configuration Options)
*********************************

相关配置选项:

* :kconfig:option:`CONFIG_HWINFO`

API 参考 (API Reference)
*************************

.. doxygengroup:: hwinfo_interface
