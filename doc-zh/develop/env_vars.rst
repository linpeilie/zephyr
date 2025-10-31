.. _env_vars:

环境变量
=======

此文档中的各个页面都涉及设置 Zephyr 特定的环境变量。此页面描述了如何进行。

设置变量
*******

选项 1: 仅一次
-----------

要为当前终端窗口的生命周期将环境变量 ``MY_VARIABLE`` 设置为 ``foo``:

.. tabs::

   .. group-tab:: Linux/macOS

      .. code-block:: console

         export MY_VARIABLE=foo

   .. group-tab:: Windows

      .. code-block:: console

         set MY_VARIABLE=foo

.. warning::

  这最适合实验。如果你关闭终端窗口、使用另一个终端窗口或选项卡、重新启动计算机等,
  此设置将永久丢失。

  如果你想继续使用该设置,建议使用选项 2 或 3。

选项 2: 在所有终端中
------------------

.. tabs::

   .. group-tab:: Linux/macOS

      将 ``export MY_VARIABLE=foo`` 行添加到主目录中的 shell 启动脚本。对于 Bash,
      这通常是 Linux 上的 :file:`~/.bashrc` 或 macOS 上的 :file:`~/.bash_profile`。
      这些启动脚本中的更改不会影响已启动的 shell 实例;尝试打开新终端窗口以获取新设置。

   .. group-tab:: Windows

      你可以使用 ``cmd.exe`` 中的 ``setx`` 程序或第三方 RapidEE 程序。

      要使用 ``setx``,输入此命令,然后关闭终端窗口。任何新的 ``cmd.exe`` 窗口都将
      具有设置为 ``foo`` 的 ``MY_VARIABLE``。

      .. code-block:: console

         setx MY_VARIABLE foo

      要安装 RapidEE(免费的图形环境变量编辑器),在管理员命令提示符中
      `使用 Chocolatey <using Chocolatey>`_:

      .. code-block:: console

         choco install rapidee

      然后你可以从终端运行 ``rapidee`` 以启动程序和设置环境变量。
      确保使用"User"环境变量区域 -- 否则,你必须以管理员身份运行 RapidEE。
      还要确保在退出前点击左上角的保存按钮保存更改。你在 RapidEE 中所做的设置
      将在打开新终端窗口时可用。

.. _env_vars_zephyrrc:

选项 3: 使用 ``zephyrrc`` 文件
---------------------------

如果你不想使变量的设置对所有终端都可用,但仍希望在使用 Zephyr 时将值保存以加载到你的环境中,
请选择此选项。

.. tabs::

   .. group-tab:: Linux/macOS

      Zephyr 支持 :file:`zephyrrc` 文件的多个位置,在可能的情况下遵循 XDG 基目录规范。
      在以下位置之一创建 zephyrrc 文件(将按顺序检查):

      #. :file:`$XDG_CONFIG_HOME/zephyr/zephyrrc`
      #. :file:`$HOME/.config/zephyr/zephyrrc`
      #. :file:`$HOME/.zephyrrc`

      将此行添加到你首选位置的文件中:

      .. code-block:: console

         export MY_VARIABLE=foo

      要将此值重新获取到当前终端环境中,**你必须从主 ``zephyr`` 存储库运行**
      ``source zephyr-env.sh``。除其他事项外,此脚本源你的 :file:`zephyrrc`
      (从上面的位置列表中找到的第一个)。

      如果你关闭窗口等,该值将丢失;再次运行 ``source zephyr-env.sh`` 以恢复。

   .. group-tab:: Windows

      将行 ``set MY_VARIABLE=foo`` 添加到文件 :file:`%userprofile%\\zephyrrc.cmd`
      使用文本编辑器(如记事本)保存值。

      要将此值重新获取到当前终端环境中,**你必须在将目录更改为主 ``zephyr`` 存储库后
      在 ``cmd.exe`` 窗口中运行** ``zephyr-env.cmd``。除其他事项外,此脚本运行
      :file:`%userprofile%\\zephyrrc.cmd`。

      如果你关闭窗口等,该值将丢失;再次运行 ``zephyr-env.cmd`` 以恢复。

      这些脚本:

      - 设置 :envvar:`ZEPHYR_BASE` 为 zephyr 存储库的位置
      - 向你的 :envvar:`PATH` 环境变量添加一些 Zephyr 特定位置(例如 zephyr 的 :file:`scripts` 目录)
      - 从上面 :ref:`env_vars_zephyrrc` 中描述的 ``zephyrrc`` 文件加载任何设置。

      因此,你可以在任何时候需要这些设置中的任何一个时使用它们。

