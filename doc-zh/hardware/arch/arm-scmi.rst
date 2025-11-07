.. _arm_scmi:

ARM 系统控制和管理接口
#######################

概述 (Overview)
****************

什么是 SCMI?
************

系统控制和管理接口 (System Control and Management Interface, SCMI) 是由
ARM 开发的规范,它描述了一组与操作系统无关的软件接口,用于执行系统管理
(例如:时钟控制、引脚控制等)。


代理、平台、协议和传输 (Agent, platform, protocol and transport)
*****************************************************************

SCMI 规范定义了 **四个** 关键术语,这些术语也将在本文档中使用:

	#. 代理 (Agent)
		执行 SCMI 请求的实体(例如:门控时钟或配置引脚)。在此上下文中,
		Zephyr 本身就是一个代理。
	#. 平台 (Platform)
		这是指一组硬件组件,用于处理来自代理的请求并提供必要的功能。
		在某些情况下,请求由运行在专用于执行系统管理任务的核心上的固件处理。
	#. 协议 (Protocol)
		协议是按功能分组的一组消息。直观地说,消息可以被视为远程过程调用。

		SCMI 规范定义了十个标准协议:

		#. **基础协议** (0x10)
		#. **电源域管理** (0x11)
		#. **系统电源管理** (0x12)
		#. **性能域管理** (0x13)
		#. **时钟管理** (0x14)
		#. **传感器管理** (0x15)
		#. **复位域管理** (0x16)
		#. **电压域管理** (0x17)
		#. **功耗上限和监控** (0x18)
		#. **引脚控制** (0x19)

		其中每个协议都由唯一的协议 ID 标识(列在括号中)。

		除了标准协议外,SCMI 规范还为特定供应商的协议保留了
		**0x80-0xFF** 协议 ID 范围。


	#. 传输 (Transport)
		这描述了代理和平台之间如何交换消息。通信本身通过通道进行。

.. note::
	一个系统可能有多个代理。

通道 (Channels)
***************

**通道** 是代理和平台交换消息的媒介。通道的结构及其工作方式完全取决于传输方式。

每个代理都有自己独立的通道集,这意味着例如某个通道 A 不能被两个不同的代理使用。

通道是 **双向的**(例外:FastChannels),并且根据哪个实体发起通信,
可以是以下 **两种** 类型之一:

	#. A2P (代理到平台, agent to platform)
		代理是发起者/请求者。通过这些通道传递的消息称为 **命令**。
	#. P2A (平台到代理, platform to agent)
		平台是发起者/请求者。

消息 (Messages)
***************

SCMI 规范定义了 **四种** 消息类型:

	#. 同步 (Synchronous)
		这些命令会阻塞,直到平台完成所请求的工作,并通过 A2P 通道发送。
	#. 异步 (Asynchronous)
		对于这些命令,平台会将请求的工作安排在稍后执行。因此,它们几乎立即返回。
		这些命令通过 A2P 通道发送。
	#. 延迟响应 (Delayed response)
		这些消息指示与异步命令相关联的工作已完成。这些通过 P2A 通道发送。

	#. 通知 (Notification)
		这些消息用于通知代理平台上发生的事件。这些通过 P2A 通道发送。

Zephyr 对 SCMI 的支持基于 ARM 提供的文档:
`DEN0056E <https://developer.arm.com/documentation/den0056/latest/>`_。有关规范的
更多详细信息,建议读者查阅该文档。

Zephyr 中的 SCMI 支持
**********************

基于共享内存和门铃的传输 (Shared memory and doorbell-based transport)
**********************************************************************

这种传输形式使用共享内存来读/写消息,使用门铃进行信号传递。与共享内存区域的
交互通过驱动程序 (:file:`drivers/firmware/scmi/shmem.c`) 执行,该驱动程序为
此目的提供了一组函数。此外,信号传递使用 Zephyr MBOX API 执行(仅信号模式,
无消息传递)。

与共享内存区域的交互和信号传递由传输 API 抽象,该 API 由基于共享内存和门铃的
传输驱动程序 (:file:`drivers/firmware/scmi/mailbox.c`) 实现。

以下步骤示例说明了使用此传输方式时 Zephyr 代理和平台之间如何进行通信:

	#. 将消息写入共享内存区域。
	#. Zephyr 响铃请求门铃。如果处于 ``PRE_KERNEL_1`` 或 ``PRE_KERNEL_2`` 阶段,则开始轮询回复,否则等待回复门铃响铃。
	#. 平台从共享内存区域读取消息,处理它,将回复写回同一区域并响铃回复门铃。
	#. Zephyr 从共享内存区域读取回复。

