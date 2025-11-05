.. _bluetooth_mesh_blob_srv:

BLOB 传输服务器
####################

二进制大对象 (BLOB) 传输服务器模型实现了大型二进制对象的可靠接收。它作为 :ref:`bluetooth_mesh_dfu_srv` 的后端，但也可用于接收其他二进制镜像。

BLOB
*****

如 :ref:`bluetooth_mesh_blob` 所述，BLOB 传输模型传输的二进制对象被划分为块，块又被划分为数据块。由于传输由 BLOB 传输客户端模型控制，BLOB 传输服务器必须允许块以任意顺序到达。块内的数据块也可以任意顺序到达，但在一个块开始之前必须接收到该块中的所有数据块。

BLOB 传输服务器跟踪接收到的块和数据块，并将仅处理每个块和数据块一次。BLOB 传输服务器还确保任何丢失的数据块都由 BLOB 传输客户端重新发送。

用法
*****

BLOB 传输服务器在元素上实例化，具有一组事件处理程序回调：

.. code-block:: C

   static const struct bt_mesh_blob_srv_cb blob_cb = {
       /* 回调 */
   };

   static struct bt_mesh_blob_srv blob_srv = {
       .cb = &blob_cb,
   };

   static const struct bt_mesh_model models[] = {
       BT_MESH_MODEL_BLOB_SRV(&blob_srv),
   };

BLOB 传输服务器一次只能接收一个 BLOB 传输。在 BLOB 传输服务器可以接收传输之前，它必须由用户准备。传输 ID 必须通过 :c:func:`bt_mesh_blob_srv_recv` 函数传递给 BLOB 传输服务器，然后由 BLOB 传输客户端启动传输。ID 必须在 BLOB 传输客户端和 BLOB 传输服务器之间通过一些高级程序共享，如供应商特定的传输管理模型。

一旦在 BLOB 传输服务器上设置了传输，它就准备好接收 BLOB。应用程序通过事件处理程序回调通知传输进度，BLOB 数据被发送到 BLOB 流。

BLOB 传输服务器、BLOB 流和应用程序之间的交互如下所示：

.. figure:: images/blob_srv.svg
   :align: center
   :alt: BLOB Transfer Server model interaction

   BLOB 传输服务器模型交互

传输暂停
*******************

BLOB 传输服务器在传输期间保持一个运行计时器，该计时器在每个接收到的消息上重置。如果 BLOB 传输客户端在传输计时器过期之前未发送消息，传输将由 BLOB 传输服务器暂停。

BLOB 传输服务器通过调用 :c:member:`suspended
<bt_mesh_blob_srv_cb.suspended>` 回调通知用户暂停。如果 BLOB 传输服务器正在接收一个块，该块将被丢弃。

BLOB 传输客户端可以通过启动新的块传输来恢复暂停的传输。BLOB 传输服务器通过调用 :c:member:`resume <bt_mesh_blob_srv_cb.resume>`
回调通知用户。

传输恢复
*****************

BLOB 传输的状态被持久存储。如果发生重启，BLOB 传输服务器将尝试恢复传输。当蓝牙网状子系统启动（例如通过调用 :c:func:`bt_mesh_init`）时，BLOB 传输服务器将检查中止的传输，并调用 :c:member:`recover <bt_mesh_blob_srv_cb.recover>` 回调（如果有）。在恢复回调中，用户必须提供用于传输剩余部分的 BLOB 流。如果恢复回调未成功返回或未提供 BLOB 流，传输将被放弃。如果未实现恢复回调，重启后传输总是被放弃。

传输成功恢复后，BLOB 传输服务器进入暂停状态。它将保持暂停状态，直到 BLOB 传输客户端恢复传输，或用户取消它。

.. note::
   发送传输的 BLOB 传输客户端必须支持传输恢复才能完成传输。如果 BLOB 传输客户端已经放弃传输，BLOB 传输服务器将保持暂停状态，直到应用程序调用 :c:func:`bt_mesh_blob_srv_cancel`。

API 参考
*************

.. doxygengroup:: bt_mesh_blob_srv
