.. _eclair:


ECLAIR 支持
##############

Bugseng 的 `ECLAIR <https://www.bugseng.com/eclair/>`__ 是一套经过认证的静态分析工具与软件验证平台。
它的应用范围广泛，从代码规则校验（尤其关注 MISRA 与 BARR-C 编码规范）、软件度量计算、组件间独立性与互不干扰检查，到自动检测重要类别的软件错误。

先决条件
*************

必须安装 ECLAIR 工具，并将其可执行路径添加到操作系统的 PATH 变量中。

可通过运行以下命令验证安装：

.. code-block:: shell

   eclair -version

使用 ECLAIR 需要有效的许可证或试用许可证。要申请试用许可证，请访问 `此页面 <https://www.bugseng.com/eclair/free-trial>`__。

运行 ECLAIR
**************

要运行 ECLAIR，请在调用 :ref:`west build <west-building>` 时添加 ``-DZEPHYR_SCA_VARIANT=eclair`` 参数。

.. code-block:: shell

    west build -b mimxrt1064_evk samples/basic/blinky -- -DZEPHYR_SCA_VARIANT=eclair

.. note::
   这将仅使用预定义规则集 ``first_analysis`` 调用 ECLAIR 进行分析。若要使用其他规则集，需要提供配置文件；详见下节。

配置
**************

ECLAIR SCA 环境的配置可以通过 CMake 选项文件或作为命令行参数传递。

要在 ECLAIR 调用中使用 CMake 选项文件，可定义 ``ECLAIR_OPTIONS_FILE`` 变量，例如：

.. code-block:: shell

    west build -b mimxrt1064_evk samples/basic/blinky -- -DZEPHYR_SCA_VARIANT=eclair -DECLAIR_OPTIONS_FILE=my_options.cmake

如果未提供配置文件，默认的配置为 ``first_analysis``，这是一个用于验证环境是否正常工作的简要规则集。

若希望通过命令行覆盖默认配置（而非选项文件），可通过传递类似 ``-DOption=ON|OFF`` 的参数实现。

例如：

.. code-block:: shell

    west build -b mimxrt1064_evk samples/basic/blinky -- -DZEPHYR_SCA_VARIANT=eclair -DECLAIR_REPORTS_SARIF=ON

由于 Zephyr 项目规模和复杂度较大，配置集按照 Zephyr 的编码指南（来源：
https://docs.zephyrproject.org/latest/contribute/coding_guidelines/index.html）被划分为五类，以便在私有机器上更易于使用：

* first_analysis（默认）：用于验证基本功能的简要规则子集。

* STU：可通过独立分析单个翻译单元来验证的规则子集。

* STU_heavy：更复杂的 STU 类规则集，分析耗时较长。

* WP：全程序（whole program）级别的规则集（在 MISRA 术语中相当于“system”）。

* std_lib：与 C 标准库相关的项目规则集。

此外，zephyr_guidelines 规则集包含 `编码指南 <https://docs.zephyrproject.org/latest/contribute/coding_guidelines/index.html>`__ 中的主要规则。

相关的 CMake 选项：

* ``ECLAIR_RULESET_FIRST_ANALYSIS``
* ``ECLAIR_RULESET_STU``
* ``ECLAIR_RULESET_STU_HEAVY``
* ``ECLAIR_RULESET_WP``
* ``ECLAIR_RULESET_STD_LIB``
* ``ECLAIR_RULESET_ZEPHYR_GUIDELINES``

用户自定义规则集
====================

若要使用自定义规则集（替代预定义的 Zephyr 规则集），可将 :code:`ECLAIR_RULESET_USER=ON` 设置为启用。
创建自定义规则文件时，文件名应为 ``analysis_<RULESET>.ecl``，并通过 CMake 变量 :code:`ECLAIR_USER_RULESET_NAME` 指定规则集名称。
若规则文件不在应用源码目录中，可使用 :code:`ECLAIR_USER_RULESET_PATH` 指定规则文件路径，支持相对路径和绝对路径。

相关 CMake 选项和变量：

* ``ECLAIR_RULESET_USER``
* ``ECLAIR_USER_RULESET_NAME``
* ``ECLAIR_USER_RULESET_PATH``

生成额外报告格式
**********************************

ECLAIR 可生成除默认 ecd 文件外的多种报告格式（如 DOC、ODT、XLSX）和不同变体，示例包括：

* 电子表格格式的度量（Metrics）。

* 电子表格格式的问题清单（Findings）。

* SARIF 格式的问题清单（Findings）。

* 纯文本格式的摘要报告。

* DOC 格式的摘要报告。

* ODT 格式的摘要报告。

* HTML 格式的摘要报告。

* TXT 格式的详细报告。

* DOC 格式的详细报告。

* ODT 格式的详细报告。

* HTML 格式的详细报告。

相关 CMake 选项：

* ``ECLAIR_METRICS_TAB``
* ``ECLAIR_REPORTS_TAB``
* ``ECLAIR_REPORTS_SARIF``
* ``ECLAIR_SUMMARY_TXT``
* ``ECLAIR_SUMMARY_DOC``
* ``ECLAIR_SUMMARY_ODT``
* ``ECLAIR_SUMMARY_HTML``
* ``ECLAIR_FULL_TXT``
* ``ECLAIR_FULL_DOC``
* ``ECLAIR_FULL_ODT``
* ``ECLAIR_FULL_HTML``

完整报告的详细级别
============================

TXT 与 DOC 格式的完整报告的详细级别也可通过配置调整，当前可用的选项包括：

* 显示全部区域（Show all areas）。

* 仅显示第一个区域（Show only the first area）。

Related CMake options:

* ``ECLAIR_FULL_DOC_ALL_AREAS``
* ``ECLAIR_FULL_DOC_FIRST_AREA``
* ``ECLAIR_FULL_TXT_ALL_AREAS``
* ``ECLAIR_FULL_TXT_FIRST_AREA``
