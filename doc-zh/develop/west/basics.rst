.. _west-basics:.. _west-basics:



基础知识Basics

##############



本页介绍了 west 的基本概念并提供了进一步阅读的参考。This page introduces west's basic concepts and provides references to further

reading.

West 的内置命令允许你在公共 :term:`工作区 <west workspace>` 目录下与 :term:`项目 <west project>`

（Git 仓库）一起工作。West's built-in commands allow you to work with :term:`projects <west project>`

(Git repositories) under a common :term:`workspace <west workspace>` directory.

West 的工作方式如下：``west init`` 命令创建 :term:`west 工作区` 并克隆

:term:`清单仓库 <west manifest repository>`，而 ``west update`` 命令最初克隆，West works in the following manner: the ``west init`` command creates the

然后更新工作区中清单中列出的 :term:`项目 <west project>`。:term:`west workspace`, and clones the :term:`manifest repo <west manifest

repository>`, while the ``west update`` command initially clones, and later updates, the

示例工作区:term:`projects <west project>` listed in the manifest in the workspace.

**********

Example workspace

如果你按照 :ref:`getting_started` 进行操作，你的本地 :term:`west 工作区`，*****************

在这种情况下是名为 :file:`zephyrproject` 的文件夹及其所有子文件夹，看起来像这样：

.. _west-basics:


基础知识
########

本页介绍 west 的基本概念并提供进一步阅读的参考。

west 内置命令允许你在公共 :term:`工作区 <west workspace>` 目录下与 :term:`项目 <west project>`（Git 仓库）一起工作。
其工作方式简述如下：``west init`` 创建 :term:`west 工作区` 并克隆 :term:`清单仓库 <west manifest repository>`；
``west update`` 初次克隆并在后续更新清单中列出的 :term:`项目 <west project>`。


示例工作区
**********

如果你按照 :ref:`getting_started` 操作，本地 :term:`west 工作区`（此例名为 :file:`zephyrproject`）大致如下：

.. code-block:: none

   zephyrproject/                 # 工作区顶目录（topdir）
   ├── .west/                     # 标记顶目录的位置
   │   └── config                 # 工作区本地配置文件
   ├── zephyr/                    # 清单仓库（含 .git/）
   │   ├── west.yml               # 清单文件
   │   └── [... 其他文件 ...]
   ├── modules/                   # 由 west 管理的项目（示例）
   │   └── lib/
   │       └── zcbor/             # 一个项目（含 .git/）
   ├── tools/
   │   └── net-tools/             # 另一个项目（含 .git/）
   └── [... 其他项目 ...]

.. _west-workspace:

工作区概念
**********

以下是理解工作区结构所需的基础概念，更多细节参见 :ref:`west-workspaces`。

顶目录（topdir）
  顶目录是工作区的根目录，例如上面的 :file:`zephyrproject`（名称可自定义，如 ``z`` 或 ``my-zephyr-workspace``）。
  你通常通过 :ref:`west init <west-init-basics>` 创建顶目录及关联文件。

.west 目录
  顶目录包含 :file:`.west` 目录。west 通过查找 :file:`.west` 定位顶目录；查找自当前工作目录开始，
  若失败会从 :envvar:`ZEPHYR_BASE` 指定位置重试。

配置文件
  :file:`.west/config` 是工作区的 :ref:`本地配置文件 <west-config>`。

清单仓库（manifest repository）
  每个工作区恰有一个清单仓库（Git 仓库，包含清单文件）。其路径由本地配置的
  :ref:`manifest.path <west-config-index>` 指定。上游 Zephyr 默认使用 :file:`zephyr` 作为清单仓库，
  也可改为工作区内任意包含有效清单的仓库。更多形态参见 :ref:`west-topologies`，清单格式见 :ref:`west-manifests`。

清单文件（manifest file）
  清单文件为 YAML，定义由 west 管理的附加 Git 仓库（即“项目”）。默认文件名为 :file:`west.yml`，
  可通过 ``manifest.file`` 覆盖。你通过 :ref:`west update <west-update-basics>` 根据清单内容同步项目。

项目（project）
  项目是在清单中定义、由 west 管理的 Git 仓库，位置可在工作区任意处。上例中 ``zcbor`` 与 ``net-tools`` 均为项目。
  注意：Zephyr :ref:`构建系统 <build_overview>` 会用 west 提供的项目位置来发现 :ref:`模块`，
  但二者 :ref:`在概念上并不相同 <modules-vs-projects>`。

扩展（extensions）
  west 已知的任一仓库（清单仓库或项目）都可定义 :ref:`west-extensions`，即你可在该工作区使用的额外 west 命令。
  例如 Zephyr 仓库通过扩展提供 :ref:`west build <west-building>` 等命令，从而保持 west 核心与具体工作区细节解耦。

忽略的文件
  工作区中除 :file:`.west`、清单仓库及清单中列出的项目外的其它文件/仓库，west 基本都会忽略。


.. _west-init-basics:

``west init`` 基础
------------------

该命令用于创建 west 工作区。

.. important::

   运行 ``west init`` 后，west 不会再修改你的清单仓库内容；后续获取新版本请直接使用 Git。

常见的一次性用法：

.. code-block:: console

   west init -m https://github.com/zephyrproject-rtos/zephyr --mr v2.5.0 zephyrproject

执行后将会：

#. 创建顶目录 :file:`zephyrproject`，并生成 :file:`.west/` 与 :file:`.west/config`
#. 从 https://github.com/zephyrproject-rtos/zephyr 克隆清单仓库至 :file:`zephyrproject/zephyr`
#. 在本地 zephyr 仓库检出 ``v2.5.0`` 标签
#. 在 :file:`.west/config` 中设置 ``manifest.path=zephyr`` 与 ``manifest.file=west.yml``

此时只需运行 ``west update`` 克隆其余项目即可。更多细节见 :ref:`west-init`。


.. _west-update-basics:

``west update`` 基础
--------------------

该命令确保你的工作区包含与清单文件一致的项目仓库。

.. important::

   当你在清单仓库切换到不同修订后，请运行 ``west update`` 以同步新修订所需的项目集。

``west update`` 的主要步骤：

#. 定位顶目录（例如上例中的 :file:`zephyrproject`）
#. 读取顶目录下 :file:`.west/config` 的 ``manifest.path`` 与 ``manifest.file``
#. 加载清单文件（如 :file:`zephyrproject/zephyr/west.yml`）
#. 根据清单决定缺失项目的路径、克隆 URL 与目标修订；已存在的项目则获取并检出指定修订

更多细节见 :ref:`west-update`。


其他内置命令
************

参见 :ref:`west-built-in-cmds`。


.. _west-zephyr-extensions:

Zephyr 扩展
***********

关于 Zephyr 提供的扩展命令，参见：

- :ref:`west-build-flash-debug`
- :ref:`west-sign`
- :ref:`west-zephyr-ext-cmds`
- :ref:`west-shell-completion`


故障排除
********

参见 :ref:`west-troubleshooting`。
  将这些定义为扩展使 west 的核心对任何工作区的 Zephyr 版本等的细节不可知。  Projects are Git repositories managed by west. Projects are defined in the
