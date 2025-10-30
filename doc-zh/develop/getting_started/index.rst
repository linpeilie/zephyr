.. _getting_started:.. _getting_started:



入门指南Getting Started Guide

##########################################



按照本指南：Follow this guide to:



- 在Ubuntu、macOS或Windows上设置命令行Zephyr开发环境（其他Linux发行版的说明- Set up a command-line Zephyr development environment on Ubuntu, macOS, or

  请参见 :ref:`installation_linux`）  Windows (instructions for other Linux distributions are discussed in

- 获取源代码  :ref:`installation_linux`)

- 构建、烧录和运行示例应用程序- Get the source code

- Build, flash, and run a sample application

.. _host_setup:

.. _host_setup:

选择并更新操作系统

********************Select and Update OS

********************

点击您正在使用的操作系统。

Click the operating system you are using.

.. tabs::

.. tabs::

   .. group-tab:: Ubuntu

   .. group-tab:: Ubuntu

      本指南涵盖Ubuntu 22.04 LTS及更高版本。

      如果您使用的是不同的Linux发行版，请参见 :ref:`installation_linux`。      This guide covers Ubuntu version 22.04 LTS and later.

      If you are using a different Linux distribution see :ref:`installation_linux`.

      .. code-block:: bash

      .. code-block:: bash

         sudo apt update

         sudo apt upgrade         sudo apt update

         sudo apt upgrade

   .. group-tab:: macOS

   .. group-tab:: macOS

      在macOS Mojave或更高版本上，选择 *系统偏好设置* >

      *软件更新*。如有必要，点击 *立即更新*。      On macOS Mojave or later, select *System Preferences* >

      *Software Update*. Click *Update Now* if necessary.

      在其他版本上，请参见 `Apple支持主题

      <https://support.apple.com/en-us/HT201541>`_。      On other versions, see `this Apple support topic

      <https://support.apple.com/en-us/HT201541>`_.

   .. group-tab:: Windows

   .. group-tab:: Windows

      选择 *开始* > *设置* > *更新和安全* > *Windows更新*。

      点击 *检查更新* 并安装任何可用的更新。      Select *Start* > *Settings* > *Update & Security* > *Windows Update*.

      Click *Check for updates* and install any that are available.

.. _install-required-tools:

.. _install-required-tools:

安装依赖项

********************Install dependencies

********************

接下来，您将使用包管理器安装一些主机依赖项。

Next, you'll install some host dependencies using your package manager.

主要依赖项当前所需的最低版本为：

The current minimum required version for the main dependencies are:

.. list-table::

   :header-rows: 1.. list-table::

   :header-rows: 1

   * - 工具

     - 最低版本   * - Tool

     - Min. Version

   * - `CMake <https://cmake.org/>`_

     - 3.20.5   * - `CMake <https://cmake.org/>`_

     - 3.20.5

   * - `Python <https://www.python.org/>`_

     - 3.10   * - `Python <https://www.python.org/>`_

     - 3.10

   * - `Devicetree compiler <https://www.devicetree.org/>`_

     - 1.4.6   * - `Devicetree compiler <https://www.devicetree.org/>`_

     - 1.4.6

.. tabs::

.. tabs::

   .. group-tab:: Ubuntu

   .. group-tab:: Ubuntu

      .. _install_dependencies_ubuntu:

      .. _install_dependencies_ubuntu:

      #. 使用 ``apt`` 安装所需的依赖项：

      #. Use ``apt`` to install the required dependencies:

         .. code-block:: bash

         .. code-block:: bash

            sudo apt install --no-install-recommends git cmake ninja-build gperf \

              ccache dfu-util device-tree-compiler wget python3-dev python3-venv python3-tk \            sudo apt install --no-install-recommends git cmake ninja-build gperf \

              xz-utils file make gcc gcc-multilib g++-multilib libsdl2-dev libmagic1              ccache dfu-util device-tree-compiler wget python3-dev python3-venv python3-tk \

              xz-utils file make gcc gcc-multilib g++-multilib libsdl2-dev libmagic1

         .. note::

         .. note::

            由于在AArch64（ARM64）系统上无法使用 ``gcc-multilib`` 和 ``g++-multilib``，

            您可能需要从要安装的包列表中省略它们。            Due to the unavailability of ``gcc-multilib`` and ``g++-multilib`` on AArch64

            (ARM64) systems, you may need to omit them from the list of packages to install.

      #. 通过输入以下命令验证系统上安装的主要依赖项的版本：

      #. Verify the versions of the main dependencies installed on your system by entering:

         .. code-block:: bash

         .. code-block:: bash

            cmake --version

            python3 --version            cmake --version

            dtc --version            python3 --version

            dtc --version

         将这些版本与本节开头表格中的版本进行对比。

         有关手动更新依赖项的其他信息，请参阅 :ref:`installation_linux` 页面。         Check those against the versions in the table in the beginning of this section.

         Refer to the :ref:`installation_linux` page for additional information on updating

   .. group-tab:: macOS         the dependencies manually.



      .. _install_dependencies_macos:   .. group-tab:: macOS



      #. 安装 `Homebrew <https://brew.sh/>`_：      .. _install_dependencies_macos:



         .. code-block:: bash      #. Install `Homebrew <https://brew.sh/>`_:



            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"         .. code-block:: bash



      #. Homebrew安装脚本完成后，按照屏幕上的说明将Homebrew安装添加到路径中。            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"



         * 在Apple Silicon上运行的macOS上，使用以下命令：      #. After the Homebrew installation script completes, follow the on-screen

         instructions to add the Homebrew installation to the path.

           .. code-block:: bash

         * On macOS running on Apple Silicon, this is achieved with:

              (echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> ~/.zprofile

              source ~/.zprofile           .. code-block:: bash



         * 在Intel上运行的macOS上，使用Apple Silicon的命令，但将 ``/opt/homebrew/`` 替换为 ``/usr/local/``。              (echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> ~/.zprofile

              source ~/.zprofile

      #. 使用 ``brew`` 安装所需的依赖项：

         * On macOS running on Intel, use the command for Apple Silicon, but replace ``/opt/homebrew/`` with ``/usr/local/``.

         .. code-block:: bash

      #. Use ``brew`` to install the required dependencies:

            brew install cmake ninja gperf python3 python-tk ccache qemu dtc libmagic wget openocd

         .. code-block:: bash

      #. 将Homebrew Python文件夹添加到路径中，以便能够

         执行 ``python`` 和 ``pip`` 以及 ``python3`` 和 ``pip3``。            brew install cmake ninja gperf python3 python-tk ccache qemu dtc libmagic wget openocd



           .. code-block:: bash      #. Add the Homebrew Python folder to the path, in order to be able to

         execute ``python`` and ``pip`` as well ``python3`` and ``pip3``.

              (echo; echo 'export PATH="'$(brew --prefix)'/opt/python/libexec/bin:$PATH"') >> ~/.zprofile

              source ~/.zprofile           .. code-block:: bash



   .. group-tab:: Windows              (echo; echo 'export PATH="'$(brew --prefix)'/opt/python/libexec/bin:$PATH"') >> ~/.zprofile

              source ~/.zprofile

      .. note::

   .. group-tab:: Windows

         由于查找可执行文件的问题，Zephyr项目目前

         不支持使用 `适用于Linux的Windows子系统(WSL)      .. note::

         <https://msdn.microsoft.com/en-us/commandline/wsl/install_guide>`_

         (WSL)进行应用程序烧录。         Due to issues finding executables, the Zephyr Project doesn't

         currently support application flashing using the `Windows Subsystem

         因此，我们不建议在入门时使用WSL。         for Linux (WSL)

         <https://msdn.microsoft.com/en-us/commandline/wsl/install_guide>`_

      在现代版本的Windows（10及更高版本）中，建议从Microsoft Store安装Windows Terminal         (WSL).

      应用程序。提供了 ``cmd.exe`` 或PowerShell命令提示符的说明。

         Therefore, we don't recommend using WSL when getting started.

      这些说明依赖于Windows的官方包管理器 `winget`_。

      如果无法使用winget，您可以从各自的网站安装依赖项，      In modern version of Windows (10 and later) it is recommended to install the Windows Terminal

      并确保命令行工具在您的 :envvar:`PATH` :ref:`环境变量 <env_vars>` 中。      application from the Microsoft Store. Instructions are provided for a ``cmd.exe`` or

      PowerShell command prompts.

      |p|

      These instructions rely on Windows' official package manager, `winget`_.

      .. _install_dependencies_windows:      If using winget isn't an option, you can install dependencies from their

      respective websites and ensure the command line tools are on your

      #. 在现代Windows版本中，winget默认已预装。      :envvar:`PATH` :ref:`environment variable <env_vars>`.

         您可以通过在终端窗口中输入 ``winget`` 来验证是否如此。

         如果失败，您可以 `安装winget`_。      |p|



      #. 打开命令提示符（``cmd.exe``）或PowerShell终端窗口。      .. _install_dependencies_windows:

         为此，按Windows键，输入 ``cmd.exe`` 或PowerShell，然后

         点击结果。      #. In modern Windows versions, winget is already pre-installed by default.

         You can verify that this is the case by typing ``winget`` in a terminal

      #. 使用 ``winget`` 安装所需的依赖项：         window. If that fails, you can then `install winget`_.



         .. code-block:: bat      #. Open a Command Prompt (``cmd.exe``) or PowerShell terminal window.

         To do so, press the Windows key, type ``cmd.exe`` or PowerShell and

            winget install Kitware.CMake Ninja-build.Ninja oss-winget.gperf Python.Python.3.12 Git.Git oss-winget.dtc wget 7zip.7zip         click on the result.



      #. 关闭终端窗口。      #. Use ``winget`` to install the required dependencies:



      .. note::         .. code-block:: bat



         您可能需要将7zip安装文件夹添加到您的 ``PATH`` 中。            winget install Kitware.CMake Ninja-build.Ninja oss-winget.gperf Python.Python.3.12 Git.Git oss-winget.dtc wget 7zip.7zip



      #. Close the terminal window.

.. _winget: https://learn.microsoft.com/en-us/windows/package-manager/

.. _安装winget: https://aka.ms/getwinget      .. note::



.. _get_the_code:         You may need to add the 7zip installation folder to your ``PATH``.

.. _clone-zephyr:

.. _install_py_requirements:

.. _gs_python_deps:.. _winget: https://learn.microsoft.com/en-us/windows/package-manager/

.. _install winget: https://aka.ms/getwinget

获取Zephyr并安装Python依赖项

******************************************.. _get_the_code:

.. _clone-zephyr:

接下来，将Zephyr及其 :ref:`模块 <modules>` 克隆到一个新的 :ref:`west.. _install_py_requirements:

<west>` 工作空间中。在以下说明中，工作空间名称使用 :file:`zephyrproject`，.. _gs_python_deps:

但在实践中其名称和位置可以自由选择。您还将在

`Python虚拟环境`_ 中安装Zephyr的附加Python依赖项。Get Zephyr and install Python dependencies

******************************************

.. _Python虚拟环境: https://docs.python.org/3/library/venv.html

Next, clone Zephyr and its :ref:`modules <modules>` into a new :ref:`west

.. tabs::<west>` workspace. In the following instructions the name :file:`zephyrproject`

is used for the workspace, however in practice its name and location can be freely

   .. group-tab:: Ubuntuchosen. You'll also install Zephyr's additional Python dependencies in a

`Python virtual environment`_.

      #. 创建一个新的虚拟环境：

.. _Python virtual environment: https://docs.python.org/3/library/venv.html

         .. code-block:: bash

.. tabs::

            python3 -m venv ~/zephyrproject/.venv

   .. group-tab:: Ubuntu

      #. 激活虚拟环境：

      #. Create a new virtual environment:

         .. code-block:: bash

         .. code-block:: bash

            source ~/zephyrproject/.venv/bin/activate

            python3 -m venv ~/zephyrproject/.venv

         激活后，您的shell将以 ``(.venv)`` 为前缀。

         虚拟环境可以随时通过运行 ``deactivate`` 来停用。      #. Activate the virtual environment:



         .. note::         .. code-block:: bash



            请记住在每次开始工作时激活虚拟环境。            source ~/zephyrproject/.venv/bin/activate



      #. 安装west：         Once activated your shell will be prefixed with ``(.venv)``. The

         virtual environment can be deactivated at any time by running

         .. code-block:: bash         ``deactivate``.



            pip install west         .. note::



      #. 获取Zephyr源代码：            Remember to activate the virtual environment every time you

            start working.

         .. only:: not release

      #. Install west:

            .. code-block:: bash

         .. code-block:: bash

               west init ~/zephyrproject

               cd ~/zephyrproject            pip install west

               west update

      #. Get the Zephyr source code:

         .. only:: release

         .. only:: not release

            .. 我们需要在这里使用parsed-literal，因为替换在代码块中不起作用。

               这意味着用户不能像其他块一样轻松地复制粘贴这些行，但应该仍然足够好 :)            .. code-block:: bash



            .. parsed-literal::               west init ~/zephyrproject

               cd ~/zephyrproject

               west init ~/zephyrproject --mr v |zephyr-version-ltrim|               west update

               cd ~/zephyrproject

               west update         .. only:: release



      #. 导出 :ref:`Zephyr CMake包 <cmake_pkg>`。这允许CMake            .. We need to use a parsed-literal here because substitutions do not work in code

         自动加载构建Zephyr应用程序所需的样板代码。               blocks. This means users can't copy-paste these lines as easily as other blocks but

               should be good enough still :)

         .. code-block:: bash

            .. parsed-literal::

            west zephyr-export

               west init ~/zephyrproject --mr v |zephyr-version-ltrim|

      #. 使用 ``west packages`` 安装Python依赖项。               cd ~/zephyrproject

               west update

         .. code-block:: bash

      #. Export a :ref:`Zephyr CMake package <cmake_pkg>`. This allows CMake to

            west packages pip --install         automatically load boilerplate code required for building Zephyr

         applications.

   .. group-tab:: macOS

         .. code-block:: bash

      #. 创建一个新的虚拟环境：

            west zephyr-export

         .. code-block:: bash

      #. Install Python dependencies using ``west packages``.

            python3 -m venv ~/zephyrproject/.venv

         .. code-block:: bash

      #. 激活虚拟环境：

            west packages pip --install

         .. code-block:: bash

   .. group-tab:: macOS

            source ~/zephyrproject/.venv/bin/activate

      #. Create a new virtual environment:

         激活后，您的shell将以 ``(.venv)`` 为前缀。

         虚拟环境可以随时通过运行 ``deactivate`` 来停用。         .. code-block:: bash



         .. note::            python3 -m venv ~/zephyrproject/.venv



            请记住在每次开始工作时激活虚拟环境。      #. Activate the virtual environment:



      #. 安装west：         .. code-block:: bash



         .. code-block:: bash            source ~/zephyrproject/.venv/bin/activate



            pip install west         Once activated your shell will be prefixed with ``(.venv)``. The

         virtual environment can be deactivated at any time by running

      #. 获取Zephyr源代码：         ``deactivate``.



         .. code-block:: bash         .. note::



            west init ~/zephyrproject            Remember to activate the virtual environment every time you

            cd ~/zephyrproject            start working.

            west update

      #. Install west:

      #. 导出 :ref:`Zephyr CMake包 <cmake_pkg>`。这允许CMake

         自动加载构建Zephyr应用程序所需的样板代码。         .. code-block:: bash



         .. code-block:: bash            pip install west



            west zephyr-export      #. Get the Zephyr source code:



      #. 使用 ``west packages`` 安装Python依赖项。         .. code-block:: bash



         .. code-block:: bash            west init ~/zephyrproject

            cd ~/zephyrproject

            west packages pip --install            west update



   .. group-tab:: Windows      #. Export a :ref:`Zephyr CMake package <cmake_pkg>`. This allows CMake to

         automatically load boilerplate code required for building Zephyr

      #. **以普通用户身份**打开 ``cmd.exe`` 或PowerShell终端窗口         applications.



      #. 创建一个新的虚拟环境：         .. code-block:: bash



         .. tabs::            west zephyr-export



            .. code-tab:: bat      #. Install Python dependencies using ``west packages``.



               cd %HOMEPATH%         .. code-block:: bash

               python -m venv zephyrproject\.venv

            west packages pip --install

            .. code-tab:: powershell

   .. group-tab:: Windows

               cd $Env:HOMEPATH

               python -m venv zephyrproject\.venv      #. Open a ``cmd.exe`` or PowerShell terminal window **as a regular user**



      #. 激活虚拟环境：      #. Create a new virtual environment:



         .. note::         .. tabs::



            Python在PowerShell中激活虚拟环境需要            .. code-tab:: bat

            运行脚本本身，这需要被允许。

               cd %HOMEPATH%

            .. code-block:: powershell               python -m venv zephyrproject\.venv



               Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser            .. code-tab:: powershell



         .. tabs::               cd $Env:HOMEPATH

               python -m venv zephyrproject\.venv

            .. code-tab:: bat

      #. Activate the virtual environment:

               zephyrproject\.venv\Scripts\activate.bat

         .. note::

            .. code-tab:: powershell

            Python's virtual environment activation in PowerShell requires

               zephyrproject\.venv\Scripts\Activate.ps1            running a script itself, which needs to be allowed.



         激活后，您的shell将以 ``(.venv)`` 为前缀。            .. code-block:: powershell

         虚拟环境可以随时通过运行 ``deactivate`` 来停用。

               Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

         .. note::

         .. tabs::

            请记住在每次开始工作时激活虚拟环境。

            .. code-tab:: bat

      #. 安装west：

               zephyrproject\.venv\Scripts\activate.bat

         .. code-block:: bat

            .. code-tab:: powershell

            pip install west

               zephyrproject\.venv\Scripts\Activate.ps1

      #. 获取Zephyr源代码：

         Once activated your shell will be prefixed with ``(.venv)``. The

         .. code-block:: bat         virtual environment can be deactivated at any time by running

         ``deactivate``.

            west init zephyrproject

            cd zephyrproject         .. note::

            west update

            Remember to activate the virtual environment every time you

      #. 导出 :ref:`Zephyr CMake包 <cmake_pkg>`。这允许CMake            start working.

         自动加载构建Zephyr应用程序所需的样板代码。

      #. Install west:

         .. code-block:: bat

         .. code-block:: bat

            west zephyr-export

            pip install west

      #. 使用 ``west packages`` 安装Python依赖项。

      #. Get the Zephyr source code:

         .. code-block:: bat

         .. code-block:: bat

            west packages pip --install

            west init zephyrproject

安装Zephyr SDK            cd zephyrproject

**********************            west update



:ref:`Zephyr软件开发工具包(SDK) <toolchain_zephyr_sdk>`      #. Export a :ref:`Zephyr CMake package <cmake_pkg>`. This allows CMake to

包含Zephyr支持的每个架构的工具链，其中包括构建         automatically load boilerplate code required for building Zephyr

Zephyr应用程序所需的编译器、汇编器、链接器和其他程序。         applications.



对于Linux，它还包含额外的主机工具，例如用于模拟、烧录和         .. code-block:: bat

调试Zephyr应用程序的自定义QEMU和OpenOCD构建。

            west zephyr-export



.. tabs::      #. Install Python dependencies using ``west packages``.



   .. group-tab:: Ubuntu         .. code-block:: bat



      使用 ``west sdk install`` 安装Zephyr SDK。            west packages pip --install



         .. code-block:: bashInstall the Zephyr SDK

**********************

            cd ~/zephyrproject/zephyr

            west sdk installThe :ref:`Zephyr Software Development Kit (SDK) <toolchain_zephyr_sdk>`

contains toolchains for each of Zephyr's supported architectures, which

      .. tip::include a compiler, assembler, linker and other programs required to build

Zephyr applications.

          使用命令选项，您可以指定SDK安装目标

          以及要安装的架构工具链。For Linux, it also contains additional host tools, such as custom QEMU and OpenOCD builds

          详见 ``west sdk install --help``。that are used to emulate, flash and debug Zephyr applications.



   .. group-tab:: macOS

