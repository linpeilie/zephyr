.. _vulnerabilities:

漏洞 (Vulnerabilities)
#######################

本页收集了在每个版本中发现和修复的所有漏洞。它通常还会提供比版本说明中更多的详细信息。某些漏洞被视为敏感信息,在有足够时间修复之前不会公开讨论。由于版本说明被锁定到特定版�?因此在解除禁运后可以更新此处的信�?(This page collects all of the vulnerabilities that are discovered and
fixed in each release.  It will also often have more details than is
available in the releases.  Some vulnerabilities are deemed to be
sensitive, and will not be publicly discussed until there is
sufficient time to fix them.  Because the release notes are locked to
a version, the information here can be updated after the embargo is
lifted)�?

CVE-2017
========

:cve:`2017-14199`
-----------------

:code:`getaddrinfo()` 中的缓冲区溢�?(Buffer overflow in :code:`getaddrinfo()`)�?

- `Zephyr 项目错误跟踪�?ZEPSEC-12 (Zephyr project bug tracker ZEPSEC-12)
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-12>`_

- `PR6158 fix for 1.11.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/6158>`_

:cve:`2017-14201`
-----------------

shell DNS 命令由于滥用栈变量可能导致不可预测的结果 (The shell DNS command can cause unpredictable results due to misuse of
stack variables)�?

Zephyr shell 中的释放后使用漏洞允许串行或 telnet 连接的用户导致拒绝服�?并可能导致远程代码执�?(Use After Free vulnerability in the Zephyr shell allows a serial or
telnet connected user to cause denial of service, and possibly remote
code execution)�?

此问题已�?v1.14.0 版本中修�?(This has been fixed in release v1.14.0)�?

- `Zephyr 项目错误跟踪�?ZEPSEC-17 (Zephyr project bug tracker ZEPSEC-17)
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-17>`_

- `PR13260 fix for v1.14.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/13260>`_

:cve:`2017-14202`
-----------------

shell 实现不能防止缓冲区溢�?导致不可预测的行�?(The shell implementation does not protect against buffer overruns
resulting in unpredictable behavior)�?

Zephyr �?shell 组件中的内存缓冲区边界内操作限制不当漏洞允许串行�?telnet 连接的用户导致崩�?可能伴随任意代码执行 (Improper Restriction of Operations within the Bounds of a Memory
Buffer vulnerability in the shell component of Zephyr allows a serial
or telnet connected user to cause a crash, possibly with arbitrary
code execution)�?

此问题已�?v1.14.0 版本中修�?(This has been fixed in release v1.14.0)�?

- `Zephyr 项目错误跟踪�?ZEPSEC-18 (Zephyr project bug tracker ZEPSEC-18)
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-18>`_

- `PR13048 fix for v1.14.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/13048>`_

CVE-2019
========

:cve:`2019-9506`
----------------

蓝牙 BR/EDR 规范(包括 5.1 版本)允许足够低的加密密钥长度,并且不阻止攻击者影响密钥长度协商。这允许实际的暴力攻�?又名"KNOB")可以解密流量并在受害者不注意的情况下注入任意密文 (The Bluetooth BR/EDR specification up to and including version 5.1
permits sufficiently low encryption key length and does not prevent an
attacker from influencing the key length negotiation. This allows
practical brute-force attacks (aka "KNOB") that can decrypt traffic
and inject arbitrary ciphertext without the victim noticing)�?

- `Zephyr 项目错误跟踪�?ZEPSEC-20 (Zephyr project bug tracker ZEPSEC-20)
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-20>`_

- `PR18702 fix for v1.14.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/18702>`_

- `PR18659 fix for v2.0.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/18659>`_

CVE-2020
========

:cve:`2020-10019`
-----------------

zephyr �?USB DFU 中的缓冲区溢出漏洞允�?USB 连接的主机可能导致远程代码执�?(Buffer Overflow vulnerability in USB DFU of zephyr allows a USB
connected host to cause possible remote code execution)�?

此问题已�?v1.14.2、v2.2.0 �?v2.1.1 版本中修�?(This has been fixed in releases v1.14.2, v2.2.0, and v2.1.1)�?

- `Zephyr 项目错误跟踪�?ZEPSEC-25 (Zephyr project bug tracker ZEPSEC-25)
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-25>`_

- `PR23460 fix for 1.14.x
  <https://github.com/zephyrproject-rtos/zephyr/pull/23460>`_

- `PR23457 fix for 2.1.x
  <https://github.com/zephyrproject-rtos/zephyr/pull/23457>`_

- `PR23190 fix in 2.2.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/23190>`_

:cve:`2020-10021`
-----------------

USB 大容量存储中不对齐大小的越界写入 (Out-of-bounds write in USB Mass Storage with unaligned sizes)

USB 大容量存�?memoryWrite 处理程序中不对齐大小的越界写�?(Out-of-bounds Write in the USB Mass Storage memoryWrite handler with
unaligned Sizes)�?

参见 NCC-ZEP-024、NCC-ZEP-025、NCC-ZEP-026 (See NCC-ZEP-024, NCC-ZEP-025, NCC-ZEP-026)

此问题已�?v1.14.2 �?v2.2.0 版本中修�?(This has been fixed in releases v1.14.2, and v2.2.0)�?

- `Zephyr 项目错误跟踪�?ZEPSEC-26 (Zephyr project bug tracker ZEPSEC-26)
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-26>`_

- `PR23455 fix for v1.14.2
  <https://github.com/zephyrproject-rtos/zephyr/pull/23455>`_

- `PR23456 fix for the v2.1 branch
  <https://github.com/zephyrproject-rtos/zephyr/pull/23456>`_

- `PR23240 fix for v2.2.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/23240>`_

:cve:`2020-10022`
-----------------

UpdateHub 模块将可变大小的哈希字符串复制到固定大小的数组中 (UpdateHub Module Copies a Variable-Size Hash String Into a Fixed-Size Array)

�?UpdateHub 服务器接收的格式错误�?JSON 载荷可能会触�?Zephyr OS 中的内存损坏。在最好的情况下这可能导致拒绝服务,在最坏的情况下可能导致代码执�?(A malformed JSON payload that is received from an UpdateHub server may
trigger memory corruption in the Zephyr OS. This could result in a
denial of service in the best case, or code execution in the worst
case)�?

参见 NCC-ZEP-016 (See NCC-ZEP-016)

此问题已在以下针对主分支、v2.1.0 分支�?v2.2.0 分支的拉取请求中修复 (This has been fixed in the below pull requests for main, branch from
v2.1.0, and branch from v2.2.0)�?

- `Zephyr 项目错误跟踪�?ZEPSEC-28 (Zephyr project bug tracker ZEPSEC-28)
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-28>`_

- `PR24154 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/24154>`_

- `PR24065 fix for branch from v2.1.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/24065>`_

- `PR24066 fix for branch from v2.2.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/24066>`_

:cve:`2020-10023`
-----------------

Shell 子系统在 shell_spaces_trim 中包含缓冲区溢出漏洞 (Shell Subsystem Contains a Buffer Overflow Vulnerability In
shell_spaces_trim)

shell 子系统包含缓冲区溢出,攻击者通过物理访问设备能够导致内存损坏,从而导致拒绝服务或可能�?Zephyr 内核中执行代�?(The shell subsystem contains a buffer overflow, whereby an adversary
with physical access to the device is able to cause a memory
corruption, resulting in denial of service or possibly code execution
within the Zephyr kernel)�?

参见 NCC-ZEP-019 (See NCC-ZEP-019)

此问题已�?v1.14.2、v2.2.0 版本以及 v2.1.0 的分支中修复 (This has been fixed in releases v1.14.2, v2.2.0, and in a branch from
v2.1.0)�?

- `Zephyr 项目错误跟踪�?ZEPSEC-29 (Zephyr project bug tracker ZEPSEC-29)
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-29>`_

- `PR23646 fix for v1.14.2
  <https://github.com/zephyrproject-rtos/zephyr/pull/23646>`_

- `PR23649 fix for branch from v2.1.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/23649>`_

- `PR23304 fix for v2.2.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/23304>`_

:cve:`2020-10024`
-----------------

ARM 平台在验证系统调用号时使用有符号整数比较 (ARM Platform Uses Signed Integer Comparison When Validating Syscall
Numbers)

arm 平台特定代码在验证系统调用号时使用有符号整数比较。在用户线程中获得代码执行权限的攻击者能够将权限提升到内核权�?(The arm platform-specific code uses a signed integer comparison when
validating system call numbers. An attacker who has obtained code
execution within a user thread is able to elevate privileges to that
of the kernel)�?

参见 NCC-ZEP-001 (See NCC-ZEP-001)

此问题已�?v1.14.2、v2.2.0 版本以及 v2.1.0 的分支中修复 (This has been fixed in releases v1.14.2, and v2.2.0, and in a branch
from v2.1.0)�?

- `Zephyr 项目错误跟踪�?ZEPSEC-30 (Zephyr project bug tracker ZEPSEC-30)
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-30>`_

- `PR23535 fix for v1.14.2
  <https://github.com/zephyrproject-rtos/zephyr/pull/23535>`_

- `PR23498 fix for branch from v2.1.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/23498>`_

- `PR23323 fix for v2.2.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/23323>`_

:cve:`2020-10027`
-----------------

