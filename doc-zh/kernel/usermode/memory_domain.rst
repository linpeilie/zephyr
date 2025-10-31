.. _memory_domain:

内存保护设计
############

Zephyr 的内存保护设计主要面向带有 MPU（内存保护单元）的微控制器。我们也支持部分具有分页 MMU（内存管理单元）的架构（如 x86），但在这种情况下，MMU 以“恒等页表”的方式被当作 MPU 使用。

下文统一采用 MPU 术语进行描述；具备 MMU 的系统可等效理解为“拥有无限可编程区域数量的 MPU”。

启用 Zephyr 的内存保护功能后，内存访问的配置可分多层进行，主要包括：

引导期内存配置
**************

这是内核启动后对 MPU 的初始配置，应包含：

- 对部分内存区域进行特殊缓存/回写策略的配置，以满足基础硬件与驱动的需求。注意，大多数 MPU 提供默认内存访问策略映射的概念，可作为“背景”映射启用，用于那些没有被显式 MPU 区域覆盖的内存。强烈建议启用背景映射，以最大化留给最终应用使用的 MPU 区域数量。在 ARMv7-M/ARMv8-M 上，这称为 System Address Map；其他 CPU 也可能有类似能力。参见 :ref:`mem_mgmt_api` 了解如何在设备树中标注系统映射。

- 为程序文本与 ro-data 配置用户态可访问的只读（文本还需可执行）区域。也可进一步将 ro-data 与文本分别放入不同的只读/只读可执行区域，但这会多消耗一个 MPU 区域。用户态线程需要能够读取 ro-data 并取指执行。

- 视配置而定，提供用户可访问的读写区域以支持 GCOV、HEP 等额外特性。

若已启用允许特权态访问任意内存的背景映射，并定义了授予用户态访问文本/ro-data 的区域，则上述内容即可满足引导期配置的基本需求。

硬件栈溢出
**********

:kconfig:option:`CONFIG_HW_STACK_PROTECTION` 是一个可选特性，用于在系统处于特权态运行时检测栈缓冲溢出。该特性检测的是整个栈缓冲的溢出，而非单个栈帧；后者可使用编译器辅助的 :kconfig:option:`CONFIG_STACK_CANARIES`。

与其他特权态崩溃类似，特权态栈溢出后无法保证系统整体健康性，因此应视为严重错误。不过，及时获知发生了溢出仍然非常有价值；若缺乏稳健的检测逻辑，栈溢出会导致系统以难以捉摸的方式崩溃或进入未定义行为。

某些系统通过在运行期创建一个只读的“守护”MPU 区域来实现该特性，该区域位于特权态栈缓冲的开始处或紧邻其前方；当栈溢出时会触发异常。

该特性对检测用户态栈溢出并非必需；禁用它可视 MPU 设计释放 1-2 个 MPU 区域。

也有系统由 CPU 提供专用的栈溢出检测支持，无需额外 MPU 区域。

线程栈
******

任何在用户态运行的线程都需要访问其自身的栈缓冲。在切换到用户态线程的上下文时，会为该线程配置一个专用的 MPU 区域或 MMU 页表项，边界即为其栈缓冲范围。若线程越界使用栈缓冲，会向其无权访问的内存写入数据，从而触发内存访问违规异常。

注意：同一内存域中的用户线程可以访问彼此的栈。这是架构支持内存域的最低要求。架构可以进一步限制对栈的访问，使每个用户线程仅能访问自己的栈；若某架构支持该能力，可通过 :kconfig:option:`CONFIG_ARCH_MEM_DOMAIN_SUPPORTS_ISOLATED_STACKS` 进行声明。若支持，该行为默认启用；若架构同时支持两种模式，可通过 :kconfig:option:`CONFIG_MEM_DOMAIN_ISOLATED_STACKS` 选择性禁用。然而，部分架构可能始终强制启用该行为，此时该选项无法禁用。无论这些 Kconfig 如何设定，用户线程都不能访问其内存域之外的其他用户线程的栈。

