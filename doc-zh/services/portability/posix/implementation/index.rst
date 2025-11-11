.. _posix_details:

实现细节 (Implementation Details)
##################################

在许多方面,Zephyr 提供了与任何 POSIX 操作系统相似的支持:提供 C 编程语言的 API 绑定,配置后 POSIX 头文件可在标准包含路径中使用。(In many ways, Zephyr provides support like any POSIX OS; API bindings are provided in the C programming language, POSIX headers are available in the standard include path, when configured.)

与其他多用途 POSIX 操作系统不同: (Unlike other multi-purpose POSIX operating systems)

- Zephyr 不是"POSIX 操作系统"。Zephyr 内核并非围绕 POSIX 标准设计,POSIX 支持是可选特性 (Zephyr is not "a POSIX OS". The Zephyr kernel was not designed around the POSIX standard, and POSIX support is an opt-in feature)
- Zephyr 应用程序不单独链接,也不作为子进程执行 (Zephyr apps are not linked separately, nor do they execute as subprocesses)
- Zephyr、库与应用代码一起编译和链接,在单一(可能是虚拟的)地址空间中以类似单进程应用的方式运行 (Zephyr, libraries, and application code are compiled and linked together, running similarly to a single-process application, in a single (possibly virtual) address space)
- Zephyr 不提供 POSIX shell、编译器、实用程序,也不是自托管的 (Zephyr does not provide a POSIX shell, compiler, utilities, and is not self-hosting.)

.. note::
   与 Linux 内核或 FreeBSD 不同,Zephyr 不为每个支持的架构维护静态系统调用号表,而是在构建时动态生成系统调用。详情参见 :ref:`系统调用 <syscalls>`。(Unlike the Linux kernel or FreeBSD, Zephyr does not maintain a static table of system call numbers for each supported architecture, but instead generates system calls dynamically at build time. See :ref:`System Calls <syscalls>` for more information.)

设计 (Design)
==============

作为库,Zephyr 的 POSIX API 实现致力于在应用程序、中间件与 Zephyr 内核之间提供一个轻薄的抽象层。(As a library, Zephyr's POSIX API implementation makes an effort to be a thin abstraction layer between the application, middleware, and the Zephyr kernel.)

一些通用设计考虑: (Some general design considerations:)

- POSIX 接口与实现应属于 Zephyr 的 POSIX 库,除非 POSIX API 实现和其他特性同时需要,否则不应放在别处。实现应保留在 POSIX 实现中的示例如 ``getopt()``。应属于独立库的实现示例包括多线程与网络。(The POSIX interface and implementations should be part of Zephyr's POSIX library, and not elsewhere, unless required both by the POSIX API implementation and some other feature. An example where the implementation should remain part of the POSIX implementation is ``getopt()``. Examples where the implementation should be part of separate libraries are multithreading and networking.)

- 当 POSIX API 与另一个 Zephyr 子系统都依赖某个特性时,该特性的实现应作为独立的 Zephyr 库,可同时被 POSIX API 和其他库或子系统使用。这减少了代码中出现依赖循环的可能性。在实际中,该规则也应扩展到宏。下面的示例中,``libposix`` 依赖 ``libzfoo`` 来实现 Zephyr 中某些"foo"功能。如果 ``libzfoo`` 也依赖 ``libposix``,就会形成依赖循环。可以通过互相依赖 ``libcommon`` 来消除循环。(When the POSIX API and another Zephyr subsystem both rely on a feature, the implementation of that feature should be as a separate Zephyr library that can be used by both the POSIX API and the other library or subsystem. This reduces the likelihood of dependency cycles in code. When practical, that rule should expand to include macros. In the example below, ``libposix`` depends on ``libzfoo`` for the implementation of some functionality "foo" in Zephyr. If ``libzfoo`` also depends on ``libposix``, then there is a dependency cycle. The cycle can be removed via mutual dependency, ``libcommon``.)

.. graphviz::
   :caption: POSIX 与另一个 Zephyr 库之间的依赖循环 (Dependency cycle between POSIX and another Zephyr library)

   digraph {
       node [shape=rect, style=rounded];
       rankdir=LR;

       libposix [fillcolor="#d5e8d4"];
       libzfoo [fillcolor="#dae8fc"];

       libposix -> libzfoo;
       libzfoo -> libposix;
   }

.. graphviz::
   :caption: POSIX 与其他 Zephyr 库之间的互相依赖 (Mutual dependencies between POSIX and other Zephyr libraries)

   digraph {
       node [shape=rect, style=rounded];
       rankdir=LR;

       libposix [fillcolor="#d5e8d4"];
       libzfoo [fillcolor="#dae8fc"];
       libcommon [fillcolor="#f8cecc"];

       libposix -> libzfoo;
       libposix -> libcommon;
       libzfoo -> libcommon;
   }

- POSIX API 调用应作为常规可调用的 C 函数提供;如果实现的一部分需要 Zephyr :ref:`系统调用 <syscalls>`,该系统调用的声明和实现应隐藏在 POSIX API 后面。(POSIX API calls should be provided as regular callable C functions; if a Zephyr :ref:`System Call <syscalls>` is needed as part of the implementation, the declaration and the implementation of that system call should be hidden behind the POSIX API.)
