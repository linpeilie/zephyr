.. _ec_host_cmd_backend_api:

EC主机命令 (EC Host Command)
#############################

概述 (Overview)
****************
主机命令协议定义了主机或应用处理器与目标嵌入式控制器(EC)通信的接口 (The host command protocol defines the interface for a host, or application processor, to communicate with a target embedded controller (EC))。EC主机命令子系统实现协议的目标端,生成对主机发送的命令的响应 (The EC Host command subsystem implements the target side of the protocol, generating responses to commands sent by the host)。主机命令协议接口支持多个版本,但此子系统实现仅支持协议版本3 (The host command protocol interface supports multiple versions, but this subsystem implementation only support protocol version 3)。

架构 (Architecture)
********************
主机命令子系统包含几个组件 (The Host Command subsystem contains a few components):

* 后端 (Backend)
* 通用处理程序 (General handler)
* 命令处理程序 (Command handler)

后端是外设驱动程序和通用处理程序之间的一层 (The backend is a layer between a peripheral driver and the general handler)。它负责通过选定的外设发送和接收命令 (It is responsible for sending and receiving commands via chosen peripheral)。

通用处理程序验证来自后端的数据,例如检查大小、校验和等 (The general handler validates data from the backend e.g. check sizes, checksum, etc)。如果命令有效并且用户为接收到的命令ID提供了处理程序,则调用命令处理程序 (If the command is valid and the user has provided a handler for a received command id, the command handler is called)。

.. image:: ec_host_cmd.png
   :align: center

SHI(串行主机接口)与此不同,因为它仅用于与主机通信 (SHI (Serial Host Interface) is different to this because it is used only for communication with a host)。SHI没有自己的API,因此后端和外设驱动程序层合并为一个后端层 (SHI does not have API itself, thus the backend and peripheral driver layers are combined into one backend layer)。

.. image:: ec_host_cmd_shi.png
   :align: center

