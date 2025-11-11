.. _disk_nvme:

NVMe
####

NVMe 是 PCIe 总线上的标准化逻辑设备接口,用于公开存储设备。(NVMe is a standardized logical device interface on PCIe bus exposing storage devices.)

支持 NVMe 控制器和磁盘。可以通过它们公开的 :ref:`磁盘访问 API <disk_access_api>` 访问磁盘,从而通过 :ref:`文件系统 API <file_system_api>` 使用。(NVMe controllers and disks are supported. Disks can be accessed via the :ref:`Disk Access API <disk_access_api>` they expose and thus be used through the :ref:`File System API <file_system_api>`.)

驱动程序设计 (Driver design)
*****************************

驱动程序分为 3 个主要部分:(The driver is sliced up in 3 main parts:)

- NVMe 控制器 (NVMe controller): :zephyr_file:`drivers/disk/nvme/nvme_controller.c`
- NVMe 命令 (NVMe commands): :zephyr_file:`drivers/disk/nvme/nvme_cmd.c`
- NVMe 命名空间 (NVMe namespace): :zephyr_file:`drivers/disk/nvme/nvme_namespace.c`

其中 NVMe 控制器是设备驱动程序的根。这是将获得设备驱动程序实例的那个。请注意,这只是 DTS 描述的内容:NVMe 控制器,而不是它的命名空间(磁盘)。NVMe 命令是用于与控制器及其公开的命名空间通信的通用逻辑。最后,NVMe 命名空间是处理实际命名空间的专用部分,该部分反过来使应用程序能够通过磁盘访问 API :zephyr_file:`drivers/disk/nvme/nvme_disk.c` 访问每个命名空间。(Where the NVMe controller is the root of the device driver. This is the one that will get device driver instances. Note that this is only what DTS describes: the NVMe controller, and none of its namespaces (disks). The NVMe command is the generic logic used to communicate with the controller and the namespaces it exposes. Finally the NVMe namespace is the dedicated part to deal with an actual namespace which, in turn, enables applications accessing each ones through the Disk Access API :zephyr_file:`drivers/disk/nvme/nvme_disk.c`.)

如果控制器公开多个命名空间(磁盘),则可以通过调整配置选项 CONFIG_NVME_MAX_NAMESPACES(见下文)来增加内置命名空间支持的数量。(If a controller exposes more than 1 namespace (disk), it will be possible to raise the amount of built-in namespace support by tweaking the configuration option CONFIG_NVME_MAX_NAMESPACES (see below).)

通过其相关的 disk_info 结构公开的每个磁盘将通过其名称进行区分,该名称继承自其相关的命名空间。因此,磁盘名称遵循 NVMe 命名,即 nvme<k>n<n>,其中 k 是控制器编号,n 是命名空间编号。大多数情况下,如果系统中只插入了一个 NVMe 磁盘,您将看到 'nvme0n0' 作为公开的磁盘。(Each exposed disk, via it's related disk_info structure, will be distinguished by its name which is inherited from it's related namespace. As such, the disk name follows NVMe naming which is nvme<k>n<n> where k is the controller number and n the namespame number. Most of the time, if only one NVMe disk is plugged into the system, one will see 'nvme0n0' as an exposed disk.)

NVMe 配置 (NVMe configuration)
******************************

DTS
===

任何公开 NVMe 磁盘的开发板都应提供 DTS 覆盖以在 Zephyr 中启用其使用 (Any board exposing an NVMe disk should provide a DTS overlay to enable its use within Zephyr)

.. code-block:: devicetree

    #include <zephyr/dt-bindings/pcie/pcie.h>
    / {
        pcie0 {
            nvme0: nvme0 {
                compatible = "nvme-controller";
                vendor-id = <VENDOR_ID>;
                device-id = <DEVICE_ID>;
                status = "okay";
            };
        };
    };

其中 VENDOR_ID 和 DEVICE_ID 是来自公开的 NVMe 控制器的。(Where VENDOR_ID and DEVICE_ID are the ones from the exposed NVMe controller.)

选项 (Options)
===============

* :kconfig:option:`CONFIG_NVME`

请注意,NVME 要求目标支持 PCIe 多向量 MSI-X 才能正常工作。(Note that NVME requires the target to support PCIe multi-vector MSI-X in order to function.)

* :kconfig:option:`CONFIG_NVME_MAX_NAMESPACES`

用户重要注意事项 (Important note for users)
*******************************************

NVMe 规范要求数据缓冲区放置在双字(4 字节)对齐的地址中。虽然这对于管理虚拟内存和用户进程下动态分配的高级操作系统来说不是问题,但在 Zephyr 中,一旦缓冲区地址直接映射到物理内存,这可能会成为问题。(NVMe specifications mandate the data buffer to be placed in a dword (4 bytes) aligned address. While this is not a problem for advanced OS managing virtual memory and dynamic allocations below the user processes, this can become an issue in Zephyr as soon as buffer addresses map directly to physical memory.)

因此,在此阶段,用户需要确保提供给 :c:func:`disk_access_read` 和 :c:func:`disk_access_write` 的缓冲区地址是双字对齐的。(At this stage then, it is up to the user to make sure the buffer address being provided to :c:func:`disk_access_read` and :c:func:`disk_access_write` are dword aligned.)
