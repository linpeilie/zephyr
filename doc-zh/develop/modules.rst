.. _modules:

模块(外部项目)
############################

Zephyr 依赖于几个外部维护项目的源代码,以避免重复造轮子,并在合理的情况下尽可能重用经过充分验证的成熟代码。在 Zephyr 构建系统的上下文中,这些被称为 *模块*。这些模块必须与 Zephyr 构建系统集成,本页其他部分将对此进行更详细的描述。

要被归类为包含在默认模块列表中的候选项,外部项目需要在 Zephyr 项目之外拥有自己的生命周期,即驻留在自己的仓库中,并拥有自己的贡献和维护工作流程以及发布过程。Zephyr 模块不应包含专门为 Zephyr 编写的代码。相反,此类代码应贡献给主 zephyr 树。

要包含在 Zephyr 项目的默认清单中的模块需要提供由项目技术指导委员会认可和批准的功能或特性,并应符合 :ref:`模块许可要求<modules_licensing>` 和 :ref:`贡献指南<modules_contributing>`。它们还应有一个致力于维护模块代码库的 Zephyr 开发人员。

Zephyr 依赖于几类模块,包括但不限于:

- 调试器集成
- 芯片供应商硬件抽象层 (HAL)
- 加密库
- 文件系统
- 进程间通信 (IPC) 库

此外,在某些情况下,模块(特别是供应商 HAL)可以包含对可选 :ref:`二进制 blob <bin-blobs>` 的引用。

本页总结了一系列旨在更好地组织 Zephyr 模块工作流程的策略和最佳实践。

.. _modules-vs-projects:

模块与 west 项目
************************

本页描述的 Zephyr 模块与 :ref:`west 项目 <west-workspace>` 不同。实际上,模块 :ref:`根本不需要 west <modules_without_west>`。但是,在 :ref:`使用 west 的模块 <modules_using_west>` 时,构建系统使用 west 来查找模块。

总之:

模块是包含 :file:`zephyr/module.yml` 文件的仓库,以便 Zephyr 构建系统可以从仓库中拉取源代码。:ref:`West 项目 <west-manifests-projects>` 是 :file:`west.yml` 清单文件中 ``projects:`` 部分的条目。West 项目通常也是模块,但并非总是如此。有些 West 项目不包含在最终固件映像中(例如工具),因此不需要作为模块。模块由 Zephyr 构建系统通过 :ref:`west 本身 <modules_using_west>` 或通过 :ref:`ZEPHYR_MODULES CMake 变量 <modules_without_west>` 找到。

本页内容仅适用于模块,而不适用于一般的 West 项目(除非它们本身是模块)。


模块仓库
*******************

* 默认清单中包含的所有模块都应托管在 zephyrproject-rtos GitHub 组织下的仓库中。

* 模块仓库代码库应在仓库根目录的 :file:`zephyr/` 文件夹中包含一个 *module.yml* 文件。

* 模块仓库名称应遵循使用小写字母和短划线而不是下划线的约定。此规则将适用于所有新模块仓库,但直接跟踪外部项目(托管在 Git 仓库中)的仓库除外;此类模块可以与其外部项目对应项同名。

  .. note::

     不符合上述约定的现有模块仓库无需重命名以符合上述约定。

* 模块仓库名称应在 :file:`zephyr/module.yml` 文件中明确设置。

* 模块应使用 "zephyr" 作为仓库主分支的默认名称。用于特定目的的分支,例如 LTS Zephyr 版本的模块分支,应具有以 'zephyr\_' 前缀开头的名称。

* 如果模块有外部(上游)项目仓库,模块仓库应保留上游仓库的文件夹结构。

  .. note::

     模块仓库中不需要维护镜像外部仓库主分支的 'master' 分支。不建议这样做,因为这可能会在模块的主分支周围产生混淆,主分支应该是 'zephyr'。

* 模块应公开所有提供的头文件,包含路径名以模块名称开头。(例如,mcuboot 应将其 ``bootutil/bootutil.h`` 公开为 "mcuboot/bootutil/bootutil.h"。)

.. _modules_synchronization:

与上游同步
===========================

首选将模块仓库与相应外部项目的最新稳定版本同步。但是,如果需要获取模块代码库中的重要更新,则允许使用最新开发分支尖端更新 Zephyr 模块仓库。将模块与上游同步时,必须记录执行特定更新的理由。

允许实践的要求
----------------------------------

对模块仓库主分支的更改,包括与上游代码库的同步,只能通过拉取请求应用。这些拉取请求应可由 Zephyr CI *验证*,并且可*合并*(例如,使用 Github UI 的 *Rebase and merge* 或 *Create a merge commit* 选项)。这确保传入的更改始终是**可审查的**,并且*下游*模块仓库历史是增量的(即,现有提交、标签等始终被保留)。此策略还允许直接对要引入模块仓库的更改集运行 Zephyr CI、git lint、身份和许可检查。

.. note::

     不允许强制推送到模块的主分支。

允许的实践
-----------------

以下实践符合上述要求,应在所有模块仓库中遵循。由模块代码所有者选择首选的同步实践,但是,要求在相应的模块仓库中一致地遵循所选实践。

**使用上游的差异更新模块:**
将上游更改作为单个*快照*提交(手动差异)引入到针对模块主分支的拉取请求中,可以使用 *Rebase & merge* 操作合并。这种方法很简单,应该适用于所有模块,缺点是抑制了模块仓库中的上游历史。

  .. note::

     上述实践是外部项目未托管在上游 Git 仓库中的模块中唯一允许的实践。

提交消息应标识上游项目 URL、模块更新到的版本(上游版本、标签、提交 SHA,如果适用等)以及进行更新的原因。

