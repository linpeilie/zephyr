.. _formatted_output:

格式化输出 (Formatted Output)
################

应用程序以及 Zephyr 本身都需要基础设施来格式化供用户使用的值。标准 C99 库 ``*printf()`` 功能满足了流式输出设备或内存缓冲区的需求,但在嵌入式系统中,设备可能不接受流式数据,并且可能没有可用内存来存储格式化输出 (Applications as well as Zephyr itself requires infrastructure to format
values for user consumption.  The standard C99 library ``*printf()``
functionality fulfills this need for streaming output devices or memory
buffers, but in an embedded system devices may not accept streamed data
and memory may not be available to store the formatted output)。

内部 Zephyr API 传统上为 :c:func:`printk` 和 Zephyr 的内部最小 libc 提供此功能,但使用单独的内部接口。日志记录、跟踪、shell 和其他应用程序根据构建选项使用这些 API 或标准 libc 例程 (Internal Zephyr API traditionally provided this both for
:c:func:`printk` and for Zephyr's internal minimal libc, but with
separate internal interfaces.  Logging, tracing, shell, and other
applications made use of either these APIs or standard libc routines
based on build options)。

:c:func:`cbprintf` 公共 API 转换 C99 格式字符串和参数,通过回调机制一次产生一个字符的输出,替换原始内部函数并支持几乎所有 C99 格式规范。Zephyr 中现有的 ``s*printf()`` C 库使用可以转换为 :c:func:`snprintfcb()` 以避免引入 libc 实现 (The :c:func:`cbprintf` public APIs convert C99 format strings and
arguments, providing output produced one character at a time through a
callback mechanism, replacing the original internal functions and
providing support for almost all C99 format specifications.  Existing
use of ``s*printf()`` C libraries in Zephyr can be converted to
:c:func:`snprintfcb()` to avoid pulling in libc implementations)。

几个 Kconfig 选项控制启用的功能集,允许对功能和内存使用进行一定的控制 (Several Kconfig options control the set of features that are enabled,
allowing some control over features and memory usage):

* :kconfig:option:`CONFIG_CBPRINTF_FULL_INTEGRAL`
  或 (or) :kconfig:option:`CONFIG_CBPRINTF_REDUCED_INTEGRAL`
* :kconfig:option:`CONFIG_CBPRINTF_FP_SUPPORT`
* :kconfig:option:`CONFIG_CBPRINTF_FP_A_SUPPORT`
* :kconfig:option:`CONFIG_CBPRINTF_FP_ALWAYS_A`
* :kconfig:option:`CONFIG_CBPRINTF_N_SPECIFIER`

:kconfig:option:`CONFIG_CBPRINTF_LIBC_SUBSTS` 可用于提供行为类似标准 libc 函数的函数,但使用选定的 cbprintf 格式化器而不是从 libc 引入另一个格式化器 (:kconfig:option:`CONFIG_CBPRINTF_LIBC_SUBSTS` can be used to provide functions
that behave like standard libc functions but use the selected cbprintf
formatter rather than pulling in another formatter from libc)。

此外,:kconfig:option:`CONFIG_CBPRINTF_NANO` 可用于恢复到在添加此功能之前用于 :c:func:`printk` 的非常节省空间但功能有限的格式化器 (In addition :kconfig:option:`CONFIG_CBPRINTF_NANO` can be used to revert back to
the very space-optimized but limited formatter used for :c:func:`printk`
before this capability was added)。

.. _cbprintf_packaging:

Cbprintf 打包 (Cbprintf Packaging)
******************

