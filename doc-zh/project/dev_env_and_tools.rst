.. _dev-environment-and-tools:

开发环境和工具 (Development Environment and Tools)
##################################################

代码审查 (Code Review)
**********************

GitHub 旨在提供一个框架,在每个提交被接受到代码库之前对其进行审查。更改以拉取请求 (PR) 的形式上传到 GitHub,但在经过审查、通过一系列检查 (CI) 和由维护者批准后,才能真正成为项目的一部分。GitHub 用于支持提交补丁的标准开源实践,然后由项目成员审查,最后应用到代码库中。

拉取请求应该适当地 :ref:`标记 <gh_labels>`,
并链接到任何相关的 :ref:`错误或功能跟踪问题 <bug_reporting>`。

Zephyr 项目使用 GitHub 进行代码审查和 Git 树管理。在提交对任何 Zephyr 组件的更改或增强时,开发人员应使用 GitHub。GitHub Actions 根据 Zephyr 项目仓库中存储的 :zephyr_file:`MAINTAINERS.yml` 文件定义的组件基础,自动分配一个负责任的审查者。一旦审查完成,有限的一组发布经理被允许将拉取请求合并到主分支中。

.. _review_time:

在代码合并前给予审查者足够的时间 (Give reviewers time to review before code merge)
====================================================================================

Zephyr 项目是一个全球性项目,不受特定地理位置或时区的限制。我们有来自全球各地的开发人员和贡献者。当使用拉取请求提出更改时,我们需要允许最少的审查时间,以便给予开发人员和贡献者审查和评论更改的机会。有不同类别的更改,我们知道某些更改确实需要由主题专家和被更改子系统所有者进行审查。许多更改属于"微不足道"的类别,可以通过一般审查来处理,不需要排队等待维护者或代码所有者的审查。此外,某些更改可能需要进一步讨论,并由 TSC 或安全工作组做出决定。总结上述情况,下面的图表为每个类别提出了最少的审查时间:

.. figure:: pull_request_classes.png
    :align: center
    :alt: 拉取请求类别 (Pull request classes)
    :figclass: align-center

    拉取请求类别

工作流程 (Workflow)
-------------------

- 更改的作者可以在他/她的拉取请求中建议该更改应该属于哪个类别。项目维护者或 TSC 成员监控更改的流入,可以通过添加评论来更改拉取请求的标签,说明为什么更改应该属于另一个类别。
- 项目将使用标签系统对拉取请求进行分类。
- 在最少时间过期之前,不应合并更改。

类别/标签 (Categories/Labels)
-------------------------------

紧急修复 (Hotfix)
  阻止开发人员进行日常工作的任何问题的修复,例如 CI 故障、测试故障、影响用户体验的小文档修复。

  这样的修复可以在通过 CI 检查后立即合并。根据修复的严重程度和是否有人(除作者外)可以审查它们,它们可以在没有项目所有者审查的情况下以正当理由合并。

微不足道 (Trivial)
  微不足道的更改是那些看起来很明显且不需要维护者或代码所有者参与的更改。这样的更改不应该改变子系统或组件的逻辑或设计。例如,微不足道的更改可以是:

  - 文档更改
  - 配置更改
  - 次要构建系统调整
  - 代码逻辑的次要优化而不改变逻辑
  - 测试更改和修复
  - 示例修改以支持其他配置或板等

维护者 (Maintainer)
  任何触及子系统或组件的逻辑或原始设计的更改都需要由代码所有者或指定的子系统维护者进行审查。如果代码更改是由所有者以外的贡献者或开发人员发起的,拉取请求需要分配给代码所有者,他/她必须通过向作者提供反馈并请求来自其他开发人员的更多审查来推动拉取请求达到可合并状态。

安全 (Security)
  似乎对系统整体安全性有影响的任何更改都需要由安全工作组的安全专家进行审查。

TSC 和工作组 (TSC and Working Groups)
  引入新功能或功能或改变系统总体工作方式的更改需要由 TSC 或相应的工作组进行审查。例如,对于 :ref:`破坏性 API 更改 <breaking_api_changes>`,提案需要在架构会议上提出,以便相关利益相关者意识到该更改。

拉取请求应该有一个受让人 (A Pull-Request should have an Assignee)
==================================================================

- 拉取请求的受让人不应该是拉取请求的作者
- 拉取请求的受让人负责推动拉取请求达到可合并状态
- 受让人负责驳回过时的审查并从其他开发人员和贡献者那里寻求审查
- 拉取请求不应该在没有受让人批准的情况下合并。

拉取请求不应该由作者在没有审查的情况下合并 (Pull Request should not be merged by author without review)
==========================================================================================================

所有拉取请求都需要进行审查,不应该由作者在没有审查的情况下合并。以下例外适用:

- 热修复: 修复 CI 问题、还原和系统故障
- 发布相关更改: 更改版本文件、应用标签和发布相关活动,不进行任何代码更改。

开发人员和贡献者应该始终寻求审查,但在某些情况下,审查者不可用,需要尽快将代码更改纳入树中。

