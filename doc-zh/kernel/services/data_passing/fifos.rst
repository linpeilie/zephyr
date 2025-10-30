.. _fifos_v2:.. _fifos_v2:



FIFO 队列FIFOs

##############



:dfn:`FIFO` 是一个内核对象,它实现了传统的先进先出 (FIFO) 队列,允许线程和 ISR A :dfn:`FIFO` is a kernel object that implements a traditional

添加和删除任意大小的数据项。first in, first out (FIFO) queue, allowing threads and ISRs

to add and remove data items of any size.

.. contents::

    :local:.. contents::

    :depth: 2    :local:

    :depth: 2

概念

****Concepts

********

可以定义任意数量的 FIFO(仅受可用 RAM 限制)。每个 FIFO 由其内存地址引用。

Any number of FIFOs can be defined (limited only by available RAM). Each FIFO is

FIFO 具有以下关键属性:referenced by its memory address.



* 已添加但尚未删除的数据项的**队列**。队列实现为简单的链表。A FIFO has the following key properties:



FIFO 在使用之前必须初始化。这会将其队列设置为空。* A **queue** of data items that have been added but not yet removed.

  The queue is implemented as a simple linked list.

FIFO 数据项必须在字边界对齐,因为内核保留项的第一个字用作指向队列中下一个数据项

的指针。因此,包含 N 字节应用程序数据的数据项需要 N+4(或 N+8)字节的内存。A FIFO must be initialized before it can be used. This sets its queue to empty.

如果使用 :c:func:`k_fifo_alloc_put` 添加数据项,则对数据项没有对齐或保留空间要求,

而是从调用线程的资源池临时分配额外的内存。FIFO data items must be aligned on a word boundary, as the kernel reserves

the first word of an item for use as a pointer to the next data item in

.. note::the queue. Consequently, a data item that holds N bytes of application

    FIFO 数据项在所有 FIFO 数据队列中仅限于单个活动实例。在数据项从先前添加到的data requires N+4 (or N+8) bytes of memory. There are no alignment or

    队列中删除之前,任何重新添加 FIFO 数据项到队列的尝试都将导致未定义的行为。reserved space requirements for data items if they are added with

:c:func:`k_fifo_alloc_put`, instead additional memory is temporarily

数据项可以由线程或 ISR **添加**到 FIFO。如果存在等待的线程,则该项直接给予它;allocated from the calling thread's resource pool.

否则该项被添加到 FIFO 的队列。可排队的项数没有限制。

.. note::

数据项可以由线程从 FIFO **删除**。如果 FIFO 的队列为空,线程可以选择等待数据项    FIFO data items are restricted to single active instance across all FIFO

被给予。任意数量的线程可以同时在空 FIFO 上等待。添加数据项时,它会被给予等待时间    data queues. Any attempt to re-add a FIFO data item to a queue before

最长的最高优先级线程。    it has been removed from the queue to which it was previously added will

    result in undefined behavior.

.. note::

    内核确实允许 ISR 从 FIFO 删除项,但是如果 FIFO 为空,ISR 不得尝试等待。A data item may be **added** to a FIFO by a thread or an ISR.

The item is given directly to a waiting thread, if one exists;

如果需要,可以在单个操作中将**多个数据项**添加到 FIFO,前提是它们被链接成otherwise the item is added to the FIFO's queue.

单链表。如果多个写入者正在向 FIFO 添加相关数据项集,此功能可能很有用,因为它There is no limit to the number of items that may be queued.

确保每个集中的数据项不会与其他数据项交错。将多个数据项添加到 FIFO 也比一次

添加一个更高效,并且可用于保证删除集中第一个数据项的任何人都能够删除剩余的A data item may be **removed** from a FIFO by a thread. If the FIFO's queue

数据项而无需等待。is empty a thread may choose to wait for a data item to be given.

Any number of threads may wait on an empty FIFO simultaneously.

实现When a data item is added, it is given to the highest priority thread

****that has waited longest.



定义 FIFO.. note::

=========    The kernel does allow an ISR to remove an item from a FIFO, however

    the ISR must not attempt to wait if the FIFO is empty.

使用类型 :c:struct:`k_fifo` 的变量定义 FIFO。然后必须通过调用

:c:func:`k_fifo_init` 初始化它。If desired, **multiple data items** can be added to a FIFO in a single operation

if they are chained together into a singly-linked list. This capability can be

以下代码定义并初始化空 FIFO。useful if multiple writers are adding sets of related data items to the FIFO,

as it ensures the data items in each set are not interleaved with other data

