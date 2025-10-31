.. _devicetree_style:

设备树样式指南 (Devicetree Style Guidelines)
###########################################

  * 使用制表符缩进。
  * 制表符大小为 8 个字符。
  * 遵循设备树规范约定和规则。
  * 如果 Linux 内核规则在 `设备树源 (DTS) 编码风格 (Devicetree Sources (DTS) Coding Style)
    <https://docs.kernel.org/devicetree/bindings/dts-coding-style.html>`_
    中提出建议,这是 Zephyr 中也优先考虑的风格。
  * 如果有助于可读性,你可以通过用一个空行(两个换行符)分离它们,将相关属性组分成"段落"。
  * 为节点和属性名称使用破折号(``-``)作为单词分隔符。
  * 在节点标签中使用下划线(``_``)作为单词分隔符。
  * 在属性定义中的等号(``=``)两侧留一个空格。
  * 不要在缩进的 ``};`` 之前插入空行。
  * 在同一层级的节点之间插入一个空行。
  * 当将长属性值拆分跨多行时,在与开括号相同的行上指定第一个值(``<`` 或 ``[``)。
    在属性的最后一个值之后,将关闭括号和分号(``>;`` 或 ``];``)放在同一行上。

示例 (Examples):

.. literalinclude:: style-example.dts
  :language: devicetree
  :start-after: start-after-here
