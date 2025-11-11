.. _tfm_build_system:

TF-M 构建系统 (TF-M Build System)
##################################

当构建一个有效的 ``_ns`` 开发板目标时,TF-M 将在后台构建,并与 Zephyr 非安全应用程序链接。在大多数情况下不需要了解 TF-M 的构建系统,以下命令将构建 TF-M 和 Zephyr 映像对,并在 qemu 中运行,无需额外步骤 (When building a valid ``_ns`` board target, TF-M will be built in the
background, and linked with the Zephyr non-secure application. No knowledge
of TF-M's build system is required in most cases, and the following will
build a TF-M and Zephyr image pair, and run it in qemu with no additional
steps required):

   .. code-block:: bash

     $ west build -p auto -b mps2/an521/cpu0/ns samples/tfm_integration/psa_protected_storage/ -t run

此处描述了此构建过程中的输出和某些关键步骤,因为您需要理解输出并与之交互,并在部署之前处理安全和非安全映像的签名 (The outputs and certain key steps in this build process are described here,
however, since you will need to understand and interact with the outputs, and
deal with signing the secure and non-secure images before deploying them)。

TF-M 构建创建的映像 (Images Created by the TF-M Build)
*******************************************************

TF-M 构建系统创建以下可执行文件 (The TF-M build system creates the following executable files):

* tfm_s - TF-M 安全固件 (TF-M secure firmware)
* tfm_ns - TF-M 非安全应用程序 (仅用于回归测试) (TF-M non-secure app (only used by regression tests))
* bl2 - TF-M MCUboot,如果启用 (TF-M MCUboot, if enabled)

对于每一个文件,它都会创建 .bin、.hex、.elf 和 .axf 文件 (For each of these, it creates .bin, .hex, .elf, and .axf files)。

TF-M 构建系统还创建 tfm_s 和 tfm_ns 的签名变体,以及一个组合它们的文件 (The TF-M build system also creates signed variants of tfm_s and tfm_ns, and a
file which combines them):

* tfm_s_signed
* tfm_ns_signed
* tfm_s_ns_signed

对于这些文件,仅创建 .bin 文件 (For each of these, only .bin files are created)。

TF-M 非安全应用程序被丢弃,改用 Zephyr 非安全应用程序,除非运行 TF-M 回归测试套件 (The TF-M non-secure app is discarded in favor of Zephyr non-secure app except
when running the TF-M regression test suite)。

Zephyr 构建系统通常会同时签名 tfm_s 和 Zephyr 非安全应用程序本身。详见下文 (The Zephyr build system usually signs both tfm_s and the Zephyr non-secure app itself.
See below for details)。

'tfm' 目标包含所有这些路径的属性。例如,以下内容将解析为 ``<path>/tfm_s.hex`` (The 'tfm' target contains properties for all these paths.
For example, the following will resolve to ``<path>/tfm_s.hex``):

   .. code-block::

      $<TARGET_PROPERTY:tfm,TFM_S_HEX_FILE>

有关所有属性的概述,请参见 tfm 模块中的顶级 CMakeLists.txt 文件 (See the top level CMakeLists.txt file in the tfm module for an overview of all
the properties)。

签名映像 (Signing Images)
**************************

当 :kconfig:option:`CONFIG_TFM_BL2` 设置为 ``y`` 时,TF-M 使用安全引导加载程序 (BL2),固件映像必须使用私钥签名。引导加载程序在更新期间使用相应的公钥验证固件映像,该公钥存储在安全引导加载程序固件映像中 (When :kconfig:option:`CONFIG_TFM_BL2` is set to ``y``, TF-M uses a secure bootloader
(BL2) and firmware images must be signed with a private key. The firmware image
is validated by the bootloader during updates using the corresponding public
key, which is stored inside the secure bootloader firmware image)。

在签名过程中,所有 HEX 文件都被标记为 ``confirmed`` (已确认),而所有 BIN 文件保持 ``unconfirmed`` (未确认)。这确保了刷入设备的任何映像都具有与 `PSA Certified Firmware Update API`_ 兼容所需的属性。然后可以在固件更新过程中将相应的 BIN 文件用作有效载荷 (During the signing procedure, all HEX files are marked as ``confirmed``,
whereas all BIN files remain ``unconfirmed``. This guarantees that any image
flashed into a device possesses the required properties for compatibility
with the `PSA Certified Firmware Update API`_. The corresponding BIN file
can then be used as the payload in the Firmware Update procedure)。

默认情况下,``<tfm-dir>/bl2/ext/mcuboot/root-rsa-3072.pem`` 用于签名安全映像,``<tfm-dir>/bl2/ext/mcuboot/root-rsa-3072_1.pem`` 用于签名非安全映像。这些默认的 .pem 密钥可以 (并且 **应该**) 使用 :kconfig:option:`CONFIG_TFM_KEY_FILE_S` 和 :kconfig:option:`CONFIG_TFM_KEY_FILE_NS` 配置标志进行覆盖 (By default, ``<tfm-dir>/bl2/ext/mcuboot/root-rsa-3072.pem`` is used to sign secure
images, and ``<tfm-dir>/bl2/ext/mcuboot/root-rsa-3072_1.pem`` is used to sign
non-secure images. These default .pem keys can (and **should**) be overridden
using the :kconfig:option:`CONFIG_TFM_KEY_FILE_S` and
:kconfig:option:`CONFIG_TFM_KEY_FILE_NS` config flags)。

为了满足 `PSA Certified Level 1`_ 要求,**您必须用新的密钥对替换默认的 .pem 文件!** (To satisfy `PSA Certified Level 1`_ requirements, **You MUST replace
the default .pem file with a new key pair!**)

要生成新的公钥/私钥对,请运行以下命令 (To generate a new public/private key pair, run the following commands):

   .. code-block:: bash

     $ imgtool keygen -k root-rsa-3072_s.pem -t rsa-3072
     $ imgtool keygen -k root-rsa-3072_ns.pem -t rsa-3072

然后,您可以将新的 .pem 文件放在其他位置,例如您的 Zephyr 应用程序文件夹,并通过 :kconfig:option:`CONFIG_TFM_KEY_FILE_S` 和 :kconfig:option:`CONFIG_TFM_KEY_FILE_NS` 配置标志在 ``prj.conf`` 文件中引用它们 (You can then place the new .pem files in an alternate location, such as your
Zephyr application folder, and reference them in the ``prj.conf`` file via the
:kconfig:option:`CONFIG_TFM_KEY_FILE_S` and :kconfig:option:`CONFIG_TFM_KEY_FILE_NS` config
flags)。

   .. warning::

     请务必将您的私钥文件保存在安全、可靠的位置!如果您丢失了这个密钥文件,您将无法签名任何未来的固件映像,并且将无法在现场更新您的设备 (Be sure to keep your private key file in a safe, reliable location! If you
     lose this key file, you will be unable to sign any future firmware images,
     and it will no longer be possible to update your devices in the field)!

内置签名脚本运行后,它会创建一个包含所有三个二进制文件的 ``tfm_merged.hex`` 文件:bl2、tfm_s 和 zephyr 应用程序。然后可以将此十六进制文件刷入您的开发板或在 QEMU 中运行 (After the built-in signing script has run, it creates a ``tfm_merged.hex``
file that contains all three binaries: bl2, tfm_s, and the zephyr app. This
hex file can then be flashed to your development board or run in QEMU)。

.. _PSA Certified Level 1:
  https://www.psacertified.org/security-certification/psa-certified-level-1/
.. _PSA Certified Firmware Update API:
  https://arm-software.github.io/psa-api/fwu/

自定义 CMake 参数 (Custom CMake arguments)
===========================================

在使用 TF-M 构建 Zephyr 应用程序时,可能需要控制传递给 TF-M 构建的 CMake 参数 (When building a Zephyr application with TF-M it might be necessary to control
the CMake arguments passed to the TF-M build)。

