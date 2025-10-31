.. _development_model:

项目与治理
##########

Zephyr 项目通过 GitHub 管理协作：使用 **Issues** 跟踪功能、增强与缺陷，使用 **Pull Requests (PR)** 提交与审查变更。社区成员协作审查 Issue 和 PR，并通过定期发布来管理功能演进与质量改进（见 `Program Management 概览 <https://wiki.zephyrproject.org/Program-Management>`_）。为控制 Issue/PR 规模，我们要求贡献者及时参与审查、反馈与回复。建议先了解项目的 :ref:`开发流程与工具 <dev-environment-and-tools>` 以及 :ref:`审查时间表 <review_time>`，以把握贡献期望与协作节奏。

.. toctree::
   :maxdepth: 1

   tsc
   project_roles.rst
   working_groups
   release_process
   proposals
   code_flow
   dev_env_and_tools
   issues
   communication
   documentation

术语
****

- 主线（mainline）：核心功能与核心特性正在开发的主树。
- 子系统/功能分支（subsystem/feature branch）：同一仓库内的分支；当引用不在同一仓库中的分支时，也沿用“分支”一词（共享相同历史的仓库副本）。
- 上游（upstream）：源代码所基于的父分支，你从其中拉取并向其推送。
- LTS：长期支持（Long Term Support）。
