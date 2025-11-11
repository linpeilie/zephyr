.. _pm-power-domain:

电源域 (Power Domain)
#####################

简介 (Introduction)
********************

Zephyr 电源域抽象旨在支持由公共电源供电的设备分组,以便以通用方式通知电源状态变化。使用设备 A 的应用程序代码不需要知道设备 B 在同一个电源域上,也应该被配置为低功耗状态。(The Zephyr power domain abstraction is designed to support groupings of devices powered by a common source to be notified of power source state changes in a generic fashion. Application code that is using device A does not need to know that device B is on the same power domain and should also be configured into a low power state.)

电源域在 Zephyr 中是可选的,要启用此功能,必须设置 :kconfig:option:`CONFIG_PM_DEVICE_POWER_DOMAIN` 选项。(Power domains are optional on Zephyr, to enable this feature the option :kconfig:option:`CONFIG_PM_DEVICE_POWER_DOMAIN` has to be set.)

当电源域自身打开或关闭时,电源域有责任通过它们的电源管理回调通知所有使用它的设备,分别使用 :c:enumerator:`PM_DEVICE_ACTION_TURN_ON` 或 :c:enumerator:`PM_DEVICE_ACTION_TURN_OFF` 调用。此工作流程在下图中说明。(When a power domain turns itself on or off, it is the responsibility of the power domain to notify all devices using it through their power management callback called with :c:enumerator:`PM_DEVICE_ACTION_TURN_ON` or :c:enumerator:`PM_DEVICE_ACTION_TURN_OFF` respectively. This work flow is illustrated in the diagram below.)

.. _pm-domain-work-flow:

.. graphviz::
   :caption: Power domain work flow

   digraph {
       rankdir="TB";

       action [style=invis]
       {
           rank = same;
           rankdir="LR"
           devA [label="gpio0"]
           devB [label="gpio1"]
       }
       domain [label="gpio_domain"]

      action -> devA [label="pm_device_get()"]
      devA:se -> domain:n [label="pm_device_get()"]

      domain -> devB [label="action_cb(PM_DEVICE_ACTION_TURN_ON)"]
      domain:sw -> devA:sw [label="action_cb(PM_DEVICE_ACTION_TURN_ON)"]
   }

内部电源域 (Internal Power Domains)
------------------------------------

