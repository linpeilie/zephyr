.. _vscode_ide:

Visual Studio Code
##################

`Visual Studio Code`_ (简称 VS Code)是一个流行的跨平台 IDE,支持 C 项目并拥有丰富的扩展集。

本指南描述了在 VS Code 中为 Zephyr 的 :zephyr:code-sample:`blinky` 示例设置 VS Code 的过程。

这些说明已在 Linux 上测试过,但对于 macOS 和 Windows,步骤应该是相同的,只需确保根据需要调整路径。

获取 VS Code
************

`下载 VS Code`_ 并安装。

通过左侧面板中的 :guilabel:`Extensions` 市场安装所需的扩展。搜索 `C/C++ Extension Pack`_ 并安装它。

初始化新工作区
**************

本指南详细介绍了如何配置 :zephyr:code-sample:`blinky` 示例应用程序,但对于任何 Zephyr 项目和 :ref:`工作区布局 <west-workspaces>`,说明都是类似的。

开始之前,请确保您按照 :ref:`getting_started` 中的说明拥有一个可工作的 Zephyr 开发环境。

在 VS Code 中打开项目
*********************

#. 在 VS Code 中,从主菜单中选择 :menuselection:`File --> Open Folder`。

#. 导航到您的 Zephyr 工作区并选择它(即,如果您按照入门说明操作,则为 HOME 目录中的 :file:`zephyrproject` 文件夹)。

#. 如果出现提示,请启用工作区信任。

生成编译命令
************

为了支持代码导航和 linting 功能,您必须编译一次项目以生成 :file:`compile_commands.json` 文件,该文件将为 C/C++ 扩展提供所需信息(例如 include 路径)。您可以从 VS Code 嵌入式终端执行此操作;从顶部菜单或命令面板 (:kbd:`Ctrl+Shift+P`) 中选择 :menuselection:`Terminal --> New Terminal`,然后输入:

.. code-block:: console

   $ cd zephyr
   $ west build -p always -b native_sim/native/64


配置 C/C++ 扩展
***************

现在,您需要指向生成的 :file:`compile_commands.json` 文件以在 VS Code 中启用 linting 和代码导航。

#. 在 VS Code 顶部菜单中转到 :menuselection:`File --> Preferences --> Settings`。

#. 搜索参数 :guilabel:`C_Cpp > Default: Compile Commands` 并将其值设置为: ``zephyr/build/compile_commands.json``。

   代码中的 linting 错误现在应该得到解决,您应该能够浏览代码。

附加资源
********

在使用 Zephyr 和 VS Code 时,还有许多其他扩展可能很有用。虽然本指南尚未涵盖它们,但您可以参考它们的文档进行设置:

贡献工具
========

- `Checkpatch Extension`_
- `EditorConfig Extension`_

文档语言扩展
============

- `reStructuredText Extension Pack`_

IDE 扩展
========

- `CMake Extension documentation`_
- `nRF Kconfig Extension`_
- `nRF DeviceTree Extension`_
- `GNU Linker Map files Extension`_

附加指南
========

- `How to Develop Zephyr Apps with a Modern, Visual IDE`_

.. note::

   请注意,这些扩展可能并非都具有相同的质量和维护水平。

.. _Visual Studio Code: https://code.visualstudio.com/
.. _下载 VS Code: https://code.visualstudio.com/Download
.. _VS Code documentation: https://code.visualstudio.com/docs
.. _C/C++ Extension Pack: https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools-extension-pack
.. _C/C++ Extension documentation: https://code.visualstudio.com/docs/languages/cpp
.. _CMake Extension documentation: https://code.visualstudio.com/docs/cpp/cmake-linux

.. _Checkpatch Extension: https://marketplace.visualstudio.com/items?itemName=idanp.checkpatch
.. _EditorConfig Extension: https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig

.. _reStructuredText Extension Pack: https://marketplace.visualstudio.com/items?itemName=lextudio.restructuredtext-pack

.. _nRF Kconfig Extension: https://marketplace.visualstudio.com/items?itemName=nordic-semiconductor.nrf-kconfig
.. _nRF DeviceTree Extension: https://marketplace.visualstudio.com/items?itemName=nordic-semiconductor.nrf-devicetree
.. _GNU Linker Map files Extension: https://marketplace.visualstudio.com/items?itemName=trond-snekvik.gnu-mapfiles

.. _How to Develop Zephyr Apps with a Modern, Visual IDE: https://github.com/beriberikix/zephyr-vscode-example
