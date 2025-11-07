.. _shields:

Shields (屏蔽板/扩展板)
########################

Shields(也称为"附加板"或"子板")连接到板上以扩展其功能和服务,以便更轻松和模块化的原型设计。在 Zephyr 中,shield 功能提供 Zephyr 格式的 shield 描述,以便与应用程序更轻松地兼容。

Shield 激活 (Shield activation)
********************************

通过向 west 命令添加匹配的 ``--shield`` 参数来激活对一个或多个 shield 的支持:

  .. zephyr-app-commands::
     :app: your_app
     :board: your_board
     :shield: x_nucleo_idb05a1,x_nucleo_iks01a1
     :goals: build


或者,可以在项目的 CMakeLists.txt 中默认设置:

.. code-block:: cmake

	set(SHIELD x_nucleo_iks01a1)


Shield 接口 (Shield interfaces)
*********************************

Shield 由两个关键特征定义:

#. **物理连接器** - 机械接口
#. **电信号** - 每个引脚实际执行的功能

Shield 和板之间的连接通过 Devicetree 文件进行:

- 板侧: 板的 devicetree 文件使用 :ref:`GPIO nexus node <gpio-nexus-node>` 将连接器引脚映射到微控制器的实际 GPIO 引脚。它还为通过连接器公开的总线定义标签(如 ``arduino_i2c``、``arduino_spi``、``arduino_uart``)。

- Shield 侧: Shield 的 .overlay 文件引用这些相同的标签来描述其组件如何连接到板。

在构建时,板的 devicetree 和 shield 的 overlay 结合在一起,创建硬件设置的完整图像。

例如,假设您有一个带有 Arduino 连接器但没有内置加速度计的板。您可以使用 Arduino shield 添加一个:

#. 板的 Devicetree 定义 ``arduino_i2c`` 标签: 它是 Arduino 连接器上可用的 I2C 总线

#. 加速度计 shield 的 overlay 文件也引用 ``arduino_i2c`` 以指示它使用同一 I2C 总线。如果它需要使用连接器的 GPIO 引脚,它引用板的 Devicetree 定义的 GPIO nexus 节点(例如 ``arduino_header``)。

当您使用此 shield 为此板构建时,Zephyr 会自动"将它们连接"在一起。

.. note::

   Some boards and shields may only support a limited set of features of a shield hardware
   interface. Refer to their documentation for more details.


Arduino MKR
-----------

这是 Arduino MKR 板的外形尺寸。

.. figure:: ../../../boards/arduino/mkrzero/doc/img/arduino_mkrzero.jpg
   :align: center
   :width: 200px
   :alt: Arduino MKR Zero

   Arduino MKR Zero,具有 Arduino MKR shield 接口的板示例

相关的 devicetree 节点标签:

- ``arduino_mkr_header`` 有关 GPIO 引脚定义和用于 devicetree 文件的包含的详细信息,请参阅 :dtcompatible:`arduino-mkr-header`。
- ``arduino_mkr_i2c``
- ``arduino_mkr_spi``
- ``arduino_mkr_serial``


Arduino Nano
------------

这是 Arduino Nano 板的外形尺寸。

.. figure:: ../../../boards/arduino/nano_33_iot/doc/img/nano_33_iot.jpg
   :align: center
   :width: 300px
   :alt: Arduino Nano 33 IOT

   Arduino Nano 33 IOT,具有 Arduino Nano shield 接口的板示例

相关的 devicetree 节点标签:

- ``arduino_nano_header`` 有关 GPIO 引脚定义和用于 devicetree 文件的包含的详细信息,请参阅 :dtcompatible:`arduino-nano-header`。
- ``arduino_nano_i2c``
- ``arduino_nano_spi``
- ``arduino_nano_serial``


Arduino Uno R3
--------------

这是 Arduino Uno R3 板的外形尺寸。

.. figure:: ../../../boards/shields/mcp2515/doc/keyestudio_can_bus_ks0411.jpg
   :align: center
   :width: 300px
   :alt: Keyestudio CAN-BUS Shield (KS0411)

   Keyestudio CAN-BUS,Arduino shield 示例(Credit: Keyestudio)

相关的 devicetree 节点标签:

- ``arduino_header`` 有关 GPIO 引脚定义和用于 devicetree 文件的包含的详细信息,请参阅 :dtcompatible:`arduino-header-r3`。
- ``arduino_adc`` 参阅 :dtcompatible:`arduino,uno-adc`
- ``arduino_pwm`` 参阅 :dtcompatible:`arduino-header-pwm`
- ``arduino_serial``
- ``arduino_i2c``
- ``arduino_spi``

有关技术细节,请参阅 `Arduino Uno R3 pinout`_。


