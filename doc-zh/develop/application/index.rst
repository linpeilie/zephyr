.. _application:

应用开发
#######################

.. note::

   在本文档中,我们将假设:

   - 您的 **应用目录** :file:`<app>` 类似于 :file:`<home>/zephyrproject/app`
   - 它的 **构建目录** 是 :file:`<app>/build`

   这些术语定义如下。在 Linux/macOS 上,<home> 等同于 ``~``。在 Windows 上,它是 ``%userprofile%``。

   将应用保存在工作区 (:file:`<home>/zephyrproject`) 内使得使用 ``west build`` 和其他命令更容易。(只要 :ref:`ZEPHYR_BASE <important-build-vars>` 设置得当,您可以将应用放在任何地方。)

概述
********

Zephyr 的构建系统基于 `CMake`_。

构建系统以应用为中心,需要基于 Zephyr 的应用来启动构建 Zephyr 源代码。应用构建控制应用和 Zephyr 本身的配置和构建过程,将它们编译成单个二进制文件。

主 zephyr 仓库包含 Zephyr 的源代码、配置文件和构建系统。您可能还在 zephyr 仓库旁边安装了各种 :ref:`模块 <modules>`,它们提供第三方源代码集成。

**应用目录** 中的文件将 Zephyr 和任何模块与应用链接起来。此目录包含所有特定于应用的文件,例如特定于应用的配置文件和源代码。

以下是简单 Zephyr 应用中的文件:

.. code-block:: none

   <app>
   ├── CMakeLists.txt
   ├── app.overlay
   ├── prj.conf
   ├── VERSION
   └── src
       └── main.c

这些内容是:

* **CMakeLists.txt**: 此文件告诉构建系统在哪里找到其他应用文件,并将应用目录与 Zephyr 的 CMake 构建系统链接。此链接提供 Zephyr 构建系统支持的功能,例如特定于板的配置文件、在真实或仿真硬件上运行和调试编译后的二进制文件的能力等。

* **app.overlay**: 这是一个设备树覆盖文件,指定应用特定的更改,这些更改应应用于您为其构建的任何板的基本设备树。设备树覆盖的目的通常是配置应用使用的硬件。

  构建系统默认查找 :file:`app.overlay`,但您可以添加更多设备树覆盖,也会搜索其他默认文件。

  有关设备树的更多信息,请参阅 :ref:`devicetree`。

* **prj.conf**: 这是一个 Kconfig 片段,为一个或多个 Kconfig 选项指定特定于应用的值。这些应用设置与其他设置合并以生成最终配置。Kconfig 片段的目的通常是配置应用使用的软件功能。

  构建系统默认查找 :file:`prj.conf`,但您可以添加更多 Kconfig 片段,也会搜索其他默认文件。

  有关更多信息,请参阅下面的 :ref:`application-kconfig`。

* **VERSION**: 包含多个版本信息字段的文本文件。这些字段让您管理应用的生命周期,并在签署应用映像时自动提供应用版本。

  有关此文件及其使用方法的更多信息,请参阅 :ref:`app-version-details`。

* **main.c**: 源代码文件。应用通常包含用 C、C++ 或汇编语言编写的源文件。Zephyr 的约定是将它们放在 :file:`<app>` 的名为 :file:`src` 的子目录中。

一旦定义了应用,您将使用 CMake 生成 **构建目录**,其中包含构建应用和 Zephyr 所需的文件,然后将它们链接在一起成为可以在板上运行的最终二进制文件。最简单的方法是使用 :ref:`west build <west-building>`,但您也可以直接使用 CMake。应用构建工件始终在单独的构建目录中生成:Zephyr 不支持"树内"构建。

以下部分描述如何创建、构建和运行 Zephyr 应用,然后是更详细的参考资料。

.. _zephyr-app-types:

应用类型
*****************

我们根据 :file:`<app>` 的位置区分三种基本类型的 Zephyr 应用:

.. table::

   +------------------------------+--------------------------------+
   | 应用类型                     | :file:`<app>` 位置             |
   +------------------------------+--------------------------------+
   | :ref:`仓库                   | zephyr 仓库                    |
   | <zephyr-repo-app>`           |                                |
   +------------------------------+--------------------------------+
   | :ref:`工作区                 | 安装 Zephyr 的 west 工作区     |
   | <zephyr-workspace-app>`      |                                |
   +------------------------------+--------------------------------+
   | :ref:`独立                   | 其他位置                       |
   | <zephyr-freestanding-app>`   |                                |
   +------------------------------+--------------------------------+

我们将在下面更详细地讨论这些。要了解构建系统如何支持每种类型,请参阅 :ref:`cmake_pkg`。

.. _zephyr-repo-app:

Zephyr 仓库应用
=============================

位于 Zephyr :ref:`west 工作区 <west-workspaces>` 中 ``zephyr`` 源代码仓库内的应用称为 Zephyr 仓库应用。在以下示例中,:zephyr:code-sample:`hello_world 示例 <hello_world>` 是 Zephyr 仓库应用:

.. code-block:: none

   zephyrproject/
   ├─── .west/
   │    └─── config
   └─── zephyr/
        ├── arch/
        ├── boards/
        ├── cmake/
        ├── samples/
        │    ├── hello_world/
        │    └── ...
        ├── tests/
        └── ...

.. _zephyr-workspace-app:

Zephyr 工作区应用
============================

位于 :ref:`工作区 <west-workspaces>` 内但在 zephyr 仓库本身之外的应用称为 Zephyr 工作区应用。在以下示例中,``app`` 是 Zephyr 工作区应用:

.. code-block:: none

   zephyrproject/
   ├─── .west/
   │    └─── config
   ├─── zephyr/
   ├─── bootloader/
   ├─── modules/
   ├─── tools/
   ├─── <vendor/private-repositories>/
   └─── applications/
        └── app/

.. _zephyr-freestanding-app:

Zephyr 独立应用
===============================

位于 Zephyr :ref:`工作区 <west-workspaces>` 外部的 Zephyr 应用称为 Zephyr 独立应用。在以下示例中,``app`` 是 Zephyr 独立应用:

.. code-block:: none

   <home>/
   ├─── zephyrproject/
   │     ├─── .west/
   │     │    └─── config
   │     ├── zephyr/
   │     ├── bootloader/
   │     ├── modules/
   │     └── ...
   │
   └─── app/
        ├── CMakeLists.txt
        ├── prj.conf
        └── src/
            └── main.c

.. _zephyr-creating-app:

创建应用
***********************

在 Zephyr 中,您可以使用参考工作区应用或手动创建应用。

.. _zephyr-creating-app-from-example:

使用参考工作区应用
=======================================

`example-application`_ Git 仓库包含一个参考 :ref:`工作区应用 <zephyr-workspace-app>`。建议在创建您自己的应用时使用它作为参考,如以下部分所述。

example-application 仓库演示了如何使用几个常用功能,例如:

- 自定义 :ref:`板移植 <board_porting_guide>`
- 自定义 :ref:`设备树绑定 <dt-bindings>`
- 自定义 :ref:`设备驱动程序 <device_model_api>`
- 持续集成 (CI) 设置,包括使用 :ref:`twister <twister_script>`
- 自定义 west :ref:`扩展命令 <west-extensions>`

基本 example-application 用法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在现有 Zephyr 工作区内开始使用 example-application 仓库的最简单方法是遵循以下步骤:

.. code-block:: console

   cd <home>/zephyrproject
   git clone https://github.com/zephyrproject-rtos/example-application my-app

上面的目录名 :file:`my-app` 是任意的:根据需要更改它。您现在可以进入此目录并根据需要调整其内容。由于您使用的是现有的 Zephyr 工作区,因此可以使用 ``west build`` 或任何其他 west 命令来构建、烧录和调试。

高级 example-application 用法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

您还可以使用 example-application 仓库作为构建您自己的定制基于 Zephyr 的软件发行版的起点。这让您可以做以下事情:

- 删除您不需要的 Zephyr 模块
- 添加您自己的其他自定义仓库
- 用您自己的版本覆盖 Zephyr 提供的仓库
- 与其他人共享结果并进一步协作

example-application 仓库包含一个 :file:`west.yml` 文件,因此也是一个 west :ref:`清单仓库 <west-workspace>`。使用它通过以下步骤创建一个新的定制工作区:

.. code-block:: console

   cd <home>
   mkdir my-workspace
   cd my-workspace
   git clone https://github.com/zephyrproject-rtos/example-application my-manifest-repo
   west init -l my-manifest-repo

这将创建一个具有 :ref:`T2 拓扑 <west-t2>` 的新工作区,其中 :file:`my-manifest-repo` 作为清单仓库。:file:`my-workspace` 和 :file:`my-manifest-repo` 名称是任意的:根据需要更改它们。

接下来,自定义清单仓库。克隆时,此仓库的初始内容将与 example-application 的内容匹配。然后,您可以根据需要编辑 :file:`my-manifest-repo/west.yml`,更改其中的仓库集。有关如何根据需要从工作区添加或删除不同仓库的许多示例,请参阅 :ref:`west-manifest-import`。对其他文件进行任何其他必要的更改。

当您满意时,可以运行:

.. code-block::

   west update

您的工作区将准备就绪可供使用。

如果您将生成的 :file:`my-manifest-repo` 仓库推送到其他地方,您可以与其他人共享您的工作。例如,假设您将仓库推送到 ``https://git.example.com/my-manifest-repo``。其他人可以通过运行以下命令来设置匹配的工作区:

.. code-block::

   west init -m https://git.example.com/my-manifest-repo my-workspace
   cd my-workspace
   west update

从现在开始,您可以通过将更改推送到您正在使用的仓库并根据需要更新 :file:`my-manifest-repo/west.yml` 来添加和删除仓库或更改其内容,从而在共享软件上进行协作。

.. _zephyr-creating-app-by-hand:

手动创建应用
===============================

您可以按照以下步骤从头开始创建基本应用目录。但是,使用 `example-application`_ 仓库或 Zephyr 的 :zephyr:code-sample-category:`示例 <samples>` 之一作为起点可能会更容易。

#. 创建应用目录。

   例如,在 Unix shell 或 Windows ``cmd.exe`` 提示符中:

   .. code-block:: console

      mkdir app

   .. warning::

      不支持在路径中任何位置包含空格的目录中构建 Zephyr 或创建应用。因此 Windows 路径 :file:`C:\\Users\\YourName\\app` 可以工作,但 :file:`C:\\Users\\Your Name\\app` 不行。

#. 创建源代码文件。

   建议将所有应用源代码放在名为 :file:`src` 的子目录中。这使得更容易区分项目文件和源代码。

   继续前面的示例,输入:

   .. code-block:: console

      cd app
      mkdir src

#. 将应用源代码放在 :file:`src` 子目录中。对于本示例,我们假设您创建了一个名为 :file:`src/main.c` 的文件。

