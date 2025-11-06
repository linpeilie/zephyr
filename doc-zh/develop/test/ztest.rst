.. _test-framework:

测试框架
########

Zephyr测试框架（Ztest）提供了一个简单的测试框架，旨在开发期间使用。它提供基本的断言宏和通用测试结构。

该框架可以通过两种方式使用：既可以作为集成测试的通用框架，也可以用于特定模块的单元测试。

创建测试套件
*************

使用Ztest创建测试套件只需调用:c:macro:`ZTEST_SUITE`宏即可。该宏接受以下参数：

* ``suite_name`` - 套件的名称。此名称在单个二进制文件中必须是唯一的。
* :c:type:`ztest_suite_predicate_t` - 可选的条件函数，用于选择测试何时运行。条件函数将获得通过:c:func:`ztest_run_all`传递的全局状态的指针，并应返回布尔值来决定套件是否应该运行。
* :c:type:`ztest_suite_setup_t` - 可选的设置函数，返回测试固件。该函数将在每次测试套件运行期间被调用和执行一次。
* :c:type:`ztest_suite_before_t` - 可选的前置函数，将在套件中的每个测试之前运行。
* :c:type:`ztest_suite_after_t` - 可选的后置函数，将在套件中的每个测试之后运行。
* :c:type:`ztest_suite_teardown_t` - 可选的拆卸函数，将在套件中所有测试结束时运行。

以下是使用条件函数的测试套件示例：

.. code-block:: C

   #include <zephyr/ztest.h>
   #include "test_state.h"

   static bool predicate(const void *global_state)
   {
   	return ((const struct test_state*)global_state)->x == 5;
   }

   ZTEST_SUITE(alternating_suite, predicate, NULL, NULL, NULL, NULL);

向套件添加测试
**************

有5个宏用于向套件添加测试，它们是：

* :c:macro:`ZTEST` ``(suite_name, test_name)`` - 可用于通过``suite_name``给定的套件中添加名为``test_name``的测试。
* :c:macro:`ZTEST_P` ``(suite_name, test_name)`` - 通过指定``suite_name``和``test_name``向给定套件添加参数化测试。然后，您可以在测试体内使用``data``指针访问传递的参数。
* :c:macro:`ZTEST_USER` ``(suite_name, test_name)`` - 行为与:c:macro:`ZTEST`相同，唯一的区别是当:kconfig:option:`CONFIG_USERSPACE`启用时，测试将在用户空间线程中运行。
* :c:macro:`ZTEST_F` ``(suite_name, test_name)`` - 行为与:c:macro:`ZTEST`相同，唯一的区别是测试函数已经包含一个名为``fixture``的变量，其类型为``<suite_name>_fixture``。
* :c:macro:`ZTEST_USER_F` ``(suite_name, test_name)`` - 结合了:c:macro:`ZTEST_F`的固件功能和测试的用户空间线程功能。

测试固件
=========

测试固件可用于帮助简化重复的测试设置操作。在许多情况下，同一套件中的测试需要一些初始设置，然后在每次测试之间进行某种形式的重置。这是通过固件按以下方式实现的：

.. code-block:: C

   #include <zephyr/ztest.h>

   struct my_suite_fixture {
   	size_t max_size;
   	size_t size;
   	uint8_t buff[1];
   };

   static void *my_suite_setup(void)
   {
   	/* 分配带有256字节缓冲区的固件 */
      struct my_suite_fixture *fixture = malloc(sizeof(struct my_suite_fixture) + 255);

   	zassume_not_null(fixture, NULL);
   	fixture->max_size = 256;

   	return fixture;
   }

   static void my_suite_before(void *f)
   {
   	struct my_suite_fixture *fixture = (struct my_suite_fixture *)f;
   	zmemset(fixture->buff, 0, fixture->max_size);
   	fixture->size = 0;
   }

   static void my_suite_teardown(void *f)
   {
      free(f);
   }

   ZTEST_SUITE(my_suite, NULL, my_suite_setup, my_suite_before, NULL, my_suite_teardown);

   ZTEST_F(my_suite, test_feature_x)
   {
   	zassert_equal(0, fixture->size);
   	zassert_equal(256, fixture->max_size);
   }

在用户空间线程中使用测试固件分配的内存，例如在执行:c:macro:`ZTEST_USER`或:c:macro:`ZTEST_USER_F`期间，需要将该内存声明为用户空间可访问的。这是因为固件内存由内核空间拥有和初始化。Ztest框架提供了:c:macro:`ZTEST_DMEM`和:c:macro:`ZTEST_BMEM`宏用于这种用户/内核空间共享内存的使用。

