.. _c_library_picolibc:

Picolibc
########

`Picolibc`_ 是为嵌入式系统编写的完整 C 库实现,针对 `C17 (ISO/IEC 9899:2018)`_
和 `POSIX 2018 (IEEE Std 1003.1-2017)`_ 标准。Picolibc 是一个外部开源项目,
作为模块提供给 Zephyr,并作为 :ref:`toolchain_zephyr_sdk` 的一部分以预编译形式
包含在每个支持的架构中(:file:`libc.a`)。

.. note::
   Picolibc 也适用于其他第三方工具链,例如 :ref:`toolchain_gnuarmemb`。

Zephyr 实现了由 Picolibc 中的 C 标准库函数调用的"API 钩子"函数。这些钩子函数在
:file:`lib/libc/picolibc/libc-hooks.c` 中实现,并将库内部系统调用转换为等效的
Zephyr API 调用。

.. _`Picolibc`: https://github.com/picolibc/picolibc
.. _`C17 (ISO/IEC 9899:2018)`: https://www.iso.org/standard/74528.html
.. _`POSIX 2018 (IEEE Std 1003.1-2017)`: https://pubs.opengroup.org/onlinepubs/9699919799/functions/printf.html

.. _c_library_picolibc_module:

Picolibc 模块
===============

作为 Zephyr 模块构建时,有几个配置选项可用于调整库中的功能集,平衡库支持的内容
与生成函数的代码大小。由于标准 C++ 库必须针对目标 C 库进行编译,因此 Picolibc
模块不能与使用标准 C++ 库的应用程序一起使用。构建 Picolibc 模块将增加编译
应用程序所需的时间。

可以通过在应用程序配置文件中选择 :kconfig:option:`CONFIG_PICOLIBC_USE_MODULE`
来启用 Picolibc 模块。

将 Picolibc 模块更新到较新版本时,:ref:`Zephyr SDK 中捆绑的工具链 Picolibc
<c_library_picolibc_toolchain>` 也必须更新到相同版本。

.. _c_library_picolibc_toolchain:

工具链 Picolibc
==================

从版本 0.16 开始,Zephyr SDK 为每个目标架构包含预编译版本的 Picolibc,
以及预编译版本的 libstdc++。

可以通过在应用程序配置文件中取消选择 :kconfig:option:`CONFIG_PICOLIBC_USE_MODULE`
来启用工具链版本的 Picolibc。

对于 Zephyr 的每个版本,使用 :ref:`推荐版本的 Zephyr SDK
<toolchain_zephyr_sdk_compatibility>` 时,工具链捆绑的 Picolibc 和
:ref:`Picolibc 模块 <c_library_picolibc_module>` 保证同步。

在没有工具链捆绑 Picolibc 的情况下构建
-------------------------------------------

对于没有捆绑 Picolibc 的工具链,仍然可以通过从源代码构建来使用 Picolibc。
请注意,:ref:`c_library_picolibc_module` 中提到的任何限制仍然适用。

要在没有工具链捆绑 Picolibc 的情况下构建,工具链必须启用
:kconfig:option:`CONFIG_PICOLIBC_SUPPORTED`。例如,需要将以下内容添加到
工具链 Kconfig 文件中:

.. code-block:: kconfig

   config TOOLCHAIN_<name>_PICOLIBC_SUPPORTED
      def_bool y
      select PICOLIBC_SUPPORTED

通过启用 :kconfig:option:`CONFIG_PICOLIBC_SUPPORTED`,当没有工具链捆绑的 Picolibc 时,
构建系统将自动使用其模块从源代码构建 Picolibc。

格式化输出
****************

Picolibc 支持所有标准 C 格式化输入和输出函数,包括 :c:func:`printf`、
:c:func:`fprintf`、:c:func:`sprintf` 和 :c:func:`sscanf`。

Picolibc 格式化输入和输出函数实现支持 C17 和 POSIX 2018 标准定义的所有格式说明符,
但有以下例外:

* 浮点格式说明符(例如 ``%f``)需要 :kconfig:option:`CONFIG_PICOLIBC_IO_FLOAT`。

* long long 格式说明符(例如 ``%lld``)需要
  :kconfig:option:`CONFIG_PICOLIBC_IO_LONG_LONG`。此选项会自动通过
  :kconfig:option:`CONFIG_PICOLIBC_IO_FLOAT` 启用。

Printk、cbprintf 及相关功能
****************************

使用 Picolibc 时,Zephyr 格式化输出函数是根据 stdio 调用实现的。这包括:

 * printk、snprintk 和 vsnprintk
 * cbprintf 和 cbvprintf
 * fprintfcb、vfprintfcb、printfcb、vprintfcb、snprintfcb 和 vsnprintfcb

使用标记参数时(:kconfig:option:`CONFIG_CBPRINTF_PACKAGE_SUPPORT_TAGGED_ARGUMENTS`
和 :c:macro:`CBPRINTF_PACKAGE_ARGS_ARE_TAGGED`),对 cbpprintf 的调用不会使用
Picolibc,因此使用这些代码的输出格式将与 Picolibc 结果不同,因为 cbprintf 函数
不完全符合 C/POSIX 标准。

数学函数
**************

Picolibc 为 float、double 和 long double 数学运算提供完整的 C17/`IEEE STD 754-2019`_
支持,Bessel 函数的 long double 版本除外。

.. _`IEEE STD 754-2019`: https://ieeexplore.ieee.org/document/8766229

线程本地存储
********************

Picolibc 使用线程本地存储(TLS)(在支持的情况下)存储应保持每个线程本地的数据,
例如 :c:macro:`errno`。这意味着使用 Picolibc 时会启用 TLS 支持。由于所有 TLS
变量都从线程堆栈区域分配,这可能会影响堆栈大小要求几个字节。

C 库本地变量
*************************

Picolibc 使用一些内部变量来处理诸如堆管理之类的事情。这些变量收集在名为
:c:var:`z_libc_partition` 的专用内存分区中。使用
:kconfig:option:`CONFIG_USERSPACE` 和内存域的应用程序必须确保此分区包含在
Picolibc 调用期间处于活动状态的任何域中。

动态内存管理
*************************

Picolibc 使用 :ref:`通用 C 库 <c_library_common>` 提供的 malloc api 系列实现,
该实现本身建立在 :ref:`内核内存堆 API <heap_v2>` 之上。
