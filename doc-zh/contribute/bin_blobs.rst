.. _bin-blobs:

二进制 Blobs（Binary Blobs）
###########################

在支持多种架构和众多不同 IC 系列的操作系统语境下，如果没有以二进制形式分发的可执行代码的帮助，某些功能可能无法实现。二进制 blob（Binary blob，简称 blob）是包含专有机器代码或二进制格式数据的文件，例如没有在 OSI 批准的许可证（Open Source Initiative approved license）下发布相应源代码的情形。

Zephyr 通过其内置机制支持下载并使用第三方二进制 blobs，但需要注意一些重要的限定，详见下文各节。需要特别说明的是，本节中的所有信息仅适用于 `上游（vanilla）Zephyr <https://github.com/zephyrproject-rtos/zephyr>`_。

对于 Zephyr 的分支（fork）或第三方发行版，在支持二进制 blobs 方面没有任何限制（或许仅需考虑许可证兼容性）。事实上，Zephyr 的构建系统支持与 blobs 相关的各种用例，包括与库进行链接、将镜像烧录到目标设备等。因此，如果无法满足本页描述的要求，用户可以自由创建基于 Zephyr 的下游软件来使用二进制 blobs。

软件许可证（Software license）
****************************

大多数二进制 blobs 都在专有许可证（proprietary licenses）下分发，其性质和条件差异很大。由供应商在提交 blob 的流程中明确其许可证。用户在获取并安装 blobs 时，供应商可能会要求点击确认（click-through）或其他类似于 EULA（终端用户许可协议，End-User License Agreement）的流程。

托管（Hosting）
**************

Blobs 必须托管在互联网上，并由第三方基础设施进行管理。两个可能的例子是由硬件供应商管理的 Git 仓库和 Web 服务器。

Zephyr 项目不会在其 Git 仓库或任何其他地方托管二进制 blobs。

获取 blobs（Fetching blobs）
***************************

Blobs 通过 :ref:`west blobs <west-blobs>` 命令从官方第三方来源获取。

Blobs 本身必须在独立的 Zephyr :ref:`模块仓库 <modules>`（module repositories）中的 :ref:`module.yml <modules-bin-blobs>` 文件里进行声明，该仓库由各自的供应商维护。这意味着要在上游 Zephyr 发行版中加入对某个二进制 blob 的引用，必须先存在一个模块仓库，或在提交流程中创建该仓库。

每个可被获取的 blob 都必须在相应的 :file:`module.yml` 文件中单独标识。一个 blob 的规范应包含：

- 对 blob 本身的抽象性描述
- 版本信息（version information）
- 指向供应商提供文档的引用
- blob 的 :ref:`类型 <bin-blobs-types>`，且必须属于允许的类型之一
- blob 的校验和（checksum），``west blobs`` 在下载后会进行检查。这对于可重现性（reproducibility）以及在 blobs 发生变化时配合 Git 与 west 进行问题二分（bisect）是必要的
- 适用于该 blob 的许可证文本或其引用，采用 SPDX 格式（SPDX format）

更正式的字段定义见 :ref:`对应小节 <modules-bin-blobs>`。

可以使用 :ref:`west blobs <west-blobs>` 命令列出可用 blobs 的元数据，并从用户选择的模块中获取 blobs。

``west blobs`` 命令只获取并存储二进制 blobs 本体。任何随附代码（包括 blob 的接口头文件）都必须存在于对应的模块仓库中。

污染（Tainting）
****************

包含二进制 blobs 会使 Zephyr 构建被标记为“污染”（tainted）。“污染”的定义源自 `Linux 内核 <https://www.kernel.org/doc/html/latest/admin-guide/tainted-kernels.html>`_。在 Zephyr 语境中，包含二进制 blobs 的镜像将被视为已污染（tainted image）。

污染状态会通过以下方式告知用户：

- 一个或多个 Kconfig 选项 ``TAINT_BLOBS_*`` 会被设置为 ``y``
- Zephyr 构建系统在配置阶段会发出警告，可通过 Kconfig 禁用该警告
- ``west spdx`` 命令的输出会包含污染状态
- 内核默认的致命错误处理程序会显式打印内核的污染状态
- 启动横幅（boot banner）会打印内核的污染状态

.. _bin-blobs-types:

允许的类型（Allowed types）
***************************

以下类型的二进制 blob 在 Zephyr 中是可接受的：

* 预编译库（Precompiled libraries）：用于硬件使能（hardware enablement）的库，以预编译的二进制形式分发，通常用于 SoC 外设。例如某无线外设的使能库。
* 固件镜像（Firmware images）：包含次级处理器或 CPU 可执行代码的镜像。可以是完整或部分（通常为增量或补丁数据），通常由主 CPU 复制到 RAM 或闪存中。例如运行蓝牙 LE 控制器（Bluetooth LE Controller）的核心固件。
* 其他各类二进制数据文件（Miscellaneous binary data files）。例如预训练的神经网络模型数据。

通过专有库提供的与硬件无关（hardware agnostic）的特性不可接受。例如，以静态归档（static archive）分发的专有且与硬件无关的 TCP/IP 协议栈会被拒绝。

请注意，某个 blob 具有可接受的类型并不意味着它会被项目无条件接纳；任何 blob 都可能因其他原因被逐案否决（详见下文“预编译库特定要求”）。若发生分歧，TSC（Technical Steering Committee，技术指导委员会）将裁定某个 blob 是否属于上述类型之一。

