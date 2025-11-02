.. _cpptest:


Parasoft C/C++test 支持
##########################

Parasoft 的 `C/C++test <https://www.parasoft.com/products/parasoft-c-ctest/>`__ 是一款用于 C/C++ 的软件测试与静态分析工具。它是商业软件，需获取商业许可证才能使用。

有关 C/C++test 的文档请参阅 https://docs.parasoft.com/，其中包含使用说明。

生成构建数据文件
***************************

要使用 C/C++test，系统的 :envvar:`PATH` 环境变量中必须包含 ``cpptestscan`` 可执行文件。并且在调用 :ref:`west build <west-building>` 时需要添加 ``-DZEPHYR_SCA_VARIANT=cpptest`` 参数，例如：

.. code-block:: shell

    west build -b qemu_cortex_m3 zephyr/samples/hello_world -- -DZEPHYR_SCA_VARIANT=cpptest


将会生成一个 ``.bdf`` 文件，位于 :file:`build/sca/cpptest/cpptestscan.bdf`。

生成报告文件
************************

有关更多细节，请参考 Parasoft C/C++test 的官方文档。

要导入并生成报告文件，类似下面的命令通常可行：

.. code-block:: shell

    cpptestcli -data out -localsettings local.conf -bdf build/sca/cpptest/cpptestscan.bdf -config "builtin://Recommended Rules" -report out/report


可能需要将 ``bdf.import.c.compiler.exec``、``bdf.import.cpp.compiler.exec`` 和
``bdf.import.linker.exec`` 设置为用于构建的工具链（参见 :ref:`west build <west-building>`）。
