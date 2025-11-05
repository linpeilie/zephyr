.. _bluetooth_mesh_sar_cfg_cli:

SAR 配置客户端
########################

SAR 配置客户端模型是蓝牙网状规范定义的基础模型。它是一个可选模型，通过
:kconfig:option:`CONFIG_BT_MESH_SAR_CFG_CLI` 配置选项启用。

SAR 配置客户端模型在蓝牙网状协议规范版本 1.1 中引入，它支持配置支持
:ref:`bluetooth_mesh_sar_cfg_srv` 模型的节点的下层传输层行为。

该模型可以使用 SAR 配置消息向 SAR 配置服务器（ SAR 发送器和 SAR 接收器）发送消息以查询或更改其支持的状态。

SAR 发送器过程用于确定和配置 SAR 配置服务器的 SAR 发送器状态。函数调用
:c:func:`bt_mesh_sar_cfg_cli_transmitter_get` 和 :c:func:`bt_mesh_sar_cfg_cli_transmitter_set` 分别用于获取和设置目标节点的 SAR 发送器状态。

SAR 接收器过程用于确定和配置 SAR 配置服务器的 SAR 接收器状态。函数调用
:c:func:`bt_mesh_sar_cfg_cli_receiver_get` 和 :c:func:`bt_mesh_sar_cfg_cli_receiver_set` 分别用于获取和设置目标节点的 SAR 接收器状态。

有关这两个状态的更多信息，请参见 :ref:`bt_mesh_sar_cfg_states`。

元素可以随时发送任何 SAR 配置客户端消息来查询或更改对等节点 SAR 配置服务器模型支持的状态。SAR 配置客户端模型仅接受使用支持 SAR 配置服务器模型的节点的设备密钥加密的消息。

如果存在，SAR 配置客户端模型只能在主元素上实例化。

API 参考
***********

.. doxygengroup:: bt_mesh_sar_cfg_cli
