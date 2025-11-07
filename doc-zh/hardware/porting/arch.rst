.. _architecture_porting_guide:

架构移植指南 (Architecture Porting Guide)
##########################################

需要架构移植以使 Zephyr 能够在当前不支持的 :abbr:`ISA (指令集架构,instruction set architecture)` 或 :abbr:`ABI (应用程序二进制接口,Application Binary Interface)` 上运行。

以下是 Zephyr 支持的 ISA 和 ABI 示例:

* x86_32 ISA 与 System V ABI
* ARMv7-M ISA 与 Thumb2 指令集和 ARM 嵌入式 ABI (aeabi)
* ARCv2 ISA

有关 Kconfig 配置的信息,请参见 :ref:`setting_configuration_values`。架构使用与板类似的 Kconfig 配置方案。

架构移植可以分为几个部分;大部分是必需的,有些是可选的:

* **早期启动序列**: 每个架构在 CPU 从复位状态恢复时必须采取不同的步骤(必需)。

* **中断和异常处理**: 每个架构以特定方式处理异步和非请求事件(必需)。

* **线程上下文切换**: Zephyr 上下文切换依赖于 ABI,每个 ISA 都有不同的寄存器集需要保存(必需)。

* **线程创建和终止**: 线程的初始栈帧是 ABI 和架构相关的,线程中止可能也是如此(必需)。

* **设备驱动程序**: 通常,系统时钟定时器和中断控制器与架构绑定(部分必需,部分可选)。

* **实用程序库**: 出于性能原因,一些常见的内核 API 依赖于架构特定的实现(必需)。

* **CPU 空闲/电源管理**: 大多数架构实现了将 CPU 置于睡眠状态的指令(部分可选,但很可能非常需要)。

* **故障管理**: 用于实现架构特定的调试帮助和处理线程中的致命错误(部分可选)。

* **链接脚本和工具链**: 构建系统和链接镜像时很可能需要架构特定的细节(必需)。

* **内存管理和内存映射**: 用于支持内存管理和内存映射的架构特定细节。

* **栈对象**: 用于有关栈对象的内存保护硬件的架构特定细节。

* **用户模式线程**: 用于支持用户模式下的线程。

* **GDB 存根**: 用于支持 GDB 存根以启用远程调试。

早期启动序列 (Early Boot Sequence)
************************************

早期启动序列的目标是将系统从复位后的状态转换到可以运行 C 代码的状态,从而进入通用的内核初始化序列。大多数时候,只需要很少的步骤,而某些架构需要执行更多工作。

所有架构的通用步骤:

* 设置初始栈。
* 如果运行 :abbr:`XIP (就地执行,eXecute-In-Place)` 内核,将已初始化的数据从 ROM 复制到 RAM。
* 如果不使用 ELF 加载器,将 BSS 段清零。
* 跳转到 :code:`z_cstart()`,即早期内核初始化

  * :code:`z_cstart()` 负责将上下文从启动时运行的虚假上下文切换到主线程。

必须采取的架构特定步骤的一些示例:

* 如果在 x86_32 上以实模式获得控制权,则切换到 32 位保护模式。
* 在 x86_32 上设置段寄存器,以处理引导加载程序将其保留在未知或损坏状态的情况。
* 在 Cortex-M3/4 上初始化板特定的看门狗。
* 在 Cortex-M 上将栈从 MSP 切换到 PSP。
* 在 Cortex-M 上使用与调用 z_swap() 不同的方法来防止竞态条件。
* 在 ARCv2 上设置 FIRQ 和常规 IRQ 处理。

早期启动序列钩子 (Early Boot Sequence Hooks)
===============================================

Zephyr 公开了几个钩子(在 :zephyr_file:`include/zephyr/platform/hooks.h` 中描述),允许在启动过程的精确时刻执行 SoC 或板特定的代码。

内核负责从架构无关的代码中调用大多数钩子。但是,某些钩子必须在早期启动序列期间调用;由于序列是在架构特定代码中实现的,因此对钩子的调用也必须在那里完成。以下概述了早期启动序列以及架构特定代码应何时调用钩子:

#. 执行从架构特定的入口点开始,其名称与 :kconfig:option:`CONFIG_KERNEL_ENTRY` 匹配。

#. 立即重新初始化架构特定的状态(如果启用了 :kconfig:option:`CONFIG_INIT_ARCH_HW_AT_BOOT`)。

#. 调用 :c:func:`soc_early_reset_hook`。

   .. note::
    在调用此钩子之前不需要设置有效的栈。但是,钩子允许在返回之前覆盖栈指针。架构特定的代码不能期望栈指针寄存器的值在调用 :c:func:`soc_early_reset_hook` 时被保留。

    在具有多个栈指针的架构上,通常有一个可直接访问的 *"主"* 栈指针和 *"辅助"* 栈指针寄存器。:c:func:`soc_early_reset_hook` 实现可以覆盖 *"主"* 栈指针,但 **不得** 读取或修改任何 *"辅助"* 栈指针的值。(这允许架构特定的代码在调用 :c:func:`soc_early_reset_hook` 之前设置任何 *"辅助"* 栈指针)

    例如,ARM Cortex-A 架构定义了几种执行模式,每种模式都有自己的栈指针寄存器 :samp:`sp_{mode}`。当处理器以模式 :samp:`{X}` 执行时,涉及 ``sp`` 通用寄存器的操作在 :samp:`sp_{X}` 上操作。在这个架构上,假设调用 :c:func:`soc_early_reset_hook` 时处理器以模式 :samp:`{M}` 执行,钩子允许覆盖 :samp:`sp_{M}`(通过 ``sp`` 访问),但 **不得** 读取或覆盖任何其他 :samp:`sp_{mode}`(其中 :samp:`{mode} != {M}`)。

    :c:func:`soc_early_reset_hook` 实现允许不将执行返回到架构特定的代码,在这种情况下它们会"接管"系统。此类钩子不受上述规则的约束,可以读取或覆盖任何栈指针。但是,当提供这样的实现时,早期启动序列的其余部分显然不会执行。

