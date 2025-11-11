.. _cmsis_rtos_v2:

CMSIS RTOS v2
##########################

Cortex-M 软件接口标准 (CMSIS) RTOS 是针对 ARM Cortex-M 处理器系列的与供应商无关的硬件抽象层,并定义了通用工具接口。虽然它最初仅为 ARM Cortex-M 微控制器定义,但它可以很容易地扩展到其他微控制器,使其成为通用的。有关 CMSIS RTOS v2 的更多信息,请参阅 `CMSIS-RTOS2 文档 <https://arm-software.github.io/CMSIS_6/latest/RTOS2/index.html>`_。(Cortex-M Software Interface Standard (CMSIS) RTOS is a vendor-independent hardware abstraction layer for the ARM Cortex-M processor series and defines generic tool interfaces. Though it was originally defined for ARM Cortex-M microcontrollers alone, it could be easily extended to other microcontrollers making it generic. For more information on CMSIS RTOS v2, please refer to the `CMSIS-RTOS2 Documentation <https://arm-software.github.io/CMSIS_6/latest/RTOS2/index.html>`_.)

Zephyr 实现中不支持的功能 (Features not supported in Zephyr implementation)
*****************************************************************************

内核 (Kernel)
   不支持 ``osKernelGetState``、``osKernelSuspend``、``osKernelResume``、``osKernelInitialize`` 和 ``osKernelStart``。(``osKernelGetState``, ``osKernelSuspend``, ``osKernelResume``, ``osKernelInitialize`` and ``osKernelStart`` are not supported.)

互斥锁 (Mutex)
   默认支持 ``osMutexPrioInherit`` 且不可配置,您无法选择/取消选择此属性。(``osMutexPrioInherit`` is supported by default and is not configurable, you cannot select/unselect this attribute.)

   默认也支持 ``osMutexRecursive``。如果未设置此属性,当同一线程第二次尝试获取它时会抛出错误。(``osMutexRecursive`` is also supported by default. If this attribute is not set, an error is thrown when the same thread tries to acquire it the second time.)

   Zephyr 不支持 ``osMutexRobust``。(``osMutexRobust`` is not supported in Zephyr.)

Zephyr 实现中不支持的返回值 (Return values not supported in the Zephyr implementation)
*****************************************************************************************

``osKernelUnlock``、``osKernelLock``、``osKernelRestoreLock``
   不支持 ``osError``(未指定的错误)。(``osError`` (Unspecified error) is not supported.)

``osSemaphoreDelete``
   不支持 ``osErrorResource``(由参数 semaphore_id 指定的信号量处于无效的信号量状态)。(``osErrorResource`` (the semaphore specified by parameter semaphore_id is in an invalid semaphore state) is not supported.)

``osMutexDelete``
   不支持 ``osErrorResource``(由参数 mutex_id 指定的互斥锁处于无效的互斥锁状态)。(``osErrorResource`` (mutex specified by parameter mutex_id is in an invalid mutex state) is not supported.)

``osTimerDelete``
   不支持 ``osErrorResource``(由参数 timer_id 指定的定时器处于无效的定时器状态)。(``osErrorResource`` (the timer specified by parameter timer_id is in an invalid timer state) is not supported.)

``osMessageQueueReset``
   不支持 ``osErrorResource``(由参数 msgq_id 指定的消息队列处于无效的消息队列状态)。(``osErrorResource`` (the message queue specified by parameter msgq_id is in an invalid message queue state) is not supported.)

``osMessageQueueDelete``
   不支持 ``osErrorResource``(由参数 msgq_id 指定的消息队列处于无效的消息队列状态)。(``osErrorResource`` (the message queue specified by parameter msgq_id is in an invalid message queue state) is not supported.)

``osMemoryPoolFree``
   不支持 ``osErrorResource``(由参数 mp_id 指定的内存池处于无效的内存池状态)。(``osErrorResource`` (the memory pool specified by parameter mp_id is in an invalid memory pool state) is not supported.)

``osMemoryPoolDelete``
   不支持 ``osErrorResource``(由参数 mp_id 指定的内存池处于无效的内存池状态)。(``osErrorResource`` (the memory pool specified by parameter mp_id is in an invalid memory pool state) is not supported.)

``osEventFlagsSet``、``osEventFlagsClear``
   不支持 ``osFlagsErrorUnknown``(未指定的错误)和 ``osFlagsErrorResource``(由参数 ef_id 指定的事件标志对象未准备好使用)。(``osFlagsErrorUnknown`` (Unspecified error) and osFlagsErrorResource (Event flags object specified by parameter ef_id is not ready to be used) are not supported.)

``osEventFlagsDelete``
   不支持 ``osErrorParameter``(参数 ef_id 的值不正确)。(``osErrorParameter`` (the value of the parameter ef_id is incorrect) is not supported.)

``osThreadFlagsSet``
   不支持 ``osFlagsErrorUnknown``(未指定的错误)和 ``osFlagsErrorResource``(由参数 thread_id 指定的线程未处于活动状态以接收标志)。(``osFlagsErrorUnknown`` (Unspecified error) and ``osFlagsErrorResource`` (Thread specified by parameter thread_id is not active to receive flags) are not supported.)

``osThreadFlagsClear``
   不支持 ``osFlagsErrorResource``(运行中的线程未处于活动状态以接收标志)。(``osFlagsErrorResource`` (Running thread is not active to receive flags) is not supported.)

``osDelayUntil``
   不支持 ``osParameter``(时间无法处理)。(``osParameter`` (the time cannot be handled) is not supported.)
