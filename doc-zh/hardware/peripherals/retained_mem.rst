.. _retained_mem_api:

保持内存 (Retained Memory)
###########################

概述 (Overview)
****************

保持内存驱动程序 API 提供了一种从内存区域读取/写入的方法,在设备供电期间内存内容会保留(在低功耗模式下数据可能会丢失)。

配置选项 (Configuration Options)
*********************************

相关配置选项:

* :kconfig:option:`CONFIG_RETAINED_MEM`
* :kconfig:option:`CONFIG_RETAINED_MEM_INIT_PRIORITY`
* :kconfig:option:`CONFIG_RETAINED_MEM_MUTEX_FORCE_DISABLE`

互斥锁保护 (Mutex Protection)
******************************

当应用程序使用多线程支持编译时,保持内存驱动程序的互斥锁保护默认启用。这意味着不同的线程可以安全地调用保持内存函数,而不会与其他并发线程函数使用发生冲突,但这意味着保持内存函数不能从 ISR 使用。可以通过启用 :kconfig:option:`CONFIG_RETAINED_MEM_MUTEX_FORCE_DISABLE` 在全局范围内禁用所有保持内存驱动程序的互斥锁保护 - 然后用户负责确保函数调用不会相互冲突。

API 参考 (API Reference)
*************************

.. doxygengroup:: retained_mem_interface
