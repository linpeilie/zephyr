.. _zms_api:

Zephyr 内存存储 (Zephyr Memory Storage, ZMS)
#############################################

Zephyr 内存存储是一个新的键值存储系统,旨在与所有类型的非易失性存储技术配合使用。它支持经典的片上 NOR 闪存以及像 RRAM 和 MRAM 这样不需要单独擦除操作的新技术,也就是说,这些类型设备上的数据可以随时直接覆盖。(Zephyr Memory Storage is a new key-value storage system that is designed to work with all types of non-volatile storage technologies. It supports classical on-chip NOR flash as well as new technologies like RRAM and MRAM that do not require a separate erase operation at all, that is, data on these types of devices can be overwritten directly at any time.)

通用行为 (General behavior)
****************************

ZMS 将内存空间划分为扇区(最少 2 个),每个扇区都填充键值对,直到它满为止。(ZMS divides the memory space into sectors (minimum 2), and each sector is filled with key-value pairs until it is full.)

键值对分为两部分:(The key-value pair is divided into two parts:)

- 键部分写入称为 "ID-ATE" 的 ATE(分配表条目,Allocation Table Entry)中,从扇区底部开始存储。(The key part is written in an ATE (Allocation Table Entry) called "ID-ATE" which is stored starting from the bottom of the sector.)
- 值部分定义为 "数据",从扇区顶部开始原始存储。(The value part is defined as "data" and is stored raw starting from the top of the sector.)

此外,对于每个扇区,我们在最后位置存储头部 ATE,这些 ATE 是扇区描述其状态(关闭、打开)和 ZMS 当前版本所需的。(Additionally, for each sector we store at the last positions header ATEs which are ATEs that are needed for the sector to describe its status (closed, open) and the current version of ZMS.)

当当前扇区满时,我们首先验证下一个扇区是否为空,通过将有效的 ATE 移动到 N+1 空扇区来垃圾收集扇区 N+2(其中 N 是当前扇区编号),擦除垃圾收集的扇区,然后通过写入 garbage_collect_done ATE 和 close ATE(头部条目之一)来关闭当前扇区。之后,我们前进到下一个扇区并再次开始写入条目。(When the current sector is full we verify first that the following sector is empty, we garbage collect the sector N+2 (where N is the current sector number) by moving the valid ATEs to the N+1 empty sector, we erase the garbage-collected sector and then we close the current sector by writing a garbage_collect_done ATE and the close ATE (one of the header entries). Afterwards we move forward to the next sector and start writing entries again.)

重复此行为直到到达分区末尾。然后在垃圾收集并擦除其内容后,从第一个扇区重新开始。(This behavior is repeated until it reaches the end of the partition. Then it starts again from the first sector after garbage collecting it and erasing its content.)

扇区的组成 (Composition of a sector)
=====================================

扇区以这种形式组织(3 个扇区的示例):(A sector is organized in this form (example with 3 sectors):)

.. list-table::
   :widths: 25 25 25
   :header-rows: 1

   * - Sector 0 (closed)
     - Sector 1 (open)
     - Sector 2 (empty)
   * - Data_a0
     - Data_b0
     - Data_c0
   * - Data_a1
     - Data_b1
     - Data_c1
   * - Data_a2
     - Data_b2
     - Data_c2
   * - GC_done
     -    .
     -    .
   * -    .
     -    .
     -    .
   * -    .
     -    .
     -    .
   * -    .
     - ID ATE_b2
     - ID ATE_c2
   * - ID ATE_a2
     - ID ATE_b1
     - ID ATE_c1
   * - ID ATE_a1
     - ID ATE_b0
     - ID ATE_c0
   * - ID ATE_a0
     - GC_done ATE
     - GC_done ATE
   * - Close ATE (cyc=1)
     - Close ATE (cyc=1)
     - Close ATE (cyc=1)
   * - Empty ATE (cyc=1)
     - Empty ATE (cyc=2)
     - Empty ATE (cyc=2)

扇区中每个元素的定义 (Definition of each element in the sector)
================================================================

``Empty ATE`` 在擦除扇区时写入(扇区的最后位置)。(``Empty ATE`` is written when erasing a sector (last position of the sector).)

``Close ATE`` 在关闭扇区时写入(扇区的倒数第二个位置)。(``Close ATE`` is written when closing a sector (second to last position of the sector).)

``GC_done ATE`` 写入以表明下一个扇区已被垃圾收集。此 ATE 可以在扇区的任何位置。(``GC_done ATE`` is written to indicate that the next sector has already been garbage-collected. This ATE could be at any position of the sector.)

