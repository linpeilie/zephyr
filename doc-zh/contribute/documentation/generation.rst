.. _zephyr_doc:

文档生成 (Documentation Generation)
#################################

本指南将带你在本地生成 Zephyr Project 的文档，使用与线上文档 https://docs.zephyrproject.org 相同的文档来源。

.. _documentation-overview:

文档概览 (Documentation overview)
******************************

Zephyr 文档内容使用 reStructuredText 标记语言 (.rst 扩展名) 编写，并配合 Sphinx 扩展，通过 Sphinx 处理生成完整的网站。开发者既可以直接以 .rst 源文件形式查看，也可以在本地产生 HTML 后用浏览器查看。同样的 .rst 内容也会被用于 Zephyr 公共网站的文档区域（仅主题不同）。

你可以在官方站点阅读 `reStructuredText`_ 与 `Sphinx`_ 的详细信息。

项目文档包含以下内容：

* 用于生成 https://docs.zephyrproject.org 文档的网站的 reStructuredText 源文件。大多数源文件位于 ``/doc`` 目录，但也有部分存放在代码树中与其组件相邻的位置（例如 ``/samples`` 与 ``/boards``）。
* 用于创建所有 API 文档的 Doxygen 生成材料，也会发布在 https://docs.zephyrproject.org。
* 基于源码树中的 Kconfig 文件、脚本生成的内核配置项文档材料。

.. graphviz::
   :caption: 文档构建流程示意

   digraph {
      rankdir=LR

      images [shape="rectangle" label=".png, .jpg\nimages"]
      rst [shape="rectangle" label="restructuredText\nfiles"]
      conf [shape="rectangle" label="conf.py\nconfiguration"]
      rtd [shape="rectangle" label="read-the-docs\ntheme"]
      header [shape="rectangle" label="c header\ncomments"]
      xml [shape="rectangle" label="XML"]
      html [shape="rectangle" label="HTML\nweb site"]
      sphinx[shape="ellipse" label="sphinx +\ndocutils"]
      images -> sphinx
      rst -> sphinx
      conf -> sphinx
      header -> doxygen
      doxygen -> xml
      xml-> sphinx
      rtd -> sphinx
      sphinx -> html
   }


reStructuredText 文件由 Sphinx 文档系统处理，并结合 Doxygen 生成的 API 材料。要在本地生成文档，还需要一些额外工具，见下文。

.. _documentation-processors:

安装文档处理工具 (Installing the documentation processors)
*******************************************************

我们的文档处理流程已在以下环境下验证：

* Doxygen 1.8.13
* Graphviz 2.43
* Latexmk 4.56
* 仓库文件 ``doc/requirements.txt`` 中列出的所有 Python 依赖

请先按照 :ref:`getting_started` 安装 Zephyr。随后安装仅用于生成文档的附加工具，如下：

.. doc_processors_installation_start

.. tabs::

   .. group-tab:: Linux

      对所有 Linux 发行版，先安装用于构建文档的 Python 依赖：

      .. code-block:: console

         pip install -U -r ~/zephyrproject/zephyr/doc/requirements.txt

      在 Ubuntu Linux 上：

      .. code-block:: console

         sudo apt-get install --no-install-recommends doxygen graphviz librsvg2-bin \
         texlive-latex-base texlive-latex-extra latexmk texlive-fonts-recommended imagemagick

      在 Fedora Linux 上：

      .. code-block:: console

         sudo dnf install doxygen graphviz texlive-latex latexmk \
         texlive-collection-fontsrecommended librsvg2-tools ImageMagick

      在 Clear Linux 上：

      .. code-block:: console

         sudo swupd bundle-add texlive graphviz ImageMagick

      在 Arch Linux 上：

      .. code-block:: console

         sudo pacman -S graphviz doxygen librsvg texlive-core texlive-bin \
         texlive-latexextra texlive-fontsextra imagemagick

   .. group-tab:: macOS

      安装用于构建文档的 Python 依赖：

      .. code-block:: console

         pip install -U -r ~/zephyrproject/zephyr/doc/requirements.txt

      使用 ``brew`` 与 ``tlmgr`` 安装工具：

      .. code-block:: console

         brew install doxygen graphviz mactex librsvg imagemagick
         tlmgr install latexmk
         tlmgr install collection-fontsrecommended

   .. group-tab:: Windows

      安装用于构建文档的 Python 依赖：

      .. code-block:: console

         pip install -U -r %USERPROFILE%\zephyrproject\zephyr\doc\requirements.txt

      以 **管理员** 打开 ``cmd.exe``，运行：

      .. code-block:: console

         choco install doxygen.install graphviz strawberryperl miktex rsvg-convert imagemagick

      .. note::
         在 Windows 上，Sphinx 可执行程序 ``sphinx-build.exe`` 位于 Python 安装路径的 ``Scripts`` 文件夹。取决于你的 Python 安装方式，你可能需要将其加入 ``PATH`` 环境变量。参见 `Windows Python Path`_。

