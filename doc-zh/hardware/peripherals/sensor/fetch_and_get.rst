.. _sensor-fetch-and-get:

获取和读取 (Fetch and Get)
###########################

用于读取传感器数据和处理触发器的稳定且长期存在的 API 是:

* :c:func:`sensor_sample_fetch`
* :c:func:`sensor_sample_fetch_chan`
* :c:func:`sensor_channel_get`
* :c:func:`sensor_trigger_set`

这些函数协同工作。获取 API 会阻塞调用上下文(必须是线程)，
直到请求的 :c:enum:`sensor_channel`(或所有通道)被获取并存储到驱动程序实例的私有数据中。

然后可以通过为每个通道类型调用 :c:func:`sensor_channel_get`
来获取最近获取的通道数据作为 :c:struct:`sensor_value`。

.. warning::
   应该注意的是，在没有锁定机制的情况下从多个上下文调用 fetch 和 get 是未定义的，
   大多数传感器驱动程序不会在这些调用期间或之间尝试内部提供对设备的独占访问。

轮询 (Polling)
***************

使用 fetch 和 get，传感器可以从软件线程以轮询方式读取。


.. literalinclude:: ../../../../samples/sensor/magn_polling/src/main.c
   :language: c

触发器 (Triggers)
******************

稳定 API 中的触发器需要使用设备特定的 Kconfig 启用触发器。
设备特定的 Kconfig 通常允许选择触发器运行的上下文。
然后，应用程序需要使用 :c:func:`sensor_trigger_set` 为要监听的特定触发器(事件)
注册一个函数签名与 :c:type:`sensor_trigger_handler_t` 匹配的回调。

.. note::
   触发器不能从用户模式线程设置，并且回调不在用户模式上下文中运行。

通常为每个驱动程序提供两个选项来运行触发器处理程序。
触发器处理程序要么使用系统工作队列线程(:ref:`workqueues_v2`)运行，
要么使用专用线程运行。一个很好的示例可以在 BMI160 驱动程序中找到，
它具有用于选择触发器模式的 Kconfig 选项。
请参阅 :kconfig:option:`CONFIG_BMI160_TRIGGER_NONE`、
:kconfig:option:`CONFIG_BMI160_TRIGGER_GLOBAL_THREAD`(工作队列)、
:kconfig:option:`CONFIG_BMI160_TRIGGER_OWN_THREAD`(专用线程)。

使用驱动程序专用线程与系统工作队列的一些显著特性。

* 驱动程序专用线程具有专用堆栈(RAM)，仅用于该单个触发器处理程序函数。
* 驱动程序专用线程*确实*拥有自己的优先级，通常允许您在其他线程之间对触发器处理进行优先级排序。
* 如果驱动程序需要时间来处理触发器，驱动程序专用线程不会出现队首阻塞。

.. note::
   在所有情况下，从实际中断到运行回调函数很可能会有可变延迟。
   在工作队列(GLOBAL_THREAD)情况下，工作队列本身可能是可变延迟的来源！

.. literalinclude:: tap_count.c
   :language: c
