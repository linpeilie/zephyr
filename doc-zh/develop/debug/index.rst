.. _develop_debug:

调试
#########

.. _application_debugging:

应用程序调试
*********************

本节是使用 QEMU 开始调试应用程序的快速实践参考。本节中的大部分内容已在 `QEMU`_ 和 `GNU_Debugger`_ 参考手册中涵盖。

.. _QEMU: https://wiki.qemu.org/Main_Page

.. _GNU_Debugger: https://www.gnu.org/software/gdb

在此快速参考中,您将找到可以帮助您快速设置调试环境的快捷方式、特定环境变量和参数。

调试在 QEMU 中运行的应用程序的最简单方法是使用 GNU 调试器,并通过 QEMU 在开发系统中设置本地 GDB 服务器。

您需要一个用于调试目的的 :abbr:`ELF (可执行和可链接格式)` 二进制映像。构建系统在构建目录中生成映像。默认情况下,内核二进制文件名为 :file:`zephyr.elf`。可以使用 :kconfig:option:`CONFIG_KERNEL_BIN_NAME` 更改名称。

GDB 服务器
==========

我们将使用标准的 1234 TCP 端口打开一个 :abbr:`GDB (GNU 调试器)` 服务器实例。可以将此端口号更改为最适合开发环境的端口。有多种方法可以做到这一点。每种方法都会启动一个 QEMU 实例,在启动时暂停处理器,并使 GDB 服务器实例侦听连接。

直接运行 QEMU
~~~~~~~~~~~~~~~~~~~~~

您可以运行 QEMU 在开始执行任何代码以调试之前侦听"gdb 连接"。

.. code-block:: bash

   qemu -s -S <image>

将设置 Qemu 侦听端口 1234 并等待与其的 GDB 连接。

上面使用的选项具有以下含义:

* ``-S`` 启动时不启动 CPU;相反,您必须在监视器中键入 'c'。
* ``-s`` :literal:`-gdb tcp::1234` 的简写:在 TCP 端口 1234 上打开 GDB 服务器。


通过 :command:`ninja` 运行 QEMU
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在应用程序的构建目录中运行以下命令:

.. code-block:: console

   ninja debugserver

QEMU 将通过 CMake 将控制台输出写入 :makevar:`${QEMU_PIPE}` 中指定的路径,通常是构建目录中的 :file:`qemu-fifo`。您可以在运行期间使用 :command:`tail -f qemu-fifo` 监视此文件。

通过 :command:`west` 运行 QEMU
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

从项目根目录运行以下命令:

.. code-block:: console

   west build -t debugserver_qemu

QEMU 将控制台输出写入您调用 :command:`west` 的终端。

配置 :command:`gdbserver` 侦听设备
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Kconfig 选项 :kconfig:option:`CONFIG_QEMU_GDBSERVER_LISTEN_DEV` 控制侦听设备,可以是 TCP 端口号或字符设备的路径。GDB 9.0 及更新版本还支持 Unix 域套接字。

如果未设置该选项,则 QEMU 调用将缺少 ``-s`` 或 ``-gdb`` 参数。然后,您可以使用 :envvar:`QEMU_EXTRA_FLAGS` shell 环境变量传入您自己的侦听设备配置。

GDB 客户端
==========

通过运行 :command:`gdb` 并给出以下命令来连接到服务器:

.. code-block:: bash

   $ path/to/gdb path/to/zephyr.elf
   (gdb) target remote localhost:1234
   (gdb) dir ZEPHYR_BASE

.. note::

   为您的系统替换正确的 :ref:`ZEPHYR_BASE <important-build-vars>`。

您可以使用本地 GDB 配置文件 :file:`.gdbinit` 在每次运行时初始化您的 GDB 实例。您的主目录是 :file:`.gdbinit` 的典型位置,但您可以配置 GDB 从其他位置加载,包括您调用 :command:`gdb` 的目录。此示例文件执行与上述相同的配置:

.. code-block:: none

   target remote localhost:1234
   dir ZEPHYR_BASE

