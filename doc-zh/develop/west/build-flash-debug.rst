.. _west-build-flash-debug:

构建、烧录和调试
################

Zephyr为构建、烧录和与运行在板上的Zephyr程序交互提供了多个:ref:`west扩展命令<west-extensions>`：
``build``、``flash``、``debug``、``debugserver``和``attach``。

有关为烧录和调试命令添加板级支持的信息，请参见板卡移植指南中的:ref:`flash-and-debug-support`。

.. Add a per-page contents at the top of the page. This page is nested
   deeply enough that it doesn't have any subheadings in the main nav.

.. only:: html

   .. contents::
      :local:

.. _west-building:

构建: ``west build``
************************

.. tip:: 运行``west build -h``以快速了解概览。

``build``命令帮助您从源代码构建Zephyr应用程序。您可以使用:ref:`west配置<west-config-cmd>`来配置其行为。

其默认行为尝试"做您想要的"：

- 如果您当前工作目录中有一个名为:file:`build`的Zephyr构建目录，它将被增量重新编译。如果您从Zephyr构建目录运行``west build``，情况也是如此。

- 否则，如果您从Zephyr应用程序的源目录运行``west build``且没有找到构建目录，将创建一个新目录，应用程序将在其中编译。

基础知识
======

使用``west build``的最简单方法是转到应用程序的根目录（即包含应用程序:file:`CMakeLists.txt`的文件夹），然后运行::

  west build -b <BOARD>

其中``<BOARD>``是您要构建的板卡名称。这与您调用CMake时将提供的名称完全相同：``cmake -DBOARD=<BOARD>``。

.. tip::

   您可以使用:ref:`west boards <west-boards>`命令列出所有支持的板卡。

将创建一个名为:file:`build`的构建目录，在``west build``运行CMake在该目录中创建构建系统后，应用程序将在那里编译。如果``west build``找到现有的构建目录，应用程序将在那里增量重新编译，而不会重新运行CMake。您可以使用``--cmake``强制CMake再次运行。

如果您已经有一个现有的构建目录，则不需要使用``--board``选项；``west build``可以从CMake缓存中找出板卡。对于新构建，将依次检查``--board``选项、:envvar:`BOARD`环境变量或``build.board``配置选项。

.. _west-multi-domain-builds:

Sysbuild（多域构建）
==============================

:ref:`sysbuild`可用于创建多域构建系统，为单个或多个板卡组合多个镜像。

使用``--sysbuild``选择带有``west build``的:ref:`sysbuild`构建基础架构来构建多个域。

有关使用sysbuild的更多详细信息，可以在:ref:`sysbuild`指南中找到。

.. tip::

   可以启用``build.sysbuild``配置选项来告诉``west build``默认使用sysbuild构建。
   ``--no-sysbuild``可用于为特定构建禁用sysbuild。

``west build``将通过sysbuild指定的域的顶级构建文件夹构建所有域。

多域项目中的单个域可以通过使用``--domain``参数来构建。

示例
========

以下是按区域分组的一些``west build``使用示例。

强制CMake重新运行
--------------------------

要强制CMake重新运行，请使用``--cmake``（或``-c``）选项::

  west build -c

设置默认板卡
-----------------------

要配置``west build``默认构建``reel_board``::

  west config build.board reel_board

（您可以在此处使用Zephyr支持的任何其他板卡；不一定是``reel_board``。）

.. _west-building-dirs:

设置源目录和构建目录
------------------------------------

要显式设置应用程序源目录，请将其路径作为位置参数提供::

  west build -b <BOARD> path/to/source/directory

要显式设置构建目录，请使用``--build-dir``（或``-d``）::

  west build -b <BOARD> --build-dir path/to/build/directory

要将默认构建目录从:file:`build`更改为其他目录，请使用``build.dir-fmt``配置选项。这允许您使用格式字符串命名构建目录，如下所示::

  west config build.dir-fmt "build/{board}/{app}"

使用上述配置，运行``west build -b reel_board samples/hello_world``将使用构建目录:file:`build/reel_board/hello_world`。有关此选项的更多详细信息，请参见:ref:`west-building-config`。

设置构建系统目标
-------------------------------

要指定要运行的构建系统目标，请使用``--target``（或``-t``）。

例如，在带有QEMU的主机平台上，您可以使用``run``目标在一个命令中构建并运行模拟:zephyr:board:`qemu_x86 <qemu_x86>`板卡的:zephyr:code-sample:`hello_world`示例::

  west build -b qemu_x86 -t run samples/hello_world

