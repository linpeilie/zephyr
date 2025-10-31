.. _external_module_wolfssl:

wolfSSL
#######

简介
************

wolfSSL 是一个轻量级、可移植的 SSL/TLS 库，针对嵌入式系统、RTOS 环境和资源受限设备进行了优化。
它提供了一系列加密功能和安全通信协议（支持到 TLS 1.3 和 DTLS 1.3）以及后量子密码学支持。
其对多种构建配置的支持使其适用于利用 Zephyr RTOS 的广泛应用和硬件平台。

wolfSSL 支持 Zephyr 网络栈，因此应用程序可以使用 wolfSSL API 与网络上的其他设备或服务建立安全连接。

wolfSSL 以 GPLv3 和商业许可证双重许可。

GitHub 仓库：`wolfSSL Repository`_

与 Zephyr 配合使用
*****************

在你的 west.yml 中将 wolfssl 添加为一个项目：

.. code-block:: yaml

  manifest:
    remotes:
    # <your other remotes>
    - name: wolfssl
      url-base: https://github.com/wolfssl
  projects:
    # <your other projects>
    - name: wolfssl
      path: modules/crypto/wolfssl
      revision: master
      remote: wolfssl

更新 west 的模块：

.. code-block:: bash

   west update

现在 west 识别 ``wolfssl`` 作为一个模块，并将其 Kconfig 和 CMakeLists.txt 包含在构建系统中。

关于在 Zephyr 中使用 wolfSSL 的更多信息，请参阅 `wolfSSL Zephyr Example Usage`_。

关于 Zephyr 中的应用代码示例，请参阅 `wolfSSL NXP AppCodeHub`_。

关于 wolfSSL API 文档，请参阅 `wolfSSL Documentation`_。

参考资料
*********

.. target-notes::

.. _wolfssl Repository:
    https://github.com/wolfSSL/wolfssl

.. _wolfSSL Zephyr Example Usage:
    https://github.com/wolfSSL/wolfssl/blob/master/zephyr/README.md#build-and-run-wolfcrypt-benchmark-application

.. _wolfSSL NXP AppCodeHub:
    https://github.com/wolfSSL/nxp-appcodehub

.. _wolfSSL Documentation:
    https://www.wolfssl.com/docs/
