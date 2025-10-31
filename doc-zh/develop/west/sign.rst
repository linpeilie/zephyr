.. _west-sign:

签署二进制文件
##############

``west sign`` :ref:`扩展 <west-extensions>` 命令可用于签署 Zephyr 应用二进制文件，供使用外部工具的引导加载程序使用。在某些配置中，``west sign`` 也用于调用外部后处理工具，该工具"缝合"图像的最终组件。运行 ``west sign -h`` 获取命令行帮助。

rimage
******

rimage 配置使用不依赖于 Kconfig 或 CMake 的方法，而是依赖于 :ref:`west config<west-config>`，类似于 :ref:`west-building-cmake-config`。

签署涉及许多相互堆叠的"包装器"脚本：``west flash`` 调用 ``west build``，它调用 ``cmake`` 和 ``ninja``，它们调用 ``west sign``，它调用 ``imgtool`` 或 `rimage`_。只要所需的签署参数是默认参数且相当静态，这些间接方式就不是问题。另一方面，通过所有这些层传递 ``imgtool`` 或 ``rimage`` 选项会导致这些层不抽象任何东西时的典型问题。首先，这通常需要在每层中进行样板代码。通过所有包装器引用空格或其他特殊字符可能很困难。重现较低的 ``west sign`` 命令来调试某些构建时间问题可能非常耗时：它至少需要启用和搜索详细构建日志以查找使用了哪些确切选项。从构建日志复制这些选项可能不可靠：由于微妙的环境差异，它可能产生不同的结果。最后和最坏的情况：新的签署特性和选项是不可能使用的，直到更多的样板代码被添加到每一层。

要避免这些问题，``rimage`` 参数可以在 ``west config`` 中设置。这是一个 ``workspace/.west/config`` 示例：

.. code-block:: ini

   [sign]
   # 从 CMake 调用时不需要
   tool = rimage

   [rimage]
   # 引用是可选的，像在 Unix shell 中一样工作
   # 当 rimage 可以在默认 PATH 中找到时不需要
   path = "/home/me/zworkspace/build-rimage/rimage"

   # 使用默认开发密钥时不需要
   extra-args = -i 4 -k 'keys/key argument with space.pem'

为了支持引用，值由 Python 的 ``shlex.split()`` 解析，如在 :ref:`west-building-cmake-args` 中。

``extra-args`` 直接传递给 ``rimage`` 命令。上面的示例与在命令行后附加它们的效果相同，如下所示：``west sign --tool rimage -- -i 4 -k 'keys/key argument with space.pem'``。如果都使用了，命令行参数最后出现。

.. _rimage:
   https://github.com/thesofproject/rimage

silabs_commander
*****************

``silabs_commander`` 工具用于为 Silicon Labs 设备应用签署、MIC 或加密二进制文件。当 ``sign.tool`` 配置设置为 ``silabs_commander`` 时，或当设置 ``CONFIG_SIWX91X_SIGN_KEY`` 或 ``CONFIG_SIWX91X_MIC_KEY`` 时，可以由 ``west sign`` 或 ``west build`` 调用。

如果设置了 ``CONFIG_SIWX91X_SIGN_KEY`` 或 ``CONFIG_SIWX91X_MIC_KEY`` 中的一个，``west flash`` 将自动刷写二进制文件的已签署版本。

``silabs_commander`` 需要在主机上安装 `Simplicity Commander`_。设备上密钥的置备在 `UG574 SiWx917 SoC Manufacturing Utility User Guide`_ 中描述。

.. _Simplicity Commander:
   https://www.silabs.com/developer-tools/simplicity-studio/simplicity-commander?tab=downloads
.. _UG574 SiWx917 SoC Manufacturing Utility User Guide:
   https://www.silabs.com/documents/public/user-guides/ug574-siwx917-soc-manufacturing-utility-user-guide.pdf
