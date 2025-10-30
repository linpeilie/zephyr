.. _stacks_v2:.. _stacks_v2:



栈Stacks

########



:dfn:`栈` 是一个内核对象,它实现了传统的后进先出 (LIFO) 队列,允许线程和 ISR A :dfn:`stack` is a kernel object that implements a traditional

添加和删除有限数量的整数数据值。last in, first out (LIFO) queue, allowing threads and ISRs

to add and remove a limited number of integer data values.

.. contents::

    :local:.. contents::

    :depth: 2    :local:

    :depth: 2

概念

****Concepts

********

可以定义任意数量的栈(仅受可用 RAM 限制)。每个栈由其内存地址引用。

Any number of stacks can be defined (limited only by available RAM). Each stack

栈具有以下关键属性:is referenced by its memory address.



* 已添加但尚未删除的整数数据值的**队列**。队列使用 stack_data_t 值数组实现,A stack has the following key properties:

  并且必须在本机字边界对齐。stack_data_t 类型对应于本机字大小,即根据 CPU

  架构和编译模式为 32 位或 64 位。* A **queue** of integer data values that have been added but not yet removed.

  The queue is implemented using an array of stack_data_t values

* 可以在数组中排队的数据值的**最大数量**。  and must be aligned on a native word boundary.

  The stack_data_t type corresponds to the native word size i.e. 32 bits or

栈在使用之前必须初始化。这会将其队列设置为空。  64 bits depending on the CPU architecture and compilation mode.



数据值可以由线程或 ISR **添加**到栈。如果存在等待的线程,则该值直接给予它;* A **maximum quantity** of data values that can be queued in the array.

否则该值被添加到 LIFO 的队列。

A stack must be initialized before it can be used. This sets its queue to empty.

.. note::

    如果启用了 :kconfig:option:`CONFIG_NO_RUNTIME_CHECKS`,内核将*不*检测A data value can be **added** to a stack by a thread or an ISR.

    和防止尝试向已达到其最大排队值数量的栈添加数据值。向已满的栈添加数据值将The value is given directly to a waiting thread, if one exists;

    导致数组溢出,并导致不可预测的行为。otherwise the value is added to the LIFO's queue.



数据值可以由线程从栈**删除**。如果栈的队列为空,线程可以选择等待它被给予。.. note::

任意数量的线程可以同时在空栈上等待。添加数据项时,它会被给予等待时间最长的    If :kconfig:option:`CONFIG_NO_RUNTIME_CHECKS` is enabled, the kernel will *not* detect

最高优先级线程。    and prevent attempts to add a data value to a stack that has already reached

    its maximum quantity of queued values. Adding a data value to a stack that is

.. note::    already full will result in array overflow, and lead to unpredictable behavior.

    内核确实允许 ISR 从栈删除项,但是如果栈为空,ISR 不得尝试等待。

A data value may be **removed** from a stack by a thread.

实现If the stack's queue is empty a thread may choose to wait for it to be given.

****Any number of threads may wait on an empty stack simultaneously.

When a data item is added, it is given to the highest priority thread

定义栈that has waited longest.

======

.. note::

使用类型 :c:struct:`k_stack` 的变量定义栈。然后必须通过调用     The kernel does allow an ISR to remove an item from a stack, however

:c:func:`k_stack_init` 或 :c:func:`k_stack_alloc_init` 初始化它。    the ISR must not attempt to wait if the stack is empty.

在后一种情况下,不提供缓冲区,而是从调用线程的资源池分配它。

Implementation

以下代码定义并初始化能够容纳最多十个字大小数据值的空栈。**************



.. code-block:: cDefining a Stack

================

    #define MAX_ITEMS 10

A stack is defined using a variable of type :c:struct:`k_stack`.

    stack_data_t my_stack_array[MAX_ITEMS];It must then be initialized by calling :c:func:`k_stack_init` or

    struct k_stack my_stack;:c:func:`k_stack_alloc_init`. In the latter case, a buffer is not

provided and it is instead allocated from the calling thread's resource

    k_stack_init(&my_stack, my_stack_array, MAX_ITEMS);pool.



或者,可以通过调用 :c:macro:`K_STACK_DEFINE` 在编译时定义和初始化栈。The following code defines and initializes an empty stack capable of holding

up to ten word-sized data values.

以下代码与上面的代码段具有相同的效果。请注意,宏定义了栈及其数据值数组。

.. code-block:: c

.. code-block:: c

    #define MAX_ITEMS 10

    K_STACK_DEFINE(my_stack, MAX_ITEMS);

    stack_data_t my_stack_array[MAX_ITEMS];

压入栈    struct k_stack my_stack;

======

    k_stack_init(&my_stack, my_stack_array, MAX_ITEMS);

通过调用 :c:func:`k_stack_push` 将数据项添加到栈。

Alternatively, a stack can be defined and initialized at compile time

以下代码基于上面的示例,并显示线程如何通过将其内存地址保存在栈中来创建数据结构池。by calling :c:macro:`K_STACK_DEFINE`.



.. code-block:: cThe following code has the same effect as the code segment above. Observe

that the macro defines both the stack and its array of data values.

    /* 定义数据结构数组 */

    struct my_buffer_type {.. code-block:: c

        int field1;

        ...    K_STACK_DEFINE(my_stack, MAX_ITEMS);

	};

    struct my_buffer_type my_buffers[MAX_ITEMS];Pushing to a Stack

==================

    /* 将每个数据结构的地址保存在栈中 */

    for (int i = 0; i < MAX_ITEMS; i++) {A data item is added to a stack by calling :c:func:`k_stack_push`.

        k_stack_push(&my_stack, (stack_data_t)&my_buffers[i]);

    }The following code builds on the example above, and shows how a thread

can create a pool of data structures by saving their memory addresses

从栈弹出in a stack.

========

.. code-block:: c

通过调用 :c:func:`k_stack_pop` 从栈获取数据项。

    /* define array of data structures */

以下代码基于上面的示例,并显示线程如何动态分配未使用的数据结构。当不再需要    struct my_buffer_type {

数据结构时,线程必须将其地址推回栈以允许重用数据结构。        int field1;

        ...

.. code-block:: c	};

    struct my_buffer_type my_buffers[MAX_ITEMS];

    struct my_buffer_type *new_buffer;

    /* save address of each data structure in a stack */

    k_stack_pop(&buffer_stack, (stack_data_t *)&new_buffer, K_FOREVER);    for (int i = 0; i < MAX_ITEMS; i++) {

    new_buffer->field1 = ...        k_stack_push(&my_stack, (stack_data_t)&my_buffers[i]);

    }

建议用途

********Popping from a Stack

====================

当已知存储项的最大数量时,使用栈以"后进先出"方式存储和检索整数数据值。

A data item is taken from a stack by calling :c:func:`k_stack_pop`.

配置选项

********The following code builds on the example above, and shows how a thread

can dynamically allocate an unused data structure.

相关配置选项:When the data structure is no longer required, the thread must push

its address back on the stack to allow the data structure to be reused.

* 无。

.. code-block:: c

API 参考

********    struct my_buffer_type *new_buffer;



.. doxygengroup:: stack_apis    k_stack_pop(&buffer_stack, (stack_data_t *)&new_buffer, K_FOREVER);

    new_buffer->field1 = ...

Suggested Uses
**************

Use a stack to store and retrieve integer data values in a "last in,
first out" manner, when the maximum number of stored items is known.

Configuration Options
*********************

Related configuration options:

* None.

API Reference
*************

.. doxygengroup:: stack_apis
