.. _memory_management_api_demand_paging:.. _memory_management_api_demand_paging:.. _memory_management_api_demand_paging:



按需分页 (Demand Paging)

#########################

请求分页Demand Paging

按需分页 (Demand paging) 提供了一种机制，其中数据仅在当前执行上下文需要时才被带入物理内存。

物理内存在概念上被划分为页面大小的页帧 (page frames)，作为保存数据的区域。#####################



* 当处理器尝试访问数据并且数据页存在于其中一个页帧中时，执行继续而不会有任何中断。



* 当处理器尝试访问不存在于任何页帧中的数据页时，会发生页面错误 (page fault)。请求分页提供了一种机制,仅在当前执行上下文需要时才将数据带入物理内存。物理内存Demand paging provides a mechanism where data is only brought into physical

  然后，分页代码会将相应的数据页从后备存储 (backing store) 带入物理内存（如果有空闲页帧）。

  如果没有更多空闲页帧，则会调用驱逐算法 (eviction algorithm) 来选择要换出的数据页，在概念上被划分为页面大小的页框,作为保存数据的区域。memory as required by current execution context. The physical memory is

  从而释放页帧以供新数据换入。如果此数据页在首次换入后已被修改，则数据将被写回后备存储。

  如果未进行修改或在写回后备存储之后，数据页现在被认为已换出，相应的页帧现在是空闲的。conceptually divided in page-sized page frames as regions to hold data.

  然后，分页代码调用后备存储来换入与请求数据位置相对应的数据页。后备存储将该数据页复制到空闲页帧中。

  现在数据页在物理内存中，执行可以继续。* 当处理器尝试访问数据并且数据页存在于某个页框中时,执行将继续而不会有任何



有一些函数可以使用 :c:func:`k_mem_page_in()` 和 :c:func:`k_mem_page_out()` 手动调用换入和换出。  中断。* When the processor tries to access data and the data page exists in

:c:func:`k_mem_page_in()` 可用于预先换入数据页，因为预计它们将在不久的将来需要。

这用于最小化页面错误的数量，因为这些数据页已经在物理内存中，从而最小化延迟。  one of the page frames, the execution continues without any interruptions.

:c:func:`k_mem_page_out()` 可用于换出在相当长的时间内不会被访问的数据页。

这会释放页帧，以便下一次换入可以更快地执行，因为分页代码不需要调用驱逐算法。* 当处理器尝试访问不存在于任何页框中的数据页时,会发生页面错误。如果有空闲



术语 (Terminology)  页框,分页代码将相应的数据页从后备存储带入物理内存。如果没有更多空闲页框,* When the processor tries to access the data page that does not exist

*******************

  则调用驱逐算法选择要换出的数据页,从而为要换入的新数据释放页框。如果此数据  in any page frames, a page fault occurs. The paging code then brings in

数据页 (Data Page)

==================  页在首次换入后被修改,则数据将被写回后备存储。如果没有进行修改或写回后备  the corresponding data page from backing store into physical memory if

  数据页是页面大小的数据区域。它可能存在于页帧中，或被换出到某个后备存储。

  它的位置始终可以通过虚拟地址在 CPU 的页表（或等效物）中查找。  存储后,数据页现在被视为已换出,相应的页框现在空闲。然后分页代码调用后备  there is a free page frame. If there is no more free page frames,

  数据类型始终是 ``void *``，或在进行指针运算时是 ``uint8_t *``。

  存储来换入与请求数据位置对应的数据页。后备存储将该数据页复制到空闲页框中。  the eviction algorithm is invoked to select a data page to be paged out,

页帧 (Page Frame)

