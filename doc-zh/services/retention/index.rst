.. _retention_api:

保持系统 (Retention System)
############################

保持系统提供了一个 API,允许应用程序在设备供电时从保持数据的内存区域或设备读取和写入数据。这允许在不同应用程序之间或单个应用程序内共享信息,而不会在设备重启时丢失状态信息。存储的数据不应在断电事件中(或在某些设备的某些低功耗模式下)持久保存,也不应存储到非易失性存储器,如 :ref:`flash_api`、:ref:`eeprom_api` 或电池备份 RAM。(The retention system provides an API which allows applications to read and write data from and to memory areas or devices that retain the data while the device is powered. This allows for sharing information between different applications or within a single application without losing state information when a device reboots. The stored data should not persist in the event of a power failure (or during some low-power modes on some devices) nor should it be stored to a non-volatile storage like :ref:`flash_api`, :ref:`eeprom_api`, or battery-backed RAM.)

保持系统建立在保持数据驱动程序之上,并为其添加了额外的软件级功能以确保数据的有效性。可选地,可以使用魔术头来检查保持数据内存部分的前面是否包含此特定值,并且可以将数据的可选校验和(大小为 1、2 或 4 字节)附加到数据末尾。此外,保持系统 API 允许将保持数据部分划分为多个不同的区域。例如,64 字节的保持数据区域可以分为 4 字节用于启动模式、16 字节用于时间戳、44 字节用于最后的日志消息。所有这些部分都可以独立访问或更新。可以使用设备树为每个实例设置前缀和校验和。(The retention system builds on top of the retained data driver, and adds additional software-level features to it for ensuring the validity of data. Optionally, a magic header can be used to check if the front of the retained data memory section contains this specific value, and an optional checksum (1, 2, or 4-bytes in size) of the stored data can be appended to the end of the data. Additionally, the retention system API allows partitioning of the retained data sections into multiple distinct areas. For example, a 64-byte retained data area could be split up into 4 bytes for a boot mode, 16 bytes for a timestamp, 44 bytes for a last log message. All of these sections can be accessed or updated independently. The prefix and checksum can be set per-instance using devicetree.)

设备树设置 (Devicetree setup)
******************************

要使用保持系统,必须为您使用的开发板设置保持数据驱动程序,有一个 zephyr 驱动程序可以使用一些 RAM 作为非初始化数据用于此目的。然后将保持系统初始化为此设备的子节点 1 次或多次 - 请注意,内存区域需要减少以考虑这部分保留的 RAM。请参阅以下示例(本指南中的示例基于 :zephyr:board:`nrf52840dk` 开发板和内存布局):(To use the retention system, a retained data driver must be setup for the board you are using, there is a zephyr driver which can be used which will use some RAM as non-init for this purpose. The retention system is then initialised as a child node of this device 1 or more times - note that the memory region will need to be decremented to account for this reserved portion of RAM. See the following example (examples in this guide are based on the :zephyr:board:`nrf52840dk` board and memory layout):)

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

				/* This creates a 256-byte partition */
				retention0: retention@0 {
					compatible = "zephyr,retention";
					status = "okay";

					/* The total size of this area is 256
					 * bytes which includes the prefix and
					 * checksum, this means that the usable
					 * data storage area is 256 - 3 = 253
					 * bytes
					 */
					reg = <0x0 0x100>;

					/* This is the prefix which must appear
					 * at the front of the data
					 */
					prefix = [08 04];

					/* This uses a 1-byte checksum */
					checksum = <1>;
				};

				/* This creates a 768-byte partition */
				retention1: retention@100 {
					compatible = "zephyr,retention";
					status = "okay";

					/* Start position must be after the end
					 * of the previous partition. The total
					 * size of this area is 768 bytes which
					 * includes the prefix and checksum,
					 * this means that the usable data
					 * storage area is 768 - 6 = 762 bytes
					 */
					reg = <0x100 0x300>;

					/* This is the prefix which must appear
					 * at the front of the data
					 */
					prefix = [00 11 55 88 fa bc];

					/* If omitted, there will be no
					 * checksum
					 */
				};
			};
		};
	};

	/* Reduce SRAM0 usage by 1KB to account for non-init area */
	&sram0 {
		reg = <0x20000000 DT_SIZE_K(255)>;
	};

然后可以使用数据保持 API(一旦使用 :kconfig:option:`CONFIG_RETENTION` 启用,这需要启用 :kconfig:option:`CONFIG_RETAINED_MEM`)通过以下方式获取设备来访问保持区域:(The retention areas can then be accessed using the data retention API (once enabled with :kconfig:option:`CONFIG_RETENTION`, which requires that :kconfig:option:`CONFIG_RETAINED_MEM` be enabled) by getting the device by using:)

.. code-block:: C

	#include <zephyr/device.h>
	#include <zephyr/retention/retention.h>

	const struct device *retention0 = DEVICE_DT_GET(DT_NODELABEL(retention0));
	const struct device *retention1 = DEVICE_DT_GET(DT_NODELABEL(retention1));

