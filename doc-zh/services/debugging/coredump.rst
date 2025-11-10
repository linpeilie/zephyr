.. _coredump:

核心转储 (Core Dump)
####################

核心转储模块支持转储CPU寄存器和内存内容以供离线调试 (The core dump module enables dumping the CPU registers and memory content for offline debugging)。当遇到致命错误时会调用此模块,并根据启用的后端打印或存储数据 (This module is called when a fatal error is encountered and prints or stores data according to which backends are enabled)。

配置 (Configuration)
********************

使用以下选项配置此模块 (Configure this module using the following options)。

* ``DEBUG_COREDUMP``: 启用该模块 (enable the module)。

以下是用于核心转储的输出后端启用选项 (Here are the options to enable output backends for core dump):

* ``DEBUG_COREDUMP_BACKEND_LOGGING``: 使用日志模块进行核心转储输出 (use log module for core dump output)。
* ``DEBUG_COREDUMP_BACKEND_FLASH_PARTITION``: 使用flash分区进行核心转储输出 (use flash partition for core dump output)。
* ``DEBUG_COREDUMP_BACKEND_NULL``: 如果其他后端无法启用,则回退的核心转储后端 (fallback core dump backend if other backends cannot be enabled)。所有输出发送到null (All output is sent to null)。

以下是有关内存转储的选项 (Here are the choices regarding memory dump):

* ``DEBUG_COREDUMP_MEMORY_DUMP_MIN``: 仅转储异常线程的栈、其线程结构以及一些其他最基本的数据以支持在调试器中遍历栈 (only dumps the stack of the exception thread, its thread struct, and some other bare minimal data to support walking the stack in the debugger)。仅在需要绝对最小数据转储时使用此选项 (Use this only if absolute minimum of data dump is desired)。

* ``DEBUG_COREDUMP_MEMORY_DUMP_THREADS``: 转储所有线程的线程结构和栈以及调试线程所需的所有数据 (Dumps the thread struct and stack of all threads and all data required to debug threads)。

* ``DEBUG_COREDUMP_MEMORY_DUMP_LINKER_RAM``: 转储_image_ram_start[]和_image_ram_end[]之间的内存区域 (Dumps the memory region between _image_ram_start[] and _image_ram_end[])。这至少包括data、noinit和BSS段 (This includes at least data, noinit, and BSS sections)。这是默认选项 (This is the default)。

即使选择了"DEBUG_COREDUMP_MEMORY_DUMP_MIN"配置,也可以通过一个或多个 :ref:`核心转储设备 <coredump_device_api>` 在转储中包含其他内存 (Additional memory can be included in a dump (even with the "DEBUG_COREDUMP_MEMORY_DUMP_MIN" config selected) through one or more :ref:`coredump devices <coredump_device_api>`)。

用法 (Usage)
*************

当启用核心转储模块时,在致命错误期间,CPU寄存器和内存内容会根据启用的后端进行打印或存储 (When the core dump module is enabled, during a fatal error, CPU registers and memory content are printed or stored according to which backends are enabled)。此核心转储数据可以作为远程目标馈送到自定义GDB服务器中供GDB(和其他GDB兼容调试器)使用 (This core dump data can be fed into a custom-made GDB server as a remote target for GDB (and other GDB compatible debuggers))。可以在调试器中检查CPU寄存器、内存内容和栈 (CPU registers, memory content and stack can be examined in the debugger)。

这通常涉及以下步骤 (This usually involves the following steps):

1. 根据启用的后端从设备获取核心转储日志 (Get the core dump log from the device depending on enabled backends)。
   例如,如果使用日志模块后端,则从日志模块后端获取日志输出 (For example, if the log module backend is used, get the log output from the log module backend)。

2. 将核心转储日志转换为可由GDB服务器解析的二进制格式 (Convert the core dump log into a binary format that can be parsed by the GDB server)。例如,
   :zephyr_file:`scripts/coredump/coredump_serial_log_parser.py` 可用于将串行控制台日志转换为二进制文件 (For example, :zephyr_file:`scripts/coredump/coredump_serial_log_parser.py` can be used to convert the serial console log into a binary file)。