另一个示例，使用``-t``列出所有构建系统目标::

  west build -t help

最后一个示例，使用``-t``运行``pristine``目标，该目标删除构建目录中的所有文件::

  west build -t pristine

.. _west-building-pristine:

全新构建
---------------

*pristine*构建目录本质上是一个新的构建目录。所有先前构建的副产物都已被移除。

要强制``west build``在重新运行CMake生成构建系统之前使构建目录保持原始状态，请使用``--pristine=always``（或``-p=always``）选项。

不提供值而给出``--pristine``或``-p``与为其提供值``always`具有相同的效果。例如，以下命令是等效的::

  west build -p -b reel_board samples/hello_world
  west build -p=always -b reel_board samples/hello_world

默认情况下，``west build``不会尝试检测是否需要使构建目录保持原始状态。如果您执行诸如尝试为不同的``--board`重用构建目录之类的操作，这可能会导致错误。

使用``--pristine=auto`使``west build`检测这些情况中的一些，并在尝试构建之前使构建目录保持原始状态。

.. tip::

   您可以运行``west config build.pristine always``来始终进行原始构建，或运行``west config build.pristine never`来禁用启发式算法。有关详细信息，请参见``west build``:ref:`west-building-config`。

.. _west-building-verbose:

详细构建
--------------

要打印由``west build`运行的CMake和编译器命令，请使用全局west详细选项``-v``::

  west -v build -b reel_board samples/hello_world

.. _west-building-generator:
.. _west-building-cmake-args:

一次性CMake参数
------------------------

要向由``west build`执行的CMake调用传递附加参数，请在命令行末尾的``--`之后传递它们。

.. important::

   像这样传递额外的CMake参数会强制``west build`重新运行CMake构建配置步骤，即使已经生成了构建系统。这将使增量构建变慢（但仍然比从头构建快得多）。

   使用``--``一次生成构建目录后，在后续运行中使用``west build -d
   <build-dir>``进行增量构建。

   或者，按照下一节所述使您的CMake参数永久化；这不会减慢增量构建。

例如，要使用Unix Makefiles CMake生成器而不是Ninja（这是
``west build``的默认生成器），请运行::

  west build -b reel_board -- -G'Unix Makefiles'

要使用Unix Makefiles并将`CMAKE_VERBOSE_MAKEFILE`_设置为``ON``::

  west build -b reel_board -- -G'Unix Makefiles' -DCMAKE_VERBOSE_MAKEFILE=ON

请注意，即使给出多个CMake参数，``--``也只出现一次。所有
``west build``命令行中``--``之后的参数都会传递给CMake。

.. _west-building-dtc-overlay-file:

要设置:ref:`DTC_OVERLAY_FILE <important-build-vars>`为
:file:`enable-modem.overlay`，将该文件作为
:ref:`设备树覆盖 <dt-guide>`使用::

  west build -b reel_board -- -DDTC_OVERLAY_FILE=enable-modem.overlay

要将:file:`file.conf` Kconfig片段合并到构建的
:file:`.config`中::

  west build -- -DEXTRA_CONF_FILE=file.conf

.. _west-building-cmake-config:

永久CMake参数
-------------------------

上一节描述了如何为单个``west build``命令添加CMake参数。如果你想保存``west build``在每次生成新构建系统时要使用的CMake参数，你应该使用``build.cmake-args``配置选项。每当``west build``运行CMake生成构建系统时，它会根据shell规则拆分此选项的值，并将结果包含在``cmake``命令行中。

请记住，默认情况下，``west build``**尝试避免在构建目录中已有构建系统时生成新的构建系统**。因此，你需要删除任何现有的构建目录或在设置``build.cmake-args``之后执行:ref:`原始构建<west-building-pristine>`以确保其生效。

例如，要始终启用:makevar:`CMAKE_EXPORT_COMPILE_COMMANDS`，你可以运行::

  west config build.cmake-args -- -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

（额外的``--``用于强制将命令的其余部分视为位置参数。如果没有它，:ref:`west config <west-config-cmd>`会将``-DVAR=VAL``语法视为其``-D``选项的用法。）

要启用:makevar:`CMAKE_VERBOSE_MAKEFILE`，使CMake始终生成详细的构建系统::

  west config build.cmake-args -- -DCMAKE_VERBOSE_MAKEFILE=ON

要在``build.cmake-args``中保存多个参数，请使用一个可以拆分为不同参数的字符串值（``west build``在内部使用Python函数`shlex.split()`_来拆分该值）。

.. _shlex.split(): https://docs.python.org/3/library/shlex.html#shlex.split

例如，要同时启用:makevar:`CMAKE_EXPORT_COMPILE_COMMANDS`和
:makevar:`CMAKE_VERBOSE_MAKEFILE`::

  west config build.cmake-args -- "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_VERBOSE_MAKEFILE=ON"

如果你想将CMake参数保存在单独的文件中，可以将CMake的``-C <initial-cache>``选项与``build.cmake-args`结合使用。例如，设置前一个示例中使用的选项的另一种方法是创建一个名为:file:`~/my-cache.cmake`的文件，内容如下：

