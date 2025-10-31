.. _stacks_v2:

栈 (Stacks)
###########

:dfn:`栈 (stack)` 是一个内核对象，实现了传统的后进先出 (LIFO, last in first out) 队列，允许线程和 ISR 添加和移除有限数量的整数数据值。

.. contents::
    :local:
    :depth: 2

概念 (Concepts)
***************

可以定义任意数量的栈（仅受可用 RAM 限制）。每个栈通过其内存地址引用。

栈具有以下关键属性：

* 一个已添加但尚未移除的整数数据值的 **队列 (queue)**。该队列使用 stack_data_t 值数组实现，并且必须在本机字边界 (native word boundary) 上对齐。stack_data_t 类型对应于本机字大小，即根据 CPU 架构和编译模式为 32 位或 64 位。

* 可在数组中排队的数据值的 **最大数量 (maximum quantity)**。

栈在使用之前必须初始化。这会将其队列设置为空。

数据值可以由线程或 ISR **添加 (added)** 到栈中。如果存在等待线程，该值会直接交给等待线程；否则该值会添加到 LIFO 的队列中。

.. note::
    如果启用了 :kconfig:option:`CONFIG_NO_RUNTIME_CHECKS`，内核将 *不会* 检测和防止向已达到其最大排队值数量的栈添加数据值的尝试。向已满的栈添加数据值将导致数组溢出，并导致不可预测的行为。

数据值可以由线程从栈中 **移除 (removed)**。如果栈的队列为空，线程可以选择等待它被赋值。任意数量的线程可以同时等待一个空栈。当添加数据项时，它会被交给等待时间最长的最高优先级线程。

.. note::
    内核确实允许 ISR 从栈中移除项，但是如果栈为空，ISR 不得尝试等待。

实现 (Implementation)
*********************

定义栈 (Defining a Stack)
==========================

栈使用 :c:struct:`k_stack` 类型的变量定义。然后必须通过调用 :c:func:`k_stack_init` 或 :c:func:`k_stack_alloc_init` 进行初始化。在后一种情况下，不提供缓冲区，而是从调用线程的资源池 (resource pool) 中分配。

以下代码定义并初始化了一个能够容纳最多十个字大小数据值的空栈。

.. code-block:: c

    #define MAX_ITEMS 10

    stack_data_t my_stack_array[MAX_ITEMS];
    struct k_stack my_stack;

    k_stack_init(&my_stack, my_stack_array, MAX_ITEMS);

或者，可以通过调用 :c:macro:`K_STACK_DEFINE` 在编译时定义并初始化栈。

以下代码与上面的代码段具有相同的效果。请注意，宏既定义了栈又定义了其数据值数组。

.. code-block:: c

    K_STACK_DEFINE(my_stack, MAX_ITEMS);

压入栈 (Pushing to a Stack)
============================

通过调用 :c:func:`k_stack_push` 将数据项添加到栈中。

以下代码基于上面的示例，展示了线程如何通过将数据结构的内存地址保存在栈中来创建数据结构池。

.. code-block:: c

    /* 定义数据结构数组 */
    struct my_buffer_type {
        int field1;
        ...
	};
    struct my_buffer_type my_buffers[MAX_ITEMS];

    /* 将每个数据结构的地址保存在栈中 */
    for (int i = 0; i < MAX_ITEMS; i++) {
        k_stack_push(&my_stack, (stack_data_t)&my_buffers[i]);
    }

从栈弹出 (Popping from a Stack)
================================

通过调用 :c:func:`k_stack_pop` 从栈中取出数据项。

以下代码基于上面的示例，展示了线程如何动态分配未使用的数据结构。当不再需要该数据结构时，线程必须将其地址推回栈中以允许数据结构被重用。

.. code-block:: c

    struct my_buffer_type *new_buffer;

    k_stack_pop(&buffer_stack, (stack_data_t *)&new_buffer, K_FOREVER);
    new_buffer->field1 = ...

建议用途 (Suggested Uses)
*************************

当已知存储项的最大数量时，使用栈以"后进先出"方式存储和检索整数数据值。

配置选项 (Configuration Options)
********************************

相关配置选项：

* 无。

API 参考 (API Reference)
************************

.. doxygengroup:: stack_apis
