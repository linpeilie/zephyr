.. _security-overview:

Zephyr 安全概述 (Zephyr Security Overview)
##########################################

简介 (Introduction)
*******************

本文档概述了 Zephyr 安全小组委员会朝着定义的安全流程迈出的步骤,该流程帮助开发人员构建更安全的软件,同时满足安全合规要求。它介绍了安全流程的关键思想,并概述了需要创建的文档。在实施流程并创建所有支持文档后,本文档是顶层概述和入口点。

概述和范围 (Overview and Scope)
==================

我们从 Zephyr 开发流程的概述开始,该流程主要关注安全功能。

在后续章节中,将详细介绍流程的各个部分。如图 1 所示,这些主要步骤是:

1. **安全开发 (Secure Development):** 定义系统架构和开发流程,确保遵守相关编码原则和质量保证程序。

2. **安全设计 (Secure Design):** 定义安全程序并实施措施来执行它们。创建系统和相关子模块的安全架构,识别威胁,并设计对策。通过代码审查检查其正确实施和威胁模型的有效性。最后,应定义一个用于报告、分类和缓解安全问题的流程。

3. **安全认证 (Security Certification):** 定义 Zephyr RTOS 的可认证部分。这包括评估目标、其资产以及如何保护这些资产。认证声明应得到适当证据的支持。

.. figure:: media/security-process-steps.png

   图 1. 安全流程步骤 (Figure 1. Security Process Steps)

目标受众 (Intended Audience)
=================

本文档是 Zephyr 安全小组委员会和 Zephyr 技术指导委员会开发安全流程的指南。它为(安全)工程师和架构师提供了 Zephyr 安全流程的概述。

术语 (Nomenclature)
============

在本文档中,关键词"MUST"、"MUST NOT"、"REQUIRED"、"SHALL"、"SHALL NOT"、"SHOULD"、"SHOULD NOT"、"RECOMMENDED"、"MAY"和"OPTIONAL"应按照 [RFC2119]_ 中的描述进行解释。

这些词用于定义绝对要求(或禁止)、强烈推荐的要求和真正可选的要求。如 RFC-2119 中所述,"这些术语经常用于指定具有安全影响的行为。不实施 MUST 或 SHOULD,或做规范说 MUST NOT 或 SHOULD NOT 做的事情对安全的影响可能非常微妙。文档作者应该花时间详细说明不遵循建议或要求的安全影响,因为大多数实施者将没有产生规范的经验和讨论的好处。"

安全文档更新 (Security Document Update)
========================

本文档是一个活文档。随着识别出新的要求、特性和更改,它们将通过以下流程添加到本文档中:

1. 相关方将通过拉取请求向 Zephyr 文档仓库提交更改。

2. Zephyr 安全小组委员会将审查这些更改并提供反馈或接受更改。

3. 一旦接受,这些更改将成为文档的一部分。

当前安全定义 (Current Security Definition)
***************************

本节概述了 Zephyr RTOS 内安全开发的当前状态。目前,重点放在功能安全和代码质量保证上,尽管已确定了额外的安全特性范围。

目前实施的三个主要安全措施是:

-  **安全功能 (Security Functionality)** 重点关注加密算法和协议。加密硬件的支持已纳入未来版本的范围。Zephyr 运行时架构是一个单体二进制文件,消除了对动态加载器的需求,从而减少了暴露的攻击面。

-  **质量保证 (Quality Assurance)** 由使用开发流程驱动,该流程要求在将所有代码提交到公共仓库之前进行审查。此外,重用经过验证的构建块(如网络栈)可提高整体质量水平并保证稳定的 API。静态代码分析提供额外的质量检查。

-  **执行保护 (Execution Protection)** 包括线程分离、栈和内存保护,目前在上游 Zephyr RTOS 中可用,从版本 1.9.0 开始(栈保护)。内存保护和线程分离在 X86 的版本 1.10.0 中添加,在 ARM 和 ARC 的版本 1.11.0 中添加。

这些主题将在以下小节中更详细地讨论。

安全功能 (Security Functionality)
======================

Zephyr 中的安全功能主要依赖于加密算法的包含以及其单体系统设计。

加密功能通过 PSA Crypto 提供,mbedTLS 作为底层实现。应用程序利用 PSA Crypto API,确保加密操作的标准化和安全方法。mbedTLS 作为 PSA Crypto 的实现,支持广泛的加密算法,使其适合各种应用需求。

