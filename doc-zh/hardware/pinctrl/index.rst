.. _pinctrl-guide:

引脚控制 (Pin Control)
########################

这是引脚控制的高级指南。API 参考资料请参见 :ref:`pinctrl_api`。

简介 (Introduction)
********************

控制引脚复用和引脚配置参数(如引脚方向、上拉/下拉电阻等)的硬件块被称为 **引脚控制器**。引脚控制器的主要用户是 SoC 硬件外设,因为控制器能够公开外设信号,例如,将 ``I2C0`` ``SDA`` 信号映射到引脚 ``PX0``。不仅如此,它通常还允许配置外设正确运行所需的某些引脚设置,例如,根据工作频率配置压摆率。可用的配置选项取决于供应商/SoC,范围可以从简单的上拉/下拉选项到更高级的设置,如去抖动、低功耗模式等。

引脚控制在硬件中的实现方式是供应商/SoC 特定的。常见的是采用 *集中式* 方法,即所有引脚配置参数由单个硬件块(通常称为 pinmux)控制,包括信号映射。下图说明了这种方法。根据 ``AF`` 控制位,``PX0`` 可以映射到 ``UART0_TX``、``I2C0_SCK`` 或 ``SPI0_MOSI``。其他配置参数(如上拉/下拉)通过 ``CONFIG`` 位在同一块中控制。此模型被多个 SoC 系列使用,例如许多来自 NXP 和 STM32 的 SoC。

.. figure:: images/hw-cent-control.svg

    集中到单个每引脚块中的引脚控制示例

其他供应商/SoC 使用 *分布式* 方法。在这种情况下,引脚映射和配置由多个硬件块控制。下图说明了一种分布式方法,其中引脚映射由外设控制,例如 Nordic nRF SoC。

.. figure:: images/hw-dist-control.svg

    在外设寄存器和每引脚块之间分布的引脚控制示例

从用户角度来看,无论硬件实现如何,引脚控制器的使用都没有区别:用户总是应用一个状态。唯一的区别在于驱动程序实现。一般来说,为使用分布式方法的硬件实现引脚控制器驱动程序需要更多努力,因为驱动程序需要收集外设相关寄存器的知识。

引脚控制与 GPIO (Pin control vs. GPIO)
=======================================

引脚控制器驱动程序涵盖的某些功能与 GPIO 驱动程序重叠。例如,上拉/下拉电阻通常可以由引脚控制驱动程序和 GPIO 驱动程序启用。在 Zephyr 上下文中,引脚控制驱动程序的目的是执行外设信号复用以及配置外设正确运行所需的其他引脚参数。因此,引脚控制驱动程序的主要用户是 SoC 外设。相比之下,GPIO 驱动程序用于引脚的通用控制,即手动读取或控制其逻辑电平。

状态模型 (State model)
************************

为了使设备驱动程序正确运行,需要应用特定的引脚配置。某些设备驱动程序需要静态配置,通常在初始化时设置。其他驱动程序需要根据运行条件在运行时更改配置,例如,在挂起设备时启用低功耗模式。此类需求使用 **状态** 建模,这是一个从 Linux 内核中改编的概念。每个设备驱动程序拥有一组状态。每个状态都有唯一的名称,并包含完整的引脚配置集(见下图)。这实际上意味着状态彼此独立,因此不需要按任何特定顺序应用。状态模型的另一个优点是它将设备驱动程序与引脚配置隔离。

.. table:: 使用状态模型编码的引脚配置示例
    :align: center

    +----+------------------+----+------------------+
    | ``UART0`` peripheral                          |
    +====+==================+====+==================+
    | ``default`` state     | ``sleep`` state       |
    +----+------------------+----+------------------+
    | TX | - Pin: PA0       | TX | - Pin: PA0       |
    |    | - Pull: NONE     |    | - Pull: NONE     |
    |    | - Low Power: NO  |    | - Low Power: YES |
    +----+------------------+----+------------------+
    | RX | - Pin: PA1       | RX | - Pin: PA1       |
    |    | - Pull: UP       |    | - Pull: NONE     |
    |    | - Low Power: NO  |    | - Low Power: YES |
    +----+------------------+----+------------------+

