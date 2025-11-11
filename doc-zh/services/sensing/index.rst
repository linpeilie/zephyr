.. _sensing:

传感子系统 (Sensing Subsystem)
##############################

.. contents::
    :local:
    :depth: 2

概述 (Overview)
***************

传感子系统是操作系统用户空间服务层内的高级传感器框架。它是一个专注于传感器融合、客户端仲裁、采样、定时、调度和基于传感器的电源管理的框架。(Sensing Subsystem is a high level sensor framework inside the OS user space service layer. It is a framework focused on sensor fusion, client arbitration, sampling, timing, scheduling and sensor based power management.)

传感子系统中的关键概念包括物理传感器和虚拟传感器对象,以及传感器对象关系上的调度框架。物理传感器不依赖任何其他传感器对象作为输入,将直接与现有的 Zephyr 传感器设备驱动程序交互。虚拟传感器依赖其他传感器对象(物理或虚拟)作为报告输入。(Key concepts in Sensing Subsystem include physical sensor and virtual sensor objects, and a scheduling framework over sensor object relationships. Physical sensors do not depend on any other sensor objects for input, and will directly interact with existing zephyr sensor device drivers. Virtual sensors rely on other sensor objects (physical or virtual) as report inputs.)

传感子系统依赖 Zephyr 传感器设备 API(现有版本或未来更新)来利用 Zephyr 的大型传感器设备驱动程序库(100+)。(The sensing subsystem relies on Zephyr sensor device APIs (existing version or update in future) to leverage Zephyr's large library of sensor device drivers (100+).)

传感子系统的使用是可选的。只需要访问简单传感器设备的应用程序可以直接使用 Zephyr :ref:`sensor` API。(Use of the sensing subsystem is optional. Applications that only need to access simple sensors devices can use the Zephyr :ref:`sensor` API directly.)

由于传感子系统与设备驱动程序层或内核空间分离,并且可以通过虚拟传感器概念在用户空间中支持各种自定义和传感器算法。现有的传感器设备驱动程序可以专注于低层设备端工作,可以尽可能保持简单,只提供设备硬件抽象和操作等。这对系统稳定性非常有利。(Since the sensing subsystem is separated from device driver layer or kernel space and could support various customizations and sensor algorithms in user space with virtual sensor concepts. The existing sensor device driver can focus on low layer device side works, can keep simple as much as possible, just provide device HW abstraction and operations etc. This is very good for system stability.)

传感子系统与任何传感器暴露/传输协议解耦,目标是支持具有不同传感器暴露/传输协议的各种上层框架和应用程序,例如 `CHRE <https://github.com/zephyrproject-rtos/chre>`_、HID 传感器应用程序、MQTT 传感器应用程序,根据不同的产品需求。甚至通过其多客户端支持设计,同时支持具有不同上层传感器协议的多个应用程序。(The sensing subsystem is decoupled with any sensor expose/transfer protocols, the target is to support various up-layer frameworks and Applications with different sensor expose/transfer protocols, such as `CHRE <https://github.com/zephyrproject-rtos/chre>`_, HID sensors Applications, MQTT sensor Applications according different products requirements. Or even support multiple Applications with different up-layer sensor protocols at the same time with it's multiple clients support design.)

传感子系统可以帮助构建统一的 Zephyr 传感架构,以支持跨主机操作系统以及 IoT 传感器解决方案。(Sensing subsystem can help build a unified Zephyr sensing architecture for cross host OSes support and as well as IoT sensor solutions.)

下图说明了传感子系统如何与上层框架集成。(The diagram below illustrates how the Sensing Subsystem integrates with up-layer frameworks.)

.. image:: images/sensing_solution.png
   :align: center
   :alt: 统一的 Zephyr 传感架构 (Unified Zephyr sensing architecture).

可配置性 (Configurability)
**************************

* 可重用和可配置的独立子系统。(Reusable and configurable standalone subsystem.)
* 基于 Zephyr 现有的低级传感器 API(重用 100+ 现有传感器设备驱动程序) (Based on Zephyr existing low-level Sensor API (reuse 100+ existing sensor device drivers))
* 为应用程序提供 Zephyr 高级传感子系统 API。(Provide Zephyr high-level Sensing Subsystem API for Applications.)
* 独立的可选 CHRE 传感器 PAL 实现模块以支持 CHRE。(Separate option CHRE Sensor PAL Implementation module to support CHRE.)
* 与任何主机链接协议解耦,由 Zephyr 应用程序负责处理不同的协议(MQTT、HID 或专有协议,全部可配置) (Decoupled with any host link protocols, it's Zephyr Application's role to handle different protocols (MQTT, HID or Private, all configurable))

主要功能 (Main Features)
************************

* 范围 (Scope)
    * 专注于传感器融合、多客户端、仲裁、数据采样、时间管理和调度的框架。(Focus on framework for sensor fusion, multiple clients, arbitration, data sampling, timing management and scheduling.)

* 传感器抽象 (Sensor Abstraction)
    * ``物理传感器 (Physical sensor)``: 与 Zephyr 传感器设备驱动程序交互,专注于数据收集。(interacts with Zephyr sensor device drivers, focus on data collecting.)
    * ``虚拟传感器 (Virtual sensor)``: 依赖其他传感器,``物理 (physical)`` 或 ``虚拟 (virtual)``,专注于数据融合。(relies on other sensor(s), ``physical`` or ``virtual``, focus on data fusion.)

* 数据驱动模型 (Data Driven Model)
    * ``轮询模式 (Polling mode)``: 周期性采样率 (periodical sampling rate)
    * ``中断模式 (Interrupt mode)``: 数据就绪、阈值中断等 (data ready, threshold interrupt etc.)

* 调度 (Scheduling)
    * 所有传感器对象采样和处理的单线程主循环。(single thread main loop for all sensor objects sampling and process.)

* 批处理的缓冲模式 (Buffer Mode for Batching)

* 通过设备树可配置 (Configurable Via Device Tree)


下图显示了 API 位置和范围:(Below diagram shows the API position and scope:)

.. image:: images/sensing_api_org.png
   :align: center
   :alt: 传感子系统 API 组织 (Sensing subsystem API organization).

``传感子系统 API (Sensing Subsystem API)`` 用于应用程序。(``Sensing Subsystem API`` is for Applications.)
``传感传感器 API (Sensing Sensor API)`` 用于开发 ``传感器 (sensors)``。(``Sensing Sensor API`` is for development ``sensors``.)


主要流程 (Major Flows)
**********************

* 传感器配置流程 (Sensor Configuration Flow)

.. image:: images/sensor_config_flow.png
   :align: center
   :alt: 传感器配置流程(应用程序设置铰链角度传感器报告间隔示例) (Sensor Configuration Flow (App set report interval to hinge angel sensor example)).

* 传感器数据流程 (Sensor Data Flow)

.. image:: images/sensor_data_flow.png
   :align: center
   :alt: 传感器数据流程(应用程序通过数据事件回调接收铰链角度数据示例) (Sensor Data Flow (App receive hinge angel data through data event callback example)).

传感器类型和实例 (Sensor Types And Instance)
*******************************************

``传感子系统 (Sensing Subsystem)`` 支持同一传感器类型的多个实例,应用程序有两种方法来识别和打开唯一的传感器实例:(The ``Sensing Subsystem`` supports multiple instances of the same sensor type, there're two methods for Applications to identify and open an unique sensor instance:)

* 枚举所有传感器实例 (Enumerate all sensor instances)

  :c:func:`sensing_get_sensors` 在 :c:struct:`sensing_sensor_info` 指针数组中返回当前板配置支持的所有传感器实例的信息。(:c:func:`sensing_get_sensors` returns all current board configuration supported sensor instances' information in a :c:struct:`sensing_sensor_info` pointer array .)

  然后应用程序可以使用 :c:func:`sensing_open_sensor` 打开特定的传感器实例,以便将来访问、配置和接收传感器数据等。(Then Applications can use :c:func:`sensing_open_sensor` to open specific sensor instance for future accessing, configuration and receive sensor data etc.)

  此方法适用于支持某些上层框架,如 ``CHRE``、``HID``,它们需要动态枚举底层平台的传感器实例。(This method is suitable for supporting some up-layer frameworks like ``CHRE``, ``HID`` which need to dynamically enumerate the underlying platform's sensor instances.)

* 直接通过设备树节点打开传感器实例 (Open the sensor instance by devicetree node directly)

  应用程序可以使用 :c:func:`sensing_open_sensor_by_dt` 直接使用传感器设备树节点标识符打开传感器实例。(Applications can use :c:func:`sensing_open_sensor_by_dt` to open a sensor instance directly with sensor devicetree node identifier.)

  例如:(For example:)

.. code-block:: c

   sensing_open_sensor_by_dt(DEVICE_DT_GET(DT_NODELABEL(base_accel)), cb_list, handle);
   sensing_open_sensor_by_dt(DEVICE_DT_GET(DT_CHOSEN(zephyr_sensing_base_accel)), cb_list, handle);

此方法对于只想访问特定传感器的简单应用程序很有用且易于使用。(This method is useful and easy use for some simple Application which just want to access specific sensor(s).)


``传感器类型 (Sensor type)`` 遵循 `HID 标准传感器类型定义 <https://usb.org/sites/default/files/hutrr39b_0.pdf>`_。(``Sensor type`` follows the `HID standard sensor types definition <https://usb.org/sites/default/files/hutrr39b_0.pdf>`_.)

参见 :zephyr_file:`include/zephyr/sensing/sensing_sensor_types.h`

传感器实例处理程序 (Sensor Instance Handler)
*******************************************

客户端使用 :c:type:`sensing_sensor_handle_t` 类型处理程序来处理已打开的传感器实例,对该传感器实例的所有后续操作都需要使用此处理程序,例如设置配置、读取传感器采样数据等。(Clients using a :c:type:`sensing_sensor_handle_t` type handler to handle a opened sensor instance, and all subsequent operations on this sensor instance need use this handler, such as set configurations, read sensor sample data, etc.)

对于传感器实例,可以有两种客户端:``应用程序客户端 (Application clients)`` 和 ``传感器客户端 (Sensor clients)``。(For a sensor instance, could have two kinds of clients: ``Application clients`` and ``Sensor clients``.)

``应用程序客户端 (Application clients)`` 可以使用 :c:func:`sensing_open_sensor` 打开传感器实例并获取其处理程序。(``Application clients`` can use :c:func:`sensing_open_sensor` to open a sensor instance and get it's handler.)

对于 ``传感器客户端 (Sensor clients)``,没有用于打开报告器的打开 API,因为客户端-报告器关系是在传感器的注册阶段通过设备树建立的。(For ``Sensor clients``, there is no open API for opening a reporter, because the client-report relationship is built at the sensor's registration stage with devicetree.)

``传感子系统 (Sensing Subsystem)`` 将自动打开并为客户端传感器到其报告器传感器创建 ``处理程序 (handlers)``。``传感器客户端 (Sensor clients)`` 可以通过 :c:func:`sensing_sensor_get_reporters` 获取其报告器的处理程序。(The ``Sensing Subsystem`` will auto open and create ``handlers`` for client sensor to it's reporter sensors. ``Sensor clients`` can get it's reporters' handlers via :c:func:`sensing_sensor_get_reporters`.)

.. image:: images/sensor_top.png
   :align: center
   :alt: 传感器报告拓扑 (Sensor Reporting Topology).

.. note::
   传感子系统内部的传感器,它们之间的报告关系都是由传感子系统根据设备树定义自动生成的,客户端传感器和报告器传感器之间的处理程序会自动创建。应用程序需要调用 :c:func:`sensing_open_sensor` 来显式打开传感器实例。(Sensors inside the Sensing Subsystem, the reporting relationship between them are all auto generated by Sensing Subsystem according devicetree definitions, handlers between client sensor and reporter sensors are auto created. Application(s) need to call :c:func:`sensing_open_sensor` to explicitly open the sensor instance.)

传感器采样值 (Sensor Sample Value)
*********************************

* 数据结构 (Data Structure)

  每个传感器采样值定义为通用的 ``header`` + ``readings[]`` 数据结构,如 :c:struct:`sensing_sensor_value_3d_q31`、:c:struct:`sensing_sensor_value_q31` 和 :c:struct:`sensing_sensor_value_uint32`。(Each sensor sample value defines as a common ``header`` + ``readings[]`` data structure, like :c:struct:`sensing_sensor_value_3d_q31`, :c:struct:`sensing_sensor_value_q31`, and :c:struct:`sensing_sensor_value_uint32`.)

  ``header`` 定义为 :c:func:`sensing_sensor_value_header`。(The ``header`` definition :c:func:`sensing_sensor_value_header`.)


* 时间戳 (Time Stamp)

  传感子系统中的时间戳单位是 ``微秒 (micro seconds)``。(Time stamp unit in sensing subsystem is ``micro seconds``.)

  ``header`` 定义了 **base_timestamp**,**readings[]** 数组中的每个元素定义 **timestamp_delta**。(The ``header`` defines a **base_timestamp**, and each element in the **readings[]** array defines **timestamp_delta**.)

  **timestamp_delta** 相对于前一个 **readings**(或 **base_timestamp**) (The **timestamp_delta** is in relation to the previous **readings** (or the **base_timestamp**))

  例如:(For example:)

  * ``readings[0]`` 的时间戳是 ``header.base_timestamp`` + ``readings[0].timestamp_delta``。(timestamp of ``readings[0]`` is ``header.base_timestamp`` + ``readings[0].timestamp_delta``.)

  * ``readings[1]`` 的时间戳是 ``readings[0] 的时间戳`` + ``readings[1].timestamp_delta``。(timestamp of ``readings[1]`` is ``timestamp of readings[0]`` + ``readings[1].timestamp_delta``.)

  由于时间戳单位是微秒,最大 **timestamp_delta**(``uint32_t``)是 ``4295`` 秒。(Since timestamp unit is micro seconds, the max **timestamp_delta** (``uint32_t``) is ``4295`` seconds.)

  如果传感器具有批处理数据,其中两个连续读数相差超过 ``4295`` 秒,传感子系统运行时将把它们拆分到 readings 结构的多个实例中,并发送多个事件。(If a sensor has batched data where two consecutive readings differ by more than ``4295`` seconds, the sensing subsystem runtime will split them across multiple instances of the readings structure, and send multiple events.)

  此概念参考自 `CHRE 传感器 API <https://github.com/zephyrproject-rtos/chre/blob/zephyr/chre_api/include/chre_api/chre/sensor_types.h>`_。(This concept is referred from `CHRE Sensor API <https://github.com/zephyrproject-rtos/chre/blob/zephyr/chre_api/include/chre_api/chre/sensor_types.h>`_.)

* 数据格式 (Data Format)

  ``传感子系统 (Sensing Subsystem)`` 使用每个传感器类型定义的数据格式结构,并支持 :zephyr_file:`include/zephyr/dsp/types.h` 中定义的 ``Q 格式 (Q Format)``,以支持 ``zdsp`` 库。(``Sensing Subsystem`` uses per sensor type defined data format structure, and support ``Q Format`` defined in :zephyr_file:`include/zephyr/dsp/types.h` for ``zdsp`` lib support.)

  例如 :c:struct:`sensing_sensor_value_3d_q31` 可用于 3D IMU 传感器,如 :c:macro:`SENSING_SENSOR_TYPE_MOTION_ACCELEROMETER_3D`、:c:macro:`SENSING_SENSOR_TYPE_MOTION_UNCALIB_ACCELEROMETER_3D` 和 :c:macro:`SENSING_SENSOR_TYPE_MOTION_GYROMETER_3D`。(For example :c:struct:`sensing_sensor_value_3d_q31` can be used by 3D IMU sensors like :c:macro:`SENSING_SENSOR_TYPE_MOTION_ACCELEROMETER_3D`, :c:macro:`SENSING_SENSOR_TYPE_MOTION_UNCALIB_ACCELEROMETER_3D`, and :c:macro:`SENSING_SENSOR_TYPE_MOTION_GYROMETER_3D`.)

  :c:struct:`sensing_sensor_value_uint32` 可用于 :c:macro:`SENSING_SENSOR_TYPE_LIGHT_AMBIENTLIGHT` 传感器,(:c:struct:`sensing_sensor_value_uint32` can be used by :c:macro:`SENSING_SENSOR_TYPE_LIGHT_AMBIENTLIGHT` sensor,)

  :c:struct:`sensing_sensor_value_q31` 可用于 :c:macro:`SENSING_SENSOR_TYPE_MOTION_HINGE_ANGLE` 传感器 (and :c:struct:`sensing_sensor_value_q31` can be used by :c:macro:`SENSING_SENSOR_TYPE_MOTION_HINGE_ANGLE` sensor)

  参见 :zephyr_file:`include/zephyr/sensing/sensing_datatypes.h`


设备树配置 (Device Tree Configuration)
*************************************

传感子系统使用设备树配置所有传感器实例及其属性、报告关系。(Sensing subsystem using device tree to configuration all sensor instances and their properties, reporting relationships.)

参见示例 :zephyr_file:`samples/subsys/sensing/simple/boards/native_sim.overlay`

API 参考 (API Reference)
************************

.. doxygengroup:: sensing_api
