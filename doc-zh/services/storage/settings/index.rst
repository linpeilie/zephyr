.. _settings_api:

设置 (Settings)
################

设置子系统为模块提供了一种存储持久性每设备配置和运行时状态的方法。使用 FCB、NVS、ZMS 或文件系统在通用 API 后面提供了多种存储实现。这些不同的实现为应用程序开发人员提供了选择合适存储介质的灵活性,甚至可以随着需求变化而更改。该子系统被各种 Zephyr 组件使用,并且可以由用户应用程序同时使用。(The settings subsystem gives modules a way to store persistent per-device configuration and runtime state. A variety of storage implementations are provided behind a common API using FCB, NVS, ZMS or a file system. These different implementations give the application developer flexibility to select an appropriate storage medium, and even change it later as needs change. This subsystem is used by various Zephyr components and can be used simultaneously by user applications.)

设置项存储为键值对字符串。按照约定,键可以由定义键的包和子树组织,例如键 ``id/serial`` 将定义包 ``id`` 的 ``serial`` 配置元素。(Settings items are stored as key-value pair strings. By convention, the keys can be organized by the package and subtree defining the key, for example the key ``id/serial`` would define the ``serial`` configuration element for the package ``id``.)

提供了便捷例程,用于将键值与字符串类型相互转换。(Convenience routines are provided for converting a key value to and from a string type.)

有关设置子系统的示例,请参阅 :zephyr:code-sample:`settings` 示例。(For an example of the settings subsystem refer to :zephyr:code-sample:`settings` sample.)

.. note::

   截至 Zephyr 4.1 版本,非文件系统存储的推荐后端是 :ref:`NVS <nvs_api>` 和 :ref:`ZMS <zms_api>`。(As of Zephyr release 4.1 the recommended backends for non-filesystem storage are :ref:`NVS <nvs_api>` and :ref:`ZMS <zms_api>`.)

处理程序 (Handlers)
********************

子树的设置处理程序实现一组处理程序函数。这些通过调用 :c:func:`settings_register()` 注册动态处理程序,或使用调用 :c:macro:`SETTINGS_STATIC_HANDLER_DEFINE()` 定义静态处理程序。(Settings handlers for subtree implement a set of handler functions. These are registered using a call to :c:func:`settings_register()` for dynamic handlers or defined using a call to :c:macro:`SETTINGS_STATIC_HANDLER_DEFINE()` for static handlers.)

**h_get**
    当使用 :c:func:`settings_runtime_get()` 从运行时后端按名称请求设置元素值时调用此函数。(This gets called when asking for a settings element value by its name using :c:func:`settings_runtime_get()` from the runtime backend.)

**h_set**
    当使用 :c:func:`settings_load()` 从持久存储加载值时,或使用 :c:func:`settings_runtime_set()` 从运行时后端设置值时调用此函数。(This gets called when the value is loaded from persistent storage with :c:func:`settings_load()`, or when using :c:func:`settings_runtime_set()` from the runtime backend.)

