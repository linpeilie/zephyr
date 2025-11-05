.. _bluetooth_mesh_core:

核心
####

核心提供用于管理一般蓝牙网状网络状态的功能。

.. _bluetooth_mesh_lpn:

低功耗节点
**************

低功耗节点 (LPN) 角色允许电池供电设备作为叶节点参与
网状网络。LPN 通过好友节点与网状网络交互，好友节点负责中继指向
LPN 的任何消息。LPN 通过保持无线电关闭来节省功耗，只在
发送消息或轮询好友节点是否有传入消息时唤醒。

无线电控制和轮询由网状堆栈自动管理，但
LPN API 允许应用程序通过
:c:func:`bt_mesh_lpn_poll` 在任何时间触发轮询。LPN 操作参数，包括轮询
间隔、轮询事件时序和好友要求，通过
:kconfig:option:`CONFIG_BT_MESH_LOW_POWER` 选项和相关配置选项进行控制。

当将 LPN 功能与日志一起使用时，强烈建议仅使用
:kconfig:option:`CONFIG_LOG_MODE_DEFERRED` 选项。除延迟模式外的日志模式可能会在处理日志消息期间导致意外延迟。这反过来会影响接收延迟和接收窗口的调度。:kconfig:option:`CONFIG_BT_MESH_FRIEND` 选项也存在相同的限制。

重放保护列表
**********************

重放保护列表 (RPL) 用于保存网状网络中元素最近接收的序列号，以执行针对重放攻击的保护。

为了在重启后使节点免受重放攻击，它需要在断电之前将整个 RPL 存储在持久存储中。根据网状网络中流量的大小，存储最近看到的序列号可能会使闪存磨损更早或更晚。为了缓解这种情况，
可以使用 :kconfig:option:`CONFIG_BT_MESH_RPL_STORE_TIMEOUT`。此选项推迟在持久存储中存储 RPL 条目。

但是，此选项并不能完全解决问题，因为节点可能在存储 RPL 的定时器触发之前断电。为了确保消息不能被重放，节点可以通过调用 :c:func:`bt_mesh_rpl_pending_store` 在任何时间（或在断电前足够时间）启动挂起 RPL 条目的存储。在这种情况下由节点决定要存储哪些 RPL 条目。

将 :kconfig:option:`CONFIG_BT_MESH_RPL_STORE_TIMEOUT` 设置为 -1 可以完全关闭定时器，这有助于显著减少闪存磨损。
这将存储 RPL 的责任转移到用户应用程序，并要求在此 API
被调用直到所有 RPL 条目写入闪存期间有足够的电源备份。

在 :kconfig:option:`CONFIG_BT_MESH_RPL_STORE_TIMEOUT` 和调用 :c:func:`bt_mesh_rpl_pending_store` 之间找到适当的平衡可以降低安全漏洞和闪存磨损的风险。

.. warning:

   如果未启用 :kconfig:option:`CONFIG_BT_SETTINGS`，或设置
   :kconfig:option:`CONFIG_BT_MESH_RPL_STORE_TIMEOUT` 为 -1 且未在重启之间存储
   RPL，将使设备容易受到重放攻击，且不执行规范要求的重放保护。

.. _bluetooth_mesh_persistent_storage:

持久存储
******************

网状堆栈使用 :ref:`设置子系统 <settings_api>` 来持久存储设备配置。当堆栈配置更改且需要持久存储更改时，堆栈会调度一个工作项。调度工作项和将其提交到工作队列之间的延迟由 :kconfig:option:`CONFIG_BT_MESH_STORE_TIMEOUT` 选项定义。一旦
存储数据被调度，在工作项被处理之前不能重新调度。在某些情况下会有例外，如下所述。

当必须存储 IV 索引、序列号或 CDB 配置时，工作项立即提交到工作队列。如果之前已调度工作项，将立即重新调度。

重放保护列表使用相同的工作项来存储 RPL 条目。如果请求存储 RPL 条目且没有其他配置挂起存储，延迟设置为 :kconfig:option:`CONFIG_BT_MESH_RPL_STORE_TIMEOUT`。
如果要存储其他堆栈配置，则 :kconfig:option:`CONFIG_BT_MESH_STORE_TIMEOUT` 选项定义的延迟小于
:kconfig:option:`CONFIG_BT_MESH_RPL_STORE_TIMEOUT`，且工作项由重放保护列表调度，则工作项将被重新调度。

当工作项运行时，堆栈将存储所有挂起的配置，包括 RPL 条目。

工作项执行上下文
===========================

:kconfig:option:`CONFIG_BT_MESH_SETTINGS_WORKQ` 选项配置执行工作项的上下文。此选项默认启用，
导致堆栈使用专用协作线程来处理工作项。这允许堆栈在存储堆栈配置的同时处理其他传入和传出消息，以及提交到系统工作队列的其他工作项。

当禁用此选项时，工作项被提交到系统工作队列。
这意味着系统工作队列在存储堆栈配置所需的时间内被阻塞。不建议禁用此选项，因为这会使设备在相当长的时间内无响应。

.. _bluetooth_mesh_adv_identity:

广告身份
**********************

所有网状堆栈承载者都使用 :c:macro:`BT_ID_DEFAULT` 本地身份广告数据。
该值在网状堆栈实现中预设。当蓝牙® 低功耗 (LE) 和蓝牙网状网络在同设备上共存时，应用程序应在开始通信之前分配和配置另一个用于蓝牙 LE 用途的本地身份。

API 参考
**************

.. doxygengroup:: bt_mesh
