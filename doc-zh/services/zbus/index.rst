.. _zbus:

Zephyr 总线 (zbus) (Zephyr bus (zbus))
#######################################

..
   Note to documentation authors: the diagrams included in this documentation page were designed
   using the following Figma library:
   https://www.figma.com/community/file/1292866458780627559/zbus-diagram-assets


:dfn:`Zephyr 总线 - zbus` 是一个轻量级且灵活的软件总线,使线程能够以多对多的方式简单地相互通信 (The :dfn:`Zephyr bus - zbus` is a lightweight and flexible software bus enabling a simple way for
threads to talk to one another in a many-to-many way)。

.. contents::
    :local:
    :depth: 2

概念 (Concepts)
***************
线程可以使用 zbus 向一个或多个观察者发送消息。它使多对多通信成为可能。总线实现了消息传递和发布/订阅通信范式,使线程能够通过共享内存进行同步或异步通信 (Threads can send messages to one or more observers using zbus. It makes the many-to-many
communication possible. The bus implements message-passing and publish/subscribe communication
paradigms that enable threads to communicate synchronously or asynchronously through shared memory)。

通过 zbus 的通信是基于通道的。线程 (或回调) 使用通道交换消息。此外,除了其他操作外,线程可以发布和观察通道。当线程在通道上发布消息时,总线将使该消息对发布通道的所有观察者可用。根据观察者的类型,它可以直接访问消息、接收消息的副本,甚至只接收发布通道的引用 (The communication through zbus is channel-based. Threads (or callbacks) use channels to exchange
messages. Additionally, besides other actions, threads can publish and observe channels. When a
thread publishes a message on a channel, the bus will make the message available to all the
published channel's observers. Based on the observer's type, it can access the message directly,
receive a copy of it, or even receive only a reference of the published channel)。

下图显示了使用 zbus 的典型应用程序示例,其中应用程序逻辑 (硬件独立) 通过软件总线与其他线程通信。请注意,线程彼此解耦,因为它们只使用 zbus 通道,不需要彼此了解即可通信 (The figure below shows an example of a typical application using zbus in which the application logic
(hardware independent) talks to other threads via software bus. Note that the threads are decoupled
from each other because they only use zbus channels and do not need to know each other to talk)。


.. figure:: images/zbus_overview.svg
    :alt: zbus usage overview
    :width: 75%

    典型的 zbus 应用程序架构 (A typical zbus application architecture)。

总线包括 (The bus comprises):

* 由控制元数据信息和消息本身组成的通道集 (Set of channels that consists of the control metadata information, and the message itself);
* :dfn:`虚拟分布式事件分发器 (Virtual Distributed Event Dispatcher)` (VDED),负责向观察者发送通知/消息的总线逻辑。VDED 逻辑在发布操作内部以相同的线程上下文运行,给总线一种分布式执行的概念。当线程发布到通道时,它也会将通知传播给观察者 (the bus logic responsible for sending
  notifications/messages to the observers. The VDED logic runs inside the publishing action in the same
  thread context, giving the bus an idea of a distributed execution. When a thread publishes to a
  channel, it also propagates the notifications to the observers);
* 线程 (订阅者和消息订阅者) 和回调 (监听器) 发布、读取和从总线接收通知 (Threads (subscribers and message subscribers) and callbacks (listeners) publishing, reading, and
  receiving notifications from the bus)。

.. figure:: images/zbus_anatomy.svg
    :alt: ZBus anatomy
    :width: 70%

    ZBus 剖析 (ZBus anatomy)。

