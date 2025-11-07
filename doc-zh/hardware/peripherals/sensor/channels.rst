.. _sensor-channel:

传感器通道 (Sensor Channels)
#############################

:dfn:`通道`，在 :c:enum:`sensor_channel` 中枚举，是传感器设备可以测量的量。

传感器可能有多个通道，要么表示同一物理属性的不同轴(例如加速度)；
要么因为它们可以测量完全不同的属性(环境温度、压力和湿度)。
传感器可能有多个相同测量类型的通道，以便测量许多读数，
例如温度、光强度、电流、电压或电容。

在 Zephyr 中使用 :c:struct:`sensor_chan_spec` 指定通道，
它是一个包含通道类型(:c:enum:`sensor_channel`)和通道索引的对。
有时仅使用 :c:enum:`sensor_channel`，但这应该被视为历史遗留，
因为 Zephyr 3.7 引入了 :c:struct:`sensor_chan_spec`。
