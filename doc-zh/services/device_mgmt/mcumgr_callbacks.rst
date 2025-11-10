.. _mcumgr_callbacks:

MCUmgr回调 (MCUmgr Callbacks)
##############################

概述 (Overview)
****************

MCUmgr具有可自定义的回调/通知系统,允许应用程序(和模块)代码接收它们感兴趣的MCUmgr事件的回调并对其做出反应或向调用函数返回状态码,以控制是否应该允许该操作 (MCUmgr has a customisable callback/notification system that allows application (and module) code to receive callbacks for MCUmgr events that they are interested in and react to them or return a status code to the calling function that provides control over if the action should be allowed or not)。例如,对于fs_mgmt组,可以限制文件访问,回调允许应用程序检查请求路径并允许或拒绝访问该文件,或者可以将提供的路径重写为不同的路径以支持透明文件重定向 (An example of this is with the fs_mgmt group, whereby file access can be gated, the callback allows the application to inspect the request path and allow or deny access to said file, or it can rewrite the provided path to a different path for transparent file redirection support)。

实现 (Implementation)
**********************

启用 (Enabling)
===============

可以使用 :kconfig:option:`CONFIG_MCUMGR_MGMT_NOTIFICATION_HOOKS` 启用基本的回调/通知系统,这将把注册和通知系统编译到代码中 (The base callback/notification system can be enabled using :kconfig:option:`CONFIG_MCUMGR_MGMT_NOTIFICATION_HOOKS` which will compile the registration and notification system into the code)。这不会默认提供任何回调,因为构建支持的回调也必须通过启用所需回调的Kconfig来选择(详见 :ref:`mcumgr_cb_events`) (This will not provide any callbacks by default as the callbacks that are supported by a build must also be selected by enabling the Kconfig's for the required callbacks (see :ref:`mcumgr_cb_events` for further details))。然后可以声明具有 :c:type:`mgmt_cb` 类型定义的回调函数,并通过在 :c:struct:`mgmt_callback` 结构内为所需事件调用 :c:func:`mgmt_callback_register` 来注册 (A callback function with the :c:type:`mgmt_cb` type definition can then be declared and registered by calling :c:func:`mgmt_callback_register` for the desired event inside of a :c:struct:`mgmt_callback` structure)。处理程序按注册顺序调用 (Handlers are called in the order that they were registered)。

启用系统后,可以在应用程序代码中设置和定义基本处理程序,如下所示 (With the system enabled, a basic handler can be set up and defined in application code as per):

.. code-block:: c

    #include <zephyr/kernel.h>
    #include <zephyr/mgmt/mcumgr/mgmt/mgmt.h>
    #include <zephyr/mgmt/mcumgr/mgmt/callbacks.h>

    struct mgmt_callback my_callback;

    enum mgmt_cb_return my_function(uint32_t event, enum mgmt_cb_return prev_status,
                                    int32_t *rc, uint16_t *group, bool *abort_more,
                                    void *data, size_t data_size)
    {
        if (event == MGMT_EVT_OP_CMD_DONE) {
            /* This is the event we registered for */
        }

        /* Return OK status code to continue with acceptance to underlying handler */
        return MGMT_CB_OK;
    }

    int main()
    {
        my_callback.callback = my_function;
        my_callback.event_id = MGMT_EVT_OP_CMD_DONE;
        mgmt_callback_register(&my_callback);
    }

此代码为 :c:enumerator:`MGMT_EVT_OP_CMD_DONE` 事件注册处理程序,该事件将在MCUmgr命令处理完成并生成输出后调用,请注意,这需要启用 :kconfig:option:`CONFIG_MCUMGR_SMP_COMMAND_STATUS_HOOKS` 才能接收此回调 (This code registers a handler for the :c:enumerator:`MGMT_EVT_OP_CMD_DONE` event, which will be called after a MCUmgr command has been processed and output generated, note that this requires that :kconfig:option:`CONFIG_MCUMGR_SMP_COMMAND_STATUS_HOOKS` be enabled to receive this callback)。

可以设置多个回调以使用单个函数作为公共回调,并且可以通过一次注册每个组来为每个事件使用许多不同的函数,或者可以通过使用 ``MGMT_EVT_OP_*_ALL`` 事件之一来启用整个组的所有通知,或者处理程序可以通过使用 :c:enumerator:`MGMT_EVT_OP_ALL` 设置每个通知 (Multiple callbacks can be setup to use a single function as a common callback, and many different functions can be used for each event by registering each group once, or all notifications for a whole group can be enabled by using one of the ``MGMT_EVT_OP_*_ALL`` events, alternatively a handler can setup for every notification by using :c:enumerator:`MGMT_EVT_OP_ALL`)。设置处理程序时,只能组合同一组中的事件,例如可以通过单个注册调用设置5个img_mgmt回调,但要同时设置os_mgmt回调的回调,必须作为单独的注册进行 (When setting up handlers, events can be combined that are in the same group only, for example 5 img_mgmt callbacks can be setup with a single registration call, but to also setup a callback for an os_mgmt callback, this must be done as a separate registration)。组ID是数字增量,事件ID是位掩码值,因此有此限制 (Group IDs are numerical increments, event IDs are bitmask values, hence the restriction)。

例如,以下注册是允许的,它将在单个注册中使用单个回调函数注册3个SMP事件 (As an example, the following registration is allowed, which will register for 3 SMP events with a single callback function in a single registration):

.. code-block:: c

    my_callback.callback = my_function;
    my_callback.event_id = (MGMT_EVT_OP_CMD_RECV |
                            MGMT_EVT_OP_CMD_STATUS |
                            MGMT_EVT_OP_CMD_DONE);
    mgmt_callback_register(&my_callback);

以下代码是不允许的,并将导致未定义的操作,因为它将IMG管理组与OS管理组混合在一起,而组**不是**位掩码值,只有事件才是 (The following code is not allowed, and will cause undefined operation, because it mixes the IMG management group with the OS management group whereby the group is **not** a bitmask value, only the event is):

.. code-block:: c

    my_callback.callback = my_function;
    my_callback.event_id = (MGMT_EVT_OP_IMG_MGMT_DFU_STARTED |
                            MGMT_EVT_OP_OS_MGMT_RESET);
    mgmt_callback_register(&my_callback);

.. _mcumgr_cb_events:

事件 (Events)
==============

可以通过启用其相应的Kconfig选项来选择事件 (Events can be selected by enabling their corresponding Kconfig option):

 - :kconfig:option:`CONFIG_MCUMGR_SMP_COMMAND_STATUS_HOOKS`
    MCUmgr命令状态 (MCUmgr command status) (:c:enumerator:`MGMT_EVT_OP_CMD_RECV`,
    :c:enumerator:`MGMT_EVT_OP_CMD_STATUS`,
    :c:enumerator:`MGMT_EVT_OP_CMD_DONE`)
 - :kconfig:option:`CONFIG_MCUMGR_GRP_FS_FILE_ACCESS_HOOK`
    fs_mgmt文件访问 (fs_mgmt file access) (:c:enumerator:`MGMT_EVT_OP_FS_MGMT_FILE_ACCESS`)
 - :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_UPLOAD_CHECK_HOOK`
    img_mgmt上传检查 (img_mgmt upload check) (:c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_CHUNK`)
 - :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_STATUS_HOOKS`
    img_mgmt上传状态 (img_mgmt upload status) (:c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_STOPPED`,
    :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_STARTED`,
    :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_PENDING`,
    :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_CONFIRMED`)
 - :kconfig:option:`CONFIG_MCUMGR_GRP_OS_RESET_HOOK`
    os_mgmt重置检查 (os_mgmt reset check) (:c:enumerator:`MGMT_EVT_OP_OS_MGMT_RESET`)
 - :kconfig:option:`CONFIG_MCUMGR_GRP_SETTINGS_ACCESS_HOOK`
    settings_mgmt访问 (settings_mgmt access) (:c:enumerator:`MGMT_EVT_OP_SETTINGS_MGMT_ACCESS`)

操作 (Actions)
===============

某些回调需要返回状态以允许或禁止操作,例如fs_mgmt访问钩子允许允许或拒绝对文件的访问 (Some callbacks expect a return status to either allow or disallow an operation, an example is the fs_mgmt access hook which allows for access to files to be allowed or denied)。对于这些处理程序,处理程序返回的第一个非OK错误代码将返回给MCUmgr客户端 (With these handlers, the first non-OK error code returned by a handler will be returned to the MCUmgr client)。

选择性拒绝文件访问的示例 (An example of selectively denying file access):

.. code-block:: c

    #include <zephyr/kernel.h>
    #include <zephyr/mgmt/mcumgr/mgmt/mgmt.h>
    #include <zephyr/mgmt/mcumgr/mgmt/callbacks.h>
    #include <string.h>

    struct mgmt_callback my_callback;

    enum mgmt_cb_return my_function(uint32_t event, enum mgmt_cb_return prev_status,
                                    int32_t *rc, uint16_t *group, bool *abort_more,
                                    void *data, size_t data_size)
    {
        /* Only run this handler if a previous handler has not failed */
        if (event == MGMT_EVT_OP_FS_MGMT_FILE_ACCESS && prev_status == MGMT_CB_OK) {
            struct fs_mgmt_file_access *fs_data = (struct fs_mgmt_file_access *)data;

            /* Check if this is an upload and deny access if it is, otherwise check
             * the path and deny if is matches a name
             */
            if (fs_data->access == FS_MGMT_FILE_ACCESS_WRITE) {
                /* Return an access denied error code to the client and abort calling
                 * further handlers
                 */
                *abort_more = true;
                *rc = MGMT_ERR_EACCESSDENIED;

                return MGMT_CB_ERROR_RC;
            } else if (strcmp(fs_data->filename, "/lfs1/false_deny.txt") == 0) {
                /* Return a no entry error code to the client, call additional handlers
                 * (which will have failed set to true)
                 */
                *rc = MGMT_ERR_ENOENT;

                return MGMT_CB_ERROR_RC;
            }
        }

        /* Return OK status code to continue with acceptance to underlying handler */
        return MGMT_CB_OK;
    }

    int main()
    {
        my_callback.callback = my_function;
        my_callback.event_id = MGMT_EVT_OP_FS_MGMT_FILE_ACCESS;
        mgmt_callback_register(&my_callback);
    }

此代码为 :c:enumerator:`MGMT_EVT_OP_FS_MGMT_FILE_ACCESS` 事件注册处理程序,该事件将在收到fs_mgmt文件读/写命令后调用以检查是否应该允许访问该文件,请注意,这需要启用 :kconfig:option:`CONFIG_MCUMGR_GRP_FS_FILE_ACCESS_HOOK` 才能接收此回调 (This code registers a handler for the :c:enumerator:`MGMT_EVT_OP_FS_MGMT_FILE_ACCESS` event, which will be called after a fs_mgmt file read/write command has been received to check if access to the file should be allowed or not, note that this requires that :kconfig:option:`CONFIG_MCUMGR_GRP_FS_FILE_ACCESS_HOOK` be enabled to receive this callback)。
可以返回两种类型的错误,可以将 ``rc`` 参数设置为 :c:enum:`mcumgr_err_t` 错误代码并返回 :c:enumerator:`MGMT_CB_ERROR_RC`,或者可以通过将 ``group`` 值设置为组并将 ``rc`` 值设置为组错误代码并返回 :c:enumerator:`MGMT_CB_ERROR_ERR` 来设置组错误代码(MCUmgr协议版本2引入) (Two types of errors can be returned, the ``rc`` parameter can be set to an :c:enum:`mcumgr_err_t` error code and :c:enumerator:`MGMT_CB_ERROR_RC` can be returned, or a group error code (introduced with version 2 of the MCUmgr protocol) can be set by setting the ``group`` value to the group and ``rc`` value to the group error code and returning :c:enumerator:`MGMT_CB_ERROR_ERR`)。

MCUmgr命令回调使用/添加新事件类型 (MCUmgr Command Callback Usage/Adding New Event Types)
==========================================================================================

要向MCUmgr命令添加回调,可以使用事件ID调用 :c:func:`mgmt_callback_notify`,并可选地传递数据结构给回调(处理程序可以修改) (To add a callback to a MCUmgr command, :c:func:`mgmt_callback_notify` can be called with the event ID and, optionally, a data struct to pass to the callback (which can be modified by handlers))。如果不需要传递数据,可以使用 ``NULL`` 代替,并将数据大小设置为0 (If no data needs to be passed back, ``NULL`` can be used instead, and size of the data set to 0)。

MCUmgr命令处理程序示例 (An example MCUmgr command handler):

.. code-block:: c

    #include <zephyr/kernel.h>
    #include <zcbor_common.h>
    #include <zcbor_encode.h>
    #include <zephyr/mgmt/mcumgr/smp/smp.h>
    #include <zephyr/mgmt/mcumgr/mgmt/mgmt.h>
    #include <zephyr/mgmt/mcumgr/mgmt/callbacks.h>

    #define MGMT_EVT_GRP_USER_ONE MGMT_EVT_GRP_USER_CUSTOM_START

    enum user_one_group_events {
        /** Callback on first post, data is test_struct. */
        MGMT_EVT_OP_USER_ONE_FIRST  = MGMT_DEF_EVT_OP_ID(MGMT_EVT_GRP_USER_ONE, 0),

        /** Callback on second post, data is test_struct. */
        MGMT_EVT_OP_USER_ONE_SECOND = MGMT_DEF_EVT_OP_ID(MGMT_EVT_GRP_USER_ONE, 1),

        /** Used to enable all user_one events. */
        MGMT_EVT_OP_USER_ONE_ALL    = MGMT_DEF_EVT_OP_ALL(MGMT_EVT_GRP_USER_ONE),
    };

    struct test_struct {
        uint8_t some_value;
    };

    static int test_command(struct mgmt_ctxt *ctxt)
    {
        int rc;
        int err_rc;
        uint16_t err_group;
        zcbor_state_t *zse = ctxt->cnbe->zs;
        bool ok;
        struct test_struct test_data = {
            .some_value = 8,
        };

        rc = mgmt_callback_notify(MGMT_EVT_OP_USER_ONE_FIRST, &test_data,
                                  sizeof(test_data), &err_rc, &err_group);

        if (rc != MGMT_CB_OK) {
            /* A handler returned a failure code */
            if (rc == MGMT_CB_ERROR_RC) {
                /* The failure code is the RC value */
                return err_rc;
            }

            /* The failure is a group and ID error value */
            ok = smp_add_cmd_err(zse, err_group, (uint16_t)err_rc);
            goto end;
        }

        /* All handlers returned success codes */
        ok = zcbor_tstr_put_lit(zse, "output_value") &&
             zcbor_int32_put(zse, 1234);

    end:
        rc = (ok ? MGMT_ERR_EOK : MGMT_ERR_EMSGSIZE);

        return rc;
    }

如果回调不需要响应,可以调用函数并转换为void (If no response is required for the callback, the function call be called and casted to void)。

.. _mcumgr_cb_migration:

迁移 (Migration)
*****************

如果在Zephyr 3.2或更早版本中有使用以前回调系统的现有代码,则需要迁移到新系统 (If there is existing code using the previous callback system(s) in Zephyr 3.2 or earlier, then it will need to be migrated to the new system)。要迁移代码,需要将以下回调注册函数迁移为使用 :c:func:`mgmt_callback_register` 注册回调(请注意,除了任何迁移外,还需要设置 :kconfig:option:`CONFIG_MCUMGR_MGMT_NOTIFICATION_HOOKS` 以启用新的通知系统) (To migrate code, the following callback registration functions will need to be migrated to register for callbacks using :c:func:`mgmt_callback_register` (note that :kconfig:option:`CONFIG_MCUMGR_MGMT_NOTIFICATION_HOOKS` will need to be set to enable the new notification system in addition to any migrations)):

 * mgmt_evt
    使用 :c:enumerator:`MGMT_EVT_OP_CMD_RECV`、:c:enumerator:`MGMT_EVT_OP_CMD_STATUS` 或 :c:enumerator:`MGMT_EVT_OP_CMD_DONE` 作为同名事件的直接替换,其中提供的数据是 :c:struct:`mgmt_evt_op_cmd_arg` (Using :c:enumerator:`MGMT_EVT_OP_CMD_RECV`, :c:enumerator:`MGMT_EVT_OP_CMD_STATUS`, or :c:enumerator:`MGMT_EVT_OP_CMD_DONE` as drop-in replacements for events of the same name, where the provided data is :c:struct:`mgmt_evt_op_cmd_arg`)。
    需要设置 :kconfig:option:`CONFIG_MCUMGR_SMP_COMMAND_STATUS_HOOKS` (:kconfig:option:`CONFIG_MCUMGR_SMP_COMMAND_STATUS_HOOKS` needs to be set)。
 * fs_mgmt_register_evt_cb
    使用 :c:enumerator:`MGMT_EVT_OP_FS_MGMT_FILE_ACCESS`,其中提供的数据是 :c:struct:`fs_mgmt_file_access` (Using :c:enumerator:`MGMT_EVT_OP_FS_MGMT_FILE_ACCESS` where the provided data is :c:struct:`fs_mgmt_file_access`)。不要返回true以允许操作或返回false以拒绝,需要返回MCUmgr结果代码,:c:enumerator:`MGMT_ERR_EOK` 将允许操作,任何其他返回代码将禁止操作并将该代码返回给客户端(可以使用 :c:enumerator:`MGMT_ERR_EACCESSDENIED` 表示访问拒绝错误) (Instead of returning true to allow the action or false to deny, a MCUmgr result code needs to be returned, :c:enumerator:`MGMT_ERR_EOK` will allow the action, any other return code will disallow it and return that code to the client (:c:enumerator:`MGMT_ERR_EACCESSDENIED` can be used for an access denied error))。需要设置 :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_STATUS_HOOKS` (:kconfig:option:`CONFIG_MCUMGR_GRP_IMG_STATUS_HOOKS` needs to be set)。
 * img_mgmt_register_callbacks
    如果使用了 ``dfu_started_cb`` 则使用 :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_STARTED`,如果使用了 ``dfu_stopped_cb`` 则使用 :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_STOPPED`,如果使用了 ``dfu_pending_cb`` 则使用 :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_PENDING`,如果使用了 ``dfu_confirmed_cb`` 则使用 :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_CONFIRMED` (Using :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_STARTED` if ``dfu_started_cb`` was used, :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_STOPPED` if ``dfu_stopped_cb`` was used, :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_PENDING` if ``dfu_pending_cb`` was used or :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_CONFIRMED` if ``dfu_confirmed_cb`` was used)。这些回调没有任何返回状态 (These callbacks do not have any return status)。
    需要设置 :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_STATUS_HOOKS` (:kconfig:option:`CONFIG_MCUMGR_GRP_IMG_STATUS_HOOKS` needs to be set)。
 * img_mgmt_set_upload_cb
    使用 :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_CHUNK`,其中提供的数据是 :c:struct:`img_mgmt_upload_check` (Using :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_CHUNK` where the provided data is :c:struct:`img_mgmt_upload_check`)。不要返回true以允许操作或返回false以拒绝,需要返回MCUmgr结果代码,:c:enumerator:`MGMT_ERR_EOK` 将允许操作,任何其他返回代码将禁止操作并将该代码返回给客户端(可以使用 :c:enumerator:`MGMT_ERR_EACCESSDENIED` 表示访问拒绝错误) (Instead of returning true to allow the action or false to deny, a MCUmgr result code needs to be returned, :c:enumerator:`MGMT_ERR_EOK` will allow the action, any other return code will disallow it and return that code to the client (:c:enumerator:`MGMT_ERR_EACCESSDENIED` can be used for an access denied error))。需要设置 :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_UPLOAD_CHECK_HOOK` (:kconfig:option:`CONFIG_MCUMGR_GRP_IMG_UPLOAD_CHECK_HOOK` needs to be set)。
 * os_mgmt_register_reset_evt_cb
    使用 :c:enumerator:`MGMT_EVT_OP_OS_MGMT_RESET` (Using :c:enumerator:`MGMT_EVT_OP_OS_MGMT_RESET`)。不要返回true以允许操作或返回false以拒绝,需要返回MCUmgr结果代码,:c:enumerator:`MGMT_ERR_EOK` 将允许操作,任何其他返回代码将禁止操作并将该代码返回给客户端(可以使用 :c:enumerator:`MGMT_ERR_EACCESSDENIED` 表示访问拒绝错误) (Instead of returning true to allow the action or false to deny, a MCUmgr result code needs to be returned, :c:enumerator:`MGMT_ERR_EOK` will allow the action, any other return code will disallow it and return that code to the client (:c:enumerator:`MGMT_ERR_EACCESSDENIED` can be used for an access denied error))。需要设置 :kconfig:option:`CONFIG_MCUMGR_SMP_COMMAND_STATUS_HOOKS` (:kconfig:option:`CONFIG_MCUMGR_SMP_COMMAND_STATUS_HOOKS` needs to be set)。

API参考 (API Reference)
************************

.. doxygengroup:: mcumgr_callback_api
