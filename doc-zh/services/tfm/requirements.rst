TF-M 要求 (TF-M Requirements)
#############################

以下是一些可以与 TF-M 一起使用的开发板 (The following are some of the boards that can be used with TF-M):

.. list-table::
   :header-rows: 1

   * - 开发板 (Board)
     - NSPE 开发板名称 (NSPE board name)
   * - :ref:`mps2_an521_board`
     - ``mps2/an521/cpu0/ns`` (qemu supported)
   * - :ref:`mps3_board`
     -
       - ``mps3/corstone300/fvp/ns`` (armfvp supported)
       - ``mps3/corstone310/fvp/ns`` (armfvp supported)
   * - :zephyr:board:`mps4`
     -
       - ``mps4/corstone315/fvp/ns`` (armfvp supported)
       - ``mps4/corstone320/fvp/ns`` (armfvp supported)
   * - :zephyr:board:`bl5340_dvk`
     - ``bl5340_dvk/nrf5340/cpuapp/ns``
   * - :zephyr:board:`lpcxpresso55s69`
     - ``lpcxpresso55s69_ns``
   * - :ref:`nrf9160dk_nrf9160`
     - ``nrf9160dk/nrf9160/ns``
   * - :zephyr:board:`nrf5340dk`
     - ``nrf5340dk/nrf5340/cpuapp/ns``
   * - :zephyr:board:`b_u585i_iot02a`
     - ``b_u585i_iot02a/stm32u585xx/ns``
   * - :zephyr:board:`nucleo_l552ze_q`
     - ``nucleo_l552ze_q/stm32l552xx/ns``
   * - :zephyr:board:`stm32l562e_dk`
     - ``stm32l562e_dk/stm32l562xx/ns``
   * - :ref:`v2m_musca_b1_board`
     - ``v2m_musca_b1/musca_b1/ns``
   * - :ref:`v2m_musca_s1_board`
     - ``v2m_musca_s1/musca_s1/ns``

要确保某个开发板支持 TF-M，请在其默认配置中检查 :kconfig:option:`CONFIG_TRUSTED_EXECUTION_NONSECURE` 是否设置为 ``y`` (To make sure TF-M is supported for a board
in its output, check that :kconfig:option:`CONFIG_TRUSTED_EXECUTION_NONSECURE`
is set to ``y`` in that board's default configuration)。

软件要求 (Software Requirements)
*********************************

构建 TF-M 二进制文件时所需的 Python 模块列在 TF-M 仓库的 ``tools/requirements.txt`` 文件中 (The Python modules required when building TF-M binaries are listed in the
TF-M repository under ``tools/requirements.txt``)。

您可以通过以下方式安装它们 (You can install them via):

   .. code-block:: bash

      $ pip3 install -r "$(west list trusted-firmware-m -f '{abspath}')/tools/requirements.txt"

它们被 TF-M 的签名工具用来准备固件映像以供引导加载程序验证 (They are used by TF-M's signing utility to prepare firmware images for
validation by the bootloader)。

生成用于 QEMU 的二进制文件以及在某些平台上合并已签名的安全和非安全二进制文件的过程，还需要使用 ``srec_cat`` 工具 (Part of the process of generating binaries for QEMU and merging signed
secure and non-secure binaries on certain platforms also requires the use of
the ``srec_cat`` utility)。

在 Linux 上可以通过以下方式安装 (This can be installed on Linux via):

   .. code-block:: bash

      $ sudo apt-get install srecord

在 OS X 上可以通过以下方式安装 (And on OS X via):

   .. code-block:: bash

      $ brew install srecord

对于基于 Windows 的系统，请确保您的系统路径中有该工具的副本。例如，请参见 (For Windows-based systems, please make sure you have a copy of the utility
available on your system path. See, for example):
`SRecord for Windows <https://sourceforge.net/projects/srecord/files/srecord-win32>`_