计划为硬件和软件中的供应商特定加密 IP 提供 API,包括以安全访问模块 (SAM)、可信平台模块 (TPM) 和可信执行环境 (TEE) 形式的安全密钥存储。

安全架构基于单体设计,其中 Zephyr 内核和所有应用程序编译为单个静态二进制文件。系统调用实现为函数调用,无需上下文切换。静态链接消除了动态加载恶意代码的可能性。

后续版本中提供了额外的保护功能。提供栈保护机制以防止栈溢出。此外,应用程序可以利用线程分离功能将系统拆分为特权和非特权执行环境。内存保护功能提供了分区系统资源(内存、外设地址空间等)的能力,并
assign resources to individual threads or groups of threads.  Stack,
thread execution level, and memory protection constraints are enforced
at the time of context switch.

Quality Assurance
=================

The Zephyr project uses an automated quality assurance process. The goal
is to have a process including mandatory code reviews, feature and issue
management/tracking, and static code analyses.

Code reviews are documented and enforced using a voting system before
getting checked into the repository by the responsible subsystem's
maintainer. The main goals of the code review are:

-  Verifying correct functionality of the implementation

-  Increasing the readability and maintainability of the contributed
   source code

-  Ensuring appropriate usage of string and memory functions

-  Validation of the user input

-  Reviewing the security relevant code for potential issues

The current coding principles focus mostly on coding styles and
conventions. Functional correctness is ensured by the build system and
the experience of the reviewer. Especially for security relevant code,
concrete and detailed guidelines need to be developed and aligned with
the developers (see: :ref:`secure code`).

Static code analyses are run on the Zephyr code tree on a regular basis,
see :ref:`static_analysis`.

Bug and issue tracking and management is performed using Github. The term
"survivability" was coined to cover pro-active security tasks such as
安全问题分类和管理。被识别为漏洞的问题在 Github 安全公告中管理。

由静态分析确定的问题在作为非问题关闭之前应该进行更严格的审查(至少另一名接受过安全流程培训的人员需要在关闭之前同意非问题)。

已成立安全小组委员会以更详细地开发安全流程;本文档是该流程的一部分。

执行保护 (Execution Protection)
====================

支持执行保护,可以分为以下任务:

-  **内存分离 (Memory separation):** 内存将被分区为区域并根据该内存区域的所有者分配属性。线程只能访问它们控制的区域。

-  **栈保护 (Stack protection):** 栈保护将提供检测和捕获栈溢出的机制。各个线程应只能访问自己的栈。

-  **线程分离 (Thread separation):** 各个线程应只能访问自己的内存资源。当调度线程时,只有该线程拥有的内存资源才可访问。程序流保护和其他防篡改措施等主题目前不在范围内。

系统级安全(生态系统等) (System Level Security (Ecosystem, ...))
================================================================

系统级安全涵盖了多种类别。其中一些示例包括 (System level security encompasses a wide variety of categories. Some
examples of these would be):

-  安全/可信启动 (Secure/trusted boot)
-  空中下载(OTA)更新 (Over the air (OTA) updates)
-  外部通信 (External Communication)
-  设备认证 (Device authentication)
-  板载资源的访问控制 (Access control of onboard resources)

   -  闪存更新 (Flash updating)
   -  安全存储 (Secure storage)
   -  外设 (Peripherals)

-  信任根 (Root of trust)
-  减少攻击面 (Reduction of attack surface)

这些类别中的一些是相互关联的,需要多个部分共同协作才能为应用程序提供完整的解决方案 (Some of these categories are interconnected and rely on multiple pieces
to be in place to produce a full solution for the application)。

安全开发流程 (Secure Development Process)
******************************************

安全代码的开发应遵守特定标准。这些标准包括可以大致分为与软件质量相关和与软件安全相关的两类编码指南和开发流程。此外,应创建系统架构文档并随着未来开发保持更新 (The development of secure code shall adhere to certain criteria. These
include coding guidelines and development processes that can be roughly
separated into two categories related to software quality and related to
software security. Furthermore, a system architecture document shall be
created and kept up-to-date with future development)。

系统架构 (System Architecture)
===============================