总线在通道上提供发布、读取、声明、完成、通知和订阅操作。发布、读取、声明和完成在所有 RTOS 线程上下文中可用,包括 ISR。发布和读取操作简单快速;过程是通道锁定,然后内存复制到共享内存区域和从共享内存区域复制,然后通道解锁 (The bus makes the publish, read, claim, finish, notify, and subscribe actions available over
channels. Publishing, reading, claiming, and finishing are available in all RTOS thread contexts,
including ISRs. The publish and read operations are simple and fast; the procedure is channel
locking followed by a memory copy to and from a shared memory region and then a channel unlocking.
Another essential aspect of zbus is the observers. There are three types of observers:

.. figure:: images/zbus_type_of_observers.svg
    :alt: ZBus observers type
    :width: 70%

    ZBus 观察者 (ZBus observers)。

* 监听器 (Listeners),每次观察的通道发布或通知时事件分发器执行的回调 (a callback that the event dispatcher executes every time an observed channel is
  published or notified);
* 订阅者 (Subscriber),基于线程的观察者,内部依赖消息队列,每次观察的通道发布或通知时事件分发器将更改通道的引用放入其中。请注意,这种观察者本身不接收消息。它应该在接收通知后从通道读取消息 (a thread-based observer that relies internally on a message queue where the event
  dispatcher puts a changed channel's reference every time an observed channel is published or
  notified. Note this kind of observer does not receive the message itself. It should read the
  message from the channel after receiving the notification);
* 消息订阅者 (Message subscribers),基于线程的观察者,内部依赖 FIFO,每次观察的通道发布或通知时事件分发器将消息的副本放入其中 (a thread-based observer that relies internally on a FIFO where the event
  dispatcher puts a copy of the message every time an observed channel is published or notified)。

通道观察结构定义通道与其观察者之间的关系。对于每个观察,一个通道/观察者对。开发人员可以使用 :c:macro:`ZBUS_CHAN_DEFINE` 或 :c:macro:`ZBUS_CHAN_ADD_OBS` 静态分配观察。还有运行时观察者,使开发人员能够创建运行时观察。可以完全禁用观察者或单独禁用观察。事件分发器将忽略禁用的观察者和观察 (Channel observation structures define the relationship between a channel and its observers. For
every observation, a pair channel/observer. Developers can statically allocate observation using the
:c:macro:`ZBUS_CHAN_DEFINE` or :c:macro:`ZBUS_CHAN_ADD_OBS`. There are also runtime observers,
enabling developers to create runtime observations. It is possible to disable an observer entirely
or observations individually.  The event dispatcher will ignore disabled observers and observations)。

.. figure:: images/zbus_observation_mask.svg
    :alt: ZBus observation mask.
    :width: 75%

    ZBus 观察掩码 (ZBus observation mask)。

上图说明了从 (a) 到 (d) 的一些状态,适用于从 ``C1`` 到 ``C5`` 的通道、``Subscriber 1`` 和观察。最后两个是橙色的,表示它们是动态分配的 (运行时观察)。(a) 显示观察者和所有观察都已启用。(b) 显示观察者被禁用,因此事件分发器将忽略它。(c) 显示观察者已启用。但是,有一个静态观察被禁用。事件分发器将只停止从通道 ``C3`` 发送通知。在 (d) 中,事件分发器将停止从通道 ``C3`` 和 ``C5`` 向 ``Subscriber 1`` 发送通知 (The above figure illustrates some states, from (a) to (d), for channels from ``C1`` to ``C5``,
``Subscriber 1``, and the observations. The last two are in orange to indicate they are dynamically
allocated (runtime observation). (a) shows that the observer and all observations are enabled. (b)
shows the observer is disabled, so the event dispatcher will ignore it. (c) shows the observer
enabled. However, there is one static observation disabled. The event dispatcher will only stop
sending notifications from channel ``C3``.  In (d), the event dispatcher will stop sending
notifications from channels ``C3`` and ``C5`` to ``Subscriber 1``)。


Suppose a usual sensor-based solution is in the figure below for illustration purposes. When
triggered, the timer publishes to the ``Trigger`` channel. As the sensor thread subscribed to the
``Trigger`` channel, it receives the sensor data. Notice the VDED executes the ``Blink`` because it
also listens to the ``Trigger`` channel. When the sensor data is ready, the sensor thread publishes
it to the ``Sensor data`` channel. The core thread receives the message as a ``Sensor data`` channel
message subscriber, processes the sensor data, and stores it in an internal sample buffer. It
repeats until the sample buffer is full; when it happens, the core thread aggregates the sample
buffer information, prepares a package, and publishes that to the ``Payload`` channel. The Lora
thread receives that because it is a ``Payload`` channel message subscriber and sends the payload to
the cloud. When it completes the transmission, the Lora thread publishes to the ``Transmission
done`` 通道。由于它监听 ``Transmission done`` 通道,VDED 再次执行 ``Blink`` (done`` channel. The VDED executes the ``Blink`` again since it listens to the ``Transmission done``
channel)。

.. figure:: images/zbus_operations.svg
    :alt: ZBus sensor-based application
    :width: 85%

    基于传感器的 ZBus 应用 (ZBus sensor-based application)。

这种实现解决方案的方式使应用程序更加灵活,使我们能够独立地更改事物。例如,我们想将触发器从定时器更改为按钮按下。我们可以做到这一点,并且更改不会影响系统的其他部分。同样,我们想将通信接口从 LoRa 更改为蓝牙;我们只需要更改 LoRa 线程。为了使其工作,不需要其他更改。因此,开发人员将对图像的每个块执行此操作。基于此,有迹象表明 zbus 促进了系统架构中的解耦 (This way of implementing the solution makes the application more flexible, enabling us to change
things independently. For example, we want to change the trigger from a timer to a button press. We
can do that, and the change does not affect other parts of the system. Likewise, we would like to
change the communication interface from LoRa to Bluetooth; we only need to change the LoRa thread.
No other change is required in order to make that work. Thus, the developer would do that for every
block of the image. Based on that, there is a sign zbus promotes decoupling in the system
architecture)。

使用 zbus 的另一个重要方面是系统模块的重用。如果具有明确定义行为的代码部分 (我们称之为模块) 只使用 zbus 通道而不使用硬件接口,则可以轻松地在其他解决方案中重用它。新解决方案必须实现模块需要工作的接口 (通道集)。这表明 zbus 可以改善模块重用 (Another important aspect of using zbus is the reuse of system modules. If a code portion with
well-defined behaviors (we call that module) only uses zbus channels and not hardware interfaces, it
can easily be reused in other solutions. The new solution must implement the interfaces (set of
channels) the module needs to work. That indicates zbus could improve the module reuse)。

最后一个重要说明是 zbus 解决方案的覆盖范围。我们可以指望使用 zbus 的多种方式,使开发人员尽可能自由地创建他们需要的东西。例如,消息可以是动态或静态分配的;通知可以是同步或异步的;开发人员可以通过声明通道以多种不同的方式控制通道,开发人员可以通过使用用户数据字段向通道添加其元数据信息,验证器的自由使用使系统能够准确地处理消息格式,等等。这些特性增加了可以使用 zbus 完成的解决方案,并使其非常适合作为开源社区工具 (The last important note is the zbus solution reach. We can count on many ways of using zbus to
enable the developer to be as free as possible to create what they need. For example, messages can
be dynamic or static allocated; notifications can be synchronous or asynchronous; the developer can
control the channel in so many different ways claiming the channel, developers can add their
metadata information to a channel by using the user-data field, the discretionary use of a validator
enables the systems to be accurate over message format, and so on. Those characteristics increase
the solutions that can be done with zbus and make it a good fit as an open-source community tool)。


.. _Virtual Distributed Event Dispatcher:

虚拟分布式事件分发器 (Virtual Distributed Event Dispatcher)
====================================

VDED 执行始终在发布者的上下文中进行。它可以是线程或 ISR。在 ISR 内发布时要小心,因为调度器不会抢占 VDED。明智地使用它。执行的基本描述如下 (The VDED execution always happens in the publisher's context. It can be a thread or an ISR. Be
careful with publications inside ISR because the scheduler won't preempt the VDED. Use that wisely.
The basic description of the execution is as follows):


* 获取通道锁 (The channel lock is acquired);
* 通道通过直接复制接收新消息 (通过原始的 :c:func:`memcpy`) (The channel receives the new message via direct copy (by a raw :c:func:`memcpy`));
* 事件分发器逻辑执行监听器,将消息的副本发送到消息订阅者,并按照它们在通道观察者列表上出现的顺序将通道的引用推送到订阅者的通知消息队列。监听器可以直接对常量消息引用执行非复制快速访问 (通过 :c:func:`zbus_chan_const_msg` 函数),因为通道仍然被锁定 (The event dispatcher logic executes the listeners, sends a copy of the message to the message
  subscribers, and pushes the channel's reference to the subscribers' notification message queue in
  the same sequence they appear on the channel observers' list. The listeners can perform non-copy
  quick access to the constant message reference directly (via the :c:func:`zbus_chan_const_msg`
  function) since the channel is still locked);
* 最后,发布函数解锁通道 (At last, the publishing function unlocks the channel)。


为了说明 VDED 执行,请考虑下图所示的示例。我们有四个优先级升序的线程 ``S1``、``MS2``、``MS1`` 和 ``T1`` (最高优先级);两个监听器 ``L1`` 和 ``L2``;以及通道 A。假设 ``L1``、``L2``、``MS1``、``MS2`` 和 ``S1`` 观察通道 A (To illustrate the VDED execution, consider the example illustrated below. We have four threads in
ascending priority ``S1``, ``MS2``, ``MS1``, and ``T1`` (the highest priority); two listeners,
``L1`` and ``L2``; and channel A. Supposing ``L1``, ``L2``, ``MS1``, ``MS2``, and ``S1`` observer
channel A)。

.. figure:: images/zbus_publishing_process_example_scenario.svg
    :alt: ZBus example scenario
    :width: 45%

    ZBus VDED 执行示例场景 (ZBus VDED execution example scenario)。

以下代码实现了通道 A。请注意,``struct a_msg`` 仅用于说明 (The following code implements channel A. Note the ``struct a_msg`` is illustrative only)。

.. code-block:: c

    ZBUS_CHAN_DEFINE(a_chan,                       /* Name */
             struct a_msg,                         /* Message type */

             NULL,                                 /* Validator */
             NULL,                                 /* User Data */
             ZBUS_OBSERVERS(L1, L2, MS1, MS2, S1), /* observers */
             ZBUS_MSG_INIT(0)                      /* Initial value {0} */
    );


在下图中,字母表示与 VDED 执行相关的某些操作。X 轴表示时间,Y 轴表示线程的优先级。通道 A 的消息由语音气球表示,仅是一个内存部分 (共享内存)。它多次出现只是为了说明该时间点的消息 (In the figure below, the letters indicate some action related to the VDED execution. The X-axis
represents the time, and the Y-axis represents the priority of threads. Channel A's message,
represented by a voice balloon, is only one memory portion (shared memory). It appears several times
only as an illustration of the message at that point in time)。


.. figure:: images/zbus_publishing_process_example.svg
    :alt: ZBus publish processing detail
    :width: 85%

    优先级 T1 > MS1 > MS2 > S1 的 ZBus VDED 执行详情 (ZBus VDED execution detail for priority T1 > MS1 > MS2 > S1)。



上图说明了当 T1 发布到通道 A 时 VDED 执行期间执行的操作。因此,下表描述了 VDED 执行的活动 (由字母表示)。该场景考虑了以下优先级:T1 > MS1 > MS2 > S1。T1 具有最高优先级 (The figure above illustrates the actions performed during the VDED execution when T1 publishes to
channel A. Thus, the table below describes the activities (represented by a letter) of the VDED
execution. The scenario considers the following priorities: T1 > MS1 > MS2 > S1. T1 has the highest
priority)。


.. list-table:: 优先级 T1 > MS1 > MS2 > S1 的详细 VDED 执行步骤 (VDED execution steps in detail for priority T1 > MS1 > MS2 > S1)。
   :widths: 5 65
   :header-rows: 1

   * - 操作 (Actions)
     - 描述 (Description)
   * - a
     - T1 启动,并在某个时刻发布到通道 A (T1 starts and, at some point, publishes to channel A)。
   * - b
     - 发布 (VDED) 进程启动。VDED 锁定通道 A (The publishing (VDED) process starts. The VDED locks the channel A)。
   * - c
     - VDED 将 T1 消息复制到通道 A 消息 (The VDED copies the T1 message to the channel A message)。

   * - d, e
     - VDED 按相应顺序执行 L1 和 L2。在监听器内部,通常会调用 :c:func:`zbus_chan_const_msg` 函数,该函数提供对通道 A 消息的直接常量引用。这很快,这里不需要复制 (The VDED executes L1 and L2 in the respective sequence. Inside the listeners, usually, there
       is a call to the :c:func:`zbus_chan_const_msg` function, which provides a direct constant
       reference to channel A's message. It is quick, and no copy is needed here)。

   * - f, g
     - VDED 复制消息并顺序发送给 MS1 和 MS2。请注意,线程在接收到通知后立即准备执行。但是,由于它们的优先级低于 T1,因此它们进入待处理状态 (The VDED copies the message and sends that to MS1 and MS2 sequentially. Notice the threads
       get ready to execute right after receiving the notification. However, they go to a pending
       state because they have less priority than T1)。
   * - h
     - VDED 将通知消息推送到 S1 的队列。请注意,线程在接收到通知后立即准备执行。但是,由于通道仍被锁定,它无法访问通道,因此进入待处理状态 (The VDED pushes the notification message to the queue of S1. Notice the thread gets ready to
       execute right after receiving the notification. However, it goes to a pending state because
       it cannot access the channel since it is still locked)。

   * - i
     - VDED 通过解锁通道 A 完成发布。MS1 离开待处理状态并开始执行 (VDED finishes the publishing by unlocking channel A. The MS1 leaves the pending state and
       starts executing)。

   * - j
     - MS1 完成执行。MS2 离开待处理状态并开始执行 (MS1 finishes execution. The MS2 leaves the pending state and starts executing)。

   * - k
     - MS2 完成执行。S1 离开待处理状态并开始执行 (MS2 finishes execution. The S1 leaves the pending state and starts executing)。

   * - l, m, n
     - S1 离开待处理状态,因为通道 A 未被锁定。它再次进入 CPU 并开始执行。由于它确实收到了来自通道 A 的通知,因此它执行了通道读取 (简单地锁定、内存复制、解锁),继续执行并退出 CPU (The S1 leaves the pending state since channel A is not locked. It gets in the CPU again and
       starts executing. As it did receive a notification from channel A, it performed a channel read
       (as simple as lock, memory copy, unlock), continues its execution and goes out of the CPU)。

   * - o
     - S1 完成其工作负载 (S1 finishes its workload)。


下图说明了当 T1 发布到通道 A 时 VDED 执行期间执行的操作。该场景考虑了以下优先级:T1 < MS1 < MS2 < S1 (The figure below illustrates the actions performed during the VDED execution when T1 publishes to
channel A. The scenario considers the following priorities: T1 < MS1 < MS2 < S1)。

.. figure:: images/zbus_publishing_process_example2.svg
    :alt: ZBus publish processing detail
    :width: 85%

    优先级 T1 < MS1 < MS2 < S1 的 ZBus VDED 执行详情 (ZBus VDED execution detail for priority T1 < MS1 < MS2 < S1)。

因此,下表描述了 VDED 执行的活动 (由字母表示) (Thus, the table below describes the activities (represented by a letter) of the VDED execution)。

.. list-table:: 优先级 T1 < MS1 < MS2 < S1 的详细 VDED 执行步骤 (VDED execution steps in detail for priority T1 < MS1 < MS2 < S1)。
   :widths: 5 65
   :header-rows: 1

   * - 操作 (Actions)
     - 描述 (Description)
   * - a
     - T1 启动,并在某个时刻发布到通道 A (T1 starts and, at some point, publishes to channel A)。
   * - b
     - 发布 (VDED) 进程启动。VDED 锁定通道 A (The publishing (VDED) process starts. The VDED locks the channel A)。
   * - c
     - VDED 将 T1 消息复制到通道 A 消息 (The VDED copies the T1 message to the channel A message)。

   * - d, e
     - VDED 按相应顺序执行 L1 和 L2。在监听器内部,通常会调用 :c:func:`zbus_chan_const_msg` 函数,该函数提供对通道 A 消息的直接常量引用。这很快,这里不需要复制 (The VDED executes L1 and L2 in the respective sequence. Inside the listeners, usually, there
       is a call to the :c:func:`zbus_chan_const_msg` function, which provides a direct constant
       reference to channel A's message. It is quick, and no copy is needed here)。

   * - f
     - VDED 复制消息并发送给 MS1。MS1 抢占 T1 并开始工作。之后,T1 重新获得 MCU (The VDED copies the message and sends that to MS1. MS1 preempts T1 and starts working.
       After that, the T1 regain MCU)。

   * - g
     - VDED 复制消息并发送给 MS2。MS2 抢占 T1 并开始工作。之后,T1 重新获得 MCU (The VDED copies the message and sends that to MS2. MS2 preempts T1 and starts working.
       After that, the T1 regain MCU)。

   * - h
     - VDED 将通知消息推送到 S1 的队列 (The VDED pushes the notification message to the queue of S1)。

   * - i
     - VDED 通过解锁通道 A 完成发布 (VDED finishes the publishing by unlocking channel A)。

   * - j, k, l
     - S1 离开待处理状态,因为通道 A 未被锁定。它再次进入 CPU 并开始执行。由于它确实收到了来自通道 A 的通知,因此它执行了通道读取 (简单地锁定、内存复制、解锁),继续执行并退出 CPU (The S1 leaves the pending state since channel A is not locked. It gets in the CPU again and
       starts executing. As it did receive a notification from channel A, it performs a channel read
       (as simple as lock, memory copy, unlock), continues its execution, and goes out the CPU)。


HLP 优先级提升 (HLP priority boost)
------------------
ZBus 实现了最高锁定器协议,该协议依赖于观察者的线程优先级来确定临时发布者优先级。该协议考虑通道的最高观察者优先级 (HOP);即使观察者没有等待通道上的消息,它也会被考虑在计算中。VDED 将根据 HOP 提升发布者的优先级,以确保较小的 (ZBus implements the Highest Locker Protocol that relies on the observers' thread priority to
determine a temporary publisher priority. The protocol considers the channel's Highest Observer
Priority (HOP); even if the observer is not waiting for a message on the channel, it is considered
in the calculation. The VDED will elevate the publisher's priority based on the HOP to ensure small
latency and as few preemptions as possible.

延迟和尽可能少的抢占 (latency and as few preemptions as possible)。

.. note::
    优先级提升默认情况下已启用。要将其停用,必须设置 :kconfig:option:`CONFIG_ZBUS_PRIORITY_BOOST` 配置 (The priority boost is enabled by default. To deactivate it, you must set the
    :kconfig:option:`CONFIG_ZBUS_PRIORITY_BOOST` configuration)。

.. warning::
    ZBus 优先级提升在 HOP 计算中不考虑运行时观察者 (ZBus priority boost does not consider runtime observers on the HOP calculations)。

下图说明了当 T1 发布到通道 A 时 VDED 执行期间执行的操作。该场景考虑了优先级提升功能和以下优先级:T1 < MS1 < MS2 < S1 (The figure below illustrates the actions performed during the VDED execution when T1 publishes to
channel A. The scenario considers the priority boost feature and the following priorities: T1 < MS1
< MS2 < S1)。

.. figure:: images/zbus_publishing_process_example_HLP.svg
    :alt: ZBus publishing process details using priority boost.
    :width: 85%

    启用优先级提升且优先级为 T1 < MS1 < MS2 < S1 的 ZBus VDED 执行详情 (ZBus VDED execution detail with priority boost enabled and for priority T1 < MS1 < MS2 < S1)。

要正确使用优先级提升,需要将观察者附加到线程。当订阅者附加到线程时,它采用其优先级,优先级提升算法将考虑观察者的优先级。以下代码说明了线程附加函数 (To properly use the priority boost, attaching the observer to a thread is necessary. When the
subscriber is attached to a thread, it assumes its priority, and the priority boost algorithm will
consider the observer's priority. The following code illustrates the thread-attaching function)。


.. code-block:: c
   :emphasize-lines: 10

   ZBUS_SUBSCRIBER_DEFINE(s1, 4);
   void s1_thread(void *ptr1, void *ptr2, void *ptr3)
   {
           ARG_UNUSED(ptr1);
           ARG_UNUSED(ptr2);
           ARG_UNUSED(ptr3);

           const struct zbus_channel *chan;

           zbus_obs_attach_to_thread(&s1);

           while (1) {
                   zbus_sub_wait(&s1, &chan, K_FOREVER);

                   /* Subscriber implementation */

           }
   }
   K_THREAD_DEFINE(s1_id, CONFIG_MAIN_STACK_SIZE, s1_thread, NULL, NULL, NULL, 2, 0, 0);

在上面的代码中,:c:func:`zbus_obs_attach_to_thread` 将 ``s1`` 观察者的优先级设置为 2,因为线程具有该优先级。可以使用 :c:func:`zbus_obs_detach_from_thread` 通过分离观察者来反转这一点。只有启用的观察者和观察才会在通道 HOP 计算中考虑。屏蔽通道的特定观察将影响通道 HOP (On the above code, the :c:func:`zbus_obs_attach_to_thread` will set the ``s1`` observer with
priority two as the thread has that priority. It is possible to reverse that by detaching the
observer using the :c:func:`zbus_obs_detach_from_thread`. Only enabled observers and observations
will be considered on the channel HOP calculation. Masking a specific observation of a channel will
affect the channel HOP)。

总而言之,该功能的好处是 (In summary, the benefits of the feature are):

* HLP 对于 zbus 比互斥锁优先级继承更有效 (The HLP is more effective for zbus than the mutexes priority inheritance);
* 发布者和观察者之间不会发生有界优先级反转 (No bounded priority inversion will happen among the publisher and the observers);
* 在 T1 和 S1 之间优先级的其他线程 (与通信无关) 无法抢占 T1,从而避免无界优先级反转 (No other threads (that are not involved in the communication) with priority between T1 and S1 can
  preempt T1, avoiding unbounded priority inversion);
* 消息订阅者将等待 VDED 完成消息传递过程。因此,VDED 执行将更快、更一致 (Message subscribers will wait for the VDED to finish the message delivery process. So the VDED
  execution will be faster and more consistent);
* HLP 优先级是动态的,可以在执行中更改 (The HLP priority is dynamic and can change in execution);
* ZBus 操作可以在 ISR 内部使用 (ZBus operations can be used inside ISRs);
* 优先级提升功能可以关闭,普通信号量可以用作通道锁定机制 (The priority boosting feature can be turned off, and plain semaphores can be used as the channel
  lock mechanism);
* 最高锁定器协议的主要缺点,即继承相关的优先级反转,在 zbus 场景中是可以接受的,因为它将确保较小的总线延迟 (The Highest Locker Protocol's major disadvantage, the Inheritance-related Priority Inversion, is
  acceptable in the zbus scenario since it will ensure a small bus latency)。


局限性 (Limitations)
===========

基于开发人员可以使用 zbus 解决许多不同问题的事实,会出现一些挑战。ZBus 不会解决每个问题,因此有必要分析情况以确保 zbus 适用。例如,基于 zbus 基准测试,它不太适合线程之间的高速字节流。:ref:`Pipe <pipes_v2>` 内核对象解决了这种需求 (Based on the fact that developers can use zbus to solve many different problems, some challenges
arise. ZBus will not solve every problem, so it is necessary to analyze the situation to be sure
zbus is applicable. For instance, based on the zbus benchmark, it would not be well suited to a
high-speed stream of bytes between threads. The :ref:`Pipe <pipes_v2>` kernel object solves this
kind of need)。
传递保证 (Delivery guarantees)
-------------------

ZBus 始终将消息传递给监听器和消息订阅者。但是,对于订阅者没有消息传递保证,因为 zbus 只发送通知,但消息读取取决于订阅者的实现。可以通过遵循设计提示来提高传递率 (ZBus always delivers the messages to the listeners and message subscribers. However, there are no
message delivery guarantees for subscribers because zbus only sends the notification, but the
message reading depends on the subscriber's implementation. It is possible to increase the delivery
rate by following design tips):

* 使监听器尽可能快 (将它们视为 ISR)。如果需要进行某些处理,请考虑将工作项提交到工作队列 (Keep the listeners quick-as-possible (deal with them as ISRs). If some processing is needed,
  consider submitting a work item to a work-queue);
* 尝试给生产者高优先级以避免损失 (Try to give producers a high priority to avoid losses);
* 为观察者留出备用 CPU 以消费产生的数据 (Leave spare CPU for observers to consume data produced);
* 考虑使用消息队列或管道进行密集的字节传输 (Consider using message queues or pipes for intensive byte transfers)。

.. warning::
   ZBus 使用 :zephyr_file:`include/zephyr/net_buf.h` (网络缓冲区) 与消息订阅者交换数据。因此,请仔细选择配置 :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_NET_BUF_POOL_SIZE` 和 :kconfig:option:`CONFIG_HEAP_MEM_POOL_ADD_SIZE_ZBUS`。考虑到消息订阅者,它们对于正确的 VDED 执行 (传递保证) 至关重要。如果您想为一组特定的通道保留一个隔离池,可以将 :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_NET_BUF_POOL_ISOLATION` 与专用池一起使用。查看 :zephyr:code-sample:`zbus-msg-subscriber` 以了解隔离的实际效果 (ZBus uses :zephyr_file:`include/zephyr/net_buf.h` (network buffers) to exchange data with message
   subscribers. Thus, choose carefully the configurations
   :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_NET_BUF_POOL_SIZE` and
   :kconfig:option:`CONFIG_HEAP_MEM_POOL_ADD_SIZE_ZBUS`. They are crucial to a proper VDED execution
   (delivery guarantee) considering message subscribers. If you want to keep an isolated pool for a
   specific set of channels, you can use
   :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_NET_BUF_POOL_ISOLATION` with a dedicated pool. Look
   at the :zephyr:code-sample:`zbus-msg-subscriber` to see the isolation in action)。

.. warning::
   订阅者将只接收变更通道的引用。如果在订阅者读取之前发布了两次通道,则可能会感知到数据丢失。第二次发布会覆盖第一次的值。因此,订阅者将收到两个通知,但只有最后的数据存在 (Subscribers will receive only the reference of the changing channel. A data loss may be perceived
   if the channel is published twice before the subscriber reads it. The second publication
   overwrites the value from the first. Thus, the subscriber will receive two notifications, but
   only the last data is there)。


.. _zbus delivery sequence:

消息传递序列 (Message delivery sequence)
-------------------------

消息传递将遵循优先级 (The message delivery will follow the precedence):

#. 使用 :c:macro:`ZBUS_CHAN_DEFINE` 在通道中定义的观察者 (遵循定义序列) (Observers defined in a channel using the :c:macro:`ZBUS_CHAN_DEFINE` (following the definition
   sequence));
#. 使用 :c:macro:`ZBUS_CHAN_ADD_OBS` 基于序列优先级 (宏的参数) 定义的观察者 (Observers defined using the :c:macro:`ZBUS_CHAN_ADD_OBS` based on the sequence priority
   (parameter of the macro));
#. 最后是使用 :c:func:`zbus_chan_add_obs` 按添加序列添加的运行时观察者 (The latest is the runtime observers in the addition sequence using the
   :c:func:`zbus_chan_add_obs`)。

.. note::
    VDED 将忽略所有禁用的观察者或观察 (The VDED will ignore all disabled observers or observations)。

使用 (Usage)
*****

ZBus 操作依赖于通道和观察者。因此,在通道定义期间需要确定其消息和观察者列表。消息是常规的 C 结构体;观察者可以是订阅者 (异步)、消息订阅者 (异步) 或监听器 (同步) (ZBus operation depends on channels and observers. Therefore, it is necessary to determine its
message and observers list during the channel definition. A message is a regular C struct; the
observer can be a subscriber (asynchronous), a message subscriber (asynchronous), or a listener
(synchronous))。

以下代码定义并初始化常规通道及其依赖项。例如,该通道交换加速度计数据 (The following code defines and initializes a regular channel and its dependencies. This channel
exchanges accelerometer data, for example)。

.. code-block:: c

    struct acc_msg {
            int x;
            int y;
            int z;
    };

    ZBUS_CHAN_DEFINE(acc_chan,                           /* Name */
             struct acc_msg,                             /* Message type */
             NULL,                                       /* Validator */
             NULL,                                       /* User Data */
             ZBUS_OBSERVERS(my_listener, my_subscriber,
                            my_msg_subscriber),          /* observers */
             ZBUS_MSG_INIT(.x = 0, .y = 0, .z = 0)       /* Initial value */
    );

    void listener_callback_example(const struct zbus_channel *chan)
    {
            const struct acc_msg *acc;
            if (&acc_chan == chan) {
                    acc = zbus_chan_const_msg(chan); // Direct message access
                    LOG_DBG("From listener -> Acc x=%d, y=%d, z=%d", acc->x, acc->y, acc->z);
            }
    }

    ZBUS_LISTENER_DEFINE(my_listener, listener_callback_example);

    ZBUS_LISTENER_DEFINE(my_listener2, listener_callback_example);

    ZBUS_CHAN_ADD_OBS(acc_chan, my_listener2, 3);

    ZBUS_SUBSCRIBER_DEFINE(my_subscriber, 4);
    void subscriber_task(void)
    {
            const struct zbus_channel *chan;

            while (!zbus_sub_wait(&my_subscriber, &chan, K_FOREVER)) {
                    struct acc_msg acc = {0};

                    if (&acc_chan == chan) {
                            // Indirect message access
                            zbus_chan_read(&acc_chan, &acc, K_NO_WAIT);
                            LOG_DBG("From subscriber -> Acc x=%d, y=%d, z=%d", acc.x, acc.y, acc.z);
                    }
            }
    }
    K_THREAD_DEFINE(subscriber_task_id, 512, subscriber_task, NULL, NULL, NULL, 3, 0, 0);

    ZBUS_MSG_SUBSCRIBER_DEFINE(my_msg_subscriber);
    static void msg_subscriber_task(void *ptr1, void *ptr2, void *ptr3)
    {
            ARG_UNUSED(ptr1);
            ARG_UNUSED(ptr2);
            ARG_UNUSED(ptr3);
            const struct zbus_channel *chan;

            struct acc_msg acc = {0};

            while (!zbus_sub_wait_msg(&my_msg_subscriber, &chan, &acc, K_FOREVER)) {
                    if (&acc_chan == chan) {
                            LOG_INF("From msg subscriber -> Acc x=%d, y=%d, z=%d", acc.x, acc.y, acc.z);
                    }
            }
    }
    K_THREAD_DEFINE(msg_subscriber_task_id, 1024, msg_subscriber_task, NULL, NULL, NULL, 3, 0, 0);



可以使用 :c:macro:`ZBUS_CHAN_ADD_OBS` 向通道添加静态观察者。我们称之为后定义静态观察者。该命令使我们能够指示影响观察者初始化顺序的初始化优先级。序列优先级参数仅影响后定义静态观察者。无法覆盖静态观察者的消息传递序列 (It is possible to add static observers to a channel using the :c:macro:`ZBUS_CHAN_ADD_OBS`. We call
that a post-definition static observer. The command enables us to indicate an initialization
priority that affects the observers' initialization order. The sequence priority param only affects
the post-definition static observers. There is no possibility to overwrite the message delivery
sequence of the static observers)。

.. note::
   在监听器内部访问消息之前无需声明/锁定通道,因为事件分发器在调用监听器时已锁定了通知通道。但是,订阅者必须声明/锁定该通道或使用常规读取操作在接收通知后访问消息 (It is unnecessary to claim/lock a channel before accessing the message inside the listener since
   the event dispatcher calls listeners with the notifying channel already locked. Subscribers,
   however, must claim/lock that or use regular read operations to access the message after being
   notified)。


通道可以有一个*验证器函数*,使通道只接受有效消息。被硬通道无效化的发布尝试将立即返回错误代码。这允许通道的原始创建者对可能想要依附于其通道的其他开发人员/发布者施加一定的权限。以下代码定义并初始化一个 :dfn:`硬通道` 及其依赖项。只有有效的消息才能发布到 :dfn:`硬通道`。这是可能的,因为*验证器函数*被传递给了通道的定义。在此示例中,只有 ``move`` 等于 0、-1 和 1 的消息是有效的。发布函数将丢弃所有其他 ``move`` 值 (Channels can have a *validator function* that enables a channel to accept only valid messages.
Publish attempts invalidated by hard channels will return immediately with an error code. This
allows original creators of a channel to exert some authority over other developers/publishers who
may want to piggy-back on their channels. The following code defines and initializes a :dfn:`hard
channel` and its dependencies. Only valid messages can be published to a :dfn:`hard channel`. It is
possible because a *validator function* was passed to the channel's definition. In this example,
only messages with ``move`` equal to 0, -1, and 1 are valid. Publish function will discard all other
values to ``move``)。

.. code-block:: c

    struct control_msg {
            int move;
    };

    bool control_validator(const void* msg, size_t msg_size) {
            const struct control_msg* cm = msg;
            bool is_valid = (cm->move == -1) || (cm->move == 0) || (cm->move == 1);
            return is_valid;
    }

    static int message_count = 0;

    ZBUS_CHAN_DEFINE(control_chan,    /* Name */
             struct control_msg,      /* Message type */

             control_validator,       /* Validator */
             &message_count,          /* User data */
             ZBUS_OBSERVERS_EMPTY,    /* observers */
             ZBUS_MSG_INIT(.move = 0) /* Initial value */
    );

以下各节详细描述如何使用 zbus 功能 (The following sections describe in detail how to use zbus features)。


.. _publishing to a channel:

发布到通道 (Publishing to a channel)
=======================

在 zbus 中,通过调用 :c:func:`zbus_chan_pub` 将消息发布到通道。例如,以下代码基于上述示例并发布到通道 ``acc_chan``。代码尝试将消息 ``acc1`` 发布到通道 ``acc_chan``,并且它将等待最多一秒钟以发布消息。否则,操作失败。从代码示例可以推断出,可以使用堆栈分配的消息,因为 VDED 在内部复制数据 (Messages are published to a channel in zbus by calling :c:func:`zbus_chan_pub`. For example, the
following code builds on the examples above and publishes to channel ``acc_chan``. The code is
trying to publish the message ``acc1`` to channel ``acc_chan``, and it will wait up to one second
for the message to be published. Otherwise, the operation fails. As can be inferred from the code
sample, it's OK to use stack allocated messages since VDED copies the data internally)。

.. code-block:: c

	struct acc_msg acc1 = {.x = 1, .y = 1, .z = 1};
	zbus_chan_pub(&acc_chan, &acc1, K_SECONDS(1));

.. warning::
    仅在 ISR 内部使用带有 :c:macro:`K_NO_WAIT` 超时的此函数 (Only use this function inside an ISR with a :c:macro:`K_NO_WAIT` timeout)。

.. _reading from a channel:

从通道读取 (Reading from a channel)
======================

在 zbus 中,通过调用 :c:func:`zbus_chan_read` 从通道读取消息。因此,例如,以下代码尝试读取通道 ``acc_chan``,它将等待最多 500 毫秒以读取消息。否则,操作失败 (Messages are read from a channel in zbus by calling :c:func:`zbus_chan_read`. So, for example, the
following code tries to read the channel ``acc_chan``, which will wait up to 500 milliseconds to
read the message. Otherwise, the operation fails)。

.. code-block:: c

    struct acc_msg acc = {0};
    zbus_chan_read(&acc_chan, &acc, K_MSEC(500));

.. warning::
    仅在 ISR 内部使用带有 :c:macro:`K_NO_WAIT` 超时的此函数 (Only use this function inside an ISR with a :c:macro:`K_NO_WAIT` timeout)。

.. warning::
   在从 :c:func:`zbus_sub_wait` 接收到通知后,请仔细选择 :c:func:`zbus_chan_read` 的超时,因为通道在 VDED 执行期间将始终不可用。如果有多个订阅者,使用 ``K_NO_WAIT`` 进行读取很可能会返回超时错误。例如,再次考虑 VDED 示例,并注意 ``S1`` 读取尝试在使用 K_NO_WAIT 时肯定会失败。有关更多详细信息,请查看 `Virtual Distributed Event Dispatcher`_ 部分 (Choose the timeout of :c:func:`zbus_chan_read` after receiving a notification from
   :c:func:`zbus_sub_wait` carefully because the channel will always be unavailable during the VDED
   execution. Using ``K_NO_WAIT`` for reading is highly likely to return a timeout error if there
   are more than one subscriber. For example, consider the VDED illustration again and notice how
   ``S1`` read attempts would definitely fail with K_NO_WAIT. For more details, check
   the `Virtual Distributed Event Dispatcher`_ section)。

channel ``acc_chan``. Note this can send events with no message, which does not require any data
exchange. See the code example under `Claim and finish a channel`_ where this may become useful.

通道 ``acc_chan``。请注意,这可以发送没有消息的事件,不需要任何数据交换。请参阅 `Claim and finish a channel`_ 下的代码示例,了解这在何处可能有用 (channel ``acc_chan``. Note this can send events with no message, which does not require any data
exchange. See the code example under `Claim and finish a channel`_ where this may become useful)。

.. code-block:: c

    zbus_chan_notify(&acc_chan, K_NO_WAIT);

.. warning::
    仅在 ISR 内部使用带有 :c:macro:`K_NO_WAIT` 超时的此函数 (Only use this function inside an ISR with a :c:macro:`K_NO_WAIT` timeout)。

声明通道和观察者 (Declaring channels and observers)
================================

对于从其定义文件之外的文件访问通道或观察者,需要通过调用 :c:macro:`ZBUS_CHAN_DECLARE` 和 :c:macro:`ZBUS_OBS_DECLARE` 来声明它们。换句话说,在不同文件中具有相同通道名称的 zbus 通道定义和声明将指向相同的 (全局) 通道。因此,开发人员应注意现有通道,并命名新通道,否则链接将失败。可以在同一调用中声明多个通道或观察者。以下代码基于上述示例并显示已定义的通道和观察者 (For accessing channels or observers from files other than its defining files, it is necessary to
declare them by calling :c:macro:`ZBUS_CHAN_DECLARE` and :c:macro:`ZBUS_OBS_DECLARE`. In other
words, zbus channel definitions and declarations with the same channel names in different files
would point to the same (global) channel. Thus, developers should be careful about existing
channels, and naming new channels or linking will fail. It is possible to declare more than one
channel or observer on the same call. The following code builds on the examples above and displays
the defined channels and observers)。

.. code-block:: c

    ZBUS_OBS_DECLARE(my_listener, my_subscriber);
    ZBUS_CHAN_DECLARE(acc_chan, version_chan);


唯一通道标识符 (Unique channel identifiers)
--------------------------

为了简化与外部实体的集成,可以为通道分配唯一的数字标识符。然后,用户可以使用标识符通过 :c:func:`zbus_chan_from_id` 检索通道引用,而不需要在编译时使用 :c:macro:`ZBUS_CHAN_DECLARE` 获取引用。使用此功能的通道使用 :c:func:`ZBUS_CHAN_DEFINE_WITH_ID` 声明 (To simplify integrations with external entities, it is possible to assign a unique numeric identifier
to a channel. Users can then retrieve the channel reference by using the identifier with
:c:func:`zbus_chan_from_id`, rather than needing to obtain the reference at compile time with
:c:macro:`ZBUS_CHAN_DECLARE`. Channels using this feature are declared with
:c:func:`ZBUS_CHAN_DEFINE_WITH_ID`)。

.. code-block:: c

    ZBUS_CHAN_DEFINE_WITH_ID(control_chan,    /* Name */
        0x12345678,              /* Unique channel identifier */
        struct control_msg,      /* Message type */
        control_validator,       /* Validator */
        &message_count,          /* User data */
        ZBUS_OBSERVERS_EMPTY,    /* observers */
        ZBUS_MSG_INIT(.move = 0) /* Initial value */
    );

    static void channel_retrieve(void)
    {
        const struct zbus_channel *chan = zbus_chan_from_id(0x12345678);

        ...
    }


迭代通道和观察者 (Iterating over channels and observers)
=====================================

ZBus 子系统还为通道和观察者实现了 :ref:`Iterable Sections <iterable_sections_api>`,为此提供了支持 API,如 :c:func:`zbus_iterate_over_channels`、:c:func:`zbus_iterate_over_channels_with_user_data`、:c:func:`zbus_iterate_over_observers` 和 :c:func:`zbus_iterate_over_observers_with_user_data`。此功能使开发人员能够在所有声明的通道上调用过程,其中过程参数是 :c:struct:`zbus_channel`。执行顺序按通道的字母名称顺序排列 (有关详细信息,请参阅 :ref:`Iterable Sections <iterable_sections_api>` 文档)。ZBus 还为 :c:struct:`zbus_observer` 实现此功能 (ZBus subsystem also implements :ref:`Iterable Sections <iterable_sections_api>` for channels and
observers, for which there are supporting APIs like :c:func:`zbus_iterate_over_channels`,
:c:func:`zbus_iterate_over_channels_with_user_data`, :c:func:`zbus_iterate_over_observers` and
:c:func:`zbus_iterate_over_observers_with_user_data`. This feature enables developers to call a
procedure over all declared channels, where the procedure parameter is a :c:struct:`zbus_channel`.
The execution sequence is in the alphabetical name order of the channels (see :ref:`Iterable
Sections <iterable_sections_api>` documentation for details). ZBus also implements this feature for
:c:struct:`zbus_observer`)。

.. code-block:: c

   static bool print_channel_data_iterator(const struct zbus_channel *chan, void *user_data)
   {
         int *count = user_data;

         LOG_INF("%d - Channel %s:", *count, zbus_chan_name(chan));
         LOG_INF("      Message size: %d", zbus_chan_msg_size(chan));
         LOG_INF("      Observers:");

         ++(*count);

         struct zbus_channel_observation *observation;

         for (int16_t i = *chan->observers_start_idx, limit = *chan->observers_end_idx; i < limit;
               ++i) {
               STRUCT_SECTION_GET(zbus_channel_observation, i, &observation);

               LOG_INF("      - %s", observation->obs->name);
         }

         struct zbus_observer_node *obs_nd, *tmp;

         SYS_SLIST_FOR_EACH_CONTAINER_SAFE(chan->observers, obs_nd, tmp, node) {
               LOG_INF("      - %s", obs_nd->obs->name);
         }

         return true;
   }

   static bool print_observer_data_iterator(const struct zbus_observer *obs, void *user_data)
   {
         int *count = user_data;

         LOG_INF("%d - %s %s", *count, obs->queue ? "Subscriber" : "Listener", zbus_obs_name(obs));

         ++(*count);

         return true;
   }

   int main(void)
   {
         int count = 0;

         LOG_INF("Channel list:");

         zbus_iterate_over_channels_with_user_data(print_channel_data_iterator, &count);

         count = 0;

         LOG_INF("Observers list:");

         zbus_iterate_over_observers_with_user_data(print_observer_data_iterator, &count);

         return 0;
   }


代码将记录以下输出 (The code will log the following output):

.. code-block:: console

    D: Channel list:
    D: 0 - Channel acc_chan:
    D:       Message size: 12
    D:       Observers:
    D:       - my_listener
    D:       - my_subscriber
    D: 1 - Channel version_chan:
    D:       Message size: 4
    D:       Observers:
    D: Observers list:
    D: 0 - Listener my_listener
    D: 1 - Subscriber my_subscriber


.. _Claim and finish a channel:

高级通道控制 (Advanced channel control)
========================

ZBus 旨在尽可能灵活和可扩展。因此,有一些功能旨在为总线提供一些控制和可扩展性 (ZBus was designed to be as flexible and extensible as possible. Thus, there are some features
designed to provide some control and extensibility to the bus)。

监听器消息访问 (Listeners message access)
------------------------

出于性能考虑,监听器可以直接访问接收通道消息,因为它们已为此锁定了通道。要访问通道的消息,监听器应使用 :c:func:`zbus_chan_const_msg`,因为作为监听器函数参数传递的通道是指向通道的常量指针。const 指针返回类型告诉开发人员不要修改消息 (For performance purposes, listeners can access the receiving channel message directly since they
already have the channel locked for it. To access the channel's message, the listener should use the
:c:func:`zbus_chan_const_msg` because the channel passed as an argument to the listener function is
a constant pointer to the channel. The const pointer return type tells developers not to modify the
message)。

.. code-block:: c

    void listener_callback_example(const struct zbus_channel *chan)
    {
            const struct acc_msg *acc;
            if (&acc_chan == chan) {
                    acc = zbus_chan_const_msg(chan); // Use this
                    // instead of zbus_chan_read(chan, &acc, K_MSEC(200))
                    // or zbus_chan_msg(chan)

                    LOG_DBG("From listener -> Acc x=%d, y=%d, z=%d", acc->x, acc->y, acc->z);
            }
    }

用户数据 (User Data)
---------
可以将自定义数据传递到通道的 ``user_data`` 中以用于各种目的,例如写入通道元数据。这可以通过将指针传递给通道定义宏的 ``user_data`` 字段来实现,然后其他人就可以访问它。请注意,``user_data`` 对于每个通道都是单独的。另外,请注意 ``user_data`` 访问不是线程安全的。对于线程安全地访问 ``user_data``,请参阅下一节 (It is possible to pass custom data into the channel's ``user_data`` for various purposes, such as
writing channel metadata. That can be achieved by passing a pointer to the channel definition
macro's ``user_data`` field, which will then be accessible by others. Note that ``user_data`` is
individual for each channel. Also, note that ``user_data`` access is not thread-safe. For
thread-safe access to ``user_data``, see the next section)。


声明和完成通道 (Claim and finish a channel)
--------------------------

为了更好地控制通道,添加了两个函数 :c:func:`zbus_chan_claim` 和 :c:func:`zbus_chan_finish`。使用这些函数,可以安全地访问通道的元数据。当通道被声明时,该通道的操作都不可用。完成通道后,所有操作再次可用 (To take more control over channels, two functions were added :c:func:`zbus_chan_claim` and
:c:func:`zbus_chan_finish`. With these functions, it is possible to access the channel's metadata
safely. When a channel is claimed, no actions are available to that channel. After finishing the
channel, all the actions are available again)。

.. warning::
   切勿直接更改通道结构体的字段。这可能会导致 zbus 行为不一致和调度问题 (Never change the fields of the channel struct directly. It may cause zbus behavior
   inconsistencies and scheduling issues)。

.. warning::
    仅在 ISR 内部使用带有 :c:macro:`K_NO_WAIT` 超时的此函数 (Only use this function inside an ISR with a :c:macro:`K_NO_WAIT` timeout)。

以下代码基于上述示例并声明 ``acc_chan`` 以将 ``user_data`` 设置为通道。假设我们想计算通道交换消息的次数。我们将 ``user_data`` 定义为 32 位整数。此代码可以添加到上面描述的监听器代码中 (The following code builds on the examples above and claims the ``acc_chan`` to set the ``user_data``
to the channel. Suppose we would like to count how many times the channels exchange messages. We
defined the ``user_data`` to have the 32 bits integer. This code could be added to the listener code
described above)。

.. code-block:: c

    if (!zbus_chan_claim(&acc_chan, K_MSEC(200))) {
            int *message_counting = (int *) zbus_chan_user_data(&acc_chan);
            *message_counting += 1;
            zbus_chan_finish(&acc_chan);
    }

以下代码具有与 :ref:`publishing to a channel` 中的代码完全相同的行为 (The following code has the exact behavior of the code in :ref:`publishing to a channel`)。

.. code-block:: c

    if (!zbus_chan_claim(&acc_chan, K_MSEC(200))) {
            struct acc_msg *acc1 = (struct acc_msg *) zbus_chan_msg(&acc_chan);
            acc1.x = 1;
            acc1.y = 1;
            acc1.z = 1;
            zbus_chan_finish(&acc_chan);
            zbus_chan_notify(&acc_chan, K_SECONDS(1));
    }

以下代码具有与 :ref:`reading from a channel` 中的代码完全相同的行为 (The following code has the exact behavior of the code in :ref:`reading from a channel`)。

.. code-block:: c

    if (!zbus_chan_claim(&acc_chan, K_MSEC(200))) {
            const struct acc_msg *acc1 = (const struct acc_msg *) zbus_chan_const_msg(&acc_chan);
            // access the acc_msg fields directly.
            zbus_chan_finish(&acc_chan);
    }


运行时观察者注册 (Runtime observer registration)
-----------------------------

可以在运行时向通道添加观察者。设置 :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS` 以启用该功能。此功能使用堆动态分配节点、使用内存板静态分配节点或使用用户提供的节点。它取决于 :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC`,它可以是 :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC_DYNAMIC`、:kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC_STATIC` 和 :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC_NONE`。动态是默认的。当启用 :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC_STATIC` 时,您需要通过设置 (It is possible to add observers to channels in runtime. Set the
:kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS` to enable the feature. This feature uses the heap to
allocate the nodes dynamically, a memory slab to allocate the nodes statically, or user-provided
nodes. It depends on the :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC`, which can be
:kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC_DYNAMIC`,
:kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_POOL_SIZE` 配置来设置您将使用的运行时观察者数量。以下示例说明了运行时注册的用法 (:kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_POOL_SIZE` configuration. The following example
illustrates the runtime registration usage)。

.. code-block:: c

    ZBUS_LISTENER_DEFINE(my_listener, callback);
    // ...
    void thread_entry(void) {
            // ...
            /* Adding the observer to channel chan1 */
            zbus_chan_add_obs(&chan1, &my_listener, K_NO_WAIT);
            /* Removing the observer from channel chan1 */
            zbus_chan_rm_obs(&chan1, &my_listener, K_NO_WAIT);


.. warning::

  只有在通过 :c:func:`zbus_chan_rm_obs` 移除首次关联的通道观察者后,才能在 :c:func:`zbus_chan_add_obs_with_node` 中重用 :c:struct:`zbus_observer_node` (The :c:struct:`zbus_observer_node` can only be re-used in :c:func:`zbus_chan_add_obs_with_node` after removing
  the channel observer it was first associated with through :c:func:`zbus_chan_rm_obs`)。


示例 (Samples)
*******

要完整了解 zbus 的使用,请查看示例。有以下可用示例 (For a complete overview of zbus usage, take a look at the samples. There are the following samples
available):

* :zephyr:code-sample:`zbus-hello-world` 说明了上述代码的实际操作 (illustrates the code used above in action);
* :zephyr:code-sample:`zbus-work-queue` 展示了如何定义和使用不同类型的观察者。请注意,有一个使用工作队列而不是执行监听器作为执行选项的示例 (shows how to define and use different kinds of observers.
  Note there is an example of using a work queue instead of executing the listener as an execution
  option);
* :zephyr:code-sample:`zbus-msg-subscriber` 说明了如何使用消息订阅者 (illustrates how to use message subscribers);
* :zephyr:code-sample:`zbus-dyn-channel` 演示了如何在 zbus 中使用动态分配的交换数据 (demonstrates how to use dynamically allocated exchanging
  data in zbus);
* :zephyr:code-sample:`zbus-uart-bridge` 展示了通过串行将通道操作发送到主机的示例 (shows an example of sending the operation of the channel to
  a host via serial);
* :zephyr:code-sample:`zbus-remote-mock` 说明了如何实现外部模拟 (在主机上) 以向总线发送和从总线接收消息 (illustrates how to implement an external mock (on the host)
  to send and receive messages to and from the bus);
* :zephyr:code-sample:`zbus-priority-boost` 通过优先级反转场景说明了 zbus 优先级提升功能 (illustrates zbus priority boost feature with a priority
  inversion scenario);
* :zephyr:code-sample:`zbus-runtime-obs-registration` 说明了使用运行时观察者注册功能的方式 (illustrates a way of using the runtime
  observer registration feature);
* :zephyr:code-sample:`zbus-confirmed-channel` 实现了仅使用订阅者实现确认通道的方式 (implements a way of implement confirmed channel only
  with subscribers);
* :zephyr:code-sample:`zbus-benchmark` 实现了具有不同输入组合的基准测试 (implements a benchmark with different combinations of inputs)。

建议的用途 (Suggested Uses)
**************

使用 zbus 以同步或异步方式在一对一、一对多和多对多的线程之间传输数据 (消息)。选择适当的观察者类型至关重要。对于可以容忍消息丢失和重复的场景,使用订阅者;当它们不能时,使用消息订阅者 (如果需要线程) 或监听器 (如果需要精简和快速)。除了监听器之外,可能还需要另一种异步消息处理机制 (如 :ref:`message queues <message_queues_v2>`),以保留挂起的消息直到它被处理 (Use zbus to transfer data (messages) between threads in one-to-one, one-to-many, and many-to-many
synchronously or asynchronously. Choosing the proper observer type is crucial. Use subscribers for
scenarios that can tolerate message losses and duplications; when they cannot, use message
subscribers (if you need a thread) or listeners (if you need to be lean and fast). In addition to
the listener, another asynchronous message processing mechanism (like :ref:`message queues
<message_queues_v2>`) may be necessary to retain the pending message until it gets processed)。

.. note::
   ZBus 可用于将流从生产者传输到消费者。但是,这会增加 zbus 的通信延迟。因此,也许可以考虑将 Pipe 作为此通信拓扑的良好替代方案 (ZBus can be used to transfer streams from the producer to the consumer. However, this can
   increase zbus' communication latency. So maybe consider a Pipe a good alternative for this
   communication topology)。

配置选项 (Configuration Options)
*********************

要启用 zbus,需要启用 :kconfig:option:`CONFIG_ZBUS` 选项 (For enabling zbus, it is necessary to enable the :kconfig:option:`CONFIG_ZBUS` option)。

相关配置选项 (Related configuration options):

* :kconfig:option:`CONFIG_ZBUS_PRIORITY_BOOST` zbus 最高锁定器协议实现 (zbus Highest Locker Protocol implementation);
* :kconfig:option:`CONFIG_ZBUS_CHANNELS_SYS_INIT_PRIORITY` 确定 zbus 用于按通道组织通道观察的 :c:macro:`SYS_INIT` 优先级 (determine the :c:macro:`SYS_INIT`
  priority used by zbus to organize the channels observations by channel);
* :kconfig:option:`CONFIG_ZBUS_CHANNEL_NAME` 使通道名称在通道元数据内可用。日志使用此信息显示通道名称 (enables the name of channels to be available inside the
  channels metadata. The log uses this information to show the channels' names);
* :kconfig:option:`CONFIG_ZBUS_OBSERVER_NAME` 使观察者名称在通道元数据内可用 (enables the name of observers to be available inside
  the channels metadata);
* :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER` 启用消息订阅者观察者类型 (enables the message subscriber observer type);
* :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_BUF_ALLOC_DYNAMIC` 使用堆分配消息缓冲区 (uses the heap to allocate message
  buffers);
* :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_BUF_ALLOC_STATIC` 使用栈分配消息缓冲区 (uses the stack to allocate message
  buffers);
* :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_NET_BUF_POOL_SIZE` 可同时使用的消息缓冲区的可用数量 (the available number of message
  buffers to be used simultaneously);
* :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_NET_BUF_POOL_ISOLATION` 使开发人员能够为一组通道的消息订阅者隔离池 (enables the developer to isolate
  a pool for the message subscriber for a set of channels);
* :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_NET_BUF_STATIC_DATA_SIZE` 要传输到消息缓冲区的 zbus 通道的最大消息 (the biggest message of zbus
  channels to be transported into a message buffer);
* :kconfig:option:`CONFIG_HEAP_MEM_POOL_ADD_SIZE_ZBUS` 整个 ZBus 的保留堆大小,包括消息缓冲区分配 (the reserved heap size for ZBus in a whole
  including message buffer allocation);
* :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS` 启用运行时观察者注册 (enables the runtime observer registration);
* :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC_DYNAMIC` 使用堆动态分配运行时观察者 (allocate the runtime observers
  dynamically using the heap);
* :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC_STATIC` 使用内存板静态分配运行时观察者 (allocate the runtime observers
  statically using a memory slab);
* :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_POOL_SIZE` 静态分配的启用运行时观察者数量 (the amount of enabled runtime
  observers to statically allocate)。
* :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC_NONE` 使用用户提供的运行时观察者节点 (use user-provided runtime
  observers nodes);

API 参考 (API Reference)
*************

.. doxygengroup:: zbus_apis
