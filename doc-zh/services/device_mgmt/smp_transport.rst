.. _mcumgr_smp_transport_specification:

SMP传输规范 (SMP Transport Specification)
##########################################

本文档指定了实现服务器端和客户端SMP传输所需的信息 (The documents specifies information needed for implementing server and client side SMP transports)。

.. _mcumgr_smp_transport_ble:

蓝牙低功耗(LE) (Bluetooth Low Energy (LE))
********************************************

MCUmgr客户端在实现SMP客户端时需要使用以下蓝牙特性 (MCUmgr Clients need to use following Bluetooth Characteristics, when implementing SMP client):

- **服务UUID (Service UUID)**: ``8D53DC1D-1DB7-4CD3-868B-8A527460AA84``
- **特性UUID (Characteristic UUID)**: ``DA2E7828-FBCE-4E01-AE9E-261174997C48``

所有SMP通信都使用单个GATT特性 (All SMP communication utilizes a single GATT characteristic)。SMP请求通过GATT无响应写入命令发送 (An SMP request is sent via a GATT Write Without Response command)。SMP响应以GATT通知的形式发送 (An SMP response is sent in the form of a GATT Notification)。

如果SMP请求或响应太大而无法容纳在单个GATT命令中 (If an SMP request or response is too large to fit in a single GATT command),发送方会将其分片到多个数据包中 (the sender fragments it across several packets)。当请求或响应被分片时不会引入额外的成帧 (No additional framing is introduced when a request or response is fragmented);有效载荷只是简单地在多个数据包之间分割 (the payload is simply split among several packets)。由于GATT保证数据包的有序传递 (Since GATT guarantees ordered delivery of packets),第一个分片中的SMP头包含足够的信息用于重组 (the SMP header in the first fragment contains sufficient information for reassembly)。

.. _mcumgr_smp_transport_uart:

UART/串行和控制台 (UART/serial and console)
********************************************

Zephyr的MCUmgr子系统的SMP协议规范使用基本的数据成帧来允许UART通道的多路复用 (SMP protocol specification by MCUmgr subsystem of Zephyr uses basic framing of data to allow multiplexing of UART channel)。多路复用需要在每个帧前面加上两字节标记并用换行符终止 (Multiplexing requires prefixing each frame with two byte marker and terminating it with newline)。
目前MCUmgr对帧大小施加了127字节的限制 (Currently MCUmgr imposes a 127 byte limit on frame size),尽管没有真正的协议约束需要该限制 (although there are no real protocol constraints that require that limit)。
该限制包括前缀和换行符 (The limit includes the prefix and the newline character),因此允许的有效载荷大小实际上是124字节 (so the allowed payload size is actually 124 bytes)。

尽管Zephyr中不存在这样的传输 (Although no such transport exists in Zephyr),但可以在UART传输上实现MCUmgr客户端/服务器 (it is possible to implement MCUmgr client/server over UART transport),该传输根本没有成帧 (that does not have framing at all),或使用硬件串行端口控制或其他成帧方式 (or uses hardware serial port control, or other means of framing)。

帧分片 (Frame fragmenting)
==========================

通过串行的SMP协议被分片为MTU大小的帧 (SMP protocol over serial is fragmented into MTU size frames);每个帧由两字节起始标记、主体和终止换行符组成 (each frame consists of two byte start marker, body and terminating newline character)。

有四种类型的帧 (There are four types of types of frames):初始帧、部分帧、部分最终帧和初始最终帧 (initial, partial, partial-final and initial-final);每种帧类型因起始标记和/或主体内容而不同 (each frame type differs by start marker and/or body contents)。

帧格式 (Frame formats)
-----------------------

初始帧需要后跟可选的部分帧序列 (Initial frame requires to be followed by optional sequence of partial frames),最后是部分最终帧 (and finally by partial-final frame)。
主体始终是Base64编码的 (Body is always Base64 encoded),因此这里描述为MTU - 3的主体大小 (so the body size, here described as MTU - 3),实际上能够携带N = (MTU - 3) / 4 * 3字节的原始数据 (is able to actually carry N = (MTU - 3) / 4 * 3 bytes of raw data)。

初始帧的主体之前有两字节的总数据包长度 (Body of initial frame is preceded by two byte total packet length),以大端序编码 (encoded in Big Endian),等于原始主体大小加上两字节CRC16的大小 (and equals size of a raw body plus two bytes, size of CRC16);这意味着允许进入初始帧的实际主体大小是N - 2 (this means that actual body size allowed into an initial frame is N - 2)。

如果主体大小小于N - 4 (If a body size is smaller than N - 4),那么可以在单个帧中携带整个主体及其前面的长度和后面的CRC (than it is possible to carry entire body with preceding length and following it CRC in a single frame),这里称为初始最终帧 (here called initial-final);有关初始最终帧的描述请看下文 (for the description of initial-final frame look below)。

初始帧格式 (Initial frame format):

.. table::
    :align: center

    +---------------+---------------+---------------------------+
    | 内容          | 大小          | 描述                      |
    | (Content)     | (Size)        | (Description)             |
    +===============+===============+===========================+
    | 0x06 0x09     | 2字节         | 帧起始标记                |
    |               | (2 bytes)     | (Frame start marker)      |
    +---------------+---------------+---------------------------+
    | <base64-i>    | 不超过        | Base64编码主体            |
    |               | MTU - 3字节   | (Base64 encoded body)     |
    |               | (no more than |                           |
    |               | MTU - 3 bytes)|                           |
    +---------------+---------------+---------------------------+
    | 0x0a          | 1字节         | 帧终止                    |
    |               | (1 byte)      | (Frame termination)       |
    +---------------+---------------+---------------------------+