.. doc_processors_installation_end

文档主题 (Documentation presentation theme)
****************************************

Sphinx 支持通过主题 (theme) 简单定制生成文档的外观。替换主题文件并再次执行 ``make html``，即可改变输出的布局与样式。``read-the-docs`` 主题会在你完成 :ref:`install_py_requirements`（入门指南中的步骤）时一并安装。

运行文档处理流程 (Running the documentation processors)
****************************************************

在你克隆的 Zephyr 仓库中，``/doc`` 目录包含所有 .rst 源文件、相关工具与用于本地生成技术文档的 Makefile。假设本地 Zephyr 目录为家目录下的 ``zephyr``，以下命令可在本地生成 HTML：

.. code-block:: console

   # 在 Linux/macOS 上
   cd ~/zephyrproject/zephyr/doc
   # 在 Windows 上
   cd %userprofile%\zephyrproject\zephyr\doc

   # 使用 cmake 配置基于 Ninja 的构建系统：
   cmake -GNinja -B_build .

   # 进入构建目录
   cd _build

   # 生成 HTML 输出：
   ninja html
   # 修改或新增 .rst 文件后，重复执行：
   ninja html

   # 生成 PDF 输出：
   ninja pdf

.. warning::

   文档构建系统会在构建目录中为每个用于生成文档的 .rst 文件（以及它们所引用的依赖）创建副本。

   这意味着 Sphinx 的告警与错误会指向“副本”，**而不是 Zephyr 中受版本控制的原文件**。请注意不要在错误信息指向的副本上进行修改，否则更改不会被保存。

根据你的开发环境，收集与生成 HTML 内容可能需要最多 15 分钟。完成后，你可以从 ``doc/_build/html/index.html`` 用浏览器查看 HTML 输出；若生成了 PDF，文件路径为 ``doc/_build/latex/zephyr.pdf``。

如需“干净构建 (from scratch)”，只需删除构建目录内容，再重新执行 ``cmake`` 和 ``ninja``。

.. note::

   如果你在文档中新增或删除文件，需要重新运行 CMake。

在类 Unix 平台下，可使用便捷的 :zephyr_file:`doc/Makefile` 直接在该目录构建文档：

.. code-block:: console

   cd ~/zephyrproject/zephyr/doc

   # 生成 HTML 输出
   make html

   # 生成 PDF 输出
   make pdf

开发者模式文档构建 (Developer-mode Document Building)
**************************************************

当你对文档进行较大调整并测试时，我们提供选项临时跳过自动生成的 Devicetree 绑定文档，从而加速构建。

在运行 cmake 时设置以下选项即可：

   -DDT_TURBO_MODE=1

另一个常见的耗时步骤是为每块开发板生成受支持功能列表。可通过如下选项禁用：

   -DHW_FEATURES_TURBO_MODE=1

使用 :command:`make` 的以下目标可在禁用上述两项的情况下构建文档：

   cd ~/zephyrproject/zephyr/doc

   # 生成不含详细 Devicetree 绑定文档与支持特性索引的 HTML 输出
   make html-fast

当你仅关注某些厂商的开发板文档时，也可以将受支持功能列表的生成限制为部分厂商。在运行 cmake 时设置以下选项：

   -DHW_FEATURES_VENDOR_FILTER=vendor1,vendor2

该选项也可配合 :command:`make` 使用：

   cd ~/zephyrproject/zephyr/doc

   # 将支持特性限制为部分厂商并生成 HTML
   make html HW_FEATURES_VENDOR_FILTER=vendor1,vendor2

本地查看生成文档 (Viewing generated documentation locally)
******************************************************

可以使用 Python 在本地托管生成的 HTML 以供浏览器查看：

.. code-block:: console

   $ python3 -m http.server -d _build/html

.. note::

   WSL2 用户可能需要显式绑定地址到 ``127.0.0.1``，以便从宿主机访问：

   .. code-block:: console

      $ python3 -m http.server -d _build/html --bind 127.0.0.1

另一种方式是使用 ``make html-live``（或 ``make html-live-fast``）构建文档、在本地托管并监听文档目录的变化。一旦检测到变更，将自动重建并刷新托管内容。

将外部 Doxygen 工程链接到 Zephyr (Linking external Doxygen projects against Zephyr)
**********************************************************************************

基于 Zephyr 的外部项目，如需在 Doxygen 中引用 Zephyr 文档（通过 @ref），可以使用导出的 tag 文件：`zephyr.tag <../../doxygen/html/zephyr.tag>`_

下载后，可在自定义 ``doxyfile.in`` 中如下使用：::

   TAGFILES = "/path/to/zephyr.tag=https://docs.zephyrproject.org/latest/doxygen/html/"

更多信息见 `Doxygen External Documentation`_。


.. _reStructuredText: https://sphinx-doc.org/rest.html
.. _Sphinx: https://sphinx-doc.org/
.. _Windows Python Path: https://docs.python.org/3/using/windows.html#finding-the-python-executable
.. _Doxygen External Documentation: https://www.doxygen.nl/manual/external.html
.. _zephyr_doc:

Documentation Generation
########################

These instructions will walk you through generating the Zephyr Project's
documentation on your local system using the same documentation sources
as we use to create the online documentation found at
https://docs.zephyrproject.org

.. _documentation-overview:

Documentation overview
**********************

Zephyr Project content is written using the reStructuredText markup
language (.rst file extension) with Sphinx extensions, and processed
using Sphinx to create a formatted stand-alone website. Developers can
view this content either in its raw form as .rst markup files, or you
can generate the HTML content and view it with a web browser directly on
your workstation. This same .rst content is also fed into the Zephyr
Project's public website documentation area (with a different theme
applied).

You can read details about `reStructuredText`_, and `Sphinx`_ from
their respective websites.

The project's documentation contains the following items:

* ReStructuredText source files used to generate documentation found at the
  https://docs.zephyrproject.org website. Most of the reStructuredText sources
  are found in the ``/doc`` directory, but others are stored within the
  code source tree near their specific component (such as ``/samples`` and
  ``/boards``)

* Doxygen-generated material used to create all API-specific documents
  also found at https://docs.zephyrproject.org

* Script-generated material for kernel configuration options based on Kconfig
  files found in the source code tree

.. graphviz::
   :caption: Schematic of the documentation build process

   digraph {
      rankdir=LR

      images [shape="rectangle" label=".png, .jpg\nimages"]
      rst [shape="rectangle" label="restructuredText\nfiles"]
      conf [shape="rectangle" label="conf.py\nconfiguration"]
      rtd [shape="rectangle" label="read-the-docs\ntheme"]
      header [shape="rectangle" label="c header\ncomments"]
      xml [shape="rectangle" label="XML"]
      html [shape="rectangle" label="HTML\nweb site"]
      sphinx[shape="ellipse" label="sphinx +\ndocutils"]
      images -> sphinx
      rst -> sphinx
      conf -> sphinx
      header -> doxygen
      doxygen -> xml
      xml-> sphinx
      rtd -> sphinx
      sphinx -> html
   }


