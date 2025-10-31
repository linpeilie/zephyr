.. _condvar:

条件变量 (Condition Variables)
################################

:dfn:`条件变量 (condition variable)` 是一种同步原语 (synchronization primitive)，使线程能够等待直到特定条件发生。

.. contents::
    :local:
    :depth: 2

概念 (Concepts)
***************

可以定义任意数量的条件变量（仅受可用 RAM 限制）。每个条件变量通过其内存地址引用。

要等待某个条件变为真，线程可以使用条件变量。

条件变量基本上是一个线程队列 (queue of threads)，当某些执行状态（即某些条件）不符合预期时，线程可以将自己放入该队列中（通过等待该条件）。函数 :c:func:`k_condvar_wait` 原子地执行以下步骤：

#. 释放最后获取的互斥锁 (mutex)。
#. 将当前线程放入条件变量队列中。

当其他线程更改该状态时，可以通过使用 :c:func:`k_condvar_signal` 或 :c:func:`k_condvar_broadcast` 在条件上发信号来唤醒一个（或多个）等待线程，从而允许它们继续执行，然后：

#. 重新获取先前释放的互斥锁。
#. 从 :c:func:`k_condvar_wait` 返回。

条件变量在使用之前必须初始化。


实现 (Implementation)
*********************

定义条件变量 (Defining a Condition Variable)
============================================

条件变量使用 :c:struct:`k_condvar` 类型的变量定义。然后必须通过调用 :c:func:`k_condvar_init` 进行初始化。

以下代码定义了一个条件变量：

.. code-block:: c

    struct k_condvar my_condvar;

    k_condvar_init(&my_condvar);

或者，可以通过调用 :c:macro:`K_CONDVAR_DEFINE` 在编译时定义并初始化条件变量。

以下代码与上面的代码段具有相同的效果。

.. code-block:: c

    K_CONDVAR_DEFINE(my_condvar);

等待条件变量 (Waiting on a Condition Variable)
===============================================

线程可以通过调用 :c:func:`k_condvar_wait` 来等待条件。

以下代码在条件变量上等待。


.. code-block:: c

    K_MUTEX_DEFINE(mutex);
    K_CONDVAR_DEFINE(condvar)

    int main(void)
    {
        k_mutex_lock(&mutex, K_FOREVER);

        /* 阻塞此线程，直到另一个线程发出 cond 信号。在阻塞期间，
         * 互斥锁被释放，然后在此线程被唤醒并且调用返回之前重新获取。
         */
        k_condvar_wait(&condvar, &mutex, K_FOREVER);
        ...
        k_mutex_unlock(&mutex);
    }

给条件变量发信号 (Signaling a Condition Variable)
==================================================

通过调用 :c:func:`k_condvar_signal` 为一个线程发信号，或通过调用 :c:func:`k_condvar_broadcast` 为多个线程发信号。

以下代码基于上面的示例构建。

.. code-block:: c

    void worker_thread(void)
    {
        k_mutex_lock(&mutex, K_FOREVER);

        /*
         * 执行一些工作并满足条件
         */
        ...
        ...
        k_condvar_signal(&condvar);
        k_mutex_unlock(&mutex);
    }

建议用途 (Suggested Uses)
*************************

使用条件变量与互斥锁结合，从一个线程向另一个线程发送状态（条件）变化的信号。条件变量不是条件本身，它们也不是事件。条件包含在周围的编程逻辑中。

互斥锁本身不被设计用作通知/同步机制 (notification/synchronization mechanism)。它们仅用于提供对共享资源的互斥访问。

配置选项 (Configuration Options)
********************************

相关配置选项：

* 无。

API 参考 (API Reference)
************************

.. doxygengroup:: condvar_apis
