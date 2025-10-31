.. _development_model:.. _development_model:.. _development_model:



项目和治理 (Project and Governance)

##################################

项目和治理Project and Governance



.. toctree::##############################################

   :maxdepth: 1



   tsc

   project_roles.rst

   working_groups

   release_process.. toctree::.. toctree::

   proposals

   code_flow   :maxdepth: 1   :maxdepth: 1

   dev_env_and_tools

   issues

   communication

   documentation   tsc   tsc



   project_roles.rst   project_roles.rst



Zephyr 项目使用 GitHub **Issues** 来追踪功能、增强和错误报告的开发流程工作流,   working_groups   working_groups

以及使用 GitHub **Pull Requests** (PR) 来提交和审查更改。Zephyr 社区成员共同合作

审查这些 Issue 和 PR,通过其定期发布来管理 Zephyr 的功能增强和质量改进,   release_process   release_process

如 `程序管理概述 (program management overview) <https://wiki.zephyrproject.org/Program-Management>`_ 中所述。

   proposals   proposals

我们只能通过要求社区和贡献者及时进行审查、反馈和回复来管理 Issue 和 PR 的数量,

无论是针对初始提交还是后续问题和澄清。了解项目的 :ref:`开发流程和工具 (development processes and tools) <dev-environment-and-tools>`   code_flow   code_flow

和关于 :ref:`审查时间表 (review timelines) <review_time>` 的具体情况,

以了解项目对我们活跃开发人员社区的目标和指南。   dev_env_and_tools   dev_env_and_tools



:ref:`project_roles` 详细描述了 Zephyr 项目角色以及与开发流程工作流相关的权限。   issues   issues



   communication   communication

术语 (Terminology)

*****************   documentation   documentation



- 主线 (mainline): 核心功能和核心功能正在开发的主树。

- 子系统/功能分支 (subsystem/feature branch): 是同一存储库中的分支。

  在我们的情况下,当引用不在同一存储库中的分支时,我们也将使用术语分支,

  这些是共享相同历史的存储库副本。

- 上游 (upstream): 源代码所基于的父分支。这是你从中拉取和推送到的分支,基本上是你的上游。

- LTS: 长期支持 (Long Term Support)

Zephyr项目使用GitHub **Issues**来跟踪功能、增强和错误报告，The Zephyr project defines a development process workflow using GitHub

使用GitHub **Pull Requests**（PR）来提交和审查更改，定义了一个开发流程工作流。**Issues** to track feature, enhancement, and bug reports together with GitHub

Zephyr社区成员共同审查这些Issues和PR，通过定期发布来管理Zephyr的功能增强**Pull Requests** (PRs) for submitting and reviewing changes.  Zephyr

和质量改进，如 `项目管理概述 <https://wiki.zephyrproject.org/Program-Management>`_community members work together to review these Issues and PRs, managing

中所述。feature enhancements and quality improvements of Zephyr through its regular

releases, as outlined in the

我们只能通过要求社区和贡献者及时审查、反馈和响应来管理Issues和PR的数量，`program management overview <https://wiki.zephyrproject.org/Program-Management>`_.

无论是初次提交还是后续问题和澄清。阅读项目的 :ref:`开发流程和工具 <dev-environment-and-tools>`

以及 :ref:`审查时间表 <review_time>` 的具体信息，了解我们活跃的开发者社区的We can only manage the volume of Issues and PRs, by requiring timely reviews,

项目目标和指南。feedback, and responses from the community and contributors, both for initial

submissions and for followup questions and clarifications.  Read about the

:ref:`project_roles` 详细描述了Zephyr项目角色以及与开发流程工作流相关的权限。project's :ref:`development processes and tools <dev-environment-and-tools>`

and specifics about :ref:`review timelines <review_time>` to learn about the

project's goals and guidelines for our active developer community.

术语

***********:ref:`project_roles` describes in detail the Zephyr project roles and associated permissions

with respect to the development process workflow.

- mainline（主线）：开发核心功能和核心特性的主树。

- subsystem/feature branch（子系统/功能分支）：同一存储库中的分支。在我们的情况下，

  我们也会在引用不在同一存储库中的分支时使用术语分支，这些分支是共享相同历史记录的Terminology

  存储库副本。***********

- upstream（上游）：源代码所基于的父分支。这是您从中拉取和推送的分支，

  基本上是您的上游。- mainline: The main tree where the core functionality and core features are

- LTS：长期支持  being developed.

- subsystem/feature branch: is a branch within the same repository. In our case,
  we will use the term branch also when referencing branches not in the same
  repository, which are a copy of a repository sharing the same history.
- upstream: A parent branch the source code is based on. This is the branch you
  pull from and push to, basically your upstream.
- LTS: Long Term Support
