.. _board_porting_guide:

板级移植指南 (Board Porting Guide)
####################################

要为新的 :term:`board` (板) 添加 Zephyr 支持,您至少需要一个包含各种文件的 *板目录*。板目录中的文件继承至少一个 SoC 及其所有功能的支持。因此,Zephyr 也必须支持您的 :term:`SoC`。

.. _hw_model_v2:

过渡到当前硬件模型 (Transition to the current hardware model)
*************************************************************

在 Zephyr 3.6.0 发布后不久,Zephyr 引入了一个新的硬件模型。这个新模型彻底改变了 SoC 和板的命名和定义方式,并增加了对多年来被确定为重要的功能的支持。其中包括:

- 支持多核、多架构 AMP(非对称多处理,Asymmetrical Multi Processing)SoC
- 支持多 SoC 板
- 支持在 Zephyr 构建系统之外重用 SoC 和板 Kconfig 树
- 支持 :ref:`sysbuild` 的高级用例
- 移除所有现有的任意和不一致的 Kconfig 和文件夹名称使用

本页面中的所有文档都指的是当前硬件模型。有关以前的、现已过时的硬件模型的信息,请参阅 Zephyr v3.6.0(或更早版本)中的文档。

有关新模型背后的基本原理、开发和概念的更多信息,可以在 :github:`原始问题 <51831>`、:github:`原始拉取请求 <50305>` 以及 `hardware model v2 commit`_ 中找到完整的更改集。

新硬件模型的一些非关键功能、增强和改进仍在开发中。请查看 :github:`hardware model v2 enhancements issue <69546>` 以获取完整列表。

从以前的硬件模型过渡到当前模型(通常称为"硬件模型 v2")需要修改所有现有的板和 SoC 定义。决定不为以前的模型提供直接向后兼容性,这使得从以前版本的 Zephyr 过渡到包含新模型的版本(v3.7.0 及更高版本)的用户如果有树外板(或 SoC),有两个选项:

#. 将树外板转换为当前硬件模型(推荐)
#. 从 Zephyr v3.6.0 获取 SoC 定义并将其复制到您的下游仓库(确保构建系统可以通过 :ref:`zephyr module <modules>` 或 ``SOC_ROOT`` 找到它)。这将允许您在以前的硬件模型中定义的板继续工作

将板从以前的硬件模型转换为当前硬件模型时,我们建议首先通读本页面以详细了解该模型。然后,您可以使用 `example-application conversion Pull Request`_ 作为如何移植简单板的示例。此外,还有一个 `conversion script`_ 可用,在许多情况下工作可靠(尽管多核 SoC 可能无法完全处理)。最后,`hardware model v2 commit`_ 包含将所有现有板从旧模型到当前模型的完整转换,因此您可以将其用作完整的转换参考。

.. _hardware model v2 commit: https://github.com/zephyrproject-rtos/zephyr/commit/8dc3f856229ce083c956aa301c31a23e65bd8cd8
.. _example-application conversion Pull Request: https://github.com/zephyrproject-rtos/example-application/pull/58
.. _conversion script: https://github.com/zephyrproject-rtos/zephyr/blob/main/scripts/utils/board_v1_to_v2.py

.. _hw_support_hierarchy:

硬件支持层次结构 (Hardware support hierarchy)
*********************************************

Zephyr 的硬件支持基于一系列分层抽象。主要是,每个 :term:`board` (板) 都有一个或多个 :term:`SoC`。每个 SoC 可以可选地分类到一个 :term:`SoC series` (SoC 系列)中,该系列又可以可选地属于一个 :term:`SoC family` (SoC 家族)。每个 SoC 有一个或多个 :term:`CPU cluster` (CPU 集群),每个集群包含一个或多个特定 :term:`architecture` (架构)的 :term:`CPU core` (CPU 核心)。

您可以在下图中可视化这个层次结构:

.. figure:: board/hierarchy.png
   :width: 500px
   :align: center
   :alt: Hardware support Hierarchy

   硬件支持层次结构

以下是本节中描述的层次结构的一些示例,形式为每行一个 :term:`board` (板)及其相应的层次结构条目。注意 :term:`SoC series` (SoC 系列)和 :term:`SoC family` (SoC 家族)级别并不总是被使用。

