.. _c_library_minimal:

最小 libc
############

最基本的 C 库,名为"最小 libc",是 Zephyr 代码库的一部分,提供了满足 Zephyr 及其
子系统需求所需的标准 C 库的最小子集,主要在字符串操作和显示方面。

它占用空间非常小,适合不依赖 ISO C 标准库中不太常用部分的项目。它还可以与多种
不同的工具链一起使用。

最小 libc 实现可以在 Zephyr 主树中的 :file:`lib/libc/minimal` 中找到。

函数
*********

最小 libc 实现了满足 Zephyr 内核需求所需的 ISO/IEC 9899:2011 标准 C 库函数的
最小子集,如 :ref:`编码指南规则 A.4
<coding_guideline_libc_usage_restrictions_in_zephyr_kernel>` 所定义。

格式化输出
****************

最小 libc 没有实现自己的格式化输出处理器;相反,它将 C 标准格式化输出函数
(如 ``printf`` 和 ``sprintf``)映射到 :c:func:`cbprintf` 函数,该函数是 Zephyr
自己的 C99 兼容格式化输出实现。

有关更多详细信息,请参阅 :ref:`格式化输出 <formatted_output>` 操作系统服务文档。

动态内存管理
*************************

最小 libc 使用 :ref:`通用 C 库 <c_library_common>` 提供的 malloc api 系列实现,
该实现本身建立在 :ref:`内核内存堆 API <heap_v2>` 之上。

错误码
*************

错误码在整个 Zephyr API 中用作函数的返回值来表示错误条件。它们通常作为本节中
定义的整数字面量的负值返回,并在 :file:`errno.h` 头文件中定义。

`POSIX errno.h 规范`_ 和其他事实标准源中定义的错误码子集已添加到最小 libc 中。

Zephyr 有意努力保持最小 libc 错误码的值与 Zephyr 支持的 C 标准库的不同实现保持
一致。最小 libc 的 :file:`errno.h` 会与 :ref:`Newlib <c_library_newlib>` 的
进行检查,以确保错误码保持一致。

以下是错误码定义的列表。有关实际数值,请参阅 `errno.h`_。

.. doxygengroup:: system_errno

.. _`POSIX errno.h 规范`: https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/errno.h.html
.. _`errno.h`: https://github.com/zephyrproject-rtos/zephyr/blob/main/lib/libc/minimal/include/errno.h