.. code-block:: citems. Adding multiple data items to a FIFO is also more efficient than adding

them one at a time, and can be used to guarantee that anyone who removes

    struct k_fifo my_fifo;the first data item in a set will be able to remove the remaining data items

without waiting.

    k_fifo_init(&my_fifo);

Implementation

或者,可以通过调用 :c:macro:`K_FIFO_DEFINE` 在编译时定义和初始化空 FIFO。**************



以下代码与上面的代码段具有相同的效果。Defining a FIFO

===============

.. code-block:: c

A FIFO is defined using a variable of type :c:struct:`k_fifo`.

    K_FIFO_DEFINE(my_fifo);It must then be initialized by calling :c:func:`k_fifo_init`.



写入 FIFOThe following code defines and initializes an empty FIFO.

=========

.. code-block:: c

通过调用 :c:func:`k_fifo_put` 将数据项添加到 FIFO。

    struct k_fifo my_fifo;

以下代码基于上面的示例,并使用 FIFO 将数据发送到一个或多个消费者线程。

    k_fifo_init(&my_fifo);

.. code-block:: c

Alternatively, an empty FIFO can be defined and initialized at compile time

    struct data_item_t {by calling :c:macro:`K_FIFO_DEFINE`.

        void *fifo_reserved;   /* 第 1 个字保留给 FIFO 使用 */

        ...The following code has the same effect as the code segment above.

    };

.. code-block:: c

    struct data_item_t tx_data;

    K_FIFO_DEFINE(my_fifo);

    void producer_thread(int unused1, int unused2, int unused3)

    {Writing to a FIFO

        while (1) {=================

            /* 创建要发送的数据项 */

            tx_data = ...A data item is added to a FIFO by calling :c:func:`k_fifo_put`.



            /* 将数据发送给消费者 */The following code builds on the example above, and uses the FIFO

            k_fifo_put(&my_fifo, &tx_data);to send data to one or more consumer threads.



            ..... code-block:: c

        }

    }    struct data_item_t {

        void *fifo_reserved;   /* 1st word reserved for use by FIFO */

此外,可以通过调用 :c:func:`k_fifo_put_list` 或 :c:func:`k_fifo_put_slist`         ...

将单链表数据项添加到 FIFO。    };



最后,可以使用 :c:func:`k_fifo_alloc_put` 将数据项添加到 FIFO。使用此 API,    struct data_item_t tx_data;

无需在数据项中为内核使用保留空间,而是从调用线程的资源池分配额外的内存,直到

读取该项。    void producer_thread(int unused1, int unused2, int unused3)

    {

从 FIFO 读取        while (1) {

============            /* create data item to send */

            tx_data = ...

通过调用 :c:func:`k_fifo_get` 从 FIFO 删除数据项。

            /* send data to consumers */

以下代码基于上面的示例,并使用 FIFO 从生产者线程获取数据项,然后以某种方式处理它们。            k_fifo_put(&my_fifo, &tx_data);



.. code-block:: c            ...

        }

    void consumer_thread(int unused1, int unused2, int unused3)    }

    {

        struct data_item_t  *rx_data;Additionally, a singly-linked list of data items can be added to a FIFO

by calling :c:func:`k_fifo_put_list` or :c:func:`k_fifo_put_slist`.

        while (1) {

            rx_data = k_fifo_get(&my_fifo, K_FOREVER);Finally, a data item can be added to a FIFO with :c:func:`k_fifo_alloc_put`.

With this API, there is no need to reserve space for the kernel's use in

            /* 处理 FIFO 数据项 */the data item, instead additional memory will be allocated from the calling

            ...thread's resource pool until the item is read.

        }

    }Reading from a FIFO

===================

建议用途

********A data item is removed from a FIFO by calling :c:func:`k_fifo_get`.



使用 FIFO 以"先进先出"方式异步传输任意大小的数据项。The following code builds on the example above, and uses the FIFO

to obtain data items from a producer thread,

配置选项which are then processed in some manner.

********

.. code-block:: c

相关配置选项:

    void consumer_thread(int unused1, int unused2, int unused3)

* 无    {

        struct data_item_t  *rx_data;

API 参考

********        while (1) {

            rx_data = k_fifo_get(&my_fifo, K_FOREVER);

.. doxygengroup:: fifo_apis

            /* process FIFO data item */
            ...
        }
    }

Suggested Uses
**************

Use a FIFO to asynchronously transfer data items of arbitrary size
in a "first in, first out" manner.

Configuration Options
*********************

Related configuration options:

* None

API Reference
*************

.. doxygengroup:: fifo_apis
