:orphan::orphan:



.. _zephyr_licensing:.. _zephyr_licensing:



Zephyr 项目组件的许可 (Licensing of Zephyr Project components)Licensing of Zephyr Project components

####################################################################################################



Zephyr 内核树导入或重用了一些不受 `Apache 2.0 许可证`_ 覆盖的软件包、脚本和其他文件。The Zephyr kernel tree imports or reuses packages, scripts and other files that

在某些地方没有 LICENSE 文件或无法放置 LICENSE 文件，因此我们在本文档中描述许可信息。are not covered by the `Apache 2.0 License`_. In some places

there is no LICENSE file or way to put a LICENSE file there, so we describe the

持续集成脚本 (Continuous Integration Scripts)licensing in this document.

----------------------------------------------

Continuous Integration Scripts

* *来源 (Origin):* Linux 内核 (Linux Kernel)------------------------------

* *许可 (Licensing):* `GPLv2 许可证`_

* *影响 (Impact):* 这些文件用于持续集成 (CI)，从不链接到固件中。* *Origin:* Linux Kernel

* *文件 (Files):** *Licensing:* `GPLv2 License`_

* *Impact:* These files are used in Continuous Integration (CI) and never linked into the firmware.

  * :zephyr_file:`scripts/checkpatch.pl`* *Files:*

  * :zephyr_file:`scripts/checkstack.pl`

  * :zephyr_file:`scripts/spelling.txt`  * :zephyr_file:`scripts/checkpatch.pl`

  * :zephyr_file:`scripts/checkstack.pl`

Coccinelle 脚本 (Coccinelle Scripts)  * :zephyr_file:`scripts/spelling.txt`

-------------------------------------

Coccinelle Scripts

  * *来源 (Origin):* Coccinelle------------------

  * *许可 (Licensing):* `GPLv2 许可证`_

  * *影响 (Impact):* 这些文件由 `Coccinelle`_ 使用，这是一个用于转换 C 代码的工具，从不链接到固件中。  * *Origin:* Coccinelle

  * *文件 (Files):*  * *Licensing:* `GPLv2 License`_

  * *Impact:* These files are used by `Coccinelle`_, a tool for transforming C-code, and never linked

    * :zephyr_file:`scripts/coccicheck`    into the firmware.

    * :zephyr_file:`scripts/coccinelle/array_size.cocci`  * *Files:*

    * :zephyr_file:`scripts/coccinelle/deref_null.cocci`

    * :zephyr_file:`scripts/coccinelle/deref_null.cocci`    * :zephyr_file:`scripts/coccicheck`

    * :zephyr_file:`scripts/coccinelle/deref_null.cocci`    * :zephyr_file:`scripts/coccinelle/array_size.cocci`

    * :zephyr_file:`scripts/coccinelle/mini_lock.cocci`    * :zephyr_file:`scripts/coccinelle/deref_null.cocci`

    * :zephyr_file:`scripts/coccinelle/mini_lock.cocci`    * :zephyr_file:`scripts/coccinelle/deref_null.cocci`

    * :zephyr_file:`scripts/coccinelle/mini_lock.cocci`    * :zephyr_file:`scripts/coccinelle/deref_null.cocci`

    * :zephyr_file:`scripts/coccinelle/noderef.cocci`    * :zephyr_file:`scripts/coccinelle/mini_lock.cocci`

    * :zephyr_file:`scripts/coccinelle/noderef.cocci`    * :zephyr_file:`scripts/coccinelle/mini_lock.cocci`

    * :zephyr_file:`scripts/coccinelle/returnvar.cocci`    * :zephyr_file:`scripts/coccinelle/mini_lock.cocci`

    * :zephyr_file:`scripts/coccinelle/semicolon.cocci`    * :zephyr_file:`scripts/coccinelle/noderef.cocci`

    * :zephyr_file:`scripts/coccinelle/noderef.cocci`

GCOV 覆盖率头文件 (GCOV Coverage Header File)    * :zephyr_file:`scripts/coccinelle/returnvar.cocci`

----------------------------------------------    * :zephyr_file:`scripts/coccinelle/semicolon.cocci`



* *来源 (Origin):* GCC，GNU 编译器集合 (GCC, the GNU Compiler Collection)GCOV Coverage Header File