标准状态 (Standard states)
===========================

分配给引脚控制状态的名称或数量取决于设备驱动程序的要求。在许多情况下,在初始化时应用单个状态就足够了,但在某些其他情况下需要更多状态。为了保持一致性,已为最常见的用例建立了命名约定。下表详细说明了标准化状态及其目的。

.. table:: 标准化状态名称
    :align: center

    +-------------+----------------------------------+-------------------------+
    | State       | Identifier                       | Purpose                 |
    +-------------+----------------------------------+-------------------------+
    | ``default`` | :c:macro:`PINCTRL_STATE_DEFAULT` | State of the pins when  |
    |             |                                  | the device is in        |
    |             |                                  | operational state       |
    +-------------+----------------------------------+-------------------------+
    | ``sleep``   | :c:macro:`PINCTRL_STATE_SLEEP`   | State of the pins when  |
    |             |                                  | the device is in low    |
    |             |                                  | power or sleep modes    |
    +-------------+----------------------------------+-------------------------+

请注意,将来可能会引入其他标准状态。

自定义状态 (Custom states)
===========================

某些设备驱动程序可能需要使用超出标准状态的自定义状态。为了实现这一点,设备驱动程序需要在其作用域中定义名为 ``PINCTRL_STATE_{STATE_NAME}`` 的自定义状态标识符,其中 ``{STATE_NAME}`` 是大写的状态名称。例如,如果必须支持 ``mystate``,则需要在驱动程序的作用域中定义名为 ``PINCTRL_STATE_MYSTATE`` 的定义。

.. note::
    重要的是,自定义状态标识符要从 :c:macro:`PINCTRL_STATE_PRIV_START` 开始

如果需要从驱动程序外部访问自定义状态,例如执行动态引脚控制,则应将自定义标识符放在可公开访问的头文件中。

跳过状态 (Skipping states)
===========================

在大多数情况下,Devicetree 中定义的状态将是编译固件中使用的状态。但是,在某些情况下,某些状态将根据编译标志有条件地使用。一个典型的例子是 ``sleep`` 状态。此状态仅在启用 :kconfig:option:`CONFIG_PM` 或 :kconfig:option:`CONFIG_PM_DEVICE` 时才实际使用。如果需要没有这些电源管理配置的固件变体,理论上应该从 Devicetree 中删除 ``sleep`` 状态,以免浪费 ROM 空间存储这种未使用的状态。

如果在定义引脚控制配置时存在名为 ``PINCTRL_SKIP_{STATE_NAME}`` 并扩展为 ``1`` 的定义,则 ``pinctrl`` Devicetree 宏可以跳过状态。对于 ``sleep`` 状态,``pinctrl`` API 已经提供了这样的定义,以设备电源管理的可用性为条件:

.. code-block:: c

    #if !defined(CONFIG_PM) && !defined(CONFIG_PM_DEVICE)
    /** Out of power management configurations, ignore "sleep" state. */
    #define PINCTRL_SKIP_SLEEP 1
    #endif

动态引脚控制 (Dynamic pin control)
***********************************

动态引脚控制是指在运行时更改引脚配置的能力。此功能在同一固件需要在略有不同的板上运行的情况下很有用,每个板的外设路由到不同的引脚集。可以通过设置 :kconfig:option:`CONFIG_PINCTRL_DYNAMIC` 来启用此功能。

.. note::

    动态引脚控制应仅用于尚未初始化的设备。在设备运行时更改引脚配置可能会导致意外行为。由于 Zephyr 尚不支持设备去初始化,因此此功能应仅在早期引导阶段使用。

