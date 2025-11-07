虚拟 I/O (Virtual I/O, VIRTIO)
##############################

概述 (Overview)
***************

虚拟 I/O (VIRTIO) 是一种用于与各种设备通信的协议,通常在虚拟化环境中使用。其主要目标是提供一种高效且标准化的机制,用于从虚拟机内与虚拟设备交互。通信依赖于 virtqueue(虚拟队列)和标准传输方法,如 PCI 或 MMIO。

概念 (Concepts)
****************

Virtio 定义了通信和初始化期间使用的各种组件。它指定了主机侧(在规范中称为"device")和客户机侧(在规范中称为"driver")。目前 Zephyr 只能作为客户机工作。在 Virtio 驱动程序公开的功能之上,可以实现特定设备(例如网卡)的驱动程序。

下图显示了具有 Virtio 设备的系统的高级概述。

.. graphviz::
   :caption: 虚拟 I/O 概述

   digraph {

        subgraph cluster_host {
            style=filled;
            color=lightgrey;
            label = "Host";
            labeljust=r;

            virtio_device [label = "virtio device"];
        }

        transfer_method [label = "virtio transfer method"];

        subgraph cluster_guest {
            style=filled;
            color=lightgrey;
            label = "Guest";
            labeljust=r;

            virtio_driver [label = "virtio driver"];
            specific_device_driver [label = "specific device driver"];
            device_user [label = "device user"];
        }

        virtio_device -> transfer_method;
        transfer_method -> virtio_device;
        transfer_method -> virtio_driver;
        virtio_driver -> transfer_method;
        virtio_driver -> specific_device_driver;
        specific_device_driver -> virtio_driver;
        specific_device_driver -> device_user;
        device_user -> specific_device_driver;
   }

配置空间 (Configuration space)
===============================
每个设备都提供配置空间,用于初始化和配置。它允许选择设备和驱动程序特性、启用特定的 virtqueue 并设置它们的地址。一旦设备被配置,其大部分配置在不重置设备的情况下无法更改。配置空间的确切布局取决于传输方法。

驱动程序和设备特性 (Driver and device features)
-----------------------------------------------
配置空间提供了一种协商特性位的方法,确定设备的一些非强制性功能。确切的可用特性位取决于设备和平台。

设备特定配置 (Device-specific configuration)
设备特定配置 (Device-specific configuration)
---------------------------------------------
一些设备提供设备特定的配置空间,提供额外的配置选项。

Virtqueue(虚拟队列)
====================
主机和客户机之间传输数据的主要机制是 virtqueue。特定设备具有不同数量的 virtqueue,例如支持双向传输的设备通常具有一个或多个 tx/rx virtqueue 对。Virtio 指定了两种类型的 virtqueue:split virtqueue 和 packed virtqueue。Zephyr 目前仅支持 split virtqueue。

Split virtqueue(分离式虚拟队列)
--------------------------------
Split virtqueue 由三部分组成:描述符表(descriptor table)、可用环(available ring)和已用环(used ring)。

描述符表保存缓冲区的描述符,即它们的物理地址、长度和标志。每个描述符要么是设备可写的,要么是驱动程序可写的。描述符可以链接,创建描述符链。通常,一个链以包含供设备读取的数据的描述符开始,以设备可写部分结束,设备在其中放置其响应。

可用环的主要部分是对描述符表中描述符的引用(以索引的形式)的循环缓冲区。一旦客户机决定将数据发送到主机,它就会将描述符链头的索引添加到可用环的顶部。

已用环类似于可用环,但它由主机用于将描述符返回给客户机。除了存储描述符索引外,它还提供有关写入它们的数据量的信息。

通用 Virtio 库 (Common Virtio libraries)
*****************************************

Zephyr 提供了一个用于与 Virtio 设备和 virtqueue 交互的 API,允许在 Virtio 设备的整个生命周期内执行必要的操作。

