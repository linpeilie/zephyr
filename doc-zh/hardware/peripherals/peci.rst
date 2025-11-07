.. _peci_api:

平台环境控制接口 (Platform Environment Control Interface, PECI)
#################################################################

概述 (Overview)
****************
平台环境控制接口,缩写为 PECI,是 2006 年与 Intel Core 2 Duo 微处理器一起引入的热管理标准。PECI 接口允许外部设备读取处理器温度、执行处理器可管理性功能,并管理处理器接口调优和诊断。PECI 总线驱动程序 API 支持嵌入式微控制器和 CPU 之间的交互。

配置选项 (Configuration Options)
*********************************

相关配置选项:

* :kconfig:option:`CONFIG_PECI`

API 参考 (API Reference)
*************************

.. doxygengroup:: peci_interface
