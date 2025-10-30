.. _stm32cube_ide:

STM32CubeIDE
############

STM32CubeIDE_ 是 STMicroelectronics 推出的基于 Eclipse 的集成开发环境,专为 STM32 系列 MCU 和 MPU 设计。

本指南描述了使用 IDE 设置、构建和调试 Zephyr 应用程序的过程。

必须已经使用 Zephyr 和 west 创建了一个项目。

这些说明已在 Linux 上使用 IDE 版本 1.16.0 验证有效。

项目设置
********

#. 开始之前,请确保您按照 :ref:`getting_started` 中的说明拥有一个可工作的 Zephyr 开发环境。

#. 从 Zephyr 环境运行 STM32CubeIDE。示例:

   .. code-block::

      $ /opt/st/stm32cubeide_1.16.0/stm32cubeide

#. 通过转到 :menuselection:`File --> New --> STM32 CMake Project` 打开您已存在的项目:

   .. figure:: img/stm32cube_new_cmake.webp
      :align: center
      :alt: 创建新的 CMake 项目

#. 选择 :guilabel:`Project with existing CMake sources`,然后单击 :guilabel:`Next`。

#. 选择 :menuselection:`Next` 并浏览到源代码位置。打开的文件夹应包含 ``CMakeLists.txt`` 和 ``prj.conf`` 文件。

#. 选择 :menuselection:`Next` 并选择适当的 MCU。按 :guilabel:`Finish`,您的项目现在应该可用了。但是,为了正确配置它,还必须执行更多操作。

#. 右键单击工作区中新创建的项目,然后选择 :guilabel:`Properties`。

#. 转到 :guilabel:`C/C++ Build` 页面并将 Generator 设置为 ``Ninja``。在 :guilabel:`Other Options` 中,以 CMake 参数格式指定目标 ``BOARD``。如果目标是树外开发板,还必须设置 ``BOARD_ROOT`` 选项。生成的设置页面应类似于:

   .. figure:: img/stm32cube_project_properties.webp
      :align: center
      :alt: 项目属性对话框

   根据您是否有树外项目,可能需要或不需要这些选项。

#. 转到 :menuselection:`C/C++ General --> Preprocessor Include` 页面。选择 :guilabel:`GNU C` 语言,然后单击 :menuselection:`CDT User Settings Entries` 选项。

   .. figure:: img/stm32cube_preprocessor_include.webp
      :align: center
      :alt: 预处理器选项的属性对话框

   单击 :guilabel:`Add` 添加指向 Zephyr 的 ``autoconf.h`` 的 :guilabel:`Include File`,该文件位于 ``<build dir>/zephyr/include/generated/autoconf.h``。这将确保 STM32CubeIDE 获取 Zephyr 配置选项。将显示以下对话框。按如下方式填写:

   .. figure:: img/stm32cube_add_include.webp
      :align: center
      :alt: 添加 include 文件对话框

   添加 include 文件后,您的属性页面应类似于以下内容:

   .. figure:: img/stm32cube_autoconf_h.webp
      :align: center
      :alt: 添加 autoconf.h 文件后的属性页面

#. 单击 :guilabel:`Apply and Close`

#. 您现在可以使用工具栏上的 :guilabel:`Build` 按钮构建项目。可以使用 :guilabel:`Run` 按钮运行项目,也可以使用 :guilabel:`Debug` 按钮进行调试。

仅调试
******

如果您只想使用 STM32CubeIDE 调试项目,可以按以下方式进行:

#. 首先,确保编译项目并拥有可用的 ``zephyr.elf``。

#. 运行 STM32CubeIDE 并通过转到 :menuselection:`File --> Import...` 导入项目:

   .. figure:: img/stm32cube_menu_import.webp
      :align: center
      :alt: 导入项目

#. 选择 :menuselection:`C/C++ --> STM32 Cortex-M Executable`,然后单击 :guilabel:`Next`:

   .. figure:: img/stm32cube_import_project.webp
      :align: center
      :alt: 导入项目选择

#. 单击 :guilabel:`Browse` 浏览到您的构建文件夹并选择您的 ``zephyr.elf``。

#. 单击 :guilabel:`Select` 选择您的 MCU。如果相关,还要选择您的 CPU 和/或核心。

#. 单击 :guilabel:`Finish`。

#. 现在可以使用 :guilabel:`Debug` 按钮调试项目。

故障排除
********

配置项目时,您看到类似以下的错误:

.. code-block::

  Error message: Traceback (most recent call last):

    File "/path/to/zephyr/scripts/list_boards.py", line 11, in <module>
      import pykwalify.core

  ModuleNotFoundError: No module named 'pykwalify'


这意味着您没有在 Zephyr 环境中启动 IDE。您必须删除 ``config_default`` 构建目录并再次启动 STM32CubeIDE,确保您可以在启动 STM32CubeIDE 的 shell 中运行 ``west``。

.. _STM32CubeIDE: https://www.st.com/en/development-tools/stm32cubeide.html