``ID ATE`` 包含类型为 :c:type:`zms_id_t` 的键,并描述数据存储位置、大小和 CRC32。(``ID ATE`` contains a key of type :c:type:`zms_id_t` and describes where the data is stored, its size and its CRC32.)

``Data`` 是与 ID-ATE 关联的实际值。(``Data`` is the actual value associated to the ID-ATE.)

ZMS 如何工作? (How does ZMS work?)
***********************************

挂载存储系统 (Mounting the storage system)
===========================================

挂载存储系统首先获取闪存参数,检查文件系统属性是否正确(sector_size、sector_count ...),然后调用 zms_init 函数使存储准备就绪。(Mounting the storage system starts by getting the flash parameters, checking that the file system properties are correct (sector_size, sector_count ...) then calling the zms_init function to make the storage ready.)

要挂载文件系统,必须初始化 :c:struct:`zms_fs` 结构中的以下元素:(To mount the filesystem the following elements in the :c:struct:`zms_fs` structure must be initialized:)

.. code-block:: c

	struct zms_fs {
		/** File system offset in flash **/
		off_t offset;

		/** Storage system is split into sectors, each sector size must be multiple of
		 * erase-blocks if the device has erase capabilities
		 */
		uint32_t sector_size;
		/** Number of sectors in the file system */
		uint32_t sector_count;

		/** Flash device runtime structure */
		const struct device *flash_device;
	};

初始化 (Initialization)
========================

由于 ZMS 具有快进写入机制,它必须找到上次停止时的最后一个扇区和条目的最后一个指针。它必须寻找一个关闭的扇区后跟一个打开的扇区,然后在打开的扇区内,它找到(恢复)最后写入的 ATE。之后,它检查此扇区之后的扇区是否为空,否则将擦除它。(As ZMS has a fast-forward write mechanism, it must find the last sector and the last pointer of the entry where it stopped the last time. It must look for a closed sector followed by an open one, then within the open sector, it finds (recovers) the last written ATE. After that, it checks that the sector after this one is empty, or it will erase it.)

ZMS ID/数据写入 (ZMS ID/data write)
====================================

为了避免使用相同的 ID 再次重写相同的数据,ZMS 必须查看所有扇区中是否存在相同的 ID,然后比较其数据。如果数据相同,则不执行写入。如果必须执行写入,则在扇区中写入 ATE 和数据(如果操作不是删除)。如果扇区已满(无法容纳当前数据 + ATE),ZMS 必须移动到下一个扇区,垃圾收集新打开扇区之后的扇区,然后擦除它。(To avoid rewriting the same data with the same ID again, ZMS must look in all the sectors if the same ID exists and then compares its data. If the data is identical, no write is performed. If it must perform a write, then an ATE and the data (if the operation is not a delete) are written in the sector. If the sector is full (cannot hold the current data + ATE), ZMS has to move to the next sector, garbage collect the sector after the newly opened one then erase it.)

ZMS ID/数据读取(带历史记录) (ZMS ID/data read (with history))
=============================================================

默认情况下,ZMS 通过从最近的 ATE 到最旧的 ATE 浏览所有存储的 ATE 来查找具有相同 ID 的最后数据。如果找到具有匹配 ID 的有效 ATE,它将检索其数据并返回读取的字节数。如果提供了历史计数且不等于 0,则检索具有相同 ID 的较旧数据。(By default ZMS looks for the last data with the same ID by browsing through all stored ATEs from the most recent ones to the oldest ones. If it finds a valid ATE with a matching ID it retrieves its data and returns the number of bytes that were read. If a history count is provided and different than 0, older data with same ID is retrieved.)

ZMS 可用空间计算 (ZMS free space calculation)
==============================================

ZMS 还可以返回分区中剩余的可用空间。但是,此操作非常耗时,因为它需要浏览分区所有扇区中的所有有效 ATE,并且对于每个有效 ATE,尝试查找是否存在较旧的 ATE。不建议应用程序经常使用此函数,因为它很耗时,可能会减慢调用线程的速度。(ZMS can also return the free space remaining in the partition. However, this operation is very time-consuming as it needs to browse through all valid ATEs in all sectors of the partition and for each valid ATE try to find if an older one exists. It is not recommended for applications to use this function often, as it is time-consuming and could slow down the calling thread.)

循环计数器 (The cycle counter)
===============================

