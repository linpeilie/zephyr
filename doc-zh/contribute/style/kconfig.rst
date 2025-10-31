.. _kconfig_style:

Kconfig 样式指南 (Kconfig Style Guidelines)
###########################################

本文档为在 Zephyr 项目中编写 Kconfig 文件提供样式指南。遵循这些指南可确保整个代码库
的一致性和可读性,使开发人员更容易理解和维护配置选项。

以下各部分通过示例提供指南以说明适当的 Kconfig 格式和命名约定。


基本格式规则 (Basic Formatting Rules)
***********************************

编写 Kconfig 文件时,请遵循以下基本格式规则:

* **行长度**: 将行保持在 100 列或更少。
* **缩进**: 使用制表符进行缩进,除了应该放在一个制表符加两个额外空格处的 ``help`` 条目文本。
* **间距**: 在选项声明之间留一个空行。
* **注释**: 将注释格式化为 ``# Comment`` 而不是 ``#Comment``。
* **条件块**: 在每个顶级 ``if`` 和 ``endif`` 语句之前/之后插入一个空行。

有关使用 ``select`` 等语句的指导,请参阅 :ref:`kconfig_tips_and_tricks` 了解更多信息。

符号命名和结构 (Symbol Naming and Structure)
*****************************************

以下示例演示了适当的 Kconfig 符号命名和结构:

.. literalinclude:: kconfig_demo_simple.txt
   :language: kconfig
   :start-after: start-after-here

.. literalinclude:: kconfig_demo_complex.txt
   :language: kconfig
   :start-after: start-after-here


命名约定 (Naming Conventions)
****************************

* 通常,涉及同一组件的符号应该与其他符号不同。这通常可以通过使用公共前缀来实现。
  此前缀可以是简单关键字,或者如驱动程序一样,是多个关键字以获得更高精度。

* 公共前缀通常表示符号所属的子系统或组件。

* 启用符号名称应由关键字组成,以提供符号在从最常见到最特定的范围中的上下文
  (例如 *驱动程序类型* -> *驱动程序名称*)。

* 启用符号的提示应使用与符号名称本身相同的逻辑,但按相反顺序使用关键字。

   * 遵守此风格使在 UI 中搜索符号更容易,因为可以按范围关键字进行过滤。

* 当启用符号依赖于设备树节点时,考虑依赖自动创建的 ``DT_HAS_<node>_ENABLED`` 符号。

各子树的具体格式:

* **驱动程序 (/drivers)**: 对符号使用格式 ``{驱动程序类型}_{驱动程序名称}`,
  对提示使用 ``{驱动程序名称} {驱动程序类型} driver``。

* **传感器 (/drivers/sensors)**: 对符号使用格式 ``SENSOR_{传感器名称}`,
  对提示使用 ``{传感器名称} {传感器类型} sensor driver``。

* **架构 (/arch)**: 许多符号在架构中共享。创建新符号之前,检查其他架构中是否已存在相似的符号。

示例 (Examples)
==============

.. note::

   以下示例仅出于简洁起见显示符号和提示行。

**驱动程序示例:**

.. literalinclude:: kconfig_example_driver.txt
   :language: kconfig
   :start-after: start-after-here

**传感器示例:**

.. literalinclude:: kconfig_example_sensor.txt
   :language: kconfig
   :start-after: start-after-here

配置符号组织 (Configuration Symbol Organization)
**********************************************

当功能使用配置符号来配置其行为时:

* 使用 ``menuconfig`` 而不是 ``config`` 来定义启用功能(即使配置符号没有提示)。

* 将配置符号封装在 ``if`` 语句中以声明它们对启用符号的依赖
  (这会自动将这些符号分组在 UI 中启用符号下)。

* 使用启用符号的名称作为配置符号的前缀以获得范围和上下文。

* 在配置符号的提示中,描述符号配置的内容,而不重复范围关键字,
  因为 UI 中的分组提供了此上下文。

文件组织 (File Organization)
***************************

组织 Kconfig 文件时:

* 保持 Kconfig 文件接近它配置的源文件。

* 处理大型 Kconfig 文件时(例如具有许多配置符号),考虑将(某些)它们分组到单独的文件中
  并使用 ``source`` 指令导入它以提高可读性。
