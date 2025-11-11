.. _logging_api:

日志 (Logging)
##############

.. contents::
    :local:
    :depth: 2

日志 API 提供了一个通用接口来处理开发人员发出的消息。消息通过前端传递,然后由活动后端处理。如果需要,可以使用自定义前端和后端。(The logging API provides a common interface to process messages issued by developers. Messages are passed through a frontend and are then processed by active backends. Custom frontend and backends can be used if needed.)

日志功能摘要:(Summary of the logging features:)

- 延迟日志通过将耗时操作转移到已知上下文而不是在调用时处理和发送日志消息,减少了记录消息所需的时间。(Deferred logging reduces the time needed to log a message by shifting time consuming operations to a known context instead of processing and sending the log message when called.)
- 支持多个后端(最多9个后端)。(Multiple backends supported (up to 9 backends).)
- 自定义前端支持。它可以与后端一起工作。(Custom frontend support. It can work together with backends.)
- 模块级别的编译时过滤。(Compile time filtering on module level.)
- 每个后端独立的运行时过滤。(Run time filtering independent for each backend.)
- 模块实例级别的额外运行时过滤。(Additional run time filtering on module instance level.)
- 使用用户提供的函数进行时间戳标记。时间戳可以有32位或64位。(Timestamping with user provided function. Timestamp can have 32 or 64 bits.)
- 用于转储数据的专用 API。(Dedicated API for dumping data.)
- 用于处理临时字符串的专用 API。(Dedicated API for handling transient strings.)
- 恐慌支持 - 在恐慌模式下,日志切换到阻塞、同步处理。(Panic support - in panic mode logging switches to blocking, synchronous processing.)
- Printk 支持 - printk 消息可以重定向到日志。(Printk support - printk message can be redirected to the logging.)
- 为多域/多处理器系统准备的设计。(Design ready for multi-domain/multi-processor system.)
- 支持记录浮点变量和 long long 参数。(Support for logging floating point variables and long long arguments.)
- 内置复制用作参数的临时字符串。(Built-in copying of transient strings used as arguments.)
- 支持多域日志。(Support for multi-domain logging.)
- 速率限制日志宏,用于防止频繁生成消息时的日志泛滥。(Rate-limited logging macros to prevent log flooding when messages are generated frequently.)

日志 API 在编译时和运行时都是高度可配置的。使用 Kconfig 选项(参见 :ref:`logging_kconfig`)可以在不需要日志时逐步从编译中删除日志,以减少镜像大小和执行时间。在编译期间,日志可以根据模块和严重级别进行过滤。(Logging API is highly configurable at compile time as well as at run time. Using Kconfig options (see :ref:`logging_kconfig`) logs can be gradually removed from compilation to reduce image size and execution time when logs are not needed. During compilation logs can be filtered out on module basis and severity level.)

日志也可以在编译时包含,但在运行时使用专用 API 进行过滤。运行时过滤对每个后端和每个日志消息源都是独立的。日志消息源可以是模块或模块的特定实例。(Logs can also be compiled in but filtered on run time using dedicate API. Run time filtering is independent for each backend and each source of log messages. Source of log messages can be a module or specific instance of the module.)

系统中有四个严重级别可用:错误、警告、信息和调试。对于每个严重级别,日志 API (:zephyr_file:`include/zephyr/logging/log.h`) 都有一组专用的宏。Logger API 还有用于记录数据的宏。(There are four severity levels available in the system: error, warning, info and debug. For each severity level the logging API (:zephyr_file:`include/zephyr/logging/log.h`) has set of dedicated macros. Logger API also has macros for logging data.)

对于每个级别,可用以下宏集:(For each level the following set of macros are available:)

- ``LOG_X`` 用于标准类似 printf 的消息,例如 :c:macro:`LOG_ERR`。(for standard printf-like messages, e.g. :c:macro:`LOG_ERR`.)
- ``LOG_HEXDUMP_X`` 用于转储数据,例如 :c:macro:`LOG_HEXDUMP_WRN`。(for dumping data, e.g. :c:macro:`LOG_HEXDUMP_WRN`.)
- ``LOG_INST_X`` 用于与特定实例关联的标准类似 printf 的消息,例如 :c:macro:`LOG_INST_INF`。(for standard printf-like message associated with the particular instance, e.g. :c:macro:`LOG_INST_INF`.)
- ``LOG_INST_HEXDUMP_X`` 用于转储与特定实例关联的数据,例如 :c:macro:`LOG_INST_HEXDUMP_DBG`。(for dumping data associated with the particular instance, e.g. :c:macro:`LOG_INST_HEXDUMP_DBG`)

警告级别还公开以下附加宏:(The warning level also exposes the following additional macro:)

- :c:macro:`LOG_WRN_ONCE` 用于仅对第一次出现感兴趣的警告。(for warnings where only the first occurrence is of interest.)

速率限制日志宏也可用于所有严重级别,以防止日志泛滥:(Rate-limited logging macros are also available for all severity levels to prevent log flooding:)

- ``LOG_X_RATELIMIT`` 用于使用默认速率的速率限制标准类似 printf 的消息,例如 :c:macro:`LOG_ERR_RATELIMIT`。(for rate-limited standard printf-like messages using default rate, e.g. :c:macro:`LOG_ERR_RATELIMIT`.)
- ``LOG_X_RATELIMIT_RATE`` 用于具有自定义速率的速率限制标准类似 printf 的消息,例如 :c:macro:`LOG_ERR_RATELIMIT_RATE`。(for rate-limited standard printf-like messages with custom rate, e.g. :c:macro:`LOG_ERR_RATELIMIT_RATE`.)
- ``LOG_HEXDUMP_X_RATELIMIT`` 用于使用默认速率的速率限制数据转储,例如 :c:macro:`LOG_HEXDUMP_WRN_RATELIMIT`。(for rate-limited data dumping using default rate, e.g. :c:macro:`LOG_HEXDUMP_WRN_RATELIMIT`.)
- ``LOG_HEXDUMP_X_RATELIMIT_RATE`` 用于具有自定义速率的速率限制数据转储,例如 :c:macro:`LOG_HEXDUMP_WRN_RATELIMIT_RATE`。(for rate-limited data dumping with custom rate, e.g. :c:macro:`LOG_HEXDUMP_WRN_RATELIMIT_RATE`.)

便捷宏使用由 ``CONFIG_LOG_RATELIMIT_INTERVAL_MS`` 指定的默认速率,而显式速率宏采用速率参数(以毫秒为单位),指定日志消息之间的最小间隔。(The convenience macros use the default rate specified by ``CONFIG_LOG_RATELIMIT_INTERVAL_MS``, while the explicit rate macros take a rate parameter (in milliseconds) that specifies the minimum interval between log messages.)

有两个配置类别:每个模块的配置和全局配置。当全局启用日志记录时,它适用于模块。但是,模块可以在本地禁用日志记录。每个模块都可以指定自己的日志记录级别。模块必须在使用 API 之前定义 :c:macro:`LOG_LEVEL` 宏。除非设置了全局覆盖,否则将遵守模块日志记录级别。全局覆盖只能提高日志记录级别。它不能用于降低先前设置得更高的模块日志记录级别。还可以通过提供系统中存在的最大严重级别来全局限制日志,其中最大意味着最低严重性(例如,如果系统中的最大级别设置为 info,则意味着存在错误、警告和信息级别,但排除调试消息)。(There are two configuration categories: configurations per module and global configuration. When logging is enabled globally, it works for modules. However, modules can disable logging locally. Every module can specify its own logging level. The module must define the :c:macro:`LOG_LEVEL` macro before using the API. Unless a global override is set, the module logging level will be honored. The global override can only increase the logging level. It cannot be used to lower module logging levels that were previously set higher. It is also possible to globally limit logs by providing maximal severity level present in the system, where maximal means lowest severity (e.g. if maximal level in the system is set to info, it means that errors, warnings and info levels are present but debug messages are excluded).)

每个使用日志记录的模块都必须指定其唯一名称并向日志记录注册自己。如果模块由多个文件组成,则在一个文件中执行注册,但每个文件都必须定义模块名称。(Each module which is using the logging must specify its unique name and register itself to the logging. If module consists of more than one file, registration is performed in one file but each file must define a module name.)

Logger 的默认前端设计为线程安全的,并最大限度地减少记录消息所需的时间。在调用日志记录 API 时,默认情况下不执行字符串格式化或访问传输等耗时操作。调用日志记录 API 时,会创建一条消息并将其添加到列表中。使用专用的可配置日志消息池缓冲区。有2种类型的消息:标准消息和十六进制转储。每条消息包含源 ID(模块或实例 ID 和可能用于多处理器系统的域 ID)、时间戳和严重级别。标准消息包含指向字符串和参数的指针。十六进制转储消息包含复制的数据和字符串。(Logger's default frontend is designed to be thread safe and minimizes time needed to log the message. Time consuming operations like string formatting or access to the transport are not performed by default when logging API is called. When logging API is called a message is created and added to the list. Dedicated, configurable buffer for pool of log messages is used. There are 2 types of messages: standard and hexdump. Each message contain source ID (module or instance ID and
domain ID which might be used for multiprocessor systems), timestamp and
severity level. Standard message contains pointer to the string and arguments.
Hexdump message contains copied data and string.

.. _logging_kconfig:

全局 Kconfig 选项 (Global Kconfig Options)
*******************************************

这些选项可以在以下路径中找到 :zephyr_file:`subsys/logging/Kconfig`。(These options can be found in the following path :zephyr_file:`subsys/logging/Kconfig`.)

:kconfig:option:`CONFIG_LOG`: 全局开关,打开/关闭日志记录。(Global switch, turns on/off the logging.)

操作模式:(Mode of operations:)

:kconfig:option:`CONFIG_LOG_MODE_DEFERRED`: 延迟模式。(Deferred mode.)

:kconfig:option:`CONFIG_LOG_MODE_IMMEDIATE`: 立即(同步)模式。(Immediate (synchronous) mode.)

:kconfig:option:`CONFIG_LOG_MODE_MINIMAL`: 最小占用模式。(Minimal footprint mode.)

过滤选项:(Filtering options:)

:kconfig:option:`CONFIG_LOG_RUNTIME_FILTERING`: 启用过滤的运行时重新配置。(Enables runtime reconfiguration of the filtering.)

:kconfig:option:`CONFIG_LOG_DEFAULT_LEVEL`: 默认级别,设置未设置自己日志级别的模块使用的日志级别。(Default level, sets the logging level used by modules that are not setting their own logging level.)

:kconfig:option:`CONFIG_LOG_OVERRIDE_LEVEL`: 当模块日志级别未设置或设置低于覆盖值时,覆盖模块日志级别。(It overrides module logging level when it is not set or set lower than the override value.)

:kconfig:option:`CONFIG_LOG_MAX_LEVEL`: 编译的最大(最低严重性)级别。(Maximal (lowest severity) level which is compiled in.)

处理选项:(Processing options:)

:kconfig:option:`CONFIG_LOG_MODE_OVERFLOW`: 当无法分配新消息时,丢弃最旧的消息。(When new message cannot be allocated, oldest one are discarded.)

:kconfig:option:`CONFIG_LOG_BLOCK_IN_THREAD`: 如果启用并且无法分配新日志消息,线程上下文将阻塞最多 :kconfig:option:`CONFIG_LOG_BLOCK_IN_THREAD_TIMEOUT_MS` 或直到分配日志消息。(If enabled and new log message cannot be allocated thread context will block for up to :kconfig:option:`CONFIG_LOG_BLOCK_IN_THREAD_TIMEOUT_MS` or until log message is allocated.)

:kconfig:option:`CONFIG_LOG_PRINTK`: 将 printk 调用重定向到日志记录。(Redirect printk calls to the logging.)

:kconfig:option:`CONFIG_LOG_PROCESS_TRIGGER_THRESHOLD`: 当缓冲的日志消息数量达到阈值时,专用线程(参见 :c:func:`log_thread_set`)被唤醒。如果启用了 :kconfig:option:`CONFIG_LOG_PROCESS_THREAD`,则内部线程将使用此阈值。(When the number of buffered log messages reaches the threshold, the dedicated thread (see :c:func:`log_thread_set`) is woken up. If :kconfig:option:`CONFIG_LOG_PROCESS_THREAD` is enabled then this threshold is used by the internal thread.)

:kconfig:option:`CONFIG_LOG_PROCESS_THREAD`: 启用时,创建处理日志处理的日志记录线程。(When enabled, logging thread is created which handles log processing.)

