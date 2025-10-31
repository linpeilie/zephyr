.. _lora_api:
.. _lorawan_api:

LoRa 和 LoRaWAN
###############

概述
****

LoRa（长距离的缩写）是由 `Semtech 公司`_ 开发的专有低功耗无线通信协议。

LoRa 充当基于啾声扩展频谱 (CSS) 调制技术的物理层 (PHY)。

LoRaWAN（长距离广域网）在 LoRa PHY 之上定义了网络层。

Zephyr 为 LoRa 提供了 API，以直接在无线接口上发送原始数据包，
以及用于 LoRaWAN 的 API，以通过网关将终端设备连接到互联网。

Zephyr 实现基于 Semtech 的 `LoRaMac-node 库`_，该库作为 Zephyr 模块包含。

.. note::

        ``LoRaMac-node`` 已被 Semtech 弃用，取而代之是
        `LoRa Basics 调制解调器`_。将 Zephyr API 移植以使用
        ``LoRa Basics 调制解调器`` 作为后端的工作正在进行中。

        目前，仅通过
        :kconfig:option:`CONFIG_LORA_MODULE_BACKEND_LORA_BASICS_MODEM`
        为 SX1261、SX1262、SX1272 和 SX1276 芯片组支持基本 LoRa API。


LoRaWAN 规范由 `LoRa 联盟`_ 发布。

.. _`Semtech 公司`: https://www.semtech.com/

.. _`LoRaMac-node 库`: https://github.com/Lora-net/LoRaMac-node

.. _`LoRa Basics 调制解调器`: https://github.com/Lora-net/SWL2001

.. _`LoRa 联盟`: https://lora-alliance.org/

配置选项
*******

LoRa PHY
========

相关配置选项可在 :zephyr_file:`drivers/lora/Kconfig` 下找到。

* :kconfig:option:`CONFIG_LORA`

* :kconfig:option:`CONFIG_LORA_SHELL`

* :kconfig:option:`CONFIG_LORA_INIT_PRIORITY`

LoRaWAN
=======

相关配置选项可在 :zephyr_file:`subsys/lorawan/Kconfig` 下找到。

* :kconfig:option:`CONFIG_LORAWAN`

* :kconfig:option:`CONFIG_LORAWAN_SYSTEM_MAX_RX_ERROR`

* :kconfig:option:`CONFIG_LORAMAC_REGION_AS923`

* :kconfig:option:`CONFIG_LORAMAC_REGION_AU915`

* :kconfig:option:`CONFIG_LORAMAC_REGION_CN470`

* :kconfig:option:`CONFIG_LORAMAC_REGION_CN779`

* :kconfig:option:`CONFIG_LORAMAC_REGION_EU433`

* :kconfig:option:`CONFIG_LORAMAC_REGION_EU868`

* :kconfig:option:`CONFIG_LORAMAC_REGION_KR920`

* :kconfig:option:`CONFIG_LORAMAC_REGION_IN865`

* :kconfig:option:`CONFIG_LORAMAC_REGION_US915`

* :kconfig:option:`CONFIG_LORAMAC_REGION_RU864`


API 参考
*******

LoRa PHY
========

.. doxygengroup:: lora_interface

LoRaWAN
=======

.. doxygengroup:: lorawan_api
