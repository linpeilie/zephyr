.. _west-manifests:

West 清单文件 (West Manifests)
##################################

本页面包含关于 west 的多仓库模型 (multiple repository model)、清单文件 (manifest files) 以及 ``west manifest`` 命令的详细信息。有关 ``west.manifest`` 模块的 API 文档,请参阅 :ref:`west-apis-manifest`。有关更通用的介绍和命令概览,请参阅 :ref:`west-basics`。

.. only:: html

   .. contents::
      :depth: 3

.. _west-mr-model:

多仓库模型 (Multiple Repository Model)
*****************************************

West 对 :term:`west workspace` 中仓库及其历史记录的视图如下图所示(尽管此示例的某些部分特定于上游 Zephyr 对 west 的使用):

.. figure:: west-mr-model.png
   :align: center
   :alt: West 多仓库历史
   :figclass: align-center

   West 多仓库历史

清单仓库 (manifest repository) 的历史记录是"漂浮"在灰色平面之上的 Git 提交线。父提交使用实线箭头指向子提交。下面的平面包含工作空间中仓库的 Git 提交历史,每个项目仓库都用矩形框起来。每个仓库中的父/子提交关系也用实线箭头表示。

清单仓库中的提交(对于上游 Zephyr 来说,这是 zephyr 仓库本身)都有一个清单文件。每个提交中的清单文件指定了它期望在每个项目仓库中对应的提交。这种关系在图中用虚线箭头表示。每个虚线箭头从清单仓库中的提交指向项目仓库中的相应提交。

请注意以下重要细节:

- 项目可以被添加(如清单仓库提交 ``D`` 和 ``E`` 之间的 ``P1``)和删除(同样在这两个清单仓库提交之间的 ``P2``)

- 项目和清单仓库的历史记录不必一起向前或向后移动:

  - ``P2`` 在 ``A → B`` 期间保持不变,``P1`` 和 ``P3`` 在 ``F → G`` 期间也是如此。
  - ``P3`` 在 ``A → B`` 期间向前移动。
  - ``P3`` 在 ``C → D`` 期间向后移动。

  向后移动项目历史记录的一个用途是通过返回到引入回归之前的修订版本来"回退"回归。

- 项目仓库提交可以被"跳过": ``P3`` 在 ``B → C`` 期间在其历史记录中向前移动了多个提交。

- 在上图中,没有项目仓库在"同一时间"有两个修订版本:每个清单文件都只引用它所关心的项目中的一个确切提交。通过使用分支名称作为清单修订版本可以放宽这一点,代价是能够对清单仓库历史记录进行二分查找。

.. _west-manifest-files:

清单文件 (Manifest Files)
****************************

West 清单是 YAML 文件。清单有一个顶级 ``manifest`` 部分,包含一些子部分,如下所示:

.. code-block:: yaml

   manifest:
     remotes:
       # short names for project URLs
     projects:
       # a list of projects managed by west
     defaults:
       # default project attributes
     self:
       # configuration related to the manifest repository itself,
       # i.e. the repository containing west.yml
     version: "<schema-version>"
     group-filter:
       # a list of project groups to enable or disable

就 YAML 术语而言,清单文件包含一个映射 (mapping),具有一个 ``manifest`` 键。任何其他键及其内容都会被忽略(west v0.5 还需要一个 ``west`` 键,但从 v0.6 开始被忽略)。

清单包含子部分,如 ``defaults``、``remotes``、``projects`` 和 ``self``。就 YAML 术语而言,``manifest`` 键的值也是一个映射,这些"子部分"作为键。从 west v0.10 开始,所有这些"子部分"键都是可选的。

``projects`` 值是 west 管理的仓库及相关元数据的列表。我们很快会讨论它,但首先我们将描述 ``remotes`` 部分,它可用于在 ``projects`` 列表中节省输入。

远程仓库 (Remotes)
=====================

``remotes`` 子部分包含一个序列,指定可以从中获取项目的基本 URL。

每个 ``remotes`` 元素都有一个名称和一个"URL 基础"。这些用于为每个项目形成完整的 Git 获取 URL。可以通过将项目特定的路径附加到远程 URL 基础来设置项目的获取 URL。(正如我们将在下面看到的,项目也可以指定其完整的获取 URL。)

例如:

.. code-block:: yaml

   manifest:
     # ...
     remotes:
       - name: remote1
         url-base: https://git.example.com/base1
       - name: remote2
         url-base: https://git.example.com/base2

``remotes`` 的键及其用法如下表所示。

.. list-table:: remotes 键
   :header-rows: 1
   :widths: 1 5

   * - 键
     - 描述

   * - ``name``
     - 必需;远程仓库的唯一名称。

   * - ``url-base``
     - 添加到具有此远程仓库的每个项目的获取 URL 的前缀。

在上面的示例中,定义了两个远程仓库,名称分别为 ``remote1`` 和 ``remote2``。它们的 URL 基础分别为 ``https://git.example.com/base1`` 和 ``https://git.example.com/base2``。您也可以使用 SSH URL 基础;例如,如果 ``remote1`` 也支持通过 SSH 进行 Git 操作,您可以使用 ``git@example.com:base1``。任何 Git 可接受的内容都可以使用。

.. _west-manifests-projects:

项目 (Projects)
==================

``projects`` 子部分包含一个序列,描述 west 工作空间中的项目仓库。每个项目都有一个唯一的名称。您可以指定克隆和获取项目时使用的 Git 远程 URL、要跟踪的修订版本以及项目应存储在本地文件系统中的位置。请注意,west 项目 :ref:`与模块不同 <modules-vs-projects>`。

这是一个示例。我们将假设使用上面给出的 ``remotes``。

.. Note: if you change this example, keep the equivalent manifest below in
   sync.

.. code-block:: yaml

   manifest:
     # [... same remotes as above...]
     projects:
       - name: proj1
         description: the first example project
         remote: remote1
         path: extra/project-1
       - name: proj2
         description: |
           A multi-line description of the second example
           project.
         repo-path: my-path
         remote: remote2
         revision: v1.3
       - name: proj3
         url: https://github.com/user/project-three
         revision: abcde413a111

在此清单中:

- ``proj1`` 的远程仓库为 ``remote1``,因此其 Git 获取 URL 为 ``https://git.example.com/base1/proj1``。远程 ``url-base`` 与项目 ``name`` 之间用 ``/`` 连接以形成 URL。

  在本地,此项目将被克隆到相对于 west 工作空间根目录的路径 ``extra/project-1``,因为它有一个具有此值的显式 ``path`` 属性。

  由于该项目没有指定 ``revision``,默认使用 ``master``。当 west 下次更新此项目时,将获取此分支的当前提示并作为分离的 ``HEAD`` 检出。

- ``proj2`` 有一个 ``remote`` 和一个 ``repo-path``,因此其获取 URL 为 ``https://git.example.com/base2/my-path``。``repo-path`` 属性(如果存在)在形成获取 URL 时会覆盖默认的 ``name``。

  由于该项目没有 ``path`` 属性,默认使用其 ``name``。它将被克隆到名为 ``proj2`` 的目录中。当 west 更新项目时,将检出 ``v1.3`` 标签指向的提交。

- ``proj3`` 有一个显式的 ``url``,因此将从 ``https://github.com/user/project-three`` 获取。

  其本地路径默认为其名称 ``proj3``。下次更新时将检出提交 ``abcde413a111``。

可用的项目键及其用法如下表所示。有时我们会引用 ``defaults`` 子部分;它将在下一节中描述。

