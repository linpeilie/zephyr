.. _opamp_api:

运算放大器 (Operational Amplifier, OPAMP)
###########################################

概述 (Overview)
****************

运算放大器是一种模拟设备,用于放大差分输入信号(反相输入和非反相输入之间的差异)以给出结果输出电压。


配置 (Configuration)
*********************

启用 OPAMP 时,必须使用设备树提供初始配置。OPAMP 增益可以在运行时调整。

相关配置选项:

* :kconfig:option:`CONFIG_OPAMP`

API 参考 (API Reference)
*************************

.. doxygengroup:: opamp_interface
