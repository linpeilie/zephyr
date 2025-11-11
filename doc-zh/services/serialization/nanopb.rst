.. _nanopb_reference:

Nanopb
######

`Nanopb <https://jpa.kapsi.fi/nanopb/>`_ 是 Google 的 `Protocol Buffers <https://protobuf.dev/>`_ 的 C 实现。(`Nanopb <https://jpa.kapsi.fi/nanopb/>`_ is a C implementation of Google's `Protocol Buffers <https://protobuf.dev/>`_.)

要求 (Requirements)
*******************

Nanopb 使用协议缓冲区编译器来生成源文件和头文件,请确保安装并可用 ``protoc`` 可执行文件。(Nanopb uses the protocol buffer compiler to generate source and header files, make sure the ``protoc`` executable is installed and available.)

.. tabs::

   .. group-tab:: Ubuntu

      使用 ``apt`` 安装依赖项:(Use ``apt`` to install dependency:)

         .. code-block:: shell

            sudo apt install protobuf-compiler

   .. group-tab:: macOS

      使用 ``brew`` 安装依赖项:(Use ``brew`` to install dependency:)

         .. code-block:: shell

            brew install protobuf

   .. group-tab:: Windows

      使用 ``choco`` 安装依赖项:(Use ``choco`` to install dependency:)

         .. code-block:: shell

            choco install protoc


配置 (Configuration)
********************

确保在 ``CMakeLists.txt`` 文件中包含 ``nanopb``,如下所示:(Make sure to include ``nanopb`` within your ``CMakeLists.txt`` file as follows:)

.. code-block:: cmake

   list(APPEND CMAKE_MODULE_PATH ${ZEPHYR_BASE}/modules/nanopb)
   include(nanopb)

可以使用 ``zephyr_nanopb_sources()`` CMake 函数添加 ``proto`` 文件,该函数确保在构建指定目标之前创建生成的头文件和源文件。(Adding ``proto`` files can be done with the ``zephyr_nanopb_sources()`` CMake function which ensures the generated header and source files are created before building the specified target.)

Nanopb 有 `生成器选项 <https://jpa.kapsi.fi/nanopb/docs/reference.html#generator-options>`_,可用于配置消息或字段。这允许设置固定大小或完全跳过字段。(Nanopb has `generator options <https://jpa.kapsi.fi/nanopb/docs/reference.html#generator-options>`_ that can be used to configure messages or fields. This allows to set fixed sizes or skip fields entirely.)

内部 CMake 生成器有一个扩展,可以使用 CMake 变量自动配置 ``*.options.in`` 文件。(The internal CMake generator has an extension to configure ``*.options.in`` files automatically with CMake variables.)

参见 :zephyr_file:`samples/modules/nanopb/src/simple.options.in` 和 :zephyr_file:`samples/modules/nanopb/CMakeLists.txt` 作为使用示例。(See :zephyr_file:`samples/modules/nanopb/src/simple.options.in` and :zephyr_file:`samples/modules/nanopb/CMakeLists.txt` for usage example.)
