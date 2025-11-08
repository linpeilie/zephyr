.. _control_flow_integrity:

控制流完整性 (Control Flow Integrity)
#####################################

控制流完整性 (CFI) 是一种安全特性,确保程序的控制流遵循预定义路径,防止攻击者将执行转移到恶意代码。CFI 在防御控制流劫持攻击(如面向返回编程 (ROP) 和面向跳转编程 (JOP))方面特别有用。

CFI 通过在运行时验证程序的控制流来工作,确保函数调用和返回都指向合法目标。这通常通过代码插桩实现,添加检查以验证控制流遵循程序控制流图定义的预期路径。

前向边和返回边 (Forward and return edges)
----------------------------------------

在 CFI 的上下文中,控制流边可以分为两种类型:

1. **前向边 (Forward edges)**: 这些表示从一个函数到另一个函数的控制流,如函数调用。前向边通常被验证以确保调用的目标是程序内的合法函数。
2. **返回边 (Return edges)**: 这些表示从函数返回到调用者。返回边被验证以确保返回地址是合法的并且对应于有效的调用点。

前向边可以通过编译器插桩来支持,添加检查以验证函数调用的目标是否有效。返回边可以通过维护影子栈或使用其他机制来支持,以确保返回地址是合法的。

Zephyr 支持维护影子栈,可以通过 :kconfig:option:`CONFIG_HW_SHADOW_STACK` 启用。然后,内核将使用像 :c:macro:`K_THREAD_HW_SHADOW_STACK_DEFINE` 这样的宏,与其他线程栈相关的宏一起,为线程使用的影子栈提供区域。通常,应用程序只需要启用 :kconfig:option:`CONFIG_HW_SHADOW_STACK`(以及相关选项,如 :kconfig:option:`CONFIG_HW_SHADOW_STACK_PERCENTAGE_SIZE` 和 :kconfig:option:`CONFIG_HW_SHADOW_STACK_MIN_SIZE`)来启用影子栈支持。内核随后将自动管理每个线程的影子栈。

实现细节 (Implementation details)
*********************************

``K_THREAD_HW_SHADOW_STACK*`` 宏系列对影子栈参数进行最小设置。然后,它们调用特定于架构的 ``ARCH_THREAD_HW_SHADOW_STACK*`` 宏来执行实际设置。

硬件支持 (Hardware support)
---------------------------

虽然 CFI 可以在软件中实现,但硬件支持可以显著增强其有效性和性能。目前,Zephyr 支持 Intel 控制流强制技术 (CET),它为 CFI 提供基于硬件的支持。

Intel CET
*********

Intel 控制流强制技术 (CET) 是一组硬件特性,通过为 CFI 提供支持来增强应用程序的安全性。CET 包含两个主要组件:

1. **影子栈 (Shadow Stack)**: 此特性为返回地址维护一个单独的栈,确保返回地址不能被篡改。当函数返回时,返回地址从影子栈中弹出并与常规栈的地址进行比较,提供针对控制流劫持的额外保护层。
2. **间接分支跟踪 (IBT - Indirect Branch Tracking)**: 此特性跟踪间接分支(如函数指针)并确保它们仅指向代码中的有效位置。它防止攻击者通过 ROP 等技术将执行重定向到任意代码。

这两个特性分别提供了返回边和前向边验证。要在支持的硬件上启用 Zephyr 中的影子栈支持,可以使用 :kconfig:option:`CONFIG_HW_SHADOW_STACK` Kconfig 选项。要启用 IBT,请使用 :kconfig:option:`CONFIG_X86_CET_IBT`。

由于 IBT 由编译器有效实现,因此需要工具链支持。目前,Zephyr SDK x86 工具链可用于构建具有 IBT 支持的应用程序。但是,它们的预编译构件(如 ``libc`` 和 ``libgcc``)没有启用 IBT。因此,对于 ``libc``,需要将其构建为模块,例如通过使用 :kconfig:option:`CONFIG_PICOLIBC_USE_MODULE`。对于其他部分,需要自定义工具链。

限制 (Limitations)
------------------

目前,在后台创建的影子栈位于全局命名空间中。因此,即使在不同的编译单元之间,也*不能*重用线程栈名称。
