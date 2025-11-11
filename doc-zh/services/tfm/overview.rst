可信固件-M 概述 (Trusted Firmware-M Overview)
############################################

`可信固件-M (Trusted Firmware-M, TF-M) <https://tf-m.docs.trustedfirmware.org/en/latest/>`__ 是平台安全架构 (Platform Security Architecture, PSA) `IoT 安全框架 <https://www.psacertified.org/what-is-psa-certified/>`__ 的参考实现。它定义并实现了一个架构和一组软件组件,旨在解决 IoT 产品中的一些主要安全问题。(`Trusted Firmware-M (TF-M) <https://tf-m.docs.trustedfirmware.org/en/latest/>`__ is a reference implementation of the Platform Security Architecture (PSA) `IoT Security Framework <https://www.psacertified.org/what-is-psa-certified/>`__. It defines and implements an architecture and a set of software components that aim to address some of the main security concerns in IoT products.)

自 Zephyr 2.0.0 与 TF-M 1.0 以来,Zephyr RTOS 已通过 PSA 认证,目前与 TF-M 2.1.0 集成。(Zephyr RTOS has been PSA Certified since Zephyr 2.0.0 with TF-M 1.0, and is currently integrated with TF-M 2.1.0.)

TF-M 提供了什么? (What Does TF-M Offer?)
******************************************

通过一组安全服务和设计,TF-M 提供:(Through a set of secure services and by design, TF-M provides:)

* 安全和非安全资源的隔离 (Isolation of secure and non-secure resources)
* 嵌入式适用的加密 (Embedded-appropriate crypto)
* 设备密钥(密钥等)的管理 (Management of device secrets (keys, etc.))
* 固件验证(和加密) (Firmware verification (and encryption))
* 受保护的片外数据存储和检索 (Protected off-chip data storage and retrieval)
* 设备身份证明(设备认证) (Proof of device identity (device attestation))
* 审计日志记录 (Audit logging)

构建系统集成 (Build System Integration)
****************************************

当在支持的平台上使用 TF-M 时,TF-M 将作为标准 Zephyr 构建过程的一部分在后台自动构建和链接。此构建过程对 TF-M 的使用方式做出了许多假设,并且对 Zephyr 应用程序映像可以和不可以做什么有一定的影响:(When using TF-M with a supported platform, TF-M will be automatically built and link in the background as part of the standard Zephyr build process. This build process makes a number of assumptions about how TF-M is being used, and has certain implications about what the Zephyr application image can and can not do:)

* 安全处理环境(安全启动和 TF-M)首先启动 (The secure processing environment (secure boot and TF-M) starts first)
* Zephyr 的资源分配依赖于安全映像中做出的选择。(Resource allocation for Zephyr relies on choices made in the secure image.)

架构概述 (Architecture Overview)
*********************************

通常,TF-M 应用程序将具有以下三个部分,从最受信任到最不受信任,从左到右,代码执行顺序相同(安全启动 > 安全映像 > ns 映像)。(A TF-M application will, generally, have the following three parts, from most to least trusted, left-to-right, with code execution happening in the same order (secure boot > secure image > ns image).)

虽然安全引导加载程序是可选的,但默认情况下是启用的,安全启动是提供安全解决方案的重要部分:(While the secure bootloader is optional, it is enabled by default, and secure boot is an important part of providing a secure solution:)

::

    +-------------------------------------+           +--------------+
    | Secure Processing Environment (SPE) |           |     NSPE     |
    | +----------++---------------------+ |           | +----------+ |
    | |          ||                     | |           | |          | |
    | | bl2.bin  ||  tfm_s_signed.bin   | |           | |zephyr.bin| |
    | |          ||                     | | <- PSA -> | |          | |
    | |  Secure  || Trusted Firmware-M  | |    APIs   | |  Zephyr  | |
    | |   Boot   ||   (Secure Image)    | |           | |(NS Image)| |
    | |          ||                     | |           | |          | |
    | +----------++---------------------+ |           | +----------+ |
    +-------------------------------------+           +--------------+

(Zephyr) 非安全处理环境 (NSPE) 和 (TF-M) 安全处理环境映像之间的通信基于一组 PSA API,通常使用作为 TF-M 构建一部分包含的 IPC 机制,并在 Zephyr 中实现(参见 :zephyr_file:`modules/trusted-firmware-m/interface`)。(Communication between the (Zephyr) Non-Secure Processing Environment (NSPE) and the (TF-M) Secure Processing Environment image happens based on a set of PSA APIs, and normally makes use of an IPC mechanism that is included as part of the TF-M build, and implemented in Zephyr (see :zephyr_file:`modules/trusted-firmware-m/interface`).)

