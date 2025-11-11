.. _flash_map_api:

闪存映射 (Flash map)
#####################

``<zephyr/storage/flash_map.h>`` API 允许通过 :c:struct:`flash_area` 结构访问有关设备闪存分区的信息。(The ``<zephyr/storage/flash_map.h>`` API allows accessing information about device flash partitions via :c:struct:`flash_area` structures.)

每个 :c:struct:`flash_area` 描述一个闪存分区。该 API 提供对"闪存映射"的访问,该映射包含可通过全局唯一 ID 号访问的预定义闪存区域。该映射是从 DTS 文件中的"fixed-partition"兼容条目创建的。用户还可以在运行时为特定于应用程序的目的创建 :c:struct:`flash_area` 对象。(Each :c:struct:`flash_area` describes a flash partition. The API provides access to a "flash map", which contains predefined flash areas accessible via globally unique ID numbers. The map is created from "fixed-partition" compatible entries in DTS file. Users may also create :c:struct:`flash_area` objects at runtime for application-specific purposes.)

本文档在引用单个"fixed-partition"实体时使用"闪存区域"。(This documentation uses "flash area" when referencing single "fixed-partition" entities.)

:c:struct:`flash_area` 包含指向 :c:struct:`device` 的指针,该指针可用于直接使用 :ref:`flash API <flash_api>` 访问区域所在的闪存设备。每个闪存区域的特征由它所在的设备、从设备开头的偏移量和设备上的大小来表征。:c:func:`flash_area_open` 函数使用附加的标识符参数在闪存映射中查找闪存区域。(The :c:struct:`flash_area` contains a pointer to a :c:struct:`device`, which can be used to access the flash device an area is placed on directly with the :ref:`flash API <flash_api>`. Each flash area is characterized by a device it is placed on, offset from the beginning of the device and size on the device. An additional identifier parameter is used by the :c:func:`flash_area_open` function to find flash area in flash map.)

flash_map.h API 提供了在 :c:struct:`flash_area` 上操作的函数。主要示例是 :c:func:`flash_area_read` 和 :c:func:`flash_area_write`。这些函数基本上是闪存 API 的包装器,具有额外的偏移量和大小检查,以将闪存操作限制在预定义区域内。(The flash_map.h API provides functions for operating on a :c:struct:`flash_area`. The main examples are :c:func:`flash_area_read` and :c:func:`flash_area_write`. These functions are basically wrappers around the flash API with additional offset and size checks, to limit flash operations to a predefined area.)

大多数 ``<zephyr/storage/flash_map.h>`` API 函数需要表征它们将在其上工作的闪存区域的 :c:struct:`flash_area` 对象指针。有两种可能的方法来获取这样的指针:(Most ``<zephyr/storage/flash_map.h>`` API functions require a :c:struct:`flash_area` object pointer characterizing the flash area they will be working on. There are two possible methods to obtain such a pointer:)

 * 使用 :c:func:`flash_area_open` 获取它;(obtain it using :c:func:`flash_area_open`;)

 * 定义 :c:struct:`flash_area` 类型对象,这需要提供有效的 :c:struct:`device` 对象指针以及闪存设备内区域的偏移量和大小。(defining a :c:struct:`flash_area` type object, which requires providing a valid :c:struct:`device` object pointer with offset and size of the area within the flash device.)

:c:func:`flash_area_open` 使用数字标识符在闪存映射中搜索 :c:struct:`flash_area` 对象,如果找到,则返回指向表示具有给定 ID 的区域的对象的指针。可以使用 :c:macro:`FIXED_PARTITION_ID()` 从 fixed-partition DTS 节点标签获取闪存区域的 ID 号;这些标签从设备树中获取,如下所述。(:c:func:`flash_area_open` uses numeric identifiers to search flash map for :c:struct:`flash_area` objects and returns, if found, a pointer to an object representing area with given ID. The ID number for a flash area can be obtained from a fixed-partition DTS node label using :c:macro:`FIXED_PARTITION_ID()`; these labels are obtained from the devicetree as described below.)

与设备树的关系 (Relationship with Devicetree)
**********************************************

