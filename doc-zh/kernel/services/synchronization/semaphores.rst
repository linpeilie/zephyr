.. _semaphores_v2:.. _semaphores_v2:



信号量Semaphores

################



:dfn:`信号量` 是实现传统计数信号量的内核对象。A :dfn:`semaphore` is a kernel object that implements a traditional

counting semaphore.

.. contents::

    :local:.. contents::

    :depth: 2    :local:

    :depth: 2

概念

****Concepts

********

可以定义任意数量的信号量(仅受可用 RAM 限制)。每个信号量由其内存地址引用。

Any number of semaphores can be defined (limited only by available RAM). Each

信号量具有以下关键属性:semaphore is referenced by its memory address.



* **计数**,指示信号量可以被获取的次数。计数为零表示信号量不可用。A semaphore has the following key properties:



* **限制**,指示信号量计数可以达到的最大值。* A **count** that indicates the number of times the semaphore can be taken.

  A count of zero indicates that the semaphore is unavailable.

信号量在使用之前必须初始化。其计数必须设置为小于或等于其限制的非负值。

* A **limit** that indicates the maximum value the semaphore's count

信号量可以由线程或 ISR **给予**。给予信号量会增加其计数,除非计数已经等于限制。  can reach.



信号量可以由线程**获取**。获取信号量会减少其计数,除非信号量不可用(即为零)。A semaphore must be initialized before it can be used. Its count must be set

当信号量不可用时,线程可以选择等待它被给予。任意数量的线程可以同时等待不可用的to a non-negative value that is less than or equal to its limit.

信号量。当信号量被给予时,它由等待时间最长的最高优先级线程获取。

A semaphore may be **given** by a thread or an ISR. Giving the semaphore

.. note::increments its count, unless the count is already equal to the limit.

    您可以初始化一个"满"信号量(计数等于限制)来限制能够同时执行临界区的线程数。

    您还可以初始化一个空信号量(计数等于 0,限制大于 0)来创建一个门,在信号量递增A semaphore may be **taken** by a thread. Taking the semaphore

    之前,没有等待线程可以通过。支持所有常见信号量的标准用例。decrements its count, unless the semaphore is unavailable (i.e. at zero).

When a semaphore is unavailable a thread may choose to wait for it to be given.

.. note::Any number of threads may wait on an unavailable semaphore simultaneously.

    内核确实允许 ISR 获取信号量,但是如果信号量不可用,ISR 不得尝试等待。When the semaphore is given, it is taken by the highest priority thread

that has waited longest.

实现

****.. note::

    You may initialize a "full" semaphore (count equal to limit) to limit the number

定义信号量    of threads able to execute the critical section at the same time. You may also

==========    initialize an empty semaphore (count equal to 0, with a limit greater than 0)

    to create a gate through which no waiting thread may pass until the semaphore

使用类型 :c:struct:`k_sem` 的变量定义信号量。然后必须通过调用 :c:func:`k_sem_init`    is incremented. All standard use cases of the common semaphore are supported.

初始化它。

.. note::

以下代码定义了一个信号量,然后通过将其计数设置为 0 并将其限制设置为 1 将其配置为    The kernel does allow an ISR to take a semaphore, however the ISR must

二进制信号量。    not attempt to wait if the semaphore is unavailable.



.. code-block:: cImplementation

**************

    struct k_sem my_sem;

Defining a Semaphore

    k_sem_init(&my_sem, 0, 1);====================



或者,可以通过调用 :c:macro:`K_SEM_DEFINE` 在编译时定义和初始化信号量。A semaphore is defined using a variable of type :c:struct:`k_sem`.

It must then be initialized by calling :c:func:`k_sem_init`.

以下代码与上面的代码段具有相同的效果。

The following code defines a semaphore, then configures it as a binary

.. code-block:: csemaphore by setting its count to 0 and its limit to 1.



    K_SEM_DEFINE(my_sem, 0, 1);.. code-block:: c



给予信号量    struct k_sem my_sem;

==========

    k_sem_init(&my_sem, 0, 1);

通过调用 :c:func:`k_sem_give` 给予信号量。

Alternatively, a semaphore can be defined and initialized at compile time

以下代码基于上面的示例,给予信号量以指示一个数据单元可供消费者线程处理。by calling :c:macro:`K_SEM_DEFINE`.



.. code-block:: cThe following code has the same effect as the code segment above.



    void input_data_interrupt_handler(void *arg).. code-block:: c

    {

        /* 通知线程数据可用 */    K_SEM_DEFINE(my_sem, 0, 1);

        k_sem_give(&my_sem);

Giving a Semaphore

        ...==================

    }

A semaphore is given by calling :c:func:`k_sem_give`.

获取信号量

==========The following code builds on the example above, and gives the semaphore to

indicate that a unit of data is available for processing by a consumer thread.

通过调用 :c:func:`k_sem_take` 获取信号量。

.. code-block:: c

以下代码基于上面的示例,等待最多 50 毫秒以获得信号量。如果未及时获得信号量,

则发出警告。    void input_data_interrupt_handler(void *arg)

    {

.. code-block:: c        /* notify thread that data is available */

        k_sem_give(&my_sem);

    void consumer_thread(void)

    {        ...

        ...    }



        if (k_sem_take(&my_sem, K_MSEC(50)) != 0) {Taking a Semaphore

            printk("输入数据不可用!");==================

        } else {

            /* 获取可用数据 */A semaphore is taken by calling :c:func:`k_sem_take`.

            ...

        }The following code builds on the example above, and waits up to 50 milliseconds

        ...for the semaphore to be given.

    }A warning is issued if the semaphore is not obtained in time.



建议用途.. code-block:: c

********

    void consumer_thread(void)

使用信号量来控制多个线程对一组资源的访问。    {

        ...

使用信号量来同步生产和消费线程或 ISR 之间的处理。

        if (k_sem_take(&my_sem, K_MSEC(50)) != 0) {

配置选项            printk("Input data not available!");

********        } else {

            /* fetch available data */

相关配置选项:            ...

        }

* 无。        ...

    }

API 参考

********Suggested Uses

**************

.. doxygengroup:: semaphore_apis

Use a semaphore to control access to a set of resources by multiple threads.

用户模式信号量 API 参考

***********************Use a semaphore to synchronize processing between a producing and consuming

threads or ISRs.

当启用用户模式时,sys_sem 存在于用户内存中,作为用户模式线程的计数信号量。

当未启用用户模式时,sys_sem 的行为类似于 k_sem。Configuration Options

*********************

.. doxygengroup:: user_semaphore_apis

Related configuration options:

* None.

API Reference
**************

.. doxygengroup:: semaphore_apis

User Mode Semaphore API Reference
*********************************

The sys_sem exists in user memory working as counter semaphore for user mode
thread when user mode enabled. When user mode isn't enabled, sys_sem behaves
like k_sem.

.. doxygengroup:: user_semaphore_apis