ARC 平台在验证系统调用号时使用有符号整数比较 (ARC Platform Uses Signed Integer Comparison When Validating Syscall
Numbers)

在用户线程中获得代码执行权限的攻击者能够将权限提升到内核权�?(An attacker who has obtained code execution within a user thread is
able to elevate privileges to that of the kernel)�?

参见 NCC-ZEP-001 (See NCC-ZEP-001)

此问题已�?v1.14.2、v2.2.0 版本以及 v2.1.0 的分支中修复 (This has been fixed in releases v1.14.2, and v2.2.0, and in a branch
from v2.1.0)�?

- `Zephyr 项目错误跟踪�?ZEPSEC-35 (Zephyr project bug tracker ZEPSEC-35)
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-35>`_

- `PR23500 fix for v1.14.2
  <https://github.com/zephyrproject-rtos/zephyr/pull/23500>`_

- `PR23499 fix for branch from v2.1.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/23499>`_

- `PR23328 fix for v2.2.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/23328>`_

:cve:`2020-10028`
-----------------

GPIO 子系统中的多个系统调用不执行参数验证 (Multiple Syscalls In GPIO Subsystem Performs No Argument Validation)

参数验证不充分的多个系统调用 (Multiple syscalls with insufficient argument validation)

参见 NCC-ZEP-006 (See NCC-ZEP-006)

此问题已�?v1.14.2、v2.2.0 版本以及 v2.1.0 的分支中修复 (This has been fixed in releases v1.14.2, and v2.2.0, and in a branch
from v2.1.0)�?

- `Zephyr 项目错误跟踪�?ZEPSEC-32 (Zephyr project bug tracker ZEPSEC-32)
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-32>`_

- `PR23733 fix for v1.14.2
  <https://github.com/zephyrproject-rtos/zephyr/pull/23733>`_

- `PR23737 fix for branch from v2.1.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/23737>`_

- `PR23308 fix for v2.2.0 (gpio patch)
  <https://github.com/zephyrproject-rtos/zephyr/pull/23308>`_

:cve:`2020-10058`
-----------------

kscan 子系统中的多个系统调用不执行参数验证 (Multiple Syscalls In kscan Subsystem Performs No Argument Validation)

Kscan 子系统中的多个系统调用执行的参数验证不充�?允许在用户空间中执行的代码可能获得提升的权限 (Multiple syscalls in the Kscan subsystem perform insufficient argument
validation, allowing code executing in userspace to potentially gain
elevated privileges)�?

参见 NCC-ZEP-006 (See NCC-ZEP-006)

此问题已�?v2.1.0 的分支和 v2.2.0 版本中修�?(This has been fixed in a branch from v2.1.0, and release v2.2.0)�?

- `Zephyr 项目错误跟踪�?ZEPSEC-34 (Zephyr project bug tracker ZEPSEC-34)
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-34>`_

- `PR23748 fix for branch from v2.1.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/23748>`_

- `PR23308 fix for v2.2.0 (kscan patch)
  <https://github.com/zephyrproject-rtos/zephyr/pull/23308>`_

:cve:`2020-10059`
-----------------

UpdateHub 模块明确禁用 TLS 验证 (UpdateHub Module Explicitly Disables TLS Verification)

UpdateHub 模块禁用 DTLS 对等检�?这允许中间人攻击。这通过要求固件镜像具有有效签名来缓解。但�?在没有对等检查的情况下使�?DTLS 没有任何好处 (The UpdateHub module disables DTLS peer checking, which allows for a
man in the middle attack. This is mitigated by firmware images
requiring valid signatures. However, there is no benefit to using DTLS
without the peer checking)�?

参见 NCC-ZEP-018 (See NCC-ZEP-018)

此问题已在针�?Zephyr 主分支的 PR 中修�?(This has been fixed in a PR against Zephyr main)�?

- `Zephyr 项目错误跟踪�?ZEPSEC-36 (Zephyr project bug tracker ZEPSEC-36)
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-36>`_

- `PR24954 fix on main (to be fixed in v2.3.0)
  <https://github.com/zephyrproject-rtos/zephyr/pull/24954>`_

- `PR24954 fix v2.1.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/24999>`_

- `PR24954 fix v2.2.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/24997>`_

:cve:`2020-10060`
-----------------

UpdateHub 可能解引用未初始化的指针 (UpdateHub Might Dereference An Uninitialized Pointer)

�?updatehub_probe �?JSON 解析完成�?从输出结构的两个不同位置访问 objects\[1]。如�?JSON 包含少于两个元素,此访问将引用未初始化的栈内存。这可能导致崩溃、拒绝服务或可能的信息泄�?(In updatehub_probe, right after JSON parsing is complete, objects\[1]
is accessed from the output structure in two different places. If the
JSON contained less than two elements, this access would reference
uninitialized stack memory. This could result in a crash, denial of
service, or possibly an information leak)�?

建议禁用 updatehub,直到可以提供修复 (Recommend disabling updatehub until such a time as a fix can be made
available)�?

参见 NCC-ZEP-030 (See NCC-ZEP-030)

此问题已在针�?Zephyr 主分支的 PR 中修�?(This has been fixed in a PR against Zephyr main)�?

- `Zephyr 项目错误跟踪�?ZEPSEC-37 (Zephyr project bug tracker ZEPSEC-37)
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-37>`_

- `PR27865 fix on main (to be fixed in v2.4.0)
  <https://github.com/zephyrproject-rtos/zephyr/pull/27865>`_

- `PR27865 fix for v2.3.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/27889>`_

- `PR27865 fix for v2.2.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/27891>`_

- `PR27865 fix for v2.1.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/27893>`_

:cve:`2020-10061`
-----------------

错误处理无效数据包序�?(Error handling invalid packet sequence)

Zephyr 蓝牙实现中对满缓冲区情况的不正确处理可能导致内存损坏 (Improper handling of the full-buffer case in the Zephyr Bluetooth
implementation can result in memory corruption)�?

此问题已�?v1.14.0、v2.2.0 的分支中修复,并将包含�?v2.3.0 �?(This has been fixed in branches for v1.14.0, v2.2.0, and will be
included in v2.3.0)�?

- `Zephyr 项目错误跟踪�?ZEPSEC-75 (Zephyr project bug tracker ZEPSEC-75)
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-75>`_

- `PR23516 fix for v2.3 (split driver)
  <https://github.com/zephyrproject-rtos/zephyr/pull/23516>`_

- `PR23517 fix for v2.3 (legacy driver)
  <https://github.com/zephyrproject-rtos/zephyr/pull/23517>`_

- `PR23091 fix for branch from v1.14.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/23091>`_

- `PR23547 fix for branch from v2.2.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/23547>`_

:cve:`2020-10062`
-----------------

MQTT 中的数据包长度解码错�?(Packet length decoding error in MQTT)

CVE: Zephyr 项目 MQTT 数据包长度解码器中的偏移一位错误可能导致内存损坏和可能的远程代码执行。NCC-ZEP-031 (An off-by-one error in the Zephyr project MQTT packet length
decoder can result in memory corruption and possible remote code
execution. NCC-ZEP-031)

MQTT 数据包头长度可以�?1 �?4 字节。代码中的偏移一位错误可能导致这被解释为 5 字节,这可能导致整数溢�?从而导致内存损�?(The MQTT packet header length can be 1 to 4 bytes. An off-by-one error
in the code can result in this being interpreted as 5 bytes, which can
cause an integer overflow, resulting in memory corruption)�?

此问题已�?v2.3 的主分支中修�?(This has been fixed in main for v2.3)�?

- `Zephyr 项目错误跟踪�?ZEPSEC-84 (Zephyr project bug tracker ZEPSEC-84)
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-84>`_

- `commit 11b7a37d for v2.3
  <https://github.com/zephyrproject-rtos/zephyr/pull/23821/commits/11b7a37d9a0b438270421b224221d91929843de4>`_

- `NCC-ZEP report`_ (NCC-ZEP-031)

.. _NCC-ZEP report: https://research.nccgroup.com/2020/05/26/research-report-zephyr-and-mcuboot-security-assessment

:cve:`2020-10063` CoAP选项解析整数溢出导致远程拒绝服务 (Remote Denial of Service in CoAP Option Parsing Due To Integer Overflow)
-----------------------------------------------------------------------------------------------------------------------------------------

能够发送任意CoAP数据包被Zephyr解析的远程攻击者能够造成拒绝服务 (A remote adversary with the ability to send arbitrary CoAP packets to be parsed by Zephyr is able to cause a denial of service)�?

此问题已在v2.3的main分支中修�?(This has been fixed in main for v2.3)�?

- `Zephyr project bug tracker ZEPSEC-55
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-55>`_

- `PR24435 fix in main for v2.3
  <https://github.com/zephyrproject-rtos/zephyr/pull/24435>`_

- `PR24531 fix for branch from v2.2
  <https://github.com/zephyrproject-rtos/zephyr/pull/24531>`_

- `PR24535 fix for branch from v2.1
  <https://github.com/zephyrproject-rtos/zephyr/pull/24535>`_

- `PR24530 fix for branch from v1.14
  <https://github.com/zephyrproject-rtos/zephyr/pull/24530>`_

- `NCC-ZEP report`_ (NCC-ZEP-032)

