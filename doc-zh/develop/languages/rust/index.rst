.. _language_rust:

Rust 语言支持
#####################

Rust 是一种现代系统编程语言,旨在提供内存安全性、并发性和性能,而不牺牲低级控制。
它通过独特的所有权模型在编译时消除了空指针解引用和数据竞争等常见错误。

Rust 对安全性和正确性的强调使其特别适合嵌入式系统和可靠性至关重要的环境。
此外,Rust 提供强大的抽象,无需运行时或垃圾收集器,允许开发人员自信且高效地
编写高级代码和低级硬件交互。

这些属性使 Rust 成为 Zephyr 项目的有力选择,在这些项目中,资源约束和系统稳定性
至关重要。

启用 Rust 支持
*********************

为了在 Zephyr 应用程序中启用 Rust 支持,需要完成以下几件事:

1.  由于 Rust 目前是一个可选模块,因此需要启用该模块。最简单的方法是使用 west:

    .. code-block:: shell

       west config manifest.project-filter +zephyr-lang-rust
       west update

    这应该会导致 Rust 语言支持被放置在 Zephyr 工作区的
    :samp:`modules/lang/rust` 中。

2.  通过 :file:`prj.conf` 中的 :kconfig:option:`CONFIG_RUST` 启用 Rust 支持。
    最简单的方法(以及下一步的 CMake 设置)是从
    :module_file:`modules/lang/rust/samples <zephyr-lang-rust:samples>` 中的
    示例之一开始。

3.  配置应用程序的 :file:`CMakeLists.txt` 文件以支持 Rust。同样,最简单的方法是
    从示例复制,但这看起来像:

    .. code-block:: cmake

       cmake_minimum_required(VERSION 3.20.0)

       find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})

       project(my_app)
       rust_cargo_application()

4.  创建一个 :file:`Cargo.toml` 来描述如何构建 Rust 应用程序。来自 Hello World
    示例:

    .. code-block:: toml

       [package]
       # 目前必须是 rustapp。
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

    唯一必需的依赖项是 ``zephyr``,它提供用于与 Zephyr 接口的 zephyr crate。

5.  像构建任何其他 Zephyr 应用程序一样进行构建。目前只有少数目标支持 Rust
    (可以在 :module_file:`modules/lang/rust/etc/platforms.txt
    <zephyr-lang-rust:etc/platforms.txt>` 文件中看到这些目标)。

API 文档
*****************

模块中最新版本的 `API 文档`_ 保存在 gh-pages 上。

.. _`API 文档`:
   https://zephyrproject-rtos.github.io/zephyr-lang-rust/nostd/zephyr/index.html

此文档是为启用了所有功能的通用目标生成的。一旦您有一个可构建的应用程序,
您可以专门为您的目标生成文档:

.. code-block:: shell

   west build -t rustdoc

   ...

   Generated /my/path/app/zephyr/build/doc/rust/target/riscv32i-unknown-none-elf/doc/rustapp/index.html

最后打印的路径可以在浏览器中打开。此顶级文档将用于您的应用程序本身。
在左侧边栏中查找 'zephyr' crate,这将带您进入 Zephyr 的文档。此页面还将
为您的应用程序直接或间接使用的任何依赖项生成本地文档。
