.. _external-contributions:

贡献外部组件（Contributing External Components）
#############################################

在某些情况下，为避免重复实现其他开源项目中已经具备的基础功能或特性，利用现有的外部源代码是明智之选。

本节描述在何种情况下可以将外部源代码引入 Zephyr，以及相关的纳入流程。

在决定是否接受时，将考虑三个主要因素，见下文各节。

请注意，本页的大部分内容讨论的是最终会被编译并链接进镜像、且将被烧录到目标硬件中的外部组件。仅在编译、代码分析、测试或仿真阶段使用的外部工具（tooling），请参见页面末尾的 :ref:`external-tooling` 小节。

软件许可证（Software License）
*****************************

.. note::

   采用 Apache-2.0 许可证的外部源代码不受本小节约束。

将使用非 Apache 2.0 许可证的其他项目代码集成到 Zephyr 项目中，需要结合上下文进行充分理解，并按照 `Zephyr 项目章程（Zephyr project charter）`_ 的描述，由 `Zephyr 管理委员会（Zephyr governing board）`_ 批准。管理委员会会自动拒绝任何未获 `开源促进会（Open Source Initiative，OSI）`_ 批准的许可证。详见 :ref:`external-src-process` 小节。

.. _Zephyr governing board:
   https://www.zephyrproject.org/governance/

.. _Zephyr project charter:
   https://www.zephyrproject.org/wp-content/uploads/2023/08/LF-Zephyr-Charter-2023.08.21.pdf

.. _Open Source Initiative (OSI):
   https://opensource.org/licenses/alphabetical

通过对潜在贡献进行严格审查，并对贡献代码强制执行 :ref:`DCO`（开发者原始签名），我们确保 Zephyr 社区可以在不担忧专利或版权问题的前提下，基于 Zephyr 项目开发产品。

价值评估（Merit）
****************

与其他常规贡献相同，包含外部代码的贡献也需要进行价值评估。对于来自既有项目的代码，接受前还需回答一些额外问题。更具体地说，技术指导委员会（Technical Steering Committee，TSC）将在外部源代码被接受前，重点考虑并认真评估如下事项：

- 这是否是为项目引入该功能的最佳方式？需要评估内部实现成本以及维护外部代码库所产生的成本。
- 外部项目是否在积极维护？这对涉及安全或密码学的代码尤为重要。
- 是否考虑过所提实现方案的替代方案？是否存在其他实现相同功能的开源项目？

集成方式（Mode of integration）
*****************************

将外部源代码集成到 Zephyr 项目有两种方式，每种情形需要谨慎选择适当方式。

集成至主树（Integration in the main tree）
=========================================

第一种方式是将源代码文件直接导入主 ``zephyr`` 仓库。这意味着导入的源代码将成为“主线”（mainline）代码库的一部分，并因此需要：

- 代码按 Zephyr 的 :ref:`coding_style` 进行格式化；
- 代码遵循项目的 :ref:`coding_guidelines`；
- 代码与主树中其他代码一样，接受相同的检查与验证要求（包括静态分析）；
- 所有文件（若尚未包含）需带有 SPDX 标签；
- 如果源代码不使用 Apache 2.0 许可证，则需在 :ref:`许可页面 <zephyr_licensing>` 添加条目。

此方式既适用于小型也适用于大型外部代码库，但更常见于前者。

作为模块集成（Integration as a module）
=====================================

第二种方式是将第三方开源项目的全部或部分导入到单独的仓库中，并以 :ref:`模块 <modules>` 的形式纳入。采用这种方式时，代码被视为在外部开发，因此不自动受上一小节所述要求的约束。

集成到主清单（west.yml）（Integration in main manifest file (west.yaml)）
-----------------------------------------------------------------------

将外部代码集成进主 :file:`west.yml` 清单文件，限于以下情形：被 Zephyr 子系统（库）使用、被某个平台或驱动（HAL）使用，或为测试/构建 Zephyr 组件所需的工具。

此组模块的集成由 Zephyr 项目的 CI 进行验证，并确保在每次 Zephyr 发布中可用。

被集成的模块不会在未给出详细迁移方案的情况下从树中移除。

作为可选模块集成（Integration as optional modules）
--------------------------------------------------

对无入向依赖的模块/项目（standalone 或松散集成）应作为“可选”处理并保持独立。那些能直接服务用户、并通过 Zephyr 子系统或平台提供价值的可选项目，应添加到默认过滤的可选清单文件（:file:`submanifests/optional.yml`）中。

此类可选项目可能在其自身仓库中包含示例与测试。

不应在 Zephyr 代码树（Git 仓库）中直接添加对此类模块的依赖；所有示例或测试代码应作为模块的一部分进行维护。