:cve:`2020-10064` ieee802154处理中的输入帧验证不�?(Improper Input Frame Validation in ieee802154 Processing)
-------------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker ZEPSEC-65
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-65>`_

- `PR24971 fix for v2.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/24971>`_

- `PR33451 fix for v1.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/33451>`_

:cve:`2020-10065` 蓝牙HCI over SPI驱动的越界写�?(OOB Write in Bluetooth HCI over SPI Driver)
------------------------------------------------------------------------------------------------------------------------

未验证用户提供的长度(<= 0xffff)并复制到固定大小缓冲�?默认:77字节)的HCI_ACL数据�?导致越界写入 (OOB Write after not validating user-supplied length (<= 0xffff) and copying to fixed-size buffer (default: 77 bytes) for HCI_ACL packets in bluetooth HCI over SPI driver)�?

- `Zephyr project bug tracker ZEPSEC-66
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-66>`_

- This issue has not been fixed.

:cve:`2020-10066` 蓝牙HCI核心中的错误处理不当 (Incorrect Error Handling in Bluetooth HCI core)
-------------------------------------------------------------------------------------------------------------------

在hci_cmd_done�?buf参数传递为null导致空指针解引用 (In hci_cmd_done, the buf argument being passed as null causes nullpointer dereference)�?

- `Zephyr project bug tracker ZEPSEC-67
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-67>`_

- `PR24902 fix for v2.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/24902>`_

- `PR25089 fix for v1.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/25089>`_

:cve:`2020-10067` is_in_region整数溢出允许用户线程访问内核内存 (Integer Overflow In is_in_region Allows User Thread To Access Kernel Memory)
--------------------------------------------------------------------------------------------------------------------------------------------------------

恶意的用户空间应用程序可以引发整数溢出并绕过系统调用处理器执行的安全检查。影响取决于底层系统调用,范围可从拒绝服务到信息泄露再到导致内核代码执行的内存损坏 (A malicious userspace application can cause a integer overflow and bypass security checks performed by system call handlers. The impact would depend on the underlying system call and can range from denial of service to information leak to memory corruption resulting in code execution within the kernel)�?

参见NCC-ZEP-005 (See NCC-ZEP-005)

此问题已在v1.14.2和v2.2.0版本中修�?(This has been fixed in releases v1.14.2, and v2.2.0)�?

- `Zephyr project bug tracker ZEPSEC-27
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-27>`_

- `PR23653 fix for v1.14.2
  <https://github.com/zephyrproject-rtos/zephyr/pull/23653>`_

- `PR23654 fix for the v2.1 branch
  <https://github.com/zephyrproject-rtos/zephyr/pull/23654>`_

- `PR23239 fix for v2.2.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/23239>`_

:cve:`2020-10068` Zephyr蓝牙DLE重复请求漏洞 (Zephyr Bluetooth DLE duplicate requests vulnerability)
----------------------------------------------------------------------------------------------------------------------------

在Zephyr项目蓝牙子系统中,某些重复和连续的数据包可能导致不正确的行�?从而引发拒绝服�?(In the Zephyr project Bluetooth subsystem, certain duplicate and back-to-back packets can cause incorrect behavior, resulting in a denial of service)�?

此问题已在v1.14.0和v2.2.0分支中修�?并将包含在v2.3.0�?(This has been fixed in branches for v1.14.0, v2.2.0, and will be included in v2.3.0)�?

- `Zephyr project bug tracker ZEPSEC-78
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-78>`_

- `PR23707 fix for v2.3 (split driver)
  <https://github.com/zephyrproject-rtos/zephyr/pull/23707>`_

- `PR23708 fix for v2.3 (legacy driver)
  <https://github.com/zephyrproject-rtos/zephyr/pull/23708>`_

- `PR23091 fix for branch from v1.14.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/23091>`_

- `PR23964 fix for v2.2.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/23964>`_

:cve:`2020-10069` Zephyr蓝牙未检查的数据包数据导致拒绝服�?(Zephyr Bluetooth unchecked packet data results in denial of service)
------------------------------------------------------------------------------------------------------------------------------------------------

蓝牙数据中未检查的参数可能导致断言失败或除零错�?从而引发拒绝服务攻�?(An unchecked parameter in bluetooth data can result in an assertion failure, or division by zero, resulting in a denial of service attack)�?

此问题已在v1.14.0和v2.2.0分支中修�?并将包含在v2.3.0�?(This has been fixed in branches for v1.14.0, v2.2.0, and will be included in v2.3.0)�?

- `Zephyr project bug tracker ZEPSEC-81
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-81>`_

- `PR23705 fix for v2.3 (split driver)
  <https://github.com/zephyrproject-rtos/zephyr/pull/23705>`_

- `PR23706 fix for v2.3 (legacy driver)
  <https://github.com/zephyrproject-rtos/zephyr/pull/23706>`_

- `PR23091 fix for branch from v1.14.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/23091>`_

- `PR23963 fix for branch from v2.2.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/23963>`_

:cve:`2020-10070` MQTT接收缓冲区溢�?(MQTT buffer overflow on receive buffer)
----------------------------------------------------------------------------------------------------------

在Zephyr项目的MQTT代码�?不当的边界检查可能导致内存损坏并可能引发远程代码执行。NCC-ZEP-031 (In the Zephyr Project MQTT code, improper bounds checking can result in memory corruption and possibly remote code execution.  NCC-ZEP-031)

计算数据包长度时,算术溢出可能导致接受大于可用缓冲区空间的接收缓冲�?从而导致用户数据被写入超出此缓冲区的位�?(When calculating the packet length, arithmetic overflow can result in accepting a receive buffer larger than the available buffer space, resulting in user data being written beyond this buffer)�?

此问题已在v2.3的main分支中修�?(This has been fixed in main for v2.3)�?

- `Zephyr project bug tracker ZEPSEC-85
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-85>`_

- `commit 0b39cbf3 for v2.3
  <https://github.com/zephyrproject-rtos/zephyr/pull/23821/commits/0b39cbf3c01d7feec9d0dd7cc7e0e374b6113542>`_

- `NCC-ZEP report`_ (NCC-ZEP-031)

:cve:`2020-10071` MQTT发布消息长度验证不足 (Insufficient publish message length validation in MQTT)
---------------------------------------------------------------------------------------------------------------------------

Zephyr MQTT解析代码对发布消息的长度字段执行的检查不�?允许缓冲区溢出并可能引发远程代码执行。NCC-ZEP-031 (The Zephyr MQTT parsing code performs insufficient checking of the length field on publish messages, allowing a buffer overflow and potentially remote code execution. NCC-ZEP-031)

此问题已在v2.3的main分支中修�?(This has been fixed in main for v2.3)�?

- `Zephyr project bug tracker ZEPSEC-86
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-86>`_

- `commit 989c4713 fix for v2.3
  <https://github.com/zephyrproject-rtos/zephyr/pull/23821/commits/989c4713ba429aa5105fe476b4d629718f3e6082>`_

- `NCC-ZEP report`_ (NCC-ZEP-031)

:cve:`2020-10072` 所有线程可访问所有套接字文件描述�?(All threads can access all socket file descriptors)
----------------------------------------------------------------------------------------------------------------------------

网络套接字API文件描述符缺少权限管理。系统上运行的任何线程只需知道文件描述符的数值即可读写套接字文件描述�?(There is no management of permissions to network socket API file descriptors. Any thread running on the system may read/write a socket file descriptor knowing only the numerical value of the file descriptor)�?

- `Zephyr project bug tracker ZEPSEC-87
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-87>`_

- `PR25804 fix for v2.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/25804>`_

- `PR27176 fix for v1.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/27176>`_

:cve:`2020-10136` IP-in-IP协议默认路由任意流量 (IP-in-IP protocol routes arbitrary traffic by default zephyrproject)
-----------------------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker ZEPSEC-64
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-64>`_

:cve:`2020-13598` 文件系统:在FAT_FS中启用长文件名并调用fs_stat时的缓冲区溢�?(FS: Buffer Overflow when enabling Long File Names in FAT_FS and calling fs_stat)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

对文件名超过12个字符的文件执行fs_stat将导致缓冲区溢出 (Performing fs_stat on a file with a filename longer than 12 characters long will cause a buffer overflow)�?

- `Zephyr project bug tracker ZEPSEC-88
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-88>`_

- `PR25852 fix for v2.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/25852>`_

- `PR28782 fix for v2.3
  <https://github.com/zephyrproject-rtos/zephyr/pull/28782>`_

- `PR33577 fix for v1.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/33577>`_

:cve:`2020-13599` settings和littlefs的安全问�?(Security problem with settings and littlefs)
-----------------------------------------------------------------------------------------------------------------------

When settings is used in combination with littlefs all security
related information can be extracted from the device using MCUmgr and
this could be used e.g in bt-mesh to get the device key, network key,
app keys from the device.

- `Zephyr project bug tracker ZEPSEC-57
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-57>`_

- `PR26083 fix for v2.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/26083>`_

:cve:`2020-13600`
-----------------

Malformed SPI in response for eswifi can corrupt kernel memory


- `Zephyr project bug tracker ZEPSEC-91
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-91>`_

- `PR26712 fix for v2.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/26712>`_

:cve:`2020-13601`
-----------------

Possible read out of bounds in dns read

- `Zephyr project bug tracker ZEPSEC-92
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-92>`_

- `PR27774 fix for v2.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/27774>`_