**通过合并上游分支更新模块:**
通过执行预期上游分支(例如主分支、最新发布分支等)的 Git 合并引入上游更改,在针对模块主分支的拉取请求中提交结果,并使用 *Create a merge commit* 操作合并拉取请求。此方法适用于具有上游项目 Git 仓库的模块。这种方法的主要优点是在模块仓库中保留了上游仓库历史(即原始提交 SHA)。这种方法的缺点是在下游主分支中生成两个额外的合并提交。


为 Zephyr 模块做贡献
******************************

.. _modules_contributing:


个人角色和职责
===================================

为便于管理 Zephyr 模块仓库,定义了以下个人角色。

**管理员:** 每个 Zephyr 模块都应有一个管理员,负责管理对模块仓库的访问,例如,根据模块所有者的请求将个人添加为仓库中的协作者。模块管理员是管理员团队的成员,即具有模块 GitHub 仓库管理权限的项目成员组。

**模块所有者:** 每个模块都应有一个模块代码所有者。模块所有者将对 Zephyr 模块仓库的内容负全面责任。特别是,模块所有者将:

* 协调模块仓库中的代码审查
* 成为针对仓库主分支的拉取请求的默认受让人
* 根据需要请求将其他协作者添加到仓库
* 按照 :ref:`modules_synchronization` 中描述的策略定期将模块仓库与其上游对应项同步
* 了解外部项目中的安全漏洞问题,并在上游代码库中提供安全修复后立即更新模块仓库以包含安全修复
* 在 Zephyr 发布说明中列出模块代码库中存在的任何已知安全漏洞问题。


  .. note::

     模块所有者不需要是 Zephyr :ref:`维护者 <project_roles>`。

**合并者:** Zephyr 发布工程团队有权和责任在模块仓库的主分支中合并已批准的拉取请求。


维护模块代码库
===============================

zephyr 主树中的更新,例如公共 Zephyr API 中的更新,可能需要修补模块的代码库。保持模块代码库最新的责任由 Zephyr 中此类更新的**贡献者**和模块**所有者**共同承担。特别是:

* Zephyr 中原始更改的贡献者需要提交模块仓库中所需的相应更改,以确保具有原始更改的拉取请求上的 Zephyr CI 以及模块集成测试成功。

* 模块所有者负责将模块代码库与 zephyr 主树同步和测试的全面责任。这包括除 Zephyr 的 CI 执行的测试之外,偶尔对模块代码库进行高级测试。模块所有者需要修复模块代码库中
    模块代码库中未被 Zephyr 拉取请求 CI 运行捕获的问题。


.. _modules_changes:

为模块贡献更改
===============================

在合并到相应的外部项目仓库之前,直接向模块代码库提交和合并更改应仅限于:

* 由于 zephyr 主树中的更新而需要的更改
* 不应等待首先在外部项目中合并的紧急更改,例如安全漏洞修复。

如果模块具有上游项目仓库,则应阻止对模块代码库的非平凡更改,包括模块设计或功能的更改。在这种情况下,此类更改应直接提交到上游项目。

:ref:`向模块提交更改 <submitting_new_modules>` 详细描述了向模块仓库贡献更改的过程。

贡献指南
-----------------------

为 Zephyr 模块做贡献应遵循通用项目 :ref:`贡献指南 <contribute_guidelines>`。

**拉取请求:** 可以在至少 2 个批准的情况下合并,包括 PR 受让人的批准。除此之外,模块仓库中的拉取请求只能在引入的更改经过 Zephyr CI 工具验证后才能合并,如本页其他部分所详述。

在模块仓库的主分支中合并拉取请求必须与 zephyr 主树中相应的清单文件更新相结合。

**问题报告:** 模块仓库中有意禁用了 `GitHub issues`_,以支持集中式问题报告策略。有关模块中的错误或增强功能等的工单应在主 zephyr 仓库中打开。在适用的情况下,应使用与每个模块对应的 GitHub 标签适当地标记问题。

  .. note::

     允许为 zephyr 模块提交错误报告以跟踪 Zephyr 中相应的上游项目错误。这些错误报告不应影响 :ref:`发布质量标准<release_quality_criteria>`。


.. _modules_licensing:

许可要求和策略
***********************************

模块代码库中的所有源文件都应包含许可证头,除非模块仓库具有涵盖不包含许可证头的源文件的**主许可证文件**。

主许可证文件应由 Zephyr 开发人员添加到模块的代码库中,仅当它们作为外部项目的一部分存在,并且它们包含宽松的 OSI 兼容许可证时。主许可证文件最好包含完整的许可证文本,而不是包含 SPDX 许可证标识符。如果存在多个主许可证文件,则应明确说明哪个许可证适用于模块代码库中的每个源文件。

模块源文件中的各个许可证头优先于主许可证。

要添加到模块仓库中的任何新内容都需要有许可证覆盖。

  .. note::

     Zephyr 建议通过各个许可证头和主许可证文件传达模块许可。这不是硬性要求;如果外部项目有自己的实践来传达许可证如何应用于模块的代码库(例如,通过拥有单个或多个主许可证文件),则此实践可以被 Zephyr 模块接受并引用,只要满足许可要求,例如 OSI 合规性。

许可证策略
================

创建模块仓库时,开发人员应:

* 如果外部项目中存在主许可证文件,则导入主许可证文件,并
* 记录(例如在模块 README 或 .yml 文件中)涵盖模块代码库的默认许可证。

许可证检查
--------------

应在模块仓库中添加新内容的每个拉取请求上启用许可证检查(通过 CI 工具)。


.. _modules_changes:

为模块贡献更改
===============================

在合并到相应的外部项目仓库之前,直接向模块代码库提交和合并更改应仅限于:

* 由于 zephyr 主树中的更新而需要的更改
* 不应等待首先在外部项目中合并的紧急更改,例如安全漏洞修复。

如果模块具有上游项目仓库,则应阻止对模块代码库的非平凡更改,包括模块设计或功能的更改。在这种情况下,此类更改应直接提交到上游项目。

:ref:`向模块提交更改 <submitting_new_modules>` 详细描述了向模块仓库贡献更改的过程。

