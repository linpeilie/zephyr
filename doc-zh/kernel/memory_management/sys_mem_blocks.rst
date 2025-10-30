.. _sys_mem_blocks:

内存块分配器
############

内存块分配器允许从指定的内存区域动态分配内存块,其中:

* 所有内存块都具有单一固定大小。

* 可以同时分配或释放多个块。

* 一起分配的一组块可能不是连续的。这对于诸如分散-聚集 DMA 传输之类的操作很有用。

* 分配块的簿记在关联缓冲区之外完成(与内存板不同)。这允许缓冲区驻留在可以
  断电以节省能源的内存区域中。

.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的内存块分配器(仅受可用 RAM 限制)。每个分配器由其内存地址引用。

内存块分配器具有以下关键属性:

* 每个块的**块大小**,以字节为单位。它必须至少为 4N 字节长,其中 N 大于 0。

* 可用于分配的**块数**。它必须大于零。

* 为内存板的块提供内存的**缓冲区**。它必须至少为"块大小"乘以"块数"字节长。

* 一个**块位图**,用于跟踪哪个块已被分配。

缓冲区必须对齐到 N 字节边界,其中 N 是大于 2 的 2 的幂(即 4、8、16...)。
为了确保缓冲区中的所有内存块都类似地对齐到此边界,块大小也必须是 N 的倍数。

由于使用内部簿记结构及其创建,每个内存块分配器必须在编译时声明和定义。

内部操作
========

与分配器关联的每个缓冲区都是固定大小块的数组,块之间没有浪费的空间。

内存块分配器使用位图跟踪未分配的块。

内存块分配器
************

在内部,内存块分配器使用位图来跟踪哪些块已被分配。每个分配器利用
``sys_bitarray`` 接口,从后备缓冲区一个接一个地获取内存块,直到达到请求的
块数。关于分配器的所有元数据都存储在后备缓冲区之外。这允许后备缓冲区的内存
区域断电以节省能源,因为分配器代码从不触及缓冲区的内容。

多内存块分配器组
****************

多内存块分配器组实用程序函数提供了一种方便的方法来管理一组分配器。使用自定义
分配器选择函数在此组中选择要使用的分配器。

分配器组应该在运行时通过 :c:func:`sys_multi_mem_blocks_init` 初始化。
然后可以通过 :c:func:`sys_multi_mem_blocks_add_allocator` 添加每个分配器。

要从组中分配内存块,调用 :c:func:`sys_multi_mem_blocks_alloc` 并使用不透明的
"配置"参数。此参数直接传递给分配器选择函数,以便可以选择适当的分配器。选择
分配器后,通过 :c:func:`sys_mem_blocks_alloc` 分配内存块。

可以通过 :c:func:`sys_multi_mem_blocks_free` 释放已分配的内存块。调用者不需要
传递配置参数。分配器代码匹配传入的内存地址以找到正确的分配器,然后通过
:c:func:`sys_mem_blocks_free` 释放内存块。

用法
****

定义内存块分配器
================

使用类型 :c:type:`sys_mem_blocks_t` 的变量定义内存块分配器。它需要在编译时
通过调用 :c:macro:`SYS_MEM_BLOCKS_DEFINE` 定义和初始化。

以下代码定义并初始化一个内存块分配器,该分配器有 4 个块,每个块长 64 字节,
每个块都对齐到 4 字节边界:

.. code-block:: c

   SYS_MEM_BLOCKS_DEFINE(allocator, 64, 4, 4);

同样,您可以在私有作用域中定义内存块分配器:

.. code-block:: c

   SYS_MEM_BLOCKS_DEFINE_STATIC(static_allocator, 64, 4, 4);

也可以向分配器提供预定义的缓冲区,其中缓冲区可以单独放置。请注意,需要在其
定义处完成缓冲区的对齐。

.. code-block:: c

   uint8_t __aligned(4) backing_buffer[64 * 4];
   SYS_MEM_BLOCKS_DEFINE_WITH_EXT_BUF(allocator, 64, 4, backing_buffer);

分配内存块
==========

可以通过调用 :c:func:`sys_mem_blocks_alloc` 分配内存块。

.. code-block:: c

   int ret;
   uintptr_t blocks[2];

   ret = sys_mem_blocks_alloc(allocator, 2, blocks);

如果 ``ret == 0``,数组 ``blocks`` 将包含指向已分配块的内存地址数组。

释放内存块
==========

通过调用 :c:func:`sys_mem_blocks_free` 释放内存块。

以下代码基于上面的示例,分配 2 个内存块,然后在不再需要时释放它们。

.. code-block:: c

   int ret;
   uintptr_t blocks[2];

   ret = sys_mem_blocks_alloc(allocator, 2, blocks);
   ... /* 对分配的内存块执行一些操作 */
   ret = sys_mem_blocks_free(allocator, 2, blocks);

使用多内存块分配器组
====================

以下代码演示如何初始化分配器组:

.. code-block:: c

   sys_mem_blocks_t *choice_fn(struct sys_multi_mem_blocks *group, void *cfg)
   {
       ...
   }

   SYS_MEM_BLOCKS_DEFINE(allocator0, 64, 4, 4);
   SYS_MEM_BLOCKS_DEFINE(allocator1, 64, 4, 4);

   static sys_multi_mem_blocks_t alloc_group;

   sys_multi_mem_blocks_init(&alloc_group, choice_fn);
   sys_multi_mem_blocks_add_allocator(&alloc_group, &allocator0);
   sys_multi_mem_blocks_add_allocator(&alloc_group, &allocator1);

要从组中分配和释放内存块:

.. code-block:: c

   int ret;
   uintptr_t blocks[1];
   size_t blk_size;

   ret = sys_multi_mem_blocks_alloc(&alloc_group, UINT_TO_POINTER(0),
                                    1, blocks, &blk_size);

   ret = sys_multi_mem_blocks_free(&alloc_group, 1, blocks);

API 参考
********

.. doxygengroup:: mem_blocks_apis