#. 为早期启动序列的下一步设置初始栈。

#. Architecture-specific "*resume from suspend-to-RAM*" logic is executed

   .. note::
    Refer to :kconfig:option:`CONFIG_PM_S2RAM` and the architecture-specific
    implementation for more details, but note that the rest of the early boot
    sequence is not executed if this logic determines that an exit from
    suspend-to-RAM is ongoing.

#. :c:func:`soc_reset_hook` is called.

#. *Architecture-specific operations (in assembly) are performed here...*

#. :c:func:`z_prep_c` is called. This architecture-specific function is implemented in C.

#. :c:func:`z_prep_c` immediately calls :c:func:`soc_prep_hook`.

#. *Architecture-specific operations (in C) are performed here...*

#. 调用 :c:func:`z_cstart`。架构无关的代码开始执行。

中断和异常处理 (Interrupt and Exception Handling)
***************************************************

每个架构以不同方式定义中断和异常处理。

当设备想要向处理器发出信号表示有一些工作需要代表它完成时,它会引发中断。当线程执行不由软件本身的串行流处理的操作时,它会引发异常。中断和异常都将控制权传递给处理程序。在中断的情况下,处理程序被称为 :abbr:`ISR (中断服务例程,Interrupt Service Routine)`。处理程序执行异常或中断所需的工作。对于中断,该工作是特定于设备的。对于异常,它取决于异常,但最常见的是核心内核本身负责提供处理程序。

内核除了处理程序本身执行的工作外,还必须执行一些工作。例如:

* 在将控制权交给处理程序之前:

  * 保存当前正在执行的上下文。
  * 可能退出省电模式,这包括唤醒设备。
  * 如果退出无滴答空闲模式,则更新内核运行时间。

* 从处理程序获得控制权后:

  * 决定是否执行上下文切换。
  * 执行上下文切换时,恢复正在切换的上下文。

这项工作在概念上跨架构是相同的,但细节完全不同:

* 要保存和恢复的寄存器。
* 执行工作的处理器指令。
* 异常的编号。
* 等等。

因此,它需要架构特定的实现,称为中断/异常存根。

另一个问题是内核将 ISR 的签名定义为:

.. code-block:: C

    void (*isr)(void *parameter)

架构没有一致或原生的方式来处理 ISR 的参数。因此,有两种常用的方法来处理参数。

* 使用某些架构定义的机制,参数值在存根中被强制设置。这在基于 X86 的架构中很常见。

* ISR 的参数通过单独的表插入和跟踪,需要架构在运行时发现正在执行的中断。为实际中断向量表的所有条目安装了一个公共中断处理程序解复用器,然后从单独的表中获取设备的 ISR 和参数。这种方法通常在 ARC 和 ARM 架构中通过 :kconfig:option:`CONFIG_GEN_ISR_TABLES` 实现使用。您可以通过查看 x86 中的 :code:`_interrupt_enter()`、ARM 中的 :code:`_isr_wrapper()` 或 :zephyr_file:`arch/arc/core/isr_wrapper.S` 中 ARC 的完整实现描述来找到存根的示例。

每个架构还必须实现中断控制的原语:

* 锁定中断::c:macro:`irq_lock()`、:c:macro:`irq_unlock()`。
* 注册中断::c:macro:`IRQ_CONNECT()`。
* 如果可能,编程优先级 :c:func:`irq_priority_set`。
* 启用/禁用中断::c:macro:`irq_enable()`、:c:macro:`irq_disable()`。

.. note::

  :c:macro:`IRQ_CONNECT` 是一个宏,它使用汇编器和/或链接器脚本技巧在构建时连接中断,节省启动时间和代码大小。

向量表应包含可能发生的每个中断和异常的处理程序。处理程序可以简单到只是一个旋转循环。但是,我们强烈建议处理程序至少打印一些调试信息。当遇到故障异常(如除零或无效内存访问)或意外中断(:dfn:`虚假中断`)时,这些信息有助于找出问题所在。请参阅 :zephyr_file:`arch/arm/core/cortex_m/fault.c` 中的 ARM 实现示例。

线程上下文切换 (Thread Context Switching)
******************************************

多线程是拥有内核的基本目的。Zephyr 支持两种类型的线程:可抢占和协作式。确定下一个要调度的线程的规则由内核处理。但是,架构移植需要实现上下文切换本身的方法。

Zephyr 提供两个互斥的上下文切换接口。首选使用的接口是 :code:`arch_switch`,当启用 :kconfig:option:`CONFIG_USE_SWITCH` 时选择它。替代接口是 :code:`arch_swap`——当禁用 :kconfig:option:`CONFIG_USE_SWITCH` 时选择。移植到新架构时,只需实现其中之一;但是,对于 SMP 平台,必须是 :code:`arch_switch`。