贡献指南
-----------------------

为 Zephyr 模块做贡献应遵循通用项目 :ref:`贡献指南 <contribute_guidelines>`。

**拉取请求:** 可以在至少 2 个批准的情况下合并,包括 PR 受让人的批准。除此之外,模块仓库中的拉取请求只能在引入的更改经过 Zephyr CI 工具验证后才能合并,如本页其他部分所详述。

在模块仓库的主分支中合并拉取请求必须与 zephyr 主树中相应的清单文件更新相结合。

**问题报告:** 模块仓库中有意禁用了 `GitHub issues`_,以支持集中式问题报告策略。有关模块中的错误或增强功能等的工单应在主 zephyr 仓库中打开。在适用的情况下,应使用与每个模块对应的 GitHub 标签适当地标记问题。

  .. note::

     允许为 zephyr 模块提交错误报告以跟踪 Zephyr 中相应的上游项目错误。这些错误报告不应影响 :ref:`发布质量标准<release_quality_criteria>`。


.. _modules_licensing:

许可要求和策略
***********************************

模块代码库中的所有源文件都应包含许可证头,除非模块仓库具有涵盖不包含许可证头的源文件的**主许可证文件**。

主许可证文件应由 Zephyr 开发人员添加到模块的代码库中,仅当它们作为外部项目的一部分存在,并且它们包含宽松的 OSI 兼容许可证时。主许可证文件最好包含完整的许可证文本,而不是包含 SPDX 许可证标识符。如果存在多个主许可证文件,则应明确说明哪个许可证适用于模块代码库中的每个源文件。

模块源文件中的单独许可证头取代主许可证。

要添加到模块仓库的任何新内容都需要具有许可证覆盖范围。

  .. note::

     Zephyr 建议通过单独的许可证头和主许可证文件传达模块许可。这不是硬性要求;如果外部项目在模块的代码库中传达许可应用方式时有其自己的实践(例如,通过具有单个或多个主许可证文件),只要满足许可要求(例如 OSI 合规性),此实践可以被 Zephyr 模块接受并引用。

许可策略
================

在创建模块仓库时,开发人员应:

* 导入主许可证文件(如果它们存在于外部项目中),并且
* 记录(例如在模块 README 或 .yml 文件中)涵盖模块代码库的默认许可证。

许可检查
--------------

许可检查(通过 CI 工具)应在向模块仓库添加新内容的每个拉取请求上启用。


文档要求
**************************

所有 Zephyr 模块仓库都应包含一个 .rst 文件,记录:

* 模块的范围和目的
* 模块如何与 Zephyr 集成
* 模块仓库的所有者
* 与外部项目的同步信息(提交、SHA、版本等)
* :ref:`modules_licensing` 中描述的许可信息。

包含模块时应要求该文件,并应保持所包含信息的最新。


测试要求
********************

所有 Zephyr 模块都应提供一定级别的**集成**测试,确保与 Zephyr 的集成正常工作。集成测试:

* 可以是驻留在 zephyr 主树中的最小示例和测试集的形式
* 应验证与 Zephyr 集成的模块的基本用法(配置、功能 API 等)。
* 应作为引入模块仓库更改的拉取请求中的 twister 运行的一部分构建和执行(例如在 QEMU 中)。

  .. note::

     作为包含在 Zephyr 默认清单中的候选项的新模块应提供一定级别的集成测试。

  .. note::

     供应商 HAL 通过在目标平台上构建或执行的 Zephyr 测试进行隐式测试,因此它们不需要提供集成测试。

集成测试的目的不是提供模块的功能验证;这应该是外部项目测试框架的一部分。

某些外部项目提供驻留在上游测试基础设施中但专门为 Zephyr 编写的测试套件。这些测试可以(但不要求)成为 Zephyr 测试框架的一部分。

弃用和删除模块
*********************************

可能由于以下原因弃用模块,包括但不限于:

* 模块中缺乏维护
* 外部项目中的许可更改
* 代码库过时

模块信息应指示模块是否已弃用,并且在尝试使用已弃用的模块构建 Zephyr 时,构建系统应发出警告。

已弃用的模块可以在 2 个 Zephyr 版本后从 Zephyr 默认清单中删除。

  .. note::

     已删除模块的仓库应通过其原始 URL 保持可访问,因为较旧的 Zephyr 版本需要它们。


在 Zephyr 构建系统中集成模块
****************************************

构建系统变量 :makevar:`ZEPHYR_MODULES` 是包含 Zephyr 模块的目录的绝对路径的 `CMake list`_。这些模块包含 :file:`CMakeLists.txt` 和 :file:`Kconfig` 文件,分别描述如何构建和配置它们。模块 :file:`CMakeLists.txt` 文件使用 CMake 的 `add_subdirectory()`_ 命令添加到构建中,并且
:file:`Kconfig` 文件包含在构建的 Kconfig 菜单树中。

如果您安装了 :ref:`west <west>`,则除非您要添加新模块,否则无需担心如何定义此变量。构建系统知道如何使用 west 设置 :makevar:`ZEPHYR_MODULES`。您可以通过设置 :makevar:`EXTRA_ZEPHYR_MODULES` CMake 变量或向 ``.zephyrrc`` 添加 :makevar:`EXTRA_ZEPHYR_MODULES` 行来向此列表添加其他模块(有关更多详细信息,请参阅 :ref:`env_vars` 部分)。如果您想保留使用 west 找到的模块列表并同时添加自己的模块,这会很有用。如果在多个地方设置了 :makevar:`EXTRA_ZEPHYR_MODULES`,例如作为环境变量和 CMake 变量,其他模块的最终列表将是所有来源的合并结果。

