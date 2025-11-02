.. _integration_with_pytest:

与 pytest 测试框架的集成
######################################

*注意：twister 与 pytest 的集成仍在进行中。目前并非所有平台类型都能被 pytest 支持。如果你在集成过程中发现问题或有改进建议，请在 GitHub 上提交 issue 或增强请求。*

简介
************

Pytest 是一个 Python 测试框架，"使编写小而可读的测试变得容易，并且能够扩展以支持应用程序和库的复杂功能测试"（详见 `<https://docs.pytest.org/en/7.3.x/>`_）。Python 拥有丰富的库并便于用于脚本编写。此外，pytest 使用插件（plugins）和夹具（fixtures）机制，增强了扩展性与可重用性。

我们引入了名为 ``pytest-twister-harness`` 的 pytest 插件，用于在 pytest 与 twister 之间建立集成，允许 Zephyr 社区在保留 twister 作为主框架的同时使用 pytest 的功能。

与 twister 的集成
************************

默认情况下，无需额外操作即可在 twister 中启用 pytest 支持。该插件作为 Zephyr 源树的一部分进行开发。为实现无需安装的运行方式，twister 会首先将该插件路径加入 ``PYTHONPATH``，然后在调用 pytest 时在命令行中追加 ``-p twister_harness.plugin`` 参数。如果希望使用已安装的插件版本，可以在 twister 命令中加入 ``--allow-installed-plugin`` 标志。

基于 pytest 的测试套件与其他 twister 测试的发现方式相同，例如通过存在 test/sample.yaml 文件来识别。该文件中的 ``harness`` 关键字告诉 twister 如何处理给定测试。当使用 ``harness: pytest`` 时，twister 的大部分工作流（测试套件发现、并行化、构建与报告）与其他 harness 一致。差异出现在执行阶段。下面插图展示了集成的简要示意。

.. figure:: figures/twister_and_pytest.svg
   :figclass: align-center


当使用 ``harness: pytest`` 时，twister 会将测试执行委托给 pytest（以子进程方式调用）。所需参数（例如构建目录、要使用的设备等）通过命令行传递。pytest 执行完成后，twister 会查找 pytest 报告（results.xml）并据此设置测试结果。

如何创建 pytest 测试
***************************

一个包含 pytest 测试、应用源码和 Twister 配置 .yaml 文件的示例目录结构如下：

.. code-block:: none

   test_foo/
   ├─── pytest/
   │    └─── test_foo.py
   ├─── src/
   │    └─── main.c
   ├─── CMakeList.txt
   ├─── prj.conf
   └─── testcase.yaml

在 :zephyr_file:`samples/subsys/testsuite/pytest/shell/pytest/test_shell.py` 中给出了一个 pytest 测试的示例。使用 ``testcase.yaml`` 中的配置，Twister 会从 ``src`` 构建应用程序；如果 .yaml 文件包含 ``harness: pytest`` 条目，则 Twister 会在单独的子进程中调用 pytest。示例配置文件可能如下所示：

.. code-block:: yaml

   tests:
      some.foo.test:
         harness: pytest
         tags: foo

默认情况下，pytest 会在与二进制源目录相邻的 ``pytest`` 目录中查找测试。可以在 .yaml 文件的 ``harness_config`` 部分使用 ``pytest_root`` 关键字来指向其他文件、目录或子测试（更多信息见 :ref:`here <pytest_root>`）。

Pytest 会按其默认的
`发现规则 <https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html#conventions-for-python-test-discovery>`_
扫描给定位置以查找测试。

传递额外参数
=======================

有两种方式可以向被调用的 pytest 子进程传递额外参数：

#. 在 .yaml 文件的 ``harness_config`` 部分使用 ``pytest_args``（更多信息见 :ref:`here <pytest_args>`）。
#. 通过 Twister 命令行使用 ``--pytest-args`` 参数。这在需要从测试套件中选择特定测试用例时非常有用。例如，可以使用：

.. code-block:: console

   $ ./scripts/twister --platform native_sim -T samples/subsys/testsuite/pytest/shell \
   -s samples/subsys/testsuite/pytest/shell/sample.pytest.shell \
   --pytest-args='-k test_shell_print_version'

命令行参数会扩展来自 .yaml 文件的参数；如果两处都存在相同参数，则命令行参数优先。

Fixtures（夹具）
********

dut
===

提供对 `DeviceAdapter`_ 类型对象的访问，该对象表示被测设备（DUT）。该夹具是 pytest harness 插件的核心，用于启动 DUT（初始化日志、烧写设备、连接串口等）。夹具会根据请求的类型（``native``、``qemu``、``hardware`` 等）返回已准备好的设备。所有设备类型共享相同 API，从而允许编写与设备类型无关的测试。该夹具的作用域由 .yaml 文件 ``harness_config`` 部分中的 ``pytest_dut_scope`` 关键字决定（更多信息见 :ref:`here <pytest_dut_scope>`）。

.. code-block:: python

   from twister_harness import DeviceAdapter

   def test_sample(dut: DeviceAdapter):
      dut.readlines_until('Hello world')

shell
=====

提供一个 `Shell <shell_class_>`_ 类对象，包含与 shell 应用交互所需的方法。它会调用 ``wait_for_promt`` 方法，以确保在 DUT 就绪前不启动场景。shell 夹具会调用 ``dut`` 夹具，因此可以访问其所有方法。``shell`` 夹具为与 shell 的交互添加了一些优化方法，可在测试中替代直接使用 ``dut``。该夹具的作用域由 .yaml 文件 ``harness_config`` 部分的 ``pytest_dut_scope`` 关键字决定（更多信息见 :ref:`here <pytest_dut_scope>`）。

.. code-block:: python

   from twister_harness import Shell

   def test_shell(shell: Shell):
      shell.exec_command('help')

mcumgr
======

示例夹具用于封装用于管理远程设备的命令行工具 ``mcumgr``。有关 MCUmgr 的更多信息，请参见 :ref:`mcu_mgr`。

.. note::
   此夹具要求系统 PATH 中包含可用的 ``mcumgr`` 可执行文件。

只有 MCUmgr 的部分功能被该夹具封装。例如，下面演示了使用 ``mcumgr`` 夹具的测试：

.. code-block:: python

   from twister_harness import DeviceAdapter, Shell, McuMgr

   def test_upgrade(dut: DeviceAdapter, shell: Shell, mcumgr: McuMgr):
      # 释放 mcumgr 使用的串口
      dut.disconnect()
      # 上传签名映像
      mcumgr.image_upload('path/to/zephyr.signed.bin')
      # 从设备获取已上传映像的哈希
      second_hash = mcumgr.get_hash_to_test()
      # 测试新的升级映像
      mcumgr.image_test(second_hash)
      # 远程重置设备
      mcumgr.reset_device()
      # 继续测试场景，检查版本等

unlaunched_dut
==============

类似于 ``dut`` 夹具，但不初始化设备。适用于需要对构建过程进行更细粒度控制的场景，测试代码将负责初始化设备。

.. code-block:: python

   from twister_harness import DeviceAdapter

   def test_sample(unlaunched_dut: DeviceAdapter):
      unlaunched_dut.launch()
      unlaunched_dut.readlines_until('Hello world')

Classes
*******

DeviceAdapter
=============

.. autoclass:: twister_harness.DeviceAdapter

   .. automethod:: launch

   .. automethod:: connect

   .. automethod:: readline

   .. automethod:: readlines

   .. automethod:: readlines_until

   .. automethod:: write

   .. automethod:: disconnect

   .. automethod:: close

.. _shell_class:

Shell
=====

.. autoclass:: twister_harness.Shell

   .. automethod:: exec_command

   .. automethod:: wait_for_prompt

   .. automethod:: get_filtered_output

Zephyr 项目中 pytest 测试示例
**********************************************

* :zephyr:code-sample:`pytest_shell`
* MCUmgr 测试 - :zephyr_file:`tests/boot/with_mcumgr`
* LwM2M 测试 - :zephyr_file:`tests/net/lib/lwm2m/interop`
* GDB stub 测试 - :zephyr_file:`tests/subsys/debug/gdbstub`

FAQ
***

如何在整个 pytest 会话中只烧写/运行一次应用？
==================================================

``dut`` 是负责烧写/运行应用的夹具。默认情况下其作用域为 ``function``。可以在 .yaml 文件的 ``harness_config`` 部分通过添加 ``pytest_dut_scope`` 关键字将其更改为会话级别：

.. code-block:: yaml

   harness: pytest
   harness_config:
      pytest_dut_scope: session

更多信息见 :ref:`here <pytest_dut_scope>`。

如何只运行 Python 文件中的某个特定测试？
================================================

可以通过多种方式实现。在 .yaml 文件中可以在 ``harness_config`` 下添加 ``pytest_root`` 条目，列出应运行的测试：

.. code-block:: yaml

   harness: pytest
   harness_config:
      pytest_root:
         - "pytest/test_shell.py::test_shell_print_help"

也可以使用 pytest 的 ``-k`` 选项选择特定测试（关于 pytest 关键字过滤的更多信息见 `here <https://docs.pytest.org/en/latest/example/markers.html#using-k-expr-to-select-tests-based-on-their-name>`_）。可以将 ``-k`` 过滤器添加到 .yaml 文件中的 ``pytest_args``：

.. code-block:: yaml

   harness: pytest
   harness_config:
      pytest_args:
         - "-k test_shell_print_help"

或者在 Twister 命令行中覆盖 .yaml 文件中的参数：

.. code-block:: console

   $ ./scripts/twister ... --pytest-args='-k test_shell_print_help'

如何获取测试中使用的设备类型信息？
========================================

可以从 ``dut`` 夹具（表示 `DeviceAdapter`_ 对象）中获取设备类型信息：

.. code-block:: python

   device_type: str = dut.device_config.type
   if device_type == 'hardware':
      ...
   elif device_type == 'native':
      ...

如何在本地重新运行 pytest 测试而无需 Twister 重新构建应用？
===============================================================

可以通过再次运行 Twister 并添加 ``--test-only`` 参数来实现。本地另一种做法是以最高详细级别（``-vv``）运行 Twister，然后从日志中复制用于启动 pytest 的命令（日志中会有类似 “Running pytest command: ...” 的条目）。

是否可以并行运行 pytest 测试？
================================================

原则上，``pytest-harness-plugin`` 并不是为并行运行 pytest 测试（尤其是面向硬件的测试）而编写。设计假设是并行化由 Twister 负责，Twister 管理可用资源（作业和硬件）。如果有人因某些原因希望并行运行（例如使用 `pytest-xdist plugin <https://pytest-xdist.readthedocs.io/en/stable/>`_），则需自行承担风险。

限制
***********

* 目前并非所有平台类型都被插件支持。
