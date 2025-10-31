.. _device_model_api:

设备驱动模型
############

简介
****
Zephyr 内核支持多种设备驱动。某个驱动是否可用取决于所用的开发板与对应驱动本身。

Zephyr 的设备模型提供了统一一致的方式来配置系统中的各类驱动，并负责在启动时初始化所有已配置的驱动。

每类驱动（例如 UART、SPI、I2C）都通过对应的通用 API 进行支持。

在该模型中，驱动会在初始化期间将其 API 函数的函数指针填入包含函数指针的结构体中。按照初始化等级顺序，这些结构被放置到 RAM 的相应段中。

.. image:: device_driver_model.svg
   :width: 40%
   :align: center
   :alt: 设备驱动模型

标准驱动
********

所有受支持的板级配置都会包含以下设备驱动：

* **中断控制器**：供内核的中断管理子系统使用。
* **定时器**：供内核的系统时钟与硬件时钟子系统使用。
* **串行通信**：供内核的系统控制台子系统使用。
* **熵源（Entropy）**：为随机数生成器子系统提供熵数来源。

  .. important::

     获取随机值请使用 :ref:`随机数 API <random_api>`。:ref:`熵源函数 <entropy_api>` 不应被直接用作随机数生成器来源，因为部分硬件实现仅设计为随机数生成器的熵种子来源，无法提供密码学意义上安全的随机数流。

同步调用
********

Zephyr 为多种开发板提供了成套的设备驱动。除非特定硬件不支持中断，否则每个驱动都应优先采用基于中断的实现，而非轮询。

通过设备专用 API（如 :file:`i2c.h`、:file:`spi.h`）提供的高层调用通常被设计为同步语义，因此这些调用应为阻塞式。

.. _device_driver_api:

驱动 API
*********

下述设备驱动相关 API 由 :file:`device.h` 提供。这些 API 仅面向驱动内部使用，不应在应用中直接调用。

:c:macro:`DEVICE_DEFINE()`
   创建设备对象及相关数据结构，并设置其在引导阶段初始化。

:c:macro:`DEVICE_NAME_GET()`
   将设备标识符转换为对应设备对象的全局标识符。

:c:macro:`DEVICE_GET()`
   通过名称获取设备对象指针。

:c:macro:`DEVICE_DECLARE()`
   声明设备对象。当需要对尚未定义的设备进行前向引用时使用。

:c:macro:`DEVICE_API()`
   包装驱动 API 声明并将其放入对应的链接器段。

.. _device_struct:

驱动数据结构
************

设备初始化相关的宏会在构建阶段填充部分数据结构，并划分为只读部分与运行期可变部分。高层结构如下：

.. code-block:: C

  struct device {
	const char *name;
	const void *config;
	const void *api;
	void * const data;
  };

``config`` 成员用于保存构建期设置的只读配置信息，例如 MMIO 基地址、IRQ 号或设备的其他固定物理特征。这就是传递给 ``DEVICE_DEFINE()`` 及相关宏的 ``config`` 指针。

``data`` 结构存放于 RAM，由驱动用于单实例的运行期维护，例如引用计数、信号量、临时缓冲等。

``api`` 结构将通用子系统 API 映射到驱动中的设备特定实现。该结构通常为只读，并在构建期填充。下一节将作进一步说明。


子系统与 API 结构
*****************

多数驱动会实现与具体设备无关的子系统 API。应用只需面向该通用 API 编程，从而避免与具体驱动实现绑定。

如果所有驱动 API 实例都被放入各自的 API 链接段，可使用 :c:macro:`DEVICE_API_IS()` 校验 API 的类型。

一个典型的子系统 API 定义如下：

.. code-block:: C

  typedef int (*subsystem_do_this_t)(const struct device *dev, int foo, int bar);
  typedef void (*subsystem_do_that_t)(const struct device *dev, void *baz);

  __subsystem struct subsystem_driver_api {
        subsystem_do_this_t do_this;
        subsystem_do_that_t do_that;
  };

  static inline int subsystem_do_this(const struct device *dev, int foo, int bar)
  {
        return DEVICE_API_GET(subsystem, dev)->do_this(dev, foo, bar);
  }

  static inline void subsystem_do_that(const struct device *dev, void *baz)
  {
        DEVICE_API_GET(subsystem, dev)->do_that(dev, baz);
  }

实现某个子系统的驱动会提供这些 API 的实际实现，并使用 :c:macro:`DEVICE_API()` 包装后，填充一个 subsystem_driver_api 结构实例：

.. code-block:: C

  static int my_driver_do_this(const struct device *dev, int foo, int bar)
  {
        ...
  }

  static void my_driver_do_that(const struct device *dev, void *baz)
  {
        ...
  }

  static DEVICE_API(subsystem, my_driver_api_funcs) = {
        .do_this = my_driver_do_this,
        .do_that = my_driver_do_that,
  };

随后，驱动会将 ``my_driver_api_funcs`` 作为 ``DEVICE_DEFINE()`` 的 ``api`` 参数传入。

.. note::

        由于 ``api`` 结构中持有 API 函数的指针，这些函数即使未被使用，也会被链接进二进制；链接器选项 ``gc-sections`` 总能看到至少一次引用。若希望通过链接期优化缩小体积，通常需要用 Kconfig 选项控制这些可选特性。

设备特定 API 扩展
******************

有些设备可被抽象为某个子系统（如 GPIO）的一个实例，但同时又提供标准 API 无法覆盖的额外能力。此时设备会将子系统操作与其设备特定的 API 结合，相关 API 通常在设备专用头文件中声明。

一个设备特定 API 的定义通常如下：

.. code-block:: C

   #include <zephyr/drivers/subsystem.h>

   /* 当扩展无需从用户态线程调用时 */
   int specific_do_that(const struct device *dev, int foo);

   /* 当扩展需要可由用户态线程调用时 */
   __syscall int specific_from_user(const struct device *dev, int bar);

   /* 仅当扩展包含系统调用时需要 */
   #include <zephyr/syscalls/specific.h>

为子系统提供扩展的驱动将同时实现子系统 API 与这些特定 API：

.. code-block:: C

   static int generic_do_this(const struct device *dev, void *arg)
   {
      ...
   }

   static struct generic_api api {
      ...
      .do_this = generic_do_this,
      ...
   };

   /* 仅特权态可用的 API 为全局可见 */
   int specific_do_that(const struct device *dev, int foo)
   {
      ...
   }

   /* 系统调用 API 通过封装进行传递 */
   int z_impl_specific_from_user(const struct device *dev, int bar)
   {
      ...
   }

   #ifdef CONFIG_USERSPACE

   #include <zephyr/internal/syscall_handler.h>

   int z_vrfy_specific_from_user(const struct device *dev, int bar)
   {
       K_OOPS(K_SYSCALL_SPECIFIC_DRIVER(dev, K_OBJ_DRIVER_GENERIC, &api));
      return z_impl_specific_do_that(dev, bar);
   }

   #include <zephyr/syscalls/specific_from_user_mrsh.c>

   #endif /* CONFIG_USERSPACE */

应用可同时通过子系统 API 与设备特定 API 来使用该设备。

.. note::
   设备特定扩展的公共 API 应以前缀标识其适用设备的 compatible。比如为 Maxim DS3231 提供专用函数时，上述示例中的标识片段 ``specific`` 应替换为 ``maxim_ds3231``。

单个驱动的多实例
******************

某些驱动在一个系统中可能会被多次实例化。例如可能存在多个 GPIO 组或多个 UART。每个驱动实例有各自不同的 ``config`` 与 ``data`` 结构。

为多个驱动实例配置中断是一个特殊情形：若每个实例需要配置不同的中断线，则可通过“每实例配置函数”来实现，因为传给 ``IRQ_CONNECT()`` 的参数必须在构建期即可解析。