每个扇区都有一个前导循环计数器,它是一个 ``uint8_t``,用于验证所有其他 ATE。前导循环计数器存储在空 ATE 中。要变为有效,ATE 必须具有与空 ATE 中存储的循环计数器相同的循环计数器。每次将 ATE 从一个扇区移动到另一个扇区时,它必须获取目标扇区的循环计数器。要擦除扇区,空 ATE 的循环计数器会递增,并执行空 ATE 的单次写入。该扇区中的所有 ATE 都将无效。(Each sector has a lead cycle counter which is a ``uint8_t`` that is used to validate all the other ATEs. The lead cycle counter is stored in the empty ATE. To become valid, an ATE must have the same cycle counter as the one stored in the empty ATE. Each time an ATE is moved from a sector to another it must get the cycle counter of the destination sector. To erase a sector, the cycle counter of the empty ATE is incremented and a single write of the empty ATE is done. All the ATEs in that sector become invalid.)

关闭扇区 (Closing sectors)
===========================

要关闭扇区,在扇区末尾添加一个关闭 ATE,它必须具有与空 ATE 相同的循环计数器。关闭扇区时,所有未使用的剩余空间都用垃圾数据填充,以避免具有有效循环计数器的旧 ATE。(To close a sector a close ATE is added at the end of the sector and it must have the same cycle counter as the empty ATE. When closing a sector, all the remaining space that has not been used is filled with garbage data to avoid having old ATEs with a valid cycle counter.)

触发垃圾收集 (Triggering garbage collection)
=============================================

