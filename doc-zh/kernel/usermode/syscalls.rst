.. _syscalls:

系统调用（System Calls）
########################
用户线程相较于特权线程拥有更少的权限：某些 CPU 指令不可用，且只能访问受限的内存区域。系统调用允许用户线程执行它们直接无法完成的操作。

在定义系统调用时，务必确保对 API 私有数据的访问仅通过系统调用接口进行；不应直接向用户态线程暴露内核私有数据。例如，``k_queue`` API 有意未暴露为系统调用，因为它们把队列的簿记信息直接放在用户可见的队列缓冲中。

允许用户注册在特权态运行的回调函数的 API 不应作为系统调用暴露，应仅供特权态使用。

本节描述如何声明新的系统调用，并讨论其实现相关的一些细节。

组成部分（Components）
*********************

所有系统调用包含以下组件：

* 以 :c:macro:`__syscall` 前缀标注的 API 的“C 原型”。该原型位于 ``include/`` 目录或其他 ``SYSCALL_INCLUDE_DIRS`` 指定的目录下的头文件中。此原型不需人工实现，而由 :ref:`gen_syscalls.py` 脚本生成。生成的内容是一个 inline 函数：若在特权态调用则直接调用实现函数；若在用户态调用则完成权限提升与参数校验后再调用。

* “实现函数”（implementation function），是真正完成工作的函数。若由用户态发起，该实现函数可假定所有入参已通过校验。

* “验证函数”（verification function），包装实现函数，对传入的所有参数进行校验。

* “解包函数/解组函数”（unmarshalling function），自动生成，用户源代码必须包含。

C 原型（C Prototype）
*******************

C 原型描述该 API 从用户态或特权态被调用时的签名。例如初始化信号量：

.. code-block:: c

    __syscall void k_sem_init(struct k_sem *sem, unsigned int initial_count,
                              unsigned int limit);

:c:macro:`__syscall` 属性非常特殊。对 C 编译器而言，它只是展开为 'static inline'；而对构建后脚本 :ref:`parse_syscalls.py` 而言，则表示该 API 是系统调用。该脚本会解析函数原型以确定返回类型与参数类型，并存在一些限制：

* 数组参数必须以指针形式传入，而非数组。例如 ``int foo[]`` 或 ``int foo[12]`` 均不允许，应使用 ``int *foo``。

* 函数指针会让有限的解析器非常困惑。解决方式是先 typedef，再在参数列表中使用该 typedef。

* :c:macro:`__syscall` 必须出现在原型声明的最前面。

在确定需要生成的系统调用集合时，预处理器不会被使用。然而，若某些生成的系统调用在当前内核配置下并不存在对应的验证函数（因为相关特性未启用），则它们会指向一个“未实现系统调用”的通用验证函数。API 的数据类型定义不应对编译器进行条件隐藏。

声明了系统调用的任何头文件，都必须在文件末尾包含一个特别生成的头，命名规则为 ``syscalls/<头文件名>``。例如在 ``include/sensor.h`` 的末尾：

.. code-block:: c

    #include <zephyr/syscalls/sensor.h>

系统调用原型必须声明在 CMake 变量 ``SYSCALL_INCLUDE_DIRS`` 所列目录之一内。通常当启用 ``CONFIG_APPLICATION_DEFINED_SYSCALL`` 时，此列表包含 ``APPLICATION_SOURCE_DIR``；启用 ``CONFIG_ZTEST`` 时包含 ``${ZEPHYR_BASE}/subsys/testsuite/ztest/include``。还可通过 CMake 命令行或在调用 ``find_package(Zephyr ...)`` 之前的 CMake 代码中加入路径。``${ZEPHYR_BASE}/include`` 始终会被扫描。

注意，并非所有系统调用都会被编译进最终二进制。CMake 函数 ``zephyr_syscall_header`` 与 ``zephyr_syscall_header_ifdef`` 用于指定哪些头文件中的系统调用原型必须出现在最终二进制中。位于 ``SYSCALL_INCLUDE_DIRS`` 指定目录中的头文件内的系统调用会被无条件包含。若希望强制所有系统调用都被包含，可启用 :kconfig:option:`CONFIG_EMIT_ALL_SYSCALLS`。