=================  现在数据页在物理内存中,执行可以继续。  thus freeing up a page frame for new data to be paged in. If this data

  页帧是 RAM 中页面大小的物理内存区域。它是可以放置数据页的容器。

  它始终通过物理地址引用。Zephyr 有一个使用 ``uintptr_t`` 表示物理地址的约定。  page has been modified after it is first paged in, the data will be

  对于每个页帧，会实例化一个 ``struct k_mem_page_frame`` 来存储元数据。

  每个页帧的标志：有一些函数可以使用 :c:func:`k_mem_page_in()` 和 :c:func:`k_mem_page_out()`   written back into the backing store. If no modifications is done or



  * ``K_MEM_PAGE_FRAME_FREE`` 表示页帧未使用且在空闲页帧列表上。手动调用换入和换出。:c:func:`k_mem_page_in()` 可用于换入预期在不久的将来  after written back into backing store, the data page is now considered

    当设置此标志时，其他标志都没有意义，不得修改它们。

需要的数据页。这用于最小化页面错误的数量,因为这些数据页已经在物理内存中,  paged out and the corresponding page frame is now free. The paging code

  * ``K_MEM_PAGE_FRAME_PINNED`` 表示页帧固定在内存中，永远不应换出。

从而最小化延迟。:c:func:`k_mem_page_out()` 可用于换出在相当长时间内不会被  then invokes the backing store to page in the data page corresponding to

  * ``K_MEM_PAGE_FRAME_RESERVED`` 表示由硬件保留的物理页面，根本不应使用。

访问的数据页。这会释放页框,以便下一个换入可以更快地执行,因为分页代码不需要  the location of the requested data. The backing store copies that data

  * ``K_MEM_PAGE_FRAME_MAPPED`` 在物理页面映射到虚拟内存地址时设置。

调用驱逐算法。  page into the free page frame. Now the data page is in physical memory

  * ``K_MEM_PAGE_FRAME_BUSY`` 表示页帧当前涉及换入/换出操作。

  and execution can continue.

  * ``K_MEM_PAGE_FRAME_BACKED`` 表示页帧在后备存储中有一个干净副本。

术语

K_MEM_SCRATCH_PAGE

==================****There are functions where paging in and out can be invoked manually

  一个特殊页面的虚拟地址，提供给后备存储以：

using :c:func:`k_mem_page_in()` and :c:func:`k_mem_page_out()`.

  * 将数据页从 ``K_MEM_SCRATCH_PAGE`` 复制到指定位置；或者，

  * 将数据页从提供的位置复制到 ``K_MEM_SCRATCH_PAGE``。数据页:c:func:`k_mem_page_in()` can be used to page in data pages



  这用作换入/换出操作的中间页面。此临时页面需要映射为读/写，以便后备存储代码可以访问。======in anticipation that they are required in the near future. This is used to

  但是，数据页本身可能仅在虚拟地址空间中映射为只读。如果将此页面按原样提供给后备存储，

  则数据页必须重新映射为读/写，这会带来安全隐患，因为数据页不再对应用程序的其他部分只读。minimize number of page faults as these data pages are already in physical



分页统计 (Paging Statistics)数据页是数据的页面大小区域。它可能存在于页框中,或被换出到某个后备存储。memory, and thus minimizing latency. :c:func:`k_mem_page_out()` can be

*****************************

它的位置总是可以通过虚拟地址在 CPU 的页表(或等效物)中查找。数据类型将始终used to page out data pages where they are not going to be accessed for

当启用 :kconfig:option:`CONFIG_DEMAND_PAGING_TIMING_HISTOGRAM_NUM_BINS` 时，

可以通过各种函数调用获取分页统计信息：是 ``void *``,或在进行指针运算时在某些情况下是 ``uint8_t *``。a considerable amount of time. This frees up page frames so that the next



* 通过 :c:func:`k_mem_paging_stats_get()` 获取总体统计信息page in can be executed faster as the paging code does not need to invoke



* 如果启用 :kconfig:option:`CONFIG_DEMAND_PAGING_THREAD_STATS`，页框the eviction algorithm.

  通过 :c:func:`k_mem_paging_thread_stats_get()` 获取每个线程的统计信息

====

