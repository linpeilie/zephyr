.. _language_c:

C 语言支持
#########

C 是一种通用的低级编程语言，广泛用于编写嵌入式系统代码。

Zephyr 主要用 C 编写，并原生支持用 C 语言编写的应用程序。所有 Zephyr API 函数和宏都用 C 实现，
并可作为 :file:`include` 目录下 C 头文件的一部分使用，因此用 C 编写 Zephyr 应用程序使开发人员能够
访问最多的功能。

``main()`` 函数必须具有返回类型 ``int``，因为 Zephyr 应用程序运行在由 C 标准定义的"托管"环境中。
应用程序必须从 main 返回零（0）。所有非零返回值都是保留的。

.. _c_standards:

语言标准
*******

Zephyr 不针对 C 标准的特定版本；但是，Zephyr 代码库广泛使用 1999 年发布的
ISO C 标准（ISO/IEC 9899:1999，以下简称 C99）中新引入的功能，如下所列，
实际上需要使用支持 C99 标准及以上版本的编译器工具链：

* 内联函数
* 标准布尔类型（``<stdbool.h>`` 中的 ``bool``）
* 固定宽度整数类型（``<stdint.h>`` 中的 ``[u]intN_t``）
* 指定的初始化器
* 可变宏
* ``restrict`` 限定符

某些 Zephyr 组件使用 2011 年发布的 ISO C 标准（ISO/IEC 9899:2011，以下简称 C11）
中新引入的功能，例如使用 ``_Generic`` 关键字的类型泛型表达式。例如，
用作 Zephyr 默认格式化输出处理器的 :c:func:`cbprintf` 组件使用 C11 类型泛型表达式，
这实际上需要大多数 Zephyr 应用程序使用支持 C11 标准及以上版本的编译器工具链进行编译。

总之，建议使用支持至少 C11 标准的编译器工具链来开发 Zephyr。但是，
重要的是要注意某些可选的 Zephyr 组件和外部模块可能使用在标准的更新版本中引入的 C 语言功能，
在这种情况下，将需要使用支持此类标准的更新编译器工具链。

.. _c_library:

标准库
*****

`C 标准库`_ 是任何 C 程序的不可或缺的一部分，Zephyr 为应用程序选择支持多个不同的 C 库，
具体取决于用于构建应用程序的编译器工具链。

.. toctree::
   :maxdepth: 2

   common_libc.rst
   minimal_libc.rst
   newlib.rst
   picolibc.rst

.. _`C Standard Library`: https://en.wikipedia.org/wiki/C_standard_library

.. _c_library_formatted_output:

格式化输出
*********

C 定义了标准格式化输出函数，如 ``printf`` 和 ``sprintf``，这些函数由 C 标准库实现。

每个 C 标准库都有其自己的一组选择格式化输出模式和功能的要求和配置。
有关更多详细信息，请参阅每个 C 标准库文档。

.. _c_library_dynamic_mem:

动态内存管理
***********

C 定义了标准的动态内存管理接口（例如 :c:func:`malloc` 和 :c:func:`free`），
这些函数由 C 标准库实现。

虽然动态内存管理实现的细节在不同 C 标准库中有所不同，但所有支持的库都必须符合
以下约定。每个受支持的 C 标准库应：

* 内部管理其自己的内存堆，或通过调用在 :file:`libc-hooks.c` 中实现的钩子函数
  （例如 :c:func:`sbrk`）来管理。

* 维护对标准动态内存分配接口（例如 :c:func:`malloc`）分配的内存块的体系结构和内存区域特定的对齐要求。

* 在启用用户空间时在 ``z_malloc_partition`` 内存分区内分配内存块。请参阅 :ref:`memory_domain_predefined_partitions`。

有关 C 标准库特定内存管理实现的更多详细信息，请参阅每个 C 标准库文档。

.. note::
   本机 Zephyr 应用程序应使用由 Zephyr 内核支持的 :ref:`内存管理 API <memory_management_api>`，
   例如 :c:func:`k_malloc`，以利用它们提供的高级功能。

   C 标准动态内存管理接口函数（如 :c:func:`malloc`）应仅由目标多个操作系统的
   便携式应用程序和库使用。