调用上下文（Invocation Context）
==============================

若可明确某个 C 文件内的代码全部在用户态运行，或全部在特权态运行，则可使使用系统调用 API 的源码更高效。系统会查找 :c:macro:`__ZEPHYR_SUPERVISOR__` 或 :c:macro:`__ZEPHYR_USER__` 的定义，通常它们会在构建系统中以编译器选项的形式为相关文件添加。

* 若未启用 :kconfig:option:`CONFIG_USERSPACE`，所有 API 仅直接调用实现函数。

* 否则，默认情况是运行时检查当前是否处于用户态，并据此要么发起系统调用，要么直接调用实现函数。

* 若定义了 :c:macro:`__ZEPHYR_SUPERVISOR__`，则假定所有代码都在特权态运行，API 直接调用实现函数。若实际在用户态运行，一旦尝试执行不被允许的操作，就会产生 CPU 异常。

* 若定义了 :c:macro:`__ZEPHYR_USER__`，则假定所有代码都在用户态运行，并无条件发起系统调用。

实现细节（Implementation Details）
================================

将 API 以 :c:macro:`__syscall` 声明，会使 :ref:`gen_syscalls.py` 在工程的 out 目录 ``include/generated/`` 下生成若干 C 与头文件：

* 在 ``include/generated/zephyr/syscall_list.h`` 中把该系统调用加入系统调用 ID 的枚举，命名为大写 API 名并加前缀 ``K_SYSCALL_``。

* 在分发表 ``_k_syscall_table``（文件 ``include/generated/zephyr/syscall_dispatch.c``）中创建对应表项。

  * 当启用 :kconfig:option:`CONFIG_EMIT_ALL_SYSCALLS` 时，仅那些其原型声明位于“指定头文件”中的系统调用会被加入该表：

    * 由 CMake 函数 ``zephyr_syscall_header`` 或 ``zephyr_syscall_header_ifdef`` 指定，或

    * 位于 ``SYSCALL_INCLUDE_DIRS`` 指定的目录下。

* 声明一个弱验证函数（weak），其为“未实现系统调用”验证器的别名。因为真正的验证函数是否会被编译取决于内核配置；例如用户线程调用了传感器子系统 API，但该子系统未启用，则会调用该弱验证器。

* 在 ``include/generated/<name>_mrsh.c`` 中定义解包函数。

API 的函数体位于生成的系统头里。以 :c:func:`k_sem_init()` 为例，该 API 在 ``include/kernel.h`` 中声明，而其底部包含：

::

    #include <zephyr/syscalls/kernel.h>

在此头中包含 :c:func:`k_sem_init()` 的函数体：

::

    static inline void k_sem_init(struct k_sem * sem, unsigned int initial_count, unsigned int limit)
    {
    #ifdef CONFIG_USERSPACE
            if (z_syscall_trap()) {
                    arch_syscall_invoke3(*(uintptr_t *)&sem, *(uintptr_t *)&initial_count, *(uintptr_t *)&limit, K_SYSCALL_K_SEM_INIT);
                    return;
            }
            compiler_barrier();
    #endif
            z_impl_k_sem_init(sem, initial_count, limit);
    }

这会生成一个接收三个参数、返回 void 的内联函数。它会根据上下文要么直接调用实现函数，要么通过系统调用路径进行权限提升。实现函数的原型也会被自动生成。

最后一层是系统调用本身的触发。所有实现系统调用的架构都必须提供七个内联函数 :c:func:`_arch_syscall_invoke0` 到 :c:func:`_arch_syscall_invoke6`，用于将参数整理到指定的寄存器并执行权限提升。在作为系统调用参数传递前，API 内联函数的参数会强制转换为 ``uintptr_t``，以匹配寄存器大小。
但在 32 位系统上传递 64 位参数是个例外：64 位参数会被拆分为高/低两部分并作为相邻的两个参数传递。系统调用始终返回 ``uintptr_t`` 类型的值；若不需要可以忽略。