相机和显示器连接器 (Camera and display connectors)
----------------------------------------------------

这些描述与相机和显示器的连接(严格来说不是 shield)。

- :dtcompatible:`arducam,dvp-20pin-connector`
- :dtcompatible:`nxp,cam-44pins-connector`
- :dtcompatible:`nxp,parallel-lcd-connector`
- :dtcompatible:`raspberrypi,csi-connector`
- :dtcompatible:`weact,dcmi-camera-connector`


Feather
-------

这是 Adafruit Feather 系列板的外形尺寸。
用于 Feather 板的 Shield 称为 Featherwing。

.. figure:: ../../../boards/shields/adafruit_adalogger_featherwing/doc/adafruit_adalogger_featherwing.webp
   :align: center
   :width: 300px
   :alt: Adafruit Adalogger Featherwing Shield

   Adafruit Adalogger,Featherwing 的一个示例 (Credit: Adafruit)

相关的 devicetree 节点标签:

- ``feather_header`` 有关 GPIO 引脚定义,请参阅 :dtcompatible:`adafruit-feather-header`。
- ``feather_adc``
- ``feather_i2c``
- ``feather_serial``
- ``feather_spi``


Microbit
--------

这适用于 Microbit 板的边缘连接器。

.. figure::  ../../../boards/bbc/microbit_v2/doc/img/bbc_microbit2.jpg
   :align: center
   :width: 500px
   :alt: Microbit V2 board

   Microbit V2 板使用 Microbit shield 接口

有关 GPIO 引脚定义和技术要求链接,请参阅 :dtcompatible:`microbit,edge-connector`。


mikroBUS |trade|
----------------

这是一个由 Mikroe 开发的附加板接口标准。

.. figure:: ../../../boards/shields/mikroe_3d_hall_3_click/doc/images/mikroe_3d_hall_3_click.webp
   :align: center
   :alt: 3D Hall 3 Click
   :height: 300px

   3D Hall 3 Click,mikroBUS |trade| shield 的一个示例

相关的 devicetree 节点标签:

- ``mikrobus_header`` 有关 GPIO 引脚定义和技术规范链接,请参阅 :dtcompatible:`mikro-bus`。
- ``mikrobus_adc``
- ``mikrobus_i2c``
- ``mikrobus_spi``
- ``mikrobus_serial``

请注意,具有多个 mikroBUS |trade| 连接器的板可能会定义例如 ``mikrobus_2_spi``。


Pico
----

这是 Raspberry Pi Pico 板的外形尺寸。

.. figure::  ../../../boards/shields/waveshare_ups/doc/waveshare_pico_ups_b.jpg
   :align: center
   :width: 300px
   :alt: Waveshare Pico UPS-B shield

   Waveshare Pico UPS-B,Pico shield 的一个示例

相关的 devicetree 节点标签:

- ``pico_header`` 有关 GPIO 引脚定义,请参阅 :dtcompatible:`raspberrypi,pico-header`。
- ``pico_i2c0``
- ``pico_i2c1``
- ``pico_serial``
- ``pico_spi``


ST Morpho
---------

ST Microelectronics 的开发板通常使用 ST Morpho shield 接口。

.. figure:: ../../../boards/shields/x_nucleo_gfx01m2/doc/x_nucleo_gfx01m2.webp
   :align: center
   :width: 300px
   :alt: X-NUCLEO-GFX01M2

   X-NUCLEO-GFX01M2,ST Morpho shield 的一个示例

相关的 devicetree 节点标签:

- ``st_morpho_header`` 有关 GPIO 引脚定义详细信息和用于 devicetree 文件的包含,请参阅 :dtcompatible:`st-morpho-header`。
- ``st_morpho_lcd_spi``
- ``st_morpho_flash_spi``


Xiao
----

这是 Seeeduino XIAO 板的外形尺寸。

.. figure:: ../../../boards/shields/seeed_xiao_expansion_board/doc/img/seeed_xiao_expansion_board.webp
     :align: center
     :width: 300px
     :alt: Seeed Studio XIAO Expansion Board

     Seeed Studio XIAO Expansion Board,Xiao shield 的一个示例 (Credit: Seeed Studio)

相关的 devicetree 节点标签:

- ``xiao_d`` 有关 GPIO 引脚定义,请参阅 :dtcompatible:`seeed,xiao-gpio`。
- ``xiao_spi``
- ``xiao_i2c``
- ``xiao_serial``
- ``xiao_adc``
- ``xiao_dac``


zephyr_i2c / Stemma QT / Quiic
------------------------------

