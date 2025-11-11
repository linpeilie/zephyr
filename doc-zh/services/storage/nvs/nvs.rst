.. _nvs_api:

非易失性存储 (Non-Volatile Storage, NVS)
#########################################

元素表示为 id-data 对,使用 FIFO 管理的循环缓冲区存储在闪存中。闪存区域被划分为扇区。元素被追加到扇区,直到扇区中的存储空间耗尽。然后准备闪存区域中的新扇区以供使用(擦除)。在擦除扇区之前,检查使用中的扇区中是否存在标识符-数据对,如果不存在,则复制 id-data 对。(Elements, represented as id-data pairs, are stored in flash using a FIFO-managed circular buffer. The flash area is divided into sectors. Elements are appended to a sector until storage space in the sector is exhausted. Then a new sector in the flash area is prepared for use (erased). Before erasing the sector it is checked that identifier - data pairs exist in the sectors in use, if not the id-data pair is copied.)

id 是一个 16 位无符号数。NVS 确保对于每个使用的 id,闪存中始终至少存储一个 id-data 对。(The id is a 16-bit unsigned number. NVS ensures that for each used id there is at least one id-data pair stored in flash at all time.)

NVS 允许存储二进制 blob、字符串、整数、长整型以及这些的任意组合。(NVS allows storage of binary blobs, strings, integers, longs, and any combination of these.)

每个元素在闪存中存储为元数据(8 字节)和数据。元数据写入从 nvs 扇区末尾开始的表中,数据从扇区开头依次写入。元数据包括:id、扇区中的数据偏移量、数据长度、part(未使用)和 CRC。此 CRC 仅在元数据上计算,仅确保写入已完成。元素的实际数据可以由不同的(可选的)CRC-32 保护。使用 :kconfig:option:`CONFIG_NVS_DATA_CRC` 配置项启用数据部分 CRC。(Each element is stored in flash as metadata (8 byte) and data. The metadata is written in a table starting from the end of a nvs sector, the data is written one after the other from the start of the sector. The metadata consists of: id, data offset in sector, data length, part (unused), and a CRC. This CRC is only calculated over the metadata and only ensures that a write has been completed. The actual data of the element can be protected by a different (and optional) CRC-32. Use the :kconfig:option:`CONFIG_NVS_DATA_CRC` configuration item to enable the data part CRC.)

.. note:: 仅当读取元素的全部数据时才检查数据 CRC。部分读取不检查数据 CRC,因为它存储在元素数据区域的末尾。(The data CRC is checked only when the whole data of the element is read. The data CRC is not checked for a partial read, as it is stored at the end of the element data area.)

.. note:: 在以前不带数据 CRC 的 NVS 内容上启用数据 CRC 功能将使所有现有数据无效。(Enabling the data CRC feature on a previously existing NVS content without data CRC will make all existing data invalid.)

向 nvs 写入数据总是从写入数据开始,然后写入元数据。在闪存中写入的没有元数据的数据在初始化期间被忽略。(A write of data to nvs always starts with writing the data, followed by a write of the metadata. Data that is written in flash without metadata is ignored during initialization.)

在初始化期间,NVS 将验证存储在闪存中的数据,如果遇到错误,它将忽略任何缺少/不正确元数据的数据。(During initialization NVS will verify the data stored in flash, if it encounters an error it will ignore any data with missing/incorrect metadata.)

NVS 在将数据写入闪存之前检查 id-data 对。如果 id-data 对未更改,则不执行闪存写入。(NVS checks the id-data pair before writing data to flash. If the id-data pair is unchanged no write to flash is performed.)

为了保护闪存区域免受频繁擦除,有足够的可用空间很重要。NVS 有一个保护机制,可以避免在可用空间有限时陷入闪存页面擦除的无限循环。当检测到这样的循环时,NVS 返回没有更多可用空间。(To protect the flash area against frequent erases it is important that there is sufficient free space. NVS has a protection mechanism to avoid getting in a endless loop of flash page erases when there is limited free space. When such a loop is detected NVS returns that there is no more space available.)

对于 NVS,文件系统声明为:(For NVS the file system is declared as:)

.. code-block:: c

	static struct nvs_fs fs = {
	.flash_device = NVS_FLASH_DEVICE,
	.sector_size = NVS_SECTOR_SIZE,
	.sector_count = NVS_SECTOR_COUNT,
	.offset = NVS_STORAGE_OFFSET,
	};

其中 (where)

- ``NVS_FLASH_DEVICE`` 是对将使用的闪存设备的引用。设备需要可操作。(is a reference to the flash device that will be used. The device needs to be operational.)
- ``NVS_SECTOR_SIZE`` 是扇区大小,它必须是闪存擦除页面大小的倍数和 2 的幂。(is the sector size, it has to be a multiple of the flash erase page size and a power of 2.)
- ``NVS_SECTOR_COUNT`` 是扇区数,至少为 2,始终保留一个空扇区以允许复制现有数据。(is the number of sectors, it is at least 2, one sector is always kept empty to allow copying of existing data.)
- ``NVS_STORAGE_OFFSET`` 是闪存中存储区域的偏移量。(is the offset of the storage area in flash.)


闪存磨损 (Flash wear)
**********************

