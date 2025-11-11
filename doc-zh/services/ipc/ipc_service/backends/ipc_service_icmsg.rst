.. _ipc_service_backend_icmsg:

ICMsg 后端 (ICMsg backend)
##########################

核间消息传递后端 (ICMsg) 是比重量级的 RPMsg 静态虚拟环后端更轻量的替代方案。它在小内存占用中提供了最小功能集。ICMsg 后端构建在 :ref:`spsc_pbuf` 之上。(The inter core messaging backend (ICMsg) is a lighter alternative to the heavier RPMsg static vrings backend. It offers a minimal feature set in a small memory footprint. The ICMsg backend is build on top of :ref:`spsc_pbuf`.)

概述 (Overview)
================

ICMsg 后端使用共享内存和 MBOX 设备来交换数据。共享内存用于存储数据,MBOX 设备用于发出数据已写入的信号。(The ICMsg backend uses shared memory and MBOX devices for exchanging data. Shared memory is used to store the data, MBOX devices are used to signal that the data has been written.)

后端支持在单个实例上注册单个端点。如果应用程序需要多个通信通道,则必须定义多个实例,每个实例都有自己的专用端点。(The backend supports the registration of a single endpoint on a single instance. If the application requires more than one communication channel, you must define multiple instances, each having its own dedicated endpoint.)

配置 (Configuration)
=====================

后端通过 Kconfig 和设备树进行配置。配置后端时,请执行以下操作:(The  backend is configured via Kconfig and devicetree. When configuring the backend, do the following:)

* 如果至少有一个核心在共享内存上使用数据缓存,请设置 ``dcache-alignment`` 值。对于通信双方,这必须是失效或写回大小的最大值。如果通信双方都没有在共享内存上使用数据缓存,则可以跳过它。(If at least one of the cores uses data cache on shared memory, set the ``dcache-alignment`` value. This must be the largest value of the invalidation or the write-back size for both sides of the communication. You can skip it if none of the communication sides is using data cache on shared memory.)
* 定义两个内存区域并将它们分配给实例的 ``tx-region`` 和 ``rx-region``。确保用于数据交换的内存区域是唯一的(不与任何其他区域重叠)并且可被两个域(或 CPU)访问。(Define two memory regions and assign them to ``tx-region`` and ``rx-region`` of an instance. Ensure that the memory regions used for data exchange are unique (not overlapping any other region) and accessible by both domains (or CPUs).)
* 定义 MBOX 设备,用于发送信号以通知其他域(或 CPU)数据已写入。确保其他域(或 CPU)能够接收信号。(Define MBOX devices which are used to send the signal that informs the other domain (or CPU) that data has been written. Ensure that the other domain (or CPU) is able to receive the signal.)

.. caution::

    确保您设置了正确的 ``dcache-alignment`` 值。最初,错误的值可能不会显示任何迹象,这可能会给人一种一切正常的错误印象。不稳定的行为迟早会出现。(Make sure that you set correct value of the ``dcache-alignment``. At first, wrong value may not show any signs, which may give a false impression that everything works. Unstable behavior will appear sooner or later.)

请参见以下实例的配置示例:(See the following configuration example for one of the instances:)

.. code-block:: devicetree

   reserved-memory {
      tx: memory@20070000 {
         reg = <0x20070000 0x0800>;
      };

      rx: memory@20078000 {
         reg = <0x20078000 0x0800>;
      };
   };

      ipc {
         ipc0: ipc0 {
            compatible = "zephyr,ipc-icmsg";
            dcache-alignment = <32>;
            tx-region = <&tx>;
            rx-region = <&rx>;
            mboxes = <&mbox 0>, <&mbox 1>;
            mbox-names = "tx", "rx";
            status = "okay";
         };
      };
   };


您必须为通信的另一侧(域或 CPU)提供类似的配置,但必须交换 MBOX 通道和内存区域(``tx-region`` 和 ``rx-region``)。(You must provide a similar configuration for the other side of the communication (domain or CPU) but you must swap the MBOX channels and  memory regions (``tx-region`` and ``rx-region``).)

绑定 (Bonding)
===============

当端点注册时,通过 IPC 实例连接的每个域(或 CPU)上都会发生以下情况:(When the endpoint is registered, the following happens on each domain (or CPU) connected through the IPC instance:)

1. 域(或 CPU)将一个魔数写入其共享内存的 ``tx-region``。(The domain (or CPU) writes a magic number to its ``tx-region`` of the shared memory.)
#. 然后,它向另一个域或 CPU 发送信号,通知数据已写入。向另一个域或 CPU 发送信号会重复超时。(It then sends a signal to the other domain or CPU, informing that the data has been written. Sending the signal to the other domain or CPU is repeated with timeout.)
#. 当收到来自另一个域或 CPU 的信号时,从 ``rx-region`` 读取魔数。如果正确,则绑定过程完成,后端通过调用 :c:member:`ipc_service_cb.bound` 回调通知应用程序。(When the signal from the other domain or CPU is received, the magic number is read from ``rx-region``. If it is correct, the bonding process is finished and the backend informs the application by calling :c:member:`ipc_service_cb.bound` callback.)

示例 (Samples)
==============

 - :zephyr:code-sample:`ipc-icmsg`

详细协议规范 (Detailed Protocol Specification)
================================================

ICMsg 使用两个共享内存区域和两个 MBOX 通道。区域和通道对用于在一个方向上传输消息。另一对是对称的,在相反方向上传输消息。因此,下面的规范侧重于一个这样的对。另一对是相同的。(The ICMsg uses two shared memory regions and two MBOX channels. The region and channel pair are used to transfer messages in one direction. The other pair is symmetric and transfers messages in the opposite direction. For this reason, the specification below focuses on one such pair. The other pair is identical.)

