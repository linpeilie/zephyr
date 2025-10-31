.. _scheduling_v2:

调度
####

内核的基于优先级的调度器允许应用程序的线程共享 CPU。

概念
****

调度器确定在任何时间点允许执行哪个线程；该线程被称为**当前线程** (current thread)。

在各种时间点，调度器有机会更改当前线程的身份，这意味着调度器将 CPU 的执行从一个线程切换到另一个线程。
这些时间点称为**重新调度点** (reschedule points)。一些潜在的重新调度点包括：

- 线程从运行状态转换到挂起或等待状态，例如通过 :c:func:`k_sem_take` 或 :c:func:`k_sleep`。
- 线程转换到 :ref:`就绪状态 <thread_states>`，例如通过 :c:func:`k_sem_give` 或 :c:func:`k_thread_start`。
- 处理中断后返回线程上下文。
- 运行中的线程调用 :c:func:`k_yield`。

当线程自愿启动使自己转换到挂起或等待状态的操作时，该线程**睡眠** (sleeps)。

每当调度器更改当前线程的身份时，或者当当前线程的执行被 ISR 替换时，
内核首先保存当前线程的 CPU 寄存器值。当线程稍后恢复执行时，这些寄存器值将被恢复。

调度算法 (Scheduling Algorithm)
===============================

内核的调度器选择最高优先级的就绪线程作为当前线程。当存在多个相同优先级的就绪线程时，
调度器选择等待时间最长的线程。

线程的相对优先级主要由其静态优先级决定。但是，当启用最早截止时间优先调度
(:kconfig:option:`CONFIG_SCHED_DEADLINE`) 并且线程的静态优先级相同时，
则具有较早截止时间的线程被认为具有较高的优先级。因此，当启用最早截止时间优先调度时，
仅当两个线程的静态优先级和截止时间都相等时，才认为它们具有相同的优先级。
例程 :c:func:`k_thread_deadline_set` 用于设置线程的截止时间。

.. note::
    ISR 的执行优先于线程执行，因此当前线程的执行可能随时被 ISR 替换，除非中断已被屏蔽。
    这适用于协作线程和抢占线程。

内核可以使用几种就绪队列实现之一构建，在代码大小、常量因子运行时开销和添加许多线程时的性能扩展之间提供不同的选择。

* 简单链表就绪队列 (:kconfig:option:`CONFIG_SCHED_SIMPLE`)

  调度器就绪队列将实现为简单的无序列表，对于单个线程具有非常快的常量时间性能和非常低的代码大小。
  应在代码大小受限的系统上选择此实现，这些系统在任何给定时间永远不会看到超过少量（也许 3 个）可运行线程在队列中。
  在大多数平台上（否则未使用红黑树），这会节省约 2k 的代码大小。

* 红黑树就绪队列 (:kconfig:option:`CONFIG_SCHED_SCALABLE`)

  调度器就绪队列将实现为红黑树。这具有相当慢的常量时间插入和删除开销，
  并且在大多数平台上（否则在其他地方未使用红黑树）需要额外的约 2kb 代码。
  产生的行为将干净且快速地扩展到数千个线程。

  对于需要许多并发可运行线程（> 20 左右）的应用程序，使用此实现。大多数应用程序不需要此就绪队列实现。

* 传统多队列就绪队列 (:kconfig:option:`CONFIG_SCHED_MULTIQ`)

  选择后，调度器就绪队列将实现为经典/教科书的列表数组，每个优先级一个。

  这对应于 Zephyr 1.12 之前版本中使用的调度器算法。

  与"简单"调度器相比，它仅产生很小的代码大小开销，并且在几乎所有情况下都以 O(1) 时间运行，
  常量因子非常低。但它需要相当大的 RAM 预算来存储这些列表头，并且有限的功能使其与需要更精细地排序线程的
  截止时间调度等功能不兼容，以及需要遍历线程列表的 SMP 亲和性。

  具有少量可运行线程的典型应用程序可能需要简单调度器。

wait_q 抽象用于 IPC 原语中暂停线程以供稍后唤醒，与调度器共享相同的后端数据结构选择，并且可以使用相同的选项。

