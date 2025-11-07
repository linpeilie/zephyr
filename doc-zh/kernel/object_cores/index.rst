.. _object_cores_api:

对象核心 (Object Cores)
########################

对象核心是一种内核调试工具,可用于识别和执行已注册对象的操作。

.. contents::
    :local:
    :depth: 2

对象核心概念 (Object Core Concepts)
************************************

每个对象实例都嵌入了一个名为 ``obj_core`` 的对象核心字段。
相同类型的对象通过各自的对象核心链接在一起,形成一个单链表。每个对象核心还链接到其
各自的对象类型。每个对象类型包含一个单链表,将该类型的所有对象核心链接在一起。对象类型也
通过单链表链接在一起。这样可以允许调试工具遍历系统中的所有对象。

对象核心已集成到以下内核对象中:
 * :ref:`条件变量 (Condition Variables) <condvar>`
 * :ref:`事件 (Events) <events>`
 * :ref:`FIFO <fifos_v2>` 和 :ref:`LIFO <lifos_v2>`
 * :ref:`邮箱 (Mailboxes) <mailboxes_v2>`
 * :ref:`内存板 (Memory Slabs) <memory_slabs_v2>`
 * :ref:`消息队列 (Message Queues) <message_queues_v2>`
 * :ref:`互斥锁 (Mutexes) <mutexes_v2>`
 * :ref:`管道 (Pipes) <pipes_v2>`
 * :ref:`信号量 (Semaphores) <semaphores_v2>`
 * :ref:`线程 (Threads) <threads_v2>`
 * :ref:`定时器 (Timers) <timers_v2>`
 * :ref:`系统内存块 (System Memory Blocks) <sys_mem_blocks>`

开发人员可以根据需要将它们集成到项目中的其他对象中。

对象核心统计概念 (Object Core Statistics Concepts)
****************************************************
各种内核对象允许收集和报告统计信息。
对象核心提供了一种统一的方法,通过对象核心统计来检索该信息。启用时,对象类型包含指向
统计描述符的指针,该描述符定义了已启用的与对象统计接口的各种操作。此外,对象
核心包含指向与该对象关联的"原始"统计信息的指针。原始数据是与统计信息关联的原始、未经处理的数据。查询的数据可能是"原始"的,但也可能已通过
计算以某种方式进行了处理(例如确定平均值)。

下表指示已集成到对象核心统计中的对象,以及用于"原始"和"查询"数据的结构。

=====================  ============================== ==============================
对象 (Object)          原始数据类型 (Raw Data Type)   查询数据类型 (Query Data Type)
=====================  ============================== ==============================
struct mem_slab        struct mem_slab_info            struct sys_memory_stats
struct sys_mem_blocks  struct sys_mem_blocks_info      struct sys_memory_stats
struct k_thread        struct k_cycle_stats            struct k_thread_runtime_stats
struct _cpu            struct k_cycle_stats            struct k_thread_runtime_stats
struct z_kernel        struct k_cycle_stats[num CPUs]  struct k_thread_runtime_stats
=====================  ============================== ==============================

实现 (Implementation)
**********************

定义新对象类型 (Defining a New Object Type)
============================================

对象类型使用类型为 :c:struct:`k_obj_type` 的全局变量定义。必须在初始化该类型的任何对象之前初始化它。以下代码显示了如何初始化新对象类型以用于对象核心和对象核心统计。

