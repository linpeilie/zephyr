.. _mac-setup-alts:.. _mac-setup-alts:



macOS 替代设置说明macOS alternative setup instructions

########################################################################



.. _mac-gatekeeper:.. _mac-gatekeeper:



关于 Gatekeeper 的重要说明Important note about Gatekeeper

**************************************************************



从 macOS 10.15 Catalina 开始,从 macOS Terminal 应用程序(或任何其他终端模拟器)Starting with macOS 10.15 Catalina, applications launched from the macOS

启动的应用程序受到与从 Dock 启动的应用程序相同的系统安全策略约束。这意味着,Terminal application (or any other terminal emulator) are subject to the same

如果您使用 Web 浏览器下载可执行二进制文件,macOS 默认不会让您从 Terminal 执行system security policies that are applied to applications launched from the

这些文件。为了解决这个问题,您可以采取两种不同的方法:Dock. This means that if you download executable binaries using a web browser,

macOS will not let you execute those from the Terminal by default. In order to

* 运行 ``xattr -r -d com.apple.quarantine /path/to/folder``,其中 get around this issue you can take two different approaches:

  ``path/to/folder`` 是您想要运行的可执行文件所在的封闭文件夹的路径。

* Run ``xattr -r -d com.apple.quarantine /path/to/folder`` where

* 打开 :menuselection:`系统偏好设置 --> 安全性与隐私 --> 隐私`,然后向下滚动  ``path/to/folder`` is the path to the enclosing folder where the executables

  到"开发者工具"。然后解锁锁定以进行更改,并选中与您选择的终端模拟器对应的复选框。  you want to run are located.

  这将适用于从该终端程序启动的任何可执行文件。

* Open :menuselection:`System Preferences --> Security and Privacy --> Privacy`

请注意,本节**不**适用于使用 Homebrew 安装的可执行文件,因为这些文件会被   and then scroll down to "Developer Tools". Then unlock the lock to be able to

``brew`` 本身自动取消隔离。但这对大多数 :ref:`toolchains` 来说是相关的。  make changes and check the checkbox corresponding to your terminal emulator of

  choice. This will apply to any executable being launched from such terminal

.. _macOS Gatekeeper: https://en.wikipedia.org/wiki/Gatekeeper_(macOS)  program.



MacPorts 用户的额外说明Note that this section does **not** apply to executables installed with

***********************************Homebrew, since those are automatically un-quarantined by ``brew`` itself. This

is however relevant for most :ref:`toolchains`.

虽然本指南不正式支持 MacPorts,但可以使用 MacPorts 代替 Homebrew 在 macOS 上

获取所有必需的依赖项。另请注意,您可能需要安装 ``rust`` 和 ``cargo`` 才能.. _macOS Gatekeeper: https://en.wikipedia.org/wiki/Gatekeeper_(macOS)

正确安装 Python 依赖项。

Additional notes for MacPorts users
***********************************

While MacPorts is not officially supported in this guide, it is possible to use
MacPorts instead of Homebrew to get all the required dependencies on macOS.
Note also that you may need to install ``rust`` and ``cargo`` for the Python
dependencies to install correctly.