在此传输的上下文中,一个通道由 **单个** 共享内存区域和一个或多个邮箱通道组成。
这是因为用户可能需要/想要为请求/回复门铃使用不同的邮箱通道。


协议 (Protocols)
*****************

目前,Zephyr 支持以下标准协议:

	#. **电源域管理**
	#. **时钟管理**
	#. **引脚控制**

NXP 特定协议:
	#. **CPU 域管理**

电源域管理 (Power domain management)
*************************************

此协议用于管理电源域的电源状态。这通过实现各种命令的一组函数来完成,
例如 ``POWER_STATE_GET`` 和 ``POWER_STATE_SET``。

.. note::
	此驱动程序与供应商无关。因此,它可以在任何使用 SCMI 进行电源域
	管理操作的系统上使用。

时钟管理协议 (Clock management protocol)
****************************************

此协议用于执行时钟管理操作。这通过驱动程序
(:file:`drivers/clock_control/clock_control_arm_scmi.c`) 完成,该驱动程序
实现了 Zephyr 时钟控制子系统 API。因此,从用户的角度来看,使用此驱动程序
与使用任何其他时钟管理驱动程序没有区别。

.. note::
	此驱动程序与供应商无关。因此,它可以在任何使用 SCMI 进行时钟
	管理操作的系统上使用。

引脚控制协议 (Pin Control protocol)
************************************

此协议用于执行引脚配置操作。这通过实现各种命令的一组函数来完成。
目前,唯一支持的命令是 ``PINCTRL_SETTINGS_CONFIGURE``。

.. note::
	对此协议的支持 **不包括** :code:`pinctrl_configure_pins` 函数的定义。
	每个供应商都应该使用自己的 :code:`pinctrl_configure_pins` 定义,
	该定义应该调用实现 ``PINCTRL_SETTINGS_CONFIGURE`` 命令的 SCMI
	引脚控制协议函数。

NXP - CPU 域管理
*****************

此协议用于管理 CPU 状态。这通过实现各种命令的一组函数来完成,
例如 ``CPU_SLEEP_MODE_SET``。

.. note::
	此驱动程序是 NXP 特定的。因此,它只能在使用 SCMI 进行 CPU 域
	管理操作的 NXP 系统上使用。

启用 SCMI 支持 (Enabling the SCMI support)
******************************************

要使用 SCMI 支持,每个供应商都需要添加一个 ``scmi`` 设备树节点
(用于传输驱动程序绑定)以及在 ``scmi`` 节点下为每个支持的协议添加一个
``protocol`` 节点。

.. note::
	Zephyr 不支持协议发现。因此,如果用户为某个协议添加了设备树节点,
	则假定平台支持该协议。

下面的示例展示了如何配置设备树以使用 SCMI 支持。假设唯一需要的协议是
时钟管理协议。

.. code-block:: devicetree

	#include <mem.h>

	#define MY_CLOCK_CONSUMER_CLK_ID 123

	scmi_res0: memory@cafebabe {
		/* 使用共享内存驱动程序时是必需的 */
		compatible = "arm,scmi-shmem";
		reg = <0xcafebabe DT_SIZE_K(1)>;
	};

	scmi {
		/* 基于共享内存和门铃的传输的 compatible */
		compatible = "arm,scmi";

		/* 一个 SCMI 通道 => A2P/transmit 通道 */
		shmem = <&scmi_res0>;

		/* 两个邮箱通道 */
		mboxes = <&my_mbox_ip 0>, <&my_mbox_ip 1>;
		mbox-names = "tx", "tx_reply";

		scmi_clk: protocol@14 {
			compatible = "arm,scmi-clock";

			/* 匹配时钟管理协议 ID */
			reg = <0x14>;

			/* 与供应商无关 - 始终为 1 */
			#clock-cells = <1>;
		};
	};

	my_mbox_ip: mailbox@deadbeef {
		compatible = "vnd,mbox-ip";
		reg = <0xdeadbeef DT_SIZE_K(1)>;
		#mbox-cells = <1>;
	};

	my_clock_consumer_ip: serial@12345678 {
		compatible = "vnd,consumer-ip";
		reg = <0x12345678 DT_SIZE_K(1)>;
		/* 时钟 ID 是供应商特定的 */
		clocks = <&scmi_clk MY_CLOCK_CONSUMER_CLK_ID>;
	};


最后,剩下的工作就是启用 :kconfig:option:`CONFIG_ARM_SCMI`。
