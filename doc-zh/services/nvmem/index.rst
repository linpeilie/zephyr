.. _nvmem:

非易失性内存 (Non-Volatile Memory (NVMEM))
##########################################

NVMEM 子系统提供了一个用于访问非易失性内存设备的通用接口。它抽象了底层硬件并提供了统一的 API 用于读写数据。(The NVMEM subsystem provides a generic interface for accessing non-volatile memory devices. It abstracts the underlying hardware and provides a unified API for reading and writing data.)

关键概念 (Key Concepts)
************************

NVMEM 提供者 (NVMEM Provider)
==============================

NVMEM 提供者是暴露 NVMEM 单元的驱动程序。例如,EEPROM 驱动程序可以是 NVMEM 提供者。NVMEM 提供者负责向底层硬件读取和写入数据。(An NVMEM provider is a driver that exposes NVMEM cells. For example, an EEPROM driver can be an NVMEM provider. The NVMEM provider is responsible for reading and writing data to the underlying hardware.)

NVMEM 单元 (NVMEM Cell)
========================

NVMEM 单元是非易失性内存的一个区域。它在设备树中定义,具有偏移量、大小和只读状态等属性。(An NVMEM cell is a region of non-volatile memory. It is defined in the devicetree and has properties like offset, size, and read-only status.)

NVMEM 消费者 (NVMEM Consumer)
==============================

NVMEM 消费者是使用 NVMEM 单元来存储或检索数据的驱动程序或应用程序。(An NVMEM consumer is a driver or application that uses NVMEM cells to store or retrieve data.)

配置 (Configuration)
*********************

* :kconfig:option:`CONFIG_NVMEM`: 启用 NVMEM 子系统。(Enables the NVMEM subsystem.)
* :kconfig:option:`CONFIG_NVMEM_EEPROM`: 为 EEPROM 设备启用 NVMEM 支持。(Enables NVMEM support for EEPROM devices.)

设备树绑定 (Devicetree Bindings)
*********************************

NVMEM 子系统依赖设备树绑定来定义 NVMEM 单元。以下是如何在设备树中定义 NVMEM 提供者和单元的示例:(The NVMEM subsystem relies on devicetree bindings to define NVMEM cells. The following is an example of how to define an NVMEM provider and cells in the devicetree:)

.. literalinclude:: devicetree_bindings.txt
   :language: dts


然后,消费者可以像这样引用 NVMEM 单元:(A consumer can then reference the NVMEM cells like this:)

.. literalinclude:: my_consumer.txt
   :language: dts


用法示例 (Usage Example)
*************************

以下是如何使用 NVMEM API 从 NVMEM 单元读取数据的示例:(The following is an example of how to use the NVMEM API to read data from an NVMEM cell:)

.. literalinclude:: usage_example.txt
   :language: c


API 参考 (API Reference)
*************************

.. doxygengroup:: nvmem_interface
