.. _code-documentation:

代码文档 (Code Documentation)
###############################

API 文档 (API Documentation)
****************************

良好文档化的 API 增强了开发人员的体验,是定义 API 成功的基本要求。Doxygen 是一个通用文档工具,Zephyr 项目使用它来记录 API。它生成在线文档浏览器(HTML 格式)和/或为其他工具提供输入,这些工具用于从文档化的源文件生成参考手册。特别是,doxygen 的 XML 输出在生成 Zephyr 项目的在线文档时用作输入。

需求参考 (Reference to Requirements)
**************************************

API 大部分记录了需求或宣传功能的实现,并且可以追溯到功能。我们使用 API 文档作为将实现追溯到文档化功能的主要接口。这是通过使用引用需求目录中其他地方维护的需求的自定义 _doxygen_ 标签来完成的。

测试文档 (Test Documentation)
******************************

为了帮助理解每个测试的作用以及它测试的功能,我们还使用相同的工具在相同的上下文中记录所有测试代码,并为在同一环境中维护的所有单元和集成测试生成文档。测试通过创建返回到 API 的链接并添加对原始需求的引用,使用对它们验证的 API 或功能的引用来记录。


文档指南 (Documentation Guidelines)
************************************

测试代码 (Test Code)
====================

Zephyr 项目使用几种测试方法,最常见的是 :ref:`Ztest 框架 <test-framework>`。测试文档应仅针对入口测试函数(通常以 test\_ 为前缀)和那些由 Ztest 框架直接调用的函数进行。这些测试将出现在测试报告中,使用它们的名称和标识符是识别它们并从需求追溯回它们的最佳方式。

测试文档不应干扰实际的 API 文档,需要遵循新的结构以避免混淆。使用一致的命名方案并遵循明确定义的结构,我们将能够将此文档分组到其自己的模块中,并在解析测试数据以生成可追溯性报告时唯一标识它。以下是一些要遵循的指南:

- 所有测试代码文档应分组在 ``all_tests`` doxygen 组下
- 所有测试文档应在以 tests\_ 为前缀的 doxygen 组下

自定义 doxygen ``@verify`` 指令表示测试验证需求::

    /**
    * @brief Tests for the Semaphore kernel object
    * @defgroup kernel_semaphore_tests Semaphore
    * @ingroup all_tests
    * @{
    */

    ...
    /**
    * @brief A brief description of the tests
    * Some details about the test
    * more details
    *
    * @verify{@req{1111}}
    */
    void test_sema_thread2thread(void)
    {
    ...
    }
    ...

    /**
    * @}
    */

为了获得实现或一段代码如何满足需求的覆盖率,我们在 doxygen 中使用 ``satisfy`` 别名::

    /**
    * @brief Give a semaphore.
    *
    * This routine gives @a sem, unless the semaphore is already at its maximum
    * permitted count.
    *
    * @note Can be called by ISRs.
    *
    * @param sem Address of the semaphore.
    *
    * @satisfy{@req{015}}
    */
    __syscall void k_sem_give(struct k_sem *sem);



要生成矩阵,您首先需要构建文档,特别是您需要构建 doxygen XML 输出::

   $ make doxygen

解析 doxygen 生成的 XML 数据以生成可追溯性矩阵。
