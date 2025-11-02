.. _sparse:

is a static code analysis tool.

Sparse 支持
##############

`Sparse <https://www.kernel.org/doc/html/latest/dev-tools/sparse.html>`__ 是一个静态代码分析工具。
除了常见的代码分析功能外，Sparse 还支持 ``address_space`` 属性，允许在 C 代码中引入不同的地址空间，并验证不同地址空间的指针不会相互混淆。此外，它还支持用于在不同地址空间之间进行指针转换的 ``force`` 属性。目前 Zephyr 引入了一个名为 ``__cache`` 的自定义地址空间，用于标识 Xtensa 架构上缓存地址范围的指针。这有助于识别缓存地址与非缓存地址混淆的情形。

使用 sparse 运行
*******************

要运行 Sparse 验证构建，请在调用 :ref:`west build <west-building>` 时传递 ``-DZEPHYR_SCA_VARIANT=sparse`` 参数，例如：

.. code-block:: shell

    west build -d hello -b intel_adsp/cavs25 zephyr/samples/hello_world -- -DZEPHYR_SCA_VARIANT=sparse
