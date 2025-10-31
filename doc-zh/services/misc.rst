.. _misc_api:

杂项 (Miscellaneous)
#############

.. comment
   不包含文档
   .. doxygengroup:: checksum
   .. doxygengroup:: structured_data

校验和API (Checksum APIs)
*************

CRC
=====

.. doxygengroup:: crc

结构化数据API (Structured Data APIs)
********************

JSON
====

.. doxygengroup:: json

JWT
===

JSON Web令牌 (JSON Web Tokens, JWT) 是一种开放的工业标准 [RFC
7519](https://tools.ietf.org/html/rfc7519) 方法，用于在两方之间安全地表示声明 (claims)。尽管JWT相当灵活，但此API仅限于创建与Google Core IoT基础设施进行身份验证所需的简单令牌。

.. doxygengroup:: jwt

标识符API (Identifier APIs)
***************

UUID
====

通用唯一标识符 (Universally Unique Identifiers, UUID)，也称为全局唯一标识符 (Globally Unique
IDentifiers, GUIDs)，是一种开放的工业标准 [RFC
9562](https://tools.ietf.org/html/rfc9562) 128位长标识符，旨在保证跨时空的唯一性。

.. doxygengroup:: uuid
