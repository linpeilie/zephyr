.. _gdbstub:

GDB存根 (GDB stub)
##################

.. contents::
   :local:
   :depth: 2

概述 (Overview)
****************

gdbstub功能提供了GDB远程串行协议(RSP)的实现,允许您使用GDB远程调试Zephyr (The gdbstub feature provides an implementation of the GDB Remote Serial Protocol (RSP) that allows you to remotely debug Zephyr using GDB)。

该协议支持不同的连接类型:串行、UDP/IP和TCP/IP (The protocol supports different connection types: serial, UDP/IP and TCP/IP)。Zephyr目前仅支持串行设备通信 (Zephyr currently supports only serial device communication)。

GDB程序充当客户端,而Zephyr gdbstub充当服务器 (The GDB program acts as a client while the Zephyr gdbstub acts as a server)。当启用此功能时,Zephyr在 :c:func:`gdb_init` 启动gdbstub服务后停止执行并等待GDB连接 (When this feature is enabled, Zephyr stops its execution after :c:func:`gdb_init` starts gdbstub service and waits for a GDB connection)。一旦建立连接,就可以同步地与Zephyr交互 (Once a connection is established it is possible to synchronously interact with Zephyr)。请注意,目前无法异步向目标发送命令 (Note that currently it is not possible to asynchronously send commands to the target)。

功能 (Features)
********

支持以下功能 (The following features are supported):

* 添加和删除断点 (Add and remove breakpoints)
* 继续和单步执行目标 (Continue and step the target)
* 打印回溯 (Print backtrace)
* 读取或写入通用寄存器 (Read or write general registers)
* 读取或写入内存 (Read or write the memory)

启用GDB存根 (Enabling GDB Stub)
*****************

可以使用 :kconfig:option:`CONFIG_GDBSTUB` 选项启用GDB存根 (GDB stub can be enabled with the :kconfig:option:`CONFIG_GDBSTUB` option)。

使用串行后端 (Using Serial Backend)
====================

GDB存根的串行后端可以使用 :kconfig:option:`CONFIG_GDBSTUB_SERIAL_BACKEND` 选项启用 (The serial backend for GDB stub can be enabled with the :kconfig:option:`CONFIG_GDBSTUB_SERIAL_BACKEND` option)。

由于串行后端利用UART设备发送和接收GDB命令 (Since serial backend utilizes UART devices to send and receive GDB commands):

* 如果板上有空闲的UART设备,请将chosen节点的 ``zephyr,gdbstub-uart`` 属性设置为空闲的UART设备,以便 :c:func:`printk` 和日志消息不会打印到用于GDB的同一UART设备 (If there are spare UART devices on the board, set ``zephyr,gdbstub-uart`` property of the chosen node to the spare UART device so that :c:func:`printk` and log messages are not being printed to the same UART device used for GDB)。

* 对于只有一个UART设备的板,如果 :c:func:`printk` 和日志记录也使用同一UART设备进行输出,则必须禁用它们 (For boards with only one UART device, :c:func:`printk` and logging must be disabled if they are also using the same UART device for output)。
  GDB相关消息可能与日志消息交错,这可能会产生意外后果 (GDB related messages may interleave with log messages which may have unintended consequences)。通常可以通过禁用 :kconfig:option:`CONFIG_PRINTK` 和 :kconfig:option:`CONFIG_LOG` 来完成此操作 (Usually this can be done by disabling :kconfig:option:`CONFIG_PRINTK` and :kconfig:option:`CONFIG_LOG`)。

调试 (Debugging)
*********

使用串行后端 (Using Serial Backend)
====================

#. 在启用GDB存根和串行后端的情况下构建 (Build with GDB stub and serial backend enabled)。

#. 将构建的镜像刷写到板上并重置板 (Flash built image onto board and reset the board)。

   * 执行现在应该在 :c:func:`gdb_init` 处暂停 (Execution should now be paused at :c:func:`gdb_init`)。

#. 在开发机器上执行GDB并连接到GDB存根 (Execute GDB on development machine and connect to the GDB stub)。

   .. code-block:: bash

      target remote <serial device>

   例如 (For example),

   .. code-block:: bash

      target remote /dev/ttyUSB1

#. 可以使用GDB命令开始调试 (GDB commands can be used to start debugging)。

示例 (Example)
*******

