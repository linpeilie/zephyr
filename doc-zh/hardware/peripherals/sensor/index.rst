.. _sensor:

传感器 (Sensors)
################

传感器驱动程序 API 提供了统一读取、配置和设置事件处理的功能，
用于以有意义的单位进行真实世界测量的设备。

传感器的范围从必须以固定比例轮询的非常简单的温度读取设备，
到从众多传感器读取数据并自己生成新的推断传感器数据(如步数、存在检测、方向等)的复杂设备。

支持如此广泛的设备是一项艰巨的任务，传感器 API 试图为它们提供统一的接口。


.. _sensor-using:

使用传感器 (Using Sensors)
***************************

从应用程序使用传感器时，有一些有助于理解的 API 和术语。
Zephyr 中的传感器由 :ref:`sensor-channel`、:ref:`sensor-attribute` 和
:ref:`sensor-trigger` 组成。属性和触发器可能是设备或通道特定的。

.. note::
   今天使用传感器 API 从传感器获取样本可以通过两种方式之一完成。
   一种是稳定且长期存在的 API :ref:`sensor-fetch-and-get`，
   另一种是更新但快速稳定的 API :ref:`sensor-read-and-decode`。
   预计在不久的将来，:ref:`sensor-fetch-and-get` 将被弃用，
   取而代之的是 :ref:`sensor-read-and-decode`。
   :ref:`sensor-fetch-and-get` 或 :ref:`sensor-read-and-decode`
   的触发器处理方式完全不同，每个部分都会说明差异。

.. toctree::
   :maxdepth: 1

   attributes.rst
   channels.rst
   triggers.rst
   power_management.rst
   device_tree.rst
   fetch_and_get.rst
   read_and_decode.rst


.. _sensor-implementing:

实现传感器驱动程序 (Implementing Sensor Drivers)
**************************************************

.. note::
   实现传感器 API 的驱动程序端需要了解如何使用传感器 API。
   请先阅读 :ref:`sensor-using`！

实现属性 (Implementing Attributes)
====================================

* 应该(SHOULD)以阻塞方式实现属性设置。
* 如果设备支持，应该(SHOULD)提供获取和设置通道比例的能力。
* 如果设备支持，应该(SHOULD)提供获取和设置通道采样率的能力。

实现获取和读取 (Implementing Fetch and Get)
=============================================

* 应该(SHOULD)将 :c:type:`sensor_sample_fetch_t` 实现为阻塞调用，
  将指定的通道(或所有传感器通道)存储为驱动程序实例数据。
* 应该(SHOULD)实现 :c:type:`sensor_channel_get_t` 时不产生副作用，
  操作驱动程序状态返回存储的传感器读数。
* 应该(SHOULD)实现 :c:type:`sensor_trigger_set_t` 时存储
  :c:struct:`sensor_trigger` 的地址而不是复制内容。
  这样可以使用 :c:macro:`CONTAINER_OF` 来获取触发器回调上下文。

实现读取和解码 (Implementing Read and Decode)
===============================================

* 必须(MUST)将 :c:type:`sensor_submit_t` 实现为非阻塞调用。
* 如果可能，应该(SHOULD)使用 :ref:`rtio` 实现 :c:type:`sensor_submit_t`
  来进行非阻塞总线传输。
* 如果总线不支持 :ref:`rtio`，可以(MAY)使用工作队列实现 :c:type:`sensor_submit_t`。
* 应该(SHOULD)实现 :c:type:`sensor_submit_t` 时检查 :c:struct:`rtio_sqe`
  是否为 :c:enum:`RTIO_SQE_RX` 类型(读取请求)。
* 应该(SHOULD)实现 :c:type:`sensor_submit_t` 时检查是否支持所有请求的通道，
  如果不支持则返回错误。
* 应该(SHOULD)实现 :c:type:`sensor_submit_t` 时检查提供的缓冲区是否足够大以容纳请求的通道。
* 应该(SHOULD)以直接读取到提供的缓冲区的方式实现 :c:type:`sensor_submit_t`，
  避免任何类型的复制，但有少数例外。
* 必须(MUST)使用纯无状态函数实现 :c:struct:`sensor_decoder_api`。
  将原始传感器读数转换为定点 SI 单位值所需的所有状态必须在提供的缓冲区中。
* 必须(MUST)实现 :c:type:`sensor_get_decoder_t` 返回该设备类型的
  :c:struct:`sensor_decoder_api`。

.. _sensor-api-reference:

API 参考 (API Reference)
*************************

.. doxygengroup:: sensor_interface
.. doxygengroup:: sensor_emulator_backend
