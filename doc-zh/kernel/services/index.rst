.. _kernel_api:

内核服务 (Kernel Services)
###########################

Zephyr 内核是每个 Zephyr 应用程序的核心。它提供低占用空间、高性能、多线程执行环境，
并具有丰富的可用功能集。Zephyr 生态系统的其他部分，包括设备驱动程序、网络堆栈
和特定于应用程序的代码，都使用内核的功能来创建完整的应用程序。

内核的可配置特性允许您仅整合应用程序所需的功能，
使其非常适合内存量有限（少至 2 KB！）或具有简单多线程要求
（例如一组中断处理程序和单个后台任务）的系统。
此类系统的示例包括：嵌入式传感器集线器、环境传感器、简单 LED 可穿戴设备和商店库存标签。

需要更多内存（50 到 900 KB）、多个通信设备（如 Wi-Fi 和蓝牙低功耗）以及复杂多线程的应用程序
也可以使用 Zephyr 内核开发。此类系统的示例包括：健身可穿戴设备、智能手表和 IoT 无线网关。

调度、中断和同步 (Scheduling, Interrupts, and Synchronization)
******************************************************************

这些页面涵盖与线程调度和同步相关的基本内核服务。

.. toctree::
   :maxdepth: 1

   threads/index.rst
   scheduling/index.rst
   threads/system_threads.rst
   threads/workqueue.rst
   threads/nothread.rst
   interrupts.rst
   polling.rst
   synchronization/semaphores.rst
   synchronization/mutexes.rst
   synchronization/condvar.rst
   synchronization/events.rst
   smp/smp.rst

.. _kernel_data_passing_api:

数据传递 (Data Passing)
************************

这些页面涵盖可用于在线程和 ISR 之间传递数据的内核对象。

下表总结了它们的高级功能。

===============   ==============      ===================    ================    =================   =================  ==============  ===============================
对象              双向?               数据结构               数据项大小          数据对齐            ISR 可接收?        ISR 可发送?     溢出处理
===============   ==============      ===================    ================    =================   =================  ==============  ===============================
FIFO              否                  队列                   任意 [#f1]_         4 B [#f2]_          是 [#f3]_          是              N/A
LIFO              否                  队列                   任意 [#f1]_         4 B [#f2]_          是 [#f3]_          是              N/A
Stack             否                  数组                   字                  字                  是 [#f3]_          是              未定义行为
Message queue     否                  环形缓冲区             任意 [#f6]_         2 的幂              是 [#f3]_          是              挂起线程或返回 -errno
Mailbox           是                  队列                   任意 [#f1]_         任意                否                 否              N/A
Pipe              否                  环形缓冲区 [#f4]_      任意                任意                是 [#f5]_          是 [#f5]_       挂起线程或返回 -errno
===============   ==============      ===================    ================    =================   =================  ==============  ===============================

.. rubric:: 脚注 (Footnotes)

.. [#f1] 调用者在数据元素本身中为队列开销分配空间。

.. [#f2] 使用 :c:func:`k_fifo_alloc_put()` 和 :c:func:`k_lifo_alloc_put()`
         添加的对象没有对齐约束，但使用来自调用线程资源池的临时内存。

.. [#f3] ISR 只能在将 K_NO_WAIT 作为超时参数传递时接收。

.. [#f4] 可选。

.. [#f5] ISR 只能在将 K_NO_WAIT 作为超时参数传递时发送和/或接收。

.. [#f6] 数据项大小必须是数据对齐的倍数。

.. toctree::
   :maxdepth: 1

   data_passing/queues.rst
   data_passing/fifos.rst
   data_passing/lifos.rst
   data_passing/stacks.rst
   data_passing/message_queues.rst
   data_passing/mailboxes.rst
   data_passing/pipes.rst

.. _kernel_memory_management_api:

内存管理 (Memory Management)
*****************************

请参见 :ref:`memory_management_api`。

时间 (Timing)
*************

这些页面涵盖与时间相关的服务。

.. toctree::
   :maxdepth: 1

   timing/clocks.rst
   timing/timers.rst

其他 (Other)
************

这些页面涵盖其他内核服务。

.. toctree::
   :maxdepth: 1

   other/atomic.rst
   other/float.rst
   other/version.rst
   other/fatal.rst
   other/thread_local_storage.rst
