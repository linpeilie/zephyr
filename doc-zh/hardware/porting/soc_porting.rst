.. _soc_porting_guide:

SoC 移植指南 (SoC Porting Guide)
#################################

本页面描述如何在 Zephyr 中添加对新 :term:`SoC` 的支持,无论是在上游 Zephyr 项目中还是在您自己的本地仓库中。

SoC 定义 (SoC Definitions)
***************************

期望您已经熟悉 Zephyr 中的板概念。
Zephyr 文档中使用的硬件支持层次结构和术语的高层概述可以在 :ref:`hw_support_hierarchy` 中看到。

对于 SoC 移植,最重要的术语是:

- SoC: 板的 CPU 所属的确切片上系统。
- SoC series (SoC 系列): 一组紧密相关的 SoC。
- SoC family (SoC 家族): 具有相似特征的更广泛的 SoC 组。
- CPU cluster (CPU 集群): 一个或多个 CPU 核心的集群。
- CPU core (CPU 核心): 给定架构的特定 CPU 实例。
- Architecture (架构): 指令集架构。

Architecture (架构)
===================

参阅 :ref:`architecture_porting_guide`。


创建您的 SoC 目录 (Create your SoC directory)
**********************************************

每个 SoC 必须有一个唯一的名称。使用 SoC 供应商给出的官方名称并检查它是否尚未被使用。在某些情况下,其他人可能已经贡献了具有相同名称的 SoC。如果 SoC 名称已被使用,那么您可能应该改进现有的 SoC 而不是创建一个新的。
脚本 ``list_hardware`` 可用于检索 Zephyr 中已知的所有 SoC 列表,例如从 Zephyr 基本目录运行 ``./scripts/list_hardware.py --soc-root=. --socs`` 可获取已使用的名称列表。

首先创建目录 ``zephyr/soc/<VENDOR>/soc1``,其中 ``<VENDOR>`` 是您的供应商子目录。

.. note::
  如果将您的 SoC 贡献给 Zephyr,则 ``<VENDOR>`` 子目录是强制性的,但如果您的 SoC 放置在本地仓库中,则允许在 ``<your-repo>/soc`` 下使用任何文件夹结构。
  ``<VENDOR>`` 子目录必须匹配 :zephyr_file:`dts/bindings/vendor-prefixes.txt` 列表中定义的供应商。如果 SoC 供应商在该列表中没有前缀,则必须创建一个。

.. note::

  SoC 目录名称不需要与 SoC 的名称匹配。
  甚至可以在一个目录中定义多个 SoC。在 Zephyr 中,SoC 通常在通用 SoC Family 或 SoC Series 树的子文件夹中组织。

您的 SoC 目录应如下所示:

.. code-block:: none

   soc/<VENDOR>/<soc-name>
   ├── soc.yml
   ├── soc.h
   ├── CMakeLists.txt
   ├── Kconfig
   ├── Kconfig.soc
   └── Kconfig.defconfig

将 ``<soc-name>`` 替换为您的 SoC 名称。

强制性文件包括:

#. :file:`soc.yml`: 描述 SoC 高层元数据的 YAML 文件,例如:

   - SoC 名称: SoC 的名称
   - CPU clusters (CPU 集群): 如果 SoC 包含一个或多个集群,则为 CPU 集群
   - SoC series (SoC 系列): SoC 所属的 SoC 系列
   - SoC family (SoC 家族): 系列所属的 SoC 家族

#. :file:`soc.h`: 一个头文件,可用于描述或为 SoC 提供配置宏。:file:`soc.h` 通常会包含在 Zephyr 中的驱动程序、子系统、板和其他源代码中。

#. :file:`Kconfig.soc`: 基本 SoC 配置,以 ``config SOC_<soc-name>`` 的形式定义 Kconfig SoC 符号,并将 SoC 名称提供给 Kconfig ``SOC`` 设置。
   如果 ``soc.yml`` 描述了 SoC 家族和系列,则还必须在此文件中定义它们。不得选择 SoC 树之外的 Kconfig 设置。要选择通用 Zephyr Kconfig 设置,必须使用 :file:`Kconfig` 文件。

