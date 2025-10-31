.. _semaphores_v2:

信号量 (Semaphores)
###################

:dfn:`信号量 (semaphore)` 是一个内核对象，实现了传统的计数信号量 (counting semaphore)。

.. contents::
    :local:
    :depth: 2

概念 (Concepts)
***************

可以定义任意数量的信号量（仅受可用 RAM 限制）。每个信号量通过其内存地址引用。

信号量具有以下关键属性：

* 一个 **计数值 (count)**，表示信号量可以被获取的次数。计数值为零表示信号量不可用。

* 一个 **限制值 (limit)**，表示信号量计数值可以达到的最大值。

信号量在使用前必须初始化。其计数值必须设置为小于或等于其限制值的非负值。

信号量可以被线程或 ISR **释放 (give)**。释放信号量会增加其计数值，除非计数值已经等于限制值。

信号量可以被线程 **获取 (take)**。获取信号量会减少其计数值，除非信号量不可用（即为零）。当信号量不可用时，线程可以选择等待它被释放。任意数量的线程可以同时等待一个不可用的信号量。当信号量被释放时，它会被等待时间最长的最高优先级线程获取。

.. note::
    您可以初始化一个"满"信号量（计数值等于限制值）来限制能够同时执行临界区 (critical section) 的线程数量。您也可以初始化一个空信号量（计数值等于 0，限制值大于 0）来创建一个门控 (gate)，在信号量递增之前，没有等待的线程可以通过。支持通用信号量的所有标准用例。

.. note::
    内核确实允许 ISR 获取信号量，但是如果信号量不可用，ISR 不得尝试等待。

实现 (Implementation)
*********************

定义信号量 (Defining a Semaphore)
=================================

信号量使用 :c:struct:`k_sem` 类型的变量定义。然后必须通过调用 :c:func:`k_sem_init` 进行初始化。

以下代码定义了一个信号量，然后通过将其计数值设置为 0、限制值设置为 1 来将其配置为二进制信号量 (binary semaphore)。

.. code-block:: c

    struct k_sem my_sem;

    k_sem_init(&my_sem, 0, 1);

或者，可以通过调用 :c:macro:`K_SEM_DEFINE` 在编译时定义并初始化信号量。

以下代码与上面的代码段具有相同的效果。

.. code-block:: c

    K_SEM_DEFINE(my_sem, 0, 1);

释放信号量 (Giving a Semaphore)
================================

通过调用 :c:func:`k_sem_give` 来释放信号量。

以下代码基于上面的示例，释放信号量以指示有一个数据单元可供消费者线程处理。

.. code-block:: c

    void input_data_interrupt_handler(void *arg)
    {
        /* 通知线程数据可用 */
        k_sem_give(&my_sem);

        ...
    }

获取信号量 (Taking a Semaphore)
================================

通过调用 :c:func:`k_sem_take` 来获取信号量。

以下代码基于上面的示例，等待最多 50 毫秒以释放信号量。如果未能及时获得信号量，则会发出警告。

.. code-block:: c

    void consumer_thread(void)
    {
        ...

        if (k_sem_take(&my_sem, K_MSEC(50)) != 0) {
            printk("Input data not available!");
        } else {
            /* 获取可用数据 */
            ...
        }
        ...
    }

建议用途 (Suggested Uses)
*************************

使用信号量来控制多个线程对一组资源的访问。

使用信号量来同步生产者和消费者线程或 ISR 之间的处理。

配置选项 (Configuration Options)
********************************

相关配置选项：

* 无。

API 参考 (API Reference)
************************

.. doxygengroup:: semaphore_apis

用户模式信号量 API 参考 (User Mode Semaphore API Reference)
**********************************************************

sys_sem 存在于用户内存 (user memory) 中，当启用用户模式 (user mode) 时作为用户模式线程的计数信号量工作。当用户模式未启用时，sys_sem 的行为类似于 k_sem。

.. doxygengroup:: user_semaphore_apis
