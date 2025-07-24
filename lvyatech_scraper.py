#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import json
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import unquote

import requests
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


class LvyaTechScraper:
    def __init__(self):
        self.base_url = "http://www.lvyatech.com:37788"
        self.api_url = f"{self.base_url}/server/index.php?s=/api/item/info"
        self.web_url = f"{self.base_url}/web/#"
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
        self.output_dir = Path("lvyatech_html_docs")
        self.browser = None
        self.context = None
        self.processed_pages = set()
        self.save_format = "mhtml"  # 可选: "html" 或 "mhtml"

    def sanitize_filename(self, filename: str) -> str:
        """清理文件名，移除不合法的字符"""
        # 移除或替换不合法的文件名字符
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # 移除控制字符
        filename = ''.join(char for char in filename if ord(char) >= 32)
        # 限制长度
        if len(filename) > 100:
            filename = filename[:100]
        return filename.strip()

    def get_api_data(self, page_id: str) -> Dict[str, Any]:
        """通过API获取页面数据"""
        data = {
            'item_id': self.item_id,
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
            print(f"Exception getting API data for page {page_id}: {e}")
            return {}

    async def init_browser(self, headless=True):
        """初始化浏览器"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=headless,
            args=['--disable-blink-features=AutomationControlled']
        )
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent=self.headers['User-Agent']
        )
        
        # 设置cookies
        cookies = []
        for name, value in self.cookies.items():
            cookies.append({
                'name': name,
                'value': value,
                'domain': 'www.lvyatech.com',
                'path': '/'
            })
        await self.context.add_cookies(cookies)

    async def close_browser(self):
        """关闭浏览器"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def get_page_content(self, item_id: str, page_id: str) -> tuple[str, bytes]:
        """获取动态渲染后的页面内容（HTML或MHTML）"""
        # 构建正确的URL格式: http://www.lvyatech.com:37788/web/#/{item_id}/{page_id}
        url = f"{self.web_url}/{item_id}/{page_id}"
        print(f"  Loading page: {url}")
        
        page = await self.context.new_page()
        try:
            # 导航到页面
            await page.goto(url, wait_until='domcontentloaded', timeout=60000)
            
            # 多重等待策略确保页面完全渲染
            # 1. 等待网络空闲
            await page.wait_for_load_state('networkidle')
            
            # 2. 等待可能的内容容器
            content_selectors = [
                '.page-content',
                '.content-wrapper', 
                '.main-content',
                '[class*="content"]',
                '.markdown-body',
                '#content',
                'article',
                'main',
                '.container',
                'pre',  # 代码块
                'table' # 表格
            ]
            
            # 尝试等待任意一个内容选择器
            try:
                await page.wait_for_selector(
                    ', '.join(content_selectors), 
                    state='visible',
                    timeout=10000
                )
            except:
                pass
            
            # 3. 等待特定时间确保JavaScript执行完成
            await page.wait_for_timeout(3000)
            
            # 4. 等待所有图片加载
            await page.evaluate("""
                () => Promise.all(
                    Array.from(document.images)
                        .filter(img => !img.complete)
                        .map(img => new Promise(resolve => {
                            img.onload = img.onerror = resolve;
                        }))
                )
            """)
            
            # 5. 检查是否有动态内容加载指示器
            loading_selectors = [
                '.loading',
                '.spinner',
                '[class*="load"]',
                '.skeleton'
            ]
            
            # 等待加载指示器消失
            for selector in loading_selectors:
                try:
                    await page.wait_for_selector(selector, state='hidden', timeout=5000)
                except:
                    pass
            
            # 6. 最后再等待一下确保所有异步操作完成
            await page.wait_for_timeout(2000)
            
            # 7. 智能等待：检查页面是否有实际内容
            max_wait_time = 15000  # 最多等待15秒
            start_time = asyncio.get_event_loop().time()
            
            while (asyncio.get_event_loop().time() - start_time) * 1000 < max_wait_time:
                # 检查页面是否有实质内容
                content_check = await page.evaluate("""
                    () => {
                        // 获取页面文本内容长度
                        const bodyText = document.body ? document.body.innerText.trim() : '';
                        const hasContent = bodyText.length > 100;
                        
                        // 检查是否有代码块或表格等特殊内容
                        const hasCodeBlocks = document.querySelectorAll('pre, code').length > 0;
                        const hasTables = document.querySelectorAll('table').length > 0;
                        const hasImages = document.querySelectorAll('img').length > 0;
                        
                        // 检查是否还在加载中
                        const loadingElements = document.querySelectorAll('.loading, .spinner, [class*="load"]');
                        const isLoading = Array.from(loadingElements).some(el => 
                            el.offsetParent !== null && window.getComputedStyle(el).display !== 'none'
                        );
                        
                        return {
                            hasContent: hasContent || hasCodeBlocks || hasTables || hasImages,
                            contentLength: bodyText.length,
                            isLoading: isLoading
                        };
                    }
                """)
                
                if content_check['hasContent'] and not content_check['isLoading']:
                    print(f"    Content loaded (length: {content_check['contentLength']} chars)")
                    break
                
                await page.wait_for_timeout(500)
            
            # 根据格式获取内容
            if self.save_format == "mhtml":
                # 使用CDP获取MHTML
                client = await page.context.new_cdp_session(page)
                mhtml_data = await client.send('Page.captureSnapshot', {'format': 'mhtml'})
                mhtml_content = mhtml_data.get('data', '')
                
                # 返回空HTML和MHTML数据
                return "", mhtml_content.encode('utf-8')
            else:
                # 获取渲染后的HTML
                html_content = await page.content()
                
                # 处理相对链接，转换为绝对链接
                soup = BeautifulSoup(html_content, 'lxml')
                
                # 转换所有相对链接
                for tag in soup.find_all(['a', 'link']):
                    if tag.get('href'):
                        href = tag['href']
                        if href.startswith('/') and not href.startswith('//'):
                            tag['href'] = self.base_url + href
                
                for tag in soup.find_all(['img', 'script']):
                    if tag.get('src'):
                        src = tag['src']
                        if src.startswith('/') and not src.startswith('//'):
                            tag['src'] = self.base_url + src
                
                return str(soup), b""
            
        except Exception as e:
            print(f"  Error loading page {url}: {e}")
            error_html = f"<html><body><h1>Error loading page</h1><p>{str(e)}</p></body></html>"
            return error_html, b""
        finally:
            await page.close()

    async def save_page_content(self, page_info: Dict[str, Any], content: tuple[str, bytes], file_path: Path):
        """保存页面内容（HTML或MHTML）"""
        try:
            if self.save_format == "mhtml" and content[1]:
                # 保存MHTML文件
                with open(file_path, 'wb') as f:
                    f.write(content[1])
                print(f"  Saved MHTML: {file_path}")
            else:
                # 保存HTML文件
                html_content = content[0]
                
                # 在HTML中嵌入页面元数据
                soup = BeautifulSoup(html_content, 'lxml')
                
                # 添加元数据到head
                if not soup.head:
                    soup.html.insert(0, soup.new_tag('head'))
                
                # 添加页面信息作为meta标签
                meta_info = {
                    'page-id': page_info.get('page_id', ''),
                    'page-title': page_info.get('page_title', ''),
                    'author-uid': page_info.get('author_uid', ''),
                    'add-time': page_info.get('addtime', ''),
                    'cat-id': page_info.get('cat_id', '')
                }
                
                for name, content_value in meta_info.items():
                    meta_tag = soup.new_tag('meta', attrs={'name': name, 'content': str(content_value)})
                    soup.head.append(meta_tag)
                
                # 保存HTML文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                
                print(f"  Saved HTML: {file_path}")
            
        except Exception as e:
            print(f"  Error saving {file_path}: {e}")

    async def process_page(self, page_info: Dict[str, Any], parent_path: Path, item_id: str = None):
        """处理单个页面"""
        page_id = page_info.get('page_id')
        
        # 避免重复处理
        if page_id in self.processed_pages:
            return
        self.processed_pages.add(page_id)
        
        page_title = page_info.get('page_title', 'Untitled')
        page_title_clean = self.sanitize_filename(page_title)
        
        # 使用传入的item_id或默认的self.item_id
        current_item_id = item_id or self.item_id
        
        print(f"Processing page: {page_title} (Item: {current_item_id}, Page: {page_id})")
        
        # 获取页面内容
        content = await self.get_page_content(current_item_id, page_id)
        
        # 根据格式确定文件扩展名
        file_ext = ".mhtml" if self.save_format == "mhtml" else ".html"
        file_name = f"{page_id}_{page_title_clean}{file_ext}"
        file_path = parent_path / file_name
        
        await self.save_page_content(page_info, content, file_path)
        
        # 延迟避免请求过快
        await asyncio.sleep(1)

    async def process_catalog(self, catalog: Dict[str, Any], parent_path: Path, item_id: str = None):
        """递归处理目录和页面"""
        # 获取目录名称并清理
        cat_name = catalog.get('cat_name', 'Unnamed')
        cat_name_clean = self.sanitize_filename(cat_name)
        cat_path = parent_path / cat_name_clean
        
        # 使用catalog中的item_id或传入的item_id或默认值
        current_item_id = catalog.get('item_id') or item_id or self.item_id
        
        print(f"\nProcessing catalog: {cat_name} (Item: {current_item_id})")
        cat_path.mkdir(parents=True, exist_ok=True)
        
        # 创建目录索引文件
        index_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{cat_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin: 10px 0; }}
        a {{ text-decoration: none; color: #0066cc; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>{cat_name}</h1>
    <ul>
"""
        
        # 处理该目录下的页面
        pages = catalog.get('pages', [])
        for page in pages:
            await self.process_page(page, cat_path, current_item_id)
            # 添加到索引
            page_title = page.get('page_title', 'Untitled')
            page_id = page.get('page_id')
            file_ext = ".mhtml" if self.save_format == "mhtml" else ".html"
            file_name = f"{page_id}_{self.sanitize_filename(page_title)}{file_ext}"
            index_content += f'        <li><a href="{file_name}">{page_title}</a></li>\n'
        
        # 递归处理子目录
        sub_catalogs = catalog.get('catalogs', [])
        if sub_catalogs:
            index_content += '        <li><hr></li>\n'
            index_content += '        <li><strong>子目录:</strong></li>\n'
            
        for sub_catalog in sub_catalogs:
            sub_cat_name = sub_catalog.get('cat_name', 'Unnamed')
            sub_cat_clean = self.sanitize_filename(sub_cat_name)
            index_content += f'        <li>📁 <a href="{sub_cat_clean}/index.html">{sub_cat_name}</a></li>\n'
            await self.process_catalog(sub_catalog, cat_path, current_item_id)
        
        index_content += """    </ul>
</body>
</html>"""
        
        # 保存目录索引
        with open(cat_path / "index.html", 'w', encoding='utf-8') as f:
            f.write(index_content)

    async def scrape_site(self, headless=True, save_format="mhtml"):
        """爬取整个网站"""
        self.save_format = save_format
        print(f"Starting to scrape site with item_id: {self.item_id}")
        print(f"Browser mode: {'Headless' if headless else 'Visible'}")
        print(f"Save format: {self.save_format}")
        
        # 初始化浏览器
        await self.init_browser(headless=headless)
        
        try:
            # 获取网站结构
            site_data = self.get_api_data("539")  # 使用默认页面ID
            
            if not site_data:
                print("Failed to get site structure")
                return
            
            # 创建输出目录
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            # 保存网站元数据
            with open(self.output_dir / 'site_structure.json', 'w', encoding='utf-8') as f:
                json.dump(site_data, f, ensure_ascii=False, indent=2)
            
            menu = site_data.get('menu', {})
            
            # 创建主索引文件
            item_name = site_data.get('item_name', 'Documentation')
            index_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{item_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin: 10px 0; }}
        a {{ text-decoration: none; color: #0066cc; }}
        a:hover {{ text-decoration: underline; }}
        .section {{ margin-top: 30px; }}
    </style>
</head>
<body>
    <h1>{item_name}</h1>
    
    <div class="section">
        <h2>页面列表</h2>
        <ul>
"""
            
            # 处理根目录下的页面
            root_pages = menu.get('pages', [])
            current_item_id = site_data.get('item_id', self.item_id)
            
            for page in root_pages:
                await self.process_page(page, self.output_dir, current_item_id)
                # 添加到主索引
                page_title = page.get('page_title', 'Untitled')
                page_id = page.get('page_id')
                file_ext = ".mhtml" if self.save_format == "mhtml" else ".html"
                file_name = f"{page_id}_{self.sanitize_filename(page_title)}{file_ext}"
                index_content += f'            <li><a href="{file_name}">{page_title}</a></li>\n'
            
            # 处理目录结构
            catalogs = menu.get('catalogs', [])
            if catalogs:
                index_content += """        </ul>
    </div>
    
    <div class="section">
        <h2>目录结构</h2>
        <ul>
"""
            
            for catalog in catalogs:
                cat_name = catalog.get('cat_name', 'Unnamed')
                cat_clean = self.sanitize_filename(cat_name)
                index_content += f'            <li>📁 <a href="{cat_clean}/index.html">{cat_name}</a></li>\n'
                await self.process_catalog(catalog, self.output_dir, current_item_id)
            
            index_content += """        </ul>
    </div>
</body>
</html>"""
            
            # 保存主索引文件
            with open(self.output_dir / "index.html", 'w', encoding='utf-8') as f:
                f.write(index_content)
            
            print(f"\nScraping completed!")
            print(f"All content saved to: {self.output_dir}")
            print(f"Total pages processed: {len(self.processed_pages)}")
            
        finally:
            # 关闭浏览器
            await self.close_browser()


async def main():
    import sys
    
    # 检查命令行参数
    headless = True
    save_format = "mhtml"  # 默认使用MHTML格式
    
    if '--show-browser' in sys.argv:
        headless = False
        print("Running with visible browser for debugging...")
    
    if '--html' in sys.argv:
        save_format = "html"
        print("Using HTML format (without embedded resources)")
    
    scraper = LvyaTechScraper()
    await scraper.scrape_site(headless=headless, save_format=save_format)


if __name__ == "__main__":
    asyncio.run(main())