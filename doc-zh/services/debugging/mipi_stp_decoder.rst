.. _mipi_stp_decoder:

MIPI STP解码器 (MIPI STP Decoder)
##################################

MIPI系统跟踪协议(MIPI STP)被开发为一种通用基础协议,可以由多个特定于应用程序的跟踪协议共享 (The MIPI System Trace Protocol (MIPI STP) was developed as a generic base protocol that can be shared by multiple application-specific trace protocols)。它作为一个包装协议,合并来自不同跟踪源的通常包含不同跟踪协议的不同流 (It serves as a wrapper protocol that merges disparate streams that typically contain different trace protocols from different trace sources)。流由操作码(最短为4位长)后跟可选数据和可选时间戳组成 (Stream consists of opcode (shortest is 4 bit long) followed by optional data and optional timestamp)。有用于数据(8、16、32、64位数据标记/未标记,带或不带时间戳)、流识别(主机和通道)、同步(ASYNC操作码)等的操作码 (There are opcodes for data (8, 16, 32, 64 bit data marked/not marked, with or without timestamp), stream recognition (master and channel), synchronization (ASYNC opcode) and others)。

使用该协议的一个例子是ARM Coresight STM(系统跟踪宏单元),其中写入激励端口寄存器的数据直接映射到STP流 (One example where protocol is used is ARM Coresight STM (System Trace Macrocell) where data written to Stimulus Port registers maps directly to STP stream)。

此模块可用于执行数据流的芯片上解码 (This module can be used to perform on-chip decoding of the data stream)。使用STP v2 (STP v2 is used)。

用法 (Usage)
*****

解码器使用回调初始化 (Decoder is initialized with a callback)。在每个解码的操作码上调用回调 (A callback is called on each decoded opcode)。
解码器具有内部状态,因为操作码之间存在依赖关系(例如时间戳可以是相对的) (Decoder has internal state since there are dependency between opcodes (e.g. timestamp can be relative))。解码器可以处于同步或不同步状态 (Decoder can be in synchronization or not)。初始状态是可配置的 (Initial state is configurable)。
如果解码器与流不同步,则它解码每个半字节以搜索ASYNC操作码 (If decoder is not synchronized to the stream then it decodes each nibble in search for ASYNC opcode)。
可以通过调用 :c:func:`mipi_stp_decoder_sync_loss` 向解码器指示同步丢失 (Loss of synchronization can be indicated to the decoder by calling :c:func:`mipi_stp_decoder_sync_loss`)。使用 :c:func:`mipi_stp_decoder_decode` 解码数据 (`:c:func:`mipi_stp_decoder_decode` is used to decode the data)。

限制 (Limitations)
***********

存在以下限制 (There are following limitations):

* 解码器仅支持小端架构 (Decoder supports only little endian architectures)。
* 解码半字节时,如果核心支持未对齐内存访问会更有效 (When decoding nibbles, it is more efficient when core supports unaligned memory access)。
  实现支持具有未对齐内存访问的优化版本和通用版本 (Implementation supports optimized version with unaligned memory access and generic one)。
  优化版本用于ARM Cortex-M(M0除外) (Optimized version is used for ARM Cortex-M (expect for M0))。
* 实现了最常见操作码的有限集合 (Limited set of the most common opcodes is implemented)。

API文档 (API documentation)
*****************

.. doxygengroup:: mipi_stp_decoder_apis
