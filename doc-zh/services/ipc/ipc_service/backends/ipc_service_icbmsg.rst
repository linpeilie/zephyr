.. _ipc_service_backend_icbmsg:

具有动态分配缓冲区的 ICMsg 后端 (ICMsg with dynamically allocated buffers backend)
###################################################################################

此后端构建在 :ref:`ipc_service_backend_icmsg` 之上。通过此后端传输的数据在共享内存上的动态分配缓冲区中传输。ICMsg 只发送对缓冲区的引用。它还支持多个端点。(This backend is built on top of the :ref:`ipc_service_backend_icmsg`. Data transferred over this backend travels in dynamically allocated buffers on shared memory. The ICMsg just sends references to the buffers. It also supports multiple endpoints.)

此架构允许克服其他后端的一些常见问题(主要与多线程访问和零拷贝有关)。此后端提供了一种没有显著限制的替代方案。(This architecture allows for overcoming some common problems with other backends (mostly related to multithread access and zero-copy). This backend provides an alternative with no significant limitations.)

概述 (Overview)
================

共享内存分为两部分。一部分保留给 ICMsg,另一部分包含大小相等的块。块的数量在设备树中配置。(The shared memory is divided into two parts. One is reserved for the ICMsg and the other contains equal-sized blocks. The number of blocks is configured in the devicetree.)

数据发送过程如下:(The data sending process is following:)

* 发送器分配一个或多个块。如果没有足够的连续块,它将使用参数中提供的超时等待,该参数还包括 K_FOREVER 和 K_NO_WAIT。(The sender allocates one or more blocks. If there are not enough sequential blocks, it waits using the timeout provided in the parameter that also includes K_FOREVER and K_NO_WAIT.)
* 分配的块填充数据。对于零拷贝情况,这由调用者完成,否则会自动复制。在此期间,只要有足够的空闲块,其他线程就不会以任何方式被阻塞。它们可以分配、发送数据和接收数据。(The allocated blocks are filled with data. For the zero-copy case, this is done by the caller, otherwise, it is copied automatically. During this time other threads are not blocked in any way as long as there are enough free blocks for them. They can allocate, send data and receive data.)
* 通过 ICMsg 向接收器发送包含块索引的消息。ICMsg 队列的大小足以容纳所有块的消息,因此永远不会溢出。(A message containing the block index is sent over ICMsg to the receiver. The size of the ICMsg queue is large enough to hold messages for all blocks, so it will never overflow.)
* 接收器可以根据需要保留数据。同样,只要有足够的空闲块,其他线程就不会被阻塞。(The receiver can hold the data as long as desired. Again, other threads are not blocked as long as there are enough free blocks for them.)
* 当不再需要数据时,后端通过 ICMsg 发送释放消息。(When data is no longer needed, the backend sends a release message over ICMsg.)
* 当后端收到此消息时,它会释放所有块。这由后端内部完成,对调用者是不可见的。(When the backend receives this message, it deallocates all blocks. It is done internally by the backend and it is invisible to the caller.)

配置 (Configuration)
=====================

后端通过 Kconfig 和设备树进行配置。配置后端时,请执行以下操作:(The backend is configured using Kconfig and devicetree. When configuring the backend, do the following:)

* 如果至少有一个核心在共享内存上使用数据缓存,请设置 ``dcache-alignment`` 值。对于通信双方,这必须是失效或写回大小的最大值。如果通信双方都没有在共享内存上使用数据缓存,则可以跳过它。(If at least one of the cores uses data cache on shared memory, set the ``dcache-alignment`` value. This must be the largest value of the invalidation or the write-back size for both sides of the communication. You can skip it if none of the communication sides is using data cache on shared memory.)
* 定义两个内存区域并将它们分配给实例的 ``tx-region`` 和 ``rx-region``。确保用于数据交换的内存区域是唯一的(不与任何其他区域重叠)并且可被两个域(或 CPU)访问。(Define two memory regions and assign them to ``tx-region`` and ``rx-region`` of an instance. Ensure that the memory regions used for data exchange are unique (not overlapping any other region) and accessible by both domains (or CPUs).)
* 使用 ``tx-blocks`` 和 ``rx-blocks`` 为每个区域定义可分配块的数量。(Define the number of allocable blocks for each region with ``tx-blocks`` and ``rx-blocks``.)
* 定义 MBOX 设备以发送信号,通知其他域(或 CPU)已写入数据。确保其他域(或 CPU)可以接收信号。(Define MBOX devices for sending a signal that informs the other domain (or CPU) of the written data. Ensure that the other domain (or CPU) can receive the signal.)

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
         compatible = "zephyr,ipc-icbmsg";
         dcache-alignment = <32>;
         tx-region = <&tx>;
         rx-region = <&rx>;
         tx-blocks = <16>;
         rx-blocks = <32>;
         mboxes = <&mbox 0>, <&mbox 1>;
         mbox-names = "tx", "rx";
         status = "okay";
      };
   };