:kconfig:option:`CONFIG_LOG_PROCESS_THREAD_STARTUP_DELAY_MS`: 启动日志记录线程后的延迟(以毫秒为单位)。(Delay in milliseconds after which logging thread is started.)

:kconfig:option:`CONFIG_LOG_BUFFER_SIZE`: 专用于循环数据包缓冲区的字节数。(Number of bytes dedicated for the circular packet buffer.)

:kconfig:option:`CONFIG_LOG_FRONTEND`: 将日志定向到自定义前端。(Direct logs to a custom frontend.)

:kconfig:option:`CONFIG_LOG_FRONTEND_ONLY`: 当消息发送到前端时不使用后端。(No backends are used when messages goes to frontend.)

:kconfig:option:`CONFIG_LOG_FRONTEND_OPT_API`: 为最常见的简单消息优化的可选 API。(Optional API optimized for the most common simple messages.)

:kconfig:option:`CONFIG_LOG_CUSTOM_HEADER`: 将应用程序提供的头文件注入到 log.h 中。(Injects an application provided header into log.h)

:kconfig:option:`CONFIG_LOG_TIMESTAMP_64BIT`: 64 位时间戳。(64 bit timestamp.)

:kconfig:option:`CONFIG_LOG_SIMPLE_MSG_OPTIMIZE`: 优化简单日志消息的大小和性能。选项仅适用于 32 位架构。(Optimizes simple log messages for size and performance. Option available only for 32 bit architectures.)

格式化选项:(Formatting options:)

:kconfig:option:`CONFIG_LOG_FUNC_NAME_PREFIX_ERR`: 在标准 ERROR 日志消息前添加函数名称。十六进制转储消息不添加前缀。(Prepend standard ERROR log messages with function name. Hexdump messages are not prepended.)

:kconfig:option:`CONFIG_LOG_FUNC_NAME_PREFIX_WRN`: 在标准 WARNING 日志消息前添加函数名称。十六进制转储消息不添加前缀。(Prepend standard WARNING log messages with function name. Hexdump messages are not prepended.)

:kconfig:option:`CONFIG_LOG_FUNC_NAME_PREFIX_INF`: 在标准 INFO 日志消息前添加函数名称。十六进制转储消息不添加前缀。(Prepend standard INFO log messages with function name. Hexdump messages are not prepended.)

:kconfig:option:`CONFIG_LOG_FUNC_NAME_PREFIX_DBG`: 在标准 DEBUG 日志消息前添加函数名称。十六进制转储消息不添加前缀。(Prepend standard DEBUG log messages with function name. Hexdump messages are not prepended.)

:kconfig:option:`CONFIG_LOG_BACKEND_SHOW_TIMESTAMP`: 启用后端在日志中打印时间戳。(Enables backend to print timestamps with log.)

:kconfig:option:`CONFIG_LOG_BACKEND_SHOW_LEVEL`: 启用后端在日志中打印级别。(Enables backend to print levels with log.)

:kconfig:option:`CONFIG_LOG_BACKEND_SHOW_COLOR`: 启用错误(红色)和警告(黄色)的着色。(Enables coloring of errors (red) and warnings (yellow).)

:kconfig:option:`CONFIG_LOG_BACKEND_FORMAT_TIMESTAMP`: 如果启用,时间戳格式化为 *hh:mm:ss:mmm,uuu*。否则以原始格式打印。(If enabled timestamp is formatted to *hh:mm:ss:mmm,uuu*. Otherwise is printed in raw format.)

后端选项:(Backend options:)

:kconfig:option:`CONFIG_LOG_BACKEND_UART`: 启用内置 UART 后端。(Enabled built-in UART backend.)

.. _log_usage:

使用 (Usage)
*************

模块中的日志记录 (Logging in a module)
=======================================

为了在模块中使用日志记录,必须指定模块的唯一名称,并且必须使用 :c:macro:`LOG_MODULE_REGISTER` 注册模块。可选地,可以将模块的编译时日志级别指定为第二个参数。如果未提供自定义日志级别,则使用默认日志级别(:kconfig:option:`CONFIG_LOG_DEFAULT_LEVEL`)。(In order to use logging in the module, a unique name of a module must be specified and module must be registered using :c:macro:`LOG_MODULE_REGISTER`. Optionally, a compile time log level for the module can be specified as the second parameter. Default log level (:kconfig:option:`CONFIG_LOG_DEFAULT_LEVEL`) is used if custom log level is not provided.)

.. code-block:: c

   #include <zephyr/logging/log.h>
   LOG_MODULE_REGISTER(foo, CONFIG_FOO_LOG_LEVEL);

如果模块由多个文件组成,则 ``LOG_MODULE_REGISTER()`` 应仅出现在其中一个文件中。其他每个文件都应使用 :c:macro:`LOG_MODULE_DECLARE` 来声明其在模块中的成员身份。可选地,可以将模块的编译时日志级别指定为第二个参数。如果未提供自定义日志级别,则使用默认日志级别(:kconfig:option:`CONFIG_LOG_DEFAULT_LEVEL`)。(If the module consists of multiple files, then ``LOG_MODULE_REGISTER()`` should appear in exactly one of them. Each other file should use :c:macro:`LOG_MODULE_DECLARE` to declare its membership in the module. Optionally, a compile time log level for the module can be specified as the second parameter. Default log level (:kconfig:option:`CONFIG_LOG_DEFAULT_LEVEL`) is used if custom log level is not provided.)

.. code-block:: c

   #include <zephyr/logging/log.h>
   /* In all files comprising the module but one */
   LOG_MODULE_DECLARE(foo, CONFIG_FOO_LOG_LEVEL);

为了在头文件中实现的函数中使用日志记录 API,必须在调用日志记录 API 之前在函数体中使用 :c:macro:`LOG_MODULE_DECLARE` 宏。可选地,可以将模块的编译时日志级别指定为第二个参数。如果未提供自定义日志级别,则使用默认日志级别(:kconfig:option:`CONFIG_LOG_DEFAULT_LEVEL`)。(In order to use logging API in a function implemented in a header file :c:macro:`LOG_MODULE_DECLARE` macro must be used in the function body before logging API is called. Optionally, a compile time log level for the module can be specified as the second parameter. Default log level (:kconfig:option:`CONFIG_LOG_DEFAULT_LEVEL`) is used if custom log level is not provided.)

.. code-block:: c

   #include <zephyr/logging/log.h>

   static inline void foo(void)
   {
   	LOG_MODULE_DECLARE(foo, CONFIG_FOO_LOG_LEVEL);

   	LOG_INF("foo");
   }

可以使用专用的 Kconfig 模板(:zephyr_file:`subsys/logging/Kconfig.template.log_config`)来创建本地日志级别配置。(Dedicated Kconfig template (:zephyr_file:`subsys/logging/Kconfig.template.log_config`) can be used to create local log level configuration.)

下面的示例展示了模板的使用。结果将生成 CONFIG_FOO_LOG_LEVEL:(Example below presents usage of the template. As a result CONFIG_FOO_LOG_LEVEL will be generated:)

.. code-block:: none

   module = FOO
   module-str = foo
   source "subsys/logging/Kconfig.template.log_config"

模块实例中的日志记录 (Logging in a module instance)
====================================================

对于多实例模块,且实例在整个系统中广泛使用的情况,启用日志将导致日志泛滥。日志记录器提供了一些工具,可用于在实例级别而不是模块级别提供过滤。在这种情况下,可以为特定实例启用日志记录。(In case of modules which are multi-instance and instances are widely used across the system enabling logs will lead to flooding. The logger provides the tools which can be used to provide filtering on instance level rather than module level. In that case logging can be enabled for particular instance.)

为了使用实例级别的过滤,必须执行以下步骤:(In order to use instance level filtering following steps must be performed:)

- 在实例结构中声明指向特定日志记录结构的指针。:c:macro:`LOG_INSTANCE_PTR_DECLARE` 用于此目的。(a pointer to specific logging structure is declared in instance structure. :c:macro:`LOG_INSTANCE_PTR_DECLARE` is used for that.)

.. code-block:: c

   #include <zephyr/logging/log_instance.h>

   struct foo_object {
   	LOG_INSTANCE_PTR_DECLARE(log);
   	uint32_t id;
   }

- 模块必须提供用于实例化的宏。在该宏中,日志实例被注册,并且日志实例指针在对象结构中被初始化。(module must provide macro for instantiation. In that macro, logging instance is registered and log instance pointer is initialized in the object structure.)

.. code-block:: c

   #define FOO_OBJECT_DEFINE(_name)                             \
   	LOG_INSTANCE_REGISTER(foo, _name, CONFIG_FOO_LOG_LEVEL) \
   	struct foo_object _name = {                             \
   		LOG_INSTANCE_PTR_INIT(log, foo, _name)          \
   	}

请注意,当日志记录被禁用时,不会创建日志实例和指向该实例的指针。(Note that when logging is disabled logging instance and pointer to that instance are not created.)

为了在源文件中使用实例日志记录 API,必须使用 :c:macro:`LOG_LEVEL_SET` 设置编译时日志级别。(In order to use the instance logging API in a source file, a compile-time log level must be set using :c:macro:`LOG_LEVEL_SET`.)

.. code-block:: c

   LOG_LEVEL_SET(CONFIG_FOO_LOG_LEVEL);

   void foo_init(foo_object *f)
   {
   	LOG_INST_INF(f->log, "Initialized.");
   }

为了在头文件中使用实例日志记录 API,必须使用 :c:macro:`LOG_LEVEL_SET` 设置编译时日志级别。(In order to use the instance logging API in a header file, a compile-time log level must be set using :c:macro:`LOG_LEVEL_SET`.)

.. code-block:: c

   static inline void foo_init(foo_object *f)
   {
   	LOG_LEVEL_SET(CONFIG_FOO_LOG_LEVEL);

   	LOG_INST_INF(f->log, "Initialized.");
   }

控制日志记录 (Controlling the logging)
=======================================

默认情况下,延迟模式下的日志处理由自动启动的专用任务在内部处理。但是,如果禁用多线程,它可能不可用。也可以通过取消设置 :kconfig:option:`CONFIG_LOG_PROCESS_TRIGGER_THRESHOLD` 来禁用它。在这种情况下,可以使用 :zephyr_file:`include/zephyr/logging/log_ctrl.h` 中定义的 API 来控制日志记录。日志记录必须在使用之前进行初始化。可选地,用户可以提供返回时间戳值的函数。如果未提供,则使用 :c:macro:`k_cycle_get` 或 :c:macro:`k_cycle_get_32` 进行时间戳记录。:c:func:`log_process` 函数用于触发一条日志消息(如果挂起)的处理,并在有更多消息挂起时返回 true。但是,建议使用宏包装器(:c:macro:`LOG_INIT` 和 :c:macro:`LOG_PROCESS`),它们处理禁用日志记录的情况。(By default, logging processing in deferred mode is handled internally by the dedicated task which starts automatically. However, it might not be available if multithreading is disabled. It can also be disabled by unsetting :kconfig:option:`CONFIG_LOG_PROCESS_TRIGGER_THRESHOLD`. In that case, logging can be controlled using the API defined in :zephyr_file:`include/zephyr/logging/log_ctrl.h`. Logging must be initialized before it can be used. Optionally, the user can provide a function which returns the timestamp value. If not provided, :c:macro:`k_cycle_get` or :c:macro:`k_cycle_get_32` is used for timestamping. The :c:func:`log_process` function is used to trigger processing of one log message (if pending), and returns true if there are more messages pending. However, it is recommended to use macro wrappers (:c:macro:`LOG_INIT` and :c:macro:`LOG_PROCESS`) which handle the case where logging is disabled.)

以下代码片段展示了如何在简单的永久循环中处理日志记录。(The following snippet shows how logging can be processed in simple forever loop.)

.. code-block:: c

   #include <zephyr/logging/log_ctrl.h>

   int main(void)
   {
   	LOG_INIT();
   	/* If multithreading is enabled provide thread id to the logging. */
   	log_thread_set(k_current_get());

   	while (1) {
   		if (LOG_PROCESS() == false) {
   			/* sleep */
   		}
   	}
   }

如果从线程(用户或内部)处理日志,则可以启用一个功能,当缓冲了一定数量的日志消息时,该功能将唤醒处理线程(请参阅 :kconfig:option:`CONFIG_LOG_PROCESS_TRIGGER_THRESHOLD`)。(If logs are processed from a thread (user or internal) then it is possible to enable a feature which will wake up processing thread when certain amount of log messages are buffered (see :kconfig:option:`CONFIG_LOG_PROCESS_TRIGGER_THRESHOLD`).)

