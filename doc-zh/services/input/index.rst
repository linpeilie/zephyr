.. _input:

输入 (Input)
#############

输入子系统提供了一个API,用于将输入事件从输入设备分发到应用程序 (The input subsystem provides an API for dispatching input events from input devices to the application)。

输入事件 (Input Events)
*************************

该子系统围绕 :c:struct:`input_event` 结构构建 (The subsystem is built around the :c:struct:`input_event` structure)。输入事件表示单个事件实体的变化 (An input event represents a change in an individual event entity),例如单个按钮的状态,或单个轴的移动 (for example the state of a single button, or a movement in a single axis)。

:c:struct:`input_event` 结构描述特定事件 (The :c:struct:`input_event` structure describes the specific event),并包含一个同步位以指示设备达到稳定状态 (and includes a synchronization bit to indicate that the device reached a stable state),例如当已报告多轴设备的多个轴对应的事件时 (for example when the events corresponding to multiple axes of a multi-axis device have been reported)。

输入设备 (Input Devices)
**************************

输入设备可以使用 :c:func:`input_report` 或任何相关函数直接报告输入事件 (An input device can report input events directly using :c:func:`input_report` or any related function);例如按钮或其他开关输入实体将使用 :c:func:`input_report_key` (for example buttons or other on-off input entities would use :c:func:`input_report_key`)。

复杂设备可能使用多个事件的组合 (Complex devices may use a combination of multiple events),并在输出稳定后设置 ``sync`` 位 (and set the ``sync`` bit once the output is stable)。

``input_report*`` 函数接受一个 :c:struct:`device` 指针 (The ``input_report*`` functions take a :c:struct:`device` pointer),用于指示哪个设备报告了事件 (which is used to indicate which device reported the event),订阅者可以使用它来仅接收来自特定设备的事件 (and can be used by subscribers to only receive events from a specific device)。如果没有与事件关联的实际设备 (If there's no actual device associated with the event),可以将其设置为 ``NULL`` (it can be set to ``NULL``),在这种情况下,只有没有设备过滤器的订阅者才会接收该事件 (in which case only subscribers with no device filter will receive the event)。

应用程序API (Application API)
*******************************

应用程序可以使用 :c:macro:`INPUT_CALLBACK_DEFINE` 宏注册回调 (An application can register a callback using the :c:macro:`INPUT_CALLBACK_DEFINE` macro)。如果指定了设备节点 (If a device node is specified),则仅针对来自特定设备的事件调用回调 (the callback is only invoked for events from the specific device),否则回调将接收系统中的所有事件 (otherwise the callback will receive all the events in the system)。这是唯一支持的过滤类型 (This is the only type of filtering supported),任何更复杂的过滤逻辑都必须在回调本身中实现 (any more complex filtering logic has to be implemented in the callback itself)。

子系统可以同步操作或使用事件队列 (The subsystem can operate synchronously or by using an event queue),具体取决于 :kconfig:option:`CONFIG_INPUT_MODE` 选项 (depending on the :kconfig:option:`CONFIG_INPUT_MODE` option)。如果使用输入线程 (If the input thread is used),所有事件都会添加到队列并在公共 ``input`` 线程中执行 (all the events are added to a queue and executed in a common ``input`` thread)。
如果不使用线程 (If the thread is not used),则直接在输入驱动程序上下文中调用回调 (the callback are invoked directly in the input driver context)。

同步模式可以在简单应用程序中使用以保持最小占用空间 (The synchronous mode can be used in a simple application to keep a minimal footprint),或在具有现有事件模型的复杂应用程序中使用 (or in a complex application with an existing event model),其中回调只是将事件管道传回更复杂的应用程序特定事件系统的包装器 (where the callback is just a wrapper to pipe back the event in a more complex application specific event system)。

HID代码映射 (HID code mapping)
********************************

输入设备的常见用例是使用它们生成HID报告 (A common use case for input devices is to use them to generate HID reports)。为此 (For this purpose),可以使用 :c:func:`input_to_hid_code` 和 :c:func:`input_to_hid_modifier` 函数将输入代码映射到HID代码和修饰符 (the :c:func:`input_to_hid_code` and :c:func:`input_to_hid_modifier` functions can be used to map input codes to HID codes and modifiers)。

通用驱动程序 (General Purpose Drivers)
****************************************

- :dtcompatible:`adc-keys`: 用于连接到电阻梯的按钮 (for buttons connected to a resistor ladder)。
- :dtcompatible:`analog-axis`: 用于连接到ADC输入的绝对位置设备 (for absolute position devices connected to an ADC input) (摇杆、滑块等 (thumbsticks, sliders...))。
- :dtcompatible:`gpio-kbd-matrix`: 用于GPIO连接的键盘矩阵 (for GPIO-connected keyboard matrices)。
- :dtcompatible:`gpio-keys`: 用于直接连接到GPIO的开关 (for switches directly connected to a GPIO),实现按钮去抖动 (implements button debouncing)。
- :dtcompatible:`gpio-qdec`: 用于GPIO连接的正交编码器 (for GPIO-connected quadrature encoders)。
- :dtcompatible:`input-keymap`: 将键盘矩阵的行/列/触摸事件映射到按键事件 (maps row/col/touch events from a keyboard matrix to key events)。
- :dtcompatible:`zephyr,input-longpress`: 监听按键事件 (listens for key events),发出短按和长按事件 (emits events for short and long press)。
- :dtcompatible:`zephyr,input-double-tap`: 监听按键事件 (listens for key events),发出输入双击事件 (emits events for input double taps)。
- :dtcompatible:`zephyr,lvgl-button-input`
  :dtcompatible:`zephyr,lvgl-encoder-input`
  :dtcompatible:`zephyr,lvgl-keypad-input`
  :dtcompatible:`zephyr,lvgl-pointer-input`: 监听输入事件并将其转换为各种类型的LVGL输入设备 (listens for input events and translates those to various types of LVGL input devices)。

详细驱动程序文档 (Detailed Driver Documentation)
**************************************************

.. toctree::
   :maxdepth: 1

   gpio-kbd.rst


API参考 (API Reference)
************************

.. doxygengroup:: input_interface

输入事件定义 (Input Event Definitions)
****************************************

.. doxygengroup:: input_events

模拟轴API参考 (Analog Axis API Reference)
*******************************************

.. doxygengroup:: input_analog_axis

触摸屏API参考 (Touchscreen API Reference)
*******************************************

.. doxygengroup:: touch_events
