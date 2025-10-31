.. _code_data_relocation:

代码和数据重定位 (Code And Data Relocation)
############################################

概述 (Overview)
****************

此功能允许从所需文件重定位 .text、.rodata、.data 和 .bss 节，并将它们放置在所需的内存区域中。
内存区域和文件以字符串的形式提供给 :ref:`gen_relocate_app.py` 脚本。
此脚本始终从 cmake 内部调用。

此脚本提供了一种强大的方法来重新排序内存内容，而无需实际修改代码。
简单来说，此脚本将为一组文件一起完成 ``__attribute__((section("name")))`` 的工作。

可以使用正则表达式过滤器来选择仅需要重定位的节。

详细信息 (Details)
*******************

内存区域和文件通过一个文件提供给 :ref:`gen_relocate_app.py` 脚本，
其中每行指定要放置在给定区域中的文件列表。

这样的文件的示例是：

  .. code-block:: none

     SRAM2:/home/xyz/zephyr/samples/hello_world/src/main.c,
     SRAM1:/home/xyz/zephyr/samples/hello_world/src/main2.c,

此脚本使用以下参数调用：
``python3 gen_relocate_app.py -i input_file -o generated_linker -c generated_code``

Kconfig :kconfig:option:`CONFIG_CODE_DATA_RELOCATION` 选项，
在 ``prj.conf`` 中启用时，将调用脚本并执行所需的重定位。

此脚本还会触发生成 ``linker_relocate.ld`` 和 ``code_relocation.c`` 文件。
``linker_relocate.ld`` 文件创建适当的节，并从所有选定文件链接所需的函数或变量。

.. note::

   文本节在主链接器脚本中分为 2 部分。第一个节将包含一些有关向量表和其他调试相关信息的信息。
   第二个节将有完整的文本节。这是为了强制所需的函数和数据变量到正确的位置所需的。
   这是由于链接器的行为。链接器只会链接一次，因此必须拆分此文本节以为生成的链接器脚本腾出空间。

``code_relocation.c`` 文件包含初始化数据节所需的代码，以及文本节的副本（如果是 XIP）。
此外，这还包含 bss 清零和从 ROM 到所需内存类型的数据复制操作所需的代码。

**调用此功能的过程是：**

* 在 ``prj.conf`` 文件中启用 :kconfig:option:`CONFIG_CODE_DATA_RELOCATION`

* 在项目中的 ``CMakeLists.txt`` 文件中，提及所有需要重定位的文件。

  ``zephyr_code_relocate(FILES src/*.c LOCATION SRAM2)``

  其中第一个参数是文件/文件，第二个参数是必须放置它的内存。

  .. note::

     函数 zephyr_code_relocate() 可以根据需要调用多次。

附加配置 (Additional Configurations)
=====================================

本节显示可以在 ``CMakeLists.txt`` 中设置的附加配置选项。

* 如果内存是 ``SRAM1``、``SRAM2``、``CCD`` 或 ``AON``，
  则将完整的对象放在节中。例如：

  .. code-block:: none

     zephyr_code_relocate(FILES src/file1.c LOCATION SRAM2)
     zephyr_code_relocate(FILES src/file2.c LOCATION SRAM)

* 如果内存类型附加了 ``_DATA``、``_TEXT``、``_RODATA``、``_BSS`` 或 ``_NOINIT``，
  则仅将选定的内存放置在所需的内存区域中。例如：

  .. code-block:: none

     zephyr_code_relocate(FILES src/file1.c LOCATION SRAM2_DATA)
     zephyr_code_relocate(FILES src/file2.c LOCATION SRAM2_TEXT)

* 多个区域也可以附加在一起，例如：``SRAM2_DATA_BSS_NOINIT``。
  这将把所有数据：有值初始化、零初始化和未初始化的数据放在 ``SRAM2`` 中。

* 可以将多个文件传递给 ``FILES`` 参数，或者可以使用 CMake 生成器表达式
  来重定位逗号分隔的文件列表。

  .. code-block:: none

     file(GLOB sources "file*.c")
     zephyr_code_relocate(FILES ${sources} LOCATION SRAM)
     zephyr_code_relocate(FILES $<TARGET_PROPERTY:my_tgt,SOURCES> LOCATION SRAM)

节过滤 (Section Filtering)
===========================

默认情况下，指定文件的所有节都将被重定位。如果使用 ``FILTER``，
则提供正则表达式以仅选择要重定位的节。

正则表达式适用于节名称，当文件使用 ``-ffunction-sections`` 和 ``-fdata-sections`` 构建时
（默认情况下），可以使用它来选择文件的符号。

  .. code-block:: none

     zephyr_code_relocate(FILES src/file1.c FILTER ".*\\.func1|.*\\.func2" LOCATION SRAM2_TEXT)

上面的示例将仅重定位文件 ``src/file1.c`` 的 ``func1()`` 和 ``func2()``

NOKEEP 标志 (NOKEEP flag)
==========================

默认情况下，在生成 ``linker_relocate.ld`` 时，所有重定位的函数和变量都将标记为 ``KEEP()``。
因此，如果任何输入文件恰好包含未使用的符号，则链接器不会丢弃它们，
即使使用 ``--gc-sections`` 调用链接器也是如此。如果您想覆盖此行为，
可以将 ``NOKEEP`` 传递给 ``zephyr_code_relocate()`` 调用。

  .. code-block:: none

     zephyr_code_relocate(FILES src/file1.c LOCATION SRAM2_TEXT NOKEEP)

上面的示例将有助于确保在 ``file1.c`` 的 .text 节中找到的任何未使用的代码不会粘附到 SRAM2。

NOCOPY 标志 (NOCOPY flag)
==========================

当 ``NOCOPY`` 选项传递给 ``zephyr_code_relocate()`` 函数时，
不会在 ``code_relocation.c`` 中生成重定位代码。当我们想要将特定文件
（或文件集）的内容移动到 XIP 区域时，可以使用此标志。

此示例将把 ``xip_external_flash.c`` 文件的 .text 节放置到 ``EXTFLASH`` 内存区域，
在那里将从中执行（XIP）。.data 将像往常一样重定位到 SRAM 中。

  .. code-block:: none

     zephyr_code_relocate(FILES src/xip_external_flash.c LOCATION EXTFLASH_TEXT NOCOPY)
     zephyr_code_relocate(FILES src/xip_external_flash.c LOCATION SRAM_DATA)

重定位库 (Relocating libraries)
================================

可以使用库名称的 LIBRARY 参数将库重定位到 ``zephyr_code_relocation()``。
例如，以下代码段将把串行驱动程序重定位到 SRAM2：

  .. code-block:: none

    zephyr_code_relocate(LIBRARY drivers__serial LOCATION SRAM2)

提示 (Tips)
===========

如果重定位 kernel/arch 文件，请小心，因为某些文件包含在代码重定位发生之前执行的早期初始化代码。

可能需要额外的 MPU/MMU 配置，以确保目标内存区域被配置为允许代码执行。

示例/测试 (Samples/ Tests)
==========================

展示此功能的测试在 ``$ZEPHYR_BASE/tests/application_development/code_relocation`` 中提供

此测试显示如何使用代码重定位功能。

此测试将使用从 ``include/zephyr/arch/arm/cortex_m/scripts/linker.ld`` 派生的自定义链接器文件
将 3 个文件中的 .text、.data、.bss 放置到 SRAM 的各个部分

展示 NOCOPY 标志的示例在此处提供：:zephyr:code-sample:`code_relocation_nocopy`。
