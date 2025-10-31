.. _contribute_to_zephyr:.. _contribute_to_zephyr:.. _contribute_to_zephyr:



对 Zephyr 的贡献 (Contributing to Zephyr)

#######################################

为Zephyr做出贡献Contributing to Zephyr

来自社区的贡献是项目的支柱。无论是通过提交代码、改进文档还是提议新功能,

你的努力都受到高度赞赏。此页面列出了有用的资源和指南,以帮助你完成贡献之旅。############################################



一般指南 (General Guidelines)

===========================

来自社区的贡献是项目的支柱。无论是提交代码、改进文档还是提出新功能，Contributions from the community are the backbone of the project. Whether it is by submitting code,

.. toctree::

   :maxdepth: 1您的努力都非常值得赞赏。本页列出了有用的资源和指南，帮助您完成贡献之旅。improving documentation, or proposing new features, your efforts are highly appreciated. This page

   :hidden:

lists useful resources and guidelines to help you in your contribution journey.

   guidelines.rst

   contributor_expectations.rst总体指南

   reviewer_expectations.rst

   coding_guidelines/index.rst==================General Guidelines

   style/index.rst

   proposals_and_rfcs.rst==================

   modifying_contributions.rst

.. toctree::



:ref:`contribute_guidelines`   :maxdepth: 1.. toctree::

   了解对 Zephyr 项目的贡献过程和指南。

   :hidden:   :maxdepth: 1

   对于首次贡献者,这是必读的页面,因为它包含关于如何确保你的贡献能够被考虑纳入项目

   并可能被合并的重要信息。   :hidden:



:ref:`contributor-expectations`   guidelines.rst

   这份文件是另一份必读材料,描述了项目所有贡献者的预期行为。

   contributor_expectations.rst   guidelines.rst

:ref:`reviewer-expectations`

   这份文件是另一份必读材料,描述了审查项目贡献时的预期行为。   reviewer_expectations.rst   contributor_expectations.rst



:ref:`coding_guidelines`   coding_guidelines/index.rst   reviewer_expectations.rst

   代码贡献应遵循一套编码指南以确保整个代码库中的一致性和可读性。

   style/index.rst   coding_guidelines/index.rst

:ref:`coding_style`

   代码贡献应遵循一套样式指南以确保整个代码库中的一致性和可读性。   proposals_and_rfcs.rst   style/index.rst



:ref:`rfcs`   modifying_contributions.rst   proposals_and_rfcs.rst

   了解何时以及如何为新功能和项目更改提交 RFC (征求意见稿 Request for Comments)。

   modifying_contributions.rst

:ref:`modifying_contributions`

   修改其他开发人员所做的贡献和如何处理陈旧拉取请求的指南。



文档 (Documentation):ref:`contribute_guidelines`

===================

   了解为Zephyr项目做出贡献的总体流程和指南。:ref:`contribute_guidelines`

Zephyr 项目需要优质的文档。无论是作为代码贡献的一部分还是作为独立工作,

为项目贡献文档特别有价值。   Learn about the overall process and guidelines for contributing to the Zephyr project.



.. toctree::   对于首次贡献者来说，本页是必读内容，因为它包含重要信息，

   :maxdepth: 1

   :hidden:   说明如何确保您的贡献可以被考虑纳入项目并可能被合并。   This page is a mandatory read for first-time contributors as it contains important information on



   documentation/guidelines.rst   how to ensure your contribution can be considered for inclusion in the project and potentially

   documentation/generation.rst

:ref:`contributor-expectations`   merged.

:ref:`doc_guidelines`

   此页面为使用 reStructuredText (reST) 标记语言和 Sphinx 文档生成器编写文档提供了一些简单的指南。   这是另一份必读文档，描述了项目*所有*贡献者的预期行为。



:ref:`zephyr_doc`:ref:`contributor-expectations`

   当你写文档时,看到它在呈现时的样子会很有帮助。

:ref:`reviewer-expectations`   This document is another mandatory read that describes the expected behavior of *all*

   此页面描述了如何在本地构建 Zephyr 文档。

   这是另一份必读文档，描述了审查项目贡献时的预期行为。   contributors to the project.



处理外部组件 (Dealing with external components)

==============================================

:ref:`coding_guidelines`:ref:`reviewer-expectations`

.. toctree::

   :maxdepth: 1   代码贡献应遵循一套编码指南，以确保代码库的一致性和可读性。   This document is another mandatory read that describes the expected behavior when revieweing

   :hidden:

   contributions to the project.

   external.rst

   bin_blobs.rst:ref:`coding_style`



:ref:`external-contributions`   代码贡献应遵循一套样式指南，以确保代码库的一致性和可读性。:ref:`coding_guidelines`

   可能会轻松地在其他开源项目中获得有用功能或功能补充 Zephyr 的基本功能,

   建议并鼓励重用此类代码。此页面更详细地描述了何时以及如何将外部源代码导入 Zephyr。   Code contributions are expected to follow a set of coding guidelines to ensure consistency and



:ref:`external-tooling`:ref:`rfcs`   readability across the code base.

   类似地,编译、代码分析、测试或模拟期间使用的外部工具是有益的,并在本部分中介绍。

   了解何时以及如何为项目的新功能和更改提交RFC（征求意见）。

:ref:`bin-blobs`

   由于某些功能可能仅通过以二进制形式分发的可执行代码来提供,此页面描述了:ref:`coding_style`

   :ref:`为项目贡献二进制 blobs <blobs-process>` 的流程和指南。

:ref:`modifying_contributions`   Code contributions are expected to follow a set of style guidelines to ensure consistency and

沿路需要帮助?

===========   修改其他开发人员的贡献以及如何处理过时拉取请求的指南。   readability across the code base.



如果你对贡献流程有疑问,Zephyr 社区可以帮助你。

你可以加入我们的 Discord_ 频道或使用 `开发人员邮件列表 (Developer Mailing List)`_。

文档:ref:`rfcs`



.. _Discord: https://chat.zephyrproject.org=============   Learn when and how to submit RFCs (Request for Comments) for new features and changes to the

.. _Developer Mailing List: https://lists.zephyrproject.org/g/devel

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
