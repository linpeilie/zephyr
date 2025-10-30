.. _events:

事件
####

:dfn:`事件对象` 是实现传统事件的内核对象。

.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的事件对象(仅受可用 RAM 限制)。每个事件对象由其内存地址引用。
一个或多个线程可以等待事件对象,直到所需的事件集已传递到事件对象。当新事件传递
到事件对象时,所有等待条件已满足的线程同时变为就绪。

事件对象具有以下关键属性:

* 一个 32 位值,跟踪已传递给它的事件。

事件对象在使用之前必须初始化。

事件可以由线程或 ISR **传递**。传递事件时,事件可以覆盖现有的事件集或以位方式
添加到它们。覆盖现有的事件集时,这称为设置。以位方式添加到它们时,这称为发布。
发布和设置事件都有可能满足等待事件对象的多个线程的匹配条件。所有满足匹配条件的
线程同时变为活动状态。

线程可以等待一个或多个事件。它们可以等待所有请求的事件,也可以等待其中任何一个。
此外,发出等待请求的线程可以选择在等待之前重置事件对象跟踪的当前事件集。当多个
线程等待同一事件对象时,必须小心使用此选项。

.. note::
    内核确实允许 ISR 查询事件对象,但是 ISR 不得尝试等待事件。

实现
****

定义事件对象
============

使用类型 :c:struct:`k_event` 的变量定义事件对象。然后必须通过调用
:c:func:`k_event_init` 初始化它。

以下代码定义事件对象。

.. code-block:: c

    struct k_event my_event;

    k_event_init(&my_event);

或者,可以通过调用 :c:macro:`K_EVENT_DEFINE` 在编译时定义和初始化事件对象。

以下代码与上面的代码段具有相同的效果。

.. code-block:: c

    K_EVENT_DEFINE(my_event);

设置事件
========

通过调用 :c:func:`k_event_set` 设置事件对象中的事件。

以下代码基于上面的示例,将事件对象跟踪的事件设置为 0x001。

.. code-block:: c

    void input_available_interrupt_handler(void *arg)
    {
        /* 通知线程数据可用 */

        k_event_set(&my_event, 0x001);

        ...
    }

发布事件
========

通过调用 :c:func:`k_event_post` 将事件发布到事件对象。

以下代码基于上面的示例,将一组事件发布到事件对象。

.. code-block:: c

    void input_available_interrupt_handler(void *arg)
    {
        ...

        /* 通知线程更多数据可用 */

        k_event_post(&my_event, 0x120);

        ...
    }

等待事件(不删除)
=================

线程通过调用 :c:func:`k_event_wait` 等待事件。

以下代码基于上面的示例,等待最多 50 毫秒以发布任何指定的事件。如果没有及时发布
事件,则发出警告。

.. code-block:: c

    void consumer_thread(void)
    {
        uint32_t  events;

        events = k_event_wait(&my_event, 0xFFF, false, K_MSEC(50));
        if (events == 0) {
            printk("没有可用的输入设备!");
        } else {
            /* 访问所需的输入设备 */
            ...
        }
        ...
    }

或者,消费者线程可能希望在继续之前等待所有事件。

.. code-block:: c

    void consumer_thread(void)
    {
        uint32_t  events;

        events = k_event_wait_all(&my_event, 0x121, false, K_MSEC(50));
        if (events == 0) {
            printk("至少有一个输入设备不可用!");
        } else {
            /* 访问所需的输入设备 */
            ...
        }
        ...
    }

等待事件(带删除)
=================

线程通过调用 :c:func:`k_event_wait_safe` 等待事件(在接收时原子删除)。

以下代码基于上面的示例,等待最多 50 毫秒以发布任何指定的事件。如果没有及时发布
事件,则发出警告。

如果及时接收到事件,则在下次设置或发布事件之前,它们将不会出现在事件对象中。

.. code-block:: c

    void consumer_thread(void)
    {
        uint32_t  events;

        events = k_event_wait_safe(&my_event, 0xFFF, false, K_MSEC(50));
        if (events == 0) {
            printk("没有可用的输入设备!");
        } else {
            /* 访问所需的输入设备 */
            ...
        }
        ...
    }

或者,消费者线程可能希望在继续之前等待所有事件(在接收时原子删除),
使用 :c:func:`k_event_wait_all_safe`。

如果及时接收到所有事件,则在下次设置或发布事件之前,它们将不会出现在事件对象中。

.. code-block:: c

    void consumer_thread(void)
    {
        uint32_t  events;

        events = k_event_wait_all_safe(&my_event, 0x121, false, K_MSEC(50));
        if (events == 0) {
            printk("至少有一个输入设备不可用!");
        } else {
            /* 访问所需的输入设备 */
            ...
        }
        ...
    }

建议用途
********

使用事件来指示已发生一组条件。

使用事件一次将少量数据传递给多个线程。

配置选项
********

相关配置选项:

* :kconfig:option:`CONFIG_EVENTS`

API 参考
********

.. doxygengroup:: event_apis
