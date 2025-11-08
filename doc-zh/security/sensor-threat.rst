.. _sensor-threat:

传感器设备威胁模型 (Sensor Device Threat Model)
################################################

本文档描述了物联网传感器设备的威胁模型。明确威胁模型有助于指导开发工作,也可用于帮助确定这些工作的优先级 (This document describes a threat model for an IoT sensor device.
Spelling out a threat model helps direct development effort, and can
be used to help prioritize these efforts as well)。

该设备包含某种类型的传感器(例如温度传感器或管道中的压力传感器),该传感器将这些数据发送到运行微控制器的 SoC。该微控制器连接到云服务,并将此传感器数据中继到该服务。云服务还能够向设备发送配置数据以及软件更新镜像。通用图表如图 1 所示 (This device contains a sensor of some type (for example temperature, or a
pressure in a pipe), which sends this data to an SoC running a
microcontroller. This microcontroller connects to a cloud service, and
relays this sensor data to this service. The cloud service is also able
to send configuration data to the device, as well as software update
images. A general diagram can be seen in Figure 1):

.. figure:: media/sensor-model.svg

   图 1. 传感器总体图 (Figure 1. Sensor General Diagram)

在此传感器设备中,传感器通过 SPI 总线与 SoC 连接,而 SoC 具有用于与云服务通信的网络接口。这些接口的具体细节可能会以意想不到的方式影响威胁模型,需要考虑这方面的变体(例如,使用通过某种类型总线连接的独立网络接口 SoC) (In this sensor device, the sensor connects with the SoC via an SPI bus,
and the SoC has a network interface that it uses to communicate with the
cloud service. The particulars of these interfaces can impact the threat
model in unexpected ways, and variants on this will need to be
considered (for example, using a separate network interface SoC
connected via some type of bus))。

该模型还侧重于通过 MQTT-over-TLS 协议进行通信,因为这似乎被广泛使用 [1]_ (This model also focuses on communicating via the MQTT-over-TLS protocol,
as this seems to be in wide use [1]_)。

资产 (Assets)
==============

威胁模型要考虑的一个方面是设备操作中涉及的资产。以下列表列举了此模型中包含的资产 (One aspect of the threat model to consider are assets involved in the
operation of the device. The following list enumerates the assets
included in this model):

1. **引导加载程序 (The bootloader)**。这是包含在片上闪存中的小型代码/数据镜像,是第一个运行的代码。为了建立信任根,该镜像必须是不可变的。该模型假设 SoC 提供了一种机制来保护闪存的某个区域免受未来写入的影响,并且这将在该镜像编程到设备后在生产早期完成 [th-imboot]_。

2. **应用程序固件镜像 (The application firmware image)**。该资产包括微控制器运行的固件的其余部分。之所以进行区分,是因为该镜像的这一部分需要随着安全漏洞的发现而定期更新。此镜像的更新要求包括 (Requirements
   for updates to this image are):

   a. 镜像只能用授权镜像替换 [th-authrepl]_。

   b. 当授权替换镜像可用时,应及时执行更新 [th-timely-update]_。

   c. 镜像更新应被视为原子操作,这意味着当镜像运行时,闪存应包含完整的更新镜像或完整的旧镜像 [th-atomic-update]_。

3. **根证书列表 (Root certificate list)**。为了对云服务(服务器)进行身份验证,物联网设备必须具有允许签署服务器证书的根证书列表。对于基于云提供商的服务,该列表通常由服务提供商提供。由于根证书可能会过期并可能被撤销,因此需要定期更新此列表 [th-root-certs]_, [th-root-check]_。

4. **客户端密钥 (Client secrets)**。为了向服务验证客户端,客户端必须拥有某种密钥。这通常是私钥,通常是 RSA 密钥或 EC 私钥。在与服务器建立通信时,设备将使用此密钥作为 TLS 建立的一部分,或签署通信中使用的消息。

   该密钥通常由服务提供商或在其他地方运行的软件生成,并且必须安全地安装在设备上。策略可能规定定期替换此密钥,这将需要一种更新客户端密钥的方法。通常,服务将允许两个或三个活动密钥,以允许在使用旧密钥时进行此更新。

   这些密钥必须受到读取保护,并且应只有尽可能少的代码可以访问它们。[th-secret-storage]_

