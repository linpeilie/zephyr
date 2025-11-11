设备电源管理 (Device Power Management)
#######################################

简介 (Introduction)
********************

Zephyr 中的设备电源管理是一个功能,它提供了机制来连贯地影响设备驱动程序要采取的电源管理操作的控制。此控制基于可以由系统的任何组件设置的明确期望,以及设备之间可能存在的与电源相关的依赖关系。(Device Power Management in Zephyr is a feature which presents mechanisms to coherently affect the control of power management actions to be taken by device drivers. This control is based on unambiguous expectations which could be set by any component of the system, and on power-related dependencies that devices may have on each other.)

Zephyr 支持两种设备电源管理方法:(Zephyr supports two methods of device power management:)

 - :ref:`设备运行时电源管理 <pm-device-runtime-pm>` (Device Runtime Power Management)
 - :ref:`系统管理的设备电源管理 <pm-device-system-pm>` (System-Managed Device Power Management)

.. _pm-device-runtime-pm:

设备运行时电源管理 (Device Runtime Power Management)
=====================================================

设备运行时电源管理涉及设备驱动程序、子系统和应用程序之间的协调交互。虽然设备驱动程序在直接控制设备的电源状态方面起着关键作用,但挂起或恢复设备的决定也可以受到软件堆栈更高层的影响。(Device runtime power management involves coordinated interaction between device drivers, subsystems, and applications. While device drivers play a crucial role in directly controlling the power state of devices, the decision to suspend or resume a device can also be influenced by higher layers of the software stack.)

每一层——设备驱动程序、子系统和应用程序——都可以独立运行,而无需了解其他层的具体信息,因为子系统使用引用计数来检查何时需要挂起或恢复设备。(Each layer—device drivers, subsystems, and applications—can operate independently without needing to know about the specifics of the other layers because the subsystem uses reference count to check when it needs to suspend or resume a device.)

- **设备驱动程序** 负责管理设备的电源状态。它们直接与硬件交互,在设备不使用时将其置于低功耗状态(挂起),并在需要时将其恢复。驱动程序应该使用 Zephyr 提供的 :ref:`设备运行时电源管理 API <device_runtime_apis>` 来控制设备的电源状态。(**Device drivers** are responsible for managing the power state of devices. They interact directly with the hardware to put devices into low-power states (suspend) when they are not in use, and bring them back (resume) when needed. Drivers should use the :ref:`device runtime power management APIs <device_runtime_apis>` provided by Zephyr to control the power state of devices.)

- **子系统**,如传感器、文件系统和网络,也可以影响设备电源管理。子系统可能对整体系统状态和工作负载有更好的了解,允许它们对何时挂起或恢复设备做出明智的决定。例如,如果网络子系统预期在不久的将来会有网络活动,它可能会决定保持网络接口通电。(**Subsystems**, such as sensors, file systems, and network, can also influence device power management. Subsystems may have better knowledge about the overall system state and workload, allowing them to make informed decisions about when to suspend or resume devices. For example, a networking subsystem may decide to keep a network interface powered on if it expects network activity in the near future.)

