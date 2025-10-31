.. _queues:

队列 (Queues)
#############

Zephyr 中的队列 (Queue) 是一个内核对象，实现了传统的队列，允许线程和 ISR 添加和移除任意大小的数据项。队列类似于 FIFO，并作为 :ref:`k_fifo <fifos_v2>` 和 :ref:`k_lifo <lifos_v2>` 的底层实现。有关用法的更多信息，请参阅 :ref:`k_fifo <fifos_v2>`。


配置选项 (Configuration Options)
********************************

相关配置选项：

* 无

API 参考 (API Reference)
************************

.. doxygengroup:: queue_apis
