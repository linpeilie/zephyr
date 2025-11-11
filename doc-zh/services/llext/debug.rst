.. _llext_debug:

调试扩展 (Debugging extensions)
################################

调试扩展是一项复杂的任务。由于扩展代码根据定义不是与 Zephyr 应用程序一起构建的,因此最终的 Zephyr ELF 文件不包含扩展代码的符号。此外,扩展在运行时由 :c:func:`llext_load` 动态重定位,因此即使符号可用,调试器也无法知道扩展代码中符号的最终位置。(Debugging extensions is a complex task. Since the extension code is by definition not built with the Zephyr application, the final Zephyr ELF file does not contain the symbols for extension code. Furthermore, the extension is dynamically relocated by :c:func:`llext_load` at runtime, so even if the symbols were available, it would be impossible for the debugger to know the final locations of the symbols in the extension code.)

在这种情况下正确设置调试器会话需要几个手动步骤。以下部分将提供有关如何使用 Zephyr SDK 和 ``west`` 提供的调试功能执行此操作的一些提示,但这些说明可以适应任何基于 GDB 的调试环境。(Setting up the debugger session properly in this case requires a few manual steps. The following sections will provide some tips on how to do it with the Zephyr SDK and the debug features provided by ``west``, but the instructions can be adapted to any GDB-based debugging environment.)

扩展调试过程 (Extension debugging process)
==========================================

1. 确保项目设置为显示详细的 LLEXT 调试输出(设置 :kconfig:option:`CONFIG_LOG` 和 :kconfig:option:`CONFIG_LLEXT_LOG_LEVEL_DBG`)。(Make sure the project is set up to display the verbose LLEXT debug output (:kconfig:option:`CONFIG_LOG` and :kconfig:option:`CONFIG_LLEXT_LOG_LEVEL_DBG` are set).)

2. 构建 Zephyr 应用程序和扩展。(Build the Zephyr application and the extensions.)

   对于当前构建中包含的每个目标 ``name``,将在构建根目录的 ``llext`` 子目录中生成两个文件:(For each target ``name`` included in the current build, two files will be generated into the ``llext`` subdirectory of the build root:)

   ``name_ext_debug.elf``

        包含完整调试信息的中间 ELF 文件。(An intermediate ELF file with full debugging information.)

   ``name.llext``

        最终扩展二进制文件,剥离到加载到 Zephyr 应用程序所需的基本数据。(The final extension binary, stripped to the essential data required for loading into the Zephyr application.)

   根据目标架构和构建配置,可能存在其他文件。(Other files may be present, depending on the target architecture and the build configuration.)

3. 启动主 Zephyr 应用程序的调试会话。这在文档的 :ref:`调试 <west-debugging>` 部分中描述;在支持的板上,运行 ``west debug`` 就很容易,可能需要一些其他参数。(Start a debugging session of the main Zephyr application. This is described in the :ref:`Debugging <west-debugging>` section of the documentation; on supported boards it is as easy as running ``west debug``, perhaps with some additional arguments.)

4. 在代码中的 :c:func:`llext_load` 函数之后设置一个断点并让其运行。这将把扩展加载到内存中并重定位它。输出日志将包含一行 ``gdb add-symbol-file flags:``,后跟所有以 ``-s`` 开头的行。(Set a breakpoint just after the :c:func:`llext_load` function in your code and let it run. This will load the extension into memory and relocate it. The output logs will contain a line with ``gdb add-symbol-file flags:``, followed by lines all starting with ``-s``.)

