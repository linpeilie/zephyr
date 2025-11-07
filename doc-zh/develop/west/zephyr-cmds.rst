.. _west-zephyr-ext-cmds:

其他 Zephyr 扩展命令 (Additional Zephyr extension commands)
############################################################

本页面记录了其他 :ref:`west-zephyr-extensions <west-zephyr-extensions>`。

.. _west-boards:

列出开发板: ``west boards``
****************************

``boards`` 命令可用于列出 Zephyr 支持的开发板,而无需求助于其他信息来源。

可以通过输入以下命令运行::

  west boards

此命令以默认格式列出所有支持的开发板。如果您希望自己指定显示格式,可以使用 ``--format``(或 ``-f``)标志::

  west boards -f "{arch}:{name}"

有关格式化选项的其他帮助,可以通过运行以下命令找到::

  west boards -h

.. _west-completion:

Shell 补全脚本: ``west completion``
************************************

``completion`` 扩展命令输出 shell 补全脚本,然后可以直接使用这些脚本为支持的 shell 启用 shell 补全。

它目前支持以下 shell:

- bash
- zsh
- fish
- powershell(仅限开发板限定符)

命令的帮助中提供了其他说明::

  west help completion

.. _west-zephyr-export:

安装 CMake 包: ``west zephyr-export``
**************************************

此命令将当前 Zephyr 安装注册为 CMake 用户包注册表中的 CMake 配置包。

在 Windows 中,CMake 用户包注册表位于
``HKEY_CURRENT_USER\Software\Kitware\CMake\Packages``。

在 Linux 和 MacOS 中,CMake 用户包注册表位于
:file:`~/.cmake/packages`。

您可以在设置 Zephyr 工作空间时运行此命令。如果这样做,
工作空间外部的应用程序 CMakeLists.txt 文件将能够使用以下内容找到 Zephyr 仓库:

.. code-block:: cmake

   find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})

有关详细信息,请参阅 :zephyr_file:`share/zephyr-package/cmake`。

.. _west-spdx:

软件物料清单: ``west spdx``
****************************

此命令生成 SPDX 2.2 或 2.3 标签值文档,创建从源文件到相应生成的构建文件的关系。
扫描源文件中的 ``SPDX-License-Identifier`` 注释并填充到 SPDX 文档中。

要使用此命令:

#. 像这样预填充构建目录 :file:`BUILD_DIR`:

   .. code-block:: bash

      west spdx --init -d BUILD_DIR

   此步骤确保构建目录包含生成 SPDX 文档所需的 CMake 元数据。

#. 在您的项目中启用 :file:`CONFIG_BUILD_OUTPUT_META`。

#. 使用此预创建的构建目录构建您的应用程序,如下所示:

   .. code-block:: bash

      west build -d BUILD_DIR [...]

#. 使用此构建目录生成 SPDX 文档:

   .. code-block:: bash

      west spdx -d BUILD_DIR

   默认情况下,这会生成 SPDX 2.3 文档。要生成 SPDX 2.2 文档,请使用:

   .. code-block:: bash

      west spdx -d BUILD_DIR --spdx-version 2.2

.. note::

   使用 :ref:`sysbuild` 构建时,请确保针对要为其生成 SBOM 的实际应用程序。
   例如,如果应用程序名为 ``hello_world``:

   .. code-block:: bash

     west spdx --init  -d BUILD_DIR/hello_world
     west build -d BUILD_DIR/hello_world
     west spdx -d BUILD_DIR/hello_world

这会在 :file:`BUILD_DIR/spdx/` 中生成以下 SPDX 物料清单(BOM)文档:

- :file:`app.spdx`: 用于构建的应用程序源文件的 BOM
- :file:`zephyr.spdx`: 用于构建的特定 Zephyr 源代码文件的 BOM
- :file:`build.spdx`: 构建输出文件的 BOM
- :file:`modules-deps.spdx`: 模块依赖项的 BOM。有关详细信息,请查看
  :ref:`模块 <modules-vulnerability-monitoring>`。

物料清单中的每个文件都会被扫描,以便记录其哈希值(SHA256 和 SHA1),
以及如果文件中出现 ``SPDX-License-Identifier`` 注释,则会记录任何检测到的许可证。

使用 REUSE 组的第三方 :command:`reuse` 工具提取版权声明。
找到后,这些声明将作为 ``FileCopyrightText`` 字段添加到 SPDX 文档中。

.. note::
   版权提取使用启发式方法,可能无法捕获完整的声明文本,因此
   ``FileCopyrightText`` 内容是尽力而为的。这与 SPDX 规范建议一致。

创建 SPDX 关系以指示 CMake 构建目标之间的依赖关系、
链接在一起的构建目标以及编译以生成构建库文件的源文件。

``west spdx`` 接受这些附加选项:

- ``-n PREFIX``: 将包含在生成的 SPDX 文档中的文档命名空间的前缀。
  有关详细信息,请参阅 `SPDX 规范第 6 条`_。如果省略 ``-n``,
  将根据第 2.5 节中描述的默认格式使用随机 UUID 生成默认命名空间。

- ``-s SPDX_DIR``: 指定应写入 SPDX 文档的备用目录,而不是 :file:`BUILD_DIR/spdx/`。

- ``--spdx-version {2.2,2.3}``: 指定要使用的 SPDX 规范版本。
  默认为 ``2.3``。SPDX 2.3 包含 SPDX 2.2 中不可用的附加字段,如 ``PrimaryPackagePurpose``。

- ``--analyze-includes``: 除了在物料清单中记录已编译的源代码文件
  (例如 ``.c``、``.S``)之外,还尝试确定每个 ``.c`` 文件包含的特定头文件。

  这需要更长时间,因为它使用与实际构建时传递给每个 ``.c`` 文件相同的参数,
  对每个 ``.c`` 文件使用 C 编译器执行试运行。

- ``--include-sdk``: 与 ``--analyze-includes`` 一起使用时,还会创建第四个 SPDX
  文档 :file:`sdk.spdx`,其中列出从 SDK 包含的头文件。

.. warning::

   当前不支持为 ``native_sim`` 平台生成 SBOM 文档。

.. _SPDX specification clause 6:
   https://spdx.github.io/spdx-spec/v2.2.2/document-creation-information/

.. _west-blobs:

处理二进制 blob: ``west blobs``
********************************

``blobs`` 命令允许用户通过其 :ref:`module.yml <module-yml>` 文件与一个或多个
:ref:`模块 <modules>` 中声明的 :ref:`二进制 blob <bin-blobs>` 进行交互。

``blobs`` 命令有三个子命令,用于列出、获取或清理(即删除)二进制 blob 本身。

您可以在列出二进制 blob 时指定输出格式::

  west blobs list -f '{module}: {type} {path}'

有关 ``-f/--format`` 中可用的完整变量集,请运行 ``west blobs -h``。

获取 blob 的工作方式类似::

  west blobs fetch

请注意,如 :ref:`模块部分 <modules-bin-blobs>` 所述,
获取的 blob 存储在相应模块仓库根目录的 :file:`zephyr/blobs/` 文件夹中。

删除它们也是如此::

  west blobs clean

此外,该工具允许您通过键入模块名称作为命令行参数来指定要列出、获取或清理 blob 的模块。

参数 ``--allow-regex`` 可以传递给 ``west blobs fetch`` 以通过传递正则表达式来限制获取的特定 blob::

  # 例如,仅下载 esp32 blob,跳过其他变体
  west blobs fetch hal_espressif --allow-regex 'lib/esp32/.*'

.. _west-twister:

Twister 包装器: ``west twister``
*********************************
此命令是 :ref:`twister <twister_script>` 的包装器。

然后可以通过 west 调用 Twister,如下所示::

  west twister -help
  west twister -T tests/ztest/base

.. _west-bindesc:

处理二进制描述符: ``west bindesc``
***********************************