您必须为通信的另一侧(域或 CPU)提供类似的配置。交换 MBOX 通道、内存区域(``tx-region`` 和 ``rx-region``)以及块计数(``tx-blocks`` 和 ``rx-blocks``)。(You must provide a similar configuration for the other side of the communication (domain or CPU). Swap the MBOX channels, memory regions (``tx-region`` and ``rx-region``), and block count (``tx-blocks`` and ``rx-blocks``).)

示例 (Samples)
===============

* :zephyr:code-sample:`ipc_multi_endpoint`

详细协议规范 (Detailed Protocol Specification)
================================================

ICBMsg 协议使用动态分配的共享内存块传输消息。在内部,它使用 ICMsg 进行控制消息。(The ICBMsg protocol transfers messages using dynamically allocated blocks of shared memory. Internally, it uses ICMsg for control messages.)

共享内存组织 (Shared Memory Organization)
------------------------------------------

ICBMsg 使用两个共享内存区域,``rx-region`` 用于接收消息,``tx-region`` 用于传输消息。这些区域不需要相邻、以任何特定顺序放置或大小相同。这些区域在每个核心上互换。(The ICBMsg uses two shared memory regions, ``rx-region`` for message receiving, and ``tx-region`` for message transmission. The regions do not need to be next to each other, placed in any specific order, or be of the same size. Those regions are interchanged on each core.)

每个共享内存区域分为以下两部分:(Each shared memory region is divided into following two parts:)

* **ICMsg 区域 (ICMsg area)** - ICMsg 实例保留并用于传输控制消息的区域。(An area reserved by ICMsg instance and used to transfer the control messages.)
* **块区域 (Blocks area)** - 包含承载消息内容的可分配块的区域。该区域被划分为对齐到缓存边界的大小相等的块。(An area containing allocatable blocks carrying the content of the messages. This area is divided into even-sized blocks aligned to cache boundaries.)

每个区域的位置经过计算以满足缓存边界要求并允许最佳区域使用。使用以下算法计算:(The location of each area is calculated to fulfill cache boundary requirements and allow optimal region usage. It is calculated using the following algorithm:)

输入:(Inputs:)

* ``region_begin``, ``region_end`` - 区域的边界。(Boundaries of the region.)
* ``local_blocks`` - 此区域中的块数。(Number of blocks in this region.)
* ``remote_blocks`` - 相反区域中的块数。(Number of blocks in the opposite region.)
* ``alignment`` - 内存缓存对齐方式。(Memory cache alignment.)

算法:(The algorithm:)

#. 将区域边界对齐到缓存:(Align region boundaries to cache:)

   * ``region_begin_aligned = ROUND_UP(region_begin, alignment)``
   * ``region_end_aligned = ROUND_DOWN(region_end, alignment)``
   * ``region_size_aligned = region_end_aligned - region_begin_aligned``

#. 计算 ICMsg 区域所需的最小大小 ``icmsg_min_size``,它是以下各项的总和:(Calculate the minimum size required for ICMsg area ``icmsg_min_size``, which is a sum of:)

   * ICMsg 头大小(请参阅 ICMsg 规范) (ICMsg header size (refer to the ICMsg specification))
   * 包含 4 字节内容的 ICMsg 消息大小(请参阅 ICMsg 规范)乘以 ``local_blocks + remote_blocks + 2`` (ICMsg message size for 4 bytes of content (refer to the ICMsg specification) multiplied by ``local_blocks + remote_blocks + 2``)

#. 计算块区域的可用大小。请注意,由于块对齐,实际大小可能会更小:(Calculate available size for block area. Note that the actual size may be smaller because of block alignment:)

   ``blocks_area_available_size = region_size_aligned - icmsg_min_size``

#. 计算单个块大小:(Calculate single block size:)

   ``block_size = ROUND_DOWN(blocks_area_available_size / local_blocks, alignment)``

#. 计算实际块区域大小:(Calculate actual block area size:)

   ``blocks_area_size = block_size * local_blocks``

#. 计算块区域起始地址:(Calculate block area start address:)

   ``blocks_area_begin = region_end_aligned - blocks_area_size``

