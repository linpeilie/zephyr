.. _bluetooth_mesh_access:

接入层
######

接入层是应用程序与蓝牙网状网络的接口。
接入层提供了将节点行为划分为元素和模型的机制，
这些由应用程序实现。

网状模型
********

网状节点的功能由模型表示。模型实现节点支持的单一行为，
如灯、传感器或恒温器。网状模型被分组为*元素*。每个元素
被分配自己的单播地址，并且每种类型的模型只能包含一个。
通常，每个元素代表网状节点行为的单个方面。例如，包含一个传感器、
两个灯和一个电源插座的节点将把此功能分布在四个元素上，每个元素
实例化支持行为的单个方面所需的所有模型。

节点的元素和模型结构在节点组成数据中指定，
在初始化期间传递给 :c:func:`bt_mesh_init`。蓝牙 SIG 定义了一组基础模型（参见
:ref:`bluetooth_mesh_models`）和一组用于在 `蓝牙网状模型规范
<https://www.bluetooth.com/specifications/mesh-specifications/>`_ 中实现常见行为的模型。所有未由
蓝牙 SIG 指定的模型都是供应商模型，必须绑定到公司 ID。

网状模型有几个参数可以通过网状堆栈的初始化或通过
:ref:`bluetooth_mesh_models_cfg_srv` 进行配置：

操作码列表
==========

操作码列表包含模型可以接收的所有消息操作码，以及
最小可接受的有效载荷长度和传递给它们的回调。模型
可以支持任意数量的操作码，但每个操作码在每个元素中只能由一个
模型列出。

完整的操作码列表必须传递给组合数据中模型结构中的模型，
并且不能在运行时更改。操作码列表的结尾由特殊的 :c:macro:`BT_MESH_MODEL_OP_END` 条目确定。此条目
必须始终存在于操作码列表中，除非列表为空。在那种情况下，应使用 :c:macro:`BT_MESH_MODEL_NO_OPS` 来替代
操作码列表定义。

AppKey 列表
===========

AppKey 列表包含模型可以接收消息的所有应用密钥。只有使用 AppKey 列表中
应用密钥加密的消息才会传递给模型。

每个模型可以持有的最大支持应用密钥数量通过 :kconfig:option:`CONFIG_BT_MESH_MODEL_KEY_COUNT` 配置
选项进行配置。AppKey 列表的内容由
:ref:`bluetooth_mesh_models_cfg_srv` 管理。

订阅列表
========

模型将处理寻址到其元素单播地址的所有消息（假设使用的应用密钥
存在于 AppKey 列表中）。此外，模型将处理寻址到其订阅列表中任何组或
虚拟地址的数据包。这允许节点通过单个消息寻址
整个网状网络中的多个节点。

每个模型可以持有的订阅列表中支持的最大地址数量通过 :kconfig:option:`CONFIG_BT_MESH_MODEL_GROUP_COUNT`
配置选项进行配置。订阅列表的内容由
:ref:`bluetooth_mesh_models_cfg_srv` 管理。

模型发布
========

模型可以通过两种方式发送消息：

* 通过在 :c:struct:`bt_mesh_msg_ctx` 中指定一组消息参数，
  并调用 :c:func:`bt_mesh_model_send`。
* 通过设置 :c:struct:`bt_mesh_model_pub` 结构并调用
  :c:func:`bt_mesh_model_publish`。

当使用 :c:func:`bt_mesh_model_publish` 发布消息时，模型
将使用由 :ref:`bluetooth_mesh_models_cfg_srv` 配置的发布参数。这是发送
无提示模型消息的推荐方式，因为它将选择
消息参数的责任传递给网络管理员，网络管理员可能比单个节点
更了解网状网络。

为了支持使用发布参数进行发布，模型必须为发布分配
数据包缓冲区，并将其传递给
:c:member:`bt_mesh_model_pub.msg`。配置服务器还可以为发布消息设置周期
发布。为了支持这一点，模型必须填充 :c:member:`bt_mesh_model_pub.update` 回调。在
消息发布之前会调用 :c:member:`bt_mesh_model_pub.update` 回调，允许模型更改有效载荷以反映其
当前状态。

