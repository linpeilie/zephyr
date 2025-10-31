.. _west-config:

配置
####

本页记录了 west 的配置文件系统、``west config`` 命令以及内置命令使用的配置选项。有关 ``west.configuration`` 模块的 API 文档，请参见 :ref:`west-apis-configuration`。

West 配置文件
-------------

West 的配置文件语法类似于 INI 格式；以下是一个示例文件：

.. code-block:: ini

   [manifest]
   path = zephyr

   [zephyr]
   base = zephyr

上面，``manifest`` 部分有选项 ``path`` 设置为 ``zephyr``。另一种说法是 ``manifest.path`` 在此文件中是 ``zephyr``。

配置文件有三种类型：

1. **系统配置**：此文件中的设置影响登录到计算机的每个用户 west 的行为。其位置取决于平台：

   - Linux: :file:`/etc/westconfig`
   - macOS: :file:`/usr/local/etc/westconfig`
   - Windows: :file:`%PROGRAMDATA%\\west\\config`

2. **全局配置**（每个用户）：此文件中的设置影响特定用户在计算机上运行 west 时的行为。

   - 所有平台：默认值是用户主目录中的 :file:`.westconfig`。
   - Linux 注意：如果设置了环境变量 ``XDG_CONFIG_HOME``，则使用 :file:`$XDG_CONFIG_HOME/west/config`。
   - Windows 注意：测试以下环境变量以查找主目录：``%HOME%``，然后是 ``%USERPROFILE%``，然后是 ``%HOMEDRIVE%`` 和 ``%HOMEPATH%`` 的组合。

3. **本地配置**：此文件中的设置影响当前 :term:`west 工作区` 的 west 行为。该文件是 :file:`.west/config`，相对于工作区的根目录。

此列表中较低位置出现的文件中的设置会覆盖较早的设置。例如，如果系统配置文件中的 ``color.ui`` 是 ``true``，但工作区的是 ``false``，则最终值是 ``false``。类似地，用户配置文件中的设置覆盖系统设置，以此类推。

.. _west-config-cmd:

west config
-----------

内置 ``config`` 命令可用于获取和设置配置值。可以向 ``west config`` 传递选项 ``--system``、``--global`` 或 ``--local`` 以指定要使用的配置文件。其中只有一个可以同时使用。如果没有给定，则写入默认为 ``--local``，读取显示应用覆盖后的最终值。

以下是常见用途的一些示例；运行 ``west config -h`` 获取详细帮助，有关内置选项的更多详细信息，请参见 :ref:`west-config-index`。

要将 ``manifest.path`` 设置为 :file:`some-other-manifest`：

.. code-block:: console

   west config manifest.path some-other-manifest

这样做意味着 ``west update`` 之类的命令将在 :file:`some-other-manifest` 目录内（相对于工作区根目录）而不是给予 ``west init`` 的目录中查找 :term:`west 清单`，所以要小心！

要读取 ``zephyr.base``，即如果在调用环境中未设置时将用作 ``ZEPHYR_BASE`` 的值（也相对于工作区根目录）：

.. code-block:: console

   west config zephyr.base

可以在不改变 ``manifest.path`` 的情况下切换到另一个 zephyr 仓库，因此不会改变 ``west update`` 之类命令的行为，使用：

.. code-block:: console

   west config zephyr.base some-other-zephyr

如果使用 ``git worktree`` 之类的命令创建自己的 zephyr 目录，并希望 ``west build`` 之类的命令使用它们而不是清单中指定的 zephyr 仓库，这会很有用。（可以通过运行 ``west config zephyr.base zephyr`` 回到使用上游清单中的目录。）

要在全局（用户范围）配置文件中将 ``color.ui`` 设置为 ``false``，以便该用户在任何工作区中运行 west 时将不再输出彩色输出：

.. code-block:: console

   west config --global color.ui false

要撤销上述更改：

.. code-block:: console

   west config --global color.ui true

.. _west-config-index:

内置配置选项
-----------

下表记录了 west 内置命令支持的配置选项。Zephyr 扩展命令支持的配置选项记录在这些命令的页面中。

.. NOTE: 文档作者：按部分然后选项保持此表排序。

