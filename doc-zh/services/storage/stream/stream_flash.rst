.. _stream_flash:

流式闪存 (Stream Flash)
########################
流式闪存模块接收连续的数据流片段(例如来自无线电数据包),将它们聚合到用户提供的缓冲区中,然后当缓冲区填满(或流结束)时将其写入原始闪存分区。它支持向客户端提供回读缓冲区,用于验证持久化的流内容。(The Stream Flash module takes contiguous fragments of a stream of data (e.g. from radio packets), aggregates them into a user-provided buffer, then when the buffer fills (or stream ends) writes it to a raw flash partition. It supports providing the read-back buffer to the client to use in validating the persisted stream content.)

流写入操作的一个典型用途是在接收要在 DFU 操作中使用的新固件映像时。(One typical use of a stream write operation is when receiving a new firmware image to be used in a DFU operation.)

有几个原因可能导致人们想要使用缓冲写入而不是在数据可用时直接写入。某些设备具有硬件限制,不允许与其他操作(如无线电 RX 和 TX)并行执行闪存写入。此外,较少的写入操作导致应用程序看到的响应时间更快。(There are several reasons why one might want to use buffered writes instead of writing the data directly as it is made available. Some devices have hardware limitations which does not allow flash writes to be performed in parallel with other operations, such as radio RX and TX. Also, fewer write operations result in faster response times seen from the application.)

持久化流写入进度 (Persistent stream write progress)
****************************************************
某些流写入操作(例如 DFU 操作)可能会运行很长时间。在执行此类长时间运行的操作时,能够将流写入进度保存到持久存储中可能很有用,以便在意外中断后可以在同一点恢复操作。(Some stream write operations, such as DFU operations, may run for a long time. When performing such long running operations it can be useful to be able to save the stream write progress to persistent storage so that the operation can resume at the same point after an unexpected interruption.)

流式闪存模块提供了一个 API,用于使用 :ref:`Settings <settings_api>` 模块将流写入进度加载、保存和清除到持久存储。可以使用 :kconfig:option:`CONFIG_STREAM_FLASH_PROGRESS` 启用该 API。(The Stream Flash module offers an API for loading, saving and clearing stream write progress to persistent storage using the :ref:`Settings <settings_api>` module. The API can be enabled using :kconfig:option:`CONFIG_STREAM_FLASH_PROGRESS`.)

API 参考 (API Reference)
*************************

.. doxygengroup:: stream_flash