.. note::
   如果模块 ``FOO`` 由 :ref:`west <west>` 提供,但也通过 ``-DEXTRA_ZEPHYR_MODULES=/<path>/foo`` 给出,则命令行变量 :makevar:`EXTRA_ZEPHYR_MODULES` 给出的模块将优先。这允许您在构建时使用自定义版本的 ``FOO``,同时仍使用 :ref:`west <west>` 提供的其他 Zephyr 模块。例如,这对于特殊测试目的很有用。

如果您想永久地将模块添加到 zephyr 工作空间,并且您正在使用 zephyr 作为清单仓库,您还可以将 west 清单文件添加到 :zephyr_file:`submanifests` 目录中。有关更多详细信息,请参阅 :zephyr_file:`submanifests/README.txt`。

有关 west 工作空间的更多信息,请参阅 :ref:`west-basics`。

最后,您还可以以各种方式自己指定模块列表,或者如果您的应用不需要模块,则根本不使用模块。

.. _module-yml:

模块 yaml 文件描述
****************************

可以使用名为 :file:`zephyr/module.yml` 的文件描述模块。:file:`zephyr/module.yml` 的格式如下所述:

模块名称
===========

每个 Zephyr 模块都被赋予一个名称,构建系统可以通过该名称引用它。

名称应在 :file:`zephyr/module.yml` 文件中指定。这将确保模块名称不会通过用户定义的目录名称或 ``west`` 清单文件更改:

.. code-block:: yaml

   name: <name>

在 CMake 中,然后可以使用 CMake 变量 ``ZEPHYR_<MODULE_NAME>_MODULE_DIR`` 引用 Zephyr 模块的位置,变量 ``ZEPHYR_<MODULE_NAME>_CMAKE_DIR`` 保存包含模块的 :file:`CMakeLists.txt` 文件的目录的位置。

.. note::
   当用于 CMake 和 Kconfig 变量时,模块名称中的所有字母都转换为大写,所有非字母数字字符都转换为下划线 (_)。例如,模块 ``foo-bar`` 必须在 CMake 和 Kconfig 中引用为 ``ZEPHYR_FOO_BAR_MODULE_DIR``。

以下是 Zephyr 模块 ``foo`` 的示例:

.. code-block:: yaml

   name: foo

.. note::
   如果未指定 ``name`` 字段,则 Zephyr 模块名称将设置为模块文件夹的名称。例如,位于 :file:`<workspace>/modules/bar` 中的 Zephyr 模块如果在 :file:`zephyr/module.yml` 中未指定任何内容,将使用 ``bar`` 作为其模块名称。

模块集成文件(模块内)
====================================

可以如下描述构建文件 :file:`CMakeLists.txt` 和 :file:`Kconfig` 的包含:

.. code-block:: yaml

   build:
     cmake: <cmake-directory>
     kconfig: <directory>/Kconfig

``cmake: <cmake-directory>`` 部分指定 :file:`<cmake-directory>` 包含要使用的 :file:`CMakeLists.txt`。``kconfig: <directory>/Kconfig`` 部分指定要使用的 Kconfig 文件。两者都不是必需的:``cmake`` 默认为 ``zephyr``,``kconfig`` 默认为 ``zephyr/Kconfig``。

以下是引用模块根目录中的 :file:`CMakeLists.txt` 和 :file:`Kconfig` 文件的 :file:`module.yml` 文件示例:

.. code-block:: yaml

   build:
     cmake: .
     kconfig: Kconfig

.. _sysbuild_module_integration:

Sysbuild 集成
====================

:ref:`Sysbuild<sysbuild>` 是 Zephyr 构建系统,允许作为单个应用的一部分构建多个映像,sysbuild 构建过程可以根据需要使用模块进行外部扩展,例如添加自定义构建步骤或向构建添加额外的目标。可以如下描述 sysbuild 特定构建文件 :file:`CMakeLists.txt` 和 :file:`Kconfig` 的包含:

.. code-block:: yaml

   build:
     sysbuild-cmake: <cmake-directory>
     sysbuild-kconfig: <directory>/Kconfig

``sysbuild-cmake: <cmake-directory>`` 部分指定 :file:`<cmake-directory>` 包含要使用的 :file:`CMakeLists.txt`。``sysbuild-kconfig: <directory>/Kconfig`` 部分指定要使用的 Kconfig 文件。

以下是引用模块的 ``sysbuild`` 目录中的 :file:`CMakeLists.txt` 和 :file:`Kconfig` 文件的 :file:`module.yml` 文件示例:

.. code-block:: yaml

   build:
     sysbuild-cmake: sysbuild
     sysbuild-kconfig: sysbuild/Kconfig

模块描述文件 :file:`zephyr/module.yml` 还可用于指定构建文件 :file:`CMakeLists.txt` 和 :file:`Kconfig` 位于 :ref:`modules_module_ext_root` 中。

位于 ``MODULE_EXT_ROOT`` 中的构建文件可以如下描述:

.. code-block:: yaml

   build:
     sysbuild-cmake-ext: True
     sysbuild-kconfig-ext: True

这允许在 Zephyr 模块外部描述构建包含的控制。

.. _modules-vulnerability-monitoring:

漏洞监控
========================

模块描述文件 :file:`zephyr/module.yml` 可用于改进漏洞监控。

如果您的模块需要使用外部引用跟踪漏洞(例如您的模块是从另一个仓库分叉的),您可以使用 ``security`` 部分。它包含 ``external-references`` 字段,该字段包含需要为您的模块监控的引用列表。支持的格式为:

- CPE (通用平台枚举)
- PURL (包 URL)

.. code-block:: yaml

   security:
     external-references:
       - <module-related-cpe>
       - <an-other-module-related-cpe>
       - <module-related-purl>

``mbedTLS`` 模块的真实示例可能如下所示:

.. code-block:: yaml

   security:
     external-references:
       - cpe:2.3:a:arm:mbed_tls:3.5.2:*:*:*:*:*:*:*
       - pkg:github/Mbed-TLS/mbedtls@V3.5.2

