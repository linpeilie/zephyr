.. _host_toolchains:

主机工具链
##########

在某些特定配置中,例如在 Linux 主机上为非 MCU x86 目标构建时,您可能能够重用操作系统提供的本地开发工具。

要使用主机 gcc,请将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` :ref:`环境变量 <env_vars>` 设置为 ``host``。要使用 clang,请将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为 ``llvm``。
