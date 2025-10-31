:orphan:

.. _west_projects_index:

West 工程索引
#############

关于导入组件的贡献和审核流程的更多信息，请参阅 :ref:`external-contributions`。

有效的工程/模块
+++++++++++++++++++++

下列工程默认启用，当你调用 :command:`west update` 时将被下载。
下列许多工程或模块对于构建通用的 Zephyr 应用至关重要，其中包括对 Zephyr 中许多可用平台的硬件支持。

要禁用任何活跃模块，例如特定的 HAL，请使用以下命令::

        west config manifest.project-filter -- -hal_FOO
        west update

.. manifest-projects-table::
   :filter: active

不活跃和可选的工程/模块
+++++++++++++++++++++++++


下列工程是可选的，当你调用 :command:`west update` 时不会被下载。
你可以添加下列任何工程或模块，并使用它们编写应用代码和通过添加的功能扩展你的工作区。

要启用下列任何模块，请使用以下命令::

        west config manifest.project-filter -- +nanopb
        west update

.. manifest-projects-table::
   :filter: inactive

外部工程/模块
+++++++++++++++++++

下列工程是外部的，不直接导入到默认清单中。
要使用下列任何工程，你需要定义自己的清单文件（包含它们）。
有关在仍然继承 Zephyr :file:`west.yml` 中的强制模块的同时推荐的方法，请参阅 :ref:`west-manifest-import`。

使用模板 :file:`doc/develop/manifest/external/external.rst.tmpl` 将外部模块添加到下面的列表中：

.. toctree::
   :titlesonly:
   :maxdepth: 1
   :glob:

   external/*
