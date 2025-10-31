.. _external_module_cannectivity:

CANnectivity USB 转 CAN 适配器固件
########################################

简介
************

`CANnectivity`_ 是一个用于通用串行总线（USB）到控制器局域网（CAN）适配器的开源固件。

该固件实现了 Geschwister Schneider USB/CAN 设备协议（通常称为 “gs_usb”）。
该协议受到 Linux 内核 SocketCAN 的 `gs_usb driver`_、`python-can`_ 以及众多其他软件包的支持。

该固件基于 Zephyr RTOS，可将你常用的微控制器开发板变成功能完善的 USB 转 CAN 适配器。

CANnectivity 以 Apache-2.0 许可证发布。

与 Zephyr 配合使用
*****************

CANnectivity 固件仓库是一个 Zephyr :ref:`module <modules>`，这使得其组件（例如 “gs_usb” 协议实现）
可以在 CANnectivity 固件应用之外复用。

要将 CANnectivity 作为 Zephyr 模块引入，可以在 ``west.yaml`` 中将其添加为一个 West 工程，
或通过添加一个子清单（例如 ``zephyr/submanifests/cannectivity.yaml``）并包含以下内容后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: cannectivity
         url: https://github.com/CANnectivity/cannectivity.git
         revision: main
         path: custom/cannectivity # adjust the path as needed

当 CANnectivity 作为 Zephyr 模块添加后，可以在 CANnectivity 固件应用之外通过包含其头文件来复用 “gs_usb” 的实现：

.. code-block:: c

   #include <cannectivity/usb/class/gs_usb.h>

API 详情请参阅该头文件。

.. _CANnectivity:
   https://github.com/CANnectivity/cannectivity

.. _gs_usb driver:
   https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/can/usb/gs_usb.c

.. _python-can:
   https://python-can.readthedocs.io/en/stable/interfaces/gs_usb.html
