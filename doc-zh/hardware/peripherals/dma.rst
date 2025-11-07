.. _dma_api:

直接内存访问 (Direct Memory Access, DMA)
##########################################

概述 (Overview)
****************

直接内存访问(控制器)是一种常见的协处理器类型,通常可以卸载与外设和内存之间的数据传输。

DMA API 不是可移植的 API,实际上也无法做到,因为每个 DMA 都有独特的内存要求、外设交互和功能。该 API 实际上提供了树中驱动程序所需的所有有用 DMA 功能的联合。对于 DMA IP 可能非常相似但略有差异的供应商的外设设备,只要小心使用,它仍然可以是一个很好的抽象。

DMA 驱动程序通常不处理缓存一致性;这由开发人员决定,因为需求因应用程序而异。有关 Zephyr 中缓存管理的概述,请参见 :ref:`cache_guide`。

驱动程序实现预期 (Driver Implementation Expectations)
********************************************************

同步和所有权 (Synchronization and Ownership)
+++++++++++++++++++++++++++++++++++++++++++++++

从 API 角度来看,DMA 通道是单一所有者对象,这意味着驱动程序不应尝试使用互斥锁或信号量等内核同步原语包装通道。如果 DMA 通道需要修改共享寄存器,这些寄存器更新应该包装在自旋锁中。

这使得整个 API 成本低廉,可以从任何调用上下文调用,包括 ISR,在 ISR 中启动/停止/挂起/恢复/重新加载通道传输可能非常有用。

传输描述符内存管理 (Transfer Descriptor Memory Management)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

驱动程序不应尝试使用任何类型的堆分配。如果传输描述符需要对象池,则应以不破坏 ISR 可调用调用承诺的方式设置它们。许多驱动程序选择为每个通道创建一个简单的静态描述符数组,描述符数组的大小可使用 Kconfig 调整。

通道状态机预期 (Channel State Machine Expectations)
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

DMA 通道应被视为状态机,DMA API 以 API 调用的形式为其提供转换事件。每个驱动程序都应该维护自己的通道状态跟踪。通道的忙碌状态应该可以随时通过 :c:func:`dma_get_status()` 检查。

这里提供了一个显示预期可能状态转换及其 API 调用的图表,供参考。

.. graphviz::
   :caption: DMA 状态有限状态机

   digraph {
       node [style=rounded];
       edge [fontname=Courier];
       init [shape=point];

       CONFIGURED [label=Configured,shape=box];
       RUNNING [label=Running,shape=box];
       SUSPENDED [label=Suspended,shape=box];

       init -> CONFIGURED [label=dma_config];

       CONFIGURED -> RUNNING [label=dma_start];
       CONFIGURED -> CONFIGURED [label=dma_stop, headport=c, tailport=e];
       CONFIGURED -> CONFIGURED [label=dma_config, headport=c, tailport=w];

       RUNNING -> CONFIGURED [label=dma_stop];
       RUNNING -> RUNNING [label=dma_start];
       RUNNING -> RUNNING [label=dma_resume, headport=w];
       RUNNING -> SUSPENDED [label=dma_suspend];

       SUSPENDED -> SUSPENDED [label=dma_suspend];
       SUSPENDED -> RUNNING [label=dma_resume];
       SUSPENDED -> CONFIGURED [label=dma_stop];
   }

API 参考 (API Reference)
*************************

.. doxygengroup:: dma_interface
