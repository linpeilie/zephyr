.. _modem:

调制解调器模块 (Modem modules)
###############################

此服务提供与调制解调器通信所需的模块。(This service provides modules necessary to communicate with modems.)

调制解调器是独立的设备,实现了执行射频(RF)通信所需的硬件和软件,包括 GNSS、蜂窝网络、WiFi 等。(Modems are self-contained devices that implement the hardware and software necessary to perform RF (Radio-Frequency) communication, including GNSS, Cellular, WiFi etc.)

调制解调器模块使用数据输入/数据输出管道动态互连,使它们可以独立测试并且高度灵活,确保稳定性和可扩展性。(The modem modules are inter-connected dynamically using data-in/data-out pipes making them independently testable and highly flexible, ensuring stability and scalability.)

调制解调器管道 (Modem pipe)
****************************

此模块用于以线程安全的方式抽象通过各种机制(如 UART 和 CMUX DLCI 通道)进行的数据输入/数据输出通信。(This module is used to abstract data-in/data-out communication over a variety of mechanisms, like UART and CMUX DLCI channels, in a thread-safe manner.)

调制解调器后端将在内部包含一个 modem_pipe 结构的实例,以及抽象其底层机制所需的任何缓冲区和附加结构。(A modem backend will internally contain an instance of a modem_pipe structure, alongside any buffers and additional structures required to abstract away its underlying mechanism.)

调制解调器后端在初始化时将返回指向其内部 modem_pipe 结构的指针,该指针将用于通过调制解调器管道 API 与后端交互。(The modem backend will return a pointer to its internal modem_pipe structure when initialized, which will be used to interact with the backend through the modem pipe API.)

.. doxygengroup:: modem_pipe

调制解调器 PPP (Modem PPP)
***************************

此模块定义并绑定一个 L2 PPP 网络接口(在 :ref:`net_l2_interface` 中描述)到调制解调器后端。L2 PPP 接口发送和接收网络数据包。这些网络数据包在通过调制解调器后端传输之前必须包装在 PPP 帧中。此模块执行所述包装。(This module defines and binds a L2 PPP network interface, described in :ref:`net_l2_interface`, to a modem backend. The L2 PPP interface sends and receives network packets. These network packets have to be wrapped in PPP frames before being transported via a modem backend. This module performs said wrapping.)

.. doxygengroup:: modem_ppp

调制解调器 CMUX (Modem CMUX)
*****************************

此模块是遵循 3GPP 27.010 规范的 CMUX 实现。CMUX 是一种多路复用协议,允许多个双向数据流,称为 DLCI 通道。该模块连接到单个调制解调器后端,暴露多个调制解调器后端,每个后端代表一个 DLCI 通道。(This module is an implementation of CMUX following the 3GPP 27.010 specification. CMUX is a multiplexing protocol, allowing for multiple bi-directional streams of data, called DLCI channels. The module attaches to a single modem backend, exposing multiple modem backends, each representing a DLCI channel.)

.. doxygengroup:: modem_cmux

调制解调器管道链接 (Modem pipelink)
************************************

此模块用于全局共享调制解调器管道。此模块旨在将设备驱动程序中调制解调器管道的创建和设置与所述管道的用户解耦。有关如何在设备驱动程序和应用程序之间使用调制解调器管道链接的示例,请参见 :zephyr_file:`drivers/modem/modem_at_shell.c` 和 :zephyr_file:`drivers/modem/modem_cellular.c`。(This module is used to share modem pipes globally. This module aims to decouple the creation and setup of modem pipes in device drivers from the users of said pipes. See :zephyr_file:`drivers/modem/modem_at_shell.c` and :zephyr_file:`drivers/modem/modem_cellular.c` for examples of how to use the modem pipelink between device driver and application.)

.. doxygengroup:: modem_pipelink