.. note::

   以上对所有新的可选模块有效。对于目前在 Zephyr Git 仓库中仍包含示例与测试代码的既有可选模块，将会随时间逐步迁移出去。

作为外部模块集成（Integration as external modules）
--------------------------------------------------

这与可选模块类似，但其以文档中的一个条目加入 Zephyr 项目（使用预定义模板）。此类模块不在 Zephyr 项目清单内，文档中会指导用户和开发者如何集成其功能。

持续维护（Ongoing maintenance）
******************************

无论采用何种集成方式，集成到 Zephyr 的外部源代码都需要定期、持续的维护。因此，提交集成外部源代码提案的人必须承诺在可预见的未来维护该集成。必要时，需在流程中向 :file:`MAINTAINERS.yml` 添加条目。

.. _external-src-process:

提交流程与评审（Submission and review process）
*********************************************

在外部源代码可以被纳入项目前，必须经过技术指导委员会（TSC）审查并接受；在某些情况下，还需要 Zephyr 管理委员会批准。

对外部源代码的集成请求，应在 GitHub 的 Zephyr 项目问题跟踪系统中新建一个 issue，详细说明源代码及其与项目的集成方式。

请按以下步骤发起提交流程：

#. 仔细阅读 :ref:`external-contributions` 小节，了解 TSC 与管理委员会用于批准或拒绝请求的准则；
#. 使用 :github:`New External Source Code Issue <new?assignees=&labels=RFC&template=007_ext-source.yml>` 新建一个 issue；
#. 填写所有必填部分，确保提供足够细节，以便 TSC 评估请求的价值。可选地，你也可以创建一个展示外部源代码集成方式的 Pull Request，并在 issue 中附上链接；
#. 等待 TSC 反馈，并对作为 GitHub issue 评论提出的其他问题进行回复。

如果 TSC 评估后认为集成外部源代码是最佳方案，且该外部源代码使用 Apache-2.0 许可证，则提交流程结束，可以进行集成。

然而，如果外部源代码使用的并非 Apache-2.0 许可证，则需遵循以下附加步骤：

#. TSC 主席会将早期提交流程中创建的 GitHub issue 链接转交 Zephyr 管理委员会进行进一步审查；

#. Zephyr 管理委员会有两周时间进行审阅并提出问题：

   - 若无人提出异议，则流程结束。若全体委员在两周内一致通过，也可加速批准；

   - 若某位委员提出无法通过邮件解决的异议，则管理委员会将召开会议，讨论是否推翻 TSC 的批准，或寻找另一些可解决异议的办法。

#. 当 Zephyr TSC 与管理委员会均批准后，提交流程完成。

下图展示了流程概览：

.. figure:: media/ext-src-flowchart.svg
   :align: center

   提交流程

.. _external-tooling:

贡献外部工具（Contributing External Tooling）
*******************************************

本小节专门讨论在 Zephyr 项目中纳入外部工具（tooling）的情形。外部工具在此定义为：辅助编译、测试或仿真过程的软件，但绝不会成为最终镜像中被编译并链接的代码。“纳入”（Inclusion）在此语境下，指成为 Zephyr 默认发行版的一部分：要么直接位于主树的 :file:`scripts/` 目录下，要么作为主 :file:`west.yml` 清单中的一个 west 项目。因此，本小节不适用于第三方工具链、模拟器等——它们可以被 Zephyr 的构建系统或文档引用，但不属于“被纳入 Zephyr”。

工具组件必须采用 `OSI（Open Source Initiative）`_ 批准的许可证发布。

与常规外部组件相同，来自其他项目的工具既可集成到主树，也可作为 :ref:`west 项目 <west-workspace>` 集成。注意此时相应的 west 项目并非 :ref:`模块 <modules>`，因为工具不使用 Zephyr 构建系统，也无需由其处理。差异详情参见 :ref:`modules-vs-projects`。

若工具被集成到主树，应放置在 :file:`scripts/` 目录下；若作为 west 项目集成，那么项目仓库可以托管在 zephyrproject-rtos 组织之外，但需在主 :file:`west.yml` 清单中通过 ``group-filter:`` 字段将其设为可选。关于可选项目的更多信息见 :ref:`此小节 <west-manifest-groups>`。

任何引入新外部工具组件的 Pull Request 都必须由 TSC 批准。TSC 代表将逐案进行个别分析并作出决定。

关于主清单的额外考虑（Additional considerations about the main manifest）
**********************************************************************

一般而言，对 `主清单文件（main manifest file）`_ 的 ``projects:`` 区域进行任何增删改都需要 TSC 批准。这包括但不限于：

- 添加/删除分组与分组过滤（groups 与 group filters）；
- 添加/删除项目（projects）；
- 添加/删除 ``import`` 语句。

.. _main manifest file:
   https://github.com/zephyrproject-rtos/zephyr/blob/main/west.yml