有一个测试应用程序 :zephyr_file:`tests/subsys/debug/gdbstub`,其测试用例之一 ``debug.gdbstub.breakpoints`` 演示了如何使用Zephyr GDB存根 (There is a test application :zephyr_file:`tests/subsys/debug/gdbstub` with one of its test cases ``debug.gdbstub.breakpoints`` demonstrating how the Zephyr GDB stub can be used)。
该测试还有一个用例连接到QEMU的GDB存根实现(在自定义端口 ``tcp:1235`` )作为参考,以验证测试脚本本身 (The test also has a case to connect to the QEMU's GDB stub implementation (at a custom port ``tcp:1235``) as a reference to validate the test script itself)。

从您的 :envvar:`ZEPHYR_BASE` 目录使用以下命令运行测试 (Run the test with the following command from your :envvar:`ZEPHYR_BASE` directory):

   .. code-block:: console

      ./scripts/twister -p qemu_x86 -T tests/subsys/debug/gdbstub

测试应成功运行,现在让我们一步步做类似的事情 (The test should run successfully, and now let's do something similar step-by-step)
来通过Zephyr gdbstub与QEMU交互并调试示例应用程序 (to interact with QEMU through Zephyr's gdbstub and debug a sample application):

#. 在第一个终端中,从 :envvar:`ZEPHYR_BASE` 目录,使用GDB存根和Twister运行示例应用程序 (On the first terminal, from the :envvar:`ZEPHYR_BASE` directory, run the sample application with GDB stub and Twister):

   .. zephyr-app-commands::
      :app: samples/hello_world
      :board: qemu_x86
      :gen-args: '-DCONFIG_GDBSTUB=y -DCONFIG_GDBSTUB_SERIAL_BACKEND=y'
      :gen-args: '-DCONFIG_QEMU_EXTRA_FLAGS="-serial tcp:localhost:5678,server"'
      :goals: build run

   注意我们如何设置 :kconfig:option:`CONFIG_QEMU_EXTRA_FLAGS` 将QEMU串行控制台端口定向到 ``localhost`` TCP端口 ``5678`` 以等待来自我们将在下一步执行的GDB ``remote`` 命令的连接 (Note how we set :kconfig:option:`CONFIG_QEMU_EXTRA_FLAGS` to direct QEMU serial console port to the ``localhost`` TCP port ``5678`` to wait for a connection from the GDB ``remote`` command we are going to do on the next steps)。

#. 在第二个终端中,启动GDB (On the second terminal, start GDB):

   .. code-block:: bash

      <SDK install directory>/x86_64-zephyr-elf/bin/x86_64-zephyr-elf-gdb

   #. 告诉GDB在哪里查找构建的ELF文件 (Tell GDB where to look for the built ELF file):

      .. code-block:: text

         (gdb) symbol-file <build directory>/zephyr/zephyr.elf

      GDB的响应 (Response from GDB):

      .. code-block:: text

         Reading symbols from <build directory>/zephyr/zephyr.elf...

   #. 告诉GDB连接到Zephyr gdbstub串行后端,该后端之前通过QEMU的TCP端口 ``-serial`` 重定向作为服务器公开 (Tell GDB to connect to the Zephyr gdbstub serial backend which is exposed earlier as a server through the TCP port ``-serial`` redirection at QEMU)。

      .. code-block:: text

         (gdb) target remote localhost:5678

      GDB的响应 (Response from GDB):

      .. code-block:: text

         Remote debugging using localhost:5678
         arch_gdb_init () at <ZEPHYR_BASE>/arch/x86/core/ia32/gdbstub.c:252
         252     }

      GDB还显示代码执行停止的位置 (GDB also shows where the code execution is stopped)。在这种情况下,它在 :zephyr_file:`arch/x86/core/ia32/gdbstub.c` 的第252行 (In this case, it is at :zephyr_file:`arch/x86/core/ia32/gdbstub.c`, line 252)。

   #. 使用命令 ``bt`` 或 ``backtrace`` 显示栈帧的回溯 (Use command ``bt`` or ``backtrace`` to show the backtrace of stack frames)。

to demonstrate how the Zephyr GDB stub works from the GDB user's perspective.

In the snippets below use and expect your appropriate directories instead of
``<SDK install directory>``, ``<build_directory>``, ``<ZEPHYR_BASE>``.


#. Open two terminal windows.

#. On the first terminal, build and run the test application:

   .. zephyr-app-commands::
      :zephyr-app: tests/subsys/debug/gdbstub
      :host-os: unix
      :board: qemu_x86
      :gen-args: '-DCONFIG_QEMU_EXTRA_FLAGS="-serial tcp:localhost:5678,server"'
      :goals: build run

   Note how we set :kconfig:option:`CONFIG_QEMU_EXTRA_FLAGS` to direct QEMU serial
   console port to the ``localhost`` TCP port ``5678`` to wait for a connection
   from the GDB ``remote`` command we are going to do on the next steps.

#. On the second terminal, start GDB:

   .. code-block:: bash

      <SDK install directory>/x86_64-zephyr-elf/bin/x86_64-zephyr-elf-gdb

   #. Tell GDB where to look for the built ELF file:

      .. code-block:: text

         (gdb) symbol-file <build directory>/zephyr/zephyr.elf

      Response from GDB:

      .. code-block:: text

         Reading symbols from <build directory>/zephyr/zephyr.elf...

   #. Tell GDB to connect to the Zephyr gdbstub serial backend which is exposed
      earlier as a server through the TCP port ``-serial`` redirection at QEMU.

      .. code-block:: text

         (gdb) target remote localhost:5678

      Response from GDB:

      .. code-block:: text

         Remote debugging using localhost:5678
         arch_gdb_init () at <ZEPHYR_BASE>/arch/x86/core/ia32/gdbstub.c:252
         252     }

      GDB also shows where the code execution is stopped. In this case,
      it is at :zephyr_file:`arch/x86/core/ia32/gdbstub.c`, line 252.

   #. Use command ``bt`` or ``backtrace`` to show the backtrace of stack frames.

      .. code-block:: text

         (gdb) bt
         #0  arch_gdb_init () at <ZEPHYR_BASE>/arch/x86/core/ia32/gdbstub.c:252
         #1  0x00104140 in gdb_init () at <ZEPHYR_BASE>/zephyr/subsys/debug/gdbstub.c:852
         #2  0x00109c13 in z_sys_init_run_level (level=INIT_LEVEL_PRE_KERNEL_2) at <ZEPHYR_BASE>/kernel/init.c:360
         #3  0x00109e73 in z_cstart () at <ZEPHYR_BASE>/kernel/init.c:630
         #4  0x00104422 in z_prep_c (arg=0x1245bc <x86_cpu_boot_arg>) at <ZEPHYR_BASE>/arch/x86/core/prep_c.c:80
         #5  0x001000c9 in __csSet () at <ZEPHYR_BASE>/arch/x86/core/ia32/crt0.S:290
         #6  0x001245bc in uart_dev ()
         #7  0x00134988 in z_interrupt_stacks ()
         #8  0x00000000 in ?? ()

   #. 使用命令 ``list`` 显示代码执行停止位置的源代码和周围内容 (Use command ``list`` to show the source code and surroundings where code execution is stopped)。

      .. code-block:: text

         (gdb) list
         247             __asm__ volatile ("int3");
         248
         249     #ifdef CONFIG_GDBSTUB_TRACE
         250             printk("gdbstub:%s GDB is connected\n", __func__);
         251     #endif
         252     }
         253
         254     /* Hook current IDT. */
         255     _EXCEPTION_CONNECT_NOCODE(z_gdb_debug_isr, IV_DEBUG, 3);
         256     _EXCEPTION_CONNECT_NOCODE(z_gdb_break_isr, IV_BREAKPOINT, 3);

   #. 使用命令 ``s`` 或 ``step`` 单步执行程序,直到到达不同的源代码行 (Use command ``s`` or ``step`` to step through program until it reaches a different source line)。现在它完成了执行 :c:func:`arch_gdb_init` 并在 :c:func:`gdb_init` 中继续 (Now that it finished executing :c:func:`arch_gdb_init` and is continuing in :c:func:`gdb_init`)。

      .. code-block:: text

         (gdb) s
         gdb_init () at <ZEPHYR_BASE>/subsys/debug/gdbstub.c:857
         857     return 0;

      .. code-block:: text

         (gdb) list
         852             arch_gdb_init();
         853
         854     #ifdef CONFIG_GDBSTUB_TRACE
         855             printk("gdbstub:%s exit\n", __func__);
         856     #endif
         857             return 0;
         858     }
         859
         860     #ifdef CONFIG_XTENSA
         861     /*

   #. 使用命令 ``br`` 或 ``break`` 设置断点 (Use command ``br`` or ``break`` to setup a breakpoint)。对于此示例,在 :c:func:`main` 处设置断点,并使用命令 ``c``(或 ``continue``)让代码执行继续而不进行任何干预 (For this example set up a breakpoint at :c:func:`main`, and let code execution continue without any intervention using command ``c`` (or ``continue``))。

      .. code-block:: text

         (gdb) break main
         Breakpoint 1 at 0x10064d: file <ZEPHYR_BASE>/tests/subsys/debug/gdbstub/src/main.c, line 27.

      .. code-block:: text

         (gdb) continue
         Continuing.

      一旦代码执行到达 :c:func:`main`,执行将停止并返回GDB提示符 (Once code execution reaches :c:func:`main`, execution will be stopped and GDB prompt returns)。

      .. code-block:: text

         Breakpoint 1, main () at <ZEPHYR_BASE>/tests/subsys/debug/gdbstub/src/main.c:27
         27              printk("%s():enter\n", __func__);

      现在GDB在 :c:func:`main` 的开头等待 (Now GDB is waiting at the beginning of :c:func:`main`):

      .. code-block:: text

         (gdb) list
         22
         23      int main(void)
         24      {
         25              int ret;
         26
         27              printk("%s():enter\n", __func__);
         28              ret = test();
         29              printk("ret=%d\n", ret);
         30              return 0;
         31      }

   #. 要检查 ``ret`` 的值,可以使用命令 ``p`` 或 ``print`` (To examine the value of ``ret``, the command ``p`` or ``print`` can be used)。

      .. code-block:: text

         (gdb) p ret
         $1 = 1273788

      由于 ``ret`` 尚未初始化,它包含一些随机值 (Since ``ret`` has not been initialized, it contains some random value)。

   #. 如果在这里使用step(``s`` 或 ``step``),它将继续执行跳过 :c:func:`test` 的内部 (If step (``s`` or ``step``) is used here, it will continue execution skipping the interior of :c:func:`test`)。
      要检查 :c:func:`test` 内部的代码执行 (To examine code execution inside :c:func:`test`),
      可以为 :c:func:`test` 设置断点,或者简单地使用 ``si``(或 ``stepi``)执行一条机器指令 (a breakpoint can be set for :c:func:`test`, or simply using ``si`` (or ``stepi``) to execute one machine instruction), 其中
      the side effect of going into the function. The GDB command ``finish``
      can be used to continue execution without intervention until the function
      returns.

      .. code-block:: text

      它将进入机器指令所代表的函数 (it has will go into the function representing the machine instruction)。

      .. code-block:: text

         (gdb) si
         0x00100667 in main () at <ZEPHYR_BASE>/tests/subsys/debug/gdbstub/src/main.c:28
         28              ret = test();
         Value returned is $2 = 30

   #. 再次检查 ``ret`` 的值,它应该包含来自 :c:func:`test` 的返回值 (Examine ``ret`` again which should have the return value from :c:func:`test`)。有时,赋值不会完成,直到再次执行 ``step`` 命令,就像本例中一样 (Sometimes, the assignment is not done until another ``step`` is issued, as in this case)。这是因为赋值代码是在从函数返回后完成的 (This is due to the assignment code is done after returning from function)。赋值代码由工具链生成为机器指令,在查看相应的C源文件时不可见 (The assignment code is generated by the toolchain as machine instructions which are not visible when viewing the corresponding C source file)。

      .. code-block:: text

         (gdb) p ret
         $3 = 1273788
         (gdb) step
         29              printk("ret=%d\n", ret);
         (gdb) p ret
         $4 = 30

   #. 如果此时执行 ``continue``,代码将无限期地继续执行,因为没有进一步的断点来停止执行 (If ``continue`` is issued here, code execution will continue indefinitely as there are no breakpoints to further stop execution)。通过 :kbd:`Ctrl-C` 在GDB中中断执行目前不起作用,因为Zephyr gdbstub还不支持此功能 (Breaking execution in GDB via :kbd:`Ctrl-C` does not currently work as the Zephyr gdbstub does not support this functionality yet)。切换到运行Zephyr镜像的QEMU的第一个控制台,并使用 :kbd:`Ctrl+a x` 手动停止它 (Switch to the first console with QEMU running the Zephyr image and stop it manually with :kbd:`Ctrl+a x`)。
      当Twister执行相同的测试时,它会自动停止QEMU实例 (When the same test is executed by Twister, it automatically takes care of stopping the QEMU instance)。
   #. If ``continue`` is issued here, code execution will continue indefinitely
      as there are no breakpoints to further stop execution. Breaking execution
      in GDB via :kbd:`Ctrl-C` does not currently work as the Zephyr gdbstub does
      not support this functionality yet. Switch to the first console with QEMU
      running the Zephyr image and stop it manually with :kbd:`Ctrl+a x`.
      When the same test is executed by Twister, it automatically takes care of
      stopping the QEMU instance.