替代界面
~~~~~~~~~~~~~~~~~~~~

GDB 提供了在终端中运行的基于 curses 的界面。在调用 :command:`gdb` 时传递 ``--tui`` 选项,或在 :command:`gdb` 中给出 ``tui enable`` 命令。

.. note::

   您的开发系统上的 GDB 版本可能不支持 ``--tui`` 选项。请确保使用来自 SDK 的 GDB 二进制文件,该文件对应于用于构建二进制文件的工具链。

最后,下面的命令使用 :abbr:`DDD (数据显示调试器)` 连接到 GDB 服务器,这是 GDB 的图形前端。以下命令从 ELF 二进制文件(在本例中为 :file:`zephyr.elf`)加载符号表。

.. code-block:: bash

   ddd --gdb --debugger "gdb zephyr.elf"

这两个命令都执行 :command:`gdb`。命令名称可能会根据您使用的工具链和交叉开发工具而改变。

:command:`ddd` 可能默认情况下未安装在您的开发系统中。按照系统说明安装它。例如,在 Ubuntu 系统上使用 :command:`sudo apt-get install ddd`。

调试
=========

如上所述配置后,当您连接 GDB 客户端时,应用程序将在系统启动时停止。您可以设置断点、单步执行代码等,就像直接在 :command:`gdb` 中运行应用程序时一样。

.. note::

   :command:`gdb` 不会在应用程序运行时打印系统控制台输出,这与您直接在 GDB 中运行本机应用程序时不同。如果您在连接客户端后只是 :command:`continue`,应用程序将运行,但似乎什么也不会发生。如上所述检查控制台输出。

使用 Eclipse 调试
******************

概述
========

CMake 支持生成项目描述文件,该文件可以导入到 Eclipse 集成开发环境 (IDE) 中并用于图形调试。

`GNU MCU Eclipse 插件`_ 提供了一种在 Eclipse 中使用 pyOCD、Segger J-Link 和 OpenOCD 调试工具调试 ARM 项目的机制。

以下教程演示了如何在 Windows 中使用 pyOCD 在 Eclipse 中调试 Zephyr 应用程序。它假设您已经安装了 GCC ARM Embedded 工具链和 pyOCD。

设置 Eclipse 开发环境
==========================================

#. 下载并安装 `Eclipse IDE for C/C++ Developers`_。

#. 在 Eclipse 中,通过打开菜单 ``Window->Eclipse Marketplace...``,搜索 ``GNU MCU Eclipse``,然后在匹配的结果上点击 ``Install`` 来安装 `GNU MCU Eclipse 插件`_。

#. 通过打开菜单 ``Window->Preferences``,导航到 ``MCU``,并设置 ``Global pyOCD Path`` 来配置 pyOCD GDB 服务器的路径。

生成并导入 Eclipse 项目
======================================

#. 按照 :ref:`toolchain_gnuarmemb` 中的描述设置 GNU Arm Embedded 工具链。

#. 导航到 Zephyr 树外的文件夹以构建应用程序。

   .. code-block:: console

      # On Windows
      cd %userprofile%

   .. note::
      如果构建目录是源目录的子目录,就像 Zephyr 中通常所做的那样,CMake 会警告:

      "构建目录是源目录的子目录。

      Eclipse 不能很好地支持这一点。强烈建议使用与源目录同级的构建目录。"

#. 使用 CMake 配置应用程序并使用 ninja 构建它。请注意 ``-G"Eclipse CDT4 - Ninja"`` 参数指定的不同 CMake 生成器。除了通常的 ninja 构建文件外,这还将生成 Eclipse 项目描述文件 :file:`.project`。

   .. zephyr-app-commands::
      :tool: all
      :zephyr-app: samples/synchronization
      :host-os: win
      :board: frdm_k64f
      :gen-args: -G"Eclipse CDT4 - Ninja"
      :goals: build
      :compact:

#. 在 Eclipse 中,通过打开菜单 ``File->Import...`` 并选择选项 ``Existing Projects into Workspace`` 来导入生成的项目。在 ``Select root directory:`` 选择中浏览到您的应用程序构建目录。选中在找到的项目列表中您的项目的复选框,然后点击 ``Finish`` 按钮。

创建调试器配置
===============================

#. 打开菜单 ``Run->Debug Configurations...``。

#. 选择 ``GDB PyOCD Debugging``,点击 ``New`` 按钮,并配置以下选项:

   - 在 Main 选项卡中:

     - Project: ``my_zephyr_app@build``
     - C/C++ Application: :file:`zephyr/zephyr.elf`

   - 在 Debugger 选项卡中:

     - pyOCD Setup

       - Executable path: :file:`${pyocd_path}\\${pyocd_executable}`
       - 取消选中 "Allocate console for semihosting"

     - Board Setup

       - Bus speed: 8000000 Hz
       - 取消选中 "Enable semihosting"

     - GDB Client Setup

       - Executable path 示例(使用您的 ``GNUARMEMB_TOOLCHAIN_PATH``):
         :file:`C:\\gcc-arm-none-eabi-6_2017-q2-update\\bin\\arm-none-eabi-gdb.exe`

   - 在 SVD Path 选项卡中:

     - File path: :file:`<workspace
       top>\\modules\\hal\\nxp\\mcux\\devices\\MK64F12\\MK64F12.xml`

     .. note::
        这是可选的。它向调试器提供 SoC 的内存映射寄存器地址和位字段。

#. 点击 ``Debug`` 按钮开始调试。

RTOS 感知
==============

Zephyr RTOS 感知支持在 `pyOCD v0.11.0`_ 及更高版本中实现。它与 Eclipse 中的 GDB PyOCD 调试兼容,但您必须在应用程序中启用 CONFIG_DEBUG_THREAD_INFO=y。

调试 I2C 通信
***************************

有可能记录应用程序完成的所有或部分 I2C 事务。此功能由 Kconfig 选项 :kconfig:option:`CONFIG_I2C_DUMP_MESSAGES` 启用,但它使用 :c:macro:`LOG_DBG` 函数打印内容,因此还必须启用 :kconfig:option:`CONFIG_I2C_LOG_LEVEL_DBG` 选项。

转储的示例输出如下所示::

   D: I2C msg: io_i2c_ctrl7_port0, addr=50
   D:    W      len=01: 00
   D:    R Sr P len=08:
   D: contents:
   D: 43 42 41 00 00 00 00 00 |CBA.....

第一行指示 I2C 控制器和事务的目标地址。在上面的示例中,I2C 控制器名为 ``io_i2c_ctrl7_port0``,目标设备地址为 ``0x50``

.. note::

   地址、长度和内容值采用十六进制,但缺少 ``0x`` 前缀

接下来的行包含发送和接收的消息。始终显示写消息的内容,而读消息的内容由函数 ``i2c_dump_msgs_rw`` 的参数控制。此函数可供用户使用,但也由 ``i2c_transfer`` API 函数内部调用,并启用读内容转储。在长度参数之前,使用缩写打印消息的标头:

  - W - 写消息
  - R - 读消息
  - Sr - 重启位
  - P - 停止位

上面的示例显示了一条写消息,字节 ``0x00`` 表示要从 I2C 目标读取的寄存器地址。之后,日志显示接收消息的长度,然后是从目标读取的字节 ``43 42 41 00 00 00 00 00``。内容转储由十六进制和 ASCII 表示组成。

过滤 I2C 通信转储
====================================

默认情况下,记录所有 I2C 控制器和 I2C 目标之间的所有 I2C 通信。它可能会使日志充满不相关的设备,并使有效调试与感兴趣的设备的通信变得困难。

