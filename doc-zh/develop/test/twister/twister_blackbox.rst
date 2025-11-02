.. _twister_blackbox:

Twister 黑盒测试
######################

本指南旨在说明测试文件的结构，帮助读者理解现有文件并创建自己的测试。所有开发者在对代码进行修改时，应修复其破坏的测试；在引入新功能时，应创建相应的新测试，因此这些知识对任何 Twister 开发者都十分重要。

基础
******

Twister 黑盒测试使用 Python 编写，基于 ``pytest`` 库。相关说明见 :ref:`here <integration_with_pytest>` 。
辅助测试数据保持其原始格式。
测试与数据全部位于 :zephyr_file:`scripts/tests/twister_blackbox` 目录，且文件名前缀为 ``test_``。

黑盒测试不应依赖 Twister 的内部实现，而应像用户一样调用 Twister 并检查其输出结果。

示例测试文件
****************

.. literalinclude:: ./sample_blackbox_test.py
   :language: python
   :linenos:

与命令行的比较
*******************

上例测试会运行如下命令：

.. code-block:: console

  twister -i --outdir $OUTDIR -T $TEST_DATA/tests -y --level $LEVEL
  --test-config $TEST_DATA/test_config.yaml -p qemu_x86 -p frdm_k64f

该测试假定命令行环境中已运行过 ``zephyr-env.sh`` 或 ``zephyr-env.cmd``。

得益于 ``importlib`` 的 ``exec_module()`` [#f1]_，此类测试能提供我们在 Twister 运行中通常期望得到的所有输出。
我们可以通过 ``args`` 变量轻松设置预期的 Twister 调用参数 [#f2]_，并在 ``out`` 与 ``err`` 变量中检查标准输出与标准错误。

除了标准输出外，还可以检查文件输出，通常位于 ``twister-out`` 目录中。大多数情况下，我们会将 ``out_path`` 夹具与 ``--outdir`` 标志（见 L52）配合使用，以便将测试生成的文件保存在临时目录中。
黑盒测试中常读取的文件包括 ``testplan.json``、``twister.xml`` 和 ``twister.log``。

其他功能
*********************

装饰器
==========

* ``@pytest.mark.usefixtures('clear_log')``
  - 允许我们使用来自 ``conftest.py`` 的 ``clear_log`` 夹具。该夹具未来可能设为 ``autouse``，届时可移除该装饰器。
* ``@pytest.mark.parametrize('level, expected_tests', TESTDATA_X, ids=['smoke', 'acceptance'])``
  - 这是 ``pytest`` 的参数化测试示例。详情见 `here <https://docs.pytest.org/en/7.1.x/example/parametrize.html#different-options-for-test-ids>`__。
    TESTDATA 通常声明为类字段。
* ``@mock.patch.object(TestPlan, 'TESTSUITE_FILENAME', suite_filename_mock)``
  - 该装饰器允许我们仅使用 ``test_data`` 中定义的测试，从而忽略 ``tests`` 目录中的 Zephyr 测试用例。**注意：所有 ``test_data`` 的测试文件名均使用** ``test_data.yaml`` **而不是** ``testcase.yaml`` **！**
    有关 ``mock`` 库的说明见 `here <https://docs.python.org/3/library/unittest.mock.html>`__。

夹具（Fixtures）
========

黑盒测试使用 ``pytest`` 的夹具，详情见 `here <https://docs.pytest.org/en/6.2.x/fixture.html>`__。

如果你想添加自定义夹具，请考虑它们是仅在单个测试文件中使用还是在多个文件中复用：

* 若在多个文件中使用，请将该夹具放到 :zephyr_file:`scripts/tests/twister_blackbox/conftest.py` 中。

  - :zephyr_file:`scripts/tests/twister_blackbox/conftest.py` 已包含若干夹具，参考其中示例。
* 若仅在单个文件中使用，可直接在该文件中声明。

  - 还可以考虑使用类字段来声明夹具——参见 TESTDATA 的示例。

如何……
***********

在同一个测试中多次调用 Twister？
========================================

有时我们需要先运行一次 Twister（例如使用 ``--build-only``），再运行一次（例如 ``--test-only``）。如果直接两次调用 ``importlib`` 的 ``exec_module``，会导致日志重复：``twister.log`` 中的每行会被重复写入（若调用三次则三次），而不是覆盖或追加为单一日志。

这是由于 Twister 文件中使用了 logger 的模块级变量，重复执行模块会导致 logger 拥有多个处理器句柄。

为避免此问题，两次调用之间应执行：

.. code:: python

  capfd.readouterr()   # 清除输出缓冲区的内容
             # 注意：如果希望保留所有运行的输出以便连续查看，则跳过此行。
  clear_log_in_test()  # 清除日志重复的处理器


------

.. rubric:: 脚注

.. [#f1] 请注意 ``setup_class()`` 类方法，它允许我们像直接调用一样运行
     ``twister`` 的 Python 文件（绕开 ``__name__ == '__main__'`` 的检查）。

.. [#f2] 我们建议在大多数测试中保持 ``args`` 定义的第一部分不变，因为它用于通用的测试初始化设置。
