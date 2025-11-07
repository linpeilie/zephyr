.. _cache_guide:

缓存基础 (Caching Basics)
##########################

本节讨论缓存一致性的基础知识以及用户需要在哪些情况下显式处理缓存。
有关 Zephyr 缓存工具的更多详细信息,请参阅 :ref:`cache_config` 了解 Zephyr Kconfig 选项,
或参阅 :ref:`cache_api` 了解 API 参考。本节主要关注数据缓存,
尽管对于具有缓存支持的系统通常也有指令缓存。

.. note::

  此处的信息假设已启用特定于架构的 MPU 支持。有关详细信息,请参阅特定于架构的文档。

.. note::

  虽然缓存一致性可能是 SMP 核心之间共享数据的一个问题,
  但 Zephyr 通常会确保从多个核心看到的内存处于一致状态。
  大多数应用程序只需要使用缓存 API 与外部硬件(如 DMA 控制器或运行不同 OS 镜像的外部 CPU)进行交互。
  有关 SMP 核心之间缓存一致性的更多信息,请参阅 :kconfig:option:`CONFIG_KERNEL_COHERENCE`。

在处理处理器核心和其他总线主设备之间共享的内存时,需要考虑缓存一致性。
通常,处理器缓存尽可能靠近每个处理器核心以最大化性能提升。
因此,DMA 引擎移入和移出内存的数据在处理器缓存中将是陈旧的,导致看起来像是损坏的数据。
如果您使用 DMA 移动数据,但处理器看不到您期望的数据,则缓存一致性可能是问题所在。

有多种方法可以确保处理器核心和外围设备看到的数据是一致的。
最简单的方法是禁用缓存,但这违背了拥有硬件缓存的初衷,并导致显著的性能下降。
许多架构提供了仅针对部分内存禁用缓存的方法。
当缓存一致性比性能更重要时(例如将 DMA 与 SPI 一起使用时),这可能很有用。
最后,还有一个选项是在运行时刷新或使内存区域的缓存无效。

全局禁用数据缓存 (Globally Disabling the Data Cache)
------------------------------------------------------

如上所述,全局禁用数据缓存可能会对性能产生重大影响,但对于调试很有用。

要求:

* :kconfig:option:`CONFIG_DCACHE`: 在 Zephyr 中启用 DCACHE 控制。

* :kconfig:option:`CONFIG_CACHE_MANAGEMENT`: 启用缓存 API。

* 调用 :c:func:`sys_cache_data_disable()` 以全局禁用数据缓存。

禁用内存区域的缓存 (Disabling Caching for a Memory Region)
-----------------------------------------------------------

如果未缓存内存上的性能对应用程序不是至关重要的,则仅针对部分内存禁用缓存可能是一个很好的性能折衷方案。
如果应用程序需要许多小于缓存行的小型不相关缓冲区,这是一个不错的选择。

要求:

* :kconfig:option:`CONFIG_DCACHE`: 在 Zephyr 中启用 DCACHE 控制。

* :kconfig:option:`CONFIG_MEM_ATTR`: 启用 ``mem-attr`` 库以处理设备树中的内存属性。

* 根据 :ref:`mem_mgmt_api` 注释您的设备树。

假设 MPU 驱动程序已启用,它将在内核初始化期间根据指定的内存属性配置指定的区域。
当使用专用的非缓存内存区域时,需要指示链接器将缓冲区放入该区域。
这可以通过使用 ``Z_GENERIC_SECTION`` 显式指定内存区域来完成:

.. code-block:: c

  /* SRAM4 在设备树中标记为非缓存 */
  uint8_t buffer[BUF_SIZE] Z_GENERIC_SECTION("SRAM4");

.. note::

  使用单独的缓存规则配置不同的内存区域需要使用 MPU 区域,
  这在某些架构上可能是有限的资源。其他内存保护功能(如 :ref:`用户空间 <mpu_userspace>`、
  :ref:`栈保护 <mpu_stack_objects>` 或 :ref:`内存域<memory_domain>`)可能需要 MPU 区域。

