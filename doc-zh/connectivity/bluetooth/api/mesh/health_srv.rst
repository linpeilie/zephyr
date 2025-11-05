.. _bluetooth_mesh_models_health_srv:

健康服务器
#############

健康服务器模型为 :ref:`bluetooth_mesh_models_health_cli` 模型提供注意回调和节点诊断。它主要用于报告网状节点中的故障并将网状节点映射到其物理位置。

如果存在，健康服务器模型必须在主元素上实例化。

故障
******

健康服务器模型可以报告设备生命周期中发生的一系列故障。通常，故障是可能改变节点行为的事件或条件，如电源故障或故障外设。故障分为警告和错误。警告指示接近节点设计承受极限的条件，但不一定损坏设备。错误指示超出节点设计限制的条件，并可能导致无效行为或永久设备损坏。

故障值 ``0x01`` 到 ``0x7f`` 保留给蓝牙网状规范，规范定义的故障完整列表可在 :ref:`bluetooth_mesh_health_faults` 中找到。故障值 ``0x80`` 到 ``0xff`` 是供应商特定的。故障列表始终与公司 ID 一起报告，以帮助解释供应商特定故障。

.. _bluetooth_mesh_models_health_srv_attention:

注意状态
***************

注意状态用于使设备通过一些物理行为（如闪烁、播放声音或振动）引起对自身的注意。注意状态可在配置期间使用，以让用户知道他们正在配置哪个设备，以及在运行时通过健康模型使用。

启用时，注意状态始终分配一到 255 秒范围内的超时。健康服务器 API 为应用程序提供两个回调来运行其注意调用行为：:c:member:`bt_mesh_health_srv_cb.attn_on` 在注意期开始时调用，:c:member:`bt_mesh_health_srv_cb.attn_off` 在结束时调用。

注意期的剩余时间可以通过 :c:member:`bt_mesh_health_srv.attn_timer` 查询。

API 参考
*************

.. doxygengroup:: bt_mesh_health_srv

.. _bluetooth_mesh_health_faults:

健康故障
=============

蓝牙网状规范定义的故障值。

.. doxygengroup:: bt_mesh_health_faults
