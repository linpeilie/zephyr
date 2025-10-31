.. _external_module_libmpix:

libmpix
#######

简介
************

`libmpix`_ 项目提供了一个在微控制器上处理图像数据的库。
它支持像素格式转换、去马赛克、模糊、锐化、色彩校正、缩放等功能。

它将多个操作管道化，消除中间缓冲区。
这使得更大的图像分辨率能够在资源受限的系统中运行而不影响性能。

特性
********

* 简单的零拷贝管道引擎，运行时开销低
* 减少内存开销（例如仅用 5 kB RAM 处理 1 MB 数据）
* 支持 POSIX（Linux/BSD/MacOS）和 Zephyr

与 Zephyr 配合使用
*****************

要将 libmpix 作为 Zephyr 模块引入，可以在 :file:`west.yaml` 中将其作为 West 工程添加，
或通过添加子清单（例如 ``zephyr/submanifests/libmpix.yaml``）并包含以下内容后运行 :command:`west update`：

.. code-block:: yaml

   manifest:
     projects:
       - name: libmpix
         url: https://github.com/libmpix/libmpix.git
         revision: main
         path: modules/lib/libmpix

API 详情请参阅 ``libmpix`` 头文件。下面是一个简单的示例。

.. code-block:: c

   #include <mpix/image.h>

   struct mpix_image img;

   mpix_image_from_buf(&img, buf_in, sizeof(buf_in), MPIX_FORMAT_RGB24);
   mpix_image_kernel(&img, MPIX_KERNEL_DENOISE, 5);
   mpix_image_kernel(&img, MPIX_KERNEL_SHARPEN, 3);
   mpix_image_convert(&img, MPIX_FORMAT_YUYV);
   mpix_image_to_buf(&img, buf_out, sizeof(buf_out));

   return img.err;

参考资料
**********

.. target-notes::

.. _libmpix: https://github.com/libmpix/libmpix
