.. _west-release-notes:

West 发布说明 (West Release Notes)
###################################

v1.5.0
******

主要变更 (Major changes):

- 添加对自动缓存的支持。
  向 ``west update`` 传递 ``--auto-cache <directory>`` 参数。

其他变更 (Other changes):

- 允许对 ``west update`` 同时使用 ``--name-cache`` 和 ``--path-cache``。

- 在清单模式中记录默认修订版本值。

错误修复 (Bug fixes):

- 允许空的或缺失的清单项目列表。

- 在冻结或解析清单文件时,使 ``manifest.group-filter`` 列表顺序具有确定性。

v1.4.0
******

变更 (Changes):

- 允许向配置字符串追加数据。
  要向 ``<name>`` 的值追加数据,请输入: ``west config -a <name> <value>``。

- 向 ``west manifest`` 添加 ``--untracked`` 参数选项。
  在工作空间中运行 ``west manifest --untracked`` 以打印所有未被 west 跟踪或管理的文件和目录。

- 向 ``west list`` 添加 ``--inactive`` 参数选项,以支持打印非活动项目。

- 为 ``west manifest --resolve`` 和 ``west manifest --freeze`` 命令支持 ``--active-only`` 参数选项。
  这允许冻结具有活动项目或组过滤器的工作空间。

API 变更 (API changes):

- ``west.manifest.Manifest`` 方法 ``as_dict()``、``as_frozen_dict()``、``as_yaml()`` 和
  ``as_frozen_yaml()`` 现在有一个可选的 ``active_only`` 参数 (默认为 ``False``)
  用于返回包含所有项目或仅包含活动项目的对象。

v1.3.0
******

主要变更 (Major changes):

- 添加了对 :ref:`west-aliases` 命令的支持。

- 采用 `pyproject TOML 规范`_ 进行打包。

.. _pyproject TOML specification:
   https://packaging.python.org/en/latest/specifications/pyproject-toml/

其他变更 (Other changes):

- 为子模块添加缓存支持。

- 默认将清单文件解码为 UTF-8。

- 将 ``west diff`` 和 ``west status`` 的未知参数传递给底层的 ``git`` 命令。

- 向 ``west diff`` 添加 ``--manifest`` 参数,以允许将当前工作空间与清单修订版本进行比较。

- 环境变量可以与 west forall 一起使用
  定义了以下环境变量:

  - ``WEST_PROJECT_NAME``
  - ``WEST_PROJECT_PATH``
  - ``WEST_PROJECT_ABSPATH``
  - ``WEST_PROJECT_REVISION``
  - ``WEST_PROJECT_URL``
  - ``WEST_PROJECT_REMOTE``

- 添加了对早期参数 ``-q/--quiet`` 的支持,以减少详细输出。

- 向 ``west init`` 添加 ``-o/--clone-opt`` 参数,以传递给 ``git clone``。

- 支持 Python 3.13 并放弃对 Python 3.8 的支持。

- 防止清单在 ``.west`` 目录中包含项目。

- 为 ``west init`` 添加 NTFS 变通方法和 ``--rename-delay``。

- 在调试模式 ``-vvv`` 中调用 die 时打印堆栈跟踪。

错误修复 (Bug fixes):

- 使用 ``'backslashreplace'`` 以避免在子进程输出格式错误的 UTF 时崩溃。

- 修复了 ``west diff`` 在有合并冲突的仓库中的处理问题。
  此外改进了错误打印并处理 ``git diff`` 返回代码。

- 修复了当使用 git 子模块时 ``west manifest`` 命令的 ``--freeze`` 和 ``--resolve``。

v1.2.0
******

主要变更 (Major changes):

- 新增 ``west grep`` 命令,用于在您的 west 工作空间的仓库中运行 "grep 工具"。
  目前支持 ``git grep``、`ripgrep`_ 和标准 ``grep`` 作为 grep 工具。

  要运行此命令以从所有已克隆的活动仓库获取 ``git grep foo`` 结果,请运行:

  .. code-block:: console

     west grep foo

  以下是使用 ``west grep`` 运行不同 grep 命令的其他示例:

  .. list-table::

     * - ``git grep --untracked``
       - ``west grep --untracked foo``
     * - ``ripgrep``
       - ``west grep --tool ripgrep foo``
     * - ``grep --recursive``
       - ``west grep --tool grep foo``

  要在工作空间中切换默认的 grep 工具,请运行此表中的相应命令:

  .. list-table::

     * - ``ripgrep``
       - ``west config grep.tool ripgrep``
     * - ``grep``
       - ``west config grep.tool grep``

  有关更多详细信息,请运行 ``west help grep``。