#. 在 ``app`` 目录中创建一个名为 :file:`CMakeLists.txt` 的文件,内容如下:

   .. code-block:: cmake

      cmake_minimum_required(VERSION 3.20.0)

      find_package(Zephyr)
      project(my_zephyr_app)

      target_sources(app PRIVATE src/main.c)

   注意:

   - CMake 需要 ``cmake_minimum_required()`` 调用。它也会在下一行由 Zephyr 包调用。如果其版本比您的 :file:`CMakeLists.txt` 中的版本或 Zephyr 包中的版本号旧,CMake 将出错。

   - ``find_package(Zephyr)`` 引入 Zephyr 构建系统,它创建一个名为 ``app`` 的 CMake 目标(请参阅 :ref:`cmake_pkg`)。将源添加到此目标是在构建中包含它们的方式。Zephyr 包将定义 ``Zephyr-Kernel`` 作为 CMake 项目,并启用对 ``C``、``CXX``、``ASM`` 语言的支持。

   - ``project(my_zephyr_app)`` 定义您的应用的 CMake 项目。这必须在 ``find_package(Zephyr)`` 之后调用,以避免干扰 Zephyr 的 ``project(Zephyr-Kernel)``。

   - ``target_sources(app PRIVATE src/main.c)`` 是将源文件添加到 ``app`` 目标。这必须在定义目标的 ``find_package(Zephyr)`` 之后。您可以使用 ``target_sources()`` 添加任意数量的文件。

#. 为您的应用创建至少一个 Kconfig 片段(通常名为 :file:`prj.conf`)并在那里设置应用需要的 Kconfig 选项值。请参阅 :ref:`application-kconfig`。如果不需要设置 Kconfig 选项,则创建一个空文件。

#. 配置应用所需的任何设备树覆盖,通常在名为 :file:`app.overlay` 的文件中。请参阅 :ref:`set-devicetree-overlays`。

#. 设置您可能需要的任何其他文件,例如 :ref:`twister <twister_script>` 配置文件、持续集成文件、文档等。

.. _important-build-vars:

重要的构建系统变量
********************************

您可以使用许多变量来控制 Zephyr 构建系统。本节描述每个 Zephyr 开发人员都应该了解的最重要的变量。

.. note::

   变量 :makevar:`BOARD`、:makevar:`CONF_FILE` 和 :makevar:`DTC_OVERLAY_FILE` 可以通过 3 种方式提供给构建系统(按优先级顺序):

   * 作为 ``west build`` 或 ``cmake`` 调用的参数,通过 ``-D`` 命令行开关。如果您有多个覆盖文件,应使用引号,``"file1.overlay;file2.overlay"``
   * 作为 :ref:`环境变量 <env_vars>`。
   * 作为 :file:`CMakeLists.txt` 中的 ``set(<VARIABLE> <VALUE>)`` 语句

* :makevar:`ZEPHYR_BASE`: 构建系统使用的 Zephyr 基本变量。``find_package(Zephyr)`` 将自动将其设置为缓存的 CMake 变量。但 ``ZEPHYR_BASE`` 也可以设置为环境变量,以强制 CMake 使用特定的 Zephyr 安装。

* :makevar:`BOARD`: 选择应用构建将用于默认配置的板。有关内置板,请参阅 :ref:`boards`,有关添加板支持的信息,请参阅 :ref:`board_porting_guide`。

* :makevar:`CONF_FILE`: 指示一个或多个 Kconfig 配置片段文件的名称。多个文件名可以用空格或分号分隔。每个文件都包含覆盖默认配置值的 Kconfig 配置值。

  有关更多信息,请参阅 :ref:`initial-conf`。

* :makevar:`EXTRA_CONF_FILE`: 附加的 Kconfig 配置片段文件。多个文件名可以用空格或分号分隔。这可用于将 :makevar:`CONF_FILE` 保留为其默认值,但"混入"一些附加配置选项。

* :makevar:`DTC_OVERLAY_FILE`: 要使用的一个或多个设备树覆盖文件。多个文件可以用分号分隔。有关示例,请参阅 :ref:`set-devicetree-overlays`,有关设备树和 Zephyr 的信息,请参阅 :ref:`devicetree-intro`。

* :makevar:`EXTRA_DTC_OVERLAY_FILE`: 要使用的附加设备树覆盖文件。多个文件可以用分号分隔。这可用于将 :makevar:`DTC_OVERLAY_FILE` 保留为其默认值,但"混入"一些附加覆盖文件。

* :makevar:`SHIELD`: 请参阅 :ref:`shields`

* :makevar:`ZEPHYR_MODULES`: 一个 `CMake 列表`_,包含应在应用构建中使用的源代码、Kconfig 等的附加目录的绝对路径。有关详细信息,请参阅 :ref:`modules`。如果设置此变量,它必须是要使用的所有模块的完整列表,因为构建系统不会自动从 west 获取任何模块。

* :makevar:`EXTRA_ZEPHYR_MODULES`: 类似于 :makevar:`ZEPHYR_MODULES`,但这些将添加到通过 west 找到的模块列表中,而不是替换它。

* :makevar:`FILE_SUFFIX`: 文件名的可选后缀,将添加到 Kconfig 片段和设备树覆盖(如果这些文件存在,否则将回退到没有前缀的名称)。有关详细信息,请参阅 :ref:`application-file-suffixes`。

.. note::

   您可以使用 :ref:`cmake_build_config_package` 来共享这些变量的常用设置。

.. _zephyr-app-cmakelists:

应用 CMakeLists.txt
**************************

每个应用都必须有一个 :file:`CMakeLists.txt` 文件。此文件是构建系统的入口点或顶层。最终的 :file:`zephyr.elf` 映像包含应用和内核库。

本节描述您可以在 :file:`CMakeLists.txt` 中执行的一些操作。确保按顺序执行这些步骤。

