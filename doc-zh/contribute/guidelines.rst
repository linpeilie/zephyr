.. _contribute_guidelines:

贡献指南 (Contribution Guidelines)
###############################

作为一个开源项目，我们欢迎并鼓励社区直接向项目提交补丁 (patch)。在协作式开源环境中，统一的提交标准与方法有助于降低活跃开发社区可能带来的混乱。

本文档介绍如何参与项目讨论、记录缺陷 (bug) 与改进需求 (enhancement requests)，以及如何向项目提交补丁，以便你的修改能更快地被接受并合入代码库。


先决条件 (Prerequisites)
**********************

.. _Zephyr Project website: https://zephyrproject.org

作为贡献者，你需要熟悉 Zephyr 项目本身，了解如何按照 `Zephyr Project website`_ 中的说明进行配置、安装与使用，以及如何按照 Zephyr 的 :ref:`getting_started` 搭建开发环境。

你应当熟悉常见的开发者工具，例如 Git 与 CMake，以及诸如 GitHub 等平台。

如果你尚未注册，请在 https://github.com 创建一个免费的 GitHub 账号，并在开发环境中安装好 Git 工具。

.. note::
   Zephyr 的开发流程支持三大主流操作系统 (Linux、macOS 与 Windows)，但下文中的某些工具仅在 Linux 与 macOS 上可用。在 Windows 上，你无需本地运行这些工具，而是依赖使用 GitHub Actions 的持续集成 (Continuous Integration, CI) 服务：当你提交 Pull Request (PR) 时，它会在 GitHub 上自动执行。你可以在 PR 会话列表底部的工作流详情链接中查看失败结果。更多信息见 `Continuous Integration`_。


.. _licensing_requirements:

许可 (Licensing)
***************

许可对开源项目至关重要，它能够确保软件持续以作者期望的条款对外提供。

.. _Apache 2.0 license:
   https://github.com/zephyrproject-rtos/zephyr/blob/main/LICENSE

.. _GitHub repo: https://github.com/zephyrproject-rtos/zephyr

Zephyr 采用 `Apache 2.0 license`_（参见项目 `GitHub repo`_ 中的 LICENSE 文件），在开放贡献与自由使用之间取得平衡。Apache 2.0 是一种宽松 (permissive) 的开源许可，允许你自由使用、修改、分发并销售包含 Apache 2.0 许可软件的自有产品。（更多背景可参考 `Why choose Apache 2.0 licensing`_ 与 `Top 10 Apache License Questions Answered`_ 等文章。）

.. _Why choose Apache 2.0 licensing:
   https://www.zephyrproject.org/faqs/#1571346989065-9216c551-f523

.. _Top 10 Apache License Questions Answered:
   https://www.whitesourcesoftware.com/whitesource-blog/top-10-apache-license-questions-answered/

许可证明确了版权持有者授予开发者的权利。贡献者应充分理解并同意这些许可权利。有时，版权持有者并非贡献者本人，例如当贡献者以公司名义开展工作时。

使用其他许可的组件 (Components using other Licenses)
==============================================

Zephyr 项目中有一些引入或复用的组件使用其他许可，详见 :ref:`Zephyr_Licensing`。

将其他项目中使用非 Apache 2.0 许可的代码引入 Zephyr，需要充分评估其上下文，并获得 Zephyr 管理委员会批准。

通过仔细审查潜在的贡献，并对所贡献的代码强制执行 :ref:`DCO`，我们可以确保 Zephyr 社区基于 Zephyr Project 开发产品时无需担忧专利或版权问题。

关于引入组件的贡献与评审流程，参见 :ref:`external-contributions`。

.. only:: latex

   .. toctree::
      :maxdepth: 1

      ../LICENSING.rst

.. _copyright:

版权与许可声明 (Copyright and License Notices)
=========================================

Zephyr 采用 SPDX/REUSE 风格的文件头。在每个文件开头加入机器可读的版权声明与许可证标识，以便工具识别（例如使用 `REUSE tool`_ 的 :ref:`west spdx <west-spdx>`）。

Zephyr 项目遵循 Linux Foundation 的版权声明 `Community Best Practice`_，因此推荐使用如下版权声明：

.. code-block:: none

   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors

并在其后附上许可证标识：

.. code-block:: none

   SPDX-License-Identifier: Apache-2.0

实践建议：

- 将以上两行置于文件最顶部，并使用该文件语言原生的注释语法。
- 如果你贡献了大量原创内容，*可以* 为你本人或你的组织额外添加一行说明。

.. _Community Best Practice:
   https://www.linuxfoundation.org/blog/copyright-notices-in-open-source-software-projects/

.. _REUSE tool:
   https://github.com/fsfe/reuse-tool

.. _DCO:

开发者来源证明 (Developer Certification of Origin, DCO)
*****************************************************

为尽力确保许可条款得到遵守，Zephyr 项目要求遵循开发者来源证明 (DCO) 流程。

DCO 是附加在每位开发者每次贡献上的声明。在该贡献的提交信息 (commit message) 中（本文稍后将详细说明），开发者只需添加一行 ``Signed-off-by``，即表示同意 DCO。

当开发者提交补丁时，即承诺其有权按照许可证提交该补丁。DCO 协议内容如下，亦可在 https://developercertificate.org/ 查阅。

.. code-block:: none

    Developer's Certificate of Origin 1.1

    By making a contribution to this project, I certify that:

    (a) The contribution was created in whole or in part by me and I
        have the right to submit it under the open source license
        indicated in the file; or

    (b) The contribution is based upon previous work that, to the
        best of my knowledge, is covered under an appropriate open
        source license and I have the right under that license to
        submit that work with modifications, whether created in whole
        or in part by me, under the same open source license (unless
        I am permitted to submit under a different license), as
        Indicated in the file; or

    (c) The contribution was provided directly to me by some other
        person who certified (a), (b) or (c) and I have not modified
        it.

    (d) I understand and agree that this project and the contribution
        are public and that a record of the contribution (including
        all personal information I submit with it, including my
        sign-off) is maintained indefinitely and may be redistributed
        consistent with this project or the open source license(s)
        involved.

DCO 签署 (DCO Sign-Off)
======================

在 DCO 中，“签署 (sign-off)”是指在每个提交日志中加入一行 "Signed-off-by:"。其格式必须如下所示::

   Signed-off-by: Your Name <your.email@example.com>

在你的提交中，请将：

- ``Your Name`` 替换为你的法定姓名（不允许使用化名、黑客昵称或团队名称）。
- ``your.email@example.com`` 替换为你用于撰写提交的真实邮箱地址。不允许使用伪造或匿名邮箱地址，例如 ``you-id+your-username@users.noreply.github.com``。该邮箱必须与提交作者邮箱一致（不一致会导致 CI 失败）。

你可以通过 ``git commit -s`` 自动在提交正文中添加 Signed-off-by: 行。可参考 Zephyr 仓库历史中的其他提交。有关在 Git 中配置用户名与邮箱的说明，见 :ref:`git_setup`。

附加要求：

- 如果你修改了他人创建的既有提交，必须在不移除原有 Signed-off-by 行的前提下，额外加入你自己的 Signed-off-by 行。


源码树结构 (Source Tree Structure)
*******************************

要克隆 Zephyr 主仓库，请参见 :ref:`get_the_code`。

本节介绍主仓库的源码树结构。除 Zephyr 内核本身外，你还会找到技术文档、示例代码、受支持开发板的配置、以及子系统测试的源码。以上内容均欢迎开发者贡献与增强。

理解 Zephyr 源码树有助于你定位与某特定 Zephyr 特性相关的代码。

在源码树顶层，有若干重要文件：

:file:`CMakeLists.txt`
    顶层 CMake 构建系统文件，包含构建 Zephyr 所需的大量逻辑。

:file:`Kconfig`
    顶层 Kconfig 文件，其会引用顶层目录中的 :file:`Kconfig.zephyr`。

    详细的 Kconfig 文档见手册中的 :ref:`Kconfig 章节 <kconfig>`。