启用 Kconfig 选项 :kconfig:option:`CONFIG_I2C_DUMP_MESSAGES_ALLOWLIST` 以创建要记录的 I2C 目标的允许列表。设备的允许列表使用设备树配置,例如::

  / {
      i2c {
          display0: some-display@a {
              ...
          };
          sensor3: some-sensor@b {
              ...
          };
      };

      i2c-dump-allowlist {
          compatible = "zephyr,i2c-dump-allowlist";
          devices = < &display0 >, < &sensor3 >;
      };
  };

过滤器节点由具有 ``zephyr,i2c-dump-allowlist`` 值的兼容字符串标识。使用 ``devices`` 属性和 I2C 总线上设备的 phandles 选择设备。

在上面的示例中,与设备 ``display0`` 和 ``sensor3`` 的通信将显示在日志中。



.. _Eclipse IDE for C/C++ Developers: https://www.eclipse.org/downloads/packages/eclipse-ide-cc-developers/oxygen2
.. _GNU MCU Eclipse plug-ins: https://gnu-mcu-eclipse.github.io/plugins/install/
.. _pyOCD v0.11.0: https://github.com/pyocd/pyOCD/releases/tag/v0.11.0

GDB server
==========

We will use the standard 1234 TCP port to open a :abbr:`GDB (GNU Debugger)`
server instance. This port number can be changed for a port that best suits the
development environment. There are multiple ways to do this. Each way starts a
QEMU instance with the processor halted at startup and with a GDB server
instance listening for a connection.

Running QEMU directly
~~~~~~~~~~~~~~~~~~~~~

You can run QEMU to listen for a "gdb connection" before it starts executing any
code to debug it.

.. code-block:: bash

   qemu -s -S <image>

will setup Qemu to listen on port 1234 and wait for a GDB connection to it.

The options used above have the following meaning:

* ``-S`` Do not start CPU at startup; rather, you must type 'c' in the
  monitor.
* ``-s`` Shorthand for :literal:`-gdb tcp::1234`: open a GDB server on
  TCP port 1234.


Running QEMU via :command:`ninja`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the following inside the build directory of an application:

.. code-block:: console

   ninja debugserver

QEMU will write the console output to the path specified in
:makevar:`${QEMU_PIPE}` via CMake, typically :file:`qemu-fifo` within the build
directory. You may monitor this file during the run with :command:`tail -f
qemu-fifo`.

Running QEMU via :command:`west`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the following from your project root:

.. code-block:: console

   west build -t debugserver_qemu

QEMU will write the console output to the terminal from which you invoked
:command:`west`.

Configuring the :command:`gdbserver` listening device
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Kconfig option :kconfig:option:`CONFIG_QEMU_GDBSERVER_LISTEN_DEV` controls
the listening device, which can be a TCP port number or a path to a character
device. GDB releases 9.0 and newer also support Unix domain sockets.

If the option is unset, then the QEMU invocation will lack a ``-s`` or a
``-gdb`` parameter. You can then use the :envvar:`QEMU_EXTRA_FLAGS` shell
environment variable to pass in your own listen device configuration.

GDB client
==========

Connect to the server by running :command:`gdb` and giving these commands:

.. code-block:: bash

   $ path/to/gdb path/to/zephyr.elf
   (gdb) target remote localhost:1234
   (gdb) dir ZEPHYR_BASE

.. note::

   Substitute the correct :ref:`ZEPHYR_BASE <important-build-vars>` for your
   system.

You can use a local GDB configuration :file:`.gdbinit` to initialize your GDB
instance on every run. Your home directory is a typical location for
:file:`.gdbinit`, but you can configure GDB to load from other locations,
including the directory from which you invoked :command:`gdb`. This example
file performs the same configuration as above:

.. code-block:: none

   target remote localhost:1234
   dir ZEPHYR_BASE

Alternate interfaces
~~~~~~~~~~~~~~~~~~~~

GDB provides a curses-based interface that runs in the terminal. Pass the ``--tui``
option when invoking :command:`gdb` or give the ``tui enable`` command within
:command:`gdb`.

.. note::

   The GDB version on your development system might not support the ``--tui``
   option. Please make sure you use the GDB binary from the SDK which
   corresponds to the toolchain that has been used to build the binary.