- `PR30503 fix for v1.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/30503>`_

:cve:`2020-13602`
-----------------

:cve:`2020-13600` LwM2M do_write_op_tlv中的远程拒绝服务 (Remote Denial of Service in LwM2M do_write_op_tlv)
--------------------------------------------------------------------------------------------------------------------------

在Zephyr LwM2M实现�?格式错误的输入可能导致无限循�?从而引发拒绝服务攻�?(In the Zephyr LwM2M implementation, malformed input can result in an infinite loop, resulting in a denial of service attack)�?

- `Zephyr project bug tracker ZEPSEC-56
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-56>`_

- `PR26571 fix for v2.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/26571>`_

- `PR33578 fix for v1.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/33578>`_

:cve:`2020-13603` mempool中可能的溢出 (Possible overflow in mempool)
--------------------------------------------------------------------------------------------

 * Zephyr提供预构建的'malloc'包装函数 (Zephyr offers pre-built 'malloc' wrapper function instead)�?
 * 'malloc'函数�?sys_mem_pool_alloc'函数的包装器 (The 'malloc' function is wrapper for the 'sys_mem_pool_alloc' function)
 * sys_mem_pool_alloc以不安全的方式分�?size + WB_UP(sizeof(struct sys_mem_pool_block))' (sys_mem_pool_alloc allocates 'size + WB_UP(sizeof(struct sys_mem_pool_block))' in an unsafe manner)�?
 * 请求非常大的size值会导致内部整数环绕 (Asking for very large size values leads to internal integer wrap-around)�?
 * 整数环绕导致成功分配非常小的内存 (Integer wrap-around leads to successful allocation of very small memory)�?
 * 例如:调用malloc(0xffffffff)会成功分�?字节 (For example: calling malloc(0xffffffff) leads to successful allocation of 7 bytes)�?
 * 这会导致堆溢�?(That leads to heap overflow)�?

- `Zephyr project bug tracker ZEPSEC-111
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-111>`_

- `PR31796 fix for v2.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/31796>`_

- `PR32808 fix for v1.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/26571>`_

CVE-2021 (2021年度CVE)
========

:cve:`2021-3319` 拒绝服务:省略�?目的地址�?02154帧验证不正确 (DOS: Incorrect 802154 Frame Validation for Omitted Source / Dest Addresses)
-----------------------------------------------------------------------------------------------------------------------------------------------------------

在ieee802154帧验�?ieee802154_validate_frame)中对省略的源地址和目的地址处理不当 (Improper processing of omitted source and destination addresses in ieee802154 frame validation (ieee802154_validate_frame))

此问题已在v2.5.0的main分支中修�?(This has been fixed in main for v2.5.0)

- `Zephyr project bug tracker GHSA-94jg-2p6q-5364
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-94jg-2p6q-5364>`_

- `PR31908 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/31908>`_

:cve:`2021-3320` 802154 ACK帧验证与处理不匹�?(Mismatch between validation and handling of 802154 ACK frames)
--------------------------------------------------------------------------------------------------------------------------------------------

在验证期间考虑ACK�?但在实际处理期间不考虑,导致类型混淆 (ACK frames are considered during validation, but not during actual processing, leading to a type confusion)�?

- `PR31908 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/31908>`_

:cve:`2021-3321` IEEE 802154最小片段大小检查不完整导致整数下溢 (Incomplete check of minimum IEEE 802154 fragment size leading to an integer underflow)
-------------------------------------------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker ZEPSEC-114
  <https://zephyrprojectsec.atlassian.net/browse/ZEPSEC-114>`_

- `PR33453 fix for v2.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/33453>`_

:cve:`2021-3323` 6LoWPAN IPHC头解压中的整数下�?(Integer Underflow in 6LoWPAN IPHC Header Uncompression)
------------------------------------------------------------------------------------------------------------------------------------

此问题已在v2.5.0的main分支中修�?(This has been fixed in main for v2.5.0)

- `Zephyr project bug tracker GHSA-89j6-qpxf-pfpc
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-89j6-qpxf-pfpc>`_

- `PR 31971 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/31971>`_

:cve:`2021-3430` 重复的LL_CONNECTION_PARAM_REQ可触发断言 (Assertion reachable with repeated LL_CONNECTION_PARAM_REQ)
------------------------------------------------------------------------------------------------------------------------

此问题已在v2.6.0的main分支中修�?(This has been fixed in main for v2.6.0)

- `Zephyr project bug tracker GHSA-46h3-hjcq-2jjr
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-46h3-hjcq-2jjr>`_

- `PR 33272 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/33272>`_

- `PR 33369 fix for 2.5
  <https://github.com/zephyrproject-rtos/zephyr/pull/33369>`_

- `PR 33759 fix for 1.14.2
  <https://github.com/zephyrproject-rtos/zephyr/pull/33759>`_

:cve:`2021-3431` 蓝牙:重复的LL_FEATURE_REQ导致断言失败 (BT: Assertion failure on repeated LL_FEATURE_REQ)
---------------------------------------------------------------------------------------------------------------------------

此问题已在v2.6.0的main分支中修�?(This has been fixed in main for v2.6.0)

- `Zephyr project bug tracker GHSA-7548-5m6f-mqv9
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-7548-5m6f-mqv9>`_

- `PR 33340 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/33340>`_

- `PR 33369 fix for 2.5
  <https://github.com/zephyrproject-rtos/zephyr/pull/33369>`_

:cve:`2021-3432` CONNECT_IND中的无效间隔导致除零错误 (Invalid interval in CONNECT_IND leads to Division by Zero)
---------------------------------------------------------------------------------------------------------------------------------------

此问题已在v2.6.0的main分支中修�?(This has been fixed in main for v2.6.0)

- `Zephyr project bug tracker GHSA-7364-p4wc-8mj4
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-7364-p4wc-8mj4>`_

- `PR 33278 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/33278>`_

- `PR 33369 fix for 2.5
  <https://github.com/zephyrproject-rtos/zephyr/pull/33369>`_

:cve:`2021-3433`
----------------

蓝牙:CONNECT_IND中的无效通道映射导致死锁 (BT: Invalid channel map in CONNECT_IND results to Deadlock)

此问题已在v2.6.0的main分支中修�?(This has been fixed in main for v2.6.0)

- `Zephyr project bug tracker GHSA-3c2f-w4v6-qxrp
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-3c2f-w4v6-qxrp>`_

- `PR 33278 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/33278>`_

- `PR 33369 fix for 2.5
  <https://github.com/zephyrproject-rtos/zephyr/pull/33369>`_

:cve:`2021-3434` L2CAP:le_ecred_conn_req()中的基于栈的缓冲区溢�?(L2CAP: Stack based buffer overflow in le_ecred_conn_req())
-----------------------------------------------------------------------------------------------------------------------------

此问题已在v2.6.0的main分支中修�?(This has been fixed in main for v2.6.0)

- `Zephyr project bug tracker GHSA-8w87-6rfp-cfrm
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-8w87-6rfp-cfrm>`_

- `PR 33305 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/33305>`_

- `PR 33419 fix for 2.5
  <https://github.com/zephyrproject-rtos/zephyr/pull/33419>`_

- `PR 33418 fix for 1.14.2
  <https://github.com/zephyrproject-rtos/zephyr/pull/33418>`_

:cve:`2021-3435` L2CAP:le_ecred_conn_req()中的信息泄露 (L2CAP: Information leakage in le_ecred_conn_req())
-----------------------------------------------------------------------------------------------------------------------

此问题已在v2.6.0的main分支中修�?(This has been fixed in main for v2.6.0)

- `Zephyr project bug tracker GHSA-xhg3-gvj6-4rqh
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-xhg3-gvj6-4rqh>`_

- `PR 33305 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/33305>`_

- `PR 33419 fix for 2.5
  <https://github.com/zephyrproject-rtos/zephyr/pull/33419>`_

- `PR 33418 fix for 1.14.2
  <https://github.com/zephyrproject-rtos/zephyr/pull/33418>`_

:cve:`2021-3436`
----------------

Bluetooth: Possible to overwrite an existing bond during keys
distribution phase when the identity address of the bond is known

During the distribution of the identity address information we don’t
check for an existing bond with the same identity address.This means
that a duplicate entry will be created in RAM while the newest entry
will overwrite the existing one in persistent storage.

����������v2.6.0��main��֧���޸� (This has been fixed in main for v2.6.0)

- `Zephyr project bug tracker GHSA-j76f-35mc-4h63
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-j76f-35mc-4h63>`_

- `PR 33266 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/33266>`_

- `PR 33432 fix for 2.5
  <https://github.com/zephyrproject-rtos/zephyr/pull/33432>`_

- `PR 33433 fix for 2.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/33433>`_

- `PR 33718 fix for 1.14.2
  <https://github.com/zephyrproject-rtos/zephyr/pull/33718>`_

:cve:`2021-3454` 截断的L2CAP K帧导致断言失败 (Truncated L2CAP K-frame causes assertion failure)
---------------------------------------------------------------------------------------------------------------------

例如,发送SDU长度字段被截断为仅一个字节的L2CAP K�?会在Zephyr的早期版本中导致断言失败。这已在主分支中通过提交0ba9437修复,但尚未回溯到旧版本分�?(For example, sending L2CAP K-frame where SDU length field is truncated to only one byte, causes assertion failure in previous releases of Zephyr. This has been fixed in master by commit 0ba9437 but has not yet been backported to older release branches)�?