高级功能
********

测试结果期望
============

某些测试是为了失败而创建的。在由于代码的性质而预期测试将失败或跳过的情况下，可以将测试标记为如此。例如：

  .. code-block:: C

    #include <zephyr/ztest.h>

    ZTEST_SUITE(my_suite, NULL, NULL, NULL, NULL, NULL);

    ZTEST_EXPECT_FAIL(my_suite, test_fail);
    ZTEST(my_suite, test_fail)
    {
      /** 这将使测试失败 */
      zassert_true(false, NULL);
    }

    ZTEST_EXPECT_SKIP(my_suite, test_skip);
    ZTEST(my_suite, test_skip)
    {
      /** 这将跳过测试 */
      zassume_true(false, NULL);
    }

在这个例子中，上述测试应分别标记为失败和跳过。相反，由于期望，Ztest会将两者都标记为通过。

测试规则
========

测试规则是一种为每个测试和每个套件运行相同逻辑的方法。在许多情况下，您可能想要在二进制文件中的每个测试之前重置某些状态（无论当前运行的是哪个套件）。例如，这可能是为了重置模拟器、重置仿真器、刷新UART等：

.. code-block:: C

   #include <zephyr/fff.h>
   #include <zephyr/ztest.h>

   #include "test_mocks.h"

   DEFINE_FFF_GLOBALS;

   DEFINE_FAKE_VOID_FUN(my_weak_func);

   static void fff_reset_rule_before(const struct ztest_unit_test *test, void *fixture)
   {
   	ARG_UNUSED(test);
   	ARG_UNUSED(fixture);

   	RESET_FAKE(my_weak_func);
   }

   ZTEST_RULE(fff_reset_rule, fff_reset_rule_before, NULL);

自定义 ``test_main``
==================

虽然Ztest框架提供了默认的:c:func:`test_main`函数，但某些应用程序可能希望提供自定义行为。如果测试依赖的某些全局状态无法复制或在不使用重新启动进程的情况下难以复制，这一点尤其正确。例如，这样的状态可能是电源序列。假设有一个板上电序列包含多个步骤，可以使用``predicate``编写测试套件来控制其运行时间。在这种情况下，:c:func:`test_main`函数可以编写如下：

.. code-block:: C

   #include <zephyr/ztest.h>

   #include "my_test.h"

   void test_main(void)
   {
        struct power_sequence_state state;

        /* 只有使用检查phase == PWR_PHASE_0的条件函数的套件才会运行。 */
        state.phase = PWR_PHASE_0;
        ztest_run_all(&state, false, 1, 1);

        /* 只有使用检查phase == PWR_PHASE_1的条件函数的套件才会运行。 */
        state.phase = PWR_PHASE_1;
        ztest_run_all(&state, false, 1, 1);

        /* 只有使用检查phase == PWR_PHASE_2的条件函数的套件才会运行。 */
        state.phase = PWR_PHASE_2;
        ztest_run_all(&state, false, 1, 1);

        /* 检查此二进制文件中的所有套件至少运行过一次。 */
        ztest_verify_all_test_suites_ran();
   }


快速入门 - 集成测试
******************

一个简单的工作基础位于:zephyr_file:`samples/subsys/testsuite/integration`。要为**foo**的**bar**组件创建测试应用程序，您应将示例文件夹复制到``tests/foo/bar``并在那里编辑文件，以适应您的测试应用程序的目的。

要构建并执行测试应用程序中定义的所有适用测试场景，请使用:ref:`Twister <twister_script>`工具，例如：

.. code-block:: console

    ./scripts/twister -T tests/foo/bar/

要仅选择一个测试场景，请使用``--scenario``命令运行Twister：

.. code-block:: console

   ./scripts/twister --scenario tests/foo/bar/your.test.scenario.name

在上面的命令行中，``tests/foo/bar``是测试应用程序的路径，``your.test.scenario.name``引用在:file:`testcase.yaml`文件中定义的测试场景，这类似于样板测试套件示例中的``sample.testing.ztest``。

有关Twister如何处理Ztest应用程序的更多详细信息，请参见:ref:`Twister测试项目图<twister_test_project_diagram>`。

示例包含以下文件：

CMakeLists.txt

.. literalinclude:: ../../../samples/subsys/testsuite/integration/CMakeLists.txt
   :language: CMake
   :linenos:

testcase.yaml

.. literalinclude:: ../../../samples/subsys/testsuite/integration/testcase.yaml
   :language: yaml
   :linenos:

prj.conf

