.. _other_x_compilers:

其他交叉编译器
##############

此工具链变体借鉴自 Linux 内核构建系统使用 ``CROSS_COMPILE`` 环境变量设置基于 GNU 的交叉工具链的机制。

此类"其他交叉编译器"的示例包括 Linux 发行版打包的交叉工具链、您自己编译的工具链或从网上下载的工具链。与 :ref:`toolchains` 中特别列出的工具链不同,Zephyr 构建系统可能未经过它们的测试,也不正式支持它们。(尽管如此,工具链设置机制本身是受支持的。)

按照以下步骤使用这些工具链之一。

#. 安装适合您的主机和目标系统的交叉编译器。

   例如,您可能在基于 Debian 的 Linux 系统上安装 ``gcc-arm-none-eabi`` 包,或在 Fedora 或 Red Hat 上安装 ``arm-none-eabi-newlib``:

   .. code-block:: console

      # On Debian or Ubuntu
      sudo apt-get install gcc-arm-none-eabi
      # On Fedora or Red Hat
      sudo dnf install arm-none-eabi-newlib

#. :ref:`设置这些环境变量 <env_vars>`:

   - 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为 ``cross-compile``。
   - 将 ``CROSS_COMPILE`` 设置为工具链二进制文件具有的公共路径前缀,例如,包含编译器二进制文件的目录路径加上目标三元组和尾随破折号。

#. 要检查您是否在当前环境中正确设置了这些变量,请遵循这些示例 shell 会话(您系统上的 ``CROSS_COMPILE`` 值可能不同):

   .. code-block:: console

      # Linux, macOS:
      $ echo $ZEPHYR_TOOLCHAIN_VARIANT
      cross-compile
      $ echo $CROSS_COMPILE
      /usr/bin/arm-none-eabi-

   您还可以将 ``CROSS_COMPILE`` 设置为 CMake 变量。

使用此选项时,您的所有工具链二进制文件必须位于同一目录中并具有公共文件名前缀。``CROSS_COMPILE`` 变量设置为目录与文件名前缀的连接。在上面的 Debian 示例中,``gcc-arm-none-eabi`` 包在目录 ``/usr/bin/`` 中安装诸如 ``arm-none-eabi-gcc`` 和 ``arm-none-eabi-ld`` 之类的二进制文件,因此公共前缀是 ``/usr/bin/arm-none-eabi-``(包括尾随破折号 ``-``)。如果您的工具链安装在 ``/opt/mytoolchain/bin`` 中,二进制名称基于目标三元组 ``myarch-none-elf``,则 ``CROSS_COMPILE`` 将设置为 ``/opt/mytoolchain/bin/myarch-none-elf-``。