此问题已在v2.6.0的main分支中修�?(This has been fixed in main for v2.6.0)

- `Zephyr project bug tracker GHSA-fx88-6c29-vrp3
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-fx88-6c29-vrp3>`_

- `PR 32588 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/32588>`_

- `PR 33513 fix for 2.5
  <https://github.com/zephyrproject-rtos/zephyr/pull/33513>`_

- `PR 33514 fix for 2.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/33514>`_

:cve:`2021-3455` 无效ATT请求后立即断开L2CAP通道导致冻结 (Disconnecting L2CAP channel right after invalid ATT request leads freeze)
------------------------------------------------------------------------------------------------------------------------------------------------

当中央设备连接到外围设备并为增强型ATT创建L2CAP连接�?发送一些无效的ATT请求并立即断开连接会导致冻�?(When Central device connects to peripheral and creates L2CAP connection for Enhanced ATT, sending some invalid ATT request and disconnecting immediately causes freeze)�?

此问题已在v2.6.0的main分支中修�?(This has been fixed in main for v2.6.0)

- `Zephyr project bug tracker GHSA-7g38-3x9v-v7vp
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-7g38-3x9v-v7vp>`_

- `PR 35597 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/35597>`_

- `PR 36104 fix for 2.5
  <https://github.com/zephyrproject-rtos/zephyr/pull/36104>`_

- `PR 36105 fix for 2.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/36105>`_

:cve:`2021-3510` Zephyr JSON解码器错误地解码数组的数�?(Zephyr JSON decoder incorrectly decodes array of array)
-------------------------------------------------------------------------------------------------------------------------------