The reStructuredText files are processed by the Sphinx documentation system,
and make use of the doxygen-generated API material.
Additional tools are required to generate the
documentation locally, as described in the following sections.

.. _documentation-processors:

Installing the documentation processors
***************************************

Our documentation processing has been tested to run with:

* Doxygen version 1.8.13
* Graphviz 2.43
* Latexmk version 4.56
* All Python dependencies listed in the repository file
  ``doc/requirements.txt``

In order to install the documentation tools, first install Zephyr as
described in :ref:`getting_started`. Then install additional tools
that are only required to generate the documentation,
as described below:

.. doc_processors_installation_start

.. tabs::

   .. group-tab:: Linux

      Common to all Linux installations, install the Python dependencies
      required to build the documentation:

      .. code-block:: console

         pip install -U -r ~/zephyrproject/zephyr/doc/requirements.txt

      On Ubuntu Linux:

      .. code-block:: console

         sudo apt-get install --no-install-recommends doxygen graphviz librsvg2-bin \
         texlive-latex-base texlive-latex-extra latexmk texlive-fonts-recommended imagemagick

      On Fedora Linux:

      .. code-block:: console

         sudo dnf install doxygen graphviz texlive-latex latexmk \
         texlive-collection-fontsrecommended librsvg2-tools ImageMagick

      On Clear Linux:

      .. code-block:: console

         sudo swupd bundle-add texlive graphviz ImageMagick

      On Arch Linux:

      .. code-block:: console

         sudo pacman -S graphviz doxygen librsvg texlive-core texlive-bin \
         texlive-latexextra texlive-fontsextra imagemagick

   .. group-tab:: macOS

      Install the Python dependencies required to build the documentation:

      .. code-block:: console

         pip install -U -r ~/zephyrproject/zephyr/doc/requirements.txt

      Use ``brew`` and ``tlmgr`` to install the tools:

      .. code-block:: console

         brew install doxygen graphviz mactex librsvg imagemagick
         tlmgr install latexmk
         tlmgr install collection-fontsrecommended

   .. group-tab:: Windows

      Install the Python dependencies required to build the documentation:

      .. code-block:: console

         pip install -U -r %HOMEPATH$\zephyrproject\zephyr\doc\requirements.txt

      Open a ``cmd.exe`` window as **Administrator** and run the following command:

      .. code-block:: console

         choco install doxygen.install graphviz strawberryperl miktex rsvg-convert imagemagick

      .. note::
         On Windows, the Sphinx executable ``sphinx-build.exe`` is placed in
         the ``Scripts`` folder of your Python installation path.
         Depending on how you have installed Python, you might need to
         add this folder to your ``PATH`` environment variable. Follow
         the instructions in `Windows Python Path`_ to add those if needed.

.. doc_processors_installation_end

Documentation presentation theme
********************************

Sphinx supports easy customization of the generated documentation
appearance through the use of themes. Replace the theme files and do
another ``make html`` and the output layout and style is changed.
The ``read-the-docs`` theme is installed as part of the
:ref:`install_py_requirements` step you took in the getting started
guide.

Running the documentation processors
************************************

The ``/doc`` directory in your cloned copy of the Zephyr project git
repo has all the .rst source files, extra tools, and Makefile for
generating a local copy of the Zephyr project's technical documentation.
Assuming the local Zephyr project copy is in a folder ``zephyr`` in your home
folder, here are the commands to generate the html content locally:

.. code-block:: console

   # On Linux/macOS
   cd ~/zephyrproject/zephyr/doc
   # On Windows
   cd %userprofile%\zephyrproject\zephyr\doc

   # Use cmake to configure a Ninja-based build system:
   cmake -GNinja -B_build .

   # Enter the build directory
   cd _build

   # To generate HTML output, run ninja on the generated build system:
   ninja html
   # If you modify or add .rst files, run ninja again:
   ninja html

   # To generate PDF output, run ninja on the generated build system:
   ninja pdf