.. note::
   CPE 字段必须遵循 `NVD <https://csrc.nist.gov/projects/security-content-automation-protocol/specifications/cpe>`_ 提供的 CPE 2.3 架构。PURL 字段必须遵循 `Github <https://github.com/package-url/purl-spec/blob/master/PURL-SPECIFICATION.rst>`_ 提供的 PURL 规范。


构建系统集成
========================

当模块具有 :file:`module.yml` 文件时,它将自动包含在 Zephyr 构建系统中。然后可以通过 Kconfig 和 CMake 变量访问模块的路径。

Zephyr 模块
--------------

在 Kconfig 和 CMake 中,变量 ``ZEPHYR_<MODULE_NAME>_MODULE_DIR`` 包含模块的绝对路径。

此外,会为可用模块自动生成 ``ZEPHYR_<MODULE_NAME>_MODULE`` 和 ``ZEPHYR_<MODULE_NAME>_MODULE_BLOBS``(如果模块声明了 blob)符号。例如,这些可用于从依赖于模块或模块中的 blob 的其他 Kconfig 符号声明依赖关系。为了在没有模块的情况下构建 Zephyr 时满足合规性检查,建议模块在 Zephyr 主树的 ``modules/`` 下的相应 Kconfig 文件中为这些符号提供默认定义。

在 CMake 中,``ZEPHYR_<MODULE_NAME>_CMAKE_DIR`` 包含包含 :file:`CMakeLists.txt` 文件的目录的绝对路径,该文件包含在 CMake 构建系统中。如果 module.yml 文件未指定 CMakeLists.txt,则此变量的值为空。

要读取名为 ``foo`` 的 Zephyr 模块的这些变量:

- 在 CMake 中: 对于模块的顶级目录使用 ``${ZEPHYR_FOO_MODULE_DIR}``,对于包含其 :file:`CMakeLists.txt` 的目录使用 ``${ZEPHYR_FOO_CMAKE_DIR}``
- 在 Kconfig 中: 对于模块的顶级目录使用 ``$(ZEPHYR_FOO_MODULE_DIR)``

请注意小写模块名称 ``foo`` 在 CMake 和 Kconfig 中都大写为 ``FOO``。

这些变量还可用于测试给定模块是否存在。例如,要验证 ``foo`` 是 Zephyr 模块的名称:

.. code-block:: cmake

  if(ZEPHYR_FOO_MODULE_DIR)
    # 如果 FOO 存在则执行某些操作。
  endif()

在 Kconfig 中,该变量可用于查找要包含的其他文件。例如,要在模块 ``foo`` 中包含文件 :file:`some/Kconfig`:

.. code-block:: kconfig

  source "$(ZEPHYR_FOO_MODULE_DIR)/some/Kconfig"

在处理每个 Zephyr 模块的 CMake 期间,还可以使用以下变量:

- 当前模块的名称: ``${ZEPHYR_CURRENT_MODULE_NAME}``
- 当前模块的顶级目录: ``${ZEPHYR_CURRENT_MODULE_DIR}``
- 当前模块的 :file:`CMakeLists.txt` 目录: ``${ZEPHYR_CURRENT_CMAKE_DIR}``

这消除了 Zephyr 模块在 CMake 处理期间需要知道自己名称的需要。模块可以使用这些 ``CURRENT`` 变量引用其他 CMake 文件。例如:

.. code-block:: cmake

  include(${ZEPHYR_CURRENT_MODULE_DIR}/cmake/code.cmake)

可以从模块的第一个 CMakeLists.txt 文件向 Zephyr `CMake list`_ 变量附加值。为此,将值附加到列表,然后在 CMakeLists.txt 文件的 PARENT_SCOPE 中设置列表。例如,要将 ``bar`` 附加到 Zephyr CMakeLists.txt 范围中的 ``FOO_LIST`` 变量:

.. code-block:: cmake

  list(APPEND FOO_LIST bar)
  set(FOO_LIST ${FOO_LIST} PARENT_SCOPE)

一个有用的 Zephyr 列表示例是向 ``SYSCALL_INCLUDE_DIRS`` 列表添加其他目录时。

Sysbuild 模块
----------------

在 Kconfig 和 CMake 中,变量 ``SYSBUILD_CURRENT_MODULE_DIR`` 包含 sysbuild 模块的绝对路径。在 CMake 中,``SYSBUILD_CURRENT_CMAKE_DIR`` 包含包含 :file:`CMakeLists.txt` 文件的目录的绝对路径,该文件包含在 CMake 构建系统中。如果 module.yml 文件未指定 CMakeLists.txt,则此变量的值为空。

要读取 sysbuild 模块的这些变量:

- 在 CMake 中: 对于模块的顶级目录使用 ``${SYSBUILD_CURRENT_MODULE_DIR}``,对于包含其 :file:`CMakeLists.txt` 的目录使用 ``${SYSBUILD_CURRENT_CMAKE_DIR}``
- 在 Kconfig 中: 对于模块的顶级目录使用 ``$(SYSBUILD_CURRENT_MODULE_DIR)``

在 Kconfig 中,该变量可用于查找要包含的其他文件。例如,要包含文件 :file:`some/Kconfig`:

.. code-block:: kconfig

  source "$(SYSBUILD_CURRENT_MODULE_DIR)/some/Kconfig"

模块可以使用这些变量引用其他 CMake 文件。例如:

.. code-block:: cmake

  include(${SYSBUILD_CURRENT_MODULE_DIR}/cmake/code.cmake)

可以从模块的第一个 CMakeLists.txt 文件向 Zephyr `CMake list`_ 变量附加值。为此,将值附加到列表,然后在 CMakeLists.txt 文件的 PARENT_SCOPE 中设置列表。例如,要将 ``bar`` 附加到 Zephyr CMakeLists.txt 范围中的 ``FOO_LIST`` 变量:

.. code-block:: cmake

  list(APPEND FOO_LIST bar)
  set(FOO_LIST ${FOO_LIST} PARENT_SCOPE)

Sysbuild 模块钩子
----------------------

Sysbuild 提供了一个基础设施,允许 sysbuild 模块定义一个函数,该函数将在 CMake 流程中的预定义点由 sysbuild 调用。

sysbuild 调用的函数:

- ``<module-name>_pre_cmake(IMAGES <images>)``: 在为所有映像调用 CMake 配置之前,为每个 sysbuild 模块调用此函数。
- ``<module-name>_post_cmake(IMAGES <images>)``: 在所有映像的 CMake 配置完成后,为每个 sysbuild 模块调用此函数。
- ``<module-name>_pre_domains(IMAGES <images>)``: 在 sysbuild 创建 domains yaml 之前,为每个 sysbuild 模块调用此函数。
- ``<module-name>_post_domains(IMAGES <images>)``: 在 sysbuild 创建 domains yaml 之后,为每个 sysbuild 模块调用此函数。

从 sysbuild 传递给模块定义的函数的参数:

- ``<images>`` 是构建系统将创建的 Zephyr 映像列表。

如果模块 ``foo`` 想要提供 post CMake 配置函数,则模块的 sysbuild :file:`CMakeLists.txt` 文件必须定义函数 ``foo_post_cmake()``。

为了便于命名函数,在加载模块的 sysbuild :file:`CMakeLists.txt` 文件时,sysbuild CMake 通过 ``SYSBUILD_CURRENT_MODULE_NAME`` CMake 变量提供模块名称。

``foo`` sysbuild 模块如何定义 ``foo_post_cmake()`` 的示例:

.. code-block:: cmake

   function(${SYSBUILD_CURRENT_MODULE_NAME}_post_cmake)
     cmake_parse_arguments(POST_CMAKE "" "" "IMAGES" ${ARGN})

     message("Invoking ${CMAKE_CURRENT_FUNCTION}. Images: ${POST_CMAKE_IMAGES}")
   endfunction()

Zephyr 模块依赖关系
==========================

Zephyr 模块可能依赖于其他 Zephyr 模块的存在才能正常运行。或者可能是给定的 Zephyr 模块必须在另一个 Zephyr 模块之后处理,这是由于某些 CMake 目标的依赖关系。

可以使用 ``depends`` 字段描述这种依赖关系。

.. code-block:: yaml

   build:
     depends:
       - <module>

以下是依赖于 Zephyr 模块 ``bar`` 存在于构建系统中的 Zephyr 模块 ``foo`` 的示例:

.. code-block:: yaml

   name: foo
   build:
     depends:
       - bar

此示例将确保在将 ``foo`` 包含到构建系统时 ``bar`` 存在,并且还将确保在 ``foo`` 之前处理 ``bar``。

.. _modules_module_ext_root:

模块集成文件(外部)
===================================

模块集成文件可以位于 Zephyr 模块本身的外部。``MODULE_EXT_ROOT`` 变量保存包含位于 Zephyr 模块外部的集成文件的根列表。

Zephyr 中的模块集成文件
----------------------------------

Zephyr 仓库包含某些已知 Zephyr 模块的 :file:`CMakeLists.txt` 和 :file:`Kconfig` 构建文件。

这些文件位于

.. code-block:: none

   <ZEPHYR_BASE>
   └── modules
       └── <module_name>
           ├── CMakeLists.txt
           └── Kconfig

自定义位置中的模块集成文件
---------------------------------------------

您可以为其他模块创建类似的 ``MODULE_EXT_ROOT``,并使 Zephyr 构建系统知道这些模块。

使用以下结构创建 ``MODULE_EXT_ROOT``

.. code-block:: none

   <MODULE_EXT_ROOT>
   └── modules
       ├── modules.cmake
       └── <module_name>
           ├── CMakeLists.txt
           └── Kconfig

然后通过向 CMake 构建系统指定 ``-DMODULE_EXT_ROOT`` 参数来构建应用程序。``MODULE_EXT_ROOT`` 接受一个 `CMake list`_ 的根作为参数。

可以使用模块描述文件 :file:`zephyr/module.yml` 将 Zephyr 模块自动添加到 ``MODULE_EXT_ROOT`` 列表,请参见 :ref:`modules_build_settings`。

.. note::

   ``ZEPHYR_BASE`` 始终作为优先级最低的 ``MODULE_EXT_ROOT`` 添加。这允许您使用自己的 ``MODULE_EXT_ROOT`` 中的实现覆盖 ``<ZEPHYR_BASE>/modules/<module_name>`` 下的任何集成文件。

:file:`modules.cmake` 文件必须包含通过特定命名的 CMake 变量为 Zephyr 模块指定集成文件的逻辑。

要包含模块的 CMake 文件,请将变量 ``ZEPHYR_<MODULE_NAME>_CMAKE_DIR`` 设置为包含 CMake 文件的路径。

要包含模块的 Kconfig 文件,请将变量 ``ZEPHYR_<MODULE_NAME>_KCONFIG`` 设置为 Kconfig 文件的路径。

以下是如何添加对 ``FOO`` 模块的支持的示例。

创建以下结构

.. code-block:: none

   <MODULE_EXT_ROOT>
   └── modules
       ├── modules.cmake
       └── foo
           ├── CMakeLists.txt
           └── Kconfig

并在 :file:`modules.cmake` 文件中,添加以下内容

.. code-block:: cmake

   set(ZEPHYR_FOO_CMAKE_DIR ${CMAKE_CURRENT_LIST_DIR}/foo)
   set(ZEPHYR_FOO_KCONFIG   ${CMAKE_CURRENT_LIST_DIR}/foo/Kconfig)

模块集成文件(zephyr/module.yml)
--------------------------------------------

模块描述文件 :file:`zephyr/module.yml` 可用于指定构建文件 :file:`CMakeLists.txt` 和 :file:`Kconfig` 位于 :ref:`modules_module_ext_root` 中。