其他变更 (Other changes):

- 清单文件格式现在支持在每个 ``projects:`` 元素中使用 ``description`` 字段。
  请参阅 :ref:`west-manifests-projects` 以获取示例。

- ``west list --format`` 现在在格式字符串中接受 ``{description}``,
  用于打印项目的 ``description:`` 值。

- ``west compare`` 现在总是打印关于 :ref:`west-manifest-rev` 的信息。

错误修复 (Bug fixes):

- 如果目标目录已经存在,``west init`` 会中止。

API 变更 (API changes):

- ``west.commands.WestCommand`` 方法 ``check_call()`` 和 ``check_output()``
  现在可以接受任何可以传递给底层 subprocess 函数的 kwargs。

- ``west.commands.WestCommand.run_subprocess()``: 围绕 ``subprocess.run()`` 的新包装器。
  这不能命名为 ``run()``,因为 ``WestCommand`` 已经有一个同名方法。

- ``west.commands.WestCommand`` 方法 ``dbg()``、``inf()``、``wrn()`` 和 ``err()``
  现在都接受一个 ``end`` kwarg,它会被传递给 ``print()`` 调用。

- ``west.manifest.Project`` 现在有一个 ``description`` 属性,
  其中包含清单数据中 ``description:`` 字段的解析值。

.. _ripgrep: https://github.com/BurntSushi/ripgrep#readme

v1.1.0
******

主要变更 (Major changes):

- ``west compare``: 新命令,用于比较工作空间的状态与清单。

- 支持新的 ``manifest.project-filter`` 配置选项。
  详见 :ref:`west-config-index`。当设置此选项时,目前无法使用
  ``west manifest --freeze`` 和 ``west manifest --resolve`` 命令。
  此限制可以在以后的版本中移除。

- 包含逗号 (``,``) 或空格的项目名称现在会生成警告。
  如果设置了新的 ``manifest.project-filter`` 配置选项,这些警告将变为错误。
  这些警告可能在 west 的未来主要版本中被提升为错误。

其他变更 (Other changes):

- ``west forall`` 现在接受一个 ``--group`` 参数,可用于将命令限制为仅在一个或多个组中运行。
  运行 ``west help forall`` 以获取详细信息。

- 所有 west 命令现在将以警告级别或更高级别输出来自 west API 模块的日志消息。
  此外,west 的 ``--verbose`` 参数可以使用一次以包含信息性消息,
  或使用两次以包含来自所有命令的调试消息。

错误修复 (Bug fixes):

- 对错误消息、调试日志和错误处理的各种改进。

API 变更 (API changes):

- ``west.manifest.Manifest.is_active()`` 现在遵守 ``manifest.project-filter`` 配置选项的值。

v1.0.1
******

主要变更 (Major changes):

- 清单模式版本 "1.0" 现在可以在此版本中使用。这在功能上与 "0.13" 模式版本相同,
  但可以被不希望使用 "0.x" 清单 "version:" 字段的应用程序使用。
  有关此功能的详细信息,请参阅 :ref:`west-manifest-schema-version`。

错误修复 (Bug fixes):

- West 在收到中断信号时不再以成功的错误代码退出。
  相反,它以特定于平台的错误代码退出,并向调用环境发出进程被中断的信号。

v1.0.0
******

此版本的主要变更 (Major changes in this release):

- :ref:`west-apis` 现在被声明为稳定的。任何破坏性变更都将通过从 v1.x.y 到 v2.x.y 的主版本号提升来通知。

- West v1.0 不再适用于 Zephyr v1.14 LTS 版本。此 LTS 早已被 Zephyr v2.7 LTS 淘汰。
  如果您需要使用 Zephyr v1.14,则必须使用 west v0.14 或更早版本。

- 与 Zephyr 的其余部分一样,west 现在需要 Python v3.8 或更高版本

- West 命令不再接受缩写的命令行参数。例如,您现在必须指定 ``west update --keep-descendants``
  而不是使用像 ``west update --keep-d`` 这样的缩写。这是应用于所有 Zephyr 的 Python 脚本
  命令行接口的更改的一部分。当命令被更新以添加与现有选项名称相似但行为不同的新选项时,
  缩写在实践中会引起问题。

