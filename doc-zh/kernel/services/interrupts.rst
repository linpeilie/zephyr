.. _interrupts_v2:

中断
####

:dfn:`中断服务例程` (ISR) 是一个响应硬件或软件中断异步执行的函数。ISR 通常会
抢占当前线程的执行,允许以非常低的开销进行响应。只有在所有 ISR 工作完成后,
线程执行才会恢复。

.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的 ISR(仅受可用 RAM 限制),但受底层硬件施加的约束。

ISR 具有以下关键属性:

* 触发 ISR 的**中断请求 (IRQ) 信号**。
* 与 IRQ 关联的**优先级级别**。
* 调用以处理中断的**中断服务例程**。
* 传递给该函数的**参数值**。

:abbr:`IDT (中断描述符表)` 或向量表用于将给定的中断源与给定的 ISR 相关联。
在任何给定时间,只有单个 ISR 可以与特定 IRQ 关联。

多个 ISR 可以使用相同的函数来处理中断,允许单个函数为生成多种类型中断的设备
或为多个设备(通常是相同类型)提供服务。传递给 ISR 函数的参数值允许函数确定
已发出哪个中断的信号。

内核为所有未使用的 IDT 条目提供默认 ISR。如果发出意外中断的信号,此 ISR 会
生成致命系统错误。

内核支持**中断嵌套**。这允许如果发出更高优先级的中断信号,则可以在执行中间
抢占 ISR。一旦更高优先级的 ISR 完成其处理,较低优先级的 ISR 就会恢复执行。

ISR 在内核的**中断上下文**中执行。此上下文有自己的专用栈区域(或在某些架构上,
栈区域)。如果启用了中断嵌套支持,则中断上下文栈的大小必须能够处理多个并发
ISR 的执行。

.. important::
    许多内核 API 只能由线程使用,不能由 ISR 使用。在可能由线程和 ISR 调用
    例程的情况下,内核提供 :c:func:`k_is_in_isr` API,允许例程根据它是作为
    线程的一部分还是作为 ISR 的一部分执行来改变其行为。

.. _multi_level_interrupts:

多级中断处理
============

硬件平台可以通过使用一个或多个嵌套中断控制器来支持比本机提供的更多中断线。
硬件中断源被组合成一条线,然后路由到父控制器。

如果支持嵌套中断控制器,应启用
:kconfig:option:`CONFIG_MULTI_LEVEL_INTERRUPTS`,并根据硬件架构配置
:kconfig:option:`CONFIG_2ND_LEVEL_INTERRUPTS` 和
:kconfig:option:`CONFIG_3RD_LEVEL_INTERRUPTS`。

分配一个唯一的 32 位中断号,其中嵌入了信息以选择和调用正确的中断服务例程
(ISR)。每个中断级别在此 32 位数字内被赋予一个字节,使用此架构提供对最多四个
中断级别的支持,如下所示和说明:

.. code-block:: none

                 9             2   0
           _ _ _ _ _ _ _ _ _ _ _ _ _         (LEVEL 1)
         5       |         A   |
       _ _ _ _ _ _ _         _ _ _ _ _ _ _   (LEVEL 2)
         |   C                       B
       _ _ _ _ _ _ _                         (LEVEL 3)
               D

这里显示了三个中断级别。

* '-' 表示中断线,从 0(最右边)开始编号。
* LEVEL 1 有 12 条中断线,其中两条线(2 和 9)连接到嵌套控制器,一个设备 'A'
  在第 4 线。
* 其中一个 LEVEL 2 控制器的中断线 5 连接到 LEVEL 3 嵌套控制器,一个设备 'C'
  在第 3 线。
* 另一个 LEVEL 2 控制器没有嵌套控制器,但在第 2 线有一个设备 'B'。
* LEVEL 3 控制器在第 2 线有一个设备 'D'。

以下是如何为每个硬件中断生成唯一中断号的方法。让我们考虑上面显示的四个中断,
即 A、B、C 和 D:

.. code-block:: none

   A -> 0x00000004
   B -> 0x00000302
   C -> 0x00000409
   D -> 0x00030609

.. note::
   LEVEL 2 及以后的位位置偏移 1,因为 0 表示该级别不存在中断号。对于我们的
   示例,LEVEL 3 控制器在第 2 线有设备 D,连接到 LEVEL 2 控制器的第 5 线,
   该线连接到 LEVEL 1 控制器的第 9 线 (2 -> 5 -> 9)。由于 LEVEL 2 及以后的
   编码偏移,设备 D 被赋予号码 0x00030609。

防止中断
========

在某些情况下,当前线程在执行时间敏感或临界区操作时可能需要防止 ISR 执行。

线程可以使用 **IRQ 锁**暂时防止系统中的所有 IRQ 处理。即使此锁已经生效,
也可以应用此锁,因此例程可以使用它而无需知道它是否已经生效。在线程运行时,
线程必须解锁其 IRQ 锁与锁定次数相同,然后内核才能再次处理中断。

.. important::
    IRQ 锁是特定于线程的。如果线程 A 锁定中断然后执行使自己休眠的操作(例如
    休眠 N 毫秒),一旦线程 A 被换出并且下一个就绪线程 B 开始运行,线程的 IRQ
    锁就不再适用。

    这意味着当线程 B 运行时可以处理中断,除非线程 B 也使用自己的 IRQ 锁锁定了
    中断。(在使用 IRQ 锁的两个线程之间切换时内核是否可以处理中断是特定于
    架构的。)

    当线程 A 最终再次成为当前线程时,内核会重新建立线程 A 的 IRQ 锁。这确保
    线程 A 在显式解锁其 IRQ 锁之前不会被中断。

    如果线程 A 不休眠但确实使更高优先级的线程 B 就绪,则 IRQ 锁将抑制否则会
    发生的任何抢占。线程 B 将不会运行,直到释放 IRQ 锁后到达下一个
    :ref:`重新调度点 <scheduling_v2>`。

或者,线程可以暂时**禁用**指定的 IRQ,以便在发出 IRQ 信号时其关联的 ISR 不
执行。随后必须**启用** IRQ 以允许 ISR 执行。

.. important::
    禁用 IRQ 会阻止系统中的*所有*线程被关联的 ISR 抢占,而不仅仅是禁用 IRQ
    的线程。

.. _zlis:

零延迟中断
----------

通过应用 IRQ 锁来防止中断可能会增加观察到的中断延迟。然而,对于某些低延迟
用例,高中断延迟可能是不可接受的。

内核通过允许具有关键延迟约束的中断以中断锁定无法阻止的优先级级别执行来解决
此类用例。这些中断被定义为*零延迟中断*。对零延迟中断的支持需要启用
:kconfig:option:`CONFIG_ZERO_LATENCY_IRQS`。配置为零延迟的任何中断也必须
声明为 :ref:`直接 ISR <direct_isrs>`(并且不得在其中使用
:c:macro:`ISR_DIRECT_PM`),因为常规 ISR 与内核交互。除此之外,标志
:c:macro:`IRQ_ZERO_LATENCY` 必须传递给 :c:macro:`IRQ_DIRECT_CONNECT` 宏以
配置具有零延迟的特定中断。在某些架构上可以将零延迟中断 ISR 声明为直接和
动态,请参阅 :ref:`direct_isrs`。

零延迟中断预期用于直接管理硬件事件,而根本不与内核代码互操作。它们应该将
所有内核 API 视为未定义行为(即,在零延迟中断上下文中使用 API 的应用程序负责
直接验证正确的行为)。零延迟中断不得修改从正常 Zephyr 上下文调用的内核 API
检查的任何数据,并且不得生成需要同步处理的异常(例如内核恐慌)。

.. important::
    零延迟中断在特定于架构的基础上受支持。该功能目前在 ARM Cortex-M 架构
    变体中实现。

.. tip::
    为了缓解 flash 访问延迟,请考虑将 ISR 和所有相关符号重新定位到 RAM。