* 当启用 :kconfig:option:`CONFIG_DEMAND_PAGING_TIMING_HISTOGRAM` 并定义

  :kconfig:option:`CONFIG_DEMAND_PAGING_TIMING_HISTOGRAM_NUM_BINS` 时，Terminology

  可以获取执行时间直方图。请注意，时间高度依赖于架构、SoC 或板。

  强烈建议为特定应用程序定义 ``k_mem_paging_eviction_histogram_bounds[]`` 页框是 RAM 中的页面大小物理内存区域。它是可以放置数据页的容器。它总是通过***********

  和 ``k_mem_paging_backing_store_histogram_bounds[]``。

物理地址引用。Zephyr 有一个惯例,即使用 ``uintptr_t`` 表示物理地址。对于每个

  * 通过 :c:func:`k_mem_paging_histogram_eviction_get()`

    获取驱逐算法的执行时间直方图页框,都会实例化一个 ``struct k_mem_page_frame`` 来存储元数据。每个页框的标志:Data Page



  * 通过 :c:func:`k_mem_paging_histogram_backing_store_page_in_get()`   A data page is a page-sized region of data. It may exist in a page frame,

    获取后备存储执行换入操作的执行时间直方图

* ``K_MEM_PAGE_FRAME_FREE`` 表示页框未使用并且在空闲页框列表上。当设置此标志时,  or be paged out to some backing store. Its location can always be looked

  * 通过 :c:func:`k_mem_paging_histogram_backing_store_page_out_get()`

    获取后备存储执行换出操作的执行时间直方图  其他标志都没有意义,并且不得修改它们。  up in the CPU's page tables (or equivalent) by virtual address.



驱逐算法 (Eviction Algorithm)  The data type will always be ``void *`` or in some cases ``uint8_t *``

******************************

* ``K_MEM_PAGE_FRAME_PINNED`` 表示页框被固定在内存中,永远不应被换出。  when doing pointer arithmetic.

驱逐算法用于确定哪个数据页及其相应的页帧可以换出以释放页帧供下一次换入操作使用。

有四个函数从内核分页代码调用：



* :c:func:`k_mem_paging_eviction_init()` 被调用以初始化驱逐算法。* ``K_MEM_PAGE_FRAME_RESERVED`` 表示硬件保留的物理页,根本不应该使用。Page Frame

  这在 ``POST_KERNEL`` 时调用。

  A page frame is a page-sized physical memory region in RAM. It is a

* :c:func:`k_mem_paging_eviction_add()` 在每次数据页变得有资格将来驱逐时调用。

* ``K_MEM_PAGE_FRAME_MAPPED`` 在物理页映射到虚拟内存地址时设置。  container where a data page may be placed. It is always referred to by

* :c:func:`k_mem_paging_eviction_remove()` 在数据页不再有资格驱逐时调用。

  如果给定的数据页变为固定、取消映射或即将被驱逐，则可能会发生这种情况。  physical address. Zephyr has a convention of using ``uintptr_t`` for physical



* :c:func:`k_mem_paging_eviction_select()` 被调用以选择要驱逐的数据页。* ``K_MEM_PAGE_FRAME_BUSY`` 表示页框当前涉及换入/换出操作。  addresses. For every page frame, a ``struct k_mem_page_frame`` is instantiated to

  函数参数 ``dirty`` 被写入以向调用者发出信号，指示所选数据页自首次换入以来是否已被修改。

  如果 ``dirty`` 位被设置返回，分页代码向后备存储发出信号，将数据页写回存储  store metadata. Flags for each page frame:

  （从而更新其内容）。该函数返回一个指向与所选数据页对应的页帧的指针。

* ``K_MEM_PAGE_FRAME_BACKED`` 表示页框在后备存储中有一个干净的副本。

还有一个附加函数由架构的内存管理代码调用，以在数据页触发访问错误时标记数据页：

:c:func:`k_mem_paging_eviction_accessed()`。LRU 算法使用此功能来重新排队"已使用"的页面。  * ``K_MEM_PAGE_FRAME_FREE`` indicates a page frame is unused and on the list of



目前有两种驱逐算法可用：K_MEM_SCRATCH_PAGE    free page frames. When this flag is set, none of the other flags are



