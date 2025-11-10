.. _mcumgr_handlers:

MCUmgr处理程序 (MCUmgr handlers)
#################################

概述 (Overview)
****************

MCUmgr通过使用组处理程序来工作,这些处理程序标识与特定管理区域相关的一组函数,使用16位标识值进行寻址 (MCUmgr functions by having group handlers which identify a group of functions relating to a specific management area, which is addressed with a 16-bit identification value),:c:enum:`mcumgr_group_t` 包含Zephyr中可用的管理组及其相应的组ID值 (:c:enum:`mcumgr_group_t` contains the management groups available in Zephyr with their corresponding group ID values)。组ID包含在SMP头中以标识命令属于哪个组,还有一个8位命令ID用于标识该组要执行的功能 (The group ID is included in SMP headers to identify which group a command belongs to, there is also an 8-bit command ID which identifies the function of that group to execute) - 有关SMP协议和头的详细信息,请参见 :ref:`mcumgr_smp_protocol_specification` (see :ref:`mcumgr_smp_protocol_specification` for details on the SMP protocol and header)。每个唯一ID只能有一个注册的组 (There can only be one registered group per unique ID)。

实现 (Implementation)
**********************

MCUmgr处理程序可以由应用程序代码或模块代码外部添加,它们不必驻留在上游Zephyr树中即可使用 (MCUmgr handlers can be added externally by application code or by module code, they do not have to reside in the upstream Zephyr tree to be usable)。创建处理程序的第一步是为其创建文件夹结构,典型的Zephyr MCUmgr组布局如下 (The first step to creating a handler is to create the folder structure for it, the typical Zephyr MCUmgr group layout is as follows):

.. code-block:: none

   <dir>/grp/<grp_name>_mgmt/
   ├── CMakeLists.txt
   ├── Kconfig
   ├── include
   ├──── <grp_name>_mgmt.h
   ├──── <grp_name>_mgmt_callbacks.h
   └── src
   └──── <grp_name>_mgmt.c

请注意,上游Zephyr MCUmgr处理程序中的头文件位于 ``zephyr/include/zephyr/mgmt/mcumgr/grp/<grp_name>_mgmt`` 目录中,以允许应用程序全局包含这些文件 (Note that the header files in upstream Zephyr MCUmgr handlers reside in the ``zephyr/include/zephyr/mgmt/mcumgr/grp/<grp_name>_mgmt`` directory to allow the files to be globally included by applications)。

初始头文件 <grp_name>_mgmt.h (Initial header <grp_name>_mgmt.h)
================================================================

头文件的目的是提供MCUmgr处理程序本身和应用程序代码可以使用的定义,例如引用用于执行函数的命令ID (The purpose of the header file is to provide defines which can be used by the MCUmgr handler itself and application code, e.g. to reference the command IDs for executing functions)。示例文件类似于 (An example file would look similar to):

.. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/example_as_module/include/example_mgmt.h
   :language: c
   :linenos:

这为2个命令 ``test`` 和 ``other`` 提供了定义,并设置了SMP版本2错误响应(每个组具有唯一的错误代码,而不是返回 :c:enum:`mcumgr_err_t` 的传统SMP版本1错误响应 (This provides the defines for 2 command ``test`` and ``other`` and sets up the SMP version 2 error responses (which have unique error codes per group as opposed to the legacy SMP version 1 error responses that return a :c:enum:`mcumgr_err_t`) - 应始终有一个值为0的OK错误代码和一个值为1的未知错误代码 (there should always be an OK error code with the value 0 and an unknown error code with the value 1)。上面的示例然后添加了一个值为2的错误代码 ``not wanted`` (The above example then adds an error code of ``not wanted`` with value 2)。此外,组ID设置为 :c:enumerator:`MGMT_GROUP_ID_PERUSER`,这是用户定义组的起始组ID (In addition, the group ID is set to be :c:enumerator:`MGMT_GROUP_ID_PERUSER`, which is the start group ID for user-defined groups),请注意组ID需要是唯一的,因此其他自定义组应使用不同的值,可以使用中央索引头文件(如上游Zephyr所拥有的)来更轻松地分配组ID (note that group IDs need to be unique so other custom groups should use different values, a central index header file (as upstream Zephyr has) can be used to distribute group IDs more easily)。

初始头文件 <grp_name>_mgmt_callbacks.h (Initial header <grp_name>_mgmt_callbacks.h)
===================================================================================

头文件的目的是提供MCUmgr处理程序本身和应用程序代码可以使用的定义,例如引用用于执行函数的命令ID (The purpose of the header file is to provide defines which can be used by the MCUmgr handler itself and application code, e.g. to reference the command IDs for executing functions)。示例文件类似于 (An example file would look similar to):

.. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/example_as_module/include/example_mgmt_callbacks.h
   :language: c
   :linenos:

这设置了一个单一事件,应用程序(或模块)代码可以注册该事件以在执行函数处理程序时接收回调,这允许更改处理程序的流程(即返回错误而不是继续) (This sets up a single event which application (or module) code can register for to receive a callback when the function handler is executed, which allows the flow of the handler to be changed (i.e. to return an error instead of continuing))。事件组ID设置为 :c:enumerator:`MGMT_EVT_GRP_USER_CUSTOM_START`,这是用户定义组的起始事件ID (The event group ID is set to :c:enumerator:`MGMT_EVT_GRP_USER_CUSTOM_START`, which is the start event ID for user-defined groups),请注意事件ID需要是唯一的,因此其他自定义组应使用不同的值,可以使用中央索引头文件(如上游Zephyr所拥有的)来更轻松地分配事件ID (note that event IDs need to be unique so other custom groups should use different values, a central index header file (as upstream Zephyr has) can be used to distribute event IDs more easily)。

初始源文件 <grp_name>_mgmt.c (Initial source <grp_name>_mgmt.c)
================================================================

此源文件的目的是处理传入的MCUmgr命令、提供响应并向MCUmgr注册传输,以便将命令发送到它 (The purpose of this source file is to handle the incoming MCUmgr commands, provide responses, and register the transport with MCUmgr so that commands will be sent to it)。示例文件类似于 (An example file would look similar to):

.. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/example_as_module/src/example_mgmt.c
   :language: c
   :linenos:

上述代码创建了2个函数处理程序,``test`` 支持读取请求并需要2个必需参数,``other`` 支持写入请求并需要1个可选参数 (The above code creates 2 function handlers, ``test`` which supports read requests and takes 2 required parameters, and ``other`` which supports write requests and takes 1 optional parameter),此函数处理程序具有可选的通知回调功能,允许代码的其他部分监听事件并采取必要的操作或通过返回错误来阻止进一步执行函数 (this function handler has an optional notification callback feature that allows other parts of the code to listen for the event and take any required actions that are necessary or prevent further execution of the function by returning an error),有关MCUmgr回调功能的更多详细信息,请参见 :ref:`mcumgr_callbacks` (further details on MCUmgr callback functionality can be found on :ref:`mcumgr_callbacks`)。

请注意,引用自定义MCUmgr处理程序回调的其他代码需要包含基本Zephyr回调包含文件和自定义处理程序回调文件,仅在包含上游Zephyr回调头文件时包含树内Zephyr处理程序头 (Note that other code referencing callbacks for custom MCUmgr handlers needs to include both the base Zephyr callback include file and the custom handler callback file, only in-tree Zephyr handler headers are included when including the upstream Zephyr callback header file)。

初始Kconfig (Initial Kconfig)
==============================

Kconfig文件的目的是提供用户可以启用或更改的与正在实现的处理程序功能相关的选项 (The purpose of the Kconfig file is to provide options which users can enable or change relating to the functionality of the handler being implemented)。示例文件类似于 (An example file would look similar to):

.. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/Kconfig
   :language: kconfig

初始CMakeLists.txt (Initial CMakeLists.txt)
============================================

CMakeLists.txt文件由构建系统使用,用于设置要编译的文件、添加包含目录并指定可以更改的选项 (The CMakeLists.txt file is used by the build system to setup files to compile, include directories to add and specify options that can be changed)。如果启用了Kconfig选项,基本文件只需包含源文件 (A basic file only need to include the source files if the Kconfig options are enabled)。示例文件类似于 (An example file would look similar to):

.. tabs::

   .. group-tab:: Zephyr module

      .. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/example_as_module/CMakeLists.txt
         :language: cmake

   .. group-tab:: Application

      .. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/CMakeLists.txt
         :language: cmake
         :start-after: Include handler files

从应用程序包含 (Including from application)
********************************************

可以通过创建/编辑应用程序构建文件来添加特定于应用程序的MCUmgr处理程序 (Application-specific MCUmgr handlers can be added by creating/editing application build files)。
下面显示了示例修改 (Example modifications are shown below)。

示例CMakeLists.txt (Example CMakeLists.txt)
============================================

应用程序 ``CMakeLists.txt`` 文件可以通过添加以下内容来加载示例MCUmgr处理程序的CMake文件 (The application ``CMakeLists.txt`` file can load the CMake file for the example MCUmgr handler by adding the following):

.. code-block:: cmake

    add_subdirectory(mcumgr/grp/<grp_name>)

示例Kconfig (Example Kconfig)
==============================

应用程序Kconfig文件可以通过在应用程序目录中的 ``Kconfig`` 文件中添加以下内容(如果不存在则创建它)来包含示例MCUmgr处理程序的Kconfig文件 (The application Kconfig file can include the Kconfig file for the example MCUmgr handler by adding the following to the ``Kconfig`` file in the application directory (or creating it if it does not exist)):

.. code-block:: kconfig

    rsource "mcumgr/grp/<grp_name>/Kconfig"

    # Include Zephyr's Kconfig
    source "Kconfig.zephyr"

从Zephyr模块包含 (Including from Zephyr Module)
************************************************

Zephyr :ref:`modules` 可用于将自定义MCUmgr处理程序添加到多个不同的应用程序,而无需在每个应用程序的源树中复制代码 (Zephyr :ref:`modules` can be used to add custom MCUmgr handlers to multiple different applications without needing to duplicate the code in each application's source tree),有关如何设置模块文件的详细信息,请参见 :ref:`module-yml` (see :ref:`module-yml` for details on how to set up the module files)。下面显示了示例文件 (Example files are shown below)。

示例zephyr/module.yml (Example zephyr/module.yml)
==================================================

这是一个示例文件,可用于从模块目录的根目录加载Kconfig和CMake文件,并将放置在 ``zephyr/module.yml`` (This is an example file which can be used to load the Kconfig and CMake files from the root of the module directory, and would be placed at ``zephyr/module.yml``):

.. code-block:: yaml

    build:
      kconfig: Kconfig
      cmake: .

示例CMakeLists.txt (Example CMakeLists.txt)
============================================

这是一个示例CMakeLists.txt文件,它加载示例MCUmgr处理程序的CMake文件,并将放置在 ``CMakeLists.txt`` (This is an example CMakeLists.txt file which loads the CMake file for the example MCUmgr handler, and would be placed at ``CMakeLists.txt``):

.. code-block:: cmake

    add_subdirectory(mcumgr/grp/<grp_name>)

示例Kconfig (Example Kconfig)
==============================

这是一个示例Kconfig文件,它加载示例MCUmgr处理程序的Kconfig文件,并将放置在 ``Kconfig`` (This is an example Kconfig file which loads the Kconfig file for the example MCUmgr handler, and would be placed at ``Kconfig``):

.. code-block:: kconfig

    rsource "mcumgr/grp/<grp_name>/Kconfig"

演示处理程序 (Demonstration handler)
************************************

有一个演示项目,包含应用程序和zephyr模块MCUmgr处理程序的配置,可用作创建您自己的处理程序的基础,位于 :zephyr_file:`tests/subsys/mgmt/mcumgr/handler_demo/` (There is a demonstration project which includes configuration for both application and zephyr module-MCUmgr handlers which can be used as a basis for created your own in :zephyr_file:`tests/subsys/mgmt/mcumgr/handler_demo/`)。
