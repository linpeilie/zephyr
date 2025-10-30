.. _toolchain_iar_arm:

IAR Arm 工具链
##############

#. 在您的主机上下载并安装 `IAR Arm Toolchain`_ v9.70 或更新版本(IAR Embedded Workbench 或 IAR Build Tools,永久或订阅许可)

#. 确保您的主机上已安装 :ref:`Zephyr SDK <toolchain_zephyr_sdk>`。

#. :ref:`设置这些环境变量 <env_vars>`:

    - 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为 ``iar``。
    - 将 :envvar:`IAR_TOOLCHAIN_PATH` 设置为工具链安装目录。

#. IAR 工具链的云许可变体需要将 :envvar:`IAR_LMS_BEARER_TOKEN` 环境变量设置为有效的 ``许可证载体令牌``(订阅许可)。

例如:

.. code-block:: bash

    # Linux (默认安装路径):
    export IAR_TOOLCHAIN_PATH=/opt/iar/cxarm-<version>/arm
    export ZEPHYR_TOOLCHAIN_VARIANT=iar
    export IAR_LMS_BEARER_TOKEN="<BEARER-TOKEN>"

.. code-block:: batch

    # Windows:
    set IAR_TOOLCHAIN_PATH=c:\<path>\cxarm-<version>\arm
    set ZEPHYR_TOOLCHAIN_VARIANT=iar
    set IAR_LMS_BEARER_TOKEN="<BEARER-TOKEN>"

.. note::

    已知限制:

    - IAR 工具链使用 ``ilink`` 进行链接,并依赖于 Zephyr 的 CMAKE_LINKER_GENERATOR。``ilink`` 与 Zephyr 的链接器脚本模板不兼容,后者与 GNU ld 配合使用。

    - Zephyr SDK 分发的 GNU 汇编器用于 ``.S-files``。

    - C 库仅支持 ``Minimal libc``。不支持 C++。

    - 某些 Zephyr 子系统或模块可能包含依赖于 GNU 内部函数的 C 或汇编代码,尚未更新以完全支持 ``iar``。

    - 不支持 TrustedFirmware

.. _IAR Arm Toolchain: https://www.iar.com/products/architectures/arm/
