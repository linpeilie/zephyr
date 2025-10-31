.. _beyond-gsg:

入门指南之外
===========

本文档展示了如何使用更高级的 Zephyr 开发功能。

Python 和 pip
=============

.. tip::

   如果你在 macOS 上使用 Homebrew 安装的 Python，请查看
   `Homebrew 禁用了 --user <Homebrew disables -\\-user_>`_ 。

在整个本文档中，各个小节都参考了 Python 3 和 pip。Zephyr 项目有
:file:`requirements.txt` 文件。我们强烈建议设置一个 virtualenv
来处理 Python 依赖关系。

要使用 ``pip`` 安装 :file:`requirements.txt` 中列出的依赖项，并将
软件包安装到你的用户站点（而不是系统范围内），请运行::

   pip install --user -r requirements.txt

.. [#pip]

   pip 是 Python 的包安装程序。其 ``install`` 命令首先尝试重用已在
   你的计算机上安装的软件包和软件包依赖项。如果这是不可能的，``pip install``
   会从互联网上的 Python 软件包索引（PyPI）下载它们。

   Zephyr 的 :file:`requirements.txt` 所请求的软件包版本可能与系统上的其他
   要求冲突，在这种情况下，你可能希望为 Zephyr 开发设置一个 virtualenv。

.. _information on -\\-user:
 https://packaging.python.org/tutorials/installing-packages/#installing-to-the-user-site
.. _Homebrew disables -\\-user:
 https://docs.brew.sh/Homebrew-and-Python#note-on-pip-install---user

高级平台设置
***********

这一部分提供了在你的操作系统上设置 Zephyr 开发环境的替代说明，
用于有特定需求的开发人员。

Linux
-----

如果你想在 Linux 系统上手动设置 Zephyr 开发环境，而不使用 SDK，
请遵循这些步骤。

macOS
-----

如果你想在 macOS 系统上手动设置 Zephyr 开发环境，请遵循这些步骤。

Windows
-------

如果你想在 Windows 系统上手动设置 Zephyr 开发环境，请遵循这些步骤。

安装 Toolchain
==============

Zephyr 需要一个 toolchain 来编译应用程序。工作流程是：

#. 从 :ref:`gs_prerequisites` 安装 toolchain
#. :ref:`gs_toolchain_setup` 所需工具

安装 SDK Toolchain
------------------

:ref:`gs_installing_zephyr_sdk` 提供了如何安装 Zephyr SDK 的说明。

更新 SDK Toolchain
------------------

要更新现有的 Zephyr SDK 安装，请遵循这些步骤：

#. 下载最新的 Zephyr SDK 安装程序
#. 运行安装程序并遵循步骤

检查安装
--------

要验证 toolchain 是否已正确安装，请检查以下内容：

#. ZEPHYR_SDK_INSTALL_DIR 环境变量设置正确
#. Zephyr SDK 的 bin 目录在 PATH 中

克隆 Zephyr 存储库
==================

在 ``~/zephyrproject`` 目录中克隆 Zephyr 存储库：

.. code-block:: console

   cd ~
   mkdir zephyrproject
   cd zephyrproject

现在使用 ``west init`` 和 ``west update`` 来初始化和更新工作区：

.. code-block:: console

   west init -m https://github.com/zephyrproject-rtos/zephyr.git
   west update

或者直接克隆 Zephyr：

.. code-block:: console

   git clone https://github.com/zephyrproject-rtos/zephyr.git

保持 Zephyr 更新
================

保持 Zephyr 实例最新版本有几种方法。

使用 Git 和 West 保持更新
-------------------------

要从主存储库获取最新更新，请运行：

.. code-block:: console

   west update

如果你直接克隆了 Zephyr（不使用 west），请使用标准的 Git 命令：

.. code-block:: console

   git pull

CMake 包导出
============

Zephyr 的 CMake 包导出允许你在你的 CMakeLists.txt 中导入 Zephyr。

Board 别名
==========

Zephyr 支持为 board 定义别名。别名允许你为 board 提供一个简短的名称，
用于 ``west build`` 等命令中。

例如，如果你经常为 ``reel_board`` 构建，你可以设置一个别名 ``rb``，
然后运行::

   west build -b rb

Board 别名在 :file:`board_aliases.txt` 中定义（如果存在）。

构建、烧写和运行应用程序
======================

构建应用程序
-----------

要为 ``reel_board`` 构建 blinky 示例：

#. 进入 zephyr 存储库：

   .. code-block:: console

      cd zephyrproject/zephyr

#. 为 ``reel_board`` 构建 blinky 示例：

   .. zephyr-app-commands::
      :zephyr-app: samples/basic/blinky
      :board: reel_board
      :goals: build

主要的构建产品位于 :file:`build/zephyr`；:file:`build/zephyr/zephyr.elf`
是 ELF 格式的 blinky 应用程序二进制文件。根据你的 board，可能会出现其他二进制格式、
反汇编和映射文件。

:zephyr_file:`samples` 文件夹中的其他示例应用程序在
:zephyr:code-sample-category:`samples` 中有文档记录。

.. note:: 如果你想为另一个 board 或应用程序重新使用现有的构建目录，
   你需要向 ``west build`` 添加参数 ``-p=auto`` 以清除来自
   先前构建的设置和工件。

通过烧写到 Board 来运行应用程序
==============================

大多数由 Zephyr 支持的硬件 board 可以通过运行 ``west flash`` 来烧写。
这可能需要特定于 board 的工具安装和配置才能正常工作。

有关更多详细信息，请参阅 :ref:`application_run` 和你的特定 board
在 :ref:`boards` 中的文档。

.. _setting-udev-rules:

设置 udev 规则
=============

烧写 board 需要有权直接访问 board 硬件，通常由烧写工具的安装来管理。
在 Linux 系统上，如果 ``west flash`` 命令失败，你可能需要定义 udev 规则
来授予所需的访问权限。

udev 是 Linux 内核的设备管理器，udev 守护程序处理当硬件设备被添加（或移除）
到系统时引发的所有用户空间事件。我们可以添加一个规则文件来授予非 root 用户
对某些 USB 连接设备的访问权限。

OpenOCD（On-Chip Debugger）项目方便地提供了一个规则文件，该文件为大多数
Zephyr 支持的基于 ARM 的 board 定义了特定于 board 的规则。我们建议通过从
他们的 sourceforge 仓库下载或者如果你已经安装了 Zephyr SDK，这个规则文件
的副本位于 SDK 文件夹中来安装这个规则文件：

* 要么下载 OpenOCD 规则文件并将其复制到正确的位置::

     wget -O 60-openocd.rules https://sf.net/p/openocd/code/ci/master/tree/contrib/60-openocd.rules?format=raw
     sudo cp 60-openocd.rules /etc/udev/rules.d

* 或者从 Zephyr SDK 文件夹复制规则文件::

     sudo cp ${ZEPHYR_SDK_INSTALL_DIR}/sysroots/x86_64-pokysdk-linux/usr/share/openocd/contrib/60-openocd.rules /etc/udev/rules.d

然后，在任何一种情况下，要求 udev 守护程序重新加载这些规则::

   sudo udevadm control --reload

断开并重新插入你的 board 的 USB 连接，你应该有权访问 board 硬件进行烧写。
如果需要，请查阅你的 board 特定文档（:ref:`boards`）获取更多信息。

在 QEMU 中运行应用程序
====================

在 Linux 和 macOS 上，当针对 x86 或 ARM Cortex-M3 架构时，
你可以使用 `QEMU <https://www.qemu.org/>`_ 在你的主机系统上通过模拟运行 Zephyr 应用程序。
（QEMU 包含在 Zephyr SDK 安装中。）

在 Windows 上，你需要从 `Download QEMU <https://www.qemu.org/download/#windows>`_
手动安装 QEMU。安装后，将 QEMU 安装文件夹的路径添加到 PATH 环境变量。
要在 Windows 上的 Test Runner（Twister）中启用 QEMU，
:ref:`设置环境变量 <env_vars>` ``QEMU_BIN_PATH`` 为 QEMU 安装文件夹的路径。

例如，你可以使用 x86 模拟 board 配置（``qemu_x86``）来构建和运行
:zephyr:code-sample:`hello_world` 示例：

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :host-os: unix
   :board: qemu_x86
   :goals: build run

要退出 QEMU，请按 :kbd:`Ctrl-a`，然后按 :kbd:`x`。

使用 ``qemu_cortex_m3`` 来针对模拟的 Arm Cortex-M3 示例。

.. _gs_native:

以本机方式运行示例应用程序（Linux）
==================================

你可以编译一些示例作为主机程序在 Linux 上运行。
有关更多信息，请参阅 :zephyr:board:`native_sim`。
在 64 位主机操作系统上，你需要安装一个 32 位 C 库，
或者针对 :ref:`native_sim/native/64<native_sim32_64>` 构建。

首先，为 ``native_sim`` 构建 Hello World。

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :host-os: unix
   :board: native_sim
   :goals: build

接下来，运行应用程序。

.. code-block:: console

   west build -t run
   # 或者直接运行 zephyr.exe：
   ./build/zephyr/zephyr.exe

按 :kbd:`Ctrl-C` 退出。

你可以运行 ``./build/zephyr/zephyr.exe --help`` 来获取可用选项的列表。

这个可执行文件可以使用标准工具（如 gdb 或 valgrind）进行检测。

.. rubric:: 脚注

.. [#board_misnomer]

   随着时间的推移，这已经在某种程度上成为一个用词不当。虽然目标可以是，
   而且通常是，运行在自己的专用硬件 board 上的微处理器，但 Zephyr 还支持
   使用 QEMU 在模拟中运行为其他架构构建的目标、生成实现 Zephyr 驱动程序
   接口的本机主机系统二进制文件和 POSIX API 的目标，甚至在同一物理芯片上
   不同架构的 CPU 核心上运行不同的基于 Zephyr 的二进制文件。每个这些硬件
   配置都被称为"board"，即使在上下文中这并不总是完全有意义的。

.. _Installing Packages:
 https://packaging.python.org/tutorials/installing-packages/
