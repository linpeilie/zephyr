.. _binary_descriptors:

二进制描述符 (Binary Descriptors)
###################################

二进制描述符是存储有关二进制可执行文件信息的常量数据对象 (Binary Descriptors are constant data objects storing information about the binary executable)。与"常规"常量不同,二进制描述符链接到二进制文件中的已知偏移量,使其可被其他程序访问,例如在同一设备上运行的不同镜像或主机工具 (Unlike "regular" constants, binary descriptors are linked to a known offset in the binary, making them accessible to other programs, such as a different image running on the same device or a host tool)。一些有用的二进制描述符常量示例包括:内核版本、应用版本、构建时间、编译器版本、环境变量、编译主机名等 (A few examples of constants that would make useful binary descriptors are: kernel version, app version, build time, compiler version, environment variables, compiling host name, etc)。

二进制描述符通过使用 ``DEFINE_BINDESC_*`` 宏创建 (Binary descriptors are created by using the ``DEFINE_BINDESC_*`` macros)。例如 (For example):

.. code-block:: c

   #include <zephyr/bindesc.h>

   BINDESC_STR_DEFINE(my_string, 2, "Hello world!"); // 唯一ID是2 (Unique ID is 2)

然后可以使用以下方式访问 ``my_string`` (``my_string`` could then be accessed using):

.. code-block:: c

   printk("my_string: %s\n", BINDESC_GET_STR(my_string));

但它也可以通过 ``west bindesc`` 检索 (But it could also be retrieved by ``west bindesc``):

.. code-block:: bash

   $ west bindesc custom_search STR 2 build/zephyr/zephyr.bin
   "Hello world!"

内部机制 (Internals)
*********************
二进制描述符使用链接到二进制镜像中已知偏移量的TLV(标签、长度、值)头实现 (Binary descriptors are implemented with a TLV (tag, length, value) header linked to a known offset in the binary image)。此偏移量可能因架构而异,但通常描述符会尽可能链接到镜像的开头附近 (This offset may vary between architectures, but generally the descriptors are linked as close to the beginning of the image as possible)。在镜像必须以向量表开头的架构中(例如ARM),描述符链接在向量表之后 (In architectures where the image must begin with a vector table (such as ARM), the descriptors are linked right after the vector table)。复位向量指向文本段的开头,它在描述符之后 (The reset vector points to the beginning of the text section, which is after the descriptors)。在镜像必须以可执行代码开头的架构中(例如x86),在镜像开头注入跳转指令,以跳过紧跟在跳转指令之后的二进制描述符 (In architectures where the image must begin with executable code (e.g. x86), a jump instruction is injected at the beginning of the image, in order to skip over the binary descriptors, which are right after the jump instruction)。

每个标签是一个16位无符号整数,其中最高有效半字节(4位)是类型(当前为uint、string或bytes),其余部分是ID (Each tag is a 16 bit unsigned integer, where the most significant nibble (4 bits) is the type (currently uint, string or bytes), and the rest is the ID)。ID对于每个描述符是全局唯一的 (The ID is globally unique to each descriptor)。例如,应用版本字符串的ID是 ``0x800``,字符串用0x1表示,因此应用版本标签为 ``0x1800`` (For example, the ID of the app version string is ``0x800``, and a string is denoted by 0x1, making the app version tag ``0x1800``)。长度是一个16位数字,等于数据的字节长度 (The length is a 16 bit number equal to the length of the data in bytes)。数据是实际的描述符值 (The data is the actual descriptor value)。所有二进制描述符数字(魔数、标签、无符号整数)在内存中以SoC原生的字节序排列 (All binary descriptor numbers (magic, tags, uints) are laid out in memory in the endianness native to the SoC)。``west bindesc`` 默认假定为小端序,因此如果镜像属于大端序SoC,应向工具提供适当的标志 (``west bindesc`` assumes little endian by default, so if the image belongs to a big endian SoC, the appropriate flag should be given to the tool)。