.. figure:: media/security-zephyr-system-architecture.png

   图 2: Zephyr 系统架构 (Figure 2: Zephyr System Architecture)

Zephyr 系统架构的高级示意图如图 2 所示。它将架构分为操作系统部分(*内核 + OS 服务*)和用户特定部分(*应用服务*)。操作系统部分本身包含低级、平台特定的驱动程序以及 I/O API、文件系统、内核特定函数和加密库的通用实现 (A high-level schematic of the Zephyr system architecture is given in
Figure 2. It separates the architecture into an OS part (*kernel + OS
Services*) and a user-specific part (*Application Services*). The OS
part itself contains low-level, platform specific drivers and the
generic implementation of I/O APIs, file systems, kernel-specific
functions, and the cryptographic library)。

应创建描述系统架构和设计选择的文档,并随着未来开发保持更新。该文档应包括 Zephyr OS 的基础架构和重要子模块的概述。对于每个模块,应创建专用的架构文档并根据实现进行评估。这些文档应作为新开发人员的入口点和安全架构的基础。有关详细信息,请参阅 :ref:`Zephyr 子系统文档 <os_services>` (A document describing the system architecture and design choices shall
be created and kept up to date with future development. This document
shall include the base architecture of the Zephyr OS and an overview of
important submodules. For each of the modules, a dedicated architecture
document shall be created and evaluated against the implementation.
These documents shall serve as an entry point to new developers and as a
basis for the security architecture. Please refer to the
:ref:`Zephyr subsystem documentation <os_services>` for
detailed information)。

安全编码 (Secure Coding)
=========================

设计像 Zephyr 这样的开放软件系统以保证安全需要遵守一组定义的设计标准。这些标准包含在 Zephyr 项目文档中,特别是在其 :ref:`安全代码 <secure code>` 部分。在 [SALT75]_ 中,定义了以下广泛接受的保护机制原则,以防止安全违规并限制其影响 (Designing an open software system such as Zephyr to be secure requires
adhering to a defined set of design standards. These standards are
included in the Zephyr Project documentation, specifically in its
:ref:`secure code` section. In [SALT75]_, the following, widely
accepted principles for protection mechanisms are defined to prevent
security violations and limit their impact):

-  **开放设计 (Open design)** 作为一种设计原则,融入了这样的格言:在任何广泛使用的系统上,保护机制都不能保密。应使用公开接受的加密算法和完善的加密库,而不是依赖秘密的、定制的安全措施。

-  **机制经济性 (Economy of mechanism)** 规定系统的底层设计应尽可能保持简单和小型。在 Zephyr 项目的背景下,这可以通过模块化代码 [PAUL09]_ 和抽象 API 等方式来实现。

-  **完全中介 (Complete mediation)** 要求对每个对象和进程的每次访问都需要首先进行身份验证。如果可能,应避免存储访问条件的机制。

-  **故障安全默认值 (Fail-safe defaults)** 定义了默认情况下访问受到限制,仅在系统保护方案定义的特定条件下(例如,成功验证后)才被允许。此外,服务的默认设置应选择以提供最大安全性的方式。这对应于"默认安全 (Secure by Default)"范式 [MS12]_。

-  **特权分离 (Separation of privilege)** 是指在授予访问权限之前需要满足两个或更多条件的原则。在 Zephyr 项目的背景下,这可能包括分割密钥 [PAUL09]_。

-  **最小特权 (Least privilege)** 描述了一种访问模型,其中每个用户、程序和线程应在系统中拥有执行其任务所需的最小可能权限子集。这种积极的安全模型旨在最小化系统的攻击面。

-  **Least common mechanism** specifies that mechanisms common to more
   than one user or process shall not be shared if not strictly
   required. The example given in [SALT75]_ is a function that should
   be implemented as a shared library executed by each user and not
   as a supervisor procedure shared by all users.

-  **Psychological acceptability** requires that security features are
   easy to use by the developers in order to ensure its usage and
   the correctness of its application.

In addition to these general principles, the following points are
specific to the development of a secure RTOS:

-  **Complementary Security/Defense in Depth:** do not rely on a single
   threat mitigation approach. In case of the complementary security
   approach, parts of the threat mitigation are performed by the
   underlying platform. In case such mechanisms are not provided by
   the platform, or are not trusted, a defense in depth [MS12]_
   paradigm shall be used.

