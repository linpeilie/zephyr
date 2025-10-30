.. _c_library_common:

通用 C 库代码
#####################

Zephyr 提供了一些 C 库函数,旨在与多个 C 库一起使用。这些函数要么提供多个 C 库中
不可用的功能,要么旨在用更适合 Zephyr 环境的代码替换 C 库中的功能。

时间函数
*************

这提供了标准 C 函数 :c:func:`time` 的实现,依赖于 Zephyr 函数
:c:func:`sys_clock_gettime`。可以通过选择 :kconfig:option:`COMMON_LIBC_TIME`
来启用此函数。

动态内存管理
*************************

可以通过在应用程序配置文件中选择 :kconfig:option:`CONFIG_COMMON_LIBC_MALLOC`
来启用通用动态内存管理实现。

通用 C 库在内部使用 :ref:`内核内存堆 API <heap_v2>` 来管理标准动态内存管理接口函数
(如 :c:func:`malloc` 和 :c:func:`free`)使用的内存堆。

内部内存堆通常位于 ``.bss`` 段中。但是,当启用用户空间时,它被放置在名为
``z_malloc_partition`` 的专用内存分区中,该分区可以从用户模式线程访问。
内部内存堆的大小由 :kconfig:option:`CONFIG_COMMON_LIBC_MALLOC_ARENA_SIZE` 指定。

使用通用 C 库的应用程序的默认堆大小为零(无堆)。对于其他 C 库用户,如果存在 MMU,
则默认堆为 16kB。否则,堆使用所有可用内存。

还有单独的控制来选择 :c:func:`calloc`(:kconfig:option:`COMMON_LIBC_CALLOC`)
和 :c:func:`reallocarray`(:kconfig:option:`COMMON_LIBC_REALLOCARRAY`)。
这两者默认都已启用,因为这不会影响不使用它们的应用程序的内存使用。

通用 C 库实现的标准动态内存管理接口函数是线程安全的,可以由多个线程同时调用。
这些函数在 :file:`lib/libc/common/source/stdlib/malloc.c` 中实现。