例如，需要为两个 ``my_driver`` 实例配置不同的中断线，可在 ``drivers/subsystem/subsystem_my_driver.h`` 中：

.. code-block:: C

  typedef void (*my_driver_config_irq_t)(const struct device *dev);

  struct my_driver_config {
        DEVICE_MMIO_ROM;
        my_driver_config_irq_t config_func;
  };

在公共 init 函数的实现中：

.. code-block:: C

  void my_driver_isr(const struct device *dev)
  {
        /* 处理中断 */
        ...
  }

  int my_driver_init(const struct device *dev)
  {
        const struct my_driver_config *config = dev->config;

        DEVICE_MMIO_MAP(dev, K_MEM_CACHE_NONE);

        /* 进行其他初始化动作 */
        ...

        config->config_func(dev);

        return 0;
  }

随后在声明具体实例时：

.. code-block:: C

  #if CONFIG_MY_DRIVER_0

  DEVICE_DECLARE(my_driver_0);

  static void my_driver_config_irq_0(const struct device *dev)
  {
        IRQ_CONNECT(MY_DRIVER_0_IRQ, MY_DRIVER_0_PRI, my_driver_isr,
                    DEVICE_GET(my_driver_0), MY_DRIVER_0_FLAGS);
  }

  const static struct my_driver_config my_driver_config_0 = {
        DEVICE_MMIO_ROM_INIT(DT_DRV_INST(0)),
        .config_func = my_driver_config_irq_0
  }

  static struct my_data_0;

  DEVICE_DEFINE(my_driver_0, MY_DRIVER_0_NAME, my_driver_init,
                NULL, &my_data_0, &my_driver_config_0,
                POST_KERNEL, MY_DRIVER_0_PRIORITY, &my_api_funcs);

  #endif /* CONFIG_MY_DRIVER_0 */

注意这里使用了 ``DEVICE_DECLARE()``，以避免在提供 IRQ 处理函数参数与设备自身定义之间产生循环依赖。

初始化等级
**********

驱动可能依赖其他驱动先被初始化，或需要使用内核服务。:c:func:`DEVICE_DEFINE()` 及相关 API 允许指定初始化函数在引导序列中的执行时机。任何驱动都应选择以下三个初始化等级之一：

``PRE_KERNEL_1``
        适用于无依赖的设备，例如只依赖处理器/SoC 上硬件的设备。此等级配置阶段无法使用任何内核服务（尚不可用）。但中断子系统会完成配置，因此可以设置中断。该等级的初始化函数在中断栈上运行。

``PRE_KERNEL_2``
        适用于依赖 ``PRE_KERNEL_1`` 等级初始化完成的设备。此等级配置阶段同样无法使用内核服务。该等级的初始化函数在中断栈上运行。

``POST_KERNEL``
        适用于在配置期间需要内核服务的设备。该等级的初始化函数在内核主任务上下文中运行。

在每个初始化等级内，还可以指定相对于同等级其他设备的优先级。优先级为 0 到 999 的整数，数值越小表示越早初始化。优先级必须为不带前导零和符号的十进制整数字面量（例如 32），或等价的符号名称（例如 ``#define MY_INIT_PRIO 32``）；不允许使用表达式（例如 ``CONFIG_KERNEL_INIT_PRIORITY_DEFAULT + 5``）。

驱动及其他系统工具可以通过 :c:func:`k_is_pre_kernel` 判断启动是否仍处于 pre-kernel 阶段。

延迟初始化
**********

设备初始化也可以被延后执行。在这种情况下，设备不会在 Zephyr 启动时自动初始化，而是在应用调用 :c:func:`device_init` 时才进行初始化。若需延后某个设备驱动的初始化，可在对应 DTS 设备节点上添加属性 ``zephyr,deferred-init``。例如：

.. code-block:: devicetree

   / {
           a-driver@40000000 {
                   reg = <0x40000000 0x1000>;
                   zephyr,deferred-init;
           };
   };

系统级驱动
**********

