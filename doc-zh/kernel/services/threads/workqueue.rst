.. _workqueues_v2:

工作队列线程 (Workqueue Threads)
################################

.. contents::
    :local:
    :depth: 1

:dfn:`工作队列` (workqueue) 是一个内核对象，它使用专用线程以先进先出的方式处理工作项。
每个工作项通过调用工作项指定的函数来处理。工作队列通常由 ISR 或高优先级线程使用，
将非紧急处理卸载到较低优先级的线程，以便不影响时间敏感的处理。

可以定义任意数量的工作队列（仅受可用 RAM 限制）。每个工作队列通过其内存地址引用。

工作队列具有以下关键属性：

* 一个已添加但尚未处理的工作项**队列** (queue)。

* 一个处理队列中工作项的**线程** (thread)。线程的优先级是可配置的，
  允许它根据需要是协作的或抢占的。

无论工作队列线程优先级如何，工作队列线程都将在每个提交的工作项之间让出，
以防止协作工作队列饿死其他线程。

工作队列在使用之前必须进行初始化。这会将其队列设置为空并生成工作队列的线程。
线程永远运行，但在没有工作项可用时会休眠。

.. note::
   此处描述的行为与 Zephyr 2.6 版本之前使用的 Zephyr 工作队列实现有所不同。
   这些变化包括：

   * 精确跟踪已取消工作项的状态，因此调用者无需担心在取消返回时项目可能正在处理。
     仍然需要检查取消的返回值。
   * 使用 :c:macro:`K_NO_WAIT` 直接将可延迟工作项提交到队列，
     而不是总是通过超时 API，这可能会引入延迟。
   * 能够等待工作项完成或队列被排空。
   * 在调度可延迟工作项时对行为进行更精细的控制，特别是允许在再次调度工作项时保持先前的截止时间不变。
   * 当项目在另一个工作队列上处理时，安全处理工作项的重新提交。

   应避免使用 :c:func:`k_work_busy_get()` 或 :c:func:`k_work_is_pending()` 的返回值，
   或测量可延迟工作的剩余时间，以防止与先前实现观察到的类型相同的竞争条件。
   另请参见 `工作队列最佳实践`_。

工作项生命周期 (Work Item Lifecycle)
************************************

可以定义任意数量的**工作项** (work items)。每个工作项通过其内存地址引用。

为工作项分配了一个**处理函数** (handler function)，
该函数是工作队列的线程在处理工作项时执行的函数。此函数接受单个参数，即工作项本身的地址。
工作项还维护有关其状态的信息。

工作项在使用之前必须进行初始化。这会记录工作项的处理函数并将其标记为未挂起。

工作项可以通过 ISR 或线程将其提交到工作队列来**排队** (:c:enumerator:`K_WORK_QUEUED`)。
提交工作项会将工作项追加到工作队列的队列中。一旦工作队列的线程处理完队列中所有前面的工作项，
线程将从队列中删除下一个工作项并调用工作项的处理函数。根据工作队列线程的调度优先级
以及队列中其他项目所需的工作，排队的工作项可能会很快处理，或者可能在队列中停留很长时间。

可延迟工作项可以**调度** (:c:enumerator:`K_WORK_DELAYED`) 到工作队列；
请参见 `可延迟工作`_。

当工作项在工作队列上运行时，它将是**运行中** (:c:enumerator:`K_WORK_RUNNING`)，
如果它在线程请求取消之前开始运行，它也可能是**取消中** (:c:enumerator:`K_WORK_CANCELING`)。

工作项可以处于多个状态；例如，它可以：

* 在队列上运行；
* 标记为取消中（因为线程使用 :c:func:`k_work_cancel_sync()` 等待工作项完成）；
* 排队以在同一队列上再次运行；
* 调度为提交到（可能不同的）队列

*所有这些都是同时发生的*。处于这些状态中任何一种的工作项是**挂起的** (:c:func:`k_work_is_pending()`)
或**忙碌的** (:c:func:`k_work_busy_get()`)。

处理函数可以使用线程可用的任何内核 API。但是，必须谨慎使用可能阻塞的操作
（例如，获取信号量），因为在处理函数完成执行之前，工作队列无法处理其队列中的后续工作项。

如果不需要，可以忽略传递给处理函数的单个参数。如果处理函数需要有关其要执行的工作的其他信息，
则可以将工作项嵌入到更大的数据结构中。然后，处理函数可以使用参数值使用 :c:macro:`CONTAINER_OF`
计算封闭数据结构的地址，从而获得对其所需的其他信息的访问权限。

