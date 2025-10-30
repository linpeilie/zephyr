.. _c_library_newlib:

Newlib
######

`Newlib`_ 是为嵌入式系统编写的完整 C 库实现。它是一个单独的开源项目,
不以源代码形式包含在 Zephyr 中。相反,:ref:`toolchain_zephyr_sdk` 包含
每个支持架构的预编译库(:file:`libc.a` 和 :file:`libm.a`)。

.. note::
   其他第三方工具链,例如 :ref:`toolchain_gnuarmemb`,也将 Newlib 作为预编译库捆绑。

Zephyr 实现了由 Newlib 中的 C 标准库函数调用的"API 钩子"函数。这些钩子函数在
:file:`lib/libc/newlib/libc-hooks.c` 中实现,并将库内部系统调用转换为等效的
Zephyr API 调用。

Newlib 的类型
***************

:ref:`toolchain_zephyr_sdk` 中包含的 Newlib 有两个版本:"完整"和"nano"变体。

完整 Newlib
===========

Newlib 完整变体(:file:`libc.a` 和 :file:`libm.a`)是 Zephyr SDK 中可用的
Newlib 最强大的变体,支持几乎所有标准 C 库功能。它针对性能进行了优化
(优先考虑性能而非代码大小),其占用空间明显大于 nano 变体。

可以通过选择 :kconfig:option:`CONFIG_NEWLIB_LIBC` 并取消选择应用程序配置文件中的
:kconfig:option:`CONFIG_NEWLIB_LIBC_NANO` 来启用此变体。

Nano Newlib
===========

Newlib nano 变体(:file:`libc_nano.a` 和 :file:`libm_nano.a`)是 Newlib 的
大小优化版本,支持完整变体支持的所有功能,除了 C99 中引入的新格式说明符,
例如 ``char``、``long long`` 类型格式说明符(即 ``%hhX`` 和 ``%llX``)。

可以通过在应用程序配置文件中选择 :kconfig:option:`CONFIG_NEWLIB_LIBC` 和
:kconfig:option:`CONFIG_NEWLIB_LIBC_NANO` 来启用此变体。

请注意,Newlib nano 变体并非适用于所有架构。nano 变体的可用性由
:kconfig:option:`CONFIG_HAS_NEWLIB_LIBC_NANO` 指定。

.. _`Newlib`: https://sourceware.org/newlib/

格式化输出
****************

Newlib 支持所有标准 C 格式化输入和输出函数,包括 ``printf``、``fprintf``、
``sprintf`` 和 ``sscanf``。

Newlib 格式化输入和输出函数实现支持 C 标准定义的所有格式说明符,但有以下例外:

* 浮点格式说明符(例如 ``%f``)需要启用
  :kconfig:option:`CONFIG_NEWLIB_LIBC_FLOAT_PRINTF` 和
  :kconfig:option:`CONFIG_NEWLIB_LIBC_FLOAT_SCANF`。
* Newlib nano 变体不支持 C99 格式说明符(即 ``char`` 的 ``%hhX``、
  ``long long`` 的 ``%llX``、``intmax_t`` 的 ``%jX``、``size_t`` 的 ``%zX``、
  ``ptrdiff_t`` 的 ``%tX``)。

动态内存管理
*************************

Newlib 实现了内部堆分配器来管理标准动态内存管理接口函数(例如,:c:func:`malloc`
和 :c:func:`free`)使用的内存块。

Newlib 实现的内部堆分配器可能因使用的 Newlib 类型而异。例如,Zephyr SDK 的
完整 Newlib(:file:`libc.a` 和 :file:`libm.a`)中实现的堆分配器向操作系统请求
更大的内存块,与 Nano Newlib(:file:`libc_nano.a` 和 :file:`libm_nano.a`)
相比,其最小内存要求明显更高。

Newlib 动态内存管理函数与 Zephyr 端 libc 钩子之间的唯一接口是 :c:func:`sbrk`
函数,Newlib 使用它来管理为其内部堆分配器保留的内存池的大小。

在 :file:`libc-hooks.c` 中实现的 :c:func:`_sbrk` 钩子函数处理来自 Newlib 的
内存池大小更改请求,并通过在系统内存不足时返回错误来确保 Newlib 内部堆分配器
内存池大小不超过可用内存空间量。

启用用户空间时,Newlib 内部堆分配器内存池放置在名为 ``z_malloc_partition`` 的
专用内存分区中,该分区可以从用户模式线程访问。

可用于 Newlib 堆的内存空间量取决于系统配置:

* 启用 MMU 时(选择 :kconfig:option:`CONFIG_MMU`),为 Newlib 堆保留的内存空间量
  由 :c:func:`k_mem_free_get` 函数返回的空闲内存空间大小或
  :kconfig:option:`CONFIG_NEWLIB_LIBC_MAX_MAPPED_REGION_SIZE` 设置,以较小者为准。

* 启用 MPU 且 MPU 需要 2 的幂分区大小和地址对齐时
  (:kconfig:option:`CONFIG_NEWLIB_LIBC_ALIGNED_HEAP_SIZE` 设置为非零值),
  为 Newlib 堆保留的内存空间量由
  :kconfig:option:`CONFIG_NEWLIB_LIBC_ALIGNED_HEAP_SIZE` 设置。

* 否则,为 Newlib 堆保留的内存空间量等于 SRAM 区域中空闲(未分配)内存量。

Newlib 实现的标准动态内存管理接口函数是线程安全的,可以由多个线程同时调用。
