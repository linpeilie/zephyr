.. _sca:

静态代码分析 (SCA)
##########################

Zephyr 通过 CMake 支持静态代码分析工具。

构建设置 :makevar:`ZEPHYR_SCA_VARIANT` 可用于指定要使用的 SCA 工具。:envvar:`ZEPHYR_SCA_VARIANT` 也支持作为 :ref:`环境变量 <env_vars>`。

使用 ``-DZEPHYR_SCA_VARIANT=<tool>``,例如 ``-DZEPHYR_SCA_VARIANT=sparse`` 来启用静态分析工具 ``sparse``。

.. _sca_infrastructure:

SCA 工具基础设施
***********************

对 SCA 工具的支持在 :file:`sca.cmake` 文件中实现。:file:`sca.cmake` 必须放置在 :file:`{SCA_ROOT}/cmake/sca/{tool}/sca.cmake` 下。Zephyr 本身始终作为 :makevar:`SCA_ROOT` 添加,但构建系统提供了向 :makevar:`SCA_ROOT` 设置添加其他文件夹的可能性。

您可以通过创建以下结构来提供对树外 SCA 工具的支持:

.. code-block:: none

   <sca_root>/                 # 自定义 SCA 根目录
   └── cmake/
       └── sca/
           └── <tool>/         # SCA 工具的名称,这是给 ZEPHYR_SCA_VARIANT 的值
               └── sca.cmake   # 配置工具与 Zephyr 一起使用的 CMake 代码

要在 ``/path/to/my_tools/cmake/sca`` 下添加 ``foo``,请创建以下结构:

.. code-block:: none

   /path/to/my_tools
            └── cmake/
                └── sca/
                    └── foo/
                        └── sca.cmake

要使用 ``foo`` 作为 SCA 工具,您必须指定 ``-DZEPHYR_SCA_VARIANT=foo``。

记得将 ``/path/to/my_tools`` 添加到 :makevar:`SCA_ROOT`。

:makevar:`SCA_TOOL` 可以使用 ``-DSCA_ROOT=<sca_root>`` 设置为常规 CMake 设置,或由 Zephyr 模块在其 :file:`module.yml` 文件中添加,请参阅 :ref:`Zephyr 模块 - 构建设置 <modules_build_settings>`

.. _sca_native_tools:

原生 SCA 工具支持
***********************

以下是 Zephyr 构建系统原生支持的 SCA 工具列表。

.. toctree::
   :maxdepth: 1
   :glob:

   *