卸载 ISR 工作
=============

ISR 应该快速执行以确保可预测的系统操作。如果需要耗时的处理,ISR 应该将部分
或全部处理卸载到线程,从而恢复内核响应其他中断的能力。

内核支持几种机制来将中断相关处理卸载到线程。

* ISR 可以使用内核对象(如 FIFO、LIFO 或信号量)向辅助线程发出信号以执行
  中断相关处理。

* ISR 可以指示系统工作队列线程执行工作项。(请参阅 :ref:`workqueues_v2`。)

当 ISR 将工作卸载到线程时,当 ISR 完成时通常会有一次上下文切换到该线程,
允许中断相关处理几乎立即继续。但是,根据处理卸载的线程的优先级,可能在调度
处理卸载的线程之前执行当前执行的协作线程或其他更高优先级的线程。

共享中断线
==========

在某些硬件平台的情况下,不同的 IP 可能使用相同的中断线。例如,中断 17 可能
被 DMA 控制器用于发出数据传输已完成的信号,或者被 DAI 控制器用于发出传输
FIFO 已达到其水印的信号。为了使这一点工作,必须采用一些特殊逻辑或找到解决
方法(例如,使用 shared_irq 中断控制器),这不能很好地扩展。

为了解决这个问题,可以使用共享中断,可以使用
:kconfig:option:`CONFIG_SHARED_INTERRUPTS` 启用。每当尝试在同一中断线上
注册第二个 ISR/参数对时(使用 :c:macro:`IRQ_CONNECT` 或
:c:func:`irq_connect_dynamic`),中断线将变为共享,这意味着每次触发中断时
都将调用两个 ISR/参数对(前一个和刚刚注册的一个)。在共享中断上下文中使用
中断线的实体被称为客户端。中断的最大允许客户端数由
:kconfig:option:`CONFIG_SHARED_IRQ_MAX_NUM_CLIENTS` 控制。

中断共享对用户是透明的。因此,用户可以像通常那样使用 :c:macro:`IRQ_CONNECT`
和 :c:func:`irq_connect_dynamic` 注册中断。中断共享在幕后处理。

启用共享中断支持和动态中断支持将允许用户使用
:c:func:`irq_disconnect_dynamic` 动态断开 ISR。断开 ISR 后,每当触发为其
注册的中断线时,ISR 将不再被调用。

请注意,启用 :kconfig:option:`CONFIG_SHARED_INTERRUPTS` 将导致二进制大小
显著增加。请谨慎使用。

实现
****

定义常规 ISR
============

通过调用 :c:macro:`IRQ_CONNECT` 在运行时定义 ISR。然后必须通过调用
:c:func:`irq_enable` 启用它。

.. important::
    IRQ_CONNECT() 不是 C 函数,在幕后执行一些内联汇编魔法。它的所有参数
    必须在构建时已知。具有多个实例的驱动程序可能需要定义每个实例的配置函数
    来配置中断的每个实例。

以下代码定义并启用 ISR。

.. code-block:: c

    #define MY_DEV_IRQ  24       /* 设备使用 IRQ 24 */
    #define MY_DEV_PRIO  2       /* 设备使用中断优先级 2 */
    /* 传递给 my_isr() 的参数,在这种情况下是指向设备的指针 */
    #define MY_ISR_ARG  DEVICE_GET(my_device)
    #define MY_IRQ_FLAGS 0       /* IRQ 标志 */

    void my_isr(void *arg)
    {
       ... /* ISR 代码 */
    }

    void my_isr_installer(void)
    {
       ...
       IRQ_CONNECT(MY_DEV_IRQ, MY_DEV_PRIO, my_isr, MY_ISR_ARG, MY_IRQ_FLAGS);
       irq_enable(MY_DEV_IRQ);
       ...
    }

