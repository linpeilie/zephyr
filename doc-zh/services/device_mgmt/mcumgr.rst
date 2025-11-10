.. _mcu_mgr:

MCUmgr
#######

概述 (Overview)
****************

管理子系统允许远程管理支持Zephyr的设备 (The management subsystem allows remote management of Zephyr-enabled devices)。
可用的管理操作如下 (The following management operations are available):

* 镜像管理 (Image management)
* 文件系统管理 (File System management)
* 操作系统管理 (OS management)
* 设置(配置)管理 (Settings (config) management)
* Shell管理 (Shell management)
* 统计管理 (Statistic management)
* Zephyr管理 (Zephyr management)

通过以下传输方式 (over the following transports):

* 低功耗蓝牙(LE) (Bluetooth Low Energy (LE))
* 串行(UART) (Serial (UART))
* UDP over IP

管理子系统基于 `MCUmgr`_ 提供的简单管理协议(SMP) (The management subsystem is based on the Simple Management Protocol (SMP) provided by `MCUmgr`_),这是一个开源项目,提供跨多个实时操作系统可移植的管理子系统 (an open source project that provides a management subsystem that is portable across multiple real-time operating systems)。

管理子系统位于Zephyr树内的 :zephyr_file:`subsys/mgmt/` 中 (The management subsystem is located in :zephyr_file:`subsys/mgmt/` inside of the Zephyr tree)。

此外,还有一个通过低功耗蓝牙和串行提供管理功能的 :zephyr:code-sample:`示例服务器 <smp-svr>` (Additionally, there is a :zephyr:code-sample:`sample <smp-svr>` server that provides management functionality over Bluetooth LE and serial)。

.. _mcumgr_tools_libraries:

工具/库 (Tools/libraries)
***************************

有各种工具和库可用于在设备上启用MCUmgr功能,如下所列 (There are various tools and libraries available which enable usage of MCUmgr functionality on a device which are listed below)。请注意,这些工具不是Zephyr项目的一部分或与之相关 (Note that these tools are not part of or related to the Zephyr project)。

.. only:: html

    .. table:: Tools and Libraries for MCUmgr
        :align: center

        +--------------------------------------------------------------------------------+-------------------------------------------+--------------------------+---------------------------------------------------------+---------------+------------+------------+
        | Name                                                                           | OS support                                | Transports               | Groups                                                  | Type          | Language   | License    |
        |                                                                                +---------+-------+-----+--------+----------+--------+-----------+-----+----+-----+------+----------+----+-------+------+--------+               |            |            |
        |                                                                                | Windows | Linux | mac | Mobile | Embedded | Serial | Bluetooth | UDP | OS | IMG | Stat | Settings | FS | Shell | Enum | Zephyr |               |            |            |
        +================================================================================+=========+=======+=====+========+==========+========+===========+=====+====+=====+======+==========+====+=======+======+========+===============+============+============+
        | `AuTerm <https://github.com/thedjnK/AuTerm/>`_                                 | ✓       | ✓     | ✓   | ✕      | ✕        | ✓      | ✓         | ✓   | ✓  | ✓   | ✓    | ✓        | ✓  | ✓     | ✓    | ✓      | Application   | C++ (Qt)   | GPL-3.0    |
        +--------------------------------------------------------------------------------+---------+-------+-----+--------+----------+--------+-----------+-----+----+-----+------+----------+----+-------+------+--------+---------------+------------+------------+
        | `mcumgr-client <https://github.com/vouch-opensource/mcumgr-client/>`_          | ✓       | ✓     | ✓   | ✕      | ✕        | ✓      | ✕         | ✕   | ✕  | ✓   | ✕    | ✕        | ✕  | ✕     | ✕    | ✕      | Application   | Rust       | Apache-2.0 |
        +--------------------------------------------------------------------------------+---------+-------+-----+--------+----------+--------+-----------+-----+----+-----+------+----------+----+-------+------+--------+---------------+------------+------------+
        | `mcumgr-web <https://github.com/boogie/mcumgr-web/>`_                          | ✓       | ✓     | ✓   | ✕      | ✕        | ✕      | ✓         | ✕   | ✕  | ✓   | ✕    | ✕        | ✕  | ✕     | ✕    | ✕      | Web page      | Javascript | MIT        |
        |                                                                                |         |       |     |        |          |        |           |     |    |     |      |          |    |       |      |        | (chrome only) |            |            |
        +--------------------------------------------------------------------------------+---------+-------+-----+--------+----------+--------+-----------+-----+----+-----+------+----------+----+-------+------+--------+---------------+------------+------------+
        | nRF Connect Device Manager: |br|                                               |         |       |     |        |          |        |           |     |    |     |      |          |    |       |      |        |               |            |            |
        | `Android                                                                       | ✕       | ✕     | ✕   | ✓      | ✕        | ✕      | ✓         | ✕   | ✓  | ✓   | ✓    | ✓        | ✓  | ✓     | ✕    | ✓      | Library and   | Java,      | Apache-2.0 |
        | <https://github.com/NordicSemiconductor/Android-nRF-Connect-Device-Manager/>`_ |         |       |     |        |          |        |           |     |    |     |      |          |    |       |      |        | application   | Kotlin,    |            |
        | and `iOS                                                                       |         |       |     |        |          |        |           |     |    |     |      |          |    |       |      |        |               | Swift      |            |
        | <https://github.com/NordicSemiconductor/IOS-nRF-Connect-Device-Manager>`_      |         |       |     |        |          |        |           |     |    |     |      |          |    |       |      |        |               |            |            |
        +--------------------------------------------------------------------------------+---------+-------+-----+--------+----------+--------+-----------+-----+----+-----+------+----------+----+-------+------+--------+---------------+------------+------------+
        | `smp <https://pypi.org/project/smp/>`_                                         | ✓       | ✓     | ✓   | ✓      | ✕        | N/A    | N/A       | N/A | ✓  | ✓   | ✓    | ✓        | ✓  | ✓     | ✕    | ✓      | Library       | Python     | Apache-2.0 |
        +--------------------------------------------------------------------------------+---------+-------+-----+--------+----------+--------+-----------+-----+----+-----+------+----------+----+-------+------+--------+---------------+------------+------------+
        | `smpclient <https://pypi.org/project/smpclient/>`_                             | ✓       | ✓     | ✓   | ✕      | ✕        | ✓      | ✓         | ✓   | ✓  | ✓   | ✓    | ✓        | ✓  | ✓     | ✕    | ✓      | Library       | Python     | Apache-2.0 |
        +--------------------------------------------------------------------------------+---------+-------+-----+--------+----------+--------+-----------+-----+----+-----+------+----------+----+-------+------+--------+---------------+------------+------------+
        | Zephyr MCUmgr client (in-tree)                                                 | ✕       | ✓     | ✕   | ✕      | ✓        | ✓      | ✓         | ✓   | ✓  | ✓   | ✕    | ✕        | ✕  | ✕     | ✕    | ✕      | Library       | C          | Apache-2.0 |
        +--------------------------------------------------------------------------------+---------+-------+-----+--------+----------+--------+-----------+-----+----+-----+------+----------+----+-------+------+--------+---------------+------------+------------+

