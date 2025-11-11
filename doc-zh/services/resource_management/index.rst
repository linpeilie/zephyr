.. _resource_mgmt:

资源管理 (Resource Management)
################################

在多种情况下,需要在运行时协调多个客户端之间的资源使用。这些情况包括电源轨、时钟、其他外设以及二进制设备电源管理。在多线程系统中正确管理设备的多个消费者的复杂性,特别是当转换可能是异步的时候,表明需要一个共享的实现。(There are various situations where it's necessary to coordinate resource use at runtime among multiple clients. These include power rails, clocks, other peripherals, and binary device power management. The complexity of properly managing multiple consumers of a device in a multithreaded system, especially when transitions may be asynchronous, suggests that a shared implementation is desirable.)

Zephyr 为多种协调策略提供了管理器。这些管理器嵌入到使用它们执行特定功能的服务中。(Zephyr provides managers for several coordination policies. These managers are embedded into services that use them for specific functions.)

.. contents::
    :local:
    :depth: 2

.. _resource_mgmt_onoff:

开关管理器 (On-Off Manager)
****************************

开关管理器支持具有二进制状态的服务的任意数量的客户端。示例应用包括电源轨、时钟和二进制设备电源管理。(An on-off manager supports an arbitrary number of clients of a service which has a binary state. Example applications are power rails, clocks, and binary device power management.)

该管理器具有以下属性: (The manager has the following properties:)

* 稳定状态为关闭、开启和错误。服务始终从关闭状态开始。服务也可能处于向给定状态的转换中。(The stable states are off, on, and error. The service always begins in the off state. The service may also be in a transition to a given state.)
* 核心操作是请求(添加依赖)和释放(移除依赖)。支持操作包括重置(清除错误状态)和取消(从进行中的转换中回收客户端数据)。服务根据调用启动这些操作的函数来管理状态。(The core operations are request (add a dependency) and release (remove a dependency). Supporting operations are reset (to clear an error state) and cancel (to reclaim client data from an in-progress transition). The service manages the state based on calls to functions that initiate these operations.)
* 当收到第一个客户端请求时,服务从关闭转换到开启。(The service transitions from off to on when first client request is received.)
* 当收到最后一个客户端释放时,服务从开启转换到关闭。(The service transitions from on to off when last client release is received.)
* 每个服务配置都提供函数来实现从关闭到开启、从开启到关闭以及可选地从错误状态到关闭的转换。转换必须可从线程和中断上下文调用。(Each service configuration provides functions that implement the transition from off to on, from on to off, and optionally from an error state to off. Transitions must be invokable from both thread and interrupt context.)
* 请求和重置操作使用 :ref:`async_notification` 是异步的。两种操作都可以取消,但取消不会影响进行中的转换。(The request and reset operations are asynchronous using :ref:`async_notification`. Both operations may be cancelled, but cancellation has no effect on the in-progress transition.)
* 在转换到关闭进行中时,开启请求可能会排队:当服务成功关闭后,它将立即再次开启(在上下文允许的情况下),并在启动完成时通知等待的客户端。(Requests to turn on may be queued while a transition to off is in progress: when the service has turned off successfully it will be immediately turned on again (where context allows) and waiting clients notified when the start completes.)

请求被引用计数,但不被跟踪。这意味着客户端负责记录他们的请求是否被接受,并且仅在先前成功完成请求的情况下才启动释放。API 的不当使用可能导致活跃的客户端被关闭,并且管理器不维护已授予请求的特定客户端的记录。(Requests are reference counted, but not tracked. That means clients are responsible for recording whether their requests were accepted, and for initiating a release only if they have previously successfully completed a request. Improper use of the API can cause an active client to be shut out, and the manager does not maintain a record of specific clients that have been granted a request.)

执行转换中的失败会被记录,并阻止进一步的请求或释放,直到管理器被重置。当发现错误时,待处理的请求会被通知(并取消)。(Failures in executing a transition are recorded and inhibit further requests or releases until the manager is reset. Pending requests are notified (and cancelled) when errors are discovered.)

转换操作完成通知通过 :ref:`async_notification` 提供。(Transition operation completion notifications are provided through :ref:`async_notification`.)

客户端和其他对跟踪所有服务状态变化感兴趣的组件(包括当服务开始关闭或进入错误状态时),可以通过使用 onoff_monitor_register() 注册监视器来获知状态转换。在发出与新状态关联的完成通知之前,会提供变化通知。(Clients and other components interested in tracking all service state changes, including when a service begins turning off or enters an error state, can be informed of state transitions by registering a monitor with onoff_monitor_register(). Notification of changes are provided before issuing completion notifications associated with the new state.)

.. note::

   通用 API 可能由多个驱动程序实现,其中常见情况是异步的。开关客户端结构可能是通用 API 的合适解决方案。在驱动程序可以保证同步的上下文无关转换的情况下,驱动程序可以使用 :c:struct:`onoff_sync_service` 及其支持 API,而不是 :c:struct:`onoff_manager`,功能仅略有减少(主要是不支持监视器 API)。(A generic API may be implemented by multiple drivers where the common case is asynchronous. The on-off client structure may be an appropriate solution for the generic API. Where drivers that can guarantee synchronous context-independent transitions a driver may use :c:struct:`onoff_sync_service` and its supporting API rather than :c:struct:`onoff_manager`, with only a small reduction in functionality (primarily no support for the monitor API).)

.. doxygengroup:: resource_mgmt_onoff_apis
