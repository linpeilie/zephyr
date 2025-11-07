.. _cache_config:

缓存控制配置 (Cache Control Configuration)
###########################################

这是 Zephyr 缓存接口和与缓存控制器相关的 Kconfig 选项的高级指南。
有关 API 参考资料,请参阅 :ref:`cache_api`。

Zephyr 有不同的 Kconfig 选项来控制缓存控制器的实现和控制方式。

* :kconfig:option:`CONFIG_CPU_HAS_DCACHE` /
  :kconfig:option:`CONFIG_CPU_HAS_ICACHE`: 这些隐藏选项应该在 SoC / 平台级别选择,
  当 CPU 实际支持数据或指令缓存时。缓存控制器可以在核心中,也可以是提供了驱动程序的外部缓存控制器。

  这些选项的目标是记录可用的硬件功能,无论我们是否计划在 Zephyr 中支持和使用缓存控制,都应该设置它们。

* :kconfig:option:`CONFIG_DCACHE` / :kconfig:option:`CONFIG_ICACHE`:
  当数据或指令缓存的支持在 zephyr 中存在且可用时,必须选择这些选项。
  请注意,如果禁用这些选项,根据硬件默认设置,缓存可能仍然处于启用状态。

  与缓存控制相关的所有代码路径必须根据这些符号有条件地启用。
  当设置该符号时,缓存被认为是启用并使用的。

  这些符号对暴露给用户的实际 API 接口没有任何说明。
  例如,使用数据缓存的平台可以启用 :kconfig:option:`CONFIG_DCACHE` 符号,
  并在某些特定于平台的代码中使用 HAL 导出的函数来启用和管理 d-cache。

* :kconfig:option:`CONFIG_CACHE_MANAGEMENT`: 当通过标准 API
  (参见 :ref:`cache_api`)向用户公开缓存操作时,必须选择此选项。

  当启用此选项时,我们假设所有缓存函数都在架构代码或外部缓存控制器驱动程序中实现。

* :kconfig:option:`CONFIG_MEM_ATTR`: 此选项允许用户指定
  (使用 :ref:`内存区域属性<mem_mgmt_api>`)内存中的固定区域,
  一旦内核初始化,该区域将禁用缓存。

* :kconfig:option:`CONFIG_NOCACHE_MEMORY`: 此选项允许用户使用 ``__nocache``
  将单个全局变量指定为非缓存。这将指示链接器将任何标记的变量放入内存中的特殊 ``nocache`` 区域,
  并且 MPU 驱动程序将该区域配置为非缓存。

* :kconfig:option:`CONFIG_ARCH_CACHE`/:kconfig:option:`CONFIG_EXTERNAL_CACHE`:
  用于 :kconfig:option:`CACHE_TYPE` 的互斥选项,用于定义缓存操作是在架构级别实现
  还是使用提供了驱动程序的外部缓存控制器。

  * :kconfig:option:`CONFIG_ARCH_CACHE`: 缓存 API 由架构代码实现

  * :kconfig:option:`CONFIG_EXTERNAL_CACHE`: 缓存 API 由支持外部缓存控制器的驱动程序实现。
    在这种情况下,驱动程序必须像往常一样位于 :file:`drivers/cache/` 目录中

.. _cache_api:

缓存 API (Cache API)
*********************

.. doxygengroup:: cache_interface
