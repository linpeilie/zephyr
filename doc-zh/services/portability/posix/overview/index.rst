.. _posix_overview:

概述
####

可移植操作系统接口（POSIX）是一组由 `IEEE Computer Society`_ 制定的标准，用于维持不同操作系统之间的兼容性。
Zephyr 实现了 `IEEE 1003.1-2017`_（亦称 POSIX-1.2017）中规定的标准 POSIX API 的一个子集。

..  figure:: posix.svg
    :align: center
    :alt: POSIX Support in Zephyr

    Zephyr 中的 POSIX 支持

.. note::
    本页不涉及 Zephyr 的 :ref:`POSIX 架构<Posix arch>`（用于在宿主操作系统下以原生应用形式运行 Zephyr，
    以便进行原型设计、测试与诊断）。

借助 Zephyr 提供的 POSIX 支持，现有的符合 POSIX 的应用可以移植到 Zephyr 内核上运行，从而利用 Zephyr 的特性与功能。
此外，设计为符合 POSIX 的库也可以无需修改地用于基于 Zephyr 内核的应用。

POSIX API 作为 IoT 与嵌入式应用的 OSAL（操作系统抽象层）日益流行，常见于 Zephyr、AWS:FreeRTOS、TI-RTOS 与 NuttX 等。

Zephyr 中启用 POSIX 的收益包括：

- 为非嵌入式背景的开发者（尤其来自 Linux）提供熟悉的 API
- 复用（移植）基于 POSIX API 的既有库
- 提供适合小型（MCU）嵌入式系统的高效 API 子集

.. _posix_subprofiles:

POSIX 子配置
============

尽管 Zephyr 支持运行多个 :ref:`线程 <threads_v2>`（可在 :ref:`SMP <smp_arch>` 配置下），以及
:ref:`虚拟内存与 MMU <memory_management_api>`，但 Zephyr 的代码与数据通常共享一个地址空间，
通过 :ref:`内存域 <memory_domain>` 进行划分。内核与应用的可执行代码通常被编译到同一二进制中，
因此可将 Zephyr 应用视为在单一进程上下文中运行。

通用操作系统通常提供完整的 POSIX 兼容性；而 Zephyr 这类实时操作系统（RTOS）通常服务于固定用途、
硬件资源有限且用户交互有限。在此类系统中，完整 POSIX 兼容往往既不现实也无必要。

因此，POSIX 在 `IEEE 1003.13-2003`_（亦称 POSIX.13-2003）中定义了如下
:ref:`应用环境配置（AEP）<posix_aep>`。每个 AEP 在所需的 :ref:`POSIX 系统接口 <posix_system_interfaces>` 之上
逐步增加更多特性。

..  figure:: aep.svg
    :align: center
    :scale: 150%
    :alt: POSIX Application Environment Profiles (AEP)

    POSIX 应用环境配置（AEP）

* 最小实时系统配置（:ref:`PSE51 <posix_aep_pse51>`）
* 实时控制器系统配置（:ref:`PSE52 <posix_aep_pse52>`）
* 专用实时系统配置（:ref:`PSE53 <posix_aep_pse53>`）
* 通用实时系统（PSE54）

POSIX.13-2003 的 AEP 在 2003 年以“功能单元”的形式被形式化，但该规范现在已归档（仅作参考）。
其意图仍然在 POSIX-1.2017 中通过 :ref:`选项 <posix_options>` 与 :ref:`选项组 <posix_option_groups>` 得以保留。

更多信息参见 `IEEE 1003.1-2017, Section E, Subprofiling Considerations`_。

.. _posix_apps:

Zephyr 中的 POSIX 应用
=====================

Zephyr 中的 POSIX 应用与其他应用 :ref:`构建方式相同 <application>`，因此需要常见的
:file:`prj.conf`、:file:`CMakeLists.txt` 与源代码。例如，下面的应用使用了 ``nanosleep()`` 与 ``perror()``：

.. code-block:: cfg
   :caption: 简单 POSIX 应用的 `prj.conf`

    CONFIG_POSIX_API=y

.. code-block:: c
   :caption: 使用 Zephyr POSIX API 的简单应用

    #include <stddef.h>
    #include <stdio.h>
    #include <time.h>

    void megasleep(size_t megaseconds)
    {
        struct timespec ts = {
            .tv_sec = megaseconds * 1000000,
            .tv_nsec = 0,
        };

        printf("See you in a while!\n");
        if (nanosleep(&ts, NULL) == -1) {
            perror("nanosleep");
        }
    }

    int main()
    {
        megasleep(42);
        return 0;
    }

更多 POSIX 应用示例参见 :zephyr:code-sample-category:`POSIX 示例应用 <posix>`。

.. _posix_config:

配置
====

与 Zephyr 中的大多数特性一样，POSIX 特性是 :ref:`高度可配置的 <zephyr_intro_configurability>`，
但默认关闭。用户需要通过 :ref:`Kconfig <kconfig>` 显式启用。

子配置
++++++

启用以下任一 Kconfig 选项可快速选择预定义的 :ref:`POSIX 子配置 <posix_subprofiles>`：

* :kconfig:option:`CONFIG_POSIX_AEP_CHOICE_BASE`（:ref:`基础 <posix_system_interfaces_required>`）
* :kconfig:option:`CONFIG_POSIX_AEP_CHOICE_PSE51`（:ref:`PSE51 <posix_aep_pse51>`）
* :kconfig:option:`CONFIG_POSIX_AEP_CHOICE_PSE52`（:ref:`PSE52 <posix_aep_pse52>`）
* :kconfig:option:`CONFIG_POSIX_AEP_CHOICE_PSE53`（:ref:`PSE53 <posix_aep_pse53>`）

还可按需通过 Kconfig（例如 ``CONFIG_POSIX_C_LIB_EXT=y``）启用额外的 POSIX :ref:`选项与选项组 <posix_option_groups>`，
并通过 :ref:`更多 POSIX 相关 Kconfig 选项 <posix_kconfig_options>` 进行细化配置。

未来建议优先通过子配置、选项与选项组来配置 Zephyr 中的 POSIX。

传统方式
+++++++

历史上，Zephyr 使用 :kconfig:option:`CONFIG_POSIX_API` 来配置一组不断膨胀的 POSIX 特性：

* :kconfig:option:`CONFIG_POSIX_API`

该选项现已冻结，可视为以下组合的等价物：

* :kconfig:option:`CONFIG_POSIX_AEP_CHOICE_PSE51`
* :kconfig:option:`CONFIG_POSIX_FD_MGMT`
* :kconfig:option:`CONFIG_POSIX_MESSAGE_PASSING`
* :kconfig:option:`CONFIG_POSIX_NETWORKING`

但 :kconfig:option:`CONFIG_POSIX_API` 现被视为遗留，不应用于新的 Zephyr 应用。

.. _IEEE: https://www.ieee.org/
.. _IEEE Computer Society: https://www.computer.org/
.. _IEEE 1003.1-2017: https://standards.ieee.org/ieee/1003.1/7101/
.. _IEEE 1003.13-2003: https://standards.ieee.org/ieee/1003.13/3322/
.. _IEEE 1003.1-2017, Section E, Subprofiling Considerations:
    https://pubs.opengroup.org/onlinepubs/9699919799/xrat/V4_subprofiles.html
