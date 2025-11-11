测试套件 (Test Suites)
#######################

TF-M 包含两组测试套件 (TF-M includes two sets of test suites):

* tf-m-tests - 标准 TF-M 特定回归测试 (Standard TF-M specific regression tests)
* psa-arch-tests - 特定 PSA API 的测试套件 (安全存储等) (Test suites for specific PSA APIs (secure storage, etc.))

这些测试套件可以通过 samples/tfm_integration 文件夹中的适当示例应用程序从 Zephyr 运行 (These test suites can be run from Zephyr via an appropriate sample application
in the samples/tfm_integration folder)。

TF-M 回归测试 (TF-M Regression Tests)
**************************************

回归测试套件可以通过 :ref:`tfm_regression_test` 示例运行 (The regression test suite can be run via the :ref:`tfm_regression_test` sample)。

此示例通过 PSA API 测试跨 NS/S 边界的各种服务和通信机制。它们为 NS RTOS (本例中为 Zephyr) 和安全应用程序 (TF-M) 之间的正确集成提供了有用的健全性检查 (This sample tests various services and communication mechanisms across the
NS/S boundary via the PSA APIs. They provide a useful sanity check for proper
integration between the NS RTOS (Zephyr in this case) and the secure
application (TF-M))。

PSA 架构测试 (PSA Arch Tests)
******************************

PSA 架构测试套件可通过 :ref:`tfm_psa_test` 获得,包含许多测试套件,可用于验证安全应用程序是否遵循 PSA API 规范,TF-M 是平台安全架构 (PSA) 的一个实现 (The PSA Arch Test suite, available via :ref:`tfm_psa_test`, contains a number of
test suites that can be used to validate that PSA API specifications are
being followed by the secure application, TF-M being an implementation of
the Platform Security Architecture (PSA))。

一次只能运行这些套件中的一个,可用的测试套件通过 ``CONFIG_TFM_PSA_TEST_*`` KConfig 标志描述 (Only one of these suites can be run at a time, with the available test suites
described via ``CONFIG_TFM_PSA_TEST_*`` KConfig flags):

目的 (Purpose)
**************

这些测试套件的输出是为您的特定开发板、RTOS (此处为 Zephyr) 和 PSA 实现 (此例中为 TF-M) 获得 PSA 认证所必需的 (The output of these test suites is required to obtain PSA Certification for
your specific board, RTOS (Zephyr here), and PSA implementation (TF-M in this
case))。

它们还提供了一个有用的测试用例,用于验证对 TF-M 进行有意义更改的任何 PR,例如启用新的 TF-M 开发板目标,或对核心 TF-M 模块进行更改。它们通常应作为连贯性检查运行,然后再发布新的 PR 以支持新开发板等 (They also provide a useful test case to validate any PRs that make meaningful
changes to TF-M, such as enabling a new TF-M board target, or making changes
to the core TF-M module(s). They should generally be run as a coherence check
before publishing a new PR for new board support, etc.)。