- **应用程序** 在 Zephyr 上运行也可以影响设备电源管理。应用程序可能对设备使用和功耗有特定要求。例如,通过网络流式传输数据的应用程序可能需要保持网络接口持续通电。(**Applications** running on Zephyr can impact device power management as well. An application may have specific requirements regarding device usage and power consumption. For
  example, an application that streams data over a network may need
  to keep the network interface powered on continuously.

设备驱动程序、子系统和应用程序之间的协调是高效设备电源管理的关键。例如,设备驱动程序可能不知道子系统将执行一系列需要设备保持通电的连续操作。在这种情况下,子系统可以使用设备运行时电源管理来确保设备在操作完成之前保持活动状态。(Coordination between device drivers, subsystems, and applications is key to efficient device power management. For example, a device driver may not know that a subsystem will perform a series of sequential operations that require a device to remain powered on. In such cases, the subsystem can use device runtime power management to ensure that the device remains in an active state until the operations are complete.)

当使用此设备运行时电源管理时,系统电源管理子系统能够快速更改电源状态,因为它不需要花费时间挂起和恢复已启用运行时的设备。(When using this Device Runtime Power Management, the System Power Management subsystem is able to change power states quickly because it does not need to spend time suspending and resuming devices that are runtime enabled.)

有关更多信息,请参阅 :ref:`pm-device-runtime`。(For more information, see :ref:`pm-device-runtime`.)

.. _pm-device-system-pm:

系统管理的设备电源管理 (System-Managed Device Power Management)
================================================================

系统管理的设备电源管理 (PM) 框架是一种在系统进入 CPU(或 SoC)电源状态时同时挂起设备的方法。可以通过设置 :kconfig:option:`CONFIG_PM_DEVICE_SYSTEM_MANAGED` 来启用它。使用此方法时,设备电源管理主要在 :c:func:`pm_system_suspend()` 内完成。(The system managed device power management (PM) framework is a method where devices are suspended along with the system entering a CPU (or SoC) power state. It can be enabled by setting :kconfig:option:`CONFIG_PM_DEVICE_SYSTEM_MANAGED`. When using this method, device power management is mostly done inside :c:func:`pm_system_suspend()`.)

如果做出进入 CPU 较低电源状态的决定,电源管理子系统将检查所选的低功耗状态是否触发设备电源管理,然后在更改状态之前挂起设备。子系统按照初始化顺序挂起设备,确保满足它们之间可能的依赖关系。一旦 CPU 从睡眠状态唤醒,设备就会按照它们被挂起的相反顺序恢复。(If a decision to enter a CPU lower power state is made, the power management subsystem will check if the selected low power state triggers device power management and then suspend devices before changing state. The subsystem takes care of suspending devices following their initialization order, ensuring that possible dependencies between them are satisfied. As soon as the CPU wakes up from a sleep state, devices are resumed in the opposite order that they were suspended.)

关于在进入低功耗状态时是否挂起设备的决定是基于状态以及是否设置了属性 ``zephyr,pm-device-disabled``。这是一个具有两个低功耗状态的目标示例,只有一个触发设备电源管理:(The decision about suspending devices when entering a low power state is done based on the state and if it has set the property ``zephyr,pm-device-disabled``. Here is an example of a target with two low power states with only one triggering device power management:)

.. code-block:: devicetree

   /* Node in a DTS file */
   cpus {
        power-states {
                state0: state0 {
                        compatible = "zephyr,power-state";
                        power-state-name = "standby";
                        min-residency-us = <5000>;
                        exit-latency-us = <240>;
                        zephyr,pm-device-disabled;
                };
                state1: state1 {
                        compatible = "zephyr,power-state";
                        power-state-name = "suspend-to-ram";
                        min-residency-us = <8000>;
                        exit-latency-us = <360>;
                };
        };
   };

.. note::

   使用 :ref:`pm-system` 时,设备转换可以从空闲线程运行。由于此上下文中的函数不能阻塞,打算使用阻塞 API 的转换 **必须** 使用 :c:func:`k_can_yield` 检查它们是否可以这样做。(When using :ref:`pm-system`, device transitions can be run from the idle thread. As functions in this context cannot block, transitions that intend to use blocking APIs **must** check whether they can do so with :c:func:`k_can_yield`.)

此设备电源管理方法在以下场景中可能很有用:(This method of device power management can be useful in the following scenarios:)

- 挂起和恢复时没有设备需要任何阻塞操作的系统。此实现比设备运行时电源管理要简单得多。(Systems with no device requiring any blocking operations when suspending and resuming. This implementation is reasonably simpler than device runtime power management.)
- 对于无法做出任何电源管理决策且必须始终处于活动状态的设备。例如,由外部实体(例如主机 CPU)控制的使用 Zephyr 的固件。在这种情况下,某些设备必须始终处于活动状态,并且应该在此外部实体请求时与 SoC 一起挂起。(For devices that can not make any power management decision and have to be always active. For example a firmware using Zephyr that is controlled by an external entity (e.g Host CPU). In this scenario, some devices have to be always active and should be suspended together with the SoC when requested by this external entity.)

重要的是要强调,此方法存在缺点(见上文),而 :ref:`设备运行时电源管理 <pm-device-runtime-pm>` 是实现设备电源管理的 **首选** 方法。(It is important to emphasize that this method has drawbacks (see above) and :ref:`Device Runtime Power Management <pm-device-runtime-pm>` is the **preferred** method for implementing device power management.)
:ref:`Device Runtime Power Management <pm-device-runtime-pm>` is the
**preferred** method for implementing device power management.

.. note::

    使用此设备电源管理方法时,如果设备无法被挂起,CPU 将不会进入低功耗状态。例如,如果设备响应 ``PM_DEVICE_ACTION_SUSPEND`` 动作返回 ``-EBUSY`` 等错误,表示它正在进行无法中断的事务。另一个阻止 CPU 进入低功耗状态的条件是如果设置了 :kconfig:option:`CONFIG_PM_NEED_ALL_DEVICES_IDLE` 选项并且设备被标记为忙碌。(When using this method of device power management, the CPU will not enter a low-power state if a device cannot be suspended. For example, if a device returns an error such as ``-EBUSY`` in response to the ``PM_DEVICE_ACTION_SUSPEND`` action, indicating it is in the middle of a transaction that cannot be interrupted. Another condition that prevents the CPU from entering a low-power state is if the option :kconfig:option:`CONFIG_PM_NEED_ALL_DEVICES_IDLE` is set and a device is marked as busy.)

.. note::

   仅当最后一个活动核心进入低功耗状态时才挂起设备,并且设备由变为活动的第一个核心恢复。(Devices are suspended only when the last active core is entering a low power state and devices are resumed by the first core that becomes active.)

设备电源管理状态 (Device Power Management States)
**************************************************

电源管理子系统在 :c:enum:`pm_device_state` 中定义设备状态。此方法用于跟踪特定设备的电源状态。重要的是要强调,虽然状态由子系统跟踪,但每个设备驱动程序负责处理更改设备状态的设备动作 (:c:enum:`pm_device_action`)。(The power management subsystem defines device states in :c:enum:`pm_device_state`. This method is used to track power states of a particular device. It is important to emphasize that, although the state is tracked by the subsystem, it is the responsibility of each device driver to handle device actions(:c:enum:`pm_device_action`) which change device state.)

设备驱动程序在内部实现 :c:func:`pm_device_action_cb_t` 钩子,它接收设备驱动程序要处理的 :c:enum:`pm_device_action`。如果选择了 :kconfig:option:`CONFIG_PM_DEVICE` 选项,设备驱动程序的钩子实现将暴露给 PM 子系统,从而启用设备的运行时电源管理。(Device drivers implement the :c:func:`pm_device_action_cb_t` hook internally which receives the :c:enum:`pm_device_action` for the device driver to handle. If the :kconfig:option:`CONFIG_PM_DEVICE` option is selected, the device drivers implementations of the hooks are exposed to the PM subsystem, enabling runtime power management of the devices.)

:c:enum:`pm_device_action` 动作与 :c:enum:`pm_device_state` 状态有直接且明确的关系:(:c:enum:`pm_device_action` actions have direct and unambiguous relationships with :c:enum:`pm_device_state` states:)

.. graphviz::
   :caption: Device actions x states

    digraph {
        node [shape=circle];
        rankdir=LR;
        subgraph {

            SUSPENDED [label=PM_DEVICE_STATE_SUSPENDED];
            SUSPENDING [label=PM_DEVICE_STATE_SUSPENDING];
            ACTIVE [label=PM_DEVICE_STATE_ACTIVE];
            OFF [label=PM_DEVICE_STATE_OFF];

            ACTIVE -> SUSPENDING;
            SUSPENDING -> ACTIVE;
            SUSPENDING -> SUSPENDED ["label"="PM_DEVICE_ACTION_SUSPEND"];

            ACTIVE -> SUSPENDED ["label"="PM_DEVICE_ACTION_SUSPEND"];
            SUSPENDED -> ACTIVE ["label"="PM_DEVICE_ACTION_RESUME"];

            {rank = same; SUSPENDED; SUSPENDING;}

            OFF -> SUSPENDED ["label"="PM_DEVICE_ACTION_TURN_ON"];
            SUSPENDED -> OFF ["label"="PM_DEVICE_ACTION_TURN_OFF"];
        }
    }

如上所述,设备驱动程序不会直接在这些状态之间切换。这完全由电源管理子系统完成。相反,驱动程序负责实现处理状态更改所需的任何硬件特定任务。(As mentioned above, device drivers do not directly change between these states. This is entirely done by the power management subsystem. Instead, drivers are responsible for implementing any hardware-specific tasks needed to handle state changes.)

支持设备电源管理的设备模型 (Device Model with Device Power Management Support)
********************************************************************************

驱动程序使用宏初始化设备。有关如何使用这些宏的详细信息,请参阅 :ref:`device_model_api`。实现设备电源管理支持的驱动程序必须为这些宏提供描述其电源管理实现的参数。(Drivers initialize devices using macros. See :ref:`device_model_api` for details on how these macros are used. A driver which implements device power management support must provide these macros with arguments that describe its power management implementation.)

使用 :c:macro:`PM_DEVICE_DEFINE` 或 :c:macro:`PM_DEVICE_DT_DEFINE` 定义驱动程序所需的电源管理资源。这些宏分配电源管理子系统所需的驱动程序特定上下文。(Use :c:macro:`PM_DEVICE_DEFINE` or :c:macro:`PM_DEVICE_DT_DEFINE` to define the power management resources required by a driver. These macros allocate the driver-specific context which is required by the power management subsystem.)

驱动程序可以使用 :c:macro:`PM_DEVICE_GET` 或 :c:macro:`PM_DEVICE_DT_GET` 获取指向此上下文的指针。这些指针应该传递给 ``DEVICE_DEFINE`` 或 ``DEVICE_DT_DEFINE`` 以初始化每个 :c:struct:`device` 中的电源管理字段。(Drivers can use :c:macro:`PM_DEVICE_GET` or :c:macro:`PM_DEVICE_DT_GET` to get a pointer to this context. These pointers should be passed to ``DEVICE_DEFINE`` or ``DEVICE_DT_DEFINE`` to initialize the power management field in each :c:struct:`device`.)

以下示例代码展示了如何在设备驱动程序中实现设备电源管理支持。请注意,为了简洁起见,返回值被明确忽略,在实际驱动程序中必须处理它们。(The following example code shows how to implement device power management support in a device driver. Note that return values are explicitly ignored for brevity, in real drivers they must be handled.)

.. code-block:: c

   #include <zephyr/pm/device.h>
   #include <zephyr/pm/device_runtime.h>

   #define DT_DRV_COMPAT dummy_device

   struct dummy_driver_data {
           struct gpio_callback int_pin_callback;
           const struct device *dev;
   };

   struct dummy_driver_config {
           const struct device *bus;
           const struct gpio_dt_spec int_pin;
           const struct gpio_dt_spec enable_pin;
   };

   static void dummy_driver_int_pin_handler(const struct device *dev,
                                            struct gpio_callback *cb,
                                            uint32_t pins)
   {
           struct dummy_driver_data *dev_data =
                   CONTAINER_OF(cb, struct dummy_driver_data, int_pin_callback);
           const struct device *dev = dev_data->dev;
           const struct dummy_driver_config *dev_config = dev->config;

           /* ... */
   }

   static int dummy_driver_pm_suspend(const struct device *dev)
   {
           struct dummy_driver_data *dev_data = dev->data;
           const struct dummy_driver_config *dev_config = dev->config;

           /* Request devices needed by device */
           (void)pm_device_runtime_get(config->enable_pin.port);

           /* Disable and remove interrupt pin interrupt */
           (void)gpio_pin_interrupt_configure_dt(&config->int_gpio, GPIO_INT_DISABLED);
           (void)gpio_remove_callback(config->int_pin.port, &data->int_pin_callback);

           /* Disable the device. In this case, we use the enable pin */
           (void)gpio_pin_set_dt(&config->enable_pin, 0);

           /* Release devices currently not needed by device */
           (void)pm_device_runtime_put(config->enable_pin.port);
           (void)pm_device_runtime_put(config->int_pin.port);

           /*
            * Note that we now have suspended the device and released all the
            * devices this device depends on. We are ready for the power
            * domain being suspended, the device being resumed again, or the
            * device driver being deinitialized.
            */

           return 0;
   }

   static int dummy_driver_pm_resume(const struct device *dev)
   {
           struct dummy_driver_data *dev_data = dev->data;
           const struct dummy_driver_config *dev_config = dev->config;

           /* Request devices needed by device */
           (void)pm_device_runtime_get(config->enable_pin.port);
           (void)pm_device_runtime_get(config->int_pin.port);
           (void)pm_device_runtime_get(config->bus);

           /* Enable the device. In this case, we use the enable pin */
           (void)gpio_pin_set_dt(&config->enable_pin, 1);

           /*
            * Write initial commands to device, in this case configuring
            * the device's interrupt output pin using the bus
            */

           /* ... */

           /* Add and enable interrupt pin interrupt */
           (void)gpio_add_callback(config->int_pin.port, &data->int_pin_callback);
           (void)gpio_pin_interrupt_configure_dt(&config->int_gpio, GPIO_INT_EDGE_TO_ACTIVE);

           /*
            * Release devices currently not needed by device. In this case, we
            * are releasing the bus and the enable pin.
            *
            * The device driver would keep the bus ACTIVE while the device is
            * ACTIVE in cases of high throughput or unsolicitet data on the
            * bus, to avoid inefficient RESUME/SUSPEND cycles of the bus
            * for every transaction, and allowing reception of unsolicitet
            * data on buses like UART.
            */
           (void)pm_device_runtime_put(config->bus);
           (void)pm_device_runtime_put(config->enable_pin.port);

           /*
            * Note that the interrupt pin's port is kept resumed as it
            * it needs to service the GPIO interrupt we enabled.
            */

           return 0;
   }

   static int dummy_driver_pm_turn_off(const struct device *dev)
   {
           const struct dummy_driver_config *dev_config = dev->config;

           /* Request devices needed for configuring device */
           (void)pm_device_runtime_get(config->enable_pin.port);

           /*
            * We prepare the device for being powered off. In this case, we
            * have an active low enable pin, which could back power the device
            * once the power domain is suspended, so we configure it as
            * disconnected if supported, input otherwise.
            */
           if (gpio_pin_configure_dt(&config->enable_pin, GPIO_DISCONNECTED)) {
                   (void)gpio_pin_configure_dt(&config->enable_pin, GPIO_INPUT);
           }

           /* Release devices needed for configuring device */
           (void)pm_device_runtime_put(config->enable_pin.port);

           /*
            * We have now prepared the device for being powered off and have
            * released all the devices this device depends on. We assume that
            * the enable pin will retain its configuration, even as we have
            * released the enable pin's port.
            */

            return 0;
   }

   static int dummy_driver_pm_turn_on(const struct device *dev)
   {
           const struct dummy_driver_config *dev_config = dev->config;

           /* Request devices needed for configuring device */
           (void)pm_device_runtime_get(config->enable_pin.port);
           (void)pm_device_runtime_get(config->int_gpio.port);

           /*
            * We ensure the device is suspended, and if possible in its reset
            * state. In this case we are using an enable pin, for other devices
            * we may need to reset them by toggling a reset pin, using an SoC
            * reset controller, or writing a reset command to them using their
            * bus.
            */
           (void)gpio_pin_configure_dt(&config->enable_pin, GPIO_OUTPUT_INACTIVE);

           /* We configure pins for suspended */
           (void)gpio_pin_configure_dt(&config->int_gpio, GPIO_INPUT);

           /* Release devices needed for configuring device */
           (void)pm_device_runtime_put(config->int_gpio.port);
           (void)pm_device_runtime_put(config->enable_pin.port);

           return 0;
   }

   static int dummy_driver_pm_action(const struct device *dev,
                                     enum pm_device_action action)
   {
           int ret;

           switch (action) {
           case PM_DEVICE_ACTION_SUSPEND:
                   ret = dummy_driver_pm_suspend(dev);
                   break;
           case PM_DEVICE_ACTION_RESUME:
                   ret = dummy_driver_pm_resume(dev);
                   break;
           case PM_DEVICE_ACTION_TURN_OFF:
                   ret = dummy_driver_pm_turn_off(dev);
                   break;
           case PM_DEVICE_ACTION_TURN_ON:
                   ret = dummy_driver_pm_turn_on(dev);
                   break;
           default:
                   ret = -EINVAL;
                   break;
           }

           return ret;
   }

   static int dummy_init(const struct device *dev)
   {
           struct dummy_driver_data *dev_data = dev->data;
           const struct dummy_driver_config *dev_config = dev->config;

           /*
            * We must ensure all devices we depend on, excluding a potential
            * power domain, are initialized.
            *
            * If CONFIG_PM_DEVICE=n, this also ensures the devices are ACTIVE.
            */
           if (!device_is_ready(dev_config->bus) ||
               !gpio_is_ready_dt(&dev_config->int_pin) ||
               !gpio_is_ready_dt(&dev_config->enable_pin)) {
                   return -ENODEV;
           }

           /* We then initialize the device driver data structure */
           gpio_init_callback(&dev_data->int_pin_callback,
                              dummy_driver_int_pin_handler,
                              BIT(dev_config->int_pin.pin));

           dev_data->dev = dev;

          /*
           * This call must be the last call of the device init function.
           * It will initialize the device's PM_DEVICE context and use the
           * dummy_driver_pm_action callback to initialize the device into
           * the appropriate state.
           */
          return pm_device_driver_init(dev, dummy_driver_pm_action);
   }

   static int dummy_deinit(const struct device *dev)
   {
           int ret;

           /*
            * This call must be the first call of the device deinit function.
            * It will use the dummy_driver_pm_action callback to move the
            * device into, or verify the device is already in, an appropriate
            * state for deinitialization, and deinitialize the device's
            * PM_DEVICE context.
            */
           ret = pm_device_driver_deinit(dev, dummy_driver_pm_action);
           if (ret) {
                   return ret;
           }

           /*
            * The device is now either SUSPENDED or OFF, all the devices this
            * device depends on have been released, and devices with persistent
            * configurations like GPIO pins have been configured to match the
            * device state.
            *
            * The device will be left in this state until a new "owner" takes
            * over.
            */

           /*
            * If we had allocated memory, DMA channels or other resources, we would
            * release them here.
            */

           return ret;
   }

   static struct dummy_driver_data data0;

   static struct dummy_driver_config config0 = {
           .bus = DEVICE_DT_GET(DT_INST_PARENT(0)),
           .int_pin = GPIO_DT_SPEC_INST_GET(0, int_gpios),
           .enable_pin = GPIO_DT_SPEC_INST_GET(0, enable_gpios),
   };

   /* Define the device's PM DEVICE context */
   PM_DEVICE_DT_INST_DEFINE(0, dummy_driver_pm_action);

   /* Define the device, pointing to the device's PM DEVICE context */
   DEVICE_DT_INST_DEINIT_DEFINE(
           0,
           &dummy_init,
           &dummy_deinit,
           PM_DEVICE_DT_INST_GET(0),
           &data0,
           &config0,
           POST_KERNEL,
           CONFIG_KERNEL_INIT_PRIORITY_DEFAULT,
           NULL
   );

支持部分设备电源管理的设备模型 (Device Model with Partial Device Power Management Support)
***********************************************************************************************

如果未启用 :kconfig:option:`CONFIG_PM_DEVICE`,则设备电源状态与设备初始化状态绑定。(If :kconfig:option:`CONFIG_PM_DEVICE` is not enabled, The device power state is tied to the devices initialization state.)

一旦设备被初始化,设备驱动程序 PM 动作钩子就会通过调用 :c:func:`pm_device_driver_init` 将设备移动到 ``ACTIVE`` 状态。遵循 ``Device actions x states`` 图和 ``OFF`` 状态的定义,这会导致调用 ``PM_DEVICE_ACTION_TURN_ON`` 后跟 ``PM_DEVICE_ACTION_RESUME``。(Once a device is initialized, the device driver PM action hook is used to move the device to the ``ACTIVE`` state through calling :c:func:`pm_device_driver_init`. Following the ``Device actions x states`` graph and the definition of the ``OFF`` state, this results in a call to ``PM_DEVICE_ACTION_TURN_ON`` followed by ``PM_DEVICE_ACTION_RESUME``.)

鉴于电源域和总线是"仅仅是设备",每个电源域和总线都会在其子设备之前恢复,因为它们根据设备树依赖序号进行初始化。当设备被初始化时,假定每个设备都已通电,并且设备所依赖的设备假定为 ``ACTIVE``。(Given power domains and buses are "just devices", every power domain and bus will be resumed before its child devices as they are initialized according to the devicetree dependency ordinals. Every device is assumed to be powered, and the devices a device depends on are assumed to be ``ACTIVE``, when device is initialized.)

一旦设备被去初始化,设备驱动程序 PM 动作钩子就会通过调用 :c:func:`pm_device_driver_deinit` 将设备移动到 ``SUSPENDED`` 状态。遵循 ``Device actions x states``,并假设电源域"始终开启",这会导致调用 ``PM_DEVICE_ACTION_SUSPEND``。(Once a device is deinitialized, the device driver PM action hook is used to move the device to the ``SUSPENDED`` state through calling :c:func:`pm_device_driver_deinit`. Following the ``Device actions x states``, and assuming power domains are "always on" this results in a call to ``PM_DEVICE_ACTION_SUSPEND``.)

.. _pm-device-shell:

Shell 命令 (Shell Commands)
****************************

可以从 shell 命令触发电源管理操作以进行测试。为此,请启用 :kconfig:option:`CONFIG_PM_DEVICE_SHELL` 选项,并从 shell 对设备发出 ``pm`` 命令,例如:(Power management actions can be triggered from shell commands for testing
purposes. To do that, enable the :kconfig:option:`CONFIG_PM_DEVICE_SHELL`
option and issue a ``pm`` command on a device from the shell, for example:

.. code-block:: console

        uart:~$ device list
        - buttons (active)
        uart:~$ pm suspend buttons
        uart:~$ device list
        devices:
        - buttons (suspended)

要打印设备的电源管理状态,请启用 :kconfig:option:`CONFIG_DEVICE_SHELL` 并使用 ``device list`` 命令,例如:(To print the power management state of a device, enable :kconfig:option:`CONFIG_DEVICE_SHELL` and use the ``device list`` command, for example:)

.. code-block:: console

        uart:~$ device list
        devices:
        - i2c@40003000 (active)
        - buttons (active, usage=1)
        - leds (READY)

在这种情况下,``leds`` 不支持 PM,``i2c`` 支持具有手动挂起和恢复操作的 PM 并且当前处于活动状态,``buttons`` 支持运行时 PM 并且当前处于活动状态,有一个用户。(In this case, ``leds`` does not support PM, ``i2c`` supports PM with manual suspend and resume actions and it's currently active, ``buttons`` supports runtime PM and it's currently active with one user.)

.. _pm-device-busy:

忙碌状态指示 (Busy Status Indication)
**************************************

当系统空闲并且 SoC 即将休眠时,电源管理子系统可以挂起设备,如 :ref:`pm-device-system-pm` 中所述。这可能会导致设备硬件丢失某些状态。挂起正在进行硬件事务的设备(例如写入闪存)可能会导致未定义的行为或不一致的状态。此 API 通过向内核指示设备正在进行操作且不应被挂起来保护此类事务。(When the system is idle and the SoC is going to sleep, the power management subsystem can suspend devices, as described in :ref:`pm-device-system-pm`. This can cause device hardware to lose some states. Suspending a device which is in the middle of a hardware transaction, such as writing to a flash memory, may lead to undefined behavior or inconsistent states. This API guards such transactions by indicating to the kernel that the device is in the middle of an operation and should not be suspended.)

当调用 :c:func:`pm_device_busy_set` 时,设备被标记为忙碌,系统将不会对其进行电源管理。当设备不再执行操作并且可以挂起后,它应该调用 :c:func:`pm_device_busy_clear`。(When :c:func:`pm_device_busy_set` is called, the device is marked as busy and the system will not do power management on it. After the device is no longer doing an operation and can be suspended, it should call :c:func:`pm_device_busy_clear`.)

.. _pm-device-constraint:

设备电源管理 X 系统电源管理 (Device Power Management X System Power Management)
**********************************************************************************

在嵌入式系统中管理电源时,了解设备电源状态和整体系统电源状态之间的相互作用至关重要。某些设备可能依赖于系统电源状态。例如,SoC 的某些低功耗状态可能不向外设供电,如果设备正在进行操作,则会导致问题。正确的协调对于维护系统稳定性和数据完整性至关重要。(When managing power in embedded systems, it's crucial to understand the interplay between device power state and the overall system power state. Some devices may have dependencies on the system power state. For example, certain low-power states of the SoC might not supply power to peripheral devices, leading to problems if the device is in the middle of an operation. Proper coordination is essential to maintain system stability and data integrity.)

为了避免此类问题,设备必须在操作期间 :ref:`获取和释放锁定 <pm-policy-power-states>` 导致电源丢失的电源状态。(To avoid this sort of problem, devices must :ref:`get and release lock <pm-policy-power-states>` power states that cause power loss during an operation.)

Zephyr provides a mechanism for devices to declare which power states cause power
loss and an API that automatically get and put lock on them. This feature is
enabled setting :kconfig:option:`CONFIG_PM_POLICY_DEVICE_CONSTRAINTS` to ``y``.

Zephyr 提供了一种机制,允许设备声明哪些电源状态会导致电源丢失,以及一个自动获取和释放它们的锁的 API。通过将 :kconfig:option:`CONFIG_PM_POLICY_DEVICE_CONSTRAINTS` 设置为 ``y`` 来启用此功能。(Zephyr provides a mechanism for devices to declare which power states cause power loss and an API that automatically get and put lock on them. This feature is enabled setting :kconfig:option:`CONFIG_PM_POLICY_DEVICE_CONSTRAINTS` to ``y``.)

一旦启用此功能,设备必须在设备树中声明哪些状态会导致电源丢失。在以下示例中,设备 ``test_dev`` 声明电源状态 ``state1`` 和 ``state2`` 会导致电源丢失。(Once this feature is enabled, devices must declare in devicetree which states cause power loss. In the following example, device ``test_dev`` says that power states ``state1`` and ``state2`` cause power loss.)

.. code-block:: devicetree

    power-states {
            state0: state0 {
                    compatible = "zephyr,power-state";
                    power-state-name = "suspend-to-idle";
                    min-residency-us = <10000>;
                    exit-latency-us = <100>;
            };

            state1: state1 {
                    compatible = "zephyr,power-state";
                    power-state-name = "standby";
                    min-residency-us = <20000>;
                    exit-latency-us = <200>;
            };

            state2: state2 {
                    compatible = "zephyr,power-state";
                    power-state-name = "suspend-to-ram";
                    min-residency-us = <50000>;
                    exit-latency-us = <500>;
            };

            state3: state3 {
                    compatible = "zephyr,power-state";
                    power-state-name = "suspend-to-ram";
                    status = "disabled";
            };
    };

    test_dev: test_dev {
            compatible = "test-device-pm";
            status = "okay";
            zephyr,disabling-power-states = <&state1 &state2>;
    };

之后,设备可以通过调用 :c:func:`pm_policy_device_power_lock_get` 锁定这些状态,并通过 :c:func:`pm_policy_device_power_lock_put` 释放。例如:(After that devices can lock these state calling :c:func:`pm_policy_device_power_lock_get` and release with :c:func:`pm_policy_device_power_lock_put`. For example:)

.. code-block:: C

    static void timer_expire_cb(struct k_timer *timer)
    {
           struct test_driver_data *data = k_timer_user_data_get(timer);

           data->ongoing = false;
           k_timer_stop(timer);
           pm_policy_device_power_lock_put(data->self);
    }

    void test_driver_async_operation(const struct device *dev)
    {
           struct test_driver_data *data = dev->data;

           data->ongoing = true;
           pm_policy_device_power_lock_get(dev);

           /** Lets set a timer big enough to ensure that any deep
            *  sleep state would be suitable but constraints will
            *  make only state0 (suspend-to-idle) will be used.
            */
           k_timer_start(&data->timer, K_MSEC(500), K_NO_WAIT);
    }

唤醒能力 (Wakeup capability)
*****************************

某些设备能够从睡眠状态唤醒系统。当设备具有此能力时,应用程序可以使用 :c:func:`pm_device_wakeup_enable` 动态启用或禁用设备上的此功能。(Some devices are capable of waking the system up from a sleep state. When a device has such capability, applications can enable or disable this feature on a device dynamically using :c:func:`pm_device_wakeup_enable`.)

可以通过在设备树中的设备节点中声明属性 ``wakeup-source`` 来在设备上设置此属性。例如,此设备树片段将 ``gpio0`` 设备设置为"唤醒"源:(This property can be set on device declaring the property ``wakeup-source`` in the device node in devicetree. For example, this devicetree fragment sets the ``gpio0`` device as a "wakeup" source:)

.. code-block:: devicetree

                gpio0: gpio@40022000 {
                        compatible = "ti,cc13xx-cc26xx-gpio";
                        reg = <0x40022000 0x400>;
                        interrupts = <0 0>;
                        status = "disabled";
                        label = "GPIO_0";
                        gpio-controller;
                        wakeup-source;
                        #gpio-cells = <2>;
                };

默认情况下,"唤醒"功能的设备在设备初始化期间不会启用此功能。应用程序可以稍后通过调用 :c:func:`pm_device_wakeup_enable` 来启用此功能。(By default, "wakeup" capable devices do not have this functionality enabled during the device initialization. Applications can enable this functionality later calling :c:func:`pm_device_wakeup_enable`.)

.. note::

   此属性 **仅** 由系统电源管理用于识别不应被挂起的设备。驱动程序或应用程序有责任执行设备支持它所需的任何其他配置。(This property is **only** used by the system power management to identify devices that should not be suspended. It is responsibility of driver or the application to do any additional configuration required by the device to support it.)

示例 (Examples)
****************

一些展示设备电源管理功能的有用示例:(Some helpful examples showing device power management features:)

* :zephyr_file:`samples/subsys/pm/device_pm/`
* :zephyr_file:`tests/subsys/pm/power_mgmt/`
* :zephyr_file:`tests/subsys/pm/device_wakeup_api/`
* :zephyr_file:`tests/subsys/pm/device_driver_init/`
