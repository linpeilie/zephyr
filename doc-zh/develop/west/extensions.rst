.. _west-extensions:

扩展
####

West 是"可插拔的"：可以向 west 添加自己的命令，而无需编辑其源代码。这些称为 **west 扩展命令**，或简称"扩展"。扩展在 ``west --help`` 输出中以定义它们的项目的特殊部分显示。本页提供关于 west 扩展命令的一般信息，并包含编写自己扩展的教程。

在使用 west 与 Zephyr 时可以运行的某些命令，如用于 :ref:`构建、刷写和调试 <west-build-flash-debug>` 的命令和 :ref:`此处描述 <west-zephyr-ext-cmds>` 的命令，都是扩展。这就是为什么它们的帮助在 ``west --help`` 中显示如下：

.. code-block:: none

   commands from project at "zephyr":
     completion:           显示 shell 完成脚本
     boards:               显示有关受支持开发板的信息
     build:                编译 Zephyr 应用
     sign:                 为引导加载程序链加载签署 Zephyr 二进制文件
     flash:                在开发板上刷写并运行二进制文件
     debug:                交互式调试 Zephyr 应用
     debugserver:          连接到开发板并启动调试服务器
     attach:               交互式调试开发板

有关实现细节，请参见 :file:`zephyr/scripts/west-commands.yml` 和 :file:`zephyr/scripts/west_commands` 目录。

禁用扩展命令
***********

要禁用扩展命令支持，请将 ``commands.allow_extensions`` :ref:`配置 <west-config>` 选项设置为 ``false``。要在任何时候运行 west 时全局设置此选项，请使用：

.. code-block:: console

   west config --global commands.allow_extensions false

如果需要，可以在特定的 :term:`west 工作区` 中重新启用它们：

.. code-block:: console

   west config --local commands.allow_extensions true

请注意，包含扩展命令的文件只有在显式运行命令时才会被 west 导入。有关详细信息，请参见下文。

添加 West 扩展
**************

添加自己的扩展有三个步骤：

#. 编写实现命令的代码。
#. 将其信息添加到 :file:`west-commands.yml` 文件。
#. 确保 :file:`west-commands.yml` 文件在 :term:`west 清单` 中被引用。

请注意，west 会忽略名称与内置命令相同的扩展命令。

第 1 步：实现命令
================

创建一个 Python 文件来包含命令实现（有关当前支持的 Python 版本详情，请参见 `west PyPI 页面`_ 上的"Meta > Requires"信息）。可以将其放在 :term:`west 清单` 跟踪的任何项目中的任何位置，或清单仓库本身。此文件必须包含 ``west.commands.WestCommand`` 类的子类；当运行扩展时，此类将被实例化和使用。

以下是可用于开始的基本框架。它包含 ``WestCommand`` 的子类，具有所有抽象方法的实现。有关可以使用的 west API 的更多详细信息，请参见 :ref:`west-apis`。

.. code-block:: py

   '''my_west_extension.py

   west 扩展的基本示例。'''

   from textwrap import dedent            # 仅用于更好的代码缩进

   from west.commands import WestCommand  # 扩展必须继承此类

   class MyCommand(WestCommand):

       def __init__(self):
           super().__init__(
               'my-command-name',  # 存储为 self.name
               'one-line help for what my-command-name does',  # self.help
               # self.description:
               dedent('''
               关于 my-command 的多行描述。

               可以将其分成多个段落，它们会为您重新换行。
               也可以在下面调用 parser_adder.add_parser() 时
               传递 formatter_class=argparse.RawDescriptionHelpFormatter
               如果想保留行尾。'''))

       def do_add_parser(self, parser_adder):
           # 这是一些样板代码，允许完全控制所需的 argparse 处理类型。
           # "parser_adder" 参数是 argparse.ArgumentParser.add_subparsers() 的返回值。
           parser = parser_adder.add_parser(self.name,
                                            help=self.help,
                                            description=self.description)

           # 使用标准 argparse 模块 API 添加一些示例选项。
           parser.add_argument('-o', '--optional', help='一个可选参数')
           parser.add_argument('required', help='一个必需参数')

           return parser           # 存储为 self.parser

       def do_run(self, args, unknown_args):
           # 当用户运行命令时调用，例如：
           #
           #   $ west my-command-name -o FOO BAR
           #   --optional is FOO
           #   required is BAR
           self.inf('--optional is', args.optional)
           self.inf('required is', args.required)

