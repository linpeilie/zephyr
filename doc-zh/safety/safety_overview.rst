.. _safety_overview:.. _safety_overview:



Zephyr 安全概述 (Zephyr Safety Overview)Zephyr 安全概述 (Zephyr Safety Overview)

##################################################################################



简介 (Introduction)简介 (Introduction)

****************************************



本文档是安全文档,提供了与安全相关的活动概述,以及 Zephyr 项目和 Zephyr 安全工作组/委员会试图实现的目标。本文档是安全文档,提供了与安全相关的活动概述,以及 Zephyr 项目和 Zephyr 安全工作组/委员会试图实现的目标。



本概述适用于对 Zephyr RTOS 功能安全开发部分感兴趣的人员,以及希望为项目的安全方面做出贡献的项目成员。本概述适用于对 Zephyr RTOS 功能安全开发部分感兴趣的人员,以及希望为项目的安全方面做出贡献的项目成员。



概述 (Overview)概述 (Overview)

********************************



在本节中,我们向读者概述了安全认证的总体目标是什么,我们旨在实现什么标准,以及需要实施哪些质量标准和流程才能达到此类安全认证。在本节中,我们向读者概述了安全认证的总体目标是什么,我们旨在实现什么标准,以及需要实施哪些质量标准和流程才能达到此类安全认证。



安全文档更新 (Safety Document update)安全文档更新 (Safety Document update)

******************************************************************************



本文档是一个不断更新的文档,随着新要求、指南或流程的引入,可能会随时间演变。本文档是一个不断更新的文档,随着新要求、指南或流程的引入,可能会随时间演变。



#. 相关方将通过拉取请求向 Zephyr 文档仓库提交更改。#. 相关方将通过拉取请求向 Zephyr 文档仓库提交更改。



#. Zephyr 安全委员会将审查这些更改并提供反馈或接受这些更改。#. Zephyr 安全委员会将审查这些更改并提供反馈或接受这些更改。



#. 一旦接受,这些更改将成为文档的一部分。#. 一旦接受,这些更改将成为文档的一部分。



总体安全范围 (General safety scope)总体安全范围 (General safety scope)

************************************************************************



安全委员会的总体范围是为有限的源代码范围(参见待定的认证范围)实现 `IEC 61508安全委员会的总体范围是为有限的源代码范围(参见待定的认证范围)实现 `IEC 61508

<https://en.wikipedia.org/wiki/IEC_61508>`__ 标准和安全完整性等级 (SIL) 3 /<https://en.wikipedia.org/wiki/IEC_61508>`__ 标准和安全完整性等级 (SIL) 3 /

系统能力 (SC) 3 的认证。由于代码库是预先存在的,我们使用 IEC 61508 标准定义的 3s/1s 路线方法。系统能力 (SC) 3 的认证。由于代码库是预先存在的,我们使用 IEC 61508 标准定义的 3s/1s 路线方法。



路线 3s (Route 3s)路线 3s (Route 3s)

   *评估不合规开发。基本上是带有现有源代码的路线 1s。*   *评估不合规开发。基本上是带有现有源代码的路线 1s。*



路线 1s (Route 1s)路线 1s (Route 1s)

      *合规开发。遵守本标准关于避免和控制软件系统性故障的要求。*      *合规开发。遵守本标准关于避免和控制软件系统性故障的要求。*



IEC 61508 标准总结 (Summarization IEC 61508 standard)IEC 61508 标准总结 (Summarization IEC 61508 standard)

============================================================================================================



IEC 61508 标准是一个广泛认可的国际标准,用于电气、电子和可编程电子安全相关系统的功能安全。以下是该标准的一些关键安全方面的概述:IEC 61508 标准是一个广泛认可的国际标准,用于电气、电子和可编程电子安全相关系统的功能安全。以下是该标准的一些关键安全方面的概述:



#. **危害和风险分析 (Hazard and Risk Analysis)**: IEC 61508 标准要求对与系统相关的潜在危害和风险进行全面分析,以确定将这些风险降低到可接受水平所需的适当安全措施级别。#. **危害和风险分析 (Hazard and Risk Analysis)**: IEC 61508 标准要求对与系统相关的潜在危害和风险进行全面分析,以确定将这些风险降低到可接受水平所需的适当安全措施级别。



#. **安全完整性等级 (SIL - Safety Integrity Level)**: 该标准引入了安全完整性等级 (SIL) 的概念,以分类每个安全功能所需的风险降低级别。SIL 越高,所需的风险降低级别越大。#. **安全完整性等级 (SIL - Safety Integrity Level)**: 该标准引入了安全完整性等级 (SIL) 的概念,以分类每个安全功能所需的风险降低级别。SIL 越高,所需的风险降低级别越大。



#. **系统设计 (System Design)**: IEC 61508 标准要求采用系统的方法进行系统设计,包括识别安全要求、制定安全计划以及使用适当的安全技术和措施来确保系统满足所需的 SIL。#. **系统设计 (System Design)**: IEC 61508 标准要求采用系统的方法进行系统设计,包括识别安全要求、制定安全计划以及使用适当的安全技术和措施来确保系统满足所需的 SIL。



#. **验证和确认 (Verification and Validation)**: 该标准要求对安全相关系统进行严格的测试和评估,以确保其满足指定的 SIL 和其他安全要求。这包括验证系统设计、确认系统功能以及对系统进行持续监控和维护。#. **验证和确认 (Verification and Validation)**: 该标准要求对安全相关系统进行严格的测试和评估,以确保其满足指定的 SIL 和其他安全要求。这包括验证系统设计、确认系统功能以及对系统进行持续监控和维护。



#. **文档和可追溯性 (Documentation and Traceability)**: IEC 61508 标准要求全面的文档流程,以确保安全相关系统的所有方面都得到充分记录,并且从安全要求到最终系统设计和实施都有完全的可追溯性。#. **文档和可追溯性 (Documentation and Traceability)**: IEC 61508 标准要求全面的文档流程,以确保安全相关系统的所有方面都得到充分记录,并且从安全要求到最终系统设计和实施都有完全的可追溯性。



总体而言,IEC 61508 标准为安全相关系统的设计、开发和实施提供了一个框架,旨在降低事故风险并提高整体安全性。通过遵循该标准,组织可以确保其安全相关系统的设计和实施达到最高级别的安全完整性。总体而言,IEC 61508 标准为安全相关系统的设计、开发和实施提供了一个框架,旨在降低事故风险并提高整体安全性。通过遵循该标准,组织可以确保其安全相关系统的设计和实施达到最高级别的安全完整性。



为什么选择 IEC 61508? (Why IEC 61508?)为什么选择 IEC 61508? (Why IEC 61508?)

================================================================================

选择 IEC 61508 标准是因为它作为适用于各个行业领域的基础功能安全标准。它提供了一个强大的框架,可以用作不同行业特定标准的基础。这使得 IEC 61508 对 Zephyr 特别相关,因为该操作系统的多功能性使其能够在广泛的行业领域中有效使用。选择 IEC 61508 标准是因为它作为适用于各个行业领域的基础功能安全标准。它提供了一个强大的框架,可以用作不同行业特定标准的基础。这使得 IEC 61508 对 Zephyr 特别相关,因为该操作系统的多功能性使其能够在广泛的行业领域中有效使用。



以下图表说明了 IEC 61508 标准与其他相关标准之间的关系:以下图表说明了 IEC 61508 标准与其他相关标准之间的关系:



.. figure:: images/IEC-61508-basis.svg.. figure:: images/IEC-61508-basis.svg

   :align: center   :align: center

   :alt: IEC 61508 与其他标准的关系   :alt: IEC 61508 与其他标准的关系

   :figclass: align-center   :figclass: align-center



   IEC 61508 与其他标准的关系   IEC 61508 与其他标准的关系



质量 (Quality)质量 (Quality)

**************

Summarization IEC 61508 standard

