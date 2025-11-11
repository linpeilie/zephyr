.. _mem_mgmt_api:

内存属性 (Memory Attributes)
#############################

可以在设备树中使用 ``zephyr,memory-attr`` 属性来标记具有属性的内存区域。然后可以在运行时通过利用提供的辅助库来检索此属性和相关的内存区域。(It is possible in the devicetree to mark the memory regions with attributes by using the ``zephyr,memory-attr`` property. This property and the related memory region can then be retrieved at run-time by leveraging a provided helper library.)

可以在该属性中指定的通用属性集在 :zephyr_file:`include/zephyr/dt-bindings/memory-attr/memory-attr.h` 中定义和解释。(The set of general attributes that can be specified in the property are defined and explained in :zephyr_file:`include/zephyr/dt-bindings/memory-attr/memory-attr.h`.)

例如,要在设备树中将内存区域标记为非易失性、可缓存、乱序:(For example, to mark a memory region in the devicetree as non-volatile, cacheable, out-of-order:)

.. code-block:: devicetree

   mem: memory@10000000 {
       compatible = "mmio-sram";
       reg = <0x10000000 0x1000>;
       zephyr,memory-attr = <( DT_MEM_NON_VOLATILE | DT_MEM_CACHEABLE | DT_MEM_OOO )>;
   };

.. note::

   ``zephyr,memory-attr`` 的使用不会导致实际创建任何内存区域。当需要从设备树定义的内存区域创建实际的段时,可以使用兼容 :dtcompatible:`zephyr,memory-region`,这将导致(仅当架构支持时)创建新的链接器段和区域。(The ``zephyr,memory-attr`` usage does not result in any memory region actually created. When it is needed to create an actual section out of the devicetree defined memory region, it is possible to use the compatible :dtcompatible:`zephyr,memory-region` that will result (only when supported by the architecture) in a new linker section and region.)

``zephyr,memory-attr`` 属性还可以用于设置可以在运行时解释的特定于架构和特定于软件的自定义属性。这被用于从设备树定义的内存区域创建 MPU 区域等,例如:(The ``zephyr,memory-attr`` property can also be used to set architecture-specific and software-specific custom attributes that can be interpreted at run time. This is leveraged, among other things, to create MPU regions out of devicetree defined memory regions, for example:)

``zephyr,memory-attr`` 属性还可以用于设置可以在运行时解释的特定于架构和特定于软件的自定义属性。这被用于从设备树定义的内存区域创建 MPU 区域等,例如:(The ``zephyr,memory-attr`` property can also be used to set architecture-specific and software-specific custom attributes that can be interpreted at run time. This is leveraged, among other things, to create MPU regions out of devicetree defined memory regions, for example:)

.. code-block:: devicetree

   mem: memory@10000000 {
       compatible = "mmio-sram";
       reg = <0x10000000 0x1000>;
       zephyr,memory-region = "NOCACHE_REGION";
       zephyr,memory-attr = <( DT_MEM_ARM(ATTR_MPU_RAM_NOCACHE) )>;
   };

有关 MPU 使用的更多详细信息,请参见 :zephyr_file:`include/zephyr/dt-bindings/memory-attr/memory-attr-arm.h` 和 :ref:`arm_cortex_m_developer_guide` 中的 :ref:`arm_cortex_m_mpu_considerations`。另请参阅 :ref:`cache_guide` 以了解 Zephyr 如何处理缓存的详细信息。(See :zephyr_file:`include/zephyr/dt-bindings/memory-attr/memory-attr-arm.h` and :ref:`arm_cortex_m_mpu_considerations` in the :ref:`arm_cortex_m_developer_guide` for more details about MPU usage. Also see :ref:`cache_guide` for details on how Zephyr handles caching.)

处理和管理标记有属性的内存区域的常规和推荐方法是通过启用 :kconfig:option:`CONFIG_MEM_ATTR` 来使用提供的 ``mem-attr`` 辅助库。当启用此选项时,内存区域及其属性的列表将编译到用户可访问的数组中,并提供一组函数,可用于查询、探测和操作区域和属性(有关更多详细信息,请参见下一节)。(The conventional and recommended way to deal and manage with memory regions marked with attributes is by using the provided ``mem-attr`` helper library by enabling :kconfig:option:`CONFIG_MEM_ATTR`. When this option is enabled the list of memory regions and their attributes are compiled in a user-accessible array and a set of functions is made available that can be used to query, probe and act on regions and attributes (see next section for more details).)

