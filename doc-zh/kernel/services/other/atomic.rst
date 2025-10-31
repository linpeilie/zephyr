.. _atomic_v2:

原子操作服务
############

:dfn:`原子变量` (atomic variable) 是可以由线程和 ISR 以不可中断方式读取和修改的变量。
在 32 位机器上它是 32 位变量，在 64 位机器上它是 64 位变量。

.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的原子变量（仅受可用 RAM 限制）。

使用内核的原子 API 操作原子变量可以保证所需的操作正确发生，即使更高优先级的上下文也操作同一变量。

内核还支持对原子变量数组中的单个位进行原子操作。

实现
****

定义原子变量
===========

原子变量使用 :c:type:`atomic_t` 类型的变量进行定义。

默认情况下，原子变量初始化为零。但是，可以使用 :c:macro:`ATOMIC_INIT` 为其赋予不同的值：

.. code-block:: c

    atomic_t flags = ATOMIC_INIT(0xFF);

操作原子变量
===========

原子变量使用本节末尾列出的 API 进行操作。

以下代码显示了如何使用原子变量来跟踪函数被调用的次数。由于计数是原子递增的，
因此如果调用该函数的线程在调用过程中被更高优先级的上下文（也调用该例程）中断，
也不会有计数在递增过程中损坏的风险。

.. code-block:: c

    atomic_t call_count;

    int call_counting_routine(void)
    {
        /* 递增调用计数器 */
        atomic_inc(&call_count);

        /* 执行例程的其余处理 */
        ...
    }

操作原子变量数组
===============

可以按照传统方式定义 32 位原子变量数组。但是，您也可以使用 :c:macro:`ATOMIC_DEFINE`
定义 N 位原子变量数组。

可以使用本节末尾列出的以 :c:func:`_bit` 结尾的 API 来操作原子变量数组中的单个位。

以下代码显示了如何使用原子变量数组实现一组 200 个标志位。

.. code-block:: c

    #define NUM_FLAG_BITS 200

    ATOMIC_DEFINE(flag_bits, NUM_FLAG_BITS);

    /* 设置指定的标志位并返回其先前的值 */
    int set_flag_bit(int bit_position)
    {
        return (int)atomic_set_bit(flag_bits, bit_position);
    }

内存顺序
========

为了一致性和正确性，所有 Zephyr 原子 API 都应包含完整的内存屏障 (memory barrier)
（在例如 x86 上的"序列化"指令、ARM 上的"DMB"或 C++ 内存模型定义的"顺序一致"操作的意义上），
在硬件需要时保证跨上下文的可靠图景。任何特定于架构的实现都负责确保此行为。

建议用途
********

使用原子变量来实现仅需要操作单个 32 位值的临界区处理 (critical section processing)。

使用多个原子变量来实现对位数组中超过 32 位的一组标志位的临界区处理。

.. note::
    使用原子变量通常比使用其他技术（如使用互斥锁 (mutex) 或锁定中断 (locking interrupts)）
    来实现临界区要高效得多。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_ATOMIC_OPERATIONS_BUILTIN`
* :kconfig:option:`CONFIG_ATOMIC_OPERATIONS_ARCH`
* :kconfig:option:`CONFIG_ATOMIC_OPERATIONS_C`

API 参考
********

.. important::
    所有原子服务 API 都可以由线程和 ISR 使用。

.. doxygengroup:: atomic_apis
