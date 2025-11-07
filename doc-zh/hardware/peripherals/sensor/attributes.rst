.. _sensor-attribute:

传感器属性 (Sensor Attributes)
###############################

:dfn:`属性`，在 :c:enum:`sensor_attribute` 中枚举，是传感器及其通道的不可变和可变属性。

属性允许获取传感器的元数据并更改其配置。
常见的配置参数如通道比例、采样频率、调整通道偏移、信号滤波、功耗模式、
片上缓冲区和事件处理选项非常常见。属性为检查和操作此类设备属性提供了灵活的 API。

属性使用 :c:enum:`sensor_attribute` 指定，可以与 :c:func:`sensor_attr_get`
和 :c:func:`sensor_attr_set` 一起使用来获取和设置传感器的属性。

一个简单的示例...

.. code-block:: c

   const struct device *accel_dev = DEVICE_DT_GET(DT_ALIAS(accel0));
   struct sensor_value accel_sample_rate;
   int rc;

   rc = sensor_attr_get(accel_dev, SENSOR_CHAN_ACCEL_XYZ, SENSOR_ATTR_SAMPLING_FREQUENCY, &accel_sample_rate);
   if (rc != 0) {
                printk("Failed to get sampling frequency\n");
   }

   printk("Sample rate for accel %p is %d.06%d\n", accel_dev, accel_sample_rate.val1, accel_sample_rate.val2*1000000);

   accel_sample_rate.val1 = 2000;

   rc = sensor_attr_set(accel_dev, SENSOR_CHAN_ACCEL_XYZ, SENSOR_ATTR_SAMPLING_FREQUENCY, accel_sample_rate);
   if (rc != 0) {
                printk("Failed to set sampling frequency\n");
   }
