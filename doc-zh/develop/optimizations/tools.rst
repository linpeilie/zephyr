.. _optimization_tools:

优化工具
##################

可用的优化工具允许您使用不同的构建系统目标分析 :ref:`footprint_tools` 和
:ref:`data_structure_tools`。

.. _footprint_tools:

占用空间和内存使用
**************************

构建系统提供 3 个目标来查看和分析生成镜像中的 RAM、ROM 和堆栈使用情况。
这些工具在最终镜像上运行,并提供有关 RAM 和 ROM 中使用的符号和代码大小的信息。
此外,通过编译器提供的功能,我们还可以生成最坏情况下的堆栈使用分析。

本节中提到的一些工具根据符号的物理组织来组织其输出。由于某些符号可能在项目的
树结构之外,或者可能缺少按名称显示它们所需的元数据,因此使用以下顶级容器对
此类符号进行分组:

* Hidden - RAM 和 ROM 报告在 Hidden 类别中列出所有没有匹配映射文件的处理符号。

  这意味着列出的符号的文件未添加到元数据文件中、为空或未定义。该工具无法获取
  给定符号的函数名称,也无法确定它来自哪里。

* No paths - RAM 和 ROM 报告在 No paths 类别中列出所有具有相对路径的处理符号。

  这意味着列出的符号无法放置在报告的树结构中一个特定文件下的绝对路径中。
  该工具能够获取函数的名称,但无法确定它来自哪里。

  .. note::

     您可以有同一函数的多个案例,No paths 类别将在一个条目中列出这些的总和。


构建目标:ram_report
========================

以表格形式列出所有编译的对象及其 RAM 使用情况,包括每个符号的字节数及其使用的百分比。
数据根据对象在树中的文件系统位置和包含符号的文件进行分组。

使用 ``ram_report`` 目标与您的开发板,如下例所示。如果您使用 :ref:`sysbuild`,
请参阅 :ref:`sysbuild_dedicated_image_build_targets`。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: reel_board
    :goals: ram_report

这些命令将生成类似于以下输出的内容::

    Path                                                           Size    %      Address
    ========================================================================================
    Root                                                           4637 100.00%  -
    ├── (hidden)                                                      4   0.09%  -
    ├── (no paths)                                                 2748  59.26%  -
    │   ├── _cpus_active                                              4   0.09%  0x20000314
    │   ├── _kernel                                                  32   0.69%  0x20000318
    │   ├── _sw_isr_table                                           384   8.28%  0x00006474
    │   ├── cli.1                                                    16   0.35%  0x20000254
    │   ├── on.2                                                      4   0.09%  0x20000264
    │   ├── poll_out_lock.0                                           4   0.09%  0x200002d4
    │   ├── z_idle_threads                                          128   2.76%  0x20000120
    │   ├── z_interrupt_stacks                                     2048  44.17%  0x20000360
    │   └── z_main_thread                                           128   2.76%  0x200001a0
    ├── WORKSPACE                                                   184   3.97%  -
    │   └── modules                                                 184   3.97%  -
    │       └── hal                                                 184   3.97%  -
    │           └── nordic                                          184   3.97%  -
    │               └── nrfx                                        184   3.97%  -
    │                   └── drivers                                 184   3.97%  -
    │                       └── src                                 184   3.97%  -
    │                           ├── nrfx_clock.c                      8   0.17%  -
    │                           │   └── m_clock_cb                    8   0.17%  0x200002e4
    │                           ├── nrfx_gpiote.c                   132   2.85%  -
    │                           │   └── m_cb                        132   2.85%  0x20000060
    │                           ├── nrfx_ppi.c                        4   0.09%  -
    │                           │   └── m_channels_allocated          4   0.09%  0x200000e4
    │                           └── nrfx_twim.c                      40   0.86%  -
    │                               └── m_cb                         40   0.86%  0x200002ec
    └── ZEPHYR_BASE                                                1701  36.68%  -
        ├── arch                                                      5   0.11%  -
        │   └── arm                                                   5   0.11%  -
        │       └── core                                              5   0.11%  -
        │           ├── mpu                                           1   0.02%  -
        │           │   └── arm_mpu.c                                 1   0.02%  -
        │           │       └── static_regions_num                    1   0.02%  0x20000348
        │           └── tls.c                                         4   0.09%  -
        │               └── z_arm_tls_ptr                             4   0.09%  0x20000240
        ├── drivers                                                 258   5.56%  -
        │   ├── ...                                                 ...    ...%
    ========================================================================================
                                                                   4637


构建目标:rom_report
========================

以表格形式列出所有编译的对象及其 ROM 使用情况,包括每个符号的字节数及其使用的百分比。
数据根据对象在树中的文件系统位置和包含符号的文件进行分组。

使用 ``rom_report`` 目标与您的开发板,如下例所示。如果您使用 :ref:`sysbuild`,
请参阅 :ref:`sysbuild_dedicated_image_build_targets`。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: reel_board
    :goals: rom_report

