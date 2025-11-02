.. _coverity:


Coverity 支持
#########

Coverity Scan 是 Black Duck 提供的一项服务，能够为已在 Coverity Scan 注册的开源项目开发者，提供开源代码分析结果。

本集成仅在 scan.coverity.com 及其提供的工具分发包上进行了测试。


生成构建数据文件
***************************

要使用本集成，需将 coverity 工具分发包添加到你的 :envvar:`PATH` 环境变量，并在调用 :ref:`west build <west-building>` 时添加 ``-DZEPHYR_SCA_VARIANT=coverity`` 参数，例如：

.. code-block:: shell

    west build -b qemu_cortex_m3 samples/hello_world -- -DZEPHYR_SCA_VARIANT=coverity


扫描结果将生成在 :file:`build/sca/coverity` 目录下。

你也可以通过设置 :envvar:`COVERITY_OUTPUT_DIR`，指定多个或增量扫描结果的保存位置。


结果分析
****************

请按照 https://scan.coverity.com 上的说明上传分析结果。
