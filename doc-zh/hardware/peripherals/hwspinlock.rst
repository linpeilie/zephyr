.. _hwspinlock_api:

硬件自旋锁 (Hardware Spinlocks, HWSPINLOCK)
############################################

概述 (Overview)
****************

HWSPINLOCK 设备是用于保护系统中跨集群共享资源的外设。每个 HWSPINLOCK 实例提供一个或多个自旋锁。该 API 类似于常规的 Zephyr 自旋锁。

.. doxygengroup:: spinlock_apis

由于我们还希望保护自旋锁资源不被同一集群中的多个核心使用,因此每个 HWSPINLOCK 设备都包含一个常规的 Zephyr 自旋锁,并使用它来锁定对 HWSPINLOCK 硬件的访问。

API 参考 (API Reference)
*************************

.. doxygengroup:: hwspinlock_interface
