.. _api_overview:.. _api_overview:



API 概述API 概述

###################



下表列出了 Zephyr 的 API 及其信息，包括它们当前的 :ref:`稳定性等级 <api_lifecycle>`。该表列出了 Zephyr 的 API 及其相关信息,包括它们当前的 :ref:`稳定性级别 <api_lifecycle>`。有关主要版本之间 API 更改的更多详细信息,请参阅 :ref:`zephyr_release_notes`。

有关主要版本之间 API 变化的更多详细信息，请参阅 :ref:`zephyr_release_notes`。

版本列使用 `语义版本 <https://semver.org/>`_,并具有以下预期:

版本列使用 `semantic version <https://semver.org/>`_，并具有以下期望：

 * 主版本号为零 (0.y.z) 用于初始开发。任何内容都可能随时更改。公共 API 不应被视为稳定。

 * 主版本零（0.y.z）用于初始开发。任何东西都可能随时改变。公共 API 不应被认为是稳定的。

   * 如果次版本号不超过一 (0.1.z),API 被视为 :ref:`实验性 <api_lifecycle_experimental>`。

   * 如果次版本最多为 1（0.1.z），API 被认为是 :ref:`experimental <api_lifecycle_experimental>`。   * 如果次版本号大于一 (0.y.z | y > 1),API 被视为 :ref:`不稳定 <api_lifecycle_unstable>`。

   * 如果次版本大于 1（0.y.z | y > 1），API 被认为是 :ref:`unstable <api_lifecycle_unstable>`。

 * 版本 1.0.0 定义了公共 API。此版本发布后版本号的递增方式取决于此公共 API 及其变化方式。

 * 版本 1.0.0 定义了公共 API。版本号在此发布后如何递增取决于此公共 API 及其变化方式。

   * 主版本号等于或大于一 (x.y.z | x >= 1 ) 的 API 被视为 :ref:`稳定 <api_lifecycle_stable>`。

   * 主版本等于或大于 1 的 API（x.y.z | x >= 1）被认为是 :ref:`stable <api_lifecycle_stable>`。   * Zephyr 中所有现有的稳定 API 将从版本 1.0.0 开始。

   * Zephyr 中的所有现有稳定 API 都将以版本 1.0.0 开头。

 * 如果仅引入向后兼容的错误修复,则必须递增修订版本号 Z (x.y.Z | x > 0)。错误修复定义为修复不正确行为的内部更改。

 * 补丁版本 Z（x.y.Z | x > 0）必须在仅引入向后兼容的错误修复时递增。

   错误修复定义为修复不正确行为的内部更改。 * 如果向公共 API 引入新的向后兼容功能,则必须递增次版本号 Y (x.Y.z | x > 0)。如果任何公共 API 功能被标记为已弃用,则必须递增。如果在私有代码中引入了实质性的新功能或改进,则可以递增。它可以包括修订级别的更改。当次版本号递增时,修订版本号必须重置为 0。



 * 次版本 Y（x.Y.z | x > 0）必须在向公共 API 引入新的向后兼容功能时递增。 * 如果对 API 进行了破坏兼容性的更改,则必须递增主版本号 X (x.Y.z | x > 0)。

   如果任何公共 API 功能被标记为已弃用，它也必须递增。在私有代码中引入实质性新功能或改进时，它可能会递增。

   它可能包括补丁级别的更改。当次版本递增时，补丁版本必须重置为 0。.. note::

   现有 API 的版本最初是根据 API 的当前状态设置的:

 * 主版本 X（X.Y.z | x > 0）必须在对 API 进行兼容性破坏更改时递增。

    - 0.1.0 表示 :ref:`实验性 <api_lifecycle_experimental>` API

.. note::    - 0.8.0 表示 :ref:`不稳定 <api_lifecycle_unstable>` API,

   现有 API 的版本最初是根据 API 的当前状态设置的：    - 最后 1.0.0 表示 :ref:`稳定 <api_lifecycle_stable>` API。



    - 0.1.0 表示 :ref:`experimental <api_lifecycle_experimental>` API   将来对 API 的更改将需要遵循上述指南调整版本。

    - 0.8.0 表示 :ref:`unstable <api_lifecycle_unstable>` API

    - 最后 1.0.0 表示 :ref:`stable <api_lifecycle_stable>` API

.. api-overview-table::

   将来对 API 的更改需要根据上述指南调整版本。


.. api-overview-table::