.. literalinclude:: ../../../samples/subsys/testsuite/integration/prj.conf
   :language: text
   :linenos:

src/main.c

.. literalinclude:: ../../../samples/subsys/testsuite/integration/src/main.c
   :language: c
   :linenos:

.. contents::
   :depth: 1
   :local:
   :backlinks: top



测试应用程序可以由多个测试套件组成，这些套件可以测试功能或API。实现测试用例的函数应遵循以下准则：

* 测试用例函数名应以**test_**前缀开头
* 测试用例应使用doxygen进行文档化
* 测试用例函数名在被测试的节或组件中应该是唯一的

例如：

.. code-block:: C

   /**
    * @brief 测试断言
    *
    * 此测试用例验证zassert_true宏。
    */
   ZTEST(my_suite, test_assert)
   {
           zassert_true(1, "1 was false");
   }

列出测试
========

Zephyr树中的测试（测试应用程序）由许多作为项目一部分运行并测试类似功能的测试场景组成，例如API或功能。``twister``脚本可以解析所有测试应用程序或其中一部分的测试场景、套件和用例，并可以在粒度级别生成报告，即测试用例是否通过或失败，或是否被阻止或跳过。

Twister解析源文件以查找测试用例名称，因此您可以通过运行以下命令列出所有内核测试用例：

.. code-block:: console

   ./scripts/twister --list-tests -T tests/kernel

跳过测试
========

特殊或特定于架构的测试无法在所有平台和架构上运行，但是我们仍希望将这些测试计入并报告为跳过。因为测试清单和测试列表是从代码中提取的，在测试套件内添加条件是次优的。需要为某个平台或功能跳过的测试需要使用:c:func:`ztest_test_skip`或:c:macro:`Z_TEST_SKIP_IFDEF`显式报告跳过。如果测试运行，它需要报告通过或失败。例如：

.. code-block:: C

   #ifdef CONFIG_TEST1
   ZTEST(common, test_test1)
   {
   	zassert_true(1, "true");
   }
   #else
   ZTEST(common, test_test1)
   {
   	ztest_test_skip();
   }
   #endif

   ZTEST(common, test_test2)
   {
   	Z_TEST_SKIP_IFDEF(CONFIG_BUGxxxxx);
   	zassert_equal(1, 0, NULL);
   }

   ZTEST_SUITE(common, NULL, NULL, NULL, NULL, NULL);

.. _ztest_unit_testing:

快速入门 - 单元测试
******************

Ztest可以用于单元测试。这意味着，您可以在不包含整个Zephyr OS来测试单个函数的情况下，将测试工作集中在正在讨论的特定模块上。这将加速测试，因为只需要编译模块，并且被测试的函数将被直接调用。

要设置单元测试，您必须将CMakeLists.txt、testcases.yml和prj.conf添加到包含单元测试源文件的目录。从该目录构建的生成二进制文件使用-DBOARD=unit_testing构建。当调用twister时，脚本zephyr/scripts/pylib/twister/twisterlib/testplan.py会过滤掉所有未设置type: unit的testcases.yml。只有使用BOARD=unit_testing的固件构建才会执行单元测试。

CMakeLists.txt
==============

为了声明源文件夹中存在的单元测试，您需要将相关源文件添加到CMake :zephyr_file:`unittest <cmake/modules/unittest.cmake>`组件的``testbinary``目标。请参阅下面的最小示例：

.. code-block:: cmake

   cmake_minimum_required(VERSION 3.20.0)

   project(app)
   find_package(Zephyr COMPONENTS unittest REQUIRED HINTS $ENV{ZEPHYR_BASE})
   target_sources(testbinary PRIVATE main.c)

由于您不会包含大多数代码所依赖的基本内核数据结构，您必须在测试中提供函数存根。Ztest提供了一些用于模拟函数的辅助函数，如下所示。

在单元测试中，模拟对象可以模拟复杂真实对象的行为，并用于通过验证是否与对象发生了交互来决定测试是失败还是通过，并根据需要断言该交互的顺序。

testcases.yaml
==============

您必须在testcase.yaml中为键"type"设置值"unit"

.. code-block:: yaml

   tests:
      testscenario.testsuite:
         tags: your_tag
         type: unit

prj.conf
========

对于单元测试，这通常只包含

.. code-block:: kconfig

   CONFIG_ZTEST=y

如果您的单元测试需要额外的库（例如math-lib），您必须通过CMakeLists.txt或在testcase.yaml中添加它们：

.. code-block:: yaml

   tests:
      testscenario.testsuite:
         tags: your_tag
         type: unit
         extra_args:
            - EXTRA_LDFLAGS="-lm"

