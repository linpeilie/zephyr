.. _contribute_to_zephyr:.. _contribute_to_zephyr:



为Zephyr做出贡献Contributing to Zephyr

############################################



来自社区的贡献是项目的支柱。无论是提交代码、改进文档还是提出新功能，Contributions from the community are the backbone of the project. Whether it is by submitting code,

您的努力都非常值得赞赏。本页列出了有用的资源和指南，帮助您完成贡献之旅。improving documentation, or proposing new features, your efforts are highly appreciated. This page

lists useful resources and guidelines to help you in your contribution journey.

总体指南

==================General Guidelines

==================

.. toctree::

   :maxdepth: 1.. toctree::

   :hidden:   :maxdepth: 1

   :hidden:

   guidelines.rst

   contributor_expectations.rst   guidelines.rst

   reviewer_expectations.rst   contributor_expectations.rst

   coding_guidelines/index.rst   reviewer_expectations.rst

   style/index.rst   coding_guidelines/index.rst

   proposals_and_rfcs.rst   style/index.rst

   modifying_contributions.rst   proposals_and_rfcs.rst

   modifying_contributions.rst



:ref:`contribute_guidelines`

   了解为Zephyr项目做出贡献的总体流程和指南。:ref:`contribute_guidelines`

   Learn about the overall process and guidelines for contributing to the Zephyr project.

   对于首次贡献者来说，本页是必读内容，因为它包含重要信息，

   说明如何确保您的贡献可以被考虑纳入项目并可能被合并。   This page is a mandatory read for first-time contributors as it contains important information on

   how to ensure your contribution can be considered for inclusion in the project and potentially

:ref:`contributor-expectations`   merged.

   这是另一份必读文档，描述了项目*所有*贡献者的预期行为。

:ref:`contributor-expectations`

:ref:`reviewer-expectations`   This document is another mandatory read that describes the expected behavior of *all*

   这是另一份必读文档，描述了审查项目贡献时的预期行为。   contributors to the project.



:ref:`coding_guidelines`:ref:`reviewer-expectations`

   代码贡献应遵循一套编码指南，以确保代码库的一致性和可读性。   This document is another mandatory read that describes the expected behavior when revieweing

   contributions to the project.

:ref:`coding_style`

   代码贡献应遵循一套样式指南，以确保代码库的一致性和可读性。:ref:`coding_guidelines`

   Code contributions are expected to follow a set of coding guidelines to ensure consistency and

:ref:`rfcs`   readability across the code base.

   了解何时以及如何为项目的新功能和更改提交RFC（征求意见）。

:ref:`coding_style`

:ref:`modifying_contributions`   Code contributions are expected to follow a set of style guidelines to ensure consistency and

   修改其他开发人员的贡献以及如何处理过时拉取请求的指南。   readability across the code base.



文档:ref:`rfcs`

=============   Learn when and how to submit RFCs (Request for Comments) for new features and changes to the

   project.

Zephyr项目依赖于良好的文档。无论是作为代码贡献的一部分还是作为独立工作，

贡献文档对项目特别有价值。:ref:`modifying_contributions`

   Guidelines for modifying contributions made by other developers and how to deal with stale pull

.. toctree::   requests.

   :maxdepth: 1

   :hidden:Documentation

=============

   documentation/guidelines.rst

   documentation/generation.rstThe Zephyr project thrives on good documentation. Whether it is as part of a code contribution or

as a standalone effort, contributing documentation is particularly valuable to the project.

:ref:`doc_guidelines`

   本页提供了使用reStructuredText（reST）标记语言和Sphinx文档生成器.. toctree::

   编写文档的一些简单指南。   :maxdepth: 1

   :hidden:

:ref:`zephyr_doc`

   在编写文档时，查看渲染后的效果会很有帮助。   documentation/guidelines.rst

   documentation/generation.rst

   本页描述了如何在本地构建Zephyr文档。

:ref:`doc_guidelines`

   This page provides some simple guidelines for writing documentation using the reSTructuredText

处理外部组件   (reST) markup language and Sphinx documentation generator.

================================

:ref:`zephyr_doc`

.. toctree::   As you write documentation, it can be helpful to see how it will look when rendered.

   :maxdepth: 1

   :hidden:   This page describes how to build the Zephyr documentation locally.



   external.rst

   bin_blobs.rstDealing with external components

================================

:ref:`external-contributions`

   对Zephyr有用的基本功能或特性可能在其他开源项目中已经可用，.. toctree::

   建议并鼓励重用此类代码。本页更详细地描述了何时以及如何将外部源代码   :maxdepth: 1

   导入Zephyr。   :hidden:



:ref:`external-tooling`   external.rst

   同样，在编译、代码分析、测试或模拟期间使用的外部工具可能是有益的，   bin_blobs.rst

   本节将对此进行介绍。

:ref:`external-contributions`

:ref:`bin-blobs`   Basic functionality or features that would make useful addition to Zephyr might be readily

   由于某些功能可能只能通过以二进制形式分发的可执行代码提供，   available in other open source projects, and it is recommended and encouraged to reuse such code.

   本页描述了向项目 :ref:`贡献二进制blob <blobs-process>` 的流程和指南。   This page describes in more details when and how to import external source code into Zephyr.



需要帮助吗？:ref:`external-tooling`

========================   Similarly, external tooling used during compilation, code analysis, testing or simulation, can be

   beneficial and is covered in this section.

如果您对贡献流程有疑问，Zephyr社区随时为您提供帮助。

您可以加入我们的 Discord_ 频道或使用 `开发者邮件列表`_。:ref:`bin-blobs`

   As some functionality might only be made available with the help of executable code distributed

   in binary form, this page describes the process and guidelines for :ref:`contributing binary

.. _Discord: https://chat.zephyrproject.org   blobs <blobs-process>` to the project.

.. _开发者邮件列表: https://lists.zephyrproject.org/g/devel

Need help along the way?
========================

If you have questions related to the contribution process, the Zephyr community is here to help.
You may join our Discord_ channel or use the `Developer Mailing List`_.


.. _Discord: https://chat.zephyrproject.org
.. _Developer Mailing List: https://lists.zephyrproject.org/g/devel
