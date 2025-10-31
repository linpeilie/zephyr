.. _language_rust:

Rust 语言支持
#############

Rust 是一种现代系统编程语言，旨在提供内存安全、并发和性能，而不牺牲低级控制。
它通过独特的所有权模型实现这一点，该模型在编译时消除了常见的错误，
如空指针解引用和数据竞争。

Rust 对安全性和正确性的强调使其特别适合嵌入式系统和需要可靠性至关重要的环境。
此外，Rust 提供了强大的抽象而没有运行时或垃圾收集器，允许开发人员编写高级代码和低级硬件交互，
具有信心和效率。

这些属性使 Rust 成为 Zephyr 项目的强有力选择，其中资源约束和系统稳定性至关重要。

启用 Rust 支持
**************

为了在 Zephyr 应用程序中启用 Rust 支持，需要做几件事：

1.  由于 Rust 目前是可选模块，需要启用该模块。最简单的方法是使用 west：

    .. code-block:: shell

       west config manifest.project-filter +zephyr-lang-rust
       west update

    这应该会导致 Rust 语言支持被放置在 Zephyr 工作区中的 :samp:`modules/lang/rust` 中。

2.  通过 :file:`prj.conf` 中的 :kconfig:option:`CONFIG_RUST` 启用 Rust 支持。
    最简单的方法（以及下一步的 CMake 设置）是从 :module_file:`modules/lang/rust/samples <zephyr-lang-rust:samples>`
    中的示例开始。

3.  配置应用程序的 :file:`CMakeLists.txt` 文件以支持 Rust。同样，
    最简单的方法是从示例复制，但这看起来像：

    .. code-block:: cmake

       cmake_minimum_required(VERSION 3.20.0)

       find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})

       project(my_app)
       rust_cargo_application()

4.  创建描述如何构建 Rust 应用程序的 :file:`Cargo.toml`。从 Hello World 示例：

    .. code-block:: toml

       [package]
       # This must be rustapp for now.
       name = "rustapp"
       version = "0.1.0"
       edition = "2021"
       description = "The description of my app"
       license = "Apache-2.0 or MIT"

       [lib]
       crate-type = ["staticlib"]

       [dependencies]
       zephyr = "0.1.0"
       log = "0.4.22"

    唯一必需的依赖项是 ``zephyr``，它提供了用于与 Zephyr 交互的 zephyr crate。

5.  像构建任何其他 Zephyr 应用程序一样进行构建。目前只有少数几个目标支持 Rust
    （这些可以在 :module_file:`modules/lang/rust/etc/platforms.txt <zephyr-lang-rust:etc/platforms.txt>`
    文件中看到）。

API 文档
*******

模块中最新版本的 `API 文档`_ 保留在 gh-pages 上。

.. _`API Documentation`:
   https://zephyrproject-rtos.github.io/zephyr-lang-rust/nostd/zephyr/index.html

此文档是为通用目标生成的，启用了所有功能。拥有可构建的应用程序后，
可以为你的目标生成特定文档：

.. code-block:: shell

   west build -t rustdoc

   ...

   Generated /my/path/app/zephyr/build/doc/rust/target/riscv32i-unknown-none-elf/doc/rustapp/index.html

打印在末尾的路径可以在浏览器中打开。此顶级文档将是你的应用程序本身。
在左侧边栏中查找"zephyr"crate，这将带你到 Zephyr 的文档。这个页面也将为
你的应用程序直接或间接使用的任何依赖项生成本地文档。
