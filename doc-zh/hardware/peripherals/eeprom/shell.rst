.. _eeprom_shell:

EEPROM Shell
############

.. contents::
    :local:
    :depth: 1

概述 (Overview)
****************

EEPROM shell 为 :ref:`shell <shell_api>` 模块提供了一个带有一组子命令的 ``eeprom`` 命令。
它允许通过交互式界面测试和探索 :ref:`EEPROM <eeprom_api>` 驱动程序 API，
而无需编写专用应用程序。EEPROM shell 也可以在现有应用程序中启用，
以帮助交互式调试 EEPROM 问题。

为了启用 EEPROM shell，必须启用以下 :ref:`Kconfig <kconfig>` 选项:

* :kconfig:option:`CONFIG_SHELL`
* :kconfig:option:`CONFIG_EEPROM`
* :kconfig:option:`CONFIG_EEPROM_SHELL`

例如，为 :zephyr:board:`native_sim` 构建带有 EEPROM shell 的 :zephyr:code-sample:`hello_world` 示例:

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :board: native_sim
   :gen-args: -DCONFIG_SHELL=y -DCONFIG_EEPROM=y -DCONFIG_EEPROM_SHELL=y
   :goals: build

有关如何连接和与 shell 交互的一般说明，请参阅 :ref:`shell <shell_api>` 文档。
EEPROM shell 带有内置帮助(除非禁用 :kconfig:option:`CONFIG_SHELL_HELP`)。
可以通过向 ``eeprom`` 命令或其任何子命令传递 ``-h`` 或 ``--help`` 来打印内置帮助消息。
所有子命令也支持其参数的制表符补全。

.. tip::
   所有 EEPROM shell 子命令都将 EEPROM 外设的名称作为第一个参数，
   这也支持制表符补全。当启用 :kconfig:option:`CONFIG_DEVICE_SHELL` 时，
   可以使用 ``device list`` shell 命令获取所有可用设备的列表。
   下面的示例都使用设备名称 ``eeprom@0``。

EEPROM 大小 (EEPROM Size)
**************************

可以使用 ``eeprom size`` 子命令检查 EEPROM 的大小，如下所示:

.. code-block:: console

   uart:~$ eeprom size eeprom@0
   32768 bytes

写入数据 (Writing Data)
************************

可以使用 ``eeprom write`` 子命令将数据写入 EEPROM。
此子命令至少需要三个参数：EEPROM 设备名称、开始写入的偏移量以及至少一个数据字节。
在以下示例中，十六进制字节序列 ``0x0d 0x0e 0x0a 0x0d 0x0b 0x0e 0x0e 0x0f`` 
被写入偏移量 ``0x0``:

.. code-block:: console

   uart:~$ eeprom write eeprom@0 0x0 0x0d 0x0e 0x0a 0x0d 0x0b 0x0e 0x0e 0x0f
   Writing 8 bytes to EEPROM...
   Verifying...
   Verify OK

也可以使用 ``eeprom fill`` 子命令用相同的模式填充 EEPROM 的一部分。
在以下示例中，模式 ``0xaa`` 被写入从偏移量 ``0x8`` 开始的 16 个字节:

.. code-block:: console

   uart:~$ eeprom fill eeprom@0 0x8 16 0xaa
   Writing 16 bytes of 0xaa to EEPROM...
   Verifying...
   Verify OK

读取数据 (Reading Data)
************************

可以使用 ``eeprom read`` 子命令从 EEPROM 读取数据。
此子命令需要三个参数：EEPROM 设备名称、开始读取的偏移量以及要读取的字节数:

.. code-block:: console

   uart:~$ eeprom read eeprom@0 0x0 8
   Reading 8 bytes from EEPROM, offset 0...
   00000000: 0d 0e 0a 0d 0b 0e 0e 0f                          |........         |