Finally, the command below connects to the GDB server using the :abbr:`DDD
(Data Display Debugger)`, a graphical frontend for GDB. The following command
loads the symbol table from the ELF binary file, in this instance,
:file:`zephyr.elf`.

.. code-block:: bash

   ddd --gdb --debugger "gdb zephyr.elf"

Both commands execute :command:`gdb`. The command name might
change depending on the toolchain you are using and your cross-development
tools.

:command:`ddd` may not be installed in your
development system by default. Follow your system instructions to install
it. For example, use :command:`sudo apt-get install ddd` on an Ubuntu system.

Debugging
=========

As configured above, when you connect the GDB client, the application will be
stopped at system startup. You may set breakpoints, step through code, etc. as
when running the application directly within :command:`gdb`.

.. note::

   :command:`gdb` will not print the system console output as the application runs,
   unlike when you run a native application in GDB directly. If you just
   :command:`continue` after connecting the client, the application will run,
   but nothing will appear to happen. Check the console output as described
   above.

Debug with Eclipse
******************

Overview
========

CMake supports generating a project description file that can be imported into
the Eclipse Integrated Development Environment (IDE) and used for graphical
debugging.

The `GNU MCU Eclipse plug-ins`_ provide a mechanism to debug ARM projects in
Eclipse with pyOCD, Segger J-Link, and OpenOCD debugging tools.

The following tutorial demonstrates how to debug a Zephyr application in
Eclipse with pyOCD in Windows. It assumes you have already installed the GCC
ARM Embedded toolchain and pyOCD.

Set Up the Eclipse Development Environment
==========================================

#. Download and install `Eclipse IDE for C/C++ Developers`_.

#. In Eclipse, install the `GNU MCU Eclipse plug-ins`_ by opening the menu
   ``Window->Eclipse Marketplace...``, searching for ``GNU MCU Eclipse``, and
   clicking ``Install`` on the matching result.

#. Configure the path to the pyOCD GDB server by opening the menu
   ``Window->Preferences``, navigating to ``MCU``, and setting the ``Global
   pyOCD Path``.

Generate and Import an Eclipse Project
======================================

#. Set up a GNU Arm Embedded toolchain as described in
   :ref:`toolchain_gnuarmemb`.

#. Navigate to a folder outside of the Zephyr tree to build your application.

   .. code-block:: console

      # On Windows
      cd %userprofile%

   .. note::
      If the build directory is a subdirectory of the source directory, as is
      usually done in Zephyr, CMake will warn:

      "The build directory is a subdirectory of the source directory.

      This is not supported well by Eclipse.  It is strongly recommended to use
      a build directory which is a sibling of the source directory."

#. Configure your application with CMake and build it with ninja. Note the
   different CMake generator specified by the ``-G"Eclipse CDT4 - Ninja"``
   argument. This will generate an Eclipse project description file,
   :file:`.project`, in addition to the usual ninja build files.

   .. zephyr-app-commands::
      :tool: all
      :zephyr-app: samples/synchronization
      :host-os: win
      :board: frdm_k64f
      :gen-args: -G"Eclipse CDT4 - Ninja"
      :goals: build
      :compact:

#. In Eclipse, import your generated project by opening the menu
   ``File->Import...`` and selecting the option ``Existing Projects into
   Workspace``. Browse to your application build directory in the choice,
   ``Select root directory:``. Check the box for your project in the list of
   projects found and click the ``Finish`` button.

Create a Debugger Configuration
===============================

#. Open the menu ``Run->Debug Configurations...``.