这些命令将生成类似于以下输出的内容::

    Path                                                           Size    %      Address
    ========================================================================================
    Root                                                          27828 100.00%  -
    ├── ...                                                         ...    ...%
    └── ZEPHYR_BASE                                               13558  48.72%  -
        ├── arch                                                   1766   6.35%  -
        │   └── arm                                                1766   6.35%  -
        │       └── core                                           1766   6.35%  -
        │           ├── cortex_m                                   1020   3.67%  -
        │           │   ├── fault.c                                 620   2.23%  -
        │           │   │   ├── bus_fault.constprop.0               108   0.39%  0x00000749
        │           │   │   ├── mem_manage_fault.constprop.0        120   0.43%  0x000007b5
        │           │   │   ├── usage_fault.constprop.0              84   0.30%  0x000006f5
        │           │   │   ├── z_arm_fault                         292   1.05%  0x0000082d
        │           │   │   └── z_arm_fault_init                     16   0.06%  0x00000951
        │           │   ├── ...                                     ...    ...%
        ├── boards                                                   32   0.11%  -
        │   └── arm                                                  32   0.11%  -
        │       └── reel_board                                       32   0.11%  -
        │           └── board.c                                      32   0.11%  -
        │               ├── __init_board_reel_board_init              8   0.03%  0x000063e4
        │               └── board_reel_board_init                    24   0.09%  0x00000ed5
        ├── build                                                   194   0.70%  -
        │   └── zephyr                                              194   0.70%  -
        │       ├── isr_tables.c                                    192   0.69%  -
        │       │   └── _irq_vector_table                           192   0.69%  0x00000040
        │       └── misc                                              2   0.01%  -
        │           └── generated                                     2   0.01%  -
        │               └── configs.c                                 2   0.01%  -
        │                   └── _ConfigAbsSyms                        2   0.01%  0x00005945
        ├── drivers                                                6282  22.57%  -
        │   ├── ...                                                 ...    ...%
    ========================================================================================
                                                                  21652


构建目标:ram_plot/rom_plot
================================

与 ``ram_report`` 和 ``rom_report`` 构建目标类似,这些目标以旭日图的形式生成内存使用
报告作为可视化表示。用户可以单击片段以浏览目录结构,并将鼠标悬停在片段上以获取更多详细信息。

运行目标将首先生成 CLI 报告,然后打开浏览器窗口。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: reel_board
    :goals: ram_plot

.. image:: ram_plot.png
   :align: center
   :alt: RAM 使用旭日图

ROM 使用情况类似。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: reel_board
    :goals: rom_plot

.. image:: rom_plot.png
   :align: center
   :alt: ROM 使用旭日图


构建目标:puncover
======================

此目标使用名为 puncover 的第三方工具,可在 https://github.com/HBehrens/puncover 找到。
构建此目标时,它将启动一个本地 Web 服务器,允许您打开 Web 客户端并浏览文件,
查看它们的 ROM、RAM 和堆栈使用情况。

在使用此目标之前,请安装 puncover Python 模块::

    pip3 install --user puncover

.. warning::

   这是一个第三方工具,在任何给定时间可能工作或不工作。请检查 GitHub 问题,
   并向项目维护者报告新问题。

安装 Python 模块后,使用 ``puncover`` 目标与您的开发板,如下例所示。
如果您使用 :ref:`sysbuild`,请参阅 :ref:`sysbuild_dedicated_image_build_targets`。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: reel_board
    :goals: puncover

``puncover`` 目标默认将在 ``localhost:5000`` 上启动本地 Web 服务器。
HTTP 服务器运行的主机 IP 和端口可以通过设置环境变量 ``PUNCOVER_HOST``
和 ``PUNCOVER_PORT`` 来更改。

要查看最坏情况下的堆栈使用分析,请在启用 :kconfig:option:`CONFIG_STACK_USAGE`
的情况下构建。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: reel_board
    :goals: puncover
    :gen-args: -DCONFIG_STACK_USAGE=y


.. _data_structure_tools:

数据结构
****************


构建目标:pahole
=====================

Poke-a-hole (pahole) 是一个目标文件分析工具,用于查找数据结构的大小,
以及由于编译器将数据元素对齐到 CPU 字大小而导致的空洞。

在使用此目标之前,必须安装 Poke-a-hole (pahole)。可以从
https://git.kernel.org/pub/scm/devel/pahole/pahole.git 获取,
在 fedora 和 ubuntu 的 dwarves 包中都可以找到::

    sudo apt-get install dwarves

或者,您可以从 fedora 获取::

    sudo dnf install dwarves

安装软件包后,使用 ``pahole`` 目标与您的开发板,如下例所示。
如果您使用 :ref:`sysbuild`,请参阅 :ref:`sysbuild_dedicated_image_build_targets`。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: reel_board
    :goals: pahole

Pahole 将在控制台中生成类似于以下输出的内容::

    /* Used at: [...]/build/zephyr/kobject_hash.c */
    /* <375> [...]/zephyr/include/zephyr/sys/dlist.h:37 */
    union {
            struct _dnode *            head;               /*     0     4 */
            struct _dnode *            next;               /*     0     4 */
    };
    /* Used at: [...]/build/zephyr/kobject_hash.c */
    /* <397> [...]/zephyr/include/zephyr/sys/dlist.h:36 */
    struct _dnode {
            union {
                    struct _dnode *    head;                 /*     0     4 */
                    struct _dnode *    next;                 /*     0     4 */
            };                                               /*     0     4 */
            union {
                    struct _dnode *    tail;                 /*     4     4 */
                    struct _dnode *    prev;                 /*     4     4 */
            };                                               /*     4     4 */

            /* size: 8, cachelines: 1, members: 2 */
            /* last cacheline: 8 bytes */
    };
    /* Used at: [...]/build/zephyr/kobject_hash.c */
    /* <3b7> [...]/zephyr/include/zephyr/sys/dlist.h:41 */
    union {
            struct _dnode *            tail;               /*     0     4 */
            struct _dnode *            prev;               /*     0     4 */
    };
    ...
    ...
