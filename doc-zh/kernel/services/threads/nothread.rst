.. _nothread:

无线程操作
##########

在某些应用程序中不需要线程支持：

* 引导加载程序 (Bootloaders)
* 简单的事件驱动应用程序
* 旨在演示核心功能的示例

可以通过将 :kconfig:option:`CONFIG_MULTITHREADING` 设置为 ``n`` 来禁用线程支持。
由于此配置对 Zephyr 的功能有重大影响，并且对其的测试有限，因此对此配置中可以期望工作的内容有一定的条件。

可以期望工作的功能
******************

当 :kconfig:option:`CONFIG_MULTITHREADING` 被禁用时，这些核心功能应能正确运行：

* :ref:`构建系统 <application>`

* 将应用程序引导到 ``main()`` 的能力

* :ref:`中断管理 <interrupts_v2>`

* 系统时钟，包括 :c:func:`k_uptime_get`

* 定时器 (Timers)，即 :c:func:`k_timer`

* 非睡眠延迟，例如 :c:func:`k_busy_wait`。

* 睡眠 :c:func:`k_cpu_idle`。

* ``main()`` 之前的驱动程序和子系统初始化，例如 :c:macro:`SYS_INIT`。

* :ref:`kernel_memory_management_api`

* 某些子系统中特定标识的驱动程序，如下所列。

上述期望会影响其他功能的选择；例如 :kconfig:option:`CONFIG_SYS_CLOCK_EXISTS` 不能设置为 ``n``。

不能期望工作的功能
******************

使用 :kconfig:option:`CONFIG_MULTITHREADING` 无法工作的功能包括大部分内核 API：

* :ref:`threads_v2`

* :ref:`scheduling_v2`

* :ref:`workqueues_v2`

* :ref:`polling_v2`

* :ref:`semaphores_v2`

* :ref:`mutexes_v2`

* :ref:`condvar`

* :ref:`kernel_data_passing_api`

.. contents::
    :local:
    :depth: 1

没有线程支持的子系统行为
************************

以下各节列出了在禁用 :kconfig:option:`CONFIG_MULTITHREADING` 时预期在某种程度上工作的驱动程序和功能子系统。
此处未列出的子系统不应期望能够工作。

列出的子系统中的一些现有驱动程序在禁用线程时无法工作，但基于其子系统在范围内，
或者可能足够隔离，以至于在特定平台上支持它们的影响较低。
将考虑增强功能以向原本未实现为在禁用线程时工作的现有功能添加支持。

Flash
=====

:ref:`flash_api` 预期对所有 SoC flash 外设驱动程序都有效。总线访问设备（如串行存储器）可能不受支持。

*支持的驱动程序列表/表将在此处显示*

GPIO
====

:ref:`gpio_api` 预期对所有 SoC GPIO 外设驱动程序都有效。总线访问设备（如 GPIO 扩展器）可能不受支持。

*支持的驱动程序列表/表将在此处显示*

UART
====

:ref:`uart_api` 的一个子集预期对所有 SoC UART 外设驱动程序都有效。

* 选择 :kconfig:option:`CONFIG_UART_INTERRUPT_DRIVEN` 的应用程序可能会工作，具体取决于驱动程序实现。

* 选择 :kconfig:option:`CONFIG_UART_ASYNC_API` 的应用程序可能会工作，具体取决于驱动程序实现。

* 既不选择 :kconfig:option:`CONFIG_UART_ASYNC_API` 也不选择 :kconfig:option:`CONFIG_UART_INTERRUPT_DRIVEN`
  的应用程序预期会工作。

*支持的驱动程序列表/表将在此处显示，包括支持哪些 API 选项*