-  **默认关闭不常用的服务 (Less commonly used services off by default)**: 为了减少系统对潜在攻击的暴露,如果功能或服务很少使用(在 [MS12]_ 中给出了 80% 的阈值),则不应默认启用。对于 Zephyr 项目,这可以使用配置管理来实现。每个功能和模块都应表示为一个配置选项,并需要显式启用。然后,可以禁用特定用例不需要的所有特性、协议和驱动程序。如果启用了低级选项和 API 但应用程序未使用,则应通知用户。

-  **变更管理 (Change management):** 为了保证对系统变更的可追溯性,每个变更都应遵循指定的流程,包括变更请求、影响分析、批准、实施和验证阶段。在每个阶段都应提供适当的文档。所有提交都应与问题跟踪器中的错误报告或变更请求相关。没有有效引用的提交应被拒绝。

基于这些设计原则和普遍接受的最佳实践,应开发、发布安全开发指南,并将其实施到 Zephyr 开发流程中。有关这方面的更多详细信息在 `安全设计 (Secure Design)`_ 部分中给出 (Based on these design principles and commonly accepted best practices, a
secure development guide shall be developed, published, and implemented
into the Zephyr development process. Further details on this are given
in the `Secure Design`_ section)。

质量保证 (Quality Assurance)
=============================

质量保证部分包括以下标准 (The quality assurance part encompasses the following criteria):

-  **遵守编码约定 (Adherence to the Coding Conventions)** 关于编码风格、模块、函数、变量等的命名方案。这增加了 Zephyr 代码库的可读性并简化了代码审查。这些编码约定在签入之前由自动化脚本强制执行。

-  **遵守部署指南 (Adherence to Deployment Guidelines)** 是确保发布版本具有文档完善的特性集和可跟踪的安全问题列表所必需的。

-  **代码审查 (Code Reviews)** 确保代码库的功能正确性,应在签入之前对每个提议的代码更改执行。代码审查应由至少一名独立审查者(而不是代码更改的作者)执行。这些审查应由子系统维护者和开发人员在功能层面上执行,与 `安全设计 (Secure Design)`_ 部分中列出的安全审查不同。有关更多信息,请参阅 :ref:`开发模型 <development_model>` 文档。

-  **静态代码分析 (Static Code Analysis)** 工具可以有效地检测大型代码库中的常见编码错误。所有代码在合并到主仓库之前都应使用适当的工具进行分析。这不是针对单个提交,而是要在特定分支上以某个间隔运行。在每次发布之前删除所有发现或放弃潜在的误报是强制性的。豁免应集中记录,并以源代码内部注释的形式记录。文档应包括所采用的工具及其版本、分析日期、分支和父修订号、豁免原因、相关代码的作者以及豁免的批准者。这至少应在主发布分支和安全分支上运行。应确保每个版本在静态代码分析方面(包括豁免)都有零问题。有关更多信息,请参阅 :ref:`开发模型 <development_model>` 文档。

-  **复杂性分析 (Complexity Analyses)** 应作为开发流程的一部分执行,并应评估圈复杂度等指标。主要目标是使代码尽可能简单。

-  **自动化 (Automation):** 审查流程和编码规则遵守性检查是预提交检查的强制性部分。为了确保一致的应用,它们应作为预提交程序的一部分自动化。在从子系统合并大块代码之前,除了审查流程和编码规则遵守性之外,还必须运行所有静态代码分析并解决问题。

发布和生命周期管理 (Release and Lifecycle Management)
======================================================

生命周期管理包含几个方面 (Lifecycle management contains several aspects):

-  **设备管理 (Device management)** 包括在现场更新支持 Zephyr 的设备的操作系统和/或安全相关子系统的可能性。

-  **生命周期管理 (Lifecycle management):** 应定义和记录系统阶段以及系统状态图中阶段之间的转换。出于安全原因,这应包括在检测到攻击时锁定设备,以及在达到生命周期结束时终止。

-  **发布管理 (Release management)** 描述了定义发布周期、记录发布以及维护已知漏洞和缓解措施记录的过程。特别是出于认证目的,需要以一种可以轻松检测到后续篡改(例如,插入后门等)的方式确保发布的完整性。