按变量自动禁用缓存 (Automatically Disabling Caching by Variable)
------------------------------------------------------------------

Zephyr 能够自动在内存中定义非缓存区域,并使用 ``__nocache`` 将变量分配给它。
使用此属性标记的任何变量都将放置在内存中的特殊 ``nocache`` 链接器区域中。
此区域将在初始化期间由 MPU 驱动程序配置为非缓存。
这是一个比显式声明内存区域为非缓存更简单的选项,但对这些变量的放置提供的控制较少,
因为链接器可能会在 RAM 中的任何位置分配此区域。

要求:

* :kconfig:option:`CONFIG_DCACHE`: 在 Zephyr 中启用 DCACHE 控制。

* :kconfig:option:`CONFIG_NOCACHE_MEMORY`: 启用 ``nocache`` 链接器区域的分配并将其配置为非缓存。

* 在任何非缓存缓冲区定义的末尾添加 ``__nocache`` 属性:

.. code-block:: c

  uint8_t buffer[BUF_SIZE] __nocache;

.. note::

  请参阅上面关于 MPU 区域可能限制的注释。``nocache`` 区域仍然是一个独特的 MPU 区域,
  即使它是由 Zephyr 自动创建的,而不是由用户显式定义的。

运行时缓存控制 (Runtime Cache Control)
---------------------------------------

性能最高但最复杂的选项是在运行时控制数据缓存。
在这种情况下,两个最相关的缓存操作是 **刷新** 和 **失效**。
这两个操作都在可缓存内存的最小单元——缓存行上操作。
数据缓存行通常为 16 到 128 字节。请参阅 :kconfig:option:`CONFIG_DCACHE_LINE_SIZE`。
缓存行大小通常在硬件中固定且不可配置,但 Zephyr 确实需要知道缓存行的大小,
以便正确有效地管理缓存。如果所讨论的缓冲区小于数据缓存行大小,
将它们放在非缓存区域可能更有效,因为打包到同一缓存行中的不相关数据在失效时可能会被破坏。

刷新缓存涉及将指定区域中所有修改的缓存行写回共享内存。
在处理器写入缓冲区之后以及远程总线主设备从该区域读取之前刷新与缓冲区关联的缓存。

.. note::

  某些架构支持称为 **直写** 缓存的缓存配置,
  其中来自处理器核心的数据写入会传播到共享内存。
  虽然这解决了 CPU 写入的缓存一致性问题,但它也会导致到主内存的更多流量,
  这可能会导致性能下降。

使缓存失效的工作方式类似,但方向相反。
它将指定区域中的缓存行标记为陈旧,确保当处理器下次从指定区域读取时,缓存行将从主内存刷新。
在从外围设备写入的缓冲区读取之前,使该缓冲区的数据缓存失效。

在某些情况下,同一缓冲区可能会重复用于例如 DMA 读取和 DMA 写入。
在这种情况下,可以先刷新与缓冲区关联的缓存,然后使其失效,
确保下次处理器从缓冲区读取时缓存将被刷新。

要求:

* :kconfig:option:`CONFIG_DCACHE`: 在 Zephyr 中启用 DCACHE 控制。

* :kconfig:option:`CONFIG_CACHE_MANAGEMENT`: 启用缓存 API。

* 调用 :c:func:`sys_cache_data_flush_range()` 以刷新内存区域。

* 调用 :c:func:`sys_cache_data_invd_range()` 以使内存区域失效。

* 调用 :c:func:`sys_cache_data_flush_and_invd_range()` 以刷新和失效。

对齐 (Alignment)
-----------------

如 :c:func:`sys_cache_data_invd_range()` 和相关函数中所述,
缓冲区应与缓存行大小对齐。这可以通过使用 ``__aligned`` 来完成:

.. code-block:: c

  uint8_t buffer[BUF_SIZE] __aligned(CONFIG_DCACHE_LINE_SIZE);
