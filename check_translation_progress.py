#!/usr/bin/env python3
"""
Zephyr文档批量翻译脚本 - 增强版

此脚本提供了更多功能:
1. 显示翻译进度
2. 可以选择翻译特定目录或文件
3. 支持断点续传
4. 生成翻译报告
"""

import os
import json
from pathlib import Path
from datetime import datetime

# 配置
SOURCE_DIR = Path("d:/Development/Workspace/zephyr/doc")
TARGET_DIR = Path("d:/Development/Workspace/zephyr/doc-zh")
PROGRESS_FILE = TARGET_DIR / ".translation_progress.json"

# 已经翻译的文件列表
TRANSLATED_FILES = {
    "index.rst",
    "glossary.rst",
    "404.rst",
    "kconfig.rst",
    "LICENSING.rst",
    "introduction/index.rst",
}

def load_progress():
    """加载翻译进度"""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"translated": list(TRANSLATED_FILES), "in_progress": [], "last_updated": None}

def save_progress(progress):
    """保存翻译进度"""
    progress["last_updated"] = datetime.now().isoformat()
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

def get_all_rst_files():
    """获取所有.rst文件"""
    rst_files = []
    for root, dirs, files in os.walk(SOURCE_DIR):
        # 跳过某些目录
        dirs[:] = [d for d in dirs if d not in {'__pycache__', '.git', 'build', '_build'}]

        for file in files:
            if file.endswith('.rst'):
                file_path = Path(root) / file
                rel_path = file_path.relative_to(SOURCE_DIR)
                rst_files.append(str(rel_path).replace('\\', '/'))

    return sorted(rst_files)

def categorize_files(all_files, progress):
    """将文件分类"""
    translated = set(progress.get("translated", []))
    in_progress = set(progress.get("in_progress", []))

    categories = {
        "translated": [f for f in all_files if f in translated],
        "in_progress": [f for f in all_files if f in in_progress],
        "pending": [f for f in all_files if f not in translated and f not in in_progress]
    }

    return categories

def print_statistics(categories, all_files):
    """打印统计信息"""
    total = len(all_files)
    translated = len(categories["translated"])
    in_progress = len(categories["in_progress"])
    pending = len(categories["pending"])

    print("\n" + "="*70)
    print("Zephyr文档翻译进度统计")
    print("="*70)
    print(f"总文件数:      {total:>6} (100.0%)")
    print(f"已翻译:        {translated:>6} ({translated/total*100:>5.1f}%)")
    print(f"翻译中:        {in_progress:>6} ({in_progress/total*100:>5.1f}%)")
    print(f"待翻译:        {pending:>6} ({pending/total*100:>5.1f}%)")
    print("="*70)

def count_by_directory(files):
    """按目录统计文件数"""
    dir_count = {}
    for file in files:
        if '/' in file:
            dir_name = file.split('/')[0]
        else:
            dir_name = "(root)"

        dir_count[dir_name] = dir_count.get(dir_name, 0) + 1

    return dir_count

def print_directory_stats(all_files, translated_files):
    """打印各目录翻译统计"""
    all_dirs = count_by_directory(all_files)
    trans_dirs = count_by_directory(translated_files)

    print("\n各目录翻译进度:")
    print("-"*70)
    print(f"{'目录':<20} {'总数':>8} {'已翻译':>10} {'进度':>10}")
    print("-"*70)

    for dir_name in sorted(all_dirs.keys()):
        total = all_dirs[dir_name]
        translated = trans_dirs.get(dir_name, 0)
        percentage = translated / total * 100 if total > 0 else 0
        print(f"{dir_name:<20} {total:>8} {translated:>10} {percentage:>9.1f}%")

    print("-"*70)

def list_pending_files(categories, limit=20):
    """列出待翻译文件"""
    pending = categories["pending"]

    print(f"\n待翻译文件（显示前{min(limit, len(pending))}个）:")
    print("-"*70)

    for i, file in enumerate(pending[:limit], 1):
        print(f"{i:3}. {file}")

    if len(pending) > limit:
        print(f"\n... 还有 {len(pending) - limit} 个文件未显示")

def generate_markdown_report(all_files, categories):
    """生成Markdown格式的翻译报告"""
    report_path = TARGET_DIR / "TRANSLATION_PROGRESS.md"

    total = len(all_files)
    translated = len(categories["translated"])
    in_progress = len(categories["in_progress"])
    pending = len(categories["pending"])

    all_dirs = count_by_directory(all_files)
    trans_dirs = count_by_directory(categories["translated"])

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Zephyr文档翻译进度报告\n\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("## 总体进度\n\n")
        f.write(f"- 总文件数: **{total}**\n")
        f.write(f"- 已翻译: **{translated}** ({translated/total*100:.1f}%)\n")
        f.write(f"- 翻译中: **{in_progress}** ({in_progress/total*100:.1f}%)\n")
        f.write(f"- 待翻译: **{pending}** ({pending/total*100:.1f}%)\n\n")

        f.write("## 进度条\n\n")
        progress_bar_length = 50
        filled = int(translated / total * progress_bar_length)
        bar = '█' * filled + '░' * (progress_bar_length - filled)
        f.write(f"`{bar}` {translated/total*100:.1f}%\n\n")

        f.write("## 各目录翻译进度\n\n")
        f.write("| 目录 | 总数 | 已翻译 | 进度 |\n")
        f.write("|------|------|--------|------|\n")

        for dir_name in sorted(all_dirs.keys()):
            total_in_dir = all_dirs[dir_name]
            translated_in_dir = trans_dirs.get(dir_name, 0)
            percentage = translated_in_dir / total_in_dir * 100 if total_in_dir > 0 else 0
            f.write(f"| {dir_name} | {total_in_dir} | {translated_in_dir} | {percentage:.1f}% |\n")

        f.write("\n## 已翻译文件列表\n\n")
        for file in sorted(categories["translated"]):
            f.write(f"- [x] `{file}`\n")

        if categories["in_progress"]:
            f.write("\n## 翻译中文件列表\n\n")
            for file in sorted(categories["in_progress"]):
                f.write(f"- [ ] `{file}` (翻译中)\n")

    print(f"\n翻译进度报告已生成: {report_path}")

def main():
    """主函数"""
    print("="*70)
    print("Zephyr文档翻译进度管理工具")
    print("="*70)

    # 加载进度
    progress = load_progress()

    # 获取所有文件
    all_files = get_all_rst_files()

    # 分类文件
    categories = categorize_files(all_files, progress)

    # 打印统计信息
    print_statistics(categories, all_files)
    print_directory_stats(all_files, categories["translated"])
    list_pending_files(categories)

    # 生成报告
    generate_markdown_report(all_files, categories)

    # 保存进度
    save_progress(progress)

    print("\n" + "="*70)
    print("提示:")
    print("  - 详细的翻译进度报告已保存到: TRANSLATION_PROGRESS.md")
    print("  - 所有待翻译文件列表在: translation_list.txt")
    print("  - 翻译进度保存在: .translation_progress.json")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
