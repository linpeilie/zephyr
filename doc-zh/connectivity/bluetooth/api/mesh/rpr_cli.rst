.. _bluetooth_mesh_models_rpr_cli:

远程配置客户端
########################

远程配置客户端模型是蓝牙网状规范定义的基础模型。它通过
:kconfig:option:`CONFIG_BT_MESH_RPR_CLI` 选项启用。

远程配置客户端模型在蓝牙网状协议规范版本 1.1 中引入。该模型提供将设备远程配置到网状网络中的功能，并通过与支持
:ref:`bluetooth_mesh_models_rpr_srv` 模型的网状节点交互来执行节点配置协议接口过程。

远程配置客户端模型使用包含目标远程配置服务器模型实例的节点的设备密钥与远程配置服务器模型进行通信。

如果存在，远程配置客户端模型必须在主元素上实例化。

扫描
******

扫描过程用于扫描位于远程配置服务器附近的未配置设备。远程配置客户端通过调用
:c:func:`bt_mesh_rpr_scan_start` 启动扫描过程：

.. code-block:: C

      static void rpr_scan_report(struct bt_mesh_rpr_cli *cli,
                  const struct bt_mesh_rpr_node *srv,
                  struct bt_mesh_rpr_unprov *unprov,
                  struct net_buf_simple *adv_data)
      {

      }

      struct bt_mesh_rpr_cli rpr_cli = {
         .scan_report = rpr_scan_report,
      };

      const struct bt_mesh_rpr_node srv = {
         .addr = 0x0004,
         .net_idx = 0,
         .ttl = BT_MESH_TTL_DEFAULT,
      };

      struct bt_mesh_rpr_scan_status status;
      uint8_t *uuid = NULL;
      uint8_t timeout = 10;
      uint8_t max_devs = 3;

      bt_mesh_rpr_scan_start(&rpr_cli, &srv, uuid, timeout, max_devs, &status);

上述示例显示了在目标远程配置服务器节点上启动扫描过程的伪代码。此过程将启动一个十秒的多设备扫描，其中生成的扫描报告最多包含三个未配置设备。如果指定了 UUID 参数，相同的过程将仅扫描具有相应 UUID 的设备。过程完成后，服务器发送扫描报告，该报告将在客户端的 :c:member:`bt_mesh_rpr_cli.scan_report` 回调中处理。

此外，远程配置客户端模型还支持通过 :c:func:`bt_mesh_rpr_scan_start_ext` 调用进行扩展扫描。扩展扫描通过允许远程配置服务器为特定设备报告额外数据来补充常规扫描。如果未配置设备支持，远程配置服务器将使用主动扫描从未配置设备请求扫描响应。

配置
********

远程配置客户端通过调用 :c:func:`bt_mesh_provision_remote` 启动配置过程：

.. code-block:: C

      struct bt_mesh_rpr_cli rpr_cli;

      const struct bt_mesh_rpr_node srv = {
         .addr = 0x0004,
         .net_idx = 0,
         .ttl = BT_MESH_TTL_DEFAULT,
      };

      uint8_t uuid[16] = { 0xaa };
      uint16_t addr = 0x0006;
      uint16_t net_idx = 0;

      bt_mesh_provision_remote(&rpr_cli, &srv, uuid, net_idx, addr);

上述示例显示通过远程配置服务器节点远程配置设备的伪代码。此过程将尝试配置具有相应 UUID 的设备，并使用索引零处的网络键为其主元素分配地址 0x0006。

.. note::
   在远程配置期间，与普通配置一样会触发相同的 :c:struct:`bt_mesh_prov` 回调。有关更多详细信息，请参见 :ref:`bluetooth_mesh_provisioning` 部分。

重新配置
****************

除了扫描和配置功能外，远程配置客户端还提供了重新配置支持 :ref:`bluetooth_mesh_models_rpr_srv` 模型的设备上的节点地址、设备密钥和组合数据的方法。这通过节点配置协议接口 (NPPI) 提供，支持以下三个过程：

* 设备密钥刷新过程：用于更改目标节点的设备密钥，而无需重新配置节点。
* 节点地址刷新过程：用于更改节点的设备密钥和单播地址。
* 节点组合刷新过程：用于更改节点的设备密钥，以及添加或删除节点的模型或功能。

三个 NPPI 过程可以通过 :c:func:`bt_mesh_reprovision_remote` 调用启动：

.. code-block:: C

      struct bt_mesh_rpr_cli rpr_cli;
      struct bt_mesh_rpr_node srv = {
         .addr = 0x0006,
         .net_idx = 0,
         .ttl = BT_MESH_TTL_DEFAULT,
      };

      bool composition_changed = false;
      uint16_t new_addr = 0x0009;

      bt_mesh_reprovision_remote(&rpr_cli, &srv, new_addr, composition_changed);

上述示例显示了在目标节点上触发节点地址刷新过程的伪代码。具体过程不是直接选择的，而是通过输入的其他参数来选择的。在示例中，我们可以看到目标的当前单播地址是 0x0006，而新地址设置为 0x0009。如果两个地址相同，并且 ``composition_changed`` 标志设置为 true，则此代码将改为触发节点组合刷新过程。如果两个地址相同，并且 ``composition_changed`` 标志设置为 false，则此代码将触发设备密钥刷新过程。

API 参考
***********

.. doxygengroup:: bt_mesh_rpr_cli