.. note::

   ``zephyr,memory-attr`` 属性只是关联内存区域的功能的描述性属性,但它不会导致为内存设置任何实际设置。希望使用此信息执行某些工作的用户、代码或子系统(例如从属性创建 MPU 区域)必须使用提供的 ``mem-attr`` 库或常规设备树辅助函数来执行所需的工作/设置。但请注意,对于某些架构(例如 ARM 和 ARM64),MPU 驱动程序在启动时使用此信息来正确初始化缓存。请参阅 :kconfig:option:`CONFIG_ARM_MPU`、:kconfig:option:`CONFIG_RISCV_PMP` 等。(The ``zephyr,memory-attr`` property is only a descriptive property of the capabilities of the associated memory region, but it does not result in any actual setting for the memory to be set. The user, code or subsystem willing to use this information to do some work (for example creating an MPU region out of the property) must use either the provided ``mem-attr`` library or the usual devicetree helpers to perform the required work / setting. Note, however, that for some architectures (such as ARM and ARM64) the MPU driver uses this information to properly initialize caching at boot. See :kconfig:option:`CONFIG_ARM_MPU`, :kconfig:option:`CONFIG_RISCV_PMP`, etc.)

``mem-attr`` 库及其用法的测试在 ``tests/subsys/mem_mgmt/mem_attr/`` 中提供。(A test for the ``mem-attr`` library and its usage is provided in ``tests/subsys/mem_mgmt/mem_attr/``.)

从 ``zephyr,memory-region-mpu`` 迁移指南 (Migration guide from ``zephyr,memory-region-mpu``)
***********************************************************************************************

当引入 ``zephyr,memory-attr`` 属性时,``zephyr,memory-region-mpu`` 属性被删除并弃用。(When the ``zephyr,memory-attr`` property was introduced, the ``zephyr,memory-region-mpu`` property was removed and deprecated.)

仍在使用已弃用属性的开发人员可以通过重命名属性并根据以下列表更改其值来迁移到新属性:(The developers that are still using the deprecated property can move to the new one by renaming the property and changing its value according to the following list:)

仍在使用已弃用属性的开发人员可以通过重命名属性并根据以下列表更改其值来迁移到新属性:(The developers that are still using the deprecated property can move to the new one by renaming the property and changing its value according to the following list:)

.. code-block:: none

   "RAM"         -> <( DT_ARM_MPU(ATTR_MPU_RAM) )>
   "RAM_NOCACHE" -> <( DT_ARM_MPU(ATTR_MPU_RAM_NOCACHE) )>
   "FLASH"       -> <( DT_ARM_MPU(ATTR_MPU_FLASH) )>
   "PPB"         -> <( DT_ARM_MPU(ATTR_MPU_PPB) )>
   "IO"          -> <( DT_ARM_MPU(ATTR_MPU_IO) )>
   "EXTMEM"      -> <( DT_ARM_MPU(ATTR_MPU_EXTMEM) )>

内存属性堆分配器 (Memory Attributes Heap Allocator)
****************************************************

可以利用内存属性属性 ``zephyr,memory-attr`` 来定义和创建一组内存堆,用户可以从中分配具有特定属性/功能的内存。(It is possible to leverage the memory attribute property ``zephyr,memory-attr`` to define and create a set of memory heaps from which the user can allocate memory from with certain attributes / capabilities.)

当设置 :kconfig:option:`CONFIG_MEM_ATTR_HEAP` 时,标记有 :zephyr_file:`include/zephyr/dt-bindings/memory-attr/memory-attr-sw.h` 中列出的内存属性之一的每个区域都会添加到用于动态分配具有特定属性的内存缓冲区的内存堆池中。(When the :kconfig:option:`CONFIG_MEM_ATTR_HEAP` is set, every region marked with one of the memory attributes listed in :zephyr_file:`include/zephyr/dt-bindings/memory-attr/memory-attr-sw.h` is added to a pool of memory heaps used for dynamic allocation of memory buffers with certain attributes.)

这里是可能属性的非详尽列表:(Here a non exhaustive list of possible attributes:)

.. code-block:: none

   DT_MEM_SW_ALLOC_CACHE
   DT_MEM_SW_ALLOC_NON_CACHE
   DT_MEM_SW_ALLOC_DMA

例如,我们可以定义具有不同属性的多个内存区域,并使用适当的属性来指示可以从这些区域动态分配内存:(For example we can define several memory regions with different attributes and use the appropriate attribute to indicate that it is possible to dynamically allocate memory from those regions:)

.. code-block:: devicetree

   mem_cacheable: memory@10000000 {
       compatible = "mmio-sram";
       reg = <0x10000000 0x1000>;
       zephyr,memory-attr = <( DT_MEM_CACHEABLE | DT_MEM_SW_ALLOC_CACHE )>;
   };

   mem_non_cacheable: memory@20000000 {
       compatible = "mmio-sram";
       reg = <0x20000000 0x1000>;
       zephyr,memory-attr = <( DT_MEM_NON_CACHEABLE | ATTR_SW_ALLOC_NON_CACHE )>;
   };

   mem_cacheable_big: memory@30000000 {
       compatible = "mmio-sram";
       reg = <0x30000000 0x10000>;
       zephyr,memory-attr = <( DT_MEM_CACHEABLE | DT_MEM_OOO | DT_MEM_SW_ALLOC_CACHE )>;
   };

   mem_cacheable_dma: memory@40000000 {
       compatible = "mmio-sram";
       reg = <0x40000000 0x10000>;
       zephyr,memory-attr = <( DT_MEM_CACHEABLE      | DT_MEM_DMA |
                               DT_MEM_SW_ALLOC_CACHE | DT_MEM_SW_ALLOC_DMA )>;
   };

然后用户可以使用提供的函数从这些区域动态分配内存,库将根据提供的属性和大小负责从正确的堆中分配内存:(The user can then dynamically carve memory out of those regions using the provided functions, the library will take care of allocating memory from the correct heap depending on the provided attribute and size:)

然后用户可以使用提供的函数从这些区域动态分配内存,库将根据提供的属性和大小负责从正确的堆中分配内存:(The user can then dynamically carve memory out of those regions using the provided functions, the library will take care of allocating memory from the correct heap depending on the provided attribute and size:)

.. code-block:: c

   // Init the pool
   mem_attr_heap_pool_init();

   // Allocate 0x100 bytes of cacheable memory from `mem_cacheable`
   block = mem_attr_heap_alloc(DT_MEM_SW_ALLOC_CACHE, 0x100);

   // Allocate 0x200 bytes of non-cacheable memory aligned to 32 bytes
   // from `mem_non_cacheable`
   block = mem_attr_heap_aligned_alloc(ATTR_SW_ALLOC_NON_CACHE, 0x100, 32);

   // Allocate 0x100 bytes of cacheable and dma-able memory from `mem_cacheable_dma`
   block = mem_attr_heap_alloc(DT_MEM_SW_ALLOC_CACHE | DT_MEM_SW_ALLOC_DMA, 0x100);

当多个区域标记有相同的属性时,内存的分配如下:(When several regions are marked with the same attributes, the memory is allocated:)

1. 从 ``zephyr,memory-attr`` 属性具有请求的属性(或多个属性)的区域。(From the regions where the ``zephyr,memory-attr`` property has the requested property (or properties).)

2. 在第 1 点的区域中,如果对于请求的大小还有任何未分配的空间,则从最小的区域分配。(Among the regions as at point 1, from the smallest region if there is any unallocated space left for the requested size)

3. 如果没有足够的空间,则从能够容纳请求大小的下一个更大的区域分配。(If there is not enough space, from the next bigger region able to accommodate the requested size)

以下示例展示了第 3 点:(The following example shows the point 3:)

.. code-block:: c

   // This memory is allocated from `mem_non_cacheable`
   block = mem_attr_heap_alloc(DT_MEM_SW_ALLOC_NON_CACHE, 0x100);

   // This memory is allocated from `mem_cacheable_big`
   block = mem_attr_heap_alloc(DT_MEM_SW_ALLOC_CACHE, 0x5000);

.. note::

    框架假定用于创建堆的内存区域可由代码使用,并在初始化时可用。用户必须在调用 :c:func:`mem_attr_heap_pool_init` 之前负责初始化和设置内存区域。(The framework is assuming that the memory regions used to create the heaps are usable by the code and available at init time. The user must take of initializing and setting the memory area before calling :c:func:`mem_attr_heap_pool_init`.)

    这意味着该区域必须在 MPU/MMU 方面正确配置(如果需要),并且可以从中创建实际的堆,例如通过利用 ``zephyr,memory-region`` 属性来创建适当的链接器段以容纳堆。(That means that the region must be correctly configured in terms of MPU / MMU (if needed) and that an actual heap can be created out of it, for example by leveraging the ``zephyr,memory-region`` property to create a proper linker section to accommodate the heap.)

API 参考 (API Reference)
*************************

.. doxygengroup:: memory_attr_interface
.. doxygengroup:: memory_attr_heap
