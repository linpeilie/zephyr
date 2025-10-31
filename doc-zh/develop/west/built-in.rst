.. _west-built-in-cmds:

内置命令
#######

此页面更详细地描述了 west 的内置命令，其中一些在 :ref:`west-basics` 中介绍过。

某些命令与相同名称的 Git 命令相关，但在整个工作区上运行。
例如，``west diff`` 显示工作区中多个 Git 仓库中的本地更改。

某些命令将项目作为参数。这些参数可以是在清单文件中指定的项目名称，
或者（作为备选方案）是文件系统中的路径。省略接受项目参数的命令
（如 ``west list``、``west forall`` 等）通常默认为使用清单文件中的所有项目
加上清单仓库本身。

有关其他帮助，请运行 ``west <command> -h``（例如 ``west init -h``）。

.. _west-init:

west init
*********

此命令创建 west 工作区。它可以用两种方式使用：

1. 从远程 URL 克隆新的清单仓库
2. 围绕现有的本地清单仓库创建工作区

**选项 1**: 从远程 URL 克隆新的清单仓库，使用：

.. code-block:: none

   west init [-m URL] [--mr REVISION] [--mf FILE] [directory]

新的工作区在给定的 :file:`directory` 中创建，在该目录内创建新的 :file:`.west`。
你可以使用 ``-m`` 开关给出清单 URL，使用 ``--mr`` 给出初始修订版本进行检查，
并使用 ``--mf`` 给出仓库内清单文件的位置。

例如，运行：

.. code-block:: shell

   west init -m https://github.com/zephyrproject-rtos/zephyr --mr v1.14.0 zp

会将上游官方 zephyr 仓库克隆到 :file:`zp/zephyr`，
并检查出 ``v1.14.0`` 发布版本。此命令创建 :file:`zp/.west`，
并将 ``manifest.path`` :ref:`配置选项 <west-config>` 设置为 ``zephyr``
以记录工作区中清单仓库的位置。使用默认清单文件位置。

``-m`` 选项默认为 ``https://github.com/zephyrproject-rtos/zephyr``。
``--mf`` 选项默认为 ``west.yml``。从 west v0.10.1 开始，west 将使用
清单仓库中的默认分支，除非使用 ``--mr`` 选项覆盖它。
（在早期版本中，``--mr`` 默认为 ``master``。）

如果未给出 ``directory``，则使用当前工作目录。

**选项 2**: 围绕现有的本地清单仓库创建工作区，使用：

.. code-block:: none

   west init -l [--mf FILE] directory

这在文件系统中的 :file:`directory` **旁边** 创建 :file:`.west`，
并将 ``manifest.path`` 设置为 ``directory``。

如上所述，``--mf`` 默认为 ``west.yml``。

**重新配置工作区**：

如果你稍后改变主意，你可以在运行 ``west init`` 后自由更改 ``manifest.path`` 
和 ``manifest.file``，使用 :ref:`west-config-cmd`。
只需确保之后运行 ``west update`` 以更新你的工作区以匹配新的清单文件。

.. _west-update:

west update
***********

.. code-block:: none

   west update [-f {always,smart}] [-k] [-r]
               [--group-filter FILTER] [--stats] [PROJECT ...]

**更新哪些项目：**

默认情况下，此命令解析清单文件（通常是 :file:`west.yml`），
并更新那里指定的每个项目。如果你的清单使用 :ref:`项目组 <west-manifest-groups>`，
则仅更新活跃项目。

要仅在项目子集上运行，给出 ``PROJECT`` 参数。每个 ``PROJECT`` 
可以是清单文件中给出的项目名称，或指向工作区内项目的路径。
如果你明确指定项目，无论它们是否活跃都会更新。

**项目更新过程：**

对于要更新的每个项目，此命令：

#. 如果不存在，为工作区中的项目初始化本地 Git 仓库
#. 检查清单中项目的 ``revision`` 字段，如果本地不可用，则从远程获取
#. 将项目的 :ref:`manifest-rev <west-manifest-rev>` 分支设置为
   上一步中修订版本指定的提交
#. 在本地工作副本中检查 ``manifest-rev`` 作为
   `分离的 HEAD <https://git-scm.com/docs/git-checkout#_detached_head>`_
#. 如果清单文件为项目指定了 :ref:`submodules <west-manifest-submodules>` 键，
   按照下面的描述递归更新项目的子模块。