上下文切换可能在几种情况下发生:

* 当线程执行阻塞操作时,例如获取当前不可用的信号量。

* 当可抢占线程通过释放被阻塞的对象来解除更高优先级线程的阻塞时。

* 当中断解除比当前正在执行的线程更高优先级的线程的阻塞时,如果当前执行的线程是可抢占的。

* 当线程运行完成时。

* 当线程导致致命异常并从运行线程中删除时。例如,引用无效内存。

因此,上下文切换必须能够处理所有这些情况。

有两种类型的上下文切换::dfn:`协作式` 和 :dfn:`抢占式`。

* *协作式* 上下文切换发生在线程自愿将控制权交给另一个线程时。发生这种情况有两种情况

  * 当线程显式让步时。
  * 当线程尝试获取当前不可用的对象并愿意等待直到对象可用时。

* *抢占式* 上下文切换发生在 ISR 或线程导致调度比当前运行的线程更高优先级的线程的操作时,如果当前运行的线程是可抢占的。此类操作的一个示例是释放更高优先级线程正在等待的对象。

.. note::

  当协作式线程之一是正在运行的线程时,永远不会从协作式线程中获取控制权。

协作式上下文切换总是通过让线程调用内部内核例程 :code:`z_swap`(或其变体之一)来完成。这反过来将适当地调用 :code:`arch_switch` 或 :code:`arch_swap`。调用这些函数时,不会进行检查以确定是否要进行上下文切换——必须进行上下文切换。

.. note::

  在 x86 和 Nios2 上,:code:`arch_swap` 足够通用,架构足够灵活,可以在退出中断时调用它来引发上下文切换。这不应被视为规则,因为 ARM Cortex-M 和 ARCv2 移植都不这样做。

Since :code:`z_swap` is cooperative, the caller-saved registers from the ABI are
already on the stack. There is no need to save them in the k_thread structure.

A context switch can also be performed preemptively. This happens upon exiting
an ISR, in the kernel interrupt exit stub:

* :code:`_interrupt_enter` on x86 after the handler is called.
* :code:`z_arm_exc_exit` and :code:`z_arm_int_exit` on ARM.
* :code:`_firq_exit` and :code:`_rirq_exit` on ARCv2.

The decision logic to invoke the context switch is simple and is only performed
when exiting a non-nested interrupt:

When :kconfig:option:`CONFIG_USE_SWITCH` is enabled ...

* The interrupt exit code shall call :c:func:`z_get_next_switch_handle`, and
  return to the thread context identified by the returned switch handle

When :kconfig:option:`CONFIG_USE_SWITCH` is not enabled ...

* The interrupt exit code shall fetch the cached thread from the ready queue, and:

  * If the cached thread is not the current thread, invoke the context switch.
  * Otherwise do not invoke it.

这很简单,但至关重要:如果这没有正确实现,内核将无法按预期工作,并且会经历奇怪的崩溃,主要是由于栈损坏。

线程创建和终止 (Thread Creation and Termination)
***************************************************

要启动一个新线程,必须构造一个栈帧,以便上下文切换可以像弹出已被上下文切换出去的线程一样弹出它。这将在特定于架构的内部例程 :code:`_new_thread` 中实现。

线程入口点也不能直接调用,即它不应被设置为新线程的 :abbr:`PC (program counter, 程序计数器)`。相反,它必须包装在 :code:`_thread_entry` 中。这意味着栈帧中的 PC 应设置为 :code:`_thread_entry`,并且线程入口点应作为第一个参数传递给 :code:`_thread_entry`。具体细节取决于 ABI。

对特定于架构的线程终止实现的需求取决于架构。有一个通用实现,但它可能不适用于给定的架构。

遇到的一个需要特定于架构的线程终止实现的原因是,如果由于优雅退出或由于异常而中止线程,中止线程可能会有所不同。对于 ARM Cortex-M 就是这种情况,如果线程触发了致命异常,则必须将 CPU 退出处理器模式,但如果线程优雅地退出其入口点函数,则不必这样做。

这意味着实现特定于架构的 :c:func:`k_thread_abort` 版本,并根据架构需要设置 Kconfig 选项 :kconfig:option:`CONFIG_ARCH_HAS_THREAD_ABORT`(例如,参见 :zephyr_file:`arch/arm/core/cortex_m/Kconfig`)。

线程本地存储 (Thread Local Storage)
*************************************

要在新架构上启用线程本地存储:

#. 实现 :c:func:`arch_tls_stack_setup` 以在栈中设置 TLS 存储区域。参考工具链文档了解存储区域的结构要求。可以使用一些辅助函数:

   * 函数 :c:func:`z_tls_data_size` 返回线程本地变量所需的大小(不包括工具链和架构所需的任何额外数据)。
   * 函数 :c:func:`z_tls_copy` 为线程本地变量准备 TLS 存储区域。这只复制变量本身,不做特定于架构和/或工具链的数据。

#. 在上下文切换中,获取新线程的 ``struct k_thread`` 中的 ``tls`` 字段,并将其放入适当的寄存器(或其他某个变量)中,以便访问 TLS 存储区域。参考工具链和架构文档了解使用哪些寄存器。

#. 在 kconfig 中,将 ``select CONFIG_ARCH_HAS_THREAD_LOCAL_STORAGE`` 添加到与新架构相关的 kconfig 中。

