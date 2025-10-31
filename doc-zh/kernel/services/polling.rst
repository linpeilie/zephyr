.. _polling_v2:

轮询 API (Polling API)
######################

:c:func:`k_poll` API 是 Zephyr 的实现，类似于 POSIX 的 :c:func:`poll` API，
允许单个线程等待由一个或多个内核对象一次性触发的事件。这些对象可能是
信号量 (semaphores)、FIFO、LIFO、消息队列 (message queues)、管道 (pipes) 或轮询信号 (poll signals)。

.. contents::
    :local:
    :depth: 2

概念 (Concepts)
***************

:c:func:`k_poll` 的主要用途是当线程需要在多个对象上等待而不是主动轮询每个对象时。

不是主动轮询每个对象以检查它是否已就绪：

.. code-block:: c

    while (1) {
        if (k_sem_take(my_sem, K_NO_WAIT) == 0) {
            /* 在信号量上进行工作 */
        }
        if (k_fifo_get(my_fifo, K_NO_WAIT) != NULL) {
            /* 在 FIFO 获取上进行工作 */
        }
        if (k_msgq_get(my_msgq, &recv_buffer, K_NO_WAIT) == 0) {
            /* 在消息上进行工作 */
        }
        /* 必须添加人为延迟，否则如果没有就绪事件，循环会变得紧密 */
        k_sleep(K_MSEC(10));
    }

线程可以在多个对象上等待，直到其中一个对象就绪（可以理解为，直到其中一个对象满足
线程等待的条件时可以进行非阻塞操作）：

.. code-block:: c

    struct k_poll_event events[3] = {
        K_POLL_EVENT_INITIALIZER(K_POLL_TYPE_SEM_AVAILABLE,
                                 K_POLL_MODE_NOTIFY_ONLY,
                                 &my_sem),
        K_POLL_EVENT_INITIALIZER(K_POLL_TYPE_FIFO_DATA_AVAILABLE,
                                 K_POLL_MODE_NOTIFY_ONLY,
                                 &my_fifo),
        K_POLL_EVENT_INITIALIZER(K_POLL_TYPE_MSGQ_DATA_AVAILABLE,
                                 K_POLL_MODE_NOTIFY_ONLY,
                                 &my_msgq),
    };

    while (1) {
        k_poll(events, 3, K_FOREVER);

        if (events[0].state == K_POLL_STATE_SEM_AVAILABLE) {
            k_sem_take(events[0].sem, K_NO_WAIT);
            /* 在信号量上进行工作 */
            events[0].state = K_POLL_STATE_NOT_READY;
        }
        if (events[1].state == K_POLL_STATE_FIFO_DATA_AVAILABLE) {
            data = k_fifo_get(events[1].fifo, K_NO_WAIT);
            /* 在 FIFO 获取上进行工作 */
            events[1].state = K_POLL_STATE_NOT_READY;
        }
        if (events[2].state == K_POLL_STATE_MSGQ_DATA_AVAILABLE) {
            k_msgq_get(events[2].msgq, &recv_buffer, K_NO_WAIT);
            /* 在消息上进行工作 */
            events[2].state = K_POLL_STATE_NOT_READY;
        }
    }

轮询事件 (Poll Events)
=======================

轮询事件数组 (poll event array) 是传递给 :c:func:`k_poll` 的主要参数。
每个轮询事件必须由 :c:macro:`K_POLL_EVENT_INITIALIZER()` 单独初始化，
如果数组是静态声明的，或使用 :c:func:`k_poll_event_init`，如果数组在运行时创建。
提供所使用的事件类型的辅助函数，这取决于用户使用哪个函数来初始化它们。

轮询事件具有以下公共字段：

