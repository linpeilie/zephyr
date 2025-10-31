.. _contributor-expectations:

贡献者期望 (Contributor Expectations)
###################################

Zephyr 项目鼓励 :ref:`贡献者 <contributor>` 以较小的拉取请求提交更改。较小的拉取请求 (PR)
有以下好处:

- 审查更快速且更彻底。审查者更容易在多次审查较小更改中抽出几分钟,而不是需要花费大量时间来审查大型 PR。

- 如果审查者或维护者拒绝更改的方向,浪费的工作较少。

- 更容易变基和合并。较小的 PR 不太可能与树中的其他更改冲突。

- 如果 PR 破坏功能,更容易恢复。

.. note::
  此页面不适用于可以有任何大小、任何数量的提交和任何较小 PR 组合的草稿 PR,
  用于测试和预览目的。草稿 PR 没有审查期望,从一开始创建为草稿的 PR 默认不会通知任何人。


定义较小的 PR (Defining Smaller PRs)
***********************************

- 较小的 PR 应包含一个独立自洽的逻辑更改。

- 当添加新的大型功能或 API 时,PR 应仅解决功能的一部分。在这种情况下,
  创建一个 :ref:`RFC 提议 <rfcs>` 为审查者描述功能的其他部分。

- PR 应在以下条件下包含测试或示例:

  - 添加新功能或功能。

  - 修改功能,特别是对于 API 行为合约更改。

  - 修复与硬件无关的错误。测试应该在未修复错误时失败,在应用修复时通过。

- PR 必须更新受函数代码更改影响的任何文档。

- 如果引入新 API,PR 必须包含 API 的示例用法。这为审查者提供上下文,
  并防止提交未使用 API 的 PR。


单个 PR 上的多个提交 (Multiple Commits on a Single PR)
****************************************************

贡献者进一步被鼓励将 PR 分解为多个提交。请记住 PR 中的每个提交必须仍然干净地构建
并通过所有 CI 测试。

例如,在引入 API 扩展时,贡献者可以将 PR 分解为针对这些特定更改的多个提交:

#. 引入新 API,包括共享的设备树绑定
#. 更新驱动程序实现 X,具有特定驱动程序的设备树绑定
#. 更新驱动程序实现 Y
#. 为新 API 添加测试
#. 添加使用 API 的示例
#. 更新文档

大型变更 (Large Changes)
***********************

对 Zephyr 项目的大型更改必须提交 :ref:`RFC 提议 <rfcs>` 描述完整的更改范围和未来工作。
RFC 提议为审查者提供必要的上下文,但允许将较小、增量的 PR 审查并合并到项目中。
RFC 还应定义最小可行实现。

需要 RFC 提议的更改包括:

- 提交新功能。
- 提交新 API。
- :ref:`treewide-changes`。
- 其他可以从 RFC 提议流程受益的大型更改。

维护者有权要求贡献者为太大或太复杂的 PR 创建 RFC。

.. _pr_requirements:

PR 要求 (PR Requirements)
***********************

- PR 中的每个提交必须提供遵循 :ref:`commit-guidelines` 的提交消息。

- 不允许任何 fixup 或 merge 提交,请参见 :ref:`贡献工作流程 (Contribution workflow)` 了解更多信息。

- PR 描述必须包括更改的摘要及其基本原理。

- PR 中的所有文件必须符合 :ref:`许可要求 (Licensing Requirements)<licensing_requirements>`。

- 代码必须遵循 Zephyr :ref:`coding_style` 和 :ref:`coding_guidelines`。

- PR 必须通过所有 CI 检查,如 :ref:`merge_criteria` 所述。贡献者可以将 PR 标记为草稿,
  并明确要求审查者提供早期反馈,即使 CI 检查失败。

