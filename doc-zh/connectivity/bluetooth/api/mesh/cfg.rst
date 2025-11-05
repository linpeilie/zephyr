.. _bluetooth_mesh_cfg:

运行时配置
#####################

运行时配置 API 允许应用程序直接更改其运行时配置，而无需通过配置模型。

蓝牙网状节点通常应由具有 :ref:`bluetooth_mesh_models_cfg_cli` 模型的中央网络配置设备进行配置。每个网状节点实例化一个 :ref:`bluetooth_mesh_models_cfg_srv` 模型，配置客户端可以与之通信以更改节点配置。在某些情况下，网状节点不能依赖配置客户端来检测或确定本地约束，例如电池电量低或拓扑变化。对于这些场景，此 API 可用于在本地更改配置。

.. note::
   节点配置之前的运行时配置更改不会存储在 :ref:`持久存储 <bluetooth_mesh_persistent_storage>` 中。

API 参考
*************

.. doxygengroup:: bt_mesh_cfg