线程资源池
**********

少量以系统调用形式暴露的内核 API 需要进行堆内存分配。这些内存仅供内核使用，用户态无法直接访问。要使用这类系统调用，调用线程必须先为自身指定资源池（:c:struct:`k_heap` 对象）。内存通过 :c:func:`z_thread_malloc` 从线程的资源池中分配，并通过 :c:func:`k_free` 释放。

使用资源池的 API 如下；对于不希望在应用中使用堆分配的场景，也给出了可选方案：

 - :c:func:`k_stack_alloc_init` 用来自资源池的存储缓冲初始化 k_stack，而不是使用用户提供的缓冲。可替代方案：使用 :c:macro:`K_STACK_DEFINE()` 在引导期自动初始化，或在特权态下调用 :c:func:`k_stack_init` 初始化。

 - :c:func:`k_msgq_alloc_init` 用来自资源池的存储缓冲初始化 k_msgq。可替代方案：使用 :c:macro:`K_MSGQ_DEFINE()` 在引导期自动初始化，或在特权态下调用 :c:func:`k_msgq_init` 初始化。

 - :c:func:`k_poll` 在用户态调用时，需要在内核侧为事件数组创建一个副本用于等待事件；无论因何返回，该副本都会被释放。

 - :c:func:`k_queue_alloc_prepend` 与 :c:func:`k_queue_alloc_append` 会为入队数据分配一个容器结构，因为用于描述队列的内部簿记信息不能放在用户提供的内存中。

 - :c:func:`k_object_alloc` 允许在运行期动态分配整个内核对象，并返回可用指针给调用者。

相关 API 为 :c:func:`k_thread_heap_assign`，用于为目标线程指定用于上述分配的 k_heap。

若启用了系统堆，可通过 :c:func:`k_thread_system_pool_assign` 使用系统堆。但更推荐为系统上不同的逻辑应用分别定义自身的资源池。

内存域（Memory Domains）
***********************

内核确保任一用户线程可访问其自身的栈缓冲，以及程序文本与只读数据。若需为用户线程授予更多内存访问权限，应使用内存域 API。

概念上，内存域是若干个内存分区（partition）的集合。一个域内最多可包含的分区数量受限于可用的 MPU 区域数量，因此应尽量减少引导期消耗的 MPU 区域。

内存域并非用于控制特权态的内存访问。在部分架构上这可能难以避免：例如某些架构不允许定义“用户态只读而特权态可读写”的区域。使用此类区域时需格外谨慎，避免在访问时无意导致内核崩溃。试图通过内存域 API 控制特权态访问，至多属于未定义行为；特权态访问策略仅应由引导期内存区域配置来控制。

内存域 API 只对特权态可用。用户态对内存域唯一的影响是：任一用户线程的子线程将自动加入其父线程所属的内存域。

所有线程都是某个内存域的成员，包括特权线程（尽管对其内存访问没有影响）。存在一个默认域 ``k_mem_domain_default``：若线程没有被显式指定到某个域，或未从父线程继承域成员关系，则将加入默认域。主线程从默认域成员开始运行。

内存分区（Memory Partitions）
============================

每个内存分区由起始地址、大小与访问属性组成。内存分区用于控制对系统内存的访问。定义分区需要满足以下约束：

- 分区必须表示一个可由底层内存管理硬件编程的内存区域，并符合其约束。例如，许多 MPU 系统要求分区的大小为 2 的幂，并按其自身大小对齐。对 MMU 系统，分区必须按页对齐，大小为页大小的整数倍。

- 同一内存域内的分区不能互相重叠。内存域内的分区不存在“优先级”的概念。内存域内的分区通常被认为优先于任何引导期内存区域；但分区是否可以与引导期内存区域重叠取决于具体架构。

- 同一个分区可以出现在多个内存域中。例如多个内存域可能都授予访问同一段共享内存。

- 谨慎选择在分区中暴露的内存区域。不应向用户态直接开放包含内核私有数据的任何内存。

