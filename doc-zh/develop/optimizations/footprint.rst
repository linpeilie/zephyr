.. _footprint:

占用空间优化
########################

堆栈大小
***********

各种系统线程的堆栈大小被慷慨地指定,以允许在尽可能多的支持平台上的不同场景中使用。
您应该通过检查所有堆栈大小并根据应用程序调整它们来开始优化过程:

:kconfig:option:`CONFIG_ISR_STACK_SIZE`
  默认设置为 2048

:kconfig:option:`CONFIG_MAIN_STACK_SIZE`
  默认设置为 1024

:kconfig:option:`CONFIG_IDLE_STACK_SIZE`
  默认设置为 320

:kconfig:option:`CONFIG_SYSTEM_WORKQUEUE_STACK_SIZE`
  默认设置为 1024

:kconfig:option:`CONFIG_PRIVILEGED_STACK_SIZE`
  默认设置为 1024,取决于用户空间功能。


未使用的外设
******************

某些外设默认启用。您可以在项目配置中禁用未使用的外设,例如::


        CONFIG_GPIO=n
        CONFIG_SPI=n

各种调试/信息选项
***********************************

以下选项输出有关正在运行的应用程序的更多信息,并提供调试和错误处理的方法:

:kconfig:option:`CONFIG_BOOT_BANNER`
  可以禁用此选项以节省几个字节。

:kconfig:option:`CONFIG_DEBUG`
  可以为调试构建启用此选项。

请注意,启动横幅默认启用。


MPU/MMU 支持
***************

根据您的应用程序和平台需求,您可以禁用 MPU/MMU 支持以获得一些内存并提高性能。
但请考虑此配置选择的后果,因为您将失去高级堆栈检查和支持。
