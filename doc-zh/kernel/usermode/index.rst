.. _usermode_api:

用户态（User Mode）
##################

Zephyr 支持以降低的特权级运行线程，这被称为“用户态（user mode）”。当前实现主要针对具备 MPU 硬件的设备设计。

如何创建在用户态运行的线程，请参见 :ref:`lifecycle_v2`。

.. toctree::
    :maxdepth: 2

    overview.rst
    memory_domain.rst
    kernelobjects.rst
    syscalls.rst
    mpu_stack_objects.rst
    mpu_userspace.rst