向闪存写入数据时,闪存磨损研究很重要。闪存的寿命有限,由闪存可以擦除的次数决定。闪存一次擦除一页,页面大小由硬件决定。例如,nRF51822 设备的页面大小为 1024 字节,每页可擦除约 20,000 次。(When writing data to flash a study of the flash wear is important. Flash has a limited life which is determined by the number of times flash can be erased. Flash is erased one page at a time and the pagesize is determined by the hardware. As an example a nRF51822 device has a pagesize of 1024 bytes and each page can be erased about 20,000 times.)

计算预期设备寿命 (Calculating expected device lifetime)
========================================================

假设我们使用每分钟更改一次的 4 字节状态变量,并且需要在重启后恢复。NVS 已定义 sector_size 等于页面大小(1024 字节),并且已定义 2 个扇区。(Suppose we use a 4 bytes state variable that is changed every minute and needs to be restored after reboot. NVS has been defined with a sector_size equal to the pagesize (1024 bytes) and 2 sectors have been defined.)

状态变量的每次写入需要 12 字节的闪存存储:8 字节用于元数据,4 字节用于数据。存储数据时,第一个扇区将在 1024/12 = 85.33 分钟后满。再过 85.33 分钟后,第二个扇区满。当这种情况发生时,因为我们只使用两个扇区,第一个扇区将用于存储,并将在系统时间 171 分钟后擦除。预期设备寿命为 20,000 次写入,两个扇区每 171 分钟写入一次,设备应持续约 171 * 20,000 分钟,或约 6.5 年。(Each write of the state variable requires 12 bytes of flash storage: 8 bytes for the metadata and 4 bytes for the data. When storing the data the first sector will be full after 1024/12 = 85.33 minutes. After another 85.33 minutes, the second sector is full. When this happens, because we're using only two sectors, the first sector will be used for storage and will be erased after 171 minutes of system time. With the expected device life of 20,000 writes, with two sectors writing every 171 minutes, the device should last about 171 * 20,000 minutes, or about 6.5 years.)

更一般地,使用 (More generally then, with)

- ``NS`` 作为每分钟的存储请求数,(as the number of storage requests per minute,)
- ``DS`` 作为数据大小(字节),(as the data size in bytes,)
- ``SECTOR_SIZE`` (字节),和 (in bytes, and)
- ``PAGE_ERASES`` 作为页面可以擦除的次数,(as the number of times the page can be erased,)

预期设备寿命(分钟)可以计算为::(the expected device life (in minutes) can be calculated as::)

   SECTOR_COUNT * SECTOR_SIZE * PAGE_ERASES / (NS * (DS+8)) minutes

从这个公式也可以清楚地看到,如果预期寿命太短该怎么做:增加 ``SECTOR_COUNT`` 或 ``SECTOR_SIZE``。(From this formula it is also clear what to do in case the expected life is too short: increase ``SECTOR_COUNT`` or ``SECTOR_SIZE``.)

闪存写入块大小迁移 (Flash write block size migration)
*****************************************************
在 DFU 过程中,NVS 使用的闪存驱动程序可能会更改支持的最小写入块大小。除非物理 ATE 大小改变,否则 NVS 闪存映像将保持兼容。特别是,允许在 1、2、4、8 字节写入块大小之间迁移。(It is possible that during a DFU process, the flash driver used by the NVS changes the supported minimal write block size. The NVS in-flash image will stay compatible unless the physical ATE size changes. Especially, migration between 1,2,4,8-bytes write block sizes is allowed.)

示例 (Sample)
**************

``samples/subsys/nvs`` 中提供了如何使用 NVS 的示例。(A sample of how NVS can be used is supplied in ``samples/subsys/nvs``.)

故障排除 (Troubleshooting)
***************************

使用 NVS 时出现 MPU 故障,或返回 ``-ETIMEDOUT`` 错误 (MPU fault while using NVS, or ``-ETIMEDOUT`` error returned)
   NVS 可以使用 SoC 的内部闪存。当 MPU 启用时,闪存驱动程序需要使用 :kconfig:option:`CONFIG_MPU_ALLOW_FLASH_WRITE` 配置的对闪存的 MPU RWX 访问权限。如果禁用此选项,NVS 应用程序如果引用内部 SoC 闪存并且它是唯一运行的线程,将获得 MPU 故障。在多线程应用程序中,另一个线程可能会拦截故障,NVS API 将返回 ``-ETIMEDOUT`` 错误。(NVS can use the internal flash of the SoC. While the MPU is enabled, the flash driver requires MPU RWX access to flash memory, configured using :kconfig:option:`CONFIG_MPU_ALLOW_FLASH_WRITE`. If this option is disabled, the NVS application will get an MPU fault if it references the internal SoC flash and it's the only thread running. In a multi-threaded application, another thread might intercept the fault and the NVS API will return an ``-ETIMEDOUT`` error.)


API 参考 (API Reference)
*************************

NVS 子系统 API 由 ``nvs.h`` 提供:(The NVS subsystem APIs are provided by ``nvs.h``:)

.. doxygengroup:: nvs_data_structures

.. doxygengroup:: nvs_high_level_api

.. comment
   not documenting
   .. doxygengroup:: nvs
