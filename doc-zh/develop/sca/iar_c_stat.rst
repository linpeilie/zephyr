.. _icstat:


IAR C-STAT 支持
##################

`IAR C-STAT <https://iar.com/cstat>`__ 是一款用于 C/C++ 源代码的综合静态分析工具。它能够发现错误和漏洞，并支持多种编码标准，例如 MISRA C、MISRA C++、CERT C/C++ 以及 CWE。

安装 IAR C-STAT
*********************

IAR C-STAT 随 IAR Build Tools 和 IAR Embedded Workbench 一并提供。有关安装与安装位置的详细信息，请参考相应产品的文档。

使用 IAR C-STAT 进行构建
************************

要运行 IAR C-STAT，需要 CMake 4.1.0 或更高版本。使用 :ref:`west build <west-building>` 构建时，附加参数以选择 IAR C-STAT（``-DZEPHYR_SCA_VARIANT=iar_c_stat``），例如：

.. zephyr-app-commands::
   :zephyr-app: samples/basic/blinky
   :board: stm32f429ii_aca
   :gen-args: -DZEPHYR_SCA_VARIANT=iar_c_stat
   :goals: build
   :compact:

配置 IAR C-STAT
***********************

IAR C-STAT 支持若干用于自定义分析的参数。下表列出了受支持的选项。

.. list-table::
   :header-rows: 1

   * - 参数
     - 说明
   * - ``CSTAT_RULESET``
     - 要使用的预定义规则集。（默认：``stdchecks``，可选值：``all,cert,misrac2004,misrac2012,misrac++2008,stdchecks,security``）
   * - ``CSTAT_ANALYZE_THREADS``
     - 分析时使用的线程数。（默认：<CPU 数量>）
   * - ``CSTAT_ANALYZE_OPTS``
     - 直接传递给 ``analyze`` 命令的参数。（例如：``--timeout=900;--deterministic;--fpe``）
   * - ``CSTAT_DB``
     - 覆盖默认的 C-STAT SQLite 数据库位置。（例如：``/home/user/cstat.db``）
   * - ``CSTAT_CLEANUP``
     - 对 C-STAT SQLite 数据库执行清理操作。（例如：``true``）

这些参数可以通过命令行传递，也可以设置为环境变量。下面示例展示如何启用并组合非标准规则集：

.. zephyr-app-commands::
   :zephyr-app: samples/basic/blinky
   :board: stm32f429ii_aca
   :gen-args: -DZEPHYR_SCA_VARIANT=iar_c_stat -DCSTAT_RULESET=misrac2012,cert
   :goals: build
