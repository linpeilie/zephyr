.. _release_process:.. _release_process:



发布流程 (Release Process)Release Process

#########################################



Zephyr 项目基于时间周期而不是功能驱动进行发布。Zephyr 发布代表许多贡献者、公司和来自社区的个人的工作聚合。The Zephyr project releases on a time-based cycle, rather than a feature-driven

one. Zephyr releases represent an aggregation of the work of many contributors,

基于时间的发布流程使 Zephyr 项目能够为用户提供最新技术和功能与优异的整体质量之间的平衡。companies, and individuals from the community.

大约 6 个月的发布周期允许项目协调已实际实现的功能的开发,使项目能够维护整体发布的质量,

而不会因为一两个尚未准备好的功能而延迟。A time-based release process enables the Zephyr project to provide users with a

balance of the latest technologies and features and excellent overall quality. A

每个发布期将包括开发阶段(Development Phase)和稳定阶段(Stabilization Phase)。roughly 6-month release cycle allows the project to coordinate development of

发布候选版本将在稳定阶段创建。the features that have actually been implemented, allowing the project to

maintain the quality of the overall release without delays because of one or two

features that are not ready yet.

.. figure:: release_cycle.svg

    :align: centerEach release period will consist of a development phase followed by a

    :alt: Release Cyclestabilization phase. Release candidates will be created during the stabilization

    :figclass: align-centerphase.

    :width: 80%



    发布周期 (Release Cycle).. figure:: release_cycle.svg

    :align: center

.. note::    :alt: Release Cycle

    :figclass: align-center

    当前主要版本的里程碑可以在 `官方 GitHub Wiki     :width: 80%

    <https://github.com/zephyrproject-rtos/zephyr/wiki/Release-Management>`_ 上找到。

    有关以前发布的信息可以在 :ref:`此处 <zephyr_release_notes>` 找到。    Release Cycle



.. note::

开发阶段 (Development Phase)

****************************    The milestones for the current major version can be found on the

    `Official GitHub Wiki <https://github.com/zephyrproject-rtos/zephyr/wiki/Release-Management>`_.

关于每个发布的补丁合并,遵循一个相对直接的规程。在每个开发周期的开始,主分支被称为对开发开放。    Information on previous releases can be found :ref:`here <zephyr_release_notes>`.

此时,被认为足够稳定的代码(并且被维护者和广泛社区接受)被合并到主线树中。

新开发周期的大部分更改(以及所有主要更改)将在此时间合并。

Development Phase

开发阶段持续大约五个月。此时间结束时,发布所有者将宣布开发阶段已结束,并发布第一个发布候选版本。*****************

例如,对于注定要成为 3.1.0 的代码库发布,在开发阶段结束时发生的发布将被称为 3.1.0-rc1。

-rc1 发布是一个信号,表示合并新功能的时间已过,稳定下一个代码库发布的时间已开始。A relatively straightforward discipline is followed with regard to the merging

of patches for each release.  At the beginning of each development cycle, the

稳定阶段 (Stabilization Phase)main branch is said to be open for development.  At that time, code which is deemed to be

*****************************sufficiently stable (and which is accepted by the maintainers and the wide community) is

merged into the mainline tree.  The bulk of changes for a new development cycle

在随后的几周内,根据发布里程碑,仅允许稳定、化妆品更新、错误修复、文档改进和现有功能的新测试。(and all of the major changes) will be merged during this time.

(请参见下面的 :ref:`表 <release_milestones>`)。

The development phase lasts for approximately five months.  At the end of this time,

偶尔,会允许更重大的更改和新功能,但这样的情况很少见,需要 TSC 批准和理由。the release owner will declare that the development phase is over and releases the first

作为一般规则,如果你在给定功能的开发阶段错过了提交代码,最好的做法是等待下一个开发周期。of the release candidates.  For the codebase release which is destined to be

(对于以前不支持的硬件驱动程序,偶尔会有例外;如果它们不接触任何其他树内代码,3.1.0, for example, the release which happens at the end of the development phase

它们无法引起回归,应该随时安全添加)。will be called 3.1.0-rc1.  The -rc1 release is the signal that the time to merge

new features has passed, and that the time to stabilize the next release of the

随着修复进入主线,补丁速率将随时间减慢。主线发布所有者每周发布一次或两次新的 -rc 版本;code base has begun.

一个正常系列将在代码库被认为足够稳定并且发布标准已达到的地方在 -rc4 和 -rc6 之间获得某个位置,

此时进行最终 3.1.0 发布。Stabilization Phase

*******************

此时,整个流程再次开始。

Over the following weeks and depending on the release milestone, only stabilization,

.. _merge_criteria:cosmetic updates, bug fixes, documentation improvements, and new tests for

existing features are permitted. (See :ref:`table <release_milestones>` below).

合并标准 (Merge Criteria)

***********************On occasion, more significant changes and new features will be allowed, but such

occasions are rare and require a TSC approval and a justification. As a general