这些是四引脚 I2C 连接器。SparkFun 将这些连接器称为"Qwiic",Adafruit 将其称为"Stemma QT"。I2C 连接器有四个引脚:GND、+3.3 Volt、I2C 数据和 I2C 时钟。最常见的物理连接器是 1.0 mm 间距的 JST-SH。

由于不同的品牌名称,该接口被标记为"zephyr_i2c"。

.. figure::  ../../../boards/shields/adafruit_vcnl4040/doc/adafruit_vcnl4040.webp
   :align: center
   :width: 200px
   :alt: Adafruit VCNL4040 Shield

   Adafruit VCNL4040,zephyr_i2c shield 的一个示例 (Credit: Adafruit)

有关描述和更多详细信息链接,请参阅 :dtcompatible:`stemma-qt-connector` 和 :dtcompatible:`grove-header`。

相关的 devicetree 节点标签:

- ``zephyr_i2c``


.. _shield_porting_guide:

Shield 移植和配置 (Shield porting and configuration)
*****************************************************

Shield 配置文件在板目录 :zephyr_file:`boards/shields` 下可用:

.. code-block:: none

   boards/shields/<shield>
   ├── shield.yml
   ├── <shield>.overlay
   ├── Kconfig.shield
   ├── Kconfig.defconfig
   └── pre_dt_shield.cmake

这些文件提供如下 shield 配置:

* **shield.yml**: 此文件以 YAML 格式提供有关 shield 的元数据。
  它必须包含以下字段:

  * ``name``: 在 Kconfig 和构建系统中使用的 shield 名称(必需)
  * ``full_name``: shield 的完整商业名称(必需)
  * ``vendor``: shield 的制造商/供应商(必需)
  * ``supported_features``: shield 支持的硬件特性列表(可选)。为了帮助用户识别 shield 支持的特性而无需深入研究其 overlay 文件,可以使用 ``supported_features`` 字段列出 shield 支持的特性类型。这些值应与 :zephyr_file:`dts/bindings/binding-types.txt` 文件中定义的值相同。

  示例:

  .. code-block:: yaml

     name: foo_shield
     full_name: Foo Shield for Arduino
     vendor: acme
     supported_features:
       - display
       - input

* **<shield>.overlay**: 此文件以 devicetree 格式提供 shield 描述,在编译之前与板的 :ref:`devicetree <dt-guide>` 合并。

* **Kconfig.shield**: 此文件定义将用于默认 shield 配置的 shield Kconfig 符号。为了便于与应用程序一起使用,此处的默认 shield 配置应与 :ref:`default_board_configuration` 中的配置保持一致。

* **Kconfig.defconfig**: 此文件定义默认的 shield 配置。它与 :ref:`default_board_configuration` 保持一致。因此,应该记住,功能激活是应用程序的责任。

* **pre_dt_shield.cmake**: 此可选文件可用于向 devicetree 编译器 ``dtc`` 传递附加参数。

此外,为了避免与可能在板级定义的设备发生名称冲突,建议专门为 shield devicetree 描述提供形式为 <device>_<shield> 的设备节点标签,例如:

.. code-block:: devicetree

        sdhc_myshield: sdhc@1 {
                reg = <1>;
                ...
        };

添加源代码 (Adding Source Code)
********************************

可以向 shield 添加源代码,作为满足 shield 特定配置要求(例如:初始化例程、时序约束等)的一种方式,以便与不同的 Zephyr 组件正常运行。

.. note::

   Shield 中的源代码不得用于上述目的以外的其他目的。可以在 shield(和/或目标)之间重用的通用功能不应在此处捕获。

要有效地合并源代码:添加 :file:`CMakeLists.txt` 文件以及相应的源文件(在 CMake 中引用,类似于 Zephyr 的其他区域,例如:板)。

板兼容性 (Board compatibility)
********************************

硬件 shield 到板的兼容性取决于在流行板上使用的知名连接器(例如 Arduino 和 96boards)的使用。对于软件兼容性,板还必须提供与其支持的连接器匹配的配置。

这应该在两个不同的级别完成:

* Pinmux: 连接器引脚应正确配置以匹配 shield 引脚

* Devicetree: 板 :ref:`devicetree <dt-guide>` 文件 :file:`BOARD.dts` 应为每个连接器接口定义替代节点标签。例如,对于 Arduino I2C:

.. code-block:: devicetree

        arduino_i2c: &i2c1 {};

板特定的 shield 配置 (Board specific shield configuration)
------------------------------------------------------------

如果需要修改以使 shield 适应特定板或板修订版,您可以通过向 shield 添加板或板修订版覆盖文件来覆盖特定板的 shield 描述,如下所示:

.. code-block:: none

   boards/shields/<shield>
   └── boards
       ├── <board>_<revision>.overlay
       ├── <board>.overlay
       ├── <board>.defconfig
       ├── <board>_<revision>.conf
       └── <board>.conf