.. list-table::
   :widths: 10 30
   :header-rows: 1

   * - 选项
     - 描述
   * - :samp:`alias.{ALIAS}`
     - 字符串。如果非空，则 ``<ALIAS>`` 可用作 west 命令。参见 :ref:`west-aliases`。
   * - ``color.ui``
     - 布尔值。如果为 ``true``（默认值），则当标准输出是终端时，west 输出被着色。
   * - ``commands.allow_extensions``
     - 布尔值，默认 ``true``，如果为 ``false`` 则禁用 :ref:`west-extensions`
   * - ``grep.color``
     - 字符串，默认为空。将其设置为 ``never`` 以禁用 ``west grep`` 颜色输出。如果设置，``west grep`` 将该值传递给 grep 工具的 ``--color`` 选项。
   * - ``grep.tool``
     - 字符串，``"git-grep"``（默认）、``"ripgrep"`` 或 ``"grep"`` 之一。``west grep`` 应使用的 grep 工具。
   * - ``grep.<TOOL>-args``
     - 字符串，默认为空。``<TOOL>`` 部分是可以是任何 ``grep.tool`` 值的模式，所以 ``grep.ripgrep-args`` 是一个配置选项示例。如果设置，``west grep`` 应传递给相应 grep 工具的参数。运行 ``west help grep`` 获取详细信息。
   * - ``grep.<TOOL>-path``
     - 字符串，默认为空。``<TOOL>`` 部分是可以是任何 ``grep.tool`` 值的模式，所以 ``grep.ripgrep-path`` 是一个配置选项示例。west grep 应使用的相应工具的路径，而不是搜索命令。运行 ``west help grep`` 获取详细信息。
   * - ``manifest.file``
     - 字符串，默认值为 ``west.yml``。从清单仓库根目录到 ``west init`` 和其他解析清单的命令使用的清单文件的相对路径。
   * - ``manifest.group-filter``
     - 字符串，默认为空。工作区内要启用和禁用的项目组的逗号分隔列表。在启用的组前加 ``+`` 前缀，在禁用的组前加 ``-`` 前缀。例如，值 ``"+foo,-bar"`` 启用组 ``foo`` 并禁用 ``bar``。参见 :ref:`west-manifest-groups`。
   * - ``manifest.path``
     - 字符串，从 :term:`west 工作区` 根目录到 ``west update`` 和其他解析清单的命令使用的清单仓库的相对路径。由 ``west init`` 在本地设置。
   * - ``manifest.project-filter``
     - 字符串的逗号分隔列表。

       该选项的值是逗号分隔的正则表达式列表，每个前缀为 ``+`` 或 ``-``，如下所示：

       .. code-block:: none

          +re1,-re2,-re3

       项目名称与列表中的每个正则表达式（``re1``、``re2``、``re3``、...）匹配，按顺序。如果整个项目名称与正则表达式匹配，该列表元素要么停用要么激活项目。如果元素以 ``-`` 开头，则项目被停用。如果元素以 ``+`` 开头，则项目被激活。（如果使用此选项，项目名称不能包含 ``,``，所以正则表达式不需要包含文字 ``,`` 字符。）

       如果项目的名称与列表中的多个正则表达式匹配，则使用最后一个正则表达式的结果。例如，如果 ``manifest.project-filter`` 是：

       .. code-block:: none

          -hal_.*,+hal_foo

       则名为 ``hal_bar`` 的项目是不活跃的，但名为 ``hal_foo`` 的项目是活跃的。

       如果项目被列表元素变为不活跃或活跃，则无论其任何或所有组是否被禁用，项目都是活跃或不活跃的。（这目前是使没有组的项目不活跃的唯一方法。）

       否则，即如果项目与列表中的任何正则表达式都不匹配，则根据与其组相关的常规规则它是活跃或不活跃的（有关该情况下的示例，请参见 :ref:`west-project-group-examples`）。

       在 ``manifest.project-filter`` 列表的元素内，前导和尾随空格被忽略。这意味着这些示例值是等效的：

       .. code-block:: none

          +foo,-bar
          +foo , -bar

       任何空元素都被忽略。这意味着这些示例值是等效的：

       .. code-block:: none

           +foo,,-bar
           +foo,-bar

   * - ``update.auto-cache``
     - 字符串。如果非空，``west update`` 将在命令行上未给定时使用其值作为 ``--auto-cache`` 选项的值。
   * - ``update.fetch``
     - 字符串，``"smart"``（从 v0.6.1 开始的默认行为）或 ``"always"``（之前的行为）之一。如果设置为 ``"smart"``，:ref:`west-update` 命令将跳过从项目远程获取那些项目在清单文件中的修订版本是已本地可用的 SHA 或标签的情况。``"always"`` 行为是无条件从远程获取。
   * - ``update.name-cache``
     - 字符串。如果非空，``west update`` 将在命令行上未给定时使用其值作为 ``--name-cache`` 选项的值。
   * - ``update.narrow``
     - 布尔值。如果为 ``true``，``west update`` 的行为就像在命令行上给定了 ``--narrow`` 一样。默认值是 ``false``。
   * - ``update.path-cache``
     - 字符串。如果非空，``west update`` 将在命令行上未给定时使用其值作为 ``--path-cache`` 选项的值。
   * - ``update.sync-submodules``
     - 布尔值。如果为 ``true``（默认值），:ref:`west-update` 将在更新子模块之前同步 Git 子模块。
   * - ``zephyr.base``
     - 字符串，为 :envvar:`ZEPHYR_BASE` 环境变量设置的默认值，当 west 命令运行时。默认情况下，这在 ``west init`` 期间设置为清单项目的路径，其路径为 :file:`zephyr`（如果存在）。如果变量已设置，则此设置被忽略，除非 ``zephyr.base-prefer`` 是 ``"configfile"``。
   * - ``zephyr.base-prefer``
     - 字符串，值为 ``"env"`` 和 ``"configfile"`` 之一。如果设置为 ``"env"``（默认值），在调用环境中设置 :envvar:`ZEPHYR_BASE` 会覆盖 ``zephyr.base`` 配置选项的值。如果设置为 ``"configfile"``，配置选项会赢取。
