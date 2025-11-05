.. _bluetooth_mesh_sar_cfg_srv:

SAR 配置服务器
########################

SAR 配置服务器模型是蓝牙网状规范定义的基础模型。它是一个可选模型，通过
:kconfig:option:`CONFIG_BT_MESH_SAR_CFG_SRV` 配置选项启用。

SAR 配置服务器模型在蓝牙网状协议规范版本 1.1 中引入，它支持配置蓝牙网状节点的
:ref:`分段和重组 (SAR) <bluetooth_mesh_sar_cfg>` 行为。该模型为 SAR 配置定义了一组状态和消息。

SAR 配置服务器模型定义了两个状态，SAR 发送器状态和 SAR 接收器状态。有关这两个状态的更多信息，请参见 :ref:`bt_mesh_sar_cfg_states`。

该模型还支持 SAR 发送器和 SAR 接收器的获取和设置消息。

SAR 配置服务器模型没有自己的 API，但依赖 :ref:`bluetooth_mesh_sar_cfg_cli` 来控制它。SAR 配置服务器模型仅接受使用节点设备密钥加密的消息。

如果存在，SAR 配置服务器模型只能在主元素上实例化。

API 参考
***********

.. doxygengroup:: bt_mesh_sar_cfg_srv