#. 如果您只想为一个板构建,请在新行上添加应用的板配置名称。例如:

   .. code-block:: cmake

      set(BOARD qemu_x86)

   有关可用板的更多信息,请参阅 :ref:`boards`。

   Zephyr 构建系统通过按顺序检查以下内容来确定 :makevar:`BOARD` 的值(当找到 BOARD 值时,CMake 停止进一步查找列表):

   - 由 CMake 缓存确定的任何先前使用的值具有最高优先级。这确保您不会尝试使用与构建配置步骤中设置的 :makevar:`BOARD` 值不同的值运行构建。

   - 接下来将检查并使用 CMake 命令行上给出的任何值(直接或通过 ``west build`` 间接),使用 ``-DBOARD=YOUR_BOARD``。

   - 如果设置了 :ref:`环境变量 <env_vars>` ``BOARD``,则将使用其值。

   - 最后,如果您在应用 :file:`CMakeLists.txt` 中设置 ``BOARD`` 如本步骤所述,将使用此值。

#. 如果您的应用使用除通常的 :file:`prj.conf` 之外的配置文件,请添加适当设置 :makevar:`CONF_FILE` 变量到这些文件的行。如果给出多个文件名,请用单个空格或分号分隔它们。当您想要以模块化方式构建配置片段文件时,可以使用 CMake 列表,以避免在单个地方设置 :makevar:`CONF_FILE`。例如:

   .. code-block:: cmake

     set(CONF_FILE "fragment_file1.conf")
     list(APPEND CONF_FILE "fragment_file2.conf")

   有关更多信息,请参阅 :ref:`initial-conf`。

#. 如果您的应用使用设备树覆盖,您可能需要设置 :ref:`DTC_OVERLAY_FILE <important-build-vars>`。请参阅 :ref:`set-devicetree-overlays`。

#. 如果您的应用有自己的内核配置选项,请在与应用的 :file:`CMakeLists.txt` 相同的目录中创建一个 :file:`Kconfig` 文件。

   有关详细的 Kconfig 文档,请参阅 :ref:`手册的 Kconfig 部分 <kconfig>`。

   一个(不太可能的)高级用例是,如果您的应用有自己独特的配置 **选项**,根据构建配置的不同而设置不同。

   如果您只想为现有的 Zephyr 配置选项设置特定于应用的 **值**,请参阅上面的 :makevar:`CONF_FILE` 描述。

   像这样构建您的 :file:`Kconfig` 文件:

   .. literalinclude:: application-kconfig.include
      :language: kconfig

   .. note::

      ``source`` 语句中的环境变量直接展开,因此您不需要定义 ``option env="ZEPHYR_BASE"`` Kconfig "弹跳"符号。如果使用这样的符号,它必须与环境变量具有相同的名称。

      有关更多信息,请参阅 :ref:`kconfig_extensions`。

   当放置在应用目录中时,:file:`Kconfig` 文件会自动检测到,但如果设置了 CMake 变量 :makevar:`KCONFIG_ROOT` 的绝对路径,也可以在其他地方找到它。

#. 在新行上指定应用需要 Zephyr,**在从上述步骤添加的任何行之后**:

   .. code-block:: cmake

      find_package(Zephyr)
      project(my_zephyr_app)

   .. note:: 如果应该支持通过显式设置 ``ZEPHYR_BASE`` 环境变量来强制使用特定的 Zephyr 安装,则可以使用 ``find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})``。Zephyr 中的所有示例都支持 ``ZEPHYR_BASE`` 环境变量。

#. 现在将任何应用源文件添加到 'app' 目标库中,每个文件都单独一行,如下所示:

   .. code-block:: cmake

      target_sources(app PRIVATE src/main.c)

下面是一个简单的 :file:`CMakeList.txt` 示例:

.. code-block:: cmake

   set(BOARD qemu_x86)

   find_package(Zephyr)
   project(my_zephyr_app)

   target_sources(app PRIVATE src/main.c)

Cmake 属性 ``HEX_FILES_TO_MERGE`` 利用 Kconfig 和 CMake 提供的应用配置,让您将外部构建的十六进制文件与构建 Zephyr 应用时生成的十六进制文件合并。例如:

.. code-block:: cmake

  set_property(GLOBAL APPEND PROPERTY HEX_FILES_TO_MERGE
      ${app_bootloader_hex}
      ${PROJECT_BINARY_DIR}/${KERNEL_HEX_NAME}
      ${app_provision_hex})

.. _zephyr-app-cmakecache:

CMakeCache.txt
**************

CMake 使用 CMakeCache.txt 文件作为持久键/值字符串存储,用于在运行之间缓存值,包括编译和构建选项以及库依赖项的路径。当 CMake 在空构建文件夹中运行时创建此缓存文件。

有关 CMakeCache.txt 文件的更多详细信息,请参阅官方 `CMake Cache`_ 文档。

.. _CMake Cache: https://cmake.org/cmake/help/book/mastering-cmake/chapter/CMake%20Cache.html


应用配置
*************************

.. _application-configuration-directory:

应用配置目录
===================================

Zephyr 将使用应用配置目录中的配置文件,但参数提供的绝对路径文件除外,例如 ``CONF_FILE``、``EXTRA_CONF_FILE``、``DTC_OVERLAY_FILE`` 和 ``EXTRA_DTC_OVERLAY_FILE``。

应用配置目录由 ``APPLICATION_CONFIG_DIR`` 变量定义。

``APPLICATION_CONFIG_DIR`` 将由以下来源之一设置,优先级最高的列在第一位。

1. 如果用户使用 ``-DAPPLICATION_CONFIG_DIR=<path>`` 或在 ``find_package(Zephyr)`` 之前的 CMake 文件中指定了 ``APPLICATION_CONFIG_DIR``,则此文件夹用作应用的配置目录。

2. 应用的源目录。

.. _application-kconfig:

Kconfig 配置
=====================

应用配置选项通常在应用目录中的 :file:`prj.conf` 中设置。例如,可以通过以下赋值启用 C++ 支持:

.. code-block:: cfg

   CONFIG_CPP=y

查看 :zephyr:code-sample-category:`现有示例 <samples>` 是一个很好的入门方式。

有关设置 Kconfig 配置值的详细文档,请参阅 :ref:`setting_configuration_values`。同一页上的 :ref:`initial-conf` 部分解释了如何派生初始配置。有关配置选项的完整列表,请参阅 :ref:`kconfig-search`。有关与 Kconfig 选项相关的安全信息,请参阅 :ref:`hardening`。

:ref:`手册的 Kconfig 部分 <kconfig>` 中的其他页面也值得阅读,特别是如果您计划添加新的配置选项。

实验性功能
~~~~~~~~~~~~~~~~~~~~~

Zephyr 是一个处于持续开发中的项目,因此有些功能仍处于其开发周期的早期阶段。此类功能将在其 Kconfig 标题中标记为 ``[EXPERIMENTAL]``。

:kconfig:option:`CONFIG_WARN_EXPERIMENTAL` 设置可用于在启用任何实验性功能时在 CMake 配置时启用警告。

.. code-block:: cfg

   CONFIG_WARN_EXPERIMENTAL=y

例如,如果选项 ``CONFIG_FOO`` 是实验性的,则启用它和 :kconfig:option:`CONFIG_WARN_EXPERIMENTAL` 将在构建应用时在 CMake 配置时打印以下警告:

.. code-block:: none

   warning: Experimental symbol FOO is enabled.

设备树覆盖
===================

请参阅 :ref:`set-devicetree-overlays`。

.. _application-file-suffixes:

文件后缀
=============

Zephyr 应用可能希望有一个代码库,具有针对不同构建/产品变体的多个配置,这将需要不同的 Kconfig 选项和设备树配置。为了更好地配置这一点,Zephyr 在配置应用时提供了一个 :makevar:`FILE_SUFFIX` 选项,可以自动附加到文件名。这适用于 Kconfig 片段和板覆盖,但有一个回退,因此如果这些文件不存在,将使用没有这些后缀的文件。

给定以下示例项目布局:

.. code-block:: none

   <app>
   ├── CMakeLists.txt
   ├── prj.conf
   ├── prj_mouse.conf
   ├── boards
   │   ├── native_sim.overlay
   │   └── qemu_cortex_m3_mouse.overlay
   └── src
       └── main.c

* 如果为 ``native_sim`` 正常构建而没有定义 ``FILE_SUFFIX``,则将使用 ``prj.conf`` 和 ``boards/native_sim.overlay``。

* 如果为 ``qemu_cortex_m3`` 正常构建而没有定义 ``FILE_SUFFIX``,则将使用 ``prj.conf``,不会使用应用设备树覆盖。

* 如果为 ``native_sim`` 构建时 ``FILE_SUFFIX`` 设置为 ``mouse``,则将使用 ``prj_mouse.conf`` 和 ``boards/native_sim.overlay``(没有 ``native_sim_mouse.overlay`` 文件,因此回退到 ``native_sim.overlay``)。

* 如果为 ``qemu_cortex_m3`` 构建时 ``FILE_SUFFIX`` 设置为 ``mouse``,则将使用 ``prj_mouse.conf`` 和 ``boards/qemu_cortex_m3_mouse.overlay``。

应用特定代码
*************************

应用特定的源代码文件通常添加到应用的 :file:`src` 目录。如果应用添加了大量文件,开发人员可以将它们分组到 :file:`src` 下的子目录中,深度根据需要而定。

应用特定的源代码不应使用已被内核保留供其自己使用的符号名称前缀。有关更多信息,请参阅 `命名约定 <https://github.com/zephyrproject-rtos/zephyr/wiki/Naming-Conventions>`_。

第三方库代码
========================

可以在应用的 :file:`src` 目录之外构建库代码,但重要的是应用和库代码都针对相同的应用二进制接口 (ABI)。在大多数架构上,有控制目标 ABI 的编译器标志,因此库和应用具有某些共同的编译器标志很重要。对于粘合代码访问 Zephyr 内核头文件也可能有用。

为了更容易集成第三方组件,Zephyr 构建系统定义了 CMake 函数,使应用构建脚本能够访问 zephyr 编译器选项。这些函数在 :zephyr_file:`cmake/modules/extensions.cmake` 中记录和定义,并遵循命名约定 ``zephyr_get_<type>_<format>``。

以下变量通常需要导出到第三方构建系统。

* ``CMAKE_C_COMPILER``、``CMAKE_AR``。

* ``ARCH`` 和 ``BOARD``,以及标识 Zephyr 内核版本的几个变量。

:zephyr_file:`samples/application_development/external_lib` 是一个演示其中一些功能的示例项目。


.. _build_an_application:

构建应用
***********************

Zephyr 构建系统将应用的所有组件编译并链接到一个可以在模拟硬件或真实硬件上运行的单个应用映像中。

与任何其他基于 CMake 的系统一样,构建过程 :ref:`分两个阶段 <cmake-details>` 进行。首先,使用 ``cmake`` 命令行工具生成构建文件(也称为构建系统),同时指定生成器。此生成器确定构建系统将在第二阶段使用的本地构建工具。第二阶段运行本地构建工具以实际构建源文件并生成映像。要了解有关这些概念的更多信息,请参阅官方 CMake 文档中的 `CMake 介绍`_。

