.. _external_module_zenoh_pico:

zenoh-pico
##########

简介
************

`zenoh-pico`_ 是 `Eclipse Zenoh`_ 的实现，针对受限设备设计，提供了原生 C API。
它为嵌入式系统和微控制器提供零开销发布/订阅、存储/查询和计算能力。

zenoh-pico 统一了数据动态、数据静态和计算，同时保持了远超主流协议栈的时间和空间效率。
它与主要的 Rust Zenoh 实现完全兼容，提供了大多数功能的轻量实现。

zenoh-pico 以 Eclipse Public License 2.0 和 Apache License 2.0 双重许可。

与 Zephyr 配合使用
*****************

zenoh-pico 仓库是一个 Zephyr :ref:`module <modules>`，为 Zephyr 应用提供分布式通信能力。
它支持 UDP（单播和多播）和 TCP 传输层，支持 IPv4、IPv6 和 6LoWPAN 网络，
支持 WiFi、以太网、Thread 和串行数据链路层。

要将 zenoh-pico 作为 Zephyr 模块引入，可以在 ``west.yaml`` 中将其作为 West 工程添加，
或通过添加子清单（例如 ``zephyr/submanifests/zenoh-pico.yaml``）并包含以下内容后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: zenoh-pico
         url: https://github.com/eclipse-zenoh/zenoh-pico.git
         revision: main
         path: modules/lib/zenoh-pico # adjust the path as needed

更多使用说明与 API 文档，请参阅 `zenoh-pico documentation` 以及提供的 `Zephyr examples`_。

参考资料
**********

.. target-notes::

.. _zenoh-pico:
   https://github.com/eclipse-zenoh/zenoh-pico

.. _Eclipse Zenoh:
   https://zenoh.io

.. _zenoh-pico documentation:
   https://zenoh-pico.readthedocs.io/en/latest/

.. _Zephyr examples:
   https://github.com/eclipse-zenoh/zenoh-pico/tree/main/examples/zephyr