-  **Rights management and NDAs:** if required by the chosen
   certification, the confidentiality and integrity of the system
   needs to be ensured by an appropriate rights management (e.g.,
   separate source code repository) and non-disclosure agreements
   between the relevant parties. In case of a repository shared
   between several parties, measures shall be taken that no
   malicious code is checked in.

These points shall be evaluated with respect to their impact on the
development process employed for the Zephyr project.

Secure Design
*************

In order to obtain a certifiable system or product, the security process
needs to be clearly defined and its application needs to be monitored
and driven. This process includes the development of security related
modules in all of its stages and the management of reported security
issues. Furthermore, threat models need to be created for currently
known and future attack vectors, and their impact on the system needs to
be investigated and mitigated. Please refer to the
:ref:`secure code` outlined in the Zephyr project documentation
for detailed information.

The software security process includes:

-  **Adherence to the Secure Development Coding** is mandatory to
   avoid that individual components breach the system security and
   to minimize the vulnerability of individual modules. While this
   can be partially achieved by automated tests, it is inevitable to
   investigate the correct implementation of security features such
   as countermeasures manually in security-critical modules.

-  **Security Reviews** shall be performed by a security architect in
   preparation of each security-targeted release and each time a
   security-related module of the Zephyr project is changed. This
   process includes the validation of the effectiveness of
   implemented security measures, the adherence to the global
   security strategy and architecture, and the preparation of audits
   towards a security certification if required.

-  **Security Issue Management** encompasses the evaluation of potential
   system vulnerabilities and their mitigation as described in
   :ref:`Security Issue Management <reporting>`.

These criteria and tasks need to be integrated into the development
process for secure software and shall be automated wherever possible. On
system level, and for each security related module of the secure branch
of Zephyr, a directly responsible security architect shall be defined to
guide the secure development process.

Security Architecture
=====================

The general guidelines above shall be accompanied by an architectural
security design on system- and module-level. The high level
considerations include

-  The identification of **security and compliance requirements**

-  **Functional security** such as the use of cryptographic functions
   whenever applicable

-  针对已知攻击向量设计**对策 (countermeasures)**

-  记录安全相关的**可审计事件 (auditable events)**

-  支持**可信平台模块(TPM) (Trusted Platform Modules (TPM))** 和
   **可信执行环境(TEE) (Trusted Execution Environments (TEE))**

-  允许使用 Zephyr 的设备进行**现场 (in-the-field)** **更新 (updates)** 的机制

-  任务调度器和分离 (Task scheduler and separation)

安全架构开发基于从整体系统架构的结构概述派生的资产。在此基础上,各个步骤包括 (The security architecture development is based on assets derived from
the structural overview of the overall system architecture. Based on
this, the individual steps include):

1. **识别资产 (Identification of assets)** 例如用户数据、身份验证和加密密钥、密钥生成数据(从 RNG 获得)、安全相关状态信息。

2. **识别威胁 (Identification of threats)** 针对资产的威胁,例如机密性泄露、用户数据操纵等。

3. **定义需求 (Definition of requirements)** 关于资产的安全和保护,例如对策或内存保护方案。

安全架构应与现有的系统架构和实施协调,以确定潜在的偏差并缓解现有的弱点。集成到 Zephyr 项目安全分支的新开发子模块应提供描述其安全架构的单独文档。此外,应考虑并记录它们对系统级安全的影响 (The security architecture shall be harmonized with the existing system
architecture and implementation to determine potential deviations and
mitigate existing weaknesses. Newly developed sub-modules that are
integrated into the secure branch of the Zephyr project shall provide
individual documents describing their security architecture.
Additionally, their impact on the system level security shall be
considered and documented)。

安全漏洞报告 (Security Vulnerability Reporting)
===============================================

有关报告安全漏洞的信息,请参阅 :ref:`报告 <reporting>` (Please see :ref:`reporting` for information on reporting security
vulnerabilities)。

威胁建模和缓解 (Threat Modeling and Mitigation)
================================================