由于 :c:macro:`IRQ_CONNECT` 宏要求其所有参数在构建时已知,在某些情况下这可能
不可接受。也可以使用 :c:func:`irq_connect_dynamic` 在运行时安装中断。它的
使用方式与 :c:macro:`IRQ_CONNECT` 完全相同:

.. code-block:: c

    void my_isr_installer(void)
    {
       ...
       irq_connect_dynamic(MY_DEV_IRQ, MY_DEV_PRIO, my_isr, MY_ISR_ARG,
                           MY_IRQ_FLAGS);
       irq_enable(MY_DEV_IRQ);
       ...
    }

动态中断需要启用 :kconfig:option:`CONFIG_DYNAMIC_INTERRUPTS` 选项。当前不
支持删除或重新配置动态中断。

.. _direct_isrs:

定义'直接' ISR
==============

常规 Zephyr 中断引入了一些开销,对于某些低延迟用例可能是不可接受的。具体来说:

* 检索 ISR 的参数并将其传递给 ISR

* 如果启用了电源管理并且系统处于空闲状态,则在执行 ISR 之前,所有硬件都将从
  低功耗状态恢复,这可能非常耗时

* 尽管某些架构将在硬件中执行此操作,但其他架构需要在代码中切换到中断栈

* 在服务中断后,操作系统然后执行一些逻辑以潜在地做出调度决策

* :ref:`zlis` 必须始终声明为直接 ISR,因为常规 ISR 与内核交互

Zephyr 支持所谓的'直接'中断,通过 :c:macro:`IRQ_DIRECT_CONNECT` 安装,
其处理程序使用 :c:macro:`ISR_DIRECT_DECLARE` 声明。这些直接中断有一些特殊的
实现要求和减少的功能集;有关详细信息,请参阅 :c:macro:`IRQ_DIRECT_CONNECT`
和 :c:macro:`ISR_DIRECT_DECLARE` 的定义。

以下代码演示了直接 ISR:

.. code-block:: c

    #define MY_DEV_IRQ  24       /* 设备使用 IRQ 24 */
    #define MY_DEV_PRIO  2       /* 设备使用中断优先级 2 */
    #define MY_IRQ_FLAGS 0       /* IRQ 标志 */

    ISR_DIRECT_DECLARE(my_isr)
    {
       do_stuff();
       /* 在服务中断后执行 PM 以获得最佳延迟。这不能用于零延迟 IRQ,
       因为它访问内核数据。*/
       ISR_DIRECT_PM();
       /* 要求内核检查是否应该做出调度决策。如果 ISR 用于零延迟 IRQ,
       则返回值必须始终为 0。*/
       return 1;
    }

    void my_isr_installer(void)
    {
       ...
       IRQ_DIRECT_CONNECT(MY_DEV_IRQ, MY_DEV_PRIO, my_isr, MY_IRQ_FLAGS);
       irq_enable(MY_DEV_IRQ);
       ...
    }

在特定于架构的基础上支持动态直接中断的安装。该功能目前在 Arm Cortex-M 架构
变体中通过宏 :c:macro:`ARM_IRQ_DIRECT_DYNAMIC_CONNECT` 实现,可用于声明
直接和动态中断。

基于 RAM 的 ISR 执行
====================

对于超低延迟,可以将 ISR 和向量表重新定位到 RAM 以消除 flash 访问延迟。
这可以通过启用 :kconfig:option:`CONFIG_SRAM_VECTOR_TABLE` 和
:kconfig:option:`CONFIG_SRAM_SW_ISR_TABLE` 选项来实现,这将导致向量表
放置在 RAM 中。然后,可以使用 Zephyr :ref:`代码和数据重定位
<code_data_relocation>` 将 ISR 代码和所有相关符号也重新定位到 RAM。

共享中断线
==========

以下代码使用相同的中断号定义两个 ISR。

