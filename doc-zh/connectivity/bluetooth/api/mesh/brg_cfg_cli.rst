.. _bluetooth_mesh_models_brg_cfg_cli:

桥接配置客户端
###########################

桥接配置客户端是蓝牙网状规范定义的基础模型。该模型是可选的，通过 :kconfig:option:`CONFIG_BT_MESH_BRG_CFG_CLI` 选项启用。

桥接配置客户端模型提供配置包含 :ref:`bluetooth_mesh_models_brg_cfg_srv` 的另一个网状节点的网状桥功能的功能。包含目标桥接配置服务器的节点的设备密钥用于接入层安全。

如果存在，桥接配置客户端模型只能在主元素上实例化。

API 参考
*************

.. doxygengroup:: bt_mesh_brg_cfg_cli