当使用JSON_OBJ_DESCR_ARRAY_ARRAY�?子数组具有令牌类型JSON_TOK_LIST_START,但随后分配给联合的对象部分。arr_parse然后获取数组对象的偏移量(与列表无�?,将其视为相对于父对象,并在其中存储子数组的长度 (When using JSON_OBJ_DESCR_ARRAY_ARRAY, the subarray is has the token type JSON_TOK_LIST_START, but then assigns to the object part of the union. arr_parse then takes the offset of the array-object (which has nothing todo with the list) treats it as relative to the parent object, and stores the length of the subarray in there)�?

此问题已在v2.7.0的main分支中修�?(This has been fixed in main for v2.7.0)

- `Zephyr project bug tracker GHSA-289f-7mw3-2qf4
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-289f-7mw3-2qf4>`_

- `PR 36340 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/36340>`_

- `PR 37816 fix for 2.6
  <https://github.com/zephyrproject-rtos/zephyr/pull/37816>`_

:cve:`2021-3581` HCI数据未正确检查导致蓝牙栈内存溢出 (HCI data not properly checked leads to memory overflow in the Bluetooth stack)
---------------------------------------------------------------------------------------------------------------------------------------

在通过HCI命令设置SCAN_RSP的过程中,Zephyr蓝牙协议栈未有效检查传入HCI数据的长度。导致内存溢�?然后覆盖内存中的数据,甚至可能导致任意代码执行 (In the process of setting SCAN_RSP through the HCI command, the Zephyr Bluetooth protocol stack did not effectively check the length of the incoming HCI data. Causes memory overflow, and then the data in the memory is overwritten, and may even cause arbitrary code execution)�?

此问题已在v2.6.0的main分支中修�?(This has been fixed in main for v2.6.0)

- `Zephyr project bug tracker GHSA-8q65-5gqf-fmw5
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-8q65-5gqf-fmw5>`_

- `PR 35935 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/35935>`_

- `PR 35984 fix for 2.5
  <https://github.com/zephyrproject-rtos/zephyr/pull/35984>`_

- `PR 35985 fix for 2.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/35985>`_

- `PR 35985 fix for 1.14
  <https://github.com/zephyrproject-rtos/zephyr/pull/35985>`_

:cve:`2021-3625` Zephyr USB DFU DNLOAD缓冲区溢�?(Buffer overflow in Zephyr USB DFU DNLOAD)
----------------------------------------------------------------------------------------------------------------------

此问题已在v2.6.0的main分支中修�?(This has been fixed in main for v2.6.0)

- `Zephyr project bug tracker GHSA-c3gr-hgvr-f363
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-c3gr-hgvr-f363>`_

- `PR 36694 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/36694>`_

:cve:`2021-3835`
----------------

Zephyr USB设备类缓冲区溢出 (Buffer overflow in Zephyr USB device class)

此问题已在v3.0.0的main分支中修�?(This has been fixed in main for v3.0.0)

- `Zephyr project bug tracker GHSA-fm6v-8625-99jf
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-fm6v-8625-99jf>`_

- `PR 42093 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/42093>`_

- `PR 42167 fix for 2.7
  <https://github.com/zephyrproject-rtos/zephyr/pull/42167>`_

:cve:`2021-3861` RNDIS USB设备类缓冲区溢出 (Buffer overflow in the RNDIS USB device class)
------------------------------------------------------------------------------------------------------

此问题已在v3.0.0的main分支中修�?(This has been fixed in main for v3.0.0)

- `Zephyr project bug tracker GHSA-hvfp-w4h8-gxvj
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-hvfp-w4h8-gxvj>`_

- `PR 39725 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/39725>`_

:cve:`2021-3966` USB蓝牙设备ACL读取回调缓冲区溢�?(Usb bluetooth device ACL read cb buffer overflow)
------------------------------------------------------------------------------------------------------------------

此问题已在v3.0.0的main分支中修�?(This has been fixed in main for v3.0.0)

- `Zephyr project bug tracker GHSA-hfxq-3w6x-fv2m
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-hfxq-3w6x-fv2m>`_

- `PR 42093 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/42093>`_

- `PR 42167 fix for v2.7.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/42167>`_

CVE-2022 (2022年度CVE)
========

:cve:`2022-0553` 可能检索未加密的固件镜�?(Possible to retrieve unencrypted firmware image)
-----------------------------------------------------------------------------------------------

此问题已在v3.0.0的main分支中修�?(This has been fixed in main for v3.0.0)

- `Zephyr project bug tracker GHSA-wrj2-9vj9-rrcp
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-wrj2-9vj9-rrcp>`_

- `PR 42424 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/42424>`_

:cve:`2022-1041` 在配网期间可触发蓝牙Mesh核心栈越界写入漏�?(Out-of-bound write vulnerability in the Bluetooth Mesh core stack can be triggered during provisioning)
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

此问题已在v3.1.0的main分支中修�?(This has been fixed in main for v3.1.0)

- `Zephyr project bug tracker GHSA-p449-9hv9-pj38
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-p449-9hv9-pj38>`_

- `PR 45136 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/45136>`_

- `PR 45188 fix for v3.0.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/45188>`_

- `PR 45187 fix for v2.7.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/45187>`_

:cve:`2022-1042` 在配网期间可触发蓝牙Mesh核心栈越界写入漏�?(Out-of-bound write vulnerability in the Bluetooth Mesh core stack can be triggered during provisioning)
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

此问题已在v3.1.0的main分支中修�?(This has been fixed in main for v3.1.0)

- `Zephyr project bug tracker GHSA-j7v7-w73r-mm5x
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-j7v7-w73r-mm5x>`_

- `PR 45066 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/45066>`_

- `PR 45135 fix for v3.0.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/45135>`_

- `PR 45134 fix for v2.7.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/45134>`_

:cve:`2022-1841` tcp_flags中的越界写入 (Out-of-Bound Write in tcp_flags)
--------------------------------------------------------------------------------------------------

此问题已在v3.1.0的main分支中修�?(This has been fixed in main for v3.1.0)

- `Zephyr project bug tracker GHSA-5c3j-p8cr-2pgh
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-5c3j-p8cr-2pgh>`_

- `PR 45796 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/45796>`_

:cve:`2022-2741` CAN:可由精心构造的CAN帧触发拒绝服�?(can: denial-of-service can be triggered by a crafted CAN frame)
-------------------------------------------------------------------------------------------------------------------------

此问题已在v3.2.0的main分支中修�?(This has been fixed in main for v3.2.0)

- `Zephyr project bug tracker GHSA-hx5v-j59q-c3j8
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-hx5v-j59q-c3j8>`_

- `PR 47903 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/47903>`_

- `PR 47957 fix for v3.1.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/47957>`_

- `PR 47958 fix for v3.0.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/47958>`_

- `PR 47959 fix for v2.7.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/47959>`_

:cve:`2022-2993` 蓝牙主机:错误的密钥验证检�?(bt: host: Wrong key validation check)
------------------------------------------------------------------------------------------------------

此问题已在v3.2.0的main分支中修�?(This has been fixed in main for v3.2.0)

- `Zephyr project bug tracker GHSA-3286-jgjx-8cvr
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-3286-jgjx-8cvr>`_

- `PR 48733 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/48733>`_

:cve:`2022-3806` 拒绝服务:le_read_buffer_size_complete()中的无效初始�?(DoS: Invalid Initialization in le_read_buffer_size_complete())
-----------------------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-w525-fm68-ppq3
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-w525-fm68-ppq3>`_

CVE-2023 (2023年度CVE)
========

:cve:`2023-0396` 蓝牙HCI中的缓冲区过度读�?(Buffer Overreads in Bluetooth HCI)
------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-8rpp-6vxq-pqg3
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-8rpp-6vxq-pqg3>`_

:cve:`2023-0397` 拒绝服务:le_read_buffer_size_complete()中的无效初始�?(DoS: Invalid Initialization in le_read_buffer_size_complete())
-----------------------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-wc2h-h868-q7hj
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-wc2h-h868-q7hj>`_

此问题已在v3.3.0的main分支中修�?(This has been fixed in main for v3.3.0)

- `PR 54905 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/54905>`_

- `PR 47957 fix for v3.2.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/55024>`_

- `PR 47958 fix for v3.1.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/55023>`_

- `PR 47959 fix for v2.7.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/55022>`_

:cve:`2023-0779` 网络Shell:输入验证不当 (net: shell: Improper input validation)
-----------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-9xj8-6989-r549
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-9xj8-6989-r549>`_

此问题已在v3.3.0的main分支中修�?(This has been fixed in main for v3.3.0)

- `PR 54371 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/54371>`_

- `PR 54380 fix for v3.2.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/54380>`_

- `PR 54381 fix for v2.7.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/54381>`_

:cve:`2023-1901` HCI send_sync悬空信号量引用重�?(HCI send_sync Dangling Semaphore Reference Re-use)
-------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-xvvm-8mcm-9cq3
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-xvvm-8mcm-9cq3>`_

此问题已在v3.4.0的main分支中修�?(This has been fixed in main for v3.4.0)

- `PR 56709 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/56709>`_

:cve:`2023-1902` HCI连接创建悬空状态引用重�?(HCI Connection Creation Dangling State Reference Re-use)
---------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-fx9g-8fr2-q899
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-fx9g-8fr2-q899>`_

此问题已在v3.4.0的main分支中修�?(This has been fixed in main for v3.4.0)

- `PR 56709 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/56709>`_

:cve:`2023-3725` Zephyr CANbus子系统中的潜在缓冲区溢出漏洞 (Potential buffer overflow vulnerability in the Zephyr CANbus subsystem)
--------------------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-2g3m-p6c7-8rr3
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-2g3m-p6c7-8rr3>`_

此问题已在v3.5.0的main分支中修�?(This has been fixed in main for v3.5.0)

- `PR 61502 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/61502>`_

- `PR 61518 fix for 3.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/61518>`_

- `PR 61517 fix for 3.3
  <https://github.com/zephyrproject-rtos/zephyr/pull/61517>`_

- `PR 61516 fix for 2.7
  <https://github.com/zephyrproject-rtos/zephyr/pull/61516>`_

:cve:`2023-4257` Zephyr WiFi Shell模块中未检查的用户输入长度可导致缓冲区溢出 (Unchecked user input length in the Zephyr WiFi shell module can cause buffer overflows)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-853q-q69w-gf5j
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-853q-q69w-gf5j>`_

此问题已在v3.5.0的main分支中修�?(This has been fixed in main for v3.5.0)

- `PR 605377 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/605377>`_

- `PR 61383 fix for 3.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/61383>`_

:cve:`2023-4258` 蓝牙Mesh:受配方实施配网协议的漏洞 (bt: mesh: vulnerability in provisioning protocol implementation on provisionee side)
-----------------------------------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-m34c-cp63-rwh7
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-m34c-cp63-rwh7>`_

此问题已在v3.5.0的main分支中修�?(This has been fixed in main for v3.5.0)

- `PR 59467 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/59467>`_

- `PR 60078 fix for 3.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/60078>`_

- `PR 60079 fix for 3.3
  <https://github.com/zephyrproject-rtos/zephyr/pull/60079>`_

:cve:`2023-4259` Zephyr eS-WiFi驱动中的缓冲区溢出漏�?(Buffer overflow vulnerabilities in the Zephyr eS-WiFi driver)
----------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-gghm-c696-f4j4
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-gghm-c696-f4j4>`_

此问题已在v3.5.0的main分支中修�?(This has been fixed in main for v3.5.0)

- `PR 63074 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/63074>`_

- `PR 63750 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/63750>`_

:cve:`2023-4260` Zephyr文件系统子系统中的差一缓冲区溢出漏�?(Off-by-one buffer overflow vulnerability in the Zephyr FS subsystem)
----------------------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-gj27-862r-55wh
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-gj27-862r-55wh>`_

����������v3.5.0��main��֧���޸� (This has been fixed in main for v3.5.0)

- `PR 63079 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/63079>`_

:cve:`2023-4262`
----------------

- 经进一步分�?该问题已确定为误�?(This issue has been determined to be a false positive after further analysis)�?

:cve:`2023-4263` Zephyr IEEE 802.15.4 nRF 15.4驱动中的潜在缓冲区溢出漏�?(Potential buffer overflow vulnerability in the Zephyr IEEE 802.15.4 nRF 15.4 driver)
---------------------------------------------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-rf6q-rhhp-pqhf
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-rf6q-rhhp-pqhf>`_

����������v3.5.0��main��֧���޸� (This has been fixed in main for v3.5.0)

- `PR 60528 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/60528>`_

- `PR 61384 fix for 3.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/61384>`_

- `PR 61216 fix for 2.7
  <https://github.com/zephyrproject-rtos/zephyr/pull/61216>`_

:cve:`2023-4264` Zephyr蓝牙子系统中的潜在缓冲区溢出漏洞 (Potential buffer overflow vulnerabilities in the Zephyr Bluetooth subsystem)
--------------------------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-rgx6-3w4j-gf5j
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-rgx6-3w4j-gf5j>`_

����������v3.5.0��main��֧���޸� (This has been fixed in main for v3.5.0)

- `PR 58834 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/58834>`_

- `PR 60465 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/60465>`_

- `PR 61845 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/61845>`_

- `PR 61385 fix for 3.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/61385>`_

:cve:`2023-4265` Zephyr USB代码中的两个潜在缓冲区溢出漏�?(Two potential buffer overflow vulnerabilities in Zephyr USB code)
--------------------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-4vgv-5r6q-r6xh
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-4vgv-5r6q-r6xh>`_

此问题已在v3.4.0的main分支中修�?(This has been fixed in main for v3.4.0)

- `PR 59157 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/59157>`_
- `PR 59018 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/59018>`_

:cve:`2023-4424`
----------------

bt: hci: DoS and possible RCE

- `Zephyr project bug tracker GHSA-j4qm-xgpf-qjw3
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-j4qm-xgpf-qjw3>`_

����������v3.5.0��main��֧���޸� (This has been fixed in main for v3.5.0)

- `PR 61651 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/61651>`_

- `PR 61696 fix for 3.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/61696>`_

- `PR 61695 fix for 3.3
  <https://github.com/zephyrproject-rtos/zephyr/pull/61695>`_

- `PR 61694 fix for 2.7
  <https://github.com/zephyrproject-rtos/zephyr/pull/61694>`_


:cve:`2023-5055` L2CAP:le_ecred_reconf_req()中可能的基于栈的缓冲区溢�?(L2CAP: Possible Stack based buffer overflow in le_ecred_reconf_req())
----------------------------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-wr8r-7f8x-24jj
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-wr8r-7f8x-24jj>`_

此问题已在v3.5.0的main分支中修�?(This has been fixed in main for v3.5.0)

- `PR 62381 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/62381>`_


:cve:`2023-5139` Zephyr STM32加密驱动中的潜在缓冲区溢出漏�?(Potential buffer overflow vulnerability in the Zephyr STM32 Crypto driver)
-------------------------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-rhrc-pcxp-4453
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-rhrc-pcxp-4453>`_

����������v3.5.0��main��֧���޸� (This has been fixed in main for v3.5.0)

- `PR 61839 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/61839>`_

:cve:`2023-5184` Zephyr IPM驱动中潜在的有符号到无符号转换错误和缓冲区溢出漏�?(Potential signed to unsigned conversion errors and buffer overflow vulnerabilities in the Zephyr IPM driver)
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-8x3p-q3r5-xh9g
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-8x3p-q3r5-xh9g>`_

����������v3.5.0��main��֧���޸� (This has been fixed in main for v3.5.0)

- `PR 63069 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/63069>`_

:cve:`2023-5563` SJA1000 CAN控制器驱动后端自动总线关闭恢复导致IRQ上下文中调用k_sleep()引发致命异常
------------------------------------------------------------------------------------------------------------------------------

SJA1000 CAN控制器驱动后端在使用CONFIG_CAN_AUTO_BUS_OFF_RECOVERY=y构建时会自动尝试从总线关闭事件中恢复。这会导致在IRQ上下文中调用k_sleep(),引发致命异常 (The SJA1000 CAN controller driver backend automatically attempts to recover from a bus-off event when built with CONFIG_CAN_AUTO_BUS_OFF_RECOVERY=y. This results in calling k_sleep() in IRQ context, causing a fatal exception)�?

- `Zephyr project bug tracker GHSA-98mc-rj7w-7rpv
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-98mc-rj7w-7rpv>`_

����������v3.5.0��main��֧���޸� (This has been fixed in main for v3.5.0)

- `PR 63713 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/63713>`_

- `PR 63718 fix for 3.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/63718>`_

- `PR 63717 fix for 3.3
  <https://github.com/zephyrproject-rtos/zephyr/pull/63717>`_

:cve:`2023-5753` 禁用断言时Zephyr蓝牙子系统源代码中的潜在缓冲区溢出漏�?(Potential buffer overflow vulnerabilities in the Zephyr Bluetooth subsystem source code when asserts are disabled)
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-hmpr-px56-rvww
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-hmpr-px56-rvww>`_

����������v3.5.0��main��֧���޸� (This has been fixed in main for v3.5.0)

- `PR 63605 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/63605>`_


:cve:`2023-5779` 多个CAN驱动中remove_rx_filter的越界问�?(Out of bounds issue in remove_rx_filter in multiple can drivers)
----------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-7cmj-963q-jj47
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-7cmj-963q-jj47>`_

此问题已在v3.6.0的main分支中修�?(This has been fixed in main for v3.6.0)

- `PR 64399 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/64399>`_

- `PR 64416 fix for 3.5
  <https://github.com/zephyrproject-rtos/zephyr/pull/64416>`_

- `PR 64415 fix for 3.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/64415>`_

- `PR 64427 fix for 3.3
  <https://github.com/zephyrproject-rtos/zephyr/pull/64427>`_

- `PR 64431 fix for 2.7
  <https://github.com/zephyrproject-rtos/zephyr/pull/64431>`_

:cve:`2023-6249` esp32_ipm_send中的有符号到无符号转换问题可能导致缓冲区溢出 (Signed to unsigned conversion problem in esp32_ipm_send may lead to buffer overflow)
----------------------------------------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-32f5-3p9h-2rqc
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-32f5-3p9h-2rqc>`_

����������v3.6.0��main��֧���޸� (This has been fixed in main for v3.6.0)

- `PR 65546 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/65546>`_

:cve:`2023-6749` settings Shell中未检查来自用户输入的数据导致潜在缓冲区溢�?(Potential buffer overflow due unchecked data coming from user input in settings shell)
------------------------------------------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-757h-rw37-66hw
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-757h-rw37-66hw>`_

����������v3.6.0��main��֧���޸� (This has been fixed in main for v3.6.0)

- `PR 66451 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/66451>`_

- `PR 66584 fix for 3.5
  <https://github.com/zephyrproject-rtos/zephyr/pull/66584>`_

:cve:`2023-6881` Zephyr fuse文件系统中的潜在缓冲区溢出漏�?(Potential buffer overflow vulnerability in Zephyr fuse file system)
------------------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-mh67-4h3q-p437
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-mh67-4h3q-p437>`_

����������v3.6.0��main��֧���޸� (This has been fixed in main for v3.6.0)

- `PR 66592 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/66592>`_

:cve:`2023-7060` Zephyr OS IP数据包处理中缺少安全控制 (Missing Security Control in Zephyr OS IP Packet Handling)
---------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-fjc8-223c-qgqr
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-fjc8-223c-qgqr>`_

����������v3.6.0��main��֧���޸� (This has been fixed in main for v3.6.0)

- `PR 66645 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/66645>`_

- `PR 66739 fix for 3.5
  <https://github.com/zephyrproject-rtos/zephyr/pull/66739>`_

- `PR 66738 fix for 3.4
  <https://github.com/zephyrproject-rtos/zephyr/pull/66738>`_

- `PR 66887 fix for 2.7
  <https://github.com/zephyrproject-rtos/zephyr/pull/66887>`_

CVE-2024 (2024年度CVE)
========

:cve:`2024-1638` 蓝牙特性LESC安全要求未在没有额外标志的情况下强制执行 (Bluetooth characteristic LESC security requirement not enforced without additional flags)
---------------------------------------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-p6f3-f63q-5mc2
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-p6f3-f63q-5mc2>`_

此问题已在v3.6.0的main分支中修�?(This has been fixed in main for v3.6.0)

- `PR 69170 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/69170>`_

:cve:`2024-3077` 蓝牙:gatt_find_info_rsp中的整数下溢,恶意蓝牙LE设备可通过发送格式错误的gatt数据包导致受害设备崩�?(Bluetooth: Integer underflow in gatt_find_info_rsp. A malicious Bluetooth LE device can crash Bluetooth LE victim device by sending malformed gatt packet)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-gmfv-4vfh-2mh8
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-gmfv-4vfh-2mh8>`_

����������v3.7.0��main��֧���޸� (This has been fixed in main for v3.7.0)

- `PR 69396 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/69396>`_

:cve:`2024-3332`
----------------

Bluetooth: DoS caused by null pointer dereference.

A malicious Bluetooth LE device can send a specific order of packet
sequence to cause a DoS attack on the victim Bluetooth LE device.

- `Zephyr project bug tracker GHSA-jmr9-xw2v-5vf4
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-jmr9-xw2v-5vf4>`_

此问题已在v3.7.0的main分支中修�?(This has been fixed in main for v3.7.0)

- `PR 71030 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/71030>`_


:cve:`2024-4785` 蓝牙:LL_CONNECTION_UPDATE_IND数据包中缺少检查导致除零错�?(Bluetooth: Missing Check in LL_CONNECTION_UPDATE_IND Packet Leads to Division by Zero)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-xcr5-5g98-mchp
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-xcr5-5g98-mchp>`_

����������v3.7.0��main��֧���޸� (This has been fixed in main for v3.7.0)

- `PR 72608 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/72608>`_

:cve:`2024-5754` 蓝牙:加密过程主机漏洞 (BT: Encryption procedure host vulnerability)
-------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-gvv5-66hw-5qrc
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-gvv5-66hw-5qrc>`_

����������v3.7.0��main��֧���޸� (This has been fixed in main for v3.7.0)

- `PR 7395 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/7395>`_

- `PR 74124 fix for 3.6
  <https://github.com/zephyrproject-rtos/zephyr/pull/74124>`_

- `PR 74123 fix for 3.5
  <https://github.com/zephyrproject-rtos/zephyr/pull/74123>`_

- `PR 74122 fix for 2.7
  <https://github.com/zephyrproject-rtos/zephyr/pull/74122>`_

:cve:`2024-5931` 蓝牙:bap_broadcast_assistant中未检查的用户输入 (BT: Unchecked user input in bap_broadcast_assistant)
-----------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-r8h3-64gp-wv7f
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-r8h3-64gp-wv7f>`_

����������v3.7.0��main��֧���޸� (This has been fixed in main for v3.7.0)

- `PR 74062 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/74062>`_

- `PR 77966 fix for 3.6
  <https://github.com/zephyrproject-rtos/zephyr/pull/77966>`_


:cve:`2024-6135` 蓝牙经典:多处缺少缓冲区长度检�?(BT:Classic: Multiple missing buf length checks)
------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-2mp4-4g6f-cqcx
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-2mp4-4g6f-cqcx>`_

����������v3.7.0��main��֧���޸� (This has been fixed in main for v3.7.0)

- `PR 74283 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/74283>`_

- `PR 77964 fix for 3.6
  <https://github.com/zephyrproject-rtos/zephyr/pull/77964>`_

:cve:`2024-6137` 蓝牙经典:get_att_search_list中的SDP越界访问 (BT: Classic: SDP OOB access in get_att_search_list)
----------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-pm38-7g85-cf4f
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-pm38-7g85-cf4f>`_

����������v3.7.0��main��֧���޸� (This has been fixed in main for v3.7.0)

- `PR 75575 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/75575>`_

:cve:`2024-6258` 蓝牙:rfcomm_handle_data中net_buf缺少长度检�?(BT: Missing length checks of net_buf in rfcomm_handle_data)
------------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-7833-fcpm-3ggm
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-7833-fcpm-3ggm>`_

����������v3.7.0��main��֧���޸� (This has been fixed in main for v3.7.0)

- `PR 74640 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/74640>`_

:cve:`2024-6259` 蓝牙HCI:adv_ext_report中的不当丢弃 (BT: HCI: adv_ext_report Improper discarding in adv_ext_report)
----------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-p5j7-v26w-wmcp
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-p5j7-v26w-wmcp>`_

����������v3.7.0��main��֧���޸� (This has been fixed in main for v3.7.0)

- `PR 74639 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/74639>`_

- `PR 77960 fix for 3.6
  <https://github.com/zephyrproject-rtos/zephyr/pull/77960>`_

:cve:`2024-6442` 蓝牙ASCS:响应缓冲区尾部空间未检�?(Bluetooth: ASCS Unchecked tailroom of the response buffer)
--------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-m22j-ccg7-4v4h
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-m22j-ccg7-4v4h>`_

����������v3.7.0��main��֧���޸� (This has been fixed in main for v3.7.0)

- `PR 74976 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/74976>`_

- `PR 77958 fix for 3.6
  <https://github.com/zephyrproject-rtos/zephyr/pull/77958>`_

:cve:`2024-6443` Zephyr:utf8_trunc中的越界读取 (zephyr: out-of-bound read in utf8_trunc)
-----------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-gg46-3rh2-v765
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-gg46-3rh2-v765>`_

����������v3.7.0��main��֧���޸� (This has been fixed in main for v3.7.0)

- `PR 74949 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/74949>`_

- `PR 78286 fix for 3.6
  <https://github.com/zephyrproject-rtos/zephyr/pull/78286>`_

:cve:`2024-6444` 蓝牙OTS:缺少缓冲区长度检�?(Bluetooth: ots: missing buffer length check)
-----------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-qj4r-chj6-h7qp
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-qj4r-chj6-h7qp>`_

����������v3.7.0��main��֧���޸� (This has been fixed in main for v3.7.0)

- `PR 74944 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/74944>`_

- `PR 77954 fix for 3.6
  <https://github.com/zephyrproject-rtos/zephyr/pull/77954>`_

:cve:`2024-8798` 蓝牙经典AVDTP:缺少缓冲区长度检�?(Bluetooth: classic: avdtp: missing buffer length check)
---------------------------------------------------------------------------------------------------------------------

- `Zephyr project bug tracker GHSA-r7pm-f93f-f7fp
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-r7pm-f93f-f7fp>`_

此问题已在v4.0.0的main分支中修�?(This has been fixed in main for v4.0.0)

- `PR 77969 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/77969>`_

- `PR 78409 fix for 3.7
  <https://github.com/zephyrproject-rtos/zephyr/pull/78409>`_

:cve:`2024-10395` 网络库HTTP服务�?缓冲区欠读取 (net: lib: http_server: Buffer Under-read)
---------------------------------------------------------------------------------------------------------

http_server_get_content_type_from_extension中对用户输入长度的验证不当可能导致分段错误或崩溃,原因是读取了缓冲区边界之外的内存 (No proper validation of the length of user input in http_server_get_content_type_from_extension could cause a segmentation fault or crash by causing memory to be read outside of the bounds of the buffer)�?

- `Zephyr project bug tracker GHSA-hfww-j92m-x8fv
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-hfww-j92m-x8fv>`_

此问题已在v4.0.0的main分支中修�?(This has been fixed in main for v4.0.0)

- `PR 80396 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/80396>`_

:cve:`2024-11263`
-----------------

arch: riscv: userspace: potential security risk when CONFIG_RISCV_GP=y

A rogue thread can corrupt the gp reg and cause the entire system to hard fault at best, at worst,
it can potentially trick the system to access another set of random global symbols.

- `Zephyr project bug tracker GHSA-jjf3-7x72-pqm9
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-jjf3-7x72-pqm9>`_

����������v4.0.0��main��֧���޸� (This has been fixed in main for v4.0.0)

- `PR 81155 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/81155>`_

- `PR 81370 fix for 3.7
  <https://github.com/zephyrproject-rtos/zephyr/pull/81370>`_

CVE-2025
========

:cve:`2025-1673`
----------------

Out of bounds read when calling crc16_ansi and strlen in dns_validate_msg

:cve:`2024-11263` 网络库DNS:缓冲区欠读取 (net: lib: dns: Buffer Under-read)
------------------------------------------------------------------------------------

没有有效载荷的恶意或格式错误的DNS数据包可能导致越界读�?从而引发崩�?拒绝服务)或错误计�?(A malicious or malformed DNS packet without a payload can cause an out-of-bounds read, resulting in a crash (denial of service) or an incorrect computation)�?