质量是整个行业对软件的强制性期望。项目的代码库必须达到各种软件质量目标,才能从安全角度被视为可审计的代码库,并可用于认证目的。但软件质量并不是功能安全标准引起的额外要求。功能安全将质量视为现有的前提条件,因此无论功能安全目标如何,任何项目都应追求"质量管理"状态。以下列表描述了实现可审计代码库需要达到的质量目标:================================



1. 基本软件质量标准 (Basic software quality standards)The IEC 61508 standard is a widely recognized international standard for functional safety of

electrical, electronic, and programmable electronic safety-related systems. Here's an overview of

   a. :ref:`coding_guidelines` (包括:静态代码分析、编码风格等)some of the key safety aspects of the standard:

   b. :ref:`safety_requirements` 和需求追踪

   c. 测试覆盖率#. **Hazard and Risk Analysis**: The IEC 61508 standard requires a thorough analysis of potential

   hazards and risks associated with a system in order to determine the appropriate level of safety

2. 软件架构设计原则 (Software architecture design principles)   measures needed to reduce those risks to acceptable levels.



   a. 分层架构模型#. **Safety Integrity Level (SIL)**: The standard introduces the concept of Safety Integrity Level

   b. 封装组件   (SIL) to classify the level of risk reduction required for each safety function. The higher the

   c. 封装单一功能(如果在安全方面不适合和可管理)   SIL, the greater the level of risk reduction required.



基本软件质量标准 - 安全视角 (Basic software quality standards - Safety view)#. **System Design**: The IEC 61508 standard requires a systematic approach to system design that

==============================================================================   includes the identification of safety requirements, the development of a safety plan, and the

   use of appropriate safety techniques and measures to ensure that the system meets the required

在本章中,安全委员会描述了为什么需要上述质量目标作为前提条件,以及从安全角度需要做什么来实现可审计的代码库。一般来说,可以说所有这些关于安全的质量措施都用于最小化代码开发过程中的错误率。   SIL.



编码指南 (Coding Guidelines)#. **Verification and Validation**: The standard requires rigorous testing and evaluation of the

-----------------------------   safety-related system to ensure that it meets the specified SIL and other safety requirements.

   This includes verification of the system design, validation of the system's functionality, and

编码指南是对工业软件产品的共同理解、统一规则集和开发风格的基础。对于安全来说,编码指南是必不可少的,除了统一规则集的事实之外,还有另一个目的。还有必要证明开发人员遵循统一的开发风格,以防止软件开发过程中的**系统性错误**,从而最小化整个软件系统的整体**错误率**。   ongoing monitoring and maintenance of the system.



此外,**IEC 61508 标准**设定了使用编码标准/指南以降低错误可能性的前提条件和建议。#. **Documentation and Traceability**: The IEC 61508 standard requires a comprehensive

   documentation process to ensure that all aspects of the safety-related system are fully

项目 TSC 和项目安全委员会同意实施分阶段和增量方法来遵守一套编码规则(即编码指南),以提高代码库的质量和一致性。以下是商定的阶段:   documented and that there is full traceability from the safety requirements to the final system

   design and implementation.

阶段 I (已完成 - COMPLETED)

  编码指南规则可供遵循和参考,但不强制执行。规则尚未在 CI 中强制执行,审查者/批准者不能因违规而阻止拉取请求。Overall, the IEC 61508 standard provides a framework for the design, development, and

implementation of safety-related systems that aims to reduce the risk of accidents and improve

阶段 IIoverall safety. By following the standard, organizations can ensure that their safety-related

  审查者/批准者可以因在整个代码库的拉取请求中违反编码指南而阻止拉取请求。systems are designed and implemented to the highest level of safety integrity.



  开始在代码库的有限范围内强制执行。最初,这将是安全认证范围。对于易于在整个代码库中应用的规则,我们不应将合规性限制在初始范围内。此步骤需要工具、CI 设置和强制执行策略。Why IEC 61508?

==============

