#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
为markdown文件批量添加Front Matter
Hugo需要Front Matter来识别和生成页面
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime


# 设置标准输出的编码为UTF-8，避免Windows下的编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class FrontMatterAdder:
    """Front Matter添加器"""

    def __init__(self, content_dir: str):
        """
        初始化
        Args:
            content_dir: content目录的路径
        """
        self.content_dir = Path(content_dir)
        self.processed_count = 0
        self.skipped_count = 0

    def has_front_matter(self, content: str) -> bool:
        """
        检查文件是否已有Front Matter
        Args:
            content: 文件内容
        Returns:
            True if has front matter
        """
        return content.strip().startswith('---')

    def extract_title(self, content: str) -> str:
        """
        从markdown内容中提取标题
        Args:
            content: 文件内容
        Returns:
            提取的标题
        """
        # 查找第一个 # 标题
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                title = line[2:].strip()
                # 移除可能的特殊字符
                title = title.replace('官方文档', '').strip()
                return title

        return "Untitled"

    def create_front_matter(self, title: str) -> str:
        """
        创建Front Matter
        Args:
            title: 文章标题
        Returns:
            Front Matter字符串
        """
        date = datetime.now().strftime('%Y-%m-%d')

        front_matter = f"""---
title: "{title}"
date: {date}
draft: false
---

"""
        return front_matter

    def process_file(self, file_path: Path):
        """
        处理单个markdown文件
        Args:
            file_path: 文件路径
        """
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 检查是否已有Front Matter
            if self.has_front_matter(content):
                print(f"⊘ 跳过（已有Front Matter）: {file_path.relative_to(self.content_dir)}")
                self.skipped_count += 1
                return

            # 提取标题
            title = self.extract_title(content)

            # 创建Front Matter
            front_matter = self.create_front_matter(title)

            # 合并内容
            new_content = front_matter + content

            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"✓ 已添加Front Matter: {file_path.relative_to(self.content_dir)} (标题: {title})")
            self.processed_count += 1

        except Exception as e:
            print(f"✗ 处理失败 {file_path}: {e}")

    def process_all(self):
        """
        处理所有markdown文件
        """
        print("=" * 60)
        print("批量添加Front Matter工具")
        print("=" * 60)
        print()

        # 查找所有markdown文件
        md_files = list(self.content_dir.rglob('*.md'))
        print(f"找到 {len(md_files)} 个markdown文件\n")

        # 处理每个文件
        for md_file in md_files:
            self.process_file(md_file)

        # 打印统计
        print()
        print("=" * 60)
        print(f"处理完成！")
        print(f"✓ 成功处理: {self.processed_count} 个文件")
        print(f"⊘ 跳过: {self.skipped_count} 个文件")
        print("=" * 60)


def main():
    """主函数"""
    # 获取content目录的路径
    script_dir = Path(__file__).parent
    content_dir = script_dir.parent / 'content'

    if not content_dir.exists():
        print(f"错误: content目录不存在: {content_dir}")
        return

    # 创建处理器
    adder = FrontMatterAdder(str(content_dir))

    # 执行处理
    adder.process_all()


if __name__ == '__main__':
    main()
