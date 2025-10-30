.. _lifos_v2:.. _lifos_v2:



LIFO 队列LIFOs

##############



:dfn:`LIFO` 是一个内核对象,它实现了传统的后进先出 (LIFO) 队列,允许线程和 ISR A :dfn:`LIFO` is a kernel object that implements a traditional

添加和删除任意大小的数据项。last in, first out (LIFO) queue, allowing threads and ISRs

to add and remove data items of any size.

.. contents::

    :local:.. contents::

    :depth: 2    :local:

    :depth: 2

概念

****Concepts

********

可以定义任意数量的 LIFO(仅受可用 RAM 限制)。每个 LIFO 由其内存地址引用。

Any number of LIFOs can be defined (limited only by available RAM). Each LIFO is

LIFO 具有以下关键属性:referenced by its memory address.



* 已添加但尚未删除的数据项的**队列**。队列实现为简单的链表。A LIFO has the following key properties:



LIFO 在使用之前必须初始化。这会将其队列设置为空。* A **queue** of data items that have been added but not yet removed.

  The queue is implemented as a simple linked list.

LIFO 数据项必须在字边界对齐,因为内核保留项的第一个字用作指向队列中下一个数据项

的指针。因此,包含 N 字节应用程序数据的数据项需要 N+4(或 N+8)字节的内存。A LIFO must be initialized before it can be used. This sets its queue to empty.

如果使用 :c:func:`k_lifo_alloc_put` 添加数据项,则对数据项没有对齐或保留空间要求,

而是从调用线程的资源池临时分配额外的内存。LIFO data items must be aligned on a word boundary, as the kernel reserves

the first word of an item for use as a pointer to the next data item in the

.. note::queue. Consequently, a data item that holds N bytes of application data

    LIFO 数据项在所有 LIFO 数据队列中仅限于单个活动实例。在数据项从先前添加到的requires N+4 (or N+8) bytes of memory. There are no alignment or reserved

    队列中删除之前,任何重新添加 LIFO 数据项到队列的尝试都将导致未定义的行为。space requirements for data items if they are added with

:c:func:`k_lifo_alloc_put`, instead additional memory is temporarily

数据项可以由线程或 ISR **添加**到 LIFO。如果存在等待的线程,则该项直接给予它;allocated from the calling thread's resource pool.

否则该项被添加到 LIFO 的队列。可排队的项数没有限制。

.. note::

数据项可以由线程从 LIFO **删除**。如果 LIFO 的队列为空,线程可以选择等待数据项    LIFO data items are restricted to single active instance across all LIFO

被给予。任意数量的线程可以同时在空 LIFO 上等待。添加数据项时,它会被给予等待时间    data queues. Any attempt to re-add a LIFO data item to a queue before

最长的最高优先级线程。    it has been removed from the queue to which it was previously added will

    result in undefined behavior.

.. note::

    内核确实允许 ISR 从 LIFO 删除项,但是如果 LIFO 为空,ISR 不得尝试等待。A data item may be **added** to a LIFO by a thread or an ISR.

The item is given directly to a waiting thread, if one exists;

实现otherwise the item is added to the LIFO's queue.

****There is no limit to the number of items that may be queued.



定义 LIFOA data item may be **removed** from a LIFO by a thread. If the LIFO's queue

=========is empty a thread may choose to wait for a data item to be given.

Any number of threads may wait on an empty LIFO simultaneously.

使用类型 :c:struct:`k_lifo` 的变量定义 LIFO。然后必须通过调用 When a data item is added, it is given to the highest priority thread

:c:func:`k_lifo_init` 初始化它。that has waited longest.



以下定义并初始化空 LIFO。.. note::

    The kernel does allow an ISR to remove an item from a LIFO, however

.. code-block:: c    the ISR must not attempt to wait if the LIFO is empty.



    struct k_lifo my_lifo;Implementation

**************

    k_lifo_init(&my_lifo);

Defining a LIFO

