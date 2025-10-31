.. _timeutil_api:

时间工具 (Time Utilities)
##########################

概述 (Overview)
****************

Zephyr 中的 :ref:`kernel_timing_uptime` 基于滴答计数器。
使用默认的 :kconfig:option:`CONFIG_TICKLESS_KERNEL`，此计数器从系统启动时刻的零开始
以名义上恒定的速率前进。这个计数器的 POSIX 等效项类似于 ``CLOCK_MONOTONIC``，
或者在 Linux 中是 ``CLOCK_MONOTONIC_RAW``。:c:func:`k_uptime_get()`
提供此时间的毫秒表示。

应用程序通常需要将 Zephyr 内部时间与日常生活中使用的外部时间尺度相关联，
例如本地时间或协调世界时 (Coordinated Universal Time)。这些系统以不同的方式解释时间，
并且可能由于`闰秒 <https://what-if.xkcd.com/26/>`__和本地时间偏移（如夏令时）而存在不连续性。

由于这些不连续性，以及周期计数器底层时钟的显著不准确性，
从 Zephyr 时钟估计的时间与"真实"民用时间尺度中的实际时间之间的偏移不是恒定的，
并且可以在 Zephyr 应用程序的运行时内广泛变化。

时间工具 API 支持：

* :ref:`在时间表示之间转换 <timeutil_repr>`
* :ref:`同步和对齐时间尺度 <timeutil_sync>`
* :ref:`比较、添加和减法表示 <timeutil_manip>`

有关支持这些功能的术语和概念，请参见 :ref:`timeutil_concepts`。

时间工具 API (Time Utility APIs)
**********************************

.. _timeutil_repr:

表示转换 (Representation Transformation)
=========================================

时间尺度瞬间可以用多种方式表示，包括：

* 自纪元以来的秒数。此形式的时间的 POSIX 表示包括 ``time_t`` 和 ``struct timespec``，
  它们通常被解释为 `"UNIX 时间" <https://tools.ietf.org/html/rfc8536#section-2>`__ 的表示。

* 日历时间，作为相对于纪元的年、月、日、小时、分钟和秒。
  此形式的时间的 POSIX 表示包括 ``struct tm``。

请记住，这些只是时间表示，必须相对于时间尺度进行解释，
该时间尺度可能是本地时间、UTC 或其他一些连续或不连续的尺度。

一些必要的转换可在标准 C 库例程中使用。例如，测量自 POSIX 纪元以来的秒数的 ``time_t``
使用 `gmtime() <https://pubs.opengroup.org/onlinepubs/9699919799/functions/gmtime.html>`__
转换为表示日历时间的 ``struct tm``。像 ``struct timespec`` 这样的亚秒时间戳也可以使用它
来生成日历时间表示，并分别处理亚秒偏移。

逆转换不是标准化的：像 ``mktime()`` 这样的 API 期望有关时区的信息。
Zephyr 使用 :c:func:`timeutil_timegm` 和 :c:func:`timeutil_timegm64` 提供此转换。

要在 ``struct timespec`` 和 ``k_timeout_t`` 持续时间之间转换，
请使用 :c:func:`timespec_to_timeout` 和 :c:func:`timespec_from_timeout`。

.. code-block:: c

    k_timeout_t to;
    struct timespec ts;

    timespec_from_timeout(K_FOREVER, &ts);
    to = timespec_to_timeout(&ts); /* to == K_FOREVER */

    timespec_from_timeout(K_MSEC(100), &ts);
    to = timespec_to_timeout(&ts); /* to == K_MSEC(100) */

.. doxygengroup:: timeutil_repr_apis

.. _timeutil_sync:

时间尺度同步 (Time Scale Synchronization)
==========================================

有几个因素影响时间尺度的同步：

* 离散瞬间表示变化的速率。例如，Zephyr 正常运行时间以滴答为单位跟踪，
  滴答在名义上以 :kconfig:option:`CONFIG_SYS_CLOCK_TICKS_PER_SEC` 赫兹发生的事件处前进，
  而外部时间源可能以整秒或分数秒（例如微秒）提供数据。
* 在单个瞬间对齐两个尺度所需的绝对偏移。
* 每个尺度中可观察瞬间之间的相对误差，需要一致地对齐多个瞬间。
  例如，由 1 脉冲/秒 GPS 信号调节的参考时钟将比由具有 +/- 250 ppm 误差的 RC 振荡器
  驱动的 Zephyr 系统时钟准确得多。

时间尺度之间的同步或对齐通过多步过程完成：

* 时间尺度中的瞬间由（无符号）64 位整数表示，假设以固定的名义速率前进。
* :c:struct:`timeutil_sync_config` 记录参考时间尺度/源（例如 TAI）
  和本地时间源（例如 :c:func:`k_uptime_ticks`）的名义速率。
* :c:struct:`timeutil_sync_instant` 记录参考和本地时间尺度中单个瞬间的表示。
* :c:struct:`timeutil_sync_state` 为初始瞬间、最近接收的第二个观察以及可以调整每个时间尺度
  的实际速率的相对误差的偏斜提供存储。
