.. _external_module_mender_mcu:

mender-mcu
##########

简介
************

`mender-mcu`_ 通过与 Zephyr 集成，为资源受限的设备提供稳健的固件更新能力。
它实现了一个更新模块接口，该接口允许模块定义如何处理更新的具体细节。
mender-mcu 提供了一个与 MCUboot 集成的默认更新模块，以提供 A/B 更新。
这使得微控制器单元（MCU）能够执行原子的、故障安全的 OTA 更新，包括故障时的自动回滚，
类似于 Mender 对 Linux 设备的更新。

该客户端与 Mender 服务器通信，以报告设备清单和身份、检查可用的更新、下载新固件，
并与更新模块协调以安全地安装更新。
Mender 服务器提供开源版本（Apache-2.0 许可证）和企业版本（商业许可证），
通过商业计划提供（本地部署和托管 Mender 完全托管服务）。

mender-mcu 以 Apache-2.0 许可证发布。

需求
************

* cJSON 用于 JSON 解析

与 Zephyr 配合使用
*****************

要将 mender-mcu 作为 Zephyr :ref:`module <modules>` 引入，可以在 ``west.yaml`` 中将其作为 West 工程添加，
或通过添加子清单（例如 ``zephyr/submanifests/mender-mcu.yaml``）并包含以下内容后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: mender-mcu
         url: https://github.com/mendersoftware/mender-mcu
         revision: main
         path: modules/mender-mcu # adjust the path as needed

更多使用说明与 API 文档，请参阅 `mender-mcu documentation`_。
`Zephyr reference project`_ 提供了一个示例参考集成。

参考资料
**********

.. target-notes::

.. _mender-mcu:
   https://github.com/mendersoftware/mender-mcu

.. _mender-mcu documentation:
   https://docs.mender.io/operating-system-updates-zephyr

.. _Zephyr reference project:
   https://github.com/mendersoftware/mender-mcu-integration