5. **当前日期/时间 (Current date/time)**。TLS 证书验证需要知道当前日期和时间,以确定当前时间是否在证书的当前有效期内。此外,基于令牌的客户端身份验证通常要求客户端签署包含令牌有效的时间窗口的消息。证书验证要求设备的日期和时间概念在一天左右的范围内准确。令牌生成通常要求时间在 5-10 分钟内准确。

   可以通过查询外部时间服务器来近似安全时间。安全 NTP 可能超出了物联网设备的能力。时间不正确的主要风险是拒绝服务(设备拒绝有效证书)和生成具有无效时间的令牌。可能会欺骗设备生成在未来某个时间有效的令牌,但攻击者还必须欺骗服务器的证书才能拦截此令牌。[th-time]_

6. **传感器数据 (Sensor data)**。从传感器本身接收并传递到服务的数据应在没有修改或篡改的情况下传递。

7. **设备配置 (Device configuration)**。需要由设备保留的各种配置数据,例如要连接的服务的主机名、时间服务器的地址、传感器数据发送到服务的频率和参数等。随着配置更改,需要定期更新此配置数据。应仅允许授权方进行更新。[th-conf]_

8. **日志 (Logs)**。为了帮助分析安全问题,设备应记录有关安全相关事件的信息。物联网设备通常存储空间有限,因此需要仔细选择这些日志。也可以将这些日志事件发送到云服务,在那里可以在资源更丰富的环境中存储它们。应记录的事件类型包括 (device shall log information about security-pertinent events. IoT
   devices generally have limited storage, and as such, these logs need
   to be carefully selected. It may also be possible to send these log
   events to the cloud service where they can be stored in a more
   resource-available environment. Types of events that should be logged
   include):

   a. **固件镜像更新 (Firmware image updates)**。系统应记录新镜像的下载以及镜像成功更新的时间。

   b. **客户端密钥更改 (Client secret changes)**。应记录更改和新的客户端密钥。

   c. **设备配置的更改 (Changes to the device configuration)**。

   [th-logs]_

通信 (Communication)
=====================

除了资产之外,威胁模型还考虑系统实体之间通信数据或资产的位置 (In addition to assets, the threat model also considers the locations
where data or assets are communicated between entities of the system)。