尽管 Zephyr 中的默认构建工具是 :std:ref:`west <west>`,Zephyr 的元工具,它在幕后调用 ``cmake`` 和底层构建工具(``ninja`` 或 ``make``),但如果您愿意,也可以选择直接调用 ``cmake``。在 Linux 和 macOS 上,您可以在 ``make`` 和 ``ninja`` 生成器(即构建工具)之间进行选择,而在 Windows 上,您需要使用 ``ninja``,因为此平台不支持 ``make``。为简单起见,我们将在本指南中使用 ``ninja``,如果您选择使用 ``west build`` 来构建应用,请知道它将在幕后默认使用 ``ninja``。

例如,让我们为 ``reel_board`` 构建 Hello World 示例:

.. zephyr-app-commands::
   :tool: all
   :zephyr-app: samples/hello_world
   :board: reel_board
   :goals: build

在 Linux 和 macOS 上,您还可以使用 ``make`` 而不是 ``ninja`` 进行构建:

使用 west:

- 要仅使用 ``make`` 一次,请将 ``-- -G"Unix Makefiles"`` 添加到 west build 命令行;有关示例,请参阅 :ref:`west build <west-building-generator>` 文档。
- 要从现在开始默认使用 ``make``,请运行 ``west config build.generator "Unix Makefiles"``。

直接使用 CMake:

.. zephyr-app-commands::
   :tool: cmake
   :zephyr-app: samples/hello_world
   :generator: make
   :host-os: unix
   :board: reel_board
   :goals: build


基础
======

#. 导航到应用目录 :file:`<app>`。
#. 输入以下命令为命令行参数中指定的板构建应用的 :file:`zephyr.elf` 映像:

   .. zephyr-app-commands::
      :tool: all
      :cd-into:
      :board: <board>
      :goals: build

   如果需要,您可以使用 :code:`CONF_FILE` 参数使用备用 :file:`.conf` 文件中指定的配置设置来构建应用。这些设置将覆盖应用的 :file:`.config` 文件或其默认 :file:`.conf` 文件中的设置。例如:

   .. zephyr-app-commands::
      :tool: all
      :cd-into:
      :board: <board>
      :gen-args: -DCONF_FILE=prj.alternate.conf
      :goals: build
      :compact:

   如前一节所述,您可以选择通过导出 :makevar:`BOARD` 和 :makevar:`CONF_FILE` 环境变量或使用 ``set()`` 语句在 :file:`CMakeLists.txt` 中设置它们的值来永久设置板和配置设置。此外,``west`` 允许您 :ref:`设置默认板 <west-building-config>`。

.. _build-directory-contents:

构建目录内容
========================

使用 Ninja 生成器时,构建目录如下所示:

.. code-block:: none

   <app>/build
   ├── build.ninja
   ├── CMakeCache.txt
   ├── CMakeFiles
   ├── cmake_install.cmake
   ├── rules.ninja
   └── zephyr

构建目录中最值得注意的文件是:

* :file:`build.ninja`,可以调用它来构建应用。

* 一个 :file:`zephyr` 目录,它是生成的构建系统的工作目录,大多数生成的文件都在此处创建和存储。

运行 ``ninja`` 后,以下构建输出文件将写入构建目录的 :file:`zephyr` 子目录。(这 **不是 Zephyr 基础目录**,后者包含 Zephyr 源代码等,并在上面描述。)

* :file:`.config`,其中包含用于构建应用的配置设置。

  .. note::

     每当更新配置时,:file:`.config` 的先前版本都会保存到 :file:`.config.old`。这是为了方便,因为比较旧版本和新版本可能很方便。

* 包含已编译内核和应用代码的各种对象文件(:file:`.o` 文件和 :file:`.a` 文件)。

* :file:`zephyr.elf`,其中包含最终组合的应用和内核二进制文件。还支持其他二进制输出格式,例如 :file:`.hex` 和 :file:`.bin`。

.. _application_rebuild:

重建应用
=========================

当持续测试更改时,应用开发通常最快。随着应用变得更加复杂,频繁重建应用使调试不那么痛苦。在对应用的源文件、CMakeLists.txt 文件或配置设置进行任何重大更改后,重建和测试通常是个好主意。

.. important::

    Zephyr 构建系统仅重建可能受更改影响的应用映像部分。因此,重建应用通常比第一次构建快得多。

有时构建系统不能正确重建应用,因为它未能重新编译一个或多个必要的文件。您可以通过以下过程强制构建系统从头开始重建整个应用:

#. 在主机上打开终端控制台,并导航到构建目录 :file:`<app>/build`。

#. 输入以下命令之一,具体取决于您是要直接使用 ``west`` 还是 ``cmake`` 来删除应用的生成文件,但包含应用当前配置信息的 :file:`.config` 文件除外。

   .. code-block:: console

       west build -t clean

   或

   .. code-block:: console

       ninja clean

   或者,输入以下命令之一以删除 *所有* 生成的文件,包括包含这些板类型的应用当前配置信息的 :file:`.config` 文件。

   .. code-block:: console

       west build -t pristine

   或

   .. code-block:: console

       ninja pristine

   如果使用 west,您可以利用其能力在需要时自动 :ref:`使构建文件夹保持原始状态 <west-building-config>`。

#. 按照上面 :ref:`build_an_application` 中指定的步骤正常重建应用。

.. _application_board_version:

为板修订版构建
=============================

Zephyr 构建系统支持为具有小变化的单个板指定多个硬件修订版。使用修订版允许板支持文件对板配置进行小的调整,而无需为每个修订版复制 :ref:`create-your-board-directory` 中描述的所有文件。

