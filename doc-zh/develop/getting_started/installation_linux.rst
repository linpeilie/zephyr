.. _installation_linux:.. _installation_linux:



安装 Linux 主机依赖项Install Linux Host Dependencies

##############################################################



文档适用于以下 Linux 发行版:Documentation is available for these Linux distributions:



* Ubuntu* Ubuntu

* Fedora* Fedora

* Clear Linux* Clear Linux

* Arch Linux* Arch Linux



对于不基于滚动发布的发行版,某些要求和依赖项可能无法通过包管理器满足。在这种For distributions that are not based on rolling releases, some of the

情况下,请遵循提供的额外说明,从包管理器以外的来源查找软件。requirements and dependencies may not be met by your package manager. In that

case please follow the additional instructions that are provided to find

.. note:: 如果您在企业防火墙后工作,可能需要配置代理以访问互联网(如果尚未software from sources other than the package manager.

   配置)。虽然某些工具使用环境变量 ``http_proxy`` 和 ``https_proxy`` 来获取

   代理设置,但有些工具使用自己的配置文件,最著名的是 ``apt`` 和 ``git``。.. note:: If you're working behind a corporate firewall, you'll likely

   need to configure a proxy for accessing the internet, if you haven't

更新您的操作系统   done so already.  While some tools use the environment variables

****************************   ``http_proxy`` and ``https_proxy`` to get their proxy settings, some

   use their own configuration files, most notably ``apt`` and

确保您的主机系统是最新的。   ``git``.



.. tabs::Update Your Operating System

****************************

   .. group-tab:: Ubuntu

Ensure your host system is up to date.

      .. code-block:: console

.. tabs::

         sudo apt-get update

         sudo apt-get upgrade   .. group-tab:: Ubuntu



   .. group-tab:: Fedora      .. code-block:: console



      .. code-block:: console         sudo apt-get update

         sudo apt-get upgrade

         sudo dnf upgrade

   .. group-tab:: Fedora

   .. group-tab:: Clear Linux

      .. code-block:: console

      .. code-block:: console

         sudo dnf upgrade

         sudo swupd update

   .. group-tab:: Clear Linux

   .. group-tab:: Arch Linux

      .. code-block:: console

      .. code-block:: console

         sudo swupd update

         sudo pacman -Syu

   .. group-tab:: Arch Linux

.. _linux_requirements:

      .. code-block:: console

安装要求和依赖项

*************************************         sudo pacman -Syu



.. NOTE FOR DOCS AUTHORS: DO NOT PUT DOCUMENTATION BUILD DEPENDENCIES HERE... _linux_requirements:



   This section is for dependencies to build Zephyr binaries, *NOT* thisInstall Requirements and Dependencies

   documentation. If you need to add a dependency only required for building*************************************

   the docs, add it to doc/README.rst. (This change was made following the

   introduction of LaTeX->PDF support for the docs, as the texlive footprint is.. NOTE FOR DOCS AUTHORS: DO NOT PUT DOCUMENTATION BUILD DEPENDENCIES HERE.

   massive and not needed by users not building PDF documentation.)

   This section is for dependencies to build Zephyr binaries, *NOT* this

请注意,这些说明会同时安装 Ninja 和 Make;您只需要其中一个。   documentation. If you need to add a dependency only required for building

   the docs, add it to doc/README.rst. (This change was made following the

.. tabs::   introduction of LaTeX->PDF support for the docs, as the texlive footprint is

   massive and not needed by users not building PDF documentation.)

   .. group-tab:: Ubuntu

