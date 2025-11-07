.. _semihost_guide:

半主机指南 (Semihosting Guide)
###############################

概述 (Overview)
****************

半主机 (Semihosting) 是一种机制,使在 ARM、RISC-V 和 Xtensa 目标上运行的代码
能够与运行调试器或仿真器的主机计算机进行通信并使用其输入/输出功能。

有关可用功能的更完整文档可在 `ARM Github 文档`_ 中找到。

RISC-V 功能借用了 ARM 定义,如 `RISC-V Github 文档`_ 中所述。

Xtensa 上的半主机实现支持 GDB File-I/O 扩展,该扩展在
`GDB File-I/O 远程协议`_ 中有说明。

文件操作 (File Operations)
***************************

半主机使应用程序能够打开、读取和修改主机计算机上的文件。当尝试验证代码在大于
模拟平台 ROM 容量的数据集上的行为时,这可能很有用。文件路径可以是绝对路径,
也可以是相对于运行进程目录的路径。

.. code-block:: c

   const char *path = "./data.bin";
   long file_len, bytes_read, fd;
   uint8_t buffer[16];

   /* 打开数据文件进行读取 */
   fd = semihost_open(path, SEMIHOST_OPEN_RB);
   if (fd < 0) {
      return -ENOENT;
   }
   /* 从文件读取所有数据 */
   file_len = semihost_flen(fd);
   while(file_len > 0) {
      bytes_read = semihost_read(fd, buffer, MIN(file_len, sizeof(buffer)));
      if (bytes_read < 0) {
         break;
      }
      /* 处理读取的数据 */
      do_data_processing(buffer, bytes_read);
      /* 更新剩余长度 */
      file_len -= bytes_read;
   }
   /* 关闭文件 */
   semihost_close(fd);

其他功能 (Additional Functionality)
************************************

通过使用 :c:func:`semihost_exec` 和 :c:enum:`semihost_instr` 中定义的指令之一
直接运行半主机指令,可以使用其他功能。有关所需参数和返回代码的完整文档,
请参阅 `ARM Github 文档`_。

API 参考 (API Reference)
*************************

.. doxygengroup:: semihost

.. _ARM Github 文档: https://github.com/ARM-software/abi-aa/blob/main/semihosting/semihosting.rst
.. _RISC-V Github 文档: https://github.com/riscv-non-isa/riscv-semihosting/blob/main/riscv-semihosting.adoc
.. _GDB File-I/O 远程协议: https://sourceware.org/gdb/current/onlinedocs/gdb.html/File_002dI_002fO-Remote-Protocol-Extension.html