另一种情况是SPI (Another case is SPI)。不幸的是,当前的SPI API无法用于处理主机命令通信 (Unfortunately, the current SPI API can't be used to handle the host commands communication)。主要问题是主机发送的命令大小未知(SPI事务发送/接收特定数量的字节)以及需要持续发送状态字节(SPI模块在每次事务时启用和禁用) (The main issues are unknown command size sent by the host (the SPI transaction sends/receives specific number of bytes) and need to constant sending status byte (the SPI module is enabled and disabled per transaction))。这迫使在后端内实现SPI驱动程序,就像SHI一样 (It forces implementing the SPI driver within a backend, as it is done for SHI)。这意味着必须为每个芯片系列实现SPI后端 (That means a SPI backend has to be implemented per chip family)。但是,一旦SPI API扩展以满足主机命令需求,这可能会在将来发生变化 (However, it can be changed in the future once the SPI API is extended to host command needs)。请查看 `讨论 <https://github.com/zephyrproject-rtos/zephyr/issues/56091>`_ (Please check `the discussion <https://github.com/zephyrproject-rtos/zephyr/issues/56091>`_)。

该方法需要以特殊方式配置SPI设备树节点 (That approach requires configuring the SPI dts node in a special way)。SPI节点的主要兼容字符串已更改为使用SPI驱动程序的主机命令版本 (The main compatible string of a SPI node has changed to use the Host Command version of a SPI driver)。其余属性应照常配置 (The rest of the properties should be configured as usual)。STM32的SPI节点示例 (Example of the SPI node for STM32):

.. code-block:: devicetree

   &spi1 {
           /* Change the compatible string to use the Host Command version of the
            * STM32 SPI driver
            */
           compatible = "st,stm32-spi-host-cmd";
           status = "okay";

           dmas = <&dma2 3 3 0x38440 0x03>,
                <&dma2 0 3 0x38480 0x03>;
           dma-names = "tx", "rx";
           /* This field is used to point at our CS pin */
           cs-gpios = <&gpioa 4 (GPIO_ACTIVE_LOW | GPIO_PULL_UP)>;
   };

STM32 SPI主机命令后端驱动程序支持 :dtcompatible:`st,stm32h7-spi` 和 :dtcompatible:`st,stm32-spi-fifo` 变体实现 (The STM32 SPI host command backend driver supports the :dtcompatible:`st,stm32h7-spi` and :dtcompatible:`st,stm32-spi-fifo` variant implementations)。要启用这些变体,请附加相应的兼容字符串 (To enable these variants, append the corresponding compatible string)。例如,要启用FIFO支持和STM32H7 SoC支持,请按如下所示修改兼容字符串 (For example, to enable FIFO support and support for the STM32H7 SoCs, modify the compatible string as shown)。

.. code-block:: devicetree

   &spi1 {
       compatible = "st,stm32h7-spi", "st,stm32-spi-fifo", "st,stm32-spi-host-cmd";
       ...
   };

运行Zephyr的芯片是SPI从设备,``cs-gpios`` 属性用于指向我们的CS引脚 (The chip that runs Zephyr is a SPI slave and the ``cs-gpios`` property is used to point our CS pin)。对于SPI,需要设置后端选定节点 ``zephyr,host-cmd-spi-backend`` (For the SPI, it is required to set the backend chosen node ``zephyr,host-cmd-spi-backend``)。

支持的后端和外设驱动程序 (The supported backend and peripheral drivers):

* 模拟器 (Simulator)
* SHI - ITE和NPCX (SHI - ITE and NPCX)
* eSPI - 任何支持 :kconfig:option:`CONFIG_ESPI_PERIPHERAL_EC_HOST_CMD` 和 :kconfig:option:`CONFIG_ESPI_PERIPHERAL_CUSTOM_OPCODE` 的eSPI从设备驱动程序 (eSPI - any eSPI slave driver that support :kconfig:option:`CONFIG_ESPI_PERIPHERAL_EC_HOST_CMD` and :kconfig:option:`CONFIG_ESPI_PERIPHERAL_CUSTOM_OPCODE`)
* UART - 任何支持异步API的UART驱动程序 (UART - any UART driver that supports the asynchronous API)
* SPI - STM32

初始化 (Initialization)
************************

如果应用程序配置了以下后端选定节点之一并且设置了 :kconfig:option:`CONFIG_EC_HOST_CMD_INITIALIZE_AT_BOOT`,则相应的后端通过调用 :c:func:`ec_host_cmd_init` 初始化主机命令子系统 (If the application configures one of the following backend chosen nodes and :kconfig:option:`CONFIG_EC_HOST_CMD_INITIALIZE_AT_BOOT` is set, then the corresponding backend initializes the host command subsystem by calling :c:func:`ec_host_cmd_init`):

* ``zephyr,host-cmd-espi-backend``
* ``zephyr,host-cmd-shi-backend``
* ``zephyr,host-cmd-uart-backend``
* ``zephyr,host-cmd-spi-backend``

如果没有配置后端选定节点,应用程序必须直接调用 :c:func:`ec_host_cmd_init` 函数 (If no backend chosen node is configured, the application must call the :c:func:`ec_host_cmd_init` function directly)。这种初始化方式在运行时根据例如GPIO状态选择后端时很有用 (This way of initialization is useful if a backend is chosen in runtime based on e.g. GPIO state)。

缓冲区 (Buffers)
*****************

主机命令通信需要用于rx和tx的缓冲区 (The host command communication requires buffers for rx and tx)。如果 :kconfig:option:`CONFIG_EC_HOST_CMD_HANDLER_RX_BUFFER_SIZE` > 0(用于rx缓冲区)和 :kconfig:option:`CONFIG_EC_HOST_CMD_HANDLER_TX_BUFFER_SIZE` > 0(用于tx缓冲区),则缓冲区由通用处理程序提供 (The buffers are be provided by the general handler if :kconfig:option:`CONFIG_EC_HOST_CMD_HANDLER_RX_BUFFER_SIZE` > 0 for rx buffer and :kconfig:option:`CONFIG_EC_HOST_CMD_HANDLER_TX_BUFFER_SIZE` > 0 for the tx buffer)。共享缓冲区对于使用多个后端的应用程序很有用 (The shared buffers are useful for applications that use multiple backends)。由每个后端定义单独的缓冲区会增加内存使用量 (Defining separate buffers by every backend would increase the memory usage)。但是,某些缓冲区可以由外设驱动程序定义,例如eSPI (However, some buffers can be defined by a peripheral driver e.g. eSPI)。这些应该尽可能重用 (These ones should be reused as much as possible)。

日志记录 (Logging)
*******************

主机命令具有嵌入式日志记录系统,用于记录正在进行的通信 (The host command has an embedded logging system of the ongoing communication)。有几个日志记录级别 (The are a few logging levels):

* :c:macro:`LOG_INF` 用于记录新命令的命令ID和非成功响应 (is used to log a command id of a new command and not success responses)。不记录相同命令的重复 (Repeats of the same command are not logged)
* :c:macro:`LOG_DBG` 记录每个命令,即使是重复的 (logs every command, even repeats)
* :c:macro:`LOG_DBG` + :kconfig:option:`CONFIG_EC_HOST_CMD_LOG_DBG_BUFFERS` 记录每个命令和响应及数据缓冲区 (logs every command and responses with the data buffers)

API参考 (API Reference)
************************

.. doxygengroup:: ec_host_cmd_interface
