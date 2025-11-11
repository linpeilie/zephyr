.. _zdsp_api:

数字信号处理(DSP) (Digital Signal Processing (DSP))
#####################################################

.. contents::
    :local:
    :depth: 2

DSP API提供了一种架构无关的信号处理方式 (The DSP API provides an architecture agnostic way for signal processing)。
目前,该API可在任何架构上工作,但可能未经过优化 (Currently, the API will work on any architecture but will likely not be optimized)。各种架构的状态如下所示 (The status of the various architectures can be found below):

============ =============
架构         状态
(Architecture) (Status)
============ =============
ARC          已优化 (Optimized)
ARM          已优化 (Optimized)
ARM64        已优化 (Optimized)
MIPS         未优化 (Unoptimized)
POSIX        未优化 (Unoptimized)
RISCV        未优化 (Unoptimized)
RISCV64      未优化 (Unoptimized)
SPARC        未优化 (Unoptimized)
X86          未优化 (Unoptimized)
XTENSA       未优化 (Unoptimized)
============ =============

使用zDSP (Using zDSP)
**********************

zDSP提供各种后端选项,这些选项会自动为应用程序选择 (zDSP provides various backend options which are selected automatically for the application)。默认情况下,包含CMSIS模块将使所有架构都能使用zDSP API (By default, including the CMSIS module will enable all architectures to use the zDSP APIs)。这可以通过设置来完成 (This can be done by setting)::

	CONFIG_CMSIS_DSP=y

如果您的应用程序需要一些额外的自定义 (If your application requires some additional customization),可以启用 :kconfig:option:`CONFIG_DSP_BACKEND_CUSTOM` (it's possible to enable :kconfig:option:`CONFIG_DSP_BACKEND_CUSTOM`),这意味着应用程序负责提供zDSP库的实现 (which means that the application is responsible for providing the implementation of the zDSP library)。

为您的架构优化 (Optimizing for your architecture)
**************************************************

如果您的架构显示为 ``未优化`` (If your architecture is showing as ``Unoptimized``),可以添加新的zDSP后端以更好地支持它 (it's possible to add a new zDSP backend to better support it)。为此,应在 :file:`subsys/dsp/Kconfig` 中添加新的Kconfig选项 (To do that, a new Kconfig option should be added to :file:`subsys/dsp/Kconfig`),以及所需的依赖项和为 ``DSP_BACKEND`` Kconfig选项设置的 ``default`` (along with the required dependencies and the ``default`` set for ``DSP_BACKEND`` Kconfig choice)。

接下来,应在 ``subsys/dsp/<backend>/`` 添加实现 (Next, the implementation should be added at ``subsys/dsp/<backend>/``),并在 :file:`subsys/dsp/CMakeLists.txt` 中链接 (and linked in at :file:`subsys/dsp/CMakeLists.txt`)。要添加特定于架构的属性 (To add architecture-specific attributes),应将其相应的Kconfig选项添加到 :file:`subsys/dsp/Kconfig` (its corresponding Kconfig option should be added to :file:`subsys/dsp/Kconfig`),并使用它们更新 :file:`include/zephyr/dsp/dsp.h` 中的 ``DSP_DATA`` 和 ``DSP_STATIC_DATA`` (and use them to update ``DSP_DATA`` and ``DSP_STATIC_DATA`` in :file:`include/zephyr/dsp/dsp.h`)。

API参考 (API Reference)
************************

.. doxygengroup:: math_dsp

.. _subsys/dsp/Kconfig: https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/dsp/Kconfig
.. _subsys/dsp/CMakeLists.txt: https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/dsp/CMakeLists.txt
.. _include/zephyr/dsp/dsp.h: https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/dsp/dsp.h
