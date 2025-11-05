.. _bluetooth_mesh_srpl_cli:

征求 PDU RPL 配置客户端
#########################################

征求 PDU RPL 配置客户端模型是蓝牙网状规范定义的基础模型。该模型是可选的，通过
:kconfig:option:`CONFIG_BT_MESH_SOL_PDU_RPL_CLI` 选项启用。

征求 PDU RPL 配置客户端模型在蓝牙网状协议规范版本 1.1 中引入，支持从支持
:ref:`bluetooth_mesh_srpl_srv` 模型的节点的征求重放保护列表 (SRPL) 中移除地址的功能。

征求 PDU RPL 配置客户端模型使用配置客户端配置的应用程序密钥与征求 PDU RPL 配置服务器模型进行通信。

如果存在，征求 PDU RPL 配置客户端模型只能在主元素上实例化。

配置
******

征求 PDU RPL 配置客户端模型的行为可以通过传输超时选项 :kconfig:option:`CONFIG_BT_MESH_SOL_PDU_RPL_CLI_TIMEOUT` 进行配置。
:kconfig:option:`CONFIG_BT_MESH_SOL_PDU_RPL_CLI_TIMEOUT` 控制征求 PDU RPL 配置客户端等待响应消息到达的毫秒数。此值可以使用
:c:func:`bt_mesh_sol_pdu_rpl_cli_timeout_set` 在运行时更改。

API 参考
***********

.. doxygengroup:: bt_mesh_sol_pdu_rpl_cli
