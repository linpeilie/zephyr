.. _symtab:

符号表 (Symbol Table (Symtab))
###############################

符号表模块启用后,将在Zephyr链接阶段生成完整的符号表,跟踪函数的名称和地址信息 (The Symtab module, when enabled, will generate full symbol table during the Zephyr linking stage that keep tracks of the information about the functions' name and address),对于具有大量函数的高级应用程序,这预计会消耗相当大的ROM空间 (for advanced application with a lot of functions, this is expected to consume a sizable amount of ROM)。

目前,这用于在支持的架构中进行栈跟踪期间查找函数名称 (Currently, this is being used to look up the function names during a stack trace in supported architectures)。


用法 (Usage)
*****

应用程序可以通过包含 :file:`symtab.h` 头文件并调用 :c:func:`symtab_get` 来访问符号表数据结构 (Application can gain access to the symbol table data structure by including the :file:`symtab.h` header file and call :c:func:`symtab_get`)。目前,我们只提供 :c:func:`symtab_find_symbol_name` 函数来查找地址的符号名称和偏移量 (For now, we only provide :c:func:`symtab_find_symbol_name` function to look-up the symbol name and offset of an address)。通过直接访问数据结构的成员可以实现更高级的功能 (More advanced functionalities and be achieved by directly accessing the members of the data structure)。

配置 (Configuration)
*************

使用以下选项配置此模块 (Configure this module using the following options)。

* :kconfig:option:`CONFIG_SYMTAB`: 启用符号表的生成 (enable the generation of the symbol table)。

API文档 (API documentation)
*****************

.. doxygengroup:: symtab_apis
