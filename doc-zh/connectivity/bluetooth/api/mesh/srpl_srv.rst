.. _bluetooth_mesh_srpl_srv:

征求 PDU RPL 配置服务器
#########################################

征求 PDU RPL 配置服务器模型是蓝牙网状规范定义的基础模型。如果节点启用了
:ref:`bluetooth_mesh_od_srv`，则启用该模型。

征求 PDU RPL 配置服务器模型在蓝牙网状协议规范版本 1.1 中引入，并管理保存在设备上的征求重放保护列表 (SRPL)。SRPL 用于拒绝已经由节点处理的征求 PDU。当节点成功处理有效的征求 PDU 消息时，消息的 SSRC 字段和 SSEQ 字段存储在节点的 SRPL 中。

征求 PDU RPL 配置服务器没有自己的 API，依赖 :ref:`bluetooth_mesh_srpl_cli` 来控制它。该模型仅接受使用配置客户端配置的应用程序密钥加密的消息。

如果存在，征求 PDU RPL 配置服务器模型只能在主元素上实例化。

配置
******

对于征求 PDU RPL 配置服务器模型，可以配置 :kconfig:option:`CONFIG_BT_MESH_PROXY_SRPL_SIZE` 选项来设置 SRPL 的大小。

API 参考
***********

.. doxygengroup:: bt_mesh_sol_pdu_rpl_srv