阶段 IIIThe IEC 61508 standard was selected because it serves as a foundational functional safety standard

  重新审视编码指南规则,并根据前几个阶段的经验,对选定的规则进行改进/迭代。applicable across various industry sectors. It provides a robust framework that can be used as

base for specific standards for different industries. This makes IEC 61508 particularly relevant

阶段 IVfor Zephyr, as the operating system's versatility allows it to be effectively utilized across a

   将强制执行扩展到更广泛的代码库。对于代码库的某些区域,如果有适当的理由,可以授予例外。例外需要 TSC 批准。wide range of industry sectors.



.. note::The following diagram illustrates the relationship between the IEC 61508 standard and other related

standards:

    编码指南规则可以通过提交 GH issue/RFC 随时删除/更改。

.. figure:: images/IEC-61508-basis.svg

.. important::   :align: center

   :alt: IEC 61508 relation to other standards

    **当前阶段:**   :figclass: align-center

    完成**阶段 II** 的先决条件目前正在研究中:

    工具正在评估中,CI 设置和`强制执行策略   IEC 61508 relation to other standards

    <https://github.com/zephyrproject-rtos/zephyr/issues/58903>`__正在制定中。

质量 (Quality)

需求和需求追踪 (Requirements and requirements tracing)*******

-------------------------------------------------------

质量是整个行业对软件的强制性期望。项目的代码库必须达到各种软件质量目标,才能从安全角度被视为可审计的代码库,并可用于认证目的。但软件质量并不是功能安全标准引起的额外要求。功能安全将质量视为现有的前提条件,因此无论功能安全目标如何,任何项目都应追求"质量管理"状态。以下列表描述了实现可审计代码库需要达到的质量目标:

需求和需求管理不仅对软件开发很重要,而且在安全方面也非常重要。一方面,这在技术层面上详细指定和描述了软件应该做什么,另一方面,它是一个重要且必要的工具,用于验证所描述的功能是否按预期实现。为此,使用将需求追溯到代码级别的方法。有了需求管理和追踪,现在可以验证功能是否已正确测试和实施,从而最小化系统性错误率。

1. 基本软件质量标准 (Basic software quality standards)

此外,IEC 61508 标准强烈建议(这对认证来说几乎是必须的)需求和需求追踪。

   a. :ref:`coding_guidelines` (包括:静态代码分析、编码风格等)

测试覆盖率 (Test coverage)   b. :ref:`safety_requirements` 和需求追踪

---------------------------   c. 测试覆盖率



高测试覆盖率反过来是安全的证据,表明代码精确符合其开发目的,不会执行任何不可预见的指令。如果整个代码都经过测试并具有高(理想情况下为 100%)测试覆盖率,则具有快速检测错误更改并进一步最小化错误率的额外优势。但是,必须注意的是,测试覆盖率的安全要求有所不同,必须考虑各种指标,这些指标由 IEC 61508 标准针对 SIL 3 / SC3 目标规定。除其他外,必须满足以下要求:2. 软件架构设计原则 (Software architecture design principles)



* 结构测试覆盖率(入口点)100%   a. 分层架构模型

* 结构测试覆盖率(语句)100%   b. 封装组件

* 结构测试覆盖率(分支)100%   c. 封装单一功能(如果在安全方面不适合和可管理)



如果无法达到 100%(例如防御性代码的语句覆盖率),则需要在文档中描述和说明该部分。基本软件质量标准 - 安全视角 (Basic software quality standards - Safety view)

==============================================================================

软件架构设计原则 (Software architecture design principles)

===========================================================在本章中,安全委员会描述了为什么需要上述质量目标作为前提条件,以及从安全角度需要做什么来实现可审计的代码库。一般来说,可以说所有这些关于安全的质量措施都用于最小化代码开发过程中的错误率。



要创建和维护结构化的软件产品,还需要考虑各个软件架构设计并根据安全标准实施它们,因为某些设计和实施在安全方面不合理,从而使整体软件和代码库可以用作可审计代码。但是,这些软件架构设计中的大多数已经在 Zephyr 项目中实施,需要由安全委员会/安全工作组和安全架构师进行验证。编码指南 (Coding Guidelines)