Note that both Ninja and Make are installed with these instructions; you only

      .. code-block:: consoleneed one.



         sudo apt-get install --no-install-recommends git cmake ninja-build gperf \.. tabs::

           ccache dfu-util device-tree-compiler wget \

           python3-dev python3-pip python3-setuptools python3-tk python3-wheel xz-utils file \   .. group-tab:: Ubuntu

           make gcc gcc-multilib g++-multilib libsdl2-dev libmagic1

      .. code-block:: console

   .. group-tab:: Fedora

         sudo apt-get install --no-install-recommends git cmake ninja-build gperf \

      .. code-block:: console           ccache dfu-util device-tree-compiler wget \

           python3-dev python3-pip python3-setuptools python3-tk python3-wheel xz-utils file \

         sudo dnf group install "Development Tools" "C Development Tools and Libraries"           make gcc gcc-multilib g++-multilib libsdl2-dev libmagic1

         sudo dnf install cmake ninja-build gperf dfu-util dtc wget which \

           python3-pip python3-tkinter xz file python3-devel SDL2-devel   .. group-tab:: Fedora



   .. group-tab:: Clear Linux      .. code-block:: console



      .. code-block:: console         sudo dnf group install "Development Tools" "C Development Tools and Libraries"

         sudo dnf install cmake ninja-build gperf dfu-util dtc wget which \

         sudo swupd bundle-add c-basic dev-utils dfu-util dtc \           python3-pip python3-tkinter xz file python3-devel SDL2-devel

           os-core-dev python-basic python3-basic python3-tcl

   .. group-tab:: Clear Linux

      Clear Linux 的重点是*原生*性能和安全性,而不是交叉编译。因此,它独特地

      默认导出到所有用户的 :ref:`环境 <env_vars>` 中一个编译器和链接器标志列表。      .. code-block:: console

      Zephyr 的 CMake 构建系统会因此发出警告或失败。要清除其中的 C/C++ 标志并

      修复 Zephyr 构建,请以 root 身份运行以下命令,然后注销并重新登录:         sudo swupd bundle-add c-basic dev-utils dfu-util dtc \

           os-core-dev python-basic python3-basic python3-tcl

      .. code-block:: console

      The Clear Linux focus is on *native* performance and security and not

         echo 'unset CFLAGS CXXFLAGS' >> /etc/profile.d/unset_cflags.sh      cross-compilation. For that reason it uniquely exports by default to the

      :ref:`environment <env_vars>` of all users a list of compiler and linker

      请注意,此命令会为*系统上的所有用户*取消设置 C/C++ 标志。每个 Linux 发行版      flags. Zephyr's CMake build system will either warn or fail because of

      都有一个独特的、相对复杂且可能不断发展的 bash 初始化文件序列,它们相互引用,      these. To clear the C/C++ flags among these and fix the Zephyr build, run

      Clear Linux 也不例外。如果您需要更灵活的解决方案,请从查看      the following command as root then log out and back in:

      ``/usr/share/defaults/etc/profile`` 中的逻辑开始。

      .. code-block:: console

   .. group-tab:: Arch Linux

         echo 'unset CFLAGS CXXFLAGS' >> /etc/profile.d/unset_cflags.sh

      .. code-block:: console

      Note this command unsets the C/C++ flags for *all users on the

         sudo pacman -S git cmake ninja gperf ccache dfu-util dtc wget \      system*. Each Linux distribution has a unique, relatively complex and

             python-pip python-setuptools python-wheel tk xz file make      potentially evolving sequence of bash initialization files sourcing each

      other and Clear Linux is no exception. If you need a more flexible

CMake      solution, start by looking at the logic in

=====      ``/usr/share/defaults/etc/profile``.



需要 :ref:`较新的 CMake 版本 <install-required-tools>`。使用 ``cmake --version``    .. group-tab:: Arch Linux

检查您的版本。如果您使用的是较旧版本,有几种方法可以获得更新的版本:

      .. code-block:: console

* 在 Ubuntu 上,您可以按照添加 `kitware 第三方 apt 仓库 <https://apt.kitware.com/>`_

  的说明,使用 apt 获取更新版本的 cmake。         sudo pacman -S git cmake ninja gperf ccache dfu-util dtc wget \

             python-pip python-setuptools python-wheel tk xz file make

* 从 CMake 项目网站下载并安装打包的 cmake。

  (请注意,这不会卸载以前版本的 cmake。)CMake

=====

  .. code-block:: console

A :ref:`recent CMake version <install-required-tools>` is required. Check what

     cd ~version you have by using ``cmake --version``. If you have an older version,

     wget https://github.com/Kitware/CMake/releases/download/v3.21.1/cmake-3.21.1-Linux-x86_64.shthere are several ways of obtaining a more recent one:

     chmod +x cmake-3.21.1-Linux-x86_64.sh

     sudo ./cmake-3.21.1-Linux-x86_64.sh --skip-license --prefix=/usr/local* On Ubuntu, you can follow the instructions for adding the

     hash -r  `kitware third-party apt repository <https://apt.kitware.com/>`_

  to get an updated version of cmake using apt.

  如果安装脚本将 cmake 放入 PATH 上的新位置,可能需要使用 ``hash -r`` 命令。

