.. _custom_cmake_toolchains:

自定义 CMake 工具链
###################

要使用外部 CMake 文件中定义的自定义工具链,:ref:`设置这些环境变量 <env_vars>`:

- 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为您的工具链名称
- 将 ``TOOLCHAIN_ROOT`` 设置为包含您的工具链 CMake 配置文件的目录路径。

然后,Zephyr 将包含位于 :file:`TOOLCHAIN_ROOT` 目录中的工具链 cmake 文件:

- :file:`cmake/toolchain/<toolchain name>/generic.cmake`: 为"通用"使用配置工具链,这主要意味着在生成的 :ref:`devicetree` 文件上运行 C 预处理器。
- :file:`cmake/toolchain/<toolchain name>/target.cmake`: 为"目标"使用配置工具链,即构建 Zephyr 和您的应用程序的源代码。

这里 <toolchain name> 与 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 中提供的名称相同。
有关 :file:`generic.cmake` 和 :file:`target.cmake` 文件应包含的内容的更多详细信息,请参阅 zephyr 文件 :zephyr_file:`cmake/modules/FindHostTools.cmake` 和 :zephyr_file:`cmake/modules/FindTargetTools.cmake`。

您还可以在为 Zephyr 应用程序生成构建系统时将 ``ZEPHYR_TOOLCHAIN_VARIANT`` 和 ``TOOLCHAIN_ROOT`` 设置为 CMake 变量,如下所示:

.. code-block:: console

   west build ... -- -DZEPHYR_TOOLCHAIN_VARIANT=... -DTOOLCHAIN_ROOT=...

.. code-block:: console

   cmake -DZEPHYR_TOOLCHAIN_VARIANT=... -DTOOLCHAIN_ROOT=...

如果这样做,``-C <initial-cache>`` `cmake option`_ 可能会有用。如果您将 :makevar:`ZEPHYR_TOOLCHAIN_VARIANT`、:makevar:`TOOLCHAIN_ROOT` 和其他设置保存在名为 :file:`my-toolchain.cmake` 的文件中,则可以调用 cmake 为 ``cmake -C my-toolchain.cmake ...`` 以节省输入。

Zephyr 包含 :file:`include/toolchain.h`,它再次基于编译器标识符(例如 ``__llvm__`` 或 ``__GNUC__``)包含特定于工具链的头文件。
一些自定义编译器将自己标识为它们所基于的编译器,例如 ``llvm``,然后包含 :file:`toolchain/llvm.h`。
但是,这个包含的文件可能不适合自定义工具链。为了解决这个问题,从而包含 :file:`include/other.h`,请将 set(TOOLCHAIN_USE_CUSTOM 1) cmake 行添加到位于 :file:`<TOOLCHAIN_ROOT>/cmake/toolchain/<toolchain name>/` 下的 generic.cmake 和/或 target.cmake 文件中。

当设置 :makevar:`TOOLCHAIN_USE_CUSTOM` 时,:file:`other.h` 必须在树外可用,并且它必须为自定义工具链包含正确的头文件。
:file:`other.h` 头文件的一个好位置是在 ``TOOLCHAIN_ROOT`` 中指定的目录下的目录,如 :file:`include/toolchain`。
要在 zephyr 的构建中包含工具链头文件,可以将 :makevar:`USERINCLUDE` 设置为指向 include 目录,如下所示:

.. code-block:: console

   west build -- -DZEPHYR_TOOLCHAIN_VARIANT=... -DTOOLCHAIN_ROOT=... -DUSERINCLUDE=...

.. _cmake option:
   https://cmake.org/cmake/help/latest/manual/cmake.1.html#options