.. figure:: syscall_flow.png
   :alt: 系统调用执行流程
   :width: 80%
   :align: center

   系统调用执行流程

部分系统调用可能拥有超过六个参数，但所有架构通过寄存器传参的参数数量上限均为六个。额外的参数需要通过源内存空间中的数组传递；在验证函数中必须将其视为不可信内存。相关的打包/解包与校验代码会在上述 stub 与解包函数中按需自动生成。

系统调用返回 ``uintptr_t`` 类型的值，并由包装函数转换为 API 原型声明的返回类型。这意味着在 32 位系统上，系统调用无法直接将 64 位值返回给其包装函数。为解决此问题，自动生成的包装函数会在其栈上定义一个 64 位的中间变量（作为“不可信”缓冲），并在最后一个参数中把该变量的指针传递给系统调用；返回后，包装函数将返回写入该缓冲的值。64 位系统不存在此问题。

实现函数（Implementation Function）
********************************

实现函数是实际完成 API 工作的地方。Zephyr 通常对参数进行很少甚至不进行错误检查，或仅通过断言进行检查。编写实现函数时，参数验证是可选的，应倾向用断言完成。

所有实现函数必须遵循命名约定：API 名称前加前缀 ``z_impl_``。实现函数可以在与 API 相同的头文件中以 static inline 形式声明，或在某个 C 文件中声明。实现函数不需要手写原型，系统会自动生成。

验证函数（Verification Function）
******************************

当用户线程发起系统调用时，验证函数在内核侧运行。用户线程通过软件中断提升到特权态后，通用系统调用入口会根据用户提供的系统调用 ID 查找相应的解包函数并跳转调用，由其进一步调用验证函数。

仅当从用户态调用系统调用 API 时，验证与解包函数才会运行；若从特权态调用，直接调用实现函数，不会触发软件陷阱。

验证函数的目的在于校验所有传入参数，包括：

* 任何内核对象指针。例如，信号量 API 必须确保传入的对象确为有效信号量，且调用线程对其有权限。

* 来自用户态的任何内存缓冲。必须检查调用线程对该缓冲是否具备读/写权限。

* 任何具有有限有效值范围的其他参数。

验证函数包含大量样板代码；:zephyr_file:`include/zephyr/internal/syscall_handler.h` 提供了简化编写的宏。应使用这些宏来声明验证函数。

参数校验（Argument Validation）
============================

用于校验参数的宏包括：

* :c:macro:`K_SYSCALL_OBJ()` 校验一个内存地址是否为期望类型的有效内核对象、调用线程是否具备权限、对象是否已初始化。

* :c:macro:`K_SYSCALL_OBJ_INIT()` 与 :c:macro:`K_SYSCALL_OBJ()` 类似，但允许提供的对象处于未初始化状态。适用于对象 init 函数的验证。

* :c:macro:`K_SYSCALL_OBJ_NEVER_INIT()` 与 :c:macro:`K_SYSCALL_OBJ()` 类似，但要求提供的对象必须未初始化。目前主要用于 :c:func:`k_thread_create()`。

* :c:macro:`K_SYSCALL_MEMORY_READ()` 校验给定大小的内存缓冲；调用线程必须对整个缓冲具有读权限。

* :c:macro:`K_SYSCALL_MEMORY_WRITE()` 与上述相同，但还要求调用线程具备写权限。

* :c:macro:`K_SYSCALL_MEMORY_ARRAY_READ()` 校验数组，数组总大小由元素个数与元素大小两个参数给出；该宏会正确处理乘法溢出。调用线程必须对总大小具有读权限。

* :c:macro:`K_SYSCALL_MEMORY_ARRAY_WRITE()` 与上述相同，但还要求调用线程具备写权限。

* :c:macro:`K_SYSCALL_VERIFY_MSG()` 对某布尔表达式进行运行时检查，若为假则校验失败。其变体 :c:macro:`K_SYSCALL_VERIFY` 不带消息参数，而是打印失败的表达式本身，仅应用于最明显的检查。

