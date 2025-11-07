.. _mpsc_lockfree:

多生产者单消费者无锁队列 (Multi Producer Single Consumer Lock Free Queue)
==========================================================================

:dfn:`多生产者单消费者无锁队列 (MPSC)` 是一种基于原子指针交换的无锁侵入式队列,由 Dmitry Vyukov 在 `1024cores <https://www.1024cores.net/home/lock-free-algorithms/queues/intrusive-mpsc-node-based-queue>`_ 中描述。


API 参考 (API Reference)
*************************

.. doxygengroup:: mpsc_lockfree
