构建扩展 (Building extensions)
###############################

LLEXT 子系统允许创建可加载到正在运行的 Zephyr 应用程序中的扩展。在构建这些扩展时,访问主 Zephyr 应用程序使用的头文件和编译器标志通常非常有用。(The LLEXT subsystem allows for the creation of extensions that can be loaded into a running Zephyr application. When building these extensions, it's very often useful to have access to the headers and compiler flags used by the main Zephyr application.)

实现这一目标的最简单方法是将扩展作为 Zephyr 应用程序的一部分构建,使用 `原生 Zephyr CMake 功能 <llext_build_native_>`_。这将产生一个同时提供主 Zephyr 应用程序和扩展的单个构建,它们都将自动使用相同的参数构建。(The easiest path to achieve this is to build the extension as part of the Zephyr application, using the `native Zephyr CMake features <llext_build_native_>`_. This will result in a single build providing both the main Zephyr application and the extension(s), which will all automatically be built with the same parameters.)

在某些情况下,涉及完整的 Zephyr 构建系统可能不可行或不方便;也许扩展是使用不同的编译器套件构建的,或者作为完全不同项目的一部分。在这种情况下,扩展开发人员需要导出主 Zephyr 应用程序使用的头文件和编译器标志。这可以使用 `LLEXT 扩展开发套件 <llext_build_edk_>`_ 来完成。(In some cases, involving the full Zephyr build system may not be feasible or convenient; maybe the extension is built using a different compiler suite or as part of a different project altogether. In this case, the extension developer needs to export the headers and compiler flags used by the main Zephyr application. This can be done using the `LLEXT Extension Development Kit <llext_build_edk_>`_.)

.. _llext_build_native:

使用 Zephyr CMake 功能 (Using the Zephyr CMake features)
*********************************************************

Zephyr 构建系统提供了一组功能,可用于将扩展作为 Zephyr 应用程序的一部分构建。这是构建扩展的最简单方法,因为它只需要对应用程序构建系统进行最少的添加。(The Zephyr build system provides a set of features that can be used to build extensions as part of the Zephyr application. This is the simplest way to build extensions, as it requires minimal additions to an application build system.)

构建扩展 (Building the extension)
----------------------------------

可以通过调用 ``add_llext_target`` 函数在应用程序的 ``CMakeLists.txt`` 中定义扩展,提供目标名称、输出和源文件。用法类似于标准的 ``add_custom_target`` CMake 函数:(An extension can be defined in the app's ``CMakeLists.txt`` by invoking the ``add_llext_target`` function, providing the target name, the output and the source files. Usage is similar to the standard ``add_custom_target`` CMake function:)

.. code-block:: cmake

   add_llext_target(
       <target_name>
       OUTPUT <ext_file.llext>
       SOURCES <src1> [<src2>...]
   )

其中:(where:)

- ``<target_name>`` 是将导致创建 LLEXT 二进制文件的最终 CMake 目标的名称;(is the name of the final CMake target that will result in the LLEXT binary being created;)
- ``<ext_file.llext>`` 是将包含打包扩展的输出文件的名称;(is the name of the output file that will contain the packaged extension;)
- ``<src1> [<src2>...]`` 是将被编译以创建扩展的源文件列表。(is the list of source files that will be compiled to create the extension.)

扩展构建过程的确切步骤取决于当前选择的 :ref:`ELF 对象格式 <llext_kconfig_type>`。(The exact steps of the extension building process depend on the currently selected :ref:`ELF object format <llext_kconfig_type>`.)

定义了 ``<target_name>`` 的以下自定义属性,可以使用 ``get_target_property()`` CMake 函数检索:(The following custom properties of ``<target_name>`` are defined and can be retrieved using the ``get_target_property()`` CMake function:)

``lib_target``

    源编译和/或链接步骤的目标名称。(Target name for the source compilation and/or link step.)

``lib_output``

    编译和/或链接步骤产生的二进制文件。(The binary file resulting from compilation and/or linking steps.)

``pkg_input``

     用作打包步骤输入的文件。(The file to be used as input for the packaging step.)

``pkg_output``

    最终扩展文件名。(The final extension file name.)


Tweaking the build process
--------------------------

The following CMake functions can be used to modify the build system behavior
during the extension build process to a fine degree. Each of the below
functions takes the LLEXT target name as its first argument; it is otherwise
functionally equivalent to the common Zephyr ``target_*`` version.

* ``llext_compile_definitions``
* ``llext_compile_features``
* ``llext_compile_options``
* ``llext_include_directories``
* ``llext_link_options``


自定义构建步骤 (Custom build steps)
------------------------------------

``add_llext_command`` CMake 函数可用于添加将在扩展构建过程中执行的自定义构建步骤。该命令将在指定的构建步骤运行,并可以引用目标的属性以获取特定于构建的详细信息。(The ``add_llext_command`` CMake function can be used to add custom build steps that will be executed during the extension build process. The command will be run at the specified build step and can refer to the properties of the target for build-specific details.)

函数签名为:(The function signature is:)

.. code-block:: cmake

   add_llext_command(
       TARGET <target_name>
       [PRE_BUILD | POST_BUILD | POST_PKG]
       COMMAND <command> [args...]
   )

不同的构建步骤是:(The different build steps are:)

``PRE_BUILD``

    在扩展代码链接之前,如果架构使用动态库。此步骤可以访问 ``lib_target`` 及其自己的属性。(Before the extension code is linked, if the architecture uses dynamic libraries. This step can access ``lib_target`` and its own properties.)

``POST_BUILD``

    在扩展代码构建之后,但在将其打包到 ``.llext`` 文件之前。此步骤应通过读取 :file:`lib_output` 的内容来创建 :file:`pkg_input` 文件。(After the extension code is built, but before packaging it in an ``.llext`` file. This step is expected to create a :file:`pkg_input` file by reading the contents of :file:`lib_output`.)

``POST_PKG``

    在创建扩展输出文件之后。该命令可以对最终的 llext 文件 :file:`pkg_output` 进行操作。(After the extension output file has been created. The command can operate on the final llext file :file:`pkg_output`.)

``COMMAND`` 之后的任何内容都将原样传递给 ``add_custom_command()``(包括多个命令和其他选项)。(Anything else after ``COMMAND`` will be passed to ``add_custom_command()`` as-is (including multiple commands and other options).)


.. _llext_build_edk:

LLEXT 扩展开发套件 (EDK) (LLEXT Extension Development Kit (EDK))
******************************************************************

当将扩展作为独立项目构建时,在主 Zephyr 构建系统之外,访问主 Zephyr 应用程序使用的相同生成的头文件集和编译器标志集非常重要,因为它们会直接影响 Zephyr 头文件的解释方式以及扩展的一般编译方式。(When building extensions as a standalone project, outside of the main Zephyr build system, it's important to have access to the same set of generated headers and compiler flags used by the main Zephyr application, since they have a direct impact on how Zephyr headers are interpreted and the extension is compiled in general.)

这可以通过要求 Zephyr 从主 Zephyr 应用程序的构建工件生成扩展开发套件(EDK)来实现,方法是运行以下使用 ``llext-edk`` 目标的命令:(This can be achieved by asking Zephyr to generate an Extension Development Kit (EDK) from the build artifacts of the main Zephyr application, by running the following command which uses the ``llext-edk`` target:)

.. code-block:: shell

    west build -t llext-edk

生成的 EDK 可以在 ``zephyr`` 目录下的构建目录中找到。它是一个 tarball,包含构建扩展所需的头文件和编译标志。然后扩展开发人员可以在其构建系统中包含头文件并使用编译标志来构建扩展。(The generated EDK can be found in the build directory under the ``zephyr`` directory. It's a tarball that contains the headers and compile flags needed to build extensions. The extension developer can then include the headers and use the compile flags in their build system to build the extension.)

EDK 定义文件 (EDK definition files)
------------------------------------

EDK 包含几个方便的文件,这些文件定义了一组变量,这些变量包含项目所需的编译标志以及其他与构建相关的信息(启用时)。信息当前以以下格式导出:(The EDK includes several convenience files which define a set of variables that contain the compile flags needed by the project, as well as other build-related information, when enabled. The information is currently exported in the following formats:)

- ``Makefile.cflags``,用于基于 Makefile 的项目;(for Makefile-based projects;)
- ``cmake.cflags``,用于基于 CMake 的项目。(for CMake-based projects.)

头文件和标志的路径以 EDK 根目录为前缀。这是为 CMake 项目自动从 ``CMAKE_CURRENT_LIST_DIR`` 获得的;其他格式引用 ``LLEXT_EDK_INSTALL_DIR`` 变量,在包含生成的文件之前,用户必须使用安装 EDK 的路径设置该变量。(Paths to the headers and flags are prefixed by the EDK root directory. This is automatically obtained for CMake projects from ``CMAKE_CURRENT_LIST_DIR``; other formats refer to an ``LLEXT_EDK_INSTALL_DIR`` variable, which must be set by the user with the path where the EDK is installed before including the generated file.)

.. note::
   可以使用 :kconfig:option:`CONFIG_LLEXT_EDK_NAME` 选项更改变量名称中的 ``LLEXT_EDK`` 前缀。(The ``LLEXT_EDK`` prefix in the variable name may be changed with the :kconfig:option:`CONFIG_LLEXT_EDK_NAME` option.)

编译标志 (Compile flags)
-------------------------

构建扩展所需的标志的完整列表由 ``LLEXT_CFLAGS`` 提供。还提供了一组更细粒度的标志,可用于支持不同的用例,例如为单元测试构建模拟时:(The full list of flags needed to build an extension is provided by ``LLEXT_CFLAGS``. Also provided is a more granular set of flags that can be used in support of different use cases, such as when building mocks for unit tests:)

``LLEXT_INCLUDE_CFLAGS``

        编译器标志,用于将包含非自动生成头文件的目录添加到编译器的包含搜索路径中。(Compiler flags to add directories containing non-autogenerated headers to the compiler's include search paths.)

``LLEXT_GENERATED_INCLUDE_CFLAGS``

        编译器标志,用于将包含自动生成头文件的目录添加到编译器的包含搜索路径中。(Compiler flags to add directories containing autogenerated headers to the compiler's include search paths.)

``LLEXT_ALL_INCLUDE_CFLAGS``

        编译器标志,用于将构建中使用的所有包含头文件的目录添加到编译器的包含搜索路径中。这是 ``LLEXT_INCLUDE_CFLAGS`` 和 ``LLEXT_GENERATED_INCLUDE_CFLAGS`` 的组合。(Compiler flags to add all directories containing headers used in the build to the compiler's include search paths. This is a combination of ``LLEXT_INCLUDE_CFLAGS`` and ``LLEXT_GENERATED_INCLUDE_CFLAGS``.)

``LLEXT_GENERATED_IMACROS_CFLAGS``

        必须通过 ``-imacros`` 包含在构建中的自动生成头文件的编译器标志。(Compiler flags for autogenerated headers that must be included in the build via ``-imacros``.)

``LLEXT_BASE_CFLAGS``

        控制目标 CPU 代码生成的其他编译器标志。这些标志都不包含在上述列表中。(Other compiler flags that control code generation for the target CPU. None of these flags are included in the above lists.)

``LLEXT_CFLAGS``

        构建扩展所需的所有标志。这是 ``LLEXT_ALL_INCLUDE_CFLAGS``、``LLEXT_GENERATED_IMACROS_CFLAGS`` 和 ``LLEXT_BASE_CFLAGS`` 的组合。(All flags required to build an extension. This is a combination of ``LLEXT_ALL_INCLUDE_CFLAGS``, ``LLEXT_GENERATED_IMACROS_CFLAGS`` and ``LLEXT_BASE_CFLAGS``.)

目标信息 (Target information)
------------------------------

EDK 包含标识当前 Zephyr 构建目标的信息。当前定义以下变量,并镜像 Zephyr 构建系统中可用的信息:(The EDK includes information that identifies the target of the current Zephyr build. The following variables are currently defined and mirror the information available in the Zephyr build system:)

``LLEXT_EDK_BOARD_NAME``
    Zephyr 构建中使用的板名称。(The board name used in the Zephyr build.)

``LLEXT_EDK_BOARD_QUALIFIERS``
    Zephyr 构建中使用的板限定符(如果提供)。(The board qualifiers, if provided, used in the Zephyr build.)

``LLEXT_EDK_BOARD_REVISION``
    Zephyr 构建中使用的板修订版本(如果提供)。(The board revision, if provided, used in the Zephyr build.)

``LLEXT_EDK_BOARD_TARGET``
    Zephyr 构建中使用的完全限定板目标。(The fully qualified board target used in the Zephyr build.)

.. note::
   可以使用 :kconfig:option:`CONFIG_LLEXT_EDK_NAME` 选项更改变量名称中的 ``LLEXT_EDK`` 前缀。(The ``LLEXT_EDK`` prefix in the variable names may be changed with the :kconfig:option:`CONFIG_LLEXT_EDK_NAME` option.)

.. _llext_kconfig_edk:

LLEXT EDK Kconfig 选项 (LLEXT EDK Kconfig options)
----------------------------------------------------

LLEXT EDK 可以使用以下 Kconfig 选项进行配置:(The LLEXT EDK can be configured using the following Kconfig options:)

:kconfig:option:`CONFIG_LLEXT_EDK_NAME`
    生成的 EDK tarball 的名称。这也用作 EDK 文件中定义的多个变量的前缀。(The name of the generated EDK tarball. This is also used as the prefix for several variables defined in the EDK files.)

:kconfig:option:`CONFIG_LLEXT_EDK_USERSPACE_ONLY`
    如果设置,EDK 将包含不包含将系统调用路由到内核的代码的头文件。这在构建将专门在用户模式下运行的扩展时非常有用。(If set, the EDK will include headers that do not contain code to route syscalls to the kernel. This is useful when building extensions that will run exclusively in user mode.)

EDK 示例 (EDK Sample)
----------------------

参考 :zephyr:code-sample:`llext-edk` 以获取有关如何使用 LLEXT EDK 的示例。(Refer to :zephyr:code-sample:`llext-edk` for an example of how to use the LLEXT EDK.)