.. list-table:: projects 元素的键
   :header-rows: 1
   :widths: 1 5

   * - 键
     - 描述

   * - ``name``
     - 必需;项目的唯一名称。名称不能是保留值"west"或"manifest"之一。名称在清单文件中必须是唯一的。

   * - ``description``
     - 可选,项目的信息性描述。在 west v1.2.0 中添加。

   * - ``remote``, ``url``
     - 必需(二者之一,但不能同时使用)。

       如果项目有 ``remote``,则该远程仓库的 ``url-base`` 将与项目的 ``name``(或 ``repo-path``,如果有的话)组合以形成获取 URL。

       如果项目有 ``url``,那就是远程 Git 仓库的完整获取 URL。

       如果项目两者都没有,``defaults`` 部分必须指定 ``remote``,它将用作项目的远程仓库。否则,清单无效。

   * - ``repo-path``
     - 可选。如果给定,这将与远程的 ``url-base`` 连接,而不是项目的 ``name`` 来形成其获取 URL。项目不能同时具有 ``url`` 和 ``repo-path`` 属性。

   * - ``revision``
     - 可选。``west update`` 应该检出的 Git 修订版本。默认情况下,这将作为分离的 HEAD 检出,以避免与本地分支名称冲突。如果未给出,将使用 ``defaults`` 子部分中的 ``revision`` 值(如果存在)。

       项目修订版本可以是分支、标签或 SHA。

       如果未另行指定,默认 ``revision`` 为 ``master``。

       使用 ``HEAD~0`` [#f1]_ 作为 ``revision`` 将导致 west 保持项目的当前状态。

   * - ``path``
     - 可选。指定在本地克隆仓库的相对路径,相对于 west 工作空间中的顶级目录。如果缺失,项目的 ``name`` 将用作目录名。

   * - ``clone-depth``
     - 可选。如果给定,一个正整数,它会在克隆的仓库中创建一个浅历史记录,限制为给定的提交数量。只有当 ``revision`` 是分支或标签时才能使用此选项。

   * - ``west-commands``
     - 可选。如果给定,是项目中 YAML 文件的相对路径,该文件描述了该项目提供的其他 west 命令。按照惯例,此文件名为 :file:`west-commands.yml`。详见 :ref:`west-extensions`。

   * - ``import``
     - 可选。如果为 ``true``,则从给定仓库中的清单文件导入项目到当前清单。详见 :ref:`west-manifest-import`。

   * - ``groups``
     - 可选,项目所属的组列表。详见 :ref:`west-manifest-groups`。

   * - ``submodules``
     - 可选。您可以使用此选项使 ``west update`` 也更新项目定义的 `Git submodules`_。详见 :ref:`west-manifest-submodules`。

   * - ``userdata``
     - 可选。该值是任意的 YAML 值。详见 :ref:`west-project-userdata`。

.. rubric:: 脚注

.. [#f1] 在 git 中,HEAD 是一个引用,而 HEAD~<n> 是一个有效的修订版本但不是引用。West 获取引用,如 refs/heads/main 或 HEAD,以及本地不可用的提交,但如果提交在本地已经可用,则不会获取它们。HEAD~0 被解析为本地可用的特定提交,因此 west 将简单地检出由 HEAD~0 标识的本地可用提交。

.. _Git submodules: https://git-scm.com/book/en/v2/Git-Tools-Submodules

默认值 (Defaults)
====================

``defaults`` 子部分可以为项目属性提供默认值。特别是,可以在这里指定默认的远程仓库名称和修订版本。使用 ``defaults`` 编写我们一直在描述的相同清单的另一种方法是:

.. code-block:: yaml

   manifest:
     defaults:
       remote: remote1
       revision: v1.3

     remotes:
       - name: remote1
         url-base: https://git.example.com/base1
       - name: remote2
         url-base: https://git.example.com/base2

     projects:
       - name: proj1
         description: the first example project
         path: extra/project-1
         revision: master
       - name: proj2
         description: |
           A multi-line description of the second example
           project.
         repo-path: my-path
         remote: remote2
       - name: proj3
         url: https://github.com/user/project-three
         revision: abcde413a111

可用的 ``defaults`` 键及其用法如下表所示。

.. list-table:: defaults 键
   :header-rows: 1
   :widths: 1 5

   * - 键
     - 描述

   * - ``remote``
     - 可选。如果项目没有设置 ``url`` 或 ``remote`` 键,则将使用此值作为项目的 ``remote``。

   * - ``revision``
     - 可选。如果项目没有设置修订版本,则将使用此值。如果未给出,默认值为 ``master``。

自身 (Self)
=============

``self`` 子部分可用于控制清单仓库本身。

作为示例,让我们考虑 zephyr 仓库的 :file:`west.yml` 中的这个片段:

.. code-block:: yaml

   manifest:
     # ...
     self:
       path: zephyr
       west-commands: scripts/west-commands.yml

这确保 zephyr 仓库被克隆到路径 ``zephyr`` 中,尽管如上所述,如果从默认清单 URL ``https://github.com/zephyrproject-rtos/zephyr`` 克隆,无论如何都会发生这种情况。由于 zephyr 仓库确实包含扩展命令,其 ``self`` 条目声明了相应的 :file:`west-commands.yml` 相对于仓库根目录的位置。

可用的 ``self`` 键及其用法如下表所示。

.. list-table:: self 键
   :header-rows: 1
   :widths: 1 5

   * - 键
     - 描述

   * - ``path``
     - 可选。``west init`` 应将清单仓库克隆到的路径,相对于 west 工作空间的顶级目录。

       如果未给出,默认情况下将使用清单仓库 URL 中路径组件的基本名称。例如,如果 URL 是 ``https://git.example.com/project-repo``,清单仓库将被克隆到目录 :file:`project-repo`。

   * - ``west-commands``
     - 可选。这类似于项目序列元素中的同名键。

   * - ``import``
     - 可选。这也类似于 ``projects`` 键,但允许从清单仓库中的其他文件导入项目。详见 :ref:`west-manifest-import`。

.. _west-manifest-schema-version:

版本 (Version)
================

``version`` 子部分声明清单文件使用了在某个 west 版本中引入的功能。尝试使用较旧版本的 west 加载清单将失败,并显示错误消息,说明所需的 west 最低版本。

这是一个示例:

.. code-block:: yaml

   manifest:
     # 标记此文件使用 west 清单文件格式的 0.10 版本。
     #
     # 尝试使用 west v0.8.0 加载此清单文件将失败,
     # 并显示错误消息,说明需要 west v0.10.0 或更高版本。
     version: "0.10"

`west 源代码仓库`_ 中的 pykwalify 模式 :file:`manifest-schema.yml` 用于验证清单部分。

.. _west source code repository:
   https://github.com/zephyrproject-rtos/west

以下是一个包含有效 ``version`` 值的表格,以及有关该版本中引入的清单文件功能的信息。

.. list-table::
   :header-rows: 1
   :widths: 1 4

   * - ``version``
     - 新功能

   * - ``"0.7"``
     - 对 ``version`` 功能的初始支持。此表中未另行提及的所有清单文件功能都是在 west v0.7.0 或更早版本中引入的。

   * - ``"0.8"``
     - 支持 ``import: path-prefix:`` (:ref:`west-manifest-import-map`)

   * - ``"0.9"``
     - **不建议使用 west v0.9.x**。

       提供此模式版本以允许用户显式请求与 west :ref:`west_0_9_0` 的兼容性。但是,west :ref:`west_0_10_0` 及更高版本对于 west v0.9.0 中引入的功能具有不兼容的行为。如果可能,您应该忽略版本"0.9"。

   * - ``"0.10"``

     - 支持:

       - ``projects:`` 中的 ``submodules:`` (:ref:`west-manifest-submodules`)
       - ``manifest: group-filter:`` 和 ``projects:`` 中的 ``groups:`` (:ref:`west-manifest-groups`)
       - ``import:`` 功能现在支持 ``allowlist:`` 和 ``blocklist:``;作为 Zephyr 全面包容性语言更改的一部分,建议将它们分别作为旧名称的替代品。为了向后兼容,仍然支持旧的键名。(:ref:`west-manifest-import`, :ref:`west-manifest-import-map`)

   * - ``"0.12"``
     - 支持 ``projects:`` 中的 ``userdata:`` (:ref:`west-project-userdata`)

   * - ``"0.13"``
     - 支持 ``self: userdata:`` (:ref:`west-project-userdata`)

   * - ``"1.0"``
     - 与 ``"0.13"`` 相同,但可供不希望使用 ``"0.x"`` 版本字段的用户使用。

   * - ``"1.2"``
     - 支持 ``projects:`` 中的 ``description:`` (:ref:`west-manifests-projects`)

.. note::

   没有在清单文件格式中引入新功能的 west 版本不会更改有效 ``version`` 值的列表。例如,``version: "0.11"`` 是**无效的**,因为 west v0.11.x 没有引入新的清单文件格式功能。

如上所示,将 ``version`` 值加上引号会强制 YAML 解析器将其视为字符串。如果没有引号,YAML 中的 ``0.10`` 只是浮点值 ``0.1``。如果值在转换为字符串时相同,您可以省略引号,但最好包含它们。如果不确定,请始终使用引号。

如果您的清单中不包含 ``version``,每个新版本的 west 都会假设它应该尝试使用该版本中可用的功能来加载它。如果该版本的 west 太旧而无法加载清单,这可能会导致更难理解的错误消息。

组过滤器 (Group-filter)
==========================

详见 :ref:`west-manifest-groups`。

.. _west-active-inactive-projects:

活动和非活动项目 (Active and Inactive Projects)
**************************************************

west 清单中定义的项目可以是*非活动的*或*活动的*。区别在于非活动项目通常会被 west 忽略。例如,``west update`` 不会更新非活动项目,``west list`` 默认情况下不会打印有关它们的信息。再比如,非活动项目中的任何 :ref:`west-manifest-import` 都会被 west 忽略。

有两种方法可以使项目非活动:

1. 使用 ``manifest.project-filter`` 配置选项。如果使用此选项使项目处于活动或非活动状态,则与使用其 ``groups:`` 使项目非活动相关的规则将被忽略。也就是说,如果 ``manifest.project-filter`` 中的正则表达式适用于项目,则项目的组对其是否处于活动或非活动状态没有影响。

   有关详细信息,请参阅 :ref:`west-config-index` 中此选项的条目。

2. 否则,如果项目有组,并且它们都被禁用,则该项目是非活动的。

   详见以下部分。

.. _west-manifest-groups:

项目组 (Project Groups)
**************************

您可以使用 :ref:`上面 <west-manifest-files>` 简要描述的 ``groups`` 和 ``group-filter`` 键将项目放入组中,并启用或禁用组。

例如,这允许您使用 ``west forall --group`` 仅在组中的项目上运行 ``west forall`` 命令。这也可以让您使项目非活动;有关非活动项目的更多信息,请参阅上一节。

下一节介绍项目组。以下部分描述 :ref:`west-enabled-disabled-groups`。:ref:`west-project-group-examples` 中有一些基本示例。最后,:ref:`west-group-filter-imports` 提供了 ``group-filter`` 如何与 :ref:`west-manifest-import` 功能交互的简化概述。

组基础知识 (Groups Basics)
==============================

``groups:`` 和 ``group-filter:`` 键在清单中如下所示:

.. code-block:: yaml

   manifest:
     projects:
       - name: some-project
         groups: ...
     group-filter: ...

``groups`` 键的值是组名列表。组名是字符串。

您可以使用 ``group-filter`` 启用或禁用项目组。所有组都被禁用且未通过 ``manifest.project-filter`` 配置选项使其处于活动状态的项目是非活动的。

例如,在此清单片段中:

.. code-block:: yaml

  manifest:
    projects:
      - name: project-1
        groups:
          - groupA
      - name: project-2
        groups:
          - groupB
          - groupC
      - name: project-3

项目所在的组为:

- ``project-1``: 一个组,名为 ``groupA``
- ``project-2``: 两个组,名为 ``groupB`` 和 ``groupC``
- ``project-3``: 没有组

项目组名称不得包含逗号 (,)、冒号 (:) 或空格。

组名不得以短横线 (-) 或加号 (+) 开头,但它们可以在名称的其他位置包含这些字符。例如,``foo-bar`` 和 ``foo+bar`` 是有效的组,但 ``-foobar`` 和 ``+foobar`` 无效。

组名在其他方面是任意字符串。组名区分大小写。

作为限制,任何项目都不能同时使用 ``import:`` 和 ``groups:``。(这对于避免某些病态的边缘情况是必要的。)

.. _west-enabled-disabled-groups:

已启用和已禁用的项目组 (Enabled and Disabled Project Groups)
================================================================

默认情况下,所有项目组都是启用的。您可以在清单文件和 :ref:`west-config` 中启用或禁用组。

在清单文件中,``manifest: group-filter:`` 是一个要启用和禁用的组的 YAML 列表。

要启用组,请在其名称前加上加号 (+)。例如,在此清单片段中,``groupA`` 已启用:

.. code-block:: yaml

   manifest:
     group-filter: [+groupA]

尽管这对于默认已启用的组来说是多余的,但它可用于覆盖导入的清单文件中的设置。有关更多信息,请参阅 :ref:`west-group-filter-imports`。

要禁用组,请在其名称前加上短横线 (-)。例如,在此清单片段中,``groupA`` 和 ``groupB`` 已禁用:

.. code-block:: yaml

   manifest:
     group-filter: [-groupA,-groupB]

.. note::

   由于 ``group-filter`` 是一个 YAML 列表,您可以这样编写此片段:

   .. code-block:: yaml

      manifest:
        group-filter:
          - -groupA
          - -groupB

   但是,这种语法更难阅读,因此不建议使用。

除了清单文件之外,您还可以使用 ``manifest.group-filter`` 配置选项控制启用和禁用哪些组。此选项是要启用和/或禁用的组的逗号分隔列表。

要启用组,请将其名称以 ``+`` 为前缀添加到列表中。要禁用组,请添加以 ``-`` 为前缀的名称。例如,将 ``manifest.group-filter`` 设置为 ``+groupA,-groupB`` 会启用 ``groupA`` 并禁用 ``groupB``。

配置选项的值会覆盖清单文件中的任何数据。您可以将其视为 ``manifest.group-filter`` 配置选项被附加到 YAML 中的 ``manifest: group-filter:`` 列表,并具有"最后一个条目获胜"的语义。

.. _west-project-group-examples:

项目组示例 (Project Group Examples)
======================================

本节包含涉及项目组和活动项目的示例情况。这些示例使用 ``manifest: group-filter:`` YAML 列表和 ``manifest.group-filter`` 配置列表,以展示它们如何协同工作。

请注意,以下清单中的 ``defaults`` 和 ``remotes`` 数据与使示例完整和独立无关。

.. note::

   在以下所有示例中,假设 ``manifest.project-filter`` 选项未设置。

示例 1: 没有禁用的组 (Example 1: no disabled groups)
---------------------------------------------------------

整个清单文件是:

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
         groups:
           - groupA
       - name: bar
         groups:
           - groupA
           - groupB
       - name: baz

     defaults:
       remote: example-remote
     remotes:
       - name: example-remote
         url-base: https://git.example.com

``manifest.group-filter`` 配置选项未设置(您可以通过运行 ``west config -D manifest.group-filter`` 来确保这一点)。

没有组被禁用,因为默认情况下所有组都是启用的。因此,所有三个项目(``foo``、``bar`` 和 ``baz``)都是活动的。请注意,没有办法使项目 ``baz`` 非活动,因为它没有组。

示例 2: 通过清单禁用一个组 (Example 2: Disabling one group via manifest)
-----------------------------------------------------------------------------

整个清单文件是:

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
         groups:
           - groupA
       - name: bar
         groups:
           - groupA
           - groupB

     group-filter: [-groupA]

     defaults:
       remote: example-remote
     remotes:
       - name: example-remote
         url-base: https://git.example.com

``manifest.group-filter`` 配置选项未设置(您可以通过运行 ``west config -D manifest.group-filter`` 来确保这一点)。

由于 ``groupA`` 被禁用,项目 ``foo`` 是非活动的。项目 ``bar`` 是活动的,因为 ``groupB`` 已启用。

示例 3: 通过清单禁用多个组 (Example 3: Disabling multiple groups via manifest)
-----------------------------------------------------------------------------------

整个清单文件是:

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
         groups:
           - groupA
       - name: bar
         groups:
           - groupA
           - groupB

     group-filter: [-groupA,-groupB]

     defaults:
       remote: example-remote
     remotes:
       - name: example-remote
         url-base: https://git.example.com

``manifest.group-filter`` 配置选项未设置(您可以通过运行 ``west config -D manifest.group-filter`` 来确保这一点)。

``foo`` 和 ``bar`` 都是非活动的,因为它们的所有组都被禁用了。

示例 4: 通过配置禁用组 (Example 4: Disabling a group via configuration)
--------------------------------------------------------------------------

整个清单文件是:

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
         groups:
           - groupA
       - name: bar
         groups:
           - groupA
           - groupB

     defaults:
       remote: example-remote
     remotes:
       - name: example-remote
         url-base: https://git.example.com

``manifest.group-filter`` 配置选项设置为 ``-groupA``(您可以通过运行 ``west config manifest.group-filter -- -groupA`` 来确保这一点;额外的 ``--`` 是必需的,以便参数解析器不会将 ``-groupA`` 视为命令行选项 ``-g`` 且值为 ``roupA``)。

项目 ``foo`` 是非活动的,因为 ``groupA`` 已通过 ``manifest.group-filter`` 配置选项禁用。项目 ``bar`` 是活动的,因为 ``groupB`` 已启用。

示例 5: 通过配置覆盖已禁用的组 (Example 5: Overriding a disabled group via configuration)
-----------------------------------------------------------------------------------------------

整个清单文件是:

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
       - name: bar
         groups:
           - groupA
       - name: baz
         groups:
           - groupA
           - groupB

     group-filter: [-groupA]

     defaults:
       remote: example-remote
     remotes:
       - name: example-remote
         url-base: https://git.example.com

``manifest.group-filter`` 配置选项设置为 ``+groupA``(您可以通过运行 ``west config manifest.group-filter +groupA`` 来确保这一点)。

在这种情况下,``groupA`` 已启用:``manifest.group-filter`` 配置选项的优先级高于清单文件中的 ``manifest: group-filter: [-groupA]`` 内容。

因此,项目 ``foo`` 和 ``bar`` 都是活动的。

示例 6: 通过配置覆盖多个已禁用的组 (Example 6: Overriding multiple disabled groups via configuration)
----------------------------------------------------------------------------------------------------------

整个清单文件是:

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
       - name: bar
         groups:
           - groupA
       - name: baz
         groups:
           - groupA
           - groupB

     group-filter: [-groupA,-groupB]

     defaults:
       remote: example-remote
     remotes:
       - name: example-remote
         url-base: https://git.example.com

``manifest.group-filter`` 配置选项设置为 ``+groupA,+groupB``(您可以通过运行 ``west config manifest.group-filter "+groupA,+groupB"`` 来确保这一点)。

在这种情况下,``groupA`` 和 ``groupB`` 都已启用,因为配置值会覆盖清单文件中的两个组。

因此,项目 ``foo`` 和 ``bar`` 都是活动的。

示例 7: 通过配置禁用多个组 (Example 7: Disabling multiple groups via configuration)
--------------------------------------------------------------------------------------

整个清单文件是:

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
       - name: bar
         groups:
           - groupA
       - name: baz
         groups:
           - groupA
           - groupB

     defaults:
       remote: example-remote
     remotes:
       - name: example-remote
         url-base: https://git.example.com

``manifest.group-filter`` 配置选项设置为 ``-groupA,-groupB``(您可以通过运行 ``west config manifest.group-filter -- "-groupA,-groupB"`` 来确保这一点)。

在这种情况下,``groupA`` 和 ``groupB`` 都被禁用。

因此,项目 ``foo`` 和 ``bar`` 都是非活动的。

.. _west-group-filter-imports:

组过滤器和导入 (Group Filters and Imports)
============================================

本节提供了 ``manifest: group-filter:`` 值与 :ref:`west-manifest-import` 结合使用时的简化描述。有关完整详细信息,请参阅 :ref:`west-manifest-formal`。

.. warning::

   以下语义适用于 west v0.10.0 及更高版本。West v0.9.x 的语义不同,不建议在 west v0.9.x 中将 ``group-filter`` 与 ``import`` 结合使用。

简而言之:

- 如果您只导入一个清单,它在其 ``group-filter`` 中禁用的任何组在您的清单中也被禁用
- 您可以在清单文件的 ``manifest: group-filter:`` 值、工作空间的 ``manifest.group-filter`` 配置选项或两者中覆盖此设置

以下是一些示例。

示例 1: 没有覆盖 (Example 1: no overrides)
----------------------------------------------

您正在使用这个 :file:`parent/west.yml` 清单:

.. code-block:: yaml

   # parent/west.yml:
   manifest:
     projects:
       - name: child
         url: https://git.example.com/child
         import: true
       - name: project-1
         url: https://git.example.com/project-1
         groups:
           - unstable

:file:`child/west.yml` 包含:

.. code-block:: yaml

   # child/west.yml:
   manifest:
     group-filter: [-unstable]
     projects:
       - name: project-2
         url: https://git.example.com/project-2
       - name: project-3
         url: https://git.example.com/project-3
         groups:
           - unstable

在解析的清单中,只有 ``child`` 和 ``project-2`` 是活动的。

``unstable`` 组在 :file:`child/west.yml` 中被禁用,并且在 :file:`parent/west.yml` 中没有被覆盖。因此,解析清单的最终 ``group-filter`` 为 ``[-unstable]``。

由于 ``project-1`` 和 ``project-3`` 在 ``unstable`` 组中且不在任何其他组中,因此它们是非活动的。

示例 2: 通过清单覆盖导入的 ``group-filter`` (Example 2: overriding an imported ``group-filter`` via manifest)
----------------------------------------------------------------------------------------------------------------

您正在使用这个 :file:`parent/west.yml` 清单:

.. code-block:: yaml

   # parent/west.yml:
   manifest:
     group-filter: [+unstable,-optional]
     projects:
       - name: child
         url: https://git.example.com/child
         import: true
       - name: project-1
         url: https://git.example.com/project-1
         groups:
           - unstable

:file:`child/west.yml` 包含:

.. code-block:: yaml

   # child/west.yml:
   manifest:
     group-filter: [-unstable]
     projects:
       - name: project-2
         url: https://git.example.com/project-2
         groups:
           - optional
       - name: project-3
         url: https://git.example.com/project-3
         groups:
           - unstable

只有 ``child``、``project-1`` 和 ``project-3`` 项目是活动的。

:file:`child/west.yml` 中的 ``[-unstable]`` 组过滤器在 :file:`parent/west.yml` 中被覆盖,因此 ``unstable`` 组已启用。由于 ``project-1`` 和 ``project-3`` 在 ``unstable`` 组中,因此它们是活动的。

同一个 :file:`parent/west.yml` 文件禁用了 ``optional`` 组,因此 ``project-2`` 是非活动的。

:file:`parent/west.yml` 指定的最终组过滤器为 ``[+unstable,-optional]``。

示例 3: 通过配置覆盖导入的 ``group-filter`` (Example 3: overriding an imported ``group-filter`` via configuration)
-----------------------------------------------------------------------------------------------------------------------

您正在使用这个 :file:`parent/west.yml` 清单:

.. code-block:: yaml

   # parent/west.yml:
   manifest:
     projects:
       - name: child
         url: https://git.example.com/child
         import: true
       - name: project-1
         url: https://git.example.com/project-1
         groups:
           - unstable

And :file:`child/west.yml` contains:

.. code-block:: yaml

   # child/west.yml:
   manifest:
     group-filter: [-unstable]
     projects:
       - name: project-2
         url: https://git.example.com/project-2
         groups:
           - optional
       - name: project-3
         url: https://git.example.com/project-3
         groups:
           - unstable

如果您运行:

.. code-block:: shell

   west config manifest.group-filter +unstable,-optional

则只有 ``child``、``project-1`` 和 ``project-3`` 项目是活动的。

:file:`child/west.yml` 中的 ``-unstable`` 组过滤器在 ``manifest.group-filter`` 配置选项中被覆盖,因此 ``unstable`` 组是启用的。由于 ``project-1`` 和 ``project-3`` 在 ``unstable`` 组中,因此它们是活动的。

同一配置选项禁用了 ``optional`` 组,因此 ``project-2`` 是非活动的。

:file:`parent/west.yml` 和 ``manifest.group-filter`` 配置选项指定的最终组过滤器是 ``[+unstable,-optional]``。

.. _west-manifest-submodules:

项目中的 Git 子模块 (Git Submodules in Projects)
***************************************************

您可以使用 :ref:`上面 <west-manifest-files>` 简要描述的 ``submodules`` 键来强制 ``west update`` 还处理项目 git 仓库中配置的任何 `Git submodules`_。``submodules`` 键可以出现在 ``projects`` 内部,如下所示:

.. code-block:: YAML

   manifest:
     projects:
       - name: some-project
         submodules: ...

``submodules`` 键可以是布尔值或映射列表。我们将按顺序描述这些。

选项 1: 布尔值 (Option 1: Boolean)
====================================

这是使用 ``submodules`` 的最简单方法。

如果 ``submodules`` 作为 ``projects`` 属性为 ``true``,``west update`` 将在更新项目本身时递归更新项目的 Git 子模块。如果它是 ``false`` 或缺失,则不起作用。

例如,假设您有一个源代码仓库 ``foo``,它有一些子模块,您希望 ``west update`` 将它们全部保持同步,同时在同一工作空间中还有另一个名为 ``bar`` 的项目。

您可以使用此清单文件来实现:

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
         submodules: true
       - name: bar

在这里,``west update`` 将初始化和更新 ``foo`` 中的所有子模块。如果 ``bar`` 有任何子模块,它们将被忽略,因为 ``bar`` 没有 ``submodules`` 值。

选项 2: 映射列表 (Option 2: List of mappings)
===============================================

``submodules`` 键可以是映射列表,每个所需子模块一个列表元素。列出的每个子模块都会递归更新。您仍然可以使用 ``git`` 命令手动跟踪和更新未列出的子模块;无论是否存在,west 都会完全忽略它们。

``path`` 键必须完全匹配一个子模块相对于其父 west 项目的路径,如 ``git submodule status`` 的输出中所示。``name`` 键是可选的,目前不被 west 使用;它也不会传递给 ``git submodule`` 命令。``name`` 键在 west 版本 0.9.0 中曾短暂地是强制性的,但在 0.9.1 中变为可选。

例如,假设您有一个源代码仓库 ``foo``,它有许多子模块,您希望 ``west update`` 保持其中一些但不是全部同步,同时在同一工作空间中还有另一个名为 ``bar`` 的项目。

您可以使用此清单文件来实现:

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
         submodules:
           - path: path/to/foo-first-sub
           - name: foo-second-sub
             path: path/to/foo-second-sub
       - name: bar

在这里,``west update`` 将递归初始化和更新 ``foo`` 中路径为 ``path/to/foo-first-sub`` 和 ``path/to/foo-second-sub`` 的子模块。``bar`` 中的任何子模块仍然被忽略。

.. _west-project-userdata:

仓库用户数据 (Repository user data)
*************************************

West 版本 v0.12 及更高版本支持项目中的可选 ``userdata`` 键。

West 版本 v0.13 及更高版本在 ``manifest: self:`` 部分支持此键。

它旨在供需要用户特定项目元数据的程序使用。除了将其解析为 YAML 之外,west 本身完全忽略该值。

键的值是任意 YAML。West 解析该值并使其作为相应 ``west.manifest.Project`` 对象的 ``userdata`` 属性通过 :ref:`west-apis` 可供程序访问。

示例清单片段:

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
       - name: bar
         userdata: a-string
       - name: baz
         userdata:
           key: value
     self:
       userdata: blub

示例 Python 用法:

.. code-block:: python

   manifest = west.manifest.Manifest.from_file()

   foo, bar, baz = manifest.get_projects(['foo', 'bar', 'baz'])

   foo.userdata # None
   bar.userdata # 'a-string'
   baz.userdata # {'key': 'value'}
   manifest.userdata # 'blub'

.. _west-manifest-import:

清单导入 (Manifest Imports)
*****************************

您可以使用上面简要描述的 ``import`` 键将其他清单文件中的项目包含到您的 :file:`west.yml` 中。此键可以是 ``project`` 或 ``self`` 部分属性:

.. code-block:: yaml

   manifest:
     projects:
       - name: some-project
         import: ...
     self:
       import: ...

您可以使用 "self: import:" 从包含 :file:`west.yml` 的仓库加载其他文件。您可以使用 "project: ... import:" 从该项目的 Git 历史记录中定义的其他文件加载。

West 按以下顺序从各个清单文件解析最终清单:

#. ``self`` 中的导入文件
#. 您的 :file:`west.yml` 文件
#. ``projects`` 中的导入文件

在解析过程中,west 会忽略已在其他文件中定义的项目。例如,您的 :file:`west.yml` 中名为 ``foo`` 的项目会使 west 忽略从 ``projects`` 列表中导入的其他名为 ``foo`` 的项目。

``import`` 键可以是布尔值、路径、映射或序列。我们将按顺序使用示例来描述这些:

- :ref:`布尔值 <west-manifest-import-bool>`
   - :ref:`west-manifest-ex1.1`
   - :ref:`west-manifest-ex1.2`
   - :ref:`west-manifest-ex1.3`
- :ref:`相对路径 <west-manifest-import-path>`
   - :ref:`west-manifest-ex2.1`
   - :ref:`west-manifest-ex2.2`
   - :ref:`west-manifest-ex2.3`
- :ref:`带有附加配置的映射 <west-manifest-import-map>`
   - :ref:`west-manifest-ex3.1`
   - :ref:`west-manifest-ex3.2`
   - :ref:`west-manifest-ex3.3`
   - :ref:`west-manifest-ex3.4`
- :ref:`路径和映射的序列 <west-manifest-import-seq>`
   - :ref:`west-manifest-ex4.1`
   - :ref:`west-manifest-ex4.2`

更 :ref:`正式的描述 <west-manifest-formal>` 将在示例之后最后给出。

故障排除说明 (Troubleshooting Note)
=====================================

如果您正在使用此功能并发现 west 的行为令人困惑,请尝试 :ref:`解析您的清单 <west-manifest-resolve>` 以查看导入完成后的最终结果。

.. _west-manifest-import-bool:

选项 1: 布尔值 (Option 1: Boolean)
====================================

这是使用 ``import`` 的最简单方法。

如果 ``import`` 作为 ``projects`` 属性为 ``true``,west 将从该项目根目录中的 :file:`west.yml` 文件导入项目。如果它是 ``false`` 或缺失,则不起作用。例如,此清单将从修订版本 ``v1.0`` 的 ``p1`` git 仓库导入 :file:`west.yml`:

.. code-block:: yaml

   manifest:
     # ...
     projects:
       - name: p1
         revision: v1.0
         import: true    # 从 p1 的 v1.0 git 标签导入 west.yml
       - name: p2
         import: false   # 不从 p2 导入任何内容。
       - name: p3        # 也不从 p3 导入任何内容。

在 ``self`` 内将 ``import`` 设置为 ``true`` 或 ``false`` 是错误的,如下所示:

.. code-block:: yaml

   manifest:
     # ...
     self:
       import: true  # 错误

.. _west-manifest-ex1.1:

示例 1.1: Zephyr 发行版的下游 (Example 1.1: Downstream of a Zephyr release)
-------------------------------------------------------------------------------

您有一个源代码仓库,希望与 Zephyr v1.14.1 LTS 一起使用。您想使用 west 维护整个项目。您不想修改任何主线仓库。

换句话说,您想要的 west 工作空间如下所示:

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
         submodules: true
       - name: bar

Here, ``west update`` will initialize and update all submodules in ``foo``. If
``bar`` has any submodules, they are ignored, because ``bar`` does not have a
``submodules`` value.

选项 2: 映射列表 (Option 2: List of mappings)
=============================================

``submodules`` 键可以是映射列表,每个列表元素对应一个所需的子模块。列出的每个子模块都会递归更新。您仍然可以使用 ``git`` 命令手动跟踪和更新未列出的子模块;无论是否存在,它们都将被 ``west`` 完全忽略。

``path`` 键必须完全匹配一个子模块相对于其父 west 项目的路径,如 ``git submodule status`` 的输出所示。``name`` 键是可选的,目前 west 不使用;它也不会传递给 ``git submodule`` 命令。``name`` 键在 west 版本 0.9.0 中曾短暂地是强制性的,但在 0.9.1 中变为可选。

例如,假设您有一个源代码仓库 ``foo``,它有许多子模块,您希望 ``west update`` 保持其中一些但不是全部同步,以及同一工作空间中另一个名为 ``bar`` 的项目。

您可以使用此清单文件实现:

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
         submodules:
           - path: path/to/foo-first-sub
           - name: foo-second-sub
             path: path/to/foo-second-sub
       - name: bar

Here, ``west update`` will recursively initialize and update just the
submodules in ``foo`` with paths ``path/to/foo-first-sub`` and
``path/to/foo-second-sub``. Any submodules in ``bar`` are still ignored.

.. _west-project-userdata:

仓库用户数据 (Repository user data)
************************************

West 版本 v0.12 及更高版本支持项目中的可选 ``userdata`` 键。

West 版本 v0.13 及更高版本在 ``manifest: self:`` 部分支持此键。

它用于需要用户特定项目元数据的程序。除了将其解析为 YAML 之外,west 本身完全忽略该值。

键的值是任意 YAML。West 解析该值并使其可供使用 :ref:`west-apis` 的程序作为相应 ``west.manifest.Project`` 对象的 ``userdata`` 属性访问。

示例清单片段:

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
       - name: bar
         userdata: a-string
       - name: baz
         userdata:
           key: value
     self:
       userdata: blub

Python 使用示例:

.. code-block:: python

   manifest = west.manifest.Manifest.from_file()

   foo, bar, baz = manifest.get_projects(['foo', 'bar', 'baz'])

   foo.userdata # None
   bar.userdata # 'a-string'
   baz.userdata # {'key': 'value'}
   manifest.userdata # 'blub'

.. _west-manifest-import:

Manifest Imports
清单导入 (Manifest Imports)
****************************

您可以使用上面简要描述的 ``import`` 键将其他清单文件中的项目包含到您的 :file:`west.yml` 中。此键可以是 ``project`` 或 ``self`` 部分的属性:

.. code-block:: yaml

   manifest:
     projects:
       - name: some-project
         import: ...
     self:
       import: ...

您可以使用"self: import:"从包含您的 :file:`west.yml` 的仓库加载其他文件。您可以使用"project: ... import:"来加载该项目 Git 历史中定义的其他文件。

West 按以下顺序从各个清单文件解析最终清单:

#. ``self`` 中导入的文件
#. 您的 :file:`west.yml` 文件
#. ``projects`` 中导入的文件

在解析期间,west 忽略已在其他文件中定义的项目。例如,:file:`west.yml` 中名为 ``foo`` 的项目会使 west 忽略从您的 ``projects`` 列表导入的其他名为 ``foo`` 的项目。

``import`` 键可以是布尔值、路径、映射或序列。我们将按顺序使用示例进行描述:

- :ref:`布尔值 <west-manifest-import-bool>`
   - :ref:`west-manifest-ex1.1`
   - :ref:`west-manifest-ex1.2`
   - :ref:`west-manifest-ex1.3`
- :ref:`Relative path <west-manifest-import-path>`
   - :ref:`west-manifest-ex2.1`
   - :ref:`west-manifest-ex2.2`
   - :ref:`west-manifest-ex2.3`
- :ref:`Mapping with additional configuration <west-manifest-import-map>`
   - :ref:`west-manifest-ex3.1`
   - :ref:`west-manifest-ex3.2`
   - :ref:`west-manifest-ex3.3`
   - :ref:`west-manifest-ex3.4`
- :ref:`Sequence of paths and mappings <west-manifest-import-seq>`
   - :ref:`west-manifest-ex4.1`
   - :ref:`west-manifest-ex4.2`

关于其工作原理的更 :ref:`正式描述 <west-manifest-formal>` 在示例之后。

故障排除提示 (Troubleshooting Note)
=====================================

如果您正在使用此功能并发现 west 的行为令人困惑,请尝试 :ref:`解析您的清单 <west-manifest-resolve>` 以查看导入完成后的最终结果。

.. _west-manifest-import-bool:

选项 1: 布尔值 (Option 1: Boolean)
====================================

这是使用 ``import`` 最简单的方法。

如果 ``import`` 作为 ``projects`` 属性为 ``true``,west 将从该项目根目录中的 :file:`west.yml` 文件导入项目。如果为 ``false`` 或缺失,则无效果。例如,此清单将从修订版本 ``v1.0`` 的 ``p1`` git 仓库导入 :file:`west.yml`:

.. code-block:: yaml

   manifest:
     # ...
     projects:
       - name: p1
         revision: v1.0
         import: true    # 从 p1 的 v1.0 git 标签导入 west.yml
       - name: p2
         import: false   # 不从 p2 导入任何内容。
       - name: p3        # 也不从 p3 导入任何内容。

在 ``self`` 内将 ``import`` 设置为 ``true`` 或 ``false`` 是错误的,如下所示:

.. code-block:: yaml

   manifest:
     # ...
     self:
       import: true  # 错误

.. _west-manifest-ex1.1:

示例 1.1: Zephyr 发行版的下游 (Example 1.1: Downstream of a Zephyr release)
-----------------------------------------------------------------------------

您有一个想与 Zephyr v1.14.1 LTS 一起使用的源代码仓库。您想使用 west 维护整个项目。您不想修改任何主线仓库。

换句话说,您想要的 west 工作空间如下所示:

.. code-block:: none

   my-downstream/
   ├── .west/                     # west 目录
   ├── zephyr/                    # mainline zephyr repository
   │   └── west.yml               # the v1.14.1 version of this file is imported
   ├── modules/                   # modules from mainline zephyr
   │   ├── hal/
   │   └── [...other directories..]
   ├── [ ... other projects ...]  # other mainline repositories
   └── my-repo/                   # your downstream repository
       ├── west.yml               # main manifest importing zephyr/west.yml v1.14.1
       └── [...other files..]

您可以使用以下 :file:`my-repo/west.yml` 来实现:

.. code-block:: yaml

   # my-repo/west.yml:
   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
     projects:
       - name: zephyr
         remote: zephyrproject-rtos
         revision: v1.14.1
         import: true

然后,您可以在计算机上创建工作空间,假设 ``my-repo`` 托管在 ``https://git.example.com/my-repo``:

.. code-block:: console

   west init -m https://git.example.com/my-repo my-downstream
   cd my-downstream
   west update

执行 ``west init`` 后,:file:`my-downstream/my-repo` 将被克隆。

执行 ``west update`` 后,``zephyr`` 仓库的 :file:`west.yml` 在修订版本 ``v1.14.1`` 中定义的所有项目也将被克隆到 :file:`my-downstream` 中。

此时,您可以在 :file:`my-repo` 中添加和提交任何您想要的代码,包括您自己的 Zephyr 应用程序、驱动程序等。详见 :ref:`application`。

.. _west-manifest-ex1.2:

示例 1.2: "滚动发布" Zephyr 下游 (Example 1.2: "Rolling release" Zephyr downstream)
----------------------------------------------------------------------------------------

.. code-block:: yaml

   # my-repo/west.yml:
   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
     projects:
       - name: zephyr
         remote: zephyrproject-rtos
         revision: v1.14.1
         import: true

然后,您可以在计算机上创建工作空间,假设 ``my-repo`` 托管在 ``https://git.example.com/my-repo``:

.. code-block:: console

   west init -m https://git.example.com/my-repo my-downstream
   cd my-downstream
   west update

执行 ``west init`` 后,:file:`my-downstream/my-repo` 将被克隆。

执行 ``west update`` 后,``zephyr`` 仓库的 :file:`west.yml` 在修订版本 ``v1.14.1`` 中定义的所有项目也将被克隆到 :file:`my-downstream` 中。

此时,您可以在 :file:`my-repo` 中添加和提交任何您想要的代码,包括您自己的 Zephyr 应用程序、驱动程序等。详见 :ref:`application`。

.. _west-manifest-ex1.2:

示例 1.2: "滚动发布" Zephyr 下游 (Example 1.2: "Rolling release" Zephyr downstream)
----------------------------------------------------------------------------------------

这类似于 :ref:`west-manifest-ex1.1`,只是我们将为 zephyr 仓库使用 ``revision: main``:

.. code-block:: yaml

   # my-repo/west.yml:
   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
     projects:
       - name: zephyr
         remote: zephyrproject-rtos
         revision: main
         import: true

您可以以相同的方式创建工作空间:

.. code-block:: console

   west init -m https://git.example.com/my-repo my-downstream
   cd my-downstream
   west update

这次,每当您运行 ``west update`` 时,``zephyr`` 仓库中的特殊 :ref:`manifest-rev <west-manifest-rev>` 分支将更新为指向从 URL https://github.com/zephyrproject-rtos/zephyr 新获取的 ``main`` 分支提示。

然后,新 ``manifest-rev`` 处的 :file:`zephyr/west.yml` 内容将用于从 Zephyr 导入项目。这使您可以与 Zephyr 项目的最新更改保持同步。代价是运行 ``west update`` 不会产生可重现的结果,因为远程 ``main`` 分支每次运行时都可能发生变化。

同样重要的是要理解,在解析导入时,west **完全忽略您工作树的** :file:`zephyr/west.yml`。从项目导入时,West 始终使用导入清单的内容,因为它们已提交到最新的 ``manifest-rev``。

只有当它们在清单仓库的工作树中时,您才能从文件系统导入清单。有关示例,请参阅 :ref:`west-manifest-ex2.2`。

.. _west-manifest-ex1.3:

示例 1.3: Zephyr 发行版的下游,带有模块分支 (Example 1.3: Downstream of a Zephyr release, with module fork)
---------------------------------------------------------------------------------------------------------------

此清单类似于 :ref:`west-manifest-ex1.1` 中的清单,除了它:

- 是 Zephyr 2.0 的下游
- 包括 :file:`modules/hal/nordic` :ref:`模块 <modules>` 的下游分支,该模块包含在该发行版中

.. code-block:: yaml

   # my-repo/west.yml:
   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
       - name: my-remote
         url-base: https://git.example.com
     projects:
       - name: hal_nordic         # 更高的优先级
         remote: my-remote
         revision: my-sha
         path: modules/hal/nordic
       - name: zephyr
         remote: zephyrproject-rtos
         revision: v2.0.0
         import: true             # 导入的项目具有较低的优先级

   # v2.0.0 时 zephyr/west.yml 内容的子集:
   manifest:
     defaults:
       remote: zephyrproject-rtos
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
     projects:
     # ...
     - name: hal_nordic           # 较低的优先级,值被忽略
       path: modules/hal/nordic
       revision: another-sha

使用此清单文件,名为 ``hal_nordic`` 的项目:

- 从 ``https://git.example.com/hal_nordic`` 克隆,而不是从 ``https://github.com/zephyrproject-rtos/hal_nordic`` 克隆。
- 通过 ``west update`` 更新到提交 ``my-sha``,而不是主线提交 ``another-sha``

换句话说,当您的顶级清单定义一个项目时,如 ``hal_nordic``,west 将忽略在解析导入时稍后找到的任何其他定义。

这确实意味着在 :file:`my-repo/west.yml` 中定义 ``hal_nordic`` 时,您必须将 ``path: modules/hal/nordic`` 值复制到其中。:file:`zephyr/west.yml` 中的值将被完全忽略。如果这在实践中令人困惑,请参阅 :ref:`west-manifest-resolve` 以获取故障排除建议。

当您运行 ``west update`` 时,west 将:

- 更新 zephyr 的 ``manifest-rev`` 以指向 ``v2.0.0`` 标签
- 在该 ``manifest-rev`` 处导入 :file:`zephyr/west.yml`
- 在本地检出除 ``hal_nordic`` 之外的所有 zephyr 项目的 ``v2.0.0`` 修订版本
- 将 ``hal_nordic`` 更新到 ``my-sha`` 而不是 ``another-sha``

.. _west-manifest-import-path:

选项 2: 相对路径 (Option 2: Relative path)
============================================

``import`` 值也可以是清单文件或包含清单文件的目录的相对路径。该路径相对于 ``import`` 键出现的 ``projects`` 或 ``self`` 仓库的根目录。

这是一个示例:

.. code-block:: yaml

   manifest:
     projects:
       - name: project-1
         revision: v1.0
         import: west.yml
       - name: project-2
         revision: main
         import: p2-manifests
     self:
       import: submanifests

这将导入以下内容:

- :file:`project-1/west.yml` 在 ``manifest-rev`` 处的内容,该分支在运行 ``west update`` 后指向标签 ``v1.0``
- 目录树 :file:`project-2/p2-manifests` 中的任何 YAML 文件,位于 ``main`` 分支的最新提交处(由 ``west update`` 获取),按文件名排序
- 清单仓库中 :file:`submanifests` 里的 YAML 文件,这些文件来自您的文件系统,按文件名排序

请注意 ``projects`` 导入如何使用 ``manifest-rev`` 从 Git 获取数据,而 ``self`` 导入从您的文件系统获取数据。这是因为如常,west 将清单仓库的版本控制留给您。

.. _west-manifest-ex2.1:

示例 2.1: Zephyr 发行版的下游,带有显式路径 (Example 2.1: Downstream of a Zephyr release with explicit path)
-------------------------------------------------------------------------------------------------------

这是编写与 :ref:`west-manifest-ex1.1` 中清单等效的显式方式。

.. code-block:: yaml

   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
     projects:
       - name: zephyr
         remote: zephyrproject-rtos
         revision: v1.14.1
         import: west.yml

设置 ``import: west.yml`` 意味着使用 ``zephyr`` 项目内的 :file:`west.yml` 文件。这个示例是人为构造的,但展示了这个想法。

当您想要导入的清单文件名称不是 :file:`west.yml` 时,这在实践中可能很有用。

.. _west-manifest-ex2.2:

示例 2.2: 带有清单文件目录的下游 (Example 2.2: Downstream with directory of manifest files)
-------------------------------------------------------------------------------------------

您的 Zephyr 下游有很多额外的仓库。事实上,数量如此之多,以至于您想将它们拆分到多个清单文件中,但将它们全部保存在一个清单仓库中,如下所示:

.. code-block:: none

   my-repo/
   ├── submanifests
   │   ├── 01-libraries.yml
   │   ├── 02-vendor-hals.yml
   │   └── 03-applications.yml
   └── west.yml

您想将 :file:`my-repo/submanifests` 中的所有文件添加到主清单文件 :file:`my-repo/west.yml` 中,以及 :file:`zephyr/west.yml` 中的项目。您想跟踪 Zephyr 仓库 ``main`` 分支中的最新开发代码,而不是使用固定的修订版本。

方法如下:

.. code-block:: yaml

   # my-repo/west.yml:
   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
     projects:
       - name: zephyr
         remote: zephyrproject-rtos
         revision: main
         import: true
     self:
       import: submanifests

清单文件在解析期间按以下顺序导入:

#. :file:`my-repo/submanifests/01-libraries.yml`
#. :file:`my-repo/submanifests/02-vendor-hals.yml`
#. :file:`my-repo/submanifests/03-applications.yml`
#. :file:`my-repo/west.yml`
#. :file:`zephyr/west.yml`

.. note::

   此示例中的 :file:`.yml` 文件名以数字为前缀,以确保它们按指定顺序导入。

   您可以选择任意名称。West 在导入之前按名称对目录中的文件进行排序。

请注意,:file:`submanifests` 中的清单是在 :file:`my-repo/west.yml` 和 :file:`zephyr/west.yml` **之前** 导入的。通常,``self`` 部分中的 ``import`` 在 ``projects`` 中的清单文件和主清单文件之前处理。

这意味着在 :file:`my-repo/submanifests` 中定义的项目具有最高优先级。例如,如果 :file:`01-libraries.yml` 定义了 ``hal_nordic``,则 :file:`zephyr/west.yml` 中同名的项目将被简单地忽略。如常,请参阅 :ref:`west-manifest-resolve` 以获取故障排除建议。

这可能看起来很奇怪,但它允许您"事后"重新定义项目,正如我们将在下一个示例中看到的那样。

.. _west-manifest-ex2.3:

示例 2.3: 持续集成覆盖 (Example 2.3: Continuous Integration overrides)
-------------------------------------------------------------------------

您的持续集成系统需要从开发人员的分支而不是主线开发树中获取并测试 west 工作空间中的多个仓库,以查看这些更改是否能够很好地协同工作。

从 :ref:`west-manifest-ex2.2` 开始,CI 脚本在 :file:`my-repo/submanifests` 中添加一个文件 :file:`00-ci.yml`,其内容如下:

.. code-block:: yaml

   # my-repo/submanifests/00-ci.yml:
   manifest:
     projects:
       - name: a-vendor-hal
         url: https://github.com/a-developer/hal
         revision: a-pull-request-branch
       - name: an-application
         url: https://github.com/a-developer/application
         revision: another-pull-request-branch

CI 脚本在 :file:`my-repo/submanifests` 中生成此文件后运行 ``west update``。:file:`00-ci.yml` 中定义的项目具有比 :file:`my-repo/submanifests` 中其他定义更高的优先级,因为名称 :file:`00-ci.yml` 排在其他文件名之前。

因此,``west update`` 始终检出开发人员在名为 ``a-vendor-hal`` 和 ``an-application`` 的项目中的分支,即使这些相同的项目也在其他地方定义。

.. _west-manifest-import-map:

选项 3: 映射 (Option 3: Mapping)
==================================

``import`` 键也可以包含一个映射,具有以下键:

- ``file``: 可选。要导入的清单文件或目录的名称。如果不存在,则默认为 :file:`west.yml`。
- ``name-allowlist``: 可选。如果存在,是要包含的项目名称或项目名称序列。
- ``path-allowlist``: 可选。如果存在,是要匹配的路径或项目路径序列。这是一个 shell 样式的通配符模式,目前使用 `pathlib`_ 实现。请注意,这意味着大小写敏感性是平台特定的。
- ``name-blocklist``: 可选。类似于 ``name-allowlist``,但包含要排除而不是包含的项目名称。
- ``path-blocklist``: 可选。类似于 ``path-allowlist``,但包含要排除而不是包含的项目路径。
- ``path-prefix``: 可选(v0.8.0 中的新功能)。如果给定,这将被添加到项目在工作空间中的路径之前,以及任何导入项目的路径之前。这可用于将这些项目放置在工作空间的子目录中。

.. _re: https://docs.python.org/3/library/re.html
.. _pathlib:
   https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.match

如果同时给出,允许列表将覆盖阻止列表。例如,如果某个项目被路径阻止,然后通过名称允许,它仍将被导入。

.. _west-manifest-ex3.1:

示例 3.1: 带名称允许列表的下游 (Example 3.1: Downstream with name allowlist)
-----------------------------------------------------------------------------

这是一对清单文件,代表主线和下游。但是,下游不想使用所有主线项目。我们假设主线 :file:`west.yml` 托管在 ``https://git.example.com/mainline/manifest``。

.. code-block:: yaml

   # mainline west.yml:
   manifest:
     projects:
       - name: mainline-app                # included
         path: examples/app
         url: https://git.example.com/mainline/app
       - name: lib
         path: libraries/lib
         url: https://git.example.com/mainline/lib
       - name: lib2                        # included
         path: libraries/lib2
         url: https://git.example.com/mainline/lib2

   # downstream west.yml:
   manifest:
     projects:
       - name: mainline
         url: https://git.example.com/mainline/manifest
         import:
           name-allowlist:
             - mainline-app
             - lib2
       - name: downstream-app
         url: https://git.example.com/downstream/app
       - name: lib3
         path: libraries/lib3
         url: https://git.example.com/downstream/lib3

An equivalent manifest in a single file would be:

.. code-block:: yaml

   manifest:
     projects:
       - name: mainline
         url: https://git.example.com/mainline/manifest
       - name: downstream-app
         url: https://git.example.com/downstream/app
       - name: lib3
         path: libraries/lib3
         url: https://git.example.com/downstream/lib3
       - name: mainline-app                   # imported
         path: examples/app
         url: https://git.example.com/mainline/app
       - name: lib2                           # imported
         path: libraries/lib2
         url: https://git.example.com/mainline/lib2

如果没有使用允许列表,主线清单中的 ``lib`` 项目将被导入。

.. _west-manifest-ex3.2:

示例 3.2: 带路径允许列表的下游 (Example 3.2: Downstream with path allowlist)
-----------------------------------------------------------------------------

以下是一个示例,展示如何使用 ``path-allowlist`` 仅允许列出主线的库。

.. code-block:: yaml

   # mainline west.yml:
   manifest:
     projects:
       - name: app
         path: examples/app
         url: https://git.example.com/mainline/app
       - name: lib
         path: libraries/lib                  # included
         url: https://git.example.com/mainline/lib
       - name: lib2
         path: libraries/lib2                 # included
         url: https://git.example.com/mainline/lib2

   # downstream west.yml:
   manifest:
     projects:
       - name: mainline
         url: https://git.example.com/mainline/manifest
         import:
           path-allowlist: libraries/*
       - name: app
         url: https://git.example.com/downstream/app
       - name: lib3
         path: libraries/lib3
         url: https://git.example.com/downstream/lib3

An equivalent manifest in a single file would be:

.. code-block:: yaml

   manifest:
     projects:
       - name: lib                          # imported
         path: libraries/lib
         url: https://git.example.com/mainline/lib
       - name: lib2                         # imported
         path: libraries/lib2
         url: https://git.example.com/mainline/lib2
       - name: mainline
         url: https://git.example.com/mainline/manifest
       - name: app
         url: https://git.example.com/downstream/app
       - name: lib3
         path: libraries/lib3
         url: https://git.example.com/downstream/lib3

.. _west-manifest-ex3.3:

示例 3.3: 带路径阻止列表的下游 (Example 3.3: Downstream with path blocklist)
-----------------------------------------------------------------------------

以下是一个示例,展示如何通过工作空间中的通用路径前缀阻止主线的所有供应商 HAL,为您的目标芯片添加您自己的版本,并保留其他所有内容。

.. code-block:: yaml

   # mainline west.yml:
   manifest:
     defaults:
       remote: mainline
     remotes:
       - name: mainline
         url-base: https://git.example.com/mainline
     projects:
       - name: app
       - name: lib
         path: libraries/lib
       - name: lib2
         path: libraries/lib2
       - name: hal_foo
         path: modules/hals/foo     # excluded
       - name: hal_bar
         path: modules/hals/bar     # excluded
       - name: hal_baz
         path: modules/hals/baz     # excluded

   # downstream west.yml:
   manifest:
     projects:
       - name: mainline
         url: https://git.example.com/mainline/manifest
         import:
           path-blocklist: modules/hals/*
       - name: hal_foo
         path: modules/hals/foo
         url: https://git.example.com/downstream/hal_foo

An equivalent manifest in a single file would be:

.. code-block:: yaml

   manifest:
     defaults:
       remote: mainline
     remotes:
       - name: mainline
         url-base: https://git.example.com/mainline
     projects:
       - name: app                  # imported
       - name: lib                  # imported
         path: libraries/lib
       - name: lib2                 # imported
         path: libraries/lib2
       - name: mainline
         repo-path: https://git.example.com/mainline/manifest
       - name: hal_foo
         path: modules/hals/foo
         url: https://git.example.com/downstream/hal_foo

.. _west-manifest-ex3.4:

示例 3.4: 导入到子目录 (Example 3.4: Import into a subdirectory)
------------------------------------------------------------------

您想要导入一个清单及其项目,将所有内容放入 :term:`west workspace` 的子目录中。

例如,假设您想从项目 ``foo`` 导入此清单,将此项目及其项目 ``bar`` 和 ``baz`` 添加到您的工作空间:

.. code-block:: yaml

   # foo/west.yml:
   manifest:
     defaults:
       remote: example
     remotes:
       - name: example
         url-base: https://git.example.com
     projects:
       - name: bar
       - name: baz

您不想将这些导入到顶级工作空间,而是想将所有三个项目仓库放在 :file:`external-code` 子目录中,如下所示:

.. code-block:: none

   workspace/
   └── external-code/
       ├── foo/
       ├── bar/
       └── baz/

您可以使用此清单实现:

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
         url: https://git.example.com/foo
         import:
           path-prefix: external-code

单个文件中的等效清单为:

.. code-block:: yaml

   # foo/west.yml:
   manifest:
     defaults:
       remote: example
     remotes:
       - name: example
         url-base: https://git.example.com
     projects:
       - name: foo
         path: external-code/foo
       - name: bar
         path: external-code/bar
       - name: baz
         path: external-code/baz

.. _west-manifest-import-seq:

Option 4: Sequence
==================

The ``import`` key can also contain a sequence of files, directories,
and mappings.

.. _west-manifest-ex4.1:

示例 4.1: 带清单文件序列的下游 (Example 4.1: Downstream with sequence of manifest files)
----------------------------------------------------------------------------------------

此示例清单等效于 :ref:`west-manifest-ex2.2` 中的清单,其中包含显式命名文件的序列。

.. code-block:: yaml

   # my-repo/west.yml:
   manifest:
     projects:
       - name: zephyr
         url: https://github.com/zephyrproject-rtos/zephyr
         import: west.yml
     self:
       import:
         - submanifests/01-libraries.yml
         - submanifests/02-vendor-hals.yml
         - submanifests/03-applications.yml

.. _west-manifest-ex4.2:

示例 4.2: 导入顺序示例 (Example 4.2: Import order illustration)
-----------------------------------------------------------------

这个更复杂的示例展示了 west 导入清单文件的顺序:

.. code-block:: yaml

   # my-repo/west.yml
   manifest:
     # ...
     projects:
       - name: my-library
       - name: my-app
       - name: zephyr
         import: true
       - name: another-manifest-repo
         import: submanifests
     self:
       import:
         - submanifests/libraries.yml
         - submanifests/vendor-hals.yml
         - submanifests/applications.yml
     defaults:
       remote: my-remote

对于此示例,west 按以下顺序解析导入:

#. :file:`my-repo/submanifests` 中列出的文件是第一位的,按它们出现的顺序(例如,:file:`libraries.yml` 在 :file:`applications.yml` 之前,因为这是一个文件序列),因为 ``self: import:`` 总是首先导入
#. :file:`my-repo/west.yml` 是下一个(包含 ``my-library`` 等项目,只要它们尚未在 :file:`submanifests` 中的某处定义)
#. :file:`zephyr/west.yml` 在其后,因为这是 :file:`my-repo/west.yml` 中 ``projects`` 列表中的第一个 ``import`` 键
#. :file:`another-manifest-repo/submanifests` 中的文件是最后的(按文件名排序),因为这是最后一个项目 ``import``

.. _west-manifest-formal:

清单导入详情 (Manifest Import Details)
========================================

本节更正式地描述了 west 如何解析使用 ``import`` 的清单文件。

概述 (Overview)
-----------------

``import`` 键可以出现在 west 清单的 ``projects`` 和 ``self`` 部分中。一般情况如下所示:

.. code-block:: yaml

   # 顶级清单文件。
   manifest:
     projects:
       - name: foo
         import:
           ... # import-1
       - name: bar
         import:
           ... # import-2
       # ...
       - name: baz
         import:
           ... # import-N
     self:
       import:
         ... # self-import

导入键是可选的。如果 ``import-1, ..., import-N`` 中的任何一个缺失,west 将不会从该项目导入额外的清单数据。如果 ``self-import`` 缺失,则不会导入清单仓库中的其他文件(除顶级文件之外)。

解析清单导入的最终结果是:

- 一个 ``projects`` 列表,通过组合顶级文件中定义的 ``projects`` 与导入文件中定义的项目而产生

- 一组扩展命令,从顶级文件和任何导入文件中的 ``west-commands`` 键中提取

- 一个 ``group-filter`` 列表,通过组合顶级和任何导入的过滤器而产生

导入按以下顺序完成:

#. 首先导入 ``self-import`` 中的清单。
#. 接下来处理顶级清单文件的定义。
#. 然后按该顺序导入 ``import-1``, ..., ``import-N`` 的清单。

当单个 ``import`` 键引用多个清单文件时,它们按以下顺序处理:
processed in this order:

- If the value is a relative path naming a directory (or a map whose ``file``
  is a directory), the manifest files it contains are processed in
  lexicographic order -- i.e., sorted by file name.
- If the value is a sequence, its elements are recursively imported in the
  order they appear.

如有必要,此过程会递归。例如,如果 ``import-1`` 产生一个包含 ``import`` 键的清单文件,则在进一步处理其内容之前,使用相同的规则递归地解析它。

以下各节描述了这些结果。

项目 (Projects)
------------------

本节描述如何创建最终的 ``projects`` 列表。

项目通过名称识别。如果同一名称出现在多个清单中,则使用第一个定义,并忽略后续定义。例如,如果 ``import-1`` 包含名为 ``bar`` 的项目,则会被忽略,因为顶级 :file:`west.yml` 已经定义了该名称的项目。

从 ``import-1`` 到 ``import-N`` 命名的文件的内容是从 Git 中它们项目的最新 ``manifest-rev`` 修订版本导入的。这些修订版本可以通过运行 ``west update`` 更新为值 ``rev-1`` 到 ``rev-N``。如果任何 ``manifest-rev`` 引用缺失或过期,``west update`` 还会从远程获取 URL 获取项目数据并更新引用。

还要注意,从根清单到定义项目 ``P`` 的仓库,所有导入的清单必须是最新的,west 才能更新 ``P`` 本身。例如,这意味着如果 :file:`baz/west.yml` 定义了 ``P``,则 ``west update P`` 将更新 ``baz`` 项目中的 ``manifest-rev``,以及更新 ``P`` 本地 git 克隆中的 ``manifest-rev`` 分支。令人困惑的是,更新 ``baz`` 可能会导致从 :file:`baz/west.yml` 中删除 ``P``,这"应该"导致 ``west update P`` 因无法识别的项目而失败!

因此,如果 ``P`` 在导入的清单中定义,则无法运行 ``west update P``;您必须通过普通的 ``west update`` 与所有其他项目一起更新此项目。

默认情况下,如果项目的修订版本是本地已经可用的 SHA 或标签,west 不会通过网络获取任何项目数据,因此更新额外的项目不应该花费太多时间,除非真正需要。有关更多信息,请参阅 :ref:`update.fetch <west-config-index>` 配置选项的文档。

扩展 (Extensions)
-------------------

在处理导入时发现的使用 ``west-commands`` 键定义的所有扩展命令都可在解析的清单中使用。

如果导入的清单文件在其 ``self:`` 部分中有 ``west-commands:`` 定义,则在导入清单时,那里定义的扩展命令将添加到可用扩展集中。因此,它们将优先于稍后添加的具有相同名称的任何扩展命令。

组过滤器 (Group filters)
--------------------------

解析的清单具有一个 ``group-filter`` 值,该值是通过连接顶级清单和任何导入清单中的 ``group-filter`` 值而得出的。

在导入顺序中较早出现的清单文件具有更高的优先级,因此会稍后连接到最终的 ``group-filter`` 中。

换句话说,设:

- 从 ``self-import`` 解析的子清单具有组过滤器 ``self-filter``
- 顶级清单文件具有组过滤器 ``top-filter``
- 从 ``import-1`` 到 ``import-N`` 解析的子清单分别具有组过滤器 ``filter-1`` 到 ``filter-N``

最终解析的 ``group-filter`` 值为 ``filterN + ... + filter-2 + filter-1 + top-filter + self-filter``,其中 ``+`` 此处指列表连接。

.. important::

   上述列表中过滤器出现的顺序很重要。

   最终连接列表中的最后一个过滤器元素"获胜"并确定组是启用还是禁用。

例如,在 ``[-foo] + [+foo]`` 中,组 ``foo`` **启用**。
但是,在 ``[+foo] + [-foo]`` 中,组 ``foo`` **禁用**。

为简单起见,west 和本文档可能会使用这些规则省略冗余的连接组过滤器元素。例如,``[+foo] + [-foo]`` 可以更简单地写为 ``[-foo]``,原因如上所述。再举一个例子,``[-foo] + [+foo]`` 可以写为空列表 ``[]``,因为默认情况下所有组都是启用的。

.. _west-manifest-cmd:

Manifest 命令 (Manifest Command)
**********************************

``west manifest`` 命令可用于操作清单文件。它接受一个动作和特定于动作的参数。

以下各节描述每个动作并为简单用例提供基本签名。运行 ``west manifest --help`` 以获取所有选项的完整详细信息。

.. _west-manifest-resolve:

解析清单 (Resolving Manifests)
=================================

``--resolve`` 动作输出一个与您当前清单及其所有 :ref:`导入的清单 <west-manifest-import>` 等效的单个清单文件:

.. code-block:: none

   west manifest --resolve [-o outfile]

此动作的主要用途是在执行任何 ``import`` 后查看"最终"清单内容。

要打印有关每个导入的清单文件以及在清单解析期间如何处理项目的详细信息,请使用 ``-v`` 设置最大详细程度级别:

.. code-block:: console

   west -v manifest --resolve

冻结清单 (Freezing Manifests)
===============================

``--freeze`` 动作输出一个冻结的清单:

.. code-block:: none

   west manifest --freeze [-o outfile]

"冻结的"清单是一个清单文件,其中每个项目的修订版本都是 SHA。您可以使用 ``--freeze`` 生成与当前清单文件等效的冻结清单。``-o`` 选项指定输出文件;如果未给出,则使用标准输出。

验证清单 (Validating Manifests)
=================================

如果当前清单文件有效,``--validate`` 动作成功,否则失败并返回错误:

.. code-block:: none

   west manifest --validate

错误消息可以帮助诊断错误。

在这里,"无效"意味着清单文件的语法不遵循本页面记录的规则。

如果您的清单有效但工作方式与您期望的不同,使用 ``-v`` 提高详细程度是获取有关 west 对您的清单做出的决策及其原因的详细信息的好方法:

.. code-block:: none

   west -v manifest --validate

.. _west-manifest-path:

获取清单路径 (Get the manifest path)
======================================

``--path`` 动作打印顶级清单文件的路径:

.. code-block:: none

   west manifest --path

输出类似于 ``/path/to/workspace/west.yml``。路径格式取决于您的操作系统。