* NRU（最近未使用 - Not-Recently-Used）驱逐算法已作为示例实现。==================    meaningful and they must not be modified.

  这是一个非常简单的算法，根据数据页是否已被访问和修改对其进行排名。

  选择基于此排名。



* LRU（最近最少使用 - Least-Recently-Used）驱逐算法也可用。提供给后备存储的特殊页面的虚拟地址,用于:  * ``K_MEM_PAGE_FRAME_PINNED`` indicates a page frame is pinned in memory

  它基于数据页的排序队列。LRU 代码与 NRU 代码相比更复杂，但效率也更高。

  建议用于生产环境。    and should never be paged out.



要实现新的驱逐算法，必须实现 :c:func:`k_mem_paging_eviction_init()` * 将数据页从 ``k_MEM_SCRATCH_PAGE`` 复制到指定位置;或者,

和 :c:func:`k_mem_paging_eviction_select()`。

如果为算法启用 :kconfig:option:`CONFIG_EVICTION_TRACKING`，* 将数据页从提供的位置复制到 ``K_MEM_SCRATCH_PAGE``。  * ``K_MEM_PAGE_FRAME_RESERVED`` indicates a physical page reserved by hardware

还必须实现这些附加函数：:c:func:`k_mem_paging_eviction_add()`、

:c:func:`k_mem_paging_eviction_remove()`、    and should not be used at all.

:c:func:`k_mem_paging_eviction_accessed()`。

这用作换入/换出操作的中间页。此临时页需要映射为读/写,以便后备存储代码访问。

后备存储 (Backing Store)

*************************但是,数据页本身可能仅在虚拟地址空间中映射为只读。如果将此页按原样提供给  * ``K_MEM_PAGE_FRAME_MAPPED`` is set when a physical page is mapped to



后备存储负责在其相应的页帧和存储之间换入/换出数据页。后备存储,则必须将数据页重新映射为读/写,这具有安全隐患,因为数据页对应用程序    virtual memory address.

这些是必须实现的函数：

的其他部分不再是只读的。

* :c:func:`k_mem_paging_backing_store_init()` 被调用以在 ``POST_KERNEL``

  时初始化后备存储。  * ``K_MEM_PAGE_FRAME_BUSY`` indicates a page frame is currently involved in



* :c:func:`k_mem_paging_backing_store_location_get()` 被调用以保留后备存储位置，分页统计    a page-in/out operation.

  以便可以换出数据页。此 ``location`` 令牌传递给

  :c:func:`k_mem_paging_backing_store_page_out()` 以执行实际的换出操作。********



* :c:func:`k_mem_paging_backing_store_location_free()` 被调用以释放后备存储位置  * ``K_MEM_PAGE_FRAME_BACKED`` indicates a page frame has a clean copy

  （``location`` 令牌），然后可用于后续换出操作。

当启用 :kconfig:option:`CONFIG_DEMAND_PAGING_TIMING_HISTOGRAM_NUM_BINS` 时,    in the backing store.

* :c:func:`k_mem_paging_backing_store_location_query()` 被调用以获取与要虚拟映射

  并按需换入的存储内容相对应的 ``location`` 令牌。可以通过各种函数调用获取分页统计信息:

  在使用 :kconfig:option:`CONFIG_DEMAND_MAPPING` 时最有用。

K_MEM_SCRATCH_PAGE

* :c:func:`k_mem_paging_backing_store_page_in()` 将数据页从与提供的 ``location``

  令牌关联的后备存储位置复制到 ``K_MEM_SCRATCH_PAGE`` 指向的页面。* 通过 :c:func:`k_mem_paging_stats_get()` 获取总体统计信息  The virtual address of a special page provided to the backing store to:



* :c:func:`k_mem_paging_backing_store_page_out()` 将数据页从 ``K_MEM_SCRATCH_PAGE``   * Copy a data page from ``k_MEM_SCRATCH_PAGE`` to the specified location; or,

  复制到与提供的 ``location`` 令牌关联的后备存储位置。

