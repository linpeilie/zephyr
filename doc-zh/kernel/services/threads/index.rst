.. _threads_v2:

线程
####

.. note::
   还提供对使用 :ref:`nothread` 的有限支持。

.. contents::
    :local:
    :depth: 2

本节描述用于创建、调度和删除独立可执行指令线程的内核服务。

:dfn:`线程` 是用于应用程序处理的内核对象,这些处理对于 ISR 来说太冗长或太复杂。

应用程序可以定义任意数量的线程(仅受可用 RAM 限制)。每个线程在生成时都会被分配一个
:dfn:`线程 ID` 进行引用。

线程具有以下关键属性:

* **堆栈区域**,这是用于线程堆栈的内存区域。堆栈区域的**大小**可以定制以符合线程处理
  的实际需求。存在特殊的宏来创建和使用堆栈内存区域。

* **线程控制块**,用于内核对线程元数据进行私有簿记。这是类型 :c:struct:`k_thread` 的实例。

* **入口点函数**,在线程启动时调用。最多可以将 3 个**参数值**传递给此函数。

* **调度优先级**,指示内核调度器如何为线程分配 CPU 时间。(参见 :ref:`scheduling_v2`。)

* 一组**线程选项**,允许线程在特定情况下接受内核的特殊处理。
  (参见 :ref:`thread_options_v2`。)

* **启动延迟**,指定内核在启动线程之前应等待多长时间。

* **执行模式**,可以是监督者模式或用户模式。默认情况下,线程在监督者模式下运行,
  允许访问特权 CPU 指令、整个内存地址空间和外设。用户模式线程具有减少的特权集。
  这取决于 :kconfig:option:`CONFIG_USERSPACE` 选项。参见 :ref:`usermode_api`。

.. _lifecycle_v2:

生命周期
********

.. _spawning_thread:

线程创建
========

线程在使用之前必须先创建。内核初始化线程控制块以及堆栈部分的一端。线程堆栈的其余
部分通常保持未初始化状态。

指定 :c:macro:`K_NO_WAIT` 的启动延迟会指示内核立即开始线程执行。或者,可以通过
指定超时值来指示内核延迟执行线程 -- 例如,允许线程使用的设备硬件变为可用。

内核允许在线程开始执行之前取消延迟启动。如果线程已经启动,取消请求无效。成功取消
延迟启动的线程必须重新生成才能使用。

线程终止
========

一旦线程启动,它通常会永远执行。但是,线程可以通过从其入口点函数返回来同步结束其
执行。这称为**终止**。

终止的线程负责在返回之前释放它可能拥有的任何共享资源(如互斥锁和动态分配的内存),
因为内核*不会*自动回收它们。

在某些情况下,线程可能希望睡眠,直到另一个线程终止。这可以通过 :c:func:`k_thread_join`
API 来完成。这将阻塞调用线程,直到超时到期、目标线程自行退出或目标线程中止(由于
:c:func:`k_thread_abort` 调用或触发致命错误)。

一旦线程终止,内核保证不会使用线程结构。然后,此类结构的内存可以重新用于任何目的,
包括生成新线程。请注意,线程必须完全终止,这会出现竞态条件,其中线程自己的逻辑发出
完成信号,另一个线程在内核处理完成之前看到该信号。在正常情况下,应用程序代码应使用
:c:func:`k_thread_join` 或 :c:func:`k_thread_abort` 来同步线程终止状态,而不是
依赖应用程序逻辑内的信号。

线程中止
========

线程可以通过**中止**异步结束其执行。如果线程触发致命错误条件,例如取消引用空指针,
内核会自动中止线程。

线程也可以被另一个线程(或其自身)通过调用 :c:func:`k_thread_abort` 中止。但是,
通常最好向线程发出信号以使其自行优雅终止,而不是中止它。

与线程终止一样,内核不会回收被中止线程拥有的共享资源。

.. note::
    内核目前没有就应用程序重新生成中止线程的能力做出任何声明。

线程挂起
========

如果线程变为**挂起**状态,则可以阻止其无限期执行。函数 :c:func:`k_thread_suspend`
可用于挂起任何线程,包括调用线程。挂起已经挂起的线程没有额外影响。

一旦挂起,线程就不能被调度,直到另一个线程调用 :c:func:`k_thread_resume` 移除挂起。

