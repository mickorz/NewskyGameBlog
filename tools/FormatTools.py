#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文件名、文件夹、Front Matter和链接格式化工具
用于规范化content目录下的markdown文件

功能：
1. 将文件夹名转换为小写
2. 将文件名转换为小写
3. 移除文件名中的中文字符
4. 使用 - 作为单词分隔符，替换 _
5. 添加/更新Front Matter（包含完整元数据）
6. 将markdown链接转换为Hugo ref格式
7. 更新hugo.toml中的链接
8. 删除 .meta 后缀的文件
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


# 设置标准输出的编码为UTF-8，避免Windows下的编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class MarkdownFileFormatter:
    """Markdown文件和文件夹格式化器"""

    def __init__(self, content_dir: str, hugo_toml_path: str = None):
        """
        初始化
        Args:
            content_dir: content目录的路径
            hugo_toml_path: hugo.toml文件路径
        """
        self.content_dir = Path(content_dir)
        self.hugo_toml_path = Path(hugo_toml_path) if hugo_toml_path else None
        self.file_mappings: Dict[str, str] = {}  # 旧文件名 -> 新文件名的映射
        self.folder_mappings: Dict[Path, Path] = {}  # 旧文件夹路径 -> 新文件夹路径的映射
        self.dry_run = False  # 是否为测试运行

    def normalize_filename(self, filename: str) -> str:
        """
        规范化文件名
        Args:
            filename: 原始文件名（不含路径）
        Returns:
            规范化后的文件名
        """
        name, ext = os.path.splitext(filename)

        # 特殊处理：index.md 或 readme.md 转换为 _index.md (Hugo约定)
        if name.lower() in ['index', 'readme']:
            return '_index' + ext

        # 1. 移除中文字符
        name = re.sub(r'[\u4e00-\u9fff]+', '', name)

        # 2. 将下划线替换为连字符
        name = name.replace('_', '-')

        # 3. 转换为小写
        name = name.lower()

        # 4. 移除多余的连字符
        name = re.sub(r'-+', '-', name)

        # 5. 移除首尾的连字符
        name = name.strip('-')

        return name + ext

    def normalize_foldername(self, foldername: str) -> str:
        """
        规范化文件夹名（只转换为小写）
        Args:
            foldername: 原始文件夹名
        Returns:
            规范化后的文件夹名
        """
        return foldername.lower()

    def extract_title(self, content: str) -> str:
        """
        从markdown内容中提取标题
        Args:
            content: 文件内容
        Returns:
            提取的标题
        """
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                title = line[2:].strip()
                # 移除可能的特殊字符
                title = title.replace('官方文档', '').strip()
                return title
        return "Untitled"

    def extract_tags_from_path(self, file_path: Path) -> List[str]:
        """
        从文件路径提取标签
        Args:
            file_path: 文件路径
        Returns:
            标签列表
        """
        tags = ["Unity", "Animancer"]

        # 根据路径添加标签
        path_str = str(file_path.relative_to(self.content_dir))

        if 'fsm' in path_str.lower():
            tags.append("FSM")
        if 'blend' in path_str.lower():
            tags.append("Blending")
        if 'event' in path_str.lower():
            tags.append("Events")
        if 'transition' in path_str.lower():
            tags.append("Transitions")
        if 'animator' in path_str.lower():
            tags.append("Animator")
        if 'ik' in path_str.lower():
            tags.append("IK")

        return tags

    def has_front_matter(self, content: str) -> bool:
        """
        检查文件是否已有Front Matter
        Args:
            content: 文件内容
        Returns:
            True if has front matter
        """
        return content.strip().startswith('---')

    def create_front_matter(self, title: str, tags: List[str], description: str = "") -> str:
        """
        创建Front Matter
        Args:
            title: 文章标题
            tags: 标签列表
            description: 描述
        Returns:
            Front Matter字符串
        """
        now = datetime.now()
        date_str = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')

        tags_str = ', '.join([f'"{tag}"' for tag in tags])

        if not description:
            description = f"深入了解 {title} 的使用方法和最佳实践"

        front_matter = f"""---
title: "{title}"
date: {date_str}
lastmod: {date_str}
draft: false
author: "逸空"
type: "posts"
tags: [{tags_str}]
categories: ["技术笔记"]
description: "{description}"
---

"""
        return front_matter

    def update_front_matter_in_content(self, content: str, title: str, tags: List[str]) -> str:
        """
        更新或添加Front Matter
        Args:
            content: 原始内容
            title: 标题
            tags: 标签
        Returns:
            更新后的内容
        """
        if self.has_front_matter(content):
            # 已有Front Matter，保留原内容
            return content
        else:
            # 添加新的Front Matter
            front_matter = self.create_front_matter(title, tags)
            return front_matter + content

    def fix_placeholder_links(self, content: str) -> str:
        """
        修复占位符链接 [\1] -> [filename]
        Args:
            content: 文件内容
        Returns:
            修复后的内容
        """
        # 匹配 [\1]({{< ref "filename.md" >}}) 格式
        def replace_placeholder(match):
            # 提取ref中的文件名
            ref_content = match.group(1)
            # 从ref "filename.md"中提取文件名
            filename_match = re.search(r'"([^"]+\.md)"', ref_content)
            if filename_match:
                filename = filename_match.group(1)
                # 移除.md后缀作为显示文本
                text = filename.replace('.md', '')
                return f'[{text}]({{{{< {ref_content} >}}}})'
            return match.group(0)

        # 修复 [\1]({{< ref "..." >}}) 格式
        content = re.sub(r'\[\\1\]\(\{\{<\s*(.+?)\s*>\}\}\)', replace_placeholder, content)

        return content

    def convert_links_to_ref(self, content: str) -> str:
        """
        将markdown链接转换为Hugo ref格式
        Args:
            content: 文件内容
        Returns:
            转换后的内容
        """
        # 匹配 [text](path/to/file.md) 格式
        def replace_link(match):
            original_text = match.group(1)
            link = match.group(2)

            # 只转换相对路径的.md链接
            if link.endswith('.md') and not link.startswith('http'):
                # 提取文件名
                filename = os.path.basename(link)
                # 使用文件名作为显示文本
                text = filename.replace(".md","")
                # 转换为ref格式
                return f'[{text}]({{{{< ref "{filename}" >}}}})'

            return match.group(0)

        # 处理 [text](link.md) 格式
        content = re.sub(r'\[([^\]]+)\]\(([^)]+\.md)\)', replace_link, content)

        return content

    def scan_folders(self) -> List[Path]:
        """
        扫描所有子文件夹（按深度从深到浅排序）
        Returns:
            文件夹路径列表（从深到浅）
        """
        folders = []
        for root, dirs, files in os.walk(self.content_dir):
            for dir_name in dirs:
                folder_path = Path(root) / dir_name
                folders.append(folder_path)

        # 按路径深度从深到浅排序
        folders.sort(key=lambda p: len(p.parts), reverse=True)
        return folders

    def scan_markdown_files(self) -> List[Path]:
        """
        扫描所有markdown文件
        Returns:
            markdown文件路径列表
        """
        md_files = []
        for md_file in self.content_dir.rglob('*.md'):
            md_files.append(md_file)
        return md_files

    def scan_meta_files(self) -> List[Path]:
        """
        扫描所有.meta文件
        Returns:
            .meta文件路径列表
        """
        meta_files = []
        for meta_file in self.content_dir.rglob('*.meta'):
            meta_files.append(meta_file)
        return meta_files

    def build_folder_mappings(self, folders: List[Path]) -> Dict[Path, Path]:
        """
        构建文件夹重命名映射
        Args:
            folders: 文件夹路径列表
        Returns:
            映射字典 {旧路径: 新路径}
        """
        mappings = {}
        for old_path in folders:
            old_name = old_path.name
            new_name = self.normalize_foldername(old_name)

            if old_name != new_name:
                new_path = old_path.parent / new_name
                mappings[old_path] = new_path
                print(f"计划重命名文件夹: {old_path.relative_to(self.content_dir)} -> {new_name}")

        return mappings

    def build_file_mappings(self, md_files: List[Path]) -> Dict[str, Tuple[Path, Path]]:
        """
        构建文件重命名映射
        Args:
            md_files: markdown文件路径列表
        Returns:
            映射字典 {原文件名: (原路径, 新路径)}
        """
        mappings = {}
        for old_path in md_files:
            old_name = old_path.name
            new_name = self.normalize_filename(old_name)

            if old_name != new_name:
                new_path = old_path.parent / new_name
                mappings[old_name] = (old_path, new_path)
                self.file_mappings[old_name] = new_name
                print(f"计划重命名文件: {old_name} -> {new_name}")

        return mappings

    def process_markdown_file(self, file_path: Path):
        """
        处理markdown文件：添加Front Matter和转换链接
        Args:
            file_path: 文件路径
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            modified = False

            # 1. 添加/更新Front Matter
            if not self.has_front_matter(content):
                title = self.extract_title(content)
                tags = self.extract_tags_from_path(file_path)
                content = self.update_front_matter_in_content(content, title, tags)
                modified = True
                print(f"  添加Front Matter: {title}")

            # 2. 修复占位符链接 [\1] -> [filename]
            new_content = self.fix_placeholder_links(content)
            if new_content != content:
                content = new_content
                modified = True
                print(f"  修复占位符链接")

            # 3. 转换链接为ref格式
            new_content = self.convert_links_to_ref(content)
            if new_content != content:
                content = new_content
                modified = True
                print(f"  转换链接为ref格式")

            # 写回文件
            if modified and not self.dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                if modified:
                    print(f"✓ 已更新: {file_path.relative_to(self.content_dir)}")

        except Exception as e:
            print(f"✗ 处理失败 {file_path}: {e}")

    def update_hugo_toml(self):
        """
        更新hugo.toml中的链接
        """
        if not self.hugo_toml_path or not self.hugo_toml_path.exists():
            return

        try:
            with open(self.hugo_toml_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # 更新文件名（下划线改为连字符）
            for old_name, new_name in self.file_mappings.items():
                # 移除.md后缀进行替换
                old_base = old_name.replace('.md', '')
                new_base = new_name.replace('.md', '')
                content = content.replace(old_base, new_base)

            # 更新文件夹名为小写
            content = re.sub(r'/Animancer/', '/animancer/', content)
            content = re.sub(r'/FSM/', '/fsm/', content)
            content = re.sub(r'/Blend/', '/blend/', content)
            content = re.sub(r'/Event/', '/event/', content)
            content = re.sub(r'/Transition/', '/transition/', content)
            content = re.sub(r'/Animator/', '/animator/', content)
            content = re.sub(r'/Why/', '/why/', content)

            if content != original_content and not self.dry_run:
                with open(self.hugo_toml_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print("✓ 已更新hugo.toml")

        except Exception as e:
            print(f"✗ 更新hugo.toml失败: {e}")

    def rename_folders(self, mappings: Dict[Path, Path]):
        """
        执行文件夹重命名
        Args:
            mappings: 重命名映射
        """
        for old_path, new_path in mappings.items():
            try:
                if not self.dry_run:
                    old_path.rename(new_path)
                print(f"✓ 已重命名文件夹: {old_path.relative_to(self.content_dir)} -> {new_path.name}")
            except Exception as e:
                print(f"✗ 重命名文件夹失败 {old_path.relative_to(self.content_dir)}: {e}")

    def rename_files(self, mappings: Dict[str, Tuple[Path, Path]]):
        """
        执行文件重命名
        Args:
            mappings: 重命名映射
        """
        for old_name, (old_path, new_path) in mappings.items():
            try:
                if not self.dry_run:
                    old_path.rename(new_path)
                print(f"✓ 已重命名文件: {old_name} -> {new_path.name}")
            except Exception as e:
                print(f"✗ 重命名文件失败 {old_name}: {e}")

    def delete_meta_files(self, meta_files: List[Path]):
        """
        删除.meta文件
        Args:
            meta_files: .meta文件路径列表
        """
        for meta_file in meta_files:
            try:
                if not self.dry_run:
                    meta_file.unlink()
                print(f"✓ 已删除: {meta_file.relative_to(self.content_dir)}")
            except Exception as e:
                print(f"✗ 删除失败 {meta_file.relative_to(self.content_dir)}: {e}")

    def run(self, dry_run: bool = False):
        """
        执行格式化流程
        Args:
            dry_run: 如果为True，只显示将要执行的操作
        """
        self.dry_run = dry_run

        print("=" * 60)
        print("Markdown文件和文件夹格式化工具")
        print("=" * 60)

        if dry_run:
            print("【测试模式】只显示将要执行的操作，不会实际修改文件\n")

        # 1. 扫描文件夹
        print("\n[步骤 1] 扫描文件夹...")
        folders = self.scan_folders()
        print(f"找到 {len(folders)} 个子文件夹\n")

        # 2. 扫描所有markdown文件
        print("[步骤 2] 扫描markdown文件...")
        md_files = self.scan_markdown_files()
        print(f"找到 {len(md_files)} 个markdown文件\n")

        # 3. 扫描.meta文件
        print("[步骤 3] 扫描.meta文件...")
        meta_files = self.scan_meta_files()
        if meta_files:
            print(f"找到 {len(meta_files)} 个.meta文件\n")
        else:
            print("未找到.meta文件\n")

        # 4. 构建文件夹重命名映射
        print("[步骤 4] 构建文件夹重命名映射...")
        folder_mappings = self.build_folder_mappings(folders)
        print(f"需要重命名 {len(folder_mappings)} 个文件夹\n")

        # 5. 构建文件重命名映射
        print("[步骤 5] 构建文件重命名映射...")
        file_mappings = self.build_file_mappings(md_files)
        print(f"需要重命名 {len(file_mappings)} 个文件\n")

        # 6. 执行文件夹重命名
        if folder_mappings:
            print("[步骤 6] 执行文件夹重命名...")
            self.rename_folders(folder_mappings)
            print()

        # 7. 执行文件重命名
        if file_mappings:
            print("[步骤 7] 执行文件重命名...")
            self.rename_files(file_mappings)
            print()

        # 8. 处理所有markdown文件（添加Front Matter和转换链接）
        print("[步骤 8] 处理markdown文件（Front Matter和链接）...")
        all_files = self.scan_markdown_files()
        for md_file in all_files:
            self.process_markdown_file(md_file)
        print()

        # 9. 更新hugo.toml
        if self.hugo_toml_path:
            print("[步骤 9] 更新hugo.toml...")
            self.update_hugo_toml()
            print()

        # 10. 删除.meta文件
        if meta_files:
            print("[步骤 10] 删除.meta文件...")
            self.delete_meta_files(meta_files)
            print()

        print("=" * 60)
        print("处理完成！")
        print("=" * 60)


def main():
    """主函数"""
    script_dir = Path(__file__).parent
    content_dir = script_dir.parent / 'content'
    hugo_toml = script_dir.parent / 'hugo.toml'

    if not content_dir.exists():
        print(f"错误: content目录不存在: {content_dir}")
        return

    # 创建格式化器
    formatter = MarkdownFileFormatter(str(content_dir), str(hugo_toml))

    print("即将开始格式化markdown文件和文件夹...")
    print(f"目标目录: {content_dir}\n")

    # 执行格式化
    formatter.run(dry_run=False)


if __name__ == '__main__':
    main()