**h_commit**
    在完全加载设置后调用此函数。有时您不希望单个设置值立即生效,例如,如果有多个相互依赖的设置。(This gets called after the settings have been loaded in full. Sometimes you don't want an individual setting value to take effect right away, for example if there are multiple settings which are interdependent.)

**h_export**
    调用此函数以写入所有当前设置。当 :c:func:`settings_save()` 尝试保存设置或传输到任何用户实现的后端时会发生这种情况。(This gets called to write all current settings. This happens when :c:func:`settings_save()` tries to save the settings or transfer to any user-implemented back-end.)

设置处理程序还有一个提交优先级 ``cprio``,允许对 ``h_commit`` 调用进行优先级排序。当例如一个子系统初始化其他 ``h_commit`` 调用依赖的服务时,这可能是有利的。(Settings handlers also have a commit priority ``cprio`` that allows to prioritize the ``h_commit`` calls. This can be advantageous when e.g. a subsystem initializes a service that other ``h_commit`` calls depend on.)

设置处理程序 ``h_commit`` 例程默认使用 ``cprio = 0`` 初始化,使用不同优先级初始化设置处理程序可通过调用 :c:func:`settings_register_with_cprio()` 用于动态处理程序,或使用调用 :c:macro:`SETTINGS_STATIC_HANDLER_DEFINE_WITH_CPRIO()` 用于静态处理程序来完成。指定的 ``cprio`` 值是一个整数,其中较低的值表示较高的优先级。(Settings handlers ``h_commit`` routines are by default initialized with ``cprio = 0``, initializing a settings handler with a different priority is done using a call to :c:func:`settings_register_with_cprio()` for dynamic handlers or using a call to :c:macro:`SETTINGS_STATIC_HANDLER_DEFINE_WITH_CPRIO()` for static handlers. The specified ``cprio`` value is an integer where lower values mean higher priority.)

后端 (Backends)
****************

后端旨在向/从设置处理程序加载和保存数据,并实现一组处理程序函数。这些通过调用 :c:func:`settings_src_register()` 注册可以加载数据的后端,和/或调用 :c:func:`settings_dst_register()` 注册可以保存数据的后端。当前实现允许多个源后端,但只允许单个目标后端。(Backends are meant to load and save data to/from setting handlers, and implement a set of handler functions. These are registered using a call to :c:func:`settings_src_register()` for backends that can load data, and/or :c:func:`settings_dst_register()` for backends that can save data. The current implementation allows for multiple source backends but only a single destination backend.)

**csi_load**
    使用 :c:func:`settings_load()` 从持久存储加载值时调用此函数。(This gets called when loading values from persistent storage using :c:func:`settings_load()`.)

**csi_load_one**
    使用 :c:func:`settings_load_one()` 从持久存储仅加载一项时调用此函数。(This gets called when loading only one item from persistent storage using :c:func:`settings_load_one()`.)

**csi_get_val_len**
    使用 :c:func:`settings_get_val_len()` 从持久存储获取值的长度时调用此函数。(This gets called when getting a value's length from persistent storage using :c:func:`settings_get_val_len()`.)

**csi_save**
    使用 :c:func:`settings_save_one()` 将单个设置保存到持久存储时调用此函数。(This gets called when saving a single setting to persistent storage using :c:func:`settings_save_one()`.)

**csi_save_start**
    使用 :c:func:`settings_save()` 或 :c:func:`settings_save_subtree()` 开始保存所有当前设置时调用此函数。(This gets called when starting a save of all current settings using :c:func:`settings_save()` or :c:func:`settings_save_subtree()`.)

**csi_save_end**
    使用 :c:func:`settings_save()` 或 :c:func:`settings_save_subtree()` 保存所有当前设置后调用此函数。(This gets called after having saved of all current settings using :c:func:`settings_save()` or :c:func:`settings_save_subtree()`.)

Zephyr 存储后端 (Zephyr Storage Backends)
*******************************************

Zephyr 提供以下存储后端:(Zephyr offers the following storage backends:)

* 闪存循环缓冲区 (Flash Circular Buffer) (:kconfig:option:`CONFIG_SETTINGS_FCB`)。
* 文件系统中的文件 (:kconfig:option:`CONFIG_SETTINGS_FILE`)。
* 非易失性存储 (Non-Volatile Storage) (:kconfig:option:`CONFIG_SETTINGS_NVS`)。
* Zephyr 内存存储 (Zephyr Memory Storage) (:kconfig:option:`CONFIG_SETTINGS_ZMS`)。

您可以为设置声明多个源;当调用 :c:func:`settings_load()` 时,将恢复所有这些源中的设置。(You can declare multiple sources for settings; settings from all of these are restored when :c:func:`settings_load()` is called.)

写入设置只能有一个目标;这是当您调用 :c:func:`settings_save()` 或 :c:func:`settings_save_one()` 时数据存储的位置。(There can be only one target for writing settings; this is where data is stored when you call :c:func:`settings_save()`, or :c:func:`settings_save_one()`.)

FCB 读取目标使用 :c:func:`settings_fcb_src()` 注册,写入目标使用 :c:func:`settings_fcb_dst()` 注册。作为副作用,:c:func:`settings_fcb_src()` 初始化 FCB 区域,因此必须在调用 :c:func:`settings_fcb_dst()` 之前调用。文件读取目标使用 :c:func:`settings_file_src()` 注册,写入目标使用 :c:func:`settings_file_dst()` 注册。(FCB read target is registered using :c:func:`settings_fcb_src()`, and write target using :c:func:`settings_fcb_dst()`. As a side-effect, :c:func:`settings_fcb_src()` initializes the FCB area, so it must be called before calling :c:func:`settings_fcb_dst()`. File read target is registered using :c:func:`settings_file_src()`, and write target by using :c:func:`settings_file_dst()`.)

非易失性存储读取目标使用 :c:func:`settings_nvs_src()` 注册,写入目标使用 :c:func:`settings_nvs_dst()` 注册。(Non-volatile storage read target is registered using :c:func:`settings_nvs_src()`, and write target by using :c:func:`settings_nvs_dst()`.)

Zephyr 内存存储 (ZMS) 读取目标使用 :c:func:`settings_zms_src()` 注册,写入目标使用 :c:func:`settings_zms_dst()` 注册。(Zephyr Memory Storage (ZMS) read target is registered using :c:func:`settings_zms_src()`, and write target is registered using :c:func:`settings_zms_dst()`.)

ZMS 后端的特点是在将设置键存储到持久存储之前使用哈希函数对其进行哈希处理。如果存储大量不同的键,这种实现意味着键的哈希值之间可能会发生一些冲突。此数量取决于所选的哈希函数。(ZMS backend has the particularity of using hash functions to hash the settings key before storing it to the persistent storage. This implementation implies that some collisions between key's hashes could occur if a big number of different keys are stored. This number depends on the selected hash function.)

ZMS 后端可以处理 :math:`2^n` 个最大冲突,其中 n 由 (:kconfig:option:`CONFIG_SETTINGS_ZMS_MAX_COLLISIONS_BITS`) 定义。(ZMS backend can handle :math:`2^n` maximum collisions where n is defined by (:kconfig:option:`CONFIG_SETTINGS_ZMS_MAX_COLLISIONS_BITS`).)


存储位置 (Storage Location)
*****************************

FCB、非易失性存储 (NVS) 和 ZMS 后端默认寻找标签为 "storage" 的固定分区。可以通过在设备树中设置所选节点的 ``zephyr,settings-partition`` 属性来选择不同的分区。(The FCB, non-volatile storage (NVS) and ZMS backends look for a fixed partition with label "storage" by default. A different partition can be selected by setting the ``zephyr,settings-partition`` property of the chosen node in the devicetree.)

文件后端用于存储设置的文件路径通过选项 :kconfig:option:`CONFIG_SETTINGS_FILE_PATH` 选择。(The file path used by the file backend to store settings is selected via the option :kconfig:option:`CONFIG_SETTINGS_FILE_PATH`.)

从持久存储加载数据 (Loading data from persistent storage)
***********************************************************

调用 :c:func:`settings_load()` 使用 ``h_set`` 实现从存储加载设置数据到易失性内存。加载所有数据后,发出 ``h_commit`` 处理程序,向应用程序发出信号,表明已成功检索设置。(A call to :c:func:`settings_load()` uses an ``h_set`` implementation to load settings data from storage to volatile memory. After all data is loaded, the ``h_commit`` handler is issued, signalling the application that the settings were successfully retrieved.)

或者,调用 :c:func:`settings_load_one()` 将仅加载一个设置条目并将其存储在提供的缓冲区中。(Alternatively, a call to :c:func:`settings_load_one()` will load only one Settings entry and store it in the provided buffer.)

可选地,要仅获取与设置条目关联的值的长度,可以执行 :c:func:`settings_get_val_len()` 调用。例如,动态分配数据缓冲区并需要在通过 settings_load_one() 读取之前获取数据大小的应用程序使用此方法。(Optionally, to get only the value's length associated with the Settings entry, a call to :c:func:`settings_get_val_len()` can be performed. This is used for example by applications that allocates dynamically the data buffer and needs to get the data size before reading it by settings_load_one().)

从技术上讲,FCB 和文件后端可能会存储实体的一些历史记录。这意味着最新的数据实体存储在任何较旧的现有数据实体之后。从 Zephyr 2.1 开始,后端必须过滤掉所有旧实体,并仅使用最新实体调用回调。(Technically FCB and file backends may store some history of the entities. This means that the newest data entity is stored after any older existing data entities. Starting with Zephyr 2.1, the back-end must filter out all old entities and call the callback with only the newest entity.)

将数据存储到持久存储 (Storing data to persistent storage)
***********************************************************

调用 :c:func:`settings_save_one()` 使用后端实现将设置数据存储到存储介质。调用 :c:func:`settings_save()` 使用 ``h_export`` 实现在一次操作中使用 :c:func:`settings_save_one()` 存储不同的数据。仅当键应该由 :c:func:`settings_save()` 调用存储时,键才需要由 ``h_export`` 覆盖。(A call to :c:func:`settings_save_one()` uses a backend implementation to store settings data to the storage medium. A call to :c:func:`settings_save()` uses an ``h_export`` implementation to store different data in one operation using :c:func:`settings_save_one()`. A key needs to be covered by a ``h_export`` only if it is supposed to be stored by :c:func:`settings_save()` call.)

对于 FCB 和文件后端,仅存储更改键的实际值的数据的存储请求,因此应用程序无需检查值是否更改。这种存储机制意味着存储可以包含键的多个值分配,而只有最后一个是键的当前值。(For both FCB and file back-end only storage requests with data which changes most actual key's value are stored, therefore there is no need to check whether a value changed by the application. Such a storage mechanism implies that storage can contain multiple value assignments for a key , while only the last is the current value for the key.)

垃圾收集 (Garbage collection)
==============================
当存储变满 (FCB) 或消耗太多空间(文件)时,后端会删除非最近的键值对记录和不必要的键删除记录。(When storage becomes full (FCB) or consumes too much space (file), the backend removes non-recent key-value pairs records and unnecessary key-delete records.)

安全域设置 (Secure domain settings)
************************************
目前,设置不为同一实例同时提供安全和非安全配置存储方案。建议安全域使用自己的设置实例,如果需要,它可能会使用专用接口为非安全域提供数据(取决于情况)。(Currently settings doesn't provide scheme of being secure, and non-secure configuration storage simultaneously for the same instance. It is recommended that secure domain uses its own settings instance and it might provide data for non-secure domain using dedicated interface if needed (case dependent).)

示例:设备配置 (Example: Device Configuration)
**********************************************

这是一个简单的示例,其中设置处理程序仅实现 ``h_set`` 和 ``h_export``。``h_set`` 在从存储恢复值(或初始设置)时调用,``h_export`` 用于通过 ``storage_func()`` 将值写入存储。用户还可以实现一些其他导出功能,例如写入 shell 控制台)。(This is a simple example, where the settings handler only implements ``h_set`` and ``h_export``. ``h_set`` is called when the value is restored from storage (or when set initially), and ``h_export`` is used to write the value to storage thanks to ``storage_func()``. The user can also implement some other export functionality, for example, writing to the shell console).)

.. code-block:: c

    #define DEFAULT_FOO_VAL_VALUE 1

    static int8 foo_val = DEFAULT_FOO_VAL_VALUE;

    static int foo_settings_set(const char *name, size_t len,
                                settings_read_cb read_cb, void *cb_arg)
    {
        const char *next;
        int rc;

        if (settings_name_steq(name, "bar", &next) && !next) {
            if (len != sizeof(foo_val)) {
                return -EINVAL;
            }

            rc = read_cb(cb_arg, &foo_val, sizeof(foo_val));
            if (rc >= 0) {
                /* key-value pair was properly read.
                 * rc contains value length.
                 */
                return 0;
            }
            /* read-out error */
            return rc;
        }

        return -ENOENT;
    }

    static int foo_settings_export(int (*storage_func)(const char *name,
                                                       const void *value,
                                                       size_t val_len))
    {
        return storage_func("foo/bar", &foo_val, sizeof(foo_val));
    }

    struct settings_handler my_conf = {
        .name = "foo",
        .h_set = foo_settings_set,
        .h_export = foo_settings_export
    };

示例:持久化运行时状态 (Example: Persist Runtime State)
********************************************************

这是一个简单的示例,展示如何持久化运行时状态。在此示例中,仅定义了 ``h_set``,它在从持久存储恢复值时使用。(This is a simple example showing how to persist runtime state. In this example, only ``h_set`` is defined, which is used when restoring value from persistent storage.)

在此示例中,``main`` 函数递增 ``foo_val``,然后持久化最新数字。当系统重新启动时,应用程序在初始化时调用 :c:func:`settings_load()`,``foo_val`` 将从重新启动前的位置继续计数。(In this example, the ``main`` function increments ``foo_val``, and then persists the latest number. When the system restarts, the application calls :c:func:`settings_load()` while initializing, and ``foo_val`` will continue counting up from where it was before restart.)

.. code-block:: c

    #include <zephyr/kernel.h>
    #include <zephyr/sys/reboot.h>
    #include <zephyr/settings/settings.h>
    #include <zephyr/sys/printk.h>
    #include <inttypes.h>

    #define DEFAULT_FOO_VAL_VALUE 0

    static uint8_t foo_val = DEFAULT_FOO_VAL_VALUE;

    static int foo_settings_set(const char *name, size_t len,
                                settings_read_cb read_cb, void *cb_arg)
    {
        const char *next;
        int rc;

        if (settings_name_steq(name, "bar", &next) && !next) {
            if (len != sizeof(foo_val)) {
                return -EINVAL;
            }

            rc = read_cb(cb_arg, &foo_val, sizeof(foo_val));
            if (rc >= 0) {
                return 0;
            }

            return rc;
        }


        return -ENOENT;
    }

    struct settings_handler my_conf = {
        .name = "foo",
        .h_set = foo_settings_set
    };

    int main(void)
    {
        settings_subsys_init();
        settings_register(&my_conf);
        settings_load();

        foo_val++;
        settings_save_one("foo/bar", &foo_val, sizeof(foo_val));

        printk("foo: %d\n", foo_val);

        k_msleep(1000);
        sys_reboot(SYS_REBOOT_COLD);
    }

示例:自定义后端实现 (Example: Custom Backend Implementation)
*************************************************************

这是一个简单的示例,展示如何注册简单的自定义后端处理程序 (:kconfig:option:`CONFIG_SETTINGS_CUSTOM`)。(This is a simple example showing how to register a simple custom backend handler (:kconfig:option:`CONFIG_SETTINGS_CUSTOM`).)

.. code-block:: c

    static int settings_custom_load(struct settings_store *cs,
                                    const struct settings_load_arg *arg)
    {
        //...
    }

    static int settings_custom_save(struct settings_store *cs, const char *name,
                                    const char *value, size_t val_len)
    {
        //...
    }

    /* custom backend interface */
    static struct settings_store_itf settings_custom_itf = {
        .csi_load = settings_custom_load,
        .csi_save = settings_custom_save,
    };

    /* custom backend node */
    static struct settings_store settings_custom_store = {
        .cs_itf = &settings_custom_itf
    };

    int settings_backend_init(void)
    {
        /* register custom backend */
        settings_dst_register(&settings_custom_store);
        settings_src_register(&settings_custom_store);
        return 0;
    }

API 参考 (API Reference)
*************************

设置子系统 API 由 :zephyr_file:`include/zephyr/settings/settings.h` 提供。(The Settings subsystem APIs are provided by :zephyr_file:`include/zephyr/settings/settings.h`.)

通用设置使用 API (API for general settings usage)
==================================================
.. doxygengroup:: settings

键名处理 API (API for key-name processing)
===========================================
.. doxygengroup:: settings_name_proc

运行时设置操作 API (API for runtime settings manipulation)
===========================================================
.. doxygengroup:: settings_rt

后端接口 API (API of backend interface)
========================================
..  doxygengroup:: settings_backend
