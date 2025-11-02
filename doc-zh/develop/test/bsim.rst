.. _bsim:

BabbleSim
#########

BabbleSim 与 Zephyr
********************

在 Zephyr 项目中，我们使用 `Babblesim`_ 模拟器来测试部分 Zephyr 的无线协议栈，包括 Bluetooth LE、802.15.4 以及部分网络栈。

BabbleSim_ 是一个物理层（PHY）模拟器，结合 Zephyr 的 :ref:`bsim boards<bsim boards>`，可用于模拟由 Bluetooth LE 和 15.4 设备组成的网络。针对 :ref:`bsim board<bsim boards>` 构建 Zephyr 时，会生成包含应用、Zephyr OS 以及硬件模型的 Linux 可执行文件。

当存在无线电活动时，该 Linux 可执行文件会连接到 BabbleSim 的 PHY 模拟以模拟无线信道。

有关如何获取和构建模拟器的更多信息，请参阅 BabbleSim 文档中的 `获取 <https://babblesim.github.io/fetching.html>`_ 与 `构建 <https://babblesim.github.io/building.html>`_ 页面。在 :ref:`nrf52_bsim<nrf52_bsim>`、:ref:`nrf5340bsim<nrf5340bsim>` 和 :ref:`nrf54l15bsim<nrf54l15bsim>` 板的文档中，可找到针对这些板构建 Zephyr 的说明与示例。

测试类型
**************

无无线电活动的测试：使用 twister 的 bsim 测试
=====================================================

:ref:`bsim boards<bsim boards>` 可在无无线电活动的情况下使用，此时无需将其连接到物理层模拟。因此，这些目标板可以像 :zephyr:board:`native_sim<native_sim>` 一样与 :ref:`twister <twister_script>` 配合使用，运行所有标准的 Zephyr twister 测试，但使用的是更贴近真实 SoC 硬件与驱动的模型。

有无线电活动的测试
=========================

当存在无线电活动时，BabbleSim 测试至少需要一个正在运行的物理层模拟，并且大多数测试需要多个被模拟设备。因此，这类测试不是用 twister 构建和运行的，而是使用专门的一组测试脚本。

这些测试保存在 :code:`tests/bsim/` 目录下。该目录中的 ``compile.sh`` 与 ``run_parallel.sh`` 脚本由 CI 系统使用，用于构建所需映像并批量执行这些测试。

下面各节介绍如何构建与运行这些测试以及它们遵循的约定。

主要有两类测试：

* 自检的嵌入式应用/测试：部分模拟设备的应用包含用于判定测试通过或失败的检查逻辑。这类嵌入式应用测试使用 :ref:`bs_tests<bsim_boards_bs_tests>` 系统上报通过或失败，并在许多场景下将多个测试打包到同一二进制中。

* 使用 EDTT_ 工具的测试：由 EDTT（Python）测试通过 RPC 机制控制嵌入式应用，并判定测试是否通过。目前这类测试包含 BT 认证测试套件的一个重要子集。

关于不同测试类型与 BabbleSim 及 bsim boards 的关系，请参见 :ref:`bsim boards tests section<bsim_boards_tests>`。

与 BabbleSim 的测试覆盖率
***************************

由于 :ref:`nrf52_bsim<nrf52_bsim>`、:ref:`nrf5340bsim<nrf5340bsim>` 与 :ref:`nrf54l15bsim<nrf54l15bsim>` 板基于 POSIX 架构，您可以比较方便地收集测试覆盖率信息。

可使用脚本 :zephyr_file:`tests/bsim/generate_coverage_report.sh` 从测试结果生成 HTML 覆盖率报告。

更多信息请参见 :ref:`coverage_posix` 中关于覆盖率生成的页面。

.. _BabbleSim:
  https://BabbleSim.github.io

.. _EDTT:
  https://github.com/EDTTool/EDTT

构建与运行测试
******************************

有关搭建模拟器的说明，请参阅 :ref:`nrf52_bsim` 页面。

这些脚本还期望设置若干环境变量。例如，在 Zephyr 根目录下可以运行：

.. code-block:: bash

  # 构建所有测试
  ${ZEPHYR_BASE}/tests/bsim/compile.sh

  # 并行运行它们
  RESULTS_FILE=${ZEPHYR_BASE}/myresults.xml \
    SEARCH_PATH=${ZEPHYR_BASE}/tests/bsim \
      ${ZEPHYR_BASE}/tests/bsim/run_parallel.sh

