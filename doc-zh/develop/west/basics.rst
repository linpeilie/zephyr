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

If you've followed the :ref:`getting_started`, your local

.. code-block:: none:term:`west workspace`, which in this case is the folder named

:file:`zephyrproject` as well as all its subfolders, looks like this:

   zephyrproject/                 # west 顶目录

   ├── .west/                     # 标记顶目录的位置.. code-block:: none

   │   └── config                 # 工作区本地配置文件

   │   zephyrproject/                 # west topdir

   │   # 清单仓库，west 创建后永不修改：   ├── .west/                     # marks the location of the topdir

   ├── zephyr/                    # .git/ 仓库   │   └── config                 # per-workspace local configuration file

   │   ├── west.yml               # 清单文件   │

   │   └── [... 其他文件 ...]   │   # The manifest repository, never modified by west after creation:

   │   ├── zephyr/                    # .git/ repo

   │   # 由 west 管理的项目：   │   ├── west.yml               # manifest file

   ├── modules/   │   └── [... other files ...]

   │   └── lib/   │

   │       └── zcbor/             # .git/ 项目   │   # Projects managed by west:

   ├── tools/   ├── modules/

   │   └── net-tools/             # .git/ 项目   │   └── lib/

   └── [ ... 其他项目 ...]   │       └── zcbor/             # .git/ project

   ├── tools/

.. _west-workspace:   │   └── net-tools/             # .git/ project

   └── [ ... other projects ...]

工作区概念

**********.. _west-workspace:



以下是你应该理解的有关此结构的基本概念。更多详细信息在 :ref:`west-workspaces`。Workspace concepts

******************

顶目录

  上面，:file:`zephyrproject` 是工作区顶级目录的名称，或 *topdir*。Here are the basic concepts you should understand about this structure.

  （名称 :file:`zephyrproject` 只是一个示例 -- 它可以是任何东西，Additional details are in :ref:`west-workspaces`.

  如 ``z``、``my-zephyr-workspace`` 等。）

topdir

  你通常会使用 :ref:`west init <west-init-basics>` 创建顶目录和一些其他文件和目录。  Above, :file:`zephyrproject` is the name of the workspace's top level

  directory, or *topdir*. (The name :file:`zephyrproject` is just an example

.west 目录  -- it could be anything, like ``z``, ``my-zephyr-workspace``, etc.)

  顶目录包含 :file:`.west` 目录。当 west 需要找到顶目录时，它会搜索 :file:`.west`，

  并使用其父目录。搜索从当前工作目录开始（如果失败，从 :envvar:`ZEPHYR_BASE`  You'll typically create the topdir and a few other files and directories

  环境变量中的位置重新开始作为后备）。  using :ref:`west init <west-init-basics>`.



配置文件.west directory

  文件 :file:`.west/config` 是工作区的 :ref:`本地配置文件 <west-config>`。  The topdir contains the :file:`.west` directory. When west needs to find

  the topdir, it searches for :file:`.west`, and uses its parent directory.

清单仓库  The search starts from the current working directory (and starts again from

  每个 west 工作区恰好包含一个 *清单仓库*，这是一个包含 *清单文件* 的 Git 仓库。  the location in the :envvar:`ZEPHYR_BASE` environment variable as a

  清单仓库的位置由本地配置文件中的 :ref:`manifest.path 配置选项 <west-config-index>`  fallback if that fails).

  给出。