- PR 中的提交应代表清晰、逻辑上的更改单元,易于审查并保持二分性。以下指南扩展了此原则:

  1. 不同且逻辑上的更改单元

     每个提交应对应一个独立的、有意义的更改。例如,添加功能、修复错误或重构现有代码应该是单独的提交。
     避免在同一提交中混合不同类型的更改(例如功能实现和不相关的重构)。

  2. 保留二分性

     PR 中的每个提交必须成功构建并通过所有相关测试。这确保可以有效地使用 git bisect
     来识别引入错误或问题的特定提交。

  3. 压缩中间或非最终开发历史

     在开发期间,提交可能包括中间更改(例如部分实现、临时文件或调试代码)。
     这些应该在提交 PR 之前被压缩或重写。删除非最终制品,例如:

     * 后来再次重命名的文件的临时重命名。
     * 在后来提交中被重写或显着更改的代码。

  4. 在提交前确保清晰历史

     使用交互式变基(git rebase -i)在提交 PR 之前清理提交历史。这有助于:

     * 将小的、不完整的提交压缩为单个内聚提交。
     * 确保每个提交保持可二分的。
     * 在改进清晰度时保持正确的作者身份属性。

  5. 重命名和代码重写

     如果在开发过程中的后来的提交中重命名或重写文件或代码,压缩或重写早期提交以反映最终结构。
     这确保:

     * 历史保持清晰且易于遵循。
     * 通过消除冗余重命名或部分重写来保留二分性。

  6. 作者身份属性

     在清理提交历史时,确保作者身份属性保持准确。

  7. 可读且可审查的历史

     最终提交历史应易于理解未来的维护者。逻辑上的更改单元应分组为提交,
     讲述关于所做工作的清晰、连贯的故事。

- 当添加主要新功能时,应将新功能的测试添加到自动测试套件中。所有 API 函数应具有测试用例,
  并应对 API 的行为合约进行测试。维护者和审查者有权自行决定提供的测试是否充分。
  下面的示例演示了如何有效测试 API 的最佳实践。

    - :zephyr_file:`内核计时器测试 (Kernel timer tests) <tests/kernel/timer/timer_behavior>`
      为 :zephyr_file:`内核计时器 (kernel timer) <kernel/timer.c>` 提供大约 85% 的测试覆盖率,
      按代码行数测量。
    - 片外外设的模拟器是测试驱动程序 API 的有效方法。
      :zephyr_file:`燃油表测试 (fuel gauge tests) <tests/drivers/fuel_gauge/sbs_gauge>`
      使用 :zephyr_file:`智能电池模拟器 (smart battery emulator)
      <drivers/fuel_gauge/sbs_gauge/emul_sbs_gauge.c>`,为
      :zephyr_file:`燃油表 API (fuel gauge API) <include/zephyr/drivers/fuel_gauge.h>`
      和 :zephyr_file:`智能电池驱动程序 (smart battery driver)
      <drivers/fuel_gauge/sbs_gauge/sbs_gauge.c>` 提供测试覆盖率。
    - Zephyr 项目的代码覆盖率报告在 `Codecov`_ 上可用。

- API 的不兼容更改还必须更新下一个发布的发布说明,详细说明更改。标记为实验性的 API 从此要求中被排除。

- API 更改必须根据 API 版本规则增加 API 版本号。

- 必须添加和/或更新文档以反映 PR 引入的代码中的更改。文档更改必须使用现有页面中存在的正确术语,
  并且必须用美式英语编写。如果你将图像作为文档的一部分,这些必须遵循 :ref:`doc_images` 中的规则。
  请参见 :ref:`doc_guidelines` 了解更多信息。

- PR 还必须在发布工程团队成员将 PR 合并到 zephyr 树之前满足所有 :ref:`merge_criteria`。

维护者可能要求贡献者将 PR 分解为较小的 PR 并可能要求他们创建 :ref:`RFC 提议 <rfcs>`。

.. _`Codecov`: https://app.codecov.io/gh/zephyrproject-rtos/zephyr

帮助审查者的工作流建议 (Workflow Suggestions That Help Reviewers)
==============================================================

- 除非作者完全按照审查者的建议进行,否则作者不得解决和隐藏评论,他们必须让初始审查者进行。
  Zephyr 项目不要求在合并前解决所有评论。让一些已完成的讨论保持开放有时有助于了解全局。

- 在"Files changed"(文件已更改)视图中使用"Start Review"(开始审查)和"Add Review"(添加审查)绿色按钮回复评论。
  这允许回复多个评论并批量发布响应。这减少了发送给审查者的电子邮件数量。