启用动态引脚控制的影响之一是 :c:struct:`pinctrl_dev_config` 将存储在 RAM 中而不是 ROM 中(但状态或引脚配置不会)。然后,用户可以使用 :c:func:`pinctrl_update_states` 用新集合更新存储在 :c:struct:`pinctrl_dev_config` 中的状态。这实际上意味着设备驱动程序在应用状态时将应用存储在更新状态中的引脚配置。

Devicetree 表示 (Devicetree representation)
*********************************************

由于 Devicetree 旨在描述硬件,因此在存储引脚控制配置时,它是自然的选择。在以下各节中,您将找到有关如何在 Devicetree 中表示状态和引脚配置的概述。

状态 (States)
==============

给定一个设备,其每个引脚控制状态在 Devicetree 中由 ``pinctrl-N`` 属性表示,``N`` 是从零开始的状态索引。然后使用 ``pinctrl-names`` 属性按索引为每个状态属性分配唯一标识符,例如,``pinctrl-names`` 列表条目 0 是 ``pinctrl-0`` 的名称。

.. code-block:: devicetree

    periph0: periph@0 {
        ...
        /* state 0 ("default") */
        pinctrl-0 = <...>;
        ...
        /* state N ("mystate") */
        pinctrl-N = <...>;
        /* names for state 0 up to state N */
        pinctrl-names = "default", ..., "mystate";
        ...
    };

引脚配置 (Pin configuration)
=============================

在 Devicetree 中表示引脚配置有多种方法。但是,所有方法最终都编码相同的信息:引脚复用和引脚配置参数。例如,``UART_RX`` 映射到 ``PX0`` 并启用上拉。表示选择很大程度上取决于每个供应商/SoC,因此引脚控制驱动程序的 Devicetree 绑定文件是查找详细信息的最佳位置。

下面的示例展示了一种流行且通用的选项。此选择的优点之一是基于共享引脚配置的分组能力。这允许减少引脚控制定义的冗长性。另一个优点是特定状态的引脚配置参数封装在单个 Devicetree 节点中。

.. code-block:: devicetree

    /* board.dts */
    #include "board-pinctrl.dtsi"

    &periph0 {
        pinctrl-0 = <&periph0_default>;
        pinctrl-names = "default";
    };

.. code-block:: c

    /* vnd-soc-pkgxx.h
     * File with valid mappings for a specific package (may be autogenerated).
     * This file is optional, but recommended.
     */
    ...
    #define PERIPH0_SIGA_PX0 VNDSOC_PIN(X, 0, MUX0)
    #define PERIPH0_SIGB_PY7 VNDSOC_PIN(Y, 7, MUX4)
    #define PERIPH0_SIGC_PZ1 VNDSOC_PIN(Z, 1, MUX2)
    ...

.. code-block:: devicetree

    /* board-pinctrl.dtsi */
    #include <vnd-soc-pkgxx.h>

    &pinctrl {
        /* Node with pin configuration for default state */
        periph0_default: periph0_default {
            group1 {
                /* Mappings: PERIPH0_SIGA -> PX0, PERIPH0_SIGC -> PZ1 */
                pinmux = <PERIPH0_SIGA_PX0>, <PERIPH0_SIGC_PZ1>;
                /* Pins PX0 and PZ1 have pull-up enabled */
                bias-pull-up;
            };
            ...
            groupN {
                /* Mappings: PERIPH0_SIGB -> PY7 */
                pinmux = <PERIPH0_SIGB_PY7>;
            };
        };
    };

另一种流行的模型是基于为每个引脚配置和状态设置一个节点。虽然此模型可能导致更短的板引脚控制文件,但它也需要为每个引脚映射和状态设置一个节点,因为通常,节点不能为多个状态重用。如果无法自动生成,则不建议使用此方法。

.. note::

   由于所有 Devicetree 信息都被解析为 C 头文件,因此确保其大小保持最小很重要。因此,使用 ``/omit-if-no-ref/`` 前缀预生成的节点很重要。此前缀确保在不使用时丢弃节点。

