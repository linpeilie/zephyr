.. _toolchain_armclang:

Arm Compiler 6
##############

#. 为您的操作系统下载并安装包含 `Arm Compiler 6`_ 的开发套件。

#. :ref:`设置这些环境变量 <env_vars>`:

   - 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为 ``armclang``。
   - 将 :envvar:`ARMCLANG_TOOLCHAIN_PATH` 设置为工具链安装目录。

#. Arm Compiler 6 需要 :envvar:`ARMLMD_LICENSE_FILE` 环境变量指向您的许可证文件或服务器。

例如:

   .. code-block:: bash

      # Linux, macOS, 许可证文件:
      export ARMLMD_LICENSE_FILE=/<path>/license_armds.dat
      # Linux, macOS, 许可证服务器:
      export ARMLMD_LICENSE_FILE=8224@myserver

   .. code-block:: batch

      # Windows, 许可证文件:
      set ARMLMD_LICENSE_FILE=c:\<path>\license_armds.dat
      # Windows, 许可证服务器:
      set ARMLMD_LICENSE_FILE=8224@myserver

#. 如果 Arm Compiler 6 作为 Arm Development Studio 的一部分安装,那么您必须设置 :envvar:`ARM_PRODUCT_DEF` 指向产品定义文件:
   另请参阅: `Product and toolkit configuration <https://developer.arm.com/tools-and-software/software-development-tools/license-management/resources/product-and-toolkit-configuration>`_。
   例如,如果 Arm Development Studio 安装在 ``/opt/armds-2020-1`` 并使用 Gold 许可证,则将 :envvar:`ARM_PRODUCT_DEF` 设置为指向 ``/opt/armds-2020-1/gold.elmap``。

   .. note::

      Arm Compiler 6 使用 ``armlink`` 进行链接。这与 Zephyr 的链接器脚本模板不兼容,后者与 GNU ld 配合使用。Zephyr 的 Arm Compiler 6 支持 Zephyr 的 CMake 链接器脚本生成器,它支持生成分散文件。基本的分散文件支持已经到位,但 ld 模板中涵盖的某些区域尚未得到 CMake 链接器脚本生成器的完全支持。

      某些 Zephyr 子系统或模块还可能包含依赖于 GNU 内部函数的 C 或汇编代码,尚未更新以完全支持 ``armclang``。

.. _Arm Compiler 6: https://developer.arm.com/tools-and-software/embedded/arm-compiler/downloads/version-6