``<base64-i>`` 是以下格式的Base64编码主体 (is Base64 encoded body of format):

.. table::
    :align: center

    +---------------+---------------+---------------------------+
    | 内容          | 大小          | 描述                      |
    | (Content)     | (Size)        | (Description)             |
    +===============+===============+===========================+
    | 总长度        | 2字节         | 大端序16位值,表示主体     |
    | (total length)| (2 bytes)     | 加2字节CRC16的总长度;     |
    |               |               | 注意总长度字段的大小      |
    |               |               | 不添加到总长度值中。      |
    |               |               | (Big endian 16-bit value  |
    |               |               | representing total length |
    |               |               | of body + 2 bytes for     |
    |               |               | CRC16; note that size of  |
    |               |               | total length field is not |
    |               |               | added to total length     |
    |               |               | value.)                   |
    +---------------+---------------+---------------------------+
    | 主体          | 不超过        | 原始主体数据片段          |
    | (body)        | MTU - 5       | (Raw body data fragment)  |
    |               | (no more than |                           |
    |               | MTU - 5)      |                           |
    +---------------+---------------+---------------------------+

初始最终帧格式类似于初始帧格式 (Initial-final frame format is similar to initial frame format),但 ``<base64-i>`` 定义不同 (but differs by ``<base64-i>`` definition)。

初始最终帧的 ``<base64-i>`` (``<base64-i>`` of initial-final frame),是采用以下形式的Base64编码数据 (is Base64 encoded data taking form):

.. table::
    :align: center

    +---------------+---------------+---------------------------+
    | 内容          | 大小          | 描述                      |
    | (Content)     | (Size)        | (Description)             |
    +===============+===============+===========================+
    | 总长度        | 2字节         | 大端序16位值,表示主体     |
    | (total length)| (2 bytes)     | 加2字节CRC16的总长度;     |
    |               |               | 注意总长度字段的大小      |
    |               |               | 不添加到总长度值中。      |
    |               |               | (Big endian 16-bit value  |
    |               |               | representing total length |
    |               |               | of body + 2 bytes for     |
    |               |               | CRC16; note that size of  |
    |               |               | total length field is not |
    |               |               | added to total length     |
    |               |               | value.)                   |
    +---------------+---------------+---------------------------+
    | 主体          | 不超过        | 原始主体数据片段          |
    | (body)        | MTU - 7       | (Raw body data fragment)  |
    |               | (no more than |                           |
    |               | MTU - 7)      |                           |
    +---------------+---------------+---------------------------+
    | crc16         | 2字节         | 整个数据包主体的CRC16,    |
    |               | (2 bytes)     | 不包括前面的长度。        |
    |               |               | (CRC16 of entire packet   |
    |               |               | body, preceding length    |
    |               |               | not included.)            |
    +---------------+---------------+---------------------------+

部分帧是在之前的初始帧或其他部分帧之后的继续 (Partial frame is continuation after previous initial or other partial frame)。部分帧采用以下形式 (Partial frame takes form):

.. table::
    :align: center

    +---------------+---------------+---------------------------+
    | 内容          | 大小          | 描述                      |
    | (Content)     | (Size)        | (Description)             |
    +===============+===============+===========================+
    | 0x04 0x14     | 2字节         | 帧起始标记                |
    |               | (2 bytes)     | (Frame start marker)      |
    +---------------+---------------+---------------------------+
    | <base64-i>    | 不超过        | Base64编码主体            |
    |               | MTU - 3字节   | (Base64 encoded body)     |
    |               | (no more than |                           |
    |               | MTU - 3 bytes)|                           |
    +---------------+---------------+---------------------------+
    | 0x0a          | 1字节         | 帧终止                    |
    |               | (1 byte)      | (Frame termination)       |
    +---------------+---------------+---------------------------+

部分帧的 ``<base64-i>`` (The ``<base64-i>`` of partial frame) 是采用以下形式的数据的Base64编码 (is Base64 encoding of data, taking form):

.. table::
    :align: center

    +---------------+---------------+---------------------------+
    | 内容          | 大小          | 描述                      |
    | (Content)     | (Size)        | (Description)             |
    +===============+===============+===========================+
    | 主体          | 不超过        | 原始主体数据片段          |
    | (body)        | MTU - 3       | (Raw body data fragment)  |
    |               | (no more than |                           |
    |               | MTU - 3)      |                           |
    +---------------+---------------+---------------------------+

部分最终帧的 ``<base64-i>`` (The ``<base64-i>`` of partial-final frame) 是采用以下形式的数据的Base64编码 (is Base64 encoding of data, taking form):

.. table::
    :align: center

    +---------------+---------------+---------------------------+
    | 内容          | 大小          | 描述                      |
    | (Content)     | (Size)        | (Description)             |
    +===============+===============+===========================+
    | 主体          | 不超过        | 原始主体数据片段          |
    | (body)        | MTU - 5       | (Raw body data fragment)  |
    |               | (no more than |                           |
    |               | MTU - 5)      |                           |
    +---------------+---------------+---------------------------+
    | crc16         | 2字节         | 整个数据包主体的CRC16,    |
    |               | (2 bytes)     | 不包括前面的长度。        |
    |               |               | (CRC16 of entire packet   |
    |               |               | body, preceding length    |
    |               |               | not included.)            |
    +---------------+---------------+---------------------------+


CRC详细信息 (CRC Details)
--------------------------

最终类型帧中包含的CRC16仅对原始数据计算 (The CRC16 included in final type frames is calculated over only raw data),不包括数据包长度 (and does not include packet length)。
CRC16多项式是0x1021,初始值是0 (CRC16 polynomial is 0x1021 and initial value is 0)。

API参考 (API Reference)
************************

.. doxygengroup:: mcumgr_transport_smp
