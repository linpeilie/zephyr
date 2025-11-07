.. _bbram_api:

电池备份 RAM (Battery Backed RAM, BBRAM)
########################################

BBRAM API 允许与此内存区域的独特属性进行交互。通过此 API 可以轻松访问以下常见类型的 BBRAM 属性:

- IBBR (invalid, 无效) 状态 - 检查 BBRAM 是否未损坏。
- VSBY (voltage standby, 电压待机) 状态 - 检查 BBRAM 是否正在使用待机电压。
- VCC (active power, 有源电源) 状态 - 检查 BBRAM 是否处于正常供电状态。
- Size (大小) - 获取 BBRAM 区域的大小(以字节为单位)。

除此之外,该 API 还提供了通过 :c:func:`bbram_read` 和 :c:func:`bbram_write` 分别读取和写入内存区域的方法。这两个函数预期仅在 BBRAM 处于有效状态且操作限定在内存区域范围内时才会成功。

API 参考 (API Reference)
**************************

.. doxygengroup:: bbram_interface
