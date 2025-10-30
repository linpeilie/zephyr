.. _toolchain_gnuarmemb:

GNU Arm Embedded
################

#. 为您的操作系统下载并安装 `GNU Arm Embedded`_ 构建版本,并将其提取到您的文件系统中。

   .. note::

      在 Windows 上,我们假设本指南中您安装到目录 :file:`C:\\gnu_arm_embedded`。您也可以选择 ARM GCC 安装程序使用的默认安装路径,在这种情况下,您需要在以下指南中相应地调整路径。

   .. warning::

      在 macOS Catalina 或更高版本上,您可能需要 :ref:`更改安全策略 <mac-gatekeeper>` 才能从终端运行工具链。

#. :ref:`设置这些环境变量 <env_vars>`:

   - 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为 ``gnuarmemb``。
   - 将 :envvar:`GNUARMEMB_TOOLCHAIN_PATH` 设置为工具链安装目录。

#. 要检查您是否在当前环境中正确设置了这些变量,请遵循这些示例 shell 会话(您系统上的 :envvar:`GNUARMEMB_TOOLCHAIN_PATH` 值可能不同):

   .. code-block:: console

      # Linux, macOS:
      $ echo $ZEPHYR_TOOLCHAIN_VARIANT
      gnuarmemb
      $ echo $GNUARMEMB_TOOLCHAIN_PATH
      /home/you/Downloads/gnu_arm_embedded

      # Windows:
      > echo %ZEPHYR_TOOLCHAIN_VARIANT%
      gnuarmemb
      > echo %GNUARMEMB_TOOLCHAIN_PATH%
      C:\gnu_arm_embedded

   .. warning::

      在 macOS 上,如果您对建议的过程有困难,brew 上有一个非官方包可能会帮助您。
      运行 ``brew install gcc-arm-embedded`` 并配置变量

      - 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为 ``gnuarmemb``。
      - 将 :envvar:`GNUARMEMB_TOOLCHAIN_PATH` 设置为 brew 安装目录(类似 ``/usr/local``)

.. _GNU Arm Embedded: https://developer.arm.com/open-source/gnu-toolchain/gnu-rm