:file:`west.yml`
    :ref:`west` 清单，列出了由 west 命令行工具管理的外部仓库。

Zephyr 源码树还包含以下顶层目录，每个目录下可能有一到多个层级的子目录，此处不再一一展开：

:file:`arch`
    与特定体系结构 (architecture) 和片上系统 (SoC) 相关的内核代码。
    每种受支持的体系结构（例如 x86、ARM）都有独立子目录，且包含下面这些区域的子目录：

    * 该体系结构专属的内核源文件
    * 该体系结构专属的、用于内部 API 的头文件

:file:`soc`
    SoC 相关的代码与配置文件。

:file:`boards`
    开发板相关的代码与配置文件。

:file:`doc`
    Zephyr 技术文档的源文件及用于生成 https://docs.zephyrproject.org 网站内容的工具。

:file:`drivers`
    设备驱动代码。

:file:`dts`
    用于描述非可枚举 (non-discoverable) 的板级硬件细节的 :ref:`devicetree <dt-guide>` 源文件。

:file:`include`
    公共 API 的头文件，:file:`lib` 下定义的除外。

:file:`kernel`
    与体系结构无关的内核代码。

:file:`lib`
    库代码，包括最小化的标准 C 库。

:file:`misc`
    其他不属于上述任何顶层目录的杂项代码。

:file:`samples`
    用于演示 Zephyr 各类特性的示例应用程序。

:file:`scripts`
    构建与测试 Zephyr 应用所用的各种脚本与文件。

:file:`cmake`
    构建 Zephyr 所需的其他构建脚本。

:file:`subsys`
    Zephyr 的各子系统，包括：

    * USB 设备栈代码
    * 网络相关代码（包括 Bluetooth 栈与网络栈）
    * 文件系统代码
    * Bluetooth 主机与控制器

:file:`tests`
    Zephyr 功能的测试代码与基准测试。

:file:`share`
    与体系结构无关的额外数据。目前包含 Zephyr 的 CMake 包。


Pull Request 与 Issue (Pull Requests and Issues)
*********************************************

.. _Zephyr Project Issues: https://github.com/zephyrproject-rtos/zephyr/issues

.. _open pull requests: https://github.com/zephyrproject-rtos/zephyr/pulls

.. _Zephyr devel mailing list: https://lists.zephyrproject.org/g/devel

.. _Zephyr Discord Server: https://chat.zephyrproject.org

在着手修复某个问题之前，请先在 `Zephyr Project Issues`_ 中查看是否已有相关报告。你也可以在 `Zephyr devel mailing list`_（或 `Zephyr Discord Server`_）发起讨论，了解他人对该问题（以及你的拟议方案）的看法。也许会有人遇到过同样的问题，或对改动与新增功能有类似想法。欢迎在 `Zephyr devel mailing list`_ 发送邮件，向社区介绍并讨论你的想法。

在提交新 Issue 之前先搜索现有或相关条目是个好习惯。当你提交 Issue（缺陷或特性请求）后，分诊 (triage) 团队通常会在数个工作日内进行审查并给出反馈。

你可以在 GitHub 上查看所有 `open pull requests`_，以及打开的 `Zephyr Project Issues`_。


Git 设置 (Git Setup)
*******************

我们需要知道你是谁、如何联系你。请在 Git 安装中设置 ``user.name``（你的全名）与 ``user.email``（你的邮箱地址）。

例如，若你的名字为 ``Zephyr Developer``、邮箱地址为 ``z.developer@example.com``：

.. code-block:: console

   git config --global user.name "Zephyr Developer"

   git config --global user.email "z.developer@example.com"

.. note::
   ``user.name`` 必须是你的法定全名（最少包含名与姓），不能使用化名或黑客昵称。Git 配置中的邮箱地址必须与用于签署提交的邮箱一致；若不一致，CI 将判定你的 PR 失败。

   如计划通过 Github.com 的网页界面编辑提交，请确保你在 GitHub 个人资料中的 ``email address`` 与 ``name`` 也与 Git 配置（``user.name`` 与 ``user.email``）保持一致。


Pull Request 指南 (Pull Request Guidelines)
***************************************
当你创建新 Pull Request 时，请遵循以下指南，以确保符合 Zephyr 标准并加速评审流程。

如有疑问，建议先在 Zephyr 仓库中查找现有 PR。利用搜索过滤与标签，定位与你拟议改动类似的 PR。

.. note::
   GitHub 默认代码界面使用 4 个字符的制表符宽度。但 Zephyr 遵循 `Linux kernel coding style`_，其约定为 8 个字符的制表符。

   为与其他开发者保持一致的代码视图，请前往 `user preferences on GitHub`_ 将 Tab 宽度修改为 8。

.. _Linux kernel coding style:
   https://kernel.org/doc/html/latest/process/coding-style.html#indentation

.. _user preferences on GitHub:
   https://github.com/settings/appearance

.. _commit-guidelines:

提交信息指南 (Commit Message Guidelines)
=====================================

通过 Git 提交 (commit) 变更。每个提交应包含描述变更的“提交信息 (commit message)”。合格的提交信息应类似如下：

.. code-block:: none

   [area]: [summary of change]

   [Commit message body (must be non-empty)]

   Signed-off-by: [Your Full Name] <[your.email@address]>

请将上例中方括号 (``[like this]``) 内的文本替换为与你提交相符的内容。

下面是一个良好的提交信息示例。

.. code-block:: none

   drivers: sensor: abcd1234: fix bus I/O error handling

   The abcd1234 sensor driver is failing to check the flags field in
   the response packet from the device which signals that an error
   occurred. This can lead to reading invalid data from the response
   buffer. Fix it by checking the flag and adding an error path.

   Signed-off-by: Zephyr Developer <z.developer@example.com>

[area]: [summary of change]
---------------------------

这一行称为提交的“标题 (title)”。标题必须：

* 单行
* 少于 72 个字符
* 后面紧跟一个完全空白的行

[area]
  ``[area]`` 前缀通常用于指示所修改的代码区域；若影响范围更广，也可用于标识更大的上下文。

  示例：

  * ``doc: ...`` 文档改动
  * ``drivers: foo:`` 修改 ``foo`` 驱动
  * ``Bluetooth: Shell:`` 修改 Bluetooth shell
  * ``net: ethernet:`` 与以太网相关的网络改动
  * ``dts:`` 全树 Devicetree 改动
  * ``style:`` 代码风格改动

  如果不确定如何填写，可对你修改的 ``FILE`` 运行 ``git log FILE``，参考之前修改该文件的提交作为灵感。

[summary of change]
  ``[summary of change]`` 应简要描述你做了什么。例如：

  * ``doc: update wiki references to new site``
  * ``drivers: sensor: sensor_shell: fix channel name collision``

提交信息正文 (Commit Message Body)
-------------------------------

.. warning::

   提交信息正文不能为空。即使是很小的改动，也请包含有意义的说明；否则你的 PR 会在 CI 检查中失败。

正文应说明变更做了什么以及为何需要它。务必具体，诸如 ``"Fixes stuff"`` 之类的描述会被拒绝。可视需要包括以下内容：

* 该变更做了“什么”
* 你“为什么”选择这种方式
* 你的“假设”是什么
* 你如何确认它有效——例如，你运行了哪些测试

提交信息中的每一行通常不应超过 75 个字符。更长的行请主动换行；包含长 URL、邮箱等可例外。

有关已接受提交信息的示例，可参考 Zephyr GitHub 的 `changelog <https://github.com/zephyrproject-rtos/zephyr/commits/main>`__。


Signed-off-by: ...
------------------

.. tip::

   你应当已经完成 :ref:`git_setup`。使用 ``git commit -s`` 创建提交，可基于上述信息自动添加 Signed-off-by 行。

出于开源许可原因，你的提交必须包含如下格式的 Signed-off-by 行：

.. code-block:: none

   Signed-off-by: [Your Full Name] <[your.email@address]>

例如，若你的全名为 ``Zephyr Developer``，邮箱为 ``z.developer@example.com``：