单元测试的示例可以在:zephyr_file:`tests/unit/`文件夹中找到。

声明测试套件的最佳实践
*******************************************

*twister*和其他验证工具需要获取Zephyr *ztest*测试图像将公开的测试用例列表。

.. admonition:: 理论依据

   这一切都是为了可追溯性。仅仅有一个信号量测试应用程序是不够的。我们还需要表明我们为所有API和功能都有测试点，并追溯到API文档和功能需求。

   我们的想法是测试报告显示每个测试用例的结果为通过、失败、阻止或跳过。仅报告高级测试应用程序，特别是当测试做太多事情时，是过于模糊的。

其他问题：

- 为什么不使用CPP预扫描然后解析？或后扫描ELF文件？

  如果C预处理或构建由于任何问题而失败，我们将无法判断子情况。

- 为什么不在YAML测试配置中声明它们？

  单独的测试用例描述文件比将信息保存在测试源文件本身中更难维护——只更新一个文件在更改时消除了重复。

压力测试框架
*********************

Zephyr压力测试框架（Ztress）提供了在多个优先级上下文中执行用户函数的环境。它可用于验证代码对抢占的恢复能力。框架跟踪每个上下文的执行和抢占次数。执行可以有各种完成条件，如超时、执行次数或抢占次数。

框架通过创建请求数量的线程（每个在不同优先级上）来设置环境，可选择地启动定时器。对于每个上下文，调用用户函数（每个上下文不同），然后上下文休眠随机数量的系统时钟节拍。框架跟踪CPU负载并调整睡眠期间以实现更高的CPU负载。为了增加抢占的概率，系统时钟频率应该相对较高。QEMU x86上的默认100 Hz太低，建议将其增加到100 kHz。

使用:c:macro:`ZTRESS_EXECUTE`设置并执行压力测试环境，该宏接受可变数量的参数。每个参数是由:c:macro:`ZTRESS_TIMER`或:c:macro:`ZTRESS_THREAD`宏指定的上下文。上下文按优先级降序指定。每个上下文通过提供最小执行次数和抢占次数来指定完成条件。当满足所有条件且执行完成时，打印执行报告并返回宏。请注意，在测试执行期间，会定期打印进度报告。

可以通过指定测试超时（:c:func:`ztress_set_timeout`）或显式中止（:c:func:`ztress_abort`）提前完成执行。

用户函数参数包含执行计数器和指示是否是最后执行的标志。

下面的示例演示如何设置和运行3个上下文（其中一个是k_timer中断处理程序上下文）。完成标准设置为每个上下文至少10000次执行和最低优先级上下文1000次抢占。此外，如果未满足这些条件，则配置超时在10秒后完成。每个上下文的最后一个参数是初始睡眠时间，在整个测试过程中将调整该时间以实现最高的CPU负载。

  .. code-block:: C

             ztress_set_timeout(K_MSEC(10000));
             ZTRESS_EXECUTE(ZTRESS_TIMER(foo_0, user_data_0, 10000, Z_TIMEOUT_TICKS(20)),
                            ZTRESS_THREAD(foo_1, user_data_1, 10000, 0, Z_TIMEOUT_TICKS(20)),
                            ZTRESS_THREAD(foo_2, user_data_2, 10000, 1000, Z_TIMEOUT_TICKS(20)));

配置
=============

Ztress的静态配置包含：

 - :kconfig:option:`CONFIG_ZTRESS_MAX_THREADS` - 支持的线程数。
 - :kconfig:option:`CONFIG_ZTRESS_STACK_SIZE` - 创建线程的栈大小。
 - :kconfig:option:`CONFIG_ZTRESS_REPORT_PROGRESS_MS` - 测试进度报告间隔。

API参考
*************

运行测试
=============

.. doxygengroup:: ztest_test

断言
==========

如果相关断言失败，这些宏将立即使测试失败。当断言失败时，它将打印当前文件、行和函数，以及失败的原因和可选消息。如果配置:kconfig:option:`CONFIG_ZTEST_ASSERT_VERBOSE`为0，断言将只打印文件和行号，减少测试的二进制大小。

失败宏``zassert_equal(buf->ref, 2, "Invalid refcount")``的示例输出：

.. code-block:: none

    Assertion failed at main.c:62: test_get_single_buffer: Invalid refcount (buf->ref not equal to 2)
    Aborted at unit test function

.. doxygengroup:: ztest_assert


期望
============

