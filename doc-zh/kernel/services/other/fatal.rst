.. _fatal:

致命错误
########

源代码中触发的软件错误
*********************

Zephyr 提供了多种方法来通过构建时检查 (build-time checks)、条件编译断言 (conditionally compiled assertions)
或故意调用的恐慌 (panic) 或 oops 条件来诱发致命错误条件。

运行时断言
=========

Zephyr 提供了一些宏来执行可以条件编译的运行时断言。它们的定义可以在
:zephyr_file:`include/zephyr/sys/__assert.h` 中找到。

通过将 ``__ASSERT_ON`` 预处理器符号设置为非零值来启用断言。有两种方法可以做到这一点：

- 使用 :kconfig:option:`CONFIG_ASSERT` 和 :kconfig:option:`CONFIG_ASSERT_LEVEL` kconfig 选项。
- 将 ``-D__ASSERT_ON=<level>`` 添加到项目的 CFLAGS，可以在构建命令行或 CMakeLists.txt 中添加。

如果两者都使用，``__ASSERT_ON`` 方法优先于 kconfig 选项。

指定断言级别为 1 会导致编译器发出警告，表明内核包含调试类型的 ``__ASSERT()`` 语句；
发出此提醒是因为断言代码通常不会出现在最终产品中。指定断言级别 2 会抑制这些警告。

在运行 Zephyr 测试用例时，断言默认启用，如 :kconfig:option:`CONFIG_TEST` 选项所配置。

遇到失败的断言时要执行的策略由 :c:func:`assert_post_action` 的实现控制。
Zephyr 提供了一个具有弱链接的默认实现，如果失败断言的线程在用户模式下运行，则调用内核 oops，
否则调用内核 panic。

__ASSERT()
----------

``__ASSERT()`` 宏可以在内核和应用程序代码中使用，以执行可选的运行时检查，如果检查未通过，
将引发致命错误。该宏接受一个字符串消息，该消息将被打印以提供断言的上下文。
此外，内核将打印评估的表达式代码的文本表示，以及可以找到断言的文件和行号。

例如：

.. code-block:: c

  __ASSERT(foo == 0xF0CACC1A, "Invalid value of foo, got 0x%x", foo);

如果在运行时 ``foo`` 具有某个意外值，产生的错误可能如下所示：

.. code-block:: none

	ASSERTION FAIL [foo == 0xF0CACC1A] @ ZEPHYR_BASE/tests/kernel/fatal/src/main.c:367
		Invalid value of foo, got 0xdeadbeef
	[00:00:00.000,000] <err> os: r0/a1:  0x00000004  r1/a2:  0x0000016f  r2/a3:  0x00000000
	[00:00:00.000,000] <err> os: r3/a4:  0x00000000 r12/ip:  0x00000000 r14/lr:  0x00000a6d
	[00:00:00.000,000] <err> os:  xpsr:  0x61000000
	[00:00:00.000,000] <err> os: Faulting instruction address (r15/pc): 0x00009fe4
	[00:00:00.000,000] <err> os: >>> ZEPHYR FATAL ERROR 4: Kernel panic
	[00:00:00.000,000] <err> os: Current thread: 0x20000414 (main)
	[00:00:00.000,000] <err> os: Halting system

__ASSERT_EVAL()
---------------

``__ASSERT_EVAL()`` 宏也可以在内核和应用程序代码中使用，对其参数的求值具有特殊的语义。

它使用 ``__ASSERT()`` 宏，但具有一些额外的灵活性。它允许开发人员根据 ``__ASSERT()`` 宏
是否启用来指定不同的操作。这对于防止编译器生成关于仅在 ``__ASSERT()`` 中使用的变量
被分配值但在 ``__ASSERT()`` 宏禁用时未使用的注释（错误、警告或备注）特别有用。

考虑以下示例：

.. code-block:: c

  int x;
  x = foo();
  __ASSERT(x != 0, "foo() returned zero!");

如果 ``__ASSERT()`` 被禁用，则 'x' 被分配了一个值，但从未使用。这种情况可以使用 __ASSERT_EVAL() 宏解决。

.. code-block:: c

  __ASSERT_EVAL ((void) foo(),
  		 int x = foo(),
                 x != 0,
                 "foo() returned zero!");

第一个参数告诉 ``__ASSERT_EVAL()`` 如果 ``__ASSERT()`` 被禁用该做什么。第二个参数告诉
``__ASSERT_EVAL()`` 如果 ``__ASSERT()`` 被启用该做什么。第三和第四个参数是它传递给 ``__ASSERT()`` 的参数。

__ASSERT_NO_MSG()
-----------------

``__ASSERT_NO_MSG()`` 宏可用于执行报告失败测试及其位置的断言，但缺少提供给用户用于
诊断问题的额外调试信息；不鼓励使用它。

构建断言
========

Zephyr 提供了一个用于执行构建时断言检查的宏。它完全在编译时求值，并始终进行检查。

BUILD_ASSERT()
--------------