- 内存域分区旨在控制对系统 RAM 的访问。对非 RAM 的区域进行内存分区配置可能不受架构支持；对 MMU 系统尤其如此。

分区可通过两种方式定义：手动或自动。

手动内存分区
------------

如下代码声明了一个全局数组 ``buf``，并为其声明了一个可读写的分区，可加入到内存域：

.. code-block:: c

    uint8_t __aligned(32) buf[32];

    K_MEM_PARTITION_DEFINE(my_partition, buf, sizeof(buf),
                           K_MEM_PARTITION_P_RW_U_RW);

当我们希望将分散在多个 C 文件中的多个对象纳入同一分区时，此方式可扩展性较差。

自动内存分区
------------

自动内存分区由构建系统创建。所有需要置入分区的全局变量会被标注目标分区；构建系统随后把它们聚合为单个连续内存块，在引导时为 BSS 变量清零，并据此定义一个具有合适基地址与大小、容纳所有被标注数据的内存分区。

.. figure:: auto_mem_domain.png
   :alt: 自动内存域构建流程
   :align: center

   自动内存域构建流程

自动内存分区仅配置为读写区域。使用 :c:macro:`K_APPMEM_PARTITION_DEFINE()` 定义。已初始化的数据使用 :c:macro:`K_APP_DMEM()` 路由到该分区，BSS 数据使用 :c:macro:`K_APP_BMEM()`。

.. code-block:: c

    #include <zephyr/app_memory/app_memdomain.h>

    /* 声明一个对用户态读写的 k_mem_partition“my_partition”。
     * 注意这里不指定基地址与大小。
     */
    K_APPMEM_PARTITION_DEFINE(my_partition);

    /* 全局变量 var1 将位于 my_partition 内，且在引导时被初始化为 37。*/
    K_APP_DMEM(my_partition) int var1 = 37;

    /* 全局变量 var2 将位于 my_partition 内，且在引导时被清零，
     * 因为使用了 K_APP_BMEM()，表明其为 BSS 变量。
     */
    K_APP_BMEM(my_partition) int var2;

构建系统会确保 ``my_partition`` 的基地址满足对齐要求，总大小满足内存管理硬件约束，必要时添加填充（padding）。

若需要创建多个分区，可使用 ``app_macro_support.h`` 中提供的变参预处理宏：

.. code-block:: c

    FOR_EACH(K_APPMEM_PARTITION_DEFINE, part0, part1, part2);

静态库全局的自动分区
~~~~~~~~~~~~~~~~~~~~~~

设置自动内存分区的构建逻辑位于 ``scripts/build/gen_app_partitions.py``。若将某个静态库链接进 Zephyr，可通过 ``--library`` 参数把该库中的所有全局变量路由到特定分区。

例如启用了 Newlib C 库时，Newlib 的全局变量需放入 ``z_libc_partition``。在顶层 ``CMakeLists.txt`` 中对脚本的调用会加入如下参数：

.. code-block:: none

    gen_app_partitions.py ... --library libc.a z_libc_partition ..

对于预编译库，无法在项目级配置或构建文件中表达该需求；必须修改顶层 ``CMakeLists.txt``。

对于使用 ``zephyr_library`` 或 ``zephyr_library_named`` 创建的 Zephyr 库，可用 ``zephyr_library_app_memory`` 指定该库中所有全局变量应放入的内存分区。

.. _memory_domain_predefined_partitions:

预定义内存分区
--------------

系统预定义了若干分区：

 - ``z_malloc_partition`` - libc malloc() 使用的系统级内存池所在分区。考虑到潜在的“饿死”问题，不推荐从全局池获取堆内存；更好的做法是定义多个 sys_heap 对象并将它们分配给特定内存域。

 - ``z_libc_partition`` - 包含 C 库与运行时需要的全局变量。使用 Minimal C 库或 Newlib C 库时需要该分区；启用 :kconfig:option:`CONFIG_STACK_CANARIES` 时也需要。

