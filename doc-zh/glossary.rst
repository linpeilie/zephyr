:orphan:

.. _glossary:

术语表 (Glossary of Terms)
###########################

.. glossary::
   :sorted:

   API
      (Application Program Interface - 应用程序接口) 用于构建应用软件的一组定义的例程和协议。

   application
      应用程序 (application) - Zephyr 构建系统用于为指定的开发板配置构建应用镜像的用户提供的文件集。
      它可以包含应用程序特定的代码、内核配置设置，以及至少一个 CMakeLists.txt 文件。
      应用程序的内核配置设置指导构建系统创建一个自定义内核，以有效利用开发板的资源。
      如果应用程序不需要任何开发板特定的功能，它有时可以为多种类型的开发板配置
      （包括具有不同 CPU 架构的开发板）构建。

   application image
      应用镜像 (application image) - 加载并在其构建的开发板上执行的二进制文件。
      每个应用镜像都包含应用程序的代码和支持它所需的 Zephyr 内核代码。
      它们被编译为单个完全链接的二进制文件。
      一旦应用镜像加载到开发板上，该镜像就会控制系统，初始化它，并作为系统的唯一应用程序运行。
      应用程序代码和内核代码都作为特权代码在单个共享地址空间内执行。

   architecture
      架构 (architecture) - 指令集架构 (ISA - Instruction Set Architecture) 以及编程模型。

   board
      开发板 (board) - 具有一组定义的设备和功能的目标系统，可以加载并执行应用镜像。
      它可以是实际的硬件系统或在 QEMU 下运行的模拟系统。一个开发板可以包含一个或多个 :term:`SoCs <SoC>`。
      Zephyr 内核支持 :ref:`多种开发板 <boards>`。

   board configuration
      开发板配置 (board configuration) - 一组内核配置选项，指定内核如何使用开发板上存在的设备。
      Zephyr 构建系统为其支持的每个开发板定义一个或多个开发板配置。
      如果需要，构建系统指定的内核配置设置可以由应用程序覆盖。

   board name
      开发板名称 (board name) - :term:`board` 的人类可读名称。唯一且描述性地标识特定系统，
      但不包括实际为其构建 Zephyr 镜像可能需要的其他信息。
      有关详细信息，请参阅 :ref:`board_terminology`。

   board qualifiers
      开发板限定符 (board qualifiers) - 一组附加令牌，由正斜杠 (``/``) 分隔，跟在 :term:`board name`
      （以及可选的 :term:`board revision`）之后，形成 :term:`board target`。
      当前接受的限定符是 :term:`SoC`、:term:`CPU cluster` 和 :term:`variant`。
      有关详细信息，请参阅 :ref:`board_terminology`。

   board revision
      开发板修订版 (board revision) - 标识硬件系统特定修订版的可选版本字符串。
      这在硬件系统引入小的更改时很有用，可以避免重复开发板文件。
      有关更多信息，请参阅 :ref:`porting_board_revisions` 和 :ref:`application_board_version`。

   board target
     开发板目标 (board target) - 可以提供给任何 Zephyr 构建工具以编译和链接特定硬件系统镜像的完整字符串。
     此字符串唯一标识 :term:`board name`、:term:`board revision` 和 :term:`board qualifiers` 的组合。
     有关详细信息，请参阅 :ref:`board_terminology`。

   CPU cluster
     CPU 集群 (CPU cluster) - 一组一个或多个 :term:`CPU cores <CPU core>`，
     全部在同一地址空间内以对称 (SMP - Symmetric Multi-Processing) 配置执行同一镜像。
     只有相同 :term:`architecture` 的 :term:`CPU cores <CPU core>` 才能在单个集群中。
     多个 CPU 集群（每个集群包含一个或多个核心）可以在同一 :term:`SoC` 中共存。

   CPU core
     CPU 核心 (CPU core) - 单个处理单元，具有自己的程序计数器 (Program Counter)，按顺序执行程序指令。
     CPU 核心是 :term:`CPU cluster` 的一部分，该集群可以包含一个或多个核心。

   device runtime power management
      设备运行时电源管理 (Device Runtime Power Management) - 设备运行时电源管理 (PM) 是指
      设备独立于系统电源状态节省能量的能力。设备将保持其使用的引用，并将自动挂起或恢复。
      此功能通过 :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME` Kconfig 选项启用。

   idle thread
      空闲线程 (idle thread) - 当没有其他线程准备好运行时运行的系统线程。

   IDT
      (Interrupt Descriptor Table - 中断描述符表) x86 架构用于实现中断向量表的数据结构。
      IDT 用于确定对中断和异常的正确响应。

   internal API
      内部 API (internal API) - 在 Zephyr 源代码树中任何地方定义的任何内部函数、结构或宏。
      内部 API 旨在"扩展" Zephyr，并且仅在某些 :term:`software components <software component>` 之间使用，
      通常在树内，但在某些情况下在树外（例如，添加树外架构或驱动程序）。
      应用程序不得在其自己的范围之外调用内部 API。调用或实现 API 的上下文已明确定义。
      例如，以 ``arch_`` 为前缀的函数旨在供 Zephyr 内核用于调用特定于架构的代码。
      内部 API 大部分保持稳定，但提供的保证少于 :term:`public APIs <public API>`。

   ISR
      (Interrupt Service Routine - 中断服务例程) 也称为中断处理程序，ISR 是一个回调函数，
      其执行由硬件中断（或软件中断指令）触发，用于处理需要中断处理器上当前执行代码的高优先级条件。

   kernel
      内核 (kernel) - 实现 Zephyr 内核的 Zephyr 提供的文件集，包括其核心服务、设备驱动程序、网络堆栈等。

   power domain
      电源域 (power domain) - 电源域是一组设备，在单个操作中集体施加和移除电源。
      电源域由 :c:struct:`device` 表示。

   power gating
      功率门控 (power gating) - 功率门控通过关闭集成电路中未使用的区域来降低功耗。

   private API
      私有 API (private API) - 在 Zephyr 源代码树中任何地方定义的任何函数、结构或宏，
      仅供定义它们的 :term:`software component` 内部使用。
      私有 API 可能随时更改，并且不得在相应软件组件之外的代码中使用。

   public API
      公共 API (public API) - 在 ``include/zephyr`` 文件夹内定义的任何函数、结构或宏，
      未明确标记为私有。公共 API 旨在供任何和所有树内或树外 :term:`software components <software component>` 使用。
      公共 API 不能在不遵循 :ref:`API lifecycle <api_lifecycle>` 部分所述规定的情况下修改，
      这意味着它们提供保证，随着时间的推移它们将保持稳定。

   SoC
      (System on a Chip - 片上系统) 一个 `片上系统`_，即包含至少一个 :term:`CPU cluster`
      （依次包含至少一个 :term:`CPU core`），以及外设和内存的集成电路。

   SoC family
      SoC 系列 (SoC family) - 一个或多个 :term:`SoCs <SoC>` 或 :term:`SoC series`，
      它们有足够的共同点，可以将它们视为相关的，并在单个系列名称下。

   SoC series
      SoC 系列 (SoC series) - 许多不同的 :term:`SoCs <SoC>`，它们共享相似的特性和功能，
      供应商通常将它们一起命名和销售。

   software component
      软件组件 (software component) - 软件组件是 Zephyr 源代码的独立、模块化和可替换的部分。
      驱动程序、子系统或应用程序都是 Zephyr 中存在的软件组件的示例。

   subsystem
       子系统 (subsystem) - 子系统是指操作系统中逻辑上不同的部分，处理特定功能或提供某些服务。

   system power state
      系统电源状态 (system power state) - 系统电源状态描述整个系统的功耗。
      系统电源状态由 :c:enum:`pm_state` 表示。

   variant
      变体 (variant) - 在 :term:`board qualifiers` 的上下文中，变体指定 :term:`SoC`
      和 :term:`CPU cluster` 组合构建的特定类型或配置。
      变体概念的常见用途包括为具有可信执行环境 (Trusted Execution Environment) 支持的平台引入
      安全和非安全构建，或在构建中选择使用的 RAM 类型。

   west
      为 Zephyr 项目开发的多仓库元工具 (multi-repo meta-tool)。请参阅 :ref:`west`。

   west installation
      在 west 0.7 之前使用的 :term:`west workspace` 的过时术语。

   west manifest
      YAML 文件，通常命名为 :file:`west.yml`，描述项目，或构成 :term:`west workspace` 的 Git 仓库，
      以及附加元数据。有关一般信息，请参阅 :ref:`west-basics`，有关详细信息，请参阅 :ref:`west-manifests`。

   west manifest repository
      :term:`west workspace` 中包含 :term:`west manifest` 的 Git 仓库。
      其位置由 :ref:`manifest.path 配置选项 <west-config-index>` 给出。请参阅 :ref:`west-basics`。

   west project
      :term:`west manifest` 中的每个条目，描述 west 在处理相应 :term:`west manifest repository` 时
      将克隆和管理的 Git 仓库。请注意，west project 不同于 :term:`zephyr module`，
      尽管许多项目也是模块。有关详细信息，请参阅 :ref:`west-manifests-projects`。

   west workspace
      系统上具有 :file:`.west` 子目录和 :term:`west manifest repository` 的文件夹。
      您可以使用 ``west init`` 命令创建 west workspace，将 Zephyr 源代码及其
      :term:`west projects <west project>` 的源代码克隆到您的系统上。请参阅 :ref:`west-basics`。

   XIP
      (eXecute In Place - 就地执行) 一种直接从长期存储中执行程序的方法，而不是将其复制到 RAM 中，
      为动态数据而不是静态程序代码节省可写内存。

   zephyr module
      包含 :file:`zephyr/module.yml` 文件的 Git 仓库，Zephyr 构建系统使用该文件将模块的源代码
      和配置文件集成到常规 Zephyr 构建中。Zephyr 模块可以是 west project，但不是必须的。
      有关详细信息，请参阅 :ref:`modules`。

.. _片上系统: https://en.wikipedia.org/wiki/System_on_a_chip
