.. _pm-device-runtime:

设备运行时电源管理 (Device Runtime Power Management)
######################################################

简介 (Introduction)
********************

设备运行时电源管理 (PM) 框架是一种主动电源管理机制,通过挂起空闲或未使用的设备来降低整体系统功耗,而与系统状态无关。可以通过设置 :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME` 来启用它。在此模型中,设备驱动程序负责指示何时需要设备以及何时不需要。此信息用于根据使用计数确定何时挂起或恢复设备。(The device runtime power management (PM) framework is an active power management mechanism which reduces the overall system power consumption by suspending the devices which are idle or not used independently of the system state. It can be enabled by setting :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME`. In this model the device driver is responsible to indicate when it needs the device and when it does not. This information is used to determine when to suspend or resume a device based on usage count.)

在设备上启用设备运行时电源管理时,其状态将最初设置为 :c:enumerator:`PM_DEVICE_STATE_SUSPENDED`,表示未使用。在第一次设备请求时,它将被恢复并因此进入 :c:enumerator:`PM_DEVICE_STATE_ACTIVE` 状态。设备将保持在此状态,直到不再使用。此时,设备将被挂起,直到下一次设备请求。如果同步执行挂起,设备将立即进入 :c:enumerator:`PM_DEVICE_STATE_SUSPENDED` 状态,而如果异步执行,它将首先进入 :c:enumerator:`PM_DEVICE_STATE_SUSPENDING` 状态,然后在执行操作时进入 :c:enumerator:`PM_DEVICE_STATE_SUSPENDED` 状态。(When device runtime power management is enabled on a device, its state will be initially set to a :c:enumerator:`PM_DEVICE_STATE_SUSPENDED` indicating it is not used. On the first device request, it will be resumed and so put into the :c:enumerator:`PM_DEVICE_STATE_ACTIVE` state. The device will remain in this state until it is no longer used. At this point, the device will be suspended until the next device request. If the suspension is performed synchronously the device will be immediately put into the :c:enumerator:`PM_DEVICE_STATE_SUSPENDED` state, whereas if it is performed asynchronously, it will be put into the :c:enumerator:`PM_DEVICE_STATE_SUSPENDING` state first and then into the :c:enumerator:`PM_DEVICE_STATE_SUSPENDED` state when the action is run.)

对于电源域上的设备(通过设备树 'power-domains' 属性),设备运行时电源管理会自动尝试请求和释放依赖域,以响应子设备上的 :c:func:`pm_device_runtime_get` 和 :c:func:`pm_device_runtime_put` 调用。(For devices on a power domain (via the devicetree 'power-domains' property), device runtime power management automatically attempts to request and release the dependent domain in response to :c:func:`pm_device_runtime_get` and :c:func:`pm_device_runtime_put` calls on the child device.)

要使前者自动控制电源域状态,必须在电源域设备上启用设备运行时 PM。要全局启用设备运行时 PM,请启用 :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_DEFAULT_ENABLE`。要仅为选定的设备启用设备运行时 PM,请设置 ``zephyr,pm-device-runtime-auto`` 设备树属性,或为选定的设备使用 :c:func:`pm_device_runtime_enable`。(For the previous to automatically control the power domain state, device runtime PM must be enabled on the power domain device. To enable device runtime PM globally, enable :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_DEFAULT_ENABLE`. To enable device runtime PM only for select devices, set the ``zephyr,pm-device-runtime-auto`` devicetree property, or use :c:func:`pm_device_runtime_enable` for the select devices.)

.. graphviz::
   :caption: Device states and transitions

    digraph {
        node [shape=box];
        init [shape=point];

        SUSPENDED [label=PM_DEVICE_STATE_SUSPENDED];
        ACTIVE [label=PM_DEVICE_STATE_ACTIVE];
        SUSPENDING [label=PM_DEVICE_STATE_SUSPENDING];

        init -> SUSPENDED;
        SUSPENDED -> ACTIVE;
        ACTIVE -> SUSPENDED;
        ACTIVE -> SUSPENDING [constraint=false]
        SUSPENDING -> SUSPENDED [constraint=false];
        SUSPENDED -> SUSPENDING [style=invis];
        SUSPENDING -> ACTIVE [style=invis];
    }

设备运行时电源管理框架旨在以最少的应用程序工作最小化设备功耗。设备驱动程序负责指示何时需要设备以及何时不需要。因此,应用程序无法手动挂起或恢复设备。但是,应用程序可以决定何时禁用或启用设备的运行时电源管理。例如,如果应用程序希望特定设备始终处于活动状态,这可能很有用。(The device runtime power management framework has been designed to minimize devices power consumption with minimal application work. Device drivers are responsible for indicating when they need the device to be operational and when they do not. Therefore, applications can not manually suspend or resume a device. An application can, however, decide when to disable or enable runtime power management for a device. This can be useful, for example, if an application wants a particular device to be always active.)