各库专属的分区在 ``include/app_memory/partitions.h`` 中列出。例如要在用户态使用 MBEDTLS 库，需要将 ``k_mbedtls_partition`` 加入相应内存域。

内存域使用方法
==============

创建内存域
----------

使用 :c:struct:`k_mem_domain` 定义内存域变量，随后调用 :c:func:`k_mem_domain_init` 初始化。

如下示例定义并初始化一个空的内存域：

.. code-block:: c

    struct k_mem_domain app0_domain;

    k_mem_domain_init(&app0_domain, 0, NULL);

向内存域添加分区
----------------

向内存域添加分区有两种方式。

第一种是在创建内存域时一次性添加分区：

.. code-block:: c

    /* MPU 区域的起始地址需要按其大小对齐 */
    uint8_t __aligned(32) app0_buf[32];
    uint8_t __aligned(32) app1_buf[32];

    K_MEM_PARTITION_DEFINE(app0_part0, app0_buf, sizeof(app0_buf),
                           K_MEM_PARTITION_P_RW_U_RW);

    K_MEM_PARTITION_DEFINE(app0_part1, app1_buf, sizeof(app1_buf),
                           K_MEM_PARTITION_P_RW_U_RO);

    struct k_mem_partition *app0_parts[] = {
        app0_part0,
        app0_part1
    };

    k_mem_domain_init(&app0_domain, ARRAY_SIZE(app0_parts), app0_parts);

第二种是在内存域初始化后逐个添加分区：

.. code-block:: c

    /* MPU 区域的起始地址需要按其大小对齐 */
    uint8_t __aligned(32) app0_buf[32];
    uint8_t __aligned(32) app1_buf[32];

    K_MEM_PARTITION_DEFINE(app0_part0, app0_buf, sizeof(app0_buf),
                           K_MEM_PARTITION_P_RW_U_RW);

    K_MEM_PARTITION_DEFINE(app0_part1, app1_buf, sizeof(app1_buf),
                           K_MEM_PARTITION_P_RW_U_RO);

    k_mem_domain_add_partition(&app0_domain, &app0_part0);
    k_mem_domain_add_partition(&app0_domain, &app0_part1);

.. note::
    可配置的最大内存分区数量受可用 MPU 区域上限或可用 MMU 表项上限约束。

内存域成员分配
--------------

任意线程都可以加入某个内存域；一个内存域也可以包含多个线程。通过如下 API 将线程分配到内存域：

.. code-block:: c

    k_mem_domain_add_thread(&app0_domain, app_thread_id);

若该线程已经属于其他内存域（包括默认域），则会从原域移除并加入新域。

此外，若某线程属于某内存域，则其创建的子线程也会属于该内存域。

从内存域移除分区
----------------

如下示例演示如何从内存域中移除一个分区：

.. code-block:: c

    k_mem_domain_remove_partition(&app0_domain, &app0_part1);

``k_mem_domain_remove_partition()`` 会找到与所给参数匹配的分区，并将其从内存域中移除。

可用的分区属性
--------------

定义分区时，需要为其设置访问权限属性。由于分区访问控制依赖 MPU 或 MMU，可用的属性与架构相关。

针对具体架构的分区属性完整列表可在对应架构头文件中找到：
``include/zephyr/arch/<arch name>/arch.h``（例如 ``include/zephyr/arch/arm/arch.h``）。部分示例如下：

.. code-block:: c

    /* 表示特权读写、非特权读写 */
    K_MEM_PARTITION_P_RW_U_RW
    /* 表示特权读写、非特权只读 */
    K_MEM_PARTITION_P_RW_U_RO

在几乎所有场合，``K_MEM_PARTITION_P_RW_U_RW`` 都是合适的选择。

配置选项
********

相关配置项：

* :kconfig:option:`CONFIG_MAX_DOMAIN_PARTITIONS`

API 参考
********

以下内存域 API 由 :zephyr_file:`include/zephyr/kernel.h` 提供：

.. doxygengroup:: mem_domain_apis
