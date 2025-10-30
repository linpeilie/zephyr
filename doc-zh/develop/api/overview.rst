.. _api_overview:

API 概述
############

该表列出了 Zephyr 的 API 及其相关信息,包括它们当前的 :ref:`稳定性级别 <api_lifecycle>`。有关主要版本之间 API 更改的更多详细信息,请参阅 :ref:`zephyr_release_notes`。

版本列使用 `语义版本 <https://semver.org/>`_,并具有以下预期:

 * 主版本号为零 (0.y.z) 用于初始开发。任何内容都可能随时更改。公共 API 不应被视为稳定。

   * 如果次版本号不超过一 (0.1.z),API 被视为 :ref:`实验性 <api_lifecycle_experimental>`。
   * 如果次版本号大于一 (0.y.z | y > 1),API 被视为 :ref:`不稳定 <api_lifecycle_unstable>`。

 * 版本 1.0.0 定义了公共 API。此版本发布后版本号的递增方式取决于此公共 API 及其变化方式。

   * 主版本号等于或大于一 (x.y.z | x >= 1 ) 的 API 被视为 :ref:`稳定 <api_lifecycle_stable>`。
   * Zephyr 中所有现有的稳定 API 将从版本 1.0.0 开始。

 * 如果仅引入向后兼容的错误修复,则必须递增修订版本号 Z (x.y.Z | x > 0)。错误修复定义为修复不正确行为的内部更改。

 * 如果向公共 API 引入新的向后兼容功能,则必须递增次版本号 Y (x.Y.z | x > 0)。如果任何公共 API 功能被标记为已弃用,则必须递增。如果在私有代码中引入了实质性的新功能或改进,则可以递增。它可以包括修订级别的更改。当次版本号递增时,修订版本号必须重置为 0。

 * 如果对 API 进行了破坏兼容性的更改,则必须递增主版本号 X (x.Y.z | x > 0)。

.. note::
   现有 API 的版本最初是根据 API 的当前状态设置的:

    - 0.1.0 表示 :ref:`实验性 <api_lifecycle_experimental>` API
    - 0.8.0 表示 :ref:`不稳定 <api_lifecycle_unstable>` API,
    - 最后 1.0.0 表示 :ref:`稳定 <api_lifecycle_stable>` API。

   将来对 API 的更改将需要遵循上述指南调整版本。


.. api-overview-table::
