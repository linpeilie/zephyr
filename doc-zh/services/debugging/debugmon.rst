.. _debugmon:

Cortex-M调试监视器 (Cortex-M Debug Monitor)
############################################

监视器模式调试是Cortex-M的一个功能,提供了一种非停止的调试方法 (Monitor mode debugging is a Cortex-M feature, that provides a non-halting approach to debugging)。有了这个功能,即使在断点上等待时,也可以继续执行高优先级中断 (With this it's possible to continue the execution of high-priority interrupts, even when waiting on a breakpoint)。
这种策略使得调试时间敏感的软件成为可能,否则当核心停止时这些软件会崩溃(例如需要保持通信链路活动的应用程序) (This strategy makes it possible to debug time-sensitive software, that would otherwise crash when the core halts (e.g. applications that need to keep communication links alive))。

Zephyr提供了启用和配置调试监视器异常的支持 (Zephyr provides support for enabling and configuring the Debug Monitor exception)。
它还包含一个中断的现成实现,可以与SEGGER J-Link调试器一起使用 (It also contains a ready implementation of the interrupt, which can be used with SEGGER J-Link debuggers)。

配置 (Configuration)
*************

使用以下选项配置此模块 (Configure this module using the following options)。

* :kconfig:option:`CONFIG_CORTEX_M_DEBUG_MONITOR_HOOK`: 启用该模块 (enable the module)。此选项本身需要调试监视器中断的实现,该中断将在程序每次进入断点时执行 (This option, by itself, requires an implementation of debug monitor interrupt that will be executed every time the program enters a breakpoint)。

使用SEGGER调试探针,可以使用SEGGER提供的现成中断实现 (With a SEGGER debug probe, it's possible to use a ready, SEGGER-provided implementation of the interrupt)。

* :kconfig:option:`CONFIG_SEGGER_DEBUGMON`: 启用SEGGER调试监视器中断 (enables SEGGER debug monitor interrupt)。可以与SEGGER JLinkGDBServer和SEGGER调试探针一起使用 (Can be used with SEGGER JLinkGDBServer and a SEGGER debug probe)。


用法 (Usage)
*****

当启用监视器模式调试时,进入断点不会停止处理器,而是生成一个中断,其ISR在 ``z_arm_debug_monitor`` 符号下实现 (When monitor mode debugging is enabled, entering a breakpoint will not halt the processor, but rather generate an interrupt with ISR implemented under ``z_arm_debug_monitor`` symbol)。:kconfig:option:`CONFIG_CORTEX_M_DEBUG_MONITOR_HOOK` 配置将此中断配置为最低可用优先级,这将允许其他中断在处理器在断点上旋转时执行 (:kconfig:option:`CONFIG_CORTEX_M_DEBUG_MONITOR_HOOK` config configures this interrupt to be the lowest available priority, which will allow other interrupts to execute while processor spins on a breakpoint)。

使用SEGGER提供的ISR (Using SEGGER-provided ISR)
=========================

:kconfig:option:`CONFIG_SEGGER_DEBUGMON` 提供的现成实现提供了使用常规GDB命令在监视器模式下调试所需的功能 (The ready implementation provided with :kconfig:option:`CONFIG_SEGGER_DEBUGMON` provides functionality required to debug in the monitor mode using regular GDB commands)。
配置SEGGER调试监视器的步骤 (Steps to configure SEGGER debug monitor):

1. 使用启用了 :kconfig:option:`CONFIG_CORTEX_M_DEBUG_MONITOR_HOOK` 和 :kconfig:option:`CONFIG_SEGGER_DEBUGMON` 配置构建示例 (Build a sample with :kconfig:option:`CONFIG_CORTEX_M_DEBUG_MONITOR_HOOK`` and :kconfig:option:`CONFIG_SEGGER_DEBUGMON` configs enabled)。

2. 将JLink GDB服务器连接到目标 (Attach JLink GDB server to the target)。
   Linux命令示例: ``JLinkGDBServerCLExe -device <device> -if swd`` (Example linux command: ``JLinkGDBServerCLExe -device <device> -if swd``)。

3. 使用您的GDB安装连接到服务器 (Connect to the server with your GDB installation)。
   Linux命令示例: ``arm-none-eabi-gdb --ex="file build/zephyr.elf" --ex="target remote localhost:2331"`` (Example linux command: ``arm-none-eabi-gdb --ex="file build/zephyr.elf" --ex="target remote localhost:2331"``)。

4. 在GDB中使用命令启用监视器模式调试: ``monitor exec SetMonModeDebug=1`` (Enable monitor mode debugging in GDB using command: ``monitor exec SetMonModeDebug=1``)。

完成这些步骤后,使用常规gdb命令调试您的程序 (After these steps use regular gdb commands to debug your program)。


使用其他自定义ISR (Using other custom ISR)
======================
为了提供自定义调试监视器中断,请覆盖 ``z_arm_debug_monitor`` 符号 (In order to provide a custom debug monitor interrupt, override ``z_arm_debug_monitor`` symbol)。此外,需要手动配置一些寄存器 (Additionally, manual configuration of some registers is required)
(参见 :zephyr:code-sample:`debugmon` 示例) (see :zephyr:code-sample:`debugmon` sample)。
