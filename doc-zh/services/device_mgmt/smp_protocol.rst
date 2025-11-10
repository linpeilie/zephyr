.. _mcumgr_smp_protocol_specification:

SMP协议规范 (SMP Protocol Specification)
#########################################

这是MCUmgr用于向设备传递请求并从设备接收响应的简单管理协议(SMP)的描述 (This is description of Simple Management Protocol, SMP, that is used by MCUmgr to pass requests to devices and receive responses from them)。

SMP是应用层协议 (SMP is an application layer protocol)。底层传输层不在本文档的范围内 (The underlying transport layer is not in scope of this documentation)。

.. note::
    此处的SMP指的是MCUmgr的SMP(简单管理协议) (SMP in this context refers to SMP for MCUmgr (Simple Management Protocol)),
    它与蓝牙中的SMP(安全管理器协议)无关,但有一个用于蓝牙的MCUmgr SMP传输 (it is unrelated to SMP in Bluetooth (Security Manager Protocol), but there is an MCUmgr SMP transport for Bluetooth)。

帧:信封 (Frame: The envelope)
******************************

每个帧由头和数据组成 (Each frame consists of a header and data)。如果底层传输层支持分片,头中的 ``Data Length`` 字段可用于重组目的 (The ``Data Length`` field in the header may be used for reassembly purposes if underlying transport layer supports fragmentation)。
当字段超过一个字节长时,帧以"大端序"(网络字节序)编码,并采用以下形式 (Frames are encoded in "Big Endian" (Network endianness) when fields are more than one byte long, and takes the following form):

.. _mcumgr_smp_protocol_frame:

.. table::
    :align: center

    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |3              |2              |1              |0              |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |7|6|5|4|3|2|1|0|7|6|5|4|3|2|1|0|7|6|5|4|3|2|1|0|7|6|5|4|3|2|1|0|
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | Res |Ver| OP  |      Flags    |          Data Length          |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |            Group ID           | Sequence Num  |   Command ID  |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                             Data                              |
    |                             ...                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

.. note::
    原始规范声明SMP应支持接收"小端序"和"大端序"帧,但实际上MCUmgr库被硬编码为始终将"网络"端视为"大端序" (The original specification states that SMP should support receiving both the "Little-endian" and "Big-endian" frames but in reality the MCUmgr library is hardcoded to always treat "Network" side as "Big-endian")。


数据是可选的,当 ``Data Length`` 为零时不存在 (Data is optional and is not present when ``Data Length`` is zero)。
数据的编码取决于组/ID的目标 (The encoding of data depends on the target of group/ID)。

各个字段及其含义的描述 (A description of the various fields and their meaning):