configuration file

  对于上游 Zephyr，:file:`zephyr` 是清单仓库，但你可以配置 west 使用工作区中的  The file :file:`.west/config` is the workspace's :ref:`local configuration

  任何 Git 仓库作为清单仓库。唯一的要求是它包含有效的清单文件。  file <west-config>`.

  有关其他选项的信息，请参阅 :ref:`west-topologies`，有关清单文件格式的详细信息，

  请参阅 :ref:`west-manifests`。manifest repository

  Every west workspace contains exactly one *manifest repository*, which is a

清单文件  Git repository containing a *manifest file*. The location of the manifest

  清单文件是一个 YAML 文件，定义了 *项目*，这些是工作区中由 west 管理的附加 Git 仓库。  repository is given by the :ref:`manifest.path configuration option

  清单文件默认命名为 :file:`west.yml`；这可以使用 ``manifest.file`` 本地配置选项覆盖。  <west-config-index>` in the local configuration file.



  你使用 :ref:`west update <west-update-basics>` 命令根据清单文件的内容更新  For upstream Zephyr, :file:`zephyr` is the manifest repository, but you can

  工作区的项目。  configure west to use any Git repository in the workspace as the manifest

  repository. The only requirement is that it contains a valid manifest file.

项目  See :ref:`west-topologies` for information on other options, and

  项目是由 west 管理的 Git 仓库。项目在清单文件中定义，可以位于工作区内的任何位置。  :ref:`west-manifests` for details on the manifest file format.

  在上面的示例工作区中，``zcbor`` 和 ``net-tools`` 是项目。

manifest file

  默认情况下，Zephyr :ref:`构建系统 <build_overview>` 使用 west 获取工作区中所有  The manifest file is a YAML file that defines *projects*, which are the

  项目的位置，因此它们包含的任何代码都可以用作 :ref:`模块`。但请注意，模块和项目  additional Git repositories in the workspace managed by west. The manifest

  :ref:`在概念上是不同的 <modules-vs-projects>`。  file is named :file:`west.yml` by default; this can be overridden using the

  ``manifest.file`` local configuration option.

扩展

  west 已知的任何仓库（清单仓库或任何项目仓库）都可以定义 :ref:`west-extensions`。  You use the :ref:`west update <west-update-basics>` command to update the

  扩展是你在使用该工作区时可以运行的额外 west 命令。  workspace's projects based on the contents of the manifest file.



  zephyr 仓库使用此功能提供 Zephyr 特定命令，如 :ref:`west build <west-building>`。projects

  将这些定义为扩展使 west 的核心对任何工作区的 Zephyr 版本等的细节不可知。  Projects are Git repositories managed by west. Projects are defined in the

  manifest file and can be located anywhere inside the workspace. In the above

忽略的文件  example workspace, ``zcbor`` and ``net-tools`` are projects.

  工作区可以包含由 west 不管理的附加 Git 仓库或其他文件和目录。

  West 基本上忽略工作区中除 :file:`.west`、清单仓库和清单文件中指定的项目之外的所有内容。  By default, the Zephyr :ref:`build system <build_overview>` uses west to get

  the locations of all the projects in the workspace, so any code they contain

west init 和 west update  can be used as :ref:`modules`. Note however that modules and projects

*************************  :ref:`are conceptually different <modules-vs-projects>`.



两个最重要的工作区相关命令是 ``west init`` 和 ``west update``。extensions

  Any repository known to west (either the manifest repository or any project

.. _west-init-basics:  repository) can define :ref:`west-extensions`. Extensions are extra west

  commands you can run when using that workspace.

``west init`` 基础

------------------  The zephyr repository uses this feature to provide Zephyr-specific commands

  like :ref:`west build <west-building>`. Defining these as extensions keeps

此命令创建 west 工作区。  west's core agnostic to the specifics of any workspace's Zephyr version,

  etc.

.. important::

ignored files

   West 在运行 ``west init`` 后不会更改你的清单仓库内容。使用普通 Git 命令拉取  A workspace can contain additional Git repositories or other files and

   新版本等。  directories not managed by west. West basically ignores anything in the

  workspace except :file:`.west`, the manifest repository, and the projects

你通常会像这样运行它一次：  specified in the manifest file.



.. code-block:: shellwest init and west update

*************************

   west init -m https://github.com/zephyrproject-rtos/zephyr --mr v2.5.0 zephyrproject

The two most important workspace-related commands are ``west init`` and ``west

这将：update``.



#. 创建顶目录 :file:`zephyrproject`，以及其中的 :file:`.west` 和 :file:`.west/config`.. _west-init-basics:

#. 从 https://github.com/zephyrproject-rtos/zephyr 克隆清单仓库，

   将其放入 :file:`zephyrproject/zephyr```west init`` basics

#. 在你的本地 zephyr 克隆中检出 ``v2.5.0`` git 标签--------------------

#. 在 :file:`.west/config` 中将 ``manifest.path`` 设置为 ``zephyr``

#. 将 ``manifest.file`` 设置为 ``west.yml``This command creates a west workspace.



你的工作区现在几乎可以使用了；你只需要运行 ``west update`` 来克隆工作区中的.. important::

其余项目就可以完成。

   West doesn't change your manifest repository contents after ``west init`` is

有关更多详细信息，请参阅 :ref:`west-init`。   run. Use ordinary Git commands to pull new versions, etc.



.. _west-update-basics:You will typically run it once, like this:



``west update`` 基础.. code-block:: shell

--------------------

   west init -m https://github.com/zephyrproject-rtos/zephyr --mr v2.5.0 zephyrproject

此命令确保你的工作区包含与清单文件中的项目匹配的 Git 仓库。

This will:

.. important::

#. Create the topdir, :file:`zephyrproject`, along with

   每当你在清单仓库中检出不同的修订版本时，你都应该运行 ``west update``   :file:`.west` and :file:`.west/config` inside it

   以确保你的工作区包含新修订版本所期望的项目仓库。#. Clone the manifest repository from

   https://github.com/zephyrproject-rtos/zephyr, placing it into

``west update`` 命令通过以下方式读取清单文件的内容：   :file:`zephyrproject/zephyr`

#. Check out the ``v2.5.0`` git tag in your local zephyr clone

#. 找到顶目录。在上面的 ``west init`` 示例中，这意味着找到 :file:`zephyrproject`。#. Set ``manifest.path`` to ``zephyr`` in :file:`.west/config`

#. 加载顶目录中的 :file:`.west/config` 以读取 ``manifest.path``#. Set ``manifest.file`` to ``west.yml``

   （例如 ``zephyr``）和 ``manifest.file``（例如 ``west.yml``）选项。

#. 加载这些选项给出的清单文件（例如 :file:`zephyrproject/zephyr/west.yml`）。Your workspace is now almost ready to use; you just need to run ``west update``

to clone the rest of the projects into the workspace to finish.

然后它使用清单文件来决定缺失的项目应该放在工作区的什么地方、

从什么 URL 克隆它们，以及应该在本地检出什么 Git 修订版本。For more details, see :ref:`west-init`.

已经存在的项目仓库通过获取和检出其各自的清单文件中的 Git 修订版本就地更新。

.. _west-update-basics:

有关更多详细信息，请参阅 :ref:`west-update`。

``west update`` basics

其他内置命令----------------------

*************

This command makes sure your workspace contains Git repositories matching the

参阅 :ref:`west-built-in-cmds`。projects in the manifest file.



.. _west-zephyr-extensions:.. important::



Zephyr 扩展   Whenever you check out a different revision in your manifest repository, you

***********   should run ``west update`` to make sure your workspace contains the

   project repositories the new revision expects.

有关 Zephyr 扩展命令的信息，请参阅以下页面：

The ``west update`` command reads the manifest file's contents by:

- :ref:`west-build-flash-debug`

- :ref:`west-sign`#. Finding the topdir. In the ``west init`` example above, that

- :ref:`west-zephyr-ext-cmds`   means finding :file:`zephyrproject`.

- :ref:`west-shell-completion`#. Loading :file:`.west/config` in the topdir to read the ``manifest.path``

   (e.g. ``zephyr``) and ``manifest.file`` (e.g. ``west.yml``) options.

故障排除#. Loading the manifest file given by these options (e.g.

*********   :file:`zephyrproject/zephyr/west.yml`).



参阅 :ref:`west-troubleshooting`。It then uses the manifest file to decide where missing projects should be

placed within the workspace, what URLs to clone them from, and what Git
revisions should be checked out locally. Project repositories which already
exist are updated in place by fetching and checking out their respective Git
revisions in the manifest file.

For more details, see :ref:`west-update`.

Other built-in commands
***********************

See :ref:`west-built-in-cmds`.

.. _west-zephyr-extensions:

Zephyr Extensions
*****************

See the following pages for information on Zephyr's extension commands:

- :ref:`west-build-flash-debug`
- :ref:`west-sign`
- :ref:`west-zephyr-ext-cmds`
- :ref:`west-shell-completion`

Troubleshooting
***************

See :ref:`west-troubleshooting`.