为了避免不必要的获取，``west update`` 不会获取已在本地可用的 Git SHA 或标记的项目 
``revision`` 值。这是当 ``-f``（``--fetch``）选项具有其默认值 ``smart`` 时的行为。
要强制此命令即使修订版本似乎在本地可用也从项目远程获取，
请使用 ``-f always`` 或将 ``update.fetch`` :ref:`配置选项 <west-config>` 
设置为 ``always``。只要 SHA 对 Git 是可接受的，它们可以作为唯一前缀给出 [#fetchall]_。

如果项目 ``revision`` 是既不是标记也不是 SHA 的 Git 引用
（即，如果项目跟踪分支），``west update`` 总是获取，
无论 ``-f`` 和 ``update.fetch``。

某些分支名称可能看起来像短 SHA，如 ``deadbeef``。West 将其视为 SHA。
你可以通过用 ``refs/heads/`` 前缀 ``revision`` 值来消除歧义，
例如 ``revision: refs/heads/deadbeef``。

为了安全起见，``west update`` 使用 ``git checkout --detach`` 
在每个更新的项目的清单修订版本处检查分离的 ``HEAD``，
留下任何已经检出的分支。这通常是一个安全的操作，
不会修改你的任何本地分支。

但是，如果你在 west 检出的之前分离的 ``HEAD`` 上添加了一些本地提交，
那么 git 会警告你已留下一些不再被任何分支引用的提交。
这些可能在未来的某个时刻被垃圾收集和丢失。如果项目中有本地提交，
请确保在运行 ``west update`` 之前检出本地分支，以避免这种情况。

如果你想让任何检出的本地分支都被变基，请使用 ``-r``（``--rebase``）选项。

如果你想让 ``west update`` 保持本地分支检出，只要它们指向新的
``manifest-rev`` 的后代提交，请使用 ``-k``（``--keep-descendants``）选项。

.. note::

   ``west update --rebase`` 在项目中失败的情况下会发生 git 冲突
   在你的分支和清单引入的新提交之间。你应该立即解决这些冲突，
   就像你通常使用 ``git`` 一样，或者你可以使用 
   ``git -C <project_path> rebase --abort`` 来暂时忽略传入的更改。

   使用干净的工作树，简单的 ``west update`` 永远不会失败，
   因为它不会尝试保留你的提交，只是将其搁置。

   ``west update --keep-descendants`` 提供了一个中间选项，
   也永远不会失败但不会对所有项目一视同仁：

   - 在你的分支与传入提交不同的项目中，它甚至不会尝试变基
     并像简单的 ``west update`` 那样将你的分支留下；
   - 在所有其他不需要变基或合并的项目中，它保持你的分支就位。

**一次性项目组操作：**

``--group-filter`` 选项可用于更改在单个 ``west update`` 命令期间
启用或禁用哪些项目组。有关项目组功能的详细信息，请参见 :ref:`west-manifest-groups`。

``west update`` 命令的行为就像 ``--group-filter`` 选项的值
被附加到 ``manifest.group-filter`` :ref:`配置选项 <west-config-index>` 一样。

例如，运行 ``west update --group-filter=+foo,-bar`` 的行为
与你临时将字符串 ``"+foo,-bar"`` 附加到 ``manifest.group-filter`` 
的值，运行 ``west update``，然后将 ``manifest.group-filter`` 
恢复到其原始值的方式相同。

注意使用语法 ``--group-filter=VALUE`` 而不是 ``--group-filter VALUE`` 
可以避免如果你只想禁用单个组（例如 ``--group-filter=-bar``）时解析命令行选项的问题。

**子模块更新过程：**

如果清单中的项目有 ``submodules`` 键，子模块将按如下方式进行更新，
具体取决于 ``submodules`` 键的值。

如果项目有 ``submodules: true``，west 首先将项目的子模块与以下内容同步：

.. code-block::

   git submodule sync --recursive

然后 West 在项目仓库中运行以下命令之一，具体取决于
你是否使用 ``--rebase`` 选项运行 ``west update``：

.. code-block::

   # 不使用 --rebase，例如 "west update":
   git submodule update --init --checkout --recursive

   # 使用 --rebase，例如 "west update --rebase":
   git submodule update --init --rebase --recursive

否则，项目有 ``submodules: <list-of-submodules>``。在这种情况下，
west 将项目的子模块与以下内容同步：

.. code-block::

   git submodule sync --recursive -- <submodule-path>

然后它根据你是否使用 ``--rebase`` 选项运行 ``west update``
按如下方式更新列表中的每个子模块：

.. code-block::

   # 不使用 --rebase，例如 "west update":
   git submodule update --init --checkout --recursive <submodule-path>

   # 使用 --rebase，例如 "west update --rebase":
   git submodule update --init --rebase --recursive <submodule-path>

如果 ``update.sync-submodules`` :ref:`west-config` 选项为 false，
则跳过 ``git submodule sync`` 命令。

.. _west-built-in-misc:

其他项目命令
***********

West 有一些管理工作区中项目的命令，此处总结如下。
运行 ``west <command> -h`` 获取详细帮助。

- ``west compare``: 比较工作区的状态与清单
- ``west diff``: 在本地项目仓库中运行 ``git diff``
- ``west forall``: 在本地项目仓库中运行任意命令
- ``west grep``: 在本地项目仓库中搜索模式
- ``west list``: 根据格式字符串打印清单中每个项目的一行信息
- ``west manifest``: 管理清单文件。参见 :ref:`west-manifest-cmd`。
- ``west status``: 在本地项目仓库中运行 ``git status``

其他内置命令
*************

最后，这里是其他内置命令的摘要。

- ``west config``: 获取或设置 :ref:`配置选项 <west-config>`
- ``west topdir``: 打印 west 工作区的顶级目录
- ``west help``: 获取关于命令的帮助，或打印有关工作区中所有命令的信息，
  包括 :ref:`west-extensions`

.. rubric:: 脚注

.. [#fetchall]

   当给定 SHA 作为修订版本时，West 可能会从 Git 服务器获取所有 ref。
   这是因为一些 Git 服务器历来不允许直接获取 SHA。
