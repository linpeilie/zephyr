.. _message_queues_v2:

消息队列
########

:dfn:`消息队列` (message queue) 是一种内核对象 (kernel object)，实现了简单的消息队列，
允许线程 (threads) 和中断服务程序 (ISRs) 异步发送和接收固定大小的数据项。

.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的消息队列（仅受可用 RAM 限制）。每个消息队列通过其内存地址进行引用。

消息队列具有以下关键属性：

* 一个**环形缓冲区** (ring buffer)，包含已发送但尚未接收的数据项。

* 一个**数据项大小** (data item size)，以字节为单位。

* 一个**最大数量** (maximum quantity)，表示可在环形缓冲区中排队的数据项的最大数量。

消息队列在使用前必须进行初始化 (initialized)，这会将其环形缓冲区设置为空。

数据项可以由线程或 ISR **发送** (sent) 到消息队列。发送线程指向的数据项会被复制到等待线程
（如果存在）；否则该项会被复制到消息队列的环形缓冲区（如果有可用空间）。在任何情况下，
发送的数据区域的大小*必须*等于消息队列的数据项大小。

如果线程在环形缓冲区已满时尝试发送数据项，发送线程可以选择等待空间变得可用。
任意数量的发送线程可以在环形缓冲区已满时同时等待；当空间变得可用时，
它会被给到优先级最高且等待时间最长的发送线程。

数据项可以由线程从消息队列**接收** (received)。数据项会被复制到接收线程指定的区域；
接收区域的大小*必须*等于消息队列的数据项大小。

如果线程在环形缓冲区为空时尝试接收数据项，接收线程可以选择等待数据项被发送。
任意数量的接收线程可以在环形缓冲区为空时同时等待；当数据项变得可用时，
它会被给到优先级最高且等待时间最长的接收线程。

线程还可以**窥视** (peek) 消息队列头部的消息，而不将其从队列中移除。
数据项会被复制到接收线程指定的区域；接收区域的大小*必须*等于消息队列的数据项大小。

.. note::
    内核确实允许 ISR 从消息队列接收项，但如果消息队列为空，ISR 不得尝试等待。

.. note::
    消息队列的环形缓冲区不需要对齐。底层实现使用 :c:func:`memcpy`（与对齐无关），
    并且不会暴露任何内部指针。

实现
****

定义消息队列
===========

消息队列使用 :c:struct:`k_msgq` 类型的变量进行定义。然后必须通过调用 :c:func:`k_msgq_init` 进行初始化。

以下代码定义并初始化一个空的消息队列，该队列能够容纳 10 个项，每个项长 12 字节。

.. code-block:: c

    struct data_item_type {
        uint32_t field1;
	uint32_t field2;
	uint32_t field3;
    };

    char my_msgq_buffer[10 * sizeof(struct data_item_type)];
    struct k_msgq my_msgq;

    k_msgq_init(&my_msgq, my_msgq_buffer, sizeof(struct data_item_type), 10);

或者，可以通过调用 :c:macro:`K_MSGQ_DEFINE` 在编译时定义和初始化消息队列。

以下代码与上面的代码段具有相同的效果。请注意，该宏同时定义了消息队列及其缓冲区。

.. code-block:: c

    K_MSGQ_DEFINE(my_msgq, sizeof(struct data_item_type), 10, 1);

写入消息队列
===========

通过调用 :c:func:`k_msgq_put` 将数据项添加到消息队列。

以下代码基于上面的示例，使用消息队列将数据项从生产者线程传递给一个或多个消费者线程。
如果消息队列因为消费者跟不上而填满，生产者线程会丢弃所有现有数据，以便保存更新的数据。
请注意，此 API 将触发重新调度 (reschedule)。

.. code-block:: c

    void producer_thread(void)
    {
        struct data_item_type data;

        while (1) {
            /* 创建要发送的数据项（例如测量值、时间戳等） */
            data = ...

            /* 向消费者发送数据 */
            while (k_msgq_put(&my_msgq, &data, K_NO_WAIT) != 0) {
                /* 消息队列已满：清除旧数据并重试 */
                k_msgq_purge(&my_msgq);
            }

            /* 数据项已成功添加到消息队列 */
        }
    }

从消息队列读取
=============

通过调用 :c:func:`k_msgq_get` 从消息队列获取数据项。

以下代码基于上面的示例，使用消息队列处理由一个或多个生产者线程生成的数据项。
请注意，应测试 :c:func:`k_msgq_get` 的返回值，因为由于 :c:func:`k_msgq_purge` 可能会返回 ``-ENOMSG``。

.. code-block:: c

    void consumer_thread(void)
    {
        struct data_item_type data;

        while (1) {
            /* 获取数据项 */
            k_msgq_get(&my_msgq, &data, K_FOREVER);

            /* 处理数据项 */
            ...
        }
    }


窥视消息队列
===========

通过调用 :c:func:`k_msgq_peek` 从消息队列读取数据项。

以下代码窥视消息队列以读取队列头部由一个或多个生产者线程生成的数据项。

.. code-block:: c

    void consumer_thread(void)
    {
        struct data_item_type data;

        while (1) {
            /* 通过窥视队列来读取数据项 */
            k_msgq_peek(&my_msgq, &data);

            /* 处理数据项 */
            ...
        }
    }

建议用途
********

使用消息队列以异步方式在线程之间传输小数据项。

.. note::
    如果需要，消息队列也可以用于传输大数据项。但是，这可能会增加中断延迟 (interrupt latency)，
    因为在写入或读取数据项时中断会被锁定。写入或读取数据项的时间随其大小线性增加，
    因为该项会完整地复制到内存缓冲区或从内存缓冲区复制。因此，通常最好通过交换指向数据项的指针
    而不是数据项本身来传输大数据项。

    可以使用内核的邮箱对象类型 (mailbox object type) 实现同步传输。

配置选项
********

相关配置选项：

* 无。

API 参考
********

.. doxygengroup:: msgq_apis
