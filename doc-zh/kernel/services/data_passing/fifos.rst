.. _fifos_v2:

FIFO 队列
#########

:dfn:`FIFO` 是一种内核对象 (kernel object)，实现了传统的先进先出 (first in, first out, FIFO) 队列，
允许线程 (threads) 和中断服务程序 (ISRs) 添加和移除任意大小的数据项。

.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的 FIFO 队列（仅受可用 RAM 限制）。每个 FIFO 通过其内存地址进行引用。

FIFO 具有以下关键属性：

* 一个**队列** (queue)，包含已添加但尚未移除的数据项。
  该队列实现为一个简单的链表 (linked list)。

FIFO 在使用前必须进行初始化 (initialized)，这会将其队列设置为空。

FIFO 数据项必须按字边界 (word boundary) 对齐，因为内核保留项的第一个字用作指向队列中
下一个数据项的指针。因此，一个包含 N 字节应用数据的数据项需要 N+4（或 N+8）字节的内存。
如果使用 :c:func:`k_fifo_alloc_put` 添加数据项，则数据项没有对齐或保留空间要求，
而是从调用线程的资源池 (resource pool) 中临时分配额外的内存。

.. note::
    FIFO 数据项在所有 FIFO 数据队列中仅限于单个活动实例。任何尝试在数据项从之前添加的队列中
    移除之前将其重新添加到队列的操作都将导致未定义的行为 (undefined behavior)。

数据项可以由线程或 ISR **添加** (added) 到 FIFO。如果存在等待的线程，该项会直接给到该线程；
否则该项会被添加到 FIFO 的队列中。对可排队的项数没有限制。

数据项可以由线程从 FIFO **移除** (removed)。如果 FIFO 的队列为空，线程可以选择等待数据项的到来。
任意数量的线程可以同时在空的 FIFO 上等待。当添加数据项时，它会被给到优先级最高且等待时间最长的线程。

.. note::
    内核确实允许 ISR 从 FIFO 移除项，但如果 FIFO 为空，ISR 不得尝试等待。

如果需要，可以在单个操作中将**多个数据项** (multiple data items) 添加到 FIFO，前提是它们链接成
单链表 (singly-linked list)。如果多个写入者向 FIFO 添加相关数据项集合，此功能会很有用，
因为它可以确保每个集合中的数据项不会与其他数据项交错。将多个数据项添加到 FIFO 也比逐个添加更高效，
并且可以用于保证移除集合中第一个数据项的任何人都能够移除剩余的数据项而无需等待。

实现
****

定义 FIFO
=========

FIFO 使用 :c:struct:`k_fifo` 类型的变量进行定义。然后必须通过调用 :c:func:`k_fifo_init` 进行初始化。

以下代码定义并初始化一个空的 FIFO。

.. code-block:: c

    struct k_fifo my_fifo;

    k_fifo_init(&my_fifo);

或者，可以通过调用 :c:macro:`K_FIFO_DEFINE` 在编译时定义和初始化一个空的 FIFO。

以下代码与上面的代码段具有相同的效果。

.. code-block:: c

    K_FIFO_DEFINE(my_fifo);

写入 FIFO
=========

通过调用 :c:func:`k_fifo_put` 将数据项添加到 FIFO。

以下代码基于上面的示例，使用 FIFO 向一个或多个消费者线程发送数据。

.. code-block:: c

    struct data_item_t {
        void *fifo_reserved;   /* 第一个字保留供 FIFO 使用 */
        ...
    };

    struct data_item_t tx_data;

    void producer_thread(int unused1, int unused2, int unused3)
    {
        while (1) {
            /* 创建要发送的数据项 */
            tx_data = ...

            /* 向消费者发送数据 */
            k_fifo_put(&my_fifo, &tx_data);

            ...
        }
    }

此外，可以通过调用 :c:func:`k_fifo_put_list` 或 :c:func:`k_fifo_put_slist` 将单链表数据项
添加到 FIFO。

最后，数据项可以使用 :c:func:`k_fifo_alloc_put` 添加到 FIFO。使用此 API 时，无需在数据项中
为内核的使用保留空间，而是会从调用线程的资源池中分配额外的内存，直到该项被读取。

从 FIFO 读取
===========

通过调用 :c:func:`k_fifo_get` 从 FIFO 移除数据项。

以下代码基于上面的示例，使用 FIFO 从生产者线程获取数据项，然后以某种方式处理这些数据项。

.. code-block:: c

    void consumer_thread(int unused1, int unused2, int unused3)
    {
        struct data_item_t  *rx_data;

        while (1) {
            rx_data = k_fifo_get(&my_fifo, K_FOREVER);

            /* 处理 FIFO 数据项 */
            ...
        }
    }

建议用途
********

使用 FIFO 以"先进先出"方式异步传输任意大小的数据项。

配置选项
********

相关配置选项：

* 无

API 参考
********

.. doxygengroup:: fifo_apis
