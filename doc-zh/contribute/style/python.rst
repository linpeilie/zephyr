.. _python_style:

Python 样式指南 (Python Style Guidelines)
##########################################

Python 应该按照 `PEP 8`_ 的合规方式进行格式化。Zephyr 使用 `ruff 格式化工具 (ruff formatter)`_
来实现这一点。这个自以为是的格式化工具旨在实现一致性、通用性、可读性和减少 git diffs。

要应用格式化工具,请运行:

.. code-block:: shell

   ruff check --select I --fix <file> # Sort imports
   ruff format <file>

Ruff 配置 (Ruff configuration)
****************************

在默认值之上应用一小组选项:

* 行长度为 100 列或更少。
* 单引号 ``'`` 和双引号 ``"`` 引用风格都是允许的。
* 行尾将转换为 ``\n``。Unix 上的默认行尾。

被排除的文件 (Excluded files)
****************************

格式化工具在 CI 中被强制执行,但仅对新添加的 Python 文件,
因为在引入此工具时项目已经有很大的 Python 代码库。
:zephyr_file:`.ruff-excludes.toml` 文件有一个 ``[format]`` 部分,
其中列出了当前被排除的所有文件。建议贡献者在更改被排除的文件时,
将其从列表中删除并在单独的提交中对其进行格式化。

.. _PEP 8:
   https://peps.python.org/pep-0008/

.. _ruff formatter:
   https://docs.astral.sh/ruff/formatter/