- `Zephyr project bug tracker GHSA-jjhx-rrh4-j8mx
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-jjhx-rrh4-j8mx>`_

此问题已在v4.1.0的main分支中修�?(This has been fixed in main for v4.1.0)

- `PR 82072 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/82072>`_

- `PR 82289 fix for 4.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/82289>`_

- `PR 82288 fix for 3.7
  <https://github.com/zephyrproject-rtos/zephyr/pull/82288>`_

:cve:`2025-1674` 解包DNS应答时的越界读取 (Out of bounds read when unpacking DNS answers)
----------------------------------------------------------------------------------------------------------

缺少输入验证导致恶意或格式错误的数据包引起越界读�?(A lack of input validation allows for out of bounds reads caused by malicious or malformed packets)�?

- `Zephyr project bug tracker GHSA-x975-8pgf-qh66
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-x975-8pgf-qh66>`_

此问题已在v4.1.0的main分支中修�?(This has been fixed in main for v4.1.0)

- `PR 82072 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/82072>`_

- `PR 82289 fix for 4.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/82289>`_

- `PR 82288 fix for 3.7
  <https://github.com/zephyrproject-rtos/zephyr/pull/82288>`_

:cve:`2025-1675` dns_copy_qname中的越界读取 (Out of bounds read in dns_copy_qname)
------------------------------------------------------------------------------------------------------

