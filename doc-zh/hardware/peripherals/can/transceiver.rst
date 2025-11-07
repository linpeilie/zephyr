.. _can_transceiver_api:

CAN 收发器 (CAN Transceiver)
#############################

.. contents::
    :local:
    :depth: 2

概述 (Overview)
****************

CAN 收发器是一个外部设备，它将来自 CAN 控制器的逻辑电平信号转换为总线电平。
总线线路称为 CAN 高电平(CAN H)和 CAN 低电平(CAN L)。
从控制器到收发器的发送线称为 CAN TX，接收线称为 CAN RX。
这些线使用逻辑电平，而总线电平在 CAN H 和 CAN L 之间进行差分解释。
总线可以处于隐性(逻辑 1)或显性(逻辑 0)状态。
隐性状态是指两条线路 CAN H 和 CAN L 的电压电平大致相同。此状态也是空闲状态。
要向总线写入显性位，开漏晶体管将 CAN H 连接到 Vdd，将 CAN L 连接到地。
第一个和最后一个节点在 CAN H 和 CAN L 之间使用 120 欧姆电阻来终止总线。
显性状态总是覆盖隐性状态。
这种结构称为线与(wired-AND)。

.. image:: transceiver.svg
   :width: 70%
   :align: center
   :alt: CAN 收发器

CAN 收发器 API 参考 (CAN Transceiver API Reference)
****************************************************

.. doxygengroup:: can_transceiver
