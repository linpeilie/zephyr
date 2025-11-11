.. _file_system_api:

文件系统 (File Systems)
########################

Zephyr RTOS虚拟文件系统交换机(VFS)允许应用程序在不同的挂载点挂载多个文件系统 (Zephyr RTOS Virtual Filesystem Switch (VFS) allows applications to mount multiple file systems at different mount points) (例如, ``/fatfs`` 和 ``/lfs`` (e.g., ``/fatfs`` and ``/lfs``))。挂载点数据结构包含实例化、挂载和操作文件系统所需的所有必要信息 (The mount point data structure contains all the necessary information required to instantiate, mount, and operate on a file system)。文件系统交换机通过引入文件系统注册机制 (The File system Switch decouples the applications from directly accessing an individual file system's specific API or internal functions by introducing file system registration mechanisms),将应用程序与直接访问单个文件系统的特定API或内部函数解耦 (decouples the applications from directly accessing an individual file system's specific API or internal functions)。

在Zephyr中,任何文件系统实现或库都可以通过文件系统注册API插入或拔出 (In Zephyr, any file system implementation or library can be plugged into or pulled out through a file system registration API)。每个文件系统实现必须具有全局唯一的整数标识符 (Each file system implementation must have a globally unique integer identifier);使用 :c:enumerator:`FS_TYPE_EXTERNAL_BASE` 以避免与树内标识符冲突 (use :c:enumerator:`FS_TYPE_EXTERNAL_BASE` to avoid clashes with in-tree identifiers)。

.. code-block:: c

        int fs_register(int type, const struct fs_file_system_t *fs);

        int fs_unregister(int type, const struct fs_file_system_t *fs);

Zephyr RTOS通过使用挂载点作为磁盘卷名来支持文件系统的多个实例 (Zephyr RTOS supports multiple instances of a file system by making use of the mount point as the disk volume name),文件系统库在格式化或挂载磁盘时使用该名称 (which is used by the file system library while formatting or mounting a disk)。

文件系统声明如下 (A file system is declared as):

.. code-block:: c

	static struct fs_mount_t mp = {
	.type = FS_FATFS,
	.mnt_point = FATFS_MNTP,
	.fs_data = &fat_fs,
	};

其中 (where)

- ``FS_FATFS`` 是文件系统类型,如FATFS或LittleFS (is the file system type like FATFS or LittleFS)。
- ``FATFS_MNTP`` 是文件系统将被挂载的挂载点 (is the mount point where the file system will be mounted)。
- ``fat_fs`` 是将被fs_mount() API使用的文件系统数据 (is the file system data which will be used by fs_mount() API)。



示例 (Samples)
***************

VFS的示例主要在 ``samples/subsys/fs`` 中提供 (Samples for the VFS are mainly supplied in ``samples/subsys/fs``),尽管在不同子系统的示例中也提供了VFS使用的各种示例作为重要功能 (although various examples of the VFS usage are provided as important functionalities in samples for different subsystems)。
以下是值得查看的示例列表 (Here is the list of samples worth looking at):

- :zephyr:code-sample:`fs` 是使用SDHC媒体的FAT文件系统使用示例 (is an example of FAT file system usage with SDHC media);
- :zephyr:code-sample:`shell-fs` 是Shell fs子系统的示例 (is an example of Shell fs subsystem),使用格式化为LittleFS的内部flash分区 (using internal flash partition formatted to LittleFS);
- :zephyr:code-sample:`usb-mass` 是USB大容量存储设备示例 (example of USB Mass Storage device),根据示例配置使用带有RAM或SPI连接的FLASH的FAT FS驱动程序,或flash中的LittleFS (that uses FAT FS driver with RAM or SPI connected FLASH, or LittleFS in flash, depending on the sample configuration)。

API参考 (API Reference)
************************

.. doxygengroup:: file_system_api
