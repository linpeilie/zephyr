.. _naming_conventions:.. _naming_conventions:



命名约定 (Naming conventions)Naming conventions

##############################################



本部分描述了 Zephyr 项目采用的命名约定,适用于其中使用的每种个人编程语言或工具。This section describes the naming conventions adopted by the Zephyr

Project, for each individual programming language or tool used in it.

C 代码命名约定 (C Code naming conventions)

*****************************************C Code naming conventions

*************************

本部分中的命名约定适用于 C 源文件和头文件,如各个小节中所述。

The naming conventions in this section apply to C source and header files,

公共符号前缀 (Public symbol prefixes)as stated in each individual sub-section.

====================================

Public symbol prefixes

引入到 Zephyr 的所有 :term:`公共 API (public API)` 必须按照它们所属的区域或子系统进行前缀。======================

下面为参考提供了区域或子系统前缀的示例。

All :term:`public APIs <public API>` introduced to Zephyr must be prefixed according

* ``k_`` 用于内核to the area or subsystem they belong to. Examples of area or subsystem prefixes

* ``sys_`` 用于系统级代码和功能are provided below for reference.

* ``net_`` 用于网络子系统

* ``bt_`` 用于蓝牙子系统* ``k_`` for the kernel

* ``i2c_`` 用于 I2C 控制器子系统* ``sys_`` for system-wide code and features

* ``net_`` for the networking subsystem
* ``bt_`` for the Bluetooth subsystem
* ``i2c_`` for the I2C controller subsystem