* :c:macro:`K_SYSCALL_DRIVER_OP()` 运行时检查某驱动实例是否支持某操作。该宏本身可直接使用，更多情况下作为为每个驱动子系统自动生成宏的基础。例如验证 GPIO 驱动可用 :c:macro:`K_SYSCALL_DRIVER_GPIO()`。

* :c:macro:`K_SYSCALL_SPECIFIC_DRIVER()` 运行时检查某指针是否为特定设备驱动的有效实例、调用线程是否具备权限、驱动是否已初始化。其通过检查驱动实例内保存的 API 结构体指针，校验其是否与提供的特定驱动 API 结构体地址一致。

若任何检查失败，这些宏会返回非零值。可调用 :c:macro:`K_OOPS()` 触发内核 oops 从而终止调用线程；这样做可避免为了保持从特权态调用 API 的一致性而引入错误返回值。

.. _syscall_verification:

验证器定义（Verifier Definition）
===============================

所有系统调用都会被分发到一个以 ``z_vrfy_`` 前缀命名的验证器函数。它与被包装的系统调用具有完全相同的返回类型和参数类型。其职责是在已验证所有参数后执行系统调用（通常是调用实现函数）。

验证器由自动生成的解包函数调用，该函数负责从体系结构层传入的寄存器参数中解包并转换为正确类型。此解包函数定义在必须由用户代码包含的头文件中，通常位于验证器定义之后（便于内联）。

例如：

.. code-block:: c

    static int z_vrfy_k_sem_take(struct k_sem *sem, int32_t timeout)
    {
        K_OOPS(K_SYSCALL_OBJ(sem, K_OBJ_SEM));
        return z_impl_k_sem_take(sem, timeout);
    }
    #include <zephyr/syscalls/k_sem_take_mrsh.c>


验证内存访问策略（Verification Memory Access Policies）
=====================================================

以引用方式传递给系统调用的参数需要特别处理，因为只要任一拥有该内存访问权的用户线程在任何时刻修改了该内存的内容，都可能影响内核的逻辑判断；即便做了检查，也可能引入攻击面。这类攻击称为 TOCTOU（检查时与使用时的时间差）。

规避此类攻击的正确方法是在验证函数中制作参数的副本，并仅对副本进行参数检查（用户线程永远无法访问这些副本）。实现函数接收副本，而非用户传入的原始数据。为此可使用 :c:func:`k_usermode_to_copy()` 与 :c:func:`k_usermode_from_copy()`。

有一个例外：当传入的是仅用于“写入”或“仅用于原样读取而从不参与控制流/校验”的大数据缓冲。稍后将进一步讨论。

第一个例子，输出整型参数：

.. code-block:: c

    int z_vrfy_some_syscall(int *out_param)
    {
        int local_out_param;
        int ret;

        ret = z_impl_some_syscall(&local_out_param);
        K_OOPS(k_usermode_to_copy(out_param, &local_out_param, sizeof(*out_param)));
        return ret;
    }

这里我们在栈上分配了 ``local_out_param``，将其地址传给实现函数，然后用 :c:func:`k_usermode_to_copy()` 写回调用者提供的缓冲。

看起来更简洁的写法：

.. code-block:: c

    int z_vrfy_some_syscall(int *out_param)
    {
        K_OOPS(K_SYSCALL_MEMORY_WRITE(out_param, sizeof(*out_param)));
        return z_impl_some_syscall(out_param);
    }

若实现函数出于某些逻辑需要读取该内存，这将变得不安全。例如它可能用于存储某个计数器值，拥有该内存访问权的用户线程可以篡改该值。对于小的整型值，采用第一个例子中的拷贝方式最安全。

有些参数可能是输入/输出双向的：常见的情况是传入一个 ``size_t`` 指针作为最大允许大小，随后实现函数会把它更新为实际处理的字节数。这同样应采用栈上副本：

.. code-block:: c

    int z_vrfy_in_out_syscall(size_t *size_ptr)
    {
        size_t size;
        int ret;

        K_OOPS(k_usermode_from_copy(&size, size_ptr, sizeof(size)));
        ret = z_impl_in_out_syscall(&size);
        K_OOPS(k_usermode_to_copy(size_ptr, &size, sizeof(size)));
        return ret;
    }