通过将 :c:member:`bt_mesh_model_pub.retr_update` 设置为 1，模型可以
配置 :c:member:`bt_mesh_model_pub.update` 回调在每次重传时触发。例如，这可以由使用
延迟参数的模型使用，每次重传可以调整该参数。
:c:func:`bt_mesh_model_pub_is_retransmission` 函数可以
用于区分首次发布和重传。
:c:macro:`BT_MESH_PUB_MSG_TOTAL` 和 :c:macro:`BT_MESH_PUB_MSG_NUM` 宏
可以用于返回总传输数和一次发布间隔内的重传
数。

扩展模型
========

蓝牙网状规范允许网状模型相互扩展。
当一个模型扩展另一个模型时，它继承该模型的功能，扩展
可以用于从简单模型构建复杂模型，
利用现有模型功能来避免定义新操作码。
模型可以扩展来自任何元素的任意数量的模型。当一个模型
在同一个元素中扩展另一个模型时，两个模型将共享订阅
列表。网状堆栈通过将两个模型的订阅列表
合并为一个来实现这一点，结合模型总共可以拥有的
订阅数量。模型可以扩展扩展其他模型的模型，创建"扩展
树"。扩展树中的所有模型在每个
元素上共享一个订阅列表。

模型扩展通过在初始化期间调用 :c:func:`bt_mesh_model_extend` 来完成。一个模型只能被另一个模型扩展，
扩展不能是循环的。请注意，节点状态的绑定和模型之间的其他
关系必须由模型实现定义。

模型扩展概念在接入层数据包处理中增加了一些开销，必须通过
:kconfig:option:`CONFIG_BT_MESH_MODEL_EXTENSIONS` 显式启用才能生效。

模型数据存储
============

网状模型可能与每个需要持久存储的模型实例相关联的数据。访问 API 提供了一种存储此
数据的机制，利用内部模型实例编码方案。模型可以通过调用
:c:func:`bt_mesh_model_data_store` 为每个实例存储一个用户定义的数据条目。为了能够在
设备下次重启时读出数据，模型的
:c:member:`bt_mesh_model_cb.settings_set` 回调必须被填充。在持久存储中找到模型特定数据时，将调用此
回调。模型可以通过调用作为
回调参数传递的 ``read_cb`` 来检索数据。详细信息请参见 :ref:`settings_api` 模块文档。

当模型数据频繁更改时，每次更改都存储可能会导致
闪存磨损增加。为了减少磨损，模型可以通过调用 :c:func:`bt_mesh_model_data_store_schedule` 来推迟存储
数据。堆栈将调度一个延迟由
:kconfig:option:`CONFIG_BT_MESH_STORE_TIMEOUT` 选项定义的工作项。当工作项
运行时，堆栈将为每个请求存储数据的模型调用 :c:member:`bt_mesh_model_cb.pending_store`
回调。然后模型可以调用 :c:func:`bt_mesh_model_data_store` 来存储数据。

如果启用了 :kconfig:option:`CONFIG_BT_MESH_SETTINGS_WORKQ`，则
:c:member:`bt_mesh_model_cb.pending_store` 回调从专用
线程调用。这允许堆栈在存储模型数据的同时处理其他传入和传出消息。建议在需要存储大量数据时使用此选项和
:c:func:`bt_mesh_model_data_store_schedule` 函数。

组合数据
========

组合数据提供有关网状设备的信息。
设备的组合数据包含有关设备上元素、
支持模型和其他特征的信息。组合
数据被拆分为不同的页面，每个页面包含有关设备的特定特征
信息。为了访问此信息，用户可以使用 :ref:`bluetooth_mesh_models_cfg_srv` 模型，如果支持，
或者使用 :ref:`bluetooth_mesh_lcd_srv` 模型。

组合数据页面 0
---------------