dns_pack.c中的函数dns_copy_qname使用不可信字段执行memcpy操作,并且不检查源缓冲区是否足够大以容纳复制的数据 (The function dns_copy_qname in dns_pack.c performs performs a memcpy operation with an untrusted field and does not check if the source buffer is large enough to contain the copied data)�?

- `Zephyr project bug tracker GHSA-2m84-5hfw-m8v4
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-2m84-5hfw-m8v4>`_

此问题已在v4.1.0的main分支中修�?(This has been fixed in main for v4.1.0)

- `PR 82072 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/82072>`_

- `PR 82289 fix for 4.0
  <https://github.com/zephyrproject-rtos/zephyr/pull/82289>`_

- `PR 82288 fix for 3.7
  <https://github.com/zephyrproject-rtos/zephyr/pull/82288>`_

:cve:`2025-2962` dns_copy_qname中的无限循环 (Infinite loop in dns_copy_qname)
----------------------------------------------------------------------------------------------

DNS实现中的拒绝服务问题可能导致无限循环 (A denial-of-service issue in the dns implementation could cause an infinite loop)�?

- `Zephyr project bug tracker GHSA-2qp5-c2vq-g2ww
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-2qp5-c2vq-g2ww>`_

此问题已在v4.2.0的main分支中修�?(This has been fixed in main for v4.2.0)

- `PR 87753 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/87753>`_

- `PR 87925 fix for 4.1
  <https://github.com/zephyrproject-rtos/zephyr/pull/87925>`_

- `PR 87949 fix for 3.7
  <https://github.com/zephyrproject-rtos/zephyr/pull/87949>`_

:cve:`2025-7403` 蓝牙:bt_conn_tx_processor不安全处�?(Bluetooth: bt_conn_tx_processor unsafe handling)
------------------------------------------------------------------------------------------------------------------

bt_conn_tx_processor中的不安全处理导致释放后使用,从而引发写零之前的操作。写入的4字节由攻击者控�?可实现精确的内存损坏 (Unsafe handling in bt_conn_tx_processor causes a use-after-free, resulting in a write-before-zero. The written 4 bytes are attacker-controlled, enabling precise memory corruption)�?

- `Zephyr project bug tracker GHSA-9r46-cqqw-6j2j
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-9r46-cqqw-6j2j>`_

此问题已在v4.2.0的main分支中修�?(This has been fixed in main for v4.2.0)

- `PR 90975 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/90975>`_

:cve:`2025-10456` 蓝牙:半任意能力使BLE目标发送断开连接请求 (Bluetooth: Semi-Arbitrary ability to make the BLE Target send disconnection requests)
----------------------------------------------------------------------------------------------------------------------------------------------------------------

在蓝牙低功�?BLE)固定通道(如SMP或ATT)的处理中发现了一个漏洞。具体来�?攻击者可以利用一个缺陷导致BLE目标(即受攻击的设�?尝试断开固定通道,这在蓝牙规范中是不允许的。这会导致未定义的行�?包括潜在的断言失败、崩溃或内存损坏 (A vulnerability was identified in the handling of Bluetooth Low Energy (BLE) fixed channels (such as SMP or ATT). Specifically, an attacker could exploit a flaw that causes the BLE target (i.e., the device under attack) to attempt to disconnect a fixed channel, which is not allowed per the Bluetooth specification. This leads to undefined behavior, including potential assertion failures, crashes, or memory corruption)�?

- `Zephyr project bug tracker GHSA-hcc8-3qr7-c9m8
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-hcc8-3qr7-c9m8>`_

此问题已在v4.2.0的main分支中修�?(This has been fixed in main for v4.2.0)

- `PR 93576 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/93576>`_

:cve:`2025-10457` 蓝牙:le_conn_rsp的上下文外处�?(Bluetooth: Out-Of-Context le_conn_rsp handling)
-----------------------------------------------------------------------------------------------------------------

负责处理BLE连接响应的函数不验证是否需要响�?即设备是否已发起连接请求。相�?它仅依赖标识符匹�?(The function responsible for handling BLE connection responses does not verify whether a response is expected—that is, whether the device has initiated a connection request. Instead, it relies solely on identifier matching)�?

- `Zephyr project bug tracker GHSA-xqj6-vh76-2vv8
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-xqj6-vh76-2vv8>`_

此问题已在v4.2.0的main分支中修�?(This has been fixed in main for v4.2.0)

- `PR 94080 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/94080>`_

:cve:`2025-10458` 蓝牙:le_conn_rsp未清理CID、MTU、MPS�?(Bluetooth: le_conn_rsp does not sanitize CID, MTU, MPS values)
------------------------------------------------------------------------------------------------------------------------

参数未经验证或清�?并在后续的各种内部操作中使用 (Parameters are not validated or sanitized, and are later used in various internal operations)�?

- `Zephyr project bug tracker GHSA-vmww-237q-2fwp
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-vmww-237q-2fwp>`_

此问题已在v4.2.0的main分支中修�?(This has been fixed in main for v4.2.0)

- `PR 93174 fix for main
  <https://github.com/zephyrproject-rtos/zephyr/pull/93174>`_

:cve:`2025-12035`
-----------------

�?025-12-13之前处于禁发�?(Under embargo until 2025-12-13)