* 如果启用 :kconfig:option:`CONFIG_DEMAND_PAGING_THREAD_STATS`,则通过   * Copy a data page from the provided location to ``K_MEM_SCRATCH_PAGE``.

* :c:func:`k_mem_paging_backing_store_page_finalize()` 在

  :c:func:`k_mem_paging_backing_store_page_in()` 之后调用，  :c:func:`k_mem_paging_thread_stats_get()` 获取每个线程的统计信息  This is used as an intermediate page for page in/out operations. This

  以便可以更新页帧结构以进行内部记账。这可以是无操作。

  scratch needs to be mapped read/write for backing store code to access.

要实现新的后备存储，必须实现上述提到的函数。

如果需要，:c:func:`k_mem_paging_backing_store_page_finalize()` 可以是空函数。* 当启用 :kconfig:option:`CONFIG_DEMAND_PAGING_TIMING_HISTOGRAM` 并定义   However the data page itself may only be mapped as read-only in virtual



API 参考 (API Reference)  :kconfig:option:`CONFIG_DEMAND_PAGING_TIMING_HISTOGRAM_NUM_BINS` 时,  address space. If this page is provided as-is to backing store,

*************************

  可以获取执行时间直方图。请注意,时间高度依赖于架构、SoC 或板。强烈建议  the data page must be re-mapped as read/write which has security

.. doxygengroup:: mem-demand-paging

  为特定应用程序定义 ``k_mem_paging_eviction_histogram_bounds[]`` 和  implications as the data page is no longer read-only to other parts of

驱逐算法 API (Eviction Algorithm APIs)

=======================================  ``k_mem_paging_backing_store_histogram_bounds[]``。  the application.



.. doxygengroup:: mem-demand-paging-eviction



后备存储 API (Backing Store APIs)  * 通过 :c:func:`k_mem_paging_histogram_eviction_get()` 获取驱逐算法的Paging Statistics

==================================

    执行时间直方图*****************

.. doxygengroup:: mem-demand-paging-backing-store



  * 通过 :c:func:`k_mem_paging_histogram_backing_store_page_in_get()` Paging statistics can be obtained via various function calls when

    获取后备存储执行换入的执行时间直方图:kconfig:option:`CONFIG_DEMAND_PAGING_TIMING_HISTOGRAM_NUM_BINS` is enabled:



  * 通过 :c:func:`k_mem_paging_histogram_backing_store_page_out_get()` * Overall statistics via :c:func:`k_mem_paging_stats_get()`

    获取后备存储执行换出的执行时间直方图

* Per-thread statistics via :c:func:`k_mem_paging_thread_stats_get()`

驱逐算法  if :kconfig:option:`CONFIG_DEMAND_PAGING_THREAD_STATS` is enabled

********

* Execution time histogram can be obtained when

驱逐算法用于确定可以将哪个数据页及其对应的页框换出以释放页框用于下一个换入  :kconfig:option:`CONFIG_DEMAND_PAGING_TIMING_HISTOGRAM` is enabled, and

操作。有四个函数从内核分页代码中调用:  :kconfig:option:`CONFIG_DEMAND_PAGING_TIMING_HISTOGRAM_NUM_BINS` is defined.

  Note that the timing is highly dependent on the architecture,

* :c:func:`k_mem_paging_eviction_init()` 被调用以初始化驱逐算法。这在   SoC or board. It is highly recommended that

  ``POST_KERNEL`` 时调用。  ``k_mem_paging_eviction_histogram_bounds[]`` and

  ``k_mem_paging_backing_store_histogram_bounds[]``

* :c:func:`k_mem_paging_eviction_add()` 在每次数据页变得有资格进行未来  be defined for a particular application.

  驱逐时被调用。

  * Execution time histogram of eviction algorithm via

* :c:func:`k_mem_paging_eviction_remove()` 在数据页不再有资格驱逐时被调用。    :c:func:`k_mem_paging_histogram_eviction_get()`

  如果给定的数据页被固定、取消映射或即将被驱逐,则可能发生这种情况。

  * Execution time histogram of backing store doing page-in via