设计原则 (Design principles)
*****************************

在设备上启用运行时 PM 时,它将不再在系统电源转换期间恢复或挂起。相反,设备完全负责指示何时需要设备以及何时不需要。设备运行时 PM API 使用引用计数来跟踪设备的使用情况。这允许 API 确定何时需要恢复或挂起设备。API 使用 *get* 和 *put* 术语来指示何时需要设备或不需要。当我们考虑设备依赖关系时,此机制起着关键作用。例如,如果多个传感器使用总线设备,我们可以保持总线处于活动状态,直到最后一个传感器使用完毕。(When runtime PM is enabled on a device it will no longer be resumed or suspended during system power transitions. Instead, the device is fully responsible to indicate when it needs a device and when it does not. The device runtime PM API uses reference counting to keep track of device's usage. This allows the API to determine when a device needs to be resumed or suspended. The API uses the *get* and *put* terminology to indicate when a device is needed or not, respectively. This mechanism plays a key role when we account for device dependencies. For example, if a bus device is used by multiple sensors, we can keep the bus active until the last sensor has finished using it.)

.. note::

    截至目前,设备运行时电源管理 API 不管理设备依赖关系。这实际上意味着,如果设备依赖于其他设备来运行(例如,传感器可能依赖于总线设备),则总线将在每次事务时恢复和挂起。通常,当使用子设备时保持父设备处于活动状态会更高效,因为子设备可能在短时间内执行多个事务。在添加此功能之前,设备可以手动 *get* 或 *put* 它们的依赖项。(As of today, the device runtime power management API does not manage device dependencies. This effectively means that, if a device depends on other devices to operate (e.g. a sensor may depend on a bus device), the bus will be resumed and suspended on every transaction. In general, it is more efficient to keep parent devices active when their children are used, since the children may perform multiple transactions in a short period of time. Until this feature is added, devices can manually *get* or *put* their dependencies.)

设备驱动程序可以使用 :c:func:`pm_device_runtime_get` 函数来指示它 *需要* 设备处于活动或操作状态。此函数将增加设备使用计数并在必要时恢复设备。类似地,:c:func:`pm_device_runtime_put` 函数可用于指示不再需要设备。此函数将减少设备使用计数并在必要时挂起设备。值得注意的是,在这两种情况下,操作都是同步执行的。下面显示的序列图说明了设备如何使用此 API 以及预期的事件序列。(The :c:func:`pm_device_runtime_get` function can be used by a device driver to indicate it *needs* the device to be active or operational. This function will increase device usage count and resume the device if necessary. Similarly, the :c:func:`pm_device_runtime_put` function can be used to indicate that the device is no longer needed. This function will decrease the device usage count and suspend the device if necessary. It is worth to note that in both cases, the operation is carried out synchronously. The sequence diagram shown below illustrates how a device can use this API and the expected sequence of events.)

.. figure:: images/devr-sync-ops.svg

    单个设备上的同步操作 (Synchronous operation on a single device)

同步模型非常简单。但是,它可能会引入不必要的延迟,因为应用程序在设备挂起之前不会获得操作结果(如果设备不再使用)。如果操作很快,例如寄存器切换,这可能不是问题。但是,如果挂起涉及通过慢速总线发送数据包,情况就不一样了。因此,设备驱动程序还可以使用 :c:func:`pm_device_runtime_put_async` 函数。如果设备不再使用,此函数将再次调度挂起操作。(The synchronous model is as simple as it gets. However, it may introduce unnecessary delays since the application will not get the operation result until the device is suspended (in case device is no longer used). It will likely not be a problem if the operation is fast, e.g. a register toggle. However, the situation will not be the same if suspension involves sending packets through a slow bus. For this reason the device drivers can also make use of the :c:func:`pm_device_runtime_put_async` function. This function will schedule the suspend operation, again, if device is no longer used.)


默认情况下,运行时 PM 操作被卸载到系统工作队列。但是,设备驱动程序在挂起期间不得执行任何阻塞操作,因为这可能会阻塞系统工作队列并对系统响应性产生负面影响。(By default, runtime PM operations are offloaded to the system work queue. However, device drivers must not perform any blocking operations during suspend, as this can stall the system work queue and negatively impact system responsiveness.)

为了解决这个问题,应用程序可以通过启用 :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_USE_DEDICATED_WQ` 来配置运行时 PM 使用专用工作队列。(To address this, applications can configure runtime PM to use a dedicated work queue by enabling :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_USE_DEDICATED_WQ`.)

如果需要阻塞行为——例如,访问慢速外设或等待总线事务时——则必须改用 PM 子系统工作队列。需要此行为的驱动程序可以通过启用 :kconfig:option:`CONFIG_PM_DEVICE_DRIVER_NEEDS_DEDICATED_WQ` 来明确请求它。(If blocking behavior is required—for example, when accessing a slow peripheral or waiting for a bus transaction—the PM subsystem work queue must be used instead. Drivers that require this behavior can explicitly request it by enabling :kconfig:option:`CONFIG_PM_DEVICE_DRIVER_NEEDS_DEDICATED_WQ`.)

