.. _flash_api:

闪存
####

概述
****

**闪存偏移概念**

用户 API 使用的偏移量是相对于闪存起始地址表示的。此规则应适用于所有闪存控制器
常规内存,其布局可通过 API 检索页面布局(参见 :kconfig:option:`CONFIG_FLASH_PAGE_LAYOUT`)。

此规则的例外可能适用于供应商特定的闪存专用区域(这样的区域显然不能通过 API 检索
页面布局来涵盖)。



用户 API 参考
*************
.. doxygengroup:: flash_interface

实现接口 API 参考
******************
.. doxygengroup:: flash_internal_interface
