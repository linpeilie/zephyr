.. _cs_trace_defmt:

ARM Coresight跟踪解格式化器 (ARM Coresight Trace Deformatter)
#############################################################

格式化器是一种将多个跟踪流(由7位ID指定)包装到单个输出流的方法 (Formatter is a method of wrapping multiple trace streams (specified by 7 bit ID) into a single output stream)。格式化器使用16字节帧,最多包装15字节的数据 (Formatter is using 16 byte frames which wraps up to 15 bytes of data)。例如,ETR(嵌入式跟踪路由器)使用它,ETR是一个循环RAM缓冲区,可以保存来自各种跟踪流的数据 (It is used, for example, by ETR (Embedded Trace Router) which is a circular RAM buffer where data from various trace streams can be saved)。通常,跟踪数据由主机离线解码,但解格式化器可以在芯片上使用,以在应用程序运行时解码数据 (Typically tracing data is decoded offline by the host but deformatter can be used on-chip to decode the data during application runtime)。

用法 (Usage)
*****

解格式化器使用用户回调初始化 (Deformatter is initialized with a user callback)。数据使用 :c:func:`cs_trace_defmt_process` 以16字节块进行解码 (Data is decoded using :c:func:`cs_trace_defmt_process` in 16 bytes chunks)。每当流更改或到达块末尾时,都会调用回调 (Callback is called whenever stream changes or end of chunk is reached)。回调包含流ID和数据 (Callback contains stream ID and the data)。

API文档 (API documentation)
*****************

.. doxygengroup:: cs_trace_defmt
