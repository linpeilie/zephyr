.. _disk_access_api:

磁盘访问 (Disk Access)
#######################

概述 (Overview)
****************

磁盘访问 API 提供对存储设备的访问。(The disk access API provides access to storage devices.)

初始化磁盘 (Initializing Disks)
********************************

由于许多磁盘设备(如 SD 卡)是热插拔的,磁盘访问 API 提供 IOCTL 来初始化和反初始化磁盘。它们如下:(Since many disk devices (such as SD cards) are hotpluggable, the disk access API provides IOCTLs to initialize and de-initialize the disk. They are as follows:)

* :c:macro:`DISK_IOCTL_CTRL_INIT`: 初始化磁盘。必须在对磁盘设备运行其他 I/O 操作之前调用。等效于调用旧版函数 :c:func:`disk_access_init`。(Initialize the disk. Must be called before additional I/O operations can be run on the disk device. Equivalent to calling the legacy function :c:func:`disk_access_init`.)

* :c:macro:`DISK_IOCTL_CTRL_DEINIT`: 反初始化磁盘。一旦发出此 IOCTL,则必须在磁盘可用于其他 I/O 操作之前发出 :c:macro:`DISK_IOCTL_CTRL_INIT`。(De-initialize the disk. Once this IOCTL is issued, the :c:macro:`DISK_IOCTL_CTRL_INIT` must be issued before the disk can be used for addition I/O operations.)

Init/deinit IOCTL 调用是平衡的,因此磁盘不会反初始化,直到发出与 init IOCTL 数量相等的 deinit IOCTL。(Init/deinit IOCTL calls are balanced, so a disk will not de-initialize until an equal number of deinit IOCTLs have been issued as init IOCTLs.)

还可以通过将指向设置为 ``true`` 的布尔值的指针作为参数传递给 :c:macro:`DISK_IOCTL_CTRL_DEINIT` IOCTL 来强制磁盘反初始化。这是一个不安全的操作,每个磁盘驱动程序可能以不同方式处理,但它始终返回指示成功的值。(It is also possible to force a disk de-initialization by passing a pointer to a boolean set to ``true`` as a parameter to the :c:macro:`DISK_IOCTL_CTRL_DEINIT` IOCTL. This is an unsafe operation which each disk driver may handle differently, but it will always return a value indicating success.)

请注意,反初始化磁盘是一个低级操作 - 通常应将反初始化和初始化调用留给文件系统实现,用户应用程序不需要手动反初始化磁盘,而是可以调用 :c:func:`fs_unmount` (Note that de-initializing a disk is a low level operation- typically the de-initialization and initialization calls should be left to the filesystem implementation, and the user application should not need to manually de-initialize the disk and can instead call :c:func:`fs_unmount`)

SD 卡支持 (SD Card support)
****************************

Zephyr 支持一些 SD 卡控制器,并支持通过 SPI 接口 SD 卡。这些驱动程序使用磁盘驱动程序接口,文件系统可以通过磁盘访问 API 访问 SD 卡。支持标准和高容量 SD 卡。(Zephyr has support for some SD card controllers and support for interfacing SD cards via SPI. These drivers use disk driver interface and a file system can access the SD cards via disk access API. Both standard and high-capacity SD cards are supported.)

.. note:: FAT 文件系统不是电源安全的,因此如果断电或在未卸载文件系统的情况下移除卡,文件系统可能会损坏 (FAT filesystems are not power safe so the filesystem may become corrupted if power is lost or if the card is removed without unmounting the filesystem)

SD 存储卡子系统 (SD Memory Card subsystem)
===========================================

Zephyr 通过磁盘驱动程序 API 或通过 SDMMC 子系统支持 SD 存储卡。此子系统可以通过磁盘驱动程序 API 透明使用,但也支持对卡的直接块级访问。SDMMC 子系统与 :ref:`sd 主机控制器 api <sdhc_api>` 交互以与连接的 SD 卡通信。(Zephyr supports SD memory cards via the disk driver API, or via the SDMMC subsystem. This subsystem can be used transparently via the disk driver API, but also supports direct block level access to cards. The SDMMC subsystem interacts with the :ref:`sd host controller api <sdhc_api>` to communicate with attached SD cards.)