结果:(The result:)

* ``region_begin_aligned`` - ICMsg 区域的起点。(The start of ICMsg area.)
* ``blocks_area_begin`` - ICMsg 区域的结束和块区域的起点。(End of ICMsg area and the start of block area.)
* ``block_size`` - 单个块大小。(Single block size.)
* ``region_end_aligned`` - 块区域的结束。(End of blocks area.)

.. image:: icbmsg_memory.svg
   :align: center

|

消息传输 (Message Transfer)
----------------------------

ICBMsg 使用以下两种类型的消息:(The ICBMsg uses following two types of messages:)

* **绑定消息 (Binding message)** - 在端点绑定过程中交换的消息(如下所述)。(Message exchanged during endpoint binding process (described below).)
* **数据消息 (Data message)** - 携带来自用户的实际数据的消息。(Message carrying actual data from a user.)

它们服务于不同的目的,但它们的生命周期和流程是相同的。以下步骤对此进行了描述:(They serve different purposes, but their lifetime and flow are the same. The following steps describe it:)

#. 发送器想要发送包含 ``K`` 字节的消息。(The sender wants to send a message that contains ``K`` bytes.)
#. 发送器从其 ``tx-region`` 块区域保留至少可以容纳 ``K + 4`` 字节的块。额外的 ``+ 4`` 字节保留给头部,其中包含消息的确切大小。块必须是连续的(一个接一个)。发送器负责块分配管理。如果没有可用的块,由实现决定要做什么。(The sender reserves blocks from his ``tx-region`` blocks area that can hold at least ``K + 4`` bytes. The additional ``+ 4`` bytes are reserved for the header, which contains the exact size of the message. The blocks must be continuous (one after another). The sender is responsible for block allocation management. It is up to the implementation to decide what to do if no blocks are available.)
#. 发送器用 32 位整数值 ``K``(小端)填充头部。(The sender fills the header with a 32-bit integer value, ``K`` (little-endian).)
#. 发送器用他的数据填充块的剩余部分。未使用的空间被忽略。(The sender fills the remaining part of the blocks with his data. Unused space is ignored.)
#. 发送器通过 ICMsg 发送 ``MSG_DATA`` 或 ``MSG_BOUND`` 控制消息,其中包含起始块号(头部所在位置)。有关控制消息的详细信息在下一节中。(The sender sends an ``MSG_DATA`` or ``MSG_BOUND`` control message over ICMsg that contains starting block number (where the header is located). Details about the control message are in the next section.)
#. 控制消息传输到接收器。(The control message travels to the receiver.)
#. 接收器从控制消息中收到的块号开始,从其 ``rx-region`` 读取消息大小和数据。(The receiver reads message size and data from his ``rx-region`` starting from the block number received in the control message.)
#. 接收器处理消息。(The receiver processes the message.)
#. 接收器通过 ICMsg 发送 ``MSG_RELEASE_DATA`` 或 ``MSG_RELEASE_BOUND`` 控制消息,其中包含起始块号(与接收到的控制消息中的相同)。(The receiver sends ``MSG_RELEASE_DATA`` or ``MSG_RELEASE_BOUND`` control message over ICMsg containing the starting block number (the same as inside received control message).)
#. 控制消息返回到发送器。(The control message travels back to the sender.)
#. 发送器从控制消息中提供的块号开始释放块。要释放的块数可以使用头部中的大小计算。(The sender releases the blocks starting from the block number provided in the control message. The number of blocks to release can be calculated using a size from the header.)

.. image:: icbmsg_message.svg
   :align: center

|

控制消息 (Control Messages)
----------------------------

控制消息通过 ICMsg 传输。每个控制消息包含三个字节。第一个字节告诉它是什么类型的消息。(The control messages are transmitted over ICMsg. Each control message contains three bytes. The first byte tells what kind of message it is.)

为 ICMsg 分配的大小确保最大可能数量的控制消息将适合其环形缓冲区,因此通过 ICMsg 发送永远不会因为缓冲区溢出而失败。(The allocated size for ICMsg ensures that the maximum possible number of control messages will fit into its ring buffer, so sending over the ICMsg will never fail because of buffer overflow.)

MSG_DATA
^^^^^^^^

.. list-table::
   :header-rows: 1

   * - 字节 0 (byte 0)
     - 字节 1 (byte 1)
     - 字节 2 (byte 2)
   * - MSG_DATA
     - 端点地址 (endpoint address)
     - 块号 (block number)
   * - 0x00
     - 0x00 ÷ 0xFD
     - 0x00 ÷ N-1