位于 ``MODULE_EXT_ROOT`` 中的构建文件可以描述为:

.. code-block:: yaml

   build:
     cmake-ext: True
     kconfig-ext: True

这允许在 Zephyr 模块外部描述构建包含的控制。

Zephyr 仓库本身始终作为 Zephyr 模块扩展根添加。

.. _modules_build_settings:

构建设置
==============

可以指定在将模块包含到构建系统中时必须使用的其他构建设置。

所有 ``root`` 设置都相对于模块的根。

:file:`module.yml` 文件中支持的构建设置有:

- ``board_root``: 包含构建系统可用的其他开发板。其他开发板必须位于 :file:`<board_root>/boards` 文件夹中。
- ``dts_root``: 包含与架构/SoC 系列相关的其他 dts 文件。其他 dts 文件必须位于 :file:`<dts_root>/dts` 文件夹中。
- ``snippet_root``: 包含可供使用的其他片段。这些片段必须在 :file:`<snippet_root>/snippets` 文件夹下的 :file:`snippet.yml` 文件中定义。例如,如果您有 ``snippet_root: foo``,则应将模块的 :file:`snippet.yml` 文件放在 :file:`<your-module>/foo/snippets` 或任何嵌套子目录中。
- ``soc_root``: 包含构建系统可用的其他 SoC。其他 SoC 必须位于 :file:`<soc_root>/soc` 文件夹中。
- ``arch_root``: 包含构建系统可用的其他架构。其他架构必须位于 :file:`<arch_root>/arch` 文件夹中。
- ``module_ext_root``: 包含 Zephyr 模块的 :file:`CMakeLists.txt` 和 :file:`Kconfig` 文件,另请参见 :ref:`modules_module_ext_root`。
- ``sca_root``: 包含构建系统可用的其他 :ref:`SCA <sca>` 工具实现。每个工具必须位于 :file:`<sca_root>/sca/<tool>` 文件夹中。该文件夹必须包含 :file:`sca.cmake`。

包含其他根的 :file:`module.yaml` 文件示例,以及相应的文件系统布局。

.. code-block:: yaml

   build:
     settings:
       board_root: .
       dts_root: .
       soc_root: .
       arch_root: .
       module_ext_root: .


需要以下文件夹结构:

.. code-block:: none

   <zephyr-module-root>
   ├── arch
   ├── boards
   ├── dts
   ├── modules
   └── soc

Twister(测试运行器)
=====================

要执行模块中可用的测试和示例,应将 Zephyr 测试运行器(twister)指向包含这些示例和测试的目录。这可以通过在 :file:`zephyr/module.yml` 文件中指定示例和测试的路径来完成。此外,如果模块定义了树外开发板,模块文件可以将 twister 指向模块中维护这些文件的路径。例如:


.. code-block:: yaml

    build:
      cmake: .
    samples:
      - samples
    tests:
      - tests
    boards:
      - boards

.. _modules-bin-blobs:

二进制块
============

Zephyr 支持获取和使用 :ref:`二进制块 <bin-blobs>`,其元数据完全包含在 :file:`zephyr/module.yml` 中。这是因为二进制块必须始终与 Zephyr 模块关联,因此 blob 元数据属于模块描述本身。

使用 :ref:`west blobs <west-blobs>` 获取二进制块。如果 :ref:`不使用 <modules_without_west>` ``west``,则必须手动下载和验证它们。

:file:`zephyr/module.yml` 中的 ``blobs`` 部分由一系列映射组成,每个映射具有以下条目:

- ``path``: 二进制块的路径,相对于模块仓库中的 :file:`zephyr/blobs/` 文件夹
- ``sha256``: 二进制块文件的 `SHA-256 <https://en.wikipedia.org/wiki/SHA-2>`_ 校验和
- ``type``: :ref:`二进制块的类型 <bin-blobs-types>`。目前限制为 ``img`` 或 ``lib``
- ``version``: 版本字符串
- ``license-path``: 此 blob 的许可证文件路径,相对于模块仓库的根
- ``url``: 标识将从中获取 blob 的位置以及要使用的获取方案的 URL
- ``description``: 二进制块的可读描述
- ``doc-url``: 指向此 blob 官方文档位置的 URL

包管理器依赖项
============================

Zephyr 模块可以描述包管理器提供的依赖项,目前仅支持 ``pip``。

west 扩展命令 ``west packages <manager>`` 可用于列出 Zephyr 和当前模块的依赖项,这些模块在其 ``module.yml`` 文件中利用此功能。运行 ``west help packages`` 了解更多详细信息。

Python pip
----------

调用 ``west packages pip`` 会列出 Zephyr 和模块的 `需求文件`_。传递 ``--install`` 会在有活动虚拟环境时安装这些文件。

以下示例演示了一个 ``zephyr/module.yml`` 文件,其中模块的 ``scripts`` 目录中有一些需求文件。


.. code-block:: yaml

    package-managers:
      pip:
        requirement-files:
          - scripts/requirements-build.txt
          - scripts/requirements-doc.txt


.. _modules-runners:

外部运行器
================

如果模块具有需要自定义 :ref:`运行器 <west-runner>` 的树外开发板,则可以将列表添加到其 ``zephyr/module.yml`` 文件中,例如:


.. code-block:: yaml

    runners:
      - file: scripts/my-runner.py


在执行 ``west flash`` 或 ``west debug`` 时导入每个文件条目,并注册 ``ZephyrBinaryRunner`` 的子类以供使用。

模块包含
================

.. _modules_using_west:

使用 West
----------

如果已安装 west 且尚未设置 :makevar:`ZEPHYR_MODULES`,构建系统会在您的 :term:`west 安装 <west installation>` 中查找所有模块并使用它们。它通过运行 :ref:`west list <west-built-in-misc>` 来获取安装中所有项目的路径,然后将结果过滤为仅具有必要模块元数据文件的项目。