许多系统调用会传入结构体甚至链式结构体，均应进行拷贝。典型做法是在栈上分配副本：

.. code-block:: c

    struct bar {
        ...
    };

    struct foo {
        ...
        struct bar *bar_left;
        struct bar *bar_right;
    };

    int z_vrfy_must_alloc(struct foo *foo)
    {
        int ret;
        struct foo foo_copy;
        struct bar bar_right_copy;
        struct bar bar_left_copy;

        K_OOPS(k_usermode_from_copy(&foo_copy, foo, sizeof(*foo)));
        K_OOPS(k_usermode_from_copy(&bar_right_copy, foo_copy.bar_right,
                                sizeof(struct bar)));
        foo_copy.bar_right = &bar_right_copy;
        K_OOPS(k_usermode_from_copy(&bar_left_copy, foo_copy.bar_left,
                                sizeof(struct bar)));
        foo_copy.bar_left = &bar_left_copy;

        return z_impl_must_alloc(&foo_copy);
    }

在某些情况下，数据量在编译期未知或过大，无法在栈上分配。这时可能需要通过 :c:func:`z_thread_malloc()` 从调用者的资源池分配内存。此方案应被视为最后手段。功能安全编程指南强烈不建议使用堆，且必须清晰记录资源池的使用。分配失败必须向调用者返回 ``-ENOMEM``；请勿用 ``K_OOPS()`` 来判断资源分配是否成功。

.. code-block:: c

    struct bar {
        ...
    };

    struct foo {
        size_t count;
        struct bar *bar_list; /* array of struct bar of size count */
    };

    int z_vrfy_must_alloc(struct foo *foo)
    {
        int ret;
        struct foo foo_copy;
        struct bar *bar_list_copy;
        size_t bar_list_bytes;

        /* 安全地把 foo 拷贝到 foo_copy */
        K_OOPS(k_usermode_from_copy(&foo_copy, foo, sizeof(*foo)));

        /* 对我们拷贝的计数字段做边界检查 */
        if (foo_copy.count > 32) {
            return -EINVAL;
        }

        /* 为 bar_list 分配内存，并替换 foo_copy 中的指针 */
    bar_list_bytes = foo_copy.count * sizeof(struct bar);
        bar_list_copy = z_thread_malloc(bar_list_bytes);
        if (bar_list_copy == NULL) {
            return -ENOMEM;
        }
        K_OOPS(k_usermode_from_copy(bar_list_copy, foo_copy.bar_list,
                                bar_list_bytes));
        foo_copy.bar_list = bar_list_copy;

        ret = z_impl_must_alloc(&foo_copy);

        /* 用完释放并返回 */
        k_free(bar_list_copy);
        return ret;
    }

最后，考虑大数据缓冲。这类缓冲代表用户内存区域，要么从其中拷出数据，要么向其中拷入数据。允许将这些指针直接传给实现函数，但仍需使用 ``K_SYSCALL_MEMORY`` 宏验证调用者对该缓冲的访问权限。需满足以下约束：

 * 若缓冲由实现函数“写入”（例如从某 MMIO 区域采集数据），实现函数必须仅写入，不得读取。

 * 若缓冲由实现函数“读取”（例如将其写入某硬件目标），必须不对数据做任何处理；不得基于数据内容实现条件逻辑。若需要此类逻辑，必须制作副本。

 * 缓冲必须仅在调用的同步阶段使用；实现函数不得保存缓冲地址并进行异步使用（例如在中断发生时）。

.. code-block:: c

    int z_vrfy_get_data_from_kernel(void *buf, size_t size)
    {
        K_OOPS(K_SYSCALL_MEMORY_WRITE(buf, size));
        return z_impl_get_data_from_kernel(buf, size);
    }

验证返回值策略（Verification Return Value Policies）
=================================================

在验证系统调用时，需要明确哪类验证失败应将错误返回给调用者，哪类则应直接触发 :c:macro:`K_OOPS()` 终止调用线程。当前约定如下：