.. table::
    :align: center

    +-------------------+---------------------------------------------------+
    | 字段 (Field)      | 描述 (Description)                                |
    +===================+===================================================+
    | ``Res``           | 这是保留的未使用字段,必须始终设置为0              |
    |                   | (This is reserved, not-used field and must be     |
    |                   | always set to 0)。                                |
    +-------------------+---------------------------------------------------+
    | ``Ver`` (Version) | 这表示正在使用的协议版本,应设置为0b01以使用较新   |
    |                   | 的SMP传输,其中错误代码更详细并在映射中返回,       |
    |                   | 否则保留为0b00以使用传统SMP协议                   |
    |                   | (This indicates the version of the protocol being |
    |                   | used, this should be set to 0b01 to use the newer|
    |                   | SMP transport where error codes are more detailed |
    |                   | and returned in the map, otherwise left as 0b00   |
    |                   | to use the legacy SMP protocol)。版本0b10和0b11   |
    |                   | 保留供将来使用,不应使用                           |
    |                   | (Versions 0b10 and 0b11 are reserved for future   |
    |                   | use and should not be used)。                     |
    +-------------------+---------------------------------------------------+
    | ``OP``            | :c:enum:`mcumgr_op_t`,确定是否将信息写入设备或从  |
    |                   | 设备请求信息,以及数据包是包含对SMP服务器的请求    |
    |                   | 还是来自服务器的响应                              |
    |                   | (:c:enum:`mcumgr_op_t`, determines whether        |
    |                   | information is written to a device or requested   |
    |                   | from it and whether a packet contains request to  |
    |                   | an SMP server or response from it)。              |
    +-------------------+---------------------------------------------------+
    | ``Flags``         | 为标志保留;目前尚未定义标志,该字段应设置为0       |
    |                   | (Reserved for flags; there are no flags defined   |
    |                   | yet, the field should be set to 0)                |
    +-------------------+---------------------------------------------------+
    | ``Data Length``   | ``Data`` 字段的长度                               |
    |                   | (Length of the ``Data`` field)                    |
    +-------------------+---------------------------------------------------+
    | ``Group ID``      | :c:enum:`mcumgr_group_t`,详见                     |
    |                   | :ref:`mcumgr_smp_protocol_group_ids`              |
    |                   | (:c:enum:`mcumgr_group_t`, see                    |
    |                   | :ref:`mcumgr_smp_protocol_group_ids` for further  |
    |                   | details)。                                        |
    +-------------------+---------------------------------------------------+
    | ``Sequence Num``  | 这是帧序列号 (This is a frame sequence number)。  |
    |                   | 每个请求帧的编号增加1                             |
    |                   | (The number is increased by one with each request |
    |                   | frame)。                                          |
    |                   | 响应的序列号应与请求中的序列号匹配                |
    |                   | (The Sequence Num of a response should match      |
    |                   | the one in the request)。                         |
    +-------------------+---------------------------------------------------+
    | ``Command ID``    | 这是 ``Group`` 内的命令                           |
    |                   | (This is a command, within ``Group``)。           |
    +-------------------+---------------------------------------------------+
    | ``Data``          | 这是 ``Data Length`` 大小的数据有效载荷           |
    |                   | (This is data payload of the ``Data Length``      |
    |                   | size)。它是可选的,因为 ``Data Length`` 可以设置  |
    |                   | 为零,这意味着头后没有数据                         |
    |                   | (It is optional as ``Data Length`` may be set to  |
    |                   | zero, which means that no data follows the        |
    |                   | header)。                                         |
    +-------------------+---------------------------------------------------+

.. note::
    ``Data`` 的内容取决于 ``OP``、``Group ID`` 和 ``Command ID`` 的值 (Contents of ``Data`` depends on a value of an ``OP``, a ``Group ID``, and a ``Command ID``)。

.. _mcumgr_smp_protocol_group_ids:

管理 ``Group ID``'s (Management ``Group ID``'s)
================================================

SMP协议支持预定义的公共组并允许用户定义的组 (The SMP protocol supports predefined common groups and allows user defined groups)。下表列出了公共组列表 (The following table presents a list of common groups):


.. table::
    :align: center

    +---------------+-----------------------------------------------+
    | 十进制 ID     | 组描述                                        |
    | (Decimal ID)  | (Group description)                           |
    +===============+===============================================+
    | ``0``         | :ref:`mcumgr_smp_group_0`                     |
    +---------------+-----------------------------------------------+
    | ``1``         | :ref:`mcumgr_smp_group_1`                     |
    +---------------+-----------------------------------------------+
    | ``2``         | :ref:`mcumgr_smp_group_2`                     |
    +---------------+-----------------------------------------------+
    | ``3``         | :ref:`mcumgr_smp_group_3`                     |
    +---------------+-----------------------------------------------+
    | ``4``         | 应用程序/系统日志管理                         |
    |               | (Application/system log management)           |
    |               | (Zephyr当前未使用)                            |
    |               | (currently not used by Zephyr)                |
    +---------------+-----------------------------------------------+
    | ``5``         | 运行时测试                                    |
    |               | (Run-time tests)                              |
    |               | (Zephyr未使用)                                |
    |               | (unused by Zephyr)                            |
    +---------------+-----------------------------------------------+
    | ``6``         | 分割映像管理                                  |
    |               | (Split image management)                      |
    |               | (Zephyr未使用)                                |
    |               | (unused by Zephyr)                            |
    +---------------+-----------------------------------------------+
    | ``7``         | 测试崩溃应用程序                              |
    |               | (Test crashing application)                   |
    |               | (Zephyr未使用)                                |
    |               | (unused by Zephyr)                            |
    +---------------+-----------------------------------------------+
    | ``8``         | :ref:`mcumgr_smp_group_8`                     |
    +---------------+-----------------------------------------------+
    | ``9``         | :ref:`mcumgr_smp_group_9`                     |
    +---------------+-----------------------------------------------+
    | ``63``        | :ref:`mcumgr_smp_group_63`                    |
    +---------------+-----------------------------------------------+
    | ``64``        | 这是定义应用程序特定管理组的基础组。          |
    |               | (This is the base group for defining          |
    |               | an application specific management groups.)   |
    +---------------+-----------------------------------------------+

