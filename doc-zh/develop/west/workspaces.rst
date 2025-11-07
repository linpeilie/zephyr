.. _west-workspaces:

工作空间 (Workspaces)
######################

本页面更详细地描述了在 :ref:`west-basics` 中介绍的 *west 工作空间* 概念。

.. _west-manifest-rev:

``manifest-rev`` 分支
**********************

West 在每个项目中创建并控制一个名为 ``manifest-rev`` 的 Git 分支。
该分支指向清单文件在上次运行 :ref:`west-update` 时为项目指定的修订版本。
其他工作空间管理命令可能会使用 ``manifest-rev`` 作为此最新更新时上游修订版本的参考点。
除其他目的外,``manifest-rev`` 分支允许清单文件使用 SHA 作为项目修订版本。

虽然 ``manifest-rev`` 是一个正常的 Git 分支,但 west 会在下次更新时重新创建和/或重置它。
因此,自己检出或以其他方式修改它是 **危险的**。例如,您手动添加到此分支的任何提交可能会
在下次运行 ``west update`` 时丢失。相反,请检出具有其他名称的本地分支,然后将其变基到
新的 ``manifest-rev`` 上,或将 ``manifest-rev`` 合并到其中。

.. note::

   West 不会在清单仓库中创建 ``manifest-rev`` 分支,因为 west 不管理清单仓库的分支或修订版本。