如果相关期望失败，这些宏将继续测试执行，并随后在执行结束时使测试失败。当期望失败时，它将打印当前文件、行和函数，以及失败的原因和可选消息，但继续执行测试。如果配置:kconfig:option:`CONFIG_ZTEST_ASSERT_VERBOSE`为0，期望将只打印文件和行号，减少测试的二进制大小。

例如，如果以下期望失败：

.. code-block:: C

   zexpect_equal(buf->ref, 2, "Invalid refcount");
   zexpect_equal(buf->ref, 1337, "Invalid refcount");

输出将看起来像：

.. code-block:: none

   START - test_get_single_buffer
       Expectation failed at main.c:62: test_get_single_buffer: Invalid refcount (buf->ref not equal to 2)
       Expectation failed at main.c:63: test_get_single_buffer: Invalid refcount (buf->ref not equal to 1337)
    FAIL - test_get_single_buffer in 0.0 seconds

.. doxygengroup:: ztest_expect

假设
===========

如果相关假设失败，这些宏将立即跳过测试或套件。当假设失败时，它将打印当前文件、行和函数，以及失败的原因和可选消息。如果配置:kconfig:option:`CONFIG_ZTEST_ASSERT_VERBOSE`为0，假设将只打印文件和行号，减少测试的二进制大小。

失败宏``zassume_equal(buf->ref, 2, "Invalid refcount")``的示例输出：

.. code-block::none

    START - test_get_single_buffer
        Assumption failed at main.c:62: test_get_single_buffer: Invalid refcount (buf->ref not equal to 2)
     SKIP - test_get_single_buffer in 0.0 seconds

.. doxygengroup:: ztest_assume


Ztress
======

.. doxygengroup:: ztest_ztress


.. _mocking-fff:

通过FFF进行模拟
===============

Zephyr已与FFF集成进行模拟。有关文档，请参见`FFF`_。要使用它，请包含相关头文件：

.. code-block:: C

   #include <zephyr/fff.h>

Zephyr提供几个基于FFF的虚假驱动程序，这些驱动程序可以用作存根或模拟。虚假驱动程序实例通过:ref:`devicetree`和:ref:`kconfig`进行配置。有关更多信息，请参见以下设备树绑定：

 - :dtcompatible:`zephyr,fake-can`
 - :dtcompatible:`zephyr,fake-eeprom`

Zephyr还定义了对FFF的扩展，以简化虚假函数的声明。
请参见:ref:`FFF扩展 <fff-extensions>`。

自定义测试输出
***********************
通过将:kconfig:option:`CONFIG_ZTEST_TC_UTIL_USER_OVERRIDE`设置为"y"并添加包含您覆盖的文件:file:`tc_util_user_override.h`来启用自定义。

将行``zephyr_include_directories(my_folder)``添加到项目的:file:`CMakeLists.txt`中，以让Zephyr在构建期间找到您的头文件。

请参阅文件:zephyr_file:`subsys/testsuite/include/zephyr/tc_util.h`以查看哪些宏和/或定义可以被覆盖。
这些将被以下块包围：

.. code-block:: C

   #ifndef SOMETHING
   #define SOMETHING <default implementation>
   #endif /* SOMETHING */

.. _ztest_shuffle:

洗牌测试序列
***********************
默认情况下，测试按字母数字顺序排序和运行。测试用例可能依赖于此序列。启用:kconfig:option:`CONFIG_ZTEST_SHUFFLE`以随机化顺序。测试的输出将显示失败测试的种子。对于本机模拟器构建，您可以将种子作为参数提供给twister，使用``--seed``。


重复测试
***********************
默认情况下，测试执行一次。测试用例和测试套件可以执行多次。启用:kconfig:option:`CONFIG_ZTEST_REPEAT`以多次执行测试。默认情况下，乘法因子为3，这意味着每个测试套件执行3次，每个测试用例执行3次。这可以通过:kconfig:option:`CONFIG_ZTEST_SUITE_REPEAT_COUNT`和:kconfig:option:`CONFIG_ZTEST_TEST_REPEAT_COUNT` Kconfig选项来更改。

测试选择
**************
对于为本机模拟器构建的测试，使用命令行参数列出或选择要运行的测试。测试参数期望一个逗号分隔的``suite::test``列表。您可以用``*``替换测试名称来运行套件中的所有测试。

例如

.. code-block:: bash

    $ zephyr.exe -list
    $ zephyr.exe -test="fixture_tests::test_fixture_pointer,framework_tests::test_assert_mem_equal"
    $ zephyr.exe -test="framework_tests::*"


.. _fff-extensions:

FFF扩展
**************

.. doxygengroup:: fff_extensions


.. _FFF: https://github.com/meekrosoft/fff
