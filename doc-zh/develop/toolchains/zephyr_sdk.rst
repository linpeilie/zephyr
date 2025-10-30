.. _toolchain_zephyr_sdk:

Zephyr SDK
##########

Zephyr 软件开发工具包(SDK)包含 Zephyr 支持的每个架构的工具链。它还包括额外的主机工具,
例如自定义 QEMU 和 OpenOCD。

强烈建议使用 Zephyr SDK,在某些情况下甚至可能是必需的(例如,在某些架构的 QEMU 中运行测试)。

支持的架构
***********************

Zephyr SDK 支持以下目标架构:

* ARC (32 位和 64 位;ARCv1、ARCv2、ARCv3)
* ARM (32 位和 64 位;ARMv6、ARMv7、ARMv8;A/R/M 配置文件)
* Microblaze (32 位)
* MIPS (32 位和 64 位)
* RISC-V (32 位和 64 位;RV32I、RV32E、RV64I)
* RX
* SPARC (32 位和 64 位;SPARC V8、SPARC V9)
* x86 (32 位和 64 位)
* Xtensa

.. _toolchain_zephyr_sdk_bundle_variables:

安装包和变量
*********************************

Zephyr SDK 包支持所有主要操作系统(Linux、macOS 和 Windows),并以压缩文件的形式提供。
安装包括提取文件并运行包含的设置脚本。下面的章节中描述了特定于操作系统的附加说明。

如果未选择工具链,构建系统会查找 Zephyr SDK 并使用其中的工具链。您可以通过将
环境变量 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为 ``zephyr`` 来强制执行此操作。

如果您将 Zephyr SDK 安装在任何默认位置之外(列在下面的操作系统特定说明中),
并且希望自动发现 Zephyr SDK,则必须通过运行设置脚本在 CMake 包注册表中注册
Zephyr SDK。如果您决定不在 CMake 注册表中注册 Zephyr SDK,则可以使用
:envvar:`ZEPHYR_SDK_INSTALL_DIR` 指向 Zephyr SDK 安装目录。

您还可以将 :envvar:`ZEPHYR_SDK_INSTALL_DIR` 设置为指向包含多个 Zephyr SDK 的目录,
从而允许自动选择工具链。例如,您可以将 ``ZEPHYR_SDK_INSTALL_DIR`` 设置为
``/company/tools``,其中 ``company/tools`` 文件夹包含以下子文件夹:

* ``/company/tools/zephyr-sdk-0.13.2``
* ``/company/tools/zephyr-sdk-a.b.c``
* ``/company/tools/zephyr-sdk-x.y.z``

这允许 Zephyr 构建系统选择正确版本的 SDK,同时允许将多个 Zephyr SDK 组合在特定路径中。

.. _toolchain_zephyr_sdk_compatibility:

Zephyr SDK 版本兼容性
********************************

一般来说,此页面中引用的 Zephyr SDK 版本应被视为相应 Zephyr 版本的推荐版本。

有关兼容的 Zephyr 和 Zephyr SDK 版本的完整列表,请参阅
`Zephyr SDK Version Compatibility Matrix`_。

.. _toolchain_zephyr_sdk_install:

Zephyr SDK 安装
***********************

.. toolchain_zephyr_sdk_install_start

.. note:: 如果需要,您可以在下面的说明中将 |sdk-version-literal| 更改为另一个版本;
          `Zephyr SDK Releases`_ 页面包含所有可用的 SDK 版本。

.. note:: 如果要卸载 SDK,只需删除安装它的目录即可。