工作项通常初始化一次，然后在需要执行工作时提交到特定的工作队列。
如果 ISR 或线程尝试提交已排队的工作项，则工作项不受影响；
工作项保留在工作队列队列中的当前位置，并且工作仅执行一次。

允许处理函数将其工作项参数重新提交到工作队列，因为此时工作项不再排队。
这允许处理程序分阶段执行工作，而不会过度延迟工作队列队列中其他工作项的处理。

.. important::
    在工作队列线程处理项目之前，*不得*更改挂起的工作项。这意味着在工作项忙碌时不得重新初始化它。
    此外，在处理函数完成执行之前，不得更改工作项的处理函数执行其工作所需的任何其他信息。

.. _k_delayable_work:

可延迟工作 (Delayable Work)
****************************

ISR 或线程可能需要调度一个仅在指定时间段后才处理的工作项，而不是立即处理。
这可以通过**调度** **可延迟工作项** (delayable work item) 以在将来的时间提交到工作队列来完成。

可延迟工作项包含标准工作项，但添加了记录项目应何时以及在何处提交的字段。

可延迟工作项的初始化和调度到工作队列的方式与标准工作项类似，尽管使用了不同的内核 API。
当发出调度请求时，内核会启动一个超时机制，该机制在指定的延迟过去后触发。
一旦超时发生，内核将工作项提交到指定的工作队列，在那里它保持排队状态，直到以标准方式处理。

请注意，用于可延迟的工作处理程序仍然接收指向底层不可延迟工作结构的指针，
该结构无法从 :c:struct:`k_work_delayable` 公开访问。要访问包含可延迟工作对象的对象，
请使用此习惯用法：

