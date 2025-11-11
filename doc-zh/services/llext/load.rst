加载扩展 (Loading extensions)
##############################

一旦构建了扩展并且 ELF 文件可用,就可以使用 LLEXT API 将其加载到 Zephyr 应用程序中,该 API 提供了一种将扩展加载到内存中、访问其符号并调用其函数的方法。(Once an extension is built and the ELF file is available, it can be loaded into the Zephyr application using the LLEXT API, which provides a way to load the extension into memory, access its symbols and call its functions.)

加载扩展 (Loading an extension)
================================

可以使用 :c:struct:`llext_loader` 的任何实现来加载扩展,该实现具有一组函数指针,提供读取 ELF 数据所需的必要功能。加载器还提供 :c:func:`llext_load` 函数所需的一些最小上下文(内存)。已经提供了几个加载器:(An extension may be loaded using any implementation of a :c:struct:`llext_loader` which has a set of function pointers that provide the necessary functionality to read the ELF data. A loader also provides some minimal context (memory) needed by the :c:func:`llext_load` function. Several loaders are already provided:)

 * 可寻址内存中包含 ELF 的缓冲区上的实现可用作 :c:struct:`llext_buf_loader`。要使用这种加载器,使用 :c:macro:`LLEXT_TEMPORARY_BUF_LOADER`、:c:macro:`LLEXT_PERSISTENT_BUF_LOADER` 或 :c:macro:`LLEXT_WRITABLE_BUF_LOADER` 宏之一来告诉 LLEXT 适当的内存缓冲区类型很有帮助。(An implementation over a buffer containing an ELF in addressable memory in memory is available as :c:struct:`llext_buf_loader`. To use this kind of loader, it is helpful to use one of the :c:macro:`LLEXT_TEMPORARY_BUF_LOADER`, :c:macro:`LLEXT_PERSISTENT_BUF_LOADER`, or :c:macro:`LLEXT_WRITABLE_BUF_LOADER` macros to tell LLEXT the appropriate type of memory buffer.)

 * 从文件系统中的文件读取数据的实现可用作 :c:struct:`llext_fs_loader`。使用 :c:macro:`LLEXT_FS_LOADER` 宏创建加载器时必须提供文件路径。(An implementation that reads data from a file in the filesystem is available as the :c:struct:`llext_fs_loader`. The path to the file must be provided when creating the loader with the :c:macro:`LLEXT_FS_LOADER` macro.)

通过调用 :c:func:`llext_load` 函数来加载扩展,传入扩展名称和配置的加载器。一旦成功完成,扩展就会加载到内存中并准备使用。(The extensions are loaded with a call to the :c:func:`llext_load` function, passing in the extension name and the configured loader. Once that completes successfully, the extension is loaded into memory and is ready to be used.)

.. note::
   当启用 :ref:`用户模式 <usermode_api>` 时,扩展将不会包含在任何用户内存域中。要允许从用户模式访问,必须调用 :c:func:`llext_add_domain` 函数。(When :ref:`User Mode <usermode_api>` is enabled, the extension will not be included in any user memory domain. To allow access from user mode, the :c:func:`llext_add_domain` function must be called.)

初始化和清理扩展 (Initializing and cleaning up the extension)
==============================================================

扩展可能定义了许多初始化函数,这些函数必须在加载之后但在使用其中的任何函数之前调用;这在 C++ 等提供对象构造函数概念的语言中很典型。对于在卸载扩展之前必须调用的清理函数也是如此。(The extension may define a number of initialization functions that must be called after loading but before any function in it can be used; this is typical in languages such as C++ that provide the concept of object constructors. The same is true for cleanup functions that must be called before unloading the extension.)

LLEXT 支持使用 :c:func:`llext_bringup` 函数调用 ELF 文件的 ``.preinit_array`` 和 ``.init_array`` 节中列出的函数,并使用 :c:func:`llext_teardown` 函数调用 ``.fini_array`` 节中列出的函数。这些 API 与 :ref:`用户模式 <usermode_api>` 兼容,因此可以从内核或用户上下文调用。(LLEXT supports calling the functions listed in the ``.preinit_array`` and ``.init_array`` sections of the ELF file with the :c:func:`llext_bringup` function, and the functions listed in the ``.fini_array`` section with the :c:func:`llext_teardown` function. These APIs are compatible with :ref:`User Mode <usermode_api>`, and thus can be called from either kernel or user context.)