5. 在 GDB 控制台中键入此命令以加载此扩展的符号:(Type this command in the GDB console to load this extension's symbols:)

   .. code-block::

      add-symbol-file <path-to-debug.elf> <load-addresses>

   其中 ``<path-to-debug.elf>`` 是步骤 2 中标识的带有调试信息的 ELF 文件的完整路径,``<load-addresses>`` 是从上一步骤的日志中收集的所有 ``-s`` 行的空格分隔列表。(where ``<path-to-debug.elf>`` is the full path of the ELF file with debug information identified in step 2, and ``<load-addresses>`` is a space separated list of all the ``-s`` lines collected from the log in the previous step.)

6. 扩展符号现在可供调试器使用。您可以像往常一样设置断点、检查变量和逐步执行代码。(The extension symbols are now available to the debugger. You can set breakpoints, inspect variables, and step through the code as usual.)

如果有多个扩展,可以为应用程序加载的每个扩展重复步骤 4-6。(Steps 4-6 can be repeated for every extension that is loaded by the application, if there are several.)

符号查找问题 (Symbol lookup issues)
====================================

.. warning::

   几乎可以肯定,加载的符号将被主应用程序中的其他符号遮蔽;例如,它们可能位于 ELF 缓冲区或 LLEXT 堆的内存区域内。(It is almost certain that the loaded symbols will be shadowed by others in the main application; for example, they may be located inside the memory area of the ELF buffer or the LLEXT heap.)

   在这种情况下,GDB 选择第一个已知符号,因此将地址关联到某个 ``elf_buffer+0x123`` 而不是预期的 ``ext_fn``。这进一步混淆了其高级操作,如源代码单步执行或检查局部变量,因为它们在该上下文中没有意义。(In this case GDB chooses the first known symbol and therefore associates the addresses to some ``elf_buffer+0x123`` instead of an expected ``ext_fn``. This further confuses its high-level operations like source stepping or inspecting locals, since they are meaningless in that context.)

以下段落讨论了此问题的两种可能解决方案。(Two possible solutions to this problem are discussed in the following paragraphs.)

丢弃所有 Zephyr 符号 (Discard all Zephyr symbols)
----------------------------------------------------

最简单的选项是在步骤 5 之前通过不带参数调用 ``add-symbol-file`` 从 GDB 中删除所有 Zephyr 应用程序符号。但是,这将使调试会话仅关注 llext,因为有关 Zephyr 应用程序的所有信息都将丢失。例如,调试器可能无法正确跟踪扩展代码之外的堆栈跟踪。(The simplest option is to drop all the Zephyr application symbols from GDB by invoking ``add-symbol-file`` with no arguments, before step 5. This will however focus the debugging session to the llext only, as all information about the Zephyr application will be lost. For example, the debugger may not be able to properly follow stack traces outside the extension code.)

可以在同一会话中多次使用相同的技术在主符号表和扩展符号表之间切换,但这很快就会变得麻烦。(It is possible to use the same technique multiple times in the same session to switch between the main and extension symbol tables as required, but it rapidly becomes cumbersome.)

编辑 ELF 文件 (Edit the ELF file)
----------------------------------

这种替代方法更复杂,但可以提供更无缝的调试体验。这个想法是编辑主 Zephyr ELF 文件以删除与要调试的扩展重叠的符号的信息,以便在加载扩展符号时,GDB 不会有任何歧义。这可以通过使用带有 ``-N <symbol>`` 选项的 ``objcopy`` 来完成。(This alternative is more complex but allows for a more seamless debugging experience. The idea is to edit the main Zephyr ELF file to remove information about the symbols that overlap with the extension that is to be debugged, so that when the extension symbols are loaded, GDB will not have any ambiguity. This can be done by using ``objcopy`` with the ``-N <symbol>`` option.)

然而,识别有问题的符号是一个迭代试错过程,因为可以有许多不同的层;例如,ELF 缓冲区本身可能包含在数据段的符号中。幸运的是,这些知识可以多次使用,因为对于给定项目,列表不太可能改变。(Identifying the offending symbols is however an iterative trial-and-error procedure, as there can be many different layers; for example, the ELF buffer may be itself contained in a symbol for the data segment. Fortunately, this knowledge can then be used several times as the list is unlikely to change for a given project.)

示例调试会话 (Example debugging session)
=========================================

此示例演示了如何在基于 ARM Cortex-M3 的模拟 ``mps2/an385`` 板上调试 ``tests/subsys/llext`` 项目中的 ``detached_fn`` 扩展(特别是 ``writable`` 案例)。(This example demonstrates how to debug the ``detached_fn`` extension in the ``tests/subsys/llext`` project (specifically, the ``writable`` case), on an emulated ``mps2/an385`` board which is based on an ARM Cortex-M3.)

.. note::

   下面的日志是使用 Zephyr 4.1 版本和 Zephyr SDK 0.17.0 版本获得的。但是,即使使用相同的版本,确切的地址在不同运行之间仍可能有所不同。调整下面的命令以匹配您自己会话的结果。(The logs below have been obtained using Zephyr version 4.1 and the Zephyr SDK version 0.17.0. However, the exact addresses may still vary between runs even when using the same versions. Adjust the commands below to match the results of your own session.)

以下命令将构建项目并在调试模式下启动模拟器:(The following command will build the project and start the emulator in debugging mode:)

.. code-block::
   :caption: 终端 1(构建、QEMU 模拟器、GDB 服务器) (Terminal 1 (build, QEMU emulator, GDB server))

   zephyr$ west build -p -b mps2/an385 tests/subsys/llext/ -T llext.writable -t debugserver_qemu
   -- west build: generating a build system
   [...]
   -- west build: running target debugserver_qemu
   [...]
   [186/187] To exit from QEMU enter: 'CTRL+a, x'[QEMU] CPU: cortex-m3

在单独的终端上,将 ``ZEPHYR_SDK_INSTALL_DIR`` 设置为您安装的 Zephyr SDK 的目录,然后为目标启动 GDB 客户端:(On a separate terminal, set ``ZEPHYR_SDK_INSTALL_DIR`` to the directory for the Zephyr SDK on your installation, then start the GDB client for the target:)

.. code-block::
   :caption: 终端 2(GDB 客户端) (Terminal 2 (GDB client))

   zephyr$ export LLEXT_SDK_INSTALL_DIR=/opt/zephyr-sdk-0.17.0
   zephyr$ ${LLEXT_SDK_INSTALL_DIR}/arm-zephyr-eabi/bin/arm-zephyr-eabi-gdb build/zephyr/zephyr.elf
   GNU gdb (Zephyr SDK 0.17.0) 12.1
   [...]
   Reading symbols from build/zephyr/zephyr.elf...
   (gdb)

连接,在 ``llext_load`` 函数上设置断点并运行直到完成:(Connect, set a breakpoint on the ``llext_load`` function and run until it finishes:)

.. code-block::
   :caption: 终端 2(GDB 客户端) (Terminal 2 (GDB client))

   (gdb) target extended-remote :1234
   Remote debugging using :1234
   z_arm_reset () at zephyr/arch/arm/core/cortex_m/reset.S:124
   124         movs.n r0, #_EXC_IRQ_DEFAULT_PRIO
   (gdb) break llext_load
   Breakpoint 1 at 0x236c: file zephyr/subsys/llext/llext.c, line 168.
   (gdb) continue
   Continuing.

   Breakpoint 1, llext_load (ldr=ldr@entry=0x2000bef0 <ztest_thread_stack+3488>,
                             name=name@entry=0x9d98 "test_detached",
                             ext=ext@entry=0x2000abb8 <detached_llext>,
                             ldr_parm=ldr_parm@entry=0x2000bee8 <ztest_thread_stack+3480>)
                 at zephyr/subsys/llext/llext.c:168
   168             *ext = llext_by_name(name);
   (gdb) finish
   Run till exit from #0  llext_load ([...])
       at zephyr/subsys/llext/llext.c:168
   llext_test_detached () at zephyr/tests/subsys/llext/src/test_llext.c:481
   481             zassert_ok(res, "load should succeed");

第一个终端将打印大量与扩展加载相关的调试信息。查找带有地址的部分:(The first terminal will have printed lots of debugging information related to the extension loading. Find the section with the addresses:)

.. code-block::
   :caption: 终端 1(构建、QEMU 模拟器、GDB 服务器) (Terminal 1 (build, QEMU emulator, GDB server))

   [...]
   D: Allocate and copy regions...
   [...]
   D: gdb add-symbol-file flags:
   D: -s .text 0x20000034
   D: -s .data 0x200000b4
   D: -s .bss 0x2000c2e0
   D: -s .rodata 0x200000b8
   D: -s .detach 0x200001d0
   D: Counting exported symbols...
   [...]

使用这些地址将符号加载到 GDB 中:(Use these addresses to load the symbols into GDB:)

.. code-block::
   :caption: Terminal 2 (GDB client)

   (gdb) add-symbol-file build/llext/detached_fn_ext_debug.elf -s .text 0x20000034 -s .data 0x200000b4 -s .bss 0x2000c2e0 -s .rodata 0x200000b8 -s .detach 0x200001d0
   add symbol table from file "build/llext/detached_fn_ext_debug.elf" at
           .text_addr = 0x20000034
           .data_addr = 0x200000b4
           .bss_addr = 0x2000c2e0
           .rodata_addr = 0x200000b8
           .detach_addr = 0x200001d0
   (y or n) y
   Reading symbols from build/llext/detached_fn_ext_debug.elf...
   (gdb) break detached_entry
   Breakpoint 2 at 0x200001d0 (2 locations)
   (gdb) continue
   Continuing.

   Breakpoint 2, 0x200001d0 in test_detached_ext ()
   (gdb) backtrace
   #0  0x200001d0 in test_detached_ext ()
   #1  0x200000ac in test_detached_ext ()
   #2  0x00000706 in llext_test_detached () at zephyr/tests/subsys/llext/src/test_llext.c:496
   #3  0x00001a36 in run_test_functions (suite=0x92bc <z_ztest_test_node_llext>, data=0x0 <cbvprintf_package>, test=0x92d8 <z_ztest_unit_test.llext.test_detached>) at zephyr/subsys/testsuite/ztest/src/ztest.c:328
   #4  test_cb (a=0x92bc <z_ztest_test_node_llext>, b=0x92d8 <z_ztest_unit_test.llext.test_detached>, c=0x0 <cbvprintf_package>) at zephyr/subsys/testsuite/ztest/src/ztest.c:662
   #5  0x00000e96 in z_thread_entry (entry=0x1a05 <test_cb>, p1=0x92bc <z_ztest_test_node_llext>, p2=0x92d8 <z_ztest_unit_test.llext.test_detached>, p3=0x0 <cbvprintf_package>) at zephyr/lib/os/thread_entry.c:48
   #6  0x00000000 in ?? ()

与断点位置和最后堆栈帧相关的符号错误地引用了 Zephyr 应用程序中的 ELF 缓冲区而不是扩展符号。请注意,GDB 确实知道两者:(The symbol associated with the breakpoint location and the last stack frames mistakenly reference the ELF buffer in the Zephyr application instead of the extension symbols. Note that GDB however knows both:)

.. code-block::
   :caption: 终端 2(GDB 客户端) (Terminal 2 (GDB client))

   (gdb) info sym 0x200001d0
   test_detached_ext + 464 in section datas of zephyr/build/zephyr/zephyr.elf
   detached_entry in section .detach of zephyr/build/llext/detached_fn_ext_debug.elf
   (gdb) info sym 0x200000ac
   test_detached_ext + 172 in section datas of zephyr/build/zephyr/zephyr.elf
   test_entry + 8 in section .text of zephyr/build/llext/detached_fn_ext_debug.elf

检查扩展中的变量或正确逐步执行代码也是不可能的:(It is also impossible to inspect the variables in the extension or step through code properly:)

.. code-block::
   :caption: 终端 2(GDB 客户端) (Terminal 2 (GDB client))

   (gdb) print bss_cnt
   No symbol "bss_cnt" in current context.
   (gdb) print data_cnt
   No symbol "data_cnt" in current context.
   (gdb) next
   Single stepping until exit from function test_detached_ext,
   which has no line number information.

   Breakpoint 2, 0x200001ea in test_detached_ext ()
   (gdb)

丢弃符号 (Discarding symbols)
------------------------------

丢弃 Zephyr 符号并仅关注扩展将恢复完整的调试功能,但代价是失去全局上下文(注意回溯在扩展之外停止):(Discarding the Zephyr symbols and only focusing on the extension restores full debugging functionality at the cost of losing the global context (note the backtrace stops outside the extension):)

.. code-block::
   :caption: Terminal 2 (GDB client)

   (gdb) symbol-file
   Discard symbol table from `zephyr/build/zephyr/zephyr.elf'? (y or n) y
   Error in re-setting breakpoint 1: No symbol table is loaded.  Use the "file" command.
   No symbol file now.
   (gdb) add-symbol-file build/llext/detached_fn_ext_debug.elf -s .text 0x20000034 -s .data 0x200000b4 -s .bss 0x2000c2e0 -s .rodata 0x200000b8 -s .detach 0x200001d0
   add symbol table from file "build/llext/detached_fn_ext_debug.elf" at
           .text_addr = 0x20000034
           .data_addr = 0x200000b4
           .bss_addr = 0x2000c2e0
           .rodata_addr = 0x200000b8
           .detach_addr = 0x200001d0
   (y or n) y
   Reading symbols from build/llext/detached_fn_ext_debug.elf...
   (gdb) backtrace
   #0  detached_entry () at zephyr/tests/subsys/llext/src/detached_fn_ext.c:18
   #1  0x200000ac in test_entry () at zephyr/tests/subsys/llext/src/detached_fn_ext.c:26
   #2  0x00000706 in ?? ()
   Backtrace stopped: previous frame identical to this frame (corrupt stack?)
   (gdb) next
   19              zassert_true(data_cnt < 0);
   (gdb) print bss_cnt
   $1 = 1
   (gdb) print data_cnt
   $2 = -2
   (gdb)


编辑 ELF 文件 (Editing the ELF file)
--------------------------------------

在这种替代方法中,必须在终端 1 上构建 Zephyr 二进制文件并启动模拟器之后,但在终端 2 上启动 GDB 客户端之前,对 Zephyr ELF 文件进行修补。(In this alternative approach, the patches to the Zephyr ELF file must be performed after building the Zephyr binary and starting the emulator on Terminal 1, but before starting the GDB client on Terminal 2.)

上面的调试会话已经识别出 ``test_detached_ext``(持有 ELF 文件的字符数组)是一个有问题的符号,因此将在第一次尝试中将其删除。多次执行相同的步骤后,还可以发现 ``__data_start`` 和 ``__data_region_start`` 也与感兴趣的内存区域重叠。(The above debugging session already identified ``test_detached_ext``, the char array that holds the ELF file, as an offending symbol, so that will be removed in a first pass. Performing the same steps multiple times, ``__data_start`` and ``__data_region_start`` can also be found to overlap the memory area of interest.)

以下命令将从 Zephyr ELF 文件中删除所有这些符号,然后在修改后的文件上启动调试会话:(The following commands will remove all of these from the Zephyr ELF file, then start a debugging session on the modified file:)

.. code-block::
   :caption: 终端 2(GDB 客户端) (Terminal 2 (GDB client))

   zephyr$ export LLEXT_SDK_INSTALL_DIR=/opt/zephyr-sdk-0.17.0
   zephyr$ ${LLEXT_SDK_INSTALL_DIR}/arm-zephyr-eabi/bin/arm-zephyr-eabi-objcopy -N test_detached_ext -N __data_start -N __data_region_start build/zephyr/zephyr.elf build/zephyr/zephyr-edit.elf
   zephyr$ ${LLEXT_SDK_INSTALL_DIR}/arm-zephyr-eabi/bin/arm-zephyr-eabi-gdb build/zephyr/zephyr-edit.elf
   GNU gdb (Zephyr SDK 0.17.0) 12.1
   [...]
   Reading symbols from build/zephyr/zephyr-edit.elf...
   (gdb)

可以再次执行上一次运行中使用的相同步骤,以附加到 GDB 服务器并加载扩展及其调试符号。但是,这次结果却大不相同:(The same steps used in the previous run can be performed again to attach to the GDB server and load both the extension and its debug symbols. This time, however, the result is rather different:)

 * ``break`` 命令包括行号信息;(the ``break`` command includes line number information;)

 * ``backtrace`` 的输出包含来自扩展和 Zephyr 应用程序的函数;(the output from ``backtrace`` contains functions from both the extension and the Zephyr application;)

 * 可以正确检查局部变量。(the local variables can be properly inspected.)

.. code-block::
   :caption: Terminal 2 (GDB client)

   (gdb) add-symbol-file build/llext/detached_fn_ext_debug.elf [...]
   [...]
   Reading symbols from build/llext/detached_fn_ext_debug.elf...
   (gdb) break detached_entry
   Breakpoint 2 at 0x200001d6: file zephyr/tests/subsys/llext/src/detached_fn_ext.c, line 17.
   (gdb) continue
   Continuing.

   Breakpoint 2, detached_entry () at zephyr/tests/subsys/llext/src/detached_fn_ext.c:17
   17              printk("bss %u @ %p\n", bss_cnt++, &bss_cnt);
   (gdb) backtrace
   #0  detached_entry () at zephyr/tests/subsys/llext/src/detached_fn_ext.c:17
   #1  0x200000ac in test_entry () at zephyr/tests/subsys/llext/src/detached_fn_ext.c:26
   #2  0x00000706 in llext_test_detached () at zephyr/tests/subsys/llext/src/test_llext.c:496
   #3  0x00001a36 in run_test_functions (suite=0x92bc <z_ztest_test_node_llext>, data=0x0 <cbvprintf_package>, test=0x92d8 <z_ztest_unit_test.llext.test_detached>) at zephyr/subsys/testsuite/ztest/src/ztest.c:328
   #4  test_cb (a=0x92bc <z_ztest_test_node_llext>, b=0x92d8 <z_ztest_unit_test.llext.test_detached>, c=0x0 <cbvprintf_package>) at zephyr/subsys/testsuite/ztest/src/ztest.c:662
   #5  0x00000e96 in z_thread_entry (entry=0x1a05 <test_cb>, p1=0x92bc <z_ztest_test_node_llext>, p2=0x92d8 <z_ztest_unit_test.llext.test_detached>, p3=0x0 <cbvprintf_package>) at zephyr/lib/os/thread_entry.c:48
   #6  0x00000000 in ?? ()
   (gdb) print bss_cnt
   $1 = 0
   (gdb) print data_cnt
   $2 = -3
   (gdb)
