.. _xtensa_developer_guide:

Xtensa 开发者指南 (Xtensa Developer Guide)
###########################################

概述 (Overview)
****************

本页面包含为基于 Xtensa 的平台开发时某些方面的信息。

HiFi 音频引擎 DSP (HiFi Audio Engine DSP)
******************************************

内核允许线程在支持这些寄存器的板上使用 HiFi 音频引擎 DSP 寄存器。
内核仅支持线程使用 HiFi 寄存器,不支持 ISR 使用。

.. note::
    目前,只有 Intel ADSP ACE 硬件平台默认配置为支持 HiFi。

概念 (Concepts)
================

内核可以配置为应用程序利用 Xtensa HiFi 音频引擎 DSP 提供的服务。
支持三种操作模式,如下所述。

无 HiFi 寄存器模式 (No HiFi registers mode)
--------------------------------------------

当应用程序没有使用 HiFi 寄存器的线程时使用此模式。这是内核的默认 HiFi 服务模式。

非共享 HiFi 寄存器模式 (Unshared HiFi registers mode)
------------------------------------------------------

当应用程序只有一个使用 HiFi 寄存器的线程时使用此模式。
每当发生上下文切换时,HiFi 寄存器保持不变。

.. note::
    如果两个或更多线程尝试使用 HiFi 寄存器,行为是未定义的,
    因为内核不会尝试检测(也不会阻止)多个线程使用这些寄存器。

共享 HiFi 寄存器模式 (Shared HiFi registers mode)
--------------------------------------------------

当应用程序有两个或更多使用 HiFi 寄存器的线程时使用此模式。
启用后,内核自动允许所有线程使用 HiFi 寄存器。从概念上讲,
它可以细分为两个子模式——急切模式和延迟模式。
它们都会保存和恢复 HiFi 寄存器,但它们在何时保存和恢复寄存器、
以及将它们保存到何处和从何处恢复方面有所不同。

在急切共享模型中,在每次线程上下文切换期间保存和恢复 HiFi 寄存器,
无论线程是否使用它们。每个线程可能需要额外的栈空间来考虑必须保存的额外寄存器。
这是两种模型中的默认模型。

在延迟共享模型中,内核跟踪"拥有"协处理器的线程。
如果"拥有"线程被切换出去,则在新线程尝试使用 HiFi 之前不会保存 HiFi 寄存器,
之后该新线程成为新的所有者并加载其 HiFi 寄存器。

.. note::
    如果 SMP 系统检测到即将成为所有者的线程仍然是另一个 CPU 上的所有者,
    将向该 CPU 发送 IPI 以启动将其 HiFi 寄存器保存到内存。
    然后当前处理器将旋转直到 HiFi 寄存器被保存。这种旋转可能导致偶发性较长的延迟。
    为了获得最佳性能,建议将使用 HiFi 的线程固定到单个 CPU。

配置选项 (Configuration Options)
==================================

当禁用配置选项 :kconfig:option:`CONFIG_XTENSA_HIFI_SHARING`
但启用配置选项 :kconfig:option:`CONFIG_XTENSA_HIFI3` 和/或
:kconfig:option:`CONFIG_XTENSA_HIFI4` 时,选择非共享 HiFi 寄存器模式。

当除了配置选项 :kconfig:option:`CONFIG_XTENSA_HIFI3` 和/或
:kconfig:option:`CONFIG_XTENSA_HIFI4` 之外还启用配置选项
:kconfig:option:`CONFIG_XTENSA_HIFI_SHARING` 时,选择共享 HiFi 寄存器模式。
线程必须具有足够的栈空间以在如上所述的上下文切换期间保存 HiFi 寄存器值。

急切和延迟 HiFi 共享模式都需要启用配置选项
:kconfig:option:`CONFIG_XTENSA_HIFI_SHARING`。虽然急切 HiFi 共享是默认的,
但可以通过启用配置选项 :kconfig:option:`CONFIG_XTENSA_EAGER_HIFI_SHARING` 显式选择它。
要改为选择延迟 HiFi 共享,请启用配置选项
:kconfig:option:`CONFIG_XTENSA_LAZY_HIFI_SHARING`。
