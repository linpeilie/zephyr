.. _net_buf_interface:

网络缓冲区 (Network Buffers)
#############################

.. contents::
    :local:
    :depth: 2


概述 (Overview)
****************

网络缓冲区是网络协议栈(以及蓝牙协议栈)如何传递数据的核心概念。它们的 API 在 :zephyr_file:`include/zephyr/net_buf.h`: 中定义。(Network buffers are a core concept of how the networking stack (as well as the Bluetooth stack) pass data around. The API for them is defined in :zephyr_file:`include/zephyr/net_buf.h`:.)

创建缓冲区 (Creating buffers)
******************************

网络缓冲区是通过首先定义一个缓冲区池来创建的:(Network buffers are created by first defining a pool of them:)

.. code-block:: c

   NET_BUF_POOL_DEFINE(pool_name, buf_count, buf_size, user_data_size, NULL);

该池是一个静态变量,因此如果需要将其导出到另一个模块,则需要一个单独的指针。(The pool is a static variable, so if it's needed to be exported to another module a separate pointer is needed.)

一旦定义了池,就可以从中分配缓冲区:(Once the pool has been defined, buffers can be allocated from it with:)

.. code-block:: c

   buf = net_buf_alloc(&pool_name, timeout);

池或其缓冲区没有显式的初始化函数,而是在调用 :c:func:`net_buf_alloc` 时隐式完成。(There is no explicit initialization function for the pool or its buffers, rather this is done implicitly as :c:func:`net_buf_alloc` gets called.)

如果需要在缓冲区中为稍后要添加的协议头保留空间,可以使用以下方法保留此头部空间:(If there is a need to reserve space in the buffer for protocol headers to be prepended later, it's possible to reserve this headroom with:)

.. code-block:: c

   net_buf_reserve(buf, headroom);

除了实际的协议数据和通用解析上下文之外,网络缓冲区还可能包含特定于协议的上下文,称为用户数据。缓冲区的最大数据和用户数据容量都是在声明缓冲区池时在编译时定义的。(In addition to actual protocol data and generic parsing context, network buffers may also contain protocol-specific context, known as user data. Both the maximum data and user data capacity of the buffers is compile-time defined when declaring the buffer pool.)

缓冲区原生支持通过 k_fifo 内核对象传递。使用 :c:func:`k_fifo_put` 和 :c:func:`k_fifo_get` 将缓冲区从一个线程传递到另一个线程。(The buffers have native support for being passed through k_fifo kernel objects. Use :c:func:`k_fifo_put` and :c:func:`k_fifo_get` to pass buffer from one thread to another.)

存在用于处理单链表中缓冲区的特殊函数,其中必须使用 :c:func:`net_buf_slist_put` 和 :c:func:`net_buf_slist_get` 函数,而不是 :c:func:`sys_slist_append` 和 :c:func:`sys_slist_get`。(Special functions exist for dealing with buffers in single linked lists, where the :c:func:`net_buf_slist_put` and :c:func:`net_buf_slist_get` functions must be used instead of :c:func:`sys_slist_append` and :c:func:`sys_slist_get`.)

存在用于处理单链表中缓冲区的特殊函数,其中必须使用 :c:func:`net_buf_slist_put` 和 :c:func:`net_buf_slist_get` 函数,而不是 :c:func:`sys_slist_append` 和 :c:func:`sys_slist_get`。(Special functions exist for dealing with buffers in single linked lists, where the :c:func:`net_buf_slist_put` and :c:func:`net_buf_slist_get` functions must be used instead of :c:func:`sys_slist_append` and :c:func:`sys_slist_get`.)

常见操作 (Common Operations)
*****************************

网络缓冲区 API 提供了一些有用的辅助函数,用于在缓冲区中编码和解码数据。要完全理解这些辅助函数,最好先理解与它们一起使用的基本操作名称:(The network buffer API provides some useful helpers for encoding and decoding data in the buffers. To fully understand these helpers it's good to understand the basic names of operations used with them:)

添加 (Add)
  将数据添加到缓冲区的末尾。修改数据长度值,同时保持实际数据指针不变。要求缓冲区中有足够的尾部空间。添加数据的 API 示例:(Add data to the end of the buffer. Modifies the data length value while leaving the actual data pointer intact. Requires that there is enough tailroom in the buffer. Some examples of APIs for adding data:)

  .. code-block:: c

     void *net_buf_add(struct net_buf *buf, size_t len);
     void *net_buf_add_mem(struct net_buf *buf, const void *mem, size_t len);
     uint8_t *net_buf_add_u8(struct net_buf *buf, uint8_t value);
     void net_buf_add_le16(struct net_buf *buf, uint16_t value);
     void net_buf_add_le32(struct net_buf *buf, uint32_t value);

移除 (Remove)
  从缓冲区的末尾移除数据。修改数据长度值,同时保持实际数据指针不变。移除数据的 API 示例:(Remove data from the end of the buffer. Modifies the data length value while leaving the actual data pointer intact. Some examples of APIs for removing data:)

  .. code-block:: c

     void *net_buf_remove_mem(struct net_buf *buf, size_t len);
     uint8_t net_buf_remove_u8(struct net_buf *buf);
     uint16_t net_buf_remove_le16(struct net_buf *buf);
     uint32_t net_buf_remove_le32(struct net_buf *buf);

压入 (Push)
  在缓冲区的开头前置数据。同时修改数据长度值和数据指针。要求缓冲区中有足够的头部空间。压入数据的 API 示例:(Prepend data to the beginning of the buffer. Modifies both the data length value as well as the data pointer. Requires that there is enough headroom in the buffer. Some examples of APIs for pushing data:)

  .. code-block:: c

     void *net_buf_push(struct net_buf *buf, size_t len);
     void *net_buf_push_mem(struct net_buf *buf, const void *mem, size_t len);
     void net_buf_push_u8(struct net_buf *buf, uint8_t value);
     void net_buf_push_le16(struct net_buf *buf, uint16_t value);

拉取 (Pull)
  从缓冲区的开头移除数据。同时修改数据长度值和数据指针。拉取数据的 API 示例:(Remove data from the beginning of the buffer. Modifies both the data length value as well as the data pointer. Some examples of APIs for pulling data:)

  .. code-block:: c

     void *net_buf_pull(struct net_buf *buf, size_t len);
     void *net_buf_pull_mem(struct net_buf *buf, size_t len);
     uint8_t net_buf_pull_u8(struct net_buf *buf);
     uint16_t net_buf_pull_le16(struct net_buf *buf);
     uint32_t net_buf_pull_le32(struct net_buf *buf);

添加(Add)和压入(Push)操作在将数据编码到缓冲区时使用,而移除(Remove)和拉取(Pull)操作在从缓冲区解码数据时使用。(The Add and Push operations are used when encoding data into the buffer, whereas the Remove and Pull operations are used when decoding data from a buffer.)

引用计数 (Reference Counting)
******************************

每个网络缓冲区都进行引用计数。缓冲区最初通过调用 :c:func:`net_buf_alloc()` 从空闲缓冲区池中获取,得到引用计数为 1 的缓冲区。引用计数可以使用 :c:func:`net_buf_ref()` 增加,或使用 :c:func:`net_buf_unref()` 减少。当计数降至零时,缓冲区会自动放回空闲缓冲区池。(Each network buffer is reference counted. The buffer is initially acquired from a free buffers pool by calling :c:func:`net_buf_alloc()`, resulting in a buffer with reference count 1. The reference count can be incremented with :c:func:`net_buf_ref()` or decremented with :c:func:`net_buf_unref()`. When the count drops to zero the buffer is automatically placed back to the free buffers pool.)


API 参考 (API Reference)
*************************

.. doxygengroup:: net_buf