预编译库特定要求（Precompiled library-specific requirements）
************************************************************

本节包含针对预编译库 blobs 的附加要求。

任何希望提交预编译库的人都必须声明其满足这些要求。如果后来发现该 blob 未能满足这些要求，项目可能会将其从上游发行版中移除。

接口头文件（Interface header files）
==================================

预编译库必须附带一个或多个头文件，这些头文件应在非共置版权（non-copyleft）且经 OSI 批准的许可证下分发，并用于定义该库的接口。

允许的依赖（Allowed dependencies）
================================

本节定义与库 blob 需要由构建系统提供的外部符号相关的要求。

* 该 blob 不得直接依赖 Zephyr 的 API。换言之，必须在完全没有任何 Zephyr 源代码的情况下也能构建出该二进制。这是为了解耦与可维护性，因为 Zephyr 的 API 可能变化，而此类 blobs 并非所有项目维护者都能修改。
* 如果预编译库中的代码需要 Zephyr（或一般 RTOS）提供的功能，可以在库旁提供一个操作系统抽象层（OS abstraction layer，又称移植层 porting layer）的实现。该抽象层的实现必须以源代码形式发布，采用 OSI 批准的许可证，并使用 Doxygen 进行文档化。

工具链要求（Toolchain requirements）
===================================

预编译库 blobs 必须采用与 Zephyr 项目所支持工具链兼容且可被其链接的数据格式。这对于可维护性和可用性是必要的。不过，使用此类库可能需要特殊的编译器和/或链接器选项。例如，某个移植层可能需要特殊编译参数，或者某个静态归档可能需要特定的链接器选项。

范围限制（Limited scope）
========================

允许任意库 blob 会带来降低上游 Zephyr 软件发行版开源程度的风险。极端情况下，如果某目标平台的 Zephyr 内核时钟驱动只是一个围绕库 blob 的移植层，那么用开源软件将无法引导（boot）该目标。

为降低此风险，上游库 blob 的适用范围被限制。项目维护者定义了一套开源测试套件（open source test suite），上游目标必须仅使用主线发行版及其模块中包含的开源软件即可通过该测试。目前该测试套件包括：

- :file:`samples/philosophers`
- :file:`tests/kernel`

该测试套件的范围可能会随时间扩展。目标是规定一组最小特性的测试，这些特性对于任何具有上游 Zephyr 支持的目标，都必须能够通过开源软件来实现。

在发布团队（release team）酌情决定下，如果某硬件目标无法通过该测试套件，项目可移除其支持。

支持与维护（Support and maintenance）
************************************

Zephyr 项目不负责对贡献的二进制 blobs 进行维护与支持。因此，由 Zephyr 项目发布团队酌情决定，并视情况逐案处理：

- 在 Zephyr 仓库跟踪器（repository tracker）上报告、且复现问题需要使用 blobs 的 GitHub issue，可能不会被视为 Zephyr 的缺陷（bug）
- 此类问题可能会被关闭，理由为超出 Zephyr 项目范围

这并不意味着需要 blobs 才能复现的问题会在未调查的情况下被关闭。例如，该问题可能暴露了 Zephyr 某条代码路径中的缺陷，而不借助 blob 则难以或无法触发。项目维护者可能会接受并尝试解决此类问题。

然而，需要保留一定的灵活性，因为项目维护者可能无法判断某个问题究竟是 Zephyr 的缺陷还是 blob 本身的问题，也可能因为缺乏硬件而无法复现该缺陷等。

Blobs 必须有指定的维护者（maintainers），他们需要对用户报告的问题保持响应，并提供更新以解决问题。由 Zephyr 项目发布团队酌情决定，任何引用 blobs 的模块修订版本，都可能因维护者缺乏响应或支持而随时从 :file:`zephyr/west.yml` 中移除。这对于控制项目中的腐化（bit-rot）、安全问题等是必要的。

提交集成二进制 blob 的提案者必须承诺在可预见的未来维护此类 blob 的集成。

关于持续集成（Continuous Integration，CI），为了避免回归和问题进入代码库，项目的 CI 基础设施在构建并（可选）运行测试与示例时，**不会** 获取二进制 blobs。这包括新建 GitHub Pull Request 时运行的 CI 以及其他任何定期执行的 CI。

.. _blobs-process:

提交流程与评审（Submission and review process）
*********************************************

若要在项目中包含对二进制 blobs 的引用，应通过标准的 Pull Request（PR，拉取请求）流程提交，且不需要 TSC（Technical Steering Committee，技术指导委员会）批准。维护者（maintainers）和评审者（reviewers）有责任确保所有与 blob 相关的提交符合 :ref:`bin-blobs` 中定义的标准。

用于首次集成二进制 blobs 的 PR 应包含关于这些 blobs 及其所提供功能的细节。该 PR 应包含以下信息以支持评审：

* 二进制 blob 的来源（origin）
* blob 的类型（预编译库、固件镜像）
* 将引用该 blob 的 Zephyr 模块
* 对 blob 的功能做简要说明
* blob 还依赖哪些其他组件（若有）？
* blob 分发所采用的许可证

如果首次集成的 PR 获得相应批准，则可以集成该二进制 blob（或多个）。对于任何技术分歧，适用标准的 :ref:`PR 升级处理流程 <pr_technical_escalation>`。

后续对二进制 blobs 的更新遵循 :ref:`模块更新流程 <modules_changes>`。