``MSG_DATA`` 控制消息指示发送了新的数据消息。数据消息以 ``block number`` 内的头部开始。数据消息通过 ``endpoint address`` 中指定的端点发送。在发送此控制消息之前,必须完成端点绑定过程。(The ``MSG_DATA`` control message indicates that a new data message was sent. The data message starts with a header inside ``block number``. The data message was sent over the endpoint specified in ``endpoint address``. The endpoint binding procedure must be finished before sending this control message.)

MSG_RELEASE_DATA
^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - 字节 0 (byte 0)
     - 字节 1 (byte 1)
     - 字节 2 (byte 2)
   * - MSG_RELEASE_DATA
     - 未使用 (unused)
     - 块号 (block number)
   * - 0x01
     -
     - 0x00 ÷ N-1

``MSG_RELEASE_DATA`` 控制消息作为对 ``MSG_DATA`` 的响应发送。它通知我们以 ``block number`` 开始的数据消息已被接收且不再需要。收到此控制消息时,必须释放包含该消息的块。(The ``MSG_RELEASE_DATA`` control message is sent in response to ``MSG_DATA``. It informs us that the data message starting with ``block number`` was received and is no longer needed. When this control message is received, the blocks containing the message must be released.)


MSG_BOUND
^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - 字节 0 (byte 0)
     - 字节 1 (byte 1)
     - 字节 2 (byte 2)
   * - MSG_BOUND
     - 端点地址 (endpoint address)
     - 块号 (block number)
   * - 0x02
     - 0x00 ÷ 0xFD
     - 0x00 ÷ N-1

``MSG_BOUND`` 控制消息类似于 ``MSG_DATA``,除了块携带绑定信息。有关绑定过程的详细信息,请参见下一节。(The ``MSG_BOUND`` control message is similar to the ``MSG_DATA`` except the blocks carry binding information. See the next section for details on the binding procedure.)

MSG_RELEASE_BOUND
^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - 字节 0 (byte 0)
     - 字节 1 (byte 1)
     - 字节 2 (byte 2)
   * - MSG_RELEASE_BOUND
     - 端点地址 (endpoint address)
     - 块号 (block number)
   * - 0x03
     - 0x00 ÷ 0xFD
     - 0x00 ÷ N-1

``MSG_RELEASE_BOUND`` 控制消息作为对 ``MSG_BOUND`` 的响应发送。它类似于 ``MSG_RELEASE_DATA``,除了需要 ``endpoint address``。有关绑定过程的详细信息,请参见下一节。(The ``MSG_RELEASE_BOUND`` control message is sent in response to ``MSG_BOUND``. It is similar to the ``MSG_RELEASE_DATA`` except the ``endpoint address`` is required. See the next section for details on the binding procedure.)

初始化 (Initialization)
------------------------

ICBMsg 初始化调用 ICMsg 进行初始化。完成后,不需要进一步初始化。块可以保持未初始化状态。(The ICBMsg initialization calls ICMsg to initialize. When it is done, no further initialization is required. Blocks can be left uninitialized.)

在 ICBMsg 初始化之后,您就可以进行端点绑定过程了。(After ICBMsg initialization, you are ready for the endpoint binding procedure.)

端点绑定 (Endpoint Binding)
----------------------------

到目前为止,协议是对称的。连接的每一侧都是相同的。绑定过程不是对称的。有以下两个角色:(So far, the protocol is symmetrical. Each side of the connection was the same. The binding process is not symmetrical. There are following two roles:)

* **发起者 (Initiator)** - 它分配端点地址并发送绑定消息。(It assigns endpoint addresses and sends binding messages.)
* **追随者 (Follower)** - 它等待绑定消息。(It waits for a binding message.)

角色根据 ``rx-region`` 和 ``tx-region`` 的地址确定。(The roles are determined based on the addresses of the ``rx-region`` and ``tx-region``.)

* 如果 ``address of rx-region < address of tx-region``,则它是发起者。(If ``address of rx-region < address of tx-region``, then it is initiator.)
* 如果 ``address of rx-region > address of tx-region``,则它是追随者。(If ``address of rx-region > address of tx-region``, then it is follower.)


绑定过程需要端点名称,并负责以下两件事:(The binding process needs an endpoint name and is responsible for following two things:)

* 建立公共端点地址, (To establish a common endpoint address,)
* 确保双方准备好通过该端点交换消息。(To make sure that two sides are ready to exchange messages over that endpoint.)