通过 SPI 的 SD 卡支持 (SD Card support via SPI)
================================================

下面的示例设备树片段显示了如何将 SD 卡节点添加到 ``spi1`` 接口。示例使用引脚 ``PA27`` 作为片选,并在 SD 卡初始化后以 24 MHz 运行 SPI 总线:(Example devicetree fragment below shows how to add SD card node to ``spi1`` interface. Example uses pin ``PA27`` for chip select, and runs the SPI bus at 24 MHz once the SD card has been initialized:)

.. code-block:: devicetree

    &spi1 {
            status = "okay";
            cs-gpios = <&porta 27 GPIO_ACTIVE_LOW>;

            sdhc0: sdhc@0 {
		    compatible = "zephyr,sdhc-spi-slot";
                    reg = <0>;
                    status = "okay";
		    mmc {
			compatible = "zephyr,sdmmc-disk";
                        disk-name = "SD";
			status = "okay";
		    };
                    spi-max-frequency = <24000000>;
            };
    };

SD 卡将在开发板启动时由文件系统驱动程序自动检测和初始化。(The SD card will be automatically detected and initialized by the filesystem driver when the board boots.)

要读取和写入文件和目录,请参阅 :zephyr_file:`include/zephyr/fs/fs.h` 中的 :ref:`file_system_api`,例如 :c:func:`fs_open()`、:c:func:`fs_read()` 和 :c:func:`fs_write()`。(To read and write files and directories, see the :ref:`file_system_api` in :zephyr_file:`include/zephyr/fs/fs.h` such as :c:func:`fs_open()`, :c:func:`fs_read()`, and :c:func:`fs_write()`.)

eMMC 设备支持 (eMMC Device Support)
************************************

Zephyr 还支持使用磁盘访问 API 的 eMMC 设备。Zephyr 中的 MMC 是使用 SD 子系统实现的,因为 MMC 总线与 SD 总线有很多相似之处。MMC 控制器也使用 SDHC 设备驱动程序 API。(Zephyr also has support for eMMC devices using the Disk Access API. MMC in zephyr is implemented using the SD subsystem because the MMC bus shares a lot of similarity with the SD bus. MMC controllers also use the SDHC device driver API.)

闪存分区上的模拟块设备支持 (Emulated block device on flash partition support)
******************************************************************************

Zephyr flashdisk 驱动程序可以将闪存分区用作块设备。flashdisk 实例在设备树中定义:(Zephyr flashdisk driver makes it possible to use flash memory partition as a block device. The flashdisk instances are defined in devicetree:)

.. code-block:: devicetree

    / {
        msc_disk0 {
            compatible = "zephyr,flash-disk";
            partition = <&storage_partition>;
            disk-name = "NAND";
            cache-size = <4096>;
        };
    };

在 :dtcompatible:`zephyr,flash-disk` 节点中指定的缓存大小应等于支持分区的最小可擦除块大小。(The cache size specified in :dtcompatible:`zephyr,flash-disk` node should be equal to backing partition minimum erasable block size.)

NVMe 磁盘支持 (NVMe disk support)
==================================

也支持 NVMe 磁盘 (NVMe disks are also supported)

.. toctree::
    :maxdepth: 1

    nvme.rst


磁盘访问 API 配置选项 (Disk Access API Configuration Options)
***************************************************************

相关配置选项:(Related configuration options:)

* :kconfig:option:`CONFIG_DISK_ACCESS`

API 参考 (API Reference)
*************************

.. doxygengroup:: disk_access_interface

磁盘驱动程序配置选项 (Disk Driver Configuration Options)
**********************************************************

相关驱动程序配置选项:(Related driver configuration options:)

* :kconfig:option:`CONFIG_DISK_DRIVERS`

磁盘驱动程序接口 (Disk Driver Interface)
*****************************************

.. doxygengroup:: disk_driver_interface
