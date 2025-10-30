.. _condvar:

条件变量
########

:dfn:`条件变量` 是一个同步原语,使线程能够等待直到特定条件发生。

.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的条件变量(仅受可用 RAM 限制)。每个条件变量由其内存地址引用。

要等待条件变为真,线程可以使用条件变量。

条件变量基本上是线程可以在某些执行状态(即某些条件)不符合期望时(通过等待条件)
将自己放入的线程队列。函数 :c:func:`k_condvar_wait` 原子地执行以下步骤;

#. 释放最后获取的互斥锁。
#. 将当前线程放入条件变量队列。

其他线程在更改所述状态时,可以通过使用 :c:func:`k_condvar_signal` 或
:c:func:`k_condvar_broadcast` 在条件上发出信号来唤醒一个(或多个)等待的线程,
从而允许它们继续,然后它:

#. 重新获取先前释放的互斥锁。
#. 从 :c:func:`k_condvar_wait` 返回。

条件变量在使用之前必须初始化。

实现
****

定义条件变量
============

使用类型 :c:struct:`k_condvar` 的变量定义条件变量。然后必须通过调用
:c:func:`k_condvar_init` 初始化它。

以下代码定义条件变量:

.. code-block:: c

    struct k_condvar my_condvar;

    k_condvar_init(&my_condvar);

或者,可以通过调用 :c:macro:`K_CONDVAR_DEFINE` 在编译时定义和初始化条件变量。

以下代码与上面的代码段具有相同的效果。

.. code-block:: c

    K_CONDVAR_DEFINE(my_condvar);

等待条件变量
============

线程可以通过调用 :c:func:`k_condvar_wait` 等待条件。

以下代码等待条件变量。

.. code-block:: c

    K_MUTEX_DEFINE(mutex);
    K_CONDVAR_DEFINE(condvar)

    int main(void)
    {
        k_mutex_lock(&mutex, K_FOREVER);

        /* 阻塞此线程,直到另一个线程发出 cond 信号。在阻塞时,
         * 互斥锁被释放,然后在此线程被唤醒并且调用返回之前重新获取。
         */
        k_condvar_wait(&condvar, &mutex, K_FOREVER);
        ...
        k_mutex_unlock(&mutex);
    }

发信号条件变量
==============

通过调用 :c:func:`k_condvar_signal` 为一个线程发信号条件变量,或通过调用
:c:func:`k_condvar_broadcast` 为多个线程发信号。

以下代码基于上面的示例。

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

建议用途
********

使用条件变量与互斥锁一起从一个线程向另一个线程发送更改状态(条件)的信号。
条件变量本身不是条件,它们也不是事件。条件包含在周围的编程逻辑中。

互斥锁本身不设计用作通知/同步机制。它们仅用于提供对共享资源的互斥访问。

配置选项
********

相关配置选项:

* 无。

API 参考
********

.. doxygengroup:: condvar_apis