.. figure:: img/img_release_activity.pngrule, if you miss submitting your code during the development phase for a given

      :width: 663pxfeature, the best thing to do is to wait for the next development cycle. (An

      :align: centeroccasional exception is made for drivers for previously unsupported hardware; if

      :alt: Release Activitythey do not touch any other in-tree code, they cannot cause regressions and

should be safe to add at any time).

* 必须满足所有 :ref:`pr_requirements`。

* 最少 2 个批准,包括指定受理人的批准。As fixes make their way into the mainline, the patch rate will slow over time.

* 拉取请求应由至少每个受影响区域的维护者或协作者进行审查;除非对给定区域的更改被认为足够简单,The mainline release owner releases new -rc drops once or twice a week; a normal

  在这种情况下,其他受影响的子系统维护者/协作者的批准就足够了。series will get up to somewhere between -rc4 and -rc6 before the code base is

* 组织级别的四眼原则。我们已经需要至少 2 个批准(基本四眼原则),但是这样的审查和批准可能在considered to be sufficiently stable and the release criteria have been achieved

  提交者与批准人来自同一组织的情况下无意中存在偏见。为了允许项目级别的审查和批准,at which point the final 3.1.0 release is made.

  合并标准使用以下指南扩展:

At that point, the whole process starts over again.

  * 对通用和共享代码的更改或添加应来自不同组织的批准

    (至少来自不同于提交人组织的组织的一个批准)。.. _merge_criteria:

    通用和共享代码定义为不属于 :file:`soc`、:file:`boards` 和 :file:`drivers/*/*` 的任何内容。

  * 对硬件支持(驱动程序、SoC、板卡)的更改或添加应至少由来自不同组织的合并者进行。Merge Criteria

    这仅适用于支持供应商特定硬件的 API 的实现,而不是 API 本身。**************

  * 发布工程师可能会对主要来自一个组织的贡献的区域和其他组织的审查不可能的情况进行异常处理,

    但是,合并应由来自不同组织的人员完成。在这种情况下,应严格遵循至少 2 天的最短审查期,.. figure:: img/img_release_activity.png

    以允许进行其他审查。      :width: 663px

  * 发布工程师不应合并仅由其自己的组织源自和审查的代码更改。为了能够合并此类更改,      :align: center

    至少一个审查应来自不同的组织。      :alt: Release Activity



* 最短审查期为 2 个工作日,简单更改为 4 小时(请参见 :ref:`review_time`)。* All :ref:`pr_requirements` must be met.

* 热修复(Hotfixes)在 CI 通过后随时都可以合并,并且从上面列出的大多数条件中被排除。* Minimal of 2 approvals, including an approval by the designated assignee.

