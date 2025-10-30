.. _polling_v2:

轮询 API
########

轮询 API 用于并发等待多个条件中的任何一个被满足。

.. contents::
    :local:
    :depth: 2

概念
****

轮询 API 的主要函数是 :c:func:`k_poll`,它在概念上与 POSIX :c:func:`poll`
函数非常相似,只是它操作的是内核对象而不是文件描述符。

轮询 API 允许单个线程并发等待一个或多个条件被满足,而无需主动逐个查看每个条件。

有一组有限的此类条件:

- 信号量变得可用
- 内核 FIFO 包含准备检索的数据
- 内核消息队列包含准备检索的数据
- 内核管道包含准备检索的数据
- 轮询信号被触发

想要等待多个条件的线程必须定义一个**轮询事件**数组,每个条件一个。

在可以轮询数组之前,必须初始化数组中的所有事件。

每个事件必须指定必须满足哪种**类型**的条件,以便其状态更改为发出所请求的
条件已满足的信号。

每个事件必须指定它希望满足条件的**内核对象**。

每个事件必须指定在满足条件时使用哪种**模式**的操作。

每个事件可以选择指定一个**标签**来根据用户的判断将多个事件分组在一起。

除了内核对象之外,还有一个可以直接发出信号的**轮询信号**伪对象类型。

:c:func:`k_poll` 函数一旦满足它正在等待的条件之一就会返回。当
:c:func:`k_poll` 返回时,可能有多个条件被满足,如果它们在
:c:func:`k_poll` 被调用之前就已被满足,或者由于内核的抢占式多线程性质。
调用者必须查看数组中所有轮询事件的状态,以确定哪些被满足以及要采取什么操作。

当前,只有一种操作模式可用:对象未被获取。例如,这意味着当 :c:func:`k_poll`
返回并且轮询事件状态指示信号量可用时,:c:func:`k_poll()` 的调用者必须调用
:c:func:`k_sem_take` 来获取信号量的所有权。如果信号量被竞争,则不能保证在
调用 :c:func:`k_sem_take` 时它仍然可用。

实现
****

使用 k_poll()
=============

主 API 是 :c:func:`k_poll`,它操作 :c:struct:`k_poll_event` 类型的轮询事件
数组。数组中的每个条目代表一个事件,对 :c:func:`k_poll` 的调用将等待其条件
被满足。

可以使用运行时初始化器 :c:macro:`K_POLL_EVENT_INITIALIZER()` 或
:c:func:`k_poll_event_init`,或静态初始化器
:c:macro:`K_POLL_EVENT_STATIC_INITIALIZER()` 初始化轮询事件。必须将与
指定的**类型**匹配的对象传递给初始化器。**模式***必须*设置为
:c:enumerator:`K_POLL_MODE_NOTIFY_ONLY`。状态*必须*设置为
:c:macro:`K_POLL_STATE_NOT_READY`(初始化器会处理这一点)。用户**标签**
是可选的,对 API 完全不透明:它在那里帮助用户将类似的事件分组在一起。作为
可选项,它传递给静态初始化器,但出于性能原因不传递给运行时初始化器。如果使用
运行时初始化器,用户必须在 :c:struct:`k_poll_event` 数据结构中单独设置它。
如果要忽略数组中的事件,很可能是暂时的,可以将其类型设置为
:c:macro:`K_POLL_TYPE_IGNORE`。

.. code-block:: c

    struct k_poll_event events[4] = {
        K_POLL_EVENT_STATIC_INITIALIZER(K_POLL_TYPE_SEM_AVAILABLE,
                                        K_POLL_MODE_NOTIFY_ONLY,
                                        &my_sem, 0),
        K_POLL_EVENT_STATIC_INITIALIZER(K_POLL_TYPE_FIFO_DATA_AVAILABLE,
                                        K_POLL_MODE_NOTIFY_ONLY,
                                        &my_fifo, 0),
        K_POLL_EVENT_STATIC_INITIALIZER(K_POLL_TYPE_MSGQ_DATA_AVAILABLE,
                                        K_POLL_MODE_NOTIFY_ONLY,
                                        &my_msgq, 0),
        K_POLL_EVENT_STATIC_INITIALIZER(K_POLL_TYPE_PIPE_DATA_AVAILABLE,
                                        K_POLL_MODE_NOTIFY_ONLY,
                                        &my_pipe, 0),
    };