信任根 (RoT) 架构 (Root of Trust (RoT) Architecture)
=====================================================

TF-M 基于**信任根 (Root of Trust, RoT)** 架构。这允许从最受信任到较不受信任再到最不受信任的信任层次结构,为构建或访问受信任的服务和资源提供坚实的基础。(TF-M is based upon a **Root of Trust (RoT)** architecture. This allows for hierarchies of trust from most, to less, to least trusted, providing a sound foundation upon which to build or access trusted services and resources.)

这种方法的好处是,较不受信任的组件被阻止访问或破坏系统的更关键部分,较不受信任环境中的错误条件不会破坏更受信任的隔离资源。(The benefit of this approach is that less trusted components are prevented from accessing or compromising more critical parts of the system, and error conditions in less trusted environments won't corrupt more trusted, isolated resources.)

为 TF-M 定义了以下 RoT 层次结构,从最受信任到最不受信任:(The following RoT hierarchy is defined for TF-M, from most to least trusted:)

* PSA 信任根 (**PRoT**),由以下部分组成:(PSA Root of Trust (**PRoT**), which consists of:)

  * PSA 不可变信任根:安全启动 (PSA Immutable Root of Trust: secure boot)
  * PSA 可更新信任根:最受信任的安全服务 (PSA Updateable Root of Trust: most trusted secure services)
* 应用程序信任根 (**ARoT**):隔离的安全服务 (Application Root of Trust (**ARoT**): isolated secure services)

**PSA 不可变信任根**是系统中最受信任的代码片段,后续信任根锚定在其上。在 TF-M 中,这是安全启动映像,它验证安全和非安全映像是否有效、未被篡改,并来自可靠来源。安全引导加载程序还在固件更新过程中验证新映像,这要归功于内置的公共签名密钥。如名称所示,此映像是**不可变的**。(The **PSA Immutable Root of Trust** is the most trusted piece of code in the system, to which subsequent Roots of Trust are anchored. In TF-M, this is the secure boot image, which verifies that the secure and non-secure images are valid, have not been tampered with, and come from a reliable source. The secure bootloader also verifies new images during the firmware update process, thanks to the public signing key(s) built into it. As the name implies, this image is **immutable**.)

**PSA 可更新信任根**实现 TF-M 中最受信任的安全服务和组件,例如安全分区管理器 (Secure Partition Manager, SPM) 和共享安全服务,如 PSA Crypto、内部可信存储 (Internal Trusted Storage, ITS) 等。PSA 可更新信任根中的服务可以访问同一信任根中的其他资源。(The **PSA Updateable Root of Trust** implements the most trusted secure services and components in TF-M, such as the Secure Partition Manager (SPM), and shared secure services like PSA Crypto, Internal Trusted Storage (ITS), etc. Services in the PSA Updateable Root of Trust have access to other resources in the same Root of Trust.)

**应用程序信任根**是安全处理环境中的降低权限区域,根据构建 TF-M 时选择的隔离级别,对 PRoT 甚至其他 ARoT 服务的访问受限,在最高隔离级别下更是如此。ARoT 中存在一些标准服务,例如保护存储 (Protected Storage, PS),通常您实现的自定义安全服务应放置在 ARoT 中,除非有充分的理由将它们放在 PRoT 中。(The **Application Root of Trust** is a reduced-privilege area in the secure processing environment which, depending on the isolation level chosen when building TF-M, has limited access to the PRoT, or even other ARoT services at the highest isolation levels. Some standard services exist in the ARoT, such as Protected Storage (PS), and generally custom secure services that you implement should be placed in the ARoT, unless a compelling reason is present to place them in the PRoT.)

这些划分不同于在非安全环境中运行的**不受信任的代码**,在系统中具有最少的权限。在这种情况下,这是 Zephyr 应用程序映像。(These divisions are distinct from the **untrusted code**, which runs in the non-secure environment, and has the least privilege in the system. This is the Zephyr application image in this case.)

隔离级别 (Isolation Levels)
----------------------------

目前,TF-M 中定义了三个不同的**隔离级别**,区域之间的边界越来越严格。使用的隔离级别将取决于您的安全要求和可用的系统资源。(At present, there are three distinct **isolation levels** defined in TF-M, with increasingly rigid boundaries between regions. The isolation level used will depend on your security requirements, and the system resources available to you.)

* **隔离级别 1** 是最低的隔离级别,唯一的主要边界是安全和非安全处理环境之间,通常通过 Armv8-M 处理器上的 Arm TrustZone 实现。这里 PSA 可更新信任根 (PRoT) 和应用程序信任根 (ARoT) 之间没有区别。它们以相同的权限级别执行。此隔离级别将导致最小的组合应用程序映像。(**Isolation Level 1** is the lowest isolation level, and the only major boundary is between the secure and non-secure processing environment, usually by means of Arm TrustZone on Armv8-M processors. There is no distinction here between the PSA Updateable Root of Trust (PRoT) and the Application Root of Trust (ARoT). They execute at the same privilege level. This isolation level will lead to the smallest combined application images.)
* **隔离级别 2** 在级别 1 的基础上通过引入 PSA 可更新信任根和应用程序信任根之间的区别进行构建,其中 ARoT 服务对 PRoT 服务的访问受限,只能通过 PRoT 服务公开的公共 API 与它们通信。但是,ARoT 服务彼此之间并不严格隔离。(**Isolation Level 2** builds upon level one by introducing a distinction between the PSA Updateable Root of Trust and the Application Root of Trust, where ARoT services have limited access to PRoT services, and can only communicate with them through public APIs exposed by the PRoT services. ARoT services, however, are not strictly isolated from one another.)
* **隔离级别 3** 是最高的隔离级别,在级别 2 的基础上通过将 ARoT 服务彼此隔离进行构建,以便每个 ARoT 本质上与其他服务隔离。这提供了最高级别的隔离,但也以额外的开销和服务之间的代码重复为代价。(**Isolation Level 3** is the highest isolation level, and builds upon level 2 by isolating ARoT services from each other, so that each ARoT is essentially silo'ed from other services. This provides the highest level of isolation, but also comes at the cost of additional overhead and code duplication between services.)

当前隔离级别可以通过 :kconfig:option:`CONFIG_TFM_ISOLATION_LEVEL` 检查。(The current isolation level can be checked via :kconfig:option:`CONFIG_TFM_ISOLATION_LEVEL`.)

安全启动 (Secure Boot)
=======================

TF-M 中的默认安全引导加载程序基于 `MCUBoot <https://www.mcuboot.com/>`__,在 TF-M 中称为 ``BL2``(第二阶段引导加载程序,可能在安全 MCU 上的基于硬件的引导加载程序之后等)。(The default secure bootloader in TF-M is based on `MCUBoot <https://www.mcuboot.com/>`__, and is referred to as ``BL2`` in TF-M (for the second-stage bootloader, potentially after a HW-based bootloader on the secure MCU, etc.).)

TF-M 中的所有映像都经过哈希和签名,在固件更新过程中由 MCUBoot 验证哈希和签名。(All images in TF-M are hashed and signed, with the hash and signature verified by MCUBoot during the firmware update process.)

MCUBoot 在 TF-M 中使用的一些关键特性是:(Some key features of MCUBoot as used in TF-M are:)

* 公共签名密钥内置到引导加载程序中 (Public signing key(s) are baked into the bootloader)
* S 和 NS 映像可以使用不同的密钥签名 (S and NS images can be signed using different keys)
* 固件映像可以选择加密 (Firmware images can optionally be encrypted)
* 客户端软件负责将新映像写入辅助槽 (Client software is responsible for writing a new image to the secondary slot)
* 默认情况下,使用两个大小相同的内存区域的静态闪存布局 (By default, uses static flash layout of two identically-sized memory regions)
* 可选的安全计数器用于回滚保护 (Optional security counter for rollback protection)

处理(可选)加密映像时:(When dealing with (optionally) encrypted images:)

* 只有有效负载被加密(头部、TLV 是纯文本) (Only the payload is encrypted (header, TLVs are plain text))
* 哈希和签名应用于未加密的数据 (Hashing and signing are applied over the un-encrypted data)
* 使用 ``AES-CTR-128`` 或 ``AES-CTR-256`` 进行加密 (Uses ``AES-CTR-128`` or ``AES-CTR-256`` for encryption)
* 每个加密周期加密密钥随机化(通过 ``imgtool``) (Encryption key randomized every encryption cycle (via ``imgtool``))
* ``AES-CTR`` 密钥包含在映像中,可以使用以下方式加密:(The ``AES-CTR`` key is included in the image and can be encrypted using:)

  * ``RSA-OAEP``
  * ``AES-KW``(128 或 256 位,取决于 ``AES-CTR`` 密钥长度) (``AES-KW`` (128 or 256 bits depending on the ``AES-CTR`` key length))
  * ``ECIES-P256``
  * ``ECIES-X25519``

在 Zephyr 中控制安全启动的关键配置属性是:(Key config properties to control secure boot in Zephyr are:)

* :kconfig:option:`CONFIG_TFM_BL2` 切换引导加载程序(默认 = ``y``)。(:kconfig:option:`CONFIG_TFM_BL2` toggles the bootloader (default = ``y``).)
* :kconfig:option:`CONFIG_TFM_KEY_FILE_S` 覆盖安全签名密钥。(:kconfig:option:`CONFIG_TFM_KEY_FILE_S` overrides the secure signing key.)
* :kconfig:option:`CONFIG_TFM_KEY_FILE_NS` 覆盖非安全签名密钥。(:kconfig:option:`CONFIG_TFM_KEY_FILE_NS` overrides the non-secure signing key.)

安全处理环境 (Secure Processing Environment)
==============================================

安全引导加载程序执行完成后,基于 TF-M 的安全映像将在**安全处理环境**中开始执行。这是我们的设备最初配置和初始化任何安全服务的地方。(Once the secure bootloader has finished executing, a TF-M based secure image will begin execution in the **secure processing environment**. This is where our device will be initially configured, and any secure services will be initialised.)

请注意,设备的启动状态由安全固件控制,这意味着当非安全 Zephyr 应用程序启动时,外设可能不处于硬件默认复位状态。如有疑问,请务必查阅 TF-M 中的板级支持包,可在 TF-M 模块的 ``platform/ext/target/`` 文件夹中找到(在默认的 Zephyr west 工作空间中位于 ``modules/tee/tf-m/trusted-firmware-m/``)。(Note that the starting state of our device is controlled by the secure firmware, meaning that when the non-secure Zephyr application starts, peripherals may not be in the HW-default reset state. In case of doubts, be sure to consult the board support packages in TF-M, available in the ``platform/ext/target/`` folder of the TF-M module (which is in ``modules/tee/tf-m/trusted-firmware-m/`` within a default Zephyr west workspace.).)

安全服务 (Secure Services)
---------------------------

截至 TF-M 1.8.0,以下安全服务通常可用(尽管供应商支持可能有所不同):(As of TF-M 1.8.0, the following secure services are generally available (although vendor support may vary):)

* 加密 (Crypto)
* 固件更新 (Firmware Update, FWU)
* 初始认证 (Initial Attestation)
* 平台 (Platform)
* 安全存储,由两部分组成:(Secure Storage, which has two parts:)

  * 内部可信存储 (Internal Trusted Storage, ITS)
  * 保护存储 (Protected Storage, PS)

还存在用于创建自己的自定义服务的模板。(A template also exists for creating your own custom services.)

有关这些服务及其公开的 API 的完整详细信息,请查阅 `TF-M 文档 <https://tf-m.docs.trustedfirmware.org/en/latest/>`__。(For full details on these services, and their exposed APIs, please consult the `TF-M Documentation <https://tf-m.docs.trustedfirmware.org/en/latest/>`__.)

密钥管理和派生 (Key Management and Derivation)
-----------------------------------------------

密钥和密钥管理是任何安全设备的关键部分。您需要确保密钥材料可用于需要它的区域,但不能用于其他任何区域,并且它以难以篡改或恶意访问的方式安全存储。(Key and secret management is a critical part of any secure device. You need to ensure that key material is available to regions that require it, but not to anything else, and that it is stored securely in a way that makes it difficult to tamper with or maliciously access.)

TF-M 中的**内部可信存储**服务由 **PSA Crypto** 服务(它本身使用 mbedtls)用于存储密钥,并确保私钥只能由安全处理环境访问。使用密钥材料的加密操作,例如在签名有效负载或解密敏感数据时,都通过密钥句柄进行。密钥材料在任何时候都不应暴露给 NS 环境。(The **Internal Trusted Storage** service in TF-M is used by the **PSA Crypto** service (which itself makes use of mbedtls) to store keys, and ensure that private keys are only ever accessible to the secure processing environment. Crypto operations that make use of key material, such as when signing payloads or when decrypting sensitive data, all take place via key handles. At no point should the key material ever be exposed to the NS environment.)

一个例外是,私钥可以作为单向操作提供到安全处理环境中,例如在工厂配置过程中,但即使这样也应尽可能避免,应向 SPE 请求(通过 PSA Crypto 服务)自己生成新的私钥,可以在配置期间请求该公钥并在工厂中记录。这确保私钥材料永远不会暴露,甚至在配置阶段也不知道。(One exception is that private keys can be provisioned into the secure processing environment as a one-way operation, such as during a factory provisioning process, but even this should be avoided where possible, and a request should be made to the SPE (via the PSA Crypto service) to generate a new private key itself, and the public key for that can be requested during provisioning and logged in the factory. This ensures the private key material is never exposed, or even known during the provisioning phase.)

TF-M 还广泛使用**硬件唯一密钥 (Hardware Unique Key, HUK)**,每个 TF-M 设备都必须提供。例如,**保护存储**服务使用此设备唯一密钥来加密存储在外部内存中的信息。例如,这确保如果闪存内容被移除并放置在新设备上,则无法解密,因为每个设备在首次加密内存内容时都有自己的唯一 HUK。(TF-M also makes extensive use of the **Hardware Unique Key (HUK)**, which every TF-M device must provide. This device-unique key is used by the **Protected Storage** service, for example, to encrypt information stored in external memory. For example, this ensures that the contents of flash memory can't be decrypted if they are removed and placed on a new device, since each device has its own unique HUK used while encrypting the memory contents the first time.)

HUK 为开发人员提供了额外的优势,因为它们可用于派生新密钥,并且**派生密钥**不需要存储,因为可以在启动时使用额外的盐/种子值(取决于使用的密钥派生算法)从 HUK 重新生成它们。这消除了存储问题和常见的攻击向量。HUK 本身通常在安全设备中受到高度保护,用户无法直接访问。(HUKs provide an additional advantage for developers, in that they can be used to derive new keys, and the **derived keys** don't need to be stored since they can be regenerated from the HUK at startup, using an additional salt/seed value (depending on the key derivation algorithm used). This removes the storage issue and a frequent attack vector. The HUK itself it usually highly protected in secure devices, and inaccessible directly by users.)

``TFM_CRYPTO_ALG_HUK_DERIVATION`` 标识如果使用软件实现时使用的默认密钥派生算法。当前默认算法是带有 SHA-256 哈希的 ``HKDF`` (RFC 5869)。某些平台上可能提供其他硬件实现。(``TFM_CRYPTO_ALG_HUK_DERIVATION`` identifies the default key derivation algorithm used if a software implementation is used. The current default algorithm is ``HKDF`` (RFC 5869) with a SHA-256 hash. Other hardware implementations may be available on some platforms.)

非安全处理环境 (Non-Secure Processing Environment)
===================================================

Zephyr 用于 NSPE,使用 TF-M 支持的板,其中已启用 :kconfig:option:`CONFIG_BUILD_WITH_TFM` 标志。(Zephyr is used for the NSPE, using a board that is supported by TF-M where the :kconfig:option:`CONFIG_BUILD_WITH_TFM` flag has been enabled.)

通常,您只需选择有效板的 ``*/ns`` 板目标(例如 ``mps2/an521/cpu0/ns``),这将配置您的 Zephyr 应用程序在 NSPE 中运行,正确构建并将其与 TF-M 安全映像链接,对安全和非安全映像进行签名,并将三个二进制文件合并到一个 ``tfm_merged.hex`` 文件中。在此配置中,:ref:`west flash <west-flashing>` 命令默认将闪存 ``tfm_merged.hex``。(Generally, you simply need to select the ``*/ns`` board target of a valid board (for example ``mps2/an521/cpu0/ns``), which will configure your Zephyr application to run in the NSPE, correctly build and link it with the TF-M secure images, sign the secure and non-secure images, and merge the three binaries into a single ``tfm_merged.hex`` file. The :ref:`west flash <west-flashing>` command will flash ``tfm_merged.hex`` by default in this configuration.)

目前,Zephyr 无法配置为用作安全处理环境。(At present, Zephyr can not be configured to be used as the secure processing environment.)