``bindesc`` 命令允许用户读取可执行文件的 :ref:`二进制描述符<binary_descriptors>`。
它目前支持 ``.bin``、``.hex``、``.elf`` 和 ``.uf2`` 文件作为输入。

您可以在镜像中搜索特定描述符,例如::

   west bindesc search KERNEL_VERSION_STRING build/zephyr/zephyr.bin

您可以按类型和 ID 搜索自定义描述符,例如::

   west bindesc custom_search STR 0x200 build/zephyr/zephyr.bin

您可以使用以下命令转储镜像中的所有描述符::

   west bindesc dump build/zephyr/zephyr.bin

您可以使用以下命令将镜像的描述符数据区域提取到文件::

   west bindesc extract

您可以使用以下命令列出所有已知的标准描述符名称::

   west bindesc list

您可以使用以下命令打印描述符在镜像内的偏移量::

   west bindesc get_offset

使用 GNU Global 索引源代码: ``west gtags``
*******************************************

.. important:: 您必须安装 `GNU Global`_ 提供的 ``gtags`` 和 ``global`` 程序才能使用此命令。

``west gtags`` 命令允许您为整个 west 工作空间创建 GNU Global 标签文件::

  west gtags

.. _GNU Global: https://www.gnu.org/software/global/

这将在工作空间 :ref:`topdir <west-workspace>` 中创建一个名为 ``GTAGS`` 的标签文件
(它还会在同一位置创建其他与 Global 相关的元数据文件,名为 ``GPATH`` 和 ``GRTAGS``)。

然后,您可以在工作空间内的任何位置运行 ``global`` 命令,使用此标签文件搜索符号位置。

例如,要从 ``zephyr/drivers`` 目录开始搜索 ``arch_system_halt()`` 函数的定义::

  $ cd zephyr/drivers
  $ global -x arch_system_halt
  arch_system_halt   65 ../arch/arc/core/fatal.c FUNC_NORETURN void arch_system_halt(unsigned int reason)
  arch_system_halt  455 ../arch/arm64/core/fatal.c FUNC_NORETURN void arch_system_halt(unsigned int reason)
  arch_system_halt  137 ../arch/nios2/core/fatal.c FUNC_NORETURN void arch_system_halt(unsigned int reason)
  arch_system_halt   18 ../arch/posix/core/fatal.c FUNC_NORETURN void arch_system_halt(unsigned int reason)
  arch_system_halt   17 ../arch/x86/core/fatal.c FUNC_NORETURN void arch_system_halt(unsigned int reason)
  arch_system_halt  126 ../arch/xtensa/core/fatal.c FUNC_NORETURN void arch_system_halt(unsigned int reason)
  arch_system_halt   21 ../kernel/fatal.c FUNC_NORETURN __weak void arch_system_halt(unsigned int reason)

这将打印搜索符号、定义它的行、定义它的文件的相对路径以及行本身,
适用于定义符号的所有位置。

其他提示:

- 这也可用于搜索供应商 HAL 函数定义。

- 有关如何使用此工具的更多信息,请参阅 ``global`` 命令的手册页。

- 您应该运行 ``global``,**而不是** ``west global``。不需要单独的 ``west global``
  命令,因为 ``global`` 已经从您的当前工作目录开始搜索 ``GTAGS`` 文件。
  这就是为什么您需要从工作空间内运行 ``global``。

.. _west-patch:

处理补丁: ``west patch``
*************************

``patch`` 命令允许用户以受控方式将补丁应用于 Zephyr 或 Zephyr 模块,
从而使使用 :ref:`T2 星形拓扑 <west-t2>` 的外部应用程序更容易进行自动化和跟踪。
:ref:`patches.yml <patches-yml>` 文件存储有关补丁文件的元数据,
并填补官方 Zephyr 版本之间的空白,以便用户可以轻松查看任何上游工作的状态,
并确定在升级到下一个 Zephyr 版本之前要删除哪些补丁。

