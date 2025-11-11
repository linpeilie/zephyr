.. _llext:

可链接可加载扩展 (Linkable Loadable Extensions (LLEXT))
########################################################

LLEXT 子系统提供了一个工具箱,用于在运行时使用可链接可加载代码扩展应用程序的功能。(The LLEXT subsystem provides a toolbox for extending the functionality of an application at runtime with linkable loadable code.)

扩展是 ELF 格式的预编译可执行文件,可以进行验证、加载并与主 Zephyr 二进制文件链接。扩展可以在一定程度上进行操作和自省,并且在不再需要时可以卸载。(Extensions are precompiled executables in ELF format that can be verified, loaded, and linked with the main Zephyr binary. Extensions can be manipulated and introspected to some degree, as well as unloaded when no longer needed.)

.. toctree::
   :maxdepth: 1

   config
   build
   load
   debug
   api

.. note::

   LLEXT 子系统需要架构特定的支持。它目前仅在 RISC-V、ARM、ARM64、ARC、x86 和 Xtensa 核心上可用。(The LLEXT subsystem requires architecture-specific support. It is currently available only on RISC-V, ARM, ARM64, ARC, x86, and Xtensa cores.)

