.. _slist_api:

单链表
======

Zephyr 提供了 :c:type:`sys_slist_t` 类型用于存储简单的单链表数据(即每个列表
元素存储指向下一个元素的指针,但不存储指向前一个元素的指针的数据)。这支持
对列表的第一个(头)和最后一个(尾)元素的常数时间访问,在头之前和尾之后插入列表
以及常数时间删除头。删除后续节点需要访问"前一个"指针,因此只能通过搜索列表
以线性时间执行。

:c:type:`sys_slist_t` 结构可以由用户在任何可访问的内存中实例化。在使用之前,
它应该使用 :c:func:`sys_slist_init` 初始化,或者通过 SYS_SLIST_STATIC_INIT
的静态赋值初始化。其内部字段是不透明的,用户代码不应访问。

可以使用 :c:func:`sys_slist_peek_head` 和 :c:func:`sys_slist_peek_tail`
检索列表的末端节点,如果列表为空,它们将返回 NULL,否则返回指向
:c:type:`sys_snode_t` 结构的指针。

:c:type:`sys_snode_t` 结构表示要插入的数据。通常,它预期由用户分配/控制,
通常嵌入在要添加到列表的结构中。可以使用 :c:macro:`SYS_SLIST_CONTAINER`
从列表节点检索容器结构指针,向其传递包含结构的结构名称和节点的字段名称。
在内部,:c:type:`sys_snode_t` 结构仅包含一个 next 指针,可以使用
:c:func:`sys_slist_peek_next` 访问。

可以通过使用 :c:func:`sys_slist_prepend` 和 :c:func:`sys_slist_append`
在头或尾添加单个节点来修改列表。它们还可以使用 :c:func:`sys_slist_insert`
将节点添加到内部点,该函数在现有节点之后插入新节点。类似地,
:c:func:`sys_slist_remove` 将在给定指向其前驱的指针的情况下删除节点。这些
操作都是常数时间。

存在用于对列表进行更复杂修改的便利例程。:c:func:`sys_slist_merge_slist`
将整个列表附加到现有列表。:c:func:`sys_slist_append_list` 将在常数时间内
附加现有列表的有界子集。并且 :c:func:`sys_slist_find_and_remove` 将(以线性
时间)搜索列表中的给定节点,并在存在时将其删除。

最后,slist 实现提供了一组"for each"宏,允许以自然方式迭代列表,而无需手动
遍历 next 指针。:c:macro:`SYS_SLIST_FOR_EACH_NODE` 将枚举列表中的每个节点,
给定一个本地变量来存储节点指针。:c:macro:`SYS_SLIST_FOR_EACH_NODE_SAFE`
的行为类似,但具有更复杂的实现,需要额外的临时变量进行存储,并允许用户在
迭代期间删除迭代的节点。这些宏中的每一个也存在"容器"变体
(:c:macro:`SYS_SLIST_FOR_EACH_CONTAINER` 和
:c:macro:`SYS_SLIST_FOR_EACH_CONTAINER_SAFE`),它们分配与用户容器结构类型
匹配的本地变量,而不是节点结构,在内部执行所需的偏移。并且
:c:macro:`SYS_SLIST_ITERATE_FROM_NODE` 存在以允许仅枚举节点及其所有后继,
而无需检查列表的早期部分。

单链表内部
----------

slist 代码被设计为最小和常规的。在内部,:c:type:`sys_slist_t` 结构只不过是
一对"head"和"tail"指针字段。并且 :c:type:`sys_snode_t` 仅存储单个"next"
指针。

.. figure:: slist.png
    :align: center
    :alt: slist 示例
    :figclass: align-center

    包含三个元素的 slist。

.. figure:: slist-empty.png
    :align: center
    :alt: 空 slist 示例
    :figclass: align-center

    空 slist

但是,列表代码的具体实现是使用内部"Z_GENLIST"模板 API 完成的,该 API 允许
从任意结构中提取这些字段,并发出任意命名的函数集。这允许使用相同的基本原语
实现更复杂的单链表变体。genlist 实现者负责仅对原语操作的自定义实现:每个
结构的"init"步骤,以及对其相关结构上的每个 head、tail 和 next 指针的"get"
和"set"原语。这些内联函数作为参数传递给 genlist 宏扩展。

目前,Zephyr 中仅存在一个此类变体,即 sflist。


标记列表
--------

:c:type:`sys_sflist_t` 使用所述的 genlist 模板 API 实现。除了符号命名
("sflist"而不是"slist")和下面描述的附加 API 之外,它在所有方面都与 slist
API 完全相同地运行。

它添加了将恰好两位用户定义的"标志"与每个列表节点关联的能力。这些可以使用
:c:func:`sys_sfnode_flags_get` 和 :c:func:`sys_sfnode_flags_set` 访问和
修改。在内部,标志与 next 指针的底部位联合存储,与更简单的 slist 代码相比,
不会产生 SRAM 存储开销。


单链表 API 参考
----------------

.. doxygengroup:: single-linked-list_apis

标记列表 API 参考
-----------------

.. doxygengroup:: flagged-single-linked-list_apis