**state**
   *私有* (private)，但可以读取。

   轮询事件的状态。在轮询发生之前，应始终设置为 :c:macro:`K_POLL_STATE_NOT_READY`。
   轮询事件的有效值有：

   - :c:macro:`K_POLL_STATE_NOT_READY`

     轮询事件尚未就绪。

   - :c:macro:`K_POLL_STATE_SIGNALED`

     :c:func:`k_poll_signal_raise` 已在轮询信号上调用。

   - :c:macro:`K_POLL_STATE_SEM_AVAILABLE`

     如果在信号量上调用 :c:func:`k_sem_take`，它将成功。

   - :c:macro:`K_POLL_STATE_DATA_AVAILABLE`

     已弃用 (deprecated)。已被以下事件类型特定的状态值替换。

   - :c:macro:`K_POLL_STATE_FIFO_DATA_AVAILABLE`

     如果在 FIFO 上调用 :c:func:`k_fifo_get`，它将成功。

   - :c:macro:`K_POLL_STATE_MSGQ_DATA_AVAILABLE`

     如果在消息队列上调用 :c:func:`k_msgq_get`，它将成功。

   - :c:macro:`K_POLL_STATE_PIPE_DATA_AVAILABLE`

     如果在管道上调用 :c:func:`k_pipe_get`，它将成功。

   - :c:macro:`K_POLL_STATE_CANCELLED`

     轮询事件已取消，并将不再触发（详见下文）。

**type**
   设置为以下类型之一：

   - :c:macro:`K_POLL_TYPE_IGNORE`

     轮询事件将被忽略。

   - :c:macro:`K_POLL_TYPE_SIGNAL`

     轮询事件是轮询信号。

   - :c:macro:`K_POLL_TYPE_SEM_AVAILABLE`

     轮询事件监视信号量可用性。

   - :c:macro:`K_POLL_TYPE_DATA_AVAILABLE`

     已弃用 (deprecated)。轮询事件监视 FIFO 或消息队列数据可用性。
     事件处理程序应检查具体的 :c:member:`K_POLL_STATE_FIFO_DATA_AVAILABLE`
     或 :c:member:`K_POLL_STATE_MSGQ_DATA_AVAILABLE` 状态值。
     新代码应该使用以下类型特定的值。

   - :c:macro:`K_POLL_TYPE_FIFO_DATA_AVAILABLE`

     轮询事件监视 FIFO 数据可用性。

   - :c:macro:`K_POLL_TYPE_MSGQ_DATA_AVAILABLE`

     轮询事件监视消息队列数据可用性。

   - :c:macro:`K_POLL_TYPE_PIPE_DATA_AVAILABLE`

     轮询事件监视管道数据可用性。

**tag**
   一个用户定义的值，应用程序可能想要识别轮询事件。
   不必唯一，但应至少在相同类型的事件之间不同，以便于识别。

**mode**
   此字段仅接受一个值：:c:macro:`K_POLL_MODE_NOTIFY_ONLY`。
   它指定当触发事件被满足时，不会对对象执行任何操作，而只是通知线程。
   这目前是唯一可用的模式。

**obj**
   *私有* (private)。

   指向内核对象类型的指针。

每个初始化函数（宏或标准函数）接受 *type*、*mode* 和 *obj* 参数。
如果手动或在循环中初始化它们，建议使用标准函数。

事件类型 :c:macro:`K_POLL_TYPE_IGNORE` 很特殊，
因为它允许用户创建"sparse" (稀疏) 轮询事件数组：它用于填充不再需要被监视的数组槽。

它还是 :c:func:`k_poll` 通过将 *type* 设置为 :c:macro:`K_POLL_TYPE_IGNORE`
来取消尚未准备好的事件的机制。用户可以检查事件的 *state* 字段是否已设置为
:c:macro:`K_POLL_STATE_CANCELLED` 以了解事件已取消。

:c:macro:`K_POLL_EVENT_STATIC_INITIALIZER` 还有一个静态初始化器，
当数组本身静态声明时，可用于静态初始化数组。这类似于 :c:macro:`K_SEM_DEFINE`
和类似的初始化器。:c:macro:`K_POLL_EVENT_INITIALIZER` 和
:c:func:`k_poll_event_init` 由于初始化数组中的多个条目的能力而更灵活，
因此大多数应用程序应该使用它们中的一个。

可以通过将事件的状态重置为 :c:macro:`K_POLL_STATE_NOT_READY` 来在 :c:func:`k_poll` 的多次调用中重用事件数组。

当前实现中轮询事件数组的最大数量为 255。