* *许可 (Licensing):* `GPLv2 许可证`_ 带运行时库异常 (with Runtime Library Exception)-------------------------

* *影响 (Impact):* 此文件仅在启用 :kconfig:option:`CONFIG_COVERAGE_GCOV` 时链接到固件中。

* *文件 (Files):** *Origin:* GCC, the GNU Compiler Collection

* *Licensing:* `GPLv2 License`_ with Runtime Library Exception

  * :zephyr_file:`subsys/testsuite/coverage/coverage.h`* *Impact:* This file is only linked into the firmware if :kconfig:option:`CONFIG_COVERAGE_GCOV` is

  enabled.

ENE KB1200_EVB 开发板 OpenOCD 配置 (ENE KB1200_EVB Board OpenOCD Configuration)* *Files:*

--------------------------------------------------------------------------------

  * :zephyr_file:`subsys/testsuite/coverage/coverage.h`

* *许可 (Licensing):* `GPLv2 许可证`_

* *影响 (Impact):* 此文件在对 :zephyr:board:`kb1200_evb` 开发板进行编程和调试时由 `OpenOCD`_ 使用。ENE KB1200_EVB Board OpenOCD Configuration

  它从不链接到固件中。------------------------------------------

* *文件 (Files):*

* *Licensing:* `GPLv2 License`_

  * :zephyr_file:`boards/ene/kb1200_evb/support/openocd.cfg`* *Impact:* This file is used by `OpenOCD`_ when programming and debugging the

  :zephyr:board:`kb1200_evb` board. It is never linked into the firmware.

Thread-Metric RTOS 测试套件源文件 (Thread-Metric RTOS Test Suite Source Files)* *Files:*

--------------------------------------------------------------------------------

  * :zephyr_file:`boards/ene/kb1200_evb/support/openocd.cfg`

* *来源 (Origin):* ThreadX

* *许可 (Licensing):* `MIT 许可证`_Thread-Metric RTOS Test Suite Source Files

* *影响 (Impact):* 这些文件仅链接到 Thread-Metric RTOS 测试套件测试固件中。------------------------------------------

* *文件 (Files):*

* *Origin:* ThreadX

  * :zephyr_file:`tests/benchmarks/thread_metric/thread_metric_readme.txt`* *Licensing:* `MIT License`_

  * :zephyr_file:`tests/benchmarks/thread_metric/src/tm_api.h`* *Impact:* These files are only linked into the Thread-Metric RTOS Test Suite test firmware.

  * :zephyr_file:`tests/benchmarks/thread_metric/src/tm_basic_processing_test.c`* *Files:*

  * :zephyr_file:`tests/benchmarks/thread_metric/src/tm_cooperative_scheduling_test.c`

  * :zephyr_file:`tests/benchmarks/thread_metric/src/tm_interrupt_preemption_processing_test.c`  * :zephyr_file:`tests/benchmarks/thread_metric/thread_metric_readme.txt`

  * :zephyr_file:`tests/benchmarks/thread_metric/src/tm_interrupt_processing_test.c`  * :zephyr_file:`tests/benchmarks/thread_metric/src/tm_api.h`

  * :zephyr_file:`tests/benchmarks/thread_metric/src/tm_memory_allocation_test.c`  * :zephyr_file:`tests/benchmarks/thread_metric/src/tm_basic_processing_test.c`

  * :zephyr_file:`tests/benchmarks/thread_metric/src/tm_message_processing_test.c`  * :zephyr_file:`tests/benchmarks/thread_metric/src/tm_cooperative_scheduling_test.c`

  * :zephyr_file:`tests/benchmarks/thread_metric/src/tm_porting_layer.h`  * :zephyr_file:`tests/benchmarks/thread_metric/src/tm_interrupt_preemption_processing_test.c`

  * :zephyr_file:`tests/benchmarks/thread_metric/src/tm_porting_layer_zephyr.c`  * :zephyr_file:`tests/benchmarks/thread_metric/src/tm_interrupt_processing_test.c`

  * :zephyr_file:`tests/benchmarks/thread_metric/src/tm_preemptive_scheduling_test.c`  * :zephyr_file:`tests/benchmarks/thread_metric/src/tm_memory_allocation_test.c`

  * :zephyr_file:`tests/benchmarks/thread_metric/src/tm_synchronization_processing_test.c`  * :zephyr_file:`tests/benchmarks/thread_metric/src/tm_message_processing_test.c`

  * :zephyr_file:`tests/benchmarks/thread_metric/src/tm_porting_layer.h`