#. 运行 ``tests/kernel/threads/tls`` 以确保新代码能正常工作。

设备驱动程序 (Device Drivers)
******************************

The kernel requires very few hardware devices to function. In theory, the only
required device is the interrupt controller, since the kernel can run without a
system clock. In practice, to get access to most, if not all, of the sanity
check test suite, a system clock is needed as well. Since these two are usually
tied to the architecture, they are part of the architecture port.

Interrupt Controllers
=====================

There can be significant differences between the interrupt controllers and the
interrupt concepts across architectures.

For example, x86 has the concept of an :abbr:`IDT (Interrupt Descriptor Table)`
and different interrupt controllers. The position of an interrupt in the IDT
determines its priority.

On the other hand, the ARM Cortex-M has the :abbr:`NVIC (Nested Vectored
Interrupt Controller)` as part of the architecture definition. There is no need
for an IDT-like table that is separate from the NVIC vector table. The position
in the table has nothing to do with priority of an IRQ: priorities are
programmable per-entry.

ARCv2 将其中断单元作为架构定义的一部分,这与 NVIC 有些相似。然而,ARC 定义中断在异常和中断号之间具有一对一映射(即异常 1 是 IRQ1,设备 IRQ 从 16 开始),而 ARM 将 IRQ0 等效于异常 16(而且奇怪的是,异常 1 可以被视为 IRQ-15)。

所有这些差异意味着,在中断控制器方面,架构之间几乎没有什么可以共享的,如果有的话。

系统时钟 (System Clock)
========================

x86 将 APIC 定时器和 HPET 作为其架构定义的一部分。ARM Cortex-M 有 SYSTICK 异常。最后,ARCv2 有 timer0/1 设备。

内核超时在系统时钟定时器驱动程序的中断处理程序的上下文中处理。


串行线路上的控制台 (Console Over Serial Line)
==============================================

还有另一个设备几乎是架构移植的必需品,因为它对调试非常有用。它是一个简单的轮询、仅输出的串行端口驱动程序,用于发送控制台(:code:`printk`、:code:`printf`)输出。

它不是必需的,可以使用 RAM 控制台(:kconfig:option:`CONFIG_RAM_CONSOLE`)将所有输出发送到循环缓冲区,然后由调试器读取。

实用程序库 (Utility Libraries)
********************************

内核依赖于一些函数,这些函数可以用很少的指令实现,或者在现代处理器中以无锁方式实现。因此,这些函数被期望作为架构移植的一部分来实现。

* 原子操作符 (Atomic operators)。

  * 如果给定架构存在指令,则使用 :kconfig:option:`CONFIG_ATOMIC_OPERATIONS_ARCH` Kconfig 选项配置实现。

  * 如果给定架构不存在指令,则存在一个通用版本,它在非原子操作周围包装 :c:func:`irq_lock` 或 :c:func:`irq_unlock`。它使用 :kconfig:option:`CONFIG_ATOMIC_OPERATIONS_C` Kconfig 选项配置。

* 查找最低有效位集 (Find-least-significant-bit-set) 和查找最高有效位集 (find-most-significant-bit-set)。

  * 如果给定架构不存在指令,总是可以将这些函数实现为通用 C 函数。

可以使用编译器内建函数来实现这些,但要注意它们使用所需的编译器屏障。

CPU 空闲/电源管理 (CPU Idling/Power Management)
*************************************************

The kernel provides support for CPU power management with two functions:
:c:func:`arch_cpu_idle` and :c:func:`arch_cpu_atomic_idle`.

:c:func:`arch_cpu_idle` can be as simple as calling the power saving
instruction for the architecture with interrupts unlocked, for example
:code:`hlt` on x86, :code:`wfi` or :code:`wfe` on ARM, :code:`sleep` on ARC.
This function can be called in a loop within a context that does not care if it
get interrupted or not by an interrupt before going to sleep. There are
basically two scenarios when it is correct to use this function:

* In a single-threaded system, in the only thread when the thread is not used
  for doing real work after initialization, i.e. it is sitting in a loop doing
  nothing for the duration of the application.

* In the idle thread.

另一方面,:c:func:`arch_cpu_atomic_idle` 必须能够原子地重新启用中断并调用节能指令。因此,它可以在实际应用代码中使用,同样在单线程系统中使用。

通常,CPU 空闲应该留给空闲线程处理,但在某些非常特殊的场景中,应用程序可以使用这些 API。

给定架构必须存在这两个函数。但是,如果需要,实现可以简单地执行以下步骤:

#. 解锁中断
#. NOP

但是,强烈建议进行真正的实现。

故障管理 (Fault Management)
****************************

在发生未处理的 CPU 异常时,架构代码必须调用 :c:func:`z_fatal_error`。此函数转储出与架构无关的信息,并通过调用 :c:func:`k_sys_fatal_error` 做出下一步操作的策略决定。可以覆盖此函数以实现特定于应用程序的策略,这些策略可能包括锁定中断并永远旋转(默认实现)甚至关闭系统(如果支持)。

工具链和链接 (Toolchain and Linking)
*************************************

必须将工具链支持添加到构建系统中。

在 :zephyr_file:`include/zephyr/toolchain/gcc.h` 中需要一些特定于架构的定义。查看该文件中当前支持的架构的内容。

