.. _reset_api:

复位控制器 (Reset Controller)
###############################

概述 (Overview)
****************

复位控制器是控制多个外设的复位信号的单元。复位控制器 API 允许外设驱动程序请求对其复位输入信号的控制,包括断言、解除断言和切换这些信号的能力。此外,可以检查复位输入信号的复位状态。

主要是,line_assert 和 line_deassert API 函数是可选的,因为在大多数情况下我们希望切换复位信号。

配置选项 (Configuration Options)
*********************************

相关配置选项:

* :kconfig:option:`CONFIG_RESET`

API 参考 (API Reference)
*************************

.. doxygengroup:: reset_controller_interface
