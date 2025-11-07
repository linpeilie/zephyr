:orphan:

.. _west-apis:
.. _west-apis-west:

West API
########

本页面记录了 :ref:`west <west>` 提供的 Python API,以及 zephyr 仓库中
:ref:`west 扩展 <west-extensions>` 使用的一些额外 API。

**内容**:

.. contents::
   :local:

.. NOTE: documentation authors:

   1. keep these sorted by package/module name.
   2. if you add a :ref: target here, add it to west-not-found.rst too.

.. _west-apis-commands:

west.commands
*************

.. module:: west.commands

所有内置命令和扩展命令都实现为此处定义的 :py:class:`WestCommand` 类的子类。
还提供了一些异常类型。

WestCommand
===========

.. autoclass:: west.commands.WestCommand

   实例属性 (Instance attributes):

   .. py:attribute:: name

      传递给构造函数的值。

   .. py:attribute:: help

      传递给构造函数的值。

   .. py:attribute:: description

      传递给构造函数的值。

   .. py:attribute:: accepts_unknown_args

      传递给构造函数的值。

   .. py:attribute:: requires_workspace

      传递给构造函数的值。

   .. versionadded:: 0.7.0

   .. py:attribute:: parser

      通过调用 ``WestCommand.add_parser()`` 创建的参数解析器。

   实例属性 (Instance properties):

   .. py:attribute:: manifest

      一个属性,返回当前清单文件的 :py:class:`west.manifest.Manifest` 实例,
      如果未提供则中止程序。只能在 ``do_run()`` 方法中安全使用。

   .. versionadded:: 0.6.1
   .. versionchanged:: 0.7.0
      现在可设置。

   .. py:attribute:: has_manifest

      如果读取 manifest 属性会成功而不是出错,则为 True。

   .. py:attribute:: config

      一个可设置的属性,返回 :py:class:`west.configuration.Configuration` 实例,
      如果未提供则中止程序。只能在 ``do_run()`` 方法中安全使用。

   .. versionadded:: 0.13.0

   .. py:attribute:: has_config

      如果读取 config 属性会成功而不是出错,则为 True。

   .. versionadded:: 0.13.0

   .. py:attribute:: git_version_info

      Git 版本信息的元组。

   .. versionadded:: 0.11.0

   .. py:attribute:: color_ui

      如果 west 配置允许彩色输出,则为 True,否则为 False。

   .. versionadded:: 1.0.0

   构造函数 (Constructor):

   .. automethod:: __init__

   .. versionadded:: 0.6.0
      *requires_installation* 参数 (在 v0.13.0 中移除)。
   .. versionadded:: 0.7.0
      *requires_workspace* 参数。
   .. versionchanged:: 0.8.0
      *topdir* 参数现在可以是任何 ``os.PathLike``。
   .. versionchanged:: 0.13.0
      已弃用的 *requires_installation* 参数已移除。
   .. versionadded:: 1.0.0
      *verbosity* 参数。

   方法 (Methods):

   .. automethod:: run

   .. versionchanged:: 0.6.0
      添加了 *topdir* 参数。

   .. automethod:: add_parser

   .. automethod:: add_pre_run_hook
   .. versionadded:: 1.0.0

   .. NOTE: the following 'method' (not 'automethod') directives were added for
      expediency during the west v1.2 release time frame to work around a build
      failure in this zephyr documentation that could not be fixed without
      cutting a west point release. (The docstrings in west had some RST syntax
      errors).

      These should be reverted back to automethod calls at the next release.

   .. method:: check_call(args, **kwargs)

      在 ``Verbosity.DBG_MORE`` 级别记录调用后运行 ``subprocess.check_call(args, **kwargs)``。

   .. versionchanged:: 1.2.0
      *cwd* 关键字参数被替换为通用的 ``**kwargs``。
   .. versionchanged:: 0.11.0

   .. method:: check_output(args, **kwargs)

      在 Verbosity.DBG_MORE 级别记录调用后运行 ``subprocess.check_output(args, **kwargs)``。

   .. versionchanged:: 1.2.0
      *cwd* 关键字参数被替换为通用的 ``**kwargs``。
   .. versionchanged:: 0.11.0

   .. method:: run_subprocess(args, **kwargs)

      在 Verbosity.DBG_MORE 级别记录调用后运行 ``subprocess.run(args, **kwargs)``。

   .. versionadded:: 1.2.0

   所有子类必须提供以下抽象方法,用于实现上述功能:

   .. automethod:: do_add_parser

   .. automethod:: do_run

   当命令需要打印输出时应使用以下方法。引入这些方法是为了实现从已弃用的
   ``west.log`` 模块过渡到每个命令接口,这将允许在未来版本中为 west 命令提供全局
   "安静" 模式:

   .. automethod:: dbg
   .. versionchanged:: 1.2.0
      *end* 参数。
   .. versionadded:: 1.0.0

   .. automethod:: inf
   .. versionchanged:: 1.2.0
      *end* 参数。
   .. versionadded:: 1.0.0

   .. automethod:: wrn
   .. versionchanged:: 1.2.0
      *end* 参数。
   .. versionadded:: 1.0.0

   .. automethod:: err
   .. versionchanged:: 1.2.0
      *end* 参数。
   .. versionadded:: 1.0.0

   .. automethod:: die
   .. versionadded:: 1.0.0

   .. automethod:: banner
   .. versionadded:: 1.0.0

   .. automethod:: small_banner
   .. versionadded:: 1.0.0

.. _west-apis-commands-output:

Verbosity (详细程度)
=====================

从 west v1.0 开始,west 命令应使用诸如 west.commands.WestCommand.dbg()、
west.commands.WestCommand.inf() 等方法打印输出(见上文)。
本节记录了用于声明详细程度级别的相关枚举。

.. autoclass:: west.commands.Verbosity

   .. autoattribute:: QUIET
   .. autoattribute:: ERR
   .. autoattribute:: WRN
   .. autoattribute:: INF
   .. autoattribute:: DBG
   .. autoattribute:: DBG_MORE
   .. autoattribute:: DBG_EXTREME

.. versionadded:: 1.0.0

异常 (Exceptions)
==================

.. autoclass:: west.commands.CommandError
   :show-inheritance:

   .. py:attribute:: returncode

      此错误的推荐程序退出代码。

.. autoclass:: west.commands.CommandContextError
   :show-inheritance:

.. _west-apis-configuration:

west.configuration
******************

.. automodule:: west.configuration

从 west v0.13 开始,推荐使用的类是 :py:class:`west.configuration.Configuration`。

请注意,如果您正在编写 :ref:`west 扩展 <west-extensions>`,
您可以通过 ``self.config`` 访问当前的 ``Configuration`` 对象。
请参阅 :py:class:`west.commands.WestCommand`。

配置 API (Configuration API)
=============================

这是从 west v0.13 开始推荐使用的 API。

.. autoclass:: west.configuration.ConfigFile

.. autoclass:: west.configuration.Configuration
   :members:

   .. versionadded:: 0.13.0

已弃用的 API (Deprecated APIs)
===============================

以下 API 也使用 :py:class:`west.configuration.ConfigFile`,
但它们默认在存储当前工作空间配置的全局对象上操作。
由于 west 的 API 可以从多个工作空间使用,这已被证明是一个糟糕的设计决策。
它们在 west v0.13.0 中被弃用。

这些 API 为了与旧扩展兼容而保留。当可能假定为 west v0.13.0 或更高版本时,
不应在新代码中使用它们。

.. autofunction:: west.configuration.read_config

.. versionchanged:: 0.8.0
   已弃用的 *read_config* 参数已移除。

.. versionchanged:: 0.6.0
   由于无法找到本地配置文件而导致的错误被忽略。

.. autofunction:: west.configuration.update_config

.. py:data:: west.configuration.config

   当前配置的模块全局 ConfigParser 实例。
   在读取之前应使用 :py:func:`west.configuration.read_config` 进行初始化。

.. _west-apis-log:

west.log (已弃用)
******************

.. automodule:: west.log

详细程度控制 (Verbosity control)
=================================

要设置全局详细程度级别,请使用 ``set_verbosity()``。

.. autofunction:: set_verbosity

定义了这些详细程度级别。

.. autodata:: VERBOSE_NONE
.. autodata:: VERBOSE_NORMAL
.. autodata:: VERBOSE_VERY
.. autodata:: VERBOSE_EXTREME

输出函数 (Output functions)
============================

主要函数是 ``dbg()``、``inf()``、``wrn()``、``err()`` 和 ``die()``。
``inf()`` 的两个特殊情况 ``banner()`` 和 ``small_banner()``
也可用于将输出分组为 "节"。

.. autofunction:: dbg
.. autofunction:: inf
.. autofunction:: wrn
.. autofunction:: err
.. autofunction:: die

.. autofunction:: banner
.. autofunction:: small_banner

.. _west-apis-manifest:

west.manifest
*************

.. automodule:: west.manifest

主要类是 :py:class:`Manifest` 和 :py:class:`Project`。
这些表示 :ref:`清单文件 <west-manifests>` 的内容。
解析 west 清单的推荐方法是 :py:meth:`Manifest.from_topdir`。

常量和函数 (Constants and functions)
=====================================

.. autodata:: MANIFEST_PROJECT_INDEX
.. autodata:: MANIFEST_REV_BRANCH
.. autodata:: QUAL_MANIFEST_REV_BRANCH
.. autodata:: QUAL_REFS_WEST
.. autodata:: SCHEMA_VERSION

.. autofunction:: west.manifest.manifest_path

.. autofunction:: west.manifest.validate

.. versionchanged:: 0.13.0
   这将返回包含解析的 YAML 数据的已验证字典。

清单和子对象 (Manifest and sub-objects)
========================================

.. autoclass:: west.manifest.Manifest

   .. automethod:: __init__
   .. versionchanged:: 0.7.0
      *importer* 和 *import_flags* 关键字参数。
   .. versionchanged:: 0.13.0
      所有参数都改为仅关键字。*source_file* 参数已移除(改用 *topdir*)。
      该函数不再引发 ``WestNotFound``。
   .. versionadded:: 0.13.0
      *config* 参数。
   .. versionadded:: 0.13.0
      *abspath*、*posixpath*、*relative_path*、*yaml_path*、*repo_path*、
      *repo_posixpath* 和 *userdata* 属性。

   .. automethod:: from_topdir
   .. versionadded:: 0.13.0

   .. automethod:: from_file
   .. versionchanged:: 0.7.0
      添加了 ``**kwargs``。
   .. versionchanged:: 0.8.0
      *source_file*、*manifest_path* 和 *topdir* 参数现在可以是任何 ``os.PathLike``。
   .. versionchanged:: 0.13.0
      *manifest_path* 和 *topdir* 参数已移除。

   .. automethod:: from_data
   .. versionchanged:: 0.7.0
      添加了 ``**kwargs``,*source_data* 可以是 ``str``。
   .. versionchanged:: 0.13.0
      *manifest_path* 和 *topdir* 参数已移除。

   通过名称或其他标识符访问子对象的便利方法:

   .. automethod:: get_projects
   .. versionchanged:: 0.8.0
      *project_ids* 序列现在可以包含任何 ``os.PathLike``。
   .. versionadded:: 0.6.1

   其他方法 (Additional methods):

   .. automethod:: as_dict
   .. versionadded:: 1.4.0
      *active_only* 参数。
   .. versionadded:: 0.7.0
   .. automethod:: as_frozen_dict
   .. versionadded:: 1.4.0
      *active_only* 参数。
   .. automethod:: as_yaml
   .. versionadded:: 1.4.0
      *active_only* 参数。
   .. versionadded:: 0.7.0
   .. automethod:: as_frozen_yaml
   .. versionadded:: 1.4.0
      *active_only* 参数。
   .. versionadded:: 0.7.0
   .. automethod:: is_active
   .. versionadded:: 0.9.0
   .. versionchanged:: 1.1.0
      这遵守 ``manifest.project-filter`` 配置选项。
      请参阅 :ref:`west-config-index`。

.. autoclass:: west.manifest.ImportFlag
   :members:
   :member-order: bysource

.. autoclass:: west.manifest.Project

   .. (note: attributes are part of the class docstring)

   .. versionchanged:: 0.7.0
      *remote* 属性已移除。当添加对清单 ``import`` 键的支持时,
      其语义无法再保留。

   .. versionadded:: 0.7.0
      *remote_name* 和 *name_and_path* 属性。

   .. versionchanged:: 0.8.0
      *west_commands* 属性现在始终是一个列表。在以前的版本中,
      它可以是字符串或 ``None``。

   .. versionadded:: 0.9.0
      *group_filter* 和 *submodules* 属性。

   .. versionadded:: 0.12.0
      *userdata* 属性。

   .. versionadded:: 1.2.0
      *description* 属性。

   构造函数 (Constructor):

   .. automethod:: __init__

   .. versionchanged:: 0.8.0
      *path* 和 *topdir* 参数现在可以是任何 ``os.PathLike``。

   .. versionchanged:: 0.7.0
      参数与以前的版本不兼容地更改。

   方法 (Methods):

   .. automethod:: as_dict
   .. versionadded:: 0.7.0

   .. automethod:: git
   .. versionchanged:: 0.6.1
      *capture_stderr* kwarg。
   .. versionchanged:: 0.7.0
      (现已移除的) ``Project.format`` 方法不再对参数调用。

   .. automethod:: sha
   .. versionchanged:: 0.7.0
      现在捕获标准错误。

   .. automethod:: is_ancestor_of
   .. versionchanged:: 0.8.0
      *cwd* 参数现在可以是任何 ``os.PathLike``。

   .. automethod:: is_cloned
   .. versionchanged:: 0.8.0
      *cwd* 参数现在可以是任何 ``os.PathLike``。
   .. versionadded:: 0.6.1

   .. automethod:: is_up_to_date_with
   .. versionchanged:: 0.8.0
      *cwd* 参数现在可以是任何 ``os.PathLike``。

   .. automethod:: is_up_to_date
   .. versionchanged:: 0.8.0
      *cwd* 参数现在可以是任何 ``os.PathLike``。

   .. automethod:: read_at
   .. versionchanged:: 0.8.0
      *cwd* 参数现在可以是任何 ``os.PathLike``。
   .. versionadded:: 0.7.0

   .. automethod:: listdir_at
   .. versionchanged:: 0.8.0
      *cwd* 参数现在可以是任何 ``os.PathLike``。
   .. versionadded:: 0.7.0

.. autoclass:: west.manifest.ManifestProject

   支持 Project 方法的有限子集。调用其他方法的结果未指定。

   .. versionchanged:: 0.8.0
      *url* 属性现在是空字符串而不是 ``None``。
      *abspath* 属性使用 ``os.path.abspath()`` 而不是 ``os.path.realpath()`` 创建,
      改进了对符号链接的支持。

   .. automethod:: as_dict

.. versionadded:: 0.6.0

.. autoclass:: west.manifest.Submodule

.. versionadded:: 0.9.0

异常 (Exceptions)
==================

.. autoclass:: west.configuration.MalformedConfig
   :show-inheritance:

.. autoclass:: west.manifest.MalformedManifest
   :show-inheritance:

.. autoclass:: west.manifest.ManifestVersionError
   :show-inheritance:

   .. versionchanged:: 0.8.0
      *file* 参数现在可以是任何 ``os.PathLike``。

.. autoclass:: west.manifest.ManifestImportFailed
   :show-inheritance:

.. _west-apis-west-util:

west.util
*********

.. automodule:: west.util

函数 (Functions)
================

.. autofunction:: west_dir
.. autofunction:: west_topdir

异常 (Exceptions)
==================

.. autoclass:: west.util.WestNotFound
   :show-inheritance:

   .. versionchanged:: 0.8.0
      The *filename* argument can now be any ``os.PathLike``.

   .. versionchanged:: 0.13.0
      The *filename* argument was renamed *imp*, and can now take any value.

.. _west-apis-util:

west.util
*********

.. canon_path(), escapes_directory(), etc. intentionally not documented here.

.. automodule:: west.util

Functions
=========

.. autofunction:: west.util.west_dir

   .. versionchanged:: 0.8.0
      The *start* parameter can be any ``os.PathLike``.

.. autofunction:: west.util.west_topdir

   .. versionchanged:: 0.8.0
      The *start* parameter can be any ``os.PathLike``.

Exceptions
==========

.. autoclass:: west.util.WestNotFound
   :show-inheritance:
