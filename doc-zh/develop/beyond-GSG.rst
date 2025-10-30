.. _beyond-gsg:

超越入门指南
################################

:ref:`getting_started` 提供了一条直接的路径来为 Zephyr 开发设置您的 Linux、macOS 或 Windows 环境。在本文档中,我们深入探讨 Zephyr 开发设置问题和替代方案。

.. _python-pip:

Python 和 pip
**************

Python 3 及其包管理器 pip\ [#pip]_ 被 Zephyr 广泛用于安装和运行编译和运行 Zephyr 应用所需的脚本、设置和维护 Zephyr 开发环境以及构建项目文档。

根据您的操作系统,在安装新包时,您可能需要向 ``pip3`` 命令提供 ``--user`` 标志。这在整个说明中都有记录。有关 pip\ [#pip]_ 的更多信息,包括 `关于 -\\-user 的信息`_,请参阅 Python 打包用户指南中的 `安装包`_。

- 在 Linux 上,确保 ``~/.local/bin`` 位于您的 :envvar:`PATH` :ref:`环境变量 <env_vars>` 的前面,否则将找不到使用 ``--user`` 安装的程序。使用 ``--user`` 安装可以避免 pip 与系统包管理器之间的冲突,这是基于 Debian 的发行版的默认设置。

- 在 macOS 上,`Homebrew 禁用 -\\-user`_。

- 在 Windows 上,如果需要使用此选项,请参阅 `安装包`_ 关于 ``--user`` 的信息。

在所有操作系统上,pip 的 ``-U`` 标志会安装或更新包(如果包已在本地安装但有更新版本可用)。如果需要包的最新版本,使用此标志是一个好习惯。(检查 :zephyr_file:`scripts/requirements.txt` 文件以查看是否需要特定的 Python 包版本。)

高级平台设置
***********************

以下是受支持开发平台的更高级平台设置配置的一些替代说明:

.. toctree::
   :maxdepth: 1

   Linux 设置替代方案 <getting_started/installation_linux.rst>
   macOS 设置替代方案 <getting_started/installation_mac.rst>
   Windows 设置替代方案 <getting_started/installation_win.rst>

.. _gs_toolchain:

安装工具链
*******************

Zephyr 二进制文件由 *工具链* 编译和链接,该工具链由交叉编译器和相关工具组成,与用于开发在主机操作系统上本地运行的软件的编译器和工具不同。

您可以安装 :ref:`Zephyr SDK <toolchain_zephyr_sdk>` 以获取所有支持架构的工具链,或安装 SoC 供应商或特定板推荐的 :ref:`替代工具链 <toolchains>`(查看您特定的 :ref:`板级文档 <boards>`)。

您可以通过设置 :ref:`环境变量 <env_vars>` 来配置 Zephyr 构建系统使用特定工具链,例如将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT <{TOOLCHAIN}_TOOLCHAIN_PATH>` 设置为支持的值,以及特定于工具链变体的其他变量。

.. _gs_toolchain_update:

更新 Zephyr SDK 工具链
*********************************

更新 Zephyr SDK 时,请检查 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 或 :envvar:`ZEPHYR_SDK_INSTALL_DIR` 环境变量是否已设置。

* 如果变量未设置,将默认选择 Zephyr SDK 的最新兼容版本。继续下一步而不进行任何更改。

* 如果设置了 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT`,将在构建时选择相应的工具链。Zephyr SDK 由值 ``zephyr`` 标识。如果 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 环境变量不是 ``zephyr``,则取消设置它或将其值更改为 ``zephyr`` 以确保选择 Zephyr SDK。

* 如果设置了 :envvar:`ZEPHYR_SDK_INSTALL_DIR` 环境变量,它将覆盖 Zephyr SDK 的默认查找位置。如果您将 Zephyr SDK 安装到 :ref:`推荐位置 <toolchain_zephyr_sdk_bundle_variables>` 之一,则可以取消设置此变量。否则,将其设置为您选择的安装位置。

有关 Zephyr 中这些环境变量的更多信息,请参阅 :ref:`env_vars_important`。

克隆 Zephyr 仓库
*******************************

Zephyr 项目源代码维护在 `GitHub zephyr 仓库 <https://github.com/zephyrproject-rtos/zephyr>`_ 中。Zephyr 使用的外部模块位于父 `GitHub Zephyr 项目 <https://github.com/zephyrproject-rtos/>`_ 中。由于这些依赖关系,使用 Zephyr 创建的 :ref:`west <west>` 工具来获取和管理 Zephyr 和外部模块源代码很方便。有关更多详细信息,请参阅 :ref:`west-basics`。

安装开发工具后,使用 :ref:`west` 从 zephyr 和外部模块仓库创建、初始化和下载源代码。我们将使用名称 ``zephyrproject``,但您可以选择任何在路径中任何位置都不包含空格的名称。

.. code-block:: console

   west init zephyrproject
   cd zephyrproject
   west update

``west update`` 命令获取并保持 :file:`zephyrproject` 文件夹中的 :ref:`模块 <modules>` 与本地 zephyr 仓库中的代码同步。

.. warning::

   每当 :file:`zephyr/west.yml` 更改时,您必须运行 ``west update``,例如,当您拉取 :file:`zephyr` 仓库、在其中切换分支或在其中执行 ``git bisect`` 时。

保持 Zephyr 更新
======================

要更新 Zephyr 项目源代码,您需要通过 ``git`` 获取最新更改。之后,运行前一段中提到的 ``west update``。此外,如果 Python 依赖项更新或添加,运行 ``west packages pip --install`` 将确保这些依赖项是最新的。

.. code-block:: console

   # 将 zephyrproject 替换为您给 west init 的路径
   cd zephyrproject/zephyr
   git pull
   west update
   west packages pip --install

导出 Zephyr CMake 包
***************************

如果尚未作为 :ref:`getting_started` 的一部分完成,:ref:`cmake_pkg` 可以导出到 CMake 的用户包注册表。

.. _gs-board-aliases:

板别名
*************

使用多个板的开发人员可能会发现显式板名称繁琐,并希望为常见目标使用别名。CMake 文件支持这一点,内容如下:

.. code-block:: cmake

   # 变量 foo_BOARD_ALIAS=bar 将 BOARD=foo 替换为 BOARD=bar 并在 CMake 缓存中设置 BOARD_ALIAS=foo。
   set(pca10028_BOARD_ALIAS nrf51dk/nrf51822)
   set(pca10056_BOARD_ALIAS nrf52840dk/nrf52840)
   set(k64f_BOARD_ALIAS frdm_k64f)
   set(sltb004a_BOARD_ALIAS efr32mg_sltb004a)

并在 :envvar:`ZEPHYR_BOARD_ALIASES` 中指定其位置。这使得可以在 ``cmake -DBOARD=pca10028`` 和 ``west -b pca10028`` 等上下文中使用别名 ``pca10028``。

构建和运行应用
****************************

您可以使用支持的主机系统在真实硬件上构建、烧录和运行 Zephyr 应用。根据您的操作系统,您还可以使用 QEMU 在仿真中运行它,或使用 :zephyr:board:`native_sim <native_sim>` 作为本地应用运行它。有关构建应用的其他信息可以在 :ref:`build_an_application` 部分找到。

构建 Blinky
============

让我们构建 :zephyr:code-sample:`blinky` 示例应用。

Zephyr 应用构建为在特定硬件上运行,称为"板"\ [#board_misnomer]_。我们将在这里使用 Phytec :ref:`reel_board <reel_board>`,但如果您有不同的板,可以将 ``reel_board`` 构建目标更改为另一个值。有关支持的板列表,请参阅 :ref:`boards` 或从 ``zephyrproject`` 目录内的任何位置运行 ``west boards``。

#. 转到 zephyr 仓库:

   .. code-block:: console

      cd zephyrproject/zephyr

#. 为 ``reel_board`` 构建 blinky 示例:

   .. zephyr-app-commands::
      :zephyr-app: samples/basic/blinky
      :board: reel_board
      :goals: build

主要构建产品将在 :file:`build/zephyr` 中;:file:`build/zephyr/zephyr.elf` 是 ELF 格式的 blinky 应用二进制文件。根据您的板,可能存在其他二进制格式、反汇编和映射文件。

:zephyr_file:`samples` 文件夹中的其他示例应用记录在 :zephyr:code-sample-category:`示例 <samples>` 中。

.. note:: 如果您想为另一个板或应用重用现有构建目录,则需要将参数 ``-p=auto`` 添加到 ``west build`` 以清除先前构建的设置和工件。

通过烧录到板来运行应用
==========================================

Zephyr 支持的大多数硬件板都可以通过运行 ``west flash`` 进行烧录。这可能需要特定于板的工具安装和配置才能正常工作。

有关其他详细信息,请参阅 :ref:`application_run` 和 :ref:`boards` 中您特定板的文档。

.. _setting-udev-rules:

设置 udev 规则
===================

烧录板需要直接访问板硬件的权限,通常由烧录工具的安装管理。在 Linux 系统上,如果 ``west flash`` 命令失败,您可能需要定义 udev 规则以授予所需的访问权限。

Udev 是 Linux 内核的设备管理器,udev 守护进程处理从系统添加(或删除)硬件设备时引发的所有用户空间事件。我们可以添加规则文件,以向非 root 用户授予对某些 USB 连接设备的访问权限。

OpenOCD(片上调试器)项目方便地提供了一个规则文件,为大多数 Zephyr 支持的基于 arm 的板定义了特定于板的规则,因此我们建议通过从其 sourceforge 仓库下载此规则文件来安装它,或者如果您已安装 Zephyr SDK,则 SDK 文件夹中有此规则文件的副本:

* 下载 OpenOCD 规则文件并将其复制到正确位置::

     wget -O 60-openocd.rules https://sf.net/p/openocd/code/ci/master/tree/contrib/60-openocd.rules?format=raw
     sudo cp 60-openocd.rules /etc/udev/rules.d

* 或从 Zephyr SDK 文件夹复制规则文件::

     sudo cp ${ZEPHYR_SDK_INSTALL_DIR}/sysroots/x86_64-pokysdk-linux/usr/share/openocd/contrib/60-openocd.rules /etc/udev/rules.d

然后,在任一情况下,要求 udev 守护进程重新加载这些规则::

   sudo udevadm control --reload

拔下并重新插入板的 USB 连接,您应该有权访问板硬件进行烧录。如果需要,请查看您的特定于板的文档(:ref:`boards`)以获取更多信息。

在 QEMU 中运行应用
===========================

在 Linux 和 macOS 上,当针对 x86 或 ARM Cortex-M3 架构时,您可以使用 `QEMU <https://www.qemu.org/>`_ 通过在主机系统上仿真来运行 Zephyr 应用。(QEMU 包含在 Zephyr SDK 安装中。)

在 Windows 上,您需要从 `下载 QEMU <https://www.qemu.org/download/#windows>`_ 手动安装 QEMU。安装后,将 QEMU 安装文件夹的路径添加到 PATH 环境变量。要在 Windows 上的测试运行器(Twister)中启用 QEMU,:ref:`设置环境变量 <env_vars>` ``QEMU_BIN_PATH`` 为 QEMU 安装文件夹的路径。

例如,您可以使用 x86 仿真板配置(``qemu_x86``)构建和运行 :zephyr:code-sample:`hello_world` 示例,使用:

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :host-os: unix
   :board: qemu_x86
   :goals: build run

要退出 QEMU,请键入 :kbd:`Ctrl-a`,然后键入 :kbd:`x`。

使用 ``qemu_cortex_m3`` 来针对仿真的 Arm Cortex-M3 示例。

.. _gs_native:

本地运行示例应用(Linux)
=========================================

您可以编译一些示例以在 Linux 上作为主机程序运行。有关更多信息,请参阅 :zephyr:board:`native_sim`。在 64 位主机操作系统上,您需要安装 32 位 C 库,或构建针对 :ref:`native_sim/native/64<native_sim32_64>` 的目标。

首先,为 ``native_sim`` 构建 Hello World。

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :host-os: unix
   :board: native_sim
   :goals: build

接下来,运行应用。

.. code-block:: console

   west build -t run
   # 或直接运行 zephyr.exe:
   ./build/zephyr/zephyr.exe

按 :kbd:`Ctrl-C` 退出。

您可以运行 ``./build/zephyr/zephyr.exe --help`` 以获取可用选项列表。

可以使用标准工具(如 gdb 或 valgrind)检测此可执行文件。

.. rubric:: 脚注

.. [#pip]

   pip 是 Python 的包安装程序。其 ``install`` 命令首先尝试重用计算机上已安装的包和包依赖项。如果这不可能,``pip install`` 会从 Internet 上的 Python 包索引(PyPI)下载它们。

   Zephyr 的 :file:`requirements.txt` 文件请求的包版本可能与系统上的其他要求冲突,在这种情况下,您可能希望为 Zephyr 开发设置 virtualenv。

.. [#board_misnomer]

   随着时间的推移,这已成为某种用词不当。虽然目标可以是(而且通常是)在其自己专用硬件板上运行的微处理器,但 Zephyr 还支持使用 QEMU 在仿真中运行为其他架构构建的目标,生成使用 POSIX API 实现 Zephyr 驱动程序接口的本地主机系统二进制文件的目标,甚至在同一物理芯片上的不同架构的 CPU 核心上运行不同的基于 Zephyr 的二进制文件。这些硬件配置中的每一个都称为"板",即使这在上下文中并不总是完全有意义。

.. _关于 -\\-user 的信息:
 https://packaging.python.org/tutorials/installing-packages/#installing-to-the-user-site
.. _Homebrew 禁用 -\\-user:
 https://docs.brew.sh/Homebrew-and-Python#note-on-pip-install---user
.. _安装包:
 https://packaging.python.org/tutorials/installing-packages/
