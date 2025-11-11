概述 (Overview)
################

电源管理子系统提供的接口和 API 被设计为与架构和 SOC 无关。这使得电源管理实现能够轻松适配到不同的 SOC 和架构。(The interfaces and APIs provided by the power management subsystem are designed to be architecture and SOC independent. This enables power management implementations to be easily adapted to different SOCs and architectures.)

架构和 SOC 的独立性是通过将核心 PM 基础设施与 SOC 特定组件的实现分离来实现的。因此,向操作系统的其余部分和应用层呈现了一个连贯的抽象。(The architecture and SOC independence is achieved by separating the core PM infrastructure from implementations of the SOC specific components. Thus a coherent abstraction is presented to the rest of the OS and the application layer.)

电源管理功能被分类为以下几个类别:(The power management features are classified into the following categories.)

* 系统电源管理 (System Power Management)
* 设备电源管理 (Device Power Management)