.. tabs::

      使用 ``west sdk install`` 安装Zephyr SDK。

   .. group-tab:: Ubuntu

         .. code-block:: bash

      Install the Zephyr SDK using the ``west sdk install``.

            cd ~/zephyrproject/zephyr

            west sdk install         .. code-block:: bash



      .. tip::            cd ~/zephyrproject/zephyr

            west sdk install

          使用命令选项，您可以指定SDK安装目标

          以及要安装的架构工具链。      .. tip::

          详见 ``west sdk install --help``。

          Using the command options, you can specify the SDK installation destination

   .. group-tab:: Windows          and which architecture of toolchains to install.

          See ``west sdk install --help`` for details.

      使用 ``west sdk install`` 安装Zephyr SDK。

   .. group-tab:: macOS

         .. tabs::

      Install the Zephyr SDK using the ``west sdk install``.

            .. code-tab:: bat

         .. code-block:: bash

               cd %HOMEPATH%\zephyrproject\zephyr

               west sdk install            cd ~/zephyrproject/zephyr

            west sdk install

            .. code-tab:: powershell

      .. tip::

               cd $Env:HOMEPATH\zephyrproject\zephyr

               west sdk install          Using the command options, you can specify the SDK installation destination

          and which architecture of toolchains to install.

      .. tip::          See ``west sdk install --help`` for details.



          使用命令选项，您可以指定SDK安装目标   .. group-tab:: Windows

          以及要安装的架构工具链。

          详见 ``west sdk install --help``。      Install the Zephyr SDK using the ``west sdk install``.



