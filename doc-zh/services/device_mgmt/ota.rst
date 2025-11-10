.. _ota:

空中升级 (Over-the-Air Update)
###############################

概述 (Overview)
****************

空中升级(OTA)更新是一种使用网络连接向远程设备交付固件更新的方法 (Over-the-Air (OTA) Update is a method for delivering firmware updates to remote devices using a network connection)。尽管名称暗示无线连接,但通过有线连接(如以太网)接收的更新仍通常称为OTA更新 (Although the name implies a wireless connection, updates received over a wired connection (such as Ethernet) are still commonly referred to as OTA updates)。此方法需要服务器基础设施来托管固件二进制文件并实现在更新可用时发送信号的方法 (This approach requires server infrastructure to host the firmware binary and implement a method of signaling when an update is available)。安全性是OTA更新的一个关注点;固件二进制文件应在升级前进行加密签名和验证 (Security is a concern with OTA updates; firmware binaries should be cryptographically signed and verified before upgrading)。

:ref:`dfu` 部分讨论了使用MCUboot升级Zephyr固件 (The :ref:`dfu` section discusses upgrading Zephyr firmware using MCUboot)。相同的方法可以作为OTA的一部分使用 (The same method can be used as part of OTA)。二进制文件首先下载到未占用的代码分区,通常名为 ``slot1_partition``,然后使用 :ref:`mcuboot` 过程进行升级 (The binary is first downloaded into an unoccupied code partition, usually named ``slot1_partition``, then upgraded using the :ref:`mcuboot` process)。

OTA示例 (Examples of OTA)
**************************

Golioth
=======

`Golioth`_ 是一个包含OTA更新的IoT管理平台 (`Golioth`_ is an IoT management platform that includes OTA updates)。设备配置为观察Golioth Cloud上的可用固件版本 (Devices are configured to observe your available firmware revisions on the Golioth Cloud)。当新版本可用时,设备下载并烧写二进制文件 (When a new version is available, the device downloads and flashes the binary)。在此实现中,云和设备之间的连接使用TLS/DTLS进行保护,签名的固件二进制文件在升级发生前由MCUboot确认 (In this implementation, the connection between cloud and device is secured using TLS/DTLS, and the signed firmware binary is confirmed by MCUboot before the upgrade occurs)。

1. 可以在 `Golioth Firmware SDK repository`_ 找到一个工作示例 (A working sample can be found on the `Golioth Firmware SDK repository`_)
2. `Golioth OTA documentation`_ 包括有关版本控制过程的完整信息 (The `Golioth OTA documentation`_ includes complete information about the versioning process)

Eclipse hawkBit |trade|
=======================

`Eclipse hawkBit`_ |trade| 是一个更新服务器框架,它使用REST API轮询来检测固件更新 (`Eclipse hawkBit`_ |trade| is an update server framework that uses polling on a REST api to detect firmware updates)。当检测到新更新时,下载并安装二进制文件 (When a new update is detected, the binary is downloaded and installed)。MCUboot可用于在升级固件之前验证签名 (MCUboot can be used to verify the signature before upgrading the firmware)。

Zephyr的 :zephyr:code-sample-category:`mgmt` 部分包含一个 :zephyr:code-sample:`hawkbit-api` 示例 (There is a :zephyr:code-sample:`hawkbit-api` sample included in the Zephyr :zephyr:code-sample-category:`mgmt` section)。

UpdateHub
=========

`UpdateHub`_ 是一个用于远程更新嵌入式设备的平台 (`UpdateHub`_ is a platform for remotely updating embedded devices)。可以手动触发更新或通过轮询监控 (Updates can be manually triggered or monitored via polling)。当检测到新更新时,下载并安装二进制文件 (When a new update is detected, the binary is downloaded and installed)。MCUboot可用于在升级固件之前验证签名 (MCUboot can be used to verify the signature before upgrading the firmware)。

Zephyr的 :zephyr:code-sample-category:`mgmt` 部分包含一个 :zephyr:code-sample:`updatehub-fota` 示例 (There is an :zephyr:code-sample:`updatehub-fota` sample included in the Zephyr :zephyr:code-sample-category:`mgmt` section)。

SMP服务器 (SMP Server)
======================

简单管理协议(SMP)服务器可用于通过低功耗蓝牙(LE)或UDP更新固件 (A Simple Management Protocol (SMP) server can be used to update firmware via Bluetooth Low Energy (LE) or UDP)。:ref:`mcu_mgr` 用于将签名的固件二进制文件发送到远程设备,在升级发生前由MCUboot验证 (:ref:`mcu_mgr` is used to send a signed firmware binary to the remote device where it is verified by MCUboot before the upgrade occurs)。

Zephyr的 :zephyr:code-sample-category:`mgmt` 部分包含一个 :zephyr:code-sample:`smp-svr` 示例 (There is an :zephyr:code-sample:`smp-svr` sample included in the Zephyr :zephyr:code-sample-category:`mgmt` section)。

轻量级M2M (LWM2M) (Lightweight M2M (LWM2M))
===========================================

:ref:`lwm2m_interface` 协议通过 :kconfig:option:`CONFIG_LWM2M_FIRMWARE_UPDATE_OBJ_SUPPORT` 包含对固件更新的支持 (The :ref:`lwm2m_interface` protocol includes support for firmware update via :kconfig:option:`CONFIG_LWM2M_FIRMWARE_UPDATE_OBJ_SUPPORT`)。设备使用DTLS安全连接到LwM2M服务器 (Devices securely connect to an LwM2M server using DTLS)。有一个 :zephyr:code-sample:`lwm2m-client` 示例可用,但它没有演示固件更新功能 (A :zephyr:code-sample:`lwm2m-client` sample is available but it does not demonstrate the firmware update feature)。

.. _MCUboot bootloader: https://mcuboot.com/
.. _Golioth: https://golioth.io/
.. _Golioth Firmware SDK repository: https://github.com/golioth/golioth-firmware-sdk/tree/main/examples/zephyr/fw_update
.. _Golioth OTA documentation: https://docs.golioth.io/device-management/ota
.. _Eclipse hawkBit: https://www.eclipse.org/hawkbit/
.. _UpdateHub: https://updatehub.io/