通常,当调用 ``printf`` 系列函数时,字符串是同步格式化的。但是,在某些情况下,延迟格式化是有益的。在这种情况下,必须捕获状态 (格式字符串和参数)。这样的状态形成一个自包含的包,其中包含格式字符串和参数。此外,包可能包含作为格式字符串一部分的字符串的副本 (格式字符串或任何 ``%s`` 参数)。包的主要内容类似于 va_list 栈帧,因此使用标准格式化函数来处理包。由于包包含作为 va_list 帧处理的数据,必须保持严格的对齐。由于需要填充,包的大小取决于对齐。当复制包时,应将其复制到与原始位置具有相同对齐方式的内存块 (Typically, strings are formatted synchronously when a function from ``printf``
family is called. However, there are cases when it is beneficial that formatting
is deferred. In that case, a state (format string and arguments) must be captured.
Such state forms a self-contained package which contains format string and
arguments. Additionally, package may contain copies of strings which are
part of a format string (format string or any ``%s`` argument). Package primary
content resembles va_list stack frame thus standard formatting functions are
used to process a package. Since package contains data which is processed as
va_list frame, strict alignment must be maintained. Due to required padding,
size of the package depends on alignment. When package is copied, it should be
copied to a memory block with the same alignment as origin)。

包可以具有以下变体 (Package can have following variants):

* **自包含 (Self-contained)** - 非只读字符串附加到包。只要可以访问只读字符串位置,就可以从这样的包格式化字符串。包可能包含有关只读字符串在包内位置的信息。该信息可用于将包转换为完全自包含的包 (non read-only strings appended to the package. String can be
  formatted from such package as long as there is access to read-only string
  locations. Package may contain information where read-only strings are located
  within the package. That information can be used to convert packet to fully
  self-contained package)。
* **完全自包含 (Fully self-contained)** - 所有字符串都附加到包。可以从这样的包格式化字符串,而无需任何外部数据 (all strings are appended to the package. String can be
  formatted from such package without any external data)。
* **瞬态 (Transient)** - 仅存储参数。包包含有关非只读字符串指针在包内位置的信息。可选地,它可能包含只读字符串位置信息。只要非只读字符串仍然有效且只读字符串可访问,就可以从这样的包格式化字符串。或者,如果包中存在有关只读字符串位置的信息,则可以将包转换为**自包含**包或**完全自包含**包 (only arguments are stored. Package contain information
  where pointers to non read-only strings are located within the package. Optionally,
  it may contain read-only string location information. String can be formatted
  from such package as long as non read-only strings are still valid and read-only
  strings are accessible. Alternatively, package can be converted to **self-contained**
  package or **fully self-contained** if information about read-only string
  locations is present in the package)。

可以使用两种方法创建包 (Package can be created using two methods):

* 运行时 (runtime) - 使用 :c:func:`cbprintf_package` 或 :c:func:`cbvprintf_package`。此方法扫描格式字符串并根据检测到的格式说明符构建包 (using :c:func:`cbprintf_package` or :c:func:`cbvprintf_package`. This
  method scans format string and based on detected format specifiers builds the
  package)。
* 静态 (static) - 参数类型在编译时由预处理器检测,并将包创建为对提供的内存的简单赋值。此方法比运行时快得多 (超过 15 倍),但有以下限制:需要编译器支持 ``_Generic`` 关键字 (C11 功能),并且如果使用 char 指针,则无法区分 ``%p`` 和 ``%s``。它将所有 (unsigned) char 指针视为 ``%s``,因此将尝试将字符串附加到包。在使用 :c:macro:`CBPRINTF_PACKAGE_CONVERT_PTR_CHECK` 标志从**瞬态**包转换为**自包含**包期间,可以正确处理它。但是,它需要访问格式字符串,这并不总是可行的,因此建议将用于 ``%p`` 的 char 指针强制转换为 ``void *``。当使用 :c:macro:`CBPRINTF_PACKAGE_CONVERT_PTR_CHECK` 标志调用 :c:func:`cbprintf_package_convert` 时,如果 char 指针与 ``%p`` 一起使用,会生成日志警告 (types of arguments are detected at compile time by the preprocessor
  and package is created as simple assignments to a provided memory. This method
  is significantly faster than runtime (more than 15 times) but has following
  limitations: requires ``_Generic`` keyword (C11 feature) to be supported by
  the compiler and cannot distinguish between ``%p`` and ``%s`` if char pointer
  is used. It treats all (unsigned) char pointers as ``%s`` thus it will attempt
  to append string to a package. It can be handled correctly during conversion
  from **transient** package to **self-contained** package using
  :c:macro:`CBPRINTF_PACKAGE_CONVERT_PTR_CHECK` flag. However, it requires access
  to the format string and it is not always possible thus it is recommended to
  cast char pointers used for ``%p`` to ``void *``. There is a logging warning
  generated by :c:func:`cbprintf_package_convert` called with
  :c:macro:`CBPRINTF_PACKAGE_CONVERT_PTR_CHECK` flag when char pointer is used with
  ``%p``)。