.. note::         .. tabs::



    如果您想在不使用 ``west sdk`` 命令的情况下安装Zephyr SDK，            .. code-tab:: bat

    请参见 :ref:`toolchain_zephyr_sdk_install`。

               cd %HOMEPATH%\zephyrproject\zephyr

.. _getting_started_run_sample:               west sdk install



构建Blinky示例            .. code-tab:: powershell

***********************

               cd $Env:HOMEPATH\zephyrproject\zephyr

.. note::               west sdk install



   :zephyr:code-sample:`blinky` 与大多数（但不是全部）:ref:`开发板 <boards>` 兼容。      .. tip::

   如果您的开发板不满足Blinky的 :ref:`blinky-sample-requirements`，

   那么 :zephyr:code-sample:`hello_world` 是一个不错的替代方案。          Using the command options, you can specify the SDK installation destination

          and which architecture of toolchains to install.

   如果您不确定west为您的开发板使用什么名称，可以使用 ``west boards``          See ``west sdk install --help`` for details.

   获取Zephyr支持的所有开发板的列表。

.. note::

使用 :ref:`west build <west-building>` 构建 :zephyr:code-sample:`blinky`，

将 ``<your-board-name>`` 适当地更改为您的开发板名称：    If you want to install Zephyr SDK without using the ``west sdk`` command,

    please see :ref:`toolchain_zephyr_sdk_install`.