#. 对已声明但未编译的系统调用，将路由到 :c:func:`handler_no_syscall()` 并触发 :c:macro:`K_OOPS()`。

#. 由 ``K_SYSCALL_MEMORY`` 宏、:c:func:`k_usermode_from_copy()`、:c:func:`k_usermode_to_copy()` 发现的任何非法内存访问都应触发 :c:macro:`K_OOPS()`，例如调用者对缓冲无适当权限、或尺寸计算溢出。

#. 多数系统调用会接收内核对象指针参数，使用 ``K_SYSCALL_OBJ`` 家族、``K_SYSCALL_DRIVER_nnnnn`` 或 :c:func:`k_object_validate()` 校验。可能失败的原因包括：缺少驱动 API、无效对象指针、对象类型错误、或未正确初始化。这些问题都应触发 :c:macro:`K_OOPS()`。

#. 因内存堆分配失败（常见于 :c:func:`z_thread_malloc()`）产生的错误，应将 ``-ENOMEM`` 返回给调用者。

#. 一般参数检查应在实现函数中完成，通常使用 ``CHECKIF()``。

   * ``CHECKIF()`` 的行为取决于内核配置；当启用用户态时，会强制启用 :kconfig:option:`CONFIG_RUNTIME_ERROR_CHECKS`，从而保证这些检查会执行并返回错误值。

#. 严禁从用户态注册任何在内核态执行的回调。仅安装回调的 API 不应暴露为系统调用。某些驱动子系统 API 可能带可选回调指针；其用户态验证函数必须强制为 NULL，若非空则应触发 :c:macro:`K_OOPS()`。

#. 某些仅在用户态强制的参数检查，应在验证函数中完成，并尽可能将错误返回给调用者。

在 Zephyr 中，以下行为是对上述策略的既有例外：

* 当线程对象未初始化时，:c:func:`k_thread_join()` 与 :c:func:`k_thread_abort()` 为 no-op。这是因为线程的“初始化位”兼作“线程是否正在运行”的标志，在线程退出时清除。参见 #23030。

* :c:func:`k_thread_create()` 的参数检查使用 :c:macro:`K_OOPS()`，原因是大量现有代码忽略其返回值。此问题也将由 #23030 处理。

* 若终止的是“关键（essential）”线程，:c:func:`k_thread_abort()` 将触发 :c:macro:`K_OOPS()`，因为该函数无返回值。

* 若传入无效参数，与日志相关的若干系统调用会触发 :c:macro:`K_OOPS()`，因为它们不返回错误。

配置选项（Configuration Options）
********************************

相关配置项：

* :kconfig:option:`CONFIG_USERSPACE`
* :kconfig:option:`CONFIG_EMIT_ALL_SYSCALLS`

API
***

用于创建系统调用验证函数的辅助宏位于 :zephyr_file:`include/zephyr/internal/syscall_handler.h`：

* :c:macro:`K_SYSCALL_OBJ()`
* :c:macro:`K_SYSCALL_OBJ_INIT()`
* :c:macro:`K_SYSCALL_OBJ_NEVER_INIT()`
* :c:macro:`K_OOPS()`
* :c:macro:`K_SYSCALL_MEMORY_READ()`
* :c:macro:`K_SYSCALL_MEMORY_WRITE()`
* :c:macro:`K_SYSCALL_MEMORY_ARRAY_READ()`
* :c:macro:`K_SYSCALL_MEMORY_ARRAY_WRITE()`
* :c:macro:`K_SYSCALL_VERIFY_MSG()`
* :c:macro:`K_SYSCALL_VERIFY`

用于触发系统调用的函数定义在 :zephyr_file:`include/zephyr/syscall.h`：

* :c:func:`_arch_syscall_invoke0`
* :c:func:`_arch_syscall_invoke1`
* :c:func:`_arch_syscall_invoke2`
* :c:func:`_arch_syscall_invoke3`
* :c:func:`_arch_syscall_invoke4`
* :c:func:`_arch_syscall_invoke5`
* :c:func:`_arch_syscall_invoke6`