.. note::
   线程可以使用 :c:func:`k_sleep` 阻止自己执行指定的时间段。但是,这与挂起线程
   不同,因为睡眠线程在达到时间限制时自动变为可执行状态。

.. _thread_states:

线程状态
********

没有阻止其执行的因素的线程被视为**就绪**,并且有资格被选为当前线程。

具有一个或多个阻止其执行的因素的线程被视为**未就绪**,不能被选为当前线程。

以下因素使线程未就绪:

* 线程尚未启动。
* 线程正在等待内核对象完成操作。(例如,线程正在获取不可用的信号量。)
* 线程正在等待超时发生。
* 线程已被挂起。
* 线程已终止或中止。

  .. image:: thread_states.svg
     :align: center

.. note::

  尽管上图可能似乎暗示**就绪**和**运行**都是不同的线程状态,但这不是正确的解释。
  **就绪**是线程状态,而**运行**是仅适用于**就绪**线程的调度状态。

线程堆栈对象
************

每个线程都需要自己的堆栈缓冲区供 CPU 推送上下文。根据配置,必须满足几个约束:

- 可能需要为内存管理结构保留额外的内存
- 如果启用了基于保护的堆栈溢出检测,则必须在堆栈缓冲区之前立即设置一个小的写保护
  内存管理区域以捕获溢出。
- 如果启用了用户空间,则必须保留单独的固定大小特权提升堆栈,以用作处理系统调用的
  私有内核堆栈。
- 如果启用了用户空间,则线程的堆栈缓冲区必须适当调整大小和对齐,以便可以编程内存
  保护区域以完全适合。

对齐约束可能相当严格,例如,一些 MPU 要求它们的区域大小为某个 2 的幂,并与其自身
大小对齐。

因此,可移植代码不能简单地将任意字符缓冲区传递给 :c:func:`k_thread_create`。
存在特殊的宏来静态实例化堆栈,前缀为 ``K_KERNEL_STACK`` 和 ``K_THREAD_STACK``。

此外,可以使用 :c:func:`k_thread_stack_alloc` 动态实例化堆栈,然后使用
:c:func:`k_thread_stack_free` 释放。

仅内核堆栈
==========

如果已知线程永远不会在用户模式下运行,或者堆栈用于特殊上下文(如处理中断),最好
使用 ``K_KERNEL_STACK`` 宏定义堆栈。

这些堆栈节省内存,因为永远不需要编程 MPU 区域来覆盖堆栈缓冲区本身,并且内核不需要
为特权提升堆栈保留额外空间,或仅与用户模式线程相关的内存管理数据结构。

从用户模式尝试使用以这种方式声明的堆栈将导致调用者的致命错误。

如果未启用 ``CONFIG_USERSPACE``,则 ``K_THREAD_STACK`` 宏集与 ``K_KERNEL_STACK``
宏集具有相同的效果。

线程堆栈
========

如果已知堆栈需要承载用户线程,或者无法确定这一点,请使用 ``K_THREAD_STACK`` 宏
定义堆栈。这可能会使用更多内存,但堆栈对象适合承载用户线程。

如果未启用 ``CONFIG_USERSPACE``,则 ``K_THREAD_STACK`` 宏集与 ``K_KERNEL_STACK``
宏集具有相同的效果。

.. _thread_priorities:

线程优先级
**********

线程的优先级是一个整数值,可以是负数或非负数。数值较低的优先级优先于数值较高的值。
例如,调度器给予优先级 4 的线程 A *高于*优先级 7 的线程 B 的优先级;同样,优先级 -2
的线程 C 比线程 A 和线程 B 都具有更高的优先级。

调度器根据每个线程的优先级区分两类线程。

* :dfn:`协作线程` 具有负优先级值。一旦它成为当前线程,协作线程将保持为当前线程,
  直到它执行使其未就绪的操作。

* :dfn:`可抢占线程` 具有非负优先级值。一旦它成为当前线程,如果协作线程或更高或
  相等优先级的可抢占线程变为就绪,可抢占线程可能随时被取代。

线程的初始优先级值可以在线程启动后上下更改。因此,可抢占线程可以通过更改其优先级
成为协作线程,反之亦然。