在 ICMsg 初始化之后,双方都可以开始端点绑定。双方开始端点绑定的顺序没有限制。(After ICMsg is initialized, both sides can start the endpoint binding. There are no restrictions on the order in which the sides start the endpoint binding.)

发起者绑定过程 (Initiator Binding Procedure)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

发起者发送绑定消息。它包含带有端点名称的单个以空字符结尾的字符串。与通常一样,它前面有一个包含消息大小(包括空终止符)的消息头。(The initiator sends a binding message. It contains a single null-terminated string with an endpoint name. As usual, it is preceded by a message header containing the message size (including null-terminator).)

``example`` 端点名称的绑定消息示例:(Example of the binding message for ``example`` endpoint name:)

.. list-table::
   :header-rows: 1

   * - 头部 (Header)
     - 端点名称 (Endpoint name)
     - 空终止符 (Null-terminator)
   * - 字节 0-3 (bytes 0-3)
     - 字节 4-10 (bytes 4-10)
     - 字节 11 (byte 11)
   * - 0x00000008
     - ``example``
     - 0x00

绑定消息使用 ``MSG_BOUND`` 控制消息发送,并使用 ``MSG_RELEASE_BOUND`` 控制消息释放。(The binding message is sent using the ``MSG_BOUND`` control message and released with the ``MSG_RELEASE_BOUND`` control message.)

从发起者的角度来看,端点绑定过程如下:(The endpoint binding procedure from the initiator's point of view is the following:)

#. 发起者为此端点分配端点地址。(The initiator assigns an endpoint address to this endpoint.)
#. 发起者发送包含端点名称和地址的绑定消息。(The initiator sends a binding message containing the endpoint name and address.)
#. 发起者等待来自追随者的使用此端点地址的任何消息。通常,它将是 ``MSG_RELEASE_BOUND``,但 ``MSG_DATA`` 也是允许的。(The initiator waits for any message from the follower using this endpoint address. Usually, it will be ``MSG_RELEASE_BOUND``, but ``MSG_DATA`` is also allowed.)
#. 发起者绑定到端点,它可以使用此端点发送数据消息。(The initiator is bound to an endpoint, and it can send data messages using this endpoint.)

追随者绑定过程 (Follower Binding Procedure)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

如果追随者在该端点上开始绑定过程之前收到绑定消息,则应将消息存储以供以后使用。它还不应发送 ``MSG_RELEASE_BOUND``。(If the follower receives a binding message before it starts the binding procedure on that endpoint, it should store the message for later. It should not send the ``MSG_RELEASE_BOUND`` yet.)

从追随者的角度来看,端点绑定过程如下:(The endpoint binding procedure from the follower's point of view is the following:)

#. 追随者等待包含其端点名称的绑定消息。该消息可能是新接收的消息或在绑定过程开始之前存储的消息。(The follower waits for a binding message containing its endpoint name. The message may be a newly received message or a message stored before the binding procedure started.)
#. 追随者存储发起者为此端点分配的端点地址。(The follower stores the endpoint address assigned to this endpoint by the initiator.)
#. 追随者发送 ``MSG_RELEASE_BOUND`` 控制消息。(The follower sends the ``MSG_RELEASE_BOUND`` control message.)
#. 追随者绑定到端点,它可以使用此端点发送数据消息。(The follower is bound to an endpoint, and it can send data messages using this endpoint.)

示例序列图 (Example sequence diagrams)
---------------------------------------

下图显示了一些消息如何在两端之间流动的示例。有两个端点的绑定和一个完全处理的数据消息交换。(The following diagram shows a few examples of how the messages flow between two ends. There is a binding of two endpoints and one fully processed data message exchange.)

.. image:: icbmsg_flows.svg
   :align: center

|

协议版本控制 (Protocol Versioning)
-----------------------------------

该协议允许在未来版本中进行改进。较新的实现应该能够以向后兼容模式与较旧的实现一起工作。为此,当前协议版本具有以下限制:(The protocol allows improvements in future versions. The newer implementations should be able to work with older ones in backward compatible mode. To allow it, the current protocol version has the following restrictions:)

* 如果接收器收到较长的控制消息,它应该只使用前三个字节并忽略其余字节。(If the receiver receives a longer control message, it should use only the first three bytes and ignore the remaining.)
* 如果接收器收到以不匹配此处描述的任何消息的字节开头的控制消息,它应该忽略它。(If the receiver receives a control message starting with a byte that does not match any of the messages described here, it should ignore it.)
* 如果接收器收到末尾有额外字节的绑定消息,它应该忽略额外的字节。(If the receiver receives a binding message with additional bytes at the end, it should ignore the additional bytes.)