某些应用程序需要确保存储写入具有定义的最大延迟。调用 ZMS 进行写入时,当前扇区可能几乎已满,因此 ZMS 需要触发 GC 以切换到下一个扇区。此操作很耗时,将导致某些应用程序无法满足其实时约束。ZMS 添加了一个 API,供应用程序获取扇区中当前剩余的可用空间。如果当前扇区几乎已满,应用程序可以决定何时切换到下一个扇区。这当然会触发下一个扇区的垃圾收集操作。这将保证应用程序下一次写入不会触发垃圾收集。(Some applications need to make sure that storage writes have a maximum defined latency. When calling ZMS to make a write, the current sector could be almost full such that ZMS needs to trigger the GC to switch to the next sector. This operation is time-consuming and will cause some applications to not meet their real time constraints. ZMS adds an API for the application to get the current remaining free space in a sector. The application could then decide when to switch to the next sector if the current one is almost full. This will of course trigger the garbage collection operation on the next sector. This will guarantee the application that the next write won't trigger the garbage collection.)

ATE(分配表条目)结构 (ATE (Allocation Table Entry) structure)
=============================================================

一个条目使用 16 字节来编码其信息。确切的结构由 ATE 格式确定,可以为给定的应用程序选择该格式。(An entry uses 16 bytes to encode its information. The exact structure is determined by ATE format which can be selected for a given application.)

ZMS 定义了针对不同功能集定制的多种 ATE 格式。在运行时,它使用空 ATE 中的元数据字段识别格式,该字段在所有格式中具有相同的字节位置。(ZMS defines multiple ATE formats tailored for different feature sets. At runtime, it recognizes the format using the metadata field in empty ATEs, which has the same byte position in all formats.)

.. table:: 32 位 ID 的条目格式 (Entry format for 32-bit IDs)

   +-----+----------+--+--+--+--+--+--+--+--+---+---+---+---+---+---+
   | 0   | 1        | 2| 3| 4| 5| 6| 7| 8| 9| 10| 11| 12| 13| 14| 15|
   +=====+==========+==+==+==+==+==+==+==+==+===+===+===+===+===+===+
   |     |          |     |           | data (if len <= 8)          |
   |     |          |     |           +-------------+---------------+
   | crc8| cycle_cnt| len | id        |             | data_crc      |
   |     |          |     |           | offset      +---------------+
   |     |          |     |           |             | metadata      |
   +-----+----------+-----+-----------+-------------+---------------+

这是默认格式,在 :c:struct:`zms_ate` 的 API 文档中捕获。``data_crc`` 可选地包含在内,用于完整性检查存储在扇区顶部的数据。(This is the default format which is captured in the API documentation for :c:struct:`zms_ate`. The ``data_crc`` is optionally included to integrity-check data stored at the top of the sector.)

.. note:: 仅当完整读取数据时才检查数据的 CRC。部分读取不检查数据的 CRC,因为它是为整个元素计算的。(The CRC of the data is checked only when a full read of the data is made. The CRC of the data is not checked for a partial read, as it is computed for the whole element.)

.. warning:: 在以前未启用 CRC 功能的现有 ZMS 内容上启用 CRC 功能将使所有现有数据无效。(Enabling the CRC feature on previously existing ZMS content that did not have it enabled will make all existing data invalid.)

.. table:: 64 位 ID 的条目格式 (Entry format for 64-bit IDs)

   +-----+----------+--+--+--+--+--+--+--+--+---+---+----+----+----+----+
   | 0   | 1        | 2| 3| 4| 5| 6| 7| 8| 9| 10| 11| 12 | 13 | 14 | 15 |
   +=====+==========+==+==+==+==+==+==+==+==+===+===+====+====+====+====+
   |     |          |     |                         | data (if len <= 4)|
   |     |          |     |                         +-------------------+
   | crc8| cycle_cnt| len | id                      | offset            |
   |     |          |     |                         +-------------------+
   |     |          |     |                         | metadata          |
   +-----+----------+-----+-------------------------+-------------------+

当启用 :kconfig:option:`CONFIG_ZMS_ID_64BIT` 时选择此格式。(This format is selected when :kconfig:option:`CONFIG_ZMS_ID_64BIT` is enabled.)

.. warning:: 选择与以前存在的 ZMS 内容使用的格式不同的 ATE 格式将使所有现有数据无效。(Selecting a different ATE format than the one used by previously existing ZMS content will make all existing data invalid.)

.. note:: :ref:`Settings <settings_api>` 的 ZMS 后端不支持此格式。(The ZMS backend for :ref:`Settings <settings_api>` does not support this format.)

用户数据(键值对)的可用空间 (Available space for user data (key-value pairs))
*****************************************************************************

ZMS 始终需要一个空扇区才能执行垃圾收集 (GC)。因此,如果假设分区中存在 4 个扇区,ZMS 将仅使用 3 个扇区来存储键值对,并保留一个空扇区以便能够执行 GC。空扇区将在分区中的 4 个扇区之间旋转。(ZMS always needs an empty sector to be able to perform the garbage collection (GC). So, if we suppose that 4 sectors exist in a partition, ZMS will only use 3 sectors to store key-value pairs and keep one sector empty to be able to perform GC. The empty sector will rotate between the 4 sectors in the partition.)

.. note:: 一次可以写入扇区的最大单个数据长度为 64K(这可能会在 ZMS 的未来版本中更改)。(The maximum single data length that can be written at once in a sector is 64K (this could change in future versions of ZMS).)

小数据值 (Small data values)
=============================

足够小的值将存储在条目 (ATE) 本身中,而无需在扇区顶部写入数据。可以放入条目内的数据量取决于其选定的格式。请参阅 `ATE 结构 <#ate-allocation-table-entry-structure>`_ 部分。(Values which are sufficiently small will be stored within the entry (ATE) itself, without writing data at the top of the sector. The amount of data that can fit inside the entry depends on its selected format. See the `ATE structure <#ate-allocation-table-entry-structure>`_ section.)

ZMS 的条目大小为 16 字节,这意味着在此场景中分区中存储数据的最大可用空间计算如下:(ZMS has an entry size of 16 bytes which means that the maximum available space in a partition to store data is computed in this scenario as:)

.. math::

   \small\frac{(NUM\_SECTORS - 1) \times (SECTOR\_SIZE - (5 \times ATE\_SIZE)) \times (DATA\_SIZE)}{ATE\_SIZE}

其中:(Where:)

``NUM_SECTOR``: 扇区总数 (Total number of sectors)

``SECTOR_SIZE``: 扇区大小 (Size of the sector)

``ATE_SIZE``: 16 字节

``(5 * ATE_SIZE)``: 为头部和删除项保留的 ATE (Reserved ATEs for header and delete items)

``DATA_SIZE``: 8 字节或 4 字节,取决于 ATE 格式 (8 bytes or 4 bytes depending on the ATE format)

例如,对于 4 个 1024 字节的扇区,使用默认 ATE 格式,8 字节长度数据的可用空间为 :math:`\frac{3 \times 944 \times 8}{16} = 1416 \, \text{ 字节}`。(For example for 4 sectors of 1024 bytes, with the default ATE format, free space for 8-byte length data is :math:`\frac{3 \times 944 \times 8}{16} = 1416 \, \text{ bytes}`.)

大数据值 (Large data values)
=============================

超过 ``DATA_SIZE`` 的值存储在扇区顶部的 ATE 之外。在这种情况下,很难估计可用空间,因为这取决于数据的大小。但我们可以考虑到,对于在扇区顶部添加的 N 字节数据,必须在扇区底部添加额外的 16 字节 ATE,键值对总计 :math:`N + 16` 字节。(Values exceeding ``DATA_SIZE`` are stored outside of the ATE at the top of the sector. In this case, it is hard to estimate the free available space, as this depends on the size of the data. But we can take into account that for N bytes of data added at the top of the sector, an additional 16 bytes of ATE must be added at the bottom of the sector, which adds up to :math:`N + 16` bytes for the key-value pair.)

让我们举个例子:(Let's take an example:)

对于具有 4 个 1024 字节扇区的分区,数据大小为 64 字节。只有 3 个扇区可用于写入,每个扇区的容量为 944 字节,这使得可以在每个扇区中存储 11 个键值对 (:math:`\frac{944}{64 + 16}`)。在这种情况下,可以存储在此分区中的总数据为 :math:`11 \times 3 \times 64 = 2112 \text{ 字节}`。(For a partition that has 4 sectors of 1024 bytes and for data size of 64 bytes. Only 3 sectors are available for writes with a capacity of 944 bytes each, which makes it possible to store 11 key-value pairs in each sector (:math:`\frac{944}{64 + 16}`). Total data that could be stored in this partition for this case is :math:`11 \times 3 \times 64 = 2112 \text{ bytes}`.)

磨损均衡 (Wear leveling)
*************************

此存储系统针对不需要擦除的设备进行了优化。依赖擦除值的存储系统(例如 NVS)需要使用写入操作来模拟擦除。这会导致这些设备的预期寿命显著降低,以及写入操作和设备为空时初始化设备的延迟增加。ZMS 使用循环计数机制,避免为这些设备模拟擦除操作。它还保证每个内存位置在每个扇区写入周期中仅写入一次。(This storage system is optimized for devices that do not require an erase. Storage systems that rely on an erase value (NVS as an example) need to emulate the erase with write operations. This causes a significant decrease in the life expectancy of these devices as well as more delays for write operations and initialization of the device when it is empty. ZMS uses a cycle count mechanism that avoids emulating erase operations for these devices. It also guarantees that every memory location is written only once for each cycle of sector write.)

例如,要在不需要擦除操作的设备上使用 NVS 擦除 4096 字节扇区,必须执行 256 次闪存写入(假设 ``write-block-size`` = 16 字节),而使用 ZMS,只需要 1 次 16 字节的写入。在这种情况下,此操作快 256 倍。(As an example, to erase a 4096-byte sector on devices that do not require an erase operation using NVS, 256 flash writes must be performed (supposing that ``write-block-size`` = 16 bytes), while using ZMS, only 1 write of 16 bytes is needed. This operation is 256 times faster in this case.)

垃圾收集操作还会降低内存单元的预期寿命,因为它在将块从一个扇区移动到另一个扇区时执行写入操作。为了使垃圾收集器不影响设备的预期寿命,建议适当调整分区大小。它的大小应该是可以写入存储的数据(包括头部)最大大小的两倍。(The garbage collection operation also reduces the memory cell life expectancy as it performs write operations when moving blocks from one sector to another. To make the garbage collector not affect the life expectancy of the device it is recommended to dimension the partition appropriately. Its size should be the double of the maximum size of data (including headers) that could be written in the storage.)

请参阅 `用户数据的可用空间 <#available-space-for-user-data-key-value-pairs>`_。(See `Available space for user data <#available-space-for-user-data-key-value-pairs>`_.)

设备寿命计算 (Device lifetime calculation)
===========================================

存储设备,无论是经典闪存还是像 RRAM/MRAM 这样的新技术,都有有限的预期寿命,这由内存单元可以擦除/写入的次数决定。闪存设备作为其功能行为的一部分一次擦除一页(否则无法覆盖内存单元),对于不需要擦除操作的存储设备,可以直接覆盖内存单元。(Storage devices, whether they are classical flash or new technologies like RRAM/MRAM, have a limited life expectancy which is determined by the number of times memory cells can be erased/written. Flash devices are erased one page at a time as part of their functional behavior (otherwise memory cells cannot be overwritten), and for storage devices that do not require an erase operation, memory cells can be overwritten directly.)

这里显示了一个典型场景来计算设备的预期寿命:假设我们使用相同的 ID 存储 4 字节变量,但其内容每分钟都会更改。分区有 4 个扇区,每个扇区 1024 字节。变量的每次写入需要 16 字节的存储空间。由于每个扇区有 944 字节可用于 ATE,并且因为 ZMS 是快进存储系统,我们将在 :math:`\frac{(944 \times 4)}{16} = 236 \text{ 分钟}` 后重写第一个扇区的第一个位置。(A typical scenario is shown here to calculate the life expectancy of a device: Let's suppose that we store a 4-byte variable using the same ID but its content changes every minute. The partition has 4 sectors with 1024 bytes each. Each write of the variable requires 16 bytes of storage. As we have 944 bytes available for ATEs for each sector, and because ZMS is a fast-forward storage system, we are going to rewrite the first location of the first sector after :math:`\frac{(944 \times 4)}{16} = 236 \text{ minutes}`.)

除了正常写入之外,垃圾收集器还会将仍然有效的数据从旧扇区移动到新扇区。由于我们使用相同的 ID 和大分区大小,在这种情况下,垃圾收集器不会移动任何数据。对于可以写入 20,000 次的存储设备,存储将持续约 4,720,000 分钟(约 9 年)。(In addition to the normal writes, the garbage collector will move the data that is still valid from old sectors to new ones. As we are using the same ID and a big partition size, no data will be moved by the garbage collector in this case. For storage devices that can be written 20 000 times, the storage will last about 4 720 000 minutes (~9 years).)

要制定更通用的公式,我们必须首先计算 ZMS 中我们典型数据集的有效使用大小。对于具有 `小数据 <#small-data-values>`_ 的 ID/数据对,``effective_size`` 为 ``16`` 字节,而对于 `大数据 <#large-data-values>`_,``effective_size`` 为 ``16 + sizeof(data)`` 字节。假设 ``total_effective_size`` 是写入存储的数据的总大小,并且分区大小适当(有效大小的两倍),以避免垃圾收集器一直移动块。(To make a more general formula we must first compute the effective used size in ZMS by our typical set of data. For ID/data pairs with `small data <#small-data-values>`_, ``effective_size`` is ``16`` bytes, while for `large data <#large-data-values>`_, ``effective_size`` is ``16 + sizeof(data)`` bytes. Let's suppose that ``total_effective_size`` is the total size of the data that is written in the storage and that the partition is sized appropriately (double of the effective size) to avoid having the garbage collector moving blocks all the time.)

设备的预期寿命(分钟)计算如下:(The expected lifetime of the device in minutes is computed as:)

.. math::

   \small\frac{(SECTOR\_EFFECTIVE\_SIZE \times SECTOR\_NUMBER \times MAX\_NUM\_WRITES)}{(TOTAL\_EFFECTIVE\_SIZE \times WR\_MIN)}

其中:(Where:)

``SECTOR_EFFECTIVE_SIZE``: 扇区大小 - 头部大小(80 字节) (The sector size - header size (80 bytes))

``SECTOR_NUMBER``: 扇区数量 (The number of sectors)

``MAX_NUM_WRITES``: 存储设备的预期寿命(写入次数) (The life expectancy of the storage device in number of writes)

``TOTAL_EFFECTIVE_SIZE``: 写入数据集的总有效大小 (Total effective size of the set of written data)

``WR_MIN``: 每分钟数据集的写入次数 (Number of writes of the set of data per minute)

特性 (Features)
****************

与 NVS 等现有存储系统相比,ZMS 引入了许多特性,并将从其初始版本发展到包含更多满足新技术要求(如低延迟和更大存储空间)的特性。(ZMS has introduced many features compared to existing storage system like NVS and will evolve from its initial version to include more features that satisfies new technologies requirements such as low latency and bigger storage space.)

现有特性 (Existing features)
=============================

版本 1 (Version 1)
------------------

- 支持不需要擦除操作的存储设备(仅一次写入操作即可使扇区无效) (Supports storage devices that do not require an erase operation (only one write operation to invalidate a sector))
- 支持大分区和扇区大小(64 位地址空间) (Supports large partition and sector sizes (64-bit address space))
- 支持 32 位 ID 和 64 位 ID (Supports 32-bit IDs and 64-bit IDs)
- 小数据值存储在 ATE 本身中 (Small data values are stored in the ATE itself)
- 内置数据 CRC32(包含在 ATE 中) (Built-in data CRC32 (included in the ATE))
- ZMS 的版本控制(处理未来演进) (Versioning of ZMS (to handle future evolutions))
- 支持大 ``write-block-size``(仅适用于需要它的平台) (Supports large ``write-block-size`` (only for platforms that need it))
- 支持多种 ATE 格式以满足不同应用程序的要求 (Supports multiple ATE formats to satisfy the requirements of different applications)

未来特性 (Future features)
===========================

- 添加使用不同 ATE 格式挂载多个文件系统的可能性(目前,同一应用程序中的所有文件系统必须使用相同的格式) (Add the possibility to mount multiple filesystems with different ATE formats (currently, all filesystems in the same application must use the same format))
- 对于 ID/值对定期写入且不超过分区大小一半的某些应用程序使用,添加跳过垃圾收集器的可能性(始终存在具有相同 ID 的旧条目)。(Add the possibility to skip garbage collector for some application usage where ID/value pairs are written periodically and do not exceed half of the partition size (there is always an old entry with the same ID).)
- 将 ID 划分为命名空间并根据应用程序需求分配 ID,以处理不同子系统或示例使用的 ID 之间的冲突。(Divide IDs into namespaces and allocate IDs on demand from application to handle collisions between IDs used by different subsystems or samples.)
- 添加基于循环计数值检索设备磨损值的可能性 (Add the possibility to retrieve the wear out value of the device based on the cycle count value)
- 添加恢复功能,如果出错可以恢复存储分区 (Add a recovery function that can recover a storage partition if something went wrong)
- 添加库/应用程序以允许从 NVS 条目迁移到 ZMS 条目 (Add a library/application to allow migration from NVS entries to ZMS entries)
- 添加在挂载存储时出错时强制将存储分区格式化为 ZMS 格式的可能性。(Add the possibility to force formatting the storage partition to the ZMS format if something went wrong when mounting the storage.)

ZMS 和 Zephyr 中的其他存储系统 (ZMS and other storage systems in Zephyr)
==========================================================================

本节在 Zephyr 中存储系统的更广泛背景下描述 ZMS(不是完整的文件系统,而是更简单的非分层文件系统)。今天 Zephyr 至少包括两个在范围和功能上具有一定可比性的其他系统::ref:`NVS <nvs_api>` 和 :ref:`FCB <fcb_api>`。在应用程序中使用哪一个取决于您的需求和正在使用的硬件,本节提供有助于做出选择的信息。(This section describes ZMS in the wider context of storage systems in Zephyr (not full filesystems, but simpler, non-hierarchical ones). Today Zephyr includes at least two other systems that are somewhat comparable in scope and functionality: :ref:`NVS <nvs_api>` and :ref:`FCB <fcb_api>`. Which one to use in your application will depend on your needs and the hardware you are using, and this section provides information to help make a choice.)

- 如果您使用的设备不需要擦除操作,如 RRAM 或 MRAM,:ref:`ZMS <zms_api>` 绝对是您存储子系统的最佳选择,因为它旨在避免使用大块写入为这些设备模拟擦除操作,并将其替换为单个写入调用。(If you are using devices that do not require an erase operation like RRAM or MRAM, :ref:`ZMS <zms_api>` is definitely the best fit for your storage subsystem as it is designed to avoid emulating erase operation using large block writes for these devices and replaces it with a single write call.)
- 对于具有大 ``write_block_size`` 和/或需要与经典闪存页面大小(等于 erase_block_size)不同的扇区大小的设备,:ref:`ZMS <zms_api>` 也是最佳选择,因为可以自定义这些参数并在 ZMS 中添加对这些设备的支持。(For devices that have a large ``write_block_size`` and/or need a sector size that is different than the classical flash page size (equal to erase_block_size), :ref:`ZMS <zms_api>` is also the best fit as there is the possibility to customize these parameters and add the support of these devices in ZMS.)
- 对于经典闪存技术设备,建议使用 :ref:`NVS <nvs_api>`,因为它具有低占用空间(更小的 ATE 和更小的头部 ATE)。与 ZMS 相比,NVS 中的闪存擦除也非常快,并且不需要额外的写入操作。对于这些设备,NVS 的读/写也会比 ZMS 快,因为它的 ATE 大小更小。(For classical flash technology devices, :ref:`NVS <nvs_api>` is recommended as it has low footprint (smaller ATEs and smaller header ATEs). Erasing flash in NVS is also very fast and do not require an additional write operation compared to ZMS. For these devices, NVS reads/writes will be faster as well than ZMS as it has smaller ATE size.)
- 如果您的应用程序需要超过 64K ID 用于存储,建议在此处使用 :ref:`ZMS <zms_api>`,因为 ID 字段最多为 64 位。(If your application needs more than 64K IDs for storage, :ref:`ZMS <zms_api>` is recommended here because the ID field is up to 64-bit.)
- 如果您的应用程序以 FIFO 模式(先进先出)工作,那么 :ref:`FCB <fcb_api>` 是此用例的最佳存储解决方案。(If your application is working in a FIFO mode (First-in First-out) then :ref:`FCB <fcb_api>` is the best storage solution for this use case.)

更一般地说,要在 NVS 和 ZMS 之间做出正确选择,应首先验证所有阻碍因素,以确保应用程序可以使用一个子系统或另一个子系统,然后如果两种解决方案都可以实现,最佳选择应基于本节中描述的设备预期寿命的计算:`磨损均衡 <#wear-leveling>`_。(More generally to make the right choice between NVS and ZMS, all the blockers should be first verified to make sure that the application could work with one subsystem or the other, then if both solutions could be implemented, the best choice should be based on the calculations of the life expectancy of the device described in this section: `Wear leveling <#wear-leveling>`_.)

提高性能的建议 (Recommendations to increase performance)
*********************************************************

扇区大小和数量 (Sector size and count)
=======================================

- 应适当设置存储分区的总大小,以使 ZMS 获得最佳性能。有关 ZMS 中有效可用空间的所有信息都可以在文档中找到。请参阅 `用户数据的可用空间 <#available-space-for-user-data-key-value-pairs>`_。建议选择一个存储分区大小,该大小是将写入存储的键值对大小的两倍。(The total size of the storage partition should be set appropriately to achieve the best performance with ZMS. All the information regarding the effectively available free space in ZMS can be found in the documentation. See `Available space for user data <#available-space-for-user-data-key-value-pairs>`_. It's recommended to choose a storage partition size that is double the size of the key-value pairs that will be written in the storage.)
- 需要设置扇区大小,以便扇区可以容纳将存储的最大数据大小。增加扇区大小将减慢垃圾收集操作并使其发生频率降低。相反,减小其大小将使垃圾收集操作更快,但也会更频繁地发生。(The sector size needs to be set such that a sector can fit the maximum data size that will be stored. Increasing the sector size will slow down the garbage collection operation and make it occur less frequently. Decreasing its size, on the opposite, will make the garbage collection operation faster but also occur more frequently.)
- 对于某些子系统,如 :ref:`Settings <settings_api>`,所有路径值对都分为两个 ZMS 条目 (ATE)。在计算所需的存储空间时,应考虑两个条目所需的头部。(For some subsystems like :ref:`Settings <settings_api>`, all path-value pairs are split into two ZMS entries (ATEs). The headers needed by the two entries should be accounted for when computing the needed storage space.)
- 使用 `小数据值 <#small-data-values>`_ 可以提高性能,因为此数据写入条目内。例如,对于 :ref:`Settings <settings_api>` 子系统,选择小于或等于 8 字节的路径名可以使读写更快。(Using `small data values <#small-data-values>`_ can increase the performance, as this data is written within the entry. For example, for the :ref:`Settings <settings_api>` subsystem, choosing a path name that is less than or equal to 8 bytes can make reads and writes faster.)

缓存大小 (Cache size)
======================

- 直接使用 ZMS API 时,缓存大小的建议是使其至少等于将写入存储的不同条目数。(When using the ZMS API directly, the recommendation for the cache size is to make it at least equal to the number of different entries that will be written in the storage.)
- 每个额外的缓存条目将为 RAM 使用增加 8 字节。应仔细选择缓存大小。(Each additional cache entry will add 8 bytes to your RAM usage. Cache size should be carefully chosen.)
- 如果通过 :ref:`Settings <settings_api>` 使用 ZMS,则必须考虑到每个 Settings 条目都分为两个 ZMS 条目。缓存大小的建议是使其至少是 Settings 条目数的两倍。(If you use ZMS through :ref:`Settings <settings_api>`, you have to take into account that each Settings entry is divided into two ZMS entries. The recommendation for the cache size is to make it at least twice the number of Settings entries.)

ID 大小 (ID size)
==================

- 64 位 ID 空间预计对于大多数应用程序来说都大于必要的。除非您有特定需求,否则建议坚持使用 32 位 ID。这预计对代码大小和性能有轻微影响,即使在 64 位系统上,因为存储中 ID 的字节位置未对齐到 8 字节边界。(The 64-bit ID space is expected to be larger than necessary for most applications. Unless you have a particular need for this, it's recommended to stick with 32-bit IDs. This is expected to have a slight impact on code size and performance, even on 64-bit systems, because the byte position of IDs in storage is not aligned to an 8-byte boundary.)

API 参考 (API Reference)
*************************

ZMS API 由 ``zms.h`` 提供:(The ZMS API is provided by ``zms.h``:)

.. doxygengroup:: zms_data_structures

.. doxygengroup:: zms_high_level_api

.. comment
   not documenting .. doxygengroup:: zms
