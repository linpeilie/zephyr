.. _events:

事件 (Events)
##############

:dfn:`事件对象 (event object)` 是一个内核对象，实现了传统的事件机制 (traditional events)。

.. contents::
    :local:
    :depth: 2

概念 (Concepts)
***************

可以定义任意数量的事件对象（仅受可用 RAM 限制）。每个事件对象通过其内存地址引用。一个或多个线程可以等待事件对象，直到所需的事件集合被传递到该事件对象。当新事件被传递到事件对象时，所有等待条件已满足的线程会同时变为就绪状态 (ready)。

事件对象具有以下关键属性：

* 一个 **32 位值 (32-bit value)**，用于跟踪已传递给它的事件。

事件对象在使用之前必须初始化。

事件可以由线程或 ISR **传递 (delivered)**。传递事件时，事件可以覆盖现有的事件集合，或者以按位 (bitwise) 方式添加到现有事件集合中。当覆盖现有事件集合时，这称为设置 (setting)。当以按位方式添加到现有事件集合时，这称为发布 (posting)。发布和设置事件都有可能满足等待该事件对象的多个线程的匹配条件 (match conditions)。所有满足匹配条件的线程会同时被激活 (made active)。

线程可以等待一个或多个事件。它们可以等待所有请求的事件，也可以等待其中任何一个事件。此外，发出等待请求的线程可以选择在等待之前重置事件对象跟踪的当前事件集合。当多个线程等待同一事件对象时，必须谨慎使用此选项。

.. note::
    内核确实允许 ISR 查询事件对象，但是 ISR 不得尝试等待事件。

实现 (Implementation)
*********************

定义事件对象 (Defining an Event Object)
========================================

事件对象使用 :c:struct:`k_event` 类型的变量定义。然后必须通过调用 :c:func:`k_event_init` 进行初始化。

以下代码定义了一个事件对象。

.. code-block:: c

    struct k_event my_event;

    k_event_init(&my_event);

或者，可以通过调用 :c:macro:`K_EVENT_DEFINE` 在编译时定义并初始化事件对象。

以下代码与上面的代码段具有相同的效果。

.. code-block:: c

    K_EVENT_DEFINE(my_event);

设置事件 (Setting Events)
==========================

通过调用 :c:func:`k_event_set` 来设置事件对象中的事件。

以下代码基于上面的示例，将事件对象跟踪的事件设置为 0x001。

.. code-block:: c

    void input_available_interrupt_handler(void *arg)
    {
        /* 通知线程数据可用 */

        k_event_set(&my_event, 0x001);

        ...
    }

发布事件 (Posting Events)
==========================

通过调用 :c:func:`k_event_post` 将事件发布到事件对象。

以下代码基于上面的示例，将一组事件发布到事件对象。

.. code-block:: c

    void input_available_interrupt_handler(void *arg)
    {
        ...

        /* 通知线程有更多数据可用 */

        k_event_post(&my_event, 0x120);

        ...
    }

等待事件（不移除）(Waiting for Events without removal)
=======================================================

线程通过调用 :c:func:`k_event_wait` 来等待事件。

以下代码基于上面的示例，等待最多 50 毫秒以发布任何指定的事件。如果没有及时发布事件，则会发出警告。

.. code-block:: c

    void consumer_thread(void)
    {
        uint32_t  events;

        events = k_event_wait(&my_event, 0xFFF, false, K_MSEC(50));
        if (events == 0) {
            printk("No input devices are available!");
        } else {
            /* 访问所需的输入设备 */
            ...
        }
        ...
    }

或者，消费者线程可能希望在继续之前等待所有事件。

.. code-block:: c

    void consumer_thread(void)
    {
        uint32_t  events;

        events = k_event_wait_all(&my_event, 0x121, false, K_MSEC(50));
        if (events == 0) {
            printk("At least one input device is not available!");
        } else {
            /* 访问所需的输入设备 */
            ...
        }
        ...
    }

等待事件（移除）(Waiting for Events with removal)
==================================================

线程通过调用 :c:func:`k_event_wait_safe` 来等待事件（接收时原子移除）。

以下代码基于上面的示例，等待最多 50 毫秒以发布任何指定的事件。如果没有及时发布事件，则会发出警告。

如果及时接收到事件，则在下次设置或发布事件之前，事件对象中不会存在这些事件。

.. code-block:: c

    void consumer_thread(void)
    {
        uint32_t  events;

        events = k_event_wait_safe(&my_event, 0xFFF, false, K_MSEC(50));
        if (events == 0) {
            printk("No input devices are available!");
        } else {
            /* 访问所需的输入设备 */
            ...
        }
        ...
    }

或者，消费者线程可能希望在继续之前等待所有事件（接收时原子移除），使用 :c:func:`k_event_wait_all_safe`。

如果及时接收到所有事件，则在下次设置或发布事件之前，事件对象中不会存在这些事件。

.. code-block:: c

    void consumer_thread(void)
    {
        uint32_t  events;

        events = k_event_wait_all_safe(&my_event, 0x121, false, K_MSEC(50));
        if (events == 0) {
            printk("At least one input device is not available!");
        } else {
            /* 访问所需的输入设备 */
            ...
        }
        ...
    }

建议用途 (Suggested Uses)
*************************

使用事件来指示一组条件已发生。

使用事件将少量数据同时传递给多个线程。

配置选项 (Configuration Options)
********************************

相关配置选项：

* :kconfig:option:`CONFIG_EVENTS`

API 参考 (API Reference)
************************

.. doxygengroup:: event_apis
