.. _west-troubleshooting:

West 问题排查
#############

本页涵盖 west 的常见问题及其解决方法。

``west update`` 获取失败
***********************

排查获取问题的一个好方法是以详细模式运行 ``west update``，如下所示：

.. code-block:: shell

   west -v update

输出包括 west 运行的 Git 命令及其输出。查找类似以下内容：

.. code-block:: none

   === updating your_project (path/to/your/project):
   west.manifest: your_project: checking if cloned
   [...其他 west.manifest 日志...]
   --- your_project: fetching, need revision SOME_SHA
   west.manifest: running 'git fetch ... https://github.com/your-username/your_project ...' in /some/directory

上面最后一行的 ``git fetch`` 命令示例是需要成功的内容。

一个策略是转到 ``/path/to/your/project``，复制/粘贴并运行整个 ``git fetch`` 命令，然后使用凭证存储助手的文档从那里进行调试。

如果在公司防火墙后面，可能存在代理或其他问题，``curl -v FETCH_URL``（对于 HTTPS URL）或 ``ssh -v FETCH_URL``（对于 SSH URL）可能会有所帮助。

如果在直接运行时可以使无需输入密码的情况下成功运行 ``git fetch`` 命令，则将能够在同一 shell 中无需输入密码的情况下运行 ``west update``。

"'west' 未被识别为内部或外部命令、可操作程序或批处理文件"
************************************************************

在 Windows 上，这意味着 west 未安装，或 :envvar:`PATH` 环境变量不包含 pip 安装 :file:`west.exe` 的目录。

首先，确保已安装 west；请参见 :ref:`west-install`。然后尝试从新的 ``cmd.exe`` 窗口运行 ``west``。如果仍然不起作用，请继续阅读。

需要找到包含 :file:`west.exe` 的目录，然后将其添加到 :envvar:`PATH`。（在安装 Python 和 pip 时，此 :envvar:`PATH` 更改应该为您完成，因此通常不需要按照这些步骤操作。）

在 ``cmd.exe`` 中运行此命令::

  pip3 show west

然后：

#. 在输出中查找看起来像 ``Location: C:\foo\python\python38\lib\site-packages`` 的行。确切的位置在计算机上会有所不同。
#. 在 ``scripts`` 目录 ``C:\foo\python\python38\scripts`` 中查找名为 ``west.exe`` 的文件。

   .. important::

      注意在 ``pip3 show`` 输出中 ``lib\site-packages`` 如何更改为 ``scripts``！

#. 如果在 ``scripts`` 目录中看到 ``west.exe``，请使用如下命令将 ``scripts`` 的完整路径添加到 :envvar:`PATH`::

     setx PATH "%PATH%;C:\foo\python\python38\scripts"

   **不要仅复制/粘贴此命令**。``scripts`` 目录位置在系统上会有所不同。

#. 关闭 ``cmd.exe`` 窗口并打开一个新窗口。应该能够运行 ``west``。

"invalid choice: 'build'"（或 'flash' 等）
*****************************************

如果在尝试运行 Zephyr 扩展命令（如 :ref:`west flash <west-flashing>`、:ref:`west build <west-building>` 等）时看到如下意外错误：

.. code-block:: none

   $ west build [...]
   west: error: argument <command>: invalid choice: 'build' (choose from 'init', [...])

   $ west flash [...]
   west: error: argument <command>: invalid choice: 'flash' (choose from 'init', [...])

最可能的原因是在 :ref:`west 工作区 <west-workspace>` 外运行命令。West 需要知道工作区的位置以查找 :ref:`west-extensions`。

要修复此问题，有两个选择：

#. 从工作区内运行命令（例如，在 :ref:`入门 <getting_started>` 时创建的 :file:`zephyrproject` 目录）。

   例如，在工作区内创建构建目录，或从工作区内运行 ``west flash --build-dir YOUR_BUILD_DIR``。

#. 设置 :envvar:`ZEPHYR_BASE` :ref:`环境变量 <env_vars>` 并重新运行 west 扩展命令。如果设置，west 将使用 :envvar:`ZEPHYR_BASE` 查找工作区。

如果不确定命令是内置命令还是扩展命令，请从工作区内运行 ``west help``。对于 mainline Zephyr，输出分别打印扩展命令，如下所示：

.. code-block:: none

   $ west help

   用于管理 git 仓库的内置命令：
     init:                 创建 west 工作区
     [...]

   其他内置命令：
     help:                 获取 west 或命令的帮助
     [...]

   来自项目清单的扩展命令（路径：zephyr）：
     build:                编译 Zephyr 应用
     flash:                在开发板上刷写并运行二进制文件
     [...]

"invalid choice: 'post-init'"
*****************************

如果在运行 ``west init`` 时看到此错误：

.. code-block:: none

   west: error: argument <command>: invalid choice: 'post-init'
   (choose from 'init', 'update', 'list', 'manifest', 'diff',
   'status', 'forall', 'config', 'selfupdate', 'help')

那么已安装的 west 版本较旧，并尝试在需要更新版本的工作区中使用它。

解决此问题的最简单方法是按如下方式升级 west 并重试：

#. 如 :ref:`west-install` 中所示，使用 ``pip3 install`` 的 ``-U`` 选项安装最新 west。

#. 备份要保存的 :file:`zephyrproject/.west/config` 的任何内容。（如果未设置任何配置选项，可以安全地跳过此步骤。）

#. 完全删除 :file:`zephyrproject/.west` 目录（如果不删除，将获得下一个讨论的"already in a workspace"错误消息）。

#. 再次运行 ``west init``。