.. code-block:: cmake

   set(CMAKE_EXPORT_COMPILE_COMMANDS ON CACHE BOOL "")
   set(CMAKE_VERBOSE_MAKEFILE ON CACHE BOOL "")

然后运行::

  west config build.cmake-args "-C ~/my-cache.cmake"

有关更多详细信息，请参见`cmake(1)手册页`_和`set()命令`_文档。

.. _cmake(1) manual page:
   https://cmake.org/cmake/help/latest/manual/cmake.1.html

.. _set() command:
   https://cmake.org/cmake/help/latest/command/set.html

构建工具参数
--------------------

使用``-o``向下层构建工具传递选项。

这适用于基于``ninja``（:ref:`默认值 <west-building-generator>`）
和``make``的构建系统。

例如，要将``-dexplain``传递给``ninja``::

  west build -o=-dexplain

另一个例子，要将``--keep-going``传递给``make``::

  west build -o=--keep-going

请注意，需要使用``-o=--foo``而不是``-o --foo``来防止``--foo``被``west build``选项处理。

构建并行性
-----------------

默认情况下，``ninja``使用所有核心进行构建，而``make``只使用一个核心。你可以使用两个工具都支持的``-j``选项显式控制这一点。

例如，使用4个核心进行构建::

  west build -o=-j4

前一节中进一步描述了``-o``选项。

构建单个域
---------------------

在使用:zephyr:code-sample:`hello_world`和`MCUboot`_的多域构建中，你可以使用``--domain hello_world``仅构建此域::

  west build --sysbuild --domain hello_world

``--domain``参数可以与``--target``参数结合使用来构建特定目标，例如::

  west build --sysbuild --domain hello_world --target help

使用代码片段
-------------

参见:ref:`using-snippets`。

.. _west-building-config:

配置选项
=====================

你可以使用这些选项:ref:`配置<west-config-cmd>` ``west build``。

.. NOTE: docs authors: keep this table sorted alphabetically

.. list-table::
   :widths: 10 30
   :header-rows: 1

   * - 选项
     - 描述
   * - ``build.board``
     - 字符串。如果提供，这是当未给出``--board``且``BOARD``
       在环境中未设置时由:ref:`west build
       <west-building>`使用的板卡。
   * - ``build.board_warn``
     - 布尔值，默认为``true``。如果为``false``，当
       ``west build``无法确定目标板卡时禁用警告。
   * - ``build.cmake-args``
     - 字符串。如果存在，该值将根据shell规则拆分，并
       在生成新构建系统时传递给CMake。参见
       :ref:`west-building-cmake-config`。
   * - ``build.dir-fmt``
     - 字符串，默认为``build``。构建目录格式字符串，west
       需要创建或定位构建目录时使用。当前可用的参数有：

         - ``west_topdir``: west工作区的绝对路径，由
           ``west_topdir``命令返回
         - ``board``: 板卡名称
         - ``source_dir``: CMake源目录的路径，相对于
           当前工作目录。如果当前工作目录在源目录内，
           这是一个空字符串。如果没有指定源目录，它默认为当前工作目录。
           例如，如果从``<west_topdir>/app1``运行``west build ../app``，
           ``source_dir``解析为``../app``（这是相对于
           当前工作目录的路径）。
         - ``source_dir_workspace``: 源目录的路径，相对于
           ``west_topdir``（如果它在工作区内）。否则，它相对于
           文件系统根目录（Unix上为``/``，Windows上为
           ``C:/``）。
           例如，如果从``<west_topdir>/app1``运行``west build ../app``，
           ``source_dir``解析为``app``（这是相对于
           west工作区目录的路径）。
         - ``app``: 源目录的名称。
   * - ``build.generator``
     - 字符串，默认为``Ninja``。用于创建构建系统的
       `CMake Generator`_。（要为单个构建设置生成器，请参见
       :ref:`上述示例 <west-building-generator>`）
   * - ``build.guess-dir``
     - 字符串，指示west是否尝试猜测当使用``build.dir-fmt``且
       没有足够信息解析构建目录名称时要使用的构建目录。可以采用这些值：

         - ``never``（默认）：从不尝试猜测，而是退出并
           要求用户使用``-d``提供构建目录。
         - ``runners``:在使用任何'runner'命令时尝试猜测目录。
           这些通常是调用外部工具的所有命令，如``flash``和``debug``。
   * - ``build.pristine``
     - 字符串。控制``west build``在构建前可能如何清理构建目录。可以采用以下值：

         - ``never``（默认）：从不自动使构建目录保持原始状态。
         - ``auto``:  如果存在构建系统且否则构建将失败（例如
           用户指定了与之前用于创建构建目录的板卡或应用程序不同
           的板卡或应用程序），``west build``将在构建前自动使
           构建目录保持原始状态。
         - ``always``: 如果存在构建系统，始终在构建前使构建目录保持原始状态。
   * - ``build.sysbuild``
     - 布尔值，默认为``false``。如果为``true``，使用sysbuild
       基础架构构建应用程序。