.. table::

   +--------------------------------------------+--------------------------+-------------+--------------------+--------------------+----------------+----------------------+
   | :term:`board name`                         | :term:`board qualifiers` | :term:`SoC` | :term:`SoC Series` | :term:`SoC family` | CPU core       | :term:`architecture` |
   +============================================+==========================+=============+====================+====================+================+======================+
   | :zephyr:board:`nrf52dk`                    | nrf52832                 | nRF52832    | nRF52              | Nordic nRF         | Arm Cortex-M4  | ARMv7-M              |
   +--------------------------------------------+--------------------------+-------------+--------------------+--------------------+----------------+----------------------+
   | :zephyr:board:`frdm_k64f <frdm_k64f>`      | mk64f12                  | MK64F12     | Kinetis K6x        | NXP Kinetis        | Arm Cortex-M4  | ARMv7-M              |
   +--------------------------------------------+--------------------------+-------------+--------------------+--------------------+----------------+----------------------+
   | :zephyr:board:`rv32m1_vega <rv32m1_vega>`  | openisa_rv32m1/ri5cy     | RV32M1      | (Not used)         | (Not used)         | RI5CY          | RISC-V RV32          |
   +--------------------------------------------+--------------------------+-------------+--------------------+--------------------+----------------+----------------------+
   | :zephyr:board:`nrf5340dk`                  | nrf5340/cpuapp           | nRF5340     | nRF53              | Nordic nRF         | Arm Cortex-M33 | ARMv8-M              |
   |                                            +--------------------------+-------------+--------------------+--------------------+----------------+----------------------+
   |                                            | nrf5340/cpunet           | nRF5340     | nRF53              | Nordic nRF         | Arm Cortex-M33 | ARMv8-M              |
   +--------------------------------------------+--------------------------+-------------+--------------------+--------------------+----------------+----------------------+
   | :zephyr:board:`mimx8mp_evk <imx8mp_evk>`   | mimx8ml8/a53             | i.MX8M Plus | i.MX8M             | NXP i.MX           | Arm Cortex-A53 | ARMv8-A              |
   |                                            +--------------------------+-------------+--------------------+--------------------+----------------+----------------------+
   |                                            | mimx8ml8/m7              | i.MX8M Plus | i.MX8M             | NXP i.MX           | Arm Cortex-M7  | ARMv7-M              |
   |                                            +--------------------------+-------------+--------------------+--------------------+----------------+----------------------+
   |                                            | mimx8ml8/adsp            | i.MX8M Plus | i.MX8M             | NXP i.MX           | Cadence HIFI4  | Xtensa LX6           |
   +--------------------------------------------+--------------------------+-------------+--------------------+--------------------+----------------+----------------------+

Additional details about terminology can be found in the next section.

.. _board_terminology:

板术语 (Board terminology)
**************************

前一节介绍了 Zephyr 对硬件支持进行分类和实现的层次化方式。本节重点介绍围绕硬件支持使用的术语,特别是在定义和使用板和 SoC 时。

Zephyr 中围绕板概念使用的整体术语集如下图所示,该图以 :zephyr:board:`bl5340_dvk` 板为参考。

.. figure:: board/board-terminology.svg
   :width: 500px
   :align: center
   :alt: Board terminology diagram

   板术语图

该图显示了用于描述板的不同术语:

- :term:`board name` (板名称): ``bl5340_dvk``
- 可选的 :term:`board revision` (板修订版本): ``1.2.0``
- :term:`board qualifiers` (板限定符),可选地描述 :term:`SoC`、:term:`CPU cluster` (CPU 集群)和 :term:`variant` (变体): ``nrf5340/cpuapp/ns``
- :term:`board target` (板目标),唯一标识上述的组合,可用于在使用 Zephyr 提供的工具时指定要构建的硬件: ``bl5340_dvk@1.2.0/nrf5340/cpuapp/ns``

正式地,这也可以看作 :samp:`{board name}[@{revision}][/{board qualifiers}]`,可以扩展为 :samp:`{board name}[@{revision}][/{SoC}[/{CPU cluster}][/{variant}]]`。

如果板仅包含一个单核 SoC,则可以从板目标中省略 SoC。这意味着如果板不定义任何板限定符,则板名称可以用作板目标。相反,如果板限定符是板定义的一部分,则可以通过省略 SoC 但包括相应的正斜杠来省略 SoC: ``//``。

继续上面的例子,板 :zephyr:board:`bl5340_dvk` 是一个单 SoC 板,其中 SoC 定义了两个 CPU 集群: ``cpuapp`` 和 ``cpunet``。其中一个 CPU 集群 ``cpuapp`` 还定义了一个非安全板变体 ``ns``。

板限定符 ``nrf5340/cpuapp/ns`` 可以理解为:


- ``nrf5340``: SoC,它是一个 Nordic nRF5340 双核 SoC
- ``cpuapp``: CPU 集群 ``cpuapp``,由单个 Cortex-M33 CPU 核心组成。无法从板限定符确定 CPU 集群中的核心数量。
- ``ns``: 一个变体,在这种情况下 ``ns`` 是 Zephyr 中常见的变体名称,表示支持 :ref:`tfm` 的板的非安全构建。

并非所有 SoC 都定义 CPU 集群或变体。例如,像 :zephyr:board:`thingy52` 这样的简单板包含一个没有 CPU 集群和变体的单个 SoC。对于 ``thingy52``,板目标 ``thingy52/nrf52832`` 可以理解为:

- ``thingy52``: 板名称。
- ``nrf52832``: The board qualifiers, in this case identical to the SoC, which
  is a Nordic nRF52832.


Make sure your SoC is supported
*******************************

Start by making sure your SoC is supported by Zephyr. If it is, it's time to
:ref:`create-your-board-directory`. If you don't know, try:

- checking :ref:`boards` for names that look relevant, and reading individual
  board documentation to find out for sure.
- asking your SoC vendor

If you need to add a SoC, CPU cluster, or even architecture support, this is the
wrong page, but here is some general advice.

架构 (Architecture)
===================

请参阅 :ref:`architecture_porting_guide`。

CPU 核心 (CPU Core)
====================

CPU 核心支持文件位于 :zephyr_file:`arch` 下的 ``core`` 子目录中,例如 :zephyr_file:`arch/x86/core`。

有关 Zephyr 支持的工具链(编译器、链接器等)的信息,请参阅 :ref:`gs_toolchain`。如果您需要支持新的工具链,:ref:`build_overview` 是开始了解构建系统的好地方。如果您正在寻求建议或想要在工具链支持方面进行合作,请与社区联系。

SoC
===

Zephyr SoC 支持文件位于 :zephyr_file:`soc` 的特定于架构的子目录中。它们通常按 SoC 家族分组。

在为 Zephyr 中已有 SoC 支持的供应商添加新的 SoC 家族或系列时,请尝试将公共功能提取到共享文件中以避免重复。如果您的供应商尚未得到支持,您可以在新目录 ``zephyr/soc/<VENDOR>/<YOUR-SOC>`` 中添加它;请使用自解释的目录名称。

.. _create-your-board-directory:

创建您的板目录 (Create your board directory)
*********************************************

一旦找到使用您的 SoC 的现有板,通常可以从复制/粘贴其板目录并更改其内容以适应您的硬件开始。

您需要为板提供唯一的名称。运行 ``west boards`` 以获取已使用的名称列表,并选择一个新名称。假设您的板称为 ``plank``(请不要真的使用该名称)。

首先创建板目录 ``zephyr/boards/<VENDOR>/plank``,其中 ``<VENDOR>`` 是您的供应商子目录。(您不必将板目录放在 zephyr 仓库中,但这是最简单的入门方式。一旦它工作,请参阅 :ref:`custom_board_definition` 以获取将板目录移动到单独仓库的文档。)

.. note::
  如果将板贡献给 Zephyr,则必须使用 ``<VENDOR>`` 子目录,但如果您的板放在本地仓库中,则允许在 ``<your-repo>/boards`` 下使用任何文件夹结构。如果供应商在 :zephyr_file:`dts/bindings/vendor-prefixes.txt` 的列表中定义,则必须使用该供应商前缀作为 ``<VENDOR>``。如果未定义供应商,则可以使用 ``others`` 作为供应商前缀。

.. note::

  板目录名称不需要与板名称匹配。
  Multiple boards can even be defined in one directory.

Your board directory should look like this:

.. code-block:: none

   boards/<VENDOR>/plank
   ├── board.yml
   ├── board.cmake
   ├── CMakeLists.txt
   ├── doc
   │   ├── plank.webp
   │   └── index.rst
   ├── Kconfig.plank
   ├── Kconfig.defconfig
   ├── plank_<qualifiers>_defconfig
   ├── plank_<qualifiers>.dts
   └── plank_<qualifiers>.yaml

将 ``plank`` 替换为您的板名称。

必需的文件是:

#. :file:`board.yml`: 描述板的高级元数据的 YAML 文件,例如板名称、其 SoC 和变体。多核 SoC 的 CPU 集群不在此文件中描述,因为它们是从 SoC 的 YAML 描述中继承的。

#. :file:`plank_<qualifiers>.dts`: :ref:`devicetree <dt-guide>` 格式的硬件描述。这声明了您的 SoC、连接器以及任何其他硬件组件,如 LED、按钮、传感器或通信外设(USB、蓝牙控制器等)。

#. :file:`Kconfig.plank`: 用于选择 SoC 和其他板和 SoC 相关设置的基本软件配置。不得选择板和 SoC 树之外的 Kconfig 设置。要选择通用 Zephyr Kconfig 设置,必须使用 :file:`Kconfig` 文件。


可选文件是:

- :file:`Kconfig`, :file:`Kconfig.defconfig`: :ref:`kconfig` 格式的软件配置。这为软件功能和外设驱动程序提供默认设置。
- :file:`plank_defconfig` 和 :file:`plank_<qualifiers>_defconfig`: Kconfig ``.conf`` 格式的软件配置。
- :file:`board.cmake`: 用于 :ref:`flash-and-debug-support`
- :file:`CMakeLists.txt`: 如果您需要向构建添加额外的源文件。
- :file:`doc/index.rst`, :file:`doc/plank.webp`: 板的文档和图片。仅当您将板 :ref:`contributing-your-board` 给 Zephyr 时才需要这些。
- :file:`plank_<qualifiers>.yaml`: 包含 :ref:`twister_script` 使用的杂项元数据的 YAML 文件。

形式为 ``<soc>/<cpucluster>/<variant>`` 的板限定符被规范化,以便在用于文件名时将 ``/`` 替换为 ``_``,例如: ``soc1/foo`` 在用于文件名时变为 ``soc1_foo``。

.. _board_description:

编写您的板 YAML (Write your board YAML)
****************************************

板 YAML 文件在高层次上描述板。这包括 SoC、板变体和板修订版本。

详细配置(如硬件描述和配置)在 devicetree 和 Kconfig 中完成。

板 YAML 文件的骨架是:

.. code-block:: yaml

   board:
     name: <board-name>
     vendor: <board-vendor>
     revision:
       format: <major.minor.patch|letter|number|custom>
       default: <default-revision-value>
       exact: <true|false>
       revisions:
       - name: <revA>
       - name: <revB>
         ...
     socs:
     - name: <soc-1>
       variants:
       - name: <variant-1>
       - name: <variant-2>
         variants:
         - name: <sub-variant-2-1>
           ...
     - name: <soc-2>
       ...

可以在板文件夹中放置多个板。如果在同一个板文件夹中放置多个板,则 :file:`board.yml` 文件必须以列表形式描述它们:

.. code-block:: yaml

   boards:
   - name: <board-name-1>
     vendor: <board-vendor>
     ...
   - name: <board-name-2>
     vendor: <board-vendor>
     ...
   ...


.. _default_board_configuration:

编写您的 devicetree (Write your devicetree)
********************************************

devicetree 文件 :file:`boards/<vendor>/plank/plank.dts` 或 :file:`boards/<vendor>/plank/plank_<qualifiers>.dts` 以 Devicetree Source (DTS) 格式描述您的板硬件(照常,将 ``plank`` 更改为您的板名称)。如果您是 devicetree 的新手,请参阅 :ref:`devicetree-intro`。

一般来说,:file:`plank.dts` 应该如下所示:

.. code-block:: devicetree

   /dts-v1/;
   #include <your_soc_vendor/your_soc.dtsi>

   / {
           model = "A human readable name";
           compatible = "yourcompany,plank";

           chosen {
                   zephyr,console = &your_uart_console;
                   zephyr,sram = &your_memory_node;
                   /* other chosen settings  for your hardware */
           };

           /*
            * Your board-specific hardware: buttons, LEDs, sensors, etc.
            */

           leds {
                   compatible = "gpio-leds";
                   led0: led_0 {
                           gpios = < /* GPIO your LED is hooked up to */ >;
                           label = "LED 0";
                   };
                   /* ... other LEDs ... */
           };

           buttons {
                   compatible = "gpio-keys";
                   /* ... your button definitions ... */
           };

           /* These aliases are provided for compatibility with samples */
           aliases {
                   led0 = &led0; /* now you support the blinky sample! */
                   /* other aliases go here */
           };
   };

   &some_peripheral_you_want_to_enable { /* like a GPIO or SPI controller */
           status = "okay";
   };

   &another_peripheral_you_want {
           status = "okay";
   };

只会使用一个 ``.dts`` 文件,将使用存在的最具体的文件。

这意味着如果 :file:`plank.dts` 和 :file:`plank_soc1_foo.dts` 都存在,那么在为 ``plank`` / ``plank/soc1`` 构建时,将使用 :file:`plank.dts`。在为 ``plank//foo`` / ``plank/soc1/foo`` 构建时,将使用 :file:`plank_soc1_foo.dts`。

这允许板维护者为板编写基本的 devicetree 文件,或为给定板的 SoC 或变体编写特定的 devicetree 文件。

如果您赶时间,简单的硬件通常可以通过复制/粘贴然后试错来支持。如果您想了解详细信息,您将需要阅读其余的 devicetree 文档和 devicetree 规范。

.. _dt_k6x_example:

示例:FRDM-K64F 和 Hexiwear K64 (Example: FRDM-K64F and Hexiwear K64)
====================================================================

.. Give the filenames instead of the full paths below, as it's easier to read.
   The cramped 'foo.dts<path>' style avoids extra spaces before commas.

本节包含与编写板的 devicetree 相关的具体示例。

FRDM-K64F 和 Hexiwear K64 板的 devicetree 分别定义在 :zephyr_file:`frdm_k64fs.dts <boards/nxp/frdm_k64f/frdm_k64f.dts>` 和 :zephyr_file:`hexiwear_k64.dts <boards/nxp/hexiwear/hexiwear_mk64f12.dts>` 中。两个板都有来自同一 Kinetis SoC 家族 K6X 的 NXP SoC。