Shield 变体 (Shield variants)
******************************

某些 shield 可能支持多个变体或修订版。在这种情况下,可以提供多个版本的 shield 描述:

.. code-block:: none

   boards/shields/<shield>
   ├── <shield_v1>.overlay
   ├── <shield_v1>.defconfig
   ├── <shield_v2>.overlay
   └── <shield_v2>.defconfig

在这种情况下,可以使用 shield 特定的修订版名称:

  .. zephyr-app-commands::
     :app: your_app
     :shield: shield_v2
     :goals: build

您还可以为特定的 shield 修订版提供板特定的配置:

.. code-block:: none

   boards/shields/<shield>
   ├── <shield_v1>.overlay
   ├── <shield_v1>.defconfig
   ├── <shield_v2>.overlay
   ├── <shield_v2>.defconfig
   └── boards
       └── <shield_v2>
           ├── <board>.overlay
           └── <board>.defconfig

.. _gpio-nexus-node:

GPIO nexus 节点 (GPIO nexus nodes)
***********************************

Shield 外设访问的 GPIO 必须使用 shield GPIO 抽象来识别,例如来自 ``arduino-header-r3`` 兼容性。提供此接头的板必须将接头引脚映射到 SOC 特定的引脚。这是通过在板 devicetree 文件中包含如下所示的 `nexus node`_ 来实现的:

.. _nexus node:
    https://github.com/devicetree-org/devicetree-specification/blob/4b1dac80eaca45b4babf5299452a951008a5d864/source/devicetree-basics.rst#nexus-nodes-and-specifier-mapping

.. code-block:: devicetree

    arduino_header: connector {
            compatible = "arduino-header-r3";
            #gpio-cells = <2>;
            gpio-map-mask = <0xffffffff 0xffffffc0>;
            gpio-map-pass-thru = <0 0x3f>;
            gpio-map = <0 0 &gpioa 0 0>,    /* A0 */
                       <1 0 &gpioa 1 0>,    /* A1 */
                       <2 0 &gpioa 4 0>,    /* A2 */
                       <3 0 &gpiob 0 0>,    /* A3 */
                       <4 0 &gpioc 1 0>,    /* A4 */
                       <5 0 &gpioc 0 0>,    /* A5 */
                       <6 0 &gpioa 3 0>,    /* D0 */
                       <7 0 &gpioa 2 0>,    /* D1 */
                       <8 0 &gpioa 10 0>,   /* D2 */
                       <9 0 &gpiob 3 0>,    /* D3 */
                       <10 0 &gpiob 5 0>,   /* D4 */
                       <11 0 &gpiob 4 0>,   /* D5 */
                       <12 0 &gpiob 10 0>,  /* D6 */
                       <13 0 &gpioa 8 0>,   /* D7 */
                       <14 0 &gpioa 9 0>,   /* D8 */
                       <15 0 &gpioc 7 0>,   /* D9 */
                       <16 0 &gpiob 6 0>,   /* D10 */
                       <17 0 &gpioa 7 0>,   /* D11 */
                       <18 0 &gpioa 6 0>,   /* D12 */
                       <19 0 &gpioa 5 0>,   /* D13 */
                       <20 0 &gpiob 9 0>,   /* D14 */
                       <21 0 &gpiob 8 0>;   /* D15 */
    };

这指定了 Arduino 引脚引用(如 ``<&arduino_header 11 0>``)如何转换为 SOC GPIO 引脚引用(如 ``<&gpiob 4 0>``)。

在 Zephyr 中,GPIO 说明符通常有两个参数(由 ``#gpio-cells = <2>`` 指示):引脚号和一组标志。标志的低 6 位对应于可以在 devicetree 中配置的功能。在某些情况下,需要使用非零标志值来告诉驱动程序特定引脚的行为方式,例如:

.. code-block:: devicetree

    drdy-gpios = <&arduino_header 11 GPIO_ACTIVE_LOW>;

预处理后,这变为 ``<&arduino_header 11 1>``。通常,这种标志的存在会导致映射查找失败,因为没有具有非零标志值的映射条目。``gpio-map-mask`` 属性指定,对于查找,使用引脚的所有位和标志的除低 6 位之外的所有位来识别说明符。然后 ``gpio-map-pass-thru`` 指定复制标志的低 6 位,因此 SOC GPIO 引用按预期变为 ``<&gpiob 4 1>``。

有关此功能的更多信息,请参阅 `nexus node`_。


.. _Arduino Uno R3 pinout:
  https://docs.arduino.cc/resources/pinouts/A000066-full-pinout.pdf
