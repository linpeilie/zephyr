Zephyr 在 RISC-V 处理器上的支持状态 (Zephyr support status on RISC-V processors)
##################################################################################

概述 (Overview)
****************

本页面描述了 Zephyr 对 RISC-V 处理器的当前状态。目前,支持一些开发板,
以及 Qemu 支持和一些 FPGA 实现(如 neorv32 和 litex_vexriscv)的支持。

Zephyr 支持包括 PMP、:ref:`用户模式<usermode_api>`、几个 ISA 扩展
以及 :ref:`半主机<semihost_guide>`。

用户模式和 PMP 支持 (User mode and PMP support)
************************************************

当平台具有物理内存保护 (PMP) 支持时,在 Zephyr 上启用它可以选择用户空间支持和栈保护。

ISA 扩展 (ISA extensions)
**************************

可以在 Zephyr 中设置给定平台上可用的 ISA 扩展 (RV32/64I(E)MAFD(G)QC),
方法是设置适当的 ``CONFIG_RISCV_ISA_*`` kconfig。
有关更多信息,请参阅 :file:`arch/riscv/Kconfig.isa`。

请注意,Zephyr SDK 工具链支持可能未为所有组合定义。

SMP 支持 (SMP support)
***********************

RISC-V 支持 SMP,适用于 QEMU 虚拟化和基于硬件的平台。
为了测试 SMP 支持,可以使用基于 QEMU 的平台 :zephyr:board:`qemu_riscv32`
或 :zephyr:board:`qemu_riscv64`,
或基于硬件的平台 :zephyr:board:`beaglev_fire` 或 :zephyr:board:`mpfs_icicle`。