.. note::
    调度器不会做出启发式决策来重新确定线程的优先级。线程优先级仅在应用程序的请求下
    设置和更改。

内核支持几乎无限数量的线程优先级。配置选项 :kconfig:option:`CONFIG_NUM_COOP_PRIORITIES`
和 :kconfig:option:`CONFIG_NUM_PREEMPT_PRIORITIES` 指定每类线程的优先级数量,
从而产生以下可用优先级范围:

* 协作线程: (-:kconfig:option:`CONFIG_NUM_COOP_PRIORITIES`) 到 -1
* 可抢占线程: 0 到 (:kconfig:option:`CONFIG_NUM_PREEMPT_PRIORITIES` - 1)

.. image:: priorities.svg
   :align: center

例如,配置 5 个协作优先级和 10 个可抢占优先级会分别产生 -5 到 -1 和 0 到 9 的范围。

.. _metairq_priorities:

Meta-IRQ 优先级
===============

当启用时(参见 :kconfig:option:`CONFIG_NUM_METAIRQ_PRIORITIES`),在优先级空间的
最高(数值最低)端有一个特殊的协作优先级子类:meta-IRQ 线程。这些线程根据其正常
优先级进行调度,但也具有特殊能力,可以抢占所有其他线程(和其他 meta-IRQ 线程),
即使这些线程是协作的和/或已获取调度器锁。但是,Meta-IRQ 线程仍然是线程,仍然可以
被任何硬件中断中断。

此行为使解除 meta-IRQ 线程阻塞的行为(通过任何方式,例如创建它、调用 k_sem_give()
等)在由较低优先级线程完成时等同于同步系统调用,或者在从真实中断上下文完成时等同于
类似 ARM 的"挂起 IRQ"。其目的是此功能将用于在驱动程序子系统中实现中断"下半部分"
处理和/或"tasklet"功能。一旦唤醒,线程保证在当前 CPU 返回应用程序代码之前运行。

与其他操作系统中的类似功能不同,meta-IRQ 线程是真正的线程,运行在它们自己的堆栈上
(必须正常分配),而不是每个 CPU 的中断堆栈。在支持的架构上启用使用 IRQ 堆栈的
设计工作正在进行中。

请注意,由于这打破了 Zephyr API 对协作线程做出的承诺(即操作系统不会调度其他线程,
直到当前线程故意阻塞),因此应用程序代码应非常谨慎地使用它。这些不仅仅是非常高
优先级的线程,不应该这样使用。

.. _thread_options_v2:

线程选项
********

内核支持一小组 :dfn:`线程选项`,允许线程在特定情况下接受特殊处理。生成线程时
指定与线程关联的选项集。

不需要任何线程选项的线程的选项值为零。需要线程选项的线程通过名称指定它,如果需要
多个选项,则使用 :literal:`|` 字符作为分隔符(即,使用按位 OR 运算符组合选项)。

支持以下线程选项。

:c:macro:`K_ESSENTIAL`
    此选项将线程标记为 :dfn:`基本线程`。这指示内核将线程的终止或中止视为致命的
    系统错误。

    默认情况下,线程不被视为基本线程。

:c:macro:`K_SSE_REGS`
    此 x86 特定选项指示线程使用 CPU 的 SSE 寄存器。另请参见 :c:macro:`K_FP_REGS`。

    默认情况下,内核在调度线程时不会尝试保存和恢复这些寄存器的内容。

:c:macro:`K_FP_REGS`
    此选项指示线程使用 CPU 的浮点寄存器。这指示内核在调度线程时采取额外步骤来保存
    和恢复这些寄存器的内容。(有关更多信息,请参见 :ref:`float_v2`。)

    默认情况下,内核在调度线程时不会尝试保存和恢复此寄存器的内容。

:c:macro:`K_USER`
    如果启用了 :kconfig:option:`CONFIG_USERSPACE`,此线程将在用户模式下创建并具有
    减少的特权。请参见 :ref:`usermode_api`。否则此标志不执行任何操作。

:c:macro:`K_INHERIT_PERMS`
    如果启用了 :kconfig:option:`CONFIG_USERSPACE`,此线程将继承父线程拥有的所有
    内核对象权限,但父线程对象除外。请参见 :ref:`usermode_api`。

.. _custom_data_v2:

线程自定义数据
**************

每个线程都有一个 32 位 :dfn:`自定义数据` 区域,只能由线程本身访问,并且可以由
应用程序用于任何目的。线程的默认自定义数据值为零。

.. note::
   自定义数据支持不适用于 ISR,因为它们在单个共享内核中断处理上下文中运行。

默认情况下,线程自定义数据支持被禁用。配置选项 :kconfig:option:`CONFIG_THREAD_CUSTOM_DATA`
可用于启用支持。

:c:func:`k_thread_custom_data_set` 和 :c:func:`k_thread_custom_data_get` 函数
分别用于写入和读取线程的自定义数据。线程只能访问自己的自定义数据,而不能访问另一个
线程的自定义数据。

以下代码使用自定义数据功能记录每个线程调用特定例程的次数。

.. note::
    显然,只有一个例程可以使用此技术,因为它独占使用自定义数据功能。

.. code-block:: c

    int call_tracking_routine(void)
    {
        uint32_t call_count;

        if (k_is_in_isr()) {
	    /* 忽略 ISR 进行的任何调用 */
        } else {
            call_count = (uint32_t)k_thread_custom_data_get();
            call_count++;
            k_thread_custom_data_set((void *)call_count);
	}

        /* 执行例程的其余处理 */
        ...
    }

使用线程自定义数据允许例程访问线程特定信息,方法是将自定义数据用作指向线程拥有的
数据结构的指针。

实现
****

生成线程
========

通过定义其堆栈区域和线程控制块,然后调用 :c:func:`k_thread_create` 来生成线程。

堆栈区域可以使用 :c:macro:`K_THREAD_STACK_DEFINE` 或
:c:macro:`K_KERNEL_STACK_DEFINE` 静态分配,以确保在内存中正确设置。

堆栈的大小参数必须是以下三个值之一:

- 传递给 ``K_THREAD_STACK`` 或 ``K_KERNEL_STACK`` 系列堆栈实例化宏的原始请求
  堆栈大小。
- 对于使用 ``K_THREAD_STACK`` 系列宏定义的堆栈对象,该对象的
  :c:macro:`K_THREAD_STACK_SIZEOF()` 的返回值。
- 对于使用 ``K_KERNEL_STACK`` 系列宏定义的堆栈对象,该对象的
  :c:macro:`K_KERNEL_STACK_SIZEOF()` 的返回值。

或者,堆栈区域可以使用 :c:func:`k_thread_stack_alloc` 动态分配,并使用
:c:func:`k_thread_stack_free` 释放。

线程生成函数返回其线程 ID,可用于引用线程。

以下代码生成一个立即启动的线程。

.. code-block:: c

    #define MY_STACK_SIZE 500
    #define MY_PRIORITY 5

    extern void my_entry_point(void *, void *, void *);

    K_THREAD_STACK_DEFINE(my_stack_area, MY_STACK_SIZE);
    struct k_thread my_thread_data;

    k_tid_t my_tid = k_thread_create(&my_thread_data, my_stack_area,
                                     K_THREAD_STACK_SIZEOF(my_stack_area),
                                     my_entry_point,
                                     NULL, NULL, NULL,
                                     MY_PRIORITY, 0, K_NO_WAIT);

或者,可以通过调用 :c:macro:`K_THREAD_DEFINE` 在编译时声明线程。请注意,该宏会
自动定义堆栈区域、控制块和线程 ID 变量。

以下代码与上面的代码段具有相同的效果。

.. code-block:: c

    #define MY_STACK_SIZE 500
    #define MY_PRIORITY 5

    extern void my_entry_point(void *, void *, void *);

    K_THREAD_DEFINE(my_tid, MY_STACK_SIZE,
                    my_entry_point, NULL, NULL, NULL,
                    MY_PRIORITY, 0, 0);

.. note::
   :c:func:`k_thread_create` 的延迟参数是 :c:type:`k_timeout_t` 值,因此
   :c:macro:`K_NO_WAIT` 表示立即启动线程。:c:macro:`K_THREAD_DEFINE` 的相应
   参数是以整数毫秒为单位的持续时间,因此等效参数为 0。

以下代码动态分配线程堆栈,等待线程加入,然后释放动态分配的线程堆栈。