或在运行时

.. code-block:: c

    struct k_poll_event events[4];
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

        k_poll_event_init(&events[2],
                          K_POLL_TYPE_MSGQ_DATA_AVAILABLE,
                          K_POLL_MODE_NOTIFY_ONLY,
                          &my_msgq);

        k_poll_event_init(&events[3],
                          K_POLL_TYPE_PIPE_DATA_AVAILABLE,
                          K_POLL_MODE_NOTIFY_ONLY,
                          &my_pipe);

        // 如果未使用,标签将保持未初始化状态
    }


初始化事件后,可以将数组传递给 :c:func:`k_poll`。可以指定超时仅等待指定的
时间量,或使用特殊值 :c:macro:`K_NO_WAIT` 和 :c:macro:`K_FOREVER` 来不等待
或等到事件条件被满足而不是更早。

在每个信号量或 FIFO 上提供一个轮询器列表,应用程序可以根据需要在其中等待任意
数量的事件。请注意,等待者将按照先来先服务的顺序提供服务,而不是按照优先级
顺序。

在成功的情况下,:c:func:`k_poll` 返回 0。如果超时,它返回
-:c:macro:`EAGAIN`。

.. code-block:: c

    // 假设此信号量和 FIFO 没有争用
    // 不会发生 -EADDRINUSE;信号量和/或数据将可用

    void do_stuff(void)
    {
        rc = k_poll(events, ARRAY_SIZE(events), K_MSEC(1000));
        if (rc == 0) {
            if (events[0].state == K_POLL_STATE_SEM_AVAILABLE) {
                k_sem_take(events[0].sem, 0);
            } else if (events[1].state == K_POLL_STATE_FIFO_DATA_AVAILABLE) {
                data = k_fifo_get(events[1].fifo, 0);
                // 处理数据
            } else if (events[2].state == K_POLL_STATE_MSGQ_DATA_AVAILABLE) {
                ret = k_msgq_get(events[2].msgq, buf, K_NO_WAIT);
                // 处理数据
            } else if (events[3].state == K_POLL_STATE_PIPE_DATA_AVAILABLE) {
                bytes_read = k_pipe_read(events[3].pipe, buf, bytes_to_read, K_NO_WAIT);
                // 处理数据
            }
        } else {
            // 处理超时
        }
    }

当在循环中调用 :c:func:`k_poll` 时,事件状态必须由用户重置为
:c:macro:`K_POLL_STATE_NOT_READY`。

.. code-block:: c

    void do_stuff(void)
    {
        for(;;) {
            rc = k_poll(events, ARRAY_SIZE(events), K_FOREVER);
            if (events[0].state == K_POLL_STATE_SEM_AVAILABLE) {
                k_sem_take(events[0].sem, 0);
            }
            if (events[1].state == K_POLL_STATE_FIFO_DATA_AVAILABLE) {
                data = k_fifo_get(events[1].fifo, 0);
                // 处理数据
            }
            if (events[2].state == K_POLL_STATE_MSGQ_DATA_AVAILABLE) {
                ret = k_msgq_get(events[2].msgq, buf, K_NO_WAIT);
                // 处理数据
            }
            if (events[3].state == K_POLL_STATE_PIPE_DATA_AVAILABLE) {
                bytes_read = k_pipe_read(events[3].pipe, buf, bytes_to_read, K_NO_WAIT);
                // 处理数据
            }
            events[0].state = K_POLL_STATE_NOT_READY;
            events[1].state = K_POLL_STATE_NOT_READY;
            events[2].state = K_POLL_STATE_NOT_READY;
            events[3].state = K_POLL_STATE_NOT_READY;
        }
    }

使用 k_poll_signal_raise()
===========================