* Download and install a packaged cmake from the CMake project site.

* 从 CMake 项目在 `CMake Downloads`_ 页面提供的预构建二进制文件下载并安装。  (Note this won't uninstall the previous version of cmake.)

  例如,要在 :file:`~/bin/cmake` 中安装版本 3.21.1:

  .. code-block:: console

  .. code-block:: console

     cd ~

     mkdir $HOME/bin/cmake && cd $HOME/bin/cmake     wget https://github.com/Kitware/CMake/releases/download/v3.21.1/cmake-3.21.1-Linux-x86_64.sh

     wget https://github.com/Kitware/CMake/releases/download/v3.21.1/cmake-3.21.1-Linux-x86_64.sh     chmod +x cmake-3.21.1-Linux-x86_64.sh

     yes | sh cmake-3.21.1-Linux-x86_64.sh | cat     sudo ./cmake-3.21.1-Linux-x86_64.sh --skip-license --prefix=/usr/local

     echo "export PATH=$PWD/cmake-3.21.1-Linux-x86_64/bin:\$PATH" >> $HOME/.zephyrrc     hash -r



* 使用 ``pip3``:  The ``hash -r`` command may be necessary if the installation script

  put cmake into a new location on your PATH.

  .. code-block:: console

* Download and install from the pre-built binaries provided by the CMake

     pip3 install --user cmake  project itself in the `CMake Downloads`_ page.

  For example, to install version 3.21.1 in :file:`~/bin/cmake`:

  请注意,这不会卸载以前版本的 cmake,并将新 cmake 安装到您的 ~/.local/bin

  文件夹中,因此您需要将 ~/.local/bin 添加到 PATH 中。(有关详细信息,请参阅   .. code-block:: console

  :ref:`python-pip`。)

     mkdir $HOME/bin/cmake && cd $HOME/bin/cmake

* 检查您发行版的测试版或不稳定发布包库以获取更新。     wget https://github.com/Kitware/CMake/releases/download/v3.21.1/cmake-3.21.1-Linux-x86_64.sh

     yes | sh cmake-3.21.1-Linux-x86_64.sh | cat

* 在 Ubuntu 上,您还可以使用 snap 获取最新可用版本:     echo "export PATH=$PWD/cmake-3.21.1-Linux-x86_64/bin:\$PATH" >> $HOME/.zephyrrc



  .. code-block:: console* Use ``pip3``:



     sudo snap install cmake  .. code-block:: console



更新 cmake 后,使用 ``cmake --version`` 验证是否找到新安装的 cmake。     pip3 install --user cmake

您可能还想卸载包管理器提供的 CMake 以避免冲突。(使用 ``whereis cmake``

查找其他已安装的版本。)  Note this won't uninstall the previous version of cmake and will

  install the new cmake into your ~/.local/bin folder so

DTC (设备树编译器)  you'll need to add ~/.local/bin to your PATH.  (See :ref:`python-pip`

==========================  for details.)



需要 :ref:`较新的 DTC 版本 <install-required-tools>`。使用 ``dtc --version`` * Check your distribution's beta or unstable release package library for an

检查您的版本。如果您使用的是较旧版本,可以通过从源代码构建来安装更新的版本,  update.

或者通过安装 :ref:`Zephyr SDK <toolchain_zephyr_sdk>` 来使用其中捆绑的版本。

* On Ubuntu you can also use snap to get the latest version available:

Python

======  .. code-block:: console



需要 :ref:`现代 Python 3 版本 <install-required-tools>`。使用 ``python3 --version``      sudo snap install cmake

检查您的版本。

After updating cmake, verify that the newly installed cmake is found

如果您使用的是较旧版本,则需要安装更新的 Python 3。您可以从源代码构建,或者using ``cmake --version``.

如果可用,可以使用发行版包管理器渠道的反向移植版本。建议在虚拟环境中隔离此 You might also want to uninstall the CMake provided by your package manager to