.. warning::

   The documentation build system creates copies in the build
   directory of every .rst file used to generate the documentation,
   along with dependencies referenced by those .rst files.

   This means that Sphinx warnings and errors refer to the **copies**,
   and **not the version-controlled original files in Zephyr**. Be
   careful to make sure you don't accidentally edit the copy of the
   file in an error message, as these changes will not be saved.

Depending on your development system, it will take up to 15 minutes to
collect and generate the HTML content.  When done, you can view the HTML
output with your browser started at ``doc/_build/html/index.html`` and
if generated, the PDF file is available at ``doc/_build/latex/zephyr.pdf``.

If you want to build the documentation from scratch just delete the contents
of the build folder and run ``cmake`` and then ``ninja`` again.

.. note::

   If you add or remove a file from the documentation, you need to re-run CMake.

On Unix platforms a convenience :zephyr_file:`doc/Makefile` can be used to
build the documentation directly from there:

.. code-block:: console

   cd ~/zephyrproject/zephyr/doc

   # To generate HTML output
   make html

   # To generate PDF output
   make pdf

Developer-mode Document Building
********************************

When making and testing major changes to the documentation, we provide an option
to temporarily stub-out the auto-generated Devicetree bindings documentation so
the doc build process runs faster.

To enable this mode, set the following option when invoking cmake::

   -DDT_TURBO_MODE=1

Another step that typically takes a long time is the generation of the list of
supported features for each board. This can be disabled by setting the following
option when invoking cmake::

   -DHW_FEATURES_TURBO_MODE=1

Invoking :command:`make` with the following target will build the documentation
without either of the aforementioned features::

   cd ~/zephyrproject/zephyr/doc

   # To generate HTML output without detailed Devicetree bindings documentation
   # and supported features index
   make html-fast

When working with documentation for boards from a specific vendor, it is also
possible to limit generation of the list of supported features to subset of board
vendors. This can be done by setting the following option when invoking cmake::

   -DHW_FEATURES_VENDOR_FILTER=vendor1,vendor2

This option can also be used with the :command:`make` wrapper::

   cd ~/zephyrproject/zephyr/doc

   # To generate HTML output with supported features limited to a subset of vendors
   make html HW_FEATURES_VENDOR_FILTER=vendor1,vendor2

Viewing generated documentation locally
***************************************

The generated HTML documentation can be hosted locally with python for viewing
with a web browser:

.. code-block:: console

   $ python3 -m http.server -d _build/html

.. note::

   WSL2 users may need to explicitly bind the address to ``127.0.0.1`` in order
   to be accessible from the host machine:

   .. code-block:: console

      $ python3 -m http.server -d _build/html --bind 127.0.0.1

Alternatively, the documentation can be built with the ``make html-live``
(or ``make html-live-fast``) command, which will build the documentation, host
it locally, and watch the documentation directory for changes. When changes are
observed, it will automatically rebuild the documentation and refresh the hosted
files.

Linking external Doxygen projects against Zephyr
************************************************

External projects that build upon Zephyr functionality and wish to refer to
Zephyr documentation in Doxygen (through the use of @ref), can utilize the
tag file exported at `zephyr.tag <../../doxygen/html/zephyr.tag>`_

Once downloaded, the tag file can be used in a custom ``doxyfile.in`` as follows::

   TAGFILES = "/path/to/zephyr.tag=https://docs.zephyrproject.org/latest/doxygen/html/"

For additional information refer to `Doxygen External Documentation`_.


.. _reStructuredText: https://sphinx-doc.org/rest.html
.. _Sphinx: https://sphinx-doc.org/
.. _Windows Python Path: https://docs.python.org/3/using/windows.html#finding-the-python-executable
.. _Doxygen External Documentation: https://www.doxygen.nl/manual/external.html