在某些场景，你只需要在启动时运行一个函数。此时可使用 :c:macro:`SYS_INIT`。该宏不接收任何配置或运行期数据结构，且无法在后续通过名称获取设备指针。初始化等级与优先级的策略与设备驱动保持一致。

检查初始化序列
**************

使用 :c:macro:`DEVICE_DEFINE`（或其变体）与 :c:macro:`SYS_INIT` 声明的设备驱动会在启动时被处理，并按照指定的等级与优先级顺序调用对应的初始化函数。

有时需要查看链接器最终生成的初始化调用序列。可以使用 ``initlevels`` 这个 CMake 目标，例如执行 ``west build -t initlevels``。

错误处理
********

通常建议优先使用 ``__ASSERT()`` 宏，而不是传播返回值，除非这是运行过程中预期会出现的失败（例如存储设备写满）。对于错误参数、编程失误、一致性检查、不可恢复的异常等情况，应通过断言处理。

当确有必要将错误条件返回给调用方时，成功返回 0，失败返回 POSIX :file:`errno.h` 中的错误码。详见：
https://github.com/zephyrproject-rtos/zephyr/wiki/Naming-Conventions#return-codes

内存映射
********

在某些系统上，外设 MMIO（内存映射 I/O）的线性地址无法在构建期确定：

- 需要在运行期通过总线（如 PCIe）探测 I/O 范围；
- 系统启用了 MMU，MMIO 的物理地址需要由内核映射到页表中的某个虚拟地址。

这类系统需要在 RAM 中为 MMIO 区域保留存储，并在驱动的初始化函数中建立映射。其他系统则可直接使用来自 DTS 的 MMIO 物理地址，无需任何 RAM 存储。

为可能遇到此类情况的驱动，提供了 DEVICE_MMIO 作用域下的一组 API，以及映射函数 :c:func:`device_map`。

单个 MMIO 区域的设备模型驱动
==============================

最简单的情形是驱动仅需要维护一个 MMIO 区域。此时需在 ``config_info`` 与 ``driver_data`` 结构的定义中分别使用 ``DEVICE_MMIO_ROM`` 与 ``DEVICE_MMIO_RAM`` 宏，并通过 ``DEVICE_MMIO_ROM_INIT`` 从 DTS 初始化 ``config_info``。在 init 函数中调用 ``DEVICE_MMIO_MAP()``：

.. code-block:: C

   struct my_driver_config {
      DEVICE_MMIO_ROM; /* 必须置于首位 */
      ...
   }

   struct my_driver_dev_data {
      DEVICE_MMIO_RAM; /* 必须置于首位 */
      ...
   }

   const static struct my_driver_config my_driver_config_0 = {
      DEVICE_MMIO_ROM_INIT(DT_DRV_INST(...)),
      ...
   }

   int my_driver_init(const struct device *dev)
   {
      ...
      DEVICE_MMIO_MAP(dev, K_MEM_CACHE_NONE);
      ...
   }

   int my_driver_some_function(const struct device *dev)
   {
      ...
      /* 向 MMIO 区域写入数据 */
      sys_write32(0xDEADBEEF, DEVICE_MMIO_GET(dev));
      ...
   }

这些宏的具体展开取决于配置。在没有 MMU 或 PCIe 的设备上，``DEVICE_MMIO_MAP`` 与 ``DEVICE_MMIO_RAM`` 将不产生实际代码。

具有多个 MMIO 区域的设备模型驱动
================================

有些驱动可能拥有多个 MMIO 区域。另外，有些驱动已经实现了类似“继承”的结构，需要在 ``config_info`` 与 ``driver_data`` 结构中将其他数据放在更前位置。

可以使用 ``DEVICE_MMIO_NAMED`` 系列宏来处理。这需要定义 ``DEV_CFG()`` 与 ``DEV_DATA()`` 宏，以便获得类型正确的 config_info 或 dev_data 指针。例如：