.. code-block:: none

   Signed-off-by: Zephyr Developer <z.developer@example.com>

这表示你已亲自确认你的变更符合 :ref:`DCO`。因此必须使用你的法定姓名，不允许使用化名或“黑客别名”。

你的姓名与邮箱必须与 Git 提交中 ``Author:`` 字段一致。

关于贡献者与评审者的更多期望，请参见 :ref:`contributor-expectations`。

添加链接 (Adding Links)
----------------------

.. _GitHub references:
   https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/autolinked-references-and-urls

如果你的变更针对某个具体的 GitHub issue，请在 PR 描述中按照如下格式添加引用：

.. code-block:: none

   Fixes zephyrproject-rtos/zephyr#[issue number]

对于 Zephyr 项目自身的 PR，也可使用简写形式，例如：

.. code-block:: none

   Fixes #[issue number]

将 [issue number] 替换为相关 GitHub issue 编号。例如：

.. code-block:: none

   Fixes zephyrproject-rtos/zephyr#1234

上述语法可确保在 PR 合并时自动关闭对应 issue。为避免歧义，尤其在涉及多个仓库时，请尽量写出完整仓库路径（zephyrproject-rtos/zephyr）。

提交信息中也可使用同样格式。

若需链接额外外部资源——例如相关 issue、数据手册 (datasheet) 或技术参考手册 (TRM)——请使用 ``Link:`` 标签：

.. code-block:: none

   Link: https://github.com/zephyrproject-rtos/zephyr/issues/<issue number>

.. _Continuous Integration:

持续集成 (Continuous Integration, CI)
=================================

Zephyr 项目针对每个 Pull Request (PR) 都会运行持续集成 (CI) 系统，以验证以下方面：

* Git 提交格式
* 代码风格 (Coding Style)
* 面向多体系结构与开发板的 Twister 构建
* 文档构建（用于验证任何文档变更）

CI 基于 GitHub Actions 运行，并使用与 `CI Tests`_ 一节所述相同的工具。在合并 PR 之前，CI 结果必须为绿色，即“所有检查均通过 (All checks have passed)”。CI 会在 PR 创建时运行，并在每次提交后再次运行。

你可在 GitHub PR 页面底部（评审状态下方）查看 CI 的当前状态。根据结果你会看到：

* "All checks have passed"
* "All checks have failed"

如 CI 失败，可点击失败信息下方的 “Details” 链接前往 ``GitHub Actions`` 查看结果。在该摘要页面中会展示包含各类构建的表格；点击失败（非绿色）的那一行即可查看是哪项构建或测试失败。

.. _CI Tests:

本地运行 CI 测试 (Running CI Tests Locally)
=======================================

.. _check_compliance_py:

check_compliance.py
-------------------

``check_compliance.py`` 脚本可用于评估代码是否符合 Zephyr 既定的指南与最佳实践。它充当多个工具的封装器，运行诸如 linter、formatter 等各类检查。

建议开发者在创建新 PR 前先在本地运行该脚本，验证自己的改动：

.. code-block:: bash

   ./scripts/ci/check_compliance.py -c <commit range>

.. note::
   在 Windows 上，如果尚未将 .pl 扩展名与应用程序关联，那么首次在未指定解释器的情况下运行 .pl 文件时，Windows 会询问使用哪个应用打开 Perl 文件。请将默认应用设置为 Strawberry Perl。其可执行文件默认安装在 ``C:\Strawberry\perl\bin\perl.exe``。

twister
-------

.. note::
   twister 仅在 Linux 上获得完整支持；在 Windows 与 macOS 上，并非所有目标设备上的测试执行都受支持。

如果你认为你的改动可能会破坏某些测试，可以先以草稿 (draft) PR 的形式提交，让项目 CI 自动为你运行 :ref:`twister_script`。

如果有测试失败，你可以从 CI 运行日志中查看如何在本地复现，例如：

.. code-block:: bash

   west twister -p native_sim -s tests/drivers/build_all/sensor/drivers.sensor.generic_test

.. _static_analysis:

静态代码分析 (Static Code Analysis)
********************************

Coverity Scan 是一个面向开源项目的免费静态代码分析服务，基于 Coverity 的商业产品，能够分析 C、C++ 与 Java 代码。

Coverity 的静态分析不会实际运行代码，而是通过抽象解释来推断代码的控制流与数据流，能够遍历程序可能采取的所有路径。例如，它能理解 malloc() 返回的内存应在之后使用 free() 释放，并沿分支与函数调用跟踪，检查所有可能路径是否都释放了内存。分析器能够检测各类问题，如资源泄漏（内存、文件描述符）、NULL 解引用、use-after-free、未检查的返回值、死代码、缓冲区溢出、整数溢出、未初始化变量等。

分析结果可在 `Coverity Scan <https://scan.coverity.com/projects/zephyr>`_ 网站查看。访问结果需要你自行创建账号。在 Zephyr 项目页面选择 “Add me to project” 以加入项目，新的成员需由管理员批准。

Zephyr 代码库的静态分析每两周进行一次。对于静态分析工具发现的问题，会自动在 GitHub 上创建 issue，并沿用（或等效映射）工具最初设定的优先级。

为确保问责与高效解决，这些问题将分配给相应维护者（maintainer）。

一个由静态分析、代码质量与软件安全等领域成员组成的专门团队，会持续保障静态分析流程的有效性，并核实识别问题得到及时分类 (triage) 与解决。

工作流程 (Workflow)
==================

如果分析 Coverity 报告后判断为误报 (False positive)，请将分类设为 "False positive" 或 "Intentional"，操作设为 "Ignore"，所有者 (owner) 设为你本人账号，并添加评论说明为何认定为误报或有意为之。

在 Zephyr 仓库中更新相关 GitHub issue 的详情，仅在上述步骤已在扫描服务网站完成后再关闭 issue。若代码中问题仍然存在，而你既未修复、也未在扫描服务侧忽略该条目，则该 issue 将被自动重新打开。


贡献工作流 (Contribution Workflow)
*******************************

我们鼓励的一条通用实践是：进行小而可控的改动。这将简化评审，使合并与变基更容易，并让变更历史清晰干净。

在为 Zephyr 项目做贡献时，请尽量详细说明你的改动，及时更新相关文档，并在提交前充分测试你的更改。

Zephyr 开发者通常结合命令行 Git 与浏览器与 GitHub 交互来完成工作。正如 Git 一贯的风格，完成任务的方式不止一种。下面介绍一种典型工作流：

.. _Create a Fork of Zephyr:
   https://github.com/zephyrproject-rtos/zephyr#fork-destination-box

#. `Create a Fork of Zephyr`_
   到你在 GitHub 的个人账号下。（在 Zephyr 仓库页面右上角点击 fork 按钮。）

#. 在开发电脑上，切换到你 :ref:`obtained the code <get_the_code>` 时创建的 :file:`zephyr` 目录::

     cd zephyrproject/zephyr

   将默认指向 `upstream repository <https://github.com/zephyrproject-rtos/zephyr>`_ 的远端由 ``origin`` 重命名为 ``upstream``::

     git remote rename origin upstream

   将你刚刚创建的 fork 添加为远端，并命名为 ``origin``::

     git remote add origin https://github.com/<your github id>/zephyr

   验证远端仓库::

     git remote -v

   输出应类似::

     origin   https://github.com/<your github id>/zephyr (fetch)
     origin   https://github.com/<your github id>/zephyr (push)
     upstream https://github.com/zephyrproject-rtos/zephyr (fetch)
     upstream https://github.com/zephyrproject-rtos/zephyr (push)

#. 基于 ``main`` 创建用于你改动的主题分支 (topic branch)（若针对某个 issue，建议在分支名中包含其编号）::

     git checkout main
     git checkout -b fix_comment_typo

   某些 Zephyr 子系统会基于非 ``main`` 的分支开发，因此你可能需要在检出时指定该分支::

     git checkout -b fix_out_of_date_patch origin/net

#. 修改代码，本地测试，不断迭代……（也请参考上一章关于 `twister`_ 的说明）。