.. tabs::

.. _getting_started_run_sample:

   .. group-tab:: Ubuntu

Build the Blinky Sample

      .. code-block:: bash***********************



         cd ~/zephyrproject/zephyr.. note::

         west build -p always -b <your-board-name> samples/basic/blinky

   :zephyr:code-sample:`blinky` is compatible with most, but not all, :ref:`boards`. If your board

   .. group-tab:: macOS   does not meet Blinky's :ref:`blinky-sample-requirements`, then

   :zephyr:code-sample:`hello_world` is a good alternative.

      .. code-block:: bash

   If you are unsure what name west uses for your board, ``west boards``

         cd ~/zephyrproject/zephyr   can be used to obtain a list of all boards Zephyr supports.

         west build -p always -b <your-board-name> samples/basic/blinky

Build the :zephyr:code-sample:`blinky` with :ref:`west build <west-building>`, changing

   .. group-tab:: Windows``<your-board-name>`` appropriately for your board:



      .. tabs::.. tabs::



         .. code-tab:: bat   .. group-tab:: Ubuntu



            cd %HOMEPATH%\zephyrproject\zephyr      .. code-block:: bash

            west build -p always -b <your-board-name> samples\basic\blinky

         cd ~/zephyrproject/zephyr

         .. code-tab:: powershell         west build -p always -b <your-board-name> samples/basic/blinky



            cd $Env:HOMEPATH\zephyrproject\zephyr   .. group-tab:: macOS

            west build -p always -b <your-board-name> samples\basic\blinky

      .. code-block:: bash

``-p always`` 选项强制进行全新构建，建议新用户使用。

用户也可以使用 ``-p auto`` 选项，该选项将使用启发式方法         cd ~/zephyrproject/zephyr

确定是否需要全新构建，例如在构建另一个示例时。         west build -p always -b <your-board-name> samples/basic/blinky