.. _west-flashing:

烧录: ``west flash``
************************

.. tip:: 运行``west flash -h``获取额外帮助。

基础知识
======

从Zephyr构建目录，重新构建二进制文件并将其烧录到您的板卡::

  west flash

不带选项时，行为与``ninja flash``（或``make flash`等）相同。

要指定构建目录，请使用``--build-dir``（或``-d`）::

  west flash --build-dir path/to/build/directory

如果您不指定构建目录，``west flash``会在:file:`build`中搜索，然后搜索当前工作目录。如果您设置了``build.dir-fmt``配置选项（请参见:ref:`west-building-dirs`），则``west flash``会在那里而不是:file:`build`中搜索。

选择运行器
=================

如果您的板卡的Zephyr集成支持使用多个程序进行烧录，您可以使用``--runner``（或``-r`）选项指定使用哪一个。例如，如果West默认使用``nrfjprog`烧录您的板卡，但它也支持JLink，您可以使用以下方法覆盖默认设置::

  west flash --runner jlink

您可以在构建时通过使用``BOARD_FLASH_RUNNER` CMake变量覆盖默认烧录运行器，使用``BOARD_DEBUG_RUNNER`覆盖调试运行器。

例如::

  # 将默认运行器设置为"jlink"，覆盖板卡的通常默认设置。
  west build [...] -- -DBOARD_FLASH_RUNNER=jlink

有关设置CMake参数的更多信息，请参见:ref:`west-building-cmake-args`和:ref:`west-building-cmake-config`。

有关``runner`的更多信息，请参见下面的:ref:`west-runner`
库。使用``west flash -H`可以获取支持烧录的运行器列表；如果从构建目录运行或使用``--build-dir`，这将打印有关您板卡可用运行器的其他信息。

配置覆盖
=======================

CMake缓存包含West在烧录时使用的默认值，如板卡目录在文件系统上的位置、以多种格式烧录的zephyr二进制文件的路径等。您可以通过附加选项在运行时覆盖任何这些配置。

例如，要覆盖包含要烧录的Zephyr镜像的HEX文件（假设您的运行器期望HEX文件），但将其他烧录配置保持为默认值::

  west flash --hex-file path/to/some/other.hex

``west flash -h``输出包括所有运行器支持的覆盖项的完整列表。

特定于运行器的覆盖
=========================

每个运行器可能支持与烧录相关的附加选项。例如，某些运行器支持``--erase`标志，在烧录Zephyr镜像之前对您板卡上的闪存存储进行大块擦除。

要查看您板卡支持的运行器的所有可用选项及其使用信息，请使用``--context``（或``-H`）::

  west flash --context

.. important::

   注意短选项名称中的大写H。这将重新运行构建以确保显示的信息是最新的！

当在构建目录外运行West时，``west flash -H`仅打印运行器列表。您可以使用``west flash -H -r <runner-name>`打印该运行器支持的选项的使用信息。

例如，要打印关于``jlink`运行器的使用信息::

  west flash -H -r jlink

.. _west-multi-domain-flashing:

多域烧录
=====================

当检测到:ref:`west-multi-domain-builds`文件夹时，``west flash``将按sysbuild定义的顺序烧录所有域。

