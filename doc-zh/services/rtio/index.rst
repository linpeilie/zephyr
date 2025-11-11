.. _rtio:

实时 I/O (RTIO) (Real Time I/O (RTIO))
######################################

.. contents::
  :local:
  :depth: 2

.. image:: rings.png
  :width: 800
  :alt: 提交和完成环形队列 (Submissions and Completion Ring Queues)

RTIO 提供了一个框架,用于执行事件驱动 I/O 的异步操作链。本节介绍 RTIO API、队列、执行器、iodev 以及与外设设备的常见使用模式。(RTIO provides a framework for doing asynchronous operation chains with event driven I/O. This section covers the RTIO API, queues, executor, iodev, and common usage patterns with peripheral devices.)

RTIO 在其操作和 API 方面从 Linux 的 io_uring 中获得了很多灵感,因为该 API 与硬件传输队列和描述(如 DMA 传输列表)非常匹配。(RTIO takes a lot of inspiration from Linux's io_uring in its operations and API as that API matches up well with hardware transfer queues and descriptions such as DMA transfer lists.)

问题 (Problem)
**************

如今,在 Zephyr 中希望执行复杂 DMA 或中断驱动操作的应用程序需要直接了解硬件及其工作方式。DMA API 对其他 Zephyr 设备及其关系没有理解。(An application wishing to do complex DMA or interrupt driven operations today in Zephyr requires direct knowledge of the hardware and how it works. There is no understanding in the DMA API of other Zephyr devices and how they relate.)

这意味着执行复杂的音频、视频或传感器流需要直接的硬件知识或 DMA 控制器上的泄漏抽象。这两种方式都不理想。(This means doing complex audio, video, or sensor streaming requires direct hardware knowledge or leaky abstractions over DMA controllers. Neither is ideal.)

要启用异步操作,尤其是使用 DMA,需要描述要做什么,而不是通过 C 和回调直接操作。启用 DMA 功能(如具有优先级的通道和传输序列)需要的不仅仅是简单的描述列表。(To enable asynchronous operations, especially with DMA, a description of what to do rather than direct operations through C and callbacks is needed. Enabling DMA features such as channels with priority, and sequences of transfers requires more than a simple list of descriptions.)

使用 DMA 和/或中断驱动的 I/O 不应该决定调用是否阻塞。(Using DMA and/or interrupt driven I/O shouldn't dictate whether or not the call is blocking or not.)

灵感,引入 io_uring (Inspiration, introducing io_uring)
******************************************************

最好不要重新发明轮子(或者在这种情况下是环),来自 Linux 内核的 io_uring API 提供了一个成功的模型。在 io_uring 中,有两个无锁环形缓冲区充当内核和用户态应用程序之间共享的队列。一个队列用于提交条目,可以链接和刷新以创建并发的顺序请求。第二个队列用于完成队列事件。实际上只需要一个系统调用来执行许多操作,即 io_uring_submit 调用。当给定要等待的操作数时,此调用可能会阻塞调用者。(It's better not to reinvent the wheel (or ring in this case) and io_uring as an API from the Linux kernel provides a winning model. In io_uring there are two lock-free ring buffers acting as queues shared between the kernel and a userland application. One queue for submission entries which may be chained and flushed to create concurrent sequential requests. A second queue for completion queue events. Only a single syscall is actually required to execute many operations, the io_uring_submit call. This call may block the caller when a number of operations to wait on is given.)

此模型很好地映射到 DMA 和中断驱动的传输。以异步方式执行一系列操作的请求直接关系到硬件通常使用中断驱动状态机工作的方式,可能涉及多个外设 IP,如总线和 DMA 控制器。(This model maps well to DMA and interrupt driven transfers. A request to do a sequence of operations in an asynchronous way directly relates to the way hardware typically works with interrupt driven state machines potentially involving multiple peripheral IPs like bus and DMA controllers.)

提交队列 (Submission Queue)
***************************

提交队列(sq)是并发链中要执行的操作的描述。(The submission queue (sq), is the description of the operations to perform in concurrent chains.)

例如,想象一个典型的 SPI 传输,您希望先写入寄存器地址然后读取。因此操作序列可能是...(For example imagine a typical SPI transfer where you wish to write a register address to then read from. So the sequence of operations might be...)

   1. 片选 (Chip Select)
   2. 时钟使能 (Clock Enable)
   3. 将寄存器地址写入 SPI 发送寄存器 (Write register address into SPI transmit register)
   4. 从 SPI 接收寄存器读取到缓冲区 (Read from the SPI receive register into a buffer)
   5. 禁用时钟 (Disable clock)
   6. 禁用片选 (Disable Chip Select)

如果此操作链中的任何内容失败,则放弃。其中一些操作可以体现在设备抽象中,该抽象理解读取或写入隐式意味着设置时钟和片选。请求的事务性质也需要以某种方式体现。在上述操作中,也许读取可以使用 DMA 完成,因为它足够大,有意义。这需要了解如何设置设备的特定 DMA 来执行此操作。(If anything in this chain of operations fails give up. Some of those operations can be embodied in a device abstraction that understands a read or write implicitly means setup the clock and chip select. The transactional nature of the request also needs to be embodied in some manner. Of the operations above perhaps the read could be done using DMA as its large enough make sense. That requires an understanding of how to setup the device's particular DMA to do so.)

上述操作序列在 RTIO 中体现为提交队列条目(sqe)链。通过在 sqe 中设置位标志来完成链接,以表示下一个 sqe 必须等待当前 sqe。(The above sequence of operations is embodied in RTIO as chain of submission queue entries (sqe). Chaining is done by setting a bitflag in an sqe to signify the next sqe must wait on the current one.)

因为片选和时钟对于总线上的特定 SPI 控制器和设备是通用的,所以它体现在 RTIO 称为 iodev 的东西中。(Because the chip select and clocking is common to a particular SPI controller and device on the bus it is embodied in what RTIO calls an iodev.)

对同一 iodev 的多个操作按提供的顺序尽快完成。如果两个操作链在使用同一设备的不同点有变化,则可能一个链必须等待另一个链完成。(Multiple operations against the same iodev are done in the order provided as soon as possible. If two operation chains have varying points using the same device its possible one chain will have to wait for another to complete.)

完成队列 (Completion Queue)
***************************

为了知道 sqe 何时完成,有一个完成队列(cq)和完成队列事件(cqe)。sqe 一旦完成,就会将 cqe 推入 cq。cqe 的顺序可能与 sqe 的顺序不同。但是,sqe 链将确保顺序和失败级联。(In order to know when a sqe has completed there is a completion queue (cq) with completion queue events (cqe). A sqe once completed results in a cqe being pushed into the cq. The ordering of cqe may not be the same order of sqe. A chain of sqe will however ensure ordering and failure cascading.)

其他潜在的方案也是可能的,但完成队列是 io_uring 和其他类似操作系统 API 的一个久经考验的想法。(Other potential schemes are possible but a completion queue is a well trod idea with io_uring and other similar operating system APIs.)

执行器 (Executor)
*****************

RTIO 执行器是一个低开销的并发 I/O 任务调度器。它确保某些请求标志提供预期的行为。它获取提交列表,按顺序处理它们。各种标志允许改变提交的处理方式。可以形成有序的提交链、事务性提交集或创建多次触发(持续产生)请求的标志都是可能的!(The RTIO executor is a low overhead concurrent I/O task scheduler. It ensures certain request flags provide the expected behavior. It takes a list of submissions working through them in order. Various flags allow for changing the behavior of how submissions are worked through. Flags to form in order chains of submissions, transactional sets of submissions, or create multi-shot (continuously producing) requests are all possible!)

IO 设备 (IO Device)
*******************

将提交队列条目(sqe)转换为完成队列事件(cqe)是实现 iodev(IO 设备)API 的对象的工作。此 API 以 iodev 提交 API 调用的形式接受请求。io 设备的工作是处理其内部提交队列并将它们转换为完成。实际上,每个 io 设备都可以被视为一个独立的、事件驱动的类 actor 对象,它接受永无止境的类 I/O 请求队列。iodev 如何完成这项工作取决于 iodev 的作者,也许整个操作队列可以转换为一组 DMA 传输描述符,这意味着硬件几乎完成了所有真正的工作。(Turning submission queue entries (sqe) into completion queue events (cqe) is the job of objects implementing the iodev (IO device) API. This API accepts requests in the form of the iodev submit API call. It is the io devices job to work through its internal queue of submissions and convert them into completions. In effect every io device can be viewed as an independent, event driven actor like object, that accepts a never ending queue of I/O like requests. How the iodev does this work is up to the author of the iodev, perhaps the entire queue of operations can be converted to a set of DMA transfer descriptors, meaning the hardware does almost all of the real work.)

取消 (Cancellation)
*******************

取消已排队的操作是可能的,但不能保证。如果 SQE 尚未开始,则调用 :c:func:`rtio_sqe_cancel` 可能会移除 SQE 并且永远不会运行它。但是,如果 SQE 已经开始运行,则取消请求将被忽略。(Canceling an already queued operation is possible but not guaranteed. If the SQE has not yet started, it's likely that a call to :c:func:`rtio_sqe_cancel` will remove the SQE and never run it. If, however, the SQE already started running, the cancel request will be ignored.)

内存池 (Memory pools)
*********************

在某些情况下,读取请求可能不知道将产生多少数据。或者,读取器可能正在处理来自多个 io 设备的数据,其中数据的频率是不可预测的。在这些情况下,将内存绑定到正在进行的读取请求可能是浪费的。相反,使用内存池,要读取到的内存留给 iodev 从与读取关联的 RTIO 上下文关联的内存池中分配。要创建这样的 RTIO 上下文,可以使用 :c:macro:`RTIO_DEFINE_WITH_MEMPOOL`。它允许创建一个具有专用"内存块"池的 RTIO 上下文,这些内存块可以被 iodev 消耗。下面是一个设置带有内存池的 RTIO 上下文的代码片段。内存池有 128 个块,每个块的大小为 16 字节,数据是 4 字节对齐的。(In some cases requests to read may not know how much data will be produced. Alternatively, a reader might be handling data from multiple io devices where the frequency of the data is unpredictable. In these cases it may be wasteful to bind memory to in flight read requests. Instead with memory pools the memory to read into is left to the iodev to allocate from a memory pool associated with the RTIO context that the read was associated with. To create such an RTIO context the :c:macro:`RTIO_DEFINE_WITH_MEMPOOL` can be used. It allows creating an RTIO context with a dedicated pool of "memory blocks" which can be consumed by the iodev. Below is a snippet setting up the RTIO context with a memory pool. The memory pool has 128 blocks, each block has the size of 16 bytes, and the data is 4 byte aligned.)

.. code-block:: C

  #include <zephyr/rtio/rtio.h>

  #define SQ_SIZE       4
  #define CQ_SIZE       4
  #define MEM_BLK_COUNT 128
  #define MEM_BLK_SIZE  16
  #define MEM_BLK_ALIGN 4

  RTIO_DEFINE_WITH_MEMPOOL(rtio_context,
      SQ_SIZE, CQ_SIZE, MEM_BLK_COUNT, MEM_BLK_SIZE, MEM_BLK_ALIGN);

当需要读取时,调用者只需将调用 :c:func:`rtio_sqe_prep_read`(它接受指向缓冲区的指针和长度)替换为对 :c:func:`rtio_sqe_prep_read_with_pool` 的调用。iodev 只需要进行很小的更改,它既适用于预分配的数据缓冲区,也适用于内存池。当读取准备就绪时,iodev 不应直接从 :c:struct:`rtio_iodev_sqe` 获取缓冲区,而应通过调用 :c:func:`rtio_sqe_rx_buf` 来获取缓冲区和计数,如下所示:(When a read is needed, the caller simply needs to replace the call :c:func:`rtio_sqe_prep_read` (which takes a pointer to a buffer and a length) with a call to :c:func:`rtio_sqe_prep_read_with_pool`. The iodev requires only a small change which works with both pre-allocated data buffers as well as the mempool. When the read is ready, instead of getting the buffers directly from the :c:struct:`rtio_iodev_sqe`, the iodev should get the buffer and count by calling :c:func:`rtio_sqe_rx_buf` like so:)

.. code-block:: C

  uint8_t *buf;
  uint32_t buf_len;
  int rc = rtio_sqe_rx_buff(iodev_sqe, MIN_BUF_LEN, DESIRED_BUF_LEN, &buf, &buf_len);

  if (rc != 0) {
    LOG_ERR("Failed to get buffer of at least %u bytes", MIN_BUF_LEN);
    return;
  }

最后,消费者将能够通过 :c:func:`rtio_cqe_get_mempool_buffer` 访问分配的缓冲区。(Finally, the consumer will be able to access the allocated buffer via :c:func:`rtio_cqe_get_mempool_buffer`.)

.. code-block:: C

  uint8_t *buf;
  uint32_t buf_len;
  int rc = rtio_cqe_get_mempool_buffer(&rtio_context, &cqe, &buf, &buf_len);

  if (rc != 0) {
    LOG_ERR("Failed to get mempool buffer");
    return rc;
  }

  /* Release the cqe events (note that the buffer is not released yet */
  rtio_cqe_release_all(&rtio_context);

  /* Do something with the memory */

  /* Release the mempool buffer */
  rtio_release_buffer(&rtio_context, buf);

何时使用 (When to Use)
**********************

RTIO 在并发或批量 I/O 流有用的情况下很有用。(RTIO is useful in cases where concurrent or batch like I/O flows are useful.)

从驱动程序/硬件的角度来看,API 能够批量处理 I/O 请求,可能以最佳方式进行。例如,对同一 SPI 外设的许多请求可能会完全转换为硬件命令队列或 DMA 传输描述符。这意味着硬件可能比以往任何时候都做得更多。(From the driver/hardware perspective the API enables batching of I/O requests, potentially in an optimal way. Many requests to the same SPI peripheral for example might be translated to hardware command queues or DMA transfer descriptors entirely. Meaning the hardware can potentially do more than ever.)

每个 RTIO 上下文和 iodev 都有很小的成本。这个成本可以与为每个并发 I/O 操作使用线程或每个外设的自定义队列和线程相权衡。RTIO 的成本要低得多。(There is a small cost to each RTIO context and iodev. This cost could be weighed against using a thread for each concurrent I/O operation or custom queues and threads per peripheral. RTIO is much lower cost than that.)

支持的总线 (Supported Buses)
****************************

要检查您的总线是否原生支持 RTIO,您可以检查驱动程序 API 实现,如果驱动程序实现了总线 API 的 ``iodev_submit`` 函数,则支持 RTIO。如果驱动程序不支持 RTIO API,它将把提交函数设置为 ``i2c_iodev_submit_fallback``。(To check if your bus supports RTIO natively, you can check the driver API implementation, if the driver implements the ``iodev_submit`` function of the bus API, then RTIO is supported. If the driver doesn't support the RTIO APIs, it will set the submit function to ``i2c_iodev_submit_fallback``.)

I2C 总线有一个默认实现,它允许应用程序利用 RTIO 工作队列,同时供应商实现提交函数。使用此队列,任何未实现 ``iodev_submit`` 函数的 I2C 总线驱动程序将推迟到工作项,该工作项将执行阻塞的 I2C 事务。要更改池大小,请为 :kconfig:option:`CONFIG_RTIO_WORKQ_POOL_ITEMS` 设置不同的值。(I2C buses have a default implementation which allows apps to leverage the RTIO work queue while vendors implement the submit function. With this queue, any I2C bus driver that does not implement the ``iodev_submit`` function will defer to a work item which will perform a blocking I2C transaction. To change the pool size, set a different value to :kconfig:option:`CONFIG_RTIO_WORKQ_POOL_ITEMS`.)

API 参考 (API Reference)
*************************

.. doxygengroup:: rtio