.. note::   .. group-tab:: Windows



   一个开发板可能包含一个或多个SoC，同样，每个SoC可能包含一个或      .. tabs::

   多个CPU簇。

   在为此类开发板构建时，需要指定必须为其构建示例的SoC或CPU簇。         .. code-tab:: bat

   例如，要为 :zephyr:board:`nrf5340dk` 上的 ``cpuapp`` 核心构建

   :zephyr:code-sample:`blinky`，必须将开发板提供为：            cd %HOMEPATH%\zephyrproject\zephyr

   ``nrf5340dk/nrf5340/cpuapp``。更多详细信息，另请参见 :ref:`board_terminology`。            west build -p always -b <your-board-name> samples\basic\blinky



烧录示例         .. code-tab:: powershell

****************

            cd $Env:HOMEPATH\zephyrproject\zephyr

连接您的开发板（通常通过USB），如果有电源开关，请打开它。            west build -p always -b <your-board-name> samples\basic\blinky

如果不确定该怎么做，请查看您的开发板在 :ref:`boards` 中的页面。

The ``-p always`` option forces a pristine build, and is recommended for new

然后使用 :ref:`west flash <west-flashing>` 烧录示例：users. Users may also use the ``-p auto`` option, which will use

heuristics to determine if a pristine build is required, such as when building

.. code-block:: shellanother sample.



   west flash.. note::



.. note::   A board may contain one or multiple SoCs, Also, each SoC may contain one or

   more CPU clusters.

    您可能需要安装开发板所需的额外 :ref:`主机工具 <flash-debug-host-tools>`。   When building for such boards it is necessary to specify the SoC or CPU

    如果缺少任何必需的依赖项，``west flash`` 命令将打印错误。   cluster for which the sample must be built.

   For example to build :zephyr:code-sample:`blinky` for the ``cpuapp`` core on

.. note::   the :zephyr:board:`nrf5340dk` the board must be provided as:

   ``nrf5340dk/nrf5340/cpuapp``. See also :ref:`board_terminology` for more

    在Linux上使用时，第一次使用调试探针时可能需要配置udev规则。   details.

    另请参见 :ref:`setting-udev-rules`。

Flash the Sample

如果您使用的是blinky，LED将开始闪烁，如下图所示：****************



.. figure:: img/ReelBoard-Blinky.pngConnect your board, usually via USB, and turn it on if there's a power switch.

   :width: 400pxIf in doubt about what to do, check your board's page in :ref:`boards`.

   :name: reelboard-blinky

Then flash the sample using :ref:`west flash <west-flashing>`:

   Phytec :ref:`reel_board <reel_board>` 运行blinky

.. code-block:: shell

下一步

**********   west flash



以下是探索Zephyr的一些后续步骤：.. note::



* 尝试其他 :zephyr:code-sample-category:`示例 <samples>`    You may need to install additional :ref:`host tools <flash-debug-host-tools>`

* 了解 :ref:`应用程序 <application>` 和 :ref:`west <west>` 工具    required by your board. The ``west flash`` command will print an error if any

* 了解west的 :ref:`烧录和调试 <west-build-flash-debug>` 功能，    required dependencies are missing.

  或更多关于一般 :ref:`烧录和调试 <flashing_and_debugging>` 的内容

* 查看 :ref:`beyond-GSG` 了解其他设置方案和想法.. note::

* 发现 :ref:`项目资源 <project-resources>` 以从Zephyr社区获得帮助

    When using Linux, you may need to configure udev rules the first time

.. _troubleshooting_installation:    of using a debug probe.

    Please also see :ref:`setting-udev-rules`.

安装故障排除

****************************If you're using blinky, the LED will start to blink as shown in this figure:



以下是修复与安装过程相关的一些问题的提示。.. figure:: img/ReelBoard-Blinky.png

   :width: 400px

.. _toolchain_zephyr_sdk_update:   :name: reelboard-blinky



更新时仔细检查Zephyr SDK变量   Phytec :ref:`reel_board <reel_board>` running blinky

===================================================

Next Steps