* :c:func:`timeutil_sync_ref_from_local()` 和 :c:func:`timeutil_sync_local_from_ref()`
  将一个时间尺度中的瞬间转换为另一个时间尺度，考虑到可以通过
  :c:func:`timeutil_sync_estimate_skew` 从状态结构中存储的两个实例估计的偏斜。

.. doxygengroup:: timeutil_sync_apis

.. _timeutil_manip:

``timespec`` 操作 (``timespec`` Manipulation)
==============================================

可以使用 :c:func:`timespec_is_valid` 检查 ``timespec`` 的有效性。

.. code-block:: c

    struct timespec ts = {
        .tv_sec = 0,
        .tv_nsec = -1, /* 超出范围！ */
    };

    if (!timespec_is_valid(&ts)) {
        /* 错误处理代码 */
    }

在某些情况下，可以使用 :c:func:`timespec_normalize` 重新规范化无效的 ``timespec`` 对象。

.. code-block:: c

    if (!timespec_normalize(&ts)) {
        /* 错误处理代码 */
    }

    /* ts 应该被规范化 */
    __ASSERT(timespec_is_valid(&ts) == true, "expected normalized timespec");

可以使用 :c:func:`timespec_equal` 比较两个 ``timespec`` 对象是否相等。

.. code-block:: c

    if (timespec_equal(then, now)) {
        /* 时间到了！ */
    }

可以使用 :c:func:`timespec_compare` 比较和完全排序（有效的）``timespec`` 对象。

.. code-block:: c

    int cmp = timespec_compare(a, b);

    switch (cmp) {
    case 0:
        /* a == b */
        break;
    case -1:
        /* a < b */
        break;
    case +1:
        /* a > b */
        break;
    }

可以使用 :c:func:`timespec_add`、:c:func:`timespec_sub` 和 :c:func:`timespec_negate`
分别对 ``timespec`` 对象进行加法、减法和取反。与 :c:func:`timespec_normalize` 一样，
这些函数在不会导致溢出的情况下将输出规范化的 ``timespec``。
成功时，这些函数返回 ``true``。如果发生溢出，函数返回 ``false``。

.. code-block:: c

    /* a += b */
    if (!timespec_add(&a, &b)) {
        /* 溢出 */
    }

    /* a -= b */
    if (!timespec_sub(&a, &b)) {
        /* 溢出 */
    }

    /* a = -a */
    if (!timespec_negate(&a)) {
        /* 溢出 */
    }

.. doxygengroup:: timeutil_timespec_apis


.. _timeutil_concepts:

Zephyr 中时间支持的基础概念 (Concepts Underlying Time Support in Zephyr)
***************************************************************************

来自 `ISO/TC 154/WG 5 N0038
<https://www.loc.gov/standards/datetime/iso-tc154-wg5_n0038_iso_wd_8601-1_2016-02-16.pdf>`__
(ISO/WD 8601-1) 和其他地方的术语：

* *时间轴* (time axis) 是将时间表示为瞬间的有序序列。
* *时间尺度* (time scale) 是相对于作为纪元的原点表示瞬间的一种方式。
* 如果连续时间瞬间的表示值从不减少，则时间尺度是*单调* (monotonic)（递增）的。
* 如果表示没有突然的值变化（例如，在连续瞬间之间来回跳跃），则时间尺度是*连续* (continuous) 的。
* `民用时间 <https://en.wikipedia.org/wiki/Civil_time>`__ 通常指由民政当局
  （如地方政府）合法定义的时间尺度，通常是为了使本地午夜与太阳时对齐。

相关时间尺度 (Relevant Time Scales)
====================================

`国际原子时 <https://en.wikipedia.org/wiki/International_Atomic_Time>`__ (TAI)
是基于以 SI 秒计数的时钟平均值的时间尺度。TAI 是单调和连续的时间尺度。

`世界时 <https://en.wikipedia.org/wiki/Universal_Time>`__ (UT) 是基于地球自转的时间尺度。
UT 是不连续的时间尺度，因为它需要偶尔调整（`闰秒 <https://en.wikipedia.org/wiki/Leap_second>`__）
以保持与地球自转变化的对齐。因此，TAI 和 UT 之间的差异随时间变化。UT 有几个变体，
其中 `UTC <https://en.wikipedia.org/wiki/Coordinated_Universal_Time>`__ 是最常见的。

UT 时间独立于位置。UT 是标准时间（或"本地时间"）的基础，即特定位置的时间。
标准时间在任何给定瞬间与 UT 具有固定偏移，主要受经度影响，
但偏移可能会调整（"夏令时"）以将标准时间与当地太阳时对齐。
从某种意义上说，本地时间"比 UT 更不连续"。

