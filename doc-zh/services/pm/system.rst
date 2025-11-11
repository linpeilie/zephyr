.. _pm-system:

系统电源管理 (System Power Management)
#######################################

简介 (Introduction)
********************

当内核没有可调度的任务时,它进入空闲状态。启用 :kconfig:option:`CONFIG_PM` 允许内核调用电源管理子系统,将空闲系统置于支持的电源状态之一。内核请求它希望挂起的时间量,然后 PM 子系统根据配置的电源管理策略决定要转换到的适当电源状态。(The kernel enters the idle state when it has nothing to schedule. Enabling :kconfig:option:`CONFIG_PM` allows the kernel to call upon the power management subsystem to put an idle system into one of the supported power states. The kernel requests an amount of time it would like to suspend, then the PM subsystem decides the appropriate power state to transition to based on the configured power management policy.)

设置唤醒事件是应用程序的责任。唤醒事件通常是由 SoC 外设模块触发的中断。示例包括 SysTick、RTC、计数器或 GPIO。请记住,根据 SoC 和所讨论的电源模式,并非所有外设都可能处于活动状态,因此某些唤醒源可能无法在所有电源模式下使用。(It is the application's responsibility to set up a wake-up event. A wake-up event will typically be an interrupt triggered by an SoC peripheral module. Examples include a SysTick, RTC, counter, or GPIO. Keep in mind that depending on the SoC and the power mode in question, not all peripherals may be active, and therefore some wake-up sources may not be usable in all power modes.)

以下图表描述了系统电源管理:(The following diagram describes system power management:)

.. graphviz::
   :caption: System power management

   digraph G {
       compound=true
       node [height=1.2 style=rounded]

       lock [label="Lock interruptions"]
       config_pm [label="CONFIG_PM" shape=diamond style="rounded,dashed"]
       forced_state [label="state forced ?", shape=diamond style="rounded,dashed"]
       config_system_managed_device_pm [label="CONFIG_PM_DEVICE" shape=diamond style="rounded,dashed"]
       config_system_managed_device_pm2 [label="CONFIG_PM_DEVICE" shape=diamond style="rounded,dashed"]
       pm_policy [label="Check policy manager\nfor a power state "]
       pm_suspend_devices [label="Suspend\ndevices"]
       pm_resume_devices [label="Resume\ndevices"]
       pm_state_set [label="Change power state\n(SoC API)" style="rounded,bold"]
       pm_system_resume [label="Finish wake-up\n(SoC API)\n(restore interruptions)" style="rounded,bold"]
       k_cpu_idle [label="k_cpu_idle()"]

       subgraph cluster_0 {
              style=invisible;
              lock -> config_pm
       }

       subgraph cluster_1 {
                style=dashed
                label = "pm_system_suspend()"

                forced_state -> config_system_managed_device_pm [label="yes"]
                forced_state -> pm_policy [label="no"]
                pm_policy -> config_system_managed_device_pm
                config_system_managed_device_pm -> pm_state_set:e [label="no"]
                config_system_managed_device_pm -> pm_suspend_devices [label="yes"]
                pm_suspend_devices -> pm_state_set
                pm_state_set -> config_system_managed_device_pm2
                config_system_managed_device_pm2 -> pm_resume_devices [label="yes"]
                config_system_managed_device_pm2 -> pm_system_resume [label="no"]
                pm_resume_devices -> pm_system_resume
        }

        {rankdir=LR k_cpu_idle; forced_state}
        pm_policy -> k_cpu_idle [label="PM_STATE_ACTIVE\n(no power state meet requirements)"]
        config_pm -> k_cpu_idle [label="no"]
        config_pm -> forced_state [label="yes" lhead="cluster_1"]
        pm_system_resume:e -> lock:e [constraint=false lhed="cluster_0"]
   }


电源状态 (Power States)
========================

电源管理子系统定义了一组状态,这些状态由与每个状态相关的功耗和上下文保留来描述。(The power management subsystem defines a set of states described by the power consumption and context retention associated with each of them.)

电源状态集由 :c:enum:`pm_state` 定义。通常,较低的电源状态(枚举中的较高索引)将提供更大的节能效果,但具有更高的唤醒延迟。(The set of power states is defined by :c:enum:`pm_state`. In general, lower power states (higher index in the enum) will offer greater power savings and have higher wake latencies.)

电源管理策略 (Power Management Policies)
=========================================

电源管理子系统支持以下电源管理策略:(The power management subsystem supports the following power management policies:)

* 基于驻留时间 (Residency based)
* 应用程序定义 (Application defined)

策略管理器是电源管理子系统的组件,负责决定系统应该转换到哪个电源状态。策略管理器只能在为平台定义的状态之间进行选择。对决策施加的其他约束可能包括禁止某些电源状态的锁,或根据策略的各种最小和最大延迟值。(The policy manager is the component of the power management subsystem responsible for deciding which power state the system should transition to. The policy manager can only choose between states that have been defined for the platform. Other constraints placed upon the decision may include locks disallowing certain power states, or various kinds of minimum and maximum latency values, depending on the policy.)

有关状态定义的更多详细信息,请参阅 :dtcompatible:`zephyr,power-state` 绑定文档。(More details on the states definition can be found in the :dtcompatible:`zephyr,power-state` binding documentation.)

驻留时间 (Residency)
---------------------

在驻留策略下,系统将进入提供最高节能效果的电源状态,约束条件是最小驻留值(参见 :dtcompatible:`zephyr,power-state`)与退出模式的延迟之和必须小于或等于内核调度的系统空闲时间持续时间。(Under the residency policy, the system will enter the power state which offers the highest power savings, with the constraint that the sum of the minimum residency value (see :dtcompatible:`zephyr,power-state`) and the latency to exit the mode must be less than or equal to the system idle time duration scheduled by the kernel.)

因此,核心逻辑可以用以下表达式总结:(Thus the core logic can be summarized with the following expression:)

.. code-block:: c

   if (time_to_next_scheduled_event >= (state.min_residency_us + state.exit_latency)) {
      return state
   }

应用程序 (Application)
-----------------------

应用程序通过实现 :c:func:`pm_policy_next_state` 函数来定义电源管理策略。在此策略中,应用程序可以根据到下一个计划超时的剩余时间自由决定系统应该转换到哪个电源状态。(The application defines the power management policy by implementing the :c:func:`pm_policy_next_state` function. In this policy, the application is free to decide which power state the system should transition to based on the remaining time until the next scheduled timeout.)

定义自己策略的应用程序示例可以在 :zephyr_file:`tests/subsys/pm/power_mgmt/` 中找到。(An example of an application that defines its own policy can be found in :zephyr_file:`tests/subsys/pm/power_mgmt/`.)

.. _pm-policy-power-states:

策略和电源状态 (Policy and Power States)
-----------------------------------------

电源管理子系统允许不同的 Zephyr 组件和应用程序配置策略管理器,以阻止系统转换到某些电源状态。当在后台执行任务时,设备可以使用此功能来防止系统进入会丢失上下文的特定状态。请参阅 :c:func:`pm_policy_state_lock_get`。(The power management subsystem allows different Zephyr components and applications to configure the policy manager to block the system from transitioning into certain power states. This can be used by devices when executing tasks in background to prevent the system from going to a specific state where it would lose context. See :c:func:`pm_policy_state_lock_get`.)

示例 (Examples)
================

一些展示不同电源管理功能的有用示例:(Some helpful examples showing different power management features:)

* :zephyr_file:`samples/boards/st/power_mgmt/blinky/`
* :zephyr_file:`samples/boards/espressif/deep_sleep/`
* :zephyr_file:`samples/subsys/pm/device_pm/`
* :zephyr_file:`tests/subsys/pm/power_mgmt/`
* :zephyr_file:`tests/subsys/pm/power_mgmt_soc/`
* :zephyr_file:`tests/subsys/pm/power_states_api/`
