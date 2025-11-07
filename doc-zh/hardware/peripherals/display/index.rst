.. _display_api:

显示 (Display)
##############

Zephyr 中的显示子系统提供了一种统一的方式来与各种显示设备交互。显示 API 是传输无关的：
它描述了您希望显示器执行的操作，而不暴露数据如何在线路上传输。

MIPI 显示总线接口 (MIPI Display Bus Interface, DBI)
****************************************************

**MIPI DBI** 规范定义了用于将主机连接到显示控制器的几种并行和串行总线。
在 Zephyr 中，DBI 支持提供了用于命令写入、读取、像素传输、复位和相关操作的总线级原语，
驱动程序在内部使用这些原语来实现通用 API。

应用程序不直接使用 DBI 函数。相反，它们调用通用显示 API(例如写入像素)，
显示驱动程序在后台处理 DBI 协议。

MIPI-DBI 定义了 3 种接口类型:

* Type A: Motorola 6800 并行总线
* Type B: Intel 8080 并行总线
* Type C: SPI 类型串行位总线，有 3 个选项:

  #. 每字节 9 个写时钟，最后一位是命令/数据选择位
  #. 与上面相同，但每字节 16 个写时钟
  #. 每字节 8 个写时钟。通过 GPIO 引脚选择命令/数据

目前，API 不支持具有 16 个写时钟的 Type C 控制器(选项 2)。

MIPI 显示串行接口 (MIPI Display Serial Interface, DSI)
*******************************************************

**MIPI DSI** 标准是为现代彩色 TFT 面板设计的高速差分串行总线。
Zephyr 的 DSI 支持提供了驱动程序在 DSI 链路上实现通用显示 API 所需的原语。

与 DBI 一样，应用程序永远不会直接调用 DSI 函数。它们通过使用通用显示 API 保持可移植性，
而驱动程序在内部处理 DSI 事务。

API 参考 (API Reference)
*************************

通用显示接口 (Generic Display Interface)
==========================================

.. doxygengroup:: display_interface

.. _mipi_dbi_api:

MIPI 显示总线接口 (MIPI Display Bus Interface, DBI)
====================================================

.. doxygengroup:: mipi_dbi_interface

.. _mipi_dsi_api:

MIPI 显示串行接口 (MIPI Display Serial Interface, DSI)
=======================================================

.. doxygengroup:: mipi_dsi_interface

Grove LCD 显示 (Grove LCD Display)
===================================

.. doxygengroup:: grove_display

BBC micro:bit 显示 (BBC micro:bit Display)
===========================================

.. doxygengroup:: mb_display

单色字符帧缓冲 (Monochrome Character Framebuffer)
==================================================

.. doxygengroup:: monochrome_character_framebuffer