.. code-block:: c

    #define MY_DEV_IRQ 24		/* 设备使用 INTID 24 */
    #define MY_DEV_IRQ_PRIO 2		/* 设备使用中断优先级 2 */
    /*  此参数可以是任何东西 */
    #define MY_FST_ISR_ARG INT_TO_POINTER(1)
    /*  此参数可以是任何东西 */
    #define MY_SND_ISR_ARG INT_TO_POINTER(2)
    #define MY_IRQ_FLAGS 0		/* IRQ 标志 */

    void my_first_isr(void *arg)
    {
       ... /* 这里发生一些魔法 */
    }

    void my_second_isr(void *arg)
    {
       ... /* 这里发生更多魔法 */
    }

    void my_isr_installer(void)
    {
       ...
       IRQ_CONNECT(MY_DEV_IRQ, MY_DEV_IRQ_PRIO, my_first_isr, MY_FST_ISR_ARG, MY_IRQ_FLAGS);
       IRQ_CONNECT(MY_DEV_IRQ, MY_DEV_IRQ_PRIO, my_second_isr, MY_SND_ISR_ARG, MY_IRQ_FLAGS);
       ...
    }

`定义常规 ISR`_ 中描述的关于 :c:macro:`IRQ_CONNECT` 的相同限制在这里适用。
如果禁用 :kconfig:option:`CONFIG_SHARED_INTERRUPTS`,上述代码将生成构建错误。
否则,上述代码将导致每次触发中断 24 时调用两个 ISR。

如果 :kconfig:option:`CONFIG_SHARED_IRQ_MAX_NUM_CLIENTS` 设置为低于 2
(当前客户端数)的值,将生成构建错误。

如果启用动态中断,:c:func:`irq_connect_dynamic` 将允许在运行时共享中断。
超过配置的最大允许客户端数将导致断言失败。

动态断开 ISR
============

以下代码使用相同的中断号定义两个 ISR。第二个 ISR 在运行时断开连接。

.. code-block:: c

    #define MY_DEV_IRQ 24		/* 设备使用 INTID 24 */
    #define MY_DEV_IRQ_PRIO 2		/* 设备使用中断优先级 2 */
    /*  此参数可以是任何东西 */
    #define MY_FST_ISR_ARG INT_TO_POINTER(1)
    /*  此参数可以是任何东西 */
    #define MY_SND_ISR_ARG INT_TO_POINTER(2)
    #define MY_IRQ_FLAGS 0		/* IRQ 标志 */

    void my_first_isr(void *arg)
    {
       ... /* 这里发生一些魔法 */
    }

    void my_second_isr(void *arg)
    {
       ... /* 这里发生更多魔法 */
    }

    void my_isr_installer(void)
    {
       ...
       IRQ_CONNECT(MY_DEV_IRQ, MY_DEV_IRQ_PRIO, my_first_isr, MY_FST_ISR_ARG, MY_IRQ_FLAGS);
       IRQ_CONNECT(MY_DEV_IRQ, MY_DEV_IRQ_PRIO, my_second_isr, MY_SND_ISR_ARG, MY_IRQ_FLAGS);
       ...
    }

    void my_isr_uninstaller(void)
    {
       ...
       irq_disconnect_dynamic(MY_DEV_IRQ, MY_DEV_IRQ_PRIO, my_first_isr, MY_FST_ISR_ARG, MY_IRQ_FLAGS);
       ...
    }

:c:func:`irq_disconnect_dynamic` 调用将导致中断 24 变为非共享,这意味着
系统将表现得好像第一个 :c:macro:`IRQ_CONNECT` 调用从未发生过。只有在启用
:kconfig:option:`CONFIG_DYNAMIC_INTERRUPTS` 时才允许此行为,否则将生成
链接器错误。

实现细节
========

中断表在构建时使用一些特殊的构建工具设置。这里列出的详细信息适用于除 x86
之外的所有架构,x86 在下面的 `x86 详细信息`_ 部分中介绍。

:c:macro:`IRQ_CONNECT` 的调用将声明一个 struct _isr_list 的实例,该实例
放置在特殊的 .intList 部分中。此部分仅在预编译阶段放置在编译代码中。它旨在
由 Zephyr 脚本用于生成中断表,并从最终构建中删除。该脚本实现不同的解析器来
处理来自 .intList 部分的数据并产生所需的输出。

