.. _coverage:

Generating coverage reports
###########################

使用覆盖率工具生成报告
###########################

在 Zephyr 中，你可以生成代码覆盖率报告，以分析给定测试或应用程序覆盖了代码的哪些部分。

可以通过两种方式来生成覆盖率报告：

- 在真实的嵌入式目标或 QEMU 中，使用 Zephyr 的 gcov 集成
- 在主机上直接生成，通过将你的应用程序编译为 POSIX 架构的本机可执行文件

Test coverage reports in embedded devices or QEMU
*************************************************

Overview
========
概述
====
`GCC GCOV <gcov_>`_ 是一个与 GCC 编译器配合使用的测试覆盖率工具，用于分析并生成程序的覆盖率报告，帮助你发现未被测试的代码路径，从而编写更高效、更快速的代码。

在 Zephyr 中，gcov 在应用运行时将覆盖率分析数据收集到 RAM（而不是文件系统）。由于覆盖率数据的收集和报告受可用 RAM 大小限制，目前只在嵌入式目标的 QEMU 仿真中启用该功能。

Details
=======
详细说明
========
启用该功能有两个部分：一是为设备启用覆盖率支持，二是在测试应用中启用覆盖率。如前所述，gcov 的代码覆盖率功能受可用 RAM 的影响。因此在为设备启用覆盖率时，请确保该设备有足够的 RAM。例如像 frdm_k64f 这样的小型设备可以运行简单的测试应用，但一些占用更多内存的复杂测试用例在启用覆盖率时可能会崩溃。

要为设备启用覆盖率支持，请在 Kconfig.board 文件中选择 :kconfig:option:`CONFIG_HAS_COVERAGE_SUPPORT`。

要为特定测试应用生成覆盖率报告，请设置 :kconfig:option:`CONFIG_COVERAGE`。

Steps to generate code coverage reports
=======================================

These steps will produce an HTML coverage report for a single application.

1. Build the code with CONFIG_COVERAGE=y.

   .. zephyr-app-commands::
      :board: mps2/an385
      :gen-args: -DCONFIG_COVERAGE=y -DCONFIG_COVERAGE_DUMP=y
      :goals: build
      :compact:

#. 将模拟器输出捕获到日志文件中。在覆盖率转储输出完成后，你可能需要使用 :kbd:`Ctrl-A X` 来终止模拟器以完成该操作：

   .. code-block:: console

     $ ninja -Cbuild run | tee log.log

   or

   .. code-block:: console

     $ ninja -Cbuild run | tee log.log

#. 从生成的日志文件中提取并生成 gcov 使用的 ``.gcda`` 和 ``.gcno`` 文件：

   .. code-block:: console

     $ python3 scripts/gen_gcov_files.py -i log.log

#. 在 SDK 中查找适用于目标架构的 gcov 二进制文件。在后续运行 ``gcovr`` 时需要传入该 gcov 可执行文件的路径：

   .. code-block:: console

     $ find $ZEPHYR_SDK_INSTALL_DIR -iregex ".*gcov"

#. 创建一个输出目录用于保存报告：

   .. code-block:: console

     $ mkdir -p gcov_report

#. 运行 ``gcovr`` 来生成报告：

   .. code-block:: console

     $ gcovr -r $ZEPHYR_BASE . --html -o gcov_report/coverage.html --html-details --gcov-executable <gcov_path_in_SDK>

   .. _coverage_posix:

Coverage reports using the POSIX architecture
*********************************************

When compiling for the POSIX architecture, you utilize your host native tooling
to build a native executable which contains your application, the Zephyr OS,
and some basic HW emulation.

这意味着你可以使用开发普通桌面应用所使用的相同工具链。

要为你的应用使用 ``gcc`` 的 `gcov`_ 生成覆盖率，请在编译前设置 :kconfig:option:`CONFIG_COVERAGE`。
运行应用后，``gcov`` 会将覆盖率数据转储到相应的 ``.gcda`` 和 ``.gcno`` 文件中，随后可以使用你偏好的工具对这些文件进行后处理。例如：

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :gen-args: -DCONFIG_COVERAGE=y
   :host-os: unix
   :board: native_sim
   :goals: build
   :compact:

.. code-block:: console

   $ ./build/zephyr/zephyr.exe
   # Press Ctrl+C to exit
   $ lcov --capture --directory ./ --output-file lcov.info -q --rc lcov_branch_coverage=1
   $ genhtml lcov.info --output-directory lcov_html -q --ignore-errors source --branch-coverage --highlight --legend

.. note::

   你需要较新的 lcov（至少 1.14），以支持中间文本格式。大多数现代 Linux 发行版都提供了满足要求的包。

   或者，你也可以使用 gcovr（至少 4.2 版本）。

Coverage reports using Twister
******************************

Zephyr's :ref:`twister script <twister_script>` can automatically
generate a coverage report from the tests which were executed.
You just need to invoke it with the ``--coverage`` command line option.

For example, you may invoke:

.. code-block:: console

    $ twister --coverage -p qemu_x86 -T tests/kernel

or:

.. code-block:: console

    $ twister --coverage -p native_sim -T tests/bluetooth

which will produce ``twister-out/coverage/index.html`` report as well as
the coverage data collected by ``gcovr`` tool in ``twister-out/coverage.json``.

Other reports might be chosen with ``--coverage-tool`` and ``--coverage-formats``
command line options.

如果你希望生成同时包含 Zephyr 源码以及 Zephyr 仓库外部应用代码的覆盖率报告（参见 :ref:`Application Types <zephyr-app-types>`），可以在你的工程目录中使用 Twister 并指定 ``--coverage-basedir $ZEPHYR_BASE`` 选项，例如：

.. code-block:: console

   $ $ZEPHYR_BASE/scripts/twister --coverage -p native_sim --coverage-basedir $ZEPHYR_BASE -T your_project_dir

.. note::

   默认情况下，Twister 会调用 ``gcovr`` 工具，gcovr 在过滤源文件时假定所有路径都是已解析的真实路径（参见 `all symlinks resolved <gcovr_symlinks_>`_）。如果你的开发环境中存在符号链接目录，为了避免 gcovr 生成不完整的报告，请确保 :ref:`ZEPHYR_BASE <important-build-vars>` 是真实路径，或者改用 lcov，并通过 Twister 的命令行选项指定 ``--coverage-tool lcov``。

The process differs for unit tests, which are built with the host
toolchain and require a different board:

.. code-block:: console

   $ twister --coverage -p unit_testing -T tests/unit

which produces a report in the same location as non-unit testing.

.. _gcovr_symlinks:
   https://github.com/gcovr/gcovr/blob/main/doc/source/guide/filters.rst#filters-for-symlinks

.. _gcov:
   https://gcc.gnu.org/onlinedocs/gcc/Gcov.html

Using different toolchains
==========================

Twister looks at the environment variable ``ZEPHYR_TOOLCHAIN_VARIANT``
to check which gcov tool to use by default. The following are used as the
default for the Twister ``--gcov-tool`` argument default:

+-----------+-----------------------+
| Toolchain | ``--gcov-tool`` value |
+-----------+-----------------------+
| host      | ``gcov``              |
+-----------+-----------------------+
| llvm      | ``llvm-cov gcov``     |
+-----------+-----------------------+
| zephyr    | ``gcov``              |
+-----------+-----------------------+