.. only:: latex

    .. raw:: latex

       \begin{landscape}

    .. table:: Tools and Libraries for MCUmgr
        :align: center

        +--------------------------------------------------------------------------------+---------------+-----------------+---------------------------------------------------------+---------------+------------+
        | Name                                                                           | OS support    | Transports      | Groups                                                  | Type          | Language   |
        |                                                                                |               |                 +----+-----+------+----------+----+-------+------+--------+               |            |
        |                                                                                |               |                 | OS | IMG | Stat | Settings | FS | Shell | Enum | Zephyr |               |            |
        +================================================================================+===============+=================+====+=====+======+==========+====+=======+======+========+===============+============+
        | `AuTerm <https://github.com/thedjnK/AuTerm/>`_                                 | Windows, |br| | Serial, |br|    | ✓  | ✓   | ✓    | ✓        | ✓  | ✓     | ✓    | ✓      | App           | C++ (Qt)   |
        |                                                                                | Linux, |br|   | Bluetooth, |br| |    |     |      |          |    |       |      |        |               |            |
        |                                                                                | macOS         | UDP             |    |     |      |          |    |       |      |        |               |            |
        +--------------------------------------------------------------------------------+---------------+-----------------+----+-----+------+----------+----+-------+------+--------+---------------+------------+
        | `mcumgr-client <https://github.com/vouch-opensource/mcumgr-client/>`_          | Windows, |br| | Serial          | ✕  | ✓   | ✕    | ✕        | ✕  | ✕     | ✕    | ✕      | App           | Rust       |
        |                                                                                | Linux, |br|   |                 |    |     |      |          |    |       |      |        |               |            |
        |                                                                                | macOS         |                 |    |     |      |          |    |       |      |        |               |            |
        +--------------------------------------------------------------------------------+---------------+-----------------+----+-----+------+----------+----+-------+------+--------+---------------+------------+
        | `mcumgr-web <https://github.com/boogie/mcumgr-web/>`_                          | Windows, |br| | Bluetooth       | ✕  | ✓   | ✕    | ✕        | ✕  | ✕     | ✕    | ✕      | Web (chrome   | Javascript |
        |                                                                                | Linux, |br|   |                 |    |     |      |          |    |       |      |        | only)         |            |
        |                                                                                | macOS         |                 |    |     |      |          |    |       |      |        |               |            |
        +--------------------------------------------------------------------------------+---------------+-----------------+----+-----+------+----------+----+-------+------+--------+---------------+------------+
        | nRF Connect Device Manager: |br|                                               | iOS, |br|     | Bluetooth       | ✓  | ✓   | ✓    | ✓        | ✓  | ✓     | ✕    | ✓      | Library, App  | Java,      |
        | `Android                                                                       | Android       |                 |    |     |      |          |    |       |      |        |               | Kotlin,    |
        | <https://github.com/NordicSemiconductor/Android-nRF-Connect-Device-Manager/>`_ |               |                 |    |     |      |          |    |       |      |        |               | Swift      |
        | and `iOS                                                                       |               |                 |    |     |      |          |    |       |      |        |               |            |
        | <https://github.com/NordicSemiconductor/IOS-nRF-Connect-Device-Manager>`_      |               |                 |    |     |      |          |    |       |      |        |               |            |
        +--------------------------------------------------------------------------------+---------------+-----------------+----+-----+------+----------+----+-------+------+--------+---------------+------------+
        | `smp <https://pypi.org/project/smp/>`_                                         | Windows, |br| | N/A             | ✓  | ✓   | ✓    | ✓        | ✓  | ✓     | ✕    | ✓      | Library       | Python     |
        |                                                                                | Linux, |br|   |                 |    |     |      |          |    |       |      |        |               |            |
        |                                                                                | macOS, |br|   |                 |    |     |      |          |    |       |      |        |               |            |
        |                                                                                | iOS, |br|     |                 |    |     |      |          |    |       |      |        |               |            |
        |                                                                                | Android       |                 |    |     |      |          |    |       |      |        |               |            |
        +--------------------------------------------------------------------------------+---------------+-----------------+----+-----+------+----------+----+-------+------+--------+---------------+------------+
        | `smpclient <https://pypi.org/project/smpclient/>`_                             | Windows, |br| | Serial, |br|    | ✓  | ✓   | ✓    | ✓        | ✓  | ✓     | ✕    | ✓      | Library       | Python     |
        |                                                                                | Linux, |br|   | Bluetooth, |br| |    |     |      |          |    |       |      |        |               |            |
        |                                                                                | macOS         | UDP             |    |     |      |          |    |       |      |        |               |            |
        +--------------------------------------------------------------------------------+---------------+-----------------+----+-----+------+----------+----+-------+------+--------+---------------+------------+
        | Zephyr MCUmgr client (in-tree)                                                 | Linux, |br|   | Serial, |br|    | ✓  | ✓   | ✕    | ✕        | ✕  | ✕     | ✕    | ✕      | Library       | C          |
        |                                                                                | Zephyr        | Bluetooth, |br| |    |     |      |          |    |       |      |        |               |            |
        |                                                                                |               | UDP             |    |     |      |          |    |       |      |        |               |            |
        +--------------------------------------------------------------------------------+---------------+-----------------+----+-----+------+----------+----+-------+------+--------+---------------+------------+

    .. raw:: latex

        \end{landscape}

请注意,特定组的勾选表示代码中对该组的基本支持,实现可能不支持组的所有命令/功能 (Note that a tick for a particular group indicates basic support for that group in the code, it is possible that not all commands/features of a group are supported by the implementation)。

.. _mcumgr_jlink_ob_virtual_msd:

J-Link虚拟MSD交互说明 (J-Link Virtual MSD Interaction Note)
***********************************************************

在存在同时具有CDC和MSC(虚拟大容量存储设备,也称为拖放)支持的J-Link OB的板上,MSD功能可能会阻止通过CDC UART端口进行的MCUmgr命令工作,因为J-Link固件中USB端点的配置方式(例如在 :zephyr:board:`nrf52840dk` 板上),因为限制了最大数据包大小(最有可能在使用镜像管理命令更新固件时发生) (On boards where a J-Link OB is present which has both CDC and MSC (virtual Mass Storage Device, also known as drag-and-drop) support, the MSD functionality can prevent MCUmgr commands over the CDC UART port from working due to how USB endpoints are configured in the J-Link firmware (for example on the :zephyr:board:`nrf52840dk` board) because of limiting the maximum packet size (most likely to occur when using image management commands for updating firmware))。此问题可以通过禁用J-Link设备上的MSD功能来解决,请按照 :ref:`nordic_segger_msd` 上的说明禁用MSD支持 (This issue can be resolved by disabling MSD functionality on the J-Link device, follow the instructions on :ref:`nordic_segger_msd` to disable MSD support)。

引导加载程序集成 (Bootloader Integration)
******************************************

:ref:`dfu` 子系统将管理子系统与引导加载程序集成,提供向设备发送和升级Zephyr镜像的能力 (The :ref:`dfu` subsystem integrates the management subsystem with the bootloader, providing the ability to send and upgrade a Zephyr image to a device)。

当前仅支持MCUboot引导加载程序 (Currently only the MCUboot bootloader is supported)。有关更多信息,请参见 :ref:`mcuboot` (See :ref:`mcuboot` for more information)。

.. _MCUmgr: https://github.com/apache/mynewt-mcumgr
.. _MCUboot design: https://github.com/mcu-tools/mcuboot/blob/main/docs/design.md

Discord频道 (Discord channel)
*****************************

欢迎开发者! (Developers welcome!)

* Discord mcumgr频道 (Discord mcumgr channel): https://discord.com/invite/Ck7jw53nU2

API参考 (API Reference)
************************

.. doxygengroup:: mcumgr_mgmt_api
