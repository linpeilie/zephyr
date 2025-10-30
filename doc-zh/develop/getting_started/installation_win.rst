.. _win-setup-alts:.. _win-setup-alts:



Windows 替代设置说明Windows alternative setup instructions

############################################################################



.. _win-wsl:.. _win-wsl:



Windows 10 WSL (适用于 Linux 的 Windows 子系统)Windows 10 WSL (Windows Subsystem for Linux)

****************************************************************************************



如果您运行的是最新版本的 Windows 10,您可以利用内置功能在标准命令提示符上If you are running a recent version of Windows 10 you can make use of the

直接原生运行 Ubuntu 二进制文件。这允许您使用诸如 :ref:`Zephyr SDK <toolchain_zephyr_sdk>` built-in functionality to natively run Ubuntu binaries directly on a standard

之类的软件,而无需设置虚拟机。command-prompt. This allows you to use software such as the :ref:`Zephyr SDK

<toolchain_zephyr_sdk>` without setting up a virtual machine.

.. warning::

      Windows 10 版本 1803 存在一个问题,会导致 CMake 无法正常工作,该问题.. warning::

      已在版本 1809(及更高版本)中修复。更多信息可以在       Windows 10 version 1803 has an issue that will cause CMake to not work

      :github:`Zephyr Issue 10420 <10420>` 中找到。      properly and is fixed in version 1809 (and later).

      More information can be found in :github:`Zephyr Issue 10420 <10420>`.

#. `安装适用于 Linux 的 Windows 子系统 (WSL)`_。

#. `Install the Windows Subsystem for Linux (WSL)`_.

   .. note::

         为了使 Zephyr SDK 正常工作,您需要 Windows 10 build 15002 或更高版本。   .. note::

         您可以在系统设置的"关于电脑"部分检查您运行的是哪个 Windows 10 build。         For the Zephyr SDK to function properly you will need Windows 10

         如果您运行的是较旧的 Windows 10 build,可能需要安装创意者更新。         build 15002 or greater. You can check which Windows 10 build you are

         running in the "About your PC" section of the System Settings.

#. 请遵循 :ref:`installation_linux` 文档中的 Ubuntu 说明。         If you are running an older Windows 10 build you might need to install

         the Creator's Update.

.. NOTE FOR DOCS AUTHORS: as a reminder, do *NOT* put dependencies for building

   the documentation itself here.#. Follow the Ubuntu instructions in the :ref:`installation_linux` document.



.. _安装适用于 Linux 的 Windows 子系统 (WSL): https://msdn.microsoft.com/en-us/commandline/wsl/install_guide.. NOTE FOR DOCS AUTHORS: as a reminder, do *NOT* put dependencies for building

   the documentation itself here.

.. _Install the Windows Subsystem for Linux (WSL): https://msdn.microsoft.com/en-us/commandline/wsl/install_guide