* 可扩展 wait_q 实现 (:kconfig:option:`CONFIG_WAITQ_SCALABLE`)

  选择后，wait_q 将使用平衡树实现。如果您期望有许多线程在单个原语上等待，请选择此选项。
  与 :kconfig:option:`CONFIG_WAITQ_SIMPLE` 相比，代码大小增加约 2kb（如果红黑树未在应用程序的其他地方使用，
  则可能与 :kconfig:option:`CONFIG_SCHED_SCALABLE` 共享），并且"小"队列上的 pend/unpend 操作会稍慢一些
  （尽管这通常不是性能路径）。

* 简单链表 wait_q (:kconfig:option:`CONFIG_WAITQ_SIMPLE`)

  选择后，wait_q 将使用双向链表实现。如果您期望只有少数线程阻塞在任何单个 IPC 原语上，请选择此选项。

协作时间分片 (Cooperative Time Slicing)
=======================================

一旦协作线程成为当前线程，它将保持为当前线程，直到它执行使其未就绪的操作。
因此，如果协作线程执行冗长的计算，它可能会导致其他线程（包括更高优先级和相同优先级的线程）的调度出现不可接受的延迟。

  .. image:: cooperative.svg
     :align: center

为了克服此类问题，协作线程可以不时自愿放弃 CPU 以允许其他线程执行。线程可以通过两种方式放弃 CPU：

* 调用 :c:func:`k_yield` 将线程放在调度器的优先级就绪线程列表的末尾，然后调用调度器。
  然后允许所有优先级高于或等于让出线程的优先级的就绪线程在让出线程被重新调度之前执行。
  如果不存在此类就绪线程，则调度器立即重新调度让出线程而不进行上下文切换。

* 调用 :c:func:`k_sleep` 使线程在指定的时间段内未就绪。然后允许*所有*优先级的就绪线程执行；
  但是，不能保证优先级低于睡眠线程的线程在睡眠线程再次就绪之前实际被调度。

抢占时间分片 (Preemptive Time Slicing)
======================================

一旦抢占线程成为当前线程，它将保持为当前线程，直到更高优先级的线程就绪，
或直到线程执行使其未就绪的操作。因此，如果抢占线程执行冗长的计算，
它可能会导致其他线程（包括相同优先级的线程）的调度出现不可接受的延迟。

  .. image:: preemptive.svg
     :align: center

为了克服此类问题，抢占线程可以执行协作时间分片（如上所述），或者可以使用调度器的时间分片功能
来允许相同优先级的其他线程执行。

.. image:: timeslicing.svg
   :align: center

调度器将时间划分为一系列**时间片** (time slices)，其中时间片以系统时钟滴答为单位测量。
时间片大小是可配置的，但可以在应用程序运行时更改此大小。

在每个时间片结束时，调度器检查当前线程是否可抢占，如果是，则代表线程隐式调用 :c:func:`k_yield`。
这使相同优先级的其他就绪线程有机会在当前线程再次被调度之前执行。
如果没有相同优先级的线程就绪，则当前线程保持为当前线程。

优先级高于指定限制的线程免于抢占时间分片，并且永远不会被相同优先级的线程抢占。
这允许应用程序仅在处理时间敏感性较低的低优先级线程时使用抢占时间分片。

.. note::
   内核的时间分片算法*不*确保一组相同优先级的线程接收公平的 CPU 时间量，
   因为它不测量线程实际执行的时间量。但是，该算法*确实*确保线程在被要求让出之前
   永远不会执行超过单个时间片的时间。

调度器锁定 (Scheduler Locking)
==============================

在执行关键操作时不希望被抢占的可抢占线程可以通过调用 :c:func:`k_sched_lock`
指示调度器暂时将其视为协作线程。这可以防止其他线程在执行关键操作时进行干扰。

一旦关键操作完成，可抢占线程必须调用 :c:func:`k_sched_unlock` 以恢复其正常的可抢占状态。

如果线程调用 :c:func:`k_sched_lock` 然后执行使其未就绪的操作，调度器将切换出锁定线程
并允许其他线程执行。当锁定线程再次成为当前线程时，其不可抢占状态将得到维护。

.. note::
    锁定调度器是可抢占线程防止抢占的一种更有效的方法，比将其优先级更改为负值更有效。

.. _thread_sleeping:

线程睡眠 (Thread Sleeping)
==========================

线程可以调用 :c:func:`k_sleep` 来延迟其处理指定的时间段。在线程睡眠期间，
CPU 被放弃以允许其他就绪线程执行。一旦指定的延迟已过，线程就绪并有资格再次被调度。

