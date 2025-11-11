.. _ipc_service:

IPC 服务 (IPC service)
######################

.. contents::
    :local:
    :depth: 2

IPC 服务 API 提供了一个在两个域或 CPU 之间交换数据的接口。(The IPC service API provides an interface to exchange data between two domains or CPUs.)

概述 (Overview)
================

一个 IPC 服务通信通道由一个实例和与该实例关联的一个或多个端点组成。(An IPC service communication channel consists of one instance and one or several endpoints associated with the instance.)

实例是两个域或 CPU 之间物理通信通道的外部表示。实例的实际实现和内部表示因每个后端而异。(An instance is the external representation of a physical communication channel between two domains or CPUs. The actual implementation and internal representation of the instance is peculiar to each backend.)

单独的实例不用于在域/CPU 之间发送数据。要发送和接收数据,用户必须在实例中创建(注册)一个端点。这允许连接两个感兴趣的域。(An individual instance is not used to send data between domains/CPUs. To send and receive the data, the user must create (register) an endpoint in the instance. This allows for the connection of the two domains of interest.)

对于单个实例,可以有零个或多个端点,可能具有不同的优先级,并使用每个端点交换数据。端点优先级和多实例能力高度依赖于所使用的后端。(It is possible to have zero or multiple endpoints for one single instance, possibly with different priorities, and to use each to exchange data. Endpoint prioritization and multi-instance ability highly depend on the backend used.)

端点是用户必须使用的实体,用于在两个域之间发送和接收数据(通过实例连接)。端点始终与实例相关联。(The endpoint is an entity the user must use to send and receive data between two domains (connected by the instance). An endpoint is always associated to an instance.)

实例的创建留给后端,通常在初始化时进行。端点的注册留给用户,通常在运行时进行。(The creation of the instances is left to the backend, usually at init time. The registration of the endpoints is left to the user, usually at run time.)

API 并不强制后端创建实例的方式,但强烈建议使用设备树来检索实例的配置参数。目前,每个后端定义自己的 DT 兼容配置,用于在启动时配置接口。(The API does not mandate a way for the backend to create instances but it is strongly recommended to use the devicetree to retrieve the configuration parameters for an instance. Currently, each backend defines its own DT-compatible configuration that is used to configure the interface at boot time.)

支持以下使用场景:(The following usage scenarios are supported:)

* 简单数据交换。(Simple data exchange.)
* 使用零拷贝 API 进行数据交换。(Data exchange using the no-copy API.)

简单数据交换 (Simple data exchange)
====================================

要在域或 CPU 之间发送数据,必须在实例上注册一个端点。(To send data between domains or CPUs, an endpoint must be registered onto an instance.)

请参见以下示例:(See the following example:)

.. note::

   在注册端点之前,必须使用 :c:func:`ipc_service_open_instance` 函数打开实例。(Before registering an endpoint, the instance must be opened using the :c:func:`ipc_service_open_instance` function.)



.. code-block:: c

   #include <zephyr/ipc/ipc_service.h>

   static void bound_cb(void *priv)
   {
      /* Endpoint bounded */
   }

   static void recv_cb(const void *data, size_t len, void *priv)
   {
      /* Data received */
   }

   static struct ipc_ept_cfg ept0_cfg = {
      .name = "ept0",
      .cb = {
         .bound    = bound_cb,
         .received = recv_cb,
      },
   };

   int main(void)
   {
      const struct device *inst0;
      struct ipc_ept ept0;
      int ret;

      inst0 = DEVICE_DT_GET(DT_NODELABEL(ipc0));
      ret = ipc_service_open_instance(inst0);
      ret = ipc_service_register_endpoint(inst0, &ept0, &ept0_cfg);

      /* Wait for endpoint bound (bound_cb called) */

      unsigned char message[] = "hello world";
      ret = ipc_service_send(&ept0, &message, sizeof(message));
   }

使用零拷贝 API 进行数据交换 (Data exchange using the no-copy API)
===================================================================

如果后端支持零拷贝 API,您可以使用它直接在共享内存区域中写入和读取。(If the backend supports the no-copy API you can use it to directly write and read to and from shared memory regions.)

请参见以下示例:(See the following example:)

.. code-block:: c

   #include <zephyr/ipc/ipc_service.h>
   #include <stdint.h>
   #include <string.h>

   static struct ipc_ept ept0;

   static void bound_cb(void *priv)
   {
      /* Endpoint bounded */
   }

   static void recv_cb_nocopy(const void *data, size_t len, void *priv)
   {
      int ret;

      ret = ipc_service_hold_rx_buffer(&ept0, (void *)data);
      /* Process directly or put the buffer somewhere else and release. */
      ret = ipc_service_release_rx_buffer(&ept0, (void *)data);
   }

   static struct ipc_ept_cfg ept0_cfg = {
      .name = "ept0",
      .cb = {
         .bound    = bound_cb,
         .received = recv_cb,
      },
   };

   int main(void)
   {
      const struct device *inst0;
      int ret;

      inst0 = DEVICE_DT_GET(DT_NODELABEL(ipc0));
      ret = ipc_service_open_instance(inst0);
      ret = ipc_service_register_endpoint(inst0, &ept0, &ept0_cfg);

      /* Wait for endpoint bound (bound_cb called) */
      void *data;
      unsigned char message[] = "hello world";
      uint32_t len = sizeof(message);

      ret = ipc_service_get_tx_buffer(&ept0, &data, &len, K_FOREVER);

      memcpy(data, message, len);

      ret = ipc_service_send_nocopy(&ept0, data, sizeof(message));
   }

后端 (Backends)
================

实现后端所需的要求为 IPC 服务提供了灵活性。这允许添加仅具有特定用例功能子集的专用后端。(The requirements needed for implementing backends give flexibility to the IPC service. These allow for the addition of dedicated backends having only a subsets of features for specific use cases.)

后端必须至少支持以下内容:(The backend must support at least the following:)

* 初始化时创建实例。(The init-time creation of instances.)
* 运行时在实例中注册端点。(The run-time registration of an endpoint in an instance.)

此外,后端还可以支持以下内容:(Additionally, the backend can also support the following:)

* 运行时从实例中注销端点。(The run-time deregistration of an endpoint from the instance.)
* 运行时关闭实例。(The run-time closing of an instance.)
* 零拷贝 API。(The no-copy API.)

每个后端都可以有自己的限制和特性,使后端独特并专用于特定用例。IPC 服务 API 可以同时与多个后端一起使用,结合每个后端的优缺点。(Each backend can have its own limitations and features that make the backend unique and dedicated to a specific use case. The IPC service API can be used with multiple backends simultaneously, combining the pros and cons of each backend.)

.. toctree::
   :maxdepth: 1

   backends/ipc_service_icmsg.rst
   backends/ipc_service_icbmsg.rst

API 参考 (API Reference)
=========================

IPC 服务 API (IPC service API)
*******************************

.. doxygengroup:: ipc_service_api

IPC 服务后端 API (IPC service backend API)
*******************************************

.. doxygengroup:: ipc_service_backend

