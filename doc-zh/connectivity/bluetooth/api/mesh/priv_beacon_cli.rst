.. _bluetooth_mesh_models_priv_beacon_cli:

私有信标客户端
######################

私有信标客户端模型是蓝牙网状规范定义的基础模型。它通过
:kconfig:option:`CONFIG_BT_MESH_PRIV_BEACON_CLI` 选项启用。

私有信标客户端模型在蓝牙网状协议规范版本 1.1 中引入，并提供用于配置
:ref:`bluetooth_mesh_models_priv_beacon_srv` 模型的功能。

私有信标功能通过定期随机化信标输入数据为不同的蓝牙网状信标添加隐私保护。这保护网状节点免受网状网络外部设备的跟踪，并隐藏网络的 IV 索引、IV 更新和密钥刷新状态。

私有信标客户端模型使用目标节点的设备密钥与
:ref:`bluetooth_mesh_models_priv_beacon_srv` 模型进行通信。私有信标客户端模型可以与其他节点上的服务器通信，或通过本地私有信标服务器模型进行自配置。

私有信标客户端 API 中的所有配置函数都以 ``net_idx`` 和 ``addr`` 作为第一个参数。这些参数应设置为网络索引和目标节点配置时使用的主要单播地址。

如果存在，私有信标客户端模型只能在主元素上实例化。

API 参考
***********

.. doxygengroup:: bt_mesh_priv_beacon_cli