K6X 的通用 devicetree 定义存储在 :zephyr_file:`nxp_k6x.dtsi <dts/arm/nxp/nxp_k6x.dtsi>` 中,两个板的 :file:`.dts` 文件都包含该文件。:zephyr_file:`nxp_k6x.dtsi<dts/arm/nxp/nxp_k6x.dtsi>` 又包含 :zephyr_file:`armv7-m.dtsi<dts/arm/armv7-m.dtsi>`,该文件具有 Arm v7-M 核心的通用定义。

由于 :zephyr_file:`nxp_k6x.dtsi<dts/arm/nxp/nxp_k6x.dtsi>` 旨在在基于 K6X 的板上通用,因此它默认使用 ``status`` 属性禁用许多设备。例如,有一个 CAN 控制器定义为
follows (with unimportant parts skipped):

.. code-block:: devicetree

   can0: can@40024000 {
        ...
        status = "disabled";
        ...
   };

It is up to the board :file:`.dts` or application overlay files to enable these
devices as desired, by setting ``status = "okay"``. The board :file:`.dts`
files are also responsible for any board-specific configuration of the device,
例如添加板载传感器、LED、按钮等节点。

例如,FRDM-K64(但不是 Hexiwear K64):file:`.dts` 启用 CAN 控制器并设置总线速度:

.. code-block:: devicetree

   &can0 {
        status = "okay";
   };

``&can0 { ... };`` 语法在标签为 ``can0`` 的节点(即 :file:`.dtsi` 文件中定义的 ``can@4002400`` 节点)上添加/覆盖属性。

板特定定制的其他示例是将 ``aliases`` 和 ``chosen`` 中的属性指向正确的节点(请参阅 :ref:`dt-alias-chosen`),以及进行 GPIO/pinmux 分配。

.. _board_kconfig_files:

编写 Kconfig 文件 (Write Kconfig files)
****************************************

Zephyr 使用 Kconfig 语言配置软件功能。在为板编译 Zephyr 应用程序之前,您的板需要提供一些 Kconfig 设置。

在 :ref:`setting_configuration_values` 中详细记录了设置 Kconfig 配置值。

板目录中有一个必需的 Kconfig 文件,以及名为 ``plank`` 的板的几个可选文件:

.. code-block:: none

   boards/<vendor>/plank
   ├── Kconfig
   ├── Kconfig.plank
   ├── Kconfig.defconfig
   ├── plank_defconfig
   └── plank_<qualifiers>_defconfig

:file:`Kconfig.plank`
  可以在 Zephyr Kconfig 和 sysbuild Kconfig 树中都获取的共享 Kconfig 文件。

  此文件在 Kconfig 树中选择 SoC 以及潜在的其他 SoC 相关 Kconfig 设置。此文件不得选择可重用 Kconfig 板和 SoC 树之外的任何内容。

  :file:`Kconfig.plank` 可能如下所示:

  .. code-block:: kconfig

     config BOARD_PLANK
             select SOC_SOC1

  Kconfig 符号 :samp:`BOARD_{board}` 和 :samp:`BOARD_{normalized_board_target}` 由构建系统构建,因此上述代码片段中不应定义类型。

:file:`Kconfig`
  Included by :zephyr_file:`boards/Kconfig`.

  此文件可以添加特定于当前板的 Kconfig 设置。

  并非所有板都有 :file:`Kconfig` 文件。

  板特定设置应定义自定义设置,通常带有提示,如下所示:

  .. code-block:: kconfig

     config BOARD_FEATURE
             bool "Board specific feature"

  如果设置名称与 Zephyr 中现有的 Kconfig 设置相同,并且仅修改所述设置的默认值,则应改用 :file:`Kconfig.defconfig`。

:file:`Kconfig.defconfig`
  Kconfig 选项的板特定默认值。

  并非所有板都有 :file:`Kconfig.defconfig` 文件。

  整个文件应该在一对 ``if BOARD_PLANK`` / ``endif`` 行内,如下所示:

  .. code-block:: kconfig

     if BOARD_PLANK

     config FOO
             default y

     if NETWORKING
     config SOC_ETHERNET_DRIVER
             default y
     endif # NETWORKING

     endif # BOARD_PLANK