Zephyr TF-M 构建提供了几个用于控制构建的 Kconfig 选项,但并未涵盖 TF-M 构建系统支持的每个 CMake 参数 (Zephyr TF-M build offers several Kconfig options for controlling the build, but
doesn't cover every CMake argument supported by the TF-M build system)。

``zephyr_property_target`` 上的 ``TFM_CMAKE_OPTIONS`` 属性可用于向 TF-M 构建系统传递自定义 CMake 参数 (The ``TFM_CMAKE_OPTIONS`` property on the ``zephyr_property_target`` can be used
to pass custom CMake arguments to the TF-M build system)。

要将 CMake 参数 ``-DFOO=bar`` 传递给 TF-M 构建系统,请将以下 CMake 代码片段放在您的 CMakeLists.txt 文件中 (To pass the CMake argument ``-DFOO=bar`` to the TF-M build system, place the
following CMake snippet in your CMakeLists.txt file)。

   .. code-block:: cmake

     set_property(TARGET zephyr_property_target
                  APPEND PROPERTY TFM_CMAKE_OPTIONS
                  -DFOO=bar
     )

.. note::
   ``TFM_CMAKE_OPTIONS`` 是一个列表,因此可以追加多个选项。还支持 CMake 生成器表达式,例如 ``$<1:-DFOO=bar>`` (The ``TFM_CMAKE_OPTIONS`` is a list so it is possible to append multiple
   options. Also CMake generator expressions are supported, such as
   ``$<1:-DFOO=bar>``)

由于 ``TFM_CMAKE_OPTIONS`` 是一个列表参数,它将在传递给 TF-M 构建系统之前展开。因此,具有列表参数的选项必须正确转义以避免被展开为列表 (Since ``TFM_CMAKE_OPTIONS`` is a list argument it will be expanded before it is
passed to the TF-M build system.
Options that have list arguments must therefore be properly escaped to avoid
being expanded as a list)。

   .. code-block:: cmake

     set_property(TARGET zephyr_property_target
                  APPEND PROPERTY TFM_CMAKE_OPTIONS
                  -DFOO="bar\\\;baz"
     )

占用空间和内存使用 (Footprint and Memory Usage)
*************************************************

构建系统提供了用于查看和分析生成映像中 RAM 和 ROM 使用情况的目标。这些工具在最终映像上运行,并提供有关 RAM 和 ROM 中使用的符号和代码大小的信息。有关这些工具的更多信息,请查看此处 (The build system offers targets to view and analyse RAM and ROM usage in generated images.
The tools run on the final images and give information about size of symbols and code being used in both RAM and ROM.
For more information on these tools look here)::ref:`footprint_tools`

使用 ``tfm_ram_report`` 获取 TF-M 安全固件 (tfm_s) 的 RAM 报告 (Use the ``tfm_ram_report`` to get the RAM report for TF-M secure firmware (tfm_s))。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: mps2/an521/cpu0/ns
    :goals: tfm_ram_report

使用 ``tfm_rom_report`` 获取 TF-M 安全固件 (tfm_s) 的 ROM 报告 (Use the ``tfm_rom_report`` to get the ROM report for TF-M secure firmware (tfm_s))。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: mps2/an521/cpu0/ns
    :goals: tfm_rom_report

使用 ``bl2_ram_report`` 获取 TF-M MCUboot 的 RAM 报告 (如果启用) (Use the ``bl2_ram_report`` to get the RAM report for TF-M MCUboot, if enabled)。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: mps2/an521/cpu0/ns
    :goals: bl2_ram_report

使用 ``bl2_rom_report`` 获取 TF-M MCUboot 的 ROM 报告 (如果启用) (Use the ``bl2_rom_report`` to get the ROM report for TF-M MCUboot, if enabled)。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: mps2/an521/cpu0/ns
    :goals: bl2_rom_report