其他变更 (Other changes):

- 所有内置的 west 函数都已停止使用 ``west.log``

- ``west update``: 新增 ``--submodule-init-config`` 选项。
  详见提交 `9ba92b05`_。

错误修复 (Bug fixes):

- 有时无法正确加载的 West 扩展命令会转储堆栈。
  这已被修复,west 现在在这种情况下打印合理的错误消息。

- ``west config`` 现在对缺少 ``.`` 的格式错误的配置选项参数会失败

API 变更 (API changes):

- west 包现在包含一些静态分析器(如 `mypy`_)自动检测其类型注解所需的元数据文件。
  详见提交 `d9f00e24`_。

- 已移除用于 Zephyr v1.14 LTS 兼容性的已弃用 ``west.build`` 模块

- 已移除用于 Zephyr v1.14 LTS 兼容性的已弃用 ``west.cmake`` 模块

- ``west.log`` 模块现在已弃用。此模块使用全局状态,
  这可能使其作为多个不同 python 模块可能依赖的 API 使用起来很尴尬。

- :ref:`west-apis-commands` 模块获得了一些新的 API,为将来添加命令输出的全局详细度控制
  以及从 ``west`` 包的 API 中移除全局状态的工作奠定了基础:

  - 新增 ``west.commands.WestCommand.__init__()`` 关键字参数: ``verbosity``
  - 新增 ``west.commands.WestCommand`` 属性: ``color_ui``
  - 新增 ``west.commands.WestCommand`` 方法,应该使用这些方法从扩展命令打印输出,
    而不是直接写入 sys.stdout 或 sys.stderr: ``inf()``、``wrn()``、``err()``、``die()``、
    ``banner()``、``small_banner()``
  - 新增 ``west.commands.VERBOSITY`` 枚举

.. _9ba92b05: https://github.com/zephyrproject-rtos/west/commit/9ba92b054500d75518ff4c4646590bfe134db523
.. _d9f00e24: https://github.com/zephyrproject-rtos/west/commit/d9f00e242b8cb297b56e941982adf231281c6bae
.. _mypy: https://www.mypy-lang.org/

v0.14.0
*******

错误修复 (Bug fixes):

- 使用错误的本地配置文件运行的 West 命令以令人困惑的方式转储堆栈。
  这已被修复,west 现在在这种情况下打印合理的错误消息。

- 修复了 west 查找 zephyr 仓库的方式中的一个错误。该错误通常在新工作空间中
  首次运行扩展命令(如 ``west build``)时出现;过去这会失败(仅在第一次,
  而不是在后续命令调用时),除非您在工作空间的顶层目录中运行命令。

- West 现在在用户缺少打开清单文件的权限时打印合理的错误消息,而不是转储堆栈跟踪。

API 变更 (API changes):

- ``west.manifest.MalformedConfig`` 异常类型已移至 ``west.configuration`` 模块

- ``west.manifest.MalformedConfig`` 异常类型已移至
  :ref:`west.configuration <west-apis-configuration>` 模块

- ``west.configuration.Configuration`` 类现在在某些情况下引发 ``MalformedConfig``
  而不是 ``RuntimeError``

v0.13.1
*******

错误修复 (Bug fix):

- 当在工作空间外调用 west.manifest.Manifest.from_file() 时,
  west 再次回退到 ZEPHYR_BASE 环境变量以定位工作空间。

v0.13.0
*******

新功能 (New features):

- 您现在可以在 ``manifest: self: userdata:`` 值中将任意用户数据与清单仓库本身关联,如下所示:

  .. code-block:: YAML

     manifest:
       self:
         userdata: <any YAML value can go here>

错误修复 (Bug fixes):

