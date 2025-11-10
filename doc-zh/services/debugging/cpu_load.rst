.. _cpu_load:

CPU负载 (CPU load)
##################

该模块可用于跟踪空闲时间占用了多少时间 (Module can be used to track how much time is spent in idle)。它使用在CPU进入和退出空闲状态之前和之后调用的跟踪钩子 (It is using tracing hooks which are called before and after CPU goes to idle)。与 :ref:`thread_analyzer` 相比,它更准确,因为它也考虑了在中断上下文中花费的时间 (Compared to :ref:`thread_analyzer` it is more accurate since it takes into account time spent in the interrupt context as well)。

函数 :c:func:`cpu_load_get` 用于获取最新值 (Function :c:func:`cpu_load_get` is used to get the latest value)。它也用于重置测量 (It is also used to reset the measurement)。默认情况下,模块使用 :c:func:`k_cycle_get_32`,但在需要更高精度的情况下,可以使用 :ref:`counter_api` 设备 (By default, module is using :c:func:`k_cycle_get_32` but in cases when higher precision is needed a :ref:`counter_api` device can be used)。

负载也可以使用日志消息定期报告 (Load can also be reported periodically using a logging message)。周期使用 :kconfig:option:`CONFIG_CPU_LOAD_LOG_PERIODICALLY` 配置 (Period is configured using :kconfig:option:`CONFIG_CPU_LOAD_LOG_PERIODICALLY`)。

使用计数器设备 (Using counter device)
********************

为了使用 :ref:`counter_api` 设备,必须启用 :kconfig:option:`CONFIG_CPU_LOAD_USE_COUNTER` 并且必须在设备树中设置chosen (In order to use :ref:`counter_api` device :kconfig:option:`CONFIG_CPU_LOAD_USE_COUNTER` must be enabled and chosen in devicetree must be set)。

.. code-block:: devicetree

   chosen {
     zephyr,cpu-load-counter = &counter_device;
   };