#. 当一切就绪，开始 PR 流程，首先添加改动的文件::

     git add [file(s) that changed, add -p if you want to be more specific]

   你可以通过以下命令查看尚未暂存 (staged) 的文件::

     git status

#. 确认将要提交的改动符合预期::

     git diff --cached

#. 将改动提交到本地仓库::

     git commit -s

   ``-s`` 选项会自动在提交信息中添加 ``Signed-off-by:``。没有这行表明你同意 :ref:`DCO` 的提交会被拒绝。有关提交信息撰写的具体规范，见 :ref:`commit-guidelines`。

#. 将包含改动的主题分支推送到你个人账号的 fork::

     git push origin fix_comment_typo

#. 打开浏览器进入你的 fork 仓库，点击你刚完成的分支上的 ``Compare & pull request`` 按钮以创建 PR。

#. 检查 PR 的改动，确认你是向 ``main`` 分支创建 PR。标题与描述应来自你的提交信息。

#. 机器人将基于仓库的 MAINTAINERS 文件分配一个或多个建议评审者。若你是项目成员，也可以此时添加更多评审者。

#. 点击提交按钮，PR 发送并等待评审。评审期间会有邮件通知；你也可以在 https://github.com/zephyrproject-rtos/zephyr/pulls 查看。

#. 在等待 PR 被接受和合并期间，你可以创建另一个分支处理其他问题。（务必基于 ``main`` 创建新分支，而不是之前的分支。）::

     git checkout main
     git checkout -b fix_another_issue

   接下来可按上面相同流程在该新主题分支上开展工作。

#. 如果评审者要求你修改补丁，可使用交互式 rebase 来修正。在你的开发仓库中::

     git rebase -i <offending-commit-id>^

   在交互式 rebase 编辑器中，将需要修改的提交（如你的 PR 中包含多个提交）对应的 ``pick`` 改为 ``edit``，或直接删除该行以丢弃该提交。随后修改文件以解决评审中提出的问题。

   与之前一样，检查并测试你的改动。准备好后继续提交流程::

     git add [file(s)]
     git rebase --continue

   如需更新提交说明，更新后继续::

     git push --force origin fix_comment_typo

   通过强制推送 (force push) 更新，你的原 PR 会被相应更新，无需重新创建 PR。

#. 推送更新后，在 PR 页面检查是否存在合并冲突。如有，请在本地进行 rebase::

      git fetch --all
      git rebase --ignore-whitespace upstream/main

   ``--ignore-whitespace`` 选项可阻止 ``git apply``（由 rebase 调用）修改空白字符。解决冲突后再次推送::

      git push --force origin fix_comment_typo

   .. note:: 在 GitHub 之外，修订提交并强制推送是常见且 Zephyr 推荐的评审模式，但它并非 GitHub 主推的模式。强制推送可能带来一些意外行为，例如除最后一次外无法使用 “View Changes” 按钮（GitHub 会提示找不到旧提交），也并非总能比较“最近一次被评审的版本”与“最新提交的版本”。当重写历史时，GitHub 只保证能访问到最新版本。

#. 如果 CI 失败，你需要按上述方式修改代码并通过 rebase 修订提交以修复问题。更多 CI 相关信息见 `Continuous Integration`_。

.. _contribution_tips:

贡献小贴士 (Contribution Tips)
==========================

以下小贴士可改进并加速 PR 的评审流程。遵循它们，你的 PR 更可能获得关注，并更早准备好合入：

.. _git-rebase:
   https://git-scm.com/docs/git-rebase#Documentation/git-rebase.txt---keep-base

#. 推送后续改动时，使用 `git-rebase`_ 的 ``--keep-base`` 选项
#. 在 PR 页面确认改动仍可无冲突合并
#. 确保 PR 标题清晰描述修复或新增的内容
#. 确保 PR 描述 (body) 详细说明提交内容
#. 确保在 PR 描述中引用了所修复的 issue
#. 提交后尽快关注早期 CI 结果，发现问题及时修复
#. 1-2 小时后回看 PR，确认所有 CI 检查均为绿色
#. 如果被请求修改并已提交新改动，记得在 GitHub 界面点击 “Re-request review” 以通知提出修改请求的人

识别贡献来源 (Identifying Contribution Origin)
==========================================

向代码树添加新文件时，请在提交信息中详细说明文件的来源、归属 (attribution) 与预期用途。如果文件为 Zephyr 原创，提交信息应包含如下内容（未提供 Origin 标签时默认视为 "Original"）::

      Origin: Original

若文件是 :ref:`从外部项目引入 <external-contributions>`，提交信息必须包含原项目详情、项目位置、该文件的原始提交 SHA 以及引入目的。

例如，本地维护的引入副本::

      Origin: Contiki OS
      License: BSD 3-Clause
      URL: https://www.contiki-os.org/
      commit: 853207acfdc6549b10eb3e44504b1a75ae1ad63a
      Purpose: Introduction of networking stack.

再例如，在模块仓库中由外部维护的引入副本::

      Origin: Tiny Crypt
      License: BSD 3-Clause
      URL: https://github.com/01org/tinycrypt
      commit: 08ded7f21529c39e5133688ffb93a9d0c94e5c6e
      Purpose: Introduction of TinyCrypt

对外部模块的贡献 (Contributions to External Modules)
***********************************************

关于贡献 :ref:`新模块 <submitting_new_modules>` 以及向 :ref:`已有模块 <changes_to_existing_module>` 提交变更，请遵循 :ref:`modules` 一节中的指南。

.. _treewide-changes:

全树范围更改 (Treewide Changes)
****************************

本节描述“全树范围更改 (treewide changes)”这类贡献及其附加要求。由于其影响范围较大，这些要求旨在提高此类变更在评审与用户侧的可见度。

定义与决策 (Definition and Decision Making)
=======================================

所谓 *treewide change*，是指对 Zephyr API、编码实践或其他开发要求的任何更改，这些更改要么意味着需要在整个 zephyr 源码仓库中进行相应调整，要么可合理预期将对大量基于 Zephyr 的外部源码产生类似影响。

该定义并非严格形式化，因为判断某项变更是否属于 treewide 往往具有主观性，且可能依赖附加上下文。

项目维护者应当基于良好判断、以 Zephyr 开发者体验为优先，来决定某项拟议变更是否属于 treewide。若长期存在分歧，可由 Zephyr 项目的技术指导委员会 (Technical Steering Committee, TSC) 决议，但请避免过早上升到 TSC。

Treewide 更改的要求 (Requirements for Treewide Changes)
===================================================

- zephyr 仓库必须为属于 treewide 的 issue 或 PR 打上 'treewide' GitHub 标签
- 在合并与该变更相关的任何 PR 之前，提出 treewide 更改的人必须创建一个 `RFC issue
  <https://github.com/zephyrproject-rtos/zephyr/issues/new?assignees=&labels=RFC&template=003_rfc-proposal.yml>`_，详述变更内容、动机与影响等。
- 项目的 `Architecture Working Group (WG)
  <https://github.com/zephyrproject-rtos/zephyr/wiki/Architecture-Working-Group>`_ 必须将该 issue 纳入议程，并在相关 PR 合并前讨论是否接受该变更（若 WG 无法达成一致，可上升至 TSC）。
- 架构 WG 必须为每个 treewide 更改指定合并相关 PR 的流程，包括对影响特定子系统的 PR 所需的附加审批与评审时间要求等。
- 在合并与该变更相关的任何 PR 之前，若 RFC 已被架构 WG 接受，提议者必须向 devel@lists.zephyrproject.org 发送邮件说明。

示例 (Examples)
==============

以往的部分 treewide 更改示例：

- 弃用 :ref:`Logging API <logging_api>` v1 并引入 v2（见提交 `262cc55609
  <https://github.com/zephyrproject-rtos/zephyr/commit/262cc55609b73ea61b5f999c6c6daaba20bc5240>`_）
- 移除对旧版 :ref:`dt-bindings` 语法的支持（`6bf761fc0a
  <https://github.com/zephyrproject-rtos/zephyr/commit/6bf761fc0a2811b037abec0c963d60b00c452acb>`_）

