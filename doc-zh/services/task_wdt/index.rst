.. _task_wdt_api:

任务看门狗
#############

概述
********

许多微控制器都具有硬件看门狗定时器外设。其目的是在发生严重软件故障时触发操作(通常是系统复位)。一旦初始化,看门狗定时器必须定期重新启动("喂狗")以防止其超时。如果软件卡住并且无法再喂狗,则会触发纠正操作以使系统恢复正常运行。

在并行运行多个任务的实时操作系统中,单个看门狗实例可能不再足够,因为它只能用于一个任务。这个基于内核定时器的软件看门狗提供了一种监督多个线程或任务(称为看门狗通道)的方法。

如果任务看门狗本身或调度器出现故障,可以使用现有的硬件看门狗作为可选后备。

任务看门狗使用内核定时器作为其后端。如果配置正确,在正常操作期间实际上永远不会调用定时器 ISR,因为定时器在喂狗调用中会持续更新。

目前不可能有多个任务看门狗实例。相反,任务看门狗 API 可以全局访问以添加或删除新通道,而无需在固件中传递上下文或设备指针。

通道的最大数量通过 Kconfig 预定义,应调整为与应用所需的通道数完全匹配。

配置选项
*********************

相关配置选项可以在 :zephyr_file:`subsys/task_wdt/Kconfig` 下找到。

* :kconfig:option:`CONFIG_TASK_WDT`

* :kconfig:option:`CONFIG_TASK_WDT_CHANNELS`

* :kconfig:option:`CONFIG_TASK_WDT_HW_FALLBACK`

* :kconfig:option:`CONFIG_TASK_WDT_MIN_TIMEOUT`

* :kconfig:option:`CONFIG_TASK_WDT_HW_FALLBACK_DELAY`

API 参考
*************

.. doxygengroup:: task_wdt_api
