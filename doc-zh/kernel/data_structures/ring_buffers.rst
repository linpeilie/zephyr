.. _ring_buffers_v2:

环形缓冲区
##########

:dfn:`环形缓冲区` 是一个循环缓冲区,其内容按先进先出顺序存储。

对于应用程序需要实现数据的异步"流式"复制的情况,Zephyr 提供了
``struct ring_buf`` 抽象来管理此类数据在共享内存缓冲区中的复制。

支持两种内容数据模式:

* **字节模式**:可以入队和出队原始字节。

* **数据项模式**:可以从环形缓冲区以最多 1020 字节的块入队和出队具有元数据的
  多个 32 位字数据项。每个数据项还有两个关联的元数据值:类型标识符和 16 位
  整数值,两者都是特定于应用程序的。

虽然底层数据结构相同,但在单个环形缓冲区实例上混合这两种模式是不合法的。
使用字节计数初始化的环形缓冲区必须仅与"字节"API 一起使用,使用字计数初始化
的环形缓冲区必须使用"项"调用。


.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的环形缓冲区(仅受可用 RAM 限制)。每个环形缓冲区由其内存
地址引用。

环形缓冲区具有以下关键属性:

* 字节或 32 位字的**数据缓冲区**。数据缓冲区包含已添加到环形缓冲区但尚未
  删除的原始字节或 32 位字。

* **数据缓冲区大小**,以字节或 32 位字为单位。这控制环形缓冲区可以容纳的
  最大数据量(包括可能的元数据值)。

环形缓冲区在使用之前必须初始化。这会将其数据缓冲区设置为空。

``struct ring_buf`` 可以放置在用户可访问内存中的任何位置,并且在使用之前
必须使用 :c:func:`ring_buf_init` 或 :c:func:`ring_buf_item_init` 初始化。
必须为其提供一个用户控制的内存区域用作缓冲区本身。请仔细注意,传递的缓冲区
大小的单位(字节或字)会根据以后如何使用环形缓冲区而改变。存在宏用于在单个
静态声明中组合这些步骤以方便使用。:c:macro:`RING_BUF_DECLARE` 将声明并
静态初始化具有指定字节计数的环形缓冲区,其中
:c:macro:`RING_BUF_ITEM_DECLARE` 将声明并静态初始化具有给定 32 位字计数的
缓冲区。:c:macro:`RING_BUF_ITEM_SIZEOF` 将计算对应于类型或表达式的 32 位字
的大小。注意:如果大小不是 32 位的倍数,则向上舍入。

可以使用 :c:func:`ring_buf_put` 将"字节"数据复制到环形缓冲区,传递数据指针
和字节计数。这些字节将按顺序复制到缓冲区中,尽可能多地适合分配的缓冲区。
将返回复制的总字节数(可能少于提供的)。同样,:c:func:`ring_buf_get` 将按照
写入顺序将字节从环形缓冲区复制到用户提供的缓冲区,返回传输的字节数。

为了避免多次复制数据的情况,字节模式存在"声明"API。
:c:func:`ring_buf_put_claim` 从用户获取字节大小值,并返回指向环形缓冲区
内部的内存的指针,该内存可用于接收这些字节,以及连续内部区域的大小(可能
小于请求的)。然后,用户可以稍后将数据复制到该区域,而无需首先在单个区域中
组装所有字节。完成后,可以使用 :c:func:`ring_buf_put_finish` 向缓冲区发出
传输完成的信号,传递实际传输的字节数。此时可以启动新的传输。类似地,
:c:func:`ring_buf_get_claim` 返回指向内部环形缓冲区数据的指针,用户可以从
中读取而无需进行逐字复制,并且 :c:func:`ring_buf_get_finish` 向缓冲区发出
已消耗多少字节的信号,并允许新传输开始。

"项"模式的工作方式与字节模式类似,只是所有传输都以 32 位字为单位,并且所有
内存都假定在 32 位边界上对齐。写入和读取操作是 :c:func:`ring_buf_item_put`
和 :c:func:`ring_buf_item_get`,并且与字节模式 API 的工作方式相同。没有为
项模式提供"声明"API。一个重要的区别是,与 :c:func:`ring_buf_put` 不同,
:c:func:`ring_buf_item_put` 不会执行部分传输;在提供的数据不能完全适合的
情况下,它将返回错误。

用户可以使用 :c:func:`ring_buf_space_get` 或
:c:func:`ring_buf_item_space_get` 管理环形缓冲区的容量而不修改它,它们
分别返回空闲字节数或空闲 32 位项字数,或通过测试
:c:func:`ring_buf_is_empty` 谓词。

最后,存在 :c:func:`ring_buf_reset` 调用以立即清空环形缓冲区,丢弃已写入
缓冲区的任何字节或项的跟踪。但是,它不会修改缓冲区本身的内存内容。


字节模式
========

使用 :c:macro:`RING_BUF_DECLARE()` 声明**字节模式**环形缓冲区实例,并使用:
:c:func:`ring_buf_put_claim`、:c:func:`ring_buf_put_finish`、
:c:func:`ring_buf_get_claim`、:c:func:`ring_buf_get_finish`、
:c:func:`ring_buf_put` 和 :c:func:`ring_buf_get` 访问。

数据可以复制到环形缓冲区(请参阅 :c:func:`ring_buf_put`)或用户可以直接使用
环形缓冲区内存。在后一种情况下,操作分为三个阶段:

1. 分配缓冲区(:c:func:`ring_buf_put_claim`),当用户请求可以写入数据的
   目标位置时。
#. 用户写入数据(例如,DMA 写入的缓冲区)。
#. 指示写入提供的缓冲区的数据量(:c:func:`ring_buf_put_finish`)。该量可以
   小于或等于分配的量。

可以通过复制(请参阅 :c:func:`ring_buf_get`)或按地址直接访问从环形缓冲区
检索数据。在后一种情况下,操作分为三个阶段:

1. 检索写入环形缓冲区的有效数据的源位置(请参阅
   :c:func:`ring_buf_get_claim`)。
#. 处理数据
#. 释放已处理的数据(请参阅 :c:func:`ring_buf_get_finish`)。释放的量可以
   小于或等于检索的量。

数据项模式
==========

使用 :c:macro:`RING_BUF_ITEM_DECLARE()` 声明**数据项模式**环形缓冲区实例,
并使用 :c:func:`ring_buf_item_put` 和 :c:func:`ring_buf_item_get` 访问。

环形缓冲区**数据项**是长度从 0 到 1020 字节的 32 位字数组。当数据项**入队**
(:c:func:`ring_buf_item_put`)时,其内容将与其关联的元数据值(占用一个额外的
32 位字)一起复制到数据缓冲区。如果环形缓冲区没有足够的空间来容纳新数据项,
则入队操作失败。

通过删除最旧的入队项,从环形缓冲区**出队**(:c:func:`ring_buf_item_get`)
数据项。出队数据项的内容以及其两个元数据值将复制到检索器提供的区域。如果
环形缓冲区为空,或者检索器提供的数据数组不足以容纳数据项的数据,则出队操作
失败。

并发
====

环形缓冲区 API 不提供任何并发控制。根据使用情况(特别是关于并发读取器/写入器
的数量),应用程序可能需要使用互斥锁保护环形缓冲区和/或使用信号量通知消费者
有数据可读。

对于一个生产者和一个消费者的简单情况,不需要并发控制。

内部操作
========

通过环形缓冲区流式传输的数据始终写入缓冲区内的下一个字节,在到达末尾后环绕
到第一个元素,因此是"环"结构。在内部,``struct ring_buf`` 包含其自己的缓冲区
指针及其大小,还包含一组"head"和"tail"索引,表示下一个读取和写入操作可能
发生的位置。

对于使用普通 put/get API 的用户来说,此边界是不可见的,但对于"声明"API
来说成为障碍,因为显然不能返回跨越缓冲区末尾的连续区域。这可能会让应用程序
代码感到惊讶,并且当传输需要在缓冲区末尾附近发生时会产生性能伪影,因为对
claim/finish 的调用次数需要加倍才能进行此类传输。


实现
****

定义环形缓冲区
==============

使用 :c:struct:`ring_buf` 类型的变量定义环形缓冲区。然后必须通过调用
:c:func:`ring_buf_init` 或 :c:func:`ring_buf_item_init` 对其进行初始化。

以下代码定义并初始化一个空的**数据项模式**环形缓冲区(它是较大数据结构的
一部分)。环形缓冲区的数据缓冲区能够容纳 64 字的数据和元数据信息。

.. code-block:: c

    #define MY_RING_BUF_WORDS 64

    struct my_struct {
        struct ring_buf rb;
        uint32_t buffer[MY_RING_BUF_WORDS];
        ...
    };
    struct my_struct ms;

    void init_my_struct {
        ring_buf_item_init(&ms.rb, MY_RING_BUF_WORDS, ms.buffer);
        ...
    }

或者,可以使用文件作用域的两个宏之一在编译时定义和初始化环形缓冲区。每个宏
都定义环形缓冲区本身及其数据缓冲区。

以下代码定义**数据项模式**环形缓冲区:

.. code-block:: c

    #define MY_RING_BUF_WORDS 93
    RING_BUF_ITEM_DECLARE(my_ring_buf, MY_RING_BUF_WORDS);

以下代码定义用于原始字节的环形缓冲区:

.. code-block:: c

    #define MY_RING_BUF_BYTES 93
    RING_BUF_DECLARE(my_ring_buf, MY_RING_BUF_BYTES);

入队数据
========

通过调用 :c:func:`ring_buf_put` 将字节复制到**字节模式**环形缓冲区。

.. code-block:: c

    uint8_t my_data[MY_RING_BUF_BYTES];
    uint32_t ret;

    ret = ring_buf_put(&ring_buf, my_data, MY_RING_BUF_BYTES);
    if (ret != MY_RING_BUF_BYTES) {
        /* 空间不足,部分复制。*/
	...
    }

可以通过直接访问环形缓冲区的内存将数据添加到**字节模式**环形缓冲区。例如:

.. code-block:: c

    uint32_t size;
    uint32_t rx_size;
    uint8_t *data;
    int err;

    /* 在环形缓冲区内存中分配缓冲区。*/
    size = ring_buf_put_claim(&ring_buf, &data, MY_RING_BUF_BYTES);

    /* 直接在环形缓冲区内存上工作。*/
    rx_size = uart_rx(data, size);

    /* 指示有效数据的量。rx_size 可以等于或小于 size。*/
    err = ring_buf_put_finish(&ring_buf, rx_size);
    if (err != 0) {
        /* 除非 rx_size > size,否则不应发生这种情况 */
	...
    }

通过调用 :c:func:`ring_buf_item_put` 将数据项添加到环形缓冲区。

.. code-block:: c

    uint32_t data[MY_DATA_WORDS];
    int ret;

    ret = ring_buf_item_put(&ring_buf, TYPE_FOO, 0, data, MY_DATA_WORDS);
    if (ret == -EMSGSIZE) {
        /* 数据项空间不足 */
	...
    }

如果数据项仅需要类型或特定于应用程序的整数值(即它没有数据数组),则可以
指定大小为 0 和数据指针为 :c:macro:`NULL`。

.. code-block:: c

    int ret;

    ret = ring_buf_item_put(&ring_buf, TYPE_BAR, 17, NULL, 0);
    if (ret == -EMSGSIZE) {
        /* 数据项空间不足 */
	...
    }

检索数据
========

通过调用 :c:func:`ring_buf_get` 从**字节模式**环形缓冲区复制出数据字节。
例如:

.. code-block:: c

    uint8_t my_data[MY_DATA_BYTES];
    size_t  ret;

    ret = ring_buf_get(&ring_buf, my_data, sizeof(my_data));
    if (ret != sizeof(my_data)) {
        /* 复制的字节较少。*/
    } else {
        /* 检索了请求的字节数。*/
        ...
    }

可以通过直接操作环形缓冲区的内存从**字节模式**环形缓冲区检索数据。例如:

.. code-block:: c

    uint32_t size;
    uint32_t proc_size;
    uint8_t *data;
    int err;

    /* 在环形缓冲区内存中获取缓冲区。*/
    size = ring_buf_get_claim(&ring_buf, &data, MY_RING_BUF_BYTES);

    /* 直接在环形缓冲区内存上工作。*/
    proc_size = process(data, size);

    /* 指示可以释放的数据量。proc_size 可以等于或小于 size。
     */
    err = ring_buf_get_finish(&ring_buf, proc_size);
    if (err != 0) {
        /* proc_size 超过环形缓冲区中有效数据的量。*/
	...
    }

通过调用 :c:func:`ring_buf_item_get` 从环形缓冲区中删除数据项。

.. code-block:: c

    uint32_t my_data[MY_DATA_WORDS];
    uint16_t my_type;
    uint8_t  my_value;
    uint8_t  my_size;
    int ret;

    my_size = MY_DATA_WORDS;
    ret = ring_buf_item_get(&ring_buf, &my_type, &my_value, my_data, &my_size);
    if (ret == -EMSGSIZE) {
        printk("缓冲区太小,需要 %d uint32_t\n", my_size);
    } else if (ret == -EAGAIN) {
        printk("环形缓冲区为空\n");
    } else {
        printk("获取类型 %u 值 %u 大小 %u dwords 的项\n",
               my_type, my_value, my_size);
        ...
    }

配置选项
********

相关配置选项:

* :kconfig:option:`CONFIG_RING_BUFFER`:启用环形缓冲区。

API 参考
********

以下环形缓冲区 API 由 :zephyr_file:`include/zephyr/sys/ring_buffer.h` 提供:

.. doxygengroup:: ring_buffer_apis
