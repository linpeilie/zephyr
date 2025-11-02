.. _gcc:

GCC 静态分析支持
################

静态分析在 `GCC <https://gcc.gnu.org/>`__ 10 中引入，通过选项 ``-fanalyzer`` 启用。
该选项对代码执行比传统警告更昂贵和更彻底的分析。

运行 GCC 静态分析
*****************

要运行 GCC 静态分析，应在调用 :ref:`west build <west-building>` 时传递 ``-DZEPHYR_SCA_VARIANT=gcc`` 参数，例如：

.. zephyr-app-commands::
   :zephyr-app: samples/userspace/hello_world_user
   :board: qemu_x86
   :gen-args: -DZEPHYR_SCA_VARIANT=gcc
   :goals: build
   :compact:

配置 GCC 静态分析器
*******************************

GCC 静态分析器可以通过若干专用选项进行控制。

* `Options controlling the
   analyzer <https://gcc.gnu.org/onlinedocs/gcc/Static-Analyzer-Options.html>`__
* `Options controlling the diagnostic message
   formatting <https://gcc.gnu.org/onlinedocs/gcc/Diagnostic-Message-Formatting-Options.html>`__

.. list-table::
    :header-rows: 1

    * - 参数
       - 说明
    * - ``GCC_SCA_OPTS``
       - 以分号分隔的 GCC 分析器选项列表。

这些参数可以通过命令行传递，也可以设置为环境变量。

.. zephyr-app-commands::
    :zephyr-app: samples/hello_world
    :board: stm32h573i_dk
    :gen-args: -DZEPHYR_SCA_VARIANT=gcc -DGCC_SCA_OPTS="-fdiagnostics-format=json;-fanalyzer-verbosity=3"
    :goals: build
    :compact:

.. note::

    GCC 静态分析器仍在积极开发中，每个新版本通常会引入新的选项。此 `页面 <https://gcc.gnu.org/wiki/StaticAnalyzer>`__ 概述了分析器在各个版本中引入的选项与修复内容。


分析器的最新版本
******************************

由于 Zephyr 自带的工具链可能并不包含最新版本的 GCC 静态分析器，您可以使用更新的 `GNU Arm embedded toolchain
<https://docs.zephyrproject.org/latest/develop/toolchains/gnu_arm_embedded.html>`__ 来运行 GCC 静态分析，从而利用更新的分析器功能和修复。

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :board: stm32h573i_dk
   :gen-args: -DZEPHYR_SCA_VARIANT=gcc -DZEPHYR_TOOLCHAIN_VARIANT=gnuarmemb -DGNUARMEMB_TOOLCHAIN_PATH=...
   :goals: build
   :compact:
