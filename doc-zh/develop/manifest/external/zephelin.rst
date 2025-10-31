.. _external_module_zephelin:

Zephelin
########

简介 (Introduction)
********************

`Zephyr Profiling Library`_ (ZPL)，简称 Zephelin，是一个库，用于捕获和报告运行时性能指标，
以对 Zephyr 应用程序进行性能分析和详细分析，特别关注运行 AI/ML 推理工作负载的应用程序。

除上述功能外，Zephelin 还简化了 AI 运行时的分析，例如 `LiteRT`_ 和 `microTVM`_，
使您能够更好地了解潜在的瓶颈或优化机会。

Zephelin 特性：

* 在硬件上跟踪 Zephyr 应用程序的执行
* 使用 UART、USB 或调试适配器等后端获取跟踪
* 以 CTF 和 TEF 格式交付跟踪
* 从设备捕获跟踪的脚本
* 收集以下读数：

  * 内存 (Memory) - 栈、堆、内核堆和内存片
  * 传感器 (Sensors) - 例如芯片温度传感器
  * 线程分析 (Thread analysis) - CPU 使用率
  * AI 运行时 (AI runtimes) - 例如 LiteRT 中的张量 arena 使用情况

* 显示在 LiteRT 或 microTVM 运行时执行的神经网络层的详细信息：

  * 输入、输出和权重的维度
  * 层的参数
  * 执行特定层花费的时间和资源

* 库的编译级和运行时级配置

* 能够配置性能分析层级 (profiling tier)，控制子系统和收集的数据量

所有这些都可以使用 `Zephelin Trace Viewer`_ 进行分析。

在 Zephyr 中使用 (Usage With Zephyr)
**************************************

要将 Zephelin 用作 Zephyr :ref:`module <modules>`，请添加以下条目：

.. code-block:: yaml

   manifest:
     projects:
       - name: zephelin
         url: https://github.com/antmicro/zephelin
         revision: main
         path: modules/zephelin # 根据需要调整路径

到 Zephyr 子清单（例如 ``zephyr/submanifests/zephelin.yaml``）并运行 ``west update``，
或将其作为 West project 添加到您项目的 ``west.yaml`` 清单中。

请查阅 `Zephelin 文档`_ 了解更多信息。

参考文献 (References)
**********************

.. target-notes::

.. _Zephyr Profiling Library:
   https://github.com/antmicro/zephelin

.. _Zephelin 文档:
   https://antmicro.github.io/zephelin/

.. _Zephelin Trace Viewer:
   https://antmicro.github.io/zephelin-trace-viewer

.. _LiteRT:
   https://ai.google.dev/edge/litert

.. _microTVM:
   https://tvm.apache.org/docs/v0.9.0/topic/microtvm/index.html