.. code-block:: devicetree

    /* board.dts */
    #include "board-pinctrl.dtsi"

    &periph0 {
        pinctrl-0 = <&periph0_siga_px0_default &periph0_sigb_py7_default
                     &periph0_sigc_pz1_default>;
        pinctrl-names = "default";
    };

.. code-block:: devicetree

    /* vnd-soc-pkgxx.dtsi
     * File with valid nodes for a specific package (may be autogenerated).
     * This file is optional, but recommended.
     */

    &pinctrl {
        /* Mapping for PERIPH0_SIGA -> PX0, to be used for default state */
        /omit-if-no-ref/ periph0_siga_px0_default: periph0_siga_px0_default {
            pinmux = <VNDSOC_PIN(X, 0, MUX0)>;
        };

        /* Mapping for PERIPH0_SIGB -> PY7, to be used for default state */
        /omit-if-no-ref/ periph0_sigb_py7_default: periph0_sigb_py7_default {
            pinmux = <VNDSOC_PIN(Y, 7, MUX4)>;
        };

        /* Mapping for PERIPH0_SIGC -> PZ1, to be used for default state */
        /omit-if-no-ref/ periph0_sigc_pz1_default: periph0_sigc_pz1_default {
            pinmux = <VNDSOC_PIN(Z, 1, MUX2)>;
        };
    };

.. code-block:: devicetree

    /* board-pinctrl.dts */
    #include <vnd-soc-pkgxx.dtsi>

    /* Enable pull-up for PX0 (default state) */
    &periph0_siga_px0_default {
        bias-pull-up;
    };

    /* Enable pull-up for PZ1 (default state) */
    &periph0_sigc_pz1_default {
        bias-pull-up;
    };

.. note::

    不建议在预定义节点中添加引脚配置默认值。通常,引脚配置取决于板设计或外设工作条件,因此决定应由板做出。例如,默认启用上拉可能并不总是需要,因为板已经有一个或其值取决于运行总线速度。默认值的另一个缺点是用户可能不知道它们,例如:

    .. code-block:: devicetree

        /* not evident that "periph0_siga_px0_default" also implies "bias-pull-up" */
        /omit-if-no-ref/ periph0_siga_px0_default: periph0_siga_px0_default {
            pinmux = <VNDSOC_PIN(X, 0, MUX0)>;
            bias-pull-up;
        };

实现指南 (Implementation guidelines)
*************************************

引脚控制驱动程序 (Pin control drivers)
=======================================

引脚控制驱动程序需要实现单个函数::c:func:`pinctrl_configure_pins`。此函数接收需要应用的引脚配置数组。此外,如果设置了 :kconfig:option:`CONFIG_PINCTRL_STORE_REG`,它还会接收给定引脚的关联设备寄存器地址。某些驱动程序可能需要此信息来执行设备特定的操作。

引脚配置存储在不透明类型中,该类型取决于供应商/SoC:``pinctrl_soc_pin_t``。此类型需要在名为 ``pinctrl_soc.h`` 的头文件中定义,该文件位于 Zephyr 的包含路径中。它可以从简单的整数值到具有多个字段的结构体。``pinctrl_soc.h`` 还需要定义名为 ``Z_PINCTRL_STATE_PINS_INIT`` 的宏,该宏接受两个参数:节点标识符和属性名称(``pinctrl-N``)。使用此信息,宏需要为给定节点的 ``pinctrl-N`` 属性中包含的所有引脚配置定义初始化器。

关于 Devicetree 引脚配置表示,供应商可以决定哪个选项更适合其设备。但是,应遵循以下指南:

- 使用 ``pinctrl-N`` (N=0, 1, ...) 和 ``pinctrl-names`` 属性定义引脚控制状态。这些属性在 :file:`dts/bindings/pinctrl/pinctrl-device.yaml` 中定义。
- 使用 :file:`dts/bindings/pinctrl/pincfg-node.yaml` 中定义的标准引脚配置属性。

如果供应商已在其他操作系统(例如 Linux)中使用,则可以接受不遵循这些指南的表示。

设备驱动程序 (Device drivers)
==============================

