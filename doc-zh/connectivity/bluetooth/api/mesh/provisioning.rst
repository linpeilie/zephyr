.. _bluetooth_mesh_provisioning:

配置
############

配置是将设备添加到网状网络的过程。它需要两个设备在以下角色中运行：

* *配置器* 代表网络所有者，负责将新节点添加到网状网络中。
* *被配置者* 是通过配置过程添加到网络的设备。在配置过程开始之前，被配置者是一个*未配置设备*。

Zephyr 蓝牙网状栈中的配置模块支持被配置者角色的广播和 GATT 配置承载器，以及配置器角色的广播配置承载器。

配置过程
************************

所有蓝牙网状节点必须在参与蓝牙网状网络之前进行配置。配置 API 提供了设备成为已配置网状节点所需的所有功能。配置是一个五步过程，涉及以下步骤：

* 广播
* 邀请
* 公钥交换
* 认证
* 配置数据传输

广播
=========

要开始配置过程，未配置设备必须首先开始广播未配置信标。这使其对附近可以启动配置的配置器可见。要指示设备需要配置，请调用 :c:func:`bt_mesh_prov_enable`。设备开始广播包含设备 UUID 和 ``OOB information`` 字段的未配置信标，如传递给 :c:func:`bt_mesh_init` 的 ``prov`` 参数所指定。此外，可以指定统一资源标识符 (URI)，它可以指向配置器到一些带外信息的位置，例如设备的公钥或认证值数据库。URI 在单独的信标中广告，未配置信标中包含 URI 哈希，以将两者绑定在一起。


统一资源标识符
---------------------------

统一资源标识符应遵循蓝牙核心规范补充文件中指定的格式。URI 必须以 URI 方案开头，编码为单个 utf-8 数据点，或特殊 ``none`` 方案，编码为 ``0x01``。可用方案列在 `蓝牙网站 <https://www.bluetooth.com/specifications/assigned-numbers/>`_ 上。

编码 URI 的示例：

.. list-table:: URI 编码示例

  * - URI
    - 编码后
  * - ``http://example.com``
    - ``\x16//example.com``
  * - ``https://www.zephyrproject.org/``
    - ``\x17//www.zephyrproject.org/``
  * - ``just a string``
    - ``\x01just a string``

配置邀请
=======================

配置器通过发送配置邀请来启动配置过程。邀请提示被配置者使用健康服务器 :ref:`bluetooth_mesh_models_health_srv_attention`（如果可用）来引起对自己的注意。

未配置设备通过展示其功能列表（包括支持的带外认证方法和算法）来自动响应邀请。

公钥交换
===================

在配置过程开始之前，配置器和未配置设备交换公钥，可以是带内或带外 (OOB)。

带内公钥交换是配置过程的一部分，始终由未配置设备和配置器支持。

如果应用程序希望通过 OOB 支持公钥交换，它需要向网状栈提供公钥和私钥。未配置设备将在其功能中反映这一点。配置器通过任何可用的 OOB 机制获取公钥（例如，设备可以广告包含公钥的数据包，或者可以将其编码在设备包装上的 QR 码中）。请注意，即使未配置设备已指定带外交换的公钥，如果无法通过 OOB 机制检索公钥，配置器也可以选择在带内交换公钥。在这种情况下，网状栈将为每个配置过程生成新的密钥对。

要在未配置设备端启用 OOB 公钥支持，需要启用 :kconfig:option:`CONFIG_BT_MESH_PROV_OOB_PUBLIC_KEY`。应用程序必须通过初始化指向 :c:member:`bt_mesh_prov.public_key_be` 和 :c:member:`bt_mesh_prov.private_key_be` 的指针来在配置过程开始之前提供公钥和私钥。密钥需要以大端字节顺序提供。

要提供通过 OOB 获得的设备公钥，请在配置器端调用 :c:func:`bt_mesh_prov_remote_pub_key_set`。

认证
==============

在初始交换之后，配置器选择带外 (OOB) 认证方法。这允许用户确认配置器连接的设备实际上是他们 intended 设备，而不是恶意第三方。

配置 API 支持被配置者的以下认证方法：

* **静态 OOB：** 认证值在生产时分配给设备，配置器可以通过某些应用程序特定的方式查询。
* **输入 OOB：** 用户输入认证值。可用的输入操作列在 :c:enum:`bt_mesh_input_action_t` 中。
* **输出 OOB：** 向用户显示认证值。可用的输出操作列在 :c:enum:`bt_mesh_output_action_t` 中。

应用程序必须为 :c:struct:`bt_mesh_prov` 中支持的认证方法提供回调，以及在 :c:member:`bt_mesh_prov.output_actions` 和 :c:member:`bt_mesh_prov.input_actions` 中启用支持的操作。

当选择输出 OOB 操作时，当调用输出回调时应向用户显示认证值，并保持到调用 :c:member:`bt_mesh_prov.input_complete` 或 :c:member:`bt_mesh_prov.complete` 回调。如果操作是 ``blink``、``beep`` 或 ``vibrate``，应在三秒或更长时间的延迟后重复序列。

当选择输入 OOB 操作时，当应用程序接收 :c:member:`bt_mesh_prov.input` 回调时应提示用户。用户响应应通过 :c:func:`bt_mesh_input_string` 或 :c:func:`bt_mesh_input_number` 反馈给配置 API。如果在 60 秒内没有记录用户响应，则中止配置过程。

如果被配置者希望强制使用 OOB 认证，则必须使用 BT_MESH_ECDH_P256_HMAC_SHA256_AES_CCM 算法。

数据传输
=============

在设备成功认证后，配置器传输配置数据：

* 单播地址
* 网络密钥
* IV 索引
* 网络标志

  * 密钥刷新
  * IV 更新

此外，为节点生成设备密钥。所有这些数据都由网状栈存储，并调用配置 :c:member:`bt_mesh_prov.complete` 回调。

配置安全
*********************

根据公钥交换机制和认证方法的选择，配置过程可以是安全的或不安全的。

2021 年 5 月 24 日，ANSSI `披露 <https://kb.cert.org/vuls/id/799380>`_ 了蓝牙网状配置协议中的一组漏洞，展示了闪烁、振动、推送、扭曲和输入/输出数值 OOB 方法提供的低熵如何在伪装和 MITM 攻击中被利用。作为回应，蓝牙 SIG 在蓝牙网状配置文件规范 v1.0.1 `勘误表 16350 <https://www.bluetooth.org/docman/handlers/DownloadDoc.ashx?doc_id=516072>`_ 中将这些 OOB 方法重新分类为不安全，因为 AuthValue 可能被实时暴力破解。为了确保安全配置，应用程序应使用静态 OOB 值和 OOB 公钥传输。

API 参考
*************

.. doxygengroup:: bt_mesh_prov