.. _logging_ratelimited:

速率限制日志记录 (Rate-limited logging)
****************************************

速率限制日志记录宏提供了一种在频繁生成消息时防止日志泛滥的方法。这些宏确保日志消息的输出频率不高于指定的间隔,类似于 Linux 的 ``printk_ratelimited`` 功能。(Rate-limited logging macros provide a way to prevent log flooding when messages are generated frequently. These macros ensure that log messages are not output more frequently than a specified interval, similar to Linux's ``printk_ratelimited`` functionality.)

速率限制日志记录系统提供两种类型的宏:(The rate-limited logging system provides two types of macros:)

**便捷宏(使用默认速率):(Convenience macros (using default rate):)**
- :c:macro:`LOG_ERR_RATELIMIT` - 速率限制的错误消息 (Rate-limited error messages)
- :c:macro:`LOG_WRN_RATELIMIT` - 速率限制的警告消息 (Rate-limited warning messages)
- :c:macro:`LOG_INF_RATELIMIT` - 速率限制的信息消息 (Rate-limited info messages)
- :c:macro:`LOG_DBG_RATELIMIT` - 速率限制的调试消息 (Rate-limited debug messages)
- :c:macro:`LOG_HEXDUMP_ERR_RATELIMIT` - 速率限制的错误十六进制转储 (Rate-limited error hexdump)
- :c:macro:`LOG_HEXDUMP_WRN_RATELIMIT` - 速率限制的警告十六进制转储 (Rate-limited warning hexdump)
- :c:macro:`LOG_HEXDUMP_INF_RATELIMIT` - 速率限制的信息十六进制转储 (Rate-limited info hexdump)
- :c:macro:`LOG_HEXDUMP_DBG_RATELIMIT` - 速率限制的调试十六进制转储 (Rate-limited debug hexdump)

**显式速率宏(使用自定义速率):(Explicit rate macros (with custom rate):)**
- :c:macro:`LOG_ERR_RATELIMIT_RATE` - 具有自定义速率的速率限制错误消息 (Rate-limited error messages with custom rate)
- :c:macro:`LOG_WRN_RATELIMIT_RATE` - 具有自定义速率的速率限制警告消息 (Rate-limited warning messages with custom rate)
- :c:macro:`LOG_INF_RATELIMIT_RATE` - 具有自定义速率的速率限制信息消息 (Rate-limited info messages with custom rate)
- :c:macro:`LOG_DBG_RATELIMIT_RATE` - 具有自定义速率的速率限制调试消息 (Rate-limited debug messages with custom rate)
- :c:macro:`LOG_HEXDUMP_ERR_RATELIMIT_RATE` - 具有自定义速率的速率限制错误十六进制转储 (Rate-limited error hexdump with custom rate)
- :c:macro:`LOG_HEXDUMP_WRN_RATELIMIT_RATE` - 具有自定义速率的速率限制警告十六进制转储 (Rate-limited warning hexdump with custom rate)
- :c:macro:`LOG_HEXDUMP_INF_RATELIMIT_RATE` - 具有自定义速率的速率限制信息十六进制转储 (Rate-limited info hexdump with custom rate)
- :c:macro:`LOG_HEXDUMP_DBG_RATELIMIT_RATE` - 具有自定义速率的速率限制调试十六进制转储 (Rate-limited debug hexdump with custom rate)

便捷宏使用由 :kconfig:option:`CONFIG_LOG_RATELIMIT_INTERVAL_MS` 指定的默认速率(默认为 5000 毫秒)。显式速率宏采用速率参数(以毫秒为单位),该参数指定日志消息之间的最小间隔。速率限制是按宏调用站点进行的,这意味着每个对速率限制宏的唯一调用都有其自己的独立速率限制。(The convenience macros use the default rate specified by :kconfig:option:`CONFIG_LOG_RATELIMIT_INTERVAL_MS` (5000ms by default). The explicit rate macros take a rate parameter (in milliseconds) that specifies the minimum interval between log messages. The rate limiting is per-macro-call-site, meaning that each unique call to a rate-limited macro has its own independent rate limit.)

示例用法:(Example usage:)

.. code-block:: c

    #include <zephyr/logging/log.h>
    #include <zephyr/kernel.h>

    LOG_MODULE_REGISTER(my_module, CONFIG_LOG_DEFAULT_LEVEL);

    void process_data(void)
    {
        /* Convenience macros using default rate (CONFIG_LOG_RATELIMIT_INTERVAL_MS) */
        LOG_WRN_RATELIMIT("Data processing warning: %d", error_code);
        LOG_ERR_RATELIMIT("Critical error occurred: %s", error_msg);
        LOG_INF_RATELIMIT("Processing status: %d items", item_count);
        LOG_HEXDUMP_WRN_RATELIMIT(data_buffer, data_len, "Data buffer:");

        /* Explicit rate macros with custom intervals */
        LOG_WRN_RATELIMIT_RATE(1000, "Fast rate warning: %d", error_code);
        LOG_ERR_RATELIMIT_RATE(30000, "Slow rate error: %s", error_msg);
        LOG_INF_RATELIMIT_RATE(2000, "Custom rate status: %d items", item_count);
        LOG_HEXDUMP_ERR_RATELIMIT_RATE(5000, data_buffer, data_len, "Error data:");
    }

速率限制日志记录特别适用于:(Rate-limited logging is particularly useful for:)

- 可能频繁发生但不需要淹没日志的错误条件 (Error conditions that might occur frequently but don't need to flood the logs)
- 紧密循环或高频回调中的状态更新 (Status updates in tight loops or high-frequency callbacks)
- 可能使日志系统不堪重负的调试信息 (Debug information that could overwhelm the logging system)
- 可能反复失败的网络或 I/O 操作 (Network or I/O operations that might fail repeatedly)

配置 (Configuration)
=====================

可以使用以下 Kconfig 选项配置速率限制日志记录:(Rate-limited logging can be configured using the following Kconfig options:)

- :kconfig:option:`CONFIG_LOG_RATELIMIT` - 启用/禁用速率限制日志记录的主开关 (Master switch to enable/disable rate-limited logging)
- :kconfig:option:`CONFIG_LOG_RATELIMIT_INTERVAL_MS` - 便捷宏的默认间隔(5000 毫秒)(Default interval for convenience macros (5000ms))

当 :kconfig:option:`CONFIG_LOG_RATELIMIT` 被禁用时,速率限制宏的行为由 :kconfig:option:`CONFIG_LOG_RATELIMIT_FALLBACK` 选项控制:(When :kconfig:option:`CONFIG_LOG_RATELIMIT` is disabled, the behavior of rate-limited macros is controlled by the :kconfig:option:`CONFIG_LOG_RATELIMIT_FALLBACK` choice:)

- :kconfig:option:`CONFIG_LOG_RATELIMIT_FALLBACK_LOG` - 所有速率限制宏表现为常规日志宏 (All rate-limited macros behave as regular logging macros)
- :kconfig:option:`CONFIG_LOG_RATELIMIT_FALLBACK_DROP` - 所有速率限制宏扩展为无操作(默认)(All rate-limited macros expand to no-ops (default))

这允许您控制在速率限制不可用时,速率限制日志宏应始终打印还是完全抑制。(This allows you to control whether rate-limited log macros should always print or be completely suppressed when rate limiting is not available.)

速率限制使用静态变量和 :c:func:`k_uptime_get_32` 实现,以跟踪每个调用站点的最后一次日志时间。(The rate limiting is implemented using static variables and :c:func:`k_uptime_get_32` to track the last log time for each call site.)

.. _logging_panic:

日志记录恐慌模式 (Logging panic)
*********************************

在错误条件下,系统通常不能再依赖调度器或中断。在这种情况下,延迟日志消息处理不是一个选择。日志记录控制 API 提供了一个用于进入恐慌模式的函数(:c:func:`log_panic`),应在这种情况下调用该函数。(In case of error condition system usually can no longer rely on scheduler or interrupts. In that situation deferred log message processing is not an option. Logger controlling API provides a function for entering into panic mode (:c:func:`log_panic`) which should be called in such situation.)

当调用 :c:func:`log_panic` 时,会向所有活动的后端发送 *恐慌* 通知。一旦所有后端都收到通知,所有缓冲的消息都会被刷新。从那时起,所有日志都以阻塞方式处理。(When :c:func:`log_panic` is called, _panic_ notification is sent to all active backends. Once all backends are notified, all buffered messages are flushed. Since that moment all logs are processed in a blocking way.)

.. _logging_printk:

Printk
******

通常,日志记录和 :c:func:`printk` 使用相同的输出,它们会竞争输出。如果输出不支持抢占,这可能会导致问题,但也可能导致输出损坏,因为日志数据与 printk 数据交错。但是,可以通过启用 :kconfig:option:`CONFIG_LOG_PRINTK` 将 printk 消息重定向到日志记录子系统。在这种情况下,printk 条目被视为级别为 0 的日志消息(它们无法禁用)。启用后,日志记录管理输出,因此不会发生交错。但是,在延迟模式下,printk 行为会改变,因为输出会延迟,直到日志记录线程处理数据。:kconfig:option:`CONFIG_LOG_PRINTK` 默认启用。(Typically, logging and :c:func:`printk` use the same output, which they compete for. This can lead to issues if the output does not support preemption but it may also result in corrupted output because logging data is interleaved with printk data. However, it is possible to redirect printk messages to the logging subsystem by enabling :kconfig:option:`CONFIG_LOG_PRINTK`. In that case, printk entries are treated as log messages with level 0 (they cannot be disabled). When enabled, logging manages the output so there is no interleaving. However, in deferred mode the printk behaviour is changed since the output is delayed until the logging thread processes the data. :kconfig:option:`CONFIG_LOG_PRINTK` is enabled by default.)


.. _log_architecture:

架构 (Architecture)
*******************

日志记录由 3 个主要部分组成:(Logging consists of 3 main parts:)

- 前端 (Frontend)
- 核心 (Core)
- 后端 (Backends)

日志消息由日志记录源生成,该源可以是模块或模块的实例。(Log message is generated by a source of logging which can be a module or instance of a module.)

默认前端 (Default Frontend)
============================

当在日志记录源中调用日志记录 API(例如 :c:macro:`LOG_INF`)时,会使用默认前端,它负责过滤消息(编译和运行时)、为消息分配缓冲区、创建消息和提交该消息。由于日志记录 API 可以在中断中调用,因此前端经过优化,可以尽可能快地记录消息。(Default frontend is engaged when the logging API is called in a source of logging (e.g. :c:macro:`LOG_INF`) and is responsible for filtering a message (compile and run time), allocating a buffer for the message, creating the message and committing that message. Since the logging API can be called in an interrupt, the frontend is optimized to log the message as fast as possible.)

日志消息 (Log message)
----------------------

日志消息包含消息描述符(源、域和级别)、时间戳、格式化字符串详细信息(请参阅 :ref:`cbprintf_packaging`)和可选数据。日志消息存储在连续的内存块中。内存从循环数据包缓冲区(:ref:`mpsc_pbuf`)中分配,这有几个后果:(A log message contains a message descriptor (source, domain and level), timestamp, formatted string details (see :ref:`cbprintf_packaging`) and optional data. Log messages are stored in a continuous block of memory. Memory is allocated from a circular packet buffer (:ref:`mpsc_pbuf`), which has a few consequences:)

 * 每条消息都是一个独立的、连续的内存块,因此适合复制消息(例如用于离线处理)。(Each message is a self-contained, continuous block of memory thus it is suited for copying the message (e.g. for offline processing).)
 * 消息必须按顺序释放。后端处理是同步的。后端可以制作副本以进行延迟处理。(Messages must be sequentially freed. Backend processing is synchronous. Backend can make a copy for deferred processing.)

日志消息具有以下格式:(A log message has following format:)

+------------------+----------------------------------------------------+
| 消息头           | 2 位:MPSC 数据包缓冲区头                            |
| (Message Header) | (2 bits: MPSC packet buffer header)                |
|                  +----------------------------------------------------+
|                  | 1 位:跟踪/日志消息标志                              |
|                  | (1 bit: Trace/Log message flag)                    |
|                  +----------------------------------------------------+
|                  | 3 位:域 ID                                         |
|                  | (3 bits: Domain ID)                                |
|                  +----------------------------------------------------+
|                  | 3 位:级别                                          |
|                  | (3 bits: Level)                                    |
|                  +----------------------------------------------------+
|                  | 10 位:Cbprintf 包长度                              |
|                  | (10 bits: Cbprintf Package Length)                 |
|                  +----------------------------------------------------+
|                  | 12 位:数据长度                                     |
|                  | (12 bits: Data length)                             |
|                  +----------------------------------------------------+
|                  | 1 位:保留                                          |
|                  | (1 bit: Reserved)                                  |
|                  +----------------------------------------------------+
|                  | 指针:指向源描述符的指针 [#l0]_                      |
|                  | (pointer: Pointer to the source descriptor [#l0]_) |
|                  +----------------------------------------------------+
|                  | 32 或 64 位:时间戳 [#l0]_                          |
|                  | (32 or 64 bits: Timestamp [#l0]_)                  |
|                  +----------------------------------------------------+
|                  | 可选填充 [#l1]_                                    |
|                  | (Optional padding [#l1]_)                          |
+------------------+----------------------------------------------------+
| Cbprintf         | 头                                                 |
|                  | (Header)                                           |
| | 包             +----------------------------------------------------+
| | (package)      | 参数                                               |
| | (可选)         | (Arguments)                                        |
| | (optional)     +----------------------------------------------------+
|                  | 附加字符串                                         |
|                  | (Appended strings)                                 |
+------------------+----------------------------------------------------+
| 十六进制转储数据(可选)                                                |
| (Hexdump data (optional))                                            |
+------------------+----------------------------------------------------+
| 对齐填充(可选)                                                        |
| (Alignment padding (optional))                                       |
+------------------+----------------------------------------------------+

.. rubric:: 脚注 (Footnotes)

.. [#l0] 根据平台和时间戳大小,字段可能会交换。(Depending on the platform and the timestamp size fields may be swapped.)
.. [#l1] cbprintf 包对齐可能需要。(It may be required for cbprintf package alignment)

日志消息分配 (Log message allocation)
-------------------------------------

可能会发生前端无法分配消息的情况。如果系统生成的日志消息多于它在某个时间段内可以处理的消息,就会发生这种情况。有两种策略来处理这种情况:(It may happen that the frontend cannot allocate a message. This happens if the system is generating more log messages than it can process in certain time frame. There are two strategies to handle that case:)

- 无溢出 - 如果无法分配消息空间,则丢弃新日志。(No overflow - the new log is dropped if space for a message cannot be allocated.)
- 溢出 - 释放最旧的挂起消息,直到可以分配新消息。由 :kconfig:option:`CONFIG_LOG_MODE_OVERFLOW` 启用。请注意,它会降低性能,因此建议调整缓冲区大小和启用的日志数量以限制丢弃。(Overflow - the oldest pending messages are freed, until the new message can be allocated. Enabled by :kconfig:option:`CONFIG_LOG_MODE_OVERFLOW`. Note that it degrades performance thus it is recommended to adjust buffer size and amount of enabled logs to limit dropping.)

.. _logging_runtime_filtering:

运行时过滤 (Run-time filtering)
-------------------------------

如果启用了运行时过滤,则为每个日志记录源在 RAM 中声明一个过滤器结构。此类过滤器使用 32 位,分为十个 3 位槽。除了 *槽 0* 外,每个槽存储系统中一个后端的当前过滤器。*槽 0*(位 0-2)用于聚合给定日志记录源的最大过滤器设置。聚合槽确定是否为给定条目创建日志消息,因为它指示是否至少有一个后端期望该日志条目。当核心处理消息时,会检查后端槽,以确定给定后端是否接受消息。与编译时过滤相反,二进制占用空间增加,因为日志被编译进去。(If run-time filtering is enabled, then for each source of logging a filter structure in RAM is declared. Such filter is using 32 bits divided into ten 3 bit slots. Except *slot 0*, each slot stores current filter for one backend in the system. *Slot 0* (bits 0-2) is used to aggregate maximal filter setting for given source of logging. Aggregate slot determines if log message is created for given entry since it indicates if there is at least one backend expecting that log entry. Backend slots are examined when message is processed by the core to determine if message is accepted by the given backend. Contrary to compile time filtering, binary footprint is increased because logs are compiled in.)

在下面的示例中,后端 1 设置为接收错误(*槽 1*),后端 2 最多接收信息级别(*槽 2*)。槽 3-9 未使用。聚合过滤器(*槽 0*)设置为信息级别,来自该特定源的消息将被缓冲到此级别。(In the example below backend 1 is set to receive errors (*slot 1*) and backend 2 up to info level (*slot 2*). Slots 3-9 are not used. Aggregated filter (*slot 0*) is set to info level and up to this level message from that particular source will be buffered.)

+------+------+------+------+-----+------+
|槽 0  |槽 1  |槽 2  |槽 3  | ... |槽 9  |
|(slot |(slot |(slot |(slot | ... |(slot |
| 0)   | 1)   | 2)   | 3)   |     | 9)   |
+------+------+------+------+-----+------+
| INF  | ERR  | INF  | OFF  | ... | OFF  |
+------+------+------+------+-----+------+

.. _log_frontend:

自定义前端 (Custom Frontend)
=============================

使用 :kconfig:option:`CONFIG_LOG_FRONTEND` 启用自定义前端。日志被定向到 :zephyr_file:`include/zephyr/logging/log_frontend.h` 中声明的函数。如果启用了选项 :kconfig:option:`CONFIG_LOG_FRONTEND_ONLY`,则不会创建日志消息,也不会处理任何后端。否则,自定义前端可以与后端共存。(Custom frontend is enabled using :kconfig:option:`CONFIG_LOG_FRONTEND`. Logs are directed to functions declared in :zephyr_file:`include/zephyr/logging/log_frontend.h`. If option :kconfig:option:`CONFIG_LOG_FRONTEND_ONLY` is enabled then log message is not created and no backend is handled. Otherwise, custom frontend can coexist with backends.)

在某些情况下,需要在宏级别重定向日志。对于这些情况,:kconfig:option:`CONFIG_LOG_CUSTOM_HEADER` 可用于在 :zephyr_file:`include/zephyr/logging/log.h` 末尾注入名为 :file:`zephyr_custom_log.h` 的应用程序提供的头文件。(In some cases, logs need to be redirected at the macro level. For these cases, :kconfig:option:`CONFIG_LOG_CUSTOM_HEADER` can be used to inject an application provided header named :file:`zephyr_custom_log.h` at the end of :zephyr_file:`include/zephyr/logging/log.h`.)

使用 ARM Coresight STM(系统跟踪宏单元)的前端 (Frontend using ARM Coresight STM (System Trace Macrocell))
-----------------------------------------------------------------------------------------------------------

有关使用 ARM Coresight STM 进行日志记录的更多详细信息,请参阅 :ref:`logging_cs_stm`。(For more details about logging using ARM Coresight STM see :ref:`logging_cs_stm`.)

.. _logging_strings:

日志记录字符串 (Logging strings)
=================================

字符串参数由 :ref:`cbprintf_packaging` 处理。有关限制和建议,请参阅 :ref:`cbprintf_packaging_limitations`。(String arguments are handled by :ref:`cbprintf_packaging`. See :ref:`cbprintf_packaging_limitations` for limitations and recommendations.)

多域支持 (Multi-domain support)
================================

更复杂的系统可以由多个域组成,其中每个域都是一个独立的二进制文件。域的示例是多核 SoC 中的核心或 ARM TrustZone 核心上的二进制文件之一(安全或非安全)。(More complex systems can consist of multiple domains where each domain is an independent binary. Examples of domains are a core in a multicore SoC or one of the binaries (Secure or Nonsecure) on an ARM TrustZone core.)

在多域系统上进行跟踪和调试更加复杂,需要高效的日志记录系统。可以使用两种方法来构建此日志记录系统:(Tracing and debugging on a multi-domain system is more complex and requires an efficient logging system. Two approaches can be used to structure this logging system:)

* 在每个域内独立记录日志。此选项并非总是可行的,因为它要求每个域都有可用的后端(例如 UART)。由于日志呈现在独立的输出上,因此这种方法也可能难以使用且不可扩展。(Log inside each domain independently. This option is not always possible as it requires that each domain has an available backend (for example, UART). This approach can also be troublesome to use and not scalable, as logs are presented on independent outputs.)
* 使用多域日志记录系统,其中来自每个域的日志消息最终到达一个根域,在那里它们的处理方式与单域情况完全相同。在这种方法中,日志消息使用从一侧的后端创建并链接到另一侧的域之间的连接在域之间传递。(Use a multi-domain logging system where log messages from each domain end up in one root domain, where they are processed exactly as in a single domain case. In this approach, log messages are passed between domains using a connection between domains created from the backend on one side and linked to the other.)

  日志链接是在这种多域方法中引入的接口。日志链接负责接收来自另一个域的任何日志消息,创建副本,并将该本地日志消息副本(包括远程数据)放入消息队列。这种特定的日志链接实现与互补的后端实现相匹配,以允许日志消息交换和日志记录器控制,如配置过滤、获取日志源名称等。(The Log link is an interface introduced in this multi-domain approach. The Log link is responsible for receiving any log message from another domain, creating a copy, and putting that local log message copy (including remote data) into the message queue. This specific log link implementation matches the complementary backend implementation to allow log messages exchange and logger control like configuring filtering, getting log source names, and so on.)

多域系统中有三种类型的域:(There are three types of domains in a multi-domain system:)

* *端域* 具有日志记录核心实现和跨域后端。它也可以并行拥有其他后端。(The *end domain* has the logging core implementation and a cross-domain backend. It can also have other backends in parallel.)
* *中继域* 具有到其他域的一个或多个链接,但没有向用户输出日志的后端。它具有到另一个中继或根域的跨域后端。(The *relay domain* has one or more links to other domains but does not have backends that output logs to the user. It has a cross-domain backend either to another relay or to the root domain.)
* *根域* 具有一个或多个链接以及向用户输出日志的后端。(The *root domain* has one or multiple links and a backend that outputs logs to the user.)

有关多域设置示例,请参见下图:(See the following image for an example of a multi-domain setup:)

.. figure:: images/multidomain.png

    多域示例 (Multi-domain example)

在这种架构中,一个链接可以处理多个域。例如,让我们考虑一个具有两个带 TrustZone 的 ARM Cortex-M33 核心的 SoC:核心 A 和 B(参见上面示例的插图)。系统中有四个域,因为每个核心都有安全和非安全域。如果 *核心 A 非安全*(A_NS)是根域,它有两个链接:一个到 *核心 A 安全*(A_NS-A_S),一个到 *核心 B 非安全*(A_NS-B_NS)。*B_NS* 域有一个链接,到 *核心 B 安全*(*B_NS-B_S*),以及到 *A_NS* 的后端。(In this architecture, a link can handle multiple domains. For example, let's consider an SoC with two ARM Cortex-M33 cores with TrustZone: cores A and B (see the example illustrated above). There are four domains in the system, as each core has both a Secure and a Nonsecure domain. If *core A nonsecure* (A_NS) is the root domain, it has two links: one to *core A secure* (A_NS-A_S) and one to *core B nonsecure* (A_NS-B_NS). *B_NS* domain has one link, to *core B secure* *B_NS-B_S*), and a backend to *A_NS*.)

In case of modules which are multi-instance and instances are widely used
across the system enabling logs will lead to flooding. The logger provides the tools
which can be used to provide filtering on instance level rather than module
level. In that case logging can be enabled for particular instance.

In order to use instance level filtering following steps must be performed:

- a pointer to specific logging structure is declared in instance structure.
  :c:macro:`LOG_INSTANCE_PTR_DECLARE` is used for that.

.. code-block:: c

   #include <zephyr/logging/log_instance.h>

   struct foo_object {
   	LOG_INSTANCE_PTR_DECLARE(log);
   	uint32_t id;
   }

- module must provide macro for instantiation. In that macro, logging instance
  is registered and log instance pointer is initialized in the object structure.

.. code-block:: c

   #define FOO_OBJECT_DEFINE(_name)                             \
   	LOG_INSTANCE_REGISTER(foo, _name, CONFIG_FOO_LOG_LEVEL) \
   	struct foo_object _name = {                             \
   		LOG_INSTANCE_PTR_INIT(log, foo, _name)          \
   	}

Note that when logging is disabled logging instance and pointer to that instance
are not created.

In order to use the instance logging API in a source file, a compile-time log
level must be set using :c:macro:`LOG_LEVEL_SET`.

.. code-block:: c

   LOG_LEVEL_SET(CONFIG_FOO_LOG_LEVEL);

   void foo_init(foo_object *f)
   {
   	LOG_INST_INF(f->log, "Initialized.");
   }

In order to use the instance logging API in a header file, a compile-time log
level must be set using :c:macro:`LOG_LEVEL_SET`.

.. code-block:: c

   static inline void foo_init(foo_object *f)
   {
   	LOG_LEVEL_SET(CONFIG_FOO_LOG_LEVEL);

   	LOG_INST_INF(f->log, "Initialized.");
   }

Controlling the logging
=======================

By default, logging processing in deferred mode is handled internally by the
dedicated task which starts automatically. However, it might not be available
if multithreading is disabled. It can also be disabled by unsetting
:kconfig:option:`CONFIG_LOG_PROCESS_TRIGGER_THRESHOLD`. In that case, logging can
be controlled using the API defined in :zephyr_file:`include/zephyr/logging/log_ctrl.h`.
Logging must be initialized before it can be used. Optionally, the user can provide
a function which returns the timestamp value. If not provided, :c:macro:`k_cycle_get`
or :c:macro:`k_cycle_get_32` is used for timestamping.
The :c:func:`log_process` function is used to trigger processing of one log
message (if pending), and returns true if there are more messages pending.
However, it is recommended to use macro wrappers (:c:macro:`LOG_INIT` and
:c:macro:`LOG_PROCESS`) which handle the case where logging is disabled.

The following snippet shows how logging can be processed in simple forever loop.

.. code-block:: c

   #include <zephyr/logging/log_ctrl.h>

   int main(void)
   {
   	LOG_INIT();
   	/* If multithreading is enabled provide thread id to the logging. */
   	log_thread_set(k_current_get());

   	while (1) {
   		if (LOG_PROCESS() == false) {
   			/* sleep */
   		}
   	}
   }

If logs are processed from a thread (user or internal) then it is possible to enable
a feature which will wake up processing thread when certain amount of log messages are
buffered (see :kconfig:option:`CONFIG_LOG_PROCESS_TRIGGER_THRESHOLD`).

.. _logging_ratelimited:

Rate-limited logging
********************

Rate-limited logging macros provide a way to prevent log flooding when messages are
generated frequently. These macros ensure that log messages are not output more
frequently than a specified interval, similar to Linux's ``printk_ratelimited``
functionality.

The rate-limited logging system provides two types of macros:

**Convenience macros (using default rate):**
- :c:macro:`LOG_ERR_RATELIMIT` - Rate-limited error messages
- :c:macro:`LOG_WRN_RATELIMIT` - Rate-limited warning messages
- :c:macro:`LOG_INF_RATELIMIT` - Rate-limited info messages
- :c:macro:`LOG_DBG_RATELIMIT` - Rate-limited debug messages
- :c:macro:`LOG_HEXDUMP_ERR_RATELIMIT` - Rate-limited error hexdump
- :c:macro:`LOG_HEXDUMP_WRN_RATELIMIT` - Rate-limited warning hexdump
- :c:macro:`LOG_HEXDUMP_INF_RATELIMIT` - Rate-limited info hexdump
- :c:macro:`LOG_HEXDUMP_DBG_RATELIMIT` - Rate-limited debug hexdump

**Explicit rate macros (with custom rate):**
- :c:macro:`LOG_ERR_RATELIMIT_RATE` - Rate-limited error messages with custom rate
- :c:macro:`LOG_WRN_RATELIMIT_RATE` - Rate-limited warning messages with custom rate
- :c:macro:`LOG_INF_RATELIMIT_RATE` - Rate-limited info messages with custom rate
- :c:macro:`LOG_DBG_RATELIMIT_RATE` - Rate-limited debug messages with custom rate
- :c:macro:`LOG_HEXDUMP_ERR_RATELIMIT_RATE` - Rate-limited error hexdump with custom rate
- :c:macro:`LOG_HEXDUMP_WRN_RATELIMIT_RATE` - Rate-limited warning hexdump with custom rate
- :c:macro:`LOG_HEXDUMP_INF_RATELIMIT_RATE` - Rate-limited info hexdump with custom rate
- :c:macro:`LOG_HEXDUMP_DBG_RATELIMIT_RATE` - Rate-limited debug hexdump with custom rate

The convenience macros use the default rate specified by :kconfig:option:`CONFIG_LOG_RATELIMIT_INTERVAL_MS`
(5000ms by default). The explicit rate macros take a rate parameter (in milliseconds) that specifies
the minimum interval between log messages. The rate limiting is per-macro-call-site, meaning
that each unique call to a rate-limited macro has its own independent rate limit.

Example usage:

.. code-block:: c

    #include <zephyr/logging/log.h>
    #include <zephyr/kernel.h>

    LOG_MODULE_REGISTER(my_module, CONFIG_LOG_DEFAULT_LEVEL);

    void process_data(void)
    {
        /* Convenience macros using default rate (CONFIG_LOG_RATELIMIT_INTERVAL_MS) */
        LOG_WRN_RATELIMIT("Data processing warning: %d", error_code);
        LOG_ERR_RATELIMIT("Critical error occurred: %s", error_msg);
        LOG_INF_RATELIMIT("Processing status: %d items", item_count);
        LOG_HEXDUMP_WRN_RATELIMIT(data_buffer, data_len, "Data buffer:");

        /* Explicit rate macros with custom intervals */
        LOG_WRN_RATELIMIT_RATE(1000, "Fast rate warning: %d", error_code);
        LOG_ERR_RATELIMIT_RATE(30000, "Slow rate error: %s", error_msg);
        LOG_INF_RATELIMIT_RATE(2000, "Custom rate status: %d items", item_count);
        LOG_HEXDUMP_ERR_RATELIMIT_RATE(5000, data_buffer, data_len, "Error data:");
    }

Rate-limited logging is particularly useful for:

- Error conditions that might occur frequently but don't need to flood the logs
- Status updates in tight loops or high-frequency callbacks
- Debug information that could overwhelm the logging system
- Network or I/O operations that might fail repeatedly

Configuration
==============

Rate-limited logging can be configured using the following Kconfig options:

- :kconfig:option:`CONFIG_LOG_RATELIMIT` - Master switch to enable/disable rate-limited logging
- :kconfig:option:`CONFIG_LOG_RATELIMIT_INTERVAL_MS` - Default interval for convenience macros (5000ms)

When :kconfig:option:`CONFIG_LOG_RATELIMIT` is disabled, the behavior of rate-limited macros is controlled
by the :kconfig:option:`CONFIG_LOG_RATELIMIT_FALLBACK` choice:

- :kconfig:option:`CONFIG_LOG_RATELIMIT_FALLBACK_LOG` - All rate-limited macros behave as regular logging macros
- :kconfig:option:`CONFIG_LOG_RATELIMIT_FALLBACK_DROP` - All rate-limited macros expand to no-ops (default)

This allows you to control whether rate-limited log macros should always print or be completely
suppressed when rate limiting is not available.

The rate limiting is implemented using static variables and :c:func:`k_uptime_get_32`
to track the last log time for each call site.

.. _logging_panic:

Logging panic
*************

In case of error condition system usually can no longer rely on scheduler or
interrupts. In that situation deferred log message processing is not an option.
Logger controlling API provides a function for entering into panic mode
(:c:func:`log_panic`) which should be called in such situation.

When :c:func:`log_panic` is called, _panic_ notification is sent to all active
backends. Once all backends are notified, all buffered messages are flushed. Since
that moment all logs are processed in a blocking way.

.. _logging_printk:

Printk
******

Typically, logging and :c:func:`printk` use the same output, which they compete
for. This can lead to issues if the output does not support preemption but it may
also result in corrupted output because logging data is interleaved with printk
data. However, it is possible to redirect printk messages to the
logging subsystem by enabling :kconfig:option:`CONFIG_LOG_PRINTK`. In that case,
printk entries are treated as log messages with level 0 (they cannot be disabled).
When enabled, logging manages the output so there is no interleaving. However,
in deferred mode the printk behaviour is changed since the output is delayed
until the logging thread processes the data. :kconfig:option:`CONFIG_LOG_PRINTK`
is enabled by default.


.. _log_architecture:

Architecture
************

Logging consists of 3 main parts:

- Frontend
- Core
- Backends

Log message is generated by a source of logging which can be a module or
instance of a module.

Default Frontend
================

Default frontend is engaged when the logging API is called in a source of logging (e.g.
:c:macro:`LOG_INF`) and is responsible for filtering a message (compile and run
time), allocating a buffer for the message, creating the message and committing that
message. Since the logging API can be called in an interrupt, the frontend is optimized
to log the message as fast as possible.

Log message
-----------

A log message contains a message descriptor (source, domain and level), timestamp,
formatted string details (see :ref:`cbprintf_packaging`) and optional data.
Log messages are stored in a continuous block of memory.
Memory is allocated from a circular packet buffer (:ref:`mpsc_pbuf`), which has
a few consequences:

 * Each message is a self-contained, continuous block of memory thus it is suited
   for copying the message (e.g. for offline processing).
 * Messages must be sequentially freed. Backend processing is synchronous. Backend
   can make a copy for deferred processing.

A log message has following format:

+------------------+----------------------------------------------------+
| Message Header   | 2 bits: MPSC packet buffer header                  |
|                  +----------------------------------------------------+
|                  | 1 bit: Trace/Log message flag                      |
|                  +----------------------------------------------------+
|                  | 3 bits: Domain ID                                  |
|                  +----------------------------------------------------+
|                  | 3 bits: Level                                      |
|                  +----------------------------------------------------+
|                  | 10 bits: Cbprintf Package Length                   |
|                  +----------------------------------------------------+
|                  | 12 bits: Data length                               |
|                  +----------------------------------------------------+
|                  | 1 bit: Reserved                                    |
|                  +----------------------------------------------------+
|                  | pointer: Pointer to the source descriptor [#l0]_   |
|                  +----------------------------------------------------+
|                  | 32 or 64 bits: Timestamp [#l0]_                    |
|                  +----------------------------------------------------+
|                  | Optional padding [#l1]_                            |
+------------------+----------------------------------------------------+
| Cbprintf         | Header                                             |
|                  +----------------------------------------------------+
| | package        | Arguments                                          |
| | (optional)     +----------------------------------------------------+
|                  | Appended strings                                   |
+------------------+----------------------------------------------------+
| Hexdump data (optional)                                               |
+------------------+----------------------------------------------------+
| Alignment padding (optional)                                          |
+------------------+----------------------------------------------------+

.. rubric:: Footnotes

.. [#l0] Depending on the platform and the timestamp size fields may be swapped.
.. [#l1] It may be required for cbprintf package alignment

Log message allocation
----------------------

It may happen that the frontend cannot allocate a message. This happens if the
system is generating more log messages than it can process in certain time
frame. There are two strategies to handle that case:

- No overflow - the new log is dropped if space for a message cannot be allocated.
- Overflow - the oldest pending messages are freed, until the new message can be
  allocated. Enabled by :kconfig:option:`CONFIG_LOG_MODE_OVERFLOW`. Note that it degrades
  performance thus it is recommended to adjust buffer size and amount of enabled
  logs to limit dropping.

.. _logging_runtime_filtering:

Run-time filtering
------------------

If run-time filtering is enabled, then for each source of logging a filter
structure in RAM is declared. Such filter is using 32 bits divided into ten 3
bit slots. Except *slot 0*, each slot stores current filter for one backend in
the system. *Slot 0* (bits 0-2) is used to aggregate maximal filter setting for
given source of logging. Aggregate slot determines if log message is created
for given entry since it indicates if there is at least one backend expecting
that log entry. Backend slots are examined when message is processed by the core
to determine if message is accepted by the given backend. Contrary to compile
time filtering, binary footprint is increased because logs are compiled in.

In the example below backend 1 is set to receive errors (*slot 1*) and backend
2 up to info level (*slot 2*). Slots 3-9 are not used. Aggregated filter
(*slot 0*) is set to info level and up to this level message from that
particular source will be buffered.

+------+------+------+------+-----+------+
|slot 0|slot 1|slot 2|slot 3| ... |slot 9|
+------+------+------+------+-----+------+
| INF  | ERR  | INF  | OFF  | ... | OFF  |
+------+------+------+------+-----+------+

.. _log_frontend:

Custom Frontend
===============

Custom frontend is enabled using :kconfig:option:`CONFIG_LOG_FRONTEND`. Logs are directed
to functions declared in :zephyr_file:`include/zephyr/logging/log_frontend.h`.
If option :kconfig:option:`CONFIG_LOG_FRONTEND_ONLY` is enabled then log message is not
created and no backend is handled. Otherwise, custom frontend can coexist with
backends.

In some cases, logs need to be redirected at the macro level. For these cases,
:kconfig:option:`CONFIG_LOG_CUSTOM_HEADER` can be used to inject an application provided
header named :file:`zephyr_custom_log.h` at the end of :zephyr_file:`include/zephyr/logging/log.h`.

Frontend using ARM Coresight STM (System Trace Macrocell)
---------------------------------------------------------

For more details about logging using ARM Coresight STM see :ref:`logging_cs_stm`.

.. _logging_strings:

Logging strings
===============

String arguments are handled by :ref:`cbprintf_packaging`. See
:ref:`cbprintf_packaging_limitations` for limitations and recommendations.

Multi-domain support
====================

More complex systems can consist of multiple domains where each domain is an
independent binary. Examples of domains are a core in a multicore SoC or one
of the binaries (Secure or Nonsecure) on an ARM TrustZone core.

Tracing and debugging on a multi-domain system is more complex and requires an efficient logging
system. Two approaches can be used to structure this logging system:

* Log inside each domain independently.
  This option is not always possible as it requires that each domain has an available backend
  (for example, UART). This approach can also be troublesome to use and not scalable,
  as logs are presented on independent outputs.
* Use a multi-domain logging system where log messages from each domain end up in one root domain,
  where they are processed exactly as in a single domain case.
  In this approach, log messages are passed between domains using a connection between domains
  created from the backend on one side and linked to the other.

  The Log link is an interface introduced in this multi-domain approach. The Log link is
  responsible for receiving any log message from another domain, creating a copy, and
  putting that local log message copy (including remote data) into the message queue.
  This specific log link implementation matches the complementary backend implementation
  to allow log messages exchange and logger control like configuring filtering, getting log
  source names, and so on.

There are three types of domains in a multi-domain system:

* The *end domain* has the logging core implementation and a cross-domain
  backend. It can also have other backends in parallel.
* The *relay domain* has one or more links to other domains but does not
  have backends that output logs to the user. It has a cross-domain backend either to
  another relay or to the root domain.
* The *root domain* has one or multiple links and a backend that outputs logs
  to the user.

See the following image for an example of a multi-domain setup:

.. figure:: images/multidomain.png

    Multi-domain example

In this architecture, a link can handle multiple domains.
For example, let's consider an SoC with two ARM Cortex-M33 cores with TrustZone: cores A and B (see
the example illustrated above). There are four domains in the system, as
each core has both a Secure and a Nonsecure domain. If *core A nonsecure* (A_NS) is the
root domain, it has two links: one to *core A secure* (A_NS-A_S) and one to
*core B nonsecure* (A_NS-B_NS). *B_NS* domain has one link, to *core B secure*
在这种架构中,一个链接可以处理多个域。例如,让我们考虑一个具有两个带 TrustZone 的 ARM Cortex-M33 核心的 SoC:核心 A 和 B(参见上面示例的插图)。系统中有四个域,因为每个核心都有安全和非安全域。如果 *核心 A 非安全*(A_NS)是根域,它有两个链接:一个到 *核心 A 安全*(A_NS-A_S),一个到 *核心 B 非安全*(A_NS-B_NS)。*B_NS* 域有一个链接,到 *核心 B 安全*(*B_NS-B_S*),以及到 *A_NS* 的后端。(In this architecture, a link can handle multiple domains. For example, let's consider an SoC with two ARM Cortex-M33 cores with TrustZone: cores A and B (see the example illustrated above). There are four domains in the system, as each core has both a Secure and a Nonsecure domain. If *core A nonsecure* (A_NS) is the root domain, it has two links: one to *core A secure* (A_NS-A_S) and one to *core B nonsecure* (A_NS-B_NS). *B_NS* domain has one link, to *core B secure* *B_NS-B_S*), and a backend to *A_NS*.)

由于在所有实例中都有一个标准的日志记录子系统,因此始终可以拥有多个后端并同时向它们输出消息。上图中虚线所示的 *B_NS* 域上的 UART 后端就是一个例子。(Since in all instances there is a standard logging subsystem, it is always possible to have multiple backends and simultaneously output messages to them. An example of this is shown in the illustration above as a dotted UART backend on the *B_NS* domain.)

域 ID (Domain ID)
-----------------

每条日志消息的源可以通过头中的以下字段标识:``source_id`` 和 ``domain_id``。(The source of each log message can be identified by the following fields in the header: ``source_id`` and ``domain_id``.)

分配给 ``domain_id`` 的值是相对的。每当域创建日志消息时,它都将其 ``domain_id`` 设置为 ``0``。当消息跨越域时,``domain_id`` 会发生变化,因为它会增加链接偏移量。链接偏移量在初始化期间分配,其中日志记录器核心迭代所有已注册的链接并分配偏移量。(The value assigned to the ``domain_id`` is relative. Whenever a domain creates a log message, it sets its ``domain_id`` to ``0``. When a message crosses the domain, ``domain_id`` changes as it is increased by the link offset. The link offset is assigned during the initialization, where the logger core is iterating over all the registered links and assigned offsets.)

第一个链接的偏移量设置为 1。以下偏移量等于前一个链接偏移量加上前一个链接中的域数。(The first link has the offset set to 1. The following offset equals the previous link offset plus the number of domains in the previous link.)

下面显示了以下示例,其中显示了为每个域分配的 ``domain_ids``:(The following example is shown below, where the assigned ``domain_ids`` are shown for each domain:)

.. figure:: images/domain_ids.png

    域 ID 分配示例 (Domain IDs assigning example)

让我们考虑在 *B_S* 域上创建的日志消息:(Let's consider a log message created on the *B_S* domain:)

1. 最初,它的 ``domain_id`` 设置为 ``0``。(Initially, it has its ``domain_id`` set to ``0``.)
#. 当 *B_NS-B_S* 链接接收到消息时,它通过添加 *B_NS-B_S* 偏移量将 ``domain_id`` 增加到 ``1``。(When the *B_NS-B_S* link receives the message, it increases the ``domain_id`` to ``1`` by adding the *B_NS-B_S* offset.)
#. 消息传递到 *A_NS*。(The message is passed to *A_NS*.)
#. 当 *A_NS-B_NS* 链接接收到消息时,它将偏移量(``2``)添加到 ``domain_id``。消息最终将 ``domain_id`` 设置为 ``3``,这唯一标识了消息发起者。(When the *A_NS-B_NS* link receives the message, it adds the offset (``2``) to the ``domain_id``. The message ends up with the ``domain_id`` set to ``3``, which uniquely identifies the message originator.)

跨域日志消息 (Cross-domain log message)
---------------------------------------

在大多数情况下,每个域的地址空间都是唯一的,一个域不能直接访问另一个域中的数据。因此,后端可以在将消息传递到另一个域之前部分处理该消息。部分处理可以包括将字符串包转换为 *完全自包含* 版本(将只读字符串复制到包体)。(In most cases, the address space of each domain is unique, and one domain cannot access directly the data in another domain. For this reason, the backend can partially process the message before it is passed to another domain. Partial processing can include converting a string package to a *fully self-contained* version (copying read-only strings to the package body).)

每个域在频率和偏移量方面可以有不同的时间戳源。日志记录不执行任何时间戳转换。(Each domain can have a different timestamp source in terms of frequency and offset. Logging does not perform any timestamp conversion.)

运行时过滤 (Runtime filtering)
------------------------------

在单域情况下,每个日志源对于系统中的每个后端都有一个专用的运行时过滤变量。在多域情况下,日志消息的发起者不知道根域中的后端数量。(In the single-domain case, each log source has a dedicated variable with runtime filtering for each backend in the system. In the multi-domain case, the originator of the log message is not aware of the number of backends in the root domain.)

因此,为了在多个域中过滤日志,每个源在通往根域的每个域中都需要运行时过滤设置。由于在编译期间不知道其他域中的源数量,因此远程源的运行时过滤必须使用动态分配的内存(每个源一个字)。当根域中的后端更改来自远程域的模块的过滤时,本地过滤器会更新。更新后,检查聚合过滤器(来自所有本地后端的最大值),如果更改,则通知远程域此更改。使用这种方法,运行时过滤在多域和单域场景中的工作方式相同。(As such, to filter logs in multiple domains, each source requires a runtime filtering setting in each domain on the way to the root domain. As the number of sources in other domains is not known during the compilation, the runtime filtering of remote sources must use dynamically allocated memory (one word per source). When a backend in the root domain changes the filtering of the module from a remote domain, the local filter is updated. After the update, the aggregated filter (the maximum from all the local backends) is checked and, if changed, the remote domain is informed about this change. With this approach, the runtime filtering works identically in both multi-domain and single-domain scenarios.)

消息排序 (Message ordering)
---------------------------

日志记录不提供任何用于跨多个域同步时间戳的机制:(Logging does not provide any mechanism for synchronizing timestamps across multiple domains:)

* 如果域具有不同的时间戳源,则消息将按照到达根域中的缓冲区的顺序进行处理。(If domains have different timestamp sources, messages will be processed in the order of arrival to the buffer in the root domain.)
* 如果域具有相同的时间戳源,或者如果存在重新计算时间戳的带外机制,则有 2 个选项:(If domains have the same timestamp source or if there is an out-of-bound mechanism that recalculates timestamps, there are 2 options:)

  * 消息在到达根域中的缓冲区时被处理。消息是无序的,但可以由主机按时间戳排序,因为时间戳指示消息生成的时间。(Messages are processed as they arrive in the buffer in the root domain. Messages are unordered but they can be sorted by the host as the timestamp indicates the time of the message generation.)
  * 链接具有专用缓冲区。在处理期间,检查每个缓冲区的头部,首先处理最旧的消息。(Links have dedicated buffers. During processing, the head of each buffer is checked and the oldest message is processed first.)

    使用这种方法,可以以次优的内存利用率(因为缓冲区不共享)和增加的处理延迟(请参阅 :kconfig:option:`CONFIG_LOG_PROCESSING_LATENCY_US`)为代价来维护消息的顺序。(With this approach, it is possible to maintain the order of the messages at the cost of a suboptimal memory utilization (since the buffer is not shared) and increased processing latency (see :kconfig:option:`CONFIG_LOG_PROCESSING_LATENCY_US`).)

日志记录后端 (Logging backends)
================================

使用 :c:macro:`LOG_BACKEND_DEFINE` 注册日志记录后端。该宏在专用内存部分中创建一个实例。后端可以动态启用(:c:func:`log_backend_enable`)和禁用。当启用 :ref:`logging_runtime_filtering` 时,可以使用 :c:func:`log_filter_set` 动态更改给定后端的模块日志过滤。模块由源 ID 和域 ID 标识。如果源名称已知,可以通过迭代所有已注册的源来检索源 ID。(Logging backends are registered using :c:macro:`LOG_BACKEND_DEFINE`. The macro creates an instance in the dedicated memory section. Backends can be dynamically enabled (:c:func:`log_backend_enable`) and disabled. When :ref:`logging_runtime_filtering` is enabled, :c:func:`log_filter_set` can be used to dynamically change filtering of a module logs for given backend. Module is identified by source ID and domain ID. Source ID can be retrieved if source name is known by iterating through all registered sources.)

日志记录支持最多 9 个并发后端。日志消息在处理阶段传递给每个后端。此外,当日志记录进入恐慌模式时,会使用 :c:func:`log_backend_panic` 通知后端。在该调用时,后端应切换到同步、无中断操作,或者如果不支持则关闭自己。有时,日志记录可能会使用 :c:func:`log_backend_dropped` 通知后端有关丢弃的消息数。消息处理 API 是特定于版本的。(Logging supports up to 9 concurrent backends. Log message is passed to the each backend in processing phase. Additionally, backend is notified when logging enter panic mode with :c:func:`log_backend_panic`. On that call backend should switch to synchronous, interrupt-less operation or shut down itself if that is not supported. Occasionally, logging may inform backend about number of dropped messages with :c:func:`log_backend_dropped`. Message processing API is version specific.)

:c:func:`log_backend_msg_process` 用于处理消息。它对于标准和十六进制转储消息是通用的,因为日志消息包含带参数和数据的字符串。它对于延迟和立即日志记录也是通用的。(:c:func:`log_backend_msg_process` is used for processing message. It is common for standard and hexdump messages because log message hold string with arguments and data. It is also common for deferred and immediate logging.)

.. _log_output:

消息格式化 (Message formatting)
--------------------------------

日志记录提供了一组函数,后端可以使用这些函数来格式化消息。辅助函数在 :zephyr_file:`include/zephyr/logging/log_output.h` 中可用。(Logging provides set of function that can be used by the backend to format a message. Helper functions are available in :zephyr_file:`include/zephyr/logging/log_output.h`.)

使用 :c:func:`log_output_msg_process` 格式化的示例消息。(Example message formatted using :c:func:`log_output_msg_process`.)

.. code-block:: console

   [00:00:00.000,274] <info> sample_instance.inst1: logging message


.. _logging_guide_dictionary:

基于字典的日志记录 (Dictionary-based Logging)
==============================================

基于字典的日志记录以二进制格式输出日志消息,而不是人类可读的文本。这种二进制格式以其原生存储格式对格式化字符串的参数进行编码,这可以比其文本等效项更紧凑。对于静态定义的字符串(包括格式字符串和任何字符串参数),编码对 ELF 文件的引用,而不是整个字符串。在构建时创建的字典包含这些引用与实际字符串之间的映射。这允许离线解析器从字典中获取字符串以解析日志消息。在某些场景下,这种二进制格式允许更紧凑的日志消息表示。但是,这需要使用离线解析器,并且不像基于文本的日志消息那样直观易用。(Dictionary-based logging, instead of human readable texts, outputs the log messages in binary format. This binary format encodes arguments to formatted strings in their native storage formats which can be more compact than their text equivalents. For statically defined strings (including the format strings and any string arguments), references to the ELF file are encoded instead of the whole strings. A dictionary created at build time contains the mappings between these references and the actual strings. This allows the offline parser to obtain the strings from the dictionary to parse the log messages. This binary format allows a more compact representation of log messages in certain scenarios. However, this requires the use of an offline parser and is not as intuitive to use as text-based log messages.)

请注意,Python 的 ``struct`` 模块不支持 ``long double``。因此,带有 ``long double`` 的日志消息将不会显示正确的值。(Note that ``long double`` is not supported by Python's ``struct`` module. Therefore, log messages with ``long double`` will not display the correct values.)


配置 (Configuration)
--------------------

以下是与基于字典的日志记录相关的 kconfig 选项:(Here are kconfig options related to dictionary-based logging:)

- :kconfig:option:`CONFIG_LOG_DICTIONARY_SUPPORT` 启用基于字典的日志记录支持。这应该由需要它的后端选择。(:kconfig:option:`CONFIG_LOG_DICTIONARY_SUPPORT` enables dictionary-based logging support. This should be selected by the backends which require it.)

- UART 后端可用于基于字典的日志记录。以下是 UART 后端的其他配置:(The UART backend can be used for dictionary-based logging. These are additional config for the UART backend:)

  - :kconfig:option:`CONFIG_LOG_BACKEND_UART_OUTPUT_DICTIONARY_HEX` 告诉 UART 后端为基于字典的日志记录输出十六进制字符。当需要通过终端和控制台手动捕获日志数据时,这很有用。(:kconfig:option:`CONFIG_LOG_BACKEND_UART_OUTPUT_DICTIONARY_HEX` tells the UART backend to output hexadecimal characters for dictionary based logging. This is useful when the log data needs to be captured manually via terminals and consoles.)

  - :kconfig:option:`CONFIG_LOG_BACKEND_UART_OUTPUT_DICTIONARY_BIN` 告诉 UART 后端输出二进制数据。(:kconfig:option:`CONFIG_LOG_BACKEND_UART_OUTPUT_DICTIONARY_BIN` tells the UART backend to output binary data.)


用法 (Usage)
------------

当通过启用相关的日志记录后端启用基于字典的日志记录时,将在构建目录中创建一个名为 :file:`log_dictionary.json` 的 JSON 数据库文件。此数据库文件包含解析器正确解析日志数据所需的信息。请注意,此数据库文件仅适用于同一构建,不能用于任何其他构建。(When dictionary-based logging is enabled via enabling related logging backends, a JSON database file, named :file:`log_dictionary.json`, will be created in the build directory. This database file contains information for the parser to correctly parse the log data. Note that this database file only works with the same build, and cannot be used for any other builds.)

要使用日志解析器:(To use the log parser:)

.. code-block:: console

  ./scripts/logging/dictionary/log_parser.py <build dir>/log_dictionary.json <log data file>

解析器需要两个必需参数,第一个是 JSON 数据库文件的完整路径,第二个是包含日志数据的文件。如果日志数据文件包含十六进制字符(例如当 ``CONFIG_LOG_BACKEND_UART_OUTPUT_DICTIONARY_HEX=y`` 时),请在末尾添加可选参数 ``--hex``。这告诉解析器在解析之前将十六进制字符转换为二进制。(The parser takes two required arguments, where the first one is the full path to the JSON database file, and the second part is the file containing log data. Add an optional argument ``--hex`` to the end if the log data file contains hexadecimal characters (e.g. when ``CONFIG_LOG_BACKEND_UART_OUTPUT_DICTIONARY_HEX=y``). This tells the parser to convert the hexadecimal characters to binary before parsing.)

请参阅 :zephyr:code-sample:`logging-dictionary` 示例以了解有关如何使用日志解析器的更多信息。(Please refer to the :zephyr:code-sample:`logging-dictionary` sample to learn more on how to use the log parser.)


建议和限制 (Recommendations and limitations)
*********************************************

有以下建议:(The are following recommendations:)

建议和限制 (Recommendations and limitations)
*********************************************

有以下建议:(The are following recommendations:)

* 启用 :kconfig:option:`CONFIG_LOG_SPEED` 以略微加快延迟日志记录,代价是增加图像大小。(Enable :kconfig:option:`CONFIG_LOG_SPEED` to slightly speed up deferred logging at the cost of slight increase in memory footprint.)
* 建议使用支持 C11 ``_Generic`` 关键字的编译器。如果没有它,日志记录性能会显著下降。请参阅 :ref:`cbprintf_packaging`。(Compiler with C11 ``_Generic`` keyword support is recommended. Logging performance is significantly degraded without it. See :ref:`cbprintf_packaging`.)
* 建议在将指针与 ``%s`` 格式说明符一起使用且它指向常量字符串时,将指针强制转换为 ``const char *``。(It is recommended to cast pointer to ``const char *`` when it is used with ``%s`` format specifier and it points to a constant string.)
* 建议在将指针与 ``%s`` 格式说明符一起使用且它指向瞬态字符串时,将指针强制转换为 ``char *``。(It is recommended to cast pointer to ``char *`` when it is used with ``%s`` format specifier and it points to a transient string.)
* 当字符指针与 ``%p`` 格式说明符一起使用时,需要将字符指针强制转换为非字符指针(例如 ``void *``)。(It is required to cast a character pointer to non character pointer (e.g., ``void *``) when it is used with ``%p`` format specifier.)

.. code-block:: c

   LOG_WRN("%s", str);
   LOG_WRN("%p", (void *)str);

有以下限制:(There are following limitations:)

* 日志记录不支持带宽度的字符串格式说明符(例如 ``%.*s`` 或 ``%8s``)。这是因为格式字符串内容不用于构建日志消息,只使用参数类型。(Logging does not support string format specifier with width (e.g., ``%.*s`` or ``%8s``). That is because format string content is not used to build a log message, only argument types.)

基准测试 (Benchmark)
********************

在 ``qemu_x86`` 上执行的 :zephyr_file:`tests/subsys/logging/log_benchmark` 的基准测试数字。这是一个粗略的比较,旨在提供一般概述。(Benchmark numbers from :zephyr_file:`tests/subsys/logging/log_benchmark` performed on ``qemu_x86``. It is a rough comparison to give a general overview.)

+--------------------------------------------+------------------+
| 特性 (Feature)                              |                  |
+============================================+==================+
| 内核日志记录                                | 7us [#f0]_/11us  |
| (Kernel logging)                           |                  |
+--------------------------------------------+------------------+
| 用户日志记录                                | 13us             |
| (User logging)                             |                  |
+--------------------------------------------+------------------+
| 具有覆盖的内核日志记录                       | 10us [#f0]_/15us |
| (kernel logging with overwrite)            |                  |
+--------------------------------------------+------------------+
| 记录瞬态字符串                              | 42us             |
| (Logging transient string)                 |                  |
+--------------------------------------------+------------------+
| 从用户记录瞬态字符串                        | 50us             |
| (Logging transient string from user)       |                  |
+--------------------------------------------+------------------+
| 内存利用率 [#f1]_                          | 518              |
| (Memory utilization [#f1]_)                |                  |
+--------------------------------------------+------------------+
| 内存占用(测试)[#f2]_                       | 2k               |
| (Memory footprint (test) [#f2]_)           |                  |
+--------------------------------------------+------------------+
| 内存占用(应用程序)[#f3]_                   | 3.5k             |
| (Memory footprint (application) [#f3]_)    |                  |
+--------------------------------------------+------------------+
| 消息占用 [#f4]_                            | 47 [#f0]_/32     |
| (Message footprint [#f4]_)                 | 字节 (bytes)     |
+--------------------------------------------+------------------+

.. rubric:: 基准测试详情 (Benchmark details)

.. [#f0] :kconfig:option:`CONFIG_LOG_SPEED` 已启用。(:kconfig:option:`CONFIG_LOG_SPEED` enabled.)

.. [#f1] 具有各种参数数量的日志消息数,适合专用于日志记录的 2048 字节。(Number of log messages with various number of arguments that fits in 2048 bytes dedicated for logging.)

.. [#f2] :zephyr_file:`tests/subsys/logging/log_benchmark` 中的日志记录子系统内存占用,其中不使用过滤和格式化功能。(Logging subsystem memory footprint in :zephyr_file:`tests/subsys/logging/log_benchmark` where filtering and formatting features are not used.)

.. [#f3] :zephyr_file:`samples/subsys/logging/logger` 中的日志记录子系统内存占用。(Logging subsystem memory footprint in :zephyr_file:`samples/subsys/logging/logger`.)

.. [#f4] 在 ``Cortex M3`` 上具有 2 个参数的日志消息的平均大小(不包括字符串)。(Average size of a log message (excluding string) with 2 arguments on ``Cortex M3``)

栈使用 (Stack usage)
********************

启用日志记录时,它会影响使用日志记录 API 的上下文的栈使用。如果对栈进行了优化,可能会导致栈溢出。栈使用取决于模式和优化。它在不同平台之间也有很大差异。一般来说,当使用 :kconfig:option:`CONFIG_LOG_MODE_DEFERRED` 时,栈使用更小,因为日志记录仅限于创建和存储日志消息。当使用 :kconfig:option:`CONFIG_LOG_MODE_IMMEDIATE` 时,日志消息由后端处理,包括字符串格式化。在这种模式下,栈使用将取决于使用哪些后端。(When logging is enabled it impacts stack usage of the context that uses logging API. If stack is optimized it may lead to stack overflow. Stack usage depends on mode and optimization. It also significantly varies between platforms. In general, when :kconfig:option:`CONFIG_LOG_MODE_DEFERRED` is used stack usage is smaller since logging is limited to creating and storing log message. When :kconfig:option:`CONFIG_LOG_MODE_IMMEDIATE` is used then log message is processed by the backend which includes string formatting. In case of that mode, stack usage will depend on which backends are used.)

下面列出了一些平台对具有两个 ``整数`` 参数的日志消息的特性:(Some of the platforms characterization for log message with two ``integer`` arguments listed below:)

+---------------+----------+----------------------------+-----------+-----------------------------+
| 平台          | 延迟     | 延迟(无优化)                | 立即      | 立即(无优化)                 |
| (Platform)    |(Deferred)|(Deferred (no optimization))|(Immediate)|(Immediate (no optimization))|
+===============+==========+============================+===========+=============================+
| ARM Cortex-M3 | 40       | 152                        | 412       | 783                         |
+---------------+----------+----------------------------+-----------+-----------------------------+
| x86           | 12       | 224                        | 388       | 796                         |
+---------------+----------+----------------------------+-----------+-----------------------------+
| riscv32       | 24       | 208                        | 456       | 844                         |
+---------------+----------+----------------------------+-----------+-----------------------------+
| xtensa        | 72       | 336                        | 504       | 944                         |
+---------------+----------+----------------------------+-----------+-----------------------------+
| x86_64        | 32       | 528                        | 1088      | 1440                        |
+---------------+----------+----------------------------+-----------+-----------------------------+

使用 ARM Coresight STM 进行日志记录 (Logging using ARM Coresight STM)
**********************************************************************

有关在 NRF54H20 上使用 ARM Coresight STM 进行日志记录,请参阅 :ref:`logging_cs_stm`。(For logging on NRF54H20 using ARM Coresight STM see :ref:`logging_cs_stm`.)

API 参考 (API Reference)
*************************

日志记录器 API (Logger API)
============================

.. doxygengroup:: log_api

日志记录器控制 (Logger control)
================================

.. doxygengroup:: log_ctrl

日志消息 (Log message)
=======================

.. doxygengroup:: log_msg

日志记录器后端接口 (Logger backend interface)
==============================================

.. doxygengroup:: log_backend

日志记录器输出格式化 (Logger output formatting)
================================================

.. doxygengroup:: log_output

.. toctree::
   :maxdepth: 1

   cs_stm.rst
to have multiple backends and simultaneously output messages to them. An example of this is shown
in the illustration above as a dotted UART backend on the *B_NS* domain.

Domain ID
---------

The source of each log message can be identified by the following fields in the header:
``source_id`` and ``domain_id``.

The value assigned to the ``domain_id`` is relative. Whenever a domain creates a log message,
it sets its ``domain_id`` to ``0``.
When a message crosses the domain, ``domain_id`` changes as it is increased by the link offset.
The link offset is assigned during the initialization, where the logger core is iterating
over all the registered links and assigned offsets.

The first link has the offset set to 1.
The following offset equals the previous link offset plus the number of domains in the previous
link.

The following example is shown below, where
the assigned ``domain_ids`` are shown for each domain:

.. figure:: images/domain_ids.png

    Domain IDs assigning example

Let's consider a log message created on the *B_S* domain:

1. Initially, it has its ``domain_id`` set to ``0``.
#. When the *B_NS-B_S* link receives the message, it increases the ``domain_id``
   to ``1`` by adding the *B_NS-B_S* offset.
#. The message is passed to *A_NS*.
#. When the *A_NS-B_NS* link receives the message, it adds the offset (``2``) to the ``domain_id``.
   The message ends up with the ``domain_id`` set to ``3``, which uniquely identifies the message
   originator.

Cross-domain log message
------------------------

In most cases, the address space of each domain is unique, and one domain
cannot access directly the data in another domain. For this reason, the backend can
partially process the message before it is passed to another domain. Partial
processing can include converting a string package to a *fully self-contained*
version (copying read-only strings to the package body).

Each domain can have a different timestamp source in terms of frequency and
offset. Logging does not perform any timestamp conversion.

Runtime filtering
-----------------

In the single-domain case, each log source has a dedicated variable with runtime
filtering for each backend in the system. In the multi-domain case, the originator of
the log message is not aware of the number of backends in the root domain.

As such, to filter logs in multiple domains, each source requires a runtime
filtering setting in each domain on the way to the root domain. As the number of
sources in other domains is not known during the compilation, the runtime filtering
of remote sources must use dynamically allocated memory (one word per
source). When a backend in the root domain changes the filtering of the module from a
remote domain, the local filter is updated. After the update, the aggregated
filter (the maximum from all the local backends) is checked and, if changed, the remote domain is
informed about this change. With this approach, the runtime filtering works identically
in both multi-domain and single-domain scenarios.

Message ordering
----------------

Logging does not provide any mechanism for synchronizing timestamps across multiple
domains:

* If domains have different timestamp sources, messages will be
  processed in the order of arrival to the buffer in the root domain.
* If domains have the same timestamp source or if there is an out-of-bound mechanism that
  recalculates timestamps, there are 2 options:

  * Messages are processed as they arrive in the buffer in the root domain.
    Messages are unordered but they can be sorted by the host as the timestamp
    indicates the time of the message generation.
  * Links have dedicated buffers. During processing, the head of each buffer is checked
    and the oldest message is processed first.

    With this approach, it is possible to maintain the order of the messages at the cost
    of a suboptimal memory utilization (since the buffer is not shared) and increased processing
    latency (see :kconfig:option:`CONFIG_LOG_PROCESSING_LATENCY_US`).

Logging backends
================

Logging backends are registered using :c:macro:`LOG_BACKEND_DEFINE`. The macro
creates an instance in the dedicated memory section. Backends can be dynamically
enabled (:c:func:`log_backend_enable`) and disabled. When
:ref:`logging_runtime_filtering` is enabled, :c:func:`log_filter_set` can be used
to dynamically change filtering of a module logs for given backend. Module is
identified by source ID and domain ID. Source ID can be retrieved if source name
is known by iterating through all registered sources.

Logging supports up to 9 concurrent backends. Log message is passed to the
each backend in processing phase. Additionally, backend is notified when logging
enter panic mode with :c:func:`log_backend_panic`. On that call backend should
switch to synchronous, interrupt-less operation or shut down itself if that is
not supported.  Occasionally, logging may inform backend about number of dropped
messages with :c:func:`log_backend_dropped`. Message processing API is version
specific.

:c:func:`log_backend_msg_process` is used for processing message. It is common for
standard and hexdump messages because log message hold string with arguments
and data. It is also common for deferred and immediate logging.

.. _log_output:

Message formatting
------------------

Logging provides set of function that can be used by the backend to format a
message. Helper functions are available in :zephyr_file:`include/zephyr/logging/log_output.h`.

Example message formatted using :c:func:`log_output_msg_process`.

.. code-block:: console

   [00:00:00.000,274] <info> sample_instance.inst1: logging message


.. _logging_guide_dictionary:

Dictionary-based Logging
========================

Dictionary-based logging, instead of human readable texts, outputs the log
messages in binary format. This binary format encodes arguments to formatted
strings in their native storage formats which can be more compact than their
text equivalents. For statically defined strings (including the format
strings and any string arguments), references to the ELF file are encoded
instead of the whole strings. A dictionary created at build time contains
the mappings between these references and the actual strings. This allows
the offline parser to obtain the strings from the dictionary to parse
the log messages. This binary format allows a more compact representation
of log messages in certain scenarios. However, this requires the use of
an offline parser and is not as intuitive to use as text-based log messages.

Note that ``long double`` is not supported by Python's ``struct`` module.
Therefore, log messages with ``long double`` will not display the correct
values.


Configuration
-------------

Here are kconfig options related to dictionary-based logging:

- :kconfig:option:`CONFIG_LOG_DICTIONARY_SUPPORT` enables dictionary-based logging
  support. This should be selected by the backends which require it.

- The UART backend can be used for dictionary-based logging. These are
  additional config for the UART backend:

  - :kconfig:option:`CONFIG_LOG_BACKEND_UART_OUTPUT_DICTIONARY_HEX` tells
    the UART backend to output hexadecimal characters for dictionary based
    logging. This is useful when the log data needs to be captured manually
    via terminals and consoles.

  - :kconfig:option:`CONFIG_LOG_BACKEND_UART_OUTPUT_DICTIONARY_BIN` tells
    the UART backend to output binary data.


Usage
-----

When dictionary-based logging is enabled via enabling related logging backends,
a JSON database file, named :file:`log_dictionary.json`, will be created
in the build directory. This database file contains information for the parser
to correctly parse the log data. Note that this database file only works
with the same build, and cannot be used for any other builds.

To use the log parser:

.. code-block:: console

  ./scripts/logging/dictionary/log_parser.py <build dir>/log_dictionary.json <log data file>

The parser takes two required arguments, where the first one is the full path
to the JSON database file, and the second part is the file containing log data.
Add an optional argument ``--hex`` to the end if the log data file contains
hexadecimal characters
(e.g. when ``CONFIG_LOG_BACKEND_UART_OUTPUT_DICTIONARY_HEX=y``). This tells
the parser to convert the hexadecimal characters to binary before parsing.

Please refer to the :zephyr:code-sample:`logging-dictionary` sample to learn more on how to use
the log parser.


Recommendations and limitations
*******************************

The are following recommendations:

* Enable :kconfig:option:`CONFIG_LOG_SPEED` to slightly speed up deferred logging at the
  cost of slight increase in memory footprint.
* Compiler with C11 ``_Generic`` keyword support is recommended. Logging
  performance is significantly degraded without it. See :ref:`cbprintf_packaging`.
* It is recommended to cast pointer to ``const char *`` when it is used with ``%s``
  format specifier and it points to a constant string.
* It is recommended to cast pointer to ``char *`` when it is used with ``%s``
  format specifier and it points to a transient string.
* It is required to cast a character pointer to non character pointer
  (e.g., ``void *``) when it is used with ``%p`` format specifier.

.. code-block:: c

   LOG_WRN("%s", str);
   LOG_WRN("%p", (void *)str);

There are following limitations:

* Logging does not support string format specifier with width (e.g., ``%.*s`` or ``%8s``). That
  is because format string content is not used to build a log message, only argument types.

Benchmark
*********

Benchmark numbers from :zephyr_file:`tests/subsys/logging/log_benchmark` performed
on ``qemu_x86``. It is a rough comparison to give a general overview.

+--------------------------------------------+------------------+
| Feature                                    |                  |
+============================================+==================+
| Kernel logging                             | 7us [#f0]_/11us  |
|                                            |                  |
+--------------------------------------------+------------------+
| User logging                               | 13us             |
|                                            |                  |
+--------------------------------------------+------------------+
| kernel logging with overwrite              | 10us [#f0]_/15us |
+--------------------------------------------+------------------+
| Logging transient string                   | 42us             |
+--------------------------------------------+------------------+
| Logging transient string from user         | 50us             |
+--------------------------------------------+------------------+
| Memory utilization [#f1]_                  | 518              |
|                                            |                  |
+--------------------------------------------+------------------+
| Memory footprint (test) [#f2]_             | 2k               |
+--------------------------------------------+------------------+
| Memory footprint (application) [#f3]_      | 3.5k             |
+--------------------------------------------+------------------+
| Message footprint [#f4]_                   | 47 [#f0]_/32     |
|                                            | bytes            |
+--------------------------------------------+------------------+

.. rubric:: Benchmark details

.. [#f0] :kconfig:option:`CONFIG_LOG_SPEED` enabled.

.. [#f1] Number of log messages with various number of arguments that fits in 2048
  bytes dedicated for logging.

.. [#f2] Logging subsystem memory footprint in :zephyr_file:`tests/subsys/logging/log_benchmark`
  where filtering and formatting features are not used.

.. [#f3] Logging subsystem memory footprint in :zephyr_file:`samples/subsys/logging/logger`.

.. [#f4] Average size of a log message (excluding string) with 2 arguments on ``Cortex M3``

Stack usage
***********

When logging is enabled it impacts stack usage of the context that uses logging API. If stack
is optimized it may lead to stack overflow. Stack usage depends on mode and optimization. It
also significantly varies between platforms. In general, when :kconfig:option:`CONFIG_LOG_MODE_DEFERRED`
is used stack usage is smaller since logging is limited to creating and storing log message.
When :kconfig:option:`CONFIG_LOG_MODE_IMMEDIATE` is used then log message is processed by the backend
which includes string formatting. In case of that mode, stack usage will depend on which backends
are used.

Some of the platforms characterization for log message with two ``integer`` arguments listed below:

+---------------+----------+----------------------------+-----------+-----------------------------+
| Platform      | Deferred | Deferred (no optimization) | Immediate | Immediate (no optimization) |
+===============+==========+============================+===========+=============================+
| ARM Cortex-M3 | 40       | 152                        | 412       | 783                         |
+---------------+----------+----------------------------+-----------+-----------------------------+
| x86           | 12       | 224                        | 388       | 796                         |
+---------------+----------+----------------------------+-----------+-----------------------------+
| riscv32       | 24       | 208                        | 456       | 844                         |
+---------------+----------+----------------------------+-----------+-----------------------------+
| xtensa        | 72       | 336                        | 504       | 944                         |
+---------------+----------+----------------------------+-----------+-----------------------------+
| x86_64        | 32       | 528                        | 1088      | 1440                        |
+---------------+----------+----------------------------+-----------+-----------------------------+

Logging using ARM Coresight STM
*******************************

For logging on NRF54H20 using ARM Coresight STM see :ref:`logging_cs_stm`.

API Reference
*************

Logger API
==========

.. doxygengroup:: log_api

Logger control
==============

.. doxygengroup:: log_ctrl

Log message
===========

.. doxygengroup:: log_msg

Logger backend interface
========================

.. doxygengroup:: log_backend

Logger output formatting
========================

.. doxygengroup:: log_output

.. toctree::
   :maxdepth: 1

   cs_stm.rst