审查者不应该在没有评论或理由的情况下"请求更改"(Reviewers shall not 'Request Changes' without comments or justification)
=======================================================================================================================================

拉取请求上的任何更改请求 (-1) 都必须有理由。审查者应该避免以无正当理由阻止拉取请求。如果审查者认为不应该在没有他/她的审查的情况下合并更改,那么应该:请求更改类别,例如:

- 微不足道 → 维护者
- 将拉取请求分配给自己,这意味着拉取请求不应该在没有您的批准的情况下合并。

拉取请求在合并前应该有至少 2 个批准 (Pull Requests should have at least 2 approvals before they are merged)
========================================================================================================

拉取请求只能以两个积极的审查(批准)合并。除了合并拉取请求的人(合并 ≠ 批准)外,还需要两个额外的批准才能合并拉取请求。合并请求的人可以在不批准的情况下合并,或批准并合并以达到所需的 2 个批准。

审查者应该跟踪他们已经提供反馈的拉取请求 (Reviewers should keep track of pull requests they have provided feedback to)
==================================================================================================================

如果审查者对拉取请求请求了更改,他/她应该监控拉取请求的状态和/或响应提及请求,以查看他/她的反馈是否已得到解决。未能这样做,否定的审查将被受让人或仓库所有者驳回。审查将根据以下标准被驳回:

- 作者明显解决了反馈或问题
- 审查者在 2 周后没有重新访问拉取请求并多次被作者提及
- 审查与代码更改无关或要求不当的结构更改,例如:

  - 分割 PR
  - 您能修复在 diff 中出现的无关代码吗
  - 您能修复无关问题吗
  - 等等

关闭过时的问题和拉取请求 (Closing Stale Issues and Pull Requests)
==================================================================

- GitHub 上的拉取请求和问题部分不是讨论论坛。它们是我们需要执行并推动至完成的项目。使用邮件列表进行讨论。
- 在问题和拉取请求的情况下,原始发布者需要回答问题并提供有关问题或更改的说明。在没有对请求的响应一周后,将进行第二次尝试从贡献者那里获得响应。再过一周没有响应,该项目可能会被关闭(草稿和 DNM 标记的拉取请求除外)。

持续集成 (Continuous Integration)
*********************************

提交给 GitHub 的所有更改都受到在模拟平台和架构上运行的测试的约束,以识别可以立即识别的故障和回归。使用 Twister 进行的测试还对所有板和平台进行构建测试。文档更改也通过审查和构建测试进行验证,以验证文档生成将成功。

CI 测试运行中发现的任何故障都将导致 CI 系统自动分配一个否定的审查。开发人员应该修复问题并重新处理补丁并重新提交。

CI 基础设施当前运行以下测试:

- 运行 ``checkpatch`` 进行代码样式检查(对错误可以投 -1;参见注释)
- Gitlint: 基于项目要求的 Git 提交样式
- 许可证检查: 检查冲突的许可证
- 运行 ``twister`` 脚本

  - 在 QEMU 中运行内核测试(对错误可以投 -1)
  - 为不同的板构建各种示例(对错误可以投 -1)

- 验证文档构建正确。

.. note::

   ``checkpatch`` 是一个 Perl 脚本,使用正则表达式来提取需要 C 语言解析器准确处理的信息。因此,它有时会产生假阳性。已知的情况包括以下构造:

    .. code-block:: c

      static uint8_t __aligned(PAGE_SIZE) page_pool[PAGE_SIZE * POOL_PAGES];
      IOPCTL_Type *base = config->base;

   这两行都会产生关于 ``*`` 运算符周围空格的诊断:第一行被错误识别为指针类型声明,应该是 ``PAGE_SIZE *POOL_PAGES``,而第二行被错误识别为乘法表达式,应该是 ``IOPCTL_Type * base``。

   在 CI 基础设施给出错误答案的情况下,维护者可以覆盖 -1。

.. _gh_labels:

在 GitHub 中标记问题和拉取请求 (Labeling issues and pull requests in GitHub)
*******************************************************************************

该项目使用 GitHub 问题和拉取请求 (PR) 来跟踪和管理 Zephyr 项目的日常和长期工作和贡献。我们使用 GitHub **标签** 按区域、类型、优先级等对这些问题和 PR 进行分类和组织,使查找和报告相关项目更容易。

所有 GitHub 问题或拉取请求都必须适当标记。问题和 PR 通常分配了多个标签,以帮助将它们分类到不同的可用类别中。审查 PR 时,如果它的标签缺失或不正确,维护者应该修复它。

这为我们所有人在搜索时节省了时间,降低了 PR 或问题被遗忘的机会,加快了审查速度,避免了重复的问题报告,等等。

我们目前拥有的标签按适用性分组如下:

仅适用于问题的标签 (Labels applicable to issues only)
======================================================

