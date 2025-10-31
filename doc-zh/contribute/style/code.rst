.. _general_code_style:

C 代码和通用样式指南 (C Code and General Style Guidelines)
#########################################################

编码风格在任何新代码或修改的代码上被执行,但贡献者不需要修正他们未修改的现有代码的风格。

对于指南未明确提供指导或允许多种有效表达方式的风格方面,贡献者应该遵循树中现有代码的风格,对"附近"代码(首先查看函数,然后是同一文件,然后是子系统等)给予更高的重要性。

一般来说,遵循 `Linux 内核编码风格 (Linux kernel coding style)`_,但以下例外和澄清除外:

* 制表符为 8 个字符。
* 对代码和变量使用 `蛇形命名法 (snake case)`_。
* 行长度为 100 列或更少。在文档中,URL 引用的更长行是允许的例外。
* 为每个 ``if``、``else``、``do``、``while``、``for`` 和 ``switch`` 主体添加括号,即使是单行代码块也是如此。
* 使用空格而不是制表符对齐声明后的注释,根据需要。
* 使用 C89 风格的单行注释 ``/*  */``。不允许使用 C99 风格的单行注释 ``//``。
* 对需要出现在文档中的 doxygen 注释使用 ``/**  */``。
* 避免使用二进制字面量(以 ``0b`` 开头的常量)。
* 避免在代码中使用非 ASCII 符号,除非它显着提高清晰度,在任何情况下都避免使用表情符号。
* 在代码注释中使用正确的名词大写(例如 ``UART`` 而不是 ``uart``,``CMake`` 而不是 ``cmake``)。

.. _Linux kernel coding style:
   https://kernel.org/doc/html/latest/process/coding-style.html

.. _snake case:
   https://en.wikipedia.org/wiki/Snake_case