OpenThread Spinel HDLC RCP 主机接口文件 (OpenThread Spinel HDLC RCP Host Interface Files)  * :zephyr_file:`tests/benchmarks/thread_metric/src/tm_porting_layer_zephyr.c`

------------------------------------------------------------------------------------------  * :zephyr_file:`tests/benchmarks/thread_metric/src/tm_preemptive_scheduling_test.c`

  * :zephyr_file:`tests/benchmarks/thread_metric/src/tm_synchronization_processing_test.c`

* *来源 (Origin):* OpenThread

* *许可 (Licensing):* `BSD-3-clause`_OpenThread Spinel HDLC RCP Host Interface Files

* *影响 (Impact):* 这些文件仅在启用 :kconfig:option:`CONFIG_HDLC_RCP_IF` 时链接到固件中。-----------------------------------------------

* *文件 (Files)*:

* *Origin:* OpenThread

  * :zephyr_file:`modules/openthread/platform/hdlc_interface.hpp`* *Licensing:* `BSD-3-clause`_

  * :zephyr_file:`modules/openthread/platform/radio_spinel.cpp`* *Impact:* These files are only linked into the firmware if :kconfig:option:`CONFIG_HDLC_RCP_IF` is

  * :zephyr_file:`modules/openthread/platform/hdlc_interface.cpp`  enabled.

* *Files*:

Python Devicetree 库测试文件 (Python Devicetree library test files)

---------------------------------------------------------------------  * :zephyr_file:`modules/openthread/platform/hdlc_interface.hpp`

  * :zephyr_file:`modules/openthread/platform/radio_spinel.cpp`

* *许可 (Licensing):* `BSD-3-clause`_  * :zephyr_file:`modules/openthread/platform/hdlc_interface.cpp`

* *影响 (Impact):* 这些文件仅用于测试，从不与固件链接。

* *文件 (Files)*:Python Devicetree library test files

------------------------------------

  * ``scripts/dts/python-devicetree/tests`` 下的各种 yaml 文件

* *Licensing:* `BSD-3-clause`_

FUSE 接口定义头文件 (FUSE Interface Definition Header File)* *Impact:* These are only used for testing and never linked with the firmware.

-------------------------------------------------------------* *Files*:



* *许可 (Licensing):* `BSD-2-clause`_  * Various yaml files under ``scripts/dts/python-devicetree/tests``

* *影响 (Impact):* 此头文件仅在启用 :kconfig:option:`CONFIG_FUSE_CLIENT` 时在 Zephyr 构建中使用。

* *文件 (Files)*:FUSE Interface Definition Header File

--------------------------------------

  * :zephyr_file:`subsys/fs/fuse_client/fuse_abi.h`

* *Licensing:* `BSD-2-clause`_

.. _Apache 2.0 许可证:* *Impact:* This header is used in Zephyr build only if :kconfig:option:`CONFIG_FUSE_CLIENT` is enabled.

   https://github.com/zephyrproject-rtos/zephyr/blob/main/LICENSE* *Files*:



.. _GPLv2 许可证:  * :zephyr_file:`subsys/fs/fuse_client/fuse_abi.h`

   https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/COPYING

.. _Apache 2.0 License:

.. _MIT 许可证:   https://github.com/zephyrproject-rtos/zephyr/blob/main/LICENSE

  https://opensource.org/licenses/MIT

.. _GPLv2 License:

.. _BSD-3-clause:   https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/COPYING

   https://opensource.org/license/bsd-3-clause

.. _MIT License:

.. _BSD-2-clause:  https://opensource.org/licenses/MIT

   https://opensource.org/license/bsd-2-clause

.. _BSD-3-clause:

.. _Coccinelle:   https://opensource.org/license/bsd-3-clause

   https://coccinelle.gitlabpages.inria.fr/website/

.. _BSD-2-clause:

.. _OpenOCD:   https://opensource.org/license/bsd-2-clause

   https://openocd.org

.. _Coccinelle:
   https://coccinelle.gitlabpages.inria.fr/website/

.. _OpenOCD:
   https://openocd.org
