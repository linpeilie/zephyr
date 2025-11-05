.. _bluetooth_mesh_blob_cli:

BLOB 传输客户端
####################

二进制大对象 (BLOB) 传输客户端是 BLOB 传输的发送方。它支持
以推 BLOB 传输模式和拉 BLOB 传输模式向任意数量的目标节点发送任意大小的 BLOB。

用法
*****

初始化
==============

BLOB 传输客户端在元素上实例化，具有一组事件处理程序回调：

.. code-block:: C

   static const struct bt_mesh_blob_cli_cb blob_cb = {
         /* 回调 */
   };

   static struct bt_mesh_blob_cli blob_cli = {
         .cb = &blob_cb,
   };

   static const struct bt_mesh_model models[] = {
         BT_MESH_MODEL_BLOB_CLI(&blob_cli),
   };

传输上下文
================

传输能力检索过程和 BLOB 传输都使用 :c:struct:`bt_mesh_blob_cli_inputs` 实例来确定如何执行传输。BLOB 传输客户端输入结构在用于程序之前至少必须用目标列表、应用密钥和生存时间 (TTL) 值初始化：

.. code-block:: c

   static struct bt_mesh_blob_target targets[3] = {
           { .addr = 0x0001 },
           { .addr = 0x0002 },
           { .addr = 0x0003 },
   };
   static struct bt_mesh_blob_cli_inputs inputs = {
           .app_idx = MY_APP_IDX,
           .ttl = BT_MESH_TTL_DEFAULT,
   };

   sys_slist_init(&inputs.targets);
   sys_slist_append(&inputs.targets, &targets[0].n);
   sys_slist_append(&inputs.targets, &targets[1].n);
   sys_slist_append(&inputs.targets, &targets[2].n);

请注意，传输中的所有 BLOB 传输服务器都必须绑定到所选的应用密钥。


组地址
-------------

应用程序可以在上下文结构中额外指定一个组地址。如果组不是
:c:macro:`BT_MESH_ADDR_UNASSIGNED`，传输中的消息将发送到组
地址，而不是单独发送到每个目标节点。网状管理器必须确保所有
具有 BLOB 传输服务器模型的目标节点都订阅此组地址。

使用组地址传输 BLOB 通常可以提高传输速度，因为
BLOB 传输客户端同时将每条消息发送到所有目标节点。但是，向蓝牙网状中的组地址发送大型分段消息通常不如
发送到单播地址可靠，因为组没有传输层确认机制。这可能导致每个块末尾的恢复期变长，并增加失去目标节点的风险。使用组地址进行 BLOB 传输通常只有在目标节点列表很长的情况下才会得到回报，每种寻址策略的有效性在不同的部署和数据块大小之间会有很大差异。

传输超时
----------------

如果目标节点在 BLOB 传输客户端的时间限制内未对确认消息做出响应，则该目标节点将从传输中移除。应用程序可以通过上下文结构为 BLOB 传输客户端提供额外时间来降低这种可能性。额外时间可以 10 秒为增量设置，最长 182 小时，除了 20 秒的基础时间之外。等待时间随传输 TTL 自动缩放。

请注意，BLOB 传输客户端仅在以下情况下继续传输：

* 所有目标节点都已响应。
* 节点已从目标节点列表中移除。
* BLOB 传输客户端超时。

增加等待时间会增加此延迟。

BLOB 传输能力检索
====================================

通常建议在开始传输之前检索 BLOB 传输能力。该程序用允许所有目标节点参与传输的最宽松的参数集从所有目标节点填充传输能力。任何未能响应或响应不兼容传输参数的目标节点都将被移除。

目标节点根据它们在目标节点列表中的顺序进行优先级排序。如果发现目标节点与任何先前目标节点不兼容，例如通过报告不重叠的块大小范围，它将被移除。丢失的目标节点将通过 :c:member:`lost_target <bt_mesh_blob_cli_cb.lost_target>` 回调报告。

程序结束通过 :c:member:`caps <bt_mesh_blob_cli_cb.caps>`
回调发出信号，结果能力可用于确定 BLOB 传输所需的块和数据块大小。

BLOB 传输
=============

通过调用 :c:func:`bt_mesh_blob_cli_send` 函数启动 BLOB 传输，该函数（除了
上述传输输入）需要一组传输参数和一个 BLOB 流实例。传输参数包括 64 位 BLOB ID、BLOB 大小、传输模式、对数表示的块大小和数据块大小。BLOB ID 由应用程序定义，但必须与 BLOB 传输服务器启动时使用的 BLOB ID 匹配。

传输运行直到至少一个目标节点成功完成或被取消。传输结束通过 :c:member:`end
<bt_mesh_blob_cli_cb.end>` 回调通知应用程序。丢失的目标节点将通过
:c:member:`lost_target <bt_mesh_blob_cli_cb.lost_target>` 回调报告。

API 参考
*************

.. doxygengroup:: bt_mesh_blob_cli