ICMsg 每个实例仅提供一个端点。(The ICMsg provides just one endpoint per instance.)

共享内存区域组织 (Shared Memory Region Organization)
------------------------------------------------------

如果启用了数据缓存,则提供给 ICMsg 的共享内存区域必须根据缓存要求进行对齐。如果未启用缓存,则所需的对齐方式为 4 字节。(If data caching is enabled, the shared memory region provided to ICMsg must be aligned according to the cache requirement. If cache is not enabled, the required alignment is 4 bytes.)

共享内存区域完全由单个 FIFO 使用。它包含读取和写入索引,后跟数据缓冲区。详细结构包含在下表中:(The shared memory region is entirely used by a single FIFO. It contains read and write indexes followed by the data buffer. The detailed structure is contained in the following table:)

.. list-table::
   :header-rows: 1

   * - 字段名称 (Field name)
     - 大小(字节) (Size (bytes))
     - 字节序 (Byte order)
     - 描述 (Description)
   * - ``rd_idx``
     - 4
     - 小端 (little‑endian)
     - ``data`` 字段中第一个传入字节的索引。(Index of the first incoming byte in the ``data`` field.)
   * - ``padding``
     - 取决于缓存对齐 (depends on cache alignment)
     - 不适用 (n/a)
     - 添加填充以将 ``wr_idx`` 对齐到缓存对齐方式。(Padding added to align ``wr_idx`` to the cache alignment.)
   * - ``wr_idx``
     - 4
     - 小端 (little‑endian)
     - ``data`` 字段中最后一个传入字节之后字节的索引。(Index of the byte after the last incoming byte in the ``data`` field.)
   * - ``data``
     - 到区域末尾的所有内容 (everything to the end of the region)
     - 不适用 (n/a)
     - 包含要传输的实际字节的循环缓冲区。(Circular buffer containing actual bytes to transfer.)

这是具有循环缓冲区的常规 FIFO:(This is usual FIFO with a circular buffer:)

* 当索引(``rd_idx`` 和 ``wr_idx``)到达 ``data`` 缓冲区的末尾时会回绕。(The Indexes (``rd_idx`` and ``wr_idx``) are wrapped around when they reach the end of the ``data`` buffer.)
* 如果 ``rd_idx == wr_idx``,则 FIFO 为空。(The FIFO is empty if ``rd_idx == wr_idx``.)
* FIFO 的容量比 ``data`` 缓冲区长度少一个字节。(The FIFO has one byte less capacity than the ``data`` buffer length.)

数据包 (Packets)
-----------------

数据包通过上一节中描述的 FIFO 发送。如果一个数据包出现在 FIFO 缓冲区的末尾,则可以回绕。(Packets are sent over the FIFO described in the above section. One packet can be wrapped around if it occurs at the end of the FIFO buffer.)

以下是数据包结构:(The following is the packet structure:)

.. list-table::
   :header-rows: 1

   * - 字段名称 (Field name)
     - 大小(字节) (Size (bytes))
     - 字节序 (Byte order)
     - 描述 (Description)
   * - ``len``
     - 2
     - 大端 (big‑endian)
     - ``data`` 字段的长度。(Length of the ``data`` field.)
   * - ``reserved``
     - 2
     - 不适用 (n/a)
     - 保留供将来使用。对于当前协议版本,它必须为 0。(Reserved for the future use. It must be 0 for the current protocol version.)
   * - ``data``
     - ``len``
     - 不适用 (n/a)
     - 数据包数据。(Packet data.)
   * - ``padding``
     - 0‑3
     - 不适用 (n/a)
     - 添加填充以将总数据包大小对齐到 4 字节。(Padding is added to align the total packet size to 4 bytes.)

数据包发送过程如下:(The packet send procedure is the following:)

#. 检查数据包是否适合缓冲区。(Check if the packet fits into the buffer.)
#. 从 ``wr_idx`` 开始将数据包写入 ``data`` FIFO 缓冲区。如果需要,将其回绕。(Write the packet to ``data`` FIFO buffer starting at ``wr_idx``. Wrap it if needed.)
#. 写入 ``wr_idx`` 的新值。(Write a new value of the ``wr_idx``.)
#. 通过 MBOX 通道通知接收器。(Notify the receiver over the MBOX channel.)

初始化 (Initialization)
------------------------

初始化序列如下:(The initialization sequence is the following:)

#. 将 ``wr_idx`` 和 ``rd_idx`` 设置为零。(Set the ``wr_idx`` and ``rd_idx`` to zero.)
#. 将单个数据包推送到包含魔数数据的 FIFO:``45 6d 31 6c 31 4b 30 72 6e 33 6c 69 34``。MBOX 尚未使用。(Push a single packet to FIFO containing magic data: ``45 6d 31 6c 31 4b 30 72 6e 33 6c 69 34``. The MBOX is not used yet.)
#. 初始化 MBOX。(Initialize the MBOX.)
#. 使用某个时间间隔(例如 1 毫秒)重复 MBOX 通道上的通知。(Repeat the notification over the MBOX channel using some interval, for example, 1 ms.)
#. 等待包含魔数数据的传入数据包。它将通过另一对(共享内存区域和 MBOX)到达。(Wait for an incoming packet containing the magic data. It will arrive over the other pair (shared memory region and MBOX).)
#. 停止重复 MBOX 通知。(Stop repeating the MBOX notification.)

之后,ICMsg 已绑定,可以传输数据包了。(After this, the ICMsg is bound, and it is ready to transfer packets.)

