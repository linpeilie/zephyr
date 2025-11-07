.. _sdhc_api:

安全数字接口 (Secure Digital, SD card)
#######################################

Zephyr 可以使用系统的原生 SD 卡接口或通过 SPI (Serial Peripheral Interface, 串行外设接口) 与连接的 SD 卡通信。某些设备还可以与 MMC (MultiMediaCard, 多媒体卡) 设备通信。

应用程序可以使用 Zephyr 的 :ref:`磁盘访问 API <disk_access_api>` 将 SD 卡用作存储设备,或使用 Zephyr 的 SD 卡子系统直接从卡读取和写入。

SD 主机控制器 (SD Host Controller, SDHC)
*****************************************

SD 主机控制器 (SDHC) 是能够向 SD 卡发送命令的设备。这些命令可以使用系统的原生 SD 卡接口发送,也可以通过 SPI 发送。

应用程序通常不应直接使用 SD 主机控制器 API,而应使用 Zephyr 的 SD 卡子系统。

请求 (Requests)
================

The core of the SD host controller (SDHC) API is the :c:func:`sdhc_request` API.
Requests contain a :c:struct:`sdhc_command` command structure, and an optional
:c:struct:`sdhc_data` data structure. The caller may check the return code,
or the ``response`` field of the SD command structure to determine if the
SDHC request succeeded. The data structure allows the caller to specify a
number of blocks to transfer, and a buffer location to read or write them from.
Whether the provided buffer is used for sending or reading data depends on the
command opcode provided.

Host Controller I/O
===================

The :c:func:`sdhc_set_io` API allows the user to change I/O settings of the SD
host controller, such as clock frequency, I/O voltage, and card power. Not all
controllers will support applying all I/O settings. For example, SPI mode
controllers typically cannot toggle power to the SD card.

Related configuration options:

* :kconfig:option:`CONFIG_SDHC`

API Reference
*************

.. doxygengroup:: sdhc_interface