.. tabs::

   .. group-tab:: Linux

      .. _linux_zephyr_sdk:

      #. 下载并验证 `Zephyr SDK bundle`_:

         .. parsed-literal::

            cd ~
            wget |sdk-url-linux|
            wget -O - |sdk-url-linux-sha| | shasum --check --ignore-missing

         如果您的主机架构是 64 位 ARM(例如,Raspberry Pi),请将 ``x86_64``
         替换为 ``aarch64`` 以下载 64 位 ARM Linux SDK。

      #. 提取 Zephyr SDK 包存档:

         .. parsed-literal::

            tar xvf zephyr-sdk- |sdk-version-trim| _linux-x86_64.tar.xz

         .. note::
            建议在以下位置之一提取 Zephyr SDK 包:

            * ``$HOME``
            * ``$HOME/.local``
            * ``$HOME/.local/opt``
            * ``$HOME/bin``
            * ``/opt``
            * ``/usr/local``

            Zephyr SDK 包存档包含 ``zephyr-sdk-<version>`` 目录,
            当在 ``$HOME`` 下提取时,生成的安装路径将是
            ``$HOME/zephyr-sdk-<version>``。

      #. 运行 Zephyr SDK 包设置脚本:

         .. parsed-literal::

            cd zephyr-sdk- |sdk-version-ltrim|
            ./setup.sh

         .. note::
            提取 Zephyr SDK 包后,您只需运行一次设置脚本。

            如果在初始设置后重新定位 Zephyr SDK 包目录,则必须重新运行设置脚本。

      #. 安装 `udev <https://en.wikipedia.org/wiki/Udev>`_ 规则,
         允许您作为普通用户烧录大多数 Zephyr 开发板:

         .. parsed-literal::

            sudo cp ~/zephyr-sdk- |sdk-version-trim| /sysroots/x86_64-pokysdk-linux/usr/share/openocd/contrib/60-openocd.rules /etc/udev/rules.d
            sudo udevadm control --reload

   .. group-tab:: macOS

      .. _macos_zephyr_sdk:

      #. Download and verify the `Zephyr SDK bundle`_:

         .. parsed-literal::

            cd ~
            curl -L -O |sdk-url-macos|
            curl -L |sdk-url-macos-sha| | shasum --check --ignore-missing

         如果您的主机架构是 64 位 ARM(Apple Silicon),请将 ``x86_64`` 替换为 ``aarch64`` 以便下载 64 位 ARM macOS SDK。

      #. 提取 Zephyr SDK 包存档:

         .. parsed-literal::

            tar xvf zephyr-sdk- |sdk-version-trim| _macos-x86_64.tar.xz

         .. note::
            建议在以下位置之一提取 Zephyr SDK 包:

            * ``$HOME``
            * ``$HOME/.local``
            * ``$HOME/.local/opt``
            * ``$HOME/bin``
            * ``/opt``
            * ``/usr/local``

            Zephyr SDK 包存档包含 ``zephyr-sdk-<version>`` 目录,当在 ``$HOME`` 下提取时,生成的安装路径将是 ``$HOME/zephyr-sdk-<version>``。

      #. 运行 Zephyr SDK 包设置脚本:

         .. parsed-literal::

            cd zephyr-sdk- |sdk-version-ltrim|
            ./setup.sh

         .. note::
            提取 Zephyr SDK 包后,您只需运行一次设置脚本。

            如果在初始设置后重新定位 Zephyr SDK 包目录,则必须重新运行设置脚本。

   .. group-tab:: Windows

      .. _windows_zephyr_sdk:

      #. **以普通用户身份**打开 ``cmd.exe`` 终端窗口

      #. 下载 `Zephyr SDK bundle`_:

         .. parsed-literal::

            cd %HOMEPATH%
            wget |sdk-url-windows|

      #. 提取 Zephyr SDK 包存档:

         .. parsed-literal::

            7z x zephyr-sdk- |sdk-version-trim| _windows-x86_64.7z

         .. note::
            建议在以下位置之一提取 Zephyr SDK 包:

            * ``%HOMEPATH%``
            * ``%PROGRAMFILES%``

            Zephyr SDK 包存档包含 ``zephyr-sdk-<version>`` 目录,当在 ``%HOMEPATH%`` 下提取时,生成的安装路径将是 ``%HOMEPATH%\zephyr-sdk-<version>``。

      #. 运行 Zephyr SDK 包设置脚本:

         .. parsed-literal::

            cd zephyr-sdk- |sdk-version-ltrim|
            setup.cmd

         .. note::
            提取 Zephyr SDK 包后,您只需运行一次设置脚本。

            如果在初始设置后重新定位 Zephyr SDK 包目录,则必须重新运行设置脚本。

.. _Zephyr SDK Releases: https://github.com/zephyrproject-rtos/sdk-ng/tags
.. _Zephyr SDK Version Compatibility Matrix: https://github.com/zephyrproject-rtos/sdk-ng/wiki/Zephyr-Version-Compatibility#zephyr-sdk-version-compatibility-matrix

.. toolchain_zephyr_sdk_install_end