.. _zephyr-env:

Zephyr 环境脚本
**************

你可以使用 zephyr 存储库脚本 ``zephyr-env.sh``(对于 macOS 和 Linux)
和 ``zephyr-env.cmd``(对于 Windows)将 Zephyr 特定设置加载到你的当前终端的环境中。
要执行此操作,从 zephyr 存储库运行此命令:

.. tabs::

   .. group-tab:: Linux/macOS

      .. code-block:: console

         source zephyr-env.sh

   .. group-tab:: Windows

      .. code-block:: console

         zephyr-env.cmd

这些脚本:

- 设置 :envvar:`ZEPHYR_BASE` 为 zephyr 存储库的位置
- 向你的 ``PATH`` 环境变量添加一些 Zephyr 特定位置(例如 zephyr 的 :file:`scripts` 目录)
- 从上面 :ref:`env_vars_zephyrrc` 中描述的 ``zephyrrc`` 文件加载任何设置。

因此,你可以在任何时候需要这些设置中的任何一个时使用它们。

.. _env_vars_important:

重要的环境变量
*************

某些 :ref:`important-build-vars` 也可以在环境中设置。以下是对这些重要环境变量的一些描述。
这不是一个完整的列表。

.. envvar:: BOARD

   参见 :ref:`important-build-vars`。

.. envvar:: CONF_FILE

   参见 :ref:`important-build-vars`。

.. envvar:: SHIELD

   参见 :ref:`shields`。

.. envvar:: ZEPHYR_BASE

   参见 :ref:`important-build-vars`。

.. envvar:: EXTRA_ZEPHYR_MODULES

   参见 :ref:`important-build-vars`。

.. envvar:: ZEPHYR_MODULES

   参见 :ref:`important-build-vars`。

.. envvar:: ZEPHYR_BOARD_ALIASES

   参见 :ref:`gs-board-aliases`

配置用于构建 Zephyr 应用程序的 :ref:`toolchain <gs_toolchain>` 时,
以下附加环境变量很重要。

.. envvar:: ZEPHYR_SDK_INSTALL_DIR

   Zephyr SDK 安装的路径。

.. envvar:: ZEPHYR_TOOLCHAIN_VARIANT

   要使用的工具链的名称。

.. envvar:: {TOOLCHAIN}_TOOLCHAIN_PATH

   由 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 指定的工具链的路径。例如,
   如果 ``ZEPHYR_TOOLCHAIN_VARIANT=llvm``,使用 ``LLVM_TOOLCHAIN_PATH``。
   (在形成环境变量名称时注意大小写。)

当你 :ref:`更新 Zephyr SDK 工具链 <gs_toolchain_update>` 时,
可能需要更新这些变量中的某些。

模拟器和板卡也可能依赖于其他程序。构建系统将尝试自动定位这些程序,
但可能依赖其他 CMake 或环境变量来执行此操作。请查阅你的模拟器或板卡的文档了解更多信息。
以下环境变量在此类情况下可能很有用:

.. envvar:: PATH

   ``PATH`` 是在类 Unix 或 Microsoft Windows 操作系统上使用的环境变量,
   用于指定一组可执行程序所在的目录。

.. _using Chocolatey: https://chocolatey.org/packages/RapidEE