SoC 中的大多数设备都有独立的电源控制,可以打开或关闭以降低功耗。但是,有大量的静态电流泄漏无法仅通过设备电源管理来控制。为了解决这个问题,SoC 通常被划分为几个区域,将通常一起使用的设备分组,以便可以完全关闭未使用的区域以消除这种泄漏。这些区域被称为"电源域",可以以层次结构存在并且可以嵌套。(Most of the devices in an SoC have independent power control that can be turned on or off to reduce power consumption. But there is a significant amount of static current leakage that can't be controlled only using device power management. To solve this problem, SoCs normally are divided into several regions grouping devices that are generally used together, so that an unused region can be completely powered off to eliminate this leakage. These regions are called "power domains", can be present in a hierarchy and can be nested.)

外部电源域 (External Power Domains)
------------------------------------

SoC 外部的设备可以从 SoC 主电源以外的电源供电。这些外部电源通常是开关、稳压器或专用电源 IC。多个设备可以从同一电源供电,这种设备分组通常称为"电源域"。(Devices external to a SoC can be powered from sources other than the main power source of the SoC. These external sources are typically a switch, a regulator, or a dedicated power IC. Multiple devices can be powered from the same source, and this grouping of devices is typically called a "power domain".)

将设备放置在电源域上可以出于多种原因,包括使低功耗模式下功耗高的设备在不使用时可以完全关闭。(Placing devices on power domains can be done for a variety of reasons, including to enable devices with high power consumption in low power mode to be completely turned off when not in use.)

实现指南 (Implementation guidelines)
************************************

首先,充当电源域的设备需要声明与 ``power-domain`` 兼容。以 :ref:`pm-domain-work-flow` 为例,以下代码定义了一个名为 ``gpio_domain`` 的域。(In a first place, a device that acts as a power domain needs to declare compatible with ``power-domain``. Taking :ref:`pm-domain-work-flow` as example, the following code defines a domain called ``gpio_domain``.)

.. code-block:: devicetree

	gpio_domain: gpio_domain@4 {
		compatible = "power-domain";
		...
	};

电源域需要实现 PM 子系统用于打开和关闭设备的 PM 动作回调。(A power domain needs to implement the PM action callback used by the PM subsystem to turn devices on and off.)

.. code-block:: c

    static int mydomain_pm_action(const struct device *dev,
                               enum pm_device_action *action)
    {
        switch (action) {
        case PM_DEVICE_ACTION_RESUME:
            /* resume the domain */
            ...
            /* notify children domain is now powered */
            pm_device_children_action_run(dev, PM_DEVICE_ACTION_TURN_ON, NULL);
            break;
        case PM_DEVICE_ACTION_SUSPEND:
            /* notify children domain is going down */
            pm_device_children_action_run(dev, PM_DEVICE_ACTION_TURN_OFF, NULL);
            /* suspend the domain */
            ...
            break;
        case PM_DEVICE_ACTION_TURN_ON:
            /* turn on the domain (e.g. setup control pins to disabled) */
            ...
            break;
        case PM_DEVICE_ACTION_TURN_OFF:
            /* turn off the domain (e.g. reset control pins to default state) */
            ...
            break;
        default:
            return -ENOTSUP;
        }

        return 0;
    }

属于此设备的设备可以通过在 ``power-domain`` 节点的属性中引用它来声明。下面的示例声明了属于域 ``gpio_domain`` 的设备 ``gpio0`` 和 ``gpio1``。(Devices belonging to this device can be declared referring it in the ``power-domain`` node's property. The example below declares devices ``gpio0`` and ``gpio1`` belonging to domain ``gpio_domain``.)

.. code-block:: devicetree

        &gpio0 {
                compatible = "zephyr,gpio-emul";
                gpio-controller;
                power-domains = <&gpio_domain>;
        };

        &gpio1 {
                compatible = "zephyr,gpio-emul";
                gpio-controller;
                power-domains = <&gpio_domain>;
        };

域下的所有设备在域更改状态时都会收到通知。这些通知作为设备 PM 动作回调中的动作发送,它们可以使用它们来完成任何所需的额外工作。不过它们可以安全地被忽略。(All devices under a domain will be notified when the domain changes state. These notifications are sent as actions in the device PM action callback and can be used by them to do any additional work required. They can safely be ignored though.)

.. code-block:: c

    static int mydev_pm_action(const struct device *dev,
                               enum pm_device_action *action)
    {
        switch (action) {
        case PM_DEVICE_ACTION_SUSPEND:
            /* suspend the device */
            ...
            break;
        case PM_DEVICE_ACTION_RESUME:
            /* resume the device */
            ...
            break;
        case PM_DEVICE_ACTION_TURN_ON:
            /* configure the device into low power mode */
            ...
            break;
        case PM_DEVICE_ACTION_TURN_OFF:
            /* prepare the device for power down */
            ...
            break;
        default:
            return -ENOTSUP;
        }

        return 0;
    }

.. note::

   如果依赖于它的设备用作"唤醒"源,则驱动程序或应用程序有责任将域设置为"唤醒"源。(It is responsibility of driver or the application to set the domain as "wakeup" source if a device depending on it is used as "wakeup" source.)

示例 (Examples)
****************

一些展示电源域功能的有用示例:(Some helpful examples showing power domain features:)

* :zephyr_file:`tests/subsys/pm/device_power_domains/`
* :zephyr_file:`tests/subsys/pm/power_domain/`
