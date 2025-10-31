.. _footprint:

优化占用空间
###########

堆栈大小
*******

各种系统线程的堆栈大小被慷慨地指定，以允许在尽可能多的受支持平台上在不同场景中使用。
你应该通过查看所有堆栈大小并为你的应用程序调整它们来开始优化过程：

:kconfig:option:`CONFIG_ISR_STACK_SIZE`
  默认设置为 2048

:kconfig:option:`CONFIG_MAIN_STACK_SIZE`
  默认设置为 1024

:kconfig:option:`CONFIG_IDLE_STACK_SIZE`
  默认设置为 320

:kconfig:option:`CONFIG_SYSTEM_WORKQUEUE_STACK_SIZE`
  默认设置为 1024

:kconfig:option:`CONFIG_PRIVILEGED_STACK_SIZE`
  默认设置为 1024，取决于用户空间功能。


未使用的外设
***********

默认启用某些外设。你可以在项目配置中禁用未使用的外设，例如::


        CONFIG_GPIO=n
        CONFIG_SPI=n

各种调试/信息选项
*****************

以下选项输出有关运行中应用程序的更多信息，并提供调试和错误处理的手段：

:kconfig:option:`CONFIG_BOOT_BANNER`
  可以禁用此选项以节省几个字节。

:kconfig:option:`CONFIG_DEBUG`
  可以为调试构建启用此选项。

请注意，引导横幅默认启用。


MPU/MMU 支持
***********

根据你的应用程序和平台需求，你可以禁用 MPU/MMU 支持以获得一些内存并改善性能。
但是，请考虑此配置选择的后果，因为你将失去高级堆栈检查和支持。
