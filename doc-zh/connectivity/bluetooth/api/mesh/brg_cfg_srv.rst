.. _bluetooth_mesh_models_brg_cfg_srv:

桥接配置服务器
###########################

桥接配置服务器模型是蓝牙网状规范定义的基础模型。它是一个可选模型，通过
:kconfig:option:`CONFIG_BT_MESH_BRG_CFG_SRV` 配置选项启用。该模型扩展了
:ref:`bluetooth_mesh_models_cfg_srv` 模型。

桥接配置服务器模型在蓝牙网状协议规范
版本 1.1 中引入，用于支持和管理网状桥功能。

桥接配置服务器模型依赖 :ref:`bluetooth_mesh_models_brg_cfg_cli` 进行配置。桥接配置服务器模型仅接受使用节点设备密钥加密的消息。

如果存在，桥接配置服务器模型必须在主元素上实例化。

桥接配置服务器模型提供对以下三种状态的访问：

* 网状桥
* 桥接表
* 桥接表大小

有关状态的更多信息，请参阅 :ref:`bluetooth_mesh_brg_cfg_states`。

API 参考
*************

.. doxygengroup:: bt_mesh_brg_cfg_srv
