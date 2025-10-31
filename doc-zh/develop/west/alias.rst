.. _west-aliases:

West 别名
########

West 允许向本地、全局或系统配置文件添加别名命令。这些别名可以轻松添加快捷方式以应对频繁使用或难以记忆的命令，便于开发。

类似于 ``git`` 别名的工作方式，别名命令被替换为别名的完整文本，并解析为新的 shell 参数列表（内部使用 Python 函数 `shlex.split()`_ 来分割值）。这使得可以添加参数参数，就像它们被传递到原始命令一样。空格被视为参数分隔符；如果参数不应被分割，请使用适当的转义。

.. _shlex.split(): https://docs.python.org/3/library/shlex.html#shlex.split

要添加新别名，只需调用 ``west config`` 命令：

.. code-block:: shell

   west config alias.mylist "list -f '{name} {revision}'"

要列出别名，请使用 :samp:`west help {some_alias}`。

允许递归别名，因为别名命令可以包含其他别名，有效地构建更复杂但容易记忆的命令。

可以覆盖现有命令，例如传递默认参数：

.. code-block:: shell

   west config alias.update "update -o=--depth=1 -n"

.. warning::

   覆盖/遮蔽其他或内置命令是一个高级用例，可能导致奇怪的副作用，应谨慎进行。

示例
----

向全局配置添加 ``west run`` 和 ``west menuconfig`` 快捷方式以调用 ``west build`` 及相应的 CMake 目标：

.. code-block:: shell

   west config --global alias.run "build --pristine=never --target run"
   west config --global alias.menuconfig "build --pristine=never --target menuconfig"

为正在积极开发的示例创建别名，包含其他选项：

.. code-block:: shell

   west config alias.sample "build -b native_sim samples/hello_world -t run -- -DCONFIG_ASSERT=y"

覆盖 ``west update`` 以检查本地缓存：

.. code-block:: shell

   west config alias.update "update --path-cache $HOME/.cache/zephyrproject"

运行 :ref:`Twister <twister_script>` 时自动排除 32 位本机模拟器目标（通过 west）。这在没有 32 位主机 C 库的主机系统上运行时特别有用（如 Linux/AArch64）：

.. code-block:: shell

   west config alias.twister "twister --exclude-platform native_sim/native"