几个 Kconfig 选项控制打包的行为 (Several Kconfig options control behavior of the packaging):

* :kconfig:option:`CONFIG_CBPRINTF_PACKAGE_LONGDOUBLE`
* :kconfig:option:`CONFIG_CBPRINTF_STATIC_PACKAGE_CHECK_ALIGNMENT`

Cbprintf 包转换 (Cbprintf package conversion)
===========================

可以将包转换为包含更多信息的变体,例如**瞬态**包可以转换为**自包含**包。如果在创建包时使用了 :c:macro:`CBPRINTF_PACKAGE_ADD_RO_STR_POS` 标志,则可以转换为**完全自包含**包 (It is possible to convert package to a variant which contains more information, e.g
**transient** package can be converted to **self-contained**. Conversion to
**fully self-contained** package is possible if :c:macro:`CBPRINTF_PACKAGE_ADD_RO_STR_POS`
flag was used when package was created)。

:c:func:`cbprintf_package_copy` 用于计算新包所需的空间以及复制和转换包 (:c:func:`cbprintf_package_copy` is used to calculate space needed for the new
package and to copy and convert a package)。

Cbprintf 包格式 (Cbprintf package format)
=======================

包的格式包含特定于平台的填充。包由头部组成,头部包含包的大小 (不包括附加字符串) 和附加字符串的数量。后面是参数,其中包含对齐填充并类似于 *va_list* 栈帧。后面是与字符串使用的字符指针参数相关联的数据,这些数据未附加到字符串 (但稍后可能由 :c:func:`cbprinf_package_convert` 附加)。最后,包可选地包含附加字符串。每个字符串包含 1 字节头,其中包含存储地址参数的位置索引。在打包期间,地址设置为 null,在字符串格式化之前,它会更新为指向包内的当前字符串位置。更新地址参数必须在字符串格式化之前发生,因为每次复制包时地址都会更改 (Format of the package contains paddings which are platform specific. Package consists
of header which contains size of package (excluding appended strings) and number of
appended strings. It is followed by the arguments which contains alignment paddings
and resembles *va_list* stack frame. It is followed by data associated with character
pointer arguments used by the string which are not appended to the string (but may
be appended later by :c:func:`cbprinf_package_convert`). Finally, package, optionally,
contains appended strings. Each string contains 1 byte header which contains index
of the location where address argument is stored. During packaging address is set
to null and before string formatting it is updated to point to the current string
location within the package. Updating address argument must happen just before string
formatting since address changes whenever package is copied)。

