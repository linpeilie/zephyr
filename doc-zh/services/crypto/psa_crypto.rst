.. _psa_crypto:

PSA加密 (PSA Crypto)
####################

概述 (Overview)
****************

PSA(平台安全架构,Platform Security Architecture)加密API为各种硬件上的加密操作和密钥存储提供了可移植的编程接口 (The PSA (Platform Security Architecture) Crypto API offers a portable programming interface for cryptographic operations and key storage across a wide range of hardware)。它被设计为用户友好的,同时仍然提供对现代密码学所必需的低级原语的访问 (It is designed to be user-friendly while still providing access to the low-level primitives essential for modern cryptography)。

它由Arm创建和维护 (It is created and maintained by Arm)。Arm开发了PSA作为一个全面的安全框架,以满足联网设备日益增长的安全需求 (Arm developed the PSA as a comprehensive security framework to address the increasing security needs of connected devices)。

在Zephyr中,PSA加密API使用Mbed TLS实现,Mbed TLS是一个开源加密库,提供底层加密函数 (In Zephyr, the PSA Crypto API is implemented using Mbed TLS, an open-source cryptographic library that provides the underlying cryptographic functions)。

设计目标 (Design Goals)
************************

该接口适用于各种设备:从使用内置密钥处理数据的专用加密处理器,到运行自定义应用代码的受限设备(如微控制器),以及多应用设备(如服务器) (The interface is suitable for a vast range of devices: from special-purpose cryptographic processors that process data with a built-in key, to constrained devices running custom application code, such as microcontrollers, and multi-application devices, such as servers)。它遵循加密敏捷性原则 (It follows the principle of cryptographic agility)。

算法灵活性 (Algorithm Flexibility)
  PSA加密API支持广泛的加密算法,允许开发人员根据需要在不同的加密方法之间切换 (The PSA Crypto API supports a wide range of cryptographic algorithms, allowing developers to switch between different cryptographic methods as needed)。这种灵活性对于维护安全性至关重要,因为新算法会出现而现有算法会过时 (This flexibility is crucial for maintaining security as new algorithms emerge and existing ones become obsolete)。

密钥管理 (Key Management)
  PSA加密API包含强大的密钥管理功能,支持以安全和灵活的方式创建、存储和使用加密密钥 (The PSA Crypto API includes robust key management features that support the creation, storage, and use of cryptographic keys in a secure and flexible manner)。它使用不透明的密钥标识符,允许轻松替换和更新密钥而不暴露密钥材料 (It uses opaque key identifiers, which allows for easy key replacement and updates without exposing key material)。

实现独立性 (Implementation Independence)
  PSA加密API抽象了底层加密库,这意味着可以在不影响应用代码的情况下更改具体实现 (The PSA Crypto API abstracts the underlying cryptographic library, meaning that the specific implementation can be changed without affecting the application code)。这种抽象通过支持根据需要使用不同的加密库或硬件加速器来支持加密敏捷性 (This abstraction supports cryptographic agility by enabling the use of different cryptographic libraries or hardware accelerators as needed)。

面向未来 (Future-Proofing)
  通过遵循加密敏捷性,PSA加密确保应用程序能够快速适应新的加密标准和实践,增强长期安全性和合规性 (By adhering to cryptographic agility, PSA Crypto ensures that applications can quickly adapt to new cryptographic standards and practices, enhancing long-term security and compliance)。

应用示例 (Examples of Applications)
************************************

网络安全(TLS) (Network Security (TLS))
  该API提供建立TLS连接所需的所有加密原语 (The API provides all of the cryptographic primitives needed to establish TLS connections)。

安全存储 (Secure Storage)
  该API提供与存储加密相关的所有原语,包括基于块或文件的加密,主加密密钥存储在密钥库中 (The API provides all primitives related to storage encryption, block or file-based, with master encryption keys stored inside a key store)。

网络凭证 (Network Credentials)
  该API提供密钥库内的网络凭证管理,例如,用于基于X.509的身份验证或企业网络上的预共享密钥 (The API provides network credential management inside a key store, for example, for X.509-based authentication or pre-shared keys on enterprise networks)。

设备配对 (Device Pairing)
  该API提供对密钥协商协议的支持,这些协议通常用于通过无线信道安全配对设备 (The API provides support for key agreement protocols that are often used for secure pairing of devices over wireless channels)。例如,NFC令牌或蓝牙设备的配对可能在首次使用时使用密钥协商协议 (For example, the pairing of an NFC token or a Bluetooth device might use key agreement protocols upon first use)。

安全启动 (Secure Boot)
  该API提供在安全或可信启动过程中用于固件完整性和真实性验证的原语 (The API provides primitives for use during firmware integrity and authenticity validation, during a secure or trusted boot process)。

证明 (Attestation)
  该API提供证明活动中使用的原语 (The API provides primitives used in attestation activities)。证明是设备使用设备私钥对字节数组进行签名并将结果返回给调用者的能力 (Attestation is the ability for a device to sign an array of bytes with a device private key and return the result to the caller)。有几个用例:从设备状态的证明,到生成密钥对并证明它是在安全密钥库内生成的能力 (There are several use cases; ranging from attestation of the device state, to the ability to generate a key pair and prove that it has been generated inside a secure key store)。该API提供对证明常用算法的访问 (The API provides access to the algorithms commonly used for attestation)。