默认解析器生成 C 数组,填充直接从 .intList 部分条目获取的地址形式的参数和
中断处理程序。它适用于所有架构和编译器(上面提到的例外)。此解析器的限制是,
在生成数组后,代码不应重新定位。此阶段的任何重新定位可能导致中断数组中的
条目不再指向预期的函数。这意味着此解析器虽然更兼容,但限制我们使用链接时
优化。

本地 isr 声明解析器使用不同的方法在二进制级别构造相同的数组。数组的所有条目
都在本地声明和定义,直接在使用 :c:macro:`IRQ_CONNECT` 的文件中。它们放置在
具有唯一合成名称的部分中。然后将部分的名称放置在 .intList 部分中,并用于
创建链接器脚本,以正确地将创建的条目放置在内存中的正确位置。此解析器现在
仅限于支持的架构和工具链,但作为回报,它保留了链接器的对象关系信息,从而
允许链接时优化。

使用 C 数组实现
---------------

这是所有 Zephyr 支持的架构可用的默认配置。

任何 :c:macro:`IRQ_CONNECT` 的调用都将声明一个 struct _isr_list 的实例,
该实例放置在特殊的 .intList 部分中:

.. code-block:: c

    struct _isr_list {
        /** IRQ 线号 */
        int32_t irq;
        /** 此 IRQ 的标志,请参阅 ISR_FLAG_* 定义 */
        int32_t flags;
        /** 要调用的 ISR */
        void *func;
        /** 非直接 IRQ 的参数 */
        void *param;
    };

Zephyr 分两个阶段构建;构建的第一阶段产生
``${ZEPHYR_PREBUILT_EXECUTABLE}``.elf,其中包含 .intList 部分中的所有条目,
前面有一个头:

.. code-block:: c

    struct {
        void *spurious_irq_handler;
        void *sw_irq_handler;
        uint32_t num_isrs;
        uint32_t num_vectors;
        struct _isr_list isrs[];  <- 大小为 num_isrs
    };

由 ``${ZEPHYR_PREBUILT_EXECUTABLE}``.elf 内的头和 struct _isr_list 实例
组成的此数据然后由 gen_isr_tables.py 脚本使用,以生成定义向量表和软件 ISR
表的 C 文件,然后将其编译并链接到最终应用程序中。

任何中断的优先级级别都不编码在这些表中,相反 :c:macro:`IRQ_CONNECT` 还有一个
运行时组件,它将中断的所需优先级级别编程到中断控制器。某些架构不支持中断
优先级的概念,在这种情况下忽略优先级参数。

向量表
~~~~~~

当启用 :kconfig:option:`CONFIG_GEN_IRQ_VECTOR_TABLE` 时生成向量表。此数据
结构由 CPU 本地使用,只是一个函数指针数组,其中每个元素 n 对应于 IRQ 线 n
的 IRQ 处理程序,函数指针是:

#. 对于使用 :c:macro:`IRQ_DIRECT_CONNECT` 声明的'直接'中断,处理程序函数
   将放置在这里。
#. 对于使用 :c:macro:`IRQ_CONNECT` 声明的常规中断,公共软件 IRQ 处理程序的
   地址放置在这里。此代码执行公共内核中断簿记,并从软件 ISR 表查找 ISR 和
   参数。
#. 对于根本未配置的中断线,伪中断处理程序的地址将放置在这里。如果遇到,
   伪中断处理程序会导致系统致命错误。

某些架构对所有中断都有一个公共入口点,并且不支持向量表,在这种情况下应禁用
:kconfig:option:`CONFIG_GEN_IRQ_VECTOR_TABLE` 选项。

某些架构可能为系统异常保留一些初始向量并在其他地方的表中声明这一点,在这种
情况下,需要设置 CONFIG_GEN_IRQ_START_VECTOR 以正确偏移表中的索引。

SW ISR 表
~~~~~~~~~