对于不需要异步操作的资源受限目标,可以通过取消选择 :kconfig:option:`CONFIOG_PM_DEVICE_RUNTIME_ASYNC` 来完全禁用此功能,从而减少内存使用和系统复杂性。(For targets with constrained resources that do not need asynchronous operations, this functionality can be disabled altogether by de-selecting :kconfig:option:`CONFIOG_PM_DEVICE_RUNTIME_ASYNC`, reducing memory usage and system complexity.)


.. figure:: images/devr-async-ops.svg

    单个设备上的异步操作 (Asynchronous operation on a single device)

实现指南 (Implementation guidelines)
************************************

首先,设备驱动程序需要实现 PM 子系统用于挂起或恢复设备的 PM 动作回调。(In a first place, a device driver needs to implement the PM action callback used by the PM subsystem to suspend or resume devices.)

.. code-block:: c

    static int mydev_pm_action(const struct device *dev,
                               enum pm_device_action action)
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
        default:
            return -ENOTSUP;
        }

        return 0;
    }

PM 动作回调调用由 PM 子系统序列化,因此不需要特殊的同步。(The PM action callback calls are serialized by the PM subsystem, therefore, no special synchronization is required.)

要在设备上启用设备运行时电源管理,驱动程序需要在初始化时调用 :c:func:`pm_device_runtime_enable`。请注意,如果设备状态为 :c:enumerator:`PM_DEVICE_STATE_ACTIVE`,此函数将挂起设备。如果设备在物理上被挂起,init 函数应在调用 :c:func:`pm_device_runtime_enable` 之前调用 :c:func:`pm_device_init_suspended`。(To enable device runtime power management on a device, the driver needs to call :c:func:`pm_device_runtime_enable` at initialization time. Note that this function will suspend the device if its state is :c:enumerator:`PM_DEVICE_STATE_ACTIVE`. In case the device is physically suspended, the init function should call :c:func:`pm_device_init_suspended` before calling :c:func:`pm_device_runtime_enable`.)

.. code-block:: c

    /* device driver initialization function */
    static int mydev_init(const struct device *dev)
    {
        int ret;
        ...

        /* OPTIONAL: mark device as suspended if it is physically suspended */
        pm_device_init_suspended(dev);

        /* enable device runtime power management */
        ret = pm_device_runtime_enable(dev);
        if ((ret < 0) && (ret != -ENOSYS)) {
            return ret;
        }
    }

也可以通过在相应的设备树节点上添加 ``zephyr,pm-device-runtime-auto`` 标志来自动在设备实例上启用设备运行时电源管理。如果启用,在设备的 ``init`` 函数运行并成功返回后,会立即调用 :c:func:`pm_device_runtime_enable`。(Device runtime power management can also be automatically enabled on a device instance by adding the ``zephyr,pm-device-runtime-auto`` flag onto the corresponding devicetree node. If enabled, :c:func:`pm_device_runtime_enable` is called immediately after the ``init`` function of the device runs and returns successfully.)

.. code-block:: dts

    foo {
        /* ... */
        zephyr,pm-device-runtime-auto;
    };

假设一个实现 ``operation`` API 调用的示例设备驱动程序,可以按如下方式执行 *get* 和 *put* 操作:(Assuming an example device driver that implements an ``operation`` API call, the *get* and *put* operations could be carried out as follows:)

.. code-block:: c

    static int mydev_operation(const struct device *dev)
    {
        int ret;

        /* "get" device (increases usage count, resumes device if suspended) */
        ret = pm_device_runtime_get(dev);
        if (ret < 0) {
            return ret;
        }

        /* do something with the device */
        ...

        /* "put" device (decreases usage count, suspends device if no more users) */
        return pm_device_runtime_put(dev);
    }

如果挂起操作 *缓慢*,设备驱动程序可以使用异步 API:(In case the suspend operation is *slow*, the device driver can use the asynchronous API:)

.. code-block:: c

    static int mydev_operation(const struct device *dev)
    {
        int ret;

        /* "get" device (increases usage count, resumes device if suspended) */
        ret = pm_device_runtime_get(dev);
        if (ret < 0) {
            return ret;
        }

        /* do something with the device */
        ...

        /* "put" device (decreases usage count, schedule suspend if no more users) */
        return pm_device_runtime_put_async(dev, K_NO_WAIT);
    }

示例 (Examples)
****************

一些展示设备运行时电源管理功能的有用示例:(Some helpful examples showing device runtime power management features:)

* :zephyr_file:`tests/subsys/pm/device_runtime_api/`
* :zephyr_file:`tests/subsys/pm/device_power_domains/`
* :zephyr_file:`tests/subsys/pm/power_domain/`
