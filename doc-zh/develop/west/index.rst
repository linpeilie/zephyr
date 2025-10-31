.. _west:

West（Zephyr 的元工具）
######################

Zephyr 项目包含一个名为 ``west`` [#west-name]_ 的瑞士军刀式命令行工具。West 在其自己的 `repository`_ 中开发。

West 的内置命令提供了一个多仓库管理系统，其特性受到 Google 的 Repo 工具和 Git 子模块的启发。West 也是"可插件的"：你可以编写自己的 west 扩展命令，为 west 添加额外的功能。Zephyr 使用这一特性为构建应用程序、刷新和调试应用程序等提供便利。

像 ``git`` 和 ``docker`` 一样，顶级 ``west`` 命令接受一些通用选项、要运行的子命令，以及该子命令的选项和参数::

  west [common-opts] <command> [opts] <args>

从 west v0.8 开始，你也可以这样运行 west::

  python3 -m west [common-opts] <command> [opts] <args>

你可以运行 ``west --help``（或简写 ``west -h``）来获得可用 west 命令的顶级帮助，以及 ``west <command> -h`` 来获得每个命令的详细帮助。

.. toctree::
   :maxdepth: 1

   install.rst
   release-notes.rst
   troubleshooting.rst
   basics.rst
   built-in.rst
   workspaces.rst
   manifest.rst
   config.rst
   alias.rst
   extensions.rst
   build-flash-debug.rst
   sign.rst
   zephyr-cmds.rst
   why.rst
   without-west.rst

有关 west 的 Python API 的详细信息，请参阅 :ref:`west-apis`。

.. rubric:: 脚注

.. [#west-name]

   Zephyr 是拉丁语 `Zephyrus <https://en.wiktionary.org/wiki/Zephyrus>`_
   的英文名称，古希腊的西风之神。

.. _repository:
   https://github.com/zephyrproject-rtos/west
