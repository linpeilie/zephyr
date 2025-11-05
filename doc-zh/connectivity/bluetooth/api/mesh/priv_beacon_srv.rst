.. _bluetooth_mesh_models_priv_beacon_srv:

私有信标服务器
######################

私有信标服务器模型是蓝牙网状规范定义的基础模型。它通过
:kconfig:option:`CONFIG_BT_MESH_PRIV_BEACON_SRV` 选项启用。

私有信标服务器模型在蓝牙网状协议规范版本 1.1 中引入，并控制网状节点的私有信标状态、私有 GATT 代理状态和私有节点标识状态。

私有信标功能通过定期随机化信标输入数据为不同的蓝牙网状信标添加隐私保护。这保护网状节点免受网状网络外部设备的跟踪，并隐藏网络的 IV 索引、IV 更新和密钥刷新状态。必须实例化私有信标服务器，设备才能支持发送私有信标，但节点无需该服务器即可处理接收到的私有信标。

私有信标服务器没有自己的 API，但依赖 :ref:`bluetooth_mesh_models_priv_beacon_cli` 来控制它。私有信标服务器模型仅接受使用节点设备密钥加密的消息。

应用程序可以通过传递给 :c:macro:`BT_MESH_MODEL_PRIV_BEACON_SRV` 的 :c:struct:`bt_mesh_priv_beacon_srv` 实例配置私有信标服务器模型的初始参数。请注意，如果网状节点在设置子系统中存储了对该配置的更改，则初始值可能在加载时被覆盖。

如果存在，私有信标服务器模型只能在主元素上实例化。

API 参考
***********

.. doxygengroup:: bt_mesh_priv_beacon_srv
