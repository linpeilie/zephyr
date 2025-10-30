.. _pipes_v2:

管道
####

:dfn:`管道` 是一个内核对象,允许一个线程向另一个线程发送字节流。管道支持高效的
线程间通信,并可用于同步传输整块数据或部分数据。

.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的管道,仅受可用 RAM 限制。每个管道由其内存地址引用。

管道具有以下关键属性:

* 指示管道环形缓冲区容量的**大小**。请注意,大小为零定义了没有环形缓冲区的管道。

管道在使用之前必须初始化。初始化时,管道为空。

线程与管道的交互如下:

- **写入**:数据由线程同步写入管道,可以是整体或部分写入。接受的数据要么直接
  复制到等待的读取者,要么复制到管道的环形缓冲区。如果环形缓冲区已满或根本不存在,
  操作将阻塞,直到有足够的空间可用或指定的超时到期。

- **读取**:数据由线程从管道同步读取,可以是整体或部分读取。接受的数据要么从
  管道的环形缓冲区复制,要么直接从等待的发送者复制。如果环形缓冲区为空或根本
  不存在,操作将阻塞,直到数据变得可用或指定的超时到期。

- **重置**:线程可以重置管道,这会重置其内部状态并以错误代码结束所有挂起的
  读取和写入操作。

管道非常适合生产者-消费者模式或在线程之间流式传输数据等场景。

实现
****

使用类型 :c:struct:`k_pipe` 的变量和字节缓冲区定义管道。然后必须通过调用
:c:func:`k_pipe_init` 初始化管道。

以下代码定义并初始化具有能够容纳 100 字节的环形缓冲区的空管道,对齐到 4 字节边界:

.. code-block:: c

    uint8_t __aligned(4) my_ring_buffer[100];
    struct k_pipe my_pipe;

    k_pipe_init(&my_pipe, my_ring_buffer, sizeof(my_ring_buffer));

或者,可以使用 :c:macro:`K_PIPE_DEFINE` 宏在编译时定义和初始化管道,该宏定义了
管道及其环形缓冲区:

.. code-block:: c

    K_PIPE_DEFINE(my_pipe, 100, 4);

这与上面的代码具有相同的效果。

当不使用环形缓冲区时,缓冲区指针参数应为 NULL,大小参数应为 0。

写入管道
========

通过调用 :c:func:`k_pipe_write` 将数据添加到管道。

以下示例演示使用管道将数据从生产者线程发送到一个或多个消费者线程。如果管道的
环形缓冲区填满,生产者线程会等待指定的时间。

.. code-block:: c

   struct message_header {
       size_t num_data_bytes; /* 示例字段 */
       ...
   };

   void producer_thread(void)
   {
       int rc;
       uint8_t *data;
       size_t total_size;
       size_t bytes_written;

       while (1) {
           /* 制作要在管道中发送的消息 */
           make_message(data, &total_size);
           bytes_written = 0;

           /* 将数据写入管道,处理部分写入 */
           while (bytes_written < total_size) {
               rc = k_pipe_write(&my_pipe, &data[bytes_written], total_size - bytes_written, K_NO_WAIT);

               if (rc < 0) {
                   /* 发生错误 */
                   ...
                   break;
               } else {
                   /* 部分或完全写入成功;调整下次迭代 */
                   bytes_written += rc;
               }
           }

           /* 为下一条消息重置 bytes_written */
           bytes_written = 0;
           ...
       }
   }

从管道读取
==========

通过调用 :c:func:`k_pipe_read` 从管道检索数据。

以下示例基于上面的生产者线程示例。它显示了处理生产者生成的数据的消费者线程。

.. code-block:: c

   struct message_header {
       size_t num_data_bytes; /* 示例字段 */
       ...
   };

   void consumer_thread(void)
   {
       int rc;
       uint8_t buffer[128];
       size_t bytes_read = 0;
       struct message_header *header = (struct message_header *)buffer;

       while (1) {
           /* 步骤 1:读取消息头 */
           bytes_read = 0;
      read_header:
           while (bytes_read < sizeof(*header)) {
               rc = k_pipe_read(&my_pipe, &buffer[bytes_read], sizeof(*header) - bytes_read, &bytes_read, K_NO_WAIT);

               if (rc < 0) {
                   /* 发生错误 */
                   ...
                   goto read_header;
               }

               /* 调整部分读取 */
               bytes_read += rc;
           }

           /* 步骤 2:读取消息体 */
           bytes_read = 0;
           while (bytes_read < header->num_data_bytes) {
               rc = k_pipe_read(&my_pipe, &buffer[sizeof(*header) + bytes_read], header->num_data_bytes - bytes_read, K_NO_WAIT);

               if (rc < 0) {
                   /* 发生错误 */
                   ...
                   goto read_header;
               }

               /* 调整部分读取 */
               bytes_read += rc;
           }
           /* 成功接收完整消息 */
       }
   }

重置管道
========

可以通过调用 :c:func:`k_pipe_reset` 重置管道。重置管道会重置其内部状态并以
错误代码结束所有挂起的操作。

以下示例演示响应关键错误重置管道:

.. code-block:: c

    void monitor_thread(void)
    {
        while (1) {
            ...
            /* 检测到关键错误:重置整个管道以重置它。 */
            k_pipe_reset(&my_pipe);
            ...
        }
    }

建议用途
********

管道对于在线程之间发送数据流很有用。典型应用包括:

- 实现生产者-消费者模式。
- 在线程之间流式传输日志或数据包。
- 在实时系统中处理可变长度消息传递。

API 参考
********

.. doxygengroup:: pipe_apis