- 由于 GitHub 没有实现 |git range-diff|_,尽量在审查过程中最小化变基。如果需要变基,
  将其作为与上次 PR 推送相比没有其他更改的单独更新推送。仅进行变基推送时,
  添加评论到 PR 指示哪个提交是变基。

.. |git range-diff| replace:: ``git range-diff``
.. _`git range-diff`: https://git-scm.com/docs/git-range-diff

获取 PR 审查 (Getting PRs Reviewed)
=================================

Zephyr 社区是具有不同承诺级别和优先事项的个人的多样化群体。因此,审查者和维护者可能不会立即处理 PR。

`Zephyr 开发会议 (Zephyr Dev Meeting)`_ 对缺少审查者批准的 PR 进行分类,遵循此流程:

#. 识别并更新缺少受理人的 PR。
#. 识别没有任何评论或审查的 PR,ping PR 受理人以开始审查或分配给不同的维护者。
#. 对于以其他方式停滞的 PR,Zephyr 开发会议 ping 受理人和对 PR 留下评论的任何审查者。

贡献者可以在 Zephyr 开发会议分类流程之外请求 PR 进行如下审查:

- 在 1 周的不活动后,通过向 PR 添加评论来 ping 受理人或审查者。

- 在 2 周的不活动后,在 Discord 上的 `#pr-help`_ 频道发布消息,链接到 PR。

- 在 2 周的不活动后,将 `dev-review`_ 标签添加到 PR。这会将 PR 显式添加到下一个
  `Zephyr 开发会议 (Zephyr Dev Meeting)`_ 的议程中,独立于分类流程。
  并非所有贡献者都有权向 PR 添加标签,在这种情况下贡献者应在 Discord 上寻求帮助
  或向 `Zephyr devel 邮件列表 (Zephyr devel mailing list)`_ 发送电子邮件。

请注意,对于新 PR,贡献者通常应该等待至少一个 Zephyr 开发会议,然后再自己提出请求。

.. _Zephyr devel mailing list: https://lists.zephyrproject.org/g/devel


.. _pr_technical_escalation:

PR 技术上报 (PR Technical Escalation)
===================================

在贡献者反对来自审查者的更改请求的情况下,Zephyr 为解决技术分歧定义了以下上报流程。

在上报技术分歧之前,按照下面的步骤:

- 在 PR 中的受理人、维护者和审查者之间解决。

  - 如果适用,受理人充当仲裁人。

- 或者在下一个 `Zephyr 开发会议 (Zephyr Dev Meeting)`_ 会议中与更多维护者和项目利益相关者一起解决。

  - 涉及的各方和受理人在讨论问题时应在场。

- 如果没有进展,受理人(维护者)有权通过向审查者最少 1 个工作日的时间来回应和重新考虑
  他们的初始更改请求或启动上报流程来驳回陈旧、无关或不相关的更改请求。

  受理人有责任在 PR 中记录驳回任何审查的理由,并应通知审查者他们的审查被驳回。

  为了给审查者时间回应和上报,受理人应该通过不批准 PR 或设置 *DNM* 标签来阻止 PR 被合并。

上报可以由参与审查流程的任何一方(受理人、审查者或更改的原始作者)遵循以下步骤触发:

- 通过在 PR 上添加 `Architecture Review`(架构审查)标签来上报到 `Architecture Working Group`_。
  除了处理此类上报的每周会议外,`Architecture Working Group`_ 应在要求时便于离线审查上报,
  特别是如果任何一方无法参加会议。

- 如果所有解决和上报的途径都已失败,受理人可以上报到 TSC 并通过在 PR 上添加 *TSC* 标签
  获得 TSC 的具有约束力的决议。

- 受理人应确保上报的解决和结果在相关的拉取请求或 Github 问题中得到记录。

.. _#pr-help: https://discord.com/channels/720317445772017664/997527108844798012

.. _dev-review: https://github.com/zephyrproject-rtos/zephyr/labels/dev-review

.. _Zephyr Dev Meeting: https://github.com/zephyrproject-rtos/zephyr/wiki/Zephyr-Committee-and-Working-Groups#zephyr-dev-meeting

.. _Architecture Project: https://github.com/zephyrproject-rtos/zephyr/projects/18

.. _Architecture Working Group: https://github.com/zephyrproject-rtos/zephyr/wiki/Architecture-Working-Group