更新Zephyr SDK时，检查 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT`**********

或 :envvar:`ZEPHYR_SDK_INSTALL_DIR` 环境变量是否已设置。

更多信息请参见 :ref:`gs_toolchain_update`。Here are some next steps for exploring Zephyr:



有关Zephyr中这些环境变量的更多信息，请参见 :ref:`env_vars_important`。* Try other :zephyr:code-sample-category:`samples`

* Learn about :ref:`application` and the :ref:`west <west>` tool

.. _help:* Find out about west's :ref:`flashing and debugging <west-build-flash-debug>`

  features, or more about :ref:`flashing_and_debugging` in general

寻求帮助* Check out :ref:`beyond-GSG` for additional setup alternatives and ideas

**************** Discover :ref:`project-resources` for getting help from the Zephyr

  community

您可以在邮件列表或Discord上寻求帮助。请将错误报告和

功能请求发送到GitHub。.. _troubleshooting_installation:



* **邮件列表**: users@lists.zephyrproject.org 通常是寻求帮助的正确列表。Troubleshooting Installation

  `在此处搜索存档并注册`_。****************************

* **Discord**: 您可以使用此 `Discord邀请`_ 加入。

* **GitHub**: 使用 `GitHub issues`_ 报告错误和功能请求。Here are some tips for fixing some issues related to the installation process.



如何提问.. _toolchain_zephyr_sdk_update:

==========

Double Check the Zephyr SDK Variables When Updating

.. important::===================================================



   请先搜索本文档和邮件列表存档。您的问题可能在那里已有答案。When updating Zephyr SDK, check whether the :envvar:`ZEPHYR_TOOLCHAIN_VARIANT`

or :envvar:`ZEPHYR_SDK_INSTALL_DIR` environment variables are already set.

不要只是说"这不起作用"或问"这能工作吗？"。尽可能详细地包括：See :ref:`gs_toolchain_update` for more information.



#. 您想做什么For more information about these environment variables in Zephyr, see :ref:`env_vars_important`.

#. 您尝试了什么（您输入的命令等）

#. 发生了什么（每个命令的输出等）.. _help:



使用复制/粘贴Asking for Help

==============***************



请**复制/粘贴文本**而不是对其拍照或截图。You can ask for help on a mailing list or on Discord. Please send bug reports and

文本包括源代码、终端命令及其输出。feature requests to GitHub.



这样做可以让人们更容易帮助您，也有助于其他用户* **Mailing Lists**: users@lists.zephyrproject.org is usually the right list to

搜索存档。不必要的截图会排除视力受损的开发者；  ask for help. `Search archives and sign up here`_.

其中一些是Zephyr的主要贡献者。`无障碍访问`_ 已被* **Discord**: You can join with this `Discord invite`_.

联合国承认为一项基本人权。* **GitHub**: Use `GitHub issues`_ for bugs and feature requests.



当将超过5行的计算机文本复制/粘贴到Discord或Github时，How to Ask

使用三个反引号来分隔代码段以创建代码片段。==========



.. _在此处搜索存档并注册: https://lists.zephyrproject.org/g/users.. important::

.. _Discord邀请: https://chat.zephyrproject.org

.. _GitHub issues: https://github.com/zephyrproject-rtos/zephyr/issues   Please search this documentation and the mailing list archives first. Your

.. _无障碍访问: https://www.w3.org/standards/webdesign/accessibility   question may have an answer there.


Don't just say "this isn't working" or ask "is this working?". Include as much
detail as you can about:

#. What you want to do
#. What you tried (commands you typed, etc.)
#. What happened (output of each command, etc.)

Use Copy/Paste
==============

Please **copy/paste text** instead of taking a picture or a screenshot of it.
Text includes source code, terminal commands, and their output.

Doing this makes it easier for people to help you, and also helps other users
search the archives. Unnecessary screenshots exclude vision impaired
developers; some are major Zephyr contributors. `Accessibility`_ has been
recognized as a basic human right by the United Nations.

When copy/pasting more than 5 lines of computer text into Discord or Github,
create a snippet using three backticks to delimit the snippet.

.. _Search archives and sign up here: https://lists.zephyrproject.org/g/users
.. _Discord invite: https://chat.zephyrproject.org
.. _GitHub issues: https://github.com/zephyrproject-rtos/zephyr/issues
.. _Accessibility: https://www.w3.org/standards/webdesign/accessibility
