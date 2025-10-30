.. _rtc_api:

实时时钟 (RTC)
##############

概述
****

.. list-table:: **术语表**
    :widths: 30 80
    :header-rows: 1

    * - 术语
      - 定义
    * - 实时时钟
      - 使用分解时间跟踪时间的低功耗设备
    * - 实时计数器
      - 可用于跟踪时间的低功耗计数器
    * - RTC
      - 实时时钟的缩写

RTC 是一种使用分解时间跟踪时间的低功耗设备。不应将其与有时共享相同名称、缩写或两者的
低功耗计数器混淆。

RTC 通常针对低能耗进行了优化,即使系统处于低功耗状态,通常也会保持运行。

RTC 通常包含一个或多个可以配置为在给定时间触发的闹钟。这些闹钟通常用于将系统从
低功耗状态唤醒。

设备树绑定
**********

RTC 绑定必须包含 ``rtc-device.yaml`` 绑定,该绑定包含 ``base.yaml`` 绑定和
必需的 ``alarms-count`` 属性。

.. code-block:: yaml

   include: rtc-device.yaml

设备驱动程序设计
****************

驱动程序初始化
==============

RTC 从不由系统关闭电源。在初始化时,驱动程序应该期望 RTC 处于以下状态之一:

* 已供电、已配置并正在运行。
* 已供电、未配置并已停止。

在初始化时,驱动程序应确保 RTC 配置正确,同时保留时间、闹钟和运行状态。

通过调用 :c:func:`rtc_set_time` 设置时间,此时 RTC 将开始运行。闹钟挂起状态
由 :c:func:`rtc_alarm_is_pending` 清除,或由 :c:func:`rtc_alarm_set_callback`
导致的闹钟回调清除。

GPIO 路由中断
=============

具有连接的中断输出引脚的 RTC 应在初始化时配置并启用它们。主机可以为其 GPIO 启用
和禁用中断,但 RTC 中断输出引脚必须保持启用状态。

这确保了内部和外部连接的 RTC 之间的行为一致,并允许在任何启用的 RTC 事件(如闹钟
或更新)上通过 GPIO 唤醒系统。

.. note::

   具有未连接的中断输出引脚的 RTC 不允许定期轮询 RTC 以模拟其连接。
   在这种情况下,:c:func:`rtc_alarm_set_callback` 和
   :c:func:`rtc_update_set_callback` 应返回 ``-ENOTSUP``。

时钟输出
========

如果支持,时钟输出配置在设备树中定义。驱动程序在初始化时配置输出。

配置选项
********

相关配置选项:

* :kconfig:option:`CONFIG_RTC`
* :kconfig:option:`CONFIG_RTC_ALARM`
* :kconfig:option:`CONFIG_RTC_UPDATE`
* :kconfig:option:`CONFIG_RTC_CALIBRATION`

API 参考
********

.. doxygengroup:: rtc_interface

RTC 设备驱动程序测试套件
*************************

测试套件验证 RTC 设备驱动程序的行为。它被设计为可在开发板之间移植。它使用设备树
别名 ``rtc`` 来指定要测试的 RTC 设备。

此测试套件测试以下内容:

* 设置和获取时间。
* RTC 时间正确递增。
* 如果硬件支持,在启用和未启用回调的情况下测试闹钟
* 如果硬件支持,测试校准。

校准测试测试一系列值,这些值会打印到控制台以供手动比较。用户必须检查设置和获取的
值以确保它们有效。

默认情况下,仅启用强制性的时间设置和获取以进行测试。要测试可选的闹钟、更新事件
回调和时钟校准,必须通过选择 :kconfig:option:`CONFIG_RTC_ALARM`、
:kconfig:option:`CONFIG_RTC_UPDATE` 和 :kconfig:option:`CONFIG_RTC_CALIBRATION`
来启用这些功能。

以下示例为 ``native_sim`` 开发板构建测试套件。要为不同的开发板构建测试套件,
请将 ``native_sim`` 开发板替换为您的开发板。

要使用默认配置构建测试应用程序,仅测试强制性功能,可以使用以下命令作为参考:

.. zephyr-app-commands::
   :tool: west
   :host-os: unix
   :board: native_sim
   :zephyr-app: tests/drivers/rtc/rtc_api
   :goals: build

要构建启用了其他 RTC 功能的测试,请使用 menuconfig 通过更新配置来启用其他功能。
可以使用以下命令作为参考:

.. zephyr-app-commands::
   :tool: west
   :host-os: unix
   :board: native_sim
   :zephyr-app: tests/drivers/rtc/rtc_api
   :goals: menuconfig

然后使用以下命令构建测试应用程序:

.. zephyr-app-commands::
   :tool: west
   :host-os: unix
   :board: native_sim
   :zephyr-app: tests/drivers/rtc/rtc_api
   :maybe-skip-config:
   :goals: build

要运行测试套件,将应用程序刷写并在您的开发板上运行,输出将打印到控制台。

.. note::

    如果测试的是真实硬件,每个测试最多需要 30 秒。

.. _rtc_api_emul_dev:

RTC 模拟设备
************

模拟 RTC 设备完全实现 RTC API,并将像真实的 RTC 设备一样运行,但有以下限制:

* RTC 时间在应用程序初始化过程中不持久。
* RTC 闹钟在应用程序初始化过程中不持久。
* RTC 时间会随时间漂移。

每次初始化应用程序时,RTC 的时间和闹钟都会重置。使用 :c:func:`rtc_get_time`
读取时间将返回 ``-ENODATA``,直到使用 :c:func:`rtc_set_time` 设置时间。然后
RTC 将表现得像真实的 RTC,直到应用程序重置。

模拟 RTC 设备驱动程序是为兼容的 :dtcompatible:`zephyr,rtc-emul` 构建的,
如果选择了 :kconfig:option:`CONFIG_RTC`,将包含它。

Zephyr 中 RTC 的历史
*********************

在创建此 API 之前,RTC 已使用 :ref:`counter_api` API 得到支持。unix 时间戳
用于在 RTC 驱动程序内部在分解时间和 unix 时间戳之间进行转换,该驱动程序内部
使用分解时间表示。

这种方法的缺点是硬件计数器无法设置为特定计数,需要所有 RTC 使用特定于设备的
API 来设置时间,在某些情况下不必要地从 unix 时间转换为分解时间,以及缺少一些
常见功能,如输入时钟校准和更新回调。
