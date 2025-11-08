.. _cpu_freq:

CPU频率调节 (CPU Frequency Scaling)
####################################

.. toctree::
   :maxdepth: 1

   policies/index.rst

概述 (Overview)
****************

Zephyr中的CPU频率调节子系统提供了一个框架,允许SoC根据监控的指标和性能状态(P-state)策略算法动态调整处理器频率 (The CPU Frequency Scaling subsystem in Zephyr provides a framework for SoC's to dynamically adjust their processor frequency based on a monitored metric and performance state (P-state) policy algorithm)。

设计目标 (Design Goals)
*************************

CPU频率调节子系统旨在提供一个框架,允许任何策略算法与任何P-state驱动程序配合工作,并允许每个策略利用一个或多个指标来确定最佳CPU频率 (The CPU Frequency Scaling subsystem aims to provide a framework that allows for any policy algorithm to work with any P-state driver and allows for each policy to make use of one, or many, metrics to determine an optimal CPU frequency)。该子系统应足够灵活,以允许SoC供应商定义自定义P-state、阈值和指标 (The subsystem should be flexible enough to allow for SoC vendors to define custom P-states, thresholds and metrics)。

P-state策略 (P-state Policies)
*******************************

P-state策略是一种算法,根据其消耗的指标和每个P-state定义的阈值来确定CPU的最佳P-state (A P-state policy is an algorithm that determines what the optimal P-state is for the CPU based on the metrics it consumes and the thresholds defined per P-state)。一个策略可以消耗一个或多个指标,以根据系统所需的统计数据确定最佳CPU频率 (A policy can consume one, or many, metrics to determine the optimal CPU frequency based on the desired statistics of the system)。

有关标准策略列表,请参阅 :ref:`策略 <cpu_freq_policies>` (See :ref:`policies <cpu_freq_policies>` for a list of standard policies)。

指标 (Metrics)
***************

P-state策略应包含一个或多个指标作为决策依据 (A P-state policy should include one or more metrics to base decisions)。指标示例可能包括CPU负载百分比、SoC温度等 (Examples of metrics could include percent CPU load, SoC temperature, etc)。

有关正在使用的指标示例,请参阅 :ref:`按需 <on_demand_policy>` 策略 (For an example of a metric in use, see the :ref:`on_demand <on_demand_policy>` policy)。

P-state驱动程序 (P-state Drivers)
**********************************

支持CPU频率子系统的SoC必须实现一个P-state驱动程序,该驱动程序实现 :c:func:`cpu_freq_pstate_set` 函数,在调用时将传入的 ``p_state`` 应用到CPU (A SoC supporting the CPU Freq subsystem must implement a P-state driver that implements :c:func:`cpu_freq_pstate_set` which applies the passed in ``p_state`` to the CPU when called)。

SoC还必须通过具有 :dtcompatible:`zephyr,pstate` 兼容节点在设备树中提供可用的P-state (A SoC must also provide the available P-states in devicetree by having a :dtcompatible:`zephyr,pstate` compatible node)。SoC也可以定义自己的P-state绑定,该绑定扩展 :dtcompatible:`zephyr,pstate` 以包含SoC的P-state驱动程序可能使用的其他属性 (The SoC may also define its own P-state binding, which extends :dtcompatible:`zephyr,pstate` to include additional properties that may be used by the SoC's P-state driver)。

使用注意事项 (Usage considerations)
************************************

CPU频率调节子系统设计用于在UP和SMP系统上工作 (The CPU Frequency Scaling subsystem is designed to work on both UP and SMP system)。在SMP系统上,默认假设每个CPU以相同的速率运行 (On SMP systems, it is assumed by default that each of the CPUs are clocked at the same rate)。因此,如果一个CPU经历P-state转换,那么所有其他CPU也将经历相同的P-state转换 (Thus, should one CPU undergo a P-state transition, then all other CPUs will also undergo the same P-state transition)。这可以通过SoC启用 :kconfig:option:`CONFIG_CPU_FREQ_PER_CPU_SCALING` 配置选项来覆盖,以允许每个CPU独立时钟 (This can be overridden by the SoC by enabling the :kconfig:option:`CONFIG_CPU_FREQ_PER_CPU_SCALING` configuration option to allow each CPU to be clocked independently)。

支持CPU频率的SoC必须维护Zephyr的要求,即系统定时器在程序的生命周期内保持恒定 (The SoC supporting CPU Freq must uphold Zephyr's requirement that the system timer remains constant over the lifetime of the program)。有关更多信息,请参阅 :ref:`内核定时 <kernel_timing>` (See :ref:`Kernel Timing <kernel_timing>` for more information)。

CPU频率调节子系统作为 ``k_timer`` 的处理函数运行,这意味着它在中断上下文(IRQ)中运行 (The CPU Frequency Scaling subsystem runs as a handler function to a ``k_timer``, which means it runs in interrupt context (IRQ))。SoC P-state驱动程序必须确保其 :c:func:`cpu_freq_pstate_set` 的实现是IRQ上下文安全的 (The SoC P-state driver must ensure that its implementation of :c:func:`cpu_freq_pstate_set` is IRQ context safe)。如果P-state转换无法在IRQ上下文中合理完成,建议SoC的P-state驱动程序将其任务实现为工作队列项 (If a P-state transition cannot be completed reasonably in an IRQ context, it is recommended that the P-state driver of the SoC implements its task as a workqueue item)。