睡眠线程可以被另一个线程使用 :c:func:`k_wakeup` 提前唤醒。这种技术有时可用于允许次要线程
向睡眠线程发出某事已发生的信号，*而无需*要求线程定义内核同步对象（如信号量）。
唤醒未睡眠的线程是允许的，但没有效果。

.. _busy_waiting:

忙等待 (Busy Waiting)
=====================

线程可以调用 :c:func:`k_busy_wait` 执行``忙等待``，延迟其处理指定的时间段，
*而不*将 CPU 放弃给另一个就绪线程。

当所需的延迟太短而无法保证调度器从当前线程上下文切换到另一个线程然后再返回时，
通常使用忙等待而不是线程睡眠。

建议用途
********

对设备驱动程序和其他性能关键工作使用协作线程。

使用协作线程实现互斥，而无需内核对象（如互斥锁）。

使用抢占线程为时间敏感处理优先于时间不敏感处理。

配置选项
********

* :kconfig:option:`CONFIG_TIMESLICING`
* :kconfig:option:`CONFIG_TIMESLICE_SIZE`
* :kconfig:option:`CONFIG_TIMESLICE_PRIORITY`

.. _cpu_idle:

CPU 空闲 (CPU Idling)
#####################

虽然通常为空闲线程保留，但在某些特殊应用程序中，线程可能希望使 CPU 空闲。

.. contents::
    :local:
    :depth: 2

概念
****

使 CPU 空闲会导致内核暂停所有操作，直到事件（通常是中断）唤醒 CPU。
在常规系统中，空闲线程负责此操作。但是，在某些受限系统中，可能由另一个线程承担此职责。

实现
****

使 CPU 空闲
===========

使 CPU 空闲很简单：调用 k_cpu_idle() API。CPU 将停止执行指令，直到发生事件。
最有可能的是，该函数将在循环中调用。请注意，在某些架构中，返回时，k_cpu_idle() 无条件地取消屏蔽中断。

.. code-block:: c

    static k_sem my_sem;

    void my_isr(void *unused)
    {
        k_sem_give(&my_sem);
    }

    int main(void)
    {
        k_sem_init(&my_sem, 0, 1);

        /* wait for semaphore from ISR, then do related work */

        for (;;) {

            /* wait for ISR to trigger work to perform */
            if (k_sem_take(&my_sem, K_NO_WAIT) == 0) {

                /* ... do processing */

            }

            /* put CPU to sleep to save power */
            k_cpu_idle();
        }
    }

以原子方式使 CPU 空闲
=====================

可能需要在使 CPU 空闲之前以原子方式执行一些工作。在这种情况下，应改用 k_cpu_atomic_idle()。

实际上，前面的示例中存在竞争条件：中断可能发生在获取信号量、发现它不可用和再次使 CPU 空闲之间。
在某些系统中，这可能导致 CPU 空闲，直到发生*另一个*中断，这可能*永远不会*发生，从而导致系统完全挂起。
为了防止这种情况，应该使用 k_cpu_atomic_idle()，如以下示例所示。

.. code-block:: c

    static k_sem my_sem;

    void my_isr(void *unused)
    {
        k_sem_give(&my_sem);
    }

    int main(void)
    {
        k_sem_init(&my_sem, 0, 1);

        for (;;) {

            unsigned int key = irq_lock();

            /*
             * Wait for semaphore from ISR; if acquired, do related work, then
             * go to next loop iteration (the semaphore might have been given
             * again); else, make the CPU idle.
             */

            if (k_sem_take(&my_sem, K_NO_WAIT) == 0) {

                irq_unlock(key);

                /* ... do processing */


            } else {
                /* put CPU to sleep to save power */
                k_cpu_atomic_idle(key);
            }
        }
    }

建议用途
********

当线程除了使 CPU 空闲以等待事件之外还必须执行一些实际工作时，使用 k_cpu_atomic_idle()。见上面的示例。

仅当线程仅负责使 CPU 空闲时使用 k_cpu_idle()，即不执行任何实际工作，如下面的示例。

.. code-block:: c

    int main(void)
    {
        /* ... do some system/application initialization */


        /* thread is only used for CPU idling from this point on */
        for (;;) {
            k_cpu_idle();
        }
    }

.. note::
     **除非绝对必要，否则不要使用这些 API。** 在正常系统中，空闲线程负责电源管理，包括 CPU 空闲。

API 参考
********

.. doxygengroup:: cpu_idle_apis
