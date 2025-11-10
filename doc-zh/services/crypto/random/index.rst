.. _random_api:

随机数生成 (Random Number Generation)
######################################

随机API子系统在加密安全和非加密安全实例中都提供随机数生成API (The random API subsystem provides random number generation APIs in both cryptographically and non-cryptographically secure instances)。使用哪个随机API基于随机数的加密要求 (Which random API to use is based on the cryptographic requirements of the random number)。如果需要非加密值,非加密API将更快地返回随机值 (The non-cryptographic APIs will return random values much faster if non-cryptographic values are needed)。

加密安全的随机函数应符合FIPS 140-2 [NIST02]_ 推荐的算法 (The cryptographically secure random functions shall be compliant to the FIPS 140-2 [NIST02]_ recommended algorithms)。基于硬件的随机数生成器(RNG)可以在具有适当硬件支持的平台上使用 (Hardware based random-number generators (RNG) can be used on platforms with appropriate hardware support)。
没有硬件RNG支持的平台应使用 `CTR-DRBG算法 <https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-90Ar1.pdf>`_ (Platforms without hardware RNG support shall use the `CTR-DRBG algorithm <https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-90Ar1.pdf>`_)。

该算法可以由 `mbedTLS <https://tls.mbed.org/ctr-drbg-source-code>`_ 提供 (The algorithm can be provided by  `mbedTLS <https://tls.mbed.org/ctr-drbg-source-code>`_)。

  .. note::

    CTR-DRBG生成器需要熵源来建立和维护PRNG的加密安全性 (The CTR-DRBG generator needs an entropy source to establish and maintain the cryptographic security of the PRNG)。

.. _random_kconfig:

Kconfig选项 (Kconfig Options)
******************************

这些选项可以在以下路径中找到 :zephyr_file:`subsys/random/Kconfig`。

:kconfig:option:`CONFIG_TEST_RANDOM_GENERATOR`
 用于测试,此选项允许使用非随机数生成器,并允许随机数API返回并非真正随机的值 (For testing, this option allows a non-random number generator to be used and permits random number APIs to return values that are not truly random)。

随机数生成器选择组允许通过RNG_GENERATOR_CHOICE选择组为系统选择RNG源函数 (The random number generator choice group allows selection of the RNG source function for the system via the RNG_GENERATOR_CHOICE choice group)。可以通过在SOC或板的.defconfig文件中使用以下内容来指定默认值的覆盖 (An override of the default value can be specified in the SOC or board .defconfig file by using):

.. code-block:: none

   choice RNG_GENERATOR_CHOICE
	   default XOSHIRO_RANDOM_GENERATOR
   endchoice

可用的随机数生成器包括 (The random number generators available include):

:kconfig:option:`CONFIG_TIMER_RANDOM_GENERATOR`
 启用基于系统定时器时钟的数字生成器 (enables number generator based on system timer clock)。此数字生成器不是随机的,仅用于测试 (This number generator is not random and used for testing only)。

:kconfig:option:`CONFIG_ENTROPY_DEVICE_RANDOM_GENERATOR`
 启用使用已启用的硬件熵收集驱动程序生成随机数的随机数生成器 (enables a random number generator that uses the enabled hardware entropy gathering driver to generate random numbers)。

:kconfig:option:`CONFIG_XOSHIRO_RANDOM_GENERATOR`
 启用Xoshiro128++伪随机数生成器,它使用熵驱动程序作为种子源 (enables the Xoshiro128++ pseudo-random number generator, that uses the entropy driver as a seed source)。

CSPRNG_GENERATOR_CHOICE选择组提供加密安全随机数生成器源函数的选择 (The CSPRNG_GENERATOR_CHOICE choice group provides selection of the cryptographically secure random number generator source function)。可以通过在SOC或板的.defconfig文件中使用以下内容来指定默认值的覆盖 (An override of the default value can be specified in the SOC or board .defconfig file by using):

.. code-block:: none

   choice CSPRNG_GENERATOR_CHOICE
	   default CTR_DRBG_CSPRNG_GENERATOR
   endchoice

可用的加密安全随机数生成器包括 (The cryptographically secure random number generators available include):

:kconfig:option:`CONFIG_HARDWARE_DEVICE_CS_GENERATOR`
 启用使用硬件随机生成器驱动程序的加密安全随机数生成器 (enables a cryptographically secure random number generator using the hardware random generator driver)

:kconfig:option:`CONFIG_CTR_DRBG_CSPRNG_GENERATOR`
 启用CTR-DRBG伪随机数生成器 (enables the CTR-DRBG pseudo-random number generator)。CTR-DRBG是FIPS140-2推荐的加密安全随机数生成器 (The CTR-DRBG is a FIPS140-2 recommended cryptographically secure random number generator)。

除了熵源之外,还可以提供个性化数据,以使CTR-DRBG的初始化尽可能独特 (Personalization data can be provided in addition to the entropy source to make the initialization of the CTR-DRBG as unique as possible)。

:kconfig:option:`CONFIG_CS_CTR_DRBG_PERSONALIZATION`
 CTR-DRBG初始化个性化字符串 (CTR-DRBG Initialization Personalization string)

API参考 (API Reference)
***********************

.. doxygengroup:: random_api
