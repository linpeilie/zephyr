.. _auxdisplay_api:

辅助显示器 (Auxiliary Display, auxdisplay)
###########################################

概述 (Overview)
****************

辅助显示器是基于文本的显示器，具有用于显示文本、数字或字母数字数据的简单接口，
与 :ref:`display_api` 不同，辅助显示器不支持自定义图形输出到显示器(并且通常是单色的)，
支持的最高级自定义功能是生成自定义字符。
这些廉价的显示器通常以各种配置和尺寸出现，常见的显示尺寸是 16 个字符乘 2 行。

此 API 不稳定，可能会更改。

配置选项 (Configuration Options)
**********************************

相关配置选项:

* :kconfig:option:`CONFIG_AUXDISPLAY`
* :kconfig:option:`CONFIG_AUXDISPLAY_INIT_PRIORITY`

API 参考 (API Reference)
*************************

.. doxygengroup:: auxdisplay_interface