在多域项目中，可以通过使用``--domain`来仅烧录来自单个域的镜像。

例如，在使用:zephyr:code-sample:`hello_world`和`MCUboot`_的多域构建中，您可以使用``--domain hello_world`域仅烧录此域的镜像::

  west flash --domain hello_world

.. _west-debugging:

调试: ``west debug``、``west debugserver``
***********************************************

.. tip::

   运行``west debug -h``或``west debugserver -h``获取额外帮助。

基础知识
======

从Zephyr构建目录，要将调试器连接到您的板卡并打开调试控制台（例如GDB会话）::

  west debug

要将调试器连接到您的板卡并打开本地网络端口，您可以将调试器连接到（例如IDE调试器）::

  west debugserver

不带选项时，行为与``ninja debug``和``ninja debugserver``（或``make debug`等）相同。

要指定构建目录，请使用``--build-dir``（或``-d`）::

  west debug --build-dir path/to/build/directory
  west debugserver --build-dir path/to/build/directory

如果您不指定构建目录，这些命令会在:file:`build`中搜索，然后搜索当前工作目录。如果您设置了``build.dir-fmt``配置选项（请参见:ref:`west-building-dirs`），则``west debug`会在那里而不是:file:`build`中搜索。

选择运行器
=================

如果您的板卡的Zephyr集成支持使用多个程序进行调试，您可以使用``--runner``（或``-r`）选项指定使用哪一个。例如，如果West默认使用``pyocd-gdbserver`调试您的板卡，但它也支持JLink，您可以使用以下方法覆盖默认设置::

  west debug --runner jlink
  west debugserver --runner jlink

有关West使用的``runner`库的更多信息，请参见下面的:ref:`west-runner`。使用``west debug -H`可以获取支持调试的运行器列表；如果从构建目录运行或使用``--build-dir`，这将打印有关您板卡可用运行器的其他信息。

配置覆盖
=======================

CMake缓存包含West用于调试的默认值，如板卡目录在文件系统上的位置、包含符号表的zephyr二进制文件的路径等。您可以通过附加选项在运行时覆盖任何这些配置。

例如，要覆盖包含Zephyr二进制文件和符号表的ELF文件（假设您的运行器期望ELF文件），但将其他调试配置保持为默认值::

  west debug --elf-file path/to/some/other.elf
  west debugserver --elf-file path/to/some/other.elf

``west debug -h``输出包括所有运行器支持的覆盖项的完整列表。

特定于运行器的覆盖
=========================

每个运行器可能支持与调试相关的附加选项。例如，某些运行器支持允许您设置调试服务器使用的网络端口的标志。

要查看您板卡支持的运行器的所有可用选项及其使用信息，请使用``--context``（或``-H`）::

  west debug --context

（命令``west debugserver --context`将打印相同的输出。）

.. important::

   注意短选项名称中的大写H。这将重新运行构建以确保显示的信息是最新的！

当在构建目录外运行West时，``west debug -H`仅打印运行器列表。您可以使用``west debug -H -r <runner-name>`打印该运行器支持的选项的使用信息。

例如，要打印关于``jlink`运行器的使用信息::

  west debug -H -r jlink

.. _west-multi-domain-debugging:

多域调试
=====================

``west debug``一次只能调试一个域。当检测到:ref:`west-multi-domain-builds`文件夹时，``west debug`将调试sysbuild指定的``default`域。

默认域将是作为源目录给出的应用程序。请参见以下示例::

  west build --sysbuild path/to/source/directory

例如，当使用sysbuild构建带有`MCUboot`_的``hello_world``时，``hello_world``成为默认域::

  west build --sysbuild samples/hello_world

因此，要调试``hello_world``您可以执行::

  west debug

或::

  west debug --domain hello_world

如果你希望调试MCUboot，你必须显式指定MCUboot作为要调试的域::

  west debug --domain mcuboot

.. _west-runner:

烧录和调试运行器
***********************

烧录和调试命令使用围绕各种:ref:`flash-debug-host-tools`的Python包装器。这些包装器都在:zephyr_file:`scripts/west_commands/runners`的Python库中定义。每个包装器称为*运行器*。运行器可以烧录和/或调试Zephyr程序。

该库中的核心抽象是``ZephyrBinaryRunner``，一个表示运行器的抽象类。可用运行器的集合由``ZephyrBinaryRunner`的导入子类决定。``ZephyrBinaryRunner``在``runners.core``模块中可用；单独的运行器实现在其他子模块中，如``runners.nrfjprog``、``runners.openocd`等。

运行Robot框架测试: ``west robot``
*********************************************

.. tip:: 运行``west robot -h``获取额外帮助。

基础知识
======

目前该命令仅支持一个使用``renode-test``的运行器（本质上是用于在Renode中运行Robot测试的包装器），但可以通过添加其他运行器轻松扩展。

从Zephyr构建目录，要运行Robot测试套件::

  west robot --runner=renode-robot --testsuite path/to/testsuite.robot

这将运行testsuite.robot中的所有测试，并打印Robot框架提供的输出。

要向Renode传递附加参数，请使用``--renode-robot-args``开关。
例如，除了Robot框架的输出外，还要显示Renode日志:

  west robot --runner=renode-robot --testsuite path/to/testsuite.robot --renode-robot-arg="--show-log"

特定于运行器的覆盖
=========================

要查看您板卡支持的Robot运行器的所有可用选项及其使用信息，请使用``--context``（或``-H`）::


  west robot --runner=renode-robot --context