* :c:func:`k_mem_paging_eviction_select()` 被调用以选择要驱逐的数据页。    :c:func:`k_mem_paging_histogram_backing_store_page_in_get()`

  函数参数 ``dirty`` 被写入以向调用者发出所选数据页自首次换入以来是否已被

  修改的信号。如果 ``dirty`` 位被设置返回,分页代码会向后备存储发出信号以将  * Execution time histogram of backing store doing page-out via

  数据页写回存储(从而更新其内容)。该函数返回指向与所选数据页对应的页框的    :c:func:`k_mem_paging_histogram_backing_store_page_out_get()`

  指针。

Eviction Algorithm

还有一个附加函数,当数据页触发访问错误时,由架构的内存管理代码调用来标记数据页:******************

:c:func:`k_mem_paging_eviction_accessed()`。LRU 算法使用它来重新排队"使用过的"

页面。The eviction algorithm is used to determine which data page and its

corresponding page frame can be paged out to free up a page frame

目前有两种驱逐算法可用:for the next page in operation. There are four functions which are

called from the kernel paging code:

* 已实现 NRU(Not-Recently-Used,最近未使用)驱逐算法作为示例。这是一个非常

  简单的算法,它根据数据页是否被访问和修改来对其进行排名。选择基于此排名。* :c:func:`k_mem_paging_eviction_init()` is called to initialize

  the eviction algorithm. This is called at ``POST_KERNEL``.

* 也提供 LRU(Least-Recently-Used,最近最少使用)驱逐算法。它基于数据页的

  排序队列。与 NRU 代码相比,LRU 代码更复杂,但也相当高效。建议用于生产用途。* :c:func:`k_mem_paging_eviction_add()` is called each time a data page becomes

  eligible for future eviction.

要实现新的驱逐算法,必须实现 :c:func:`k_mem_paging_eviction_init()` 和

:c:func:`k_mem_paging_eviction_select()`。如果为算法启用 * :c:func:`k_mem_paging_eviction_remove()` is called when a data page is no

:kconfig:option:`CONFIG_EVICTION_TRACKING`,则还必须实现这些附加函数,  longer eligible for eviction. This may happen if the given data page becomes

:c:func:`k_mem_paging_eviction_add()`、  pinned, gets unmapped or is about to be evicted.

:c:func:`k_mem_paging_eviction_remove()`、

:c:func:`k_mem_paging_eviction_accessed()`。* :c:func:`k_mem_paging_eviction_select()` is called to select

  a data page to evict. A function argument ``dirty`` is written to

后备存储  signal the caller whether the selected data page has been modified

********  since it is first paged in. If the ``dirty`` bit is returned

  as set, the paging code signals to the backing store to write

后备存储负责在其相应的页框和存储之间换入/换出数据页。必须实现以下函数:  the data page back into storage (thus updating its content).

  The function returns a pointer to the page frame corresponding to

* :c:func:`k_mem_paging_backing_store_init()` 被调用以在 ``POST_KERNEL``   the selected data page.

  时初始化后备存储。

There is one additional function which is called by the architecture's memory

* :c:func:`k_mem_paging_backing_store_location_get()` 被调用以保留后备management code to flag data pages when they trigger an access fault:

  存储位置,以便可以换出数据页。此 ``location`` 令牌传递给 :c:func:`k_mem_paging_eviction_accessed()`. This is used by the LRU algorithm

  :c:func:`k_mem_paging_backing_store_page_out()` 以执行实际的换出操作。to requeue "used" pages.



* :c:func:`k_mem_paging_backing_store_location_free()` 被调用以释放后备Two eviction algorithms are currently available:

  存储位置(``location`` 令牌),然后可用于后续换出操作。

* An NRU (Not-Recently-Used) eviction algorithm has been implemented as a

