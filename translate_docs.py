#!/usr/bin/env python3
"""
Zephyr文档翻译脚本
此脚本将doc目录下的所有.rst文档文件翻译为中文，并输出到doc-zh目录
"""

import os
import shutil
from pathlib import Path

# 源文档目录和目标目录
SOURCE_DIR = Path("d:/Development/Workspace/zephyr/doc")
TARGET_DIR = Path("d:/Development/Workspace/zephyr/doc-zh")

# 不需要翻译的文件类型
SKIP_EXTENSIONS = {'.py', '.pyc', '.jpg', '.png', '.svg', '.gif', '.pdf',
                   '.yaml', '.yml', '.json', '.cmake', '.in', '.txt'}

# 不需要翻译的目录
SKIP_DIRS = {'__pycache__', '.git', 'build', '_build'}

def should_translate(file_path):
    """判断文件是否需要翻译"""
    # 跳过非.rst文件
    if file_path.suffix not in ['.rst']:
        return False

    # 检查是否在跳过的目录中
    for skip_dir in SKIP_DIRS:
        if skip_dir in file_path.parts:
            return False

    return True

def copy_non_rst_files(src_path, dst_path):
    """复制非rst文件（如图片、配置文件等）"""
    if src_path.is_file():
        # 创建目标目录
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        # 复制文件
        shutil.copy2(src_path, dst_path)
        print(f"已复制: {src_path} -> {dst_path}")

def get_all_rst_files():
    """获取所有需要翻译的.rst文件"""
    rst_files = []

    for root, dirs, files in os.walk(SOURCE_DIR):
        # 移除跳过的目录
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        root_path = Path(root)
        for file in files:
            file_path = root_path / file

            if should_translate(file_path):
                # 计算相对路径
                rel_path = file_path.relative_to(SOURCE_DIR)
                target_path = TARGET_DIR / rel_path
                rst_files.append((file_path, target_path))
            elif file_path.suffix not in SKIP_EXTENSIONS:
                # 复制其他支持文件
                rel_path = file_path.relative_to(SOURCE_DIR)
                target_path = TARGET_DIR / rel_path
                copy_non_rst_files(file_path, target_path)

    return rst_files

def translate_file(source_file, target_file):
    """
    翻译单个文件

    注意：此函数需要手动翻译或使用翻译API
    当前仅作为占位符，需要实际的翻译实现
    """
    # 创建目标目录
    target_file.parent.mkdir(parents=True, exist_ok=True)

    # 读取源文件
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # TODO: 这里需要实现实际的翻译逻辑
        # 可以使用翻译API或其他翻译服务
        # 当前仅将文件复制过去作为占位

        print(f"待翻译: {source_file}")
        print(f"  -> {target_file}")

        # 暂时复制文件（实际应该是翻译后的内容）
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)

    except Exception as e:
        print(f"处理文件时出错 {source_file}: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("Zephyr文档翻译工具")
    print("=" * 60)
    print(f"源目录: {SOURCE_DIR}")
    print(f"目标目录: {TARGET_DIR}")
    print("=" * 60)

    # 创建目标目录
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    # 获取所有需要翻译的文件
    rst_files = get_all_rst_files()

    print(f"\n找到 {len(rst_files)} 个.rst文件需要翻译\n")

    # 翻译每个文件
    for i, (source_file, target_file) in enumerate(rst_files, 1):
        print(f"\n[{i}/{len(rst_files)}] ", end="")
        translate_file(source_file, target_file)

    print("\n" + "=" * 60)
    print("处理完成！")
    print(f"已处理文件数: {len(rst_files)}")
    print("=" * 60)

    # 输出文件列表到一个文件，方便后续手动翻译
    with open(TARGET_DIR / "translation_list.txt", "w", encoding="utf-8") as f:
        f.write("需要翻译的文件列表：\n\n")
        for source_file, target_file in rst_files:
            f.write(f"{source_file}\n  -> {target_file}\n\n")

    print(f"\n文件列表已保存到: {TARGET_DIR / 'translation_list.txt'}")

if __name__ == "__main__":
    main()
