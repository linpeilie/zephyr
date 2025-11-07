.. _edac_ibecc:

带内纠错码 (In Band Error Correction Code, IBECC)
#################################################

概述 (Overview)
****************

该机制最初在 Intel Elkhart Lake SOC 和后续开发板中发现，
是一个带有 IBECC 的集成内存控制器。

带内纠错码(IBECC)通过提供错误检测和纠正来提高可靠性。
IBECC 可以为物理内存空间的全部或特定区域工作。
IBECC 对于不支持带外 ECC 的内存技术非常有用。

IBECC 会增加 1/32 的内存开销。此内存不可访问，
用于存储 ECC 校验数据。IBECC 将读/写事务转换为两个独立的事务：
一个用于实际数据，另一个用于包含 ECC 值的缓存行。

有一个调试功能 IBECC 错误注入，可帮助调试和验证 IBECC 功能。
ECC 错误在写路径上注入，并在读路径上导致 ECC 错误。

IBECC 配置 (IBECC Configuration)
*********************************

Bootloader 可以选择三种 IBECC 操作模式。它们列在下面:

* OPERATION_MODE = 0x0 将功能模式设置为根据地址范围保护请求

* OPERATION_MODE = 0x1 将功能模式设置为所有请求都不受保护并忽略范围检查

* OPERATION_MODE = 0x2 将功能模式设置为保护所有请求并忽略范围检查

IBECC 操作模式通过 BIOS 或 Bootloader 配置。
对于操作模式 0，还有更多 BIOS 配置选项，例如内存区域。

由于存在高安全风险，不应为生产启用错误注入功能。
错误注入仅为测试启用。

IBECC 日志记录 (IBECC Logging)
*******************************

IBECC 记录以下字段:

* 错误地址 (Error Address)

* 错误校验 (Error Syndrome)

* 错误类型 (Error Type)

  * 可纠正错误(CE) - 错误由 IBECC 模块检测和纠正。

  * 不可纠正错误(UE) - 错误由 IBECC 模块检测但未自动纠正。

IBECC 驱动程序为更高级别的应用程序提供错误类型，
以实现处理这些内存错误的所需策略。
错误校验在 IBECC 驱动程序中不使用，但提供给更高级别的应用程序。

使用说明 (Usage notes)
***********************

需要格外小心不可屏蔽中断(NMI)。NMI 会在任何时候到达，
即使本地 CPU 已禁用中断。这意味着没有锁定机制可以保护代码免受 NMI 的影响。
Zephyr 的 IPC 机制普遍使用本地 IRQ 锁定作为所有更高级别同步原语的基础层。
因此，您不能与 NMI 共享任何受锁"保护"的内容，因为保护不起作用。
在 Zephyr API 中，您可以使用的唯一对 NMI 有效的同步工具是原子层。
这也适用于由 NMI 处理程序调用的回调函数。

配置选项 (Configuration option)
********************************

相关配置选项:

* :kconfig:option:`CONFIG_EDAC_IBECC`