* :c:func:`k_mem_paging_backing_store_location_query()` 被调用以获取与  sample. This is a very simple algorithm which ranks data pages on whether

  要虚拟映射并按需换入的存储内容对应的 ``location`` 令牌。与   they have been accessed and modified. The selection is based on this ranking.

  :kconfig:option:`CONFIG_DEMAND_MAPPING` 一起使用最有用。

* An LRU (Least-Recently-Used) eviction algorithm is also available. It is

* :c:func:`k_mem_paging_backing_store_page_in()` 将数据页从与提供的   based on a sorted queue of data pages. The LRU code is more complex compared

  ``location`` 令牌关联的后备存储位置复制到 ``K_MEM_SCRATCH_PAGE``   to the NRU code but also considerably more efficient. This is recommended for

  指向的页面。  production use.



* :c:func:`k_mem_paging_backing_store_page_out()` 将数据页从 To implement a new eviction algorithm, :c:func:`k_mem_paging_eviction_init()`

  ``K_MEM_SCRATCH_PAGE`` 复制到与提供的 ``location`` 令牌关联的后备and :c:func:`k_mem_paging_eviction_select()` must be implemented.

  存储位置。If :kconfig:option:`CONFIG_EVICTION_TRACKING` is enabled for an algorithm,

these additional functions must also be implemented,

* :c:func:`k_mem_paging_backing_store_page_finalize()` 在 :c:func:`k_mem_paging_eviction_add()`, :c:func:`k_mem_paging_eviction_remove()`,

  :c:func:`k_mem_paging_backing_store_page_in()` 之后调用,以便可以更新:c:func:`k_mem_paging_eviction_accessed()`.

  页框结构以进行内部记账。这可以是无操作。

Backing Store

要实现新的后备存储,必须实现上面提到的函数。如果需要,*************

:c:func:`k_mem_paging_backing_store_page_finalize()` 可以是空函数。

Backing store is responsible for paging in/out data page between

API 参考their corresponding page frames and storage. These are the functions

********which must be implemented:



.. doxygengroup:: mem-demand-paging* :c:func:`k_mem_paging_backing_store_init()` is called to

  initialized the backing store at ``POST_KERNEL``.

驱逐算法 API

============* :c:func:`k_mem_paging_backing_store_location_get()` is called to

  reserve a backing store location so a data page can be paged out.

.. doxygengroup:: mem-demand-paging-eviction  This ``location`` token is passed to

  :c:func:`k_mem_paging_backing_store_page_out()` to perform actual

后备存储 API  page out operation.

============

* :c:func:`k_mem_paging_backing_store_location_free()` is called to

.. doxygengroup:: mem-demand-paging-backing-store  free a backing store location (the ``location`` token) which can

  then be used for subsequent page out operation.

* :c:func:`k_mem_paging_backing_store_location_query()` is called to obtain
  the ``location`` token corresponding to storage content to be virtually
  mapped and paged-in on demand. Most useful with
  :kconfig:option:`CONFIG_DEMAND_MAPPING`.

* :c:func:`k_mem_paging_backing_store_page_in()` copies a data page
  from the backing store location associated with the provided
  ``location`` token to the page pointed by ``K_MEM_SCRATCH_PAGE``.

* :c:func:`k_mem_paging_backing_store_page_out()` copies a data page
  from ``K_MEM_SCRATCH_PAGE`` to the backing store location associated
  with the provided ``location`` token.

* :c:func:`k_mem_paging_backing_store_page_finalize()` is invoked after
  :c:func:`k_mem_paging_backing_store_page_in()` so that the page frame
  struct may be updated for internal accounting. This can be
  a no-op.

To implement a new backing store, the functions mentioned above
must be implemented.
:c:func:`k_mem_paging_backing_store_page_finalize()` can be an empty
function if so desired.

API Reference
*************

.. doxygengroup:: mem-demand-paging

Eviction Algorithm APIs
=======================

.. doxygengroup:: mem-demand-paging-eviction

Backing Store APIs
==================

.. doxygengroup:: mem-demand-paging-backing-store