要为特定修订版构建,请使用 ``<board>@<revision>`` 而不是普通的 ``<board>``。例如:

.. zephyr-app-commands::
   :tool: all
   :cd-into:
   :board: <board>@<revision>
   :goals: build
   :compact:

有关是否有多个修订版以及支持哪些修订版的详细信息,请查看您的板文档。

定位板修订版时,活动修订版将在 CMake 配置时打印,如下所示:

.. code-block:: console

   -- Board: plank, Revision: 1.5.0

.. _application_run:

运行应用
******************

应用映像可以在真实板或仿真硬件上运行。

.. _application_run_board:

在板上运行
==================

Zephyr 支持的大多数板都允许您使用 ``flash`` 目标烧录编译的二进制文件,将二进制文件复制到板并运行它。按照以下说明在真实硬件上烧录和运行应用:

#. 如 :ref:`build_an_application` 中所述构建您的应用。

#. 确保您的板已连接到主机。通常,您将通过 USB 执行此操作。

#. 从构建目录 :file:`<app>/build` 运行这些控制台命令之一,以烧录编译的 Zephyr 映像并在板上运行它:

   .. code-block:: console

      west flash

   或

   .. code-block:: console

      ninja flash

Zephyr 构建系统与板支持文件集成,使用硬件特定工具将 Zephyr 二进制文件烧录到硬件,然后运行它。

每次运行 flash 命令时,您的应用都会重建并再次烧录。

如果板支持不完整,可能不支持通过 Zephyr 构建系统进行烧录。如果您收到有关烧录支持不可用的错误消息,请查阅 :ref:`您的板文档 <boards>` 以获取有关如何烧录板的其他信息。

.. note:: 在 Linux 上开发时,通常需要安装特定于板的 udev 规则以启用 USB 设备访问您的板作为非 root 用户。如果烧录失败,请查阅板文档以查看这是否必要。

.. _application_run_qemu:

在仿真器中运行
======================

Zephyr 对 QEMU 有内置的仿真器支持。它允许您在实际加载和运行到实际目标硬件之前(或代替)虚拟运行和测试应用。

查看 :ref:`beyond-GSG` 以了解 Windows 上所需的其他步骤。

按照以下说明通过 QEMU 运行应用:

#. 如 :ref:`build_an_application` 中所述,为其中一个 QEMU 板构建应用。

   例如,您可以将 ``BOARD`` 设置为:

   - ``qemu_x86`` 以模拟在基于 x86 的板上运行
   - ``qemu_cortex_m3`` 以模拟在基于 ARM Cortex M3 的板上运行

#. 从构建目录 :file:`<app>/build` 运行这些控制台命令之一,以在 QEMU 中运行 Zephyr 二进制文件:

   .. code-block:: console

      west build -t run

   或

   .. code-block:: console

      ninja run

#. 按 :kbd:`Ctrl A, X` 停止应用在 QEMU 中运行。

   应用停止运行,终端控制台提示符重新显示。

每次执行 run 命令时,您的应用都会重建并再次运行。


.. note::

   如果安装了(仅限 Linux):ref:`Zephyr SDK <toolchain_zephyr_sdk>`,``run`` 目标将默认使用 SDK 的 QEMU 二进制文件。要使用另一个版本的 QEMU,:ref:`设置环境变量 <env_vars>` ``QEMU_BIN_PATH`` 为您要使用的 QEMU 二进制文件的路径。

.. note::

   您可以通过在目标名称后附加 ``_<emulator>`` 来选择特定的仿真器,例如 ``west build -t run_qemu`` 或 ``ninja run_qemu`` 用于 QEMU。

.. _custom_board_definition:

自定义板、设备树和 SOC 定义
********************************************

如果您正在开发的板或平台尚未得到 Zephyr 的支持,您可以将板、设备树和 SOC 定义添加到应用中,而无需将它们添加到 Zephyr 树中。

支持树外板和 SOC 开发所需的结构与 Zephyr 树中维护板和 SOC 的方式类似。通过使用这种结构,在初始开发完成后,将与平台相关的工作上游到 Zephyr 树将更加容易。

使用以下结构将自定义板添加到应用或专用仓库:

.. code-block:: console

   boards/
   soc/
   CMakeLists.txt
   prj.conf
   README.rst
   src/

其中 ``boards`` 目录托管您正在构建的板:

.. code-block:: console

   .
   ├── boards
   │   └── vendor
   │       └── my_custom_board
   │           ├── doc
   │           │   └── img
   │           └── support
   └── src

``soc`` 目录托管任何 SOC 代码。您还可以拥有由 Zephyr 树中可用的 SOC 支持的板。

板
======

在 ``my_custom_board`` 的 ``boards`` 下使用供应商名称作为文件夹名称(如果提交上游到 Zephyr,必须与 :zephyr_file:`dts/bindings/vendor-prefixes.txt` 中的供应商前缀匹配,如果不是供应商板,则为 ``others``)。

文档(在 ``doc/`` 下)和支持文件(在 ``support/`` 下)是可选的,但在提交到 Zephyr 时需要。

``my_custom_board`` 的内容应遵循任何 Zephyr 板的相同指南,并提供以下文件::

    my_custom_board_defconfig
    my_custom_board.dts
    my_custom_board.yaml
    board.cmake
    board.h
    CMakeLists.txt
    doc/
    Kconfig.my_custom_board
    Kconfig.defconfig
    support/


一旦板结构到位,您可以通过使用 ``-DBOARD_ROOT`` 参数向 CMake 构建系统指定自定义板信息的位置来构建针对此板的应用:

.. zephyr-app-commands::
   :tool: all
   :board: <board name>
   :gen-args: -DBOARD_ROOT=<path to boards>
   :goals: build
   :compact:

这将使用您的自定义板配置,并将 Zephyr 二进制文件生成到您的应用目录中。

您还可以在应用 :file:`CMakeLists.txt` 文件中定义 ``BOARD_ROOT`` 变量。确保在使用 ``find_package(Zephyr ...)`` 引入 Zephyr 样板之前这样做。

.. note::

   在 CMakeLists.txt 中指定 ``BOARD_ROOT`` 时,必须提供绝对路径,例如 ``list(APPEND BOARD_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/<extra-board-root>)``。使用 ``-DBOARD_ROOT=<board-root>`` 时,可以使用绝对路径和相对路径。相对路径相对于应用目录处理。

.. note::

   使用 sysbuild 时,必须在模块或 sysbuild ``CMakeLists.txt`` 文件中定义 ``BOARD_ROOT``,有关详细信息,请参阅 :ref:`sysbuild_var_override`。

SOC 定义
===============

与板支持类似,结构与 Zephyr 树中维护 SOC 的方式类似,例如:

.. code-block:: none

        soc
        └── st
            └── stm32
                ├── common
                └── stm32l0x


文件 :zephyr_file:`soc/Kconfig` 将在 Kconfig 中创建顶级 ``SoC/CPU/Configuration Selection`` 菜单。

可以使用 ``SOC_ROOT`` CMake 变量将树外 SoC 定义添加到此菜单。此变量包含以分号分隔的包含 SoC 支持文件的目录列表。

按照上面的结构,可以添加以下文件以将更多 SoC 加载到菜单中。

.. code-block:: none

        soc
        └── st
            └── stm32
                └── stm32l0x
                    ├── Kconfig
                    ├── Kconfig.soc
                    └── Kconfig.defconfig

上面的 Kconfig 文件可能描述 SoC 或加载其他 SoC Kconfig 文件。

在此结构中加载 ``stm31l0`` 特定 Kconfig 文件的示例:

.. code-block:: none

        soc
        └── st
            └── stm32
                ├── Kconfig.soc
                └── stm32l0x
                    └── Kconfig.soc

可以使用 ``st/stm32/Kconfig.soc`` 中的以下内容完成:

.. code-block:: kconfig

   rsource "*/Kconfig.soc"

一旦 SOC 结构到位,您可以通过使用 ``-DSOC_ROOT`` 参数向 CMake 构建系统指定自定义平台信息的位置来构建针对此平台的应用:

.. zephyr-app-commands::
   :tool: all
   :board: <board name>
   :gen-args: -DSOC_ROOT=<path to soc> -DBOARD_ROOT=<path to boards>
   :goals: build
   :compact:

这将使用您的自定义平台配置,并将 Zephyr 二进制文件生成到您的应用目录中。

有关在模块的 :file:`zephyr/module.yml` 文件中设置 SOC_ROOT 的信息,请参阅 :ref:`modules_build_settings`。

或者您可以在应用 :file:`CMakeLists.txt` 文件中定义 ``SOC_ROOT`` 变量。确保在使用 ``find_package(Zephyr ...)`` 引入 Zephyr 样板之前这样做。

.. note::

   在 CMakeLists.txt 中指定 ``SOC_ROOT`` 时,必须提供绝对路径,例如 ``list(APPEND SOC_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/<extra-soc-root>``)。使用 ``-DSOC_ROOT=<soc-root>`` 时,可以使用绝对路径和相对路径。相对路径相对于应用目录处理。

.. _dts_root:

设备树定义
======================

设备树目录树在 ``APPLICATION_SOURCE_DIR``、``BOARD_DIR`` 和 ``ZEPHYR_BASE`` 中找到,但可以通过创建此目录树添加其他树或 DTS_ROOT::

    include/
    dts/common/
    dts/arm/
    dts/
    dts/bindings/

其中 'arm' 更改为适当的架构。每个目录都是可选的。绑定目录包含绑定,其他目录包含可以从 DT 源包含的文件。

一旦目录结构到位,您可以通过 ``DTS_ROOT`` CMake 缓存变量指定其位置来使用它:

.. zephyr-app-commands::
   :tool: all
   :board: <board name>
   :gen-args: -DDTS_ROOT=<path to dts root>
   :goals: build
   :compact:

您还可以在应用 :file:`CMakeLists.txt` 文件中定义变量。确保在使用 ``find_package(Zephyr ...)`` 引入 Zephyr 样板之前这样做。

.. note::

   在 CMakeLists.txt 中指定 ``DTS_ROOT`` 时,必须提供绝对路径,例如 ``list(APPEND DTS_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/<extra-dts-root>``)。使用 ``-DDTS_ROOT=<dts-root>`` 时,可以使用绝对路径和相对路径。相对路径相对于应用目录处理。

设备树源通过 C 预处理器传递,因此您可以包含可以位于 ``DTS_ROOT`` 目录中的文件。按照约定,设备树包含文件具有 ``.dtsi`` 扩展名。

您还可以使用预处理器通过 ``DTS_EXTRA_CPPFLAGS`` CMake 缓存变量指定指令来控制设备树文件的内容:

.. zephyr-app-commands::
   :tool: all
   :board: <board name>
   :gen-args: -DDTS_EXTRA_CPPFLAGS=-DTEST_ENABLE_FEATURE
   :goals: build
   :compact:

.. _CMake: https://www.cmake.org
.. _CMake 介绍: https://cmake.org/cmake/help/latest/manual/cmake.1.html#description
.. _CMake 列表: https://cmake.org/cmake/help/latest/manual/cmake-language.7.html#lists
.. _example-application: https://github.com/zephyrproject-rtos/example-application