.. code-block:: c

    /* 唯一对象类型 ID */

    #define K_OBJ_TYPE_MY_NEW_TYPE  K_OBJ_TYPE_ID_GEN("UNIQ")
    struct k_obj_type  my_obj_type;

    struct my_obj_type_raw_info {
        ...
    };

    struct my_obj_type_query_stats {
        ...
    };

    struct my_new_obj {
        ...
        struct k_obj_core obj_core;
        struct my_obj_type_raw_info  info;
    };

    struct k_obj_core_stats_desc my_obj_type_stats_desc = {
        .raw_size = sizeof(struct my_obj_type_raw_stats),
        .query_size = sizeof(struct my_obj_type_query_stats),
        .raw = my_obj_type_stats_raw,
        .query = my_obj_type_stats_query,
        .reset = my_obj_type_stats_reset,
        .disable = NULL,    /* 统计收集始终开启 */
        .enable = NULL,     /* 统计收集始终开启 */
    };

    void my_obj_type_init(void)
    {
        z_obj_type_init(&my_obj_type, K_OBJ_TYPE_MY_NEW_TYPE,
                        offsetof(struct my_new_obj, obj_core);
        k_obj_type_stats_init(&my_obj_type, &my_obj_type_stats_desc);
    }

初始化新对象核心 (Initializing a New Object Core)
==================================================

已集成到对象核心框架中的内核对象在初始化对象时会自动初始化其对象核心。但是,希望将自己的对象添加到框架中的开发人员需要同时初始化对象核心并将其链接。以下代码基于上面的示例并初始化对象核心。

.. code-block:: c

    void my_new_obj_init(struct my_new_obj *new_obj)
    {
        ...
        k_obj_core_init(K_OBJ_CORE(new_obj), &my_obj_type);
        k_obj_core_link(K_OBJ_CORE(new_obj));
        k_obj_core_stats_register(K_OBJ_CORE(new_obj), &new_obj->raw_stats,
                                  sizeof(struct my_obj_type_raw_info));
    }

遍历对象核心列表 (Walking a List of Object Cores)
==================================================

存在两个例程用于遍历链接到对象类型的对象核心列表。这些是 :c:func:`k_obj_type_walk_locked` 和
:c:func:`k_obj_type_walk_unlocked`。以下代码基于上面的示例并打印该新对象类型的所有对象的地址。

.. code-block:: c

    int walk_op(struct k_obj_core *obj_core, void *data)
    {
        uint8_t *ptr;

        ptr = obj_core;
        ptr -= obj_core->type->obj_core_offset;

        printk("%p\n", ptr);

        return 0;
    }

    void print_object_addresses(void)
    {
        struct k_obj_type *obj_type;

        /* 查找对象类型 */

        obj_type = k_obj_type_find(K_OBJ_TYPE_MY_NEW_TYPE);

        /* 遍历对象列表 */

        k_obj_type_walk_unlocked(obj_type, walk_op, NULL);
    }

对象核心统计查询 (Object Core Statistics Querying)
===================================================

以下代码基于上面的示例,显示了集成到对象核心统计框架中的对象如何检索查询的数据并重置与对象关联的统计信息。

.. code-block:: c

    struct my_new_obj my_obj;

    ...

    void my_func(void)
    {
        struct my_obj_type_query_stats  my_stats;
        int  status;

        my_obj_type_init(&my_obj);

        ...

        status = k_obj_core_stats_query(K_OBJ_CORE(&my_obj),
                                        &my_stats, sizeof(my_stats));
        if (status != 0) {
            /* 获取统计失败 */
            ...
        } else {
            k_obj_core_stats_reset(K_OBJ_CORE(&my_obj));
        }

        ...
    }

配置选项 (Configuration Options)
*********************************

相关配置选项:

* :kconfig:option:`CONFIG_OBJ_CORE`
* :kconfig:option:`CONFIG_OBJ_CORE_CONDVAR`
* :kconfig:option:`CONFIG_OBJ_CORE_EVENT`
* :kconfig:option:`CONFIG_OBJ_CORE_FIFO`
* :kconfig:option:`CONFIG_OBJ_CORE_LIFO`
* :kconfig:option:`CONFIG_OBJ_CORE_MAILBOX`
* :kconfig:option:`CONFIG_OBJ_CORE_MEM_SLAB`
* :kconfig:option:`CONFIG_OBJ_CORE_MSGQ`
* :kconfig:option:`CONFIG_OBJ_CORE_MUTEX`
* :kconfig:option:`CONFIG_OBJ_CORE_PIPE`
* :kconfig:option:`CONFIG_OBJ_CORE_SEM`
* :kconfig:option:`CONFIG_OBJ_CORE_STACK`
* :kconfig:option:`CONFIG_OBJ_CORE_THREAD`
* :kconfig:option:`CONFIG_OBJ_CORE_TIMER`
* :kconfig:option:`CONFIG_OBJ_CORE_SYS_MEM_BLOCKS`
* :kconfig:option:`CONFIG_OBJ_CORE_STATS`
* :kconfig:option:`CONFIG_OBJ_CORE_STATS_MEM_SLAB`
* :kconfig:option:`CONFIG_OBJ_CORE_STATS_THREAD`
* :kconfig:option:`CONFIG_OBJ_CORE_STATS_SYSTEM`
* :kconfig:option:`CONFIG_OBJ_CORE_STATS_SYS_MEM_BLOCKS`

API 参考 (API Reference)
*************************

.. doxygengroup:: obj_core_apis
.. doxygengroup:: obj_core_stats_apis