设备初始化 (Device initialization)
===================================
一旦 Virtio 驱动程序完成了使用给定传输方法的所有设备通用的低级初始化(如在总线上查找设备和映射 Virtio 结构),设备特定驱动程序就会介入并在 Virtio API 的帮助下执行下一阶段的初始化。

设备特定驱动程序首先进行特性位协商。它使用 :c:func:`virtio_read_device_feature_bit` 来确定设备提供哪些特性,然后使用 :c:func:`virtio_write_driver_feature_bit` 选择它需要的特性。在选择了所有必需的特性后,设备特定驱动程序调用 :c:func:`virtio_commit_feature_bits`。然后,使用 :c:func:`virtio_init_virtqueues` 初始化 virtqueue。此函数枚举 virtqueue,调用提供的回调 :c:type:`virtio_enumerate_queues` 以确定每个 virtqueue 所需的大小。通过调用 :c:func:`virtio_finalize_init` 完成初始化过程。从此时起,如果没有函数返回错误,则 virtqueue 可以运行。如果特定设备提供了设备特定配置,可以通过调用 :c:func:`virtio_get_device_specific_config` 获取。

Virtqueue 操作 (Virtqueue operation)
=====================================
一旦 virtqueue 可以运行,它们就可以用于发送和接收数据。为此,必须使用 :c:func:`virtio_get_virtqueue` 获取第 n 个 virtqueue 的指针。要发送由描述符链组成的数据,必须使用 :c:func:`virtq_add_buffer_chain`。除了描述符链之外,它还接受指向回调的指针,该回调将在设备返回给定的描述符链时被调用。之后,必须使用 Virtio API 中的 :c:func:`virtio_notify_virtqueue` 通知 virtqueue。

客户机侧 Virtio 驱动程序 (Guest-side Virtio drivers)
*****************************************************
目前 Zephyr 提供了 Virtio over PCI 和 Virtio over MMIO 的驱动程序,以及使用 virtio 的两个设备的驱动程序 - virtiofs(用于访问主机的文件系统)和 virtio-entropy(用作熵源)。

Virtiofs
=========
此驱动程序提供对 `virtiofs <https://virtio-fs.gitlab.io/>`_ 的支持 - 一个允许虚拟机客户机访问主机上目录的文件系统。它使用 FUSE 消息在主机和客户机之间进行通信,以执行文件系统操作,例如打开和读取文件。每次客户机想要执行某些文件系统操作时,它都会在 virtqueue 中放置一个描述符链,以设备可读部分开始(包含 FUSE 输入头和输入数据),并以设备可写部分结束(为 FUSE 输出头和输出数据留出空间)。

Virtio-entropy
==============
此驱动程序允许在 Zephyr 中使用 virtio-entropy 作为熵源。此设备的操作很简单 - 驱动程序在 virtqueue 中放置一个缓冲区并接收它,填充了随机数据。

Virtio 示例 (Virtio samples)
*****************************
:zephyr:code-sample:`virtiofs` 中提供了一个展示使用依赖 Virtio 的驱动程序的示例。如果您希望检查直接与 Virtio 驱动程序交互的代码,可以检查 virtiofs 驱动程序,特别是用于初始化的 :c:func:`virtiofs_init` 以及用于与 Virtio 设备之间传输数据的 :c:func:`virtiofs_send_receive` 和 :c:func:`virtiofs_recv_cb`。
Virtio 示例 (Virtio samples)
*****************************
:zephyr:code-sample:`virtiofs` 中提供了一个展示使用依赖 Virtio 的驱动程序的示例。如果您希望检查直接与 Virtio 驱动程序交互的代码,可以检查 virtiofs 驱动程序,特别是用于初始化的 :c:func:`virtiofs_init` 以及用于与 Virtio 设备之间传输数据的 :c:func:`virtiofs_send_receive` 和 :c:func:`virtiofs_recv_cb`。

API 参考 (API Reference)
*************************

.. doxygengroup:: virtio_interface
.. doxygengroup:: virtqueue_interface
