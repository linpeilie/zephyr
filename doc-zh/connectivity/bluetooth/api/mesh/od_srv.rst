.. _bluetooth_mesh_od_srv:

按需私有代理服务器
###########################

按需私有代理服务器模型是蓝牙网状规范定义的基础模型。它通过 :kconfig:option:`CONFIG_BT_MESH_OD_PRIV_PROXY_SRV` 选项启用。

按需私有代理服务器模型在蓝牙网状协议规范版本 1.1 中引入，通过管理其按需私有 GATT 代理状态，支持配置作为征求 PDU 接收者的节点使用私有网络标识类型进行广播。

启用时，:ref:`bluetooth_mesh_srpl_srv` 也会被启用。按需私有代理服务器依赖于节点上存在的 :ref:`bluetooth_mesh_models_priv_beacon_srv`。

按需私有代理服务器没有自己的 API，依赖 :ref:`bluetooth_mesh_od_cli` 来控制它。按需私有代理服务器模型仅接受使用节点设备密钥加密的消息。

如果存在，按需私有代理服务器模型只能在主元素上实例化。

API 参考
***********

.. doxygengroup:: bt_mesh_od_priv_proxy_srv