二进制描述符头以魔数 ``0xb9863e5a7ea46046`` 开始 (The binary descriptor header starts with the magic number ``0xb9863e5a7ea46046``)。它后面跟着TLV,并以 ``DESCRIPTORS_END`` (``0xffff``)标签结束 (It's followed by the TLVs, and ends with the ``DESCRIPTORS_END`` (``0xffff``) tag)。标签始终对齐到32位 (The tags are always aligned to 32 bits)。如果前一个描述符的值长度未对齐,将添加零填充以确保当前标签对齐 (If the value of the previous descriptor had a non-aligned length, zero padding will be added to ensure that the current tag is aligned)。

将所有内容组合在一起,上面的示例在内存中(小端序SoC)的样子如下 (Putting it all together, here is what the example above would look like in memory (of a little endian SoC)):

.. code-block::

    46 60 a4 7e 5a 3e 86 b9 02 10  0d 00  48 65 6c 6c 6f 20 77 6f 72 6c 64 21 00 00 00 00 ff ff 00 00
   |         magic         | tag |length| H  e  l  l  o     w  o  r  l  d  !    |   pad  |    end    |

使用方法 (Usage)
*****************
二进制描述符始终由 ``BINDESC_*_DEFINE`` 宏创建 (Binary descriptors are always created by the ``BINDESC_*_DEFINE`` macros)。如上面的示例所示,可以使用任何ID从任何字符串或整数生成描述符 (As shown in the example above, a descriptor can be generated from any string or integer, with any ID)。但是,建议遵守 ``include/zephyr/bindesc.h`` 中定义的标准标签,因为这将带来以下好处 (However, it is recommended to comply with the standard tags defined in ``include/zephyr/bindesc.h``, as that would have the following benefits):

 1. ``west bindesc`` 工具能够识别描述符的含义并打印有意义的标签 (The ``west bindesc`` tool would be able to recognize what the descriptor means and print a meaningful tag)
 2. 它将在来自各种来源的各种应用程序之间强制保持一致性 (It would enforce consistency between various apps from various sources)
 3. 它允许描述符生成的上游能力(参见标准描述符) (It allows upstream-ability of descriptor generation (see Standard Descriptors))

要使用标准标签定义描述符,只需使用从 ``bindesc.h`` 包含的标签 (To define a descriptor with a standard tag, just use the tags included from ``bindesc.h``):

.. code-block:: c

   #include <zephyr/bindesc.h>

   BINDESC_STR_DEFINE(app_version, BINDESC_ID_APP_VERSION_STRING, "1.2.3");

标准描述符 (Standard Descriptors)
===================================
某些描述符可能实现起来很简单,因此可以在上游Zephyr中以标准方式实现 (Some descriptors might be trivial to implement, and could therefore be implemented in a standard way in upstream Zephyr)。然后可以通过Kconfig启用它们,而不需要每个用户重新实现 (These could then be enabled via Kconfig, instead of requiring every user to reimplement them)。这些包括构建时间、内核版本和主机信息 (These include build times, kernel version, and host info)。例如,要将构建日期和时间添加为字符串,应启用以下配置 (For example, to add the build date and time as a string, the following configs should be enabled):

.. code-block:: kconfig

   # 启用二进制描述符 (Enable binary descriptors)
   CONFIG_BINDESC=y

   # 启用二进制描述符的定义 (Enable definition of binary descriptors)
   CONFIG_BINDESC_DEFINE=y

   # 启用默认构建时间二进制描述符 (Enable default build time binary descriptors)
   CONFIG_BINDESC_DEFINE_BUILD_TIME=y
   CONFIG_BINDESC_BUILD_DATE_TIME_STRING=y

为避免与用户定义的描述符冲突,标准描述符被分配了 ``0x800-0xfff`` 之间的范围 (To avoid collisions with user defined descriptors, the standard descriptors were allotted the range between ``0x800-0xfff``)。这将 ``0x000-0x7ff`` 留给用户 (This leaves ``0x000-0x7ff`` to users)。有关更多信息,请阅读这些Kconfig符号的 ``help`` 部分 (For more information read the ``help`` sections of these Kconfig symbols)。按照惯例,每个Kconfig符号对应一个二进制描述符,其名称是小写的Kconfig名称(删除 ``CONFIG_BINDESC_``) (By convention, each Kconfig symbol corresponds to a binary descriptor whose name is the Kconfig name (with ``CONFIG_BINDESC_`` removed) in lower case)。例如,``CONFIG_BINDESC_KERNEL_VERSION_STRING`` 创建一个可以使用 ``BINDESC_GET_STR(kernel_version_string)`` 访问的描述符 (For example, ``CONFIG_BINDESC_KERNEL_VERSION_STRING`` creates a descriptor that can be accessed using ``BINDESC_GET_STR(kernel_version_string)``)。

读取描述符 (Reading Descriptors)
=================================
也可以从应用程序读取和解析二进制描述符 (It's also possible to read and parse binary descriptors from an application)。这对于试图读取自己描述符的镜像以及试图读取另一个镜像描述符的镜像都很有用 (This can be useful both for an image trying to read its own descriptors, and for an image trying to read another image's descriptors)。读取可以通过三种后端之一执行 (Reading can be performed through one of three backends):

 #. RAM - 假设描述符已被复制到RAM(例如由引导加载程序),可以从它们所在的缓冲区读取 (RAM - assuming the descriptors have been copied to RAM (e.g. by a bootloader), they can be read from the buffer they reside in)。

 #. 内存映射闪存 - 如果要读取的镜像所在的闪存可通过程序的地址空间访问,则可以直接从闪存读取 (Memory mapped flash - If the flash where the image to be read resides in flash and is accessible through the program's address space, it can be read directly from flash)。此选项使用最少的RAM,但如果闪存未内存映射则无法工作,并且出于安全考虑不建议用于读取引导加载程序的描述符 (This option uses the least amount of RAM, but will not work if the flash is not memory mapped, and is not recommended to read a bootloader's descriptors for security concerns)。

 #. 闪存 - 使用内部缓冲区,通过闪存API逐个读取描述符,并在它们位于缓冲区中时提供给用户 (Flash - Using an internal buffer, the descriptors are read one by one using the flash API, and given to the user while they're in the buffer)。

要启用读取描述符,请启用 :kconfig:option:`CONFIG_BINDESC_READ` (To enable reading descriptors, enable :kconfig:option:`CONFIG_BINDESC_READ`)。三个后端分别由这些Kconfig符号启用: :kconfig:option:`CONFIG_BINDESC_READ_RAM`、:kconfig:option:`CONFIG_BINDESC_READ_MEMORY_MAPPED_FLASH` 和 :kconfig:option:`CONFIG_BINDESC_READ_FLASH` (The three backends are enabled by these Kconfig symbols, respectively: :kconfig:option:`CONFIG_BINDESC_READ_RAM`, :kconfig:option:`CONFIG_BINDESC_READ_MEMORY_MAPPED_FLASH`, and :kconfig:option:`CONFIG_BINDESC_READ_FLASH`)。

要读取描述符,应首先初始化描述符的句柄 (To read the descriptors, a handle to the descriptors should first be initialized):

.. code-block:: c

   struct bindesc_handle handle;

   /* 假设buffer保存了描述符的副本 (Assume buffer holds a copy of the descriptors) */
   bindesc_open_ram(&handle, buffer);

``bindesc_open_*`` 函数是唯一与所使用的后端相关的函数 (The ``bindesc_open_*`` functions are the only functions concerned with the backend used)。API的其余部分与数据来源无关 (The rest of the API is agnostic to where the data is)。初始化句柄后,可以将其与API的其余部分一起使用 (After the handle has been initialized, it can be used with the rest of the API):

.. code-block:: c

   char *version;
   bindesc_find_str(&handle, BINDESC_ID_KERNEL_VERSION_STRING, &version);
   printk("Kernel version: %s\n", version);

west bindesc 工具 (west bindesc tool)
=======================================
``west`` 能够从给定的可执行镜像解析和显示二进制描述符 (``west`` is able to parse and display binary descriptors from a given executable image)。

有关更多信息,请参阅 ``west bindesc --help`` 或 :ref:`文档<west-bindesc>` (For more information refer to ``west bindesc --help`` or the :ref:`documentation<west-bindesc>`)。

API参考 (API Reference)
************************

.. doxygengroup:: bindesc_define

.. doxygengroup:: bindesc_read