当调用写入函数时,魔术头和校验和(如果启用)将在该区域上设置,并且从那时起该区域将被标记为有效。(When the write function is called, the magic header and checksum (if enabled) will be set on the area, and it will be marked as valid from that point onwards.)

互斥锁保护 (Mutex protection)
******************************

当应用程序使用多线程支持编译时,默认情况下会启用保持区域的互斥锁保护。这意味着不同的线程可以安全地调用保持函数,而不会与其他并发线程函数使用发生冲突,但这意味着保持函数不能在 ISR 中使用。可以通过启用 :kconfig:option:`CONFIG_RETENTION_MUTEX_FORCE_DISABLE` 在所有保持区域上全局禁用互斥锁保护 - 然后用户负责确保函数调用不会相互冲突。请注意,要使用此功能,还必须通过启用 :kconfig:option:`CONFIG_RETAINED_MEM_MUTEX_FORCE_DISABLE` 来禁用保持驱动程序互斥锁支持。(Mutex protection of retention areas is enabled by default when applications are compiled with multithreading support. This means that different threads can safely call the retention functions without clashing with other concurrent thread function usage, but means that retention functions cannot be used from ISRs. It is possible to disable mutex protection globally on all retention areas by enabling :kconfig:option:`CONFIG_RETENTION_MUTEX_FORCE_DISABLE` - users are then responsible for ensuring that the function calls do not conflict with each other. Note that to use this, retention driver mutex support must also be disabled by enabling :kconfig:option:`CONFIG_RETAINED_MEM_MUTEX_FORCE_DISABLE`.)

.. _boot_mode_api:

启动模式 (Boot mode)
*********************

保持子系统的一个附加功能是启动模式接口,当设备重启时,可以使用它动态更改应用程序的状态或使用最小的函数集运行不同的应用程序(一个例子是从主应用程序进入 mcuboot 的串行恢复功能的无按钮方式)。(An addition to the retention subsystem is a boot mode interface, this can be used to dynamically change the state of an application or run a different application with a minimal set of functions when a device is rebooted (an example is to have a buttonless way of entering mcuboot's serial recovery feature from the main application).)

要使用启动模式功能,设备树中必须存在一个数据保持条目,该条目专门用于启动模式选择(用户区域数据大小只需要一个字节),并且该区域需要分配给 ``zephyr,boot-mode`` 的 chosen 节点。请参阅以下示例:(To use the boot mode feature, a data retention entry must exist in the device tree, which is dedicated for use as the boot mode selection (the user area data size only needs to be a single byte), and this area be assigned to the chosen node of ``zephyr,boot-mode``. See the following example:)

.. code-block:: devicetree

	/ {
		sram@2003FFFF {
			compatible = "zephyr,memory-region", "mmio-sram";
			reg = <0x2003FFFF 0x1>;
			zephyr,memory-region = "RetainedMem";
			status = "okay";

			retainedmem {
				compatible = "zephyr,retained-ram";
				status = "okay";
				#address-cells = <1>;
				#size-cells = <1>;

				retention0: retention@0 {
					compatible = "zephyr,retention";
					status = "okay";
					reg = <0x0 0x1>;
				};
			};
		};

		chosen {
			zephyr,boot-mode = &retention0;
		};
	};

	/* Reduce SRAM0 usage by 1 byte to account for non-init area */
	&sram0 {
		reg = <0x20000000 0x3FFFF>;
	};

可以使用 :kconfig:option:`CONFIG_RETENTION_BOOT_MODE` 启用启动模式接口,然后使用启动模式函数访问。如果将 mcuboot 与串行恢复一起使用,可以在启用 ``CONFIG_MCUBOOT_SERIAL`` 和 ``CONFIG_BOOT_SERIAL_BOOT_MODE`` 的情况下构建它,这将允许使用以下方式直接重启进入串行恢复模式:(The boot mode interface can be enabled with :kconfig:option:`CONFIG_RETENTION_BOOT_MODE` and then accessed by using the boot mode functions. If using mcuboot with serial recovery, it can be built with ``CONFIG_MCUBOOT_SERIAL`` and ``CONFIG_BOOT_SERIAL_BOOT_MODE`` enabled which will allow rebooting directly into the serial recovery mode by using:)

.. code-block:: C

	#include <zephyr/retention/bootmode.h>
	#include <zephyr/sys/reboot.h>

	bootmode_set(BOOT_MODE_TYPE_BOOTLOADER);
	sys_reboot(0);

保持系统模块 (Retention system modules)
****************************************

模块可以通过将保持系统用作传输(例如在引导加载程序和应用程序之间)来扩展保持系统的功能。(Modules can expand the functionality of the retention system by using it as a transport (e.g. between a bootloader and application).)

.. toctree::
    :maxdepth: 1

    blinfo.rst

API 参考 (API Reference)
*************************

保持系统 API (Retention system API)
====================================

.. doxygengroup:: retention_api

启动模式接口 (Boot mode interface)
====================================

.. doxygengroup:: boot_mode_interface