`POSIX 时间 <https://tools.ietf.org/html/rfc8536#section-2>`__ 是一个时间尺度，
从 1970-01-01T00:00:00Z（即 1970 UTC 开始）的"POSIX 纪元"开始计算秒数。
`UNIX 时间 <https://tools.ietf.org/html/rfc8536#section-2>`__ 是 POSIX 时间的扩展，
使用负值表示 POSIX 纪元之前的时间。这两个尺度都假设每天正好有 86400 秒。
在正常使用中，这些尺度中的瞬间对应于 UTC 尺度中的时间，因此它们继承了不连续性。

连续类比是 `UNIX 闰秒时间 <https://tools.ietf.org/html/rfc8536#section-2>`__，
它是 UNIX 时间加上 POSIX 纪元后添加的所有闰秒校正（当 TAI-UTC 为 8 秒时）。

时间尺度差异示例 (Example of Time Scale Differences)
------------------------------------------------------

2016 年底引入了一个正闰秒，将 TAI 和 UTC 之间的差异从 36 秒增加到 37 秒。
1999 年底没有引入闰秒，当时 TAI 和 UTC 之间的差异仅为 32 秒。
下表显示了几个尺度中的相关民用和纪元时间：

==================== ========== =================== ======= ==============
UTC 日期             UNIX 时间  TAI 日期            TAI-UTC UNIX 闰秒时间
==================== ========== =================== ======= ==============
1970-01-01T00:00:00Z 0          1970-01-01T00:00:08 +8      0
1999-12-31T23:59:28Z 946684768  2000-01-01T00:00:00 +32     946684792
1999-12-31T23:59:59Z 946684799  2000-01-01T00:00:31 +32     946684823
2000-01-01T00:00:00Z 946684800  2000-01-01T00:00:32 +32     946684824
2016-12-31T23:59:59Z 1483228799 2017-01-01T00:00:35 +36     1483228827
2016-12-31T23:59:60Z 未定义     2017-01-01T00:00:36 +36     1483228828
2017-01-01T00:00:00Z 1483228800 2017-01-01T00:00:37 +37     1483228829
==================== ========== =================== ======= ==============

功能需求 (Functional Requirements)
-----------------------------------

Zephyr 滴答计数器没有闰秒或标准时间偏移的概念，是一个连续的时间尺度。
但是，它可能相对不准确，假设 RC 定时器具有 5% 的容差，漂移可达每小时三分钟。

支持 Zephyr 时间和常见人类时间尺度之间的转换需要两个阶段：

* 在连续但不准确的 Zephyr 时间尺度和准确的外部稳定时间尺度之间进行转换；
* 在稳定时间尺度和（可能不连续的）民用时间尺度之间进行转换。

围绕 :c:func:`timeutil_sync_state_update()` 的 API 支持在连续时间尺度之间转换的第一步。

第二步需要外部信息，包括闰秒和本地时间偏移变化的时间表。
这最好由外部库提供，目前不是时间工具 API 的一部分。

选择外部源和时间尺度 (Selecting an External Source and Time Scale)
--------------------------------------------------------------------

如果应用程序需要几秒钟内的民用时间精度，则可以使用 UTC 作为稳定的时间源。
但是，如果外部源调整为闰秒，则会出现不连续性：以 1 Hz 采集的两个观察之间的经过时间
不等于它们的时间戳之间的数值差异。

对于精确活动，独立于本地和太阳调整的连续尺度会大大简化事情。合适的连续尺度包括：

- GPS 时间：1980-01-06T00:00:00Z 的纪元，连续跟随 TAI，偏移为 TAI-GPS=19 s。
- 蓝牙网格时间：2000-01-01T00:00:00Z 的纪元，连续跟随 TAI，偏移为 -32。
- UNIX 闰秒时间：1970-01-01T00:00:00Z 的纪元，连续跟随 TAI，偏移为 -8。

因为 C 和 Zephyr 库函数支持使用 UNIX 纪元在整数和日历时间表示之间进行转换，
UNIX 闰秒时间是外部时间尺度的理想选择。

用于填充同步点的机制并不相关：它可能涉及从本地高精度 RTC 外设读取，
使用 NTP 或 PTP 等协议通过网络交换数据包，或处理从 GPS 接收的 NMEA 消息
（有或没有 1pps 信号）。

``timespec`` 概念 (``timespec`` Concepts)
==========================================

``struct timespec`` 最初来自 POSIX，自 C11 以来一直是 C 标准的一部分。
``struct timespec`` 的定义如下所示。

.. code-block:: c

   struct timespec {
       time_t tv_sec;  /* 秒 */
       long   tv_nsec; /* 纳秒 */
   };

.. _note:

    C 标准没有定义 ``time_t`` 的大小。但是，Zephyr 对 ``time_t`` 使用 64 位。
    ``long`` 类型要求至少为 32 位，但通常与架构的字大小匹配。
    ``struct timespec`` 的两个元素都是有符号整数。出于历史原因和足够强大以表示未来的时间，
    ``time_t`` 被定义为 64 位。

``tv_nsec`` 字段仅在 ``[0, 999999999]`` 范围内的值有效。
``tv_sec`` 字段是自纪元以来的秒数。如果 ``struct timespec`` 用于表示差异，
则 ``tv_sec`` 字段可能落入负范围。