-----------------------------

分层架构模型 (Layered architecture model)

------------------------------------------编码指南是对工业软件产品的共同理解、统一规则集和开发风格的基础。对于安全来说,编码指南是必不可少的,除了统一规则集的事实之外,还有另一个目的。还有必要证明开发人员遵循统一的开发风格,以防止软件开发过程中的**系统性错误**,从而最小化整个软件系统的整体**错误率**。



**IEC 61508 标准**强烈建议对软件架构采用模块化方法。从一开始,Zephyr 项目就通过其分层架构追求这种方法。此架构背后的想法是将具有类似功能的模块或组件组织成层。因此,可以为每一层分配系统中的特定角色。该模型在安全方面的优势在于,可以在非常高的层次上显示不同组件和层之间的接口,从而可以确定哪些功能与安全相关并可以限制。此外,可以在此架构之上构建各种分析和文档,这对于认证和负责的认证机构很重要。此外,**IEC 61508 标准**设定了使用编码标准/指南以降低错误可能性的前提条件和建议。



封装组件 (Encapsulated components)项目 TSC 和项目安全委员会同意实施分阶段和增量方法来遵守一套编码规则(即编码指南),以提高代码库的质量和一致性。以下是商定的阶段:

-----------------------------------

阶段 I (已完成 - COMPLETED)

封装组件是此时安全架构设计的重要组成部分。最重要的方面是将安全相关组件与非安全相关组件分离,包括它们的相关接口。这确保了组件对其他组件没有**影响**。  编码指南规则可供遵循和参考,但不强制执行。规则尚未在 CI 中强制执行,审查者/批准者不能因违规而阻止拉取请求。



封装单一功能(如果在安全性方面不合理且不可管理)阶段 II

(Encapsulated single functionality (if not reasonable and manageable in safety))  审查者/批准者可以因在整个代码库的拉取请求中违反编码指南而阻止拉取请求。

--------------------------------------------------------------------------------

  开始在代码库的有限范围内强制执行。最初,这将是安全认证范围。对于易于在整个代码库中应用的规则,我们不应将合规性限制在初始范围内。此步骤需要工具、CI 设置和强制执行策略。

对整个系统和软件环境的另一个要求是可以在组件内禁用单个功能。这是因为如果某个功能对于安全来说绝对不可接受(例如完全动态内存管理),那么这些单个功能应该能够被关闭。Zephyr 项目已经通过使用 Kconfig 及其灵活的可配置性提供了这样的可能性。

阶段 III

流程和工作流 (Processes and workflow)  重新审视编码指南规则,并根据前几个阶段的经验,对选定的规则进行改进/迭代。

************************************

阶段 IV

.. figure:: images/zephyr-safety-process.svg   将强制执行扩展到更广泛的代码库。对于代码库的某些区域,如果有适当的理由,可以授予例外。例外需要 TSC 批准。

   :align: center

   :alt: Safety process and workflow overview.. note::

   :figclass: align-center

    编码指南规则可以通过提交 GH issue/RFC 随时删除/更改。

   安全流程和工作流概述 (Safety process and workflow overview)

.. important::

该图描述了安全委员会定义的粗略流程,以确保 Zephyr 项目开发中的安全性。为了确保理解,需要强调几点并解释一些细节,涉及安全架构师的角色以及安全委员会在整个流程中的作用。该图仅描述了当更改与安全相关时可能的路径。

    **当前阶段:**

