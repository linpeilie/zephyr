.. _env_vars:

环境变量
=====================

本文档的各个页面都提到设置 Zephyr 特定的环境变量。本页面描述如何设置。

设置变量
*****************

选项 1: 仅一次
-------------------

在当前终端窗口的生命周期内将环境变量 ``MY_VARIABLE`` 设置为 ``foo``:

.. tabs::

   .. group-tab:: Linux/macOS

      .. code-block:: console

         export MY_VARIABLE=foo

   .. group-tab:: Windows

      .. code-block:: console

         set MY_VARIABLE=foo

.. warning::

  这最适合用于实验。如果您关闭终端窗口、使用另一个终端窗口或标签页、重新启动计算机等,此设置将永久丢失。

  如果您想继续使用该设置,建议使用选项 2 或 3。

选项 2: 在所有终端中
--------------------------

.. tabs::

   .. group-tab:: Linux/macOS

      在主目录的 shell 启动脚本中添加 ``export MY_VARIABLE=foo`` 行。对于 Bash,在 Linux 上通常是 :file:`~/.bashrc`,在 macOS 上通常是 :file:`~/.bash_profile`。这些启动脚本中的更改不会影响已启动的 shell 实例;请尝试打开新的终端窗口以获取新设置。

   .. group-tab:: Windows

      您可以在 ``cmd.exe`` 中使用 ``setx`` 程序或第三方 RapidEE 程序。

      要使用 ``setx``,请键入此命令,然后关闭终端窗口。任何新的 ``cmd.exe`` 窗口都将把 ``MY_VARIABLE`` 设置为 ``foo``。

      .. code-block:: console

         setx MY_VARIABLE foo

      要安装 RapidEE(一个免费的图形化环境变量编辑器),请在管理员命令提示符中 `使用 Chocolatey`_:

      .. code-block:: console

         choco install rapidee

      然后,您可以从终端运行 ``rapidee`` 来启动程序并设置环境变量。确保使用"用户"环境变量区域 - 否则,您必须以管理员身份运行 RapidEE。还要确保在退出前单击左上角的保存按钮保存更改。您在 RapidEE 中所做的设置将在打开新终端窗口时可用。

.. _env_vars_zephyrrc:

选项 3: 使用 ``zephyrrc`` 文件
----------------------------------

如果您不想让变量设置在所有终端中可用,但仍希望保存该值以便在使用 Zephyr 时加载到环境中,请选择此选项。

.. tabs::

   .. group-tab:: Linux/macOS

      Zephyr 支持 :file:`zephyrrc` 文件的多个位置,尽可能遵循 XDG 基本目录规范。在以下位置之一创建 zephyrrc 文件(它们将按顺序检查):

      #. :file:`$XDG_CONFIG_HOME/zephyr/zephyrrc`
      #. :file:`$HOME/.config/zephyr/zephyrrc`
      #. :file:`$HOME/.zephyrrc`

      在您首选位置的文件中添加以下行:

      .. code-block:: console

         export MY_VARIABLE=foo

      要将此值恢复到当前终端环境中,**您必须从主** ``zephyr`` **仓库运行** ``source zephyr-env.sh``。此脚本会加载您的 :file:`zephyrrc`(它找到的上述位置列表中的第一个)以及其他功能。

      如果您关闭窗口等,该值将丢失;再次运行 ``source zephyr-env.sh`` 以恢复它。

   .. group-tab:: Windows

      使用文本编辑器(如记事本)将 ``set MY_VARIABLE=foo`` 行添加到文件 :file:`%userprofile%\\zephyrrc.cmd` 中以保存该值。

      要将此值恢复到当前终端环境中,在更改目录到主 ``zephyr`` 仓库后,**您必须在** ``cmd.exe`` **窗口中运行** ``zephyr-env.cmd``。此脚本会运行 :file:`%userprofile%\\zephyrrc.cmd` 以及其他功能。

      如果您关闭窗口等,该值将丢失;再次运行 ``zephyr-env.cmd`` 以恢复它。

      这些脚本:

      - 将 :envvar:`ZEPHYR_BASE` 设置为 zephyr 仓库的位置
      - 将一些 Zephyr 特定位置(如 zephyr 的 :file:`scripts` 目录)添加到您的 :envvar:`PATH` 环境变量中
      - 加载上面 :ref:`env_vars_zephyrrc` 中描述的 ``zephyrrc`` 文件中的任何设置。

      因此,您可以在需要这些设置时随时使用它们。

.. _zephyr-env:

Zephyr 环境脚本
**************************

您可以使用 zephyr 仓库脚本 ``zephyr-env.sh``(适用于 macOS 和 Linux)和 ``zephyr-env.cmd``(适用于 Windows)将 Zephyr 特定设置加载到当前终端环境中。为此,请从 zephyr 仓库运行以下命令:

.. tabs::

   .. group-tab:: Linux/macOS

      .. code-block:: console

         source zephyr-env.sh

   .. group-tab:: Windows

      .. code-block:: console

         zephyr-env.cmd

这些脚本:

- 将 :envvar:`ZEPHYR_BASE` 设置为 zephyr 仓库的位置
- 将一些 Zephyr 特定位置(如 zephyr 的 :file:`scripts` 目录)添加到您的 ``PATH`` 环境变量中
- 加载上面 :ref:`env_vars_zephyrrc` 中描述的 ``zephyrrc`` 文件中的任何设置。

因此,您可以在需要这些设置时随时使用它们。

.. _env_vars_important:

重要的环境变量
*******************************

一些 :ref:`重要构建变量 <important-build-vars>` 也可以在环境中设置。以下是其中一些重要环境变量的描述。这不是完整列表。

.. envvar:: BOARD

   请参见 :ref:`important-build-vars`。

.. envvar:: CONF_FILE

   请参见 :ref:`important-build-vars`。

.. envvar:: SHIELD

   请参见 :ref:`shields`。

.. envvar:: ZEPHYR_BASE

   请参见 :ref:`important-build-vars`。

.. envvar:: EXTRA_ZEPHYR_MODULES

   请参见 :ref:`important-build-vars`。

.. envvar:: ZEPHYR_MODULES

   请参见 :ref:`important-build-vars`。

.. envvar:: ZEPHYR_BOARD_ALIASES

   请参见 :ref:`gs-board-aliases`

在配置用于构建 Zephyr 应用的 :ref:`工具链 <gs_toolchain>` 时,以下附加环境变量非常重要。

.. envvar:: ZEPHYR_SDK_INSTALL_DIR

   安装 Zephyr SDK 的路径。

.. envvar:: ZEPHYR_TOOLCHAIN_VARIANT

   要使用的工具链名称。

.. envvar:: {TOOLCHAIN}_TOOLCHAIN_PATH

   由 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 指定的工具链的路径。例如,如果 ``ZEPHYR_TOOLCHAIN_VARIANT=llvm``,则使用 ``LLVM_TOOLCHAIN_PATH``。(注意形成环境变量名称时的大写。)

在 :ref:`更新 Zephyr SDK 工具链 <gs_toolchain_update>` 时,您可能需要更新其中一些变量。

仿真器和开发板可能还依赖于其他程序。构建系统将尝试自动定位这些程序,但可能依赖于其他 CMake 或环境变量来执行此操作。有关更多信息,请查阅仿真器或开发板的文档。在这种情况下,以下环境变量可能很有用:

.. envvar:: PATH

   ``PATH`` 是 Unix 类或 Microsoft Windows 操作系统上使用的环境变量,用于指定可执行程序所在的一组目录。

.. _using Chocolatey: https://chocolatey.org/packages/RapidEE