这是 struct _isr_table_entry 的数组:

.. code-block:: c

    struct _isr_table_entry {
        void *arg;
        void (*isr)(void *);
    };

公共软件 IRQ 处理程序使用此表查找 ISR 及其参数并执行它。在中断控制器寄存器中
查找活动 IRQ 线并用于索引此表。

共享 SW ISR 表
~~~~~~~~~~~~~~

这是 struct z_shared_isr_table_entry 的数组:

.. code-block:: c

    struct z_shared_isr_table_entry {
        struct _isr_table_entry clients[CONFIG_SHARED_IRQ_MAX_NUM_CLIENTS];
        size_t client_num;
    };

此表跟踪每个中断线的已注册客户端。每当中断线变为共享时,
:c:func:`z_shared_isr` 将替换 _sw_isr_table 中当前注册的 ISR。此特殊 ISR
将遍历已注册客户端列表并调用 ISR。

使用链接器脚本实现
------------------

这种准备和解析 .isrList 部分以实现中断向量数组的方法称为本地 isr 声明。
该名称来自于这样一个事实,即将创建中断向量的数组的所有条目都在调用
:c:macro:`IRQ_CONNECT` 宏的位置本地创建。然后使用自动生成的链接器脚本将
其放置在内存中的正确位置。

此选项需要通过选择 :kconfig:option:`CONFIG_ISR_TABLES_LOCAL_DECLARATION`
启用。如果所使用的架构和工具链支持此配置,则设置
:kconfig:option:`CONFIG_ISR_TABLES_LOCAL_DECLARATION_SUPPORTED`。
有关当前支持的配置的信息,请参阅此选项的详细信息。

任何 :c:macro:`IRQ_CONNECT` 或 :c:macro:`IRQ_DIRECT_CONNECT` 的调用都将
声明一个 ``struct _isr_list_sname`` 的实例,该实例放置在特殊的 .intList
部分中:

.. code-block:: c

    struct _isr_list_sname {
        /** IRQ 线号 */
        int32_t irq;
        /** 此 IRQ 的标志,请参阅 ISR_FLAG_* 定义 */
        int32_t flags;
        /** 部分名称 */
        const char sname[];
    };

请注意,部分名称放置在灵活数组成员中。这意味着初始化结构的大小将根据结构
名称长度而变化。整个条目在应用程序构建期间由脚本使用,并具有正确中断放置
所需的所有信息。

除了 _isr_list_sname 之外,:c:macro:`IRQ_CONNECT` 宏还生成一个条目,该条目
将成为中断数组的一部分:

.. code-block:: c

    struct _isr_table_entry {
        const void *arg;
        void (*isr)(const void *);
    };

此数组放置在名称保存在 _isr_list_sname 结构中的部分中。

:c:macro:`IRQ_DIRECT_CONNECT` 宏创建的值取决于架构。它可以更改为指向中断
处理程序的变量:

.. code-block:: c

    static uintptr_t <唯一名称> = ((uintptr_t)func);

或者实际上是实现跳转到中断处理程序的裸函数:

.. code-block:: c

    static void <唯一名称>(void)
    {
        __asm(ARCH_IRQ_VECTOR_JUMP_CODE(func));
    }

与 :c:macro:`IRQ_CONNECT` 类似,创建的变量或函数放置在一个部分中,保存在
_isr_list_sname 部分中。

脚本生成的文件
~~~~~~~~~~~~~~

中断表生成器脚本创建 3 个文件::file:`isr_tables.c`、
:file:`isr_tables_swi.ld` 和 :file:`isr_tables_vt.ld`。

:file:`isr_tables.c` 将包含中断、直接中断和共享中断(如果启用)的所有结构。
此文件仅实现应用程序未实现的所有结构,留下注释说明在此处未实现的中断可以在
哪里找到。

然后使用两个链接器文件。:file:`isr_tables_vt.ld` 文件包含在所选架构中需要
放置中断向量的位置。:file:`isr_tables_swi.ld` 文件描述软件中断表元素的
放置。需要单独的文件,因为它可能放置在可写或不可写部分中,具体取决于当前
配置。