- west 报告的清单仓库路径在某些情况下可能不正确,详见 [issue
  #572](https://github.com/zephyrproject-rtos/west/issues/572)。
  这已作为 ``west.manifest`` API 模块中路径处理支持的大规模改进的一部分得到修复。

- ``west.Manifest.ManifestProject.__repr__`` 返回值已修复

:ref:`API <west-apis>` 变更:

- ``west.configuration.Configuration``: 当前配置的新的面向对象接口。
  这反映了系统、全局和工作空间本地配置值,并允许您从这些位置中的任何或所有位置
  读取、写入和删除配置选项。

- ``west.commands.WestCommand``:

  - ``config``: 新属性,返回 ``Configuration`` 对象,如果未设置则中止程序。
    这在扩展命令 ``do_run()`` 实现中始终可用。
  - ``has_config``: 新的布尔属性,当且仅当读取 ``self.config`` 会中止程序时为 ``True``。

- ``west.manifest`` 包中的路径处理已以向后不兼容的方式进行了全面改革。
  有关更多详细信息,请参阅提交
  [56cfe8d1d1](https://github.com/zephyrproject-rtos/west/commit/56cfe8d1d1f3c9b45de3e793c738acd62db52aca)。

- ``west.manifest.Manifest.validate()``: 现在将验证的数据作为 Python dict 返回。
  如果传递给此函数的值是 str,并且需要 dict,这可能很有用。

- ``west.manifest.Manifest``: 新增:

  - 路径属性 ``abspath``、``posixpath``、``relative_path``、
    ``yaml_path``、``repo_path``、``repo_posixpath``
  - ``userdata`` 属性,其中包含来自 ``manifest: self: userdata:`` 的解析值,或为 None
  - ``from_topdir()`` 工厂方法

- ``west.manifest.ManifestProject``: 新增 ``userdata`` 属性,
  它也包含来自 ``manifest: self: userdata:`` 的解析值,或为 None

- ``west.manifest.ManifestImportFailed``: 构造函数现在可以接受任何值;
  这可用于反映来自 :ref:`map <west-manifest-import-map>` 或其他复合值的失败导入。

- 已弃用的配置 API:

  以下 API 现在已弃用,推荐使用 ``Configuration`` 对象。
  通常这将通过 ``WestCommand`` 实例的 ``self.config`` 完成,
  但也可以通过直接实例化 ``Configuration`` 对象来完成其他用途。

  - ``west.configuration.config``
  - ``west.configuration.read_config``
  - ``west.configuration.update_config``
  - ``west.configuration.delete_config``

v0.12.0
*******

新功能 (New features):

- West 现在可以在 `MSYS2 <https://www.msys2.org/>`_ 平台上工作。

- West 清单文件现在可以包含与每个项目关联的任意用户数据。
  详见 :ref:`west-project-userdata`。

错误修复 (Bug fixes):

- ``west list`` 命令的 ``{sha}`` 格式键已针对清单仓库进行了修复;
  它现在按预期打印 ``N/A`` ("不适用")。

:ref:`API <west-apis>` 变更:

- 添加了 ``west.manifest.Project.userdata`` 属性以支持项目用户数据。

v0.11.1
*******

新功能 (New features):

- ``west status`` 现在仅打印具有非空状态的项目的输出。

错误修复 (Bug fixes):

- 清单文件解析器错误地允许包含路径分隔符字符 ``/`` 和 ``\`` 的项目名称。
  这些无效字符现在被拒绝。

  注意: 如果您需要将项目放置在工作空间 topdir 的子目录中,请使用 ``path:`` 键。
  如果您需要相对于其远程 ``url-base:`` 自定义项目的获取 URL,请使用 ``repo-path:``。
  请参阅 :ref:`west-manifests-projects` 以获取示例。

- west v0.10.1 中对 ``west init --manifest-rev`` 选项所做的更改(选择默认分支名称)
  会使清单仓库处于分离的 HEAD 状态。这已通过在内部使用 ``git clone`` 而不是
  ``git init`` 和 ``git fetch`` 得到修复。详见 `issue #522`_。

- ``WEST_CONFIG_LOCAL`` 环境变量现在可以正确覆盖默认位置
  :file:`<workspace topdir>/.west/config`。

- ``west update --fetch=smart`` (``smart`` 是默认值) 现在可以正确跳过对
  `lightweight tags`_ 的项目修订版本的获取(它已经对 annotated tags 正确工作;
  只有 lightweight tags 被不必要地获取)。

其他变更 (Other changes):

- 上面提到的对 issue #522 的修复引入了一个新的限制。
  ``west init --manifest-rev`` 选项值(如果给定)现在必须是分支或标签。
  特别是,GitHub 的 ``pull/1234/head`` 引用等 "伪分支"(以前可用于获取拉取请求)
  不能再传递给 ``--manifest-rev``。用户现在必须在运行 ``west init`` 后手动获取和检出此类修订版本。

:ref:`API <west-apis>` 变更:

- ``west.manifest.Manifest.get_projects()`` 避免了 `issue #523`_ 中描述的某些边缘情况的错误结果。

- ``west.manifest.Project.sha()`` 现在对标签修订版本正确工作。
  (这适用于 lightweight tags 和 annotated tags。)

.. _lightweight tags: https://git-scm.com/book/en/v2/Git-Basics-Tagging
.. _issue #522: https://github.com/zephyrproject-rtos/west/issues/522
.. _issue #523: https://github.com/zephyrproject-rtos/west/issues/523

v0.11.0
*******

新功能 (New features):

- ``west update`` 现在支持 ``--narrow``、``--name-cache`` 和 ``--path-cache`` 选项。
  这些可以通过 ``update.narrow``、``update.name-cache`` 和 ``update.path-cache``
  :ref:`west-config` 选项来影响。这些可用于优化更新速度。
- ``west update`` 现在支持 ``--fetch-opt`` 选项,该选项将传递给用于在更新每个项目时
  获取远程修订版本的 ``git fetch`` 命令。

错误修复 (Bug fixes):

- ``west update`` 现在默认同步项目中的 Git 子模块。
  如果清单文件中的 URL 从子模块首次初始化时发生了变化,这可以避免问题。
  可以通过将 ``update.sync-submodules`` 配置选项设置为 ``false`` 来禁用此行为。

其他变更 (Other changes):

- :ref:`west-apis-manifest` 模块为 Project 类修复了文档字符串

v0.10.1
*******

新功能 (New features):

- :ref:`west-init` 命令的 ``--manifest-rev`` (``--mr``) 选项不再默认为 ``master``。
  相反,该命令将查询仓库以获取其默认分支名称并使用它。这允许用户从 ``master``
  迁移到 ``main`` 而不会破坏不提供此选项的脚本。

.. _west_0_10_0:

v0.10.0
*******

新功能 (New features):

- 项目的 :ref:`submodules list <west-manifest-submodules>` 中的 ``name`` 键现在是可选的。

错误修复 (Bug fixes):

- West 现在检查清单模式版本是否为 :ref:`west-manifest-schema-version` 中记录的明确允许的值之一。
  旧行为只是检查模式版本是否比引入 ``manifest: version:`` 键的 west 版本更新。
  这错误地允许了无效的模式版本,如 ``0.8.2``。

其他变更 (Other changes):

- 清单文件的 ``group-filter`` 现在通过 ``import`` 传播。
  这是与 west v0.9.x 处理方式的变更。在 west v0.9.x 中,只有顶层清单文件的
  ``group-filter`` 有效;来自任何导入的清单的组过滤器列表被忽略。

  从 west v0.10.0 开始,来自导入清单的组过滤器列表也会被导入。
  有关详细信息,请参阅 :ref:`west-group-filter-imports`。

  如果未给定 ``manifest: version:`` 或至少为 ``0.10``,则新行为将生效。
  旧行为仍可在顶层清单文件中通过显式的 ``manifest: version: 0.9`` 使用。
  有关模式版本的更多信息,请参阅 :ref:`west-manifest-schema-version`。

  有关此更改的动机和附加上下文,请参阅 `west pull request #482
  <https://github.com/zephyrproject-rtos/west/pull/482>`_。

v0.9.1
******

错误修复 (Bug fixes):

- 像 ``west manifest --resolve`` 这样的命令现在可以正确包含组和组过滤器信息。

其他变更 (Other changes):

- 如果您将 ``import`` 与 ``group-filter`` 结合使用,West 现在会发出警告。
  从 v0.10.x 开始,此组合的语义已更改。有关更多信息,请参阅上面的 v0.10.0 发布说明。

.. _west_0_9_0:

v0.9.0
******

.. warning::

   下面描述的 ``west config`` 修复是有代价的: 通过该命令或 ``west.configuration`` API
   设置配置选项时,配置文件中的任何注释或其他手动编辑都将被删除。
   configuration option via that command or the ``west.configuration`` API.

.. warning::

   不建议将此版本中引入的 ``group-filter`` 功能与清单导入结合使用。
   从 west v0.10 开始,生成的行为已更改。

新功能 (New features):

- West 清单现在支持 :ref:`west-manifest-submodules`。这允许您将 `Git 子模块
  <https://git-scm.com/book/en/v2/Git-Tools-Submodules>`_ 克隆到 west 项目仓库中,
  以及项目仓库本身。

- West 清单现在支持 :ref:`west-manifest-groups`。可以启用和禁用项目组来确定哪些项目是 "活动的",
  因此将受以下命令影响: ``west update``、``west list``、``west diff``、``west status``、
  ``west forall``。

- ``west update`` 默认情况下不再更新非活动项目。它现在支持 ``--group-filter`` 选项,
  该选项允许对启用和禁用的项目组集合进行一次性修改。

- 不带参数运行 ``west list``、``west diff``、``west status`` 或 ``west forall``
  默认情况下不会打印非活动项目的信息。如果用户在命令行明确指定项目列表,
  则无论它们是否处于活动状态,都会包含它们的输出。

  这些命令现在还支持 ``--all`` 参数以包含所有项目,即使是非活动项目。

- ``west list`` 现在在其 ``--format`` 参数中支持 ``{groups}`` 格式字符串键。

错误修复 (Bug fixes):

- ``west config`` 命令和 ``west.configuration`` API 未正确存储某些配置值,
  例如包含逗号的字符串。这已被修复;详见 `commit 36f3f91e
  <https://github.com/zephyrproject-rtos/west/commit/36f3f91e270782fb05f6da13800f433a9c48f130>`_。

- 具有空 ``manifest: self: path:`` 值的清单文件是无效的,
  但 west 过去会默默地让它通过。West 现在拒绝此类清单。

- 修复了影响 ``west init -l .`` 命令行为的错误;请参阅
  `issue #435 <https://github.com/zephyrproject-rtos/west/issues/435>`_。

:ref:`API <west-apis>` 变更:

- 添加了 ``west.manifest.Manifest.is_active()``
- 添加了 ``west.manifest.Manifest.group_filter``
- 向 ``west.manifest.Project`` 添加了 ``submodules`` 属性,
  其新添加的类型为 ``west.manifest.Submodule``

其他变更 (Other changes):

- :ref:`west-manifest-import` 功能现在支持术语 ``allowlist`` 和 ``blocklist``,
  分别代替 ``whitelist`` 和 ``blacklist``。

  为了兼容性,仍支持旧术语,但文档已更新为专门使用新术语。

v0.8.0
******

这是一个功能版本,通过在 ``import:`` 映射中添加对 ``path-prefix:`` 键的支持,
更改了清单模式,以及一些其他功能和修复。

- 清单导入映射现在支持 ``path-prefix:`` 键,它将项目及其导入的仓库放置在工作空间的子目录中。
  请参阅 :ref:`west-manifest-ex3.4` 以获取示例。
- west 命令行应用程序现在也可以使用 ``python3 -m west`` 运行。
  这使得在不修改 :envvar:`PATH` 环境变量的情况下在特定的 Python 解释器下运行 west 变得更加容易。
- :ref:`west manifest --path <west-manifest-path>` 打印 west.yml 的绝对路径
- ``west init`` 现在支持 ``--mf foo.yml`` 选项,它使用 :file:`foo.yml`
  而不是 :file:`west.yml` 初始化工作空间。
- ``west list`` 现在使用 ``manifest.path`` :ref:`配置选项 <west-config>` 打印清单仓库的路径,
  这可能与清单数据中的 ``self: path:`` 值不同。旧行为仍然可用,
  但需要传递新的 ``--manifest-path-from-yaml`` 选项。
- 各种 Python API 变更;详见 :ref:`west-apis`。

v0.7.3
******

这是一个错误修复版本。

- 修复了失败的导入可能使工作空间处于不可用状态的错误
  (详见 [PR #415](https://github.com/zephyrproject-rtos/west/pull/415))

v0.7.2
******

这是一个错误修复和次要功能版本。

- 过滤掉由清单导入带来的重复扩展命令
- 修复了在通过路径查找清单仓库时的 ``west.Manifest.get_projects()``

v0.7.1
******

这是一个错误修复和次要功能版本。

- ``west update --stats`` 现在打印调用子进程的操作的计时、
  每个项目在 west 的 Python 进程中花费的时间以及更新每个项目的总时间。
- ``west topdir`` 总是打印 POSIX 风格的路径
- 次要的控制台输出更改

v0.7.0
******

west 0.7 中主要的用户可见功能是 :ref:`west-manifest-import` 功能。
这允许用户从多个不同的文件加载 west 清单数据,将结果解析为单个逻辑清单。

其他用户可见的变更:

- "west 安装" 的概念在本文档和 west API 文档中已重命名为 "west 工作空间"。
  新术语似乎对大多数人来说比旧术语更容易使用。
- West 清单现在支持 :ref:`模式版本 <west-manifest-schema-version>`。
- "west config" 命令现在可以在工作空间外运行,例如运行
  ``west config --global section.key value`` 来全局设置配置选项的值。
- 有一个新的 :ref:`west topdir <west-built-in-misc>` 命令,
  它打印当前 west 工作空间的根目录。
- ``west -vv init`` 命令现在打印正在执行的 git 操作及其结果。
- 现在强制执行没有项目可以命名为 "manifest" 的限制;名称 "manifest"
  为清单仓库保留,并且可以在诸如 ``west list manifest`` 之类的命令中使用,
  而不是 ``west list path-to-manifest-repository`` 是唯一的方式
- 如果没有名为 "zephyr" 的项目不再是错误。这是使 west 普遍适用于非 Zephyr 用例的努力的一部分。
- 各种错误修复。

对 :ref:`west-apis` 的开发人员可见的变更:

- west.build 和 west.cmake: 已弃用;这是 Zephyr 特定的功能,
  本不应该是 west 的一部分。由于 Zephyr v1.14 LTS 依赖它,
  它将继续包含在发行版中,但将在该版本的 Zephyr 被淘汰时删除。
- west.commands:

  - WestCommand.requires_installation: 已弃用;改用 requires_workspace
  - WestCommand.requires_workspace: 新增
  - WestCommand.has_manifest: 新增
  - WestCommand.manifest: 现在可设置
- west.configuration: 调用者现在可以在读取和写入配置文件时识别工作空间目录
- west.log:

  - msg(): 新增
- west.manifest:

  - 该模块现在使用标准日志模块而不是 west.log
  - QUAL_REFS_WEST: 新增
  - SCHEMA_VERSION: 新增
  - Defaults: 已移除
  - Manifest.as_dict(): 新增
  - Manifest.as_frozen_yaml(): 新增
  - Manifest.as_yaml(): 新增
  - Manifest.from_file() 和 from_data(): 这些工厂方法使用更灵活,对全局状态的依赖更少
  - Manifest.validate(): 新增
  - ManifestImportFailed: 新增
  - ManifestProject: 半弃用,以后可能会被删除。
  - Project: 构造函数现在接受 topdir 参数
  - Project.format() 及其调用者已移除。改用 f-strings。
  - Project.name_and_path: 新增
  - Project.remote_name: 新增
  - Project.sha() 现在捕获 stderr
  - Remote: 已移除

West 现在需要 Python 3.6 或更高版本。此外,某些功能可能依赖于 Python 字典的插入顺序;
这在 CPython 3.6 中只是一个实现细节,但从 Python 3.7 开始是语言规范的一部分。

v0.6.3
******

这个次要版本修复了已弃用的 ``west.cmake`` 模块行为中的错误。

v0.6.2
******

这个次要版本修复了 v0.6.1 中引入的 ``west update --fetch=smart`` 行为中的错误。

所有 v0.6.1 用户必须升级。

v0.6.1
******

.. warning::

   不要使用这个次要版本。请确保改用 v0.6.2。

此次要版本中的用户可见功能包括:

- :ref:`west-update` 命令有一个新的 ``--fetch`` 命令行标志和
  ``update.fetch`` :ref:`配置选项 <west-config>`。默认值 "smart"
  跳过获取本地可用的 SHA 和标签。
- 在 ``west diff``、``west status``、``west forall`` 和 ``west update`` 命令中
  更好且更一致的错误处理。这些命令中的每一个都可以在多个项目上操作;
  如果与一个项目相关的子进程失败,这些命令现在会继续在其余项目上操作。
  如果这些子进程中的任何一个失败,它们现在也都会从 west 进程报告非零错误代码
  (这以前对 ``west forall`` 尤其不适用)。
- :ref:`west manifest <west-built-in-misc>` 命令也更好地处理错误。
- :ref:`west list <west-built-in-misc>` 命令现在即使在项目未克隆时也可以工作,
  只要其格式字符串仅需要可以从清单文件中读取的信息。
  如果格式字符串需要存储在项目仓库中的数据,它仍然会失败,
  例如如果它包含 ``{sha}`` 格式字符串键。
- 在 git 修订版本上操作的命令和选项现在接受缩写的 SHA。
  例如,``west init --mr SHA_PREFIX`` 现在可以工作。以前,
  如果 ``--mr`` 参数不是分支或标签,则需要是完整的 40 字符 SHA。

对 :ref:`west-apis` 的开发人员可见的变更:

- west.log.banner(): 新增
- west.log.small_banner(): 新增
- west.manifest.Manifest.get_projects(): 新增
- west.manifest.Project.is_cloned(): 新增
- west.commands.WestCommand 实例现在可以在 do_run() 调用期间通过新的 self.manifest
  属性访问解析的 Manifest 对象。如果读取,它返回 Manifest 对象,
  或者如果无法解析则中止命令。
- west.manifest.Project.git() 现在有一个 capture_stderr kwarg


v0.6.0
******

- 无单独的引导程序

  在 west v0.5.x 中,该程序被分为两个组件,一个引导程序和一个每个安装的克隆。
  详见 `v1.14 文档中的多仓库管理`_。

  这类似于 Google 的 Repo 工具的工作方式,让 west 一开始可以快速迭代。
  然而,这引起了混乱,west 现在足够稳定,可以完全作为一个整体通过 PyPI 分发。

  从 v0.6.x 开始,所有核心 west 命令和辅助类都是通过 PyPI 分发的 west 包的一部分。
  这消除了复杂性,并使得可以从系统的任何地方导入 west 模块,而不仅仅是扩展命令。
- ``selfupdate`` 命令仍然存在以保持向后兼容性,但现在只是在打印错误消息后退出。
- 清单语法变更

  - west 清单文件的 ``projects`` 元素现在可以直接指定其获取 URL,如下所示:

    .. code-block:: yaml

       manifest:
         projects:
           - name: example-project-name
             url: https://github.com/example/example-project

    以这种方式设置 ``url`` 属性的项目元素不能同时具有 ``remote`` 属性。
  - 项目名称必须是唯一的: 需要这个限制来支持未来的工作,
    但在 west v0.5.x 中这是不可能的,因为不同的项目可能具有相同最终路径名组件的 URL,如下所示:

    .. code-block:: yaml

       manifest:
         remotes:
           - name: remote-1
             url-base: https://github.com/remote-1
           - name: remote-2
             url-base: https://github.com/remote-2
         projects:
           - name: project
             remote: remote-1
             path: remote-1-project
           - name: project
             remote: remote-2
             path: remote-2-project

    这些清单现在可以使用 ``url`` 而不是 ``remote`` 编写项目,如下所示:

    .. code-block:: yaml

       manifest:
         projects:
           - name: remote-1-project
             url: https://github.com/remote-1/project
           - name: remote-2-project
             url: https://github.com/remote-2/project

- ``west list`` 命令现在支持 ``{sha}`` 格式字符串键

- ``west list`` 的默认格式字符串已更改为 ``"{name:12} {path:28} {revision:40} {url}"``。

- 命令 ``west manifest --validate`` 现在可以运行来加载和验证当前的清单文件,
  以及其他与清单解析相关的错误处理修复。

- 对 west 的 API 进行了不兼容的 API 更改。在 west v1.0 中声明 API 稳定性之前,
  预计会有进一步的更改。

  - ``west.manifest.Project`` 构造函数的 ``remote`` 和 ``defaults`` 位置参数现在是 kwargs。
    还添加了一个新的 ``url`` kwarg;如果给定,则将 ``Project`` URL 设置为该值,
    并忽略 ``remote`` kwarg。

  - ``west.manifest.MANIFEST_SECTIONS`` 已移除。现在只有一个部分,即 ``manifest``。
    ``west.manifest.Manifest`` 工厂方法和构造函数中的 *sections* kwargs 也已移除。

  - ``west.manifest.SpecialProject`` 类已移除。改用 ``west.manifest.ManifestProject``。


v0.5.x
******

West v0.5.x 是 Zephyr 项目作为其 v1.14 长期支持 (LTS) 版本的一部分广泛使用的第一个版本。
`west v0.5.x 文档`_ 作为 Zephyr v1.14 文档的一部分提供。

West 在 v0.5.x 中的主要功能包括:

- 使用 Git 仓库进行多仓库管理,包括 west 本身的自更新
- 分层配置文件
- 扩展命令

v0.5.x 之前的版本 (Versions Before v0.5.x)
******************************************

west 仓库中 v0.5.x 之前的标签是原型,仅具有历史意义。

.. _v1.14 文档中的多仓库管理:
   https://docs.zephyrproject.org/1.14.0/guides/west/repo-tool.html

.. _west v0.5.x 文档:
   https://docs.zephyrproject.org/1.14.0/guides/west/index.html