:file:`plank_defconfig` / :file:`plank_<qualifiers>_defconfig`
  一个 Kconfig 片段,每当为您的板编译应用程序时,它会按原样合并到最终构建目录 :file:`.config` 中。

  如果通用 :file:`plank_defconfig` 文件和一个或多个板限定符特定的 :file:`plank_<qualifiers>_defconfig` 文件都存在,则将使用所有匹配的文件。这允许您将所有板 SoC、CPU 集群和板变体的通用配置放在基本 :file:`plank_defconfig` 中,仅将给定 SoC 或板变体特定的调整放在 :file:`plank_<qualifiers>_defconfig` 中。

  ``_defconfig`` 应包含 UART、控制台等的强制设置。结果是特定于架构的,但通常如下所示:

  .. code-block:: cfg

     CONFIG_GPIO=y
     CONFIG_CONSOLE=y
     CONFIG_UART_CONSOLE=y
     CONFIG_SERIAL=y

:file:`plank_x_y_z_defconfig` / :file:`plank_<qualifiers>_x_y_z_defconfig`
  A Kconfig fragment that is merged as-is into the final build directory
  :file:`.config` whenever an application is compiled for your board revision
  ``x.y.z``.

Build, test, and fix
********************

现在是时候构建和测试您想在板上运行的应用程序,直到您满意为止。

例如:

.. code-block:: console

   west build -b plank samples/hello_world
   west flash

要使 ``west flash`` 工作,请参阅下面的 :ref:`flash-and-debug-support`。您也可以使用您喜欢的任何其他工具刷写 :file:`build/zephyr/zephyr.elf`、:file:`zephyr.hex` 或 :file:`zephyr.bin`。

.. _porting-general-recommendations:

一般建议 (General recommendations)
***********************************

为了保持一致性并使用户更容易为您的板构建非板特定的通用应用程序,请在移植时遵循这些准则。

- 除非本节明确建议,否则默认情况下禁用外设及其驱动程序。

- 配置并启用系统时钟以及时钟源。

- 提供与板的重要组件(如传感器、按钮或 LED)以及通信接口(如 USB、以太网连接器或蓝牙/Wi-Fi 芯片)匹配的引脚和驱动程序配置。

- 如果您的板使用众所周知的连接器标准(如 Arduino、Mikrobus、Grove 或 96Boards 连接器),请将连接器节点添加到您的 DTS 并相应地配置引脚复用。

- 配置启用这些引脚使用的组件,例如配置 SPI 实例以使用通常的 Arduino SPI 引脚。

- 如果可用,使用 devicetree 中的 ``zephyr,console`` chosen 节点为控制台配置并启用串行输出。具有内置调试适配器或 USB 到 UART 适配器的开发板默认情况下应配置并使用连接到该适配器的 UART 控制器。对于像 :zephyr:board:`nrf52840dongle` 这样没有调试适配器但有 USB 设备控制器的板,有一个通用的 :zephyr_file:`Kconfig 文件 <boards/common/usb/Kconfig.cdc_acm_serial.defconfig>`,必须包含在板的 Kconfig.defconfig 文件中,以及 :zephyr_file:`devicetree 文件 <boards/common/usb/cdc_acm_serial.dtsi>`,如果板想使用 CDC ACM UART 作为日志记录和 shell 的默认后端,则必须包含在板的 devicetree 中。

- 如果您的板支持网络,请配置默认接口。

- 启用连接到外设或扩展连接器的所有 GPIO 端口。

- 如果可用,启用 pinmux 和中断控制器驱动程序。

- 如果硬件支持,建议默认启用 MPU。对于内存资源有限的板,可以接受
  disable it. When the MPU is enabled, it is recommended to also enable
  hardware stack protection (CONFIG_HW_STACK_PROTECTION=y) and, thus, allow the
  kernel to detect stack overflows when the system is running in privileged
  mode.

.. _flash-and-debug-support:

Flash and debug support
***********************

Zephyr supports :ref:`west-build-flash-debug` via west extension commands.

To add ``west flash`` and ``west debug`` support for your board, you need to
create a :file:`board.cmake` file in your board directory. This file's job is
to configure a "runner" for your board. (There's nothing special you need to
do to get ``west build`` support for your board.)

"Runners" 是特定于 Zephyr 的 Python 类,它们包装 :ref:`flash and debug host tools <flash-debug-host-tools>` 并与 west 和 zephyr 构建系统集成以支持 ``west flash`` 和相关命令。每个 runner 支持刷写、调试或两者。您需要在 :file:`board.cmake` 中配置这些 Python 脚本的参数以支持这些命令,如以下示例 :file:`board.cmake`:

.. code-block:: cmake

   board_runner_args(jlink "--device=nrf52" "--speed=4000")
   board_runner_args(pyocd "--target=nrf52" "--frequency=4000000")

   include(${ZEPHYR_BASE}/boards/common/nrfutil.board.cmake)
   include(${ZEPHYR_BASE}/boards/common/nrfjprog.board.cmake)
   include(${ZEPHYR_BASE}/boards/common/jlink.board.cmake)
   include(${ZEPHYR_BASE}/boards/common/pyocd.board.cmake)