组合数据页面 0 提供有关设备的基本信息，对于所有网状设备都是必需的。它包含元素和模型组成、
支持的功能和制造商信息。

组合数据页面 1
---------------

组合数据页面 1 提供有关模型之间关系的信息，对于所有网状设备都是必需的。一个模型可以扩展和/或对应一个
或多个模型。模型可以通过调用 :c:func:`bt_mesh_model_extend` 扩展另一个模型，
或者通过调用 :c:func:`bt_mesh_model_correspond` 对应另一个模型。
:kconfig:option:`CONFIG_BT_MESH_MODEL_EXTENSION_LIST_SIZE` 指定在设备上组合中可以存储多少模型
关系，此数字应反映 :c:func:`bt_mesh_model_extend` 和 :c:func:`bt_mesh_model_correspond` 调用的数量。

组合数据页面 2
---------------

组合数据页面 2 为支持的网状配置文件提供信息。网状配置文件规范定义了希望支持特定
蓝牙 SIG 定义配置文件的设备的产品要求。当前支持的配置文件可以在
3.12 章节中的 `蓝牙 SIG 分配编号
<https://www.bluetooth.com/specifications/assigned-numbers/uri-scheme-name-string-mapping/>`_ 中找到。
组合数据页面 2 仅对于声明支持一个或多个
网状配置文件的设备才是必需的。

组合数据页面 128、129 和 130
---------------------------------------

组合数据页面 128、129 和 130 分别镜像组合数据页面 0、1 和 2。它们用于表示镜像页面在固件更新后组合数据
更改时的新内容。详细信息请参见 :ref:`bluetooth_mesh_dfu_srv_comp_data_and_models_metadata`。

可延迟消息
==========

可延迟消息功能通过 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_ACCESS_DELAYABLE_MSG` 启用。
这是一个可选功能，实现了规范对模型响应接收消息而传输的消息（也称为
响应消息）的建议。

响应消息应通过以下随机延迟发送：

* 如果接收到的消息发送到单播地址，则在 20 到 50 毫秒之间
* 如果接收到的消息发送到组或虚拟地址，则在 20 到 500 毫秒之间

如果设置了 :c:member:`bt_mesh_msg_ctx.rnd_delay`
标志，则触发可延迟消息功能。
可延迟消息功能将消息存储在本地内存中，同时它们在等待随机延迟到期。

如果传输层在随机延迟到期时没有足够的内存来发送消息，则消息将推迟另外 10 毫秒。
如果传输层由于任何其他原因无法发送消息，可延迟消息
功能会使用传输层错误码触发 :c:member:`bt_mesh_send_cb.start` 回调。

如果可延迟消息功能找不到足够的空闲内存来存储传入
消息，它将发送延迟接近到期以释放内存的消息。

当网状堆栈挂起或重置时，尚未发送的消息将被移除并
使用错误码触发 :c:member:`bt_mesh_send_cb.start` 回调。

.. note::
   当模型连续发送几条消息时，消息可能不会按照传递给接入层的顺序发送。这是因为某些消息可能比其他消息延迟更长时间。

   当同一模型生成的一组消息需要按特定顺序发送时，通过将 :c:member:`bt_mesh_msg_ctx.rnd_delay` 设置为 ``false`` 来禁用随机化。

可延迟发布
==========

可延迟发布功能在以下情况下实现了规范对消息
发布延迟的建议：

* 在 20 到 500 毫秒之间，当蓝牙网状堆栈启动或当发布由 :c:func:`bt_mesh_model_publish` 函数触发时
* 对于周期性发布的消息，在 20 到 50 毫秒之间

此功能是可选的，并通过 :kconfig:option:`CONFIG_BT_MESH_DELAYABLE_PUBLICATION` Kconfig 选项启用。启用后，每个模型可以通过相应地将 :c:member:`bt_mesh_model_pub.delayable` 位字段设置为 ``1`` 或 ``0`` 来启用或禁用可延迟发布。此位字段可以随时更改。

API 参考
********

.. doxygengroup:: bt_mesh_access