Python,以避免干扰系统 Python。avoid conflicts.  (Use ``whereis cmake`` to find other installed

versions.)

.. _pyenv: https://github.com/pyenv/pyenv

DTC (Device Tree Compiler)

安装 Zephyr 软件开发工具包 (SDK)==========================

*************************************************

A :ref:`recent DTC version <install-required-tools>` is required. Check what

Zephyr 软件开发工具包 (SDK) 包含 Zephyr 支持的每个架构的工具链。它还包括额外的version you have by using ``dtc --version``. If you have an older version,

主机工具,例如自定义 QEMU 和 OpenOCD。either install a more recent one by building from source, or use the one that is

bundled in the :ref:`Zephyr SDK <toolchain_zephyr_sdk>` by installing it.

强烈建议使用 Zephyr SDK,在某些条件下甚至可能需要它(例如,在 QEMU 中运行某些

架构的测试)。Python

======

要安装 SDK,请遵循 :ref:`Zephyr SDK 安装指南 <linux_zephyr_sdk>` 中的 Linux 步骤。

A :ref:`modern Python 3 version <install-required-tools>` is required. Check

.. _sdkless_builds:what version you have by using ``python3 --version``.



在 Linux 上不使用 Zephyr SDK 进行构建If you have an older version, you will need to install a more recent Python 3.

****************************************You can build from source, or use a backport from your distribution's package

manager channels if one is available. Isolating this Python in a virtual

Zephyr SDK 是为了方便和易用而提供的。它为所有 Zephyr 目标架构提供工具链,environment is recommended to avoid interfering with your system Python.

并且在构建应用程序或运行测试时不需要任何额外的标志。除了交叉编译器之外,

Zephyr SDK 还提供预构建的主机工具。但是,可以通过使用 :ref:`toolchains` .. _pyenv: https://github.com/pyenv/pyenv

部分中描述的其他工具链来在不使用 SDK 工具链的情况下进行构建。

Install the Zephyr Software Development Kit (SDK)

如上所述,SDK 还包括预构建的主机工具。要将 SDK 的预构建主机工具与来自其他*************************************************

来源的工具链一起使用,必须将 :envvar:`ZEPHYR_SDK_INSTALL_DIR` 环境变量设置为

Zephyr SDK 安装目录。要在不使用 Zephyr SDK 预构建主机工具的情况下进行构建,The Zephyr Software Development Kit (SDK) contains toolchains for each of

必须取消设置 :envvar:`ZEPHYR_SDK_INSTALL_DIR` 环境变量。Zephyr's supported architectures. It also includes additional host tools, such

as custom QEMU and OpenOCD.

要确保取消设置此变量,请运行:

Use of the Zephyr SDK is highly recommended and may even be required under

.. code-block:: consolecertain conditions (for example, running tests in QEMU for some architectures).



   unset ZEPHYR_SDK_INSTALL_DIRTo install the SDK, follow the Linux steps from the :ref:`Zephyr SDK installation guide <linux_zephyr_sdk>`.



.. _Zephyr SDK Releases: https://github.com/zephyrproject-rtos/sdk-ng/tags.. _sdkless_builds:

.. _CMake Downloads: https://cmake.org/download

Building on Linux without the Zephyr SDK
****************************************

The Zephyr SDK is provided for convenience and ease of use. It provides
toolchains for all Zephyr target architectures, and does not require any extra
flags when building applications or running tests. In addition to
cross-compilers, the Zephyr SDK also provides prebuilt host tools. It is,
however, possible to build without the SDK's toolchain by using another
toolchain as described in the :ref:`toolchains` section.

As already noted above, the SDK also includes prebuilt host tools.  To use the
SDK's prebuilt host tools with a toolchain from another source, you must set the
:envvar:`ZEPHYR_SDK_INSTALL_DIR` environment variable to the Zephyr SDK
installation directory. To build without the Zephyr SDK's prebuilt host tools,
the :envvar:`ZEPHYR_SDK_INSTALL_DIR` environment variable must be unset.

To make sure this variable is unset, run:

.. code-block:: console

   unset ZEPHYR_SDK_INSTALL_DIR

.. _Zephyr SDK Releases: https://github.com/zephyrproject-rtos/sdk-ng/tags
.. _CMake Downloads: https://cmake.org/download
