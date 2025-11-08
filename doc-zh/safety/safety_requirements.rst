.. _safety_requirements:

安全需求 (Safety Requirements)
###############################

简介 (Introduction)
********************

安全委员会领导收集需求的工作,这些需求反映了实施的**实际**状态,遵循项目安全工作的 `路线 3s <https://docs.zephyrproject.org/latest/safety/safety_overview.html#general-safety-scope>`_
方法。目标**不是**创建新需求来请求项目的额外功能。

需求收集在单独的仓库中:
`需求仓库
<https://github.com/zephyrproject-rtos/reqmgmt>`__

指南 (Guidelines)
******************

以下是需求仓库的指南以及安全委员会在向仓库添加需求时的期望。

范围 (Scope)
=============

需求的范围涵盖内核功能。

一致性 (Consistency)
=====================

在所有需求中保持一致性。语言和用词的选择应该是一致的。
(参见: `语法 (Syntax)`_)

仓库中需求的级别 (Levels of requirements in the repository)
===========================================================

系统需求 (System Requirements)
  系统需求描述 Zephyr RTOS(=此处的系统)的行为。
  它们从非常高的层面描述 Zephyr RTOS 的功能,
  而不深入功能本身的细节。
  系统需求的目的是获得 Zephyr RTOS 当前实现功能的概述。
  换句话说,编写这些需求的人通常对 Zephyr RTOS
  项目有一定的了解,因为这些需求是针对 RTOS 的。

软件需求 (Software Requirements)
  软件需求在更细粒度的层面上细化系统级需求,以便
  可以测试每个需求。
  这些需求定义了功能应该能够执行的具体操作和功能的
  行为。

需求 UID(唯一标识符)处理 (Requirement UID Handling)
====================================================

用于管理需求的工具 `strictDoc <https://strictdoc.readthedocs.io/en/stable/>`_ 负责处理与每个需求关联的唯一标识符(UID)。要管理 UID,请遵循以下步骤:

#. 不要为新需求添加需求 UID 和 UID 字段
#. 完成新需求的工作后执行: ``strictDoc manage auto-uid .``
#. 如果需要,在具有新分配的 UID 的需求之间建立链接

完成此操作后,需求就准备好了,可以创建拉取请求。
PR 中的 CI 将检查需求 UID 是否有效或是否存在重复。
如果 PR 中存在重复项,则需要通过变基并重新执行
上述步骤来解决这些问题。

需求类型 (Requirement Types)
==============================

* 功能性 (Functional)
* 非功能性 (Non-Functional)

需求标题约定 (Requirement title convention)
===========================================

使用简短简洁的需求标题。

需求仓库的拉取请求 (Pull Request requirement repository)
========================================================

* 遵守 Zephyr 项目的 :ref:`contribute_guidelines`。

  * 只要它们适用于需求仓库。

* 避免创建包含琐碎和非琐碎更改的大型提交。

* 避免在同一个提交中移动和更改需求。

良好需求的特征 (Characteristics of a good requirement)
=======================================================

* 明确无歧义 (Unambiguous)
* 可验证 (Verifiable) (例如功能需求的可测试性)
* 清晰 (Clear) (简洁、succinct、简单、精确)
* 正确 (Correct)
* 可理解 (Understandable)
* 可行 (Feasible) (现实、可能)
* 独立 (Independent)
* 原子性 (Atomic)
* 必要 (Necessary)
* 无实现依赖 (Implementation-free) (抽象)

一组需求的特征 (Characteristics of a set of requirements)
==========================================================

* 完整 (Complete)
* 一致 (Consistent)
* 非冗余 (Non redundant)

语法 (Syntax)
==============

* 建议使用公认的需求语法。

  * `EARS <https://alistairmavin.com/ears/>`_ 是一个很好的参考。特别是如果您
    不熟悉需求编写。

  * 其他格式也被接受,只要满足上述需求的特征。
