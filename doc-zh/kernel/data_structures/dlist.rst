.. _dlist_api:

双链表
======

在许多方面与单链表类似,Zephyr 包含双链表实现。这为所有现有 slist 操作提供
相同的算法行为,但还允许常数时间删除和插入(在所有点:头、尾或任何内部节点
之前或之后)。为此,列表为每个节点存储两个指针,因此具有稍高的运行时代码和
内存空间需求。

:c:type:`sys_dlist_t` 结构可以由用户在任何可访问的内存中实例化。在使用之前,
它必须使用 :c:func:`sys_dlist_init` 或 :c:macro:`SYS_DLIST_STATIC_INIT`
初始化。:c:type:`sys_dnode_t` 结构预期由用户为添加到列表的任何节点提供
(通常嵌入在要跟踪的结构中,如上所述)。在使用之前,它必须在清零/bss 内存中
初始化或使用 :c:func:`sys_dnode_init` 初始化。

原语操作可以使用 :c:func:`sys_dlist_peek_head`、
:c:func:`sys_dlist_peek_tail`、:c:func:`sys_dlist_peek_next` 和
:c:func:`sys_dlist_peek_prev` 检索列表的 head/tail 以及节点的 next/prev
指针。在适当的情况下(即对于空列表,或列表端点的节点),这些都可以返回 NULL。

可以通过使用 :c:func:`sys_dlist_remove` 删除节点,使用
:c:func:`sys_dlist_prepend` 和 :c:func:`sys_dlist_append` 将节点添加到列表
的头或尾,或使用 :c:func:`sys_dlist_insert` 在现有节点之前插入节点,以常数
时间修改 dlist。

与 slist 一样,可以使用 :c:macro:`SYS_DLIST_FOR_EACH_NODE` 以自然代码块
样式处理 dlist 中的每个节点。此宏还以"FROM_NODE"形式存在,允许从已知起点
进行迭代,允许在代码块中删除正在检查的节点的"SAFE"变体,提供指向包含结构
而不是原始节点的指针的"CONTAINER"样式,以及提供两种属性的"CONTAINER_SAFE"
变体。

dlist 提供的便利实用程序包括 :c:func:`sys_dlist_insert_at`,它插入一个节点,
该节点线性搜索列表以找到正确的插入点,该插入点由用户作为 C 回调函数指针
提供,以及 :c:func:`sys_dnode_is_linked`,它将肯定返回节点当前是否链接到
dlist 中(通过与正常列表处理相比开销为零的实现)。

双链表内部
----------

在内部,dlist 实现是最小的::c:type:`sys_dlist_t` 结构包含"head"和"tail"
指针字段,:c:type:`sys_dnode_t` 包含"prev"和"next"指针,并且不存储其他数据。
但实际上,这两个结构在内部是相同的,并且列表结构作为节点插入到列表本身中。
这允许操作的非常干净的对称性:

* 空列表在列表结构中具有指向自身的反向指针,这可以简单地检测到。

* 可以通过将节点的 prev/next 指针与列表结构地址进行比较来检测列表的头和尾。

* 插入或删除永远不需要检查在头或尾插入的特殊情况。列表中永远没有任何 NULL
  指针需要避免。对于所有列表修改原语,运行完全相同的操作,而无需测试或分支。

实际上,N 个节点的 dlist 可以被认为是"N+1"个节点的"环",其中一个节点表示列表
跟踪结构。

.. figure:: dlist.png
    :align: center
    :alt: dlist 示例
    :figclass: align-center

    包含三个元素的 dlist。请注意,列表结构在列表中显示为第四个"元素"。

.. figure:: dlist-single.png
    :align: center
    :alt: 单元素 dlist 示例
    :figclass: align-center

    仅包含一个元素的 dlist。

.. figure:: dlist-empty.png
    :align: center
    :alt: dlist 示例
    :figclass: align-center

    空 dlist。


双链表 API 参考
----------------

.. doxygengroup:: doubly-linked-list_apis