* 所有必需的检查都通过:* Pull requests should be reviewed by at least a maintainer or collaborator of

  each affected area; Unless the changes to a given area are considered trivial

  * 设备树 (Device Tree)  enough, in which case approvals by other affected subsystems

  * 文档 (Documentation)  maintainers/collaborators would suffice.

  * 代码检查工具 (Code linters) (Gitlint, Pylint, Ruff, Sphinx, 等)* Four eye principle on the organisation level. We already require at least 2

  * 身份/电子邮件 (Identity/Emails)  approvals (basic four eye principle), however, such reviews and approvals

  * Kconfig  might be unintentionally biased in the case where the submitter is from the

  * 许可证检查 (License checks)  same organisation as the approvers. To allow for project wide review and

  * Checkpatch (编码风格 Coding Style)  approvals, the merge criteria is extended with the guidelines below:

  * 集成测试 (Integration Tests) (通过 twister) 在模拟/仿真平台上

  * 模拟的蓝牙测试 (Simulated Bluetooth Tests)  * Changes or additions to common and shared code shall have approvals from

    different organisations (at least one approval from an

    organisation different than the submitters').

.. _release_quality_criteria:    Common and shared code is defined as anything that does not fall under

    :file:`soc`, :file:`boards` and :file:`drivers/*/*`.

发布标准 (Release Criteria)  * Changes or additions to hardware support (driver, SoC, boards) shall at

**************************    least have the merger be from a different organisation. This applies only

    to implementation of an API supporting vendor specific hardware and not the

主要动力是清楚地制定必须满足的标准以进行发布。这将有助于定义发布何时"完成",    APIs.

符合大多数人可以理解的条款,并以帮助新人了解流程和参与创建成功发布的方式:  * Release engineers may make exceptions for areas with contributions primarily

    coming from one organisation and where reviews from other organisations are

- 发布标准记录了我们目标受众对每个 Zephyr 发布的所有要求    not possible, however, merges shall be completed by a person from a different

- 每个发布的目标受众可能不同,并且可能重叠    organisation. In such cases, the minimum review period of at least 2 days

- 任何给定时间的标准不是一成不变的:可能有被忽视的要求,或者是新的,    shall be strictly followed to allow for additional reviews.

  在这些情况下,应扩展标准以确保所有需求都得到满足。  * Release engineers shall not merge code changes originating and reviewed

    only by their own organisation. To be able to merge such changes, at least

以下是每个发布必须满足的高级标准:    one review shall be from a different organisation.



- 没有阻滞性错误 / 阻滞性问题 (No blocker bugs / blocking issues)* A minimum review period of 2 business days, 4 hours for trivial changes (see

- 所有相关测试应在 ``Tier 0`` 平台上通过  :ref:`review_time`).

- 所有相关测试应在 Tier 0 和 1 平台上通过(至少每个架构/架构变体/硬件功能 1 个)* Hotfixes can be merged at any time after CI has passed and are excluded from

- 所有适用的示例/测试应在 Tier 0、1 和 2 上编译  most of the conditions listed above.

- 所有高和关键的静态分析和安全问题已解决* All required checks are passing:

- 发布说明是最新的。

  * Device Tree

阻滞性错误 (Blocker Bugs)  * Documentation

========================  * Code linters (Gitlint, Pylint, Ruff, Sphinx, etc.)

  * Identity/Emails

阻滞性错误流程在发布流程中启动,在功能冻结里程碑之后生效。标记为阻滞性的问题实际上会阻止发布发生。  * Kconfig

所有阻滞性错误应在创建发布前解决。  * License checks

  * Checkpatch (Coding Style)

被授予 ``blocker`` 状态的错误修复可以合并到'main'并包含在发布中,直到最终发布日期。  * Integration Tests (Via twister) on emulation/simulation platforms

  * Simulated Bluetooth Tests

对所有用户有影响的中等严重性及以上的错误通常是候选升级为阻滞性错误



贡献者和发布工程团队成员应遵循这些发布阻滞性错误指南:.. _release_quality_criteria:



- 仅当 Zephyr 软件不应该在存在该错误的情况下发布时,才标记错误为阻滞性。Release Criteria

- 所有协作者都可以添加或删除阻滞性标签。****************

- 基于其严重性和普遍性评估错误为潜在的阻滞性。

- 每当添加或删除阻滞性标签时,都提供详细的理由。The main motivation is to clearly have the criteria in place that must be met

- 确保所有阻滞性问题都标记了里程碑。for a release. This will help define when a release is "done" in terms that most

- 发布管理员对阻滞性状态有最终决定权;有任何问题请与他们联系。people can understand and in ways that help new people to understand the process

and participate in creating successful releases:



.. _release_milestones:- The release criteria documents all the requirements of our target audience for

  each Zephyr release

发布里程碑 (Release Milestones)- The target audiences for each release can be different, and may overlap

*****************************- The criteria at any given time are not set in stone: there may be requirements

  that have been overlooked, or that are new, and in these cases, the criteria

  should be expanded to ensure all needs are covered.

.. list-table:: 发布里程碑 (Release Milestones)

   :widths: 15 25 100 25Below is the high level criteria to be met for each release:

   :header-rows: 1

- No blocker bugs / blocking issues

   * - 时间表 (Timeline)- All relevant tests shall pass on ``Tier 0`` platforms

     - 检查点 (Checkpoint)- All relevant tests shall pass on Tier 0 and 1 platforms (at least 1 per

     - 描述 (Description)  architecture/architecture variant/Hardware features)

     - 所有者 (Owner)- All applicable samples/tests shall build on Tiers 0, 1 and 2

   * - T-5M- All high and critical static analysis and security issues addressed

     - 规划 (Planning)- Release Notes are up-to-date.

     - 确定发布日期,分配发布所有者,就该发布的项目范围目标达成一致。

     - TSCBlocker Bugs

   * - T-7W============

     - 审查目标里程碑 (Review target milestones)

     - 确定航班中功能的目标里程碑。Blocker bug process kicks in during the release process and is in effect after the

     - 发布工程 (Release Engineering)feature freeze milestone. An issue labeled as a blocker practically blocks a

   * - T-5Wrelease from happening. All blocker bugs shall be resolved before a release is

     - 发布公告 (Release Announcement)created.

     - 发布所有者宣布功能冻结和发布时间表。

     - 发布管理员 (Release Manager)A fix for a bug that is granted ``blocker`` status can be merged to 'main' and included in

   * - T-4Wthe release all the way until the final release date.

     - 发布时间表提醒 (Release Timeline reminder)

     - 发布所有者发送功能冻结和发布时间表的提醒。Bugs of moderate severity and higher that have impact on all users are typically

     - 发布管理员 (Release Manager)the candidates to be promoted to blocker bugs

   * - T-3W

     - 功能冻结 (Feature Freeze) (RC1)Contributors and member of the release engineering team shall follow these

     - RC1 之后,不能引入新功能。仅允许稳定、化妆品更新、错误修复、文档改进和现有功能的新测试。guidelines for release blocker bugs:

     - 发布工程 (Release Engineering)

   * - T-2W- Only mark bugs as blockers if the software (Zephyr) must not be released with

     - 第二个发布候选版本 (2nd Release Candidate)  the bug present.

     - RC2 之后没有新功能,仅允许稳定和化妆品更改、错误和文档修复。- All collaborators can add or remove blocking labels.

     - 发布管理员 (Release Manager)- Evaluate bugs as potential blockers based on their severity and prevalence.

   * - T-1W- Provide detailed rationale whenever adding or removing a blocking label.

     - 硬冻结 (Hard Freeze) (RC3)- Ensure all blockers have the milestone tagged.

     - RC3 之后仅允许阻滞性错误修复、文档改进和发布说明的更改。- Release managers have final say on blocking status; contact them with any questions.

       发布说明需要在此检查点完成。发布标准已满足。

     - 发布管理员 (Release Manager)

   * - T-0W.. _release_milestones:

     - 发布 (Release)

     - (空)Release Milestones

     - 发布管理员 (Release Manager)*******************





发布 (Releases).. list-table:: Release Milestones

**************   :widths: 15 25 100 25

   :header-rows: 1

.. _release_process_lts:

   * - Timeline

长期支持 (Long Term Support, LTS)     - Checkpoint

=================================     - Description

     - Owner

长期支持发布的设计是为了在扩展期内得到支持和维护,   * - T-5M

是产品的推荐发布版本以及用于认证的可审计分支。     - Planning

     - Finalize dates for release, Assign release owner and agree on project wide goals for this release.

LTS 发布被定义为:     - TSC

   * - T-7W

- **以产品为中心** (Product focused)     - Review target milestones

- **扩展稳定期** (Extended Stabilisation period): 允许更多测试和错误修复     - Finalize target milestones for features in flight.

- **稳定的 API** (Stable APIs)     - Release Engineering

- **质量驱动的流程** (Quality Driven Process)   * - T-5W

- **长期** (Long Term): 维护扩展时间(至少 5 年)。     - Release Announcement

     - Release owner announces feature freeze and timeline for release.

     - Release Manager

以产品为中心 (Product Focused)   * - T-4W

++++++++++++++++++++++++++++     - Release Timeline reminder

     - Release owner sends a reminder of the feature freeze and timeline for release.

Zephyr LTS 是具有扩展支持和维护的产品制造商的推荐发布版本,     - Release Manager

包括一般稳定性和错误修复、安全修复。   * - T-3W

     - Feature Freeze (RC1)

LTS 包括成熟和新功能。API 和功能成熟度已记录并跟踪。成熟和稳定 API 的范围从一个 LTS 扩展到下一个,     - After RC1, no new features may be introduced. Only stabilization,

使用户能够获得最先进的功能和新硬件,同时保持随时间演变的稳定基础。       cosmetic updates, bug fixes, documentation improvements, and new tests

       for existing features are permitted.

扩展稳定期 (Extended Stabilisation Period)     - Release Engineering

++++++++++++++++++++++++++++++++++++++++++   * - T-2W

     - 2nd Release Candidate

Zephyr LTS 开发周期不同于常规发布,具有扩展的稳定期。定期发布的功能冻结发生在     - No new features after RC2, ONLY stabilization and cosmetic changes, bug and doc fixes are allowed.

预定发布日期之前 3-4 周。LTS 的稳定期延长 3 周,功能冻结发生在预期发布日期前 6-7 周。     - Release Manager

代码冻结和发布日期之间的时间在这种情况下得到延长。   * - T-1W

     - Hard Freeze (RC3)

稳定的 API (Stable APIs)     - Only blocker bug fixes after RC3, documentation improvements and changes

+++++++++++++++++++++++       to release notes are allowed.

       Release notes need to be complete by this checkpoint. Release Criteria is

Zephyr LTS 为开发产品提供稳定且长期存在的基础。为了保证 API 及这些 API       met.

的实现的稳定性,需要构成 OS 核心的任何发布软件都要经过 Zephyr API 生命周期,     - Release Manager

并在至少 2 个发布中稳定下来。这保证了我们发布许多突出和核心功能,   * - T-0W

具有成熟且完善的实现以及在 LTS 发布的生命周期内支持的稳定 API。     - Release

     -

- API 冻结 (API Freeze) (LTS - 2)     - Release Manager



  - 所有稳定的 API 需要在 LTS 前 2 个发布中冻结。API 可以使用其他功能进行扩展,

    但核心实现不被修改。这对以下子系统是有效的,例如:Releases

*********

    - 设备驱动程序 (Device Drivers) (i2c.h, spi.h)...

    - 内核 (Kernel) (k_*):.. _release_process_lts:

    - 操作系统服务 (OS services) (logging,debugging, ..)

    - DTS: API 和绑定稳定性Long Term Support (LTS)

    - Kconfig=======================



  - 实验性功能的新 API 可以随时添加,只要它们是独立的,Long-term support releases are designed to be supported and maintained

    并记录为实验性或不稳定的功能/API。for an extended period and are the recommended release for

products and the auditable branch used for certification.

- 功能冻结 (Feature Freeze) (LTS - 1)

  - 没有新功能或覆盖主要 LTS 功能的代码大修/重组。An LTS release is defined as:



    - 内核 + 基础操作系统 (Kernel + Base OS)- **Product focused**

    - 其他通告的 LTS 功能 (Additional advertised LTS features)- **Extended Stabilisation period**: Allow for more testing and bug fixing

- **Stable APIs**

  - 基础操作系统和/或扩展基础 OS 和通告 LTS 功能之上的辅助功能- **Quality Driven Process**

    可以随时添加,如果适用应标记为实验性- **Long Term**: Maintained for an extended period of time (at least 5 years).



质量驱动的流程 (Quality Driven Process)

+++++++++++++++++++++++++++++++++++++++Product Focused

+++++++++++++++

Zephyr 项目遵循行业标准和流程,目的是提供面向质量的发布。

这通过提供以下产品来实现,以跟踪进度、完整性和项目提供的软件组件的质量:Zephyr LTS is the recommended release for product makers with an extended

support and maintenance which includes general stability and bug fixes,

- 符合已发布的编码指南、风格指南和命名约定,以及对偏差的记录。security fixes.

- 静态分析报告 (Static analysis reports)

An LTS includes both mature and new features. API and feature maturity is

  - 使用可用的商业和开源工具定期对完整树进行静态分析,documented and tracked. The footprint and scope of mature and stable APIs expands

    并记录偏差和误报。as we move from one LTS to the next giving users access to bleeding edge features

and new hardware while keeping a stable foundation that evolves over time.

- 记录的组件和 API (Documented components and APIS)

- 需求目录 (Requirements Catalog)Extended Stabilisation Period

- 验证计划 (Verification Plans)+++++++++++++++++++++++++++++

- 验证报告 (Verification Reports)

- 覆盖率报告 (Coverage Reports)Zephyr LTS development cycle differs from regular releases and has an extended

- 需求可追溯性矩阵 (RTM) (Requirements Traceability Matrix)stabilization period. Feature freeze of regular releases happens 3-4 weeks

- SPDX 许可证报告 (SPDX License Reports)before the scheduled release date. The stabilization period for LTS is extended

by 3 weeks with the feature freeze occurring 6-7 weeks before the anticipated

每个发布都使用上述产品创建以记录发布时软件的质量和状态。release date. The time between code freeze and release date is extended in this case.



长期支持和维护 (Long Term Support and Maintenance)Stable APIs

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



LTS 发布每 2.5 到 3 年发布一次,并独立于主树进行分支和维护,Zephyr LTS provides a stable and long-lived foundation for developing

大约 5 年后发布。products. To guarantee stability of the APIs and the implementation of such

APIs it is required that any release software that makes the core of the OS

支持分为三个主要阶段:went through the Zephyr API lifecycle and stabilized over at least 2 releases.

This guarantees that we release many of the highlighted and core features with

- **第 1 阶段 (前 2 年)** (Phase 1 (first 2 years)): 常规错误修复和安全修复,mature and well-established implementations with stable APIs that are

  包括平台和驱动程序修复。supported during the lifetime of the release LTS.

- **第 2 阶段 (后续 3+ 年)** (Phase 2 (following 3+ years)): 仅安全和操作系统稳定性修复。

- **第 3 阶段** (Phase 3): 扩展支持可能通过第三方获得(细节待定)。- API Freeze (LTS - 2)



对给定 LTS 发布(LTS *N*)的支持一直持续到 LTS 两个版本后的初始发布(LTS *N+2*)。  - All stable APIs need to be frozen 2 releases before an LTS. APIs can be extended

LTS *N* 的最终发布发生在 LTS *N+2* 的初始发布后不久。    with additional features, but the core implementation is not modified. This

    is valid for the following subsystems for example:

当前支持的 LTS 发布及其 EOL 日期列表可以在 :ref:`此处 <supported_releases>` 找到。

    - Device Drivers (i2c.h, spi.h)...

.. figure:: lts.svg    - Kernel (k_*):

    :align: center    - OS services (logging,debugging, ..)

    :alt: Long Term Support Release    - DTS: API and bindings stability

    :figclass: align-center    - Kconfig

    :width: 80%

  - New APIs for experimental features can be added at any time as long as they

    长期支持发布 (Long Term Support Release)    are standalone and documented as experimental or unstable features/APIs.

- Feature Freeze (LTS - 1)

更改和修复双向流动。但是,从主分支到 LTS 分支的更改将仅限于适用于两个分支的修复  - No new features or overhaul/restructuring of code covering major LTS features.

和仅适用于现有功能。

    - Kernel + Base OS

所有适用于主线树的 LTS 分支的修复应也提交到主线树。    - Additional advertised LTS features



可审计的代码库 (Auditable Code Base)  - Auxiliary features on top of and/or extending the base OS and advertised LTS features

===================================    can be added at any time and should be marked as experimental if applicable



可审计的代码库应从 Zephyr OS 功能的定义子集建立,范围将受限。LTS、开发树和可审计Quality Driven Process

代码库应在创建审计分支后保持同步,但在审计分支中添加新功能时应有更严格的流程,++++++++++++++++++++++

该分支用于认证。

The Zephyr project follows industry standards and processes with the goal of

在新功能进入可审计代码库之前,将应用此流程。providing a quality oriented releases. This is achieved by providing the

following products to track progress, integrity and quality of the software

初始和后续认证目标将由 Zephyr 项目治理委员会决定。components provided by the project:



实现选定认证的流程将由安全和安全工作组确定,并与 TSC 协调。- Compliance with published coding guidelines, style guides and naming

  conventions and documentation of deviations.

- Static analysis reports

硬件支持层级 (Hardware Support Tiers)

***********************************  - Regular static analysis on the complete tree using available commercial and

    open-source tools, and documentation of deviations and false positives.

第 0 层: 模拟平台 (Tier 0: Emulation Platforms)

==============================================- Documented components and APIS

- Requirements Catalog

- 测试在这些平台上既构建又运行在 CI 中,因此运行时故障可以阻止拉取请求。- Verification Plans

- 由 Zephyr 项目本身支持,致力于在发布中修复错误。- Verification Reports

- 每个新架构需要一个第 0 层平台。- Coverage Reports

- 针对此层级平台报告的错误应被评估并视为 Zephyr 中的常规错误,应以最高优先级处理。- Requirements Traceability Matrix (RTM)

- SPDX License Reports

第 1 层: 支持的平台 (Tier 1: Supported Platforms)

===============================================Each release is created with the above products to document the quality and the

state of the software when it was released.

- 特定团队的承诺,使用 twister 设备测试为"Zephyr 兼容性测试套件"(详情待定)定期

  运行测试,使用开源和公开提供的驱动程序。Long Term Support and Maintenance

- 致力于及时修复错误以进行发布。不由"Zephyr 项目"本身支持。++++++++++++++++++++++++++++++++++

- 一般可购买性 (General availability for purchase)

- 针对此层级平台报告的错误应被评估并视为 Zephyr 中的常规错误,应以中到高优先级处理。LTS releases are published every 2.5 to 3 years and are branched and maintained independently from

the main tree for approximately 5 years after they were released.

第 2 层: 社区平台 (Tier 2: Community Platforms)

==============================================Support is provided in three main phases:



- 平台实现在上游可用,无测试承诺,可能无法一般获得。- **Phase 1 (first 2 years):** General bug fixes and security fixes, including platform and driver

- 有一位致力于响应问题 / 审查补丁的专职维护人员。  fixes.

- 针对此层级平台报告的错误不被视为 Zephyr 中的常规错误。- **Phase 2 (following 3+ years):** Security and OS stability fixes only.

- **Phase 3:** Extended support may be available through third parties (details to be determined).

第 3 层: 已弃用和不受支持的平台 (Tier 3: Deprecated and unsupported Platforms)

===========================================================================Support for a given LTS release (LTS *N*) continues until the initial release of the LTS two

versions ahead (LTS *N+2*). A final release of LTS *N* occurs shortly after the initial release of

- 平台实现可用,但无所有者或无响应的所有者。LTS *N+2*.

- 不可用支持承诺。

- 如果没有人努力将其提升到第 2 层或更好,可能会从上游删除。The list of currently supported LTS releases and their EOL dates can be found

- 针对此层级平台报告的错误不被视为 Zephyr 中的常规错误。:ref:`here <supported_releases>`.



.. figure:: lts.svg

发布程序 (Release Procedure)    :align: center

***************************    :alt: Long Term Support Release

    :figclass: align-center

本部分记录了发布管理员的责任,以便它作为发布管理员的知识存储库。    :width: 80%



发布清单 (Release Checklist)    Long Term Support Release

==========================

Changes and fixes flow in both directions. However, changes from main branch to an

每个发布都有一个与其关联的 GitHub 问题,其中包含完整的清单。发布完成后,将创建下一个发布的清单。LTS branch will be limited to fixes that apply to both branches and for existing

features only.

标记 (Tagging)

=============All fixes for an LTS branch that apply to the mainline tree shall be submitted to

mainline tree as well.



以下语法应用于 Git 中的发布和标签:Auditable Code Base

===================

- 发布 [主要].[次要].[补丁级别] (Release [Major].[Minor].[Patch Level])

- 发布候选版本 [主要].[次要].[补丁级别]-rc[RC 号] (Release Candidate [Major].[Minor].[Patch Level]-rc[RC Number])An auditable code base is to be established from a defined subset of Zephyr OS

- 标记:features and will be limited in scope. The LTS,  development tree, and the

auditable code bases shall be kept in sync after the audit branch is created,

  - v[主要].[次要].[补丁级别]-rc[RC 号]but with a more rigorous process in place for adding new features into the audit

  - v[主要].[次要].[补丁级别]branch used for certification.

  - v[主要].[次要].99 - 应用于主分支的标签,表示 v[主要].[次要+1] 的工作已开始。

    例如,v1.7.99 将在 v1.8 流程开始时标记。该标签对应于为进行中的主分支版本定义的This process will be applied before new features move into the

    VERSION_MAJOR/VERSION_MINOR/PATCHLEVEL 宏。此标签的存在允许在主分支上为"git describe"生成合理的输出,auditable code base.

    通常用于自动构建和 CI 工具。

The initial and subsequent certification targets will be decided by the Zephyr project

governing board.

.. figure:: release_flow.png

    :align: centerProcesses to achieve selected certification will be determined by the Security and

    :alt: ReleasesSafety Working Groups and coordinated with the TSC.

    :figclass: align-center

    :width: 80%

Hardware Support Tiers

    Zephyr 代码和发布 (Zephyr Code and Releases)***********************



最终发布和每个发布候选版本应使用以下步骤进行标记:Tier 0: Emulation Platforms

===========================

.. note::

- Tests are both built and run in these platforms in CI, and therefore runtime

    标记需要通过明确的 git 命令完成,而不是通过 GitHub 的发布界面。GitHub 发布界面  failures can block Pull Requests.

    不生成带注释的标签(无论是发布还是预发布,它都生成"轻量级"标签)。你还应该将你的- Supported by the Zephyr project itself, commitment to fix bugs in releases.

    gpg 公钥上传到你的 GitHub 账户,因为下面的说明涉及创建已签名的标签。但是,- One Tier 0 platform is required for each new architecture.

    如果你没有 gpg 公钥,你可以选择从下面的命令中删除 ``-s`` 选项。- Bugs reported against platforms of this tier are to be evaluated and treated as

  a general bug in Zephyr and should be dealt with the highest priority.

.. tabs::

Tier 1: Supported Platforms

    .. tab:: 发布候选版本 (Release Candidate)===========================



        .. note::- Commitment from a specific team to run tests using twister device

  testing for the "Zephyr compatibility test suite" (details TBD)

            本部分使用标记 1.11.0-rc1 作为示例,用适当的发布候选版本替换。  on a regular basis using open-source and publicly available drivers.

- Commitment to fix bugs in time for releases. Not supported by "Zephyr Project"

        #. 更新位于 Git 存储库根目录中的 :zephyr_file:`VERSION` 文件中的版本变量,  itself.

           以匹配此发布候选版本的版本。``EXTRAVERSION`` 变量用于标识此候选版本的- General availability for purchase

           rc[RC 号]值::- Bugs reported against platforms of this tier are to be evaluated and treated

  as a general bug in Zephyr and should be dealt with medium to high priority.

            EXTRAVERSION = rc1

Tier 2: Community Platforms

        #. 使用 ``release: Zephyr 1.11.0-rc1`` 作为提交主题发布包含更新的 :zephyr_file:`VERSION`===========================

           文件的 PR。成功 CI 后合并 PR。

- Platform implementation is available in upstream, no commitment to testing,

        #. 标记并推送版本,使用带注释的标签::  may not be generally available.

- Has a dedicated maintainer who commits to respond to issues / review patches.

            $ git pull- Bugs reported against platforms of this tier are NOT considered as

            $ git tag -s -m "Zephyr 1.11.0-rc1" v1.11.0-rc1  a general bug in Zephyr.



        #. 验证标签已正确签名,``git show`` 对于标签必须包含签名Tier 3: Deprecated and unsupported Platforms

           (在输出中查找 ``BEGIN PGP SIGNATURE`` 或 ``BEGIN SSH SIGNATURE`` 标记)::============================================



            $ git show v1.11.0-rc1- Platform implementation is available, but no owner or unresponsive owner.

- No commitment to support is available.

        #. 推送标签::- May be removed from upstream if no one works to bring it up to tier 2 or better.

- Bugs reported against platforms of this tier are NOT considered as

            $ git push git@github.com:zephyrproject-rtos/zephyr.git v1.11.0-rc1  a general bug in Zephyr.



        #. 发送电子邮件至邮件列表(``announce`` 和 ``devel``)的链接到发布

Release Procedure

    .. tab:: 最终发布 (Final Release)******************



        .. note::This section documents the Release manager responsibilities so that it serves as

a knowledge repository for Release managers.

            本部分使用标记 1.11.0 作为示例,用适当的最终发布版本替换。

Release Checklist

        当所有最终发布标准都满足并且最终发布说明已批准并合并到存储库中时,=================

        最终发布版本将使用以下流程进行设置和存储库标记:

Each release has a GitHub issue associated with it that contains the full

        #. 更新位于 Git 存储库根目录中的 :zephyr_file:`VERSION` 文件中的版本变量。checklist. After a release is complete, a checklist for the next release is

           将 ``EXTRAVERSION`` 变量设置为空字符串以指示最终发布::created.



            EXTRAVERSION =Tagging

=======

        #. 使用 ``release: Zephyr 1.11.0`` 作为提交主题发布包含更新的 :zephyr_file:`VERSION`

           文件的 PR。成功 CI 后合并 PR。

        #. 标记并推送版本,使用两个带注释的标签::The following syntax should be used for releases and tags in Git:



            $ git pull- Release [Major].[Minor].[Patch Level]

            $ git tag -s -m "Zephyr 1.11.0" v1.11.0- Release Candidate [Major].[Minor].[Patch Level]-rc[RC Number]

- Tagging:

        #. 验证标签已正确签名,``git show`` 对于标签必须包含签名

           (在输出中查找 ``BEGIN PGP SIGNATURE`` 或 ``BEGIN SSH SIGNATURE`` 标记)::  - v[Major].[Minor].[Patch Level]-rc[RC Number]

  - v[Major].[Minor].[Patch Level]

            $ git show v1.11.0  - v[Major].[Minor].99 - A tag applied to main branch to signify that work on

    v[Major].[Minor+1] has started. For example, v1.7.99 will be tagged at the

        #. 推送标签::    start of v1.8 process. The tag corresponds to

    VERSION_MAJOR/VERSION_MINOR/PATCHLEVEL macros as defined for a

            $ git push git@github.com:zephyrproject-rtos/zephyr.git v1.11.0    work-in-progress main branch version. Presence of this tag allows generation of

    sensible output for "git describe" on main branch, as typically used for

        #. 在发布页面顶部找到新的 ``v1.11.0`` 标签,并使用 ``Edit tag`` 按钮编辑发布,    automated builds and CI tools.

           具有以下内容:



            * 将 ``docs/releases/release-notes-1.11.rst`` 的概述复制到发布说明文本框中,.. figure:: release_flow.png

              并链接到 docs.zephyrproject.org 上的完整发布说明文件。    :align: center

    :alt: Releases

        #. 发送电子邮件至邮件列表(``announce`` 和 ``devel``)的链接到发布    :figclass: align-center

    :width: 80%

    Zephyr Code and Releases

The final release and each release candidate shall be tagged using the following
steps:

.. note::

    Tagging needs to be done via explicit git commands and not via GitHub's release
    interface.  The GitHub release interface does not generate annotated tags (it
    generates 'lightweight' tags regardless of release or pre-release). You should
    also upload your gpg public key to your GitHub account, since the instructions
    below involve creating signed tags. However, if you do not have a gpg public
    key you can opt to remove the ``-s`` option from the commands below.

.. tabs::

    .. tab:: Release Candidate

        .. note::

            This section uses tagging 1.11.0-rc1 as an example, replace with
            the appropriate release candidate version.

        #. Update the version variables in the :zephyr_file:`VERSION` file
           located in the root of the Git repository to match the version for
           this release candidate. The ``EXTRAVERSION`` variable is used to
           identify the rc[RC Number] value for this candidate::

            EXTRAVERSION = rc1

        #. Post a PR with the updated :zephyr_file:`VERSION` file using
           ``release: Zephyr 1.11.0-rc1`` as the commit subject. Merge
           the PR after successful CI.

        #. Tag and push the version, using an annotated tag::

            $ git pull
            $ git tag -s -m "Zephyr 1.11.0-rc1" v1.11.0-rc1

        #. Verify that the tag has been signed correctly, ``git show`` for the
           tag must contain a signature (look for the ``BEGIN PGP SIGNATURE``
           or ``BEGIN SSH SIGNATURE`` marker in the output)::

            $ git show v1.11.0-rc1

        #. Push the tag::

            $ git push git@github.com:zephyrproject-rtos/zephyr.git v1.11.0-rc1

        #. Send an email to the mailing lists (``announce`` and ``devel``)
           with a link to the release

    .. tab:: Final Release

        .. note::

            This section uses tagging 1.11.0 as an example, replace with the
            appropriate final release version.

        When all final release criteria has been met and the final release notes
        have been approved and merged into the repository, the final release version
        will be set and repository tagged using the following procedure:

        #. Update the version variables in the :zephyr_file:`VERSION` file
           located in the root of the Git repository. Set ``EXTRAVERSION``
           variable to an empty string to indicate final release::

            EXTRAVERSION =

        #. Post a PR with the updated :zephyr_file:`VERSION` file using
           ``release: Zephyr 1.11.0`` as the commit subject. Merge
           the PR after successful CI.
        #. Tag and push the version, using two annotated tags::

            $ git pull
            $ git tag -s -m "Zephyr 1.11.0" v1.11.0

        #. Verify that the tag has been signed correctly, ``git show`` for the
           tag must contain a signature (look for the ``BEGIN PGP SIGNATURE``
           or ``BEGIN SSH SIGNATURE`` marker in the output)::

            $ git show v1.11.0

        #. Push the tag::

            $ git push git@github.com:zephyrproject-rtos/zephyr.git v1.11.0

        #. Find the new ``v1.11.0`` tag at the top of the releases page and
           edit the release with the ``Edit tag`` button with the following:

            * Copy the overview of ``docs/releases/release-notes-1.11.rst``
              into the release notes textbox and link to the full release notes
              file on docs.zephyrproject.org.

        #. Send an email to the mailing lists (``announce`` and ``devel``) with a link
           to the release
