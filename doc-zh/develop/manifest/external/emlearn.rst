.. _external_module_emlearn:

emlearn
#######

简介
************

`emlearn`_ 是一个开源库，用于在微控制器和嵌入式系统上部署机器学习模型。
它可以把使用 scikit-learn 或 Keras 训练得到的模型，生成可移植的 C 代码。

其 Python 库可以将复杂的机器学习模型转换为最小化的 C 代码表示，
从而使资源受限的嵌入式设备也能运行机器学习推理。

emlearn 以 MIT 许可证发布。

与 Zephyr 配合使用
*****************

emlearn 仓库是一个 Zephyr :ref:`module <modules>`，为 Zephyr 应用提供 TinyML 能力，
使得机器学习模型可以直接在运行 Zephyr 的设备上执行。

要将 emlearn 作为 Zephyr 模块引入，可以在 ``west.yaml`` 中把它添加为一个 West 工程，
或通过添加子清单（例如 ``zephyr/submanifests/emlearn.yaml``）并包含以下内容后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: emlearn
         url: https://github.com/emlearn/emlearn.git
         revision: master
         path: modules/lib/emlearn # adjust the path as needed

更多使用说明与 API 文档，请参阅 `emlearn documentation`_，尤其是 `Getting Started on Zephyr RTOS`_ 章节。

参考资料
**********

.. target-notes::

.. _emlearn:
   https://github.com/emlearn/emlearn

.. _emlearn documentation:
   https://emlearn.readthedocs.io/en/latest/

.. _Getting Started on Zephyr RTOS:
   https://emlearn.readthedocs.io/en/latest/getting_started_zephyr.html
