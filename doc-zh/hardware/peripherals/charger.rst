.. _charger_api:

充电器 (Chargers)
##################

充电器子系统公开了一个 API 以统一访问电池充电器设备。

充电器设备或充电器外设是一种设备,用于接收提供给系统的外部电源作为输入,并向电池组和系统下游提供电源作为输出。充电器设备可以作为模块、集成电路或电源管理集成电路 (PMIC, Power Management Integrated Circuit) 中的功能模块存在。

为电池组充电的动作称为充电周期 (charge cycle)。当执行充电周期时,电池组根据充电器设备上配置的充电配置文件 (charge profile) 进行充电。充电配置文件在制造商提供的电池组规格中定义。在具有控制端口的充电器设备上,充电配置文件可以由主机控制器通过设置相关属性进行配置,并且可以在运行时进行调整以响应环境变化。

基本操作 (Basic Operation)
****************************

启动充电周期 (Initiating a Charge Cycle)
=========================================

充电周期通过 :c:func:`charger_charge_enable` 启动或终止。

属性 (Properties)
==================

从根本上说,属性是充电器设备可以测量的可配置设置、状态或数量。

充电器通常支持多个属性,例如电池组的温度读数或当前时间的电流/电压。

客户端使用 :c:func:`charger_get_prop` 一次获取一个属性。
客户端使用 :c:func:`charger_set_prop` 一次设置一个属性。

.. _charger_api_reference:

API 参考 (API Reference)
*************************

.. doxygengroup:: charger_interface
