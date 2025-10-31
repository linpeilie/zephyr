..
    Zephyr Project documentation main file

.. _zephyr-home:

Zephyr 项目文档
################

.. only:: release

    欢迎阅读 Zephyr 项目的 |version| 版本文档。

    Zephyr 最新（main）开发分支的文档请参见：https://docs.zephyrproject.org/

.. only:: (development or daily)

    **欢迎阅读 Zephyr 项目主开发分支的文档**（版本 |version|）。

请使用左侧的版本选择菜单查看特定 Zephyr 版本的文档。


.. raw:: html

   <ul class="grid">
       <li class="grid-item">
       <a href="introduction/index.html">
           <img alt="" src="_static/images/kite.png"/>
           <h2>简介</h2>
       </a>
       <p>架构、特性与许可信息</p>
       </li>
       <li class="grid-item">
       <a href="develop/getting_started/index.html">
               <span class="grid-icon fa fa-map-signs"></span>
           <h2>快速开始指南</h2>
       </a>
       <p>安装配置 Zephyr，构建并运行示例应用</p>
       </li>
       <li class="grid-item">
       <a href="samples/index.html">
               <span class="grid-icon fa fa-cogs"></span>
           <h2>示例与演示</h2>
       </a>
       <p>探索适用于各类开发板的示例与演示</p>
       </li>
       <li class="grid-item">
       <a href="boards/index.html">
               <span class="grid-icon fa fa-object-group"></span>
           <h2>支持的开发板</h2>
       </a>
       <p>受支持的开发板与平台列表</p>
       </li>
       <li class="grid-item">
       <a href="hardware/index.html">
               <span class="grid-icon fa fa-sign-in"></span>
           <h2>硬件支持</h2>
       </a>
       <p>支持的硬件与移植指南</p>
       </li>
       <li class="grid-item">
       <a href="security/index.html">
               <span class="grid-icon fa fa-lock"></span>
           <h2>安全</h2>
       </a>
       <p>安全流程与指南</p>
       </li>
       <li class="grid-item">
       <a href="services/index.html">
               <span class="grid-icon fa fa-puzzle-piece"></span>
           <h2>操作系统服务</h2>
       </a>
       <p>操作系统服务与使用指南</p>
       </li>
       <li class="grid-item">
       <a href="contribute/index.html">
               <span class="grid-icon fa fa-github"></span>
           <h2>贡献指南</h2>
       </a>
       <p>如何提交补丁并为 Zephyr 做出贡献</p>
       </li>
   </ul>

有关以往版本的变更与新增内容，请参阅已发布的 :ref:`zephyr_release_notes` 文档。

Zephyr OS 采用 `Apache 2.0 许可证`_ 授权（详见项目 `GitHub 仓库`_ 中的 LICENSE 文件）。
Zephyr OS 还导入或复用了一些采用其它许可证的软件包、脚本和文件，详见 :ref:`Zephyr_Licensing`。

.. toctree::
   :maxdepth: 1
   :hidden:

   introduction/index.rst
   develop/index.rst
   kernel/index.rst
   services/index.rst
   build/index.rst
   connectivity/index.rst
   hardware/index.rst
   contribute/index.rst
   project/index.rst
   security/index.rst
   safety/index.rst
   samples/index.rst
   boards/index.rst
   releases/index.rst

索引与表格
**********

* :ref:`glossary`
* :ref:`genindex`

.. _Apache 2.0 license:
   https://github.com/zephyrproject-rtos/zephyr/blob/main/LICENSE

.. _GitHub repo: https://github.com/zephyrproject-rtos/zephyr
