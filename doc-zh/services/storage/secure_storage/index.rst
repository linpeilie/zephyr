.. _secure_storage:

安全存储 (Secure Storage)
##########################

| 安全存储子系统提供了 `平台安全架构 (Platform Security Architecture, PSA) 安全存储 API <https://arm-software.github.io/psa-api/storage/>`_ 中定义的函数实现。(The secure storage subsystem provides an implementation of the functions defined in the `Platform Security Architecture (PSA) Secure Storage API <https://arm-software.github.io/psa-api/storage/>`_.)
| 可以在尚未实现此 API 的 :term:`板级目标<board target>` 上启用它。(It can be enabled on :term:`board targets<board target>` that don't already have an implementation of the API.)

概述 (Overview)
****************

安全存储子系统使 PSA 安全存储 API 在所有具有非易失性内存支持的板级目标上可用。因此,它为那些尚未实现此 API 的目标提供实现,确保 API 的功能支持。例如,启用 :ref:`tfm` 的板级目标(以 ``/ns`` 结尾)无法启用该子系统,因为 TF-M 已经提供了 API 的实现。(The secure storage subsystem makes the PSA Secure Storage API available on all board targets with non-volatile memory support. As such, it provides an implementation of the API on those that don't already have one, ensuring functional support for the API. Board targets with :ref:`tfm` enabled (ending in ``/ns``), for instance, cannot enable the subsystem because TF-M already provides an implementation of the API.)

| 除了提供 API 的功能支持外,根据设备特定的安全功能和配置,该子系统可以在静态时保护通过 PSA 安全存储 API 存储的数据。(In addition to providing functional support for the API, depending on device-specific security features and the configuration, the subsystem may secure the data stored via the PSA Secure Storage API at rest.)
| 但请记住,在可能的情况下,最好使用像 TF-M 这样的安全处理环境,因为它能够通过隔离保证提供更多安全性。(Keep in mind, however, that it's preferable to use a secure processing environment like TF-M when possible because it's able to provide more security due to isolation guarantees.)

限制 (Limitations)
*******************

安全存储子系统的 PSA 安全存储 API 实现:(The secure storage subsystem's implementation of the PSA Secure Storage API:)

* 不追求完全符合规范。(does not aim at full compliance with the specification.)

  | 其首要目标是在所有板级目标上提供 API 的功能支持。(Its foremost goal is functional support for the API on all board targets.)
  | 有关实现与规范偏离的重要方式,请参见下文。(See below for important ways the implementation deviates from the specification.)

* 并非在所有情况下都保证其存储的数据在静态时是安全的。(does not guarantee that the data it stores will be secure at rest in all cases.)

  这取决于设备特定的安全功能和配置。(This depends on device-specific security features and the configuration.)

* 截至目前尚未提供保护存储 (Protected Storage, PS) API 的实现。(does not yet provide an implementation of the Protected Storage (PS) API as of this writing.)

  相反,PS API 直接调用内部可信存储 (Internal Trusted Storage, ITS) API(除非提供了 PS API 的 `自定义实现 <#whole-api>`_)。(Instead, the PS API directly calls into the Internal Trusted Storage (ITS) API (unless a `custom implementation <#whole-api>`_ of the PS API is provided).)

以下是实现有意偏离规范的一些方式及其原因。这不是详尽列表。(Below are some ways the implementation purposefully deviates from the specification and an explanation why. This is not an exhaustive list.)

* UID 类型默认仅为 30 位。(违反 `2.5 UIDs <https://arm-software.github.io/psa-api/storage/1.0/overview/architecture.html#uids>`_。)(The UID type is only 30 bits by default. (Against `2.5 UIDs <https://arm-software.github.io/psa-api/storage/1.0/overview/architecture.html#uids>`_.))

  | 这是一种优化,目的是更方便地直接将 UID 用作存储条目 ID(例如,当启用 :kconfig:option:`CONFIG_SECURE_STORAGE_ITS_STORE_IMPLEMENTATION_ZMS` 时与 :ref:`ZMS <zms_api>` 一起使用)。(This is an optimization done to make it more convenient to directly use the UIDs as storage entry IDs (e.g., with :ref:`ZMS <zms_api>` when :kconfig:option:`CONFIG_SECURE_STORAGE_ITS_STORE_IMPLEMENTATION_ZMS` is enabled).)
  | Zephyr 定义了供 API 不同用户使用的数字范围,这保证了没有冲突,并且它们都在 30 位以内。有关更多信息,请参阅 :zephyr_file:`include/zephyr/psa` 中的头文件。(Zephyr defines numerical ranges to be used by different users of the API which guarantees that there are no collisions and that they all fit within 30 bits. See the header files in :zephyr_file:`include/zephyr/psa` for more information.)

* ITS 中存储的数据默认情况下是加密和认证的(违反 `3.2. 内部可信存储要求 <https://arm-software.github.io/psa-api/storage/1.0/overview/requirements.html#internal-trusted-storage-requirements>`_ 中的 ``1.``)。(The data stored in the ITS is by default encrypted and authenticated (Against ``1.`` in `3.2. Internal Trusted Storage requirements <https://arm-software.github.io/psa-api/storage/1.0/overview/requirements.html#internal-trusted-storage-requirements>`_.).)

  | 规范认为 ITS 的底层存储是 ``隐式保密并受重放保护`` (`2.4. 内部可信存储 API <https://arm-software.github.io/psa-api/storage/1.0/overview/architecture.html#the-internal-trusted-storage-api>`_),因为 ``大多数嵌入式微处理器 (MCU) 具有片上闪存,除了运行在 MCU 上的软件外,可以使其不可访问`` (`2.2. 技术背景 <https://arm-software.github.io/psa-api/storage/1.0/overview/architecture.html#technical-background>`_)。(The specification considers the storage underlying the ITS to be ``implicitly confidential and protected from replay`` (`2.4. The Internal Trusted Storage API <https://arm-software.github.io/psa-api/storage/1.0/overview/architecture.html#the-internal-trusted-storage-api>`_) because ``most embedded microprocessors (MCU) have on-chip flash storage that can be made inaccessible except to software running on the MCU`` (`2.2. Technical Background <https://arm-software.github.io/psa-api/storage/1.0/overview/architecture.html#technical-background>`_).)
  | 但并非所有 MCU 都是如此。因此,为存储的数据提供了额外的保护。(This is not the case on all MCUs. Thus, additional protection is provided to the stored data.)

  但是,这并不保证存储的数据在所有情况下在静态时都是安全的,因为这取决于设备特定的安全功能和配置。它需要随机熵源,特别是安全的加密密钥提供程序 (:kconfig:option:`CONFIG_SECURE_STORAGE_ITS_TRANSFORM_AEAD_KEY_PROVIDER`)。(However, this does not guarantee that the data stored will be secure at rest in all cases, because this depends on device-specific security features and the configuration. It requires a random entropy source and especially a secure encryption key provider (:kconfig:option:`CONFIG_SECURE_STORAGE_ITS_TRANSFORM_AEAD_KEY_PROVIDER`).)

  此外,ITS 中存储的数据不受重放攻击保护,因为这需要受硬件保护的存储。(In addition, the data stored in the ITS is not protected against replay attacks, because this requires storage that is protected by hardware.)

* 通过 PSA 安全存储 API 存储的数据不受软件或调试直接读/写的保护。(违反 `3.2. 内部可信存储要求 <https://arm-software.github.io/psa-api/storage/1.0/overview/requirements.html#internal-trusted-storage-requirements>`_ 中的 ``2.`` 和 ``10.``。)(The data stored via the PSA Secure Storage API is not protected from direct read/write by software or debugging. (Against ``2.`` and ``10.`` in `3.2. Internal Trusted Storage requirements <https://arm-software.github.io/psa-api/storage/1.0/overview/requirements.html#internal-trusted-storage-requirements>`_.).)

  它仅在静态时受保护。在运行时也对其进行保护需要特定的硬件机制来支持这一点。(It is only secured at rest. Protecting it at runtime as well requires specific hardware mechanisms to support this.)

配置 (Configuration)
*********************

要配置 Zephyr 提供的 PSA 安全存储 API 实现,请查看可用的 :kconfig:option-regex:`Kconfig 选项 <CONFIG_SECURE_STORAGE_.*>`。它们在 :zephyr_file:`subsys/secure_storage/` 下找到的各种 Kconfig 文件中定义。(To configure the implementation of the PSA Secure Storage API provided by Zephyr, have a look at the available :kconfig:option-regex:`Kconfig options <CONFIG_SECURE_STORAGE_.*>`. They are defined in the various Kconfig files found under :zephyr_file:`subsys/secure_storage/`.)

自定义 (Customization)
***********************

如果现有实现提供的功能不够,自定义实现也可以在不同级别替换 Zephyr 的实现。(Custom implementations can also replace those of Zephyr at different levels if the functionality provided by the existing implementations isn't enough.)

完整 API (Whole API)
====================

如果您已经有完整的 ITS 或 PS API 的实现并想要使用它,可以通过启用以下 Kconfig 选项并实现相关函数来实现:(If you already have an implementation of the whole ITS or PS API and want to make use of it, you can do so by enabling the following Kconfig option and implementing the relevant functions:)

* :kconfig:option:`CONFIG_SECURE_STORAGE_ITS_IMPLEMENTATION_CUSTOM`,用于 ITS API。(for the ITS API.)
* :kconfig:option:`CONFIG_SECURE_STORAGE_PS_IMPLEMENTATION_CUSTOM`,用于 PS API。(for the PS API.)

ITS API
=======

Zephyr 的 ITS API 实现 (:kconfig:option:`CONFIG_SECURE_STORAGE_ITS_IMPLEMENTATION_ZEPHYR`) 使用 ITS 转换和存储模块,这些模块可以单独配置和自定义。查看 :kconfig:option-regex:`ITS 转换和存储 Kconfig 选项 <CONFIG_SECURE_STORAGE_ITS_(STORE|TRANSFORM)_.*_CUSTOM>` 以了解不同的自定义可能性。(Zephyr's implementation of the ITS API (:kconfig:option:`CONFIG_SECURE_STORAGE_ITS_IMPLEMENTATION_ZEPHYR`) makes use of the ITS transform and store modules, which can be configured and customized separately. Have a look at the :kconfig:option-regex:`ITS transform and store Kconfig options <CONFIG_SECURE_STORAGE_ITS_(STORE|TRANSFORM)_.*_CUSTOM>` to see the different customization possibilities.)

如果可能,特别建议实现一个比可用选项更安全的自定义加密密钥提供程序 (:kconfig:option:`CONFIG_SECURE_STORAGE_ITS_TRANSFORM_AEAD_KEY_PROVIDER_CUSTOM`)。(It's especially recommended to implement a custom encryption key provider (:kconfig:option:`CONFIG_SECURE_STORAGE_ITS_TRANSFORM_AEAD_KEY_PROVIDER_CUSTOM`) that is more secure than the available options, if possible.)

示例 (Samples)
***************

* :zephyr:code-sample:`persistent_key`
* :zephyr:code-sample:`psa_its`

PSA 安全存储 API 参考 (PSA Secure Storage API reference)
*********************************************************

.. doxygengroup:: psa_secure_storage
