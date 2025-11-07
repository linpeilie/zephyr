.. _stepper_api:

步进器 (Steppers)
##################

步进器驱动程序 API 提供了一组用于控制和配置步进器驱动程序的函数。

配置步进器驱动程序 (Configure Stepper Driver)
===============================================

- 使用 :c:func:`stepper_set_micro_step_res` 和 :c:func:`stepper_get_micro_step_res` 配置**微步分辨率**。
- 使用 :c:func:`stepper_set_reference_position` 和 :c:func:`stepper_get_actual_position` 配置以微步为单位的**参考位置**。
- 使用 :c:func:`stepper_set_microstep_interval` 设置步之间的**步进间隔**,以纳秒为单位。
- 使用 :c:func:`stepper_enable` **启用**步进器驱动程序。
- 使用 :c:func:`stepper_disable` **禁用**步进器驱动程序。

控制步进器 (Control Stepper)
==============================

- 使用 :c:func:`stepper_move_by` 进行 +/- 微步**移动**,也称为**相对移动**。
- 使用 :c:func:`stepper_move_to` **移动到**特定位置,也称为**绝对移动**。
- 使用 :c:func:`stepper_run` 以特定方向以**恒定步进间隔**连续运行,直到检测到停止。
- 使用 :c:func:`stepper_stop` **停止**步进器。
- 使用 :c:func:`stepper_is_moving` 检查步进器是否**正在移动**。
- 使用 :c:func:`stepper_set_event_callback` 注册**事件回调**。

设备树 (Device Tree)
=====================

在步进器控制器的上下文中,设备树为每个设备级别的步进器驱动程序提供初始硬件配置。每个设备必须在 Zephyr 中指定设备树绑定,理想情况下,还应提供一组硬件配置选项,例如电流设置、斜坡参数等。然后,这些可以在板的设备树中用于将步进器驱动程序配置为其初始状态。

示例见:

- :dtcompatible:`zephyr,h-bridge-stepper`
- :dtcompatible:`adi,tmc50xx`

Discord
=======

Zephyr 有一个 `stepper discord`_ 频道用于步进器相关讨论,对所有人开放。

.. _stepper-api-reference:

步进器 API 测试套件 (Stepper API Test Suite)
==============================================

The stepper API test suite provides a set of tests that can be used to verify the functionality of
stepper drivers.

.. zephyr-app-commands::
   :zephyr-app: tests/drivers/stepper/stepper_api
   :board: <board>
   :west-args: --extra-dtc-overlay <path/to/board.overlay>
   :goals: build flash

Sample Output
=============

Below is a snippet of the test output for the tmc50xx stepper driver. Since
:c:func:`stepper_set_microstep_interval` is not implemented by the driver the corresponding tests
have been skipped.

.. code-block:: console

   ===================================================================
   TESTSUITE stepper succeeded

   ------ TESTSUITE SUMMARY START ------

   SUITE PASS - 100.00% [stepper]: pass = 4, fail = 0, skip = 2, total = 6 duration = 0.069 seconds
    - PASS - [stepper.test_actual_position] duration = 0.016 seconds
    - PASS - [stepper.test_get_micro_step_res] duration = 0.013 seconds
    - SKIP - [stepper.test_set_micro_step_interval_invalid_zero] duration = 0.007 seconds
    - PASS - [stepper.test_set_micro_step_res_incorrect] duration = 0.010 seconds
    - PASS - [stepper.test_stop] duration = 0.016 seconds
    - SKIP - [stepper.test_target_position_w_fixed_step_interval] duration = 0.007 seconds

   ------ TESTSUITE SUMMARY END ------

   ===================================================================
   PROJECT EXECUTION SUCCESSFUL

API Reference
*************

A common set of functions which should be implemented by all stepper drivers.

.. doxygengroup:: stepper_interface

Stepper controller specific APIs
********************************

Trinamic
========

.. doxygengroup:: trinamic_stepper_interface

.. _stepper discord:
   https://discord.com/channels/720317445772017664/1278263869982375946