这与 C 的 ``_Static_assert`` 或 C++ 的 ``static_assert`` 具有相同的语义。
如果求值失败，编译器将生成构建错误。如果编译器支持，将打印提供的消息以提供更多上下文。

与 ``__ASSERT()`` 不同，消息必须是静态字符串，不带 :c:func:`printf()` 样式的格式代码或额外参数。

例如，假设此检查失败：

.. code-block:: c

	BUILD_ASSERT(FOO == 2000, "Invalid value of FOO");

使用 GCC，输出类似于：

.. code-block:: none

	tests/kernel/fatal/src/main.c: In function 'test_main':
	include/toolchain/gcc.h:28:37: error: static assertion failed: "Invalid value of FOO"
	 #define BUILD_ASSERT(EXPR, MSG) _Static_assert(EXPR, "" MSG)
					 ^~~~~~~~~~~~~~
	tests/kernel/fatal/src/main.c:370:2: note: in expansion of macro 'BUILD_ASSERT'
	  BUILD_ASSERT(FOO == 2000,
	  ^~~~~~~~~~~~~~~~

内核 Oops
=========

内核 oops 是由 :c:func:`k_oops()` 调用的软件触发的致命错误。这应该用于指示应用程序逻辑中
的不可恢复条件。

生成的致命错误原因代码将是 ``K_ERR_KERNEL_OOPS``。

内核 Panic
==========

内核错误是由 :c:func:`k_panic()` 调用的软件触发的致命错误。这应该用于指示 Zephyr 内核
处于不可恢复状态。如果内核遇到 panic 条件，:c:func:`k_sys_fatal_error_handler()` 的实现
不应返回，因为整个系统需要重置。

在用户模式下运行的线程不允许调用 :c:func:`k_panic()`，这样做会生成内核 oops。
否则，生成的致命错误原因代码将是 ``K_ERR_KERNEL_PANIC``。

异常
****

虚假中断
========

如果 CPU 在未使用 ``IRQ_CONNECT()`` 或 :c:func:`irq_connect_dynamic()` 安装处理程序的中断线上
接收到硬件中断，则内核将生成原因代码为 ``K_ERR_SPURIOUS_IRQ()`` 的致命错误。

栈溢出
======

如果线程将更多数据推送到其执行栈上超过其栈缓冲区提供的容量，内核可能能够检测到这种情况，
并生成原因代码为 ``K_ERR_STACK_CHK_FAIL`` 的致命错误。

如果线程在用户模式下运行，则始终会捕获栈溢出，因为线程根本没有权限写入栈缓冲区外部的相邻内存地址。
由于这是由内存保护硬件强制执行的，因此不存在数据损坏到线程无法写入的内存的风险。

如果线程在超级用户模式下运行，或者未启用 :kconfig:option:`CONFIG_USERSPACE`，
则根据配置，可能会或可能不会捕获栈溢出。某些架构支持 :kconfig:option:`CONFIG_HW_STACK_PROTECTION`，
并将在超级用户模式下捕获栈溢出，包括代表用户线程处理系统调用时。通常，这是通过专用 CPU 功能
或紧邻栈缓冲区的只读 MMU/MPU 保护区域实现的。以这种方式捕获的栈溢出可以检测到溢出，
但不能保证防止数据损坏，应被视为影响整个系统健康的非常严重的条件。

如果平台缺少内存管理硬件支持，:kconfig:option:`CONFIG_STACK_SENTINEL` 是一种纯软件栈溢出检测功能，
它定期检查栈缓冲区末尾的哨兵值 (sentinel value) 是否已损坏。它不需要硬件支持，但不提供防止数据损坏的保护。
由于检查通常在中断退出时完成，因此在栈实际溢出后可能会在相当长的时间后才检测到溢出。

最后，Zephyr 通过 :kconfig:option:`CONFIG_STACK_CANARIES` 支持 GCC 编译器栈金丝雀 (stack canaries)。
如果启用，编译器将在函数栈帧中插入在引导时随机生成的金丝雀值，在函数退出时检查金丝雀是否未被覆盖。
如果检查失败，编译器调用 :c:func:`__stack_chk_fail()`，其 Zephyr 实现调用致命栈溢出错误。
在这种情况下，错误并不表示整个栈缓冲区已溢出，而是表示当前函数栈帧已损坏。
有关更多详细信息，请参阅编译器文档。

其他异常
========

任何其他类型的未处理 CPU 异常都将生成错误代码 ``K_ERR_CPU_EXCEPTION``。

致命错误处理
************

遇到致命错误时要执行的策略由 :c:func:`k_sys_fatal_error_handler()` 函数的实现确定。
此函数具有弱链接的默认实现，该实现调用 ``LOG_PANIC()`` 转储所有待处理的日志消息，
然后无条件地使用 :c:func:`k_fatal_halt()` 停止系统。

应用程序可以通过覆盖 :c:func:`k_sys_fatal_error_handler()` 的实现来自由实现自己的错误处理策略。
如果实现返回，故障线程将被中止，系统将继续运行。有关其他详细信息和约束，请参阅此函数的文档。

API 参考
********

.. doxygengroup:: fatal_apis