注意：在保留旧版本支持的同时新增广泛使用 API 的新版本，不属于 treewide 更改；但弃用与移除此类 API 则属于 treewide 更改。

专用驱动的要求 (Specialized driver requirements)
********************************************

独立设备 (standalone device) 的驱动在可能情况下应尽量使用 Zephyr 的总线 API（SPI、I2C 等），以便该设备可与任意厂商、任意实现了兼容总线的 SoC 配合使用。

若由于某一 SoC 系列具备专用加速器，导致使用 Zephyr API 无法达到全部性能，则可以为该 SoC 系列提供专用路径来扩展对外设的支持。但驱动仍必须为其他所有 SoC 提供常规路径（通过 Zephyr API）。每一项例外都必须经架构 WG 批准，以便进行验证，并有机会从中总结与改进。
.. _contribute_guidelines:

Contribution Guidelines
#######################

As an open-source project, we welcome and encourage the community to submit
patches directly to the project.  In our collaborative open source environment,
standards and methods for submitting changes help reduce the chaos that can result
from an active development community.

This document explains how to participate in project conversations, log bugs
and enhancement requests, and submit patches to the project so your patch will
be accepted quickly in the codebase.


Prerequisites
*************

.. _Zephyr Project website: https://zephyrproject.org

As a contributor, you'll want to be familiar with the Zephyr project, how to
configure, install, and use it as explained in the `Zephyr Project website`_
and how to set up your development environment as introduced in the Zephyr
:ref:`getting_started`.

You should be familiar with common developer tools such as Git and CMake, and
platforms such as GitHub.

If you haven't already done so, you'll need to create a (free) GitHub account
on https://github.com and have Git tools available on your development system.

.. note::
   The Zephyr development workflow supports all 3 major operating systems
   (Linux, macOS, and Windows) but some of the tools used in the sections below
   are only available on Linux and macOS. On Windows, instead of running these
   tools yourself, you will need to rely on the Continuous Integration (CI)
   service using Github Actions, which runs automatically on GitHub when you submit
   your Pull Request (PR).  You can see any failure results in the workflow
   details link near the end of the PR conversation list. See
   `Continuous Integration`_ for more information


.. _licensing_requirements:

Licensing
*********

Licensing is very important to open source projects. It helps ensure the
software continues to be available under the terms that the author desired.

.. _Apache 2.0 license:
   https://github.com/zephyrproject-rtos/zephyr/blob/main/LICENSE

.. _GitHub repo: https://github.com/zephyrproject-rtos/zephyr

