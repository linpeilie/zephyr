可信固件-M 集成 (Trusted Firmware-M Integration)
################################################

可信固件-M (TF-M) 部分包含有关 TF-M 与 Zephyr RTOS 之间集成的信息。使用此信息可帮助理解如何将 TF-M 与 Zephyr 集成到 Cortex-M 平台,并在 Zephyr 应用程序中使用其安全运行时服务 (The Trusted Firmware-M (TF-M) section contains information about the
integration between TF-M and Zephyr RTOS. Use this information to help
understand how to integrate TF-M with Zephyr for Cortex-M platforms and make
use of its secure run-time services in Zephyr applications)。

开发板定义 (Board Definitions)
*******************************

如果 :kconfig:option:`CONFIG_BUILD_WITH_TFM` 标志设置为 ``y``,TF-M 将与 Zephyr 一起为安全处理环境构建 (TF-M will be built for the secure processing environment along with Zephyr if
the :kconfig:option:`CONFIG_BUILD_WITH_TFM` flag is set to ``y``)。

但是,通常不应在应用程序级别设置此值,TF-M 所需的所有配置标志都应在带有 ``_ns`` 后缀的开发板变体中设置 (Generally, this value should never be set at the application level, however,
and all config flags required for TF-M should be set in a board variant with
the ``_ns`` suffix)。

此开发板变体必须定义适当的 flash、SRAM 和外设配置,以考虑安全处理环境中的初始化过程。还必须通过 `modules/trusted-firmware-m/Kconfig.tfm <https://github.com/zephyrproject-rtos/zephyr/blob/main/modules/trusted-firmware-m/Kconfig.tfm>`__ 将 :kconfig:option:`CONFIG_TFM_BOARD` 设置为 TF-M 为此目标期望的开发板名称,以便它知道要为安全处理环境构建哪个目标 (This board variant must define an appropriate flash, SRAM and peripheral
configuration that takes into account the initialisation process in the secure
processing environment. :kconfig:option:`CONFIG_TFM_BOARD` must also be set via
`modules/trusted-firmware-m/Kconfig.tfm <https://github.com/zephyrproject-rtos/zephyr/blob/main/modules/trusted-firmware-m/Kconfig.tfm>`__
to the board name that TF-M expects for this target, so that it knows which
target to build for the secure processing environment)。

示例 (Example):``mps2/an521/cpu0/ns``
======================================

``mps2/an521/cpu0`` 开发板目标是一个双核 Arm Cortex-M33 评估板,生成安全的 Zephyr 二进制文件 (The ``mps2/an521/cpu0`` board target is a dual-core Arm Cortex-M33 evaluation board that generates
a secure Zephyr binary)。

然而,可选的 ``mps2/an521/cpu0/ns`` 开发板目标设置了这些额外的 kconfig 标志,指示 Zephyr 应作为非安全映像构建,与 TF-M 作为外部项目链接,并可选地与安全引导加载程序链接 (The optional ``mps2/an521/cpu0/ns`` board target, however, sets these additional
kconfig flags that indicate that Zephyr should be built as a
non-secure image, linked with TF-M as an external project, and optionally the
secure bootloader):

* :kconfig:option:`CONFIG_TRUSTED_EXECUTION_NONSECURE` ``y``
* :kconfig:option:`CONFIG_ARM_TRUSTZONE_M` ``y``

比较 :zephyr_file:`boards/arm/mps2/mps2_an521_cpu0.dts` 和 :zephyr_file:`boards/arm/mps2/mps2_an521_cpu0_ns.dts` 文件,我们可以看到 ``ns`` 版本在 flash 和 SRAM 内存中定义了偏移量,为 TF-M 和安全引导加载程序留出了所需的空间 (Comparing the :zephyr_file:`boards/arm/mps2/mps2_an521_cpu0.dts` and
:zephyr_file:`boards/arm/mps2/mps2_an521_cpu0_ns.dts` files,
we can see that the ``ns`` version defines offsets in flash and SRAM memory, which leave
the required space for TF-M and the secure bootloader):

::

    reserved-memory {
		#address-cells = <1>;
		#size-cells = <1>;
		ranges;

		/* The memory regions defined below must match what the TF-M
		 * project has defined for that board - a single image boot is
		 * assumed. Please see the memory layout in:
		 * https://git.trustedfirmware.org/TF-M/trusted-firmware-m.git/tree/platform/ext/target/mps2/an521/partition/flash_layout.h
		 */

		code: memory@100000 {
			reg = <0x00100000 DT_SIZE_K(512)>;
		};

		ram: memory@28100000 {
			reg = <0x28100000 DT_SIZE_M(1)>;
		};
	};

这为安全启动和 TF-M 保留了 1 MB 的代码内存和 1 MB 的 RAM,这样我们的非安全 Zephyr 应用程序代码将从 0x10000 开始,RAM 位于 0x28100000。NS zephyr 映像有 512 KB 代码内存可用,以及 1 MB 的 RAM (This reserves 1 MB of code memory and 1 MB of RAM for secure boot and TF-M,
such that our non-secure Zephyr application code will start at 0x10000, with
RAM at 0x28100000. 512 KB code memory is available for the NS zephyr image,
along with 1 MB of RAM)。

这与我们在 TF-M 中的 ``flash_layout.h`` 中看到的 flash 内存布局相匹配 (This matches the flash memory layout we see in ``flash_layout.h`` in TF-M):

::

    * 0x0000_0000 BL2 - MCUBoot (0.5 MB)
    * 0x0008_0000 Secure image     primary slot (0.5 MB)
    * 0x0010_0000 Non-secure image primary slot (0.5 MB)
    * 0x0018_0000 Secure image     secondary slot (0.5 MB)
    * 0x0020_0000 Non-secure image secondary slot (0.5 MB)
    * 0x0028_0000 Scratch area (0.5 MB)
    * 0x0030_0000 Protected Storage Area (20 KB)
    * 0x0030_5000 Internal Trusted Storage Area (16 KB)
    * 0x0030_9000 NV counters area (4 KB)
    * 0x0030_A000 Unused (984 KB)

``mps2/an521`` 将作为开发板目标传递给 TF-M,通过 :kconfig:option:`CONFIG_TFM_BOARD` 指定 (``mps2/an521`` will be passed in to Tf-M as the board target, specified via
:kconfig:option:`CONFIG_TFM_BOARD`)。
