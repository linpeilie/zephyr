.. _polyspace:


Polyspace 支持
#################

`Polyspace® <https://mathworks.com/products/polyspace.html>`__ 是 MathWorks 提供的商业静态代码分析工具，经过认证可用于最高安全等级的场景。它可以检查对 MISRA C、CERT C 等编码指南的遵循情况，发现 CWE、检测缺陷并计算代码复杂度度量。可选地，Polyspace 可以运行形式化证明以验证诸如数组越界、溢出、数据竞争等运行时错误的不存在，从而有助于实现内存安全。

安装
**********

必须安装 Polyspace 工具并将其添加到操作系统或容器的 PATH 中。具体而言，需要将 ``<polyspace_root>/polyspace/bin`` 加入 PATH 列表。

有关安装说明，请参见 `这里 <https://mathworks.com/help/bugfinder/install-polyspace.html>`__。
若要使用形式化验证（证明缺陷的*不存在*），还需额外安装 `此处所述组件 <https://mathworks.com/help/codeprover/install-polyspace.html>`__。

安装目录中必须包含许可证文件。要申请试用许可证，请访问 `此页面 <https://www.mathworks.com/campaigns/products/trials.html>`__。

运行
*******

可通过在构建命令中追加 ``-DZEPHYR_SCA_VARIANT=polyspace`` 来触发代码分析，例如：

.. code-block:: shell

   west build -b qemu_x86 samples/hello_world -- -DZEPHYR_SCA_VARIANT=polyspace

查看结果
*****************

分析发现的问题会在构建结束时汇总并打印到控制台，同时显示包含详细结果的文件夹路径。

为便于审查，建议在 `Polyspace 用户界面 <https://mathworks.com/help/bugfinder/review-results-1.html>`__ 中打开结果文件夹，或将其 `上传到 Web 接口 <https://mathworks.com/help/bugfinder/gs/run-bug-finder-on-server.html>`__ 并在那里审查。

在 CI 管道等场景中进行程序化访问时，结果目录中也会包含描述各个问题的 CSV 文件。

配置
*************

默认情况下，Polyspace 对所有 C 和 C++ 源文件扫描常见编程缺陷。可以通过下列选项自定义行为：

.. list-table::
   :widths: 20 40 30
   :header-rows: 1

   * - 选项
     - 作用
     - 示例
   * - ``POLYSPACE_ONLY_APP``
     - 若设置，仅分析用户代码，忽略 Zephyr 源码。
     - ``-DPOLYSPACE_ONLY_APP=1``
   * - ``POLYSPACE_OPTIONS``
     - 提供额外的命令行标志，例如选择编码规则。用分号分隔选项及其值。选项列表见 `此处 <https://mathworks.com/help/bugfinder/referencelist.html?type=analysisopt&s_tid=CRUX_topnav>`__。
     - ``-DPOLYSPACE_OPTIONS="-misra3;mandatory-required;-checkers;all"``
   * - ``POLYSPACE_OPTIONS_FILE``
     - 可将命令行标志逐行放入文本文件中并通过该选项指定文件的绝对路径。
     - ``-DPOLYSPACE_OPTIONS_FILE=/workdir/zephyr/myoptions.txt``
   * - ``POLYSPACE_MODE``
     - 在 bugfinding（缺陷检测）和 proving（证明）模式之间切换。默认是 bugfinding。详情见 `此处 <https://mathworks.com/help/bugfinder/gs/use-bug-finder-and-code-prover.html>`__。
     - ``-DPOLYSPACE_MODE=prove``
   * - ``POLYSPACE_PROG_NAME``
     - 覆盖被分析应用的名称。默认使用板和应用名称。
     - ``-DPOLYSPACE_PROG_NAME=myapp``
   * - ``POLYSPACE_PROG_VERSION``
     - 覆盖被分析应用的版本。默认从 git-describe 获取。
     - ``-DPOLYSPACE_PROG_VERSION=v1.0b-28f023``