此示例配置了 ``nrfutil``、``nrfjprog``、``jlink`` 和 ``pyocd`` runner。

.. warning::

   Runner 通常具有与它们包装的工具匹配的名称,因此 ``jlink`` runner 包装 Segger 的 J-Link 工具,依此类推。但是像 ``--speed`` 等的 runner 命令行选项是特定于 Python 脚本的。

.. note::

   如果工具支持多个操作系统,则不应针对单个操作系统创建 Runner 和板配置,也不应依赖于特殊的系统设置/配置。例如;不要假设用户将拥有先验知识/配置或(如果使用 Linux)安装了特殊的 udev 规则,不要假设所有平台都使用一个特定的 ``/dev/X`` 设备,因为这将与 Windows 或 macOS 不兼容,并允许覆盖所选设备,以便可以将多个板连接到单个系统并根据用户的选择进行刷写/调试。

更多详细信息:

- 运行 ``west flash --context`` 查看支持刷写的可用 runner 列表,运行 ``west flash --context -r <RUNNER>`` 查看单个 runner 可用的特定选项。
- 运行 ``west debug --context`` 和 ``west debug --context <RUNNER>`` 获取支持调试的 runner 的相同输出。
- 运行 ``west flash --help`` 和 ``west debug --help`` 获取刷写和调试的顶级选项。
- 有关 Python API,请参阅 :ref:`west-runner`。
- 查找与您自己类似的其他板的 :file:`board.cmake` 文件以获取更多示例。

要确切查看 ``west flash`` 或 ``west debug`` 命令正在执行什么操作,请在详细模式下运行它:

.. code-block:: sh

   west --verbose flash
   west --verbose debug

详细模式会打印 runner 使用的任何主机工具命令。

The order of the ``include()`` calls in your :file:`board.cmake` matters. The
first ``include`` sets the default runner if it's not already set. For example,
including ``nrfjprog.board.cmake`` first means that ``nrfjprog`` is the default
flash runner for this board. Since ``nrfjprog`` does not support debugging,
``jlink`` is the default debug runner.

.. _porting_board_revisions:

Multiple board revisions
************************

See :ref:`application_board_version` for basics on this feature from the user
perspective.

Board revisions are described in the ``revision`` entry of the
:file:`board.yml`。

.. code-block:: yaml

   board:
     revision:
       format: <major.minor.patch|letter|number|custom>
       default: <default-revision-value>
       exact: <true|false>
       revisions:
       - name: <revA>
       - name: <revB>

Zephyr 原生支持以下修订格式:

- ``major.minor.patch``: 匹配三位修订版本,例如 ``1.2.3``。
- ``number``: 匹配整数修订版本
- ``letter``: 仅匹配从 ``A`` 到 ``Z`` 的单字母修订版本

.. _board_fuzzy_revision_matching:

模糊修订版本匹配 (Fuzzy revision matching)
==========================================

默认启用模糊修订版本匹配。

如果用户选择的修订版本位于可用版本之间,则使用不大于用户选择的最接近的修订版本号。例如,如果板 ``plank`` 定义了修订版本 ``0.5.0`` 和 ``1.5.0``,用户为 ``plank@0.7.0`` 构建,构建系统将针对修订版本 ``0.5.0``。

构建系统将在 CMake 配置时打印:

.. code-block:: console

   -- Board: plank, Revision: 0.7.0 (Active: 0.5.0)

这允许您仅为引入不兼容更改的板修订版本号创建修订配置文件。

对于 ``letter`` 也类似,如果定义了修订版本 ``A``、``D`` 和 ``F``,用户为 ``plank@E`` 构建,构建系统将针对修订版本 ``D``。

精确修订版本匹配 (Exact revision matching)
===========================================

当在 :file:`board.yml` 的修订部分中指定 ``exact: true`` 时,启用精确修订版本匹配。

当定义了 exact 时,在上述示例中为 ``plank@0.7.0`` 构建将导致以下错误消息:

.. code-block:: console

   Board revision `0.7.0` not found.  Please specify a valid board revision.

板修订版本配置调整 (Board revision configuration adjustment)
===========================================================

当用户为板 ``plank@<revision>`` 构建时,可以进行
adjustments to the board's normal configuration.

如 :ref:`default_board_configuration` 和 :ref:`board_kconfig_files` 部分所述,板默认配置从文件 :file:`<board>.dts` / :file:`<board>_<qualifiers>.dts` 和 :file:`<board>_defconfig` / :file:`<board>_<qualifiers>_defconfig` 创建。在为特定板修订版本构建时,上述文件用作起点,并且还将使用以下板文件:

- :file:`<board>_<qualifiers>_<revision>_defconfig`: 特定修订版本的 defconfig,仅用于由 ``<board>_<qualifiers>`` 标识的板和 SOC/变体。

