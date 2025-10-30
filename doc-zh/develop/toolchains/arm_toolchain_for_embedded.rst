.. _toolchain_atfe:

Arm Toolchain for Embedded (ATfE)
#################################


Arm Toolchain for Embedded (ATfE) 是 Arm 提供的 C 和 C++ 工具链,基于免费且开源的 LLVM 编译器基础设施和适用于裸机目标的 Picolib C 库。

ATfE 经过精细调优,特别关注较新的 ARM 产品(2024 年后)的性能,例如 64 位 Arm 架构 (AArch64) 或 M-Profile 向量扩展(MVE,一个 32 位 Armv8.1-M 扩展)。

安装
****

#. 为您的操作系统下载并安装 `Arm toolchain for embedded`_ 构建版本,并将其提取到您的文件系统中。

#. :ref:`设置这些环境变量 <env_vars>`:

   - 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为 ``llvm``。
   - 将 :envvar:`LLVM_TOOLCHAIN_PATH` 设置为工具链安装目录。

#. 要检查您是否在当前环境中正确设置了这些变量,请遵循这些示例 shell 会话(您系统上的 :envvar:`LLVM_TOOLCHAIN_PATH` 值可能不同):

   .. tabs::

      .. group-tab:: Ubuntu

         .. code-block:: bash

            echo $ZEPHYR_TOOLCHAIN_VARIANT
            llvm
            echo $LLVM_TOOLCHAIN_PATH
            /home/you/Downloads/ATfE

      .. group-tab:: macOS

         .. code-block:: bash

            echo $ZEPHYR_TOOLCHAIN_VARIANT
            llvm
            echo $LLVM_TOOLCHAIN_PATH
            /home/you/Downloads/ATfE

      .. group-tab:: Windows

         .. code-block:: powershell

            > echo %ZEPHYR_TOOLCHAIN_VARIANT%
            llvm
            > echo %LLVM_TOOLCHAIN_PATH%
            C:\ATfE

   .. _toolchain_env_var:

#. 您还可以在为 Zephyr 应用程序生成构建系统时将 ``ZEPHYR_TOOLCHAIN_VARIANT`` 和 ``LLVM_TOOLCHAIN_PATH`` 设置为 CMake 变量,如下所示:

      .. code-block:: console

      west build ... -- -DZEPHYR_TOOLCHAIN_VARIANT=llvm -DLLVM_TOOLCHAIN_PATH=...

工具链设置
**********

由于 LLVM 与 GNU 工具广泛兼容,当使用任何 LLVM 工具链构建时,您必须指定一些设置以让编译器知道要使用哪些工具:

链接器:
   设置 :envvar:`CONFIG_LLVM_USE_LLD=y` 以使用 LLVM 链接器。
   设置 :envvar:`CONFIG_LLVM_USE_LD=y` 以使用 GNU LD 链接器。

运行时库:
   设置 :envvar:`CONFIG_COMPILER_RT_RTLIB=y` 以使用 LLVM 运行时库。
   设置 :envvar:`CONFIG_LIBGCC_RTLIB=y` 以使用 LibGCC 运行时库。

.. code-block:: console

   west build ... -- -DZEPHYR_TOOLCHAIN_VARIANT=llvm -DLLVM_TOOLCHAIN_PATH=... -DCONFIG_LLVM_USE_LLD=y -DCONFIG_COMPILER_RT_RTLIB=y

.. _Arm Toolchain for Embedded: https://developer.arm.com/Tools%20and%20Software/Arm%20Toolchain%20for%20Embedded