.. code-block:: c

    extern void my_entry_point(void *, void *, void *);

    k_tid_t my_tid;
    void *my_stack_area;

    my_stack_area = k_thread_stack_alloc(CONFIG_DYNAMIC_THREAD_STACK_SIZE);
    my_tid = k_thread_create(&my_thread_data, my_stack_area,
                              CONFIG_DYNAMIC_THREAD_STACK_SIZE,
                              my_entry_point,
                              NULL, NULL, NULL,
                              MY_PRIORITY, 0, K_NO_WAIT);
    k_thread_join(my_tid, K_FOREVER);
    k_thread_stack_free(my_stack_area);

用户模式约束
------------

本节仅在启用 :kconfig:option:`CONFIG_USERSPACE` 并且用户线程尝试创建新线程时
适用。仍然使用 :c:func:`k_thread_create` API,但必须满足其他约束,否则调用线程
将被终止:

* 调用线程必须对子线程和堆栈参数授予权限;两者都由内核作为内核对象跟踪。

* 子线程和堆栈对象必须处于未初始化状态,即它当前未运行,堆栈内存未使用。

* 传入的堆栈大小参数必须等于或小于声明堆栈对象时的堆栈对象的边界。

* 必须使用 :c:macro:`K_USER` 选项,因为用户线程只能创建其他用户线程。

* 不得使用 :c:macro:`K_ESSENTIAL` 选项,用户线程不得被视为基本线程。

* 子线程的优先级必须是有效的优先级值,并且等于或低于父线程。

放弃权限
========

如果启用了 :kconfig:option:`CONFIG_USERSPACE`,在监督者模式下运行的线程可以使用
:c:func:`k_thread_user_mode_enter` API 执行到用户模式的单向转换。这是一个单向
操作,它将重置并清零线程的堆栈内存。线程将被标记为非基本。

终止线程
========

线程通过从其入口点函数返回来终止自身。

以下代码说明了线程可以终止的方式。

.. code-block:: c

    void my_entry_point(int unused1, int unused2, int unused3)
    {
        while (1) {
            ...
	    if (<某个条件>) {
	        return; /* 线程从入口点函数中途终止 */
	    }
	    ...
        }

        /* 线程在入口点函数末尾终止 */
    }

如果启用了 :kconfig:option:`CONFIG_USERSPACE`,中止线程还会将线程和堆栈对象标记为
未初始化,以便可以重新使用它们。

运行时统计
**********

如果启用了 :kconfig:option:`CONFIG_THREAD_RUNTIME_STATS`,则可以收集和检索线程
运行时统计信息,例如,线程的总执行周期数。

默认情况下,使用默认内核计时器收集运行时统计信息。对于某些架构、SoC 或开发板,
可以通过计时函数使用具有更高分辨率的计时器。可以通过
:kconfig:option:`CONFIG_THREAD_RUNTIME_STATS_USE_TIMING_FUNCTIONS` 启用这些
计时器的使用。

以下是一个示例:

.. code-block:: c

   k_thread_runtime_stats_t rt_stats_thread;

   k_thread_runtime_stats_get(k_current_get(), &rt_stats_thread);

   printk("周期数: %llu\n", rt_stats_thread.execution_cycles);

建议用途
********

使用线程处理不能在 ISR 中处理的处理。

使用单独的线程处理可以并行执行的逻辑上不同的处理操作。

配置选项
********

相关配置选项:

* :kconfig:option:`CONFIG_MAIN_THREAD_PRIORITY`
* :kconfig:option:`CONFIG_MAIN_STACK_SIZE`
* :kconfig:option:`CONFIG_IDLE_STACK_SIZE`
* :kconfig:option:`CONFIG_THREAD_CUSTOM_DATA`
* :kconfig:option:`CONFIG_NUM_COOP_PRIORITIES`
* :kconfig:option:`CONFIG_NUM_PREEMPT_PRIORITIES`
* :kconfig:option:`CONFIG_TIMESLICING`
* :kconfig:option:`CONFIG_TIMESLICE_SIZE`
* :kconfig:option:`CONFIG_TIMESLICE_PRIORITY`
* :kconfig:option:`CONFIG_USERSPACE`

API 参考
********

.. doxygengroup:: thread_apis

.. doxygengroup:: thread_stack_api
