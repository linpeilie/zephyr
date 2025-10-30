.. _clion_ide:

CLion
#####

.. note::

   本指南描述了如何在 CLion 中使用 IDE 的 CMake 集成来设置、构建和调试 Zephyr 的示例应用程序。这种方法不再是最优的。

   CLion 现在具有 `原生 Zephyr West 集成`_,提供了一种更简单、更直观的方式来打开、构建和运行/调试 Zephyr 项目。本指南将很快更新,但如果您更喜欢使用 CMake,它仍然有效。

CLion_ 是一个支持多线程 RTOS 调试的跨平台 C/C++ IDE。

本指南描述了在 CLion 中设置、构建和调试 Zephyr 的 :zephyr:code-sample:`multi-thread-blinky` 示例的过程。

这些说明已在 Windows 上测试过。就 CLion 工作流程而言,macOS 和 Linux 的步骤相同,但请确保选择正确的环境文件并调整路径。

获取 CLion
**********

`下载 CLion`_ 并安装。

初始化新工作区
**************

本指南详细介绍了如何构建和调试 :zephyr:code-sample:`multi-thread-blinky` 示例应用程序,但对于任何 Zephyr 项目和 :ref:`工作区布局 <west-workspaces>`,说明都是类似的。

开始之前,请确保您按照 :ref:`getting_started` 中的说明拥有一个可工作的 Zephyr 开发环境。

在 CLion 中打开项目
*******************

#. 在 CLion 中,单击欢迎屏幕上的 :guilabel:`Open`,或从主菜单中选择 :menuselection:`File --> Open`。

#. 导航到您的 Zephyr 工作区(即,如果您按照入门说明操作,则为 HOME 目录中的 :file:`zephyrproject` 文件夹),然后选择 :file:`zephyr/samples/basic/threads` 或其他示例项目文件夹。

   单击 :guilabel:`OK`。

#. 如果出现提示,请单击 :guilabel:`Trust Project`。

   有关项目安全性的更多信息,请参阅 CLion Web 帮助中的 `项目安全性`_ 部分。

配置工具链和 CMake 配置文件
*****************************

CLion 将打开 :guilabel:`Open Project Wizard` 和 CMake 配置文件设置。如果没有发生,请转到 :menuselection:`Settings --> Build, Execution, Deployment --> CMake`。

#. 单击 :guilabel:`Toolchain` 字段旁边的 :guilabel:`Manage Toolchains`。这将打开 :guilabel:`Toolchain` 设置对话框。

#. 我们建议您在 Windows 上使用带有默认设置的 :guilabel:`Bundled MinGW` 工具链,或在 Unix 机器上使用 :guilabel:`System`(默认)工具链。

#. 单击 :menuselection:`Add environment --> From file` 并选择 ``..\.venv\Scripts\activate.bat``。

   .. figure:: img/clion_toolchain_mingw.webp
      :width: 600px
      :align: center
      :alt: 带有环境脚本的 MinGW 工具链

   单击 :guilabel:`Apply` 保存更改。

#. 返回 CMake 配置文件设置对话框,在 :guilabel:`CMake options` 字段中指定您的开发板。例如:

   .. code-block::

      -DBOARD=nrf52840dk/nrf52840

   .. figure:: img/clion_cmakeprofile.webp
      :width: 600px
      :align: center
      :alt: CMake 配置文件

#. 单击 :guilabel:`Apply` 保存更改。

   CMake 加载应该成功完成。

为调试配置 Zephyr 参数
************************

#. 在右上角的配置切换器中,选择 :guilabel:`guiconfig` 并单击锤子图标。

#. 使用 GUI 应用程序设置以下标志:

   .. code-block::

      DEBUG_THREAD_INFO
      THREAD_RUNTIME_STATS
      DEBUG_OPTIMIZATIONS

构建项目
********

在配置切换器中,选择 **zephyr_final** 并单击锤子图标。

请注意,此时也可以调用其他 CMake 目标,如 ``puncover`` 或 ``hardenconfig``。


启用 RTOS 集成
**************

#. 转到 :menuselection:`Settings --> Build, Execution, Deployment --> Embedded Development --> RTOS Integration`。

#. 设置 :guilabel:`Enable RTOS Integration` 复选框。

   此选项在调试期间启用 Zephyr 任务视图。有关更多信息,请参阅 CLion Web 帮助中的 `多线程 RTOS 调试`_。

   您可以将选项设置为 :guilabel:`Auto`。CLion 将自动检测 Zephyr。

创建嵌入式 GDB 服务器配置
**************************

为了在 CLion 中调试 Zephyr 应用程序,您需要从嵌入式 GDB 服务器模板创建运行/调试配置。

以下说明显示了 Nordic Semiconductor 开发板和 Segger J-Link 调试探针的情况。如果您的设置不同,请确保相应地调整配置设置。

#. 从主菜单中选择 :menuselection:`Run --> New Embedded Configuration`。

#. 配置设置:

    .. list-table::
        :header-rows: 1

        * - 选项
          - 值

        * - :guilabel:`Name`(可选)
          - Zephyr-threads

        * - :guilabel:`GDB Server Type`
          - Segger JLink

        * - :guilabel:`Location`
          - Windows 上 ``JLinkGDBServerCL.exe`` 的路径或 macOS/Linux 上 ``JLinkGDBServer`` 二进制文件的路径。

        * - :guilabel:`Debugger`
          - Bundled GDB

            .. note:: 对于非 ARM 和非 x86 架构,请使用来自 Zephyr SDK 的 GDB 可执行文件。确保选择支持 Python 的版本(例如,**riscv64-zephyr-elf-gdb-py**),并检查 Python 是否存在于系统 ``PATH`` 中。

        * - :guilabel:`Target`
          - zephyr-final

        * - :guilabel:`Executable binary`
          - zephyr-final

        * - :guilabel:`Download binary`
          - Always

        * - :guilabel:`TCP/IP port`
          - Auto

    .. figure:: img/clion_gdbserverconfig.webp
       :width: 500px
       :align: center
       :alt: 嵌入式 GDB 服务器配置

#. 单击 :guilabel:`Next` 设置 Segger J-Link 参数。

    .. figure:: img/clion_segger_settings.webp
       :width: 500px
       :align: center
       :alt: Segger J-Link 参数

#. 准备好后单击 :guilabel:`Create`。

开始调试
********

#. 通过单击代码行旁边的左侧装订线来放置断点。

#. 确保在配置切换器中选择了 **Zephyr-threads**,然后单击错误图标或按 :kbd:`Ctrl+D`。

#. 当断点被命中时,CLion 打开调试工具窗口。

   Zephyr 任务列在 :guilabel:`Threads & Variables` 窗格中。您可以在它们之间切换并检查每个任务的变量。

    .. figure:: img/clion_debug_threads.webp
       :width: 800px
       :align: center
       :alt: 在调试会话期间查看 Zephyr 任务

   有关 IDE 调试功能的详细说明,请参阅 `CLion Web 帮助`_。

.. _原生 Zephyr West 集成: https://jb.gg/cl_zephyr_doc
.. _CLion: https://www.jetbrains.com/clion/
.. _下载 CLion: https://www.jetbrains.com/clion/download
.. _项目安全性: https://www.jetbrains.com/help/clion/project-security.html#projects_security
.. _多线程 RTOS 调试: https://www.jetbrains.com/help/clion/rtos-debug.html
.. _CLion Web 帮助: https://www.jetbrains.com/help/clion/debugging-code.html
