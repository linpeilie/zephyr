.. _west-install:

安装 west
########

West 使用 Python 3 编写，通过 `PyPI`_ 发布。
使用 :file:`pip3` 来安装或升级 west：

在 Linux 上::

  pip3 install --user -U west

在 Windows 和 macOS 上::

  pip3 install -U west

.. note::
   有关使用 ``--user`` 开关的其他说明，请参见 :ref:`python-pip`。

之后，你可以运行 ``pip3 show -f west`` 来获取有关 west 二进制文件和相关文件的安装位置的信息。

west 安装后，你可以使用它来 :ref:`克隆 Zephyr 仓库 <clone-zephyr>`。

.. _west-struct:

结构
****

West 的代码通过 PyPI 以名为 ``west`` 的 Python 包的形式发布。
此发行版包括一个启动器可执行文件，也称为 ``west``（在 Windows 上为 ``west.exe``）。

安装 west 后，启动器由 :file:`pip3` 放置在用户的文件系统的某处
（确切位置取决于操作系统，但应该在 ``PATH`` :ref:`环境变量 <env_vars>` 上）。
此启动器是运行内置命令（如 ``west init``、``west update``）
以及在工作区中发现的任何扩展的命令行入口点。

除了命令行界面外，你还可以直接使用 west 的 Python API。
有关详细信息，请参见 :ref:`west-apis`。

.. _west-shell-completion:

启用 shell 补全
***************

West 目前在以下 shell 中支持 shell 补全：

* bash
* zsh
* fish
* powershell (仅限开发板限定符)

为了启用 shell 补全，你需要获取相应的补全脚本并将其源化。
使用补全脚本：

.. tabs::

  .. group-tab:: bash

    *一次性设置*：

    .. code-block:: bash

      source <(west completion bash)

    *永久设置*：

    .. code-block:: bash

      west completion bash > ~/west-completion.bash; echo "source ~/west-completion.bash" >> ~/.bashrc

  .. group-tab:: zsh

    *One-time setup*:

    .. code-block:: zsh

      source <(west completion zsh)

    *永久设置*：

    .. code-block:: zsh

      west completion zsh > "${fpath[1]}/_west"

  .. group-tab:: fish

    *一次性设置*：

    .. code-block:: fish

      west completion fish | source

    *永久设置*：

    .. code-block:: fish

      west completion fish > $HOME/.config/fish/completions/west.fish

  .. group-tab:: powershell

    *一次性设置*：

    .. code-block:: powershell

      west completion powershell | Out-String | Invoke-Expression

    *永久设置*：

    .. code-block:: powershell

      Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
      New-item -type file -force $PROFILE
      west completion powershell > $HOME/west-completion.ps1
      (Add-Content -Path $PROFILE -Value ". '{$HOME/west-completion.ps1}'")

.. _PyPI:
   https://pypi.org/project/west/
