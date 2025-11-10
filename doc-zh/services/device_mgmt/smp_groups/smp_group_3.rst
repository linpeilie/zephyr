.. _mcumgr_smp_group_3:

设置(配置)管理组 (Settings (Config) Management Group)
########################################################

设置管理组(在原始MCUmgr存储库中称为配置管理器) (Settings management group (known as Configuration Manager in the original MCUmgr repository))
定义以下命令 (defines the following commands):

.. table::
    :align: center

    +----------------+------------------------------+
    | ``命令ID``     | 命令描述                     |
    | (``Command ID``| (Command description)        |
    +================+==============================+
    | ``0``          | 读/写设置                    |
    |                | (Read/write setting)         |
    +----------------+------------------------------+
    | ``1``          | 删除设置 (Delete setting)    |
    +----------------+------------------------------+
    | ``2``          | 提交设置 (Commit settings)   |
    +----------------+------------------------------+
    | ``3``          | 加载/保存设置                |
    |                | (Load/Save settings)         |
    +----------------+------------------------------+

请注意,Zephyr版本添加了原始上游版本不支持的额外命令和功能 (Note that the Zephyr version adds additional commands and features which are not supported by the original upstream version),但是,原始客户端功能应该可以用于读/写功能 (however, the original client functionality should work for read/write functionality)。

读/写设置命令 (Read/write setting command)
*******************************************

Read/write setting command allows updating a setting entry on a device or
getting the current value of a setting from a device.

Read setting request
====================

Read setting request header fields:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``0``  | ``3``        | ``0``          |
    +--------+--------------+----------------+

CBOR data of request:

.. code-block:: none

    {
        (str)"name"         : (str)
        (str,opt)"max_size" : (uint)
    }

where:

.. table::
    :align: center

    +------------+-----------------------------------------+
    | "name"     | string of the setting to retrieve       |
    +------------+-----------------------------------------+
    | "max_size" | optional maximum size of data to return |
    +------------+-----------------------------------------+

Read setting response
=====================

Read setting response header fields:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``1``  | ``3``        | ``0``          |
    +--------+--------------+----------------+

CBOR data of successful response:

.. code-block:: none

    {
        (str)"val"          : (bstr)
        (str,opt)"max_size" : (uint)
    }

In case of error the CBOR data takes the form:

.. tabs::

   .. group-tab:: SMP version 2

      .. code-block:: none

          {
              (str)"err" : {
                  (str)"group"    : (uint)
                  (str)"rc"       : (uint)
              }
          }

   .. group-tab:: SMP version 1

      .. code-block:: none

          {
              (str)"rc"       : (int)
          }

where:

.. table::
    :align: center

    +------------------+-------------------------------------------------------------------------+
    | "val"            | binary string of the returned data, note that the underlying data type  |
    |                  | cannot be specified through this and must be known by the client.       |
    +------------------+-------------------------------------------------------------------------+
    | "max_size"       | will be set if the maximum supported data size is smaller than the      |
    |                  | maximum requested data size, and contains the maximum data size which   |
    |                  | the device supports, equivalent to                                      |
    |                  | kconfig:option:`CONFIG_MCUMGR_GRP_SETTINGS_NAME_LEN`.                   |
    +------------------+-------------------------------------------------------------------------+
    | "err" -> "group" | :c:enum:`mcumgr_group_t` group of the group-based error code. Only      |
    |                  | appears if an error is returned when using SMP version 2.               |
    +------------------+-------------------------------------------------------------------------+
    | "err" -> "rc"    | contains the index of the group-based error code. Only appears if       |
    |                  | non-zero (error condition) when using SMP version 2.                    |
    +------------------+-------------------------------------------------------------------------+
    | "rc"             | :c:enum:`mcumgr_err_t` only appears if non-zero (error condition) when  |
    |                  | using SMP version 1 or for SMP errors when using SMP version 2.         |
    +------------------+-------------------------------------------------------------------------+

Write setting request
=====================

Write setting request header fields:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``2``  | ``3``        | ``0``          |
    +--------+--------------+----------------+

CBOR data of request:

.. code-block:: none

    {
        (str)"name"    : (str)
        (str)"val"     : (bstr)
    }

where:

.. table::
    :align: center

    +--------+-------------------------------------+
    | "name" | string of the setting to update/set |
    +--------+-------------------------------------+
    | "val"  | value to set the setting to         |
    +--------+-------------------------------------+

Write setting response
======================

Write setting response header fields:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``3``  | ``3``        | ``0``          |
    +--------+--------------+----------------+

The command sends an empty CBOR map as data if successful. In case of error the CBOR data takes
the form:

.. tabs::

   .. group-tab:: SMP version 2

      .. code-block:: none

          {
              (str)"err" : {
                  (str)"group"    : (uint)
                  (str)"rc"       : (uint)
              }
          }

   .. group-tab:: SMP version 1

      .. code-block:: none

          {
              (str)"rc"       : (int)
          }

where:

.. table::
    :align: center

    +------------------+-------------------------------------------------------------------------+
    | "err" -> "group" | :c:enum:`mcumgr_group_t` group of the group-based error code. Only      |
    |                  | appears if an error is returned when using SMP version 2.               |
    +------------------+-------------------------------------------------------------------------+
    | "err" -> "rc"    | contains the index of the group-based error code. Only appears if       |
    |                  | non-zero (error condition) when using SMP version 2.                    |
    +------------------+-------------------------------------------------------------------------+
    | "rc"             | :c:enum:`mcumgr_err_t` only appears if non-zero (error condition) when  |
    |                  | using SMP version 1 or for SMP errors when using SMP version 2.         |
    +------------------+-------------------------------------------------------------------------+

Delete setting command
**********************

Delete setting command allows deleting a setting on a device.

Delete setting request
======================

Delete setting request header fields:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``2``  | ``3``        | ``1``          |
    +--------+--------------+----------------+

CBOR data of request:

.. code-block:: none

    {
        (str)"name"   : (str)
    }

where:

.. table::
    :align: center

    +--------+---------------------------------+
    | "name" | string of the setting to delete |
    +--------+---------------------------------+

Delete setting response
=======================

Delete setting response header fields:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``3``  | ``3``        | ``1``          |
    +--------+--------------+----------------+

The command sends an empty CBOR map as data if successful. In case of error the CBOR data takes
the form:

.. tabs::

   .. group-tab:: SMP version 2

      .. code-block:: none

          {
              (str)"err" : {
                  (str)"group"    : (uint)
                  (str)"rc"       : (uint)
              }
          }

   .. group-tab:: SMP version 1

      .. code-block:: none

          {
              (str)"rc"       : (int)
          }

where:

.. table::
    :align: center

    +------------------+-------------------------------------------------------------------------+
    | "err" -> "group" | :c:enum:`mcumgr_group_t` group of the group-based error code. Only      |
    |                  | appears if an error is returned when using SMP version 2.               |
    +------------------+-------------------------------------------------------------------------+
    | "err" -> "rc"    | contains the index of the group-based error code. Only appears if       |
    |                  | non-zero (error condition) when using SMP version 2.                    |
    +------------------+-------------------------------------------------------------------------+
    | "rc"             | :c:enum:`mcumgr_err_t` only appears if non-zero (error condition) when  |
    |                  | using SMP version 1 or for SMP errors when using SMP version 2.         |
    +------------------+-------------------------------------------------------------------------+

Commit settings command
***********************

Commit settings command allows committing all settings that have been set but not yet applied on a
device.

Commit settings request
=======================

Commit settings request header fields:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``2``  | ``3``        | ``2``          |
    +--------+--------------+----------------+

The command sends an empty CBOR map as data.

Commit settings response
========================

Commit settings response header fields:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``3``  | ``3``        | ``2``          |
    +--------+--------------+----------------+

The command sends an empty CBOR map as data if successful. In case of error the CBOR data takes
the form:

.. tabs::

   .. group-tab:: SMP version 2

      .. code-block:: none

          {
              (str)"err" : {
                  (str)"group"    : (uint)
                  (str)"rc"       : (uint)
              }
          }

   .. group-tab:: SMP version 1

      .. code-block:: none

          {
              (str)"rc"       : (int)
          }

where:

.. table::
    :align: center

    +------------------+-------------------------------------------------------------------------+
    | "err" -> "group" | :c:enum:`mcumgr_group_t` group of the group-based error code. Only      |
    |                  | appears if an error is returned when using SMP version 2.               |
    +------------------+-------------------------------------------------------------------------+
    | "err" -> "rc"    | contains the index of the group-based error code. Only appears if       |
    |                  | non-zero (error condition) when using SMP version 2.                    |
    +------------------+-------------------------------------------------------------------------+
    | "rc"             | :c:enum:`mcumgr_err_t` only appears if non-zero (error condition) when  |
    |                  | using SMP version 1 or for SMP errors when using SMP version 2.         |
    +------------------+-------------------------------------------------------------------------+

Load/Save settings command
**************************

Load/Save settings command allows loading/saving all serialized items from/to persistent storage
on a device.

Load settings request
=====================

Load settings request header fields:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``0``  | ``3``        | ``3``          |
    +--------+--------------+----------------+

The command sends an empty CBOR map as data.

Load settings response
======================

Load settings response header fields:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``1``  | ``3``        | ``3``          |
    +--------+--------------+----------------+

The command sends an empty CBOR map as data if successful. In case of error the CBOR data takes
the form:

.. tabs::

   .. group-tab:: SMP version 2

      .. code-block:: none

          {
              (str)"err" : {
                  (str)"group"    : (uint)
                  (str)"rc"       : (uint)
              }
          }

   .. group-tab:: SMP version 1

      .. code-block:: none

          {
              (str)"rc"       : (int)
          }

where:

.. table::
    :align: center

    +------------------+-------------------------------------------------------------------------+
    | "err" -> "group" | :c:enum:`mcumgr_group_t` group of the group-based error code. Only      |
    |                  | appears if an error is returned when using SMP version 2.               |
    +------------------+-------------------------------------------------------------------------+
    | "err" -> "rc"    | contains the index of the group-based error code. Only appears if       |
    |                  | non-zero (error condition) when using SMP version 2.                    |
    +------------------+-------------------------------------------------------------------------+
    | "rc"             | :c:enum:`mcumgr_err_t` only appears if non-zero (error condition) when  |
    |                  | using SMP version 1 or for SMP errors when using SMP version 2.         |
    +------------------+-------------------------------------------------------------------------+

Save settings request
=====================

Save settings request header fields:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``2``  | ``3``        | ``3``          |
    +--------+--------------+----------------+

The command sends an empty CBOR map as data.

Save settings response
======================

Save settings response header fields:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``3``  | ``3``        | ``3``          |
    +--------+--------------+----------------+

The command sends an empty CBOR map as data if successful. In case of error the CBOR data takes
the form:

.. tabs::

   .. group-tab:: SMP version 2

      .. code-block:: none

          {
              (str)"err" : {
                  (str)"group"    : (uint)
                  (str)"rc"       : (uint)
              }
          }

   .. group-tab:: SMP version 1

      .. code-block:: none

          {
              (str)"rc"       : (int)
          }

where:

.. table::
    :align: center

    +------------------+------------------------------------------------------------------------+
    | "err" -> "group" | :c:enum:`mcumgr_group_t` group of the group-based error code. Only     |
    |                  | appears if an error is returned when using SMP version 2.              |
    +------------------+------------------------------------------------------------------------+
    | "err" -> "rc"    | contains the index of the group-based error code. Only appears if      |
    |                  | non-zero (error condition) when using SMP version 2.                   |
    +------------------+------------------------------------------------------------------------+
    | "rc"             | :c:enum:`mcumgr_err_t` only appears if non-zero (error condition) when |
    |                  | using SMP version 1 or for SMP errors when using SMP version 2.        |
    +------------------+------------------------------------------------------------------------+

Settings access callback
************************

There is a settings access MCUmgr callback available (see :ref:`mcumgr_callbacks` for details on
callbacks) which allows for applications/modules to know when settings management commands are
used and, optionally, block access (for example through the use of a security mechanism). This
callback can be enabled with :kconfig:option:`CONFIG_MCUMGR_GRP_SETTINGS_ACCESS_HOOK`, registered
with the event :c:enumerator:`MGMT_EVT_OP_SETTINGS_MGMT_ACCESS`, whereby the supplied callback data
is :c:struct:`settings_mgmt_access`.
