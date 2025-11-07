.. _uart_api:

通用异步收发器 (Universal Asynchronous Receiver-Transmitter, UART)
####################################################################

概述 (Overview)
****************

Zephyr 提供三种不同的方式来访问 UART 外设。根据不同的方法,使用不同的 API 函数,具体如下:

1. :ref:`uart_polling_api`
2. :ref:`uart_interrupt_api`
3. 使用 :ref:`dma_api` 的 :ref:`uart_async_api`

轮询是访问 UART 外设最基本的方法。读取函数 :c:func:`uart_poll_in` 是一个非阻塞函数,返回一个字符,或在没有有效数据时返回 ``-1``。写入函数 :c:func:`uart_poll_out` 是一个阻塞函数,线程会等待直到给定的字符被发送。

通过中断驱动 API,可能较慢的通信可以在后台进行,而线程可以继续执行其他任务。内核的 :ref:`kernel_data_passing_api` 功能可用于线程和 UART 驱动程序之间的通信。

异步 API 允许使用 DMA 在后台读取和写入数据,而完全不中断 MCU。但是,其设置比其他方法更复杂。

.. warning::

   中断驱动 API 和异步 API 不应同时用于同一个硬件外设,因为这两个 API 都需要硬件中断才能正常工作。同时使用两个 API 的回调会导致它们相互干扰。默认情况下启用 :kconfig:option:`CONFIG_UART_EXCLUSIVE_API_CALLBACKS`,以便一次只激活与一个 API 关联的回调。


配置选项 (Configuration Options)
*********************************

最重要的是,Kconfig 选项定义了是否可以使用轮询 API(默认)、中断驱动 API 或异步 API。仅启用您需要的功能以最小化内存占用。

相关配置选项:

* :kconfig:option:`CONFIG_SERIAL`
* :kconfig:option:`CONFIG_UART_INTERRUPT_DRIVEN`
* :kconfig:option:`CONFIG_UART_ASYNC_API`
* :kconfig:option:`CONFIG_UART_WIDE_DATA`
* :kconfig:option:`CONFIG_UART_USE_RUNTIME_CONFIGURE`
* :kconfig:option:`CONFIG_UART_LINE_CTRL`
* :kconfig:option:`CONFIG_UART_DRV_CMD`


API 参考 (API Reference)
*************************

.. doxygengroup:: uart_interface


.. _uart_polling_api:

轮询 API (Polling API)
=======================

.. doxygengroup:: uart_polling


.. _uart_interrupt_api:

中断驱动 API (Interrupt-driven API)
====================================

.. doxygengroup:: uart_interrupt


.. _uart_async_api:

异步 API (Asynchronous API)
============================

.. doxygengroup:: uart_async
