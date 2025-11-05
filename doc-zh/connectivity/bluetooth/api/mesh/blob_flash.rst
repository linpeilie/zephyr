.. _bluetooth_mesh_blob_flash:

BLOB 闪存
##########

BLOB 闪存读取器和写入器实现了从 :ref:`闪存映射 <flash_map_api>` 中定义的闪存分区读取和写入 BLOB。


BLOB 闪存读取器
*****************

BLOB 闪存读取器与 BLOB 传输客户端交互以直接从闪存读取 BLOB 数据。
它必须通过调用 :c:func:`bt_mesh_blob_flash_rd_init` 初始化，然后才能传递给 BLOB 传输客户端。每个 BLOB 闪存读取器一次只支持一次传输。


BLOB 闪存写入器
*****************

BLOB 闪存写入器与 BLOB 传输服务器交互以直接将 BLOB 数据写入闪存。
它必须通过调用 :c:func:`bt_mesh_blob_flash_rd_init` 初始化，然后才能传递给 BLOB 传输服务器。每个 BLOB 闪存写入器一次只支持一次传输，并且需要是闪存页大小倍数的块大小。如果以低于闪存页大小的块大小开始传输，传输将被拒绝。

BLOB 闪存写入器将数据块数据复制到缓冲区中以适应与闪存写入块大小不对齐的数据块。如果数据块的开始或长度不对齐，缓冲区数据会用 ``0xff`` 填充。

API 参考
*************

.. doxygengroup:: bt_mesh_blob_io_flash
