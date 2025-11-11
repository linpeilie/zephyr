.. _blinfo_api:

引导加载程序信息 (Bootloader Information)
##########################################

引导加载程序信息(缩写为 blinfo)子系统是 :ref:`retention_api` 的扩展,允许从引导加载程序读取共享数据并允许应用程序查询它。它具有一个可选功能,可以组织从引导加载程序检索的信息并将其存储在带有 ``blinfo/`` 前缀的 :ref:`settings_api` 中。(The bootloader information (abbreviated to blinfo) subsystem is an extension of the :ref:`retention_api` which allows for reading shared data from a bootloader and allowing applications to query it. It has an optional feature of organising the information retrieved from the bootloader and storing it in the :ref:`settings_api` with the ``blinfo/`` prefix.)

设备树设置 (Devicetree setup)
******************************

要使用引导加载程序信息子系统,需要创建一个保持区域,该区域以保持数据部分为父级,通常使用非初始化 RAM 用于此目的。请参阅以下示例(本指南中的示例基于 :zephyr:board:`nrf52840dk` 开发板和内存布局):(To use the bootloader information subsystem, a retention area needs to be created which has a retained data section as its parent, generally non-init RAM is used for this purpose. See the following example (examples in this guide are based on the :zephyr:board:`nrf52840dk` board and memory layout):)

.. code-block:: devicetree

	/ {
		sram@2003FC00 {
			compatible = "zephyr,memory-region", "mmio-sram";
			reg = <0x2003FC00 DT_SIZE_K(1)>;
			zephyr,memory-region = "RetainedMem";
			status = "okay";

			retainedmem {
				compatible = "zephyr,retained-ram";
				status = "okay";
				#address-cells = <1>;
				#size-cells = <1>;

				boot_info0: boot_info@0 {
					compatible = "zephyr,retention";
					status = "okay";
					reg = <0x0 0x100>;
				};
			};
		};

		chosen {
			zephyr,bootloader-info = &boot_info0;
		};
	};


	/* Reduce SRAM0 usage by 1KB to account for non-init area */
	&sram0 {
		reg = <0x20000000 DT_SIZE_K(255)>;
	};

请注意,此配置需要应用于引导加载程序(MCUboot)和应用程序才能使用。它可以与其他保持系统 API(如 :ref:`boot_mode_api`)结合使用。(Note that this configuration needs to be applied on both the bootloader (MCUboot) and application to be usable. It can be combined with other retention system APIs such as the :ref:`boot_mode_api`)

MCUboot 设置 (MCUboot setup)
*****************************

应用上述设备树配置后,需要配置 MCUboot 以将共享数据存储在此区域中,需要为此设置以下 Kconfig:(Once the above devicetree configuration is applied, MCUboot needs to be configured to store the shared data in this area, the following Kconfigs need to be set for this:)

* :kconfig:option:`CONFIG_RETAINED_MEM` - 启用保持内存驱动程序 (Enables retained memory driver)
* :kconfig:option:`CONFIG_RETENTION` - 启用保持系统 (Enables retention system)
* :kconfig:option:`CONFIG_BOOT_SHARE_DATA` - 启用共享数据 (Enables shared data)
* :kconfig:option:`CONFIG_BOOT_SHARE_DATA_BOOTINFO` - 启用启动信息共享数据类型 (Enables boot information shared data type)
* :kconfig:option:`CONFIG_BOOT_SHARE_BACKEND_RETENTION` - 使用保持/blinfo 子系统存储共享数据 (Stores shared data using retention/blinfo subsystem)

应用程序设置 (Application setup)
*********************************

应用程序必须启用以下基本 Kconfig 选项才能使引导加载程序信息子系统正常工作:(The application must enable the following base Kconfig options for the bootloader information subsystem to function:)

* :kconfig:option:`CONFIG_RETAINED_MEM`
* :kconfig:option:`CONFIG_RETENTION`
* :kconfig:option:`CONFIG_RETENTION_BOOTLOADER_INFO`
* :kconfig:option:`CONFIG_RETENTION_BOOTLOADER_INFO_TYPE_MCUBOOT`

使用引导加载程序信息子系统需要以下包含文件:(The following include is needed to use the bootloader information subsystem:)

.. code-block:: C

	#include <zephyr/retention/blinfo.h>

默认情况下,仅提供查找函数::c:func:`blinfo_lookup`,应用程序可以调用它来查询引导加载程序的信息。此功能默认使用 :kconfig:option:`CONFIG_RETENTION_BOOTLOADER_INFO_OUTPUT_FUNCTION` 启用,但是,应用程序可以选择使用设置存储功能。在此模式下,可以使用设置键查询引导加载程序信息,需要为此模式启用以下 Kconfig 选项:(By default, only the lookup function is provided: :c:func:`blinfo_lookup`, the application can call this to query the information from the bootloader. This function is enabled by default with :kconfig:option:`CONFIG_RETENTION_BOOTLOADER_INFO_OUTPUT_FUNCTION`, however, applications can optionally choose to use the settings storage feature instead. In this mode, the bootloader information can be queries by using settings keys, the following Kconfig options need to be enabled for this mode:)

* :kconfig:option:`CONFIG_SETTINGS`
* :kconfig:option:`CONFIG_SETTINGS_RUNTIME`
* :kconfig:option:`CONFIG_RETENTION_BOOTLOADER_INFO_OUTPUT_SETTINGS`

这允许通过 :c:func:`settings_runtime_get` 函数使用以下键查询信息:(This allows the information to be queried via the :c:func:`settings_runtime_get` function with the following keys:)

* ``blinfo/mode`` MCUboot 配置的模式(``enum mcuboot_mode`` 值) (The mode that MCUboot is configured for (``enum mcuboot_mode`` value))
* ``blinfo/signature_type`` MCUboot 配置的签名类型(``enum mcuboot_signature_type`` 值) (The signature type MCUboot is configured for (``enum mcuboot_signature_type`` value))
* ``blinfo/recovery`` MCUboot 中启用的恢复类型(``enum mcuboot_recovery_mode`` 值) (The recovery type enabled in MCUboot (``enum mcuboot_recovery_mode`` value))
* ``blinfo/running_slot`` 运行的插槽,对于直接 XIP 模式很有用,可以知道要用于更新的插槽 (The running slot, useful for direct-XIP mode to know which slot to use for an update)
* ``blinfo/bootloader_version`` 引导加载程序的版本(``struct image_version`` 对象) (Version of the bootloader (``struct image_version`` object))
* ``blinfo/max_application_size`` 可以加载的应用程序的最大大小(以字节为单位) (Maximum size of an application (in bytes) that can be loaded)

除了之前的包含文件外,此模式还需要以下包含文件:(In addition to the previous include, the following includes are required for this mode:)

.. code-block:: C

	#include <bootutil/boot_status.h>
	#include <bootutil/image.h>
	#include <zephyr/mcuboot_version.h>
	#include <zephyr/settings/settings.h>

API 参考 (API Reference)
*************************

引导加载程序信息 API (Bootloader information API)
==================================================

.. doxygengroup:: bootloader_info_interface
