.. _fuel_gauge_api:

油量计 (Fuel Gauge)
####################

油量计子系统公开了一个 API 以统一访问电池油量计设备。

基本操作 (Basic Operation)
****************************

属性 (Properties)
==================

从根本上说,属性是油量计设备可以测量的数量。

油量计通常支持多个属性,例如电池组的温度读数或当前时间的电流/电压。

客户端使用 :c:func:`fuel_gauge_get_prop` 一次获取一个属性,或使用 :c:func:`fuel_gauge_get_props` 批量获取。缓冲区属性(例如设备名称)使用 :c:func:`fuel_gauge_get_buffer_prop` 获取。

客户端使用 :c:func:`fuel_gauge_set_prop` 一次设置一个属性,或使用 :c:func:`fuel_gauge_set_props` 批量设置。

电池切断 (Battery Cutoff)
===========================

许多嵌入在电池组中的油量计公开了一个寄存器地址,当使用特定有效载荷写入时会执行电池切断。由于其在减少设备存储或运输时的电池消耗方面的实用性,此电池切断通常被称为船运 (ship)、货架 (shelf) 或睡眠 (sleep) 模式。

油量计 API 通过 :c:func:`fuel_gauge_battery_cutoff` 函数公开电池切断功能。

缓存 (Caching)
===============

油量计 API 明确不为其客户端提供缓存。


.. _fuel_gauge_api_reference:

API 参考 (API Reference)
*************************

.. doxygengroup:: fuel_gauge_interface
.. doxygengroup:: fuel_gauge_emulator_backend
