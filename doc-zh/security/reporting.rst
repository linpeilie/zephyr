.. _reporting:

安全漏洞报告 (Security Vulnerability Reporting)
###############################################

简介 (Introduction)
===================

Zephyr 项目的漏洞可以通过电子邮件报告至 vulnerabilities@zephyrproject.org 邮件列表。这些报告将在 1 周内由安全响应团队确认和分析。每个漏洞将被录入 Zephyr 项目安全公告 GitHub_。原始提交者将被授予查看他们所报告问题的权限。

.. _GitHub: https://github.com/zephyrproject-rtos/zephyr/security

安全问题管理 (Security Issue Management)
========================================

此错误跟踪系统中的问题将根据此图表在多个状态之间转换:

.. graphviz::

   digraph {
      node [style = rounded];
      init [shape = point];
      New [shape = box];
      Triage [shape = box];
      {
        rank = same;
        rankdir = LR;
        Assigned [shape = box];
        Rejected [shape = box];
      }
      Review [shape = box];
      Accepted [shape = box];
      Public [shape = box];

      init -> New;
      New -> Triage;
      Triage -> Rejected [dir = both];
      Triage -> Assigned;
      Assigned -> Review [dir = both];
      Review -> Accepted;
      Review -> Rejected;
      Accepted -> Public;

   }

- New(新建): 此状态表示由报告者直接输入的新报告。当响应团队响应电子邮件输入时,问题应直接转换到 Triage。

- Triage(分类): 此问题正在等待响应团队进行分类。响应团队将分析问题,确定负责实体,将其分配给该人员,并将问题移至 Assigned 状态。分类的一部分将是设置问题的优先级。

- Assigned(已分配): 问题已被分配,正在等待受让人修复。

- Review(审查): 一旦该问题有 Zephyr 拉取请求,PR 链接将被添加到问题的评论中,并将问题移至 Review 状态。

- Accepted(已接受): 表示此问题已合并到 Zephyr 内的适当分支中。

- Public(公开): 禁运期已结束。问题将被公开可见,相关 CVE 将被更新,文档中的漏洞页面将更新以包含详细信息。

由于安全报告的敏感性质,创建的安全公告保持私密。这些问题仅对某些方可见:

- PSIRT 邮件列表成员

- 报告者

- 其他由 Zephyr 安全小组委员会提议和批准的人员。一般情况下,这将包括:

  - 负责修复的代码所有者。

  - 受此漏洞影响的相关版本的 Zephyr 发布所有者。

Zephyr 安全小组委员会应在任何有三人以上出席的会议期间审查报告的漏洞。在此审查期间,他们应确定是否需要禁运新问题。

禁运指南将基于: 1. 问题的严重性,2. 问题的可利用性。小组委员会决定不需要禁运的问题将在常规 Zephyr 项目错误跟踪系统中重现。

.. _vulnerability_timeline:

安全敏感漏洞应在最多 90 天的禁运期后公开。目的是允许 Zephyr 项目内有 30 天来修复问题,并允许使用 Zephyr 构建产品的外部方有 60 天时间应用和分发这些修复。

.. _vulnerability_fix_recommendations:

对代码的修复应通过 Zephyr 项目 github 中的拉取请求 PR 进行。开发人员应尝试不透露正在修复内容的敏感性质,并且不应引用已分配给问题的 CVE 编号。开发人员应仅描述已修复的内容。

安全小组委员会将维护将禁运的 CVE 映射到这些 PR 的信息(此信息位于 Github 安全公告中),并定期报告安全问题的状态。

每个被视为安全漏洞的问题都将被分配一个 CVE 编号。随着修复的创建,可能需要分配额外的 CVE 编号,或撤销已分配的编号。

漏洞通知 (Vulnerability Notification)
=====================================

每个 Zephyr 版本都应包含该版本中修复的 CVE 报告。由于这些漏洞的敏感性质,该版本应仅包含已修复的 CVE 列表。禁运期后,漏洞页面将被更新以包含这些漏洞的更多详细信息。漏洞页面应对报告者给予信用,除非报告者明确要求匿名。

Zephyr 项目应维护一个漏洞警报邮件列表。此列表最初将包含每个项目成员的联系人。其他方可以通过填写 `漏洞注册表 (Vulnerability Registry)`_ 上的表格请求加入此列表。这些方将由项目总监审查,以确定他们在禁运期间了解安全漏洞具有合法利益。

.. _Vulnerability Registry: https://www.zephyrproject.org/vulnerability-registry/

安全小组委员会将定期向此邮件列表发送信息,描述已知的禁运问题及其在项目内的回溯状态。此信息旨在允许他们确定是否需要将这些更改回溯到任何内部树。

问题分类后,此列表将被告知:

- Zephyr 项目安全公告链接 (GitHub)。

- 分配的 CVE 编号。

- 涉及的子系统。

- 问题的严重性。

在接受修复问题的 PR(合并)后,除上述内容外,此列表还将被告知:

- CVE 编号与修复它的 PR 之间的关联。

- Zephyr 项目内的回溯计划。

安全漏洞的回溯 (Backporting of Security Vulnerabilities)
=========================================================

zephyr 内修复的每个安全问题都应回溯到以下版本:

- 当前长期稳定 (LTS) 版本。

- 最近的两个版本。

修复的开发人员应负责任何必要的回溯,并将其应用于上述任何列出的发布分支,除非修复不适用(漏洞是在此版本发布后引入的)。所有 :ref:`漏洞修复 <vulnerability_fix_recommendations>` 建议适用于回溯拉取请求(和相关问题)。此外,建议开发人员私下通知负责的发布管理器,回溯拉取请求和问题正在解决漏洞。

回溯将在安全公告上跟踪。

需要知道 (Need to Know)
========================

由于安全漏洞的敏感性质,重要的是仅与有需要知道的方共享详细信息和修复。以下方需要在禁运期结束前了解有关安全漏洞的详细信息:

- 维护者只能访问其域区域内的所有信息。

- 当前发布管理器以及受漏洞影响的历史版本的发布管理器(参见上面的回溯)。

- 项目安全事件响应 (PSIRT) 团队将拥有对信息的完全访问权限。PSIRT 由白金成员代表和来自其他成员的志愿者组成,他们负责分类工作。

- 根据需要,可能会邀请发布管理器和维护者参加额外的安全会议以讨论漏洞。
