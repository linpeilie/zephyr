设备树 (Device Tree)
#####################

在传感器的上下文中，设备树在每个设备级别为传感器提供初始硬件配置。
每个设备必须在 Zephyr 中指定设备树绑定，理想情况下，还要指定一组硬件配置选项，
用于通道功耗模式、数据速率、滤波器、抽取和比例等。
然后可以在开发板的设备树中使用这些选项来将传感器配置为其初始状态。

.. code-block:: dts

   #include <zephyr/dt-bindings/icm42688.h>

   &spi0 {
       /* SPI 总线选项在这里，未显示 */

       accel_gyro0: icm42688p@0 {
           compatible = "invensense,icm42688", "invensense,icm4268x";
           reg = <0>;
           int-gpios = <&pioc 6 GPIO_ACTIVE_HIGH>; /* 为中断线选择的 SoC 特定引脚 */
           spi-max-frequency = <DT_FREQ_M(24)>; /* 最大 SPI 总线频率 */
           accel-pwr-mode = <ICM42688_ACCEL_LN>; /* 低噪声模式 */
           accel-odr = <ICM42688_ACCEL_ODR_2000>; /* 2000 Hz 采样 */
           accel-fs = <ICM42688_ACCEL_FS_16>; /* 16G 比例 */
           gyro-pwr-mode = <ICM42688_GYRO_LN>; /* 低噪声模式 */
           gyro-odr = <ICM42688_GYRO_ODR_2000>; /* 2000 Hz 采样 */
           gyro-fs = <ICM42688_GYRO_FS_16>; /* 16G 比例 */
       };
    };