事件类型之一是 :c:macro:`K_POLL_TYPE_SIGNAL`:这是对轮询事件的"直接"信号。
这可以看作是只有一个线程可以等待的轻量级二进制信号量。

轮询信号是 :c:struct:`k_poll_signal` 类型的单独对象,必须附加到
k_poll_event,类似于信号量或 FIFO。它必须首先通过
:c:macro:`K_POLL_SIGNAL_INITIALIZER()` 或 :c:func:`k_poll_signal_init`
初始化。

.. code-block:: c

    struct k_poll_signal signal;
    void do_stuff(void)
    {
        k_poll_signal_init(&signal);
    }

它通过 :c:func:`k_poll_signal_raise` 函数发出信号。此函数接受一个用户
**result** 参数,该参数对 API 不透明,可用于向等待事件的线程传递额外信息。

.. code-block:: c

    struct k_poll_signal signal;

    // 线程 A
    void do_stuff(void)
    {
        k_poll_signal_init(&signal);

        struct k_poll_event events[1] = {
            K_POLL_EVENT_INITIALIZER(K_POLL_TYPE_SIGNAL,
                                     K_POLL_MODE_NOTIFY_ONLY,
                                     &signal),
        };

        k_poll(events, 1, K_FOREVER);

        int signaled, result;

        k_poll_signal_check(&signal, &signaled, &result);

        if (signaled && (result == 0x1337)) {
            // A-OK!
        } else {
            // 奇怪的错误
        }
    }

    // 线程 B
    void signal_do_stuff(void)
    {
        k_poll_signal_raise(&signal, 0x1337);
    }

如果要在循环中轮询信号,则*必须*在每次迭代时将其事件状态重置为
:c:macro:`K_POLL_STATE_NOT_READY` *并且*如果它已被发出信号,则必须使用
:c:func:`k_poll_signal_reset()` 重置其 ``result``。

.. code-block:: c

    struct k_poll_signal signal;
    void do_stuff(void)
    {
        k_poll_signal_init(&signal);

        struct k_poll_event events[1] = {
            K_POLL_EVENT_INITIALIZER(K_POLL_TYPE_SIGNAL,
                                     K_POLL_MODE_NOTIFY_ONLY,
                                     &signal),
        };

        for (;;) {
            k_poll(events, 1, K_FOREVER);

            int signaled, result;

            k_poll_signal_check(&signal, &signaled, &result);

            if (signaled && (result == 0x1337)) {
                // A-OK!
            } else {
                // 奇怪的错误
            }

            k_poll_signal_reset(&signal);
            events[0].state = K_POLL_STATE_NOT_READY;
        }
    }

请注意,轮询信号在内部不同步。传递信号的 :c:func:`k_poll` 调用将在系统中
任何代码调用 :c:func:`k_poll_signal_raise()` 之后返回。但是,如果信号在外部
管理并通过 :c:func:`k_poll_signal_init()` 重置,则在应用程序检查时,事件
状态可能不再等于 :c:macro:`K_POLL_STATE_SIGNALED`,并且(天真的)应用程序
将错过事件。最佳实践始终是仅从调用 :c:func:`k_poll` 循环的线程内重置信号,
或者使用其他跟踪事件计数的事件类型:信号量和 FIFO 在这个意义上更防错,因为它们
在架构上不会"错过"事件。

建议用途
********

使用 :c:func:`k_poll` 合并多个线程,每个线程都在等待一个对象,从而节省可能
大量的栈空间。

如果只有一个线程挂起在轮询信号上,则将其用作轻量级二进制信号量。

.. note::
    因为只有在没有其他线程等待对象可用时才发出信号,并且只有一个线程可以轮询
    特定对象,所以当对象不是多个线程之间争用的主题时,轮询最好使用,基本上当
    单个线程作为多个对象的主"服务器"或"调度程序"运行并且是唯一尝试获取这些
    对象的线程时。

配置选项
********

相关配置选项:

* :kconfig:option:`CONFIG_POLL`

API 参考
********

.. doxygengroup:: poll_apis
