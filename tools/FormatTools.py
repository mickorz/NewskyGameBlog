#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文件名和文件夹格式化工具
用于规范化content目录下的markdown文件名、文件夹名和内部链接

功能：
1. 将文件夹名转换为小写
2. 将文件名转换为小写
3. 移除文件名中的中文字符
4. 使用 - 作为单词分隔符，替换 _
5. 更新文件内的markdown链接引用
6. 删除 .meta 后缀的文件
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


# 设置标准输出的编码为UTF-8，避免Windows下的编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class MarkdownFileFormatter:
    """Markdown文件和文件夹格式化器"""

    def __init__(self, content_dir: str):
        """
        初始化
        Args:
            content_dir: content目录的路径
        """
        self.content_dir = Path(content_dir)
        self.file_mappings: Dict[str, str] = {}  # 旧文件名 -> 新文件名的映射
        self.folder_mappings: Dict[Path, Path] = {}  # 旧文件夹路径 -> 新文件夹路径的映射
        self.dry_run = False  # 是否为测试运行（不实际修改文件）

    def normalize_filename(self, filename: str) -> str:
        """
        规范化文件名
        Args:
            filename: 原始文件名（不含路径）
        Returns:
            规范化后的文件名
        """
        # 保存文件扩展名
        name, ext = os.path.splitext(filename)

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

        # 按路径深度从深到浅排序（确保先处理子文件夹，再处理父文件夹）
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

    def update_file_links(self, file_path: Path):
        """
        更新文件中的markdown链接（包括文件夹路径和文件名）
        Args:
            file_path: 要更新的文件路径
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # 查找所有markdown链接 [text](url) 和 [text]: url
            # 匹配 [xxx](xxx.md) 和 [xxx]: xxx.md
            link_patterns = [
                (r'\[([^\]]+)\]\(([^)]+\.md)\)', r'[\1]({})'),  # [text](file.md)
                (r'\[([^\]]+)\]:\s*([^\s]+\.md)', r'[\1]: {}'),  # [text]: file.md
            ]

            for pattern, replacement_template in link_patterns:
                def replace_link(match):
                    text = match.group(1)
                    link = match.group(2)
                    original_link = link

                    # 提取路径部分和文件名
                    link_parts = link.split('/')

                    # 更新文件夹名称（转换为小写）
                    for i in range(len(link_parts) - 1):
                        link_parts[i] = self.normalize_foldername(link_parts[i])

                    # 更新文件名（如果在映射中）
                    old_filename = link_parts[-1]
                    if old_filename in self.file_mappings:
                        link_parts[-1] = self.file_mappings[old_filename]

                    new_link = '/'.join(link_parts)

                    if new_link != original_link:
                        print(f"  更新链接: {original_link} -> {new_link}")
                        return replacement_template.format(new_link)

                    return match.group(0)

                content = re.sub(pattern, replace_link, content)

            # 如果内容有变化，写回文件
            if content != original_content:
                if not self.dry_run:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                print(f"✓ 已更新文件内链接: {file_path.relative_to(self.content_dir)}")

        except Exception as e:
            print(f"✗ 更新文件链接失败 {file_path}: {e}")

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
            dry_run: 如果为True，只显示将要执行的操作，不实际修改文件
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

        if not folder_mappings and not file_mappings and not meta_files:
            print("没有需要处理的文件或文件夹")
            return

        # 6. 执行文件夹重命名（从深到浅）
        if folder_mappings:
            print("[步骤 6] 执行文件夹重命名...")
            self.rename_folders(folder_mappings)
            print()

        # 7. 执行文件重命名
        if file_mappings:
            print("[步骤 7] 执行文件重命名...")
            self.rename_files(file_mappings)
            print()

        # 8. 更新所有markdown文件中的链接
        print("[步骤 8] 更新文件内链接...")
        # 重新扫描所有文件（因为路径可能已改变）
        all_files = self.scan_markdown_files()
        for md_file in all_files:
            self.update_file_links(md_file)
        print()

        # 9. 删除.meta文件
        if meta_files:
            print("[步骤 9] 删除.meta文件...")
            self.delete_meta_files(meta_files)
            print()

        print("=" * 60)
        print("处理完成！")
        print("=" * 60)


def main():
    """主函数"""
    # 获取content目录的路径（相对于脚本所在目录）
    script_dir = Path(__file__).parent
    content_dir = script_dir.parent / 'content'

    if not content_dir.exists():
        print(f"错误: content目录不存在: {content_dir}")
        return

    # 创建格式化器
    formatter = MarkdownFileFormatter(str(content_dir))

    # 先进行测试运行，让用户确认
    print("即将开始格式化markdown文件和文件夹...")
    print(f"目标目录: {content_dir}\n")

    # 执行格式化
    formatter.run(dry_run=False)


if __name__ == '__main__':
    main()