flash_map.h API 使用从 :ref:`devicetree_api` 生成的数据,特别是其 :ref:`devicetree-flash-api`。Zephyr 还有一些分区约定,用于通过 MCUboot 引导加载程序进行 :ref:`dfu`,以及定义可由 :ref:`文件系统 <file_system_api>` 或其他非易失性 :ref:`存储 <storage_reference>` 使用的分区。(The flash_map.h API uses data generated from the :ref:`devicetree_api`, in particular its :ref:`devicetree-flash-api`. Zephyr additionally has some partitioning conventions used for :ref:`dfu` via the MCUboot bootloader, as well as defining partitions usable by :ref:`file systems <file_system_api>` or other nonvolatile :ref:`storage <storage_reference>`.)

以下是一个设备树片段示例,它为 MCUboot 和存储分区使用固定闪存分区。为了清晰起见,省略了一些细节。(Here is an example devicetree fragment which uses fixed flash partitions for both MCUboot and a storage partition. Some details were left out for clarity.)

.. literalinclude:: example_fragment.dts
   :language: DTS
   :start-after: start-after-here

分区偏移量应相对于分区所属的闪存起始地址表示。(Partition offset shall be expressed in relation to the flash memory beginning address, to which the partition belongs to.)

``boot_partition``、``slot0_partition``、``slot1_partition`` 和 ``scratch_partition`` 节点标签是为 MCUboot 定义的,尽管并非所有 MCUboot 配置都需要定义所有这些标签。有关更多详细信息,请参阅 `MCUboot 文档`_。(The ``boot_partition``, ``slot0_partition``, ``slot1_partition``, and ``scratch_partition`` node labels are defined for MCUboot, though not all MCUboot configurations require all of them to be defined. See the `MCUboot documentation`_ for more details.)

``storage_partition`` 节点定义用于文件系统或其他非易失性存储 API。(The ``storage_partition`` node is defined for use by a file system or other nonvolatile storage API.)

.. _MCUboot documentation: https://docs.mcuboot.com

数字闪存区域 ID 通过将 DTS 节点标签传递给 :c:macro:`FIXED_PARTITION_ID()` 获得;例如,要获取 ``slot0_partition`` 的 ID 号,用户将调用 ``FIXED_PARTITION_ID(slot0_partition)``。(Numeric flash area ID is obtained by passing DTS node label to :c:macro:`FIXED_PARTITION_ID()`; for example to obtain ID number for ``slot0_partition``, user would invoke ``FIXED_PARTITION_ID(slot0_partition)``.)

所有 :code:`FIXED_PARTITION_*` 宏都将 DTS 节点标签作为分区标识符。(All :code:`FIXED_PARTITION_*` macros take DTS node labels as partition identifiers.)

如果 DTS 文件中定义了这样的区域,用户不必使用 :c:func:`flash_map_open` 获取 :c:struct:`flash_area` 对象指针来获取有关闪存区域大小、偏移量或设备的信息。了解区域的 DTS 节点标签,用户可以分别使用 :c:macro:`FIXED_PARTITION_OFFSET()`、:c:macro:`FIXED_PARTITION_SIZE()` 或 :c:macro:`FIXED_PARTITION_DEVICE()` 直接从 DTS 节点定义获取此类信息。例如,要获取 ``storage_partition`` 的偏移量,调用 ``FIXED_PARTITION_OFFSET(storage_partition)`` 就足够了。(Users do not have to obtain a :c:struct:`flash_area` object pointer using :c:func:`flash_map_open` to get information on flash area size, offset or device, if such area is defined in DTS file. Knowing the DTS node label of an area, users may use :c:macro:`FIXED_PARTITION_OFFSET()`, :c:macro:`FIXED_PARTITION_SIZE()` or :c:macro:`FIXED_PARTITION_DEVICE()` respectively to obtain such information directly from DTS node definition. For example to obtain offset of ``storage_partition`` it is enough to invoke ``FIXED_PARTITION_OFFSET(storage_partition)``.)

下面的示例显示了如何使用 :c:func:`flash_area_open` 和 DTS 节点标签获取 :c:struct:`flash_area` 对象指针:(Below example shows how to obtain a :c:struct:`flash_area` object pointer using :c:func:`flash_area_open` and DTS node label:)

.. code-block:: c

   const struct flash_area *my_area;
   int err = flash_area_open(FIXED_PARTITION_ID(slot0_partition), &my_area);

   if (err != 0) {
   	handle_the_error(err);
   } else {
   	flash_area_read(my_area, ...);
   }

API 参考 (API Reference)
*************************

.. doxygengroup:: flash_area_api