1. **闪存内容 (Flash contents)**。闪存设备包含多个区域。闪存的内容可以由 SoC 的 CPU 以编程方式修改 (The flash device contains several regions. The
   contents of flash can be modified programmatically by the SoC's CPU)。

   a. **引导加载程序 (The bootloader)**。如资产部分所述,引导加载程序是闪存设备的一小部分,包含最初运行的代码。该部分应在设备生命周期的早期写入,然后配置闪存设备以永久禁止修改该部分。此配置还应防止通过外部接口(例如 JTAG 或 SWD 调试器)进行修改。

      引导加载程序负责验证应用程序镜像的签名,以及在需要更新时从更新镜像更新应用程序镜像。

      引导加载程序应在安装更新镜像之前验证更新镜像的签名。

      引导加载程序应只接受版本号比当前镜像更新的更新镜像。

   b. **应用程序镜像 (The application image)**。应用程序镜像包含在设备正常操作期间执行的代码。在运行此镜像之前,引导加载程序应验证镜像的数字签名,以避免运行被篡改的镜像。闪存/系统应配置为在引导加载程序完成后,CPU 将无法写入应用程序镜像。

   c. **更新镜像 (The update image)**。这是闪存的一个区域,用于保存应用程序镜像的新版本。该镜像将在正常操作期间由应用程序下载和存储。完成后,应用程序可以触发重启,引导加载程序可以安装新镜像。

   d. **密钥存储 (Secret storage)**。闪存的一个区域将用于存储客户端密钥。该区域由应用程序镜像的子集写入和读取。应用程序应配置为保护该区域免受不需要访问它的代码的读取和写入,同时考虑在大部分应用程序代码中发现的可能漏洞。泄露密钥的内容将允许攻击者伪装此设备。

      初始密钥应在设备的配置活动期间放置在设备中,与设备的正常操作不同。以后的更新可以在通过安全通道接收到服务的通信的指导下进行。

   e. **配置存储 (Configuration storage)**。应有一个区域来存储其他配置信息。在资源受限的设备上,允许将其存储在与密钥存储相同的区域中,但是这会添加可以访问密钥存储区域的额外代码,因此需要仔细审查更多代码。

   f. **日志存储 (Log storage)**。设备可能有一个闪存区域,可以在其中写入日志事件。

2. **传感器/执行器接口 (Sensor/Actuator interface)**。在此设计中,传感器或执行器通过总线(例如 SPI)与 SoC 通信。硬件设计应使攻击拦截此总线变得困难。所需技术取决于传感器数据的敏感性和使用,范围从将传感器安装在与 MCU 相同的 PCB 上到用环氧树脂封装整个设备。

3. **与云服务的通信 (Communication with cloud service)**。设备与云服务之间的通信将通过一般互联网完成。因此,应假设攻击者可以任意拦截此通道,例如返回欺骗的 DNS 结果或尝试对与云服务的通信进行中间人攻击。

   设备应对与云服务的所有通信使用 TLS [th-all-tls]_。TLS 栈应配置为仅使用通常被认为是安全的密码套件 [2]_,包括前向保密。通信应通过以下方式保护 (The communication shall be secured by the following):

   a. **密码套件选择 (Cipher suite selection)**。设备应仅允许与通常认可的安全密码套件进行通信 [th-tls-ciphers]_。

   b. **服务器证书验证 (Server certificate verification)**。应验证服务器呈现的服务器证书 [th-root-check]_。

      i.   **命名 (Naming)**。证书应命名云服务服务器提供的主机和服务。
           `RFC6125 <https://tools.ietf.org/html/rfc6125>`__ 描述了这方面的最佳实践。允许设备要求证书比 RFC 中描述的更具限制性,前提是服务可以使用可以遵守的证书。

      ii.  **路径验证 (Path validation)**。设备应验证证书链从设备中包含的根证书到服务呈现的证书具有有效的签名路径。
           `RFC4158 <https://tools.ietf.org/html/rfc4158>`__ 对此进行了一般性描述。允许设备要求更受限制的路径,前提是使用的服务器证书遵守此限制。

      iii. **有效期 (Validity period)**。应根据设备对当前时间的最佳概念检查所有呈现的证书的有效期。

   c. **客户端认证 (Client authentication)**。客户端应使用仅该特定设备知道的密钥向服务验证自己。有几种选项,使用的技术通常由所使用的特定服务提供商规定 [th-tls-client-auth]_。

      i.  **TLS 客户端证书 (TLS client certificates)**。TLS 协议允许客户端呈现证书,并断言其对该证书描述的密钥的了解。通常,这些证书将存储在服务提供商内。这些证书可以是自签名的,也可以由 CA 签名。由于服务提供商维护有效证书列表(将它们映射到设备身份),让这些证书由 CA 签名不会增加任何额外的安全性,但可能对这些证书的管理有用。

      ii. **基于令牌的认证 (Token-based authentication)**。客户端也可以使用 MQTT CONNECT 数据包的 *password* 字段对自己进行身份验证。但是,密钥本身不得在此数据包中传输。相反,可以使用基于令牌的协议,例如
          `RFC7519 <https://tools.ietf.org/html/rfc7519>`__ 的 JSON Web
          Token (JWT)。这些令牌通常具有较短的有效期(例如 1 小时),以防止它们在被拦截时被重用。在设备验证服务器身份之前,不得发送令牌。

   d. **随机/熵源 (Random/Entropy source)**。加密通信需要生成安全的伪随机数。设备应使用现代的、公认的加密随机位生成器来生成这些随机数。它应使用在 SoC 内以硬件实现的非确定性随机位生成器(真 RBG),或由 SoC 内的熵源播种的确定性随机位生成器(伪 RBG)。有关批准的 RBG 的信息,请参阅 NIST SP 800-90A,有关测试设备熵源的信息,请参阅 NIST SP 800-90B [th-entropy]_。

4. **与时间服务的通信 (Communication with the time service)**。理想情况下,设备应包含维护安全时间的硬件。但是,正在使用的大多数 SoC 不支持此功能,因此需要咨询外部时间服务。
   `RFC4330 <https://tools.ietf.org/html/rfc4330>`__ 和引用的 RFC
   描述了简单网络时间协议,可用于从网络时间服务器查询当前时间。

5. **设备生命周期 (Device lifecycle)**。物联网设备将经历从生产到销毁和处置设备的生命周期。影响安全性的生命周期方面包括初始配置、正常操作、重新配置和销毁。

   a. **初始配置 (Initial provisioning)**。在初始配置阶段,需要编程引导加载程序、初始应用程序镜像、设备密钥和初始配置数据 [th-initial-provision]_。此外,应安装引导加载程序闪存保护。在这些信息中,只有设备密钥需要因设备而异。该密钥应得到安全维护,并在编程到设备后在设备外的所有位置销毁 [th-initial-secret]_。

   b. **正常操作 (Normal operation)**。正常操作包括本文档其余部分描述的行为。

   c. **重新配置 (Re-provisioning)**。有时需要重新配置设备,例如用于不同的应用程序。一种方法是保留相同的设备密钥,并替换配置数据以及与设备关联的云服务数据。也可以编程新的设备密钥,但如果这样做,应安全地完成,并且在编程到设备后在外部销毁新密钥 [th-reprovision]_。

   d. **销毁 (Destruction)**。为了防止设备密钥被用于伪装设备,在退役时,应使特定设备的密钥无效 [th-destruction]_。可能性包括:

      i.    设备的硬件销毁。

      ii.   安全擦除包含密钥的闪存区域 [3]_。

      iii.  从服务中删除设备身份和证书。

其他考虑 (Other Considerations)
==================================

除上述内容外,联网设备通常需要一种方法来配置它们以连接到它们所在的网络环境。有许多方法可以做到这一点,重要的是这些配置方法不会绕过上述安全要求 (In addition to the above, network connected devices generally will need
a way to configure them to connect to the network environment they are
placed in. There are numerous ways of doing this, and it is important
for these configuration methods to not circumvent the security
requirements described above)。

威胁 (Threats)
===============

.. [th-imboot] 必须使用不可变的引导加载程序启动 (Must boot with an immutable bootloader)。

.. [th-authrepl] 应用程序镜像只能用授权镜像替换 (Application image shall only be replaced with an
   authorized image)。

.. [th-timely-update]
   应及时执行应用程序更新 (Application updates shall be done in a timely manner)。

.. [th-atomic-update]
   应用程序更新应是原子的 (Application updates shall be atomic)。

.. [th-root-certs]
   TLS 必须具有可信根证书列表 (TLS must have a list of trusted root certificates)。

.. [th-root-check]
   TLS 必须验证来自服务器的根证书是否有效 (TLS must verify root certificate from server is valid)。

.. [th-secret-storage]
   必须有一种机制来安全地存储客户端密钥。应只有尽可能少的代码可以访问这些密钥 (There must be a mechanism to securely store client secrets.  The
   least amount of code necessary shall have access to these secrets)。

.. [th-time]
   系统必须对当前日期/时间有适度准确的概念 (System must have moderately accurate notion of the current
   date/time)。

.. [th-conf]
   系统必须接收并保留配置数据 (The system must receive, and keep configuration data)。

.. [th-logs]
   系统必须记录安全相关事件,并将其存储在本地或发送到服务 (The system must log security-related events, and either store them
   locally, or send to a service)。

.. [th-all-tls]
   与云服务的所有通信都应使用 TLS (All communications with the cloud service shall use TLS)。

.. [th-tls-ciphers]
   TLS 应配置为仅允许通常认可的密码套件(包括前向保密) (TLS shall be configured to allow only generally agreed cipher
   suites (including forward secrecy))。

.. [th-tls-client-auth]
   设备应使用所述方法之一向云提供商验证自己 (The device shall authenticate itself with the cloud provider using
   one of the methods described)。

.. [th-entropy]
   TLS 层应使用由 SoC 内的熵源播种的现代的、公认的加密随机位生成器 (The TLS layer shall use a modern, accepted cryptographic random-bit
   generator seeded by an entropy source within the SoC)。

.. [th-initial-provision]
   设备应在部署前加载每个设备的密钥 (The device shall have a per-device secret loaded before deployment)。

.. [th-initial-secret]
   初始密钥应得到安全维护,并在设备配置后立即在任何外部位置销毁 (The initial secret shall be securely maintained, and destroyed in
   any external location as soon as the device is provisioned)。

.. [th-reprovision]
   重新配置设备应安全地完成 (Reprovisioning a device shall be done securely)。

.. [th-destruction]
   退役时,应使设备密钥无效 (Upon decommissioning, the device secret shall be rendered
   ineffective)。

注释 (Notes)
=============

.. [1]
   参见 https://www.slideshare.net/kartben/iot-developer-survey-2018。截至撰写本文时,三大云物联网服务提供商 AWS
   IoT、Google Cloud IoT 和 Microsoft Azure IoT 都提供 MQTT over
   TLS。一些反馈表明,一些人在各种网络上发现 UDP 协议和路由问题方面存在困难 (See https://www.slideshare.net/kartben/iot-developer-survey-2018. As
   of this writing, the three major cloud IoT service providers, AWS
   IoT, Google Cloud IoT, and Microsoft Azure IoT all provide MQTT over
   TLS. Some feedback has suggested that some find difficulty with UDP
   protocols and routing issues on various networks)。

.. [2]
   随着新漏洞的发现,被认为是安全的内容可能会发生变化。诸如 https://www.ssllabs.com/ 之类的组织提供有关如何配置 TLS 才能安全的当前想法的信息 (As new exploits are discovered, what is considered secure can
   change.
   Organizations such as https://www.ssllabs.com/ provide information on
   current ideas of how TLS must be configured to be secure)。

.. [3]
   请注意,仅擦除此闪存区域可能不足够 (Note that merely erasing this flash area is unlikely to be
   sufficient)。