要查看"renode-test"运行器支持的所有可用选项，请使用::

  west robot --runner=renode-robot --renode-robot-help

使用以下命令仿真板卡: ``west simulate``
******************************************

基础知识
======

目前该命令仅支持一个使用Renode的运行器，但可以通过添加其他运行器轻松扩展。

从Zephyr构建目录，要运行构建的二进制文件::

  west simulate --runner=renode

这将启动Renode并根据当前平台的默认``.resc``脚本配置仿真，默认加载zephyr.elf文件。然后可以通过在Renode的Monitor中输入"start"或"s"来启动仿真。这也可以通过向Renode传递运行器提供的参数来实现:

  west simulate --runner=renode --renode-command start

要向Renode本身传递参数，例如在控制台模式下启动Renode而不是单独的窗口:

  west simulate --runner=renode --renode-arg="--console"

从那时起，Renode可以在控制台和窗口模式下正常使用。
有关使用Renode的详细信息，请参见`Renode - 文档`_。

.. _Renode - documentation:
   https://docs.renode.io

特定于运行器的覆盖
=========================

要查看运行器支持的所有可用选项及其使用信息，请使用``--context``（或``-H`）::

  west simulate --runner=renode --context

要查看Renode支持的所有可用选项，请使用::

  west simulate --runner=renode --renode-help

树外运行器
*******************

:ref:`Zephyr模块<modules>`可以通过在:ref:`module.yml <modules-runners>`中添加python文件来发现外部运行器。通过从``ZephyrBinaryRunner``继承并实现所有抽象方法来创建外部运行器类。

.. note::

   对自定义树外运行器的支持使``runners.core`模块成为公共API的一部分，需要进行
   :ref:`弃用过程<breaking_api_changes>`的向后不兼容更改。

黑客技术
*******

本节记录烧录和调试命令使用的``runners.core``模块。这是用于实现这些功能支持的核心抽象。

开发人员可以通过实现附加运行器来添加对Zephyr程序进行烧录和调试的新方法的支持。要将此支持引入上游Zephyr，应将运行器添加到新的或现有的``runners``模块中，并从:file:`runners/__init__.py`导入。

.. note::

   :zephyr_file:`scripts/west_commands/tests`中的测试用例为运行器包和单独的运行器类添加了单元测试覆盖率。

   请尝试在添加新运行器时添加测试。请注意，如果您
   的更改破坏了现有测试用例，上游pull
   请求上的CI测试将失败。

.. automodule:: runners.core
   :members:

手动操作
****************

如果你更喜欢不使用West来烧录或调试你的板卡，只需检查构建目录中构建系统输出的二进制文件。这些文件将根据你板卡的构建系统集成命名为类似``zephyr/zephyr.elf``、``zephyr/zephyr.hex``等。这些二进制文件可以使用你选择的替代工具烧录到板卡上，或根据需要用于调试，例如作为符号表的来源。

默认情况下，这些West命令在烧录和调试之前重新构建二进制文件。当然，这也可以使用Zephyr构建系统提供的常规目标来完成（实际上，这就是这些命令的执行方式）。

.. _cmake(1):
   https://cmake.org/cmake/help/latest/manual/cmake.1.html

.. _CMAKE_VERBOSE_MAKEFILE:
   https://cmake.org/cmake/help/latest/variable/CMAKE_VERBOSE_MAKEFILE.html

.. _CMake Generator:
   https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html

.. _MCUboot: https://mcuboot.com/
