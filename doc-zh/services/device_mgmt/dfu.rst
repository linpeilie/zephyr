.. _dfu:

设备固件升级 (Device Firmware Upgrade)
#######################################

概述 (Overview)
****************

设备固件升级子系统提供必要的框架,用于在运行时升级基于Zephyr的应用程序镜像 (The Device Firmware Upgrade subsystem provides the necessary frameworks to upgrade the image of a Zephyr-based application at run time)。它目前由两个不同的模块组成 (It currently consists of two different modules):

* :zephyr_file:`subsys/dfu/boot/`: 引导加载程序接口代码 (Interface code to bootloaders)
* :zephyr_file:`subsys/dfu/img_util/`: 镜像管理代码 (Image management code)

DFU子系统处理镜像管理,但不处理将镜像发送到目标设备所需的传输或管理协议本身 (The DFU subsystem deals with image management, but not with the transport or management protocols themselves required to send the image to the target device)。有关这些协议和框架的信息,请参阅 :ref:`device_mgmt` 部分 (For information on these protocols and frameworks please refer to the :ref:`device_mgmt` section)。

.. _flash_img_api:

Flash镜像 (Flash Image)
========================

Flash镜像API作为设备固件升级(DFU)子系统的一部分,在Flash Stream之上提供了一个抽象层,以简化将固件镜像块写入flash的操作 (The flash image API as part of the Device Firmware Upgrade (DFU) subsystem provides an abstraction on top of Flash Stream to simplify writing firmware image chunks to flash)。

API参考 (API Reference)
-----------------------

.. doxygengroup:: flash_img_api

.. _mcuboot_api:

MCUBoot API
===========

MCUboot API用于获取应用程序镜像的版本信息和启动状态 (The MCUboot API is provided to get version information and boot status of application images)。它允许为下次启动选择应用程序镜像和启动类型 (It allows to select application image and boot type for the next boot)。

API参考 (API Reference)
-----------------------

.. doxygengroup:: mcuboot_api

引导加载程序 (Bootloaders)
***************************

.. _mcuboot:

MCUboot
=======

Zephyr与开源的跨RTOS `MCUboot boot loader`_ 直接兼容 (Zephyr is directly compatible with the open source, cross-RTOS `MCUboot boot loader`_)。它与MCUboot交互并了解其所需的镜像格式,因此当MCUboot作为Zephyr的引导加载程序时,设备固件升级功能可用 (It interfaces with MCUboot and is aware of the image format required by it, so that Device Firmware Upgrade is available when MCUboot is the boot loader used with Zephyr)。源代码本身托管在 `MCUboot GitHub Project`_ 页面上 (The source code itself is hosted in the `MCUboot GitHub Project`_ page)。

为了将MCUboot与Zephyr一起使用,您需要考虑以下几点 (In order to use MCUboot with Zephyr you need to take the following into account):

1. 您需要定义MCUboot所需的flash分区;详情请参见 :ref:`flash_map_api` (You will need to define the flash partitions required by MCUboot; see :ref:`flash_map_api` for details)。
2. 您必须将flash分区指定为选定的代码分区 (You will have to specify your flash partition as the chosen code partition)

.. code-block:: devicetree

   / {
      chosen {
         zephyr,code-partition = &slot0_partition;
      };
   };

3. 您的应用程序的 :file:`.conf` 文件需要启用 :kconfig:option:`CONFIG_BOOTLOADER_MCUBOOT` Kconfig选项,以便以MCUboot兼容的方式构建Zephyr (Your application's :file:`.conf` file needs to enable the :kconfig:option:`CONFIG_BOOTLOADER_MCUBOOT` Kconfig option in order for Zephyr to be built in an MCUboot-compatible manner)
4. 您需要在设备上构建和烧写MCUboot本身 (You need to build and flash MCUboot itself on your device)
5. 您可能需要采取预防措施以避免大量擦除flash,并以正确的偏移量(紧跟在引导加载程序之后)烧写Zephyr应用程序镜像 (You might need to take precautions to avoid mass erasing the flash and also to flash the Zephyr application image at the correct offset (right after the bootloader))

有关将MCUboot与Zephyr一起使用的更详细信息,可以在MCUboot网站上的 `MCUboot with Zephyr`_ 文档页面中找到 (More detailed information regarding the use of MCUboot with Zephyr can be found in the `MCUboot with Zephyr`_ documentation page on the MCUboot website)。

.. _MCUboot boot loader: https://mcuboot.com/
.. _MCUboot with Zephyr: https://docs.mcuboot.com/readme-zephyr
.. _MCUboot GitHub Project: https://github.com/runtimeco/mcuboot