在本节中,您将找到有关设备驱动程序应如何使用 ``pinctrl`` API 成功配置其所需引脚的一些提示。

需要在相应的绑定中修改设备兼容性,以便包含 ``pinctrl-device.yaml``。例如:

.. code-block:: yaml

    include: [base.yaml, pinctrl-device.yaml]

此文件用于将 ``pinctrl-N`` 和 ``pinctrl-names`` 属性添加到设备。

从设备驱动程序的角度来看,要能够使用 ``pinctrl`` API,需要执行两个步骤。首先,需要定义引脚控制配置。这包括所有状态和引脚。应使用 :c:macro:`PINCTRL_DT_DEFINE` 或 :c:macro:`PINCTRL_DT_INST_DEFINE` 宏。其次,需要存储对设备实例 :c:struct:`pinctrl_dev_config` 的引用,因为稍后使用 API 时需要它。可以使用 :c:macro:`PINCTRL_DT_DEV_CONFIG_GET` 和 :c:macro:`PINCTRL_DT_INST_DEV_CONFIG_GET` 宏实现此目的。

值得注意的是,设备与其关联的引脚控制配置之间的唯一关系基于变量命名约定。为相应的设备实例命名 :c:struct:`pinctrl_dev_config` 实例的方式允许稍后在给定设备的 Devicetree 节点标识符的情况下获取对它的引用。这允许最小化 ROM 使用,因为只有需要引脚控制的设备才会拥有对引脚控制配置的引用。

一旦驱动程序定义了引脚控制配置并保留了对它的引用,它就可以使用 API 了。应用状态的最常见方法是使用 :c:func:`pinctrl_apply_state`。如果提前缓存(例如在初始化时),也可以使用较低级别的函数 :c:func:`pinctrl_apply_state_direct` 跳过状态查找。由于状态查找时间预计很快,因此建议使用 :c:func:`pinctrl_apply_state`。

下面的示例包含使用 ``pinctrl`` API 的设备驱动程序的完整示例。

.. code-block:: c

    /* A driver for the "mydev" compatible device */
    #define DT_DRV_COMPAT mydev

    ...
    #include <zephyr/drivers/pinctrl.h>
    ...

    struct mydev_config {
        ...
        /* Reference to mydev pinctrl configuration */
        const struct pinctrl_dev_config *pcfg;
        ...
    };

    ...

    static int mydev_init(const struct device *dev)
    {
        const struct mydev_config *config = dev->config;
        int ret;
        ...
        /* Select "default" state at initialization time */
        ret = pinctrl_apply_state(config->pcfg, PINCTRL_STATE_DEFAULT);
        if (ret < 0) {
            return ret;
        }
        ...
    }

    #define MYDEV_DEFINE(i)                                                    \
        /* Define all pinctrl configuration for instance "i" */                \
        PINCTRL_DT_INST_DEFINE(i);                                             \
        ...                                                                    \
        static const struct mydev_config mydev_config_##i = {                  \
            ...                                                                \
            /* Keep a ref. to the pinctrl configuration for instance "i" */    \
            .pcfg = PINCTRL_DT_INST_DEV_CONFIG_GET(i),                         \
            ...                                                                \
        };                                                                     \
        ...                                                                    \
                                                                               \
        DEVICE_DT_INST_DEFINE(i, mydev_init, NULL, &mydev_data##i,             \
                              &mydev_config##i, ...);

    DT_INST_FOREACH_STATUS_OKAY(MYDEV_DEFINE)

.. _pinctrl_api:

引脚控制 API (Pin Control API)
********************************

.. doxygengroup:: pinctrl_interface

动态引脚控制 (Dynamic pin control)
====================================

.. doxygengroup:: pinctrl_interface_dynamic


其他参考资料 (Other reference material)
*****************************************

- `Introduction to pin muxing and GPIO control under Linux <https://elinux.org/images/a/a7/ELC-2021_Introduction_to_pin_muxing_and_GPIO_control_under_Linux.pdf>`_
