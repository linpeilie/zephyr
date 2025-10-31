.. _design_guidelines:

API 设计指南
###########

Zephyr 的开发和演进是一个集体努力，为了简化维护和增强，
在开发新功能或接口时应遵循一些通用策略。

使用回调
*******

许多 API 涉及将回调作为参数传递或作为配置结构的成员。
在指定回调签名时应遵循以下策略：

* 第一个参数应该是指向与回调最密切相关的对象的指针。
  对于设备驱动程序，这将是 ``const struct device *dev``。
  对于库函数，它可能是在提供回调时引用的另一个对象的指针。

* 下一个参数应该是特定于回调调用的其他信息，
  如通道标识符、新状态值和/或消息指针，后跟消息长度。

* 最后一个参数应该是 ``void *user_data`` 指针，用于携带允许共享回调函数
  定位处理回调所需的其他资料的上下文。

提供 ``user_data`` 作为最后一个参数的例外情况可能会被允许，
当回调本身是通过将被嵌入另一个结构中的结构提供时。
例如 :c:struct:`gpio_callback`，通常在特定于代码的数据结构中定义，
该结构也定义了回调函数。在这些情况下，可以通过 :c:macro:`CONTAINER_OF`
间接由回调访问进一步的上下文。

示例
====

* :c:type:`k_timer_expiry_t` 的要求在系统计时器警报触发时调用，通过以下方式满足::

    void handle_timeout(struct k_timer *timer)
    { ... }

  这里的假设，与 :c:struct:`gpio_callback` 一样，是计时器被嵌入在可从
  :c:macro:`CONTAINER_OF` 访问的结构中，该结构可以向回调提供其他上下文。

* :c:type:`counter_alarm_callback_t` 的要求在计数器设备警报触发时调用，
  通过以下方式满足::

    void handle_alarm(const struct device *dev,
                      uint8_t chan_id,
		      uint32_t ticks,
		      void *user_data)
    { ... }

  这提供了更完整的有用信息，包括哪个计数器通道超时以及发生超时时的计数器值，
  以及用户上下文，可能是也可能不是用于注册回调的 :c:struct:`counter_alarm_cfg`，
  取决于用户需求。

条件数据和 API
**************

API 和库可能提供在 RAM 或代码大小中代价高昂但在某种意义上是可选的功能，
因为某些应用程序可以在没有它们的情况下实现。此类功能的示例包括
:kconfig:option:`捕获时间戳 <CONFIG_CAN_RX_TIMESTAMP>` 或
:kconfig:option:`提供替代接口 <CONFIG_SPI_ASYNC>`。
开发人员与社区协调必须确定启用功能是否应通过 Kconfig 选项控制。

在确定功能是可选的情况下，应遵循以下做法。

* 仅当启用功能时访问的任何数据应通过结构或联合声明中的
  ``#ifdef CONFIG_MYFEATURE`` 有条件包含。这减少了不需要该功能的应用程序的内存使用。
* 仅当启用选项时可用的函数声明应无条件提供。在描述中添加注释说明该函数
  仅在启用指定功能时可用，按名称引用所需的 Kconfig 符号。
  在使用函数但未启用的情况下，函数的定义应从编译中排除，
  以便对不受支持的 API 的引用将导致链接时错误。
* 当特定于功能的代码隔离在没有其他内容的源文件中时，该文件应在 ``CMakeLists.txt`` 中有条件包含::

    zephyr_sources_ifdef(CONFIG_MYFEATURE foo_funcs.c)
* 当特定于功能的代码是具有其他内容的源文件的一部分时，功能特定代码应使用
  ``#ifdef CONFIG_MYFEATURE`` 有条件处理。

用于启用功能的 Kconfig 标志应添加到 :file:`doc/zephyr.doxyfile.in` 中的
``PREDEFINED`` 变量中，以确保条件 API 和函数出现在生成的文档中。

返回代码
*******

API 的实现（例如用于访问外设的 API）可能仅实现最小操作所需功能的子集。
需要在不支持的 API 和未实现或可选的 API 之间进行区分：

- 受支持但未实现的 API 应返回 ``-ENOSYS``。

- 不受硬件支持的可选 API 应被实现，
  在这种情况下的返回代码应为 ``-ENOTSUP``。

- 当 API 被实现，但调用中请求的特定选项组合无法由实现满足时，
  调用应返回 ``-ENOTSUP``。（例如，对支持仅边沿触发中断的硬件的
  电平触发 GPIO 中断的请求）