- :file:`<board>_<revision>_defconfig`: 特定修订版本的 defconfig,用于板,无论 SOC/变体如何。

- :file:`<board>_<qualifiers>_<revision>.overlay`: 特定修订版本的 dts overlay,仅用于由 ``<board>_<qualifiers>`` 标识的板和 SOC/变体。

- :file:`<board>_<revision>.overlay`: 特定修订版本的 dts overlay,用于板,无论 SOC/变体如何。

这种拆分允许具有多个 SoC、多核 SoC 或变体的板将适用于所有 SoC 和变体的通用修订调整放在单个文件中,同时仍然提供将 SoC 或变体特定调整放在专用修订文件中的能力。

使用前面部分的 ``plank`` 板,我们可以有以下修订调整:

.. code-block:: none

   boards/zephyr/plank
   ├── plank_0_5_0_defconfig          # 修订版本 0.5.0 上所有 plank 板限定符的 Kconfig 调整
   ├── plank_0_5_0.overlay            # 修订版本 0.5.0 上所有 plank 板限定符的 DTS overlay
   └── plank_soc1_foo_1_5_0_defconfig # 在修订版本 1.5.0 上为 soc1 变体 foo 构建时 plank 板的 Kconfig 调整

自定义 revision.cmake 文件 (Custom revision.cmake files)
*********************************************************

某些板可能不使用 Zephyr 原生支持的板修订版本。例如字符串修订版本。

Zephyr 不支持字符串修订版本的一个原因是字符串可以采用多种形式,并且并不总是清楚给定的字符串是否只是字符串,例如 ``blue``、``green``、``red`` 等,还是它们提供可以与更高或更低修订版本匹配的顺序,例如 ``alpha``、``beta``、``gamma``。

由于字符串的可能性非常多,包括在内部进行正则表达式匹配的可能性,因此字符串修订版本必须使用 ``custom`` 修订类型完成。

要向构建系统指示使用 ``custom`` 修订版本,:file:`board.yml` 的 ``revision`` 部分中的 format 字段必须写为:

.. code-block:: yaml

   board:
     revision:
       format: custom

When using custom revisions then a :file:`revision.cmake` must be created in the
board directory.

The :file:`revision.cmake` will be included by the build system when building
for the board and it is the responsibility of the file to validate the revision
specified by the user.

The :makevar:`BOARD_REVISION` variable holds the revision value specified by the
user.

To signal to the build system that it should use a different revision than the
one specified by the user, :file:`revision.cmake` can set the variable
``ACTIVE_BOARD_REVISION`` to the revision to use instead. The corresponding
Kconfig files and devicetree overlays must be named
:file:`<board>_<ACTIVE_BOARD_REVISION>_defconfig` and
:file:`<board>_<ACTIVE_BOARD_REVISION>.overlay`.

.. _contributing-your-board:

贡献您的板 (Contributing your board)
**************************************

如果您想将板贡献给 Zephyr,首先 -- 感谢您!

您需要做一些额外的事情:

#. 确保您已遵循所有 :ref:`porting-general-recommendations`。它们是 Zephyr 包含的板的要求。

#. 使用模板文件 :zephyr_file:`doc/templates/board.tmpl` 为您的板添加文档。有关在提交拉取请求之前如何构建文档的信息,请参阅 :ref:`zephyr_doc`。

#. 准备一个添加您的板的拉取请求,遵循 :ref:`contribute_guidelines`。

.. _extend-board:

板扩展 (Board extensions)
**************************

Zephyr 中的板硬件模型允许您使用新的板变体扩展现有板。此类板扩展可以在您的自定义仓库中完成,因此可以在 Zephyr 仓库之外完成。

使用额外变体扩展现有板允许您调整现有板,从而在构建期间选择为现有的未修改板或新变体构建。

要扩展现有板,首先在扩展板中创建 :file:`board.yml`。确保使用 :ref:`create-your-board-directory` 中描述的目录结构。

用于扩展板的板 YAML 文件的骨架是:

.. code-block:: yaml

   board:
     extend: <existing-board-name>
      variants:
       - name: <new-variant>
         qualifier: <existing-qualifier>

扩展板时,您的板目录应如下所示:

.. code-block:: none

   boards/<VENDOR>/plank
   ├── board.yml
   ├── plank_<new-qualifiers>_defconfig
   └── plank_<new-qualifiers>.dts

将 ``plank`` 替换为您扩展的板的真实名称。

在某些情况下,您可能还想调整其他设置,如 :file:`Kconfig.defconfig` 或 :file:`Kconfig.{board}`。因此,在扩展板时还可以额外提供以下内容。

.. code-block:: none

   boards/<VENDOR>/plank
   ├── board.cmake
   ├── Kconfig
   ├── Kconfig.plank
   ├── Kconfig.defconfig
   └── plank_<new-qualifiers>.yaml

