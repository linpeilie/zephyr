.. _slist_api:

单链表 (Single-linked List)
============================

Zephyr 提供了一个 :c:type:`sys_slist_t` 类型来存储简单的单链表数据
（即每个列表元素存储指向下一个元素的指针，但不存储指向前一个元素的指针的数据）。
这支持对列表的第一个（头）和最后一个（尾）元素的常数时间访问，在头之前和尾之后插入，
以及头的常数时间删除。后续节点的删除需要访问"前一个"指针，
因此只能通过搜索列表在线性时间内执行。

:c:type:`sys_slist_t` 结构可以由用户在任何可访问的内存中实例化。
在使用之前，应使用 :c:func:`sys_slist_init` 或通过从 SYS_SLIST_STATIC_INIT
静态赋值进行初始化。其内部字段是不透明的，不应由用户代码访问。

列表的末端节点可以使用 :c:func:`sys_slist_peek_head` 和 :c:func:`sys_slist_peek_tail`
检索，如果列表为空，则返回 NULL，否则返回指向 :c:type:`sys_snode_t` 结构的指针。

:c:type:`sys_snode_t` 结构表示要插入的数据。通常，它预期由用户分配/控制，
通常嵌入在要添加到列表中的结构中。可以使用 :c:macro:`SYS_SLIST_CONTAINER`
从列表节点检索容器结构指针，传递包含结构的结构名称和节点的字段名称。
在内部，:c:type:`sys_snode_t` 结构仅包含一个 next 指针，
可以使用 :c:func:`sys_slist_peek_next` 访问。

可以通过使用 :c:func:`sys_slist_prepend` 和 :c:func:`sys_slist_append`
在头或尾添加单个节点来修改列表。它们还可以使用 :c:func:`sys_slist_insert`
在内部点添加节点，该函数在现有节点之后插入新节点。
类似地，:c:func:`sys_slist_remove` 将删除给定指向其前驱的指针的节点。
这些操作都是常数时间。

存在用于对列表进行更复杂修改的便利例程。:c:func:`sys_slist_merge_slist`
将整个列表附加到现有列表。:c:func:`sys_slist_append_list` 将在常数时间内附加现有列表的有界子集。
:c:func:`sys_slist_find_and_remove` 将搜索列表（在线性时间内）查找给定节点并在存在时删除它。

最后，slist 实现提供了一组"for each"宏，允许以自然方式迭代列表，
而无需手动遍历 next 指针。:c:macro:`SYS_SLIST_FOR_EACH_NODE`
将枚举列表中的每个节点，给定一个本地变量来存储节点指针。
:c:macro:`SYS_SLIST_FOR_EACH_NODE_SAFE` 的行为类似，
但具有更复杂的实现，需要额外的临时变量用于存储，
并允许用户在迭代期间删除迭代的节点。每个这些宏还存在一个"container"变体
（:c:macro:`SYS_SLIST_FOR_EACH_CONTAINER` 和 :c:macro:`SYS_SLIST_FOR_EACH_CONTAINER_SAFE`），
它分配一个与用户的容器结构匹配的类型的本地变量，而不是节点结构，
在内部执行所需的偏移。:c:macro:`SYS_SLIST_ITERATE_FROM_NODE`
允许仅枚举一个节点及其所有后继节点，而无需检查列表的早期部分。

单链表内部 (Single-linked List Internals)
-------------------------------------------

slist 代码旨在最小化和传统化。在内部，:c:type:`sys_slist_t` 结构只不过是一对"head"和"tail"指针字段。
:c:type:`sys_snode_t` 仅存储单个"next"指针。

.. figure:: slist.png
    :align: center
    :alt: slist 示例
    :figclass: align-center

    包含三个元素的 slist。

.. figure:: slist-empty.png
    :align: center
    :alt: 空 slist 示例
    :figclass: align-center

    空的 slist

但是，列表代码的具体实现是使用内部"Z_GENLIST"模板 API 完成的，
该 API 允许从任意结构中提取这些字段并发出任意命名的函数集。
这允许使用相同的基本原语实现更复杂的单链表变体。
genlist 实现者仅负责原语操作的自定义实现：每个结构的"init"步骤，
以及每个 head、tail 和 next 指针在其相关结构上的"get"和"set"原语。
这些内联函数作为参数传递给 genlist 宏展开。

目前 Zephyr 中只存在一个这样的变体，即 sflist。


标志列表 (Flagged List)
------------------------

:c:type:`sys_sflist_t` 使用所描述的 genlist 模板 API 实现。
除了符号命名（"sflist"而不是"slist"）和接下来描述的附加 API 之外，
它在所有方面都与 slist API 相同。

它添加了将正好两位用户定义的"标志"与每个列表节点关联的能力。
这些可以使用 :c:func:`sys_sfnode_flags_get` 和 :c:func:`sys_sfnode_flags_set` 访问和修改。
在内部，标志与 next 指针的底部位联合存储，与较简单的 slist 代码相比，
不会产生 SRAM 存储开销。


单链表 API 参考 (Single-linked List API Reference)
----------------------------------------------------

.. doxygengroup:: single-linked-list_apis

标志列表 API 参考 (Flagged List API Reference)
-----------------------------------------------

.. doxygengroup:: flagged-single-linked-list_apis