#. 在主分支上,应该识别项目的安全范围,通常代表整个代码库的一小部分子集。然后,在"main"上进行正常开发期间,应使该子集可审计,这意味着在此范围内特别注意质量目标(`Quality`_)和安全流程。安全架构师与技术指导委员会(TSC)在该领域并肩工作,监控开发流程以确保架构满足安全要求。    完成**阶段 II** 的先决条件目前正在研究中:

    工具正在评估中,CI 设置和`强制执行策略

#. 在这一点上,安全架构师发挥着越来越重要的作用。对于属于安全范围的 PR/问题,安全架构师理想情况下应该参与安全范围内小幅更改的讨论和决策,以便能够对不符合要求的安全相关更改做出反应。如果拉取请求或问题引入了需要扩展讨论或决策的重大且有影响力的更改或改进,安全架构师应酌情将其提请安全委员会或技术指导委员会(TSC)注意,以便他们就最佳行动方案做出决定。    <https://github.com/zephyrproject-rtos/zephyr/issues/58903>`__正在制定中。



#. 本节描述认证方面。此时,代码库必须处于"可审计"状态,理想情况下不应对代码库进行进一步更改或不应进行更改。从主分支到该区域仍然有一条路径。这是必需的,以防在创建 LTS 和可审计分支之后,在主分支的安全范围内发现或实施严重错误或重要更改。在这种情况下,安全委员会与安全架构师必须一起决定是否应将此错误修复或更改集成到 LTS 中,以便错误修复或更改也可以集成到可审计分支中。这种集成可以采取三种形式:第一,仅作为代码更改;第二,仅作为安全文档更新;第三,两者兼有。需求和需求追踪 (Requirements and requirements tracing)

-------------------------------------------------------

#. 这描述了认证本身所需的必要安全流程。在这里,创建并进行最终分析、测试和文档,这些必须在认证期间创建和进行,并由认证机构和正在认证的标准规定。如果认证机构在此阶段批准所有内容并且安全流程完成,则可以创建并发布安全版本。

需求和需求管理不仅对软件开发很重要,而且在安全方面也非常重要。一方面,这在技术层面上详细指定和描述了软件应该做什么,另一方面,它是一个重要且必要的工具,用于验证所描述的功能是否按预期实现。为此,使用将需求追溯到代码级别的方法。有了需求管理和追踪,现在可以验证功能是否已正确测试和实施,从而最小化系统性错误率。

#. 从可审计分支到主分支的过渡应仅在特殊情况下发生,特别是当在认证过程中发现某些内容需要在"可审计"分支上快速调整以获得认证时。为了防止在下次认证期间再次出现此问题,需要有一条路径将这些更改合并回主分支,以免丢失,并在必要时为下次认证做好准备。

此外,IEC 61508 标准强烈建议(这对认证来说几乎是必须的)需求和需求追踪。

.. important::

   安全不应阻止项目,也不应以任何方式最小化成长空间。测试覆盖率 (Test coverage)

---------------------------

.. important::

   **TODO:** 寻找并定义对维护者、审查者和贡献者以及安全架构师本身的日常工作影响最小的方法、指南和流程。但这些方法也适用于安全。高测试覆盖率反过来是安全的证据,表明代码精确符合其开发目的,不会执行任何不可预见的指令。如果整个代码都经过测试并具有高(理想情况下为 100%)测试覆盖率,则具有快速检测错误更改并进一步最小化错误率的额外优势。但是,必须注意的是,测试覆盖率的安全要求有所不同,必须考虑各种指标,这些指标由 IEC 61508 标准针对 SIL 3 / SC3 目标规定。除其他外,必须满足以下要求:


* 结构测试覆盖率(入口点)100%
* 结构测试覆盖率(语句)100%
* 结构测试覆盖率(分支)100%

如果无法达到 100%(例如防御性代码的语句覆盖率),则需要在文档中描述和说明该部分。

软件架构设计原则 (Software architecture design principles)
===========================================================

要创建和维护结构化的软件产品,还需要考虑各个软件架构设计并根据安全标准实施它们,因为某些设计和实施在安全方面不合理,从而使整体软件和代码库可以用作可审计代码。但是,这些软件架构设计中的大多数已经在 Zephyr 项目中实施,需要由安全委员会/安全工作组和安全架构师进行验证。

分层架构模型 (Layered architecture model)
------------------------------------------

