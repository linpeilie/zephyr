.. _thread_analyzer:

线程分析器 (Thread analyzer)
#############################

线程分析器模块启用跟踪线程信息所需的所有Zephyr选项,例如线程栈大小使用情况和其他运行时线程统计信息 (The thread analyzer module enables all the Zephyr options required to track the thread information, e.g. thread stack size usage and other runtime thread runtime statistics)。

当应用程序调用 :c:func:`thread_analyzer_run` 或 :c:func:`thread_analyzer_print` 时,会按需执行分析 (The analysis is performed on demand when the application calls :c:func:`thread_analyzer_run` or :c:func:`thread_analyzer_print`)。

例如,要在启用线程分析器的情况下构建同步示例,请执行以下操作 (For example, to build the synchronization sample with Thread Analyser enabled, do the following):

   .. zephyr-app-commands::
      :zephyr-app: samples/synchronization/
      :board: qemu_x86
      :goals: build
      :gen-args: -DCONFIG_QEMU_ICOUNT=n -DCONFIG_THREAD_ANALYZER=y \
                   -DCONFIG_THREAD_ANALYZER_USE_PRINTK=y -DCONFIG_THREAD_ANALYZER_AUTO=y \
                   -DCONFIG_THREAD_ANALYZER_AUTO_INTERVAL=5


当您在Qemu中运行生成的应用程序时,您将从线程分析器获得额外的信息 (When you run the generated application in Qemu, you will get the additional information from Thread Analyzer)::


	thread_a: Hello World from cpu 0 on qemu_x86!
	Thread analyze:
	 thread_b            : STACK: unused 740 usage 284 / 1024 (27 %); CPU: 0 %
	 thread_analyzer     : STACK: unused 8 usage 504 / 512 (98 %); CPU: 0 %
	 thread_a            : STACK: unused 648 usage 376 / 1024 (36 %); CPU: 98 %
	 idle                : STACK: unused 204 usage 116 / 320 (36 %); CPU: 0 %
	thread_b: Hello World from cpu 0 on qemu_x86!
	thread_a: Hello World from cpu 0 on qemu_x86!
	thread_b: Hello World from cpu 0 on qemu_x86!
	thread_a: Hello World from cpu 0 on qemu_x86!
	thread_b: Hello World from cpu 0 on qemu_x86!
	thread_a: Hello World from cpu 0 on qemu_x86!
	thread_b: Hello World from cpu 0 on qemu_x86!
	thread_a: Hello World from cpu 0 on qemu_x86!
	Thread analyze:
	 thread_b            : STACK: unused 648 usage 376 / 1024 (36 %); CPU: 7 %
	 thread_analyzer     : STACK: unused 8 usage 504 / 512 (98 %); CPU: 0 %
	 thread_a            : STACK: unused 648 usage 376 / 1024 (36 %); CPU: 9 %
	 idle                : STACK: unused 204 usage 116 / 320 (36 %); CPU: 82 %
	thread_b: Hello World from cpu 0 on qemu_x86!
	thread_a: Hello World from cpu 0 on qemu_x86!
	thread_b: Hello World from cpu 0 on qemu_x86!
	thread_a: Hello World from cpu 0 on qemu_x86!
	thread_b: Hello World from cpu 0 on qemu_x86!
	thread_a: Hello World from cpu 0 on qemu_x86!
	thread_b: Hello World from cpu 0 on qemu_x86!
	thread_a: Hello World from cpu 0 on qemu_x86!
	Thread analyze:
	 thread_b            : STACK: unused 648 usage 376 / 1024 (36 %); CPU: 7 %
	 thread_analyzer     : STACK: unused 8 usage 504 / 512 (98 %); CPU: 0 %
	 thread_a            : STACK: unused 648 usage 376 / 1024 (36 %); CPU: 8 %
	 idle                : STACK: unused 204 usage 116 / 320 (36 %); CPU: 83 %
	thread_b: Hello World from cpu 0 on qemu_x86!
	thread_a: Hello World from cpu 0 on qemu_x86!
	thread_b: Hello World from cpu 0 on qemu_x86!


配置 (Configuration)
*************
使用以下选项配置此模块 (Configure this module using the following options)。

:kconfig:option:`CONFIG_THREAD_ANALYZER`
   启用该模块 (Enable the module)。
:kconfig:option:`CONFIG_THREAD_ANALYZER_USE_PRINTK`
   使用printk输出线程统计信息 (Use printk for thread statistics)。
:kconfig:option:`CONFIG_THREAD_ANALYZER_USE_LOG`
   使用日志记录器输出线程统计信息 (Use the logger for thread statistics)。
:kconfig:option:`CONFIG_THREAD_ANALYZER_AUTO`
   自动运行线程分析器 (Run the thread analyzer automatically)。
   使用此选项时,您不需要向应用程序添加任何代码 (You do not need to add any code to the application when using this option)。
:kconfig:option:`CONFIG_THREAD_ANALYZER_AUTO_INTERVAL`
   自动模式下,模块在连续打印线程分析之间休眠的时间 (The time for which the module sleeps between consecutive printing of thread analysis in automatic mode)。
:kconfig:option:`CONFIG_THREAD_ANALYZER_AUTO_STACK_SIZE`
  线程分析器自动线程的栈大小 (The stack for thread analyzer automatic thread)。
:kconfig:option:`CONFIG_THREAD_NAME`
  打印线程的名称而不是其ID (Print the name of the thread instead of its ID)。
:kconfig:option:`CONFIG_THREAD_RUNTIME_STATS`
  打印线程运行时数据,例如利用率 (Print thread runtime data such as utilization)。
  此选项由 :kconfig:option:`CONFIG_THREAD_ANALYZER` 自动选择 (This options is automatically selected by :kconfig:option:`CONFIG_THREAD_ANALYZER`)。
:kconfig:option:`CONFIG_THREAD_ANALYZER_LONG_FRAME_PER_INTERVAL`
  打印后重置最长帧值统计信息 (Reset Longest Frame value statistics after printing)。
  当使用 :kconfig:option:`SCHED_THREAD_USAGE_ANALYSIS` 获取平均和最长帧线程统计信息时,每次打印线程统计信息后将最长帧值重置为零 (When using :kconfig:option:`SCHED_THREAD_USAGE_ANALYSIS` to get average and longest frame thread statistics, reset the Longest Frame value to zero after each time printing the thread statistics)。这使得能够观察最近间隔内的最长帧,而不是自启动以来的最长帧 (This enables observation of the longest frame during the most recent interval rather than longest frame since startup)。

API文档 (API documentation)
*****************

.. doxygengroup:: thread_analyzer
