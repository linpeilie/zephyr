.. _bluetooth_mesh_od_cli:

按需私有代理客户端
###########################

按需私有代理客户端模型是蓝牙网状规范定义的基础模型。该模型是可选的，通过
:kconfig:option:`CONFIG_BT_MESH_OD_PRIV_PROXY_CLI` 选项启用。

按需私有代理客户端模型在蓝牙网状协议规范版本 1.1 中引入，用于设置和检索按需私有 GATT 代理状态。该状态定义节点在收到征求 PDU 后，使用私有网络标识类型广播网状代理服务的时间长度。

按需私有代理客户端模型使用包含目标按需私有代理服务器模型实例的节点的设备密钥与按需私有代理服务器模型进行通信。

如果存在，按需私有代理客户端模型只能在主元素上实例化。

配置
******

按需私有代理客户端模型的行为可以通过传输超时选项
:kconfig:option:`CONFIG_BT_MESH_OD_PRIV_PROXY_CLI_TIMEOUT` 进行配置。
:kconfig:option:`CONFIG_BT_MESH_OD_PRIV_PROXY_CLI_TIMEOUT` 控制客户端等待状态响应消息到达的毫秒数。此值可以使用
:c:func:`bt_mesh_od_priv_proxy_cli_timeout_set` 在运行时更改。


API 参考
***********

.. doxygengroup:: bt_mesh_od_priv_proxy_cli