**IEC 61508 标准**强烈建议对软件架构采用模块化方法。从一开始,Zephyr 项目就通过其分层架构追求这种方法。此架构背后的想法是将具有类似功能的模块或组件组织成层。因此,可以为每一层分配系统中的特定角色。该模型在安全方面的优势在于,可以在非常高的层次上显示不同组件和层之间的接口,从而可以确定哪些功能与安全相关并可以限制。此外,可以在此架构之上构建各种分析和文档,这对于认证和负责的认证机构很重要。

封装组件 (Encapsulated components)
-----------------------

封装组件是此时安全架构设计的重要组成部分。最重要的方面是将安全相关组件与非安全相关组件分离,包括它们的相关接口。这确保了组件对其他组件没有**影响**。

封装单一功能(如果在安全性方面不合理且不可管理)
(Encapsulated single functionality (if not reasonable and manageable in safety))
--------------------------------------------------------------------------------

对整个系统和软件环境的另一个要求是可以在组件内禁用单个功能。这是因为如果某个功能对于安全来说绝对不可接受(例如完全动态内存管理),那么这些单个功能应该能够被关闭。Zephyr 项目已经通过使用 Kconfig 及其灵活的可配置性提供了这样的可能性。

Processes and workflow
**********************

.. figure:: images/zephyr-safety-process.svg
   :align: center
   :alt: Safety process and workflow overview
   :figclass: align-center

   Safety process and workflow overview

The diagram describes the rough process defined by the Safety Committee to ensure safety in the
development of the Zephyr project. To ensure understanding, a few points need to be highlighted and
some details explained regarding the role of the safety architect and the role of the safety
committee in the whole process. The diagram only describes the paths that are possible when a
change is related to safety.

#. On the main branch, the safety scope of the project should be identified, which typically
   represents a small subset of the entire code base. This subset should then be made auditable
   during normal development on “main”, which means that special attention is paid to quality goals
   (`Quality`_) and safety processes within this scope. The Safety Architect works alongside the
   Technical Steering Committee (TSC) in this area, monitoring the development process to ensure
   that the architecture meets the safety requirements.

#. At this point, the safety architect plays an increasingly important role. For PRs/issues that
   fall within the safety scope, the safety architect should ideally be involved in the discussions
   and decisions of minor changes in the safety scope to be able to react to safety-relevant
   changes that are not conformant. If a pull request or issue introduces a significant and
   influential change or improvement that requires extended discussion or decision-making, the
   safety architect should bring it to the attention of the Safety Committee or the Technical
   Steering Committee (TSC) as appropriate, so that they can make a decision on the best course of
   action.

#. This section describes the certification side. At this point, the code base has to be in an
   "auditable" state, and ideally no further changes should be necessary or made to the code base.
   There is still a path from the main branch to this area. This is needed in case a serious bug or
   important change is found or implemented on the main branch in the safety scope, after the LTS
   and the auditable branch were created. In this case, the Safety Committee, together with the
   safety architect, must decide whether this bug fix or change should be integrated into the LTS
   so that the bug fix or change could also be integrated into the auditable branch. This
   integration can take three forms: First either as only a code change or second as only an update
   to the safety documentation or third as both.

#. This describes the necessary safety process required for certification itself. Here, the final
   analyses, tests, and documents are created and conducted which must be created and conducted
   during the certification, and which are prescribed by the certifying authority and the standard
   being certified. If the certification body approves everything at this stage and the safety
   process is completed, a safety release can be created and published.

#. This transition from the auditable branch to the main branch should only occur in exceptional
   circumstances, specifically when something has been identified during the certification process
   that needs to be quickly adapted on the “auditable” branch in order to obtain certification. In
   order to prevent this issue from arising again during the next certification, there needs to be
   a path to merge these changes back into the main branch so that they are not lost, and to have
   them ready for the next certification if necessary.

.. important::
   Safety should not block the project and minimize the room to grow in any way.

.. important::
   **TODO:** Find and define ways, guidelines and processes which minimally impact the daily work
   of the maintainers, reviewers and contributors and also the safety architect itself.
   But which are also suitable for safety.