``refs/west/*`` Git 引用
*************************

West 还在本地项目仓库中为自己保留所有以 ``refs/west/`` 开头的 Git 引用(例如 ``refs/west/foo``)。
与 ``manifest-rev`` 不同,这些引用不是常规分支。West 的这种行为是实现细节;用户不应依赖这些引用的存在或行为。

私有仓库 (Private repositories)
********************************

您可以使用 west 从私有仓库获取。这没有什么 west 特定的内容。

``west update`` 命令在项目的 ``manifest-rev`` 分支必须更新为新获取的提交时,
本质上运行 ``git fetch YOUR_PROJECT_URL``。这取决于您的环境来确保获取成功。

您可以手动输入密码或使用 `Git 内置的任何凭据助手`_。
由于 Git 具有内置的凭据存储,因此不需要 west 特定的功能。

以下部分介绍了在不必输入密码的情况下运行 ``west update`` 的常见情况,以及如何排除故障。

.. _credential helpers built in to Git:
   https://git-scm.com/docs/gitcredentials

通过 HTTPS 获取 (Fetching via HTTPS)
=====================================

在 Windows 上从 GitHub 获取时,最新版本的 Git 会在图形窗口中提示您输入一次 GitHub 密码,
然后将其存储供将来使用(在默认安装中)。因此,在 Windows 上执行一次后,从 GitHub 进行
无密码获取应该可以"开箱即用"。

通常,您可以使用 "store" git 凭据助手将凭据存储在磁盘上。
有关详细信息,请参阅 `git-credential-store`_ 手册页。

要为工作空间中的所有仓库使用此助手,请运行:

.. code-block:: shell

   west forall -c "git config credential.helper store"

要仅为项目 ``foo`` 和 ``bar`` 使用此助手,请运行:

.. code-block:: shell

   west forall -c "git config credential.helper store" foo bar

要在您的计算机上默认使用此助手,请运行:

.. code-block:: shell

   git config --global credential.helper store

在 GitHub 上,您可以设置 `个人访问令牌`_ 来代替您的帐户密码。
(如果您的帐户启用了双因素身份验证,这可能是必需的,即使禁用了双因素身份验证,
这也可能比以纯文本形式存储您的帐户密码更可取。)

您可以使用 Git 凭据存储来使用 GitHub PAT(个人访问令牌)进行身份验证,如下所示:

.. code-block:: shell

   echo "https://x-access-token:$GH_TOKEN@github.com" >> ~/.git-credentials

如果您不想在文件系统上存储任何凭据,可以使用 `git-credential-cache`_ 临时将它们存储在内存中。

如果您设置了通过 SSH 获取,可以使用 Git URL 重写功能。以下命令指示 Git 对 GitHub 使用 SSH URL 而不是 HTTPS URL:

.. code-block:: shell

   git config --global url."git@github.com:".insteadOf "https://github.com/"

.. _git-credential-store:
   https://git-scm.com/docs/git-credential-store#_examples
.. _git-credential-cache:
   https://git-scm.com/docs/git-credential-cache
.. _personal access token:
   https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token

通过 SSH 获取 (Fetching via SSH)
=================================

如果您的 SSH 密钥没有密码,获取应该可以正常工作。如果它有密码,
您可以使用 `ssh-agent`_ 避免每次都手动输入密码。

在 GitHub 上,有关配置和密钥创建的详细信息,请参阅 `使用 SSH 连接到 GitHub`_。

.. _ssh-agent:
   https://www.ssh.com/ssh/agent
.. _Connecting to GitHub with SSH:
   https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh

项目位置 (Project locations)
*****************************

项目可以位于工作空间内的任何位置,但它们不能"逃离"它。

换句话说,项目仓库不必位于清单仓库的子目录中或作为顶级目录的直接子目录。
但是,项目必须具有工作空间内的路径。
但是,项目必须具有工作空间内的路径。

您可以将工作空间内的项目仓库目录替换为指向计算机上其他位置的符号链接,但 west 不会为您执行此操作。

.. _west-topologies:

支持的拓扑结构 (Topologies supported)
**************************************

以下是 west 支持的示例源代码拓扑结构。

- T1: 星形拓扑,zephyr 是清单仓库
- T2: 星形拓扑,Zephyr 应用程序是清单仓库
- T3: 森林拓扑,独立的清单仓库

T1: 星形拓扑,zephyr 是清单仓库
===============================

- zephyr 仓库充当中央仓库,并在其 :file:`west.yml` 中指定其 :ref:`模块 <modules>`
- 与现有机制的类比:Git 子模块,zephyr 作为超级项目

这是默认设置。有关主线 Zephyr 如何作为此拓扑结构的示例,请参阅 :ref:`west-workspace`。

.. _west-t2:

T2: 星形拓扑,应用程序是清单仓库
================================

- 对于那些专注于单个应用程序的人很有用
- 包含 Zephyr 应用程序的仓库充当中央仓库,并在其 :file:`west.yml` 中命名构建它所需的其他项目。
  这包括 zephyr 仓库和任何模块。
- 与现有机制的类比:Git 子模块,应用程序作为超级项目,zephyr 和其他项目作为子模块

使用此拓扑结构的工作空间如下所示:

.. code-block:: none

   west-workspace/
   │
   ├── application/         # .git/     │
   │   ├── CMakeLists.txt               │
   │   ├── prj.conf                     │  never modified by west
   │   ├── src/                         │
   │   │   └── main.c                   │
   │   └── west.yml         # main manifest with optional import(s) and override(s)
   │                                    │
   ├── modules/
   │   └── lib/
   │       └── zcbor/       # .git/ project from either the main manifest or some import.
   │
   └── zephyr/              # .git/ project
       └── west.yml         # This can be partially imported with lower precedence or ignored.
                            # Only the 'manifest-rev' version can be imported.


以下是一个 :file:`application/west.yml` 示例,它使用 :ref:`west-manifest-import`
(自 west 0.7 起可用)将 Zephyr v2.5.0 及其模块导入应用程序清单文件:

.. code-block:: yaml

   # Example T2 west.yml, using manifest imports.
   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
     projects:
       - name: zephyr
         remote: zephyrproject-rtos
         revision: v2.5.0
         import: true
     self:
       path: application

如果以这种方式使用 ``import:``,您仍然可以有选择地"覆盖"各个 Zephyr 模块;
有关示例,请参阅 :ref:`west-manifest-ex1.3`。

另一种做同样事情的方法是将 :file:`zephyr/west.yml` 复制/粘贴到 :file:`application/west.yml`,
为 zephyr 项目本身添加一个条目,如下所示:

.. code-block:: yaml

   # Equivalent to the above, but with manually maintained Zephyr modules.
   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
     defaults:
       remote: zephyrproject-rtos
     projects:
       - name: zephyr
         revision: v2.5.0
         west-commands: scripts/west-commands.yml
       - name: net-tools
         revision: some-sha-goes-here
         path: tools/net-tools
       # ... other Zephyr modules go here ...
     self:
       path: application

(``west-commands`` 用于 :ref:`west-build-flash-debug` 和其他 Zephyr 特定的
:ref:`west-extensions <west-extensions>`。使用 ``import`` 时不需要它。)

使用 ``import`` 的主要优势是不必单独跟踪导入项目的修订版本。
在上面的示例中,使用 ``import`` 意味着 Zephyr 的 :ref:`模块 <modules>` 版本会自动从
:file:`zephyr/west.yml` 修订版本中确定,而不必自己复制/粘贴(和维护)。

T3: 森林拓扑
============

- 对于那些支持多个独立应用程序或没有"中央"仓库的下游分发的人很有用
- 一个不包含 Zephyr 源代码的专用清单仓库,并指定所有处于同一"级别"的项目列表
- 与现有机制的类比:基于 Google repo 的源代码分发

使用此拓扑结构的工作空间如下所示:

.. code-block:: none

   west-workspace/
   ├── app1/               # .git/ project
   │   ├── CMakeLists.txt
   │   ├── prj.conf
   │   └── src/
   │       └── main.c
   ├── app2/               # .git/ project
   │   ├── CMakeLists.txt
   │   ├── prj.conf
   │   └── src/
   │       └── main.c
   ├── manifest-repo/      # .git/ never modified by west
   │   └── west.yml        # main manifest with optional import(s) and override(s)
   ├── modules/
   │   └── lib/
   │       └── zcbor/      # .git/ project from either the main manifest or
   │                       #       from some import
   │
   └── zephyr/             # .git/ project
       └── west.yml        # This can be partially imported with lower precedence or ignored.
                           # Only the 'manifest-rev' version can be imported.

以下是一个 T3 :file:`manifest-repo/west.yml` 示例,它使用 :ref:`west-manifest-import`
(自 west 0.7 起可用)导入 Zephyr v2.5.0 及其模块,然后添加 ``app1`` 和 ``app2`` 项目:

.. code-block:: yaml

   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
       - name: your-git-server
         url-base: https://git.example.com/your-company
     defaults:
       remote: your-git-server
     projects:
       - name: zephyr
         remote: zephyrproject-rtos
         revision: v2.5.0
         import: true
       - name: app1
         revision: SOME_SHA_OR_BRANCH_OR_TAG
       - name: app2
         revision: ANOTHER_SHA_OR_BRANCH_OR_TAG
     self:
       path: manifest-repo

您也可以通过复制/粘贴 :file:`zephyr/west.yml` 来"手动"完成此操作,
如 T2 拓扑的 :ref:`上述 <west-t2>` 所示,具有相同的注意事项。

.. _workspace-as-git-repo:

不支持:工作空间顶级目录作为 .git 仓库
***************************************

一些用户要求支持将工作空间 :ref:`topdir <west-workspace>` 设为 git 仓库,如下例所示:

.. code-block:: none

   my-workspace/                  # workspace topdir
   ├── .git/                      # puts the entire workspace in a git repository
   ├── .west/                     # marks the location of the topdir
   └── [ ... other projects ...]

这 **不是** 官方支持的拓扑结构。作为设计决策,west 假定工作空间顶级目录本身不是 git 仓库。

您可能能够让类似的东西为您自己和您自己的目标"工作"。但是,west 的未来版本可能包含可能"破坏"您的设置的更改。