工厂配置 (Factory Provisioning)
  大多数IoT设备在工厂配置过程中或部署到现场后会获得唯一身份 (Most IoT devices receive a unique identity during the factory provisioning process, or once they have been deployed to the field)。此API提供使用代表该身份的密钥填充设备所需的API (This API provides the APIs necessary for populating a device with keys that represent that identity)。

使用注意事项 (Usage considerations)
************************************

始终检查错误 (Always check for errors)
  PSA加密API中的大多数函数都可能返回错误 (Most functions in the PSA Crypto API can return errors)。所有可能失败的函数都具有返回类型 ``psa_status_t`` (All functions that can fail have the return type ``psa_status_t``)。少数函数不会失败,因此返回void或其他类型 (A few functions cannot fail, and thus, return void or some other type)。

  如果发生错误,除非另有说明,输出参数的内容是未定义的,不得使用 (If an error occurs, unless otherwise specified, the content of the output parameters is undefined and must not be used)。

  一些常见的错误原因包括 (Some common causes of errors include):

  * 在密钥存储和处理与应用程序分离的环境中的实现中,所有需要访问加密处理环境的函数可能会由于两个环境之间通信中的错误而失败 (In implementations where the keys are stored and processed in a separate environment from the application, all functions that need to access the cryptography processing environment might fail due to an error in the communication between the two environments)。

  * 如果算法使用硬件加速器实现,该加速器在逻辑上与应用处理器分离,则加速器可能会失败,即使应用处理器继续正常运行 (If an algorithm is implemented with a hardware accelerator, which is logically separate from the application processor, the accelerator might fail, even when the application processor keeps running normally)。

  * 大多数函数可能由于缺乏资源而失败 (Most functions might fail due to a lack of resources)。但是,某些实现保证某些函数始终具有足够的内存 (However, some implementations guarantee that certain functions always have sufficient memory)。

  * 所有访问持久密钥的函数可能由于存储故障而失败 (All functions that access persistent keys might fail due to a storage failure)。

  * 所有需要随机性的函数可能由于缺乏熵而失败 (All functions that require randomness might fail due to a lack of entropy)。鼓励实现在执行 ``psa_crypto_init()`` 期间使用足够的熵为随机数生成器提供种子 (Implementations are encouraged to seed the random generator with sufficient entropy during the execution of ``psa_crypto_init()``)。但是,某些安全标准需要从硬件随机数生成器定期重新播种,这可能会失败 (However, some security standards require periodic reseeding from a hardware random generator, which can fail)。

共享内存和并发 (Shared memory and concurrency)
  某些环境允许应用程序是多线程的,而其他环境则不允许 (Some environments allow applications to be multithreaded, while others do not)。在某些环境中,应用程序可以与不同的安全上下文共享内存 (In some environments, applications can share memory with a different security context)。在具有多线程应用程序或共享内存的环境中,必须仔细编写应用程序以避免数据损坏或泄漏 (In environments with multithreaded applications or shared memory, applications must be written carefully to avoid data corruption or leakage)。此规范要求应用程序遵守某些约束 (This specification requires the application to obey certain constraints)。

  一般来说,PSA加密API在任何给定对象上允许一个写入者或任意数量的同时读取者 (In general, the PSA Crypto API allows either one writer or any number of simultaneous readers, on any given object)。换句话说,如果两个或多个调用同时访问同一对象,则仅当所有调用仅从对象读取而不修改它时,行为才是明确定义的 (In other words, if two or more calls access the same object concurrently, then the behavior is only well-defined if all the calls are only reading from the object and do not modify it)。读取访问包括通过输入参数读取内存和通过使用密钥读取密钥库内容 (Read accesses include reading memory by input parameters and reading keystore content by using a key)。有关更多详细信息,请参阅 `并发调用 <https://arm-software.github.io/psa-api/crypto/1.2/overview/conventions.html#concurrent-calls>`_ (For more details, refer to `Concurrent calls <https://arm-software.github.io/psa-api/crypto/1.2/overview/conventions.html#concurrent-calls>`_)。

  如果应用程序与另一个安全上下文共享内存,它可以将共享内存块作为输入缓冲区或输出缓冲区传递,但不能作为非缓冲区参数传递 (If an application shares memory with another security context, it can pass shared memory blocks as input buffers or output buffers, but not as non-buffer parameters)。有关更多详细信息,请参阅 `参数的稳定性 <https://arm-software.github.io/psa-api/crypto/1.2/overview/conventions.html#stability-of-parameters>`_ (For more details, refer to `Stability of parameters <https://arm-software.github.io/psa-api/crypto/1.2/overview/conventions.html#stability-of-parameters>`_)。

使用后清理 (Cleaning up after use)
  为了在系统受损时最小化影响,建议应用程序在不再使用敏感数据时从内存中擦除所有敏感数据 (To minimize impact if the system is compromised, it is recommended that applications wipe all sensitive data from memory when it is no longer used)。这样,只有当前使用的数据可能会泄漏,过去的数据不会受到损害 (That way, only data that is currently in use can be leaked, and past data is not compromised)。

  擦除敏感数据包括 (Wiping sensitive data includes):

  * 清除栈或堆中的临时缓冲区 (Clearing temporary buffers in the stack or on the heap)。

  * 如果操作不会完成,则中止操作 (Aborting operations if they will not be finished)。

  * 销毁不再使用的密钥 (Destroying keys that are no longer used)。

参考资料 (References)
**********************

* `PSA Crypto`_

.. _PSA Crypto:
   https://arm-software.github.io/psa-api/crypto/

* `Mbed TLS`_

.. _Mbed TLS:
   https://www.trustedfirmware.org/projects/mbed-tls/
