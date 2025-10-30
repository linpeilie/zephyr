.. _memory_management_shared_multi_heap:

共享多堆
########

共享多堆内存池管理器使用多堆分配器来管理一组具有不同能力/属性(可缓存、
不可缓存等...)的保留内存区域。

所有不同的区域都可以在运行时添加到共享多堆池中,提供一个不透明的"属性"值
(整数或枚举值),驱动程序或应用程序可以使用该值来请求具有某些能力的内存。

此框架通常按如下方式使用:

1. 在启动时,一些平台代码使用 :c:func:`shared_multi_heap_pool_init()`
   初始化共享多堆框架,并使用 :c:func:`shared_multi_heap_add()` 将内存区域
   添加到池中,可能从 DT 收集区域所需的信息。

2. 每个内存区域都编码在 :c:struct:`shared_multi_heap_region` 结构中。
   此结构还携带一个不透明的和用户定义的整数值,用于定义区域能力(例如:
   可缓存性、CPU 亲和性等...)

.. code-block:: c

   // 初始化共享多堆池
   shared_multi_heap_pool_init()

   // 用可缓存内存的数据填充结构
   struct shared_multi_heap_region cacheable_r0 = {
        .addr = addr_r0,
        .size = size_r0,
        .attr = SMH_REG_ATTR_CACHEABLE,
   };

   // 将区域添加到池中
   shared_multi_heap_add(&cacheable_r0, NULL);

   // 添加另一个可缓存区域
   struct shared_multi_heap_region cacheable_r1 = {
        .addr = addr_r1,
        .size = size_r1,
        .attr = SMH_REG_ATTR_CACHEABLE,
   };

   shared_multi_heap_add(&cacheable_r0, NULL);

   // 添加不可缓存区域
   struct shared_multi_heap_region non_cacheable_r2 = {
        .addr = addr_r2,
        .size = size_r2,
        .attr = SMH_REG_ATTR_NON_CACHEABLE,
   };

   shared_multi_heap_add(&non_cacheable_r2, NULL);

3. 当驱动程序或应用程序需要具有某种能力的动态内存时,它可以使用
   :c:func:`shared_multi_heap_alloc()`(或对齐版本)通过使用不透明参数
   选择所需内存的正确属性集来请求内存。框架将负责根据不透明参数和堆的运行时
   状态(可用内存、堆状态等...)选择正确的堆(从而选择内存区域)来分配内存。

.. code-block:: c

   // 从可缓存内存分配 4K
   shared_multi_heap_alloc(SMH_REG_ATTR_CACHEABLE, 0x1000);

   // 从不可缓存内存分配 4K
   shared_multi_heap_alloc(SMH_REG_ATTR_NON_CACHEABLE, 0x1000);

添加新属性
**********

API 不强制执行任何属性,但至少定义了两个最常见的属性:
:c:enumerator:`SMH_REG_ATTR_CACHEABLE` 和
:c:enumerator:`SMH_REG_ATTR_NON_CACHEABLE`。

.. doxygengroup:: shared_multi_heap