x86 详细信息
------------

x86 架构有一种特殊类型的向量表,称为中断描述符表 (IDT),必须按照 x86 处理器
文档以某种方式布局。它本质上仍然是一个向量表,:ref:`gen_idt.py` 工具使用
.intList 部分创建它。但是,在基于 APIC 的系统上,向量表中的索引不对应于 IRQ
线。前 32 个向量保留用于 CPU 异常,所有剩余向量(最多索引 255)对应于优先级
级别,以 16 个为一组。在此方案中,优先级级别 0 的中断将放置在向量 32-47 中,
级别 1 48-63,依此类推。当 :ref:`gen_idt.py` 工具构造 IDT 时,当它配置中断
时,它将在请求的优先级级别的适当范围内查找空闲向量并在那里设置处理程序。

在 x86 上,当 CPU 执行中断或异常向量时,没有万无一失的方法来确定触发了哪个
向量,因此不使用按 IRQ 线索引的软件 ISR 表。相反,:c:macro:`IRQ_CONNECT`
调用创建一个小的汇编语言函数,该函数使用 ISR 和参数作为参数调用
:c:func:`_interrupt_enter` 中的公共中断代码。放置在 IDT 中的是此汇编中断
存根的地址。对于使用 :c:macro:`IRQ_DIRECT_CONNECT` 声明的中断,无参数 ISR
直接放置在 IDT 中。

在向量表中的位置对应于中断优先级级别的系统上,中断控制器需要在运行时知道
哪个向量与 IRQ 线相关联。:ref:`gen_idt.py` 另外创建一个
_irq_to_interrupt_vector 数组,该数组将 IRQ 线映射到其在 IDT 中配置的向量。
这在运行时由 :c:macro:`IRQ_CONNECT` 使用,以在中断控制器中编程 IRQ 到向量
关联。

对于动态中断,构建必须生成一些 4 字节动态中断存根,每个正在使用的动态中断
一个存根。存根的数量由 :kconfig:option:`CONFIG_X86_DYNAMIC_IRQ_STUBS` 选项
控制。每个存根推送一个唯一标识符,然后用于从连接动态中断时填充的表中获取
适当的处理程序函数和参数。

超越默认支持的中断数
--------------------

在多级配置中生成中断时,每级 8 位是确定给定中断代码属于哪个级别时使用的
默认掩码。在处理支持每个单个聚合器超过 255 个中断的 CPU 时,这可能成为问题。
在这种情况下,可能需要覆盖这些默认值并使用每个级别的自定义位数。无论每个
级别使用多少位,所有级别之间使用的总位数之和必须小于或等于 32 位,适合单个
32 位整数。要修改每个级别的位总数,请通过设置第一级的
:kconfig:option:`CONFIG_1ST_LEVEL_INTERRUPT_BITS`、第二级的
:kconfig:option:`CONFIG_2ND_LEVEL_INTERRUPT_BITS` 和第三级的
:kconfig:option:`CONFIG_3RD_LEVEL_INTERRUPT_BITS` 来覆盖
:file:`Kconfig.multilevel` 中的默认值 8。这些掩码控制在生成中断值时、
检查中断级别时以及将中断转换为不同级别时应用的位掩码和移位的长度。控制
这一点的逻辑可以在 :file:`irq_multilevel.h` 中找到。

建议用途
********

使用常规或直接 ISR 执行需要非常快速响应并且可以快速完成而不阻塞的中断处理。

.. note::
    耗时或涉及阻塞的中断处理应移交给线程。有关可在应用程序中使用的各种技术的
    说明,请参阅 `卸载 ISR 工作`_。

配置选项
********

相关配置选项:

* :kconfig:option:`CONFIG_ISR_STACK_SIZE`

还存在其他特定于架构和特定于设备的配置选项。

API 参考
********

.. doxygengroup:: isr_apis