+------------------+-------------------------------------------------------------------------+
| 头部 (Header)    | 1 字节:参数列表大小,包括头部和 *fmt* (以 32 位字为单位)                   |
|                  | (1 byte: Argument list size including header and *fmt* (in 32 bit words))|
|                  +-------------------------------------------------------------------------+
| sizeof(void \*)  | 1 字节:附加到包的字符串数量                                               |
|                  | (1 byte: Number of strings appended to the package)                     |
|                  +-------------------------------------------------------------------------+
|                  | 1 字节:只读字符串参数位置数量                                             |
|                  | (1 byte: Number of read-only string argument locations)                 |
|                  +-------------------------------------------------------------------------+
|                  | 1 字节:瞬态字符串参数位置数量                                             |
|                  | (1 byte: Number of transient string argument locations)                 |
|                  +-------------------------------------------------------------------------+
|                  | 特定于平台的填充到 sizeof(void \*)                                        |
|                  | (platform specific padding to sizeof(void \*))                          |
+------------------+-------------------------------------------------------------------------+
| 参数 (Arguments) | 指向 *fmt* 的指针 (如果 *fmt* 附加到包则为 null)                          |
|                  | (Pointer to *fmt* (or null if *fmt* is appended to the package))        |
|                  +-------------------------------------------------------------------------+
|                  | (特定于平台对齐的可选填充)                                                |
|                  | ((optional padding for platform specific alignment))                    |
|                  +-------------------------------------------------------------------------+
|                  | 参数 0 (argument 0)                                                     |
|                  +-------------------------------------------------------------------------+
|                  | (特定于平台对齐的可选填充)                                                |
|                  | ((optional padding for platform specific alignment))                    |
|                  +-------------------------------------------------------------------------+
|                  | 参数 1 (argument 1)                                                     |
|                  +-------------------------------------------------------------------------+
|                  | ...                                                                     |
+------------------+-------------------------------------------------------------------------+
| 字符串位置信息   | 包内只读字符串所在位置的字索引                                             |
| (String location | (Indexes of words within the package where read-only strings are located)|
| information)     +-------------------------------------------------------------------------+
| (可选, optional) | 瞬态字符串所在位置的参数索引和参数位置索引对                                |
|                  | (Pairs of argument index and argument location index where transient     |
|                  | strings are located)                                                    |
+------------------+-------------------------------------------------------------------------+
| 附加字符串       | 1 字节:包内关联参数位置的索引                                             |
| (Appended        | (1 byte: Index within the package to the location of associated argument)|
| strings)         +-------------------------------------------------------------------------+
| (可选, optional) | 以 null 结尾的字符串 (Null terminated string)                            |
|                  +-------------------------------------------------------------------------+
|                  | ...                                                                     |
+------------------+-------------------------------------------------------------------------+

.. warning::

  如果选择 :kconfig:option:`CONFIG_MINIMAL_LIBC` 与 :kconfig:option:`CONFIG_CBPRINTF_NANO` 组合,使用 C 标准库函数 (如 ``printf`` 或 ``snprintf``) 的格式化将受到限制。除其他外,不支持 ``%n`` 说明符、大多数格式标志、精度控制和浮点数 (If :kconfig:option:`CONFIG_MINIMAL_LIBC` is selected in combination with
  :kconfig:option:`CONFIG_CBPRINTF_NANO` formatting with C standard library
  functions like ``printf`` or ``snprintf`` is limited.  Among other
  things the ``%n`` specifier, most format flags, precision control, and
  floating point are not supported)。

.. _cbprintf_packaging_limitations:

限制和建议 (Limitations and recommendations)
===============================

* 编译器需要支持 C11 ``_Generic`` 才能使用静态 (快速) 打包 (C11 ``_Generic`` support is required by the compiler to use static (fast) packaging)。
* 建议将任何与 ``%p`` 格式说明符一起使用的字符指针强制转换为其他指针类型 (例如 ``void *``)。如果无法访问格式字符串,则只能进行静态打包,它将附加所有检测到的字符串。用于 ``%p`` 的字符指针将被视为字符串指针。从意外位置复制可能会产生严重后果 (例如,内存故障或安全违规) (It is recommended to cast any character pointer used with ``%p`` format specifier to
  other pointer type (e.g. ``void *``). If format string is not accessible then only
  static packaging is possible and it will append all detected strings. Character pointer
  used for ``%p`` will be considered as string pointer. Copying from unexpected location
  can have serious consequences (e.g., memory fault or security violation))。

API 参考 (API Reference)
*************

.. doxygengroup:: cbprintf_apis
