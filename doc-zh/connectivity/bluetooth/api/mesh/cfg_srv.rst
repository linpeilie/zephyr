.. _bluetooth_mesh_models_cfg_srv:

配置服务器
####################

配置服务器模型是蓝牙网状规范定义的基础模型。配置服务器模型控制网状节点的大多数参数。它没有自己的 API，但依赖 :ref:`bluetooth_mesh_models_cfg_cli` 来控制它。

配置服务器模型在所有蓝牙网状节点上是强制的，并且只能在主元素上实例化。

API 参考
*************

.. doxygengroup:: bt_mesh_cfg_srv
