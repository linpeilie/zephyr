.. _toolchain_designware_arc_mwdt:

DesignWare ARC MetaWare 开发工具包 (MWDT)
##########################################

#. 您需要在主机上安装 `ARC MWDT <https://www.synopsys.com/dw/ipdir.php?ds=sw_metaware>`_。

#. 您需要在主机上安装 :ref:`Zephyr SDK <toolchain_zephyr_sdk>`。

   .. note::
      Zephyr SDK 用作设备树编译器 (DTC)、QEMU 等工具的来源...
      即使 ARC MWDT 工具链用于 Zephyr RTOS 构建,GNU 预处理器和 GNU objcopy 仍可能用于某些步骤,如设备树预处理和 ``.bin`` 文件生成。我们使用 Zephyr SDK 作为这些 ARC GNU 工具的来源。
      要设置 ARC GNU 工具链,请使用 SDK Bundle(完整或最小),而不是手动安装单独的 tarball。它会在系统中安装和注册工具链和主机工具,从而允许您在构建 Zephyr 时避免与工具链相关的问题。

#. :ref:`设置这些环境变量 <env_vars>`:

   - 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为 ``arcmwdt``。
   - 将 :envvar:`ARCMWDT_TOOLCHAIN_PATH` 设置为工具链安装目录。MWDT 安装提供 :envvar:`METAWARE_ROOT`,因此只需将 :envvar:`ARCMWDT_TOOLCHAIN_PATH` 设置为 ``$METAWARE_ROOT/../`` (Linux) 或 ``%METAWARE_ROOT%\..\`` (Windows)。

   .. tip::
      如果您的机器上只安装了一个 ARC MWDT 工具链版本,您可以跳过设置 :envvar:`ARCMWDT_TOOLCHAIN_PATH` - 它会自动检测。

#. 要检查您是否在当前环境中正确设置了这些变量,请遵循这些示例 shell 会话(您系统上的 :envvar:`ARCMWDT_TOOLCHAIN_PATH` 值可能不同):

   .. code-block:: console

      # Linux:
      $ echo $ZEPHYR_TOOLCHAIN_VARIANT
      arcmwdt
      $ echo $ARCMWDT_TOOLCHAIN_PATH
      /home/you/ARC/MWDT_2023.03/

      # Windows:
      > echo %ZEPHYR_TOOLCHAIN_VARIANT%
      arcmwdt
      > echo %ARCMWDT_TOOLCHAIN_PATH%
      C:\ARC\MWDT_2023.03\