或者,可以通过调用 :c:macro:`K_LIFO_DEFINE` 在编译时定义和初始化空 LIFO。===============



以下代码与上面的代码段具有相同的效果。A LIFO is defined using a variable of type :c:struct:`k_lifo`.

It must then be initialized by calling :c:func:`k_lifo_init`.

.. code-block:: c

The following defines and initializes an empty LIFO.

    K_LIFO_DEFINE(my_lifo);

.. code-block:: c

写入 LIFO

=========    struct k_lifo my_lifo;



通过调用 :c:func:`k_lifo_put` 将数据项添加到 LIFO。    k_lifo_init(&my_lifo);



以下代码基于上面的示例,并使用 LIFO 将数据发送到一个或多个消费者线程。Alternatively, an empty LIFO can be defined and initialized at compile time

by calling :c:macro:`K_LIFO_DEFINE`.

.. code-block:: c

The following code has the same effect as the code segment above.

    struct data_item_t {

        void *LIFO_reserved;   /* 第 1 个字保留给 LIFO 使用 */.. code-block:: c

        ...

    };    K_LIFO_DEFINE(my_lifo);



    struct data_item_t tx data;Writing to a LIFO

=================

    void producer_thread(int unused1, int unused2, int unused3)

    {A data item is added to a LIFO by calling :c:func:`k_lifo_put`.

        while (1) {

            /* 创建要发送的数据项 */The following code builds on the example above, and uses the LIFO

            tx_data = ...to send data to one or more consumer threads.



            /* 将数据发送给消费者 */.. code-block:: c

            k_lifo_put(&my_lifo, &tx_data);

    struct data_item_t {

            ...        void *LIFO_reserved;   /* 1st word reserved for use by LIFO */

        }        ...

    }    };



可以使用 :c:func:`k_lifo_alloc_put` 将数据项添加到 LIFO。使用此 API,无需在    struct data_item_t tx data;

数据项中为内核使用保留空间,而是从调用线程的资源池分配额外的内存,直到读取该项。

    void producer_thread(int unused1, int unused2, int unused3)

从 LIFO 读取    {

============        while (1) {

            /* create data item to send */

通过调用 :c:func:`k_lifo_get` 从 LIFO 删除数据项。            tx_data = ...



以下代码基于上面的示例,并使用 LIFO 从生产者线程获取数据项,然后以某种方式处理它们。            /* send data to consumers */

            k_lifo_put(&my_lifo, &tx_data);

.. code-block:: c

            ...

    void consumer_thread(int unused1, int unused2, int unused3)        }

    {    }

        struct data_item_t  *rx_data;

A data item can be added to a LIFO with :c:func:`k_lifo_alloc_put`.

        while (1) {With this API, there is no need to reserve space for the kernel's use in

            rx_data = k_lifo_get(&my_lifo, K_FOREVER);the data item, instead additional memory will be allocated from the calling

thread's resource pool until the item is read.

            /* 处理 LIFO 数据项 */

            ...Reading from a LIFO

        }===================

    }

A data item is removed from a LIFO by calling :c:func:`k_lifo_get`.

建议用途

********The following code builds on the example above, and uses the LIFO

to obtain data items from a producer thread,

使用 LIFO 以"后进先出"方式异步传输任意大小的数据项。which are then processed in some manner.



配置选项.. code-block:: c

********

    void consumer_thread(int unused1, int unused2, int unused3)

相关配置选项:    {

        struct data_item_t  *rx_data;

* 无。

        while (1) {

API 参考            rx_data = k_lifo_get(&my_lifo, K_FOREVER);

********

            /* process LIFO data item */

.. doxygengroup:: lifo_apis            ...

        }
    }

Suggested Uses
**************

Use a LIFO to asynchronously transfer data items of arbitrary size
in a "last in, first out" manner.

Configuration Options
*********************

Related configuration options:

* None.

API Reference
*************

.. doxygengroup:: lifo_apis
