.. _mbox_api:

多通道处理器间邮箱 (Multi-Channel Inter-Processor Mailbox, MBOX)
##################################################################

概述 (Overview)
****************

MBOX 设备是一种能够在系统中的 CPU 和集群之间传递信号(和数据,取决于外设)的外设。每个 MBOX 实例提供一个或多个通道,每个通道针对另一个 CPU 集群(多个通道可以针对同一集群)。


API 参考 (API Reference)
*************************

.. doxygengroup:: mbox_interface
