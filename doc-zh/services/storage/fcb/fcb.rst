.. _fcb_api:

闪存循环缓冲区 (Flash Circular Buffer, FCB)
############################################

闪存循环缓冲区提供了一个抽象,通过它您可以像 FIFO 一样处理闪存。您将条目追加到末尾,并从开头读取数据。(Flash circular buffer provides an abstraction through which you can treat flash like a FIFO. You append entries to the end, and read data from the beginning.)

描述 (Description)
*******************

闪存中的条目包含条目的长度、条目中的数据以及条目内容的校验和。(Entries in the flash contain the length of the entry, the data within the entry, and checksum over the entry contents.)

闪存中条目的存储以 FIFO 方式完成。当您请求下一个条目的空间时,空间位于已使用区域的末尾。当您开始读取时,提供的第一个条目是闪存中最旧的条目。(Storage of entries in flash is done in a FIFO fashion. When you request space for the next entry, space is located at the end of the used area. When you start reading, the first entry served is the oldest entry in flash.)

可以将条目追加到区域的末尾,直到存储空间耗尽。您可以控制接下来发生的事情;要么擦除最旧的数据块,从而释放一些空间,要么停止写入新数据,直到收集了现有数据。FCB 将底层存储视为闪存扇区数组;当它擦除旧数据时,它一次擦除一个扇区。(Entries can be appended to the end of the area until storage space is exhausted. You have control over what happens next; either erase oldest block of data, thereby freeing up some space, or stop writing new data until existing data has been collected. FCB treats underlying storage as an array of flash sectors; when it erases old data, it does this a sector at a time.)

闪存中的条目带有校验和。这就是 FCB 检测将条目写入闪存是否成功完成的方式。它将跳过没有有效校验和的条目。(Entries in the flash are checksummed. That is how FCB detects whether writing entry to flash completed ok. It will skip over entries which don't have a valid checksum.)

使用方法 (Usage)
*****************

向循环缓冲区添加条目:(To add an entry to circular buffer:)

- 调用 :c:func:`fcb_append` 获取可以写入数据的位置。如果由于空间不足而失败,您可以调用 :c:func:`fcb_rotate` 擦除最旧的扇区,这将腾出空间。然后再次调用 :c:func:`fcb_append`。(Call :c:func:`fcb_append` to get the location where data can be written. If this fails due to lack of space, you can call :c:func:`fcb_rotate` to erase the oldest sector which will make the space. And then call :c:func:`fcb_append` again.)
- 使用 :c:func:`flash_area_write` 写入条目内容。(Use :c:func:`flash_area_write` to write entry contents.)
- 完成后调用 :c:func:`fcb_append_finish`。这通过计算校验和完成条目的写入。(Call :c:func:`fcb_append_finish` when done. This completes the writing of the entry by calculating the checksum.)

读取循环缓冲区的内容:(To read contents of the circular buffer:)

- 使用指向回调函数的指针调用 :c:func:`fcb_walk`。(Call :c:func:`fcb_walk` with a pointer to your callback function.)
- 在回调函数中使用 :c:func:`flash_area_read` 从条目复制数据。您可以通过监视返回条目的区域指针来判断何时已读取扇区内的所有数据。然后,如果您完成了该数据,可以调用 :c:func:`fcb_rotate`。(Within callback function copy in data from the entry using :c:func:`flash_area_read`. You can tell when all data from within a sector has been read by monitoring the returned entry's area pointer. Then you can call :c:func:`fcb_rotate`, if you're done with that data.)

或者:(Alternatively:)

- 在条目偏移量中使用 0 调用 :c:func:`fcb_getnext` 以获取指向最旧条目的指针。(Call :c:func:`fcb_getnext` with 0 in entry offset to get the pointer to the oldest entry.)
- 使用 :c:func:`flash_area_read` 读取条目内容。(Use :c:func:`flash_area_read` to read entry contents.)
- 使用指向当前条目的指针调用 :c:func:`fcb_getnext` 以获取下一个条目。依此类推。(Call :c:func:`fcb_getnext` with pointer to current entry to get the next one. And so on.)

API 参考 (API Reference)
*************************

FCB 子系统 API 由 ``fcb.h`` 提供:(The FCB subsystem APIs are provided by ``fcb.h``:)

数据结构 (Data structures)
============================
.. doxygengroup:: fcb_data_structures

API 函数 (API functions)
==========================
.. doxygengroup:: fcb_api