每个架构还需要自己的链接器脚本,即使大多数节可以从其他架构的链接器脚本派生。某些节可能特定于新架构,例如 ARM 上的 SCB 节和 x86 上的 IDT 节。

内存管理和内存映射 (Memory Management and Memory Mapping)
**********************************************************

如果目标平台启用了分页并且需要驱动程序对其 I/O 区域进行内存映射,则需要启用 :kconfig:option:`CONFIG_MMU` 并实现以下 API:

- :c:func:`arch_mem_map`
- :c:func:`arch_mem_unmap`
- :c:func:`arch_page_phys_get`

栈对象 (Stack Objects)
***********************

内存保护硬件的存在会影响栈对象的创建方式。所有架构移植都必须指定栈指针所需的对齐方式,这是 CPU 和 ABI 要求的某种组合。这在架构头文件中用 :c:macro:`ARCH_STACK_PTR_ALIGN` 定义,通常是小的值,如 4、8 或 16 字节。

Two types of thread stacks exist:

- "kernel" stacks defined with :c:macro:`K_KERNEL_STACK_DEFINE()` and related
  APIs, which can host kernel threads running in supervisor mode or
  used as the stack for interrupt/exception handling. These have significantly
  relaxed alignment requirements and use less reserved data. No memory is
  reserved for privilege elevation stacks.

- "thread" stacks which typically use more memory, but are capable of hosting
  thread running in user mode, as well as any use-cases for kernel stacks.

If :kconfig:option:`CONFIG_USERSPACE` is not enabled, "thread" and "kernel" stacks are
equivalent.

Additional macros may be defined in the architecture layer to specify
栈对象基址的对齐方式、栈对象内不用于线程栈缓冲区的任何保留数据,以及如何将栈大小向上取整以支持用户模式线程。在没有定义的情况下,假定一些默认值:

- :c:macro:`ARCH_KERNEL_STACK_RESERVED`: 默认没有保留空间
- :c:macro:`ARCH_THREAD_STACK_RESERVED`: 默认没有保留空间
- :c:macro:`ARCH_KERNEL_STACK_OBJ_ALIGN`: 默认对齐到 :c:macro:`ARCH_STACK_PTR_ALIGN`
- :c:macro:`ARCH_THREAD_STACK_OBJ_ALIGN`: 默认对齐到 :c:macro:`ARCH_STACK_PTR_ALIGN`
- :c:macro:`ARCH_THREAD_STACK_SIZE_ALIGN`: 默认向上取整到 :c:macro:`ARCH_STACK_PTR_ALIGN`

所有栈创建宏都是根据这些定义的。

所有栈对象都具有以下布局,根据配置,某些区域可能为零大小。总是有两个主要部分:开头的保留内存,然后是栈缓冲区本身。某些区域的边界只能在运行时在其关联线程对象的上下文中确定。其他区域完全可以在构建时计算。

某些架构可能需要在运行时从栈缓冲区中分离出保留内存,而不是在构建时无条件地保留它,或者补充现有的保留区域(如 ARM FPU 的情况)。此类分离将始终在 ``thread.stack_info.start`` 中跟踪。由 ``thread.stack_info.start`` 和 ``thread.stack_info.size`` 指定的区域始终可由用户模式线程完全访问。``thread.stack_info.delta`` 表示一个偏移量,可用于从栈对象的最末端计算初始栈指针,同时考虑 TLS 和 ASLR 随机偏移的存储。

.. code-block:: none

   +---------------------+ <- thread.stack_obj
   | Reserved Memory     | } K_(THREAD|KERNEL)_STACK_RESERVED
   +---------------------+
   | Carved-out memory   |
   |.....................| <- thread.stack_info.start
   | Unused stack buffer |
   |                     |
   |.....................| <- thread's current stack pointer
   | Used stack buffer   |
   |                     |
   |.....................| <- Initial stack pointer. Computable
   | ASLR Random offset  |      with thread.stack_info.delta
   +---------------------| <- thread.userspace_local_data
   | Thread-local data   |
   +---------------------+ <- thread.stack_info.start + thread.stack_info.size


目前,Zephyr 不支持向上增长的栈。

无内存保护 (No Memory Protection)
==================================

如果不使用内存保护,则默认值就足够了。

基于硬件的栈溢出检测 (HW-based stack overflow detection)
========================================================

This option uses hardware features to generate a fatal error if a thread
in supervisor mode overflows its stack. This is useful for debugging, although
for a couple reasons, you can't reliably make any assertions about the state
of the system after this happens:

* The kernel could have been inside a critical section when the overflow
  occurs, leaving important global data structures in a corrupted state.

* For systems that implement stack protection using a guard memory region,
  it's possible to overshoot the guard and corrupt adjacent data structures
  before the hardware detects this situation.

要启用 :kconfig:option:`CONFIG_HW_STACK_PROTECTION` 功能,系统必须提供某种基于硬件的栈溢出保护,并启用 :kconfig:option:`CONFIG_ARCH_HAS_STACK_PROTECTION` 选项。

支持两种形式的基于硬件的栈溢出检测:专用于此目的的 CPU 功能,或紧接在栈缓冲区之前的特殊只读保护区域。

:kconfig:option:`CONFIG_HW_STACK_PROTECTION` 仅捕获监督者线程的栈溢出。这不需要捕获用户线程的栈溢出;:kconfig:option:`CONFIG_USERSPACE` 是正交的。

