.. _bluetooth_mesh_models_rpr_srv:

远程配置服务器
########################

远程配置服务器模型是蓝牙网状规范定义的基础模型。它通过
:kconfig:option:`CONFIG_BT_MESH_RPR_SRV` 选项启用。

远程配置服务器模型在蓝牙网状协议规范版本 1.1 中引入，用于支持远程配置设备到网状网络的功能。

远程配置服务器没有自己的 API，但依赖 :ref:`bluetooth_mesh_models_rpr_cli` 来控制它。远程配置服务器模型仅接受使用节点设备密钥加密的消息。

如果存在，远程配置服务器模型必须在主元素上实例化。

请注意，通过节点配置协议接口 (NPPI) 过程刷新设备密钥、节点地址或组合数据后，将触发 :c:member:`bt_mesh_prov.reprovisioned` 回调。有关更多详细信息，请参见 :ref:`bluetooth_mesh_models_rpr_cli` 部分。

限制
-----------

远程配置服务器模型适用以下限制：

* 不支持使用 PB-GATT 配置未配置设备。
* 支持所有节点配置协议接口 (NPPI) 过程。但是，如果设备在固件更新后组合数据发生更改（参见 :ref:`固件影响 <bluetooth_mesh_dfu_firmware_effect>`），设备无法保持配置状态。如果预期组合数据会更改，设备应该取消配置。


API 参考
***********

.. doxygengroup:: bt_mesh_rpr_srv
