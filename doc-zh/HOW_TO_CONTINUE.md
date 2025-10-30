# 如何继续翻译Zephyr文档

## 快速开始

### 1. 查看当前进度

```bash
cd d:\Development\Workspace\zephyr
python check_translation_progress.py
```

### 2. 选择要翻译的文件

查看 `doc-zh/translation_list.txt` 文件，选择一个待翻译的文件。

建议优先翻译：
- `develop/getting_started/index.rst` - 入门指南主页
- `kernel/index.rst` - 内核文档主页
- `services/index.rst` - 服务文档主页

### 3. 翻译流程

#### 步骤1: 读取源文件
```bash
# 例如翻译 develop/getting_started/index.rst
cat doc/develop/getting_started/index.rst
```

#### 步骤2: 创建翻译文件
在 `doc-zh/` 对应位置创建同名文件，进行翻译。

#### 步骤3: 翻译规则
- ✅ 翻译所有文本内容
- ❌ 不翻译代码块
- ❌ 不翻译命令行
- ❌ 不翻译配置选项名
- ✅ 保留所有reStructuredText标记
- ✅ 参考 `glossary.rst` 中的术语对照

#### 步骤4: 更新进度
编辑 `doc-zh/.translation_progress.json`，将翻译的文件添加到 `translated` 列表中。

### 4. 使用AI辅助翻译

如果你想使用AI辅助翻译，可以：

1. 读取源文件内容
2. 使用AI翻译（如ChatGPT、Claude等）
3. 提示词示例：
   ```
   请将以下Zephyr项目的英文文档翻译成中文，要求：
   1. 保留所有reStructuredText格式标记
   2. 代码块保持英文不变
   3. 命令行命令保持英文不变
   4. 技术术语翻译要准确且一致
   5. 参考已有的术语表

   [粘贴源文件内容]
   ```

## 翻译示例

### 示例1: 简单段落

**原文:**
```rst
Zephyr is a small, scalable real-time operating system (RTOS) for
connected, resource-constrained embedded devices.
```

**译文:**
```rst
Zephyr是一个小型、可扩展的实时操作系统(RTOS)，
用于联网的、资源受限的嵌入式设备。
```

### 示例2: 带代码的段落

**原文:**
```rst
To build a sample, run:

.. code-block:: bash

   west build -b qemu_x86 samples/hello_world
```

**译文:**
```rst
要构建一个示例，运行:

.. code-block:: bash

   west build -b qemu_x86 samples/hello_world
```

### 示例3: 带链接的段落

**原文:**
```rst
For more information, see :ref:`getting_started`.
```

**译文:**
```rst
更多信息请参见 :ref:`getting_started`。
```

## 常见问题

### Q: 如何处理专业术语？
A: 参考 `doc-zh/glossary.rst` 中的术语对照表。如果遇到新术语，建议保留英文或添加括号注释。

### Q: 如何处理代码注释？
A: 代码块中的所有内容（包括注释）都保持英文不变。

### Q: 如何处理Kconfig选项？
A: Kconfig选项名称（如 `CONFIG_BLUETOOTH`）保持英文不变。

### Q: 如何处理文件路径？
A: 所有文件路径保持英文不变，如 `samples/hello_world`。

### Q: 翻译后如何验证？
A: 可以尝试使用Sphinx构建文档来验证格式是否正确。

## 推荐的翻译顺序

### 第一阶段（核心文档）
1. ✅ `index.rst` - 已完成
2. ✅ `glossary.rst` - 已完成
3. ✅ `introduction/index.rst` - 已完成
4. ⬜ `develop/getting_started/index.rst`
5. ⬜ `develop/getting_started/installation_linux.rst`
6. ⬜ `develop/getting_started/installation_win.rst`
7. ⬜ `develop/getting_started/installation_mac.rst`

### 第二阶段（内核文档）
8. ⬜ `kernel/index.rst`
9. ⬜ `kernel/services/index.rst`
10. ⬜ `kernel/services/threads/index.rst`
... （继续）

### 第三阶段（服务文档）
... （按需继续）

## 工具和资源

- **进度检查**: `python check_translation_progress.py`
- **文件列表**: `doc-zh/translation_list.txt`
- **进度报告**: `doc-zh/TRANSLATION_PROGRESS.md`
- **项目总结**: `doc-zh/PROJECT_SUMMARY.md`

## 联系和贡献

完成翻译后，可以：
1. 更新进度文件
2. 提交到版本控制系统
3. 与其他贡献者分享

---

祝翻译愉快！