3. 使用核心转储二进制日志文件和Zephyr ELF文件作为参数,使用脚本 :zephyr_file:`scripts/coredump/coredump_gdbserver.py` 启动自定义GDB服务器 (Start the custom GDB server using the script :zephyr_file:`scripts/coredump/coredump_gdbserver.py` with the core dump binary log file, and the Zephyr ELF file as parameters)。GDB服务器也可以从GDB内部启动,请参见下文 (The GDB server can also be started from within GDB, see below)。

4. 启动与目标架构对应的调试器 (Start the debugger corresponding to the target architecture)。

.. note::
   使用 ``ZEPHYR_TOOLCHAIN_VARIANT=zephyr`` 的Intel ADSP CAVS 15-25平台开发人员应使用SDK的 ``xtensa-intel_apl_adsp`` 工具链中的调试器 (Developers for Intel ADSP CAVS 15-25 platforms using ``ZEPHYR_TOOLCHAIN_VARIANT=zephyr`` should use the debugger in the ``xtensa-intel_apl_adsp`` toolchain of the SDK)。

5. 当启用 ``DEBUG_COREDUMP_BACKEND_FLASH_PARTITION`` 时,核心转储数据存储在flash分区中 (When ``DEBUG_COREDUMP_BACKEND_FLASH_PARTITION`` is enabled the core dump data is stored in the flash partition)。flash分区必须在设备树中定义 (The flash partition must be defined in the device tree):

	.. code-block:: devicetree

		&flash0 {
			partitions {
				coredump_partition: partition@255000 {
					label = "coredump-partition";
					reg = <0x255000 DT_SIZE_K(4)>;
				};
		};
。

Usage
*****

When the core dump module is enabled, during a fatal error, CPU registers
and memory content are printed or stored according to which backends
are enabled. This core dump data can be fed into a custom-made GDB server as
a remote target for GDB (and other GDB compatible debuggers). CPU registers,
memory content and stack can be examined in the debugger.

This usually involves the following steps:

1. Get the core dump log from the device depending on enabled backends.
   For example, if the log module backend is used, get the log output
   from the log module backend.

2. Convert the core dump log into a binary format that can be parsed by
   the GDB server. For example,
   :zephyr_file:`scripts/coredump/coredump_serial_log_parser.py` can be used
   to convert the serial console log into a binary file.

3. Start the custom GDB server using the script
   :zephyr_file:`scripts/coredump/coredump_gdbserver.py` with the core dump
   binary log file, and the Zephyr ELF file as parameters. The GDB server
   can also be started from within GDB, see below.

4. Start the debugger corresponding to the target architecture.

.. note::
   Developers for Intel ADSP CAVS 15-25 platforms using
   ``ZEPHYR_TOOLCHAIN_VARIANT=zephyr`` should use the debugger in the
   ``xtensa-intel_apl_adsp`` toolchain of the SDK.

5. When ``DEBUG_COREDUMP_BACKEND_FLASH_PARTITION`` is enabled the core dump
   data is stored in the flash partition. The flash partition must be defined
   in the device tree:

	.. code-block:: devicetree

		&flash0 {
			partitions {
				coredump_partition: partition@255000 {
					label = "coredump-partition";
					reg = <0x255000 DT_SIZE_K(4)>;
				};
		};

示例 (Example)
-------

此示例使用绑定到串行控制台的日志模块后端 (This example uses the log module backend tied to serial console)。
这是在 :zephyr:board:`qemu_x86` 上完成的,其中解引用了一个空指针 (This was done on :zephyr:board:`qemu_x86` where a null pointer was dereferenced)。

这是来自串行控制台的核心转储日志,存储在 :file:`coredump.log` 中 (This is the core dump log from the serial console, and is stored in :file:`coredump.log`):

::

   Booting from ROM..*** Booting Zephyr OS build zephyr-v2.3.0-1840-g7bba91944a63  ***
   Hello World! qemu_x86
   E: Page fault at address 0x0 (error code 0x2)
   E: Linear address not present in page tables
   E:   PDE: 0x0000000000115827 Writable, User, Execute Enabled
   E:   PTE: Non-present
   E: EAX: 0x00000000, EBX: 0x00000000, ECX: 0x00119d74, EDX: 0x000003f8
   E: ESI: 0x00000000, EDI: 0x00101aa7, EBP: 0x00119d10, ESP: 0x00119d00
   E: EFLAGS: 0x00000206 CS: 0x0008 CR3: 0x00119000
   E: call trace:
   E: EIP: 0x00100459
   E:      0x00100477 (0x0)
   E:      0x00100492 (0x0)
   E:      0x001004c8 (0x0)
   E:      0x00105465 (0x105465)
   E:      0x00101abe (0x0)
   E: >>> ZEPHYR FATAL ERROR 0: CPU exception on CPU 0
   E: Current thread: 0x00119080 (unknown)
   E: #CD:BEGIN#
   E: #CD:5a4501000100050000000000
   E: #CD:4101003800
   E: #CD:0e0000000200000000000000749d1100f803000000000000009d1100109d1100
   E: #CD:00000000a71a100059041000060200000800000000901100
   E: #CD:4d010080901100e0901100
   E: #CD:0100000000000000000000000180000000000000000000000000000000000000
   E: #CD:00000000000000000000000000000000e364100000000000000000004c9c1100
   E: #CD:000000000000000000000000b49911000004000000000000fc03000000000000
   E: #CD:4d0100b4991100b49d1100
   E: #CD:f8030000020000000200000002000000f8030000fd03000a02000000dc9e1100
   E: #CD:149a1160fd03000002000000dc9e1100249a110087201000049f11000a000000
   E: #CD:349a11000a4f1000049f11000a9e1100449a11000a8b10000200000002000000
   E: #CD:449a1100388b1000049f11000a000000549a1100ad201000049f11000a000000
   E: #CD:749a11000a201000049f11000a000000649a11000a201000049f11000a000000
   E: #CD:749a1100e8201000049f11000a000000949a1100890b10000a0000000a000000
   E: #CD:a49a1100890b10000a0000000a000000f8030000189b11000200000002000000
   E: #CD:f49a1100289b11000a000000189b1100049b11009b0710000a000000289b1100
   E: #CD:f49a110087201000049f110045000000f49a1100509011000a00000020901100
   E: #CD:f49a110060901100049f1100ffffffff0000000000000000049f1100ffffffff
   E: #CD:0000000000000000630b1000189b1100349b1100af0b1000630b1000289b1100
   E: #CD:55891000789b11000000000020901100549b1100480000004a891000609b1100
   E: #CD:649b1100d00b10004a891000709b110000000000609b11000a00000000000000
   E: #CD:849b1100709b11004a89100000000000949b1100794a10000000000058901100
   E: #CD:20901100c34a10000a00001734020000d001000000000000d49b110038000000
   E: #CD:c49b110078481000b49911000004000000000000000000000c9c11000c9c1100
   E: #CD:149c110000000000d49b110038000000f49b1100da481000b499110000040000
   E: #CD:0e0000000200000000000000744d0100b4991100b49d1100009d1100109d1100
   E: #CD:149c110099471000b4991100000400000800000000901100ad861000409c1100
   E: #CD:349c1100e94710008090110000000000349c1100b64710008086100045000000
   E: #CD:849c11002d53100000000000d09c11008090110020861000f5ffffff8c9c1100
   E: #CD:000000000000000000000000a71a1000a49c1100020200008090110000000000
   E: #CD:a49c1100020200000800000000000000a49c11001937100000000000d09c1100
   E: #CD:0c9d0000bc9c0000b49d1100b4991100c49c1100ae37100000000000d09c1100
   E: #CD:0800000000000000c888100000000000109d11005d031000d09c1100009d1100
   E: #CD:109d11000000000000000000a71a1000f803000000000000749d110002000000
   E: #CD:5904100008000000060200000e0000000202000002020000000000002c9d1100
   E: #CD:7704100000000000d00b1000c9881000549d110000000000489d110092041000
   E: #CD:00000000689d1100549d11000000000000000000689d1100c804100000000000
   E: #CD:c0881000000000007c9d110000000000749d11007c9d11006554100065541000
   E: #CD:00000000000000009c9d1100be1a100000000000000000000000000038041000
   E: #CD:08000000020200000000000000000000f4531000000000000000000000000000
   E: #CD:END#
   E: Halting system


1. 运行核心转储串行日志转换器 (Run the core dump serial log converter):

   .. code-block:: console

      ./scripts/coredump/coredump_serial_log_parser.py coredump.log coredump.bin

2. 启动自定义GDB服务器 (Start the custom GDB server):

   .. code-block:: console

      ./scripts/coredump/coredump_gdbserver.py build/zephyr/zephyr.elf coredump.bin

3. 启动GDB (Start GDB):

   .. code-block:: console

      <path to SDK>/x86_64-zephyr-elf/bin/x86_64-zephyr-elf-gdb build/zephyr/zephyr.elf

4. 在GDB内部,通过端口1234连接到GDB服务器 (Inside GDB, connect to the GDB server via port 1234):

   .. code-block:: console

      (gdb) target remote localhost:1234

5. 检查CPU寄存器 (Examine the CPU registers):

   .. code-block:: console

      (gdb) info registers

   GDB的输出 (Output from GDB):

   ::

      eax            0x0                 0
      ecx            0x119d74            1154420
      edx            0x3f8               1016
      ebx            0x0                 0
      esp            0x119d00            0x119d00 <z_main_stack+844>
      ebp            0x119d10            0x119d10 <z_main_stack+860>
      esi            0x0                 0
      edi            0x101aa7            1055399
      eip            0x100459            0x100459 <func_3+16>
      eflags         0x206               [ PF IF ]
      cs             0x8                 8
      ss             <unavailable>
      ds             <unavailable>
      es             <unavailable>
      fs             <unavailable>
      gs             <unavailable>

6. 检查回溯 (Examine the backtrace):

   .. code-block:: console

      (gdb) bt


   GDB的输出 (Output from GDB):

   ::

      #0  0x00100459 in func_3 (addr=0x0) at zephyr/rtos/zephyr/samples/hello_world/src/main.c:14
      #1  0x00100477 in func_2 (addr=0x0) at zephyr/rtos/zephyr/samples/hello_world/src/main.c:21
      #2  0x00100492 in func_1 (addr=0x0) at zephyr/rtos/zephyr/samples/hello_world/src/main.c:28
      #3  0x001004c8 in main () at zephyr/rtos/zephyr/samples/hello_world/src/main.c:42

从GDB内部启动GDB服务器 (Starting the GDB server from within GDB)
---------------------------------------

您可以使用 ``target remote |`` 从GDB内部启动自定义GDB服务器,而不是在单独的shell中启动 (You can use ``target remote |`` to start the custom GDB server from inside GDB, instead of in a separate shell)。

1. 启动GDB (Start GDB):

   .. code-block:: console

      <path to SDK>/x86_64-zephyr-elf/bin/x86_64-zephyr-elf-gdb build/zephyr/zephyr.elf

2. 在GDB内部,使用 ``--pipe`` 选项启动GDB服务器 (Inside GDB, start the GDB server using the ``--pipe`` option):

   .. code-block:: console

      (gdb) target remote | ./scripts/coredump/coredump_gdbserver.py --pipe build/zephyr/zephyr.elf coredump.bin


文件格式 (File Format)
***********************

核心转储二进制文件由一个文件头、一个架构特定块、零个或一个线程元数据块以及多个内存块组成 (The core dump binary file consists of one file header, one architecture-specific block, zero or one threads metadata block(s), and multiple memory blocks)。以下头中的所有数字均为小端格式 (All numbers in the headers below are little endian)。

文件头 (File Header)
-----------

文件头由以下字段组成 (The file header consists of the following fields):

.. list-table:: 核心转储二进制文件头 (Core dump binary file header)
   :widths: 2 1 7
   :header-rows: 1

   * - 字段 (Field)
     - 数据类型 (Data Type)
     - 描述 (Description)
   * - ID
     - ``char[2]``
     - ``Z``, ``E`` 作为文件的标识符 (``Z``, ``E`` as identifier of file)。
   * - 头版本 (Header version)
     - ``uint16_t``
     - 标识头的版本 (Identify the version of the header)。每当修改头结构时都需要递增此值 (This needs to be incremented whenever the header struct is modified)。这允许解析器拒绝较旧的头版本,因此不会错误地解析头 (This allows parser to reject older header versions so it will not incorrectly parse the header)。
   * - 目标代码 (Target code)
     - ``uint16_t``
     - 指示目标(例如架构或SoC),以便解析器可以实例化正确的寄存器块解析器 (Indicate which target (e.g. architecture or SoC) so the parser can instantiate the correct register block parser)。
   * - 指针大小 (Pointer size)
     - 'uint8_t'
     - ``uintptr_t`` 的大小(以2的幂表示)。(例如32位为5,64位为6) (Size of ``uintptr_t`` in power of 2. (e.g. 5 for 32-bit, 6 for 64-bit))。这是解析内存块地址时适应32位和64位目标所需的 (This is needed to accommodate 32-bit and 64-bit target in parsing the memory block addresses)。
   * - 标志 (Flags)
     - ``uint8_t``
     -
   * - 致命错误原因 (Fatal error reason)
     - ``unsigned int``
     - 致命错误的原因,与 :zephyr_file:`include/zephyr/fatal.h` 中定义的 ``enum k_fatal_error_reason`` 中的相同 (Reason for the fatal error, as the same in ``enum k_fatal_error_reason`` defined in :zephyr_file:`include/zephyr/fatal.h`)

架构特定块 (Architecture-specific Block)
---------------------------

架构特定块包含特定于目标架构的数据字节流(例如CPU寄存器) (The architecture-specific block contains the byte stream of data specific to the target architecture (e.g. CPU registers))

.. list-table:: 架构特定块 (Architecture-specific Block)
   :widths: 2 1 7
   :header-rows: 1

   * - 字段 (Field)
     - 数据类型 (Data Type)
     - 描述 (Description)
   * - ID
     - ``char``
     - ``A`` 表示这是一个架构特定块 (``A`` to indicate this is a architecture-specific block)。
   * - 头版本 (Header version)
     - ``uint16_t``
     - 标识此块的版本 (Identify the version of this block)。由目标架构特定块解析器解释 (To be interpreted by the target architecture specific block parser)。
   * - 字节数 (Number of bytes)
     - ``uint16_t``
     - 头之后的字节数,其中包含目标数据的字节流 (Number of bytes following the header which contains the byte stream for target data)。字节流的格式是目标特定的,仅由目标解析器解析 (The format of the byte stream is specific to the target and is only being parsed by the target parser)。
   * - 寄存器字节流 (Register byte stream)
     - ``uint8_t[]``
     - 包含目标架构特定数据 (Contains target architecture specific data)。

线程元数据块 (Threads Metadata Block)
---------------------------

线程元数据块包含调试线程所需的数据字节流 (The threads metadata block contains the byte stream of data necessary for debugging threads)。

.. list-table:: 线程元数据块 (Threads Metadata Block)
   :widths: 2 1 7
   :header-rows: 1

   * - 字段 (Field)
     - 数据类型 (Data Type)
     - 描述 (Description)
   * - ID
     - ``char``
     - ``T`` 表示这是一个线程元数据块 (``T`` to indicate this is a threads metadata block)。
   * - 头版本 (Header version)
     - ``uint16_t``
     - 标识头的版本 (Identify the version of the header)。每当修改头结构时都需要递增此值 (This needs to be incremented whenever the header struct is modified)。这允许解析器拒绝较旧的头版本,因此不会错误地解析头 (This allows parser to reject older header versions so it will not incorrectly parse the header)。
   * - 字节数 (Number of bytes)
     - ``uint16_t``
     - 头之后的字节数,其中包含目标数据的字节流 (Number of bytes following the header which contains the byte stream for target data)。
   * - 字节流 (Byte stream)
     - ``uint8_t[]``
     - 包含调试线程所需的数据 (Contains data necessary for debugging threads)。

内存块 (Memory Block)
------------

内存块包含起始和结束地址以及内存区域内的数据 (The memory block contains the start and end addresses and the data within the memory region)。

.. list-table:: 内存块 (Memory Block)
   :widths: 2 1 7
   :header-rows: 1

   * - 字段 (Field)
     - 数据类型 (Data Type)
     - 描述 (Description)
   * - ID
     - ``char``
     - ``M`` 表示这是一个内存块 (``M`` to indicate this is a memory block)。
   * - 头版本 (Header version)
     - ``uint16_t``
     - 标识头的版本 (Identify the version of the header)。每当修改头结构时都需要递增此值 (This needs to be incremented whenever the header struct is modified)。这允许解析器拒绝较旧的头版本,因此不会错误地解析头 (This allows parser to reject older header versions so it will not incorrectly parse the header)。
   * - 起始地址 (Start address)
     - ``uintptr_t``
     - 内存区域的起始地址 (The start address of the memory region)。
   * - 结束地址 (End address)
     - ``uintptr_t``
     - 内存区域的结束地址 (The end address of the memory region)。
   * - 内存字节流 (Memory byte stream)
     - ``uint8_t[]``
     - 包含起始和结束地址之间的内存内容 (Contains the memory content between the start and end addresses)。

添加新目标 (Adding New Target)
*****************

架构特定块是目标特定的,需要为新目标提供新的转储例程和解析器 (The architecture-specific block is target specific and requires new dumping routine and parser for new targets)。要添加新目标,需要完成以下操作 (To add a new target, the following needs to be done):

#. 在 :zephyr_file:`include/zephyr/debug/coredump.h` 中的 ``enum coredump_tgt_code`` 中添加新的目标代码 (Add a new target code to the ``enum coredump_tgt_code`` in :zephyr_file:`include/zephyr/debug/coredump.h`)。
#. 实现 :c:func:`arch_coredump_tgt_code_get` 简单地返回新引入的目标代码 (Implement :c:func:`arch_coredump_tgt_code_get` simply to return the newly introduced target code)。
#. 实现 :c:func:`arch_coredump_info_dump` 以构造目标架构块并调用 :c:func:`coredump_buffer_output` 将块输出到核心转储后端 (Implement :c:func:`arch_coredump_info_dump` to construct a target architecture block and call :c:func:`coredump_buffer_output` to output the block to core dump backend)。
#. 在 ``scripts/coredump/gdbstubs/`` 下向核心转储GDB存根脚本添加解析器 (Add a parser to the core dump GDB stub scripts under ``scripts/coredump/gdbstubs/``)

   #. 扩展 ``gdbstubs.gdbstub.GdbStub`` 类 (Extends the ``gdbstubs.gdbstub.GdbStub`` class)。
   #. 在 ``__init__`` 期间,将与异常原因对应的GDB信号存储在 ``self.gdb_signal`` 中 (During ``__init__``, store the GDB signal corresponding to the exception reason in ``self.gdb_signal``)。
   #. 从 ``self.logfile.get_arch_data()`` 解析架构特定块 (Parse the architecture-specific block from ``self.logfile.get_arch_data()``)。这需要匹配步骤3中实现的格式(在 :c:func:`arch_coredump_info_dump` 内部) (This needs to match the format as implemented in step 3 (inside :c:func:`arch_coredump_info_dump`))。
   #. 实现抽象方法 ``handle_register_group_read_packet``,它返回GDB期望的寄存器组 (Implement the abstract method ``handle_register_group_read_packet`` where it returns the register group as GDB expected)。参考GDB的代码和文档了解它对新目标的期望 (Refer to GDB's code and documentation on what it is expecting for the new target)。
   #. 可选地实现 ``handle_register_single_read_packet`` 以处理 ``g`` 数据包中未涵盖的寄存器 (Optionally implement ``handle_register_single_read_packet`` for registers not covered in the ``g`` packet)。

#. 扩展 :zephyr_file:`scripts/coredump/gdbstubs/__init__.py` 中的 ``get_gdbstub()`` 以返回新实现的GDB存根 (Extend ``get_gdbstub()`` in :zephyr_file:`scripts/coredump/gdbstubs/__init__.py` to return the newly implemented GDB stub)。

API文档 (API documentation)
*****************

.. doxygengroup:: coredump_apis

.. doxygengroup:: arch-coredump