Zephyr uses the `Apache 2.0 license`_ (as found in the LICENSE file in
the project's `GitHub repo`_) to strike a balance between open
contribution and allowing you to use the software however you would like
to.  The Apache 2.0 license is a permissive open source license that
allows you to freely use, modify, distribute and sell your own products
that include Apache 2.0 licensed software.  (For more information about
this, check out articles such as `Why choose Apache 2.0 licensing`_ and
`Top 10 Apache License Questions Answered`_).

.. _Why choose Apache 2.0 licensing:
   https://www.zephyrproject.org/faqs/#1571346989065-9216c551-f523

.. _Top 10 Apache License Questions Answered:
   https://www.whitesourcesoftware.com/whitesource-blog/top-10-apache-license-questions-answered/

A license tells you what rights you have as a developer, as provided by the
copyright holder. It is important that the contributor fully understands the
licensing rights and agrees to them. Sometimes the copyright holder isn't the
contributor, such as when the contributor is doing work on behalf of a
company.

Components using other Licenses
===============================

There are some imported or reused components of the Zephyr project that
use other licensing, as described in :ref:`Zephyr_Licensing`.

Importing code into the Zephyr OS from other projects that use a license
other than the Apache 2.0 license needs to be fully understood in
context and approved by the Zephyr governing board.

By carefully reviewing potential contributions and also enforcing a
:ref:`DCO` for contributed code, we can ensure that
the Zephyr community can develop products with the Zephyr Project
without concerns over patent or copyright issues.

See :ref:`external-contributions` for more information about
this contributing and review process for imported components.

.. only:: latex

   .. toctree::
      :maxdepth: 1

      ../LICENSING.rst

.. _copyrights:

Copyright and License Notices
=============================

Zephyr follows SPDX/REUSE-style file headers. Add a machine-readable copyright notice and a license
identifier at the top of each file so tooling can detect them (for example
:ref:`west spdx <west-spdx>`, which uses the `REUSE tool`_).

The Zephyr Project follows the `Community Best Practice`_ for copyright notices from the Linux
Foundation, therefore we recommend using the following copyright notice:

.. code-block:: none

   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors

Include the license identifier alongside it:

.. code-block:: none

   SPDX-License-Identifier: Apache-2.0

Practical guidance:

- Place both lines at the very top of the file using the file's native comment syntax.
- If you authored substantial, original content, you *may* add an additional line for yourself or
  your organization.

.. _Community Best Practice:
   https://www.linuxfoundation.org/blog/copyright-notices-in-open-source-software-projects/

.. _REUSE tool:
   https://github.com/fsfe/reuse-tool

.. _DCO:

Developer Certification of Origin (DCO)
***************************************

To make a good faith effort to ensure licensing criteria are met, the Zephyr
project requires the Developer Certificate of Origin (DCO) process to be
followed.

The DCO is an attestation attached to every contribution made by every
developer. In the commit message of the contribution, (described more fully
later in this document), the developer simply adds a ``Signed-off-by``
statement and thereby agrees to the DCO.

When a developer submits a patch, it is a commitment that the contributor has
the right to submit the patch per the license.  The DCO agreement is shown
below and at https://developercertificate.org/.

.. code-block:: none

    Developer's Certificate of Origin 1.1

    By making a contribution to this project, I certify that:

    (a) The contribution was created in whole or in part by me and I
        have the right to submit it under the open source license
        indicated in the file; or

    (b) The contribution is based upon previous work that, to the
        best of my knowledge, is covered under an appropriate open
        source license and I have the right under that license to
        submit that work with modifications, whether created in whole
        or in part by me, under the same open source license (unless
        I am permitted to submit under a different license), as
        Indicated in the file; or

    (c) The contribution was provided directly to me by some other
        person who certified (a), (b) or (c) and I have not modified
        it.

    (d) I understand and agree that this project and the contribution
        are public and that a record of the contribution (including
        all personal information I submit with it, including my
        sign-off) is maintained indefinitely and may be redistributed
        consistent with this project or the open source license(s)
        involved.

DCO Sign-Off
============

The "sign-off" in the DCO is a "Signed-off-by:" line in each commit's log
message. The Signed-off-by: line must be in the following format::

   Signed-off-by: Your Name <your.email@example.com>

For your commits, replace:

- ``Your Name`` with your legal name (pseudonyms, hacker handles, and the
  names of groups are not allowed)

- ``your.email@example.com`` with the real email address you are using to
  author the commit. Pseudo or anonymized emails such as
  ``you-id+your-username@users.noreply.github.com`` are not allowed. The
  email must match the one you use to author the commit (CI will fail if
  there is no match).

You can automatically add the Signed-off-by: line to your commit body using
``git commit -s``. Use other commits in the zephyr git history as examples.
See :ref:`git_setup` for instructions on configuring user and email settings
in Git.

Additional requirements:

- If you are altering an existing commit created by someone else, you must add
  your Signed-off-by: line without removing the existing one.

.. _source_tree_v2:

Source Tree Structure
*********************

To clone the main Zephyr Project repository use the instructions in
:ref:`get_the_code`.

This section describes the main repository's source tree. In addition to the
Zephyr kernel itself, you'll also find the sources for technical documentation,
sample code, supported board configurations, and a collection of subsystem
tests.  All of these are available for developers to contribute to and enhance.

Understanding the Zephyr source tree can help locate the code
associated with a particular Zephyr feature.

At the top of the tree, several files are of importance:

:file:`CMakeLists.txt`
    The top-level file for the CMake build system, containing a lot of the
    logic required to build Zephyr.

:file:`Kconfig`
    The top-level Kconfig file, which refers to the file :file:`Kconfig.zephyr`
    also found in the top-level directory.

    See :ref:`the Kconfig section of the manual <kconfig>` for detailed Kconfig
    documentation.

:file:`west.yml`
    The :ref:`west` manifest, listing the external repositories managed by
    the west command-line tool.

The Zephyr source tree also contains the following top-level
directories, each of which may have one or more additional levels of
subdirectories not described here.

:file:`arch`
    Architecture-specific kernel and system-on-chip (SoC) code.
    Each supported architecture (for example, x86 and ARM)
    has its own subdirectory,
    which contains additional subdirectories for the following areas:

    * architecture-specific kernel source files
    * architecture-specific kernel include files for private APIs

:file:`soc`
    SoC related code and configuration files.

:file:`boards`
    Board related code and configuration files.

:file:`doc`
    Zephyr technical documentation source files and tools used to
    generate the https://docs.zephyrproject.org web content.

:file:`drivers`
    Device driver code.

:file:`dts`
    :ref:`devicetree <dt-guide>` source files used to describe non-discoverable
    board-specific hardware details.

:file:`include`
    Include files for all public APIs, except those defined under :file:`lib`.

:file:`kernel`
    Architecture-independent kernel code.

:file:`lib`
    Library code, including the minimal standard C library.

:file:`misc`
    Miscellaneous code that doesn't belong to any of the other top-level
    directories.

:file:`samples`
    Sample applications that demonstrate the use of Zephyr features.

:file:`scripts`
    Various programs and other files used to build and test Zephyr
    applications.

:file:`cmake`
    Additional build scripts needed to build Zephyr.

:file:`subsys`
    Subsystems of Zephyr, including:

    * USB device stack code
    * Networking code, including the Bluetooth stack and networking stacks
    * File system code
    * Bluetooth host and controller

:file:`tests`
    Test code and benchmarks for Zephyr features.

:file:`share`
    Additional architecture independent data. It currently contains Zephyr's CMake
    package.

Pull Requests and Issues
************************

.. _Zephyr Project Issues: https://github.com/zephyrproject-rtos/zephyr/issues

.. _open pull requests: https://github.com/zephyrproject-rtos/zephyr/pulls

.. _Zephyr devel mailing list: https://lists.zephyrproject.org/g/devel

.. _Zephyr Discord Server: https://chat.zephyrproject.org

Before starting on a patch, first check in our issues `Zephyr Project Issues`_
system to see what's been reported on the issue you'd like to address.  Have a
conversation on the `Zephyr devel mailing list`_ (or the `Zephyr Discord
Server`_) to see what others think of your issue (and proposed solution).  You
may find others that have encountered the issue you're finding, or that have
similar ideas for changes or additions.  Send a message to the `Zephyr devel
mailing list`_ to introduce and discuss your idea with the development
community.

It's always a good practice to search for existing or related issues before
submitting your own. When you submit an issue (bug or feature request), the
triage team will review and comment on the submission, typically within a few
business days.

You can find all `open pull requests`_ on GitHub and open `Zephyr Project
Issues`_ in Github issues.

.. _git_setup:

Git Setup
*********

We need to know who you are, and how to contact you. To add this
information to your Git installation, set the Git configuration
variables ``user.name`` to your full name, and ``user.email`` to your
email address.

For example, if your name is ``Zephyr Developer`` and your email
address is ``z.developer@example.com``:

.. code-block:: console

   git config --global user.name "Zephyr Developer"
   git config --global user.email "z.developer@example.com"

.. note::
   ``user.name`` must be your full name (first and last at minimum), not a
   pseudonym or hacker handle. The email address that you use in your Git configuration must match the email
   address you use to sign your commits. If they don't match, the CI system will
   fail your pull request.

   If you intend to edit commits using the Github.com UI, ensure that your github profile
   ``email address`` and profile ``name`` also match those used in your git configuration
   (``user.name`` & ``user.email``).

Pull Request Guidelines
***********************
When opening a new Pull Request, adhere to the following guidelines to ensure
compliance with Zephyr standards and facilitate the review process.

If in doubt, it's advisable to explore existing Pull Requests within the Zephyr
repository. Use the search filters and labels to locate PRs related to changes
similar to the ones you are proposing.

.. note::
   GitHub's default code UI uses 4-character tabs. However, Zephyr follows the
   `Linux kernel coding style`_, which uses 8-character tabs.

   To ensure your view of the code is consistent with other developers, please
   go to your `user preferences on GitHub`_ and change the tab width to 8 spaces.

.. _Linux kernel coding style:
   https://kernel.org/doc/html/latest/process/coding-style.html#indentation

.. _user preferences on GitHub:
   https://github.com/settings/appearance

.. _commit-guidelines:

Commit Message Guidelines
=========================

Changes are submitted as Git commits. Each commit has a *commit
message* describing the change. Acceptable commit messages look like
this:

.. code-block:: none

   [area]: [summary of change]

   [Commit message body (must be non-empty)]

   Signed-off-by: [Your Full Name] <[your.email@address]>

You need to change text in square brackets (``[like this]``) above to
fit your commit.

Here is an example of a good commit message.

.. code-block:: none

   drivers: sensor: abcd1234: fix bus I/O error handling

   The abcd1234 sensor driver is failing to check the flags field in
   the response packet from the device which signals that an error
   occurred. This can lead to reading invalid data from the response
   buffer. Fix it by checking the flag and adding an error path.

   Signed-off-by: Zephyr Developer <z.developer@example.com>

[area]: [summary of change]
---------------------------

This line is called the commit's *title*. Titles must be:

* one line
* less than 72 characters long
* followed by a completely blank line

[area]
  The ``[area]`` prefix usually identifies the area of code
  being changed. It can also identify the change's wider
  context if multiple areas are affected.

  Here are some examples:

  * ``doc: ...`` for documentation changes
  * ``drivers: foo:`` for ``foo`` driver changes
  * ``Bluetooth: Shell:`` for changes to the Bluetooth shell
  * ``net: ethernet:`` for Ethernet-related networking changes
  * ``dts:`` for treewide devicetree changes
  * ``style:`` for code style changes

  If you're not sure what to use, try running ``git log FILE``, where
  ``FILE`` is a file you are changing, and using previous commits that
  changed the same file as inspiration.

[summary of change]
  The ``[summary of change]`` part should be a quick description of
  what you've done. Here are some examples:

  * ``doc: update wiki references to new site``
  * ``drivers: sensor: sensor_shell: fix channel name collision``

Commit Message Body
-------------------

.. warning::

   An empty commit message body is not permitted. Even for trivial
   changes, please include a descriptive commit message body. Your
   pull request will fail CI checks if you do not.

This part of the commit should explain what your change does, and why
it's needed. Be specific. A body that says ``"Fixes stuff"`` will be
rejected. Be sure to include the following as relevant:

* **what** the change does,
* **why** you chose that approach,
* **what** assumptions were made, and
* **how** you know it works -- for example, which tests you ran.

Each line in your commit message should usually be 75 characters or
less. Use newlines to wrap longer lines. Exceptions include lines
with long URLs, email addresses, etc.

For examples of accepted commit messages, you can refer to the Zephyr GitHub
`changelog <https://github.com/zephyrproject-rtos/zephyr/commits/main>`__.


Signed-off-by: ...
------------------

.. tip::

   You should have set your :ref:`git_setup`
   already. Create your commit with ``git commit -s`` to add the
   Signed-off-by: line automatically using this information.

For open source licensing reasons, your commit must include a
Signed-off-by: line that looks like this:

.. code-block:: none

   Signed-off-by: [Your Full Name] <[your.email@address]>

For example, if your full name is ``Zephyr Developer`` and your email
address is ``z.developer@example.com``:

.. code-block:: none

   Signed-off-by: Zephyr Developer <z.developer@example.com>

This means that you have personally made sure your change complies
with the :ref:`DCO`. For this reason, you must use your legal name.
Pseudonyms or "hacker aliases" are not permitted.

Your name and the email address you use must match the name and email
in the Git commit's ``Author:`` field.

See the :ref:`contributor-expectations` for a more complete discussion of
contributor and reviewer expectations.

Adding Links
------------

.. _GitHub references:
   https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/autolinked-references-and-urls

If your change addresses a specific GitHub issue, include a reference in the
pull request description using the following format:

.. code-block:: none

   Fixes zephyrproject-rtos/zephyr#[issue number]

For pull requests to the Zephyr project only, the short form can also be used,
for example:

.. code-block:: none

   Fixes #[issue number]

Replace [issue number] with the relevant GitHub issue number. For example:

.. code-block:: none

   Fixes zephyrproject-rtos/zephyr#1234

This syntax ensures that the issue is automatically closed when the pull
request is merged. Always specify the full repository path
(zephyrproject-rtos/zephyr) to avoid ambiguity, especially when working across
multiple repositories.

The same format can also be used in commit messages.

For linking to additional external resources—such as related issues,
datasheets, or technical reference manuals—use the ``Link:`` tag:

.. code-block:: none

   Link: https://github.com/zephyrproject-rtos/zephyr/issues/<issue number>

.. _Continuous Integration:

Continuous Integration (CI)
===========================

The Zephyr Project operates a Continuous Integration (CI) system that runs on
every Pull Request (PR) in order to verify several aspects of the PR:

* Git commit formatting
* Coding Style
* Twister builds for multiple architectures and boards
* Documentation build to verify any doc changes

CI is run on Github Actions and it uses the same tools described in the
`CI Tests`_ section.  The CI results must be green indicating "All
checks have passed" before the Pull Request can be merged.  CI is run when the
PR is created, and again every time the PR is modified with a commit.

The current status of the CI run can always be found at the bottom of the
GitHub PR page, below the review status. Depending on the success or failure
of the run you will see:

* "All checks have passed"
* "All checks have failed"

In case of failure you can click on the "Details" link presented below the
failure message in order to navigate to ``Github Actions`` and inspect the
results.
Once you click on the link you will be taken to the ``Github actions`` summary
results page where a table with all the different builds will be shown. To see
what build or test failed click on the row that contains the failed (i.e.
non-green) build.

.. _CI Tests:

Running CI Tests Locally
========================

.. _check_compliance_py:

check_compliance.py
-------------------

The ``check_compliance.py`` script serves as a valuable tool for assessing code
compliance with Zephyr's established guidelines and best practices. The script
acts as wrapper for a suite of tools that performs various checks, including
linters and formatters.

Developers are encouraged to run the script locally to validate their changes
before opening a new Pull Request:

.. code-block:: bash

   ./scripts/ci/check_compliance.py -c <commit range>

.. note::
   On Windows if the .pl extension has not yet been associated with an
   application, then the first time a .pl file is run without specifying an
   interpreter, Windows will ask what application will open Perl files.
   Set the default app to Strawberry Perl. By default the executable is
   installed at ``C:\Strawberry\perl\bin\perl.exe``.

twister
-------

.. note::
   twister is only fully supported on Linux; on Windows and MacOS the execution
   of tests is not supported on all target devices.

If you think your change may break some test, you can submit your PR as a draft
and let the project CI automatically run the :ref:`twister_script` for you.

If a test fails, you can check from the CI run logs how to rerun it locally,
for example:

.. code-block:: bash

   west twister -p native_sim -s tests/drivers/build_all/sensor/drivers.sensor.generic_test

.. _static_analysis:

Static Code Analysis
********************

Coverity Scan is a free service for static code analysis of Open Source
projects. It is based on Coverity's commercial product and is able to analyze
C, C++ and Java code.

Coverity's static code analysis doesn't run the code. Instead of that it uses
abstract interpretation to gain information about the code's control flow and
data flow. It's able to follow all possible code paths that a program may take.
For example the analyzer understands that malloc() returns a memory that must
be freed with free() later. It follows all branches and function calls to see
if all possible combinations free the memory. The analyzer is able to detect
all sorts of issues like resource leaks (memory, file descriptors), NULL
dereferencing, use after free, unchecked return values, dead code, buffer
overflows, integer overflows, uninitialized variables, and many more.

The results are available on the `Coverity Scan
<https://scan.coverity.com/projects/zephyr>`_ website. In order to access the
results you have to create an account yourself.  From the Zephyr project page,
you may select "Add me to project" to be added to the project. New members must
be approved by an admin.

Static analysis of the Zephyr codebase is conducted on a bi-weekly basis. GitHub
issues are automatically created for any issues detected by static analysis
tools. These issues will have the same (or equivalent) priority initially
defined by the tool.

To ensure accountability and efficient issue resolution, they are assigned to
the respective maintainer who is responsible for the affected code.

A dedicated team comprising members with expertise in static analysis, code
quality, and software security ensures the effectiveness of the static
analysis process and verifies that identified issues are properly
triaged and resolved in a timely manner.

Workflow
========

If after analyzing the Coverity report it is concluded that it is a false
positive please set the classification to either "False positive" or
"Intentional", the action to "Ignore", owner to your own account and add a
comment why the issue is considered false positive or intentional.

Update the related Github issue in the zephyr project with the details, and only close
it after completing the steps above on scan service website. Any issues
closed without a fix or without ignoring the entry in the scan service will be
automatically reopened if the issue continues to be present in the code.

.. _Contribution workflow:

Contribution Workflow
*********************

One general practice we encourage, is to make small,
controlled changes. This practice simplifies review, makes merging and
rebasing easier, and keeps the change history clear and clean.

When contributing to the Zephyr Project, it is also important you provide as much
information as you can about your change, update appropriate documentation,
and test your changes thoroughly before submitting.

The general GitHub workflow used by Zephyr developers uses a combination of
command line Git commands and browser interaction with GitHub.  As it is with
Git, there are multiple ways of getting a task done.  We'll describe a typical
workflow here:

.. _Create a Fork of Zephyr:
   https://github.com/zephyrproject-rtos/zephyr#fork-destination-box

#. `Create a Fork of Zephyr`_
   to your personal account on GitHub. (Click on the fork button in the top
   right corner of the Zephyr project repo page in GitHub.)

#. On your development computer, change into the :file:`zephyr` folder that was
   created when you :ref:`obtained the code <get_the_code>`::

     cd zephyrproject/zephyr

   Rename the default remote pointing to the `upstream repository
   <https://github.com/zephyrproject-rtos/zephyr>`_ from ``origin`` to
   ``upstream``::

     git remote rename origin upstream

   Let Git know about the fork you just created, naming it ``origin``::

     git remote add origin https://github.com/<your github id>/zephyr

   and verify the remote repos::

     git remote -v

   The output should look similar to::

     origin   https://github.com/<your github id>/zephyr (fetch)
     origin   https://github.com/<your github id>/zephyr (push)
     upstream https://github.com/zephyrproject-rtos/zephyr (fetch)
     upstream https://github.com/zephyrproject-rtos/zephyr (push)

#. Create a topic branch (off of ``main``) for your work (if you're addressing
   an issue, we suggest including the issue number in the branch name)::

     git checkout main
     git checkout -b fix_comment_typo

   Some Zephyr subsystems do development work on a separate branch from
   ``main`` so you may need to indicate this in your checkout::

     git checkout -b fix_out_of_date_patch origin/net

