.. _clang:

Clang 静态分析器支持
####################

Clang Static Analyzer 构建在 Clang 和 LLVM 之上。
严格来说，分析器是 Clang 的一部分，因为 Clang 包含一组可重用的 C++ 库，
用于构建强大的源代码级工具。Clang Static Analyzer 使用的静态分析引擎是一个 Clang 库，
并具有在不同上下文和不同客户端中重用的能力。

LLVM 提供了多种在代码库上运行分析器的方法，
可以通过专用工具集（scan-build 和 analyze-build），
也可以通过在运行 clang 时使用命令行参数（'--analyze'）。

- 'scan-build' 工具对于使用简单的 $CC makefile 变量的项目来说是最方便的方式，
  因为它会包装和替换编译器调用来执行分析。

- 'analyze-build' 工具是 'scan-build' 的子工具，它仅依赖 'compile_commands.json' 数据库来执行分析。

- clang 选项 '--analyze' 将在构建的同时运行分析器，但不会生成目标文件，使得任何链接阶段都无法进行。
  在我们的情况下，第一个链接阶段将失败并停止分析。

由于 Zephyr 项目具有复杂的构建基础设施，使用 'analyze-build' 调用 clang 分析器是分析 Zephyr 项目的最简单方法。

`Clang static analyzer documentation <https://clang.llvm.org/docs/ClangStaticAnalyzer.html>`__

安装 clang 分析器
*****************

'scan-build' 及其子工具 'analyze-build' 作为 llvm 二进制文件的一部分原生提供。
请确保将二进制目录添加到你的 PATH 中。

'scan-build' 也可作为独立的 Python 包在 `pypi <https://pypi.org/project/scan-build/>`__ 上获取。

.. code-block:: shell

    pip install scan-build

运行 clang 静态分析器
*********************

.. note::

  分析器要求项目使用 LLVM 工具链构建，并生成 'compile_commands.json' 数据库。

要运行 clang 静态分析器，应在调用 :ref:`west build <west-building>` 时传递 ``-DZEPHYR_SCA_VARIANT=clang`` 参数，
以及 llvm 工具链参数，例如：

.. zephyr-app-commands::
   :zephyr-app: samples/userspace/hello_world_user
   :board: qemu_x86
   :gen-args: -DZEPHYR_TOOLCHAIN_VARIANT=llvm -DLLVM_TOOLCHAIN_PATH=... -DZEPHYR_SCA_VARIANT=clang
   :goals: build
   :compact:

.. note::

  默认情况下，clang 静态分析器生成 html 报告，但可以通过选项选择各种其他输出格式（sarif、plist、html）。

配置 clang 静态分析器
*********************

可以使用特定选项控制 Clang 静态分析器。
要获取可用选项的详尽列表，请参考 'analyze-build' 帮助和 'scan-build' 帮助。

.. code-block:: shell

    analyze-build --help

默认已激活的选项：

* --analyze-headers：同时分析 #included 文件中的函数。

.. list-table::
   :header-rows: 1

   * - 参数
     - 描述
   * - ``CLANG_SCA_OPTS``
     - 以分号分隔的 'analyze-build' 选项列表。

这些参数可以在命令行上传递，或设置为环境变量。

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :board: stm32h573i_dk
   :gen-args: -DZEPHYR_TOOLCHAIN_VARIANT=llvm -DLLVM_TOOLCHAIN_PATH=... -DZEPHYR_SCA_VARIANT=clang -DCLANG_SCA_OPTS="--sarif;--verbose"
   :goals: build
   :compact:
