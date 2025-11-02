.. _codechecker:


CodeChecker 支持
###################

`CodeChecker <https://codechecker.readthedocs.io/>`__ 是一个静态分析基础设施。
它可以运行构建系统中可用的分析工具，如
`Clang-Tidy <https://clang.llvm.org/extra/clang-tidy/>`__、
`Clang Static Analyzer <https://clang-analyzer.llvm.org/>`__ 和
`Cppcheck <https://cppcheck.sourceforge.io/>`__。安装方法请参考各分析器的官方网站。


安装 CodeChecker
**********************

CodeChecker 本身是一个可在 `pypi <https://pypi.org/project/codechecker/>`__ 获取的 Python 包。

.. code-block:: shell

  pip install codechecker


使用 CodeChecker 构建
*************************

要运行 CodeChecker，需在调用 :ref:`west build <west-building>` 时添加 ``-DZEPHYR_SCA_VARIANT=codechecker`` 参数，例如：

.. code-block:: shell

  west build -b mimxrt1064_evk samples/basic/blinky -- -DZEPHYR_SCA_VARIANT=codechecker



CodeChecker 配置
***********************

CodeChecker 使用不同的命令步骤，每个步骤都有各自的配置参数。下表列出了所有可用选项。

.. list-table::
   :header-rows: 1

   * - 参数
     - 说明
   * - ``CODECHECKER_ANALYZE_JOBS``
     - 分析时使用的线程数。（默认：<CPU 数量>）
   * - ``CODECHECKER_ANALYZE_OPTS``
     - 直接传递给 ``analyze`` 命令的参数。（如 ``--timeout;360``）
   * - ``CODECHECKER_CLEANUP``
     - 解析/存储后执行清理操作，会移除所有 ``plist`` 文件。
   * - ``CODECHECKER_CONFIG_FILE``
     - 传递给所有命令的 JSON 或 YAML 配置文件。
   * - ``CODECHECKER_EXPORT``
     - 报告类型的逗号分隔列表。允许类型有：``html,json,codeclimate,gerrit,baseline``。
   * - ``CODECHECKER_NAME``
     - CodeChecker 运行元数据名称。（默认：``zephyr``）
   * - ``CODECHECKER_PARSE_EXIT_STATUS``
     - 默认情况下，CodeChecker 检测到的问题不会导致构建失败，设置此选项可在分析时失败。
   * - ``CODECHECKER_PARSE_OPTS``
     - 直接传递给 ``parse`` 命令的参数。（如 ``--verbose;debug``）
   * - ``CODECHECKER_PARSE_SKIP``
     - 跳过分析解析，仅存储结果时有用。
   * - ``CODECHECKER_STORE``
     - 分析后运行 ``store`` 命令。
   * - ``CODECHECKER_STORE_OPTS``
     - 直接传递给 ``store`` 命令的参数，隐含启用 ``CODECHECKER_STORE``。（如 ``--url;localhost:8001/Default``）
   * - ``CODECHECKER_STORE_TAG``
     - 传递标识符 ``--tag`` 给 ``store`` 命令。
   * - ``CODECHECKER_TRIM_PATH_PREFIX``
     - 从分析结果中裁剪指定路径，如 ``/home/user/zephyrproject``。默认会添加 ``west topdir`` 的值。

这些参数可以通过命令行传递，也可以设置为环境变量。



结合 twister 使用 CodeChecker
********************************

当在 ``twister`` 中运行 CodeChecker 时，会设置如下默认选项：

.. list-table::
   :header-rows: 1

   * - 参数
     - 默认值
   * - ``CODECHECKER_ANALYZE_JOBS``
     - ``1``
   * - ``CODECHECKER_NAME``
     - ``<board target>:<testsuite name>``
   * - ``CODECHECKER_STORE_TAG``
     - 应用源码目录下 ``git describe`` 的值。

如需覆盖这些值，可设置环境变量或作为额外参数传递。