上述组(除了用户组 ``64`` 及以上)的有效载荷始终使用CBOR编码 (The payload for above groups, except for user groups (``64`` and above) is always CBOR encoded)。组 ``64`` 及以上可以定义自己的数据通信方案 (The group ``64``, and above can define their own scheme for data communication)。

最小响应 (Minimal response)
****************************

无论发出什么命令,只要请求的另一端有SMP客户端,就应该发出包含头后跟CBOR map容器的响应 (Regardless of a command issued, as long as there is SMP client on the other side of a request, a response should be issued containing the header followed by CBOR map container)。
只有在没有SMP服务或设备无响应时才允许缺少响应 (Lack of response is only allowed when there is no SMP service or device is non-responsive)。

最小响应SMP数据 (Minimal response SMP data)
============================================

最小响应是 (Minimal response is):

.. tabs::

   .. group-tab:: SMP version 2 (SMP版本2)

      .. code-block:: none

          {
              (str)"err" : {
                  (str)"group"    : (uint)
                  (str)"rc"       : (uint)
              }
          }

   .. group-tab:: SMP version 1 (and non-group SMP version 2) (SMP版本1(及非组SMP版本2))

      .. code-block:: none

          {
              (str)"rc"       : (int)
          }

其中 (where):

.. table::
    :align: center

    +------------------+-------------------------------------------------------------------------+
    | "err" -> "group" | :c:enum:`mcumgr_group_t` 基于组的错误代码的组。                        |
    |                  | (group of the group-based error code.)                                  |
    |                  | 仅在使用SMP版本2返回错误时出现。                                        |
    |                  | (Only appears if an error is returned when using SMP version 2.)        |
    +------------------+-------------------------------------------------------------------------+
    | "err" -> "rc"    | 包含基于组的错误代码的索引。                                            |
    |                  | (contains the index of the group-based error code.)                     |
    |                  | 仅在非零(错误条件)时使用SMP版本2出现。                                  |
    |                  | (Only appears if non-zero (error condition) when using SMP version 2.)  |
    +------------------+-------------------------------------------------------------------------+
    | "rc"             | :c:enum:`mcumgr_err_t` 仅在非零(错误条件)时出现,                        |
    |                  | (only appears if non-zero (error condition))                            |
    |                  | 当使用SMP版本1时,或当使用SMP版本2时用于SMP错误。                        |
    |                  | (when using SMP version 1 or for SMP errors when using SMP version 2.)  |
    +------------------+-------------------------------------------------------------------------+

请注意,在成功执行命令的情况下,将返回空map (Note that in the case of a successful command, an empty map will be returned) (``rc``/``err`` 仅在出现错误条件时返回 (is only returned if there is an error condition),因此如果仅返回空map或响应缺少这些 (therefore if only an empty map is returned or a response lacks these),则可以认为请求成功 (the request can be considered as being successful))。对于SMP版本2 (For SMP version 2),与SMP本身相关但不特定于组的错误仍将作为 ``rc`` 错误返回 (errors relating to SMP itself that are not group specific will still be returned as ``rc`` errors),因此SMP版本2客户端必须能够处理两种类型的错误 (SMP version 2 clients must therefore be able to handle both types of errors)。

Zephyr支持的管理组规范 (Specifications of management groups supported by Zephyr)
**********************************************************************************

.. toctree::
    :maxdepth: 1

    smp_groups/smp_group_0.rst
    smp_groups/smp_group_1.rst
    smp_groups/smp_group_2.rst
    smp_groups/smp_group_3.rst
    smp_groups/smp_group_8.rst
    smp_groups/smp_group_9.rst
    smp_groups/smp_group_10.rst
    smp_groups/smp_group_63.rst