针对 Zephyr RTOS 的安全威胁建模是开发准确的安全架构和大多数认证方案所必需的。此过程的第一步是定义系统要保护的资产。下一步建模这些资产如何受到系统保护以及存在哪些威胁。识别威胁后,将创建相应的威胁模型。该模型包含资产和系统漏洞,以及这些漏洞的潜在利用的描述。此外,要估计对资产、其所在模块和整个系统的影响。然后在模块和系统安全架构中考虑此威胁模型,并定义适当的对策以缓解威胁或限制利用的影响 (The modeling of security threats against the Zephyr RTOS is required for
the development of an accurate security architecture and for most
certification schemes. The first step of this process is the definition
of assets to be protected by the system. The next step then models how
these assets are protected by the system and which threats against them
are present. After a threat has been identified, a corresponding threat
model is created. This model contains the asset and system
vulnerabilities, as well as the description of the potential exploits of
these vulnerabilities. Additionally, the impact on the asset, the module
it resides in, and the overall system is to be estimated. This threat
model is then considered in the module and system security architecture
and appropriate countermeasures are defined to mitigate the threat or
limit the impact of exploits)。

简而言之,威胁建模过程可以分为以下步骤(改编自 [OWASP]_) (In short, the threat modeling process can be separated into these steps
(adapted from [OWASP]_)):

1. 定义资产 (Definition of assets)

2. 应用程序分解和创建适当的数据流图(DFD) (Application decomposition and creation of appropriate data flow
   diagrams (DFDs))

3. 使用 [STRIDE09]_ 和 [CVSS]_ 方法进行威胁识别和分类 (Threat identification and categorization using the [STRIDE09]_ and
   [CVSS]_ approaches)

4. 确定对策和其他缓解方法 (Determination of countermeasures and other mitigation approaches)

此程序应在模块的设计阶段以及模块或系统架构发生重大变更之前执行。此外,每当发现新的漏洞或利用时,都应创建新模型或更新现有模型。在安全审查期间,负责的安全架构师应评估威胁模型和缓解技术 (This procedure shall be carried out during the design phase of modules
and before major changes of the module or system architecture.
Additionally, new models shall be created, or existing ones shall be
updated whenever new vulnerabilities or exploits are discovered. During
security reviews, the threat models and the mitigation techniques shall
be evaluated by the responsible security architect)。

应从这些威胁模型和缓解技术中派生测试,以证明对策的有效性。这些测试应集成到持续集成工作流中,以确保安全性不会因回归而受损 (From these threat models and mitigation techniques tests shall be
derived that prove the effectiveness of the countermeasures. These tests
shall be integrated into the continuous integration workflow to ensure
that the security is not impaired by regressions)。

漏洞分析 (Vulnerability Analyses)
==================================

为了找到软件实施中的薄弱环节,应执行漏洞分析(VA)。特别值得关注的是对加密算法、关键 OS 任务和连接协议的调查 (In order to find weak spots in the software implementation,
vulnerability analyses (VA) shall be performed. Of special interest are
investigations on cryptographic algorithms, critical OS tasks, and
connectivity protocols)。

在纯软件层面,这包括 (On a pure software level, this encompasses)

-  在特定硬件平台上对 RTOS 进行**渗透测试 (Penetration testing)**,这涉及将相应的 Zephyr OS 配置和硬件作为一个系统进行测试。

-  应考虑**侧信道攻击 (Side channel attacks)**(时序不变性、功耗不变性等)。例如,需要确保加密算法和模块的**时序不变性 (timing
   invariance)** 以减少攻击面。这适用于软件实现和使用加密硬件时。

-  应对暴露的 API 和协议执行**模糊测试 (Fuzzing tests)**。

上面给出的列表主要用于说明目的。对于每个模块和完整的 Zephyr 系统(通常在特定硬件平台上),应创建并执行合适的 VA 计划。这些分析的结果应在安全问题管理流程中考虑,并应将学到的经验制定为指南并纳入安全编码指南 (The list given above serves primarily illustration purposes. For each
module and for the complete Zephyr system (in general on a particular
hardware platform), a suitable VA plan shall be created and executed.
The findings of these analyses shall be considered in the security issue
management process, and learnings shall be formulated as guidelines and
incorporated into the secure coding guide)。

如果可能(例如模糊测试分析的情况),这些测试应集成到持续集成流程中 (If possible (as in case of fuzzing analyses), these tests shall be
integrated into the continuous integration process)。

安全认证 (Security Certification)
**********************************

