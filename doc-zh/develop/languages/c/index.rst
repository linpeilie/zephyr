.. _language_c:

C 语言支持
##################

C 是一种通用的低级编程语言,广泛用于编写嵌入式系统代码。

Zephyr 主要用 C 语言编写,原生支持用 C 语言编写的应用程序。所有 Zephyr API
函数和宏都用 C 实现,并作为 :file:`include` 目录下的 C 头文件的一部分提供,
因此用 C 编写 Zephyr 应用程序可以让开发人员访问最多的功能。

``main()`` 函数必须具有 ``int`` 返回类型,因为 Zephyr 应用程序在 C 标准
定义的"托管"环境中运行。应用程序必须从 main 返回零(0)。所有非零返回值都是保留的。

.. _c_standards:

语言标准
******************

Zephyr 不针对特定版本的 C 标准;但是,Zephyr 代码库广泛使用 ISO C 标准 1999 版
(ISO/IEC 9899:1999,以下简称 C99)中新引入的功能,例如下面列出的那些,
这实际上需要使用支持 C99 标准及更高版本的编译器工具链:

* 内联函数
* 标准布尔类型(``<stdbool.h>`` 中的 ``bool``)
* 固定宽度整数类型(``<stdint.h>`` 中的 ``[u]intN_t``)
* 指定初始化器
* 可变参数宏
* ``restrict`` 限定符

一些 Zephyr 组件使用 ISO C 标准 2011 版(ISO/IEC 9899:2011,以下简称 C11)
中新引入的功能,例如使用 ``_Generic`` 关键字的类型泛型表达式。例如,
:c:func:`cbprintf` 组件被用作 Zephyr 的默认格式化输出处理器,它使用了 C11
类型泛型表达式,这实际上要求大多数 Zephyr 应用程序使用支持 C11 标准及更高版本的
编译器工具链进行编译。

总之,建议使用至少支持 C11 标准的编译器工具链来开发 Zephyr。但是,需要注意的是,
一些可选的 Zephyr 组件和外部模块可能会使用在更新版本的标准中引入的 C 语言功能,
在这种情况下,需要使用支持这些标准的更新的编译器工具链。

.. _c_library:

标准库
****************

`C 标准库`_ 是任何 C 程序的组成部分,Zephyr 支持应用程序根据用于构建应用程序的
编译器工具链选择多种不同的 C 库。

.. toctree::
   :maxdepth: 2

   common_libc.rst
   minimal_libc.rst
   newlib.rst
   picolibc.rst

.. _`C 标准库`: https://en.wikipedia.org/wiki/C_standard_library

.. _c_library_formatted_output:

格式化输出
****************

C 定义了标准格式化输出函数,如 ``printf`` 和 ``sprintf``,这些函数由 C 标准库实现。

每个 C 标准库都有自己的一套要求和配置,用于选择格式化输出模式和功能。
有关更多详细信息,请参阅每个 C 标准库文档。

.. _c_library_dynamic_mem:

动态内存管理
*************************

C 定义了标准动态内存管理接口(例如,:c:func:`malloc` 和 :c:func:`free`),
这些函数由 C 标准库实现。

虽然动态内存管理实现的细节在不同的 C 标准库中有所不同,但所有支持的库都必须
遵守以下约定。每个支持的 C 标准库应:

* 在内部管理其自己的内存堆,或通过调用 :file:`libc-hooks.c` 中实现的钩子函数
  (例如,:c:func:`sbrk`)来管理。

* 维护标准动态内存分配接口(例如,:c:func:`malloc`)分配的内存块的架构和内存区域
  特定对齐要求。

* 在启用用户空间时,在 ``z_malloc_partition`` 内存分区内分配内存块。
  请参阅 :ref:`memory_domain_predefined_partitions`。

有关 C 标准库特定内存管理实现的更多详细信息,请参阅每个 C 标准库文档。

.. note::
   原生 Zephyr 应用程序应使用 Zephyr 内核支持的 :ref:`内存管理 API
   <memory_management_api>`,例如 :c:func:`k_malloc`,以便利用它们提供的高级功能。

   C 标准动态内存管理接口函数(例如 :c:func:`malloc`)应仅由针对多个操作系统的
   可移植应用程序和库使用。
