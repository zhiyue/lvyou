#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path
from typing import List, Tuple

class MarkdownMerger:
    def __init__(self, source_dir: str, output_file: str):
        self.source_dir = Path(source_dir)
        self.output_file = Path(output_file)
        self.toc_lines = []  # 目录
        self.content_lines = []  # 内容
        
    def merge_all(self):
        """合并所有Markdown文件"""
        print(f"开始合并 {self.source_dir} 目录下的所有Markdown文件...")
        
        # 添加文档标题
        self.content_lines.append("# 《绿邮® X系列开发板》使用指南 - 完整文档\n\n")
        self.content_lines.append("本文档由多个独立的Markdown文件合并而成，用于大模型阅读和理解。\n\n")
        self.content_lines.append("---\n\n")
        
        # 处理根目录的文件
        root_files = self._get_markdown_files(self.source_dir)
        if root_files:
            self._process_files(root_files, level=1, parent_path="")
        
        # 递归处理子目录
        self._process_directory(self.source_dir, level=1)
        
        # 生成目录
        toc_content = "## 目录\n\n" + "\n".join(self.toc_lines) + "\n\n---\n\n"
        
        # 写入文件
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(toc_content)
            f.write("\n".join(self.content_lines))
        
        print(f"合并完成！输出文件：{self.output_file}")
        print(f"共处理 {len([line for line in self.toc_lines if line.strip().startswith('-')])} 个文件")
    
    def _get_markdown_files(self, directory: Path) -> List[Path]:
        """获取目录中的Markdown文件（不包括子目录）"""
        files = []
        for item in sorted(directory.iterdir()):
            if item.is_file() and item.suffix == '.md':
                files.append(item)
        return files
    
    def _process_directory(self, directory: Path, level: int, parent_title: str = ""):
        """递归处理目录"""
        # 获取所有子目录
        subdirs = [d for d in sorted(directory.iterdir()) if d.is_dir() and d.name != 'images']
        
        for subdir in subdirs:
            # 目录标题
            dir_title = self._clean_dirname(subdir.name)
            full_title = f"{parent_title}/{dir_title}" if parent_title else dir_title
            
            # 添加到目录
            indent = "  " * (level - 1)
            self.toc_lines.append(f"{indent}- **{dir_title}/**")
            
            # 添加目录分隔
            self.content_lines.append(f"\n{'#' * (level + 1)} {dir_title}\n")
            
            # 处理目录中的文件
            files = self._get_markdown_files(subdir)
            if files:
                self._process_files(files, level + 1, full_title)
            
            # 递归处理子目录
            self._process_directory(subdir, level + 1, full_title)
    
    def _process_files(self, files: List[Path], level: int, parent_path: str):
        """处理文件列表"""
        for file_path in files:
            # 提取文件信息
            filename = file_path.name
            match = re.match(r'^(\d+)_(.+)\.md$', filename)
            if match:
                page_id = match.group(1)
                title = match.group(2)
            else:
                page_id = ""
                title = filename.replace('.md', '')
            
            # 添加到目录
            indent = "  " * (level - 1)
            self.toc_lines.append(f"{indent}- [{title}](#{self._make_anchor(title)})")
            
            # 读取文件内容
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 处理内容
                processed_content = self._process_content(content, file_path, level)
                
                # 添加锚点和内容
                anchor = f'<a name="{self._make_anchor(title)}"></a>\n'
                self.content_lines.append(anchor)
                self.content_lines.append(processed_content)
                self.content_lines.append("\n---\n")
                
                print(f"  已处理: {parent_path}/{title}" if parent_path else f"  已处理: {title}")
                
            except Exception as e:
                print(f"  错误: 无法处理文件 {file_path}: {e}")
    
    def _process_content(self, content: str, file_path: Path, base_level: int) -> str:
        """处理文件内容"""
        lines = content.split('\n')
        processed_lines = []
        in_metadata = False
        metadata_end = False
        
        for i, line in enumerate(lines):
            # 跳过元数据部分
            if i < 10 and line.strip() == '---':
                if not in_metadata:
                    in_metadata = True
                    continue
                else:
                    in_metadata = False
                    metadata_end = True
                    continue
            
            if in_metadata:
                continue
            
            # 调整标题级别
            if line.startswith('#'):
                # 计算原始级别
                original_level = len(line) - len(line.lstrip('#'))
                # 调整级别（保留原始结构，但整体下移）
                new_level = original_level + base_level
                # 确保不超过6级
                new_level = min(new_level, 6)
                line = '#' * new_level + line[original_level:]
            
            # 处理图片路径
            # 将相对路径转换为基于源目录的路径
            line = self._fix_image_paths(line, file_path)
            
            processed_lines.append(line)
        
        return '\n'.join(processed_lines).strip()
    
    def _fix_image_paths(self, line: str, file_path: Path) -> str:
        """修正图片路径"""
        # 查找 markdown 图片语法
        img_pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
        
        def replace_img(match):
            alt_text = match.group(1)
            img_path = match.group(2)
            
            # 如果是相对路径，调整为相对于源目录的路径
            if not img_path.startswith(('http://', 'https://')) and not img_path.startswith('/'):
                # 获取文件相对于源目录的路径
                rel_dir = file_path.parent.relative_to(self.source_dir)
                if str(rel_dir) != '.':
                    new_path = f"{rel_dir}/{img_path}".replace('\\', '/')
                else:
                    new_path = img_path
                return f'![{alt_text}]({new_path})'
            
            return match.group(0)
        
        return re.sub(img_pattern, replace_img, line)
    
    def _clean_dirname(self, dirname: str) -> str:
        """清理目录名称"""
        # 移除括号编号
        dirname = re.sub(r'^（\d+）', '', dirname)
        return dirname
    
    def _make_anchor(self, title: str) -> str:
        """生成锚点名称"""
        # 移除特殊字符，保留字母数字和中文
        anchor = re.sub(r'[^\w\u4e00-\u9fa5-]', '-', title)
        # 移除多余的连字符
        anchor = re.sub(r'-+', '-', anchor)
        return anchor.strip('-').lower()


if __name__ == "__main__":
    # 设置源目录和输出文件
    source_directory = "lvyatech_html_docs"
    output_filename = "lvyatech_complete_documentation.md"
    
    # 创建合并器并执行
    merger = MarkdownMerger(source_directory, output_filename)
    merger.merge_all()