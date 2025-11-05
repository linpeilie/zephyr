.. _bt_mesh_proxy:

代理
#####

代理功能允许传统设备（如手机）通过 GATT 访问蓝牙网状网络。代理功能只有在设置了 :kconfig:option:`CONFIG_BT_MESH_GATT_PROXY` 选项时才被编译。代理功能状态由 :ref:`bluetooth_mesh_models_cfg_srv` 控制，初始值可以通过 :c:member:`bt_mesh_cfg_srv.gatt_proxy` 设置。

启用代理功能的节点可以使用网络标识和节点标识进行广播，这由 :ref:`bluetooth_mesh_models_cfg_cli` 控制。

GATT 代理状态指示是否支持代理功能。

私有代理
*************

支持代理功能和 :ref:`bluetooth_mesh_models_priv_beacon_srv` 模型的节点可以使用私有网络标识和私有节点标识类型进行广播，这由 :ref:`bluetooth_mesh_models_priv_beacon_cli` 控制。通过使用这组标识类型进行广播，节点允许传统设备通过 GATT 连接到网络，同时保持网络的隐私。

私有 GATT 代理状态指示是否支持私有代理功能。

代理征求
******************

如果节点上的 GATT 代理和私有 GATT 代理状态都被禁用，传统设备无法连接到它。但是，支持 :ref:`bluetooth_mesh_od_srv` 的节点可以被征求以在未启用私有 GATT 代理状态的情况下广播可连接广告事件。要征求节点，传统设备可以通过调用 :func:`bt_mesh_proxy_solicit` 函数来发送征求 PDU。要启用此功能，设备必须使用 :kconfig:option:`CONFIG_BT_MESH_PROXY_SOLICITATION` 选项进行编译。

征求 PDU 是包含代理征求 UUID 的非网状、不可连接、非定向广告消息，使用传统设备想要连接的子网的网络密钥加密。PDU 包含传统设备的源地址和序列号。序列号由传统设备维护，并在每次发送新的征求 PDU 时递增。

每个支持征求 PDU 接收的节点都维护自己的征求重放保护列表 (SRPL)。SRPL 通过存储节点处理的有效征求 PDU 的征求序列号 (SSEQ) 和征求源 (SSRC) 对来保护征求机制免受重放攻击。更新 SRPL 和将更改存储到持久存储之间的延迟由 :kconfig:option:`CONFIG_BT_MESH_RPL_STORE_TIMEOUT` 定义。

征求 PDU RPL 配置模型 :ref:`bluetooth_mesh_srpl_cli` 和 :ref:`bluetooth_mesh_srpl_srv` 提供了保存和清除 SRPL 条目的功能。支持征求 PDU RPL 配置客户端模型的节点可以通过调用 :func:`bt_mesh_sol_pdu_rpl_clear` 函数来清除目标上的 SRPL 部分。征求 PDU RPL 配置客户端和服务器之间的通信使用应用程序密钥加密，因此征求 PDU RPL 配置客户端可以在网络中的任何设备上实例化。

当节点接收征求 PDU 并成功认证它时，它将开始使用私有网络标识类型广播可连接广告。广告的持续时间可以通过按需私有代理客户端模型进行配置。

API 参考
*************

.. doxygengroup:: bt_mesh_proxy