.. list-table::
   :header-rows: 1

   * - 标签 (Label)
     - 描述 (Description)

   * - :guilabel:`priority: {high|medium|low}`
     - 用于对错误或 :ref:`功能 <feature-tracking>` 的影响和重要性进行分类。

       注意: 问题优先级通常在错误分类或 TSC 会议期间设置或更改。

   * - :guilabel:`Regression`
     - 某些东西原来是可以工作的,但现在不行了(错误子类型)。

   * - :guilabel:`Enhancement`
     - 对现有 :ref:`功能 <feature-tracking>` 的更改/更新/添加。

   * - :guilabel:`Feature request`
     - 请求实现或包含一个新的 :ref:`功能 <feature-tracking>`。

   * - :guilabel:`Feature`
     - 一个 :ref:`计划的功能 <feature-tracking>`,有里程碑。

   * - :guilabel:`Hardware Support`
     - 涵盖将现有功能(包括 Zephyr 本身)移植到新硬件。

   * - :guilabel:`Duplicate`
     - 此问题是另一个问题的副本(请指定)。

   * - :guilabel:`Good first issue`
     - 适合第一次贡献者进行。

   * - :guilabel:`Release Notes`
     - 需要在发布说明中提及的已知问题的问题,包含额外信息。

任何问题都必须分类和标记为 *Bug*、*Enhancement*、*RFC*、*Feature*、*Feature Request* 或 *Hardware Support* 之一。有关功能请求如何处理以及如何成为功能的更多信息,请参阅 :ref:`功能跟踪 <feature-tracking>`。

仅适用于拉取请求的标签 (Labels applicable to pull requests only)
==================================================================

问题或 PR 描述了对稳定 API 的更改。

.. list-table::
   :header-rows: 1

   * - 标签 (Label)
     - 描述 (Description)

   * - :guilabel:`Hotfix`
     - 阻止开发的问题的修复。

   * - :guilabel:`Trivial`
     - 可以有更短审查时间的简单更改,任何人都可以审查,即拼写错误、简单的单行错误修复等。

   * - :guilabel:`Maintainer`
     - 需要维护者审查。

   * - :guilabel:`Security Review`
     - 由安全专家审查。

   * - :guilabel:`DNM`
     - 此 PR 不应合并(不要合并)。对于进行中的工作,首选 GitHub"草稿"PR。

   * - :guilabel:`Needs review`
     - PR 需要从维护者那里获得关注。

   * - :guilabel:`Backport`
     - PR 是反向移植或应该反向移植。

   * - :guilabel:`Licensing`
     - PR 有许可问题,需要许可专家进行审查。

.. note::
   对于所有适用于 PR 的标签: 请注意,该标签与 PR 复杂性一起会影响应该保持合并多长时间以确保正确审查。有关详细信息,请参阅 :ref:`审查流程 <review_time>`。

适用于拉取请求和问题的标签 (Labels applicable to both pull requests and issues)
===================================================================================

.. list-table::
   :header-rows: 1

   * - 标签 (Label)
     - 描述 (Description)

   * - :guilabel:`area: {area-name}`
     - 表示受错误或拉取请求影响的 Zephyr 子系统(例如,:guilabel:`area: Kernel`、:guilabel:`area: I2C`、:guilabel:`area: Memory Management`),项目功能(例如,:guilabel:`area: Debugging`、:guilabel:`area: Documentation`、:guilabel:`area: Process`)或其他类别(例如,:guilabel:`area: Coding Style`、:guilabel:`area: MISRA-C`)。

       区域维护者应该能够按区域标签进行筛选,并找到与该区域相关的所有问题和 PR。

   * - :guilabel:`platform: {platform-name}`
     - 只影响特定平台的问题或 PR。

   * - :guilabel:`dev-review`
     - 该问题将在以下 `开发审查`_ 中讨论,如果时间允许的话。

       .. _`开发审查`: https://github.com/zephyrproject-rtos/zephyr/wiki/Zephyr-Committee-and-Working-Groups#zephyr-dev-meeting

   * - :guilabel:`TSC`
     - TSC 代表技术指导委员会。该问题将在以下 `TSC 会议`_ 中讨论,如果时间允许的话。

       .. _`TSC 会议`: https://github.com/zephyrproject-rtos/zephyr/wiki/Technical-Steering-Committee-(TSC)

   * - :guilabel:`Breaking API Change`
     - 问题或 PR 描述了对稳定 API 的破坏性更改。有关其他信息,请参阅 :ref:`breaking_api_changes`。

   * - :guilabel:`bug`
     - 问题是一个错误,或 PR 是在修复一个错误。

   * - :guilabel:`Coverity`
     - Coverity 检测到的问题或其修复。

   * - :guilabel:`Waiting for response`
     - Zephyr 开发人员正在等待提交者对问题的响应或解决问题。

   * - :guilabel:`Blocked`
     - 被另一个 PR 或问题阻止。

   * - :guilabel:`Stale`
     - 似乎已被放弃的问题或 PR,需要作者关注。

   * - :guilabel:`In progress`
     - 对于 PR: 正在进行中,不应该被合并。对于问题: 正在进行中。

   * - :guilabel:`RFC`
     - 作者想要来自社区的意见。对于 PR,它应该被视为草稿。

   * - :guilabel:`LTS`
     - 长期发布分支相关。

   * - :guilabel:`EXT`
     - 与外部组件相关。