#. Select ``GDB PyOCD Debugging``, click the ``New`` button, and configure the
   following options:

   - In the Main tab:

     - Project: ``my_zephyr_app@build``
     - C/C++ Application: :file:`zephyr/zephyr.elf`

   - In the Debugger tab:

     - pyOCD Setup

       - Executable path: :file:`${pyocd_path}\\${pyocd_executable}`
       - Uncheck "Allocate console for semihosting"

     - Board Setup

       - Bus speed: 8000000 Hz
       - Uncheck "Enable semihosting"

     - GDB Client Setup

       - Executable path example (use your ``GNUARMEMB_TOOLCHAIN_PATH``):
         :file:`C:\\gcc-arm-none-eabi-6_2017-q2-update\\bin\\arm-none-eabi-gdb.exe`

   - In the SVD Path tab:

     - File path: :file:`<workspace
       top>\\modules\\hal\\nxp\\mcux\\devices\\MK64F12\\MK64F12.xml`

     .. note::
        This is optional. It provides the SoC's memory-mapped register
        addresses and bitfields to the debugger.

#. Click the ``Debug`` button to start debugging.

RTOS Awareness
==============

Support for Zephyr RTOS awareness is implemented in `pyOCD v0.11.0`_ and later.
It is compatible with GDB PyOCD Debugging in Eclipse, but you must enable
CONFIG_DEBUG_THREAD_INFO=y in your application.

Debugging I2C communication
***************************

There is a possibility to log all or some of the I2C transactions done by the application.
This feature is enabled by the Kconfig option :kconfig:option:`CONFIG_I2C_DUMP_MESSAGES`, but it
uses the :c:macro:`LOG_DBG` function to print the contents so the
:kconfig:option:`CONFIG_I2C_LOG_LEVEL_DBG` option must also be enabled.

The sample output of the dump looks like this::

   D: I2C msg: io_i2c_ctrl7_port0, addr=50
   D:    W      len=01: 00
   D:    R Sr P len=08:
   D: contents:
   D: 43 42 41 00 00 00 00 00 |CBA.....

The first line indicates the I2C controller and the target address of the transaction.
In above example, the I2C controller is named ``io_i2c_ctrl7_port0`` and the target device address
is ``0x50``

.. note::

   the address, length and contents values are in hexadecimal, but lack the ``0x`` prefix

Next lines contain messages, both sent and received. The contents of write messages is
always shown, while the content of read messages is controlled by a parameter to the
function ``i2c_dump_msgs_rw``. This function is available for use by user, but is also
called internally by ``i2c_transfer`` API function with read content dump enabled.
Before the length parameter, the header of the message is printed using abbreviations:

  - W - write message
  - R - read message
  - Sr - restart bit
  - P - stop bit

The above example shows one write message with byte ``0x00`` representing the address of register to
read from the I2C target. After that the log shows the length of received message and following
that, the bytes read from the target ``43 42 41 00 00 00 00 00``.
The content dump consist of both the hex and ASCII representation.

Filtering the I2C communication dump
====================================

By default, all I2C communication is logged between all I2C controllers and I2C targets.
It may litter the log with unrelated devices and make it difficult to effectively debug the
communication with a device of interest.

Enable the Kconfig option :kconfig:option:`CONFIG_I2C_DUMP_MESSAGES_ALLOWLIST` to create an
allowlist of I2C targets to log.
The allowlist of devices is configured using the devicetree, for example::

  / {
      i2c {
          display0: some-display@a {
              ...
          };
          sensor3: some-sensor@b {
              ...
          };
      };

      i2c-dump-allowlist {
          compatible = "zephyr,i2c-dump-allowlist";
          devices = < &display0 >, < &sensor3 >;
      };
  };

The filters nodes are identified by the compatible string with ``zephyr,i2c-dump-allowlist`` value.
The devices are selected using the ``devices`` property with phandles to the devices on the I2C bus.

In the above example, the communication with device ``display0`` and ``sensor3`` will be displayed
in the log.



.. _Eclipse IDE for C/C++ Developers: https://www.eclipse.org/downloads/packages/eclipse-ide-cc-developers/oxygen2
.. _GNU MCU Eclipse plug-ins: https://gnu-mcu-eclipse.github.io/plugins/install/
.. _pyOCD v0.11.0: https://github.com/pyocd/pyOCD/releases/tag/v0.11.0