可以忽略 ``do_run()`` 的第二个参数（上面的 ``unknown_args``），因为 ``WestCommand`` 默认会拒绝未知参数。如果想接收未知参数列表，请将 ``accepts_unknown_args=True`` 添加到 ``super().__init__()`` 参数。

第 2 步：添加或更新 :file:`west-commands.yml`
=============================================

现在需要将 :file:`west-commands.yml` 文件添加到项目中，以向 west 描述扩展。

以下是上述类定义的示例，假设它在项目根目录的 :file:`my_west_extension.py` 中：

.. code-block:: yaml

   west-commands:
     - file: my_west_extension.py
       commands:
         - name: my-command-name
           class: MyCommand
           help: one-line help for what my-command-name does

此 YAML 文件的顶级是具有 ``west-commands`` 键的映射。键的值是"命令描述符"序列。每个命令描述符给出实现 west 扩展的文件的位置，以及这些扩展的名称，以及可选的定义它们的类的名称（如果未给出，``class`` 值默认为与 ``name`` 相同的内容）。

此文件中的某些信息与 Python 代码中的定义重复。这是因为 west 在用户运行 ``west my-command-name`` 之前不会导入 :file:`my_west_extension.py`，因为：

- 它允许用户从不可信来源使用清单运行 ``west update``，然后使用其他 west 命令而不导入代码。由于导入 Python 模块相当于 shell 等效，这提供了一些安心。

- 这是一个小的优化，因为代码只有在需要时才会导入。

因此，除非显式运行命令，west 只会加载 :file:`west-commands.yml` 文件来获取在 ``west --help`` 输出等中向用户显示扩展信息所需的基本信息。

如果有多个扩展，或想跨多个文件分割扩展，:file:`west-commands.yml` 会如下所示：

.. code-block:: yaml

   west-commands:
     - file: my_west_extension.py
       commands:
         - name: my-command-name
           class: MyCommand
           help: one-line help for what my-command-name does
     - file: another_file.py
       commands:
         - name: command2
           help: another cool west extension
         - name: a-third-command
           class: ThirdCommand
           help: a third command in the same file as command2

上面：

- :file:`my_west_extension.py` 定义带有类 ``MyCommand`` 的扩展 ``my-command-name``
- :file:`another_file.py` 定义两个扩展：

  #. ``command2`` 与类 ``command2``
  #. ``a-third-command`` 与类 ``ThirdCommand``

有关描述 :file:`west-commands.yml` 内容的架构，请参见 `west 仓库`_ 中的文件 :file:`west-commands-schema.yml`。

第 3 步：更新清单
=================

最后，需要在 west 清单中指定刚刚编辑的 :file:`west-commands.yml` 的位置。如果扩展在项目中，如下所示添加它：

.. code-block:: yaml

   manifest:
      # [... 其他内容 ...]

      projects:
        - name: your-project
          west-commands: path/to/west-commands.yml
        # [... 其他项目 ...]

其中 :file:`path/to/west-commands.yml` 相对于项目的根目录。请注意，虽然鼓励使用名称 :file:`west-commands.yml`，但这只是一个约定；如果需要，可以给文件起其他名称。

或者，如果扩展在清单仓库中，只需在清单的 ``self`` 部分执行相同操作，如下所示：

.. code-block:: yaml

   manifest:
     # [... 其他内容 ...]

     self:
       west-commands: path/to/west-commands.yml

就是这样；现在可以运行 ``west my-command-name``。命令的名称、帮助和包含其代码的项目现在也会在 ``west --help`` 输出中显示。如果与其他人共享更新的仓库，他们也能使用它。

.. _west PyPI 页面:
   https://pypi.org/project/west/

.. _west 仓库:
   https://github.com/zephyrproject-rtos/west/
