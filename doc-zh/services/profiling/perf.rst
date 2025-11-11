.. _profiling-perf:

Perf
####

Perf 是一个基于栈追踪的性能分析工具。它可用于轻量级性能分析,代码开销最小。(Perf is a profiler tool based on stack tracing. It can be used for lightweight profiling with minimal code overhead.)

工作原理 (Work Principle)
**************************

``perf record`` shell 命令使用 perf 追踪器函数启动一个定时器。定时器由中断驱动,因此 perf 追踪器函数在中断期间被调用。Zephyr 核心在调用中断处理程序之前,会将返回地址和帧指针保存在中断栈或 ``callee_saved`` 结构中。因此,perf 追踪函数通过使用返回地址和帧指针来进行栈追踪。(The ``perf record`` shell command starts a timer with the perf tracer function. Timers are driven by interrupts, so the perf tracer function is called during an interruption. The Zephyr core saves the return address and frame pointer in the interrupt stack or ``callee_saved`` structure before calling the interrupt handler. Thus, the perf trace function makes stack traces by using the return address and frame pointer.)

:zephyr_file:`scripts/profiling/stackcollapse.py` 脚本可用于将栈追踪中的返回地址转换为函数名(使用 ELF 文件中的符号),并以 `FlameGraph`_ 期望的格式打印它们。(The :zephyr_file:`scripts/profiling/stackcollapse.py` script can be used to convert return addresses in the stack trace to function names using symbols from the ELF file, and to prints them in the format expected by `FlameGraph`_.)

配置 (Configuration)
*********************

您可以使用以下选项配置此模块: (You can configure this module using the following options:)

* :kconfig:option:`CONFIG_PROFILING_PERF`: 启用此模块。此选项将 ``perf`` 命令添加到 shell。(Enables the module. This option adds the ``perf`` command to the shell.)

* :kconfig:option:`CONFIG_PROFILING_PERF_BUFFER_SIZE`: 设置 perf 缓冲区的大小,样本在打印前保存在此缓冲区中。(Sets the size of the perf buffer where samples are saved before printing.)

使用方法 (Usage)
*****************

有关如何使用 perf 工具的示例,请参阅 :zephyr:code-sample:`profiling-perf` 示例。(Refer to the :zephyr:code-sample:`profiling-perf` sample for an example of how to use the perf tool.)

 .. _FlameGraph: https://github.com/brendangregg/FlameGraph/
