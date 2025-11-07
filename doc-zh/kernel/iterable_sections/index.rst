.. _iterable_sections_api:

可迭代段 (Iterable Sections)
#############################

本页包含可迭代段 API 的参考文档,该 API 可用于定义大小相等的数据结构的可迭代区域,
可以使用 :c:macro:`STRUCT_SECTION_FOREACH` 对其进行迭代。

用法 (Usage)
*************

可迭代段元素通常通过在公共头文件中定义数据结构和相关初始化器来使用,以便它们可以在代码库的任何位置实例化。

.. code-block:: c

    struct my_data {
             int a, b;
    };

    #define DEFINE_DATA(name, _a, _b) \
             STRUCT_SECTION_ITERABLE(my_data, name) = { \
                     .a = _a, \
                     .b = _b, \
             }

    ...

    DEFINE_DATA(d1, 1, 2);
    DEFINE_DATA(d2, 3, 4);
    DEFINE_DATA(d3, 5, 6);

然后必须设置链接器,使用链接器宏之一(如 :c:macro:`ITERABLE_SECTION_RAM` 或 :c:macro:`ITERABLE_SECTION_ROM`)将结构放置在连续的段中。自定义
链接器片段通常使用 ``zephyr_linker_sources()`` CMake 函数之一声明,使用适当的段
标识符,RAM 结构使用 ``DATA_SECTIONS``,ROM 结构使用 ``SECTIONS``。

.. code-block:: cmake

   # CMakeLists.txt
   zephyr_linker_sources(DATA_SECTIONS iterables.ld)

.. code-block:: c

   # iterables.ld
   #include <zephyr/linker/iterable_sections.h>
   ITERABLE_SECTION_RAM(my_data, 4)

然后可以使用 :c:macro:`STRUCT_SECTION_FOREACH` 访问数据。

.. code-block:: c

   STRUCT_SECTION_FOREACH(my_data, data) {
           printk("%p: a: %d, b: %d\n", data, data->a, data->b);
   }

.. note::
   链接器将按名称排序放置条目,因此上面的示例将按该顺序访问 ``d1``、``d2`` 和 ``d3``,无论它们在代码中如何定义。

API 参考 (API Reference)
*************************

.. doxygengroup:: iterable_section_apis