有几个子命令可用于管理工作空间中 Zephyr 或其他模块的补丁:

* ``apply``: 应用 ``patches.yml`` 中列出的补丁
* ``clean``: 删除所有已应用的补丁,并重置为清单检出状态
* ``list``: 列出 ``patches.yml`` 中的所有补丁
* ``gh-fetch``: 从 GitHub 拉取请求获取补丁

.. code-block:: none

    west-workspace/
    └── application/
       ...
       ├── west.yml
       └── zephyr
           ├── module.yml
           ├── patches
           │   ├── bootloader
           │   │   └── mcuboot
           │   │       └── my-tweak-for-mcuboot.patch
           │   └── zephyr
           │       └── my-zephyr-change.patch
           └── patches.yml

在此示例中,:ref:`west 清单 <west-manifests>` 文件 ``west.yml`` 将固定到特定的
Zephyr 修订版本(例如 ``v4.1.0``),并针对该 Zephyr 修订版本以及应用程序中使用的
其他模块的特定修订版本应用补丁。但是,此应用程序需要两个更改才能满足要求;
一个用于 Zephyr,另一个用于 MCUBoot。

.. _patches-yml:

.. code-block:: yaml

    patches:
      - path: zephyr/my-zephyr-change.patch
        sha256sum: c676cd376a4d19dc95ac4e44e179c253853d422b758688a583bb55c3c9137035
        module: zephyr
        author: Obi-Wan Kenobi
        email: obiwan@jedi.org
        date: 2025-05-04
        upstreamable: false
        comments: |
          An application-specific change we need for Zephyr.
      - path: bootloader/mcuboot/my-tweak-for-mcuboot.patch
        sha256sum: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
        module: mcuboot
        author: Darth Sidious
        email: sidious@sith.org
        date: 2025-05-04
        merge-pr: https://github.com/zephyrproject-rtos/zephyr/pull/<pr-number>
        issue: https://github.com/zephyrproject-rtos/zephyr/issues/<issue-number>
        merge-status: true
        merge-commit: 1234567890abcdef1234567890abcdef12345678
        merge-date: 2025-05-06
        apply-command: git apply
        comments: |
          A change to mcuboot that has been merged already. We can remove this
          patch when we are ready to upgrade to the next Zephyr release.

补丁可以轻松地以自动化方式应用。例如:

.. code-block:: bash

    west init -m <manifest repo> <workspace>
    cd <workspace>
    west update
    west patch apply

当需要更新到较新版本的 Zephyr 时,可以更新 ``west.yml`` 文件以指向下一个 Zephyr 版本,
例如 ``v4.2.0``。不再需要的补丁,如上面示例中的 ``my-tweak-for-mcuboot.patch``,
可以从 ``patches.yml`` 和外部应用程序仓库中删除,然后可以运行以下命令。

.. code-block:: bash

    west patch clean
    west update
    west patch apply --roll-back # 如果某个补丁未能干净地应用,则回滚所有补丁

如果需要重新处理补丁,请记住使用新的 SHA256 校验和更新 ``patches.yml`` 文件。

.. code-block:: bash

    sha256sum zephyr/patches/zephyr/my-zephyr-change.patch
    7d57ca78d5214f422172cc47fed9d0faa6d97a0796c02485bff0bf29455765e9

还可以使用 ``west patch gh-fetch`` 从 GitHub 拉取请求获取补丁并自动创建或更新
``patches.yml`` 文件。当作者已经在现有的上游拉取请求中捕获了许多更改时,这可能很有用。

.. code-block:: bash

    west patch gh-fetch --owner zephyrproject-rtos --repo zephyr --pull-request <pr-number> \
      --module zephyr --split-commits

上述命令将创建下面的目录和文件结构,其中包括与给定拉取请求关联的每个单独提交的补丁。

.. code-block:: none

    zephyr
    ├── patches
    │   ├── first-commit-from-pr.patch
    │   ├── second-commit-from-pr.patch
    │   └── third-commit-from-pr.patch
    └── patches.yml