创建 Zephyr RTOS 安全分支的一个目标是创建可认证的系统或其可认证的子模块。认证范围和方案尚待确定。但是,许多认证(例如通用标准 [CCITSE12]_)要求提供证据证明评估声明确实得到满足,因此下文概述了一般认证过程。根据认证方案和评估级别的最终选择,需要完善此流程 (One goal of creating a secure branch of the Zephyr RTOS is to create a
certifiable system or certifiable submodules thereof. The certification
scope and scheme are yet to be decided. However, many certifications such
as Common Criteria [CCITSE12]_ require evidence that the evaluation
claims are indeed fulfilled, so a general certification process is
outlined in the following. Based on the final choices for the
certification scheme and evaluation level, this process needs to be
refined)。

通用认证流程 (Generic Certification Process)
=============================================

一般来说,走向认证或预认证的步骤(比较 [MICR16]_)包括 (In general, the steps towards a certification or precertification
(compare [MICR16]_) are):

1. 在 Zephyr RTOS 内**定义要保护的资产 (definition of assets)**。潜在候选包括机密信息(例如加密密钥)、用户数据(例如通信日志)以及可能的供应商或制造商的知识产权。

2. 开发**威胁模型 (threat model)** 和**安全架构 (security architecture)** 以保护资产免受系统漏洞的利用。由于完整的威胁模型包括包括硬件平台在内的整个产品,因此可以通过拆分模型来实现,该模型包含 Zephyr 的预认证安全分支,供应商可以使用该分支来认证其支持 Zephyr 的产品。

3. 制定**评估目标 (evaluation target)**,其中包括有关要评估和认证的资产安全性的**认证声明 (certification claims)**,以及有关操作条件的假设。

4. 提供**证明 (proof)** 以证明声明得到满足。这包括安全开发过程的一致文档等。

这些步骤在前面的部分也有部分涉及。与这些部分不同,认证过程仅要求考虑应包含在认证中的那些组件。例如,安全架构考虑系统级别的资产,并可能包括与认证无关的项目 (These steps are partially covered in previous sections as well. In
contrast to these sections, the certification process only requires to
consider those components that shall be covered by the certification.
The security architecture, for example, considers assets on system level
and might include items not relevant for the certification)。

认证选项 (Certification Options)
=================================

对于安全认证本身,可以采取以下选项 (For the security certification as such, the following options can be
pursued):

1. **Zephyr 作为纯软件系统的抽象预认证 (Abstract precertification of Zephyr as a pure software system):**
   此选项需要对底层硬件平台和在 Zephyr 之上运行的最终应用程序进行假设。如果硬件和应用程序满足这些假设,则可以更容易地实现完全认证。此选项是最灵活的方法,但给产品供应商带来了最大的负担。

2. **在特定硬件平台上认证 Zephyr,而不考虑特定应用程序 (Certification of Zephyr on specific hardware platform without a
   specific application in mind):** 此场景描述了运行 Zephyr RTOS 的安全平台的启用。硬件制造商在对应用程序的定义假设下认证平台。如果满足这些假设,则可以轻松认证最终产品。

3. **实际产品的认证 (Certification of an actual product):** 在这种情况下,包括特定硬件、Zephyr RTOS 和应用程序在内的完整产品将获得认证。

在所有三种情况下,都需要确定认证方案(例如,FIPS 140-2 [NIST02]_ 或通用标准 [CCITSE12]_)、认证范围(主流 Zephyr、安全分支或某些模块)以及认证/保证级别 (In all three cases, the certification scheme (e.g., FIPS 140-2 [NIST02]_
or Common Criteria [CCITSE12]_), the scope of the certification
(main-stream Zephyr, security branch, or certain modules), and the
certification/assurance level need to be determined)。

在部分认证的情况下(选项 1 和 2),需要对硬件和/或软件进行认证假设。这些假设可以包括 [GHS10]_ (In case of partial certifications (options 1 and 2), assumptions on
hardware and/or software are required for certifications. These can
include [GHS10]_)

-  硬件平台及其环境的**适当物理安全 (Appropriate physical security)**。

-  硬件平台本身和所有连接设备的**存储和时序通道的充分保护 (Sufficient protection of storage and timing channels)**。(未提及远程连接。)

-  设备上仅运行**可信/有保证的应用程序 (trusted/assured applications)**

-  设备及其软件栈由经过**适当培训的可信人员 (properly trained and trusted individuals)** 配置和操作,且无恶意意图。

这些假设应是安全声明和评估的一部分 (These assumptions shall be part of the security claim and evaluation)
target documents.