此功能仅检测监督者模式栈溢出,包括处理系统调用时的栈溢出。它不保证内核没有被破坏。监督者模式下的任何栈溢出都应被视为致命错误,无法对整个系统的完整性做出断言。

用户模式下的栈溢出是可恢复的(从内核的角度来看),不需要特殊配置;:kconfig:option:`CONFIG_HW_STACK_PROTECTION` 仅适用于在 CPU 处于监督者模式时捕获溢出。

基于 CPU 的栈溢出检测 (CPU-based stack overflow detection)
----------------------------------------------------------

如果我们通过特殊的 CPU 寄存器(如 ARM 的 SPLIM)检测监督者模式下的栈溢出,则默认值就足够了。



基于保护区域的栈溢出检测 (Guard-based stack overflow detection)
--------------------------------------------------------------

我们通过位于栈缓冲区之前的特殊内存保护区域检测监督者模式栈溢出,该区域在写入时生成异常。保留内存将用于保护区域。

:c:macro:`ARCH_KERNEL_STACK_RESERVED` 应定义为内存保护区域的最小大小。在大多数 ARM CPU 上,这是 32 字节。:c:macro:`ARCH_KERNEL_STACK_OBJ_ALIGN` 也应设置为此区域所需的对齐方式。

基于 MMU 的系统不应为保护区域保留 RAM,而应在每个栈映射到地址空间时,在栈下方简单地留下一个不存在的虚拟页。栈对象仍需要正确对齐并调整大小到页粒度。

.. code-block:: none

   +-----------------------------+ <- thread.stack_obj
   | Guard reserved memory       | } K_KERNEL_STACK_RESERVED
   +-----------------------------+
   | Guard carve-out             |
   |.............................| <- thread.stack_info.start
   | Stack buffer                |
   .                             .

内核栈的保护区域分离是不常见的,如果可能应该避免。它们往往需要用于两种情况:

* 同一个栈可能会被重新利用来托管用户线程,在这种情况下
  the guard is unnecessary and shouldn't be unconditionally reserved.
  This is the case when privilege elevation stacks are not inside the stack
  object.

* The required guard size is variable and depends on context. For example, some
  ARM CPUs have lazy floating point stacking during exceptions and may
  decrement the stack pointer by a large value without writing anything,
  completely overshooting a minimally-sized guard and corrupting adjacent
  memory. Rather than unconditionally reserving a larger guard, the extra
  memory is carved out if the thread uses floating point.

User mode enabled
=================

Enabling user mode activates two new requirements:

* 必须分配一个单独的固定大小的特权模式栈,由 :kconfig:option:`CONFIG_PRIVILEGED_STACK_SIZE` 指定,用户线程无法访问。在处理系统调用时,内核将其用作栈。如果实现了栈保护,则必须能够在其之前放置一个栈保护区域,如有必要,支持分离。

* 内存保护硬件必须能够编程一个完全覆盖线程栈缓冲区的区域,在 ``thread.stack_info`` 中跟踪。这意味着 :c:macro:`ARCH_THREAD_STACK_SIZE_ADJUST()` 需要向上取整请求的栈大小,以便区域可以覆盖它,并且 :c:macro:`ARCH_THREAD_STACK_OBJ_ALIGN()` 也根据内存保护硬件的粒度指定。

如果内存保护硬件要求所有内存区域的大小都是 2 的幂,并与它们自己的大小对齐,这就变得更加复杂。这在较旧的 MPU 上很常见,并且通过 :kconfig:option:`CONFIG_MPU_REQUIRES_POWER_OF_TWO_ALIGNMENT` 已知。

``thread.stack_info`` 始终跟踪栈对象的用户可访问部分,使用其中存储的范围编程具有用户访问权限的内存保护区域必须始终是正确的。

非 2 的幂内存区域要求 (Non power-of-two memory region requirements)
------------------------------------------------------------------

在没有 2 的幂区域要求的系统上,由 :c:macro:`K_THREAD_STACK_RESERVED` 定义的线程栈保留内存区域可用于包含特权模式栈。布局可能类似于:

.. code-block:: none

   +------------------------------+ <- thread.stack_obj
   | Other platform data          |
   +------------------------------+
   | Guard region (if enabled)    |
   +------------------------------+
   | Guard carve-out (if needed)  |
   |..............................|
   | Privilege elevation stack    |
   +------------------------------| <- thread.stack_obj +
   | Stack buffer                 |      K_THREAD_STACK_RESERVED =
   .                              .      thread.stack_info.start

保护区域和任何分离(如果需要)将在创建线程时配置为只读区域。

* 如果线程是监督者线程,特权提升区域只是额外的栈内存。溢出最终会崩溃到保护区域中。

* 如果线程在用户模式下运行,将配置内存保护区域以允许用户线程访问栈缓冲区,但不允许访问其前后的任何内容。用户模式下的溢出将崩溃到特权提升栈中,用户线程无权访问该栈。处理系统调用时的溢出将崩溃到保护区域中。

在 MMU 系统上不应有物理保护;特权模式栈将映射到内核内存中,栈缓冲区在内存的用户部分,每个下方都有不存在的虚拟保护页来捕获运行时栈溢出。

其他平台数据可能存储在保护区域之前,但这是高度
discouraged if such data could be stored in ``thread.arch`` somewhere.

