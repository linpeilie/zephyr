.. _async_notification:

异步通知 (Asynchronous Notifications)
##########################

Zephyr API 通常包括 :ref:`api_term_async` 函数,其中操作被启动,应用程序需要在操作完成时得到通知,以及操作是否成功。使用 :c:func:`k_poll` 通常是一个好方法,但某些应用程序架构可能更适合回调通知,并且像启用时钟和电源轨道这样的操作可能需要在内核函数可用之前调用,因此可能需要忙等待完成 (Zephyr APIs often include :ref:`api_term_async` functions where an
operation is initiated and the application needs to be informed when it
completes, and whether it succeeded.  Using :c:func:`k_poll` is
often a good method, but some application architectures may be more
suited to a callback notification, and operations like enabling clocks
and power rails may need to be invoked before kernel functions are
available so a busy-wait for completion may be needed)。

此 API 旨在嵌入到特定子系统中,例如 :ref:`resource_mgmt_onoff` 和其他支持异步事务的 API。子系统包装器负责从包含通知元素的请求中提取特定于操作的数据,并使用 API 所需的参数调用回调 (This API is intended to be embedded within specific subsystems such as
:ref:`resource_mgmt_onoff` and other APIs that support async
transactions.  The subsystem wrappers are responsible for extracting
operation-specific data from requests that include a notification
element, and for invoking callbacks with the parameters required by the
API)。

一个限制是此 API 不适合 :ref:`syscalls`,因为 (A limitation is that this API is not suitable for :ref:`syscalls`
because):

* :c:struct:`sys_notify` 不是内核对象 (:c:struct:`sys_notify` is not a kernel object);
* 从用户空间复制通知内容会破坏实现函数中 :c:macro:`CONTAINER_OF` 的使用 (copying the notification content from userspace will break use of
  :c:macro:`CONTAINER_OF` in the implementing function);
* 自旋等待和回调通知方法都不能从用户空间调用者接受 (neither the spin-wait nor callback notification methods can be
  accepted from userspace callers)。

当需要从用户模式线程调用的异步操作的通知时,子系统或驱动程序应提供使用 :c:struct:`k_poll_signal` 进行通知的系统调用 API (Where a notification is required for an asynchronous operation invoked
from a user mode thread the subsystem or driver should provide a syscall
API that uses :c:struct:`k_poll_signal` for notification)。

API 参考 (API Reference)
*************

.. doxygengroup:: sys_notify_apis
