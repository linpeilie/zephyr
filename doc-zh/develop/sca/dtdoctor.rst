.. _dtdoctor:


设备树诊断（``dtdoctor``）
#####################################

``dtdoctor`` 是一个静态分析工具，用于诊断与设备树（Devicetree）相关的构建错误。

它会拦截编译器和链接器的错误信息，当这些错误涉及未解析的设备树符号（例如 ``__device_dts_ord_*``）时，提供关于可能原因以及如何修复的详细信息。

使用 dtdoctor
**************

要启用 ``dtdoctor``，请在构建时添加 ``-DZEPHYR_SCA_VARIANT=dtdoctor`` 参数。

例如：

.. code-block:: shell

   west build -b reel_board samples/basic/blinky -- -DZEPHYR_SCA_VARIANT=dtdoctor
