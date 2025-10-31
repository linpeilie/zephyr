.. _memory_management_api_virtual_memory:

虚拟内存 (Virtual Memory)
##########################

Zephyr 中的虚拟内存 (VM) 为开发人员提供了微调内存访问的能力。
要使用虚拟内存，平台必须支持内存管理单元 (Memory Management Unit - MMU)，
并且必须在构建中启用它。由于 Zephyr 的目标主要是嵌入式系统，
Zephyr 中的虚拟内存支持与传统操作系统中的虚拟内存支持有所不同：

内核映像的映射 (Mapping of Kernel Image)
  如果未启用按需分页，则默认是在物理内存地址空间和虚拟内存地址空间之间
  对内核映像（包括代码和数据）进行 1:1 映射。偏离这一点需要仔细操作链接器脚本。

二级存储 (Secondary Storage)
  基本虚拟内存支持不使用二级存储来扩展可用内存。最大可用内存与物理内存相同。

  * :ref:`memory_management_api_demand_paging` 允许使用二级存储
    作为虚拟内存的后备存储，从而允许比可用物理内存更大的可用内存。
    请注意，按需分页需要显式启用。

  * 尽管虚拟内存空间可以大于物理内存空间，但在不启用按需分页的情况下，
    所有虚拟映射的内存都必须由物理内存支持。


Kconfigs
********

必需 (Required)
================

这些是内核支持虚拟内存需要启用或定义的 Kconfig。

* :kconfig:option:`CONFIG_MMU`：必须启用以支持内核中的虚拟内存。

* :kconfig:option:`CONFIG_MMU_PAGE_SIZE`：内存页的大小。默认为 4KB。

* :kconfig:option:`CONFIG_KERNEL_VM_BASE`：虚拟地址空间的基地址。

* :kconfig:option:`CONFIG_KERNEL_VM_SIZE`：虚拟地址空间的大小。默认为 8MB。

* :kconfig:option:`CONFIG_KERNEL_VM_OFFSET`：内核映像从
  :kconfig:option:`CONFIG_KERNEL_VM_BASE` 的此偏移处开始。

可选 (Optional)
===============

* :kconfig:option:`CONFIG_KERNEL_DIRECT_MAP`：允许虚拟地址和物理地址之间进行 1:1 映射，
  而不是内核在虚拟地址空间内选择地址。这对于映射设备 MMIO 区域以实现更精确的访问控制很有用。


内存映射概述 (Memory Map Overview)
***********************************

这是虚拟内存地址空间的内存映射概述。请注意，``Z_*`` 宏在代码中使用，
根据架构和 Kconfig 可能具有不同的含义，将在下面解释。

.. code-block:: none
   :emphasize-lines: 1, 3, 9, 22, 24

   +--------------+ <- K_MEM_VIRT_RAM_START
   | Undefined VM | <- 架构特定的保留区域
   +--------------+ <- K_MEM_KERNEL_VIRT_START
   | Mapping for  |
   | main kernel  |
   | image        |
   |              |
   |              |
   +--------------+ <- K_MEM_VM_FREE_START
   |              |
   | Unused,      |
   | Available VM |
   |              |
   |..............| <- 随着更多映射的创建向下增长
   | Mapping      |
   +--------------+
   | Mapping      |
   +--------------+
   | ...          |
   +--------------+
   | Mapping      |
   +--------------+ <- 内存映射从这里开始
   | Reserved     | <- 大小为 K_MEM_VM_RESERVED 的特殊目的虚拟页
   +--------------+ <- K_MEM_VIRT_RAM_END

* ``K_MEM_VIRT_RAM_START`` 是虚拟内存地址空间的开始。这需要页对齐。
  目前，它与 :kconfig:option:`CONFIG_KERNEL_VM_BASE` 相同。

* ``K_MEM_VIRT_RAM_SIZE`` 是虚拟内存地址空间的大小。这需要页对齐。
  目前，它与 :kconfig:option:`CONFIG_KERNEL_VM_SIZE` 相同。

* ``K_MEM_VIRT_RAM_END`` 简单地是 (``K_MEM_VIRT_RAM_START`` + ``K_MEM_VIRT_RAM_SIZE``)。

* ``K_MEM_KERNEL_VIRT_START`` 与链接器脚本中指定的 ``z_mapped_start`` 相同。
  这是启动时内核映像开始的虚拟地址。

* ``K_MEM_KERNEL_VIRT_END`` 与链接器脚本中指定的 ``z_mapped_end`` 相同。
  这是启动时内核映像结束的虚拟地址。

* ``K_MEM_VM_FREE_START`` 是虚拟地址空间的开始，可以在此为内存映射分配地址。
  这取决于是否启用 :kconfig:option:`CONFIG_ARCH_MAPS_ALL_RAM`。

  * 如果启用，这意味着所有物理内存都映射在虚拟内存地址空间中，
    它与 (:kconfig:option:`CONFIG_SRAM_BASE_ADDRESS` + :kconfig:option:`CONFIG_SRAM_SIZE`) 相同。

  * 如果禁用，``K_MEM_VM_FREE_START`` 与 ``K_MEM_KERNEL_VIRT_END`` 相同，
    即内核映像的结束。

* ``K_MEM_VM_RESERVED`` 是为支持内核功能而保留的区域。例如，
  保留了一些地址来支持按需分页。


虚拟内存映射 (Virtual Memory Mappings)
***************************************

启动时设置映射 (Setting up Mappings at Boot)
=============================================

一般来说，大多数支持的架构在启动时设置内存映射如下：

* ``.text`` 节是只读和可执行的。它在内核和用户模式下都可访问。

* ``.rodata`` 节是只读和不可执行的。它在内核和用户模式下都可访问。

* 其他内核节，如 ``.data``、``.bss`` 和 ``.noinit``，是读写和不可执行的。
  它们仅在内核模式下可访问。

  * 用户模式线程的堆栈在线程创建期间会自动授予对其相应用户模式线程的读写访问权限。

  * 默认情况下，全局变量对用户模式线程不可访问。
    请参阅 :ref:`Memory Domains and Partitions<memory_domain>`，
    了解如何在用户模式线程中使用全局变量，以及如何在用户模式线程之间共享数据。

这些映射的缓存模式是特定于架构的。它们可以是无缓存 (none)、回写 (write-back) 或直写 (write-through)。

请注意，SoC 有其自己的启动所需的其他映射，这些映射在其自己的 SoC 配置下定义。
这些映射通常包括设置硬件所需的设备 MMIO 区域。


映射匿名内存 (Mapping Anonymous Memory)
========================================

未使用的物理内存可以按需映射到虚拟地址空间。这在概念上类似于从堆分配内存，
但这些映射必须在页面大小上对齐并且具有更精细的访问控制。

* :c:func:`k_mem_map` 可用于映射未使用的物理内存：

  * 请求的大小必须是页面大小的倍数。

  * 返回的地址位于 ``K_MEM_VM_FREE_START`` 和 ``K_MEM_VIRT_RAM_END``
    之间的虚拟地址空间内。

  * 映射的区域不保证在内存中物理上连续。

  * 映射的虚拟区域之前和之后的保护页会自动分配，以捕获由于缓冲区下溢或溢出而导致的访问问题。

* 映射的区域可以通过 :c:func:`k_mem_unmap` 取消映射（即释放）：

  * 必须谨慎地将相同的区域大小传递给 :c:func:`k_mem_map` 和 :c:func:`k_mem_unmap`。
    取消映射函数在取消映射之前不会检查它是否是有效的映射区域。


API 参考 (API Reference)
*************************

.. doxygengroup:: kernel_memory_management
