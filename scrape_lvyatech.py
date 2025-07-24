#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import os
import time
import re
from typing import Dict, List, Any
from urllib.parse import unquote

class LvyaTechScraper:
    def __init__(self):
        self.base_url = "http://www.lvyatech.com:37788"
        self.api_url = f"{self.base_url}/server/index.php?s=/api/item/info"
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en,zh;q=0.9,zh-CN;q=0.8,zh-HK;q=0.7,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': self.base_url,
            'Pragma': 'no-cache',
            'Referer': f'{self.base_url}/web/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
        }
        self.cookies = {
            'cookie_name': 'value',
            'think_language': 'en',
            'PHPSESSID': '7o9vc6er8cjrdioi2reea1ob37'
        }
        self.item_id = "39"
        self.output_dir = "lvyatech_docs"
        
    def get_page_content(self, item_id: str, page_id: str) -> Dict[str, Any]:
        """获取单个页面的内容"""
        data = {
            'item_id': item_id,
            'keyword': '',
            'default_page_id': page_id
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                cookies=self.cookies,
                data=data,
                verify=False
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get('error_code') == 0:
                return result.get('data', {})
            else:
                print(f"Error getting page {page_id}: {result}")
                return {}
                
        except Exception as e:
            print(f"Exception getting page {page_id}: {e}")
            return {}
    
    def sanitize_filename(self, filename: str) -> str:
        """清理文件名，移除不合法的字符"""
        # 移除或替换不合法的文件名字符
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # 移除控制字符
        filename = ''.join(char for char in filename if ord(char) >= 32)
        # 限制长度
        if len(filename) > 200:
            filename = filename[:200]
        return filename.strip()
    
    def create_directory_structure(self, path: str):
        """创建目录结构"""
        if not os.path.exists(path):
            os.makedirs(path)
    
    def save_page_content(self, page_data: Dict[str, Any], file_path: str):
        """保存页面内容到文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                # 写入页面标题
                f.write(f"# {page_data.get('page_title', 'Untitled')}\n\n")
                
                # 写入页面内容
                page_content = page_data.get('page_content', '')
                if page_content:
                    # 解码Unicode转义字符
                    page_content = page_content.encode().decode('unicode_escape')
                    f.write(page_content)
                else:
                    f.write("(No content available)\n")
                    
                # 写入元数据
                f.write(f"\n\n---\n")
                f.write(f"Page ID: {page_data.get('page_id', 'N/A')}\n")
                f.write(f"Author UID: {page_data.get('author_uid', 'N/A')}\n")
                f.write(f"Add Time: {page_data.get('addtime', 'N/A')}\n")
                
            print(f"Saved: {file_path}")
            
        except Exception as e:
            print(f"Error saving {file_path}: {e}")
    
    def process_catalog(self, catalog: Dict[str, Any], parent_path: str, level: int = 0):
        """递归处理目录和页面"""
        indent = "  " * level
        
        # 获取目录名称并清理
        cat_name = catalog.get('cat_name', 'Unnamed')
        cat_name_clean = self.sanitize_filename(cat_name)
        cat_path = os.path.join(parent_path, cat_name_clean)
        
        print(f"{indent}Processing catalog: {cat_name}")
        self.create_directory_structure(cat_path)
        
        # 处理该目录下的页面
        pages = catalog.get('pages', [])
        for page in pages:
            self.process_page(page, cat_path, level + 1)
            time.sleep(0.5)  # 避免请求过快
        
        # 递归处理子目录
        sub_catalogs = catalog.get('catalogs', [])
        for sub_catalog in sub_catalogs:
            self.process_catalog(sub_catalog, cat_path, level + 1)
    
    def process_page(self, page_info: Dict[str, Any], parent_path: str, level: int = 0):
        """处理单个页面"""
        indent = "  " * level
        page_id = page_info.get('page_id')
        page_title = page_info.get('page_title', 'Untitled')
        page_title_clean = self.sanitize_filename(page_title)
        
        print(f"{indent}Getting page: {page_title} (ID: {page_id})")
        
        # 获取页面详细内容
        page_data = self.get_page_content(self.item_id, page_id)
        
        if page_data:
            # 保存为markdown文件
            file_name = f"{page_id}_{page_title_clean}.md"
            file_path = os.path.join(parent_path, file_name)
            
            # 将页面信息合并到数据中
            page_data.update(page_info)
            self.save_page_content(page_data, file_path)
    
    def scrape_site(self):
        """爬取整个网站"""
        print(f"Starting to scrape site with item_id: {self.item_id}")
        
        # 获取网站结构
        site_data = self.get_page_content(self.item_id, "539")  # 使用默认页面ID
        
        if not site_data:
            print("Failed to get site structure")
            return
        
        # 创建输出目录
        self.create_directory_structure(self.output_dir)
        
        # 保存网站元数据
        with open(os.path.join(self.output_dir, 'site_info.json'), 'w', encoding='utf-8') as f:
            json.dump(site_data, f, ensure_ascii=False, indent=2)
        
        menu = site_data.get('menu', {})
        
        # 处理根目录下的页面
        root_pages = menu.get('pages', [])
        for page in root_pages:
            self.process_page(page, self.output_dir, 0)
            time.sleep(0.5)
        
        # 处理目录结构
        catalogs = menu.get('catalogs', [])
        for catalog in catalogs:
            self.process_catalog(catalog, self.output_dir, 0)
        
        print("\nScraping completed!")
        print(f"All content saved to: {self.output_dir}")

if __name__ == "__main__":
    scraper = LvyaTechScraper()
    scraper.scrape_site()