:c:macro:`ARCH_THREAD_STACK_RESERVED` will need to be defined to capture
the size of the reserved region containing platform data, privilege elevation
stacks, and guards. It must be appropriately sized such that an MPU region
to grant user mode access to the stack buffer can be placed immediately
after it.

Power-of-two memory region requirements
---------------------------------------

Thread stack objects must be sized and aligned to the same power of two,
without any reserved memory to allow efficient packing in memory. Thus,
any guards in the thread stack must be completely carved out, and the
privilege elevation stack must be allocated elsewhere.

:c:macro:`ARCH_THREAD_STACK_SIZE_ADJUST()` and
:c:macro:`ARCH_THREAD_STACK_OBJ_ALIGN()` should both be defined to
:c:macro:`Z_POW2_CEIL()`. :c:macro:`K_THREAD_STACK_RESERVED` must be 0.

对于特权栈,必须启用 :kconfig:option:`CONFIG_GEN_PRIV_STACKS`。对于在系统中找到的每个线程栈,会生成一个相应的固定大小的内核栈,用于处理系统调用。可以使用 :c:func:`z_priv_stack_find()` 在运行时根据线程栈地址快速查找特权栈的地址。这些栈的布局方式与其他仅限内核的栈相同。

.. code-block:: none

   +-----------------------------+ <- z_priv_stack_find(thread.stack_obj)
   | Reserved memory             | } K_KERNEL_STACK_RESERVED
   +-----------------------------+
   | Guard carve-out (if needed) |
   |.............................|
   | Privilege elevation stack   |
   |                             |
   +-----------------------------+ <- z_priv_stack_find(thread.stack_obj) +
                                        K_KERNEL_STACK_RESERVED +
                                        CONFIG_PRIVILEGED_STACK_SIZE

   +-----------------------------+ <- thread.stack_obj
   | MPU guard carve-out         |
   | (supervisor mode only)      |
   |.............................| <- thread.stack_info.start
   | Stack buffer                |
   .                             .

线程栈对象中的保护区域分离仅在线程以监督者模式运行时使用。如果线程降至用户模式,则没有保护,整个对象用作栈缓冲区,具有对关联用户模式线程的完全访问权限,并适当更新 ``thread.stack_info``。

用户模式线程 (User Mode Threads)
**********************************

要支持用户模式线程,需要实现几个内核到架构的 API,系统必须启用 :kconfig:option:`CONFIG_ARCH_HAS_USERSPACE` 选项。请参阅每个函数的文档以获取更多详细信息:

* :c:func:`arch_buffer_validate` 用于测试当前线程是否对特定内存区域具有访问权限

* :c:func:`arch_user_mode_enter` 将不可逆地将监督者线程降至用户模式权限。必须擦除栈。

* :c:func:`arch_syscall_oops` 在无法验证系统调用参数时生成内核 oops,以使 oops 看起来是从用户线程中调用系统调用的地方生成的

* :c:func:`arch_syscall_invoke0` 到 :c:func:`arch_syscall_invoke6` 使用适当数量的参数调用系统调用,所有参数都必须在通过寄存器进行特权提升期间传递。

* :c:func:`arch_is_user_context` 如果 CPU 当前以用户模式运行,则返回非零

* :c:func:`arch_mem_domain_max_partitions_get` 指示内存域的最大区域数。MMU 系统具有无限数量,
  MPU systems have constraints on this.

Some architectures may need to update software memory management structures
or modify hardware registers on another CPU when memory domain APIs are invoked.
If so, :kconfig:option:`CONFIG_ARCH_MEM_DOMAIN_SYNCHRONOUS_API` must be selected by the
architecture and some additional APIs must be implemented. This is common
on MMU systems and uncommon on MPU systems:

* :c:func:`arch_mem_domain_thread_add`

* :c:func:`arch_mem_domain_thread_remove`

* :c:func:`arch_mem_domain_partition_add`

* :c:func:`arch_mem_domain_partition_remove`

请参阅这些 API 的 doxygen 文档以获取详细信息。

除了实现这些 API 之外,还有一些其他任务:

* :c:func:`_new_thread` 需要在用户模式下使用 :c:macro:`K_USER` 生成线程

* 在上下文切换时,应通过在内存管理硬件中进行适当的配置更改,将传出线程的栈内存标记为用户模式不可访问。同样,传入线程的栈内存应标记为可访问。这确保线程不能干扰其他线程的栈。

* 在上下文切换时,系统需要在传入和传出线程的内存域之间切换。

* 线程栈区域必须包括内核栈区域。这应该始终对用户线程不可访问。进行系统调用时将使用此栈。对于所有线程,这应该是固定大小的,并且必须足够大以处理任何系统调用。

* 需要建立软件中断或某种特权提升机制。这与 _arch_syscall_invoke 宏的实现方式密切相关。在系统调用时,需要在 _k_syscall_table 中查找适当的处理程序函数。错误的系统调用 ID 应跳转到 :c:enum:`K_SYSCALL_BAD` 处理程序。完成系统调用后,必须注意不要将任何寄存器状态泄漏回用户模式。

GDB Stub
********

要在新架构上为远程调试启用 GDB stub:

#. 在适当的架构包含目录(``include/arch/<arch>/gdbstub.h``)下创建一个新的 ``gdbstub.h`` 头文件。

   * 创建一个新的结构体 ``struct gdb_ctx`` 作为 GDB 上下文。

     * 必须定义一个名为 ``exception`` 的 ``unsigned int`` 类型成员来存储 GDB 异常原因。在进入 :c:func:`z_gdb_main_loop` 之前需要设置此值。

     * 架构可以根据 GDB stub 功能的需要定义尽可能多的成员。

     * 需要将指向此结构体的指针传递给 :c:func:`z_gdb_main_loop`,该指针将传递给其他 GDB stub 函数。

#. 用于进入和退出 GDB stub 主循环的函数。

   * 如果架构依赖中断来服务断点,则需要实现中断服务例程(ISR),它将作为 GDB stub 主循环的入口点。

   * 这些函数需要保存和恢复上下文,以便代码执行可以继续,就好像没有遇到断点一样。

   * 这些函数需要在保存执行上下文后调用 :c:func:`z_gdb_main_loop` 以进入 GDB stub 主循环来接收命令
     from GDB.

   * Before calling :c:func:`z_gdb_main_loop`, :c:member:`gdb_ctx.exception`
     must be set to specify the exception reason.

#. Implement necessary functions to support GDB stub functionality:

   * :c:func:`arch_gdb_init`

     * This needs to initialize necessary bits to support GDB stub functionality,
       for example, setting up the GDB context and connecting debug interrupts.

     * This must stop code execution via architecture specific method (e.g.
       raising debug interrupts). This allows GDB to connect during boot.

   * :c:func:`arch_gdb_continue`

     * 当 GDB 发送 ``c`` 或 ``continue`` 命令继续代码执行时,将调用此函数。

   * :c:func:`arch_gdb_step`

     * 当 GDB 发送 ``si`` 或 ``stepi`` 命令执行一条机器指令后再返回 GDB 提示符时,将调用此函数。

   * 硬件寄存器读/写函数:

     * 由于 GDB stub 在目标上运行,因此需要缓存对硬件寄存器的操作以避免影响 GDB stub 的执行。可以将其视为上下文切换,其中执行上下文更改为 GDB stub。因此,需要存储上下文切换前运行线程的寄存器值。对寄存器值的操作只能对此缓存副本进行。然后,在切换回先前运行的线程之前,将更新的值写入硬件寄存器。

     * :c:func:`arch_gdb_reg_readall`

       * 这会收集所有将出现在 ``g``/``G`` 包中的硬件寄存器值,这些包将发送回 GDB。G 包的格式是特定于架构的。请咨询 GDB 了解预期内容。

       * 请注意,对于大多数架构,必须返回有效的 G 包并发送到 GDB。如果将长度不正确的包发送到 GDB,GDB 将中止调试会话。

     * :c:func:`arch_gdb_reg_writeall`

       * 这会接收 GDB 发送的 G 包,并使用 G 包中的值填充硬件寄存器。

     * :c:func:`arch_gdb_reg_readone`

       * 这会读取一个硬件寄存器的值并将结果发送到 GDB。

     * :c:func:`arch_gdb_reg_writeone`

       * 这会写入从 GDB 接收的一个硬件寄存器的值。

   * 断点 (Breakpoints):

     * :c:func:`arch_gdb_add_breakpoint` 和 :c:func:`arch_gdb_remove_breakpoint`

     * GDB 可能决定使用软件断点,它会修改断点位置的内存,用软件断点或陷阱指令替换指令。然后,一旦执行到达断点,GDB 将恢复内存内容。GDB 默认支持这一点,通常不需要在架构代码中处理软件断点(其中断点类型为 ``0``)。

     * 如果代码在 ROM 或 flash 中无法在运行时修改,则需要硬件断点(类型 ``1``)。请参阅架构数据表了解如何启用硬件断点。

     * If hardware breakpoints are not supported by the architecture,
       there is no need to implement these in architecture code.
       GDB will then rely on software breakpoints.

#. For architecture where certain memory regions are not accessible,
   an array named :c:var:`gdb_mem_region_array` of type
   :c:struct:`gdb_mem_region` needs to be defined to specify regions
   that are accessible. For each array item:

   * :c:member:`gdb_mem_region.start` specifies the start of a memory
     region.

   * :c:member:`gdb_mem_region.end` specifies the end of a memory
     region.

   * :c:member:`gdb_mem_region.attributes` 指定内存区域的权限。

     * :c:macro:`GDB_MEM_REGION_RO`: 区域为只读。

     * :c:macro:`GDB_MEM_REGION_RW`: 区域为读写。

   * :c:member:`gdb_mem_region.alignment` 指定内存区域的读/写对齐。如果没有对齐要求并且可以逐字节进行读/写,则使用 ``0``。

API 参考 (API Reference)
*************************

定时 (Timing)
=============

.. doxygengroup:: arch-timing

线程 (Threads)
===============

.. doxygengroup:: arch-threads

.. doxygengroup:: arch-tls

电源管理 (Power Management)
============================

.. doxygengroup:: arch-pm

对称多处理 (Symmetric Multi-Processing)
========================================

.. doxygengroup:: arch-smp

中断 (Interrupts)
==================

.. doxygengroup:: arch-irq

用户空间 (Userspace)
=====================

.. doxygengroup:: arch-userspace

内存管理 (Memory Management)
=============================

.. doxygengroup:: arch-mmu

杂项架构 API (Miscellaneous Architecture APIs)
===============================================

.. doxygengroup:: arch-misc

GDB Stub API
=============

.. doxygengroup:: arch-gdbstub