#. Make changes, test locally, change, test, test again, ...  (Check out the
   prior chapter on `twister`_ as well).

#. When things look good, start the pull request process by adding your changed
   files::

     git add [file(s) that changed, add -p if you want to be more specific]

   You can see files that are not yet staged using::

     git status

#. Verify changes to be committed look as you expected::

     git diff --cached

#. Commit your changes to your local repo::

     git commit -s

   The ``-s`` option automatically adds your ``Signed-off-by:`` to your commit
   message.  Your commit will be rejected without this line that indicates your
   agreement with the :ref:`DCO`.  See the :ref:`commit-guidelines` section for
   specific guidelines for writing your commit messages.

#. Push your topic branch with your changes to your fork in your personal
   GitHub account::

     git push origin fix_comment_typo

#. In your web browser, go to your forked repo and click on the
   ``Compare & pull request`` button for the branch you just worked on and
   you want to open a pull request with.

#. Review the pull request changes, and verify that you are opening a pull
   request for the ``main`` branch. The title and message from your commit
   message should appear as well.

#. A bot will assign one or more suggested reviewers (based on the
   MAINTAINERS file in the repo). If you are a project member, you can
   select additional reviewers now too.

#. Click on the submit button and your pull request is sent and awaits
   review.  Email will be sent as review comments are made, or you can check
   on your pull request at https://github.com/zephyrproject-rtos/zephyr/pulls.

