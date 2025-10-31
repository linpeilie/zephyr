.. _thread_local_storage:

线程本地存储 (TLS)
##################

线程本地存储 (Thread Local Storage, TLS) 允许在每个线程的基础上分配变量。
这些变量存储在线程栈 (thread stack) 中，这意味着每个线程都有这些变量的自己的副本。

Zephyr 目前需要工具链支持 TLS。


配置
****

要在 Zephyr 中启用线程本地存储，需要启用 :kconfig:option:`CONFIG_THREAD_LOCAL_STORAGE`。
请注意，如果架构 (architecture) 或 SoC 没有启用隐藏选项
:kconfig:option:`CONFIG_ARCH_HAS_THREAD_LOCAL_STORAGE`，则此选项可能不可用，
这意味着架构或 SoC 没有必要的代码来支持线程本地存储和/或工具链不支持 TLS。

:kconfig:option:`CONFIG_ERRNO_IN_TLS` 可以与 :kconfig:option:`CONFIG_ERRNO` 一起启用，
以使变量 ``errno`` 成为线程本地变量。这允许用户线程访问 ``errno`` 的值而无需进行系统调用 (system call)。


声明和使用线程本地变量
*********************

宏 ``Z_THREAD_LOCAL`` 可用于声明线程本地变量。

例如，在头文件中声明线程本地变量：

.. code-block:: c

   extern Z_THREAD_LOCAL int i;

在源文件中声明实际变量：

.. code-block:: c

   Z_THREAD_LOCAL int i;

关键字 ``static`` 也可用于将变量限制在源文件内：

.. code-block:: c

   static Z_THREAD_LOCAL int j;

使用线程本地变量与使用其他变量相同，例如：

.. code-block:: c

   void testing(void) {
       i = 10;
   }