.. code-block:: C

   struct my_driver_config {
      ...
	DEVICE_MMIO_NAMED_ROM(corge);
	DEVICE_MMIO_NAMED_ROM(grault);
      ...
   }

   struct my_driver_dev_data {
	   ...
	DEVICE_MMIO_NAMED_RAM(corge);
	DEVICE_MMIO_NAMED_RAM(grault);
	...
   }

   #define DEV_CFG(_dev) \
      ((const struct my_driver_config *)((_dev)->config))

   #define DEV_DATA(_dev) \
      ((struct my_driver_dev_data *)((_dev)->data))

   const static struct my_driver_config my_driver_config_0 = {
      ...
      DEVICE_MMIO_NAMED_ROM_INIT(corge, DT_DRV_INST(...)),
      DEVICE_MMIO_NAMED_ROM_INIT(grault, DT_DRV_INST(...)),
      ...
   }

   int my_driver_init(const struct device *dev)
   {
      ...
      DEVICE_MMIO_NAMED_MAP(dev, corge, K_MEM_CACHE_NONE);
      DEVICE_MMIO_NAMED_MAP(dev, grault, K_MEM_CACHE_NONE);
      ...
   }

   int my_driver_some_function(const struct device *dev)
   {
      ...
      /* 向多个 MMIO 区域写入数据 */
      sys_write32(0xDEADBEEF, DEVICE_MMIO_GET(dev, grault));
      sys_write32(0xF0CCAC1A, DEVICE_MMIO_GET(dev, corge));
      ...
   }

同一 DT 节点下具有多个 MMIO 区域的设备模型驱动
=============================================

有些驱动会在同一 DT 设备节点下定义多个 MMIO 区域，并通过 ``reg-names`` 属性加以区分，例如：

.. code-block:: devicetree

   /dts-v1/;

   / {
           a-driver@40000000 {
                   reg = <0x40000000 0x1000>,
                         <0x40001000 0x1000>;
                   reg-names = "corge", "grault";
           };
   };

此情形与上一节类似，但需要改用 ``DEVICE_MMIO_NAMED_ROM_INIT_BY_NAME`` 宏。也就是说，差异仅出现在驱动配置结构中：

.. code-block:: C

   const static struct my_driver_config my_driver_config_0 = {
      ...
      DEVICE_MMIO_NAMED_ROM_INIT_BY_NAME(corge, DT_DRV_INST(...)),
      DEVICE_MMIO_NAMED_ROM_INIT_BY_NAME(grault, DT_DRV_INST(...)),
      ...
   }

不使用 Zephyr 设备模型的驱动
============================

某些驱动或类驱动代码可能不使用 Zephyr 的设备模型，此时必须为 MMIO 数据安排替代性存储。例如定时器驱动或中断控制器代码。

可以使用 ``DEVICE_MMIO_TOPLEVEL`` 宏族来处理，例如：

.. code-block:: C

   DEVICE_MMIO_TOPLEVEL_STATIC(my_regs, DT_DRV_INST(..));

   void some_init_code(...)
   {
      ...
      DEVICE_MMIO_TOPLEVEL_MAP(my_regs, K_MEM_CACHE_NONE);
      ...
   }

   void some_function(...)
      ...
      sys_write32(DEVICE_MMIO_TOPLEVEL_GET(my_regs), 0xDEADBEEF);
      ...
   }

不使用 DTS 的驱动
=================

有些驱动（如 PCIe 场景）不会从 DTS 获取 MMIO 物理地址。此时可直接使用 :c:func:`device_map`：

.. code-block:: C

   void some_init_code(...)
   {
      ...
      struct pcie_bar mbar;
      bool bar_found = pcie_get_mbar(bdf, index, &mbar);

      device_map(DEVICE_MMIO_RAM_PTR(dev), mbar.phys_addr, mbar.size, K_MEM_CACHE_NONE);
      ...
   }

对于这类情况，可省略 DEVICE_MMIO_ROM 相关指示。

API 参考
********

.. doxygengroup:: device_model
