.. _no-west:

不使用 west 的情况下使用 Zephyr
###############################

此页面提供了有关在不使用 west 的情况下使用 Zephyr 的信息。
由于涉及的额外工作，不建议初学者使用。特别是，你必须"手动"完成这些功能的工作：

- 克隆 Zephyr 使用的其他源代码仓库（除了主 zephyr 仓库）并保持它们是最新的
- 向 Zephyr 构建系统指定这些仓库的位置
- 在不理解相关主机工具的详细使用的情况下刷新和调试

.. note::

   如果你之前安装了 west 并想停止使用它，请先卸载它：

   .. code-block:: console

      pip3 uninstall west

   否则，Zephyr 的构建系统会找到它并可能尝试使用它。

获取源代码
---------

除了下载 zephyr 源代码仓库本身外，你还需要手动克隆该仓库内的
:term:`west manifest` 文件中列出的其他项目。

.. code-block:: console

   mkdir zephyrproject
   cd zephyrproject
   git clone https://github.com/zephyrproject-rtos/zephyr
   # 克隆 zephyr/west.yml 中列出的其他仓库，
   # 并检查指定的修订版本。

当你在 zephyr 仓库中拉取更改时，你还需要维护这些其他仓库，
根据需要添加新的仓库并将现有的更新到最新的修订版本。

构建应用程序
-----------

如果你手动指定任何模块，你可以直接使用 CMake 和 Ninja（或 make）
来构建 Zephyr 应用程序，而不需要安装 west。

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :tool: cmake
   :goals: build
   :gen-args: -DZEPHYR_MODULES=module1;module2;...
   :compact:

安装 west 后，Zephyr 构建系统将使用它来设置 :ref:`ZEPHYR_MODULES <important-build-vars>`。

如果你没有安装 west 且你的应用程序不需要任何这些仓库，构建仍然会工作。

如果你没有安装 west 且你的应用程序*确实*需要这些仓库之一，
你必须自己设置 :makevar:`ZEPHYR_MODULES`，如上所示。

有关更多详细信息，请参见 :ref:`modules`。

类似地，如果你的应用程序需要二进制 blob 且你不使用 west，
你将需要下载这些 blob 并将其放置在正确的位置，而不是使用 ``west blobs``。
有关更多详细信息，请参见 :ref:`bin-blobs`。

刷新和调试
---------

运行构建系统目标（如 ``ninja flash``、``ninja debug`` 等）
只是对相应 :ref:`west 命令 <west-build-flash-debug>` 的调用。
例如，``ninja flash`` 调用 ``west flash`` [#wbninja]_。
如果你的系统上没有安装 west，运行这些目标将失败。
当然，你仍然可以使用任何 :ref:`flash-debug-host-tools`
对你的开发板有效的方式进行刷新和调试（这些 west 命令都是包装的）。

如果你想使用这些构建系统目标但不想在你的系统上使用 ``pip`` 安装 west，
可以通过手动创建 :term:`west workspace` 来实现：

.. code-block:: console

   # 如果还没有在 zephyrproject 中，进入 zephyrproject
   git clone https://github.com/zephyrproject-rtos/west.git .west/west

然后创建一个文件 :file:`.west/config`，内容如下：

.. code-block:: none

   [manifest]
   path = zephyr

   [zephyr]
   base = zephyr

之后，为了让 ``ninja`` 能够调用 ``west`` 来刷新和调试，
你必须指定 west 目录。这可以通过设置环境变量 ``WEST_DIR``
指向 :file:`zephyrproject/.west/west` 在运行 CMake 来设置构建目录之前来完成。

.. rubric:: 脚注

.. [#wbninja]

   注意 ``west build`` 调用 ``ninja`` 以及其他工具。
   但默认情况下不涉及 ``west`` 或 ``ninja`` 的递归调用，
   因为 ``west build`` 不调用 ``ninja flash``、``debug`` 等。
   唯一的例外是你特别运行其中一个构建系统目标，
   使用 ``west build -t flash`` 这样的命令行。
   在这种情况下，west 运行两次：一次用于 ``west build``，
   在子进程中再次用于 ``west flash``。
   即使在这种情况下，``ninja`` 也只运行一次，
   作为 ``ninja flash``。这是因为这些构建系统目标依赖于
   Zephyr 应用程序的最新构建，所以在 ``west flash`` 运行之前进行编译。