.. important::
   这些函数运行的代码完全由 ELF 文件的内容决定。如果其来源不受信任,这可能具有安全隐患。(The code run by these functions is fully determined by the contents of the ELF file. This may have security implications if its origin is untrusted.)

如果扩展需要专用线程,:c:func:`llext_bootstrap` 函数可用于最小化样板代码。此函数的签名与 :c:func:`k_thread_create` API 兼容,并将调用 :c:func:`llext_bringup`,然后在同一上下文中调用用户指定的函数,最后在返回之前调用 :c:func:`llext_teardown`。(If the extension requires a dedicated thread, the :c:func:`llext_bootstrap` function can be used to minimize boilerplate code. This function has a signature that is compatible with the :c:func:`k_thread_create` API, and will call :c:func:`llext_bringup`, then a user-specified function in the same context, and finally :c:func:`llext_teardown` before returning.)

访问代码和数据 (Accessing code and data)
=========================================

要与新加载的扩展进行交互,主机应用程序必须使用 :c:func:`llext_find_sym` 函数来获取导出符号的地址。然后可以将返回的 ``void *`` 转换为适当的类型并使用。(To interact with the newly loaded extension, the host application must use the :c:func:`llext_find_sym` function to get the address of the exported symbol. The returned ``void *`` can then be cast to the appropriate type and used.)

:c:func:`llext_call_fn` 中提供了一个用于调用无参数函数的包装器。(A wrapper for calling a function with no arguments is provided in :c:func:`llext_call_fn`.)

需要直接访问新加载扩展的区域的高级用户可能需要参考 :c:func:`llext_get_section_info` 和其他 LLEXT 检查 API。(Advanced users that need direct access to areas of the newly loaded extension may want to refer to :c:func:`llext_get_section_info` and other LLEXT inspection APIs.)

使用后清理 (Cleaning up after use)
===================================

一旦不再需要扩展,必须调用 :c:func:`llext_unload` 函数来释放扩展使用的内存。此调用完成后,所有指向扩展中符号的指针都将失效。(The :c:func:`llext_unload` function must be called to free the memory used by the extension once it is no longer required. After this call completes, all pointers to symbols in the extension that were obtained will be invalid.)

故障排除 (Troubleshooting)
###########################

此功能正在积极开发中,因此可能会出现一些问题。由于链接确实会修改二进制代码,因此在出现错误的情况下,结果难以预测。一些常见问题可能是:(This feature is being actively developed and as such it is possible that some issues may arise. Since linking does modify the binary code, in case of errors the results are difficult to predict. Some common issues may be:)

* :c:func:`llext_find_sym` 的结果指向无效地址;(Results from :c:func:`llext_find_sym` point to an invalid address;)

* 扩展中定义的常量和变量没有预期的值;(Constants and variables defined in the extension do not have the expected values;)

* 调用扩展中定义的函数会导致硬故障,或者从中返回后主应用程序中的内存损坏。(Calling a function defined in an extension results in a hard fault, or memory in the main application is corrupted after returning from it.)

如果发生任何这些情况,以下提示可能有助于理解问题:(If any of this happens, the following tips may help understand the issue:)

* 确保 :kconfig:option:`CONFIG_LLEXT_LOG_LEVEL` 设置为 ``DEBUG``,然后获取 :c:func:`llext_load` 调用的日志。(Make sure :kconfig:option:`CONFIG_LLEXT_LOG_LEVEL` is set to ``DEBUG``, then obtain a log of the :c:func:`llext_load` invocation.)

* 如果可能,禁用内存保护(MMU/MPU)并查看这是否导致不同的行为。(If possible, disable memory protection (MMU/MPU) and see if this results in different behavior.)

* 尝试将扩展简化为重现问题的最小可能代码。(Try to simplify the extension to the minimum possible code that reproduces the issue.)

* 使用调试器检查内存和寄存器以尝试了解正在发生的事情。有关更多详细信息,请参阅 :ref:`调试扩展 <llext_debug>`。(Use a debugger to inspect the memory and registers to try to understand what is happening. See :ref:`Debugging extensions <llext_debug>` for more details.)

如果问题仍然存在,请在 GitHub 存储库中打开问题,包括上述所有信息。(If the issue persists, please open an issue in the GitHub repository, including all the above information.)
