.. _rfcs:

提案与 RFC (Proposals and RFCs)
###############################

许多变更（包括缺陷修复与文档改进）可以通过常规的 GitHub Pull Request 工作流实现并评审。

但也有不少变更“影响较大 (substantial)”，需要经历设计流程，并在项目相关方之间达成共识。

“RFC（request for comments，请求评审）”流程旨在为新特性进入项目提供一致且可控的路径。

当你计划对 Zephyr 或其文档进行“影响较大”的变更时，贡献者与项目相关方应考虑采用此流程。以下是适合使用 RFC 的一些示例：

- 引入会扩展 API 表面的新特性，且如果直接发布需要通过特性开关 (feature flag) 控制；
- 修改现有的稳定 API；
- 移除已作为 Zephyr 一部分发布过的功能；
- 引入新的惯用用法或约定，即便它们本身不直接修改 Zephyr 代码。

RFC 过程是一个绝佳机会：让更多人能在提案成为 Zephyr 一部分之前提前审阅。很多看似“显而易见”的提案，在更广泛的关注与讨论之后往往能得到明显改进。

RFC 也有助于在设计阶段就鼓励围绕拟议特性展开讨论，并在设计仍易于调整时，就将重要约束纳入设计，而不是等到实现完成之后。

对于“重大特性 (Major Feature)”，请先创建一个 issue，概述你的提案以便讨论。这样也便于我们更好地协调工作、避免重复劳动，并帮助你以更容易被项目接受的方式来打磨改动。提供以下信息有助于更快获得处理：

  * 提案概览 (Overview of the Proposal)
  * 动机或使用场景 (Motivation for or Use Case)
  * 设计细节 (Design Details)
  * 备选方案 (Alternatives)
  * 测试策略 (Test Strategy)

某些变更或贡献不需要 RFC，但其合理性与细节仍应写入 Pull Request：

- 对既有、成熟子系统的小幅增强与修改；
- 表述调整、重组或重构；
- 警告的新增或移除；
- 在既有子系统中新增开发板、SoC 或驱动；
- …

该流程本身是：创建一个带有 :ref:`RFC 标签 <gh_labels>` 的 GitHub issue，充分记录你的提案。建议使用 `RFC form`_，以便遵循大家熟悉的模板。

与 Pull Request 一样，当存在分歧或尚未有足够意见以推动前进时，RFC 也可能需要在 `Zephyr 会议`_ 的语境中进行讨论以推动其进展。请确保为其添加恰当的标签，或将其加入相应的 GitHub project，以便在下一次会议中审阅。

.. _`RFC form`: https://github.com/zephyrproject-rtos/zephyr/issues/new?template=003_rfc-proposal.yml
.. _`Zephyr meetings`: https://github.com/zephyrproject-rtos/zephyr/wiki/Zephyr-Committee-and-Working-Groups
.. _rfcs:

Proposals and RFCs
##################

Many changes, including bug fixes and documentation improvements can be
implemented and reviewed via the normal GitHub pull request workflow.

Many changes however are "substantial" and need to go through a
design process and produce a consensus among the project stakeholders.

The "RFC" (request for comments) process is intended to provide a consistent and
controlled path for new features to enter the project.

Contributors and project stakeholders should consider using this process if
they intend to make "substantial" changes to Zephyr or its documentation. Some
examples that would benefit from an RFC are:

- A new feature that creates new API surface area, and would require a feature
  flag if introduced.
- The modification of an existing stable API.
- The removal of features that already shipped as part of Zephyr.
- The introduction of new idiomatic usage or conventions, even if they do not
  include code changes to Zephyr itself.

The RFC process is a great opportunity to get more eyeballs on proposals coming
from contributors before it becomes a part of Zephyr. Quite often, even
proposals that seem "obvious" can be significantly improved once a wider group
of interested people have a chance to weigh in.

The RFC process can also be helpful to encourage discussions about a proposed
feature as it is being designed, and incorporate important constraints into the
design while it's easier to change, before the design has been fully
implemented.

For a Major Feature, first open an issue and outline your proposal so that it
can be discussed. This will also allow us to better coordinate our efforts,
prevent duplication of work, and help you to craft the change so that it is
successfully accepted into the project. Providing the following information
will increase the chances of your issue being dealt with quickly:

  * Overview of the Proposal
  * Motivation for or Use Case
  * Design Details
  * Alternatives
  * Test Strategy

Some changes or contributions do not require an RFC, the rationale and details
of the changes should however be part of the pull-request:

- Small enhancements and modifications to existing and established subsystems.
- Rephrasing, reorganizing or refactoring
- Addition or removal of warnings
- Addition of new boards, SoCs or drivers to existing subsystems
- ...

The process in itself consists in creating a GitHub issue with the :ref:`RFC
label <gh_labels>` that documents the proposal thoroughly. You are encouraged
to use the `RFC form`_ to make sure the proposal follows a template which
project participants are already familiar with.

As with Pull Requests, RFCs might require discussion in the context of one of
the `Zephyr meetings`_ in order to move it forward in cases where there is
either disagreement or not enough voiced opinions in order to proceed. Make sure
to either label it appropriately or include it in the corresponding GitHub
project in order for it to be examined during the next meeting.

.. _`RFC form`: https://github.com/zephyrproject-rtos/zephyr/issues/new?template=003_rfc-proposal.yml
.. _`Zephyr meetings`: https://github.com/zephyrproject-rtos/zephyr/wiki/Zephyr-Committee-and-Working-Groups
