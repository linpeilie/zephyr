.. _lifos_v2:

LIFO 队列
#########

:dfn:`LIFO` 是一种内核对象 (kernel object)，实现了传统的后进先出 (last in, first out, LIFO) 队列，
允许线程 (threads) 和中断服务程序 (ISRs) 添加和移除任意大小的数据项。

.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的 LIFO 队列（仅受可用 RAM 限制）。每个 LIFO 通过其内存地址进行引用。

LIFO 具有以下关键属性：

* 一个**队列** (queue)，包含已添加但尚未移除的数据项。
  该队列实现为一个简单的链表 (linked list)。

LIFO 在使用前必须进行初始化 (initialized)，这会将其队列设置为空。

LIFO 数据项必须按字边界 (word boundary) 对齐，因为内核保留项的第一个字用作指向队列中
下一个数据项的指针。因此，一个包含 N 字节应用数据的数据项需要 N+4（或 N+8）字节的内存。
如果使用 :c:func:`k_lifo_alloc_put` 添加数据项，则数据项没有对齐或保留空间要求，
而是从调用线程的资源池 (resource pool) 中临时分配额外的内存。

.. note::
    LIFO 数据项在所有 LIFO 数据队列中仅限于单个活动实例。任何尝试在数据项从之前添加的队列中
    移除之前将其重新添加到队列的操作都将导致未定义的行为 (undefined behavior)。

数据项可以由线程或 ISR **添加** (added) 到 LIFO。如果存在等待的线程，该项会直接给到该线程；
否则该项会被添加到 LIFO 的队列中。对可排队的项数没有限制。

数据项可以由线程从 LIFO **移除** (removed)。如果 LIFO 的队列为空，线程可以选择等待数据项的到来。
任意数量的线程可以同时在空的 LIFO 上等待。当添加数据项时，它会被给到优先级最高且等待时间最长的线程。

.. note::
    内核确实允许 ISR 从 LIFO 移除项，但如果 LIFO 为空，ISR 不得尝试等待。

实现
****

定义 LIFO
=========

LIFO 使用 :c:struct:`k_lifo` 类型的变量进行定义。然后必须通过调用 :c:func:`k_lifo_init` 进行初始化。

以下代码定义并初始化一个空的 LIFO。

.. code-block:: c

    struct k_lifo my_lifo;

    k_lifo_init(&my_lifo);

或者，可以通过调用 :c:macro:`K_LIFO_DEFINE` 在编译时定义和初始化一个空的 LIFO。

以下代码与上面的代码段具有相同的效果。

.. code-block:: c

    K_LIFO_DEFINE(my_lifo);

写入 LIFO
=========

通过调用 :c:func:`k_lifo_put` 将数据项添加到 LIFO。

以下代码基于上面的示例，使用 LIFO 向一个或多个消费者线程发送数据。

.. code-block:: c

    struct data_item_t {
        void *LIFO_reserved;   /* 第一个字保留供 LIFO 使用 */
        ...
    };

    struct data_item_t tx data;

    void producer_thread(int unused1, int unused2, int unused3)
    {
        while (1) {
            /* 创建要发送的数据项 */
            tx_data = ...

            /* 向消费者发送数据 */
            k_lifo_put(&my_lifo, &tx_data);

            ...
        }
    }

数据项可以使用 :c:func:`k_lifo_alloc_put` 添加到 LIFO。使用此 API 时，无需在数据项中
为内核的使用保留空间，而是会从调用线程的资源池中分配额外的内存，直到该项被读取。

从 LIFO 读取
===========

通过调用 :c:func:`k_lifo_get` 从 LIFO 移除数据项。

以下代码基于上面的示例，使用 LIFO 从生产者线程获取数据项，然后以某种方式处理这些数据项。

.. code-block:: c

    void consumer_thread(int unused1, int unused2, int unused3)
    {
        struct data_item_t  *rx_data;

        while (1) {
            rx_data = k_lifo_get(&my_lifo, K_FOREVER);

            /* 处理 LIFO 数据项 */
            ...
        }
    }

建议用途
********

使用 LIFO 以"后进先出"方式异步传输任意大小的数据项。

配置选项
********

相关配置选项：

* 无。

API 参考
********

.. doxygengroup:: lifo_apis