或者仅构建并运行特定子集，例如主机广播测试：

.. code-block:: bash

  # 构建 Bluetooth 主机广播测试
  ${ZEPHYR_BASE}/tests/bsim/bluetooth/host/adv/compile.sh

  # 并行运行它们
  RESULTS_FILE=${ZEPHYR_BASE}/myresults.xml \
    SEARCH_PATH=${ZEPHYR_BASE}/tests/bsim/bluetooth/host/adv \
      ${ZEPHYR_BASE}/tests/bsim/run_parallel.sh

查看 ``run_parallel.sh`` 的帮助以获取更多选项和如何批量运行测试的示例。

在构建测试所需二进制之后，可使用对应的测试脚本直接运行单个测试。

例如，可以为网络测试构建所需二进制：

.. code-block:: bash

  WORK_DIR=${ZEPHYR_BASE}/bsim_out ${ZEPHYR_BASE}/tests/bsim/net/compile.sh

然后直接运行某个测试：

.. code-block:: bash

  ${ZEPHYR_BASE}/tests/bsim/net/sockets/echo_test/tests_scripts/echo_test_802154.sh

约定
===========

测试代码
---------

有关测试代码应遵循的约定，请参见 :zephyr_file:`Bluetooth sample test <tests/bsim/bluetooth/host/misc/sample_test/README.rst>`。

构建脚本
-------------

``compile.sh`` 构建脚本负责为子文件夹中的测试脚本构建所有所需的测试与示例应用。

这些构建脚本使用公共的 compile.source，该脚本提供一个函数（compile），用于调用 cmake 和 ninja，传入指定的应用、配置与覆盖文件。

为了加快仅对部分测试感兴趣的用户的编译速度，部分子文件夹中存在多个编译脚本，较上层的脚本会调用下层的脚本。

注意：此处直接使用 cmake 与 ninja，而非 ``west build`` 封装器，因为并非所有 Zephyr 用户都会使用或安装 west，但仍希望使用这些构建与测试脚本。

测试脚本
------------

请遵循现有约定，不要设计一次性专用的运行器（例如自定义 Python 脚本或其它 shell 抽象）。

这样做的理由是：如果所有测试以相同方式、使用相同变量运行，维护者在进行构建系统或兼容性更改时可以更快、更方便地对整个代码树进行更新。

如果你有改进测试脚本的好想法，请提交 PR 修改 *所有* 测试脚本，以便让所有人受益并保持一致性。你也可以先在 RFC issue 中讨论，或在 BabbleSim 的 Discord 频道交流。

以“_”开头的脚本（``_``）不会被自动发现和运行，它们可用作主脚本的辅助函数，或用于本地开发工具（例如本地构建与运行测试、调试等）。

以下是约定：

- 每个测试由扩展名为 ``.sh`` 的 shell 脚本定义，位于名为 ``test_scripts/`` 的子文件夹中。
- 建议每个脚本文件只运行单个测试，这有助于在 CI 中更好地并行化运行。
- 脚本假定所需的二进制已被构建。脚本不应编译二进制文件。
- 脚本将为每个被模拟设备及物理层模拟生成进程。
- 如果测试通过，脚本必须向调用的 shell 返回 0；若测试失败，则返回非 0 值。
- 每个测试必须具有唯一的仿真 id，以便支持并行运行不同测试。
- 脚本或镜像不得修改工作站文件系统中 ``${BSIM_OUT_PATH}/results/<simulation_id>/`` 或 ``/tmp/`` 之外的内容，换言之，不应留下额外的临时文件。
- 需要多次连续仿真的测试（例如：模拟设备配对、断电再以新仿真启动等），应为每个仿真段使用不同的仿真 id，从而确保可以事后检查每段的无线电活动。
- 避免过长的测试。如果测试运行时间超过 20 秒，考虑将其拆分为多个独立测试。
- 如果测试运行时间超过 5 秒，请将 ``EXECUTE_TIMEOUT`` 设置为至少为实际运行时间的 5 倍。
- 不要将 ``EXECUTE_TIMEOUT`` 设置为低于默认值。
- 测试输出不应过于冗长：期望输出少于一百行。可以广泛使用 ``LOG_DBG()``，但不要默认启用 ``DBG`` 日志级别。