#. :file:`CMakeLists.txt`: Zephyr 构建系统加载的 CMake 文件。此 CMake 文件可以定义在构建目标为 SoC 时要使用的附加包含路径和/或源文件。还必须定义要使用的基线链接器脚本。

可选文件包括:

- :file:`Kconfig`、:file:`Kconfig.defconfig` 以 :ref:`kconfig` 格式配置软件。这些选择架构和可用的外设。

编写您的 SoC YAML (Write your SoC YAML)
******************************************

SoC YAML 文件在高层次上描述 SoC 家族、SoC 系列和 SoC。

详细配置(如硬件描述和配置)在 devicetree 和 Kconfig 中完成。

只包含一个 SoC 的简单 SoC YAML 文件的骨架是:

.. code-block:: yaml

   socs:
     - name: <soc1>

可以在 SoC 文件夹中放置多个 SoC。
例如,如果它们属于一个共同的家族或系列,建议将此类 SoC 放置在一个共同的树中。
共同文件夹中的多个 SoC 和 SoC 系列可以在 :file:`soc.yml` 文件中描述为:

.. code-block:: yaml

   family:
     - name: <family-name>
       series:
         - name: <series-1-name>
           socs:
             - name: <soc1>
               cpuclusters:
                 - name: <coreA>
                 - name: <coreB>
                   ...
             - name: <soc2>
         - name: <series-2-name>
           ...


编写您的 SoC devicetree (Write your SoC devicetree)
*****************************************************

SoC devicetree 包含文件位于 :file:`<zephyr-repo>/dts` 文件夹下对应的 :file:`<ARCH>/<VENDOR>` 中。

SoC :file:`dts/<ARCH>/<VENDOR>/<soc>.dtsi` 以 Devicetree Source (DTS) 格式描述您的 SoC 硬件,并且必须被使用该 SoC 的任何板包含。

如果存在高级 :file:`<arch>.dtsi` 文件,那么一个好的起点是在您的 :file:`<soc>.dtsi` 中包含此文件。

一般来说,:file:`<soc>.dtsi` 应该如下所示:

.. code-block:: devicetree

   #include <arch>/<arch>.dtsi

   / {
           chosen {
                   /* 您的 SoC 的通用 chosen 设置 */
           };

           cpus {
                   #address-cells = <m>;
                   #size-cells = <n>;

                   cpu@0 {
                   device_type = "cpu";
                   compatible = "<compatibles>";
                   /* ... 您的 CPU 定义 ... */
           };

           soc {
                   /* 您的 SoC 定义和外设 */
                   /* 例如 ram、clock、bus、外设。 */
           };
   };

.. hint::
   可以在子目录中构建多个 :file:`<VENDOR>/<soc>.dtsi` 文件,以获得更清晰的文件系统结构。例如按 SoC 系列组织,像这样::file:`<VENDOR>/<SERIES>/<soc>.dtsi`。


多个 CPU 集群 (Multiple CPU clusters)
======================================

Devicetree 反映硬件。一个 CPU 集群可用的内存空间和外设可能与另一个 CPU 集群非常不同,因此每个 CPU 集群通常都有自己的 :file:`.dtsi` 文件。

CPU 集群 :file:`.dtsi` 文件应遵循命名方案 :file:`<soc>_<cluster>.dtsi`。:file:`<soc>_<cluster>.dtsi` 文件看起来类似于没有 CPU 集群的 SoC :file:`.dtsi`。

编写 Kconfig 文件 (Write Kconfig files)
*****************************************

Zephyr 使用 Kconfig 语言来配置软件功能。您的 SoC 需要提供一些 Kconfig 设置,然后才能为其编译 Zephyr 应用程序。

设置 Kconfig 配置值在 :ref:`setting_configuration_values` 中有详细记录。

SoC 目录中有一个强制性的 Kconfig 文件,以及两个可选文件:

.. code-block:: none

   soc/<vendor>/<your soc>
   ├── Kconfig.soc
   ├── Kconfig
   └── Kconfig.defconfig

:file:`Kconfig.soc`
  一个共享的 Kconfig 文件,可以在 Zephyr Kconfig 和 sysbuild Kconfig 树中引用。

  此文件在 Kconfig 树中选择 SoC 家族和系列以及潜在的其他 SoC 相关 Kconfig 设置。在某些情况下是 SOC_PART_NUMBER。
  此文件不得选择可重用 Kconfig SoC 树之外的任何内容。

  :file:`Kconfig.soc` 可能如下所示:

  .. code-block:: kconfig

     config SOC_FAMILY_<SOC_FAMILY_NAME>
             bool

     config SOC_SERIES_<SOC_SERIES_NAME>
             bool
             select SOC_FAMILY_<SOC_FAMILY_NAME>

     config SOC_<SOC_NAME>
             bool
             select SOC_SERIES_<SOC_SERIES_NAME>

     config SOC_FAMILY
             default "<soc_family_name>" if SOC_FAMILY_<SOC_FAMILY_NAME>

     config SOC_SERIES
             default "<soc_series_name>" if SOC_SERIES_<SOC_SERIES_NAME>

     config SOC
             default "<soc_name>" if SOC_<SOC_NAME>

  请注意,``SOC_NAME`` 是 SoC 名称的纯大写版本,``SOC_SERIES_NAME`` 是 SoC 系列名称的纯大写版本,``SOC_FAMILY_NAME`` 是 SoC 家族名称的纯大写版本。如果这些字段未出现在 :file:`soc.yml` 文件中,则它们不应出现在 :file:`Kconfig.soc` 文件中。

  Kconfig ``SOC``、``SOC_SERIES`` 和 ``SOC_FAMILY`` 设置在全局定义为字符串,因此 :file:`Kconfig.soc` 文件只应定义默认字符串值,而不应定义类型。请注意,字符串值必须与 :file:`soc.yml` 文件中使用的值匹配。

.. note::
  构建系统支持 ``soc_name``、``soc_series_name`` 和 ``soc_family_mame`` 的任何大小写变体,但在提交板以包含在 Zephyr 本身时,这些必须是 Kconfig 名称的纯小写版本。

:file:`Kconfig`
  由 :zephyr_file:`soc/Kconfig` 包含。

  此文件可以添加特定于当前 SoC 的 Kconfig 设置。

  :file:`Kconfig` 通常会使用 ``HAS_<support>`` 形式的设置来指示给定的硬件支持。

  .. code-block:: kconfig

     config SOC_<SOC_NAME>
             select ARM
             select CPU_HAS_FPU

  如果设置名称与 Zephyr 中现有的 Kconfig 设置相同,并且只修改该设置的默认值,则应改用 :file:`Kconfig.defconfig`。

:file:`Kconfig.defconfig`
  SoC 特定的 Kconfig 选项默认值。

  并非所有 SoC 都有 :file:`Kconfig.defconfig` 文件。

  整个文件应该在一对 ``if SOC_<SOC_NAME>`` / ``endif`` 或 ``if SOC_SERIES_<SERIES_NAME>`` / ``endif`` 内,像这样:

  .. code-block:: kconfig

     if SOC_<SOC_NAME>

     config NUM_IRQS
             default 32

     endif # SOC_<SOC_NAME>

多个 CPU 集群 (Multiple CPU clusters)
======================================

CPU 集群必须在 :file:`Kconfig.soc` 文件中提供额外的 Kconfig 设置。这通常采用 ``SOC_<SOC_NAME>_<CLUSTER>`` 的形式,因此对于具有两个集群 ``clusterA`` 和 ``clusterB`` 的给定 ``soc1``,这将如下所示:

当 SoC 定义 CPU 集群时

  .. code-block:: kconfig

     config SOC_SOC1_CLUSTERA
             bool
             select SOC_SOC1

     config SOC_SOC1_CLUSTERB
             bool
             select SOC_SOC1