.. note::
   **重要**：轮询事件必须在首次使用之前进行初始化。不初始化它们会产生不可预测的行为，
   例如在任何对象变得就绪之前 :c:func:`k_poll` 不会阻塞。

.. note::
   当就绪事件被检测到时，:c:func:`k_poll` 函数仅通知调用者。它*不*自动获取对象的所有权。
   例如，如果就绪事件是 :c:macro:`K_POLL_TYPE_SEM_AVAILABLE`，
   调用者必须使用 :c:func:`k_sem_take` 来获取信号量。

使用 (Usage)
============

主要 API 是 :c:func:`k_poll`，接受用户提供的轮询事件数组、数组中事件数量以及超时参数。
超时可以是 :c:macro:`K_NO_WAIT` 或 :c:macro:`K_FOREVER`，或者使用 :c:macro:`K_MSEC`、
:c:macro:`K_USEC`、:c:macro:`K_NSEC`、:c:macro:`K_TICKS` 或其他类似宏表示的超时（以毫秒、微秒、纳秒或 tick 为单位）。

.. note::
   当等待多个对象时，:c:func:`k_poll` 在对象之间没有优先级，
   而是使用先到先服务 (FCFS - first-come-first-serve) 算法。

在一个线程从 :c:func:`k_poll` 返回后，它必须遍历轮询事件数组以检查哪些对象已就绪。
它通过检查 *state* 字段来执行此操作。

如果在 :c:func:`k_poll` 上循环，用户必须在调用之间将 *state* 字段设置回
:c:macro:`K_POLL_STATE_NOT_READY`，
可能是在事件处理程序运行后。

.. note::
   :c:func:`k_poll` 不是线程安全的。这意味着不允许两个或多个线程使用相同的轮询事件数组调用它，
   即使轮询事件在数组中不同。如果一个或多个轮询线程在不同的轮询事件数组中等待同一对象，
   则该对象在满足时可能不会以先到先服务的方式唤醒它们。
   这些约束源于这样一个事实，即事件和轮询所属的对象通常不受锁保护，
   以允许低开销操作。

例如：

.. code-block:: c

    struct k_poll_event events[2];

    void some_init(void)
    {
        k_poll_event_init(&events[0],
                          K_POLL_TYPE_SEM_AVAILABLE,
                          K_POLL_MODE_NOTIFY_ONLY,
                          &my_sem);
        k_poll_event_init(&events[1],
                          K_POLL_TYPE_FIFO_DATA_AVAILABLE,
                          K_POLL_MODE_NOTIFY_ONLY,
                          &my_fifo);

        /* 第一次使用后，必须在每次调用 k_poll() 之间重新初始化状态：
         * 每次 k_poll() 返回时都必须这样做。
         */
        events[0].state = K_POLL_STATE_NOT_READY;
        events[1].state = K_POLL_STATE_NOT_READY;
    }

    void some_thread(void)
    {
        /* 将永远睡眠，直到事件发生：这不推荐 */
        rc = k_poll(events, 2, K_FOREVER);
        if (rc != 0) {
            printk("error: %d\n", rc);
        } else {
            if (events[0].state == K_POLL_STATE_SEM_AVAILABLE) {
                k_sem_take(events[0].sem, K_NO_WAIT);
                /* 在 sem 上工作 */
                events[0].state = K_POLL_STATE_NOT_READY;
            } else if (events[1].state == K_POLL_STATE_FIFO_DATA_AVAILABLE) {
                data = k_fifo_get(events[1].fifo, K_NO_WAIT);
                /* 在 data 上工作 */
                events[1].state = K_POLL_STATE_NOT_READY;
            }
        }

        /* 睡眠 50 毫秒，如果事件尚未准备好就放弃：这是*正确*的方式 */
        rc = k_poll(events, 2, K_MSEC(50));
        if (rc != 0) {
            printk("error: %d\n", rc);
        } else {
            if (events[0].state == K_POLL_STATE_SEM_AVAILABLE) {
                k_sem_take(events[0].sem, K_NO_WAIT);
                /* 在 sem 上工作 */
                events[0].state = K_POLL_STATE_NOT_READY;
            } else if (events[1].state == K_POLL_STATE_FIFO_DATA_AVAILABLE) {
                data = k_fifo_get(events[1].fifo, K_NO_WAIT);
                /* 在 data 上工作 */
                events[1].state = K_POLL_STATE_NOT_READY;
            }
        }
    }

轮询信号 (Poll Signals)
========================

轮询信号是专门提供给轮询 API 的内核对象。它们使应用程序、ISR 或内核本身能够以线程
可以使用 :c:func:`k_poll` API 等待的方式发出信号。

轮询信号类似于二进制信号量，但具有一些关键区别：

- 它们是专为轮询 API 设计的专用对象。
- 它们没有关联的等待队列——在它们上阻塞只能通过 :c:func:`k_poll` 进行。
- 它们可以携带可选的用户结果值。

它们有以下公共字段：

**signaled**
   *私有* (private)，但可以读取。

   如果值为 0，则信号未发出。任何非零值意味着它已发出。

**result**
   *私有* (private)，但可以读取。

   用户可以提供传递给 :c:func:`k_poll_signal_raise` 的整数值。
   API 接口不对此值进行任何处理。

轮询信号必须在使用前通过调用 :c:func:`k_poll_signal_init` 进行初始化。

使用方式与使用其他对象类似。然而，要在轮询信号上发出信号，必须使用专用函数
:c:func:`k_poll_signal_raise`。

此函数接受两个参数：

- 要发出信号的轮询信号
- 与信号关联的用户值（result）

可以通过调用 :c:func:`k_poll_signal_check` 从轮询信号获取信号状态和结果值。
此函数将清除信号的已发出状态以及信号的结果值。

应用程序可能希望在循环中重用轮询信号，在这种情况下，
它必须调用 :c:func:`k_poll_signal_reset` 以在每次调用 :c:func:`k_poll` 之间重置它，
类似于如何重置轮询事件。

.. note::
   :c:func:`k_poll_signal_check` 清除信号的已发出状态，
   而 :c:func:`k_poll_signal_reset` 既重置已发出状态也重置 result 值。

.. warning::
   轮询信号本身不提供对 ``signaled`` 和 ``result`` 字段的同步。
   这意味着即使在轮询线程中重置了信号，如果另一个线程在重置后和 :c:func:`k_poll` 调用前发出信号，
   可能会错过发出的信号。最安全的做法是仅从发出信号的同一上下文（例如，同一线程或 ISR）重置信号，
   或者如果需要计数发出的事件，请使用 :ref:`semaphores_v2` 或 :ref:`fifos_v2` 等对象。

.. code-block:: c

    struct k_poll_signal signal;

    void do_poll(void)
    {
        struct k_poll_event events[1];

        k_poll_signal_init(&signal);

        k_poll_event_init(&events[0],
                          K_POLL_TYPE_SIGNAL,
                          K_POLL_MODE_NOTIFY_ONLY,
                          &signal);

        events[0].state = K_POLL_STATE_NOT_READY;

        k_poll(events, 1, K_FOREVER);

        if (events[0].state == K_POLL_STATE_SIGNALED) {
            int result;
            unsigned int signaled;

            k_poll_signal_check(&signal, &signaled, &result);

            /* 检查是否已发出信号（should be 1） */
            if (signaled) {
                /* ... 在 result 上工作 ... */

                /* 可选，手动重置信号 */
                k_poll_signal_reset(&signal);
            }

            events[0].state = K_POLL_STATE_NOT_READY;
        }
    }

    void signal_poller(void)
    {
        k_poll_signal_raise(&signal, 0x1337);
    }

建议用途 (Suggested Uses)
**************************

使用轮询 API 在等待多个对象时合并等待线程的数量。

使用轮询信号将同一类型事件一起分组。例如，一个线程等待许多 GPIO 引脚的事件，
让每个 GPIO 引脚 ISR 发出轮询信号。这类似于具有单个服务器/分派器线程的用例，
所有事件都汇聚到该线程。

配置选项 (Configuration Options)
*********************************

相关配置选项：

* :kconfig:option:`CONFIG_POLL`

API 参考 (API Reference)
*************************

.. doxygengroup:: poll_apis