#. While you're waiting for your pull request to be accepted and merged, you
   can create another branch to work on another issue. (Be sure to make your
   new branch off of ``main`` and not the previous branch.)::

     git checkout main
     git checkout -b fix_another_issue

   and use the same process described above to work on this new topic branch.

#. If reviewers do request changes to your patch, you can interactively rebase
   commit(s) to fix review issues. In your development repo::

     git rebase -i <offending-commit-id>^

   In the interactive rebase editor, replace ``pick`` with ``edit`` to select
   a specific commit (if there's more than one in your pull request), or
   remove the line to delete a commit entirely.  Then edit files to fix the
   issues in the review.

   As before, inspect and test your changes. When ready, continue the
   patch submission::

     git add [file(s)]
     git rebase --continue

   Update commit comment if needed, and continue::

     git push --force origin fix_comment_typo

   By force pushing your update, your original pull request will be updated
   with your changes so you won't need to resubmit the pull request.

#. After pushing the requested change, check on the PR page if there is a
   merge conflict. If so, rebase your local branch::

      git fetch --all
      git rebase --ignore-whitespace upstream/main

   The ``--ignore-whitespace`` option stops ``git apply`` (called by rebase)
   from changing any whitespace. Resolve the conflicts and push again::

      git push --force origin fix_comment_typo

   .. note:: While amending commits and force pushing is a common review model
      outside GitHub, and the one recommended by Zephyr, it's not the main
      model supported by GitHub. Forced pushes can cause unexpected behavior,
      such as not being able to use "View Changes" buttons except for the last
      one - GitHub complains it can't find older commits. You're also not
      always able to compare the latest reviewed version with the latest
      submitted version. When rewriting history GitHub only guarantees access
      to the latest version.

#. If the CI run fails, you will need to make changes to your code in order
   to fix the issues and amend your commits by rebasing as described above.
   Additional information about the CI system can be found in
   `Continuous Integration`_.

.. _contribution_tips:

Contribution Tips
=================

The following is a list of tips to improve and accelerate the review process of
Pull Requests. If you follow them, chances are your pull request will get the
attention needed and it will be ready for merge sooner than later:

.. _git-rebase:
   https://git-scm.com/docs/git-rebase#Documentation/git-rebase.txt---keep-base

#. When pushing follow-up changes, use the ``--keep-base`` option of
   `git-rebase`_

#. On the PR page, check if the change can still be merged with no merge
   conflicts

#. Make sure title of PR explains what is being fixed or added

#. Make sure your PR has a body with more details about the content of your
   submission

#. Make sure you reference the issue you are fixing in the body of the PR

#. Watch early CI results immediately after submissions and fix issues as they
   are discovered

#. Revisit PR after 1-2 hours to see the status of all CI checks, make sure all
   is green

#. If you get request for changes and submit a change to address them, make
   sure you click the "Re-request review" button on the GitHub UI to notify
   those who asked for the changes

Identifying Contribution Origin
===============================

When adding a new file to the tree, it is important to detail the source of
origin on the file, provide attributions, and detail the intended usage. In
cases where the file is an original to Zephyr, the commit message should
include the following ("Original" is the assumption if no Origin tag is
present)::

      Origin: Original

In cases where the file is :ref:`imported from an external project
<external-contributions>`, the commit message shall contain details regarding
the original project, the location of the project, the SHA-id of the origin
commit for the file and the intended purpose.

For example, a copy of a locally maintained import::

      Origin: Contiki OS
      License: BSD 3-Clause
      URL: https://www.contiki-os.org/
      commit: 853207acfdc6549b10eb3e44504b1a75ae1ad63a
      Purpose: Introduction of networking stack.

For example, a copy of an externally maintained import in a module repository::

      Origin: Tiny Crypt
      License: BSD 3-Clause
      URL: https://github.com/01org/tinycrypt
      commit: 08ded7f21529c39e5133688ffb93a9d0c94e5c6e
      Purpose: Introduction of TinyCrypt

Contributions to External Modules
**********************************

Follow the guidelines in the :ref:`modules` section for contributing
:ref:`new modules <submitting_new_modules>` and
submitting changes to :ref:`existing modules <changes_to_existing_module>`.

.. _treewide-changes:

Treewide Changes
****************

This section describes contributions that are treewide changes and some
additional associated requirements that apply to them. These requirements exist
to try to give such changes increased review and user visibility due to their
large impact.

Definition and Decision Making
==============================

A *treewide change* is defined as any change to Zephyr APIs, coding practices,
or other development requirements that either implies required changes
throughout the zephyr source code repository or can reasonably be expected to
do so for a wide class of external Zephyr-based source code.

This definition is informal by necessity. This is because the decision on
whether any particular change is treewide can be subjective and may depend on
additional context.

Project maintainers should use good judgement and prioritize the Zephyr
developer experience when deciding when a proposed change is treewide.
Protracted disagreements can be resolved by the Zephyr Project's Technical
Steering Committee (TSC), but please avoid premature escalation to the TSC.

Requirements for Treewide Changes
=================================

- The zephyr repository must apply the 'treewide' GitHub label to any issues or
  pull requests that are treewide changes

- The person proposing a treewide change must create an `RFC issue
  <https://github.com/zephyrproject-rtos/zephyr/issues/new?assignees=&labels=RFC&template=003_rfc-proposal.yml>`_
  describing the change, its rationale and impact, etc. before any pull
  requests related to the change can be merged

- The project's `Architecture Working Group (WG)
  <https://github.com/zephyrproject-rtos/zephyr/wiki/Architecture-Working-Group>`_
  must include the issue on the agenda and discuss whether the project will
  accept or reject the change before any pull requests related to the change
  can be merged (with escalation to the TSC if consensus is not reached at the
  WG)

- The Architecture WG must specify the procedure for merging any PRs associated
  with each individual treewide change, including any required approvals for
  pull requests affecting specific subsystems or extra review time requirements

- The person proposing a treewide change must email
  devel@lists.zephyrproject.org about the RFC if it is accepted by the
  Architecture WG before any pull requests related to the change can be merged

Examples
========

Some example past treewide changes are:

- the deprecation of version 1 of the :ref:`Logging API <logging_api>` in favor
  of version 2 (see commit `262cc55609
  <https://github.com/zephyrproject-rtos/zephyr/commit/262cc55609b73ea61b5f999c6c6daaba20bc5240>`_)
- the removal of support for a legacy :ref:`dt-bindings` syntax
  (`6bf761fc0a
  <https://github.com/zephyrproject-rtos/zephyr/commit/6bf761fc0a2811b037abec0c963d60b00c452acb>`_)

Note that adding a new version of a widely used API while maintaining
support for the old one is not a treewide change. Deprecation and removal of
such APIs, however, are treewide changes.

Specialized driver requirements
*******************************

Drivers for standalone devices should use the Zephyr bus APIs (SPI, I2C...)
whenever possible so that the device can be used with any SoC from any vendor
implementing a compatible bus.

If it is not technically possible to achieve full performance using the Zephyr
APIs due to specialized accelerators in a particular SoC family, one could
extend the support for an external device by providing a specialized path for
that SoC family. However, the driver must still provide a regular path (via
Zephyr APIs) for all other SoCs. Every exception must be approved by the
Architecture WG in order to be validated and potentially to be learned/improved
from.