``west list`` 输出中的每个项目都按以下方式测试:

- 如果项目包含名为 :file:`zephyr/module.yml` 的文件,则该文件的内容将用于确定应将哪些文件添加到构建中,如上一节所述。

- 否则(即,如果项目没有 :file:`zephyr/module.yml`),构建系统会在项目中查找 :file:`zephyr/CMakeLists.txt` 和 :file:`zephyr/Kconfig` 文件。如果两者都存在,则该项目被视为模块,并且这些文件将被添加到构建中。

- 如果这些检查都不成功,则该项目不被视为模块,不会添加到 :makevar:`ZEPHYR_MODULES`。

.. _modules_without_west:

不使用 West
------------

如果您没有安装 west 或不希望构建系统使用它来查找 Zephyr 模块,您可以使用以下选项之一自己设置 :makevar:`ZEPHYR_MODULES`。列表中的每个目录都必须包含 :file:`zephyr/module.yml` 文件或文件 :file:`zephyr/CMakeLists.txt` 和 :file:`Kconfig`,如上一节所述。

#. 在 CMake 命令行中,如下所示:

   .. code-block:: console

      cmake -DZEPHYR_MODULES=<path-to-module1>[;<path-to-module2>[...]] ...

#. 在应用程序顶层 :file:`CMakeLists.txt` 的顶部,如下所示:

   .. code-block:: cmake

      set(ZEPHYR_MODULES <path-to-module1> <path-to-module2> [...])
      find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})

   如果您选择此选项,请确保在调用 ``find_package(Zephyr ...)`` **之前** 设置变量,如上所示。

#. 在预加载以填充 CMake 缓存的单独 CMake 脚本中,如下所示:

   .. code-block:: cmake

      # 将此放在名为 "zephyr-modules.cmake" 的文件中
      set(ZEPHYR_MODULES <path-to-module1> <path-to-module2>
        CACHE STRING "pre-cached modules")

   您可以通过在 CMake 命令行中添加 ``-C zephyr-modules.cmake`` 来告诉构建系统使用此文件。

不使用模块
-----------------

如果您没有安装 west 并且没有自己指定 :makevar:`ZEPHYR_MODULES`,则不会向构建中添加其他模块。您仍然可以构建不需要外部仓库中定义的代码或 Kconfig 选项的任何应用程序。

向模块提交更改
******************************

在提交新模块或对现有模块进行更改时,主仓库 Zephyr 需要对更改的引用才能验证更改。在主树中,这是使用修订版本完成的。对于已经合并并成为树的一部分的代码,我们使用提交哈希、标签或分支名称。但是,对于拉取请求,我们需要在修订版本字段中指定拉取请求编号,以允许使用提交到模块的更改构建 zephyr 主树。

为了避免将带有拉取请求信息的更改合并到 master,拉取请求应标记为 ``DNM``(不合并)或最好是草稿拉取请求,以确保它不会被错误合并,并允许模块首先合并并分配永久提交哈希。草稿通过在标记为"准备审查"之前不自动通知任何人来减少噪音。一旦模块合并,修订版本将需要由提交者或维护者更改为反映更改的模块的提交哈希。

请注意,可以使用完全相同的过程提交对不同模块的多个和依赖更改。在这种情况下,您将更改所有针对它们提交拉取请求的模块的多个条目。

.. _submitting_new_modules:

提交新模块的流程
===================================

请遵循 :ref:`external-src-process` 中的流程并获得 TSC 批准,以将外部源代码作为模块集成

如果请求获得批准,项目团队将创建一个新仓库,并使用基本信息对其进行初始化,这将允许按照项目贡献指南向模块项目提交代码。

如果模块作为 Github 上另一个项目的分支维护,则与 Zephyr 模块相关的文件和与上游相关的更改需要在名为 ``zephyr`` 的特殊分支中维护。

来自 Zephyr 项目的维护者将创建仓库并对其进行初始化。您将作为新仓库的协作者添加。按照 :ref:`此处 <modules_using_west>` 描述的指南将模块内容(代码)提交到新仓库,然后使用以下信息向 :zephyr_file:`west.yml` 添加新条目:

   .. code-block:: console

        - name: <仓库名称>
          path: <应克隆仓库的路径>
          revision: <指向模块拉取请求的引用指针>


例如,要将 *my_module* 添加到清单:

.. code-block:: console

    - name: my_module
      path: modules/lib/my_module
      revision: pull/23/head


其中上面示例中的 23 表示提交到 *my_module* 仓库的拉取请求编号。一旦模块更改被审查和合并,修订版本需要更改为模块仓库中的提交哈希。

.. _changes_to_existing_module:

提交对现有模块的更改的流程
==================================================

#. 按照 :ref:`贡献指南 <contribute_guidelines>` 和 :ref:`期望 <contributor-expectations>` 使用拉取请求向现有仓库提交更改。
#. 提交拉取请求,将引用模块的条目更改为 Zephyr 主树的 :zephyr_file:`west.yml`,其中包含以下信息:

   .. code-block:: console

        - name: <仓库名称>
          path: <应克隆仓库的路径>
          revision: <指向模块拉取请求的引用指针>


例如,要将 *my_module* 添加到清单:

.. code-block:: console

    - name: my_module
      path: modules/lib/my_module
      revision: pull/23/head

其中上面示例中的 23 表示提交到 *my_module* 仓库的拉取请求编号。一旦模块更改被审查和合并,修订版本需要更改为模块仓库中的提交哈希。



.. _CMake list: https://cmake.org/cmake/help/latest/manual/cmake-language.7.html#lists
.. _add_subdirectory(): https://cmake.org/cmake/help/latest/command/add_subdirectory.html
.. _GitHub issues: https://github.com/zephyrproject-rtos/zephyr/issues
.. _requirement files: https://pip.pypa.io/en/stable/reference/requirements-file-format/
