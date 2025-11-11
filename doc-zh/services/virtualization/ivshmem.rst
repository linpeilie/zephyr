.. _ivshmem_driver:

虚拟机间共享内存 (Inter-VM Shared Memory)
##########################################

.. contents::
   :local:
   :depth: 2

概述 (Overview)
***************

由于 Zephyr 能够在 Qemu 和 `ACRN <https://projectacrn.github.io/latest/tutorials/using_zephyr_as_uos.html>`_ 上作为客户操作系统运行,可能需要让虚拟机相互感知,或感知主机。这可以通过一个称为 ivshmem (虚拟机间共享内存) 的功能在各方之间公开共享内存来实现 (As Zephyr is enabled to run as a guest OS on Qemu and
`ACRN <https://projectacrn.github.io/latest/tutorials/using_zephyr_as_uos.html>`_
it might be necessary to make VMs aware of each other, or aware of the host.
This is made possible by exposing a shared memory among parties via a feature
called ivshmem, which stands for inter-VM Shared Memory)。

支持两种类型:普通共享内存 (ivshmem-plain) 或具有在另一个虚拟机上生成中断能力的共享内存,从而也可以被中断 (ivshmem-doorbell) (The two types are supported: a plain shared memory (ivshmem-plain) or a shared
memory with the ability for a VM to generate an interruption on another, and
thus to be interrupted as well itself (ivshmem-doorbell))。

请参阅官方 `Qemu ivshmem documentation
<https://www.qemu.org/docs/master/system/devices/ivshmem.html>`_ 以获取更多信息 (Please refer to the official `Qemu ivshmem documentation
<https://www.qemu.org/docs/master/system/devices/ivshmem.html>`_ for more information)。

支持 (Support)
**************

Zephyr 支持两个版本:普通版和门铃版。可以通过启用 :kconfig:option:`CONFIG_IVSHMEM` 来构建 Ivshmem 驱动程序。默认情况下,这将公开普通版本。需要启用 :kconfig:option:`CONFIG_IVSHMEM_DOORBELL` 才能获得门铃版本 (Zephyr supports both versions: plain and doorbell. Ivshmem driver can be built
by enabling :kconfig:option:`CONFIG_IVSHMEM`. By default, this will expose the plain
version. :kconfig:option:`CONFIG_IVSHMEM_DOORBELL` needs to be enabled to get the
doorbell version)。

因为门铃版本使用 MSI-X 向量来支持通知向量,所以必须将 :kconfig:option:`CONFIG_IVSHMEM_MSI_X_VECTORS` 调整为所需的向量数量 (Because the doorbell version uses MSI-X vectors to support notification vectors,
the :kconfig:option:`CONFIG_IVSHMEM_MSI_X_VECTORS` has to be tweaked to the number of
vectors that will be needed)。

请注意,可以通过启用 :kconfig:option:`CONFIG_IVSHMEM_SHELL` 来公开一个小型 shell 模块以测试 ivshmem 功能 (Note that a tiny shell module can be exposed to test the ivshmem feature by
enabling :kconfig:option:`CONFIG_IVSHMEM_SHELL`)。

ivshmem-v2
**********

Zephyr 也支持 ivshmem-v2 (Zephyr also supports ivshmem-v2):

https://github.com/siemens/jailhouse/blob/master/Documentation/ivshmem-v2-specification.md

这主要用于 Jailhouse 虚拟机管理程序中的 IPC (例如 :zephyr:code-sample:`eth-ivshmem`)。也可以通过构建 Siemens 的 QEMU 分支并修改 QEMU 启动标志来在没有 Jailhouse 的情况下使用 ivshmem-v2 (This is primarily used for IPC in the Jailhouse hypervisor
(e.g. :zephyr:code-sample:`eth-ivshmem`). It is also possible to use ivshmem-v2 without
Jailhouse by building the Siemens fork of QEMU, and modifying the QEMU launch flags):

https://github.com/siemens/qemu/tree/wip/ivshmem2

API 参考 (API Reference)
*************************

.. doxygengroup:: ivshmem