.. code-block:: c

   static void work_handler(struct k_work *work)
   {
           struct k_work_delayable *dwork = k_work_delayable_from_work(work);
           struct work_context *ctx = CONTAINER_OF(dwork, struct work_context,
	                                           timed_work);
           ...


触发工作 (Triggered Work)
**************************

:c:func:`k_work_poll_submit` 接口响应**轮询事件** (poll event)（请参见 :ref:`polling_v2`）
调度触发的工作项，当监视的资源可用或引发轮询信号或发生超时时，将调用用户定义的函数。
与 :c:func:`k_poll` 相比，触发的工作不需要专用线程等待或主动轮询轮询事件。

触发的工作项是具有以下附加属性的标准工作项：

* 指向轮询事件数组的指针，该数组将触发工作项提交到工作队列

* 包含轮询事件的数组的大小。

触发的工作项的初始化和提交到工作队列的方式与标准工作项类似，尽管使用了专用的内核 API。
当发出提交请求时，内核开始观察轮询事件指定的内核对象。一旦至少一个观察到的内核对象的状态发生变化，
工作项就会提交到指定的工作队列，在那里它保持排队状态，直到以标准方式处理。

.. important::
    触发的工作项以及引用的轮询事件数组必须有效，并且在完整的触发工作项生命周期内
    （从提交到工作项执行或取消）不能修改。

ISR 或线程可以**取消**它已提交的触发工作项，只要它仍在等待轮询事件。
在这种情况下，内核停止等待附加的轮询事件，并且不执行指定的工作。否则无法执行取消。

系统工作队列 (System Workqueue)
********************************

内核定义了一个称为*系统工作队列* (system workqueue) 的工作队列，
它可用于任何需要工作队列支持的应用程序或内核代码。系统工作队列是可选的，
仅在应用程序使用它时才存在。

.. important::
    仅当无法将新工作项提交到系统工作队列时，才应定义其他工作队列，
    因为每个新工作队列都会在内存占用方面产生重大成本。如果新工作队列的工作项无法与现有系统工作队列
    工作项共存而不会产生不可接受的影响，则可以证明新工作队列是合理的；
    例如，如果新工作项执行阻塞操作，这些操作会将其他系统工作队列处理延迟到不可接受的程度。

如何使用工作队列
****************

定义和控制工作队列 (Defining and Controlling a Workqueue)
========================================================

工作队列使用 :c:struct:`k_work_q` 类型的变量定义。工作队列通过定义其线程使用的堆栈区域、
初始化 :c:struct:`k_work_q`（将其内存清零或调用 :c:func:`k_work_queue_init`），
然后调用 :c:func:`k_work_queue_start` 来初始化。堆栈区域必须使用
:c:macro:`K_THREAD_STACK_DEFINE` 定义，以确保它在内存中正确设置。

以下代码定义并初始化工作队列：

.. code-block:: c

    #define MY_STACK_SIZE 512
    #define MY_PRIORITY 5

    K_THREAD_STACK_DEFINE(my_stack_area, MY_STACK_SIZE);

    struct k_work_q my_work_q;

    k_work_queue_init(&my_work_q);

    k_work_queue_start(&my_work_q, my_stack_area,
                       K_THREAD_STACK_SIZEOF(my_stack_area), MY_PRIORITY,
		       NULL);

此外，队列标识和与线程重新调度相关的某些行为可以由可选的最终参数控制；
有关详细信息，请参见 :c:func:`k_work_queue_start()`。

以下 API 可用于与工作队列交互：

* :c:func:`k_work_queue_drain()` 可用于阻塞调用者，直到工作队列没有剩余项目。
  从工作队列线程重新提交的工作项在队列排空时被接受，但来自任何其他线程或 ISR 的工作项被拒绝。
  对提交更多工作的限制可以延长到排空操作完成之后，以便允许阻塞线程在队列"插入" (plugged) 时执行其他工作。
  请注意，排空队列对调度或处理可延迟项目没有影响，但如果队列被插入且截止时间到期，
  则项目将静默失败提交。
* :c:func:`k_work_queue_unplug()` 删除由于先前排空操作而对队列提交的任何先前阻止。

提交工作项 (Submitting a Work Item)
===================================

工作项使用 :c:struct:`k_work` 类型的变量定义。它必须通过调用 :c:func:`k_work_init` 进行初始化，
除非它使用 :c:macro:`K_WORK_DEFINE` 定义，在这种情况下，初始化在编译时执行。

初始化的工作项可以通过调用 :c:func:`k_work_submit` 提交到系统工作队列，
或通过调用 :c:func:`k_work_submit_to_queue` 提交到指定的工作队列。

以下代码演示了 ISR 如何将错误消息的打印卸载到系统工作队列。
请注意，如果 ISR 在工作项仍排队时尝试重新提交工作项，则工作项保持不变，并且不会打印关联的错误消息。

.. code-block:: c

    struct device_info {
        struct k_work work;
        char name[16]
    } my_device;

    void my_isr(void *arg)
    {
        ...
        if (error detected) {
            k_work_submit(&my_device.work);
	}
	...
    }

    void print_error(struct k_work *item)
    {
        struct device_info *the_device =
            CONTAINER_OF(item, struct device_info, work);
        printk("Got error on device %s\n", the_device->name);
    }

    /* initialize name info for a device */
    strcpy(my_device.name, "FOO_dev");

    /* initialize work item for printing device's error messages */
    k_work_init(&my_device.work, print_error);

    /* install my_isr() as interrupt handler for the device (not shown) */
    ...


以下 API 可用于检查工作项的状态或与之同步：

* :c:func:`k_work_busy_get()` 返回指示工作项状态的标志快照。
  零值表示工作未调度、提交、执行或仍被工作队列基础结构引用。
* :c:func:`k_work_is_pending()` 是一个助手，当且仅当工作已调度、排队或运行时指示 ``true``。
* :c:func:`k_work_flush()` 可以从线程调用以阻塞，直到工作项完成。如果工作未挂起，它会立即返回。
* :c:func:`k_work_cancel()` 尝试防止工作项被执行。这可能成功也可能不成功。从 ISR 调用是安全的。
* :c:func:`k_work_cancel_sync()` 可以从线程调用以阻塞，直到工作完成；
  如果取消成功或不需要（工作未提交或运行），它将立即返回。这可以在从 ISR 调用 :c:func:`k_work_cancel()`
  后使用，以确认 ISR 启动的取消完成。

调度可延迟工作项 (Scheduling a Delayable Work Item)
===================================================

可延迟工作项使用 :c:type:`k_work_delayable` 类型的变量定义。
它必须通过调用 :c:func:`k_work_init_delayable` 进行初始化。

对于延迟工作，有两种常见的用例，具体取决于如果发生新事件是否应延长截止时间。
一个例子是收集异步传入的数据，例如来自与键盘关联的 UART 的字符。有两个 API 在延迟后提交工作：

* :c:func:`k_work_schedule()`（或 :c:func:`k_work_schedule_for_queue()`）
  调度工作在特定时间或延迟后执行。在延迟完成之前使用此 API 进一步尝试调度同一项目
  不会更改项目将提交到其队列的时间。如果策略是继续收集数据，直到自**第一个**未处理数据接收以来的指定延迟，
  请使用此选项；
* :c:func:`k_work_reschedule()`（或 :c:func:`k_work_reschedule_for_queue()`）
  无条件设置工作的截止时间，替换任何先前未完成的延迟并在必要时更改目标队列。
  如果策略是继续收集数据，直到自**最后一个**未处理数据接收以来的指定延迟，请使用此选项。

如果工作项未调度，则两个 API 的行为相同。如果将 :c:macro:`K_NO_WAIT` 指定为延迟，
则行为就像项目立即直接提交到目标队列一样，而无需等待最小超时
（除非使用 :c:func:`k_work_schedule()` 且先前的延迟尚未完成）。

两者也都有允许控制用于提交的队列的变体。

助手函数 :c:func:`k_work_delayable_from_work()` 可用于从传递给工作处理函数的
:c:struct:`k_work` 指针获取指向包含 :c:struct:`k_work_delayable` 的指针。

以下附加 API 可用于检查工作项的状态或与之同步：

* :c:func:`k_work_delayable_busy_get()` 是可延迟工作的 :c:func:`k_work_busy_get()` 的类似物。
* :c:func:`k_work_delayable_is_pending()` 是可延迟工作的 :c:func:`k_work_is_pending()` 的类似物。
* :c:func:`k_work_flush_delayable()` 是可延迟工作的 :c:func:`k_work_flush()` 的类似物。
* :c:func:`k_work_cancel_delayable()` 是可延迟工作的 :c:func:`k_work_cancel()` 的类似物；
  类似地，:c:func:`k_work_cancel_delayable_sync()` 也是如此。

与工作项同步 (Synchronizing with Work Items)
=============================================

虽然可以使用 :c:func:`k_work_busy_get()` 和 :c:func:`k_work_delayable_busy_get()`
从任何上下文确定常规和可延迟工作项的状态，但某些用例需要在提交工作项后与之同步。
:c:func:`k_work_flush()`、:c:func:`k_work_cancel_sync()` 和 :c:func:`k_work_cancel_delayable_sync()`
可以从线程上下文调用以等待，直到达到请求的状态。

必须为这些 API 提供 :c:struct:`k_work_sync` 对象，该对象没有应用程序可检查的组件，
但需要提供同步对象。如果代码预期在具有 :kconfig:option:`CONFIG_KERNEL_COHERENCE`
的架构上工作，则这些对象不应在堆栈上分配。

工作队列最佳实践 (Workqueue Best Practices)
********************************************

避免竞争条件 (Avoid Race Conditions)
====================================

有时工作项必须处理的数据本质上是线程安全的，例如当它被某个线程放入 :c:struct:`k_queue`
并在工作线程中处理时。更常见的是需要外部同步以避免数据竞争：
工作线程可能检查或操作被另一个线程或中断访问的共享状态的情况。
此类状态可能是指示需要完成工作的标志，或由 ISR 或线程填充并由工作处理程序读取的共享对象。

对于简单的标志，:ref:`atomic_v2` 可能就足够了。在其他情况下，自旋锁 (:c:struct:`k_spinlock`)
或线程感知锁 (:c:struct:`k_sem`、:c:struct:`k_mutex`、...) 可用于确保不会发生数据竞争。

如果所选的锁定机制可以 :ref:`api_term_sleep`，则允许工作线程休眠将使其他工作队列项目饿死，
这些项目可能需要取得进展才能释放锁。工作处理程序应尝试使用其无等待路径获取锁。例如：

.. code-block:: c

   static void work_handler(struct work *work)
   {
           struct work_context *parent = CONTAINER_OF(work, struct work_context,
	                                              work_item);

           if (k_mutex_lock(&parent->lock, K_NO_WAIT) != 0) {
                   /* NB: Submit will fail if the work item is being cancelled. */
                   (void)k_work_submit(work);
		   return;
	   }

	   /* do stuff under lock */
	   k_mutex_unlock(&parent->lock);
	   /* do stuff without lock */
   }

请注意，如果锁由优先级低于工作队列的线程持有，则重新提交可能会使将释放锁的线程饿死，
导致应用程序失败。在需要上述习惯用法的情况下，首选可延迟工作项，
并且应使用非零延迟（重新）调度工作，以允许持有锁的线程取得进展。

请注意，如果工作项已被取消，则从工作处理程序提交可能会失败。通常这是可以接受的，
因为一旦处理程序完成，取消将完成。如果不是，则上面的代码必须采取其他步骤通知应用程序无法执行工作。

工作项本身是自锁定的，因此您不需要持有外部锁只是为了提交或调度它们。
即使您使用由此类锁保护的外部状态来防止进一步重新提交，只要您确定最终该项目将获取其锁并检查该状态
以确定它是否应该执行任何操作，执行重新提交就是安全的。当可延迟工作项由于无法获取锁而在其处理程序中
重新调度时，需要一些其他自锁定状态（例如，当取消启动时由应用程序/驱动程序设置的原子标志）
来检测取消并避免在截止时间后再次提交已取消的工作项。

检查返回值 (Check Return Values)
=================================

所有工作 API 函数都返回底层操作的状态，在许多情况下，验证是否获得了预期结果很重要。

* 提交工作项 (:c:func:`k_work_submit_to_queue`) 如果工作正在被取消或队列不接受新项目，
  则可能失败。如果发生这种情况，工作将不会执行，这可能导致由工作处理程序活动驱动的子系统变得无响应。
* 异步取消 (:c:func:`k_work_cancel` 或 :c:func:`k_work_cancel_delayable`)
  可以在工作项仍由处理程序运行时完成。继续操作与工作处理程序共享的状态将导致可能导致失败的数据竞争。

许多竞争条件存在于 Zephyr 代码中，因为未检查操作的结果。

可能有充分的理由认为，指示操作未按预期完成的返回值不是问题。
在这些情况下，代码应该清楚地记录这一点，通过 (1) 将返回值强制转换为 ``void`` 以指示结果被有意忽略，
以及 (2) 记录在意外情况下会发生什么。例如：

.. code-block:: c

   /* If this fails, the work handler will check pub->active and
    * exit without transmitting.
    */
   (void)k_work_cancel_delayable(&pub->timer);

但是，在这种情况下，以下代码仍必须避免数据竞争，因为它无法保证工作线程不访问与工作相关的状态。

不要过早优化 (Don't Optimize Prematurely)
=========================================

工作队列 API 设计为从多个线程和中断调用时是安全的。尝试在外部检查工作项的状态并根据结果做出决定
可能会产生新问题。

因此，当新工作进来时，只需提交它。不要尝试通过使用 :c:func:`k_work_is_pending` 或
:c:func:`k_work_busy_get` 检查快照状态来检查工作项是否已提交，或通过
:c:func:`k_work_delayable_remaining_get()` 检查非零延迟来"优化"。
这些检查是脆弱的："忙碌"指示在返回测试时可能已过时，并且如果从多个上下文提交工作，
或者（对于可延迟工作）如果截止时间已完成但工作仍处于排队或运行状态，"非忙碌"指示也可能是错误的。

一般最佳实践是始终在共享状态中维护某些条件，处理程序可以检查这些条件以确认是否有工作要做。
这样，您可以使用工作处理程序作为标准清理路径：而不是必须在提交项目的点处理取消和清理，
您可能能够在工作处理程序本身中完成所有操作。

您可以安全使用 :c:func:`k_work_is_pending` 的罕见情况是作为检查以避免调用
:c:func:`k_work_flush` 或 :c:func:`k_work_cancel_sync`，如果您*确定*在检查时没有其他东西
可能提交工作（通常是因为您持有防止访问用于提交的状态的锁）。

建议用途 (Suggested Uses)
**************************

使用系统工作队列将复杂的中断相关处理从 ISR 推迟到共享线程。
这允许及时完成中断相关处理，而不会影响系统响应后续中断的能力，
并且不需要应用程序定义和管理额外的线程来执行处理。

配置选项 (Configuration Options)
*********************************

相关配置选项：

* :kconfig:option:`CONFIG_SYSTEM_WORKQUEUE_STACK_SIZE`
* :kconfig:option:`CONFIG_SYSTEM_WORKQUEUE_PRIORITY`
* :kconfig:option:`CONFIG_SYSTEM_WORKQUEUE_NO_YIELD`

API 参考 (API Reference)
*************************

.. doxygengroup:: workqueue_apis
