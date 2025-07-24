import asyncio
import os
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import hashlib

class WebCrawler:
    def __init__(self, base_url, output_dir="static_html"):
        self.base_url = base_url
        self.output_dir = output_dir
        self.visited_urls = set()
        self.to_visit = [base_url]
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
    async def crawl(self):
        async with async_playwright() as p:
            # 尝试使用 Edge 浏览器
            browser_args = [
                '--disable-blink-features=AutomationControlled',
                '--disable-features=site-per-process',
                '--no-sandbox',
                '--disable-setuid-sandbox'
            ]
            
            # 默认使用 Edge 浏览器
            print("使用 Edge 浏览器...")
            try:
                browser = await p.chromium.launch(
                    channel="msedge", 
                    headless=False,
                    args=browser_args
                )
            except Exception as e:
                print(f"Edge 浏览器启动失败: {e}")
                print("尝试使用 Chromium 浏览器...")
                browser = await p.chromium.launch(
                    headless=False,
                    args=browser_args
                )
            
            # 创建页面并设置视口和用户代理
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
            )
            page = await context.new_page()
            
            # 添加额外的请求头
            await page.set_extra_http_headers({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            })
            
            while self.to_visit:
                url = self.to_visit.pop(0)
                
                if url in self.visited_urls:
                    continue
                    
                print(f"正在爬取: {url}")
                
                try:
                    # 访问页面，增加超时时间和重试
                    await page.goto(url, wait_until='domcontentloaded', timeout=60000)
                    
                    # 等待页面加载完成
                    await page.wait_for_timeout(5000)
                    
                    # 获取页面HTML
                    html_content = await page.content()
                    
                    # 保存HTML
                    self.save_html(url, html_content)
                    
                    # 标记已访问
                    self.visited_urls.add(url)
                    
                    # 提取新链接
                    links = await self.extract_links(page, url)
                    for link in links:
                        if link not in self.visited_urls and link not in self.to_visit:
                            self.to_visit.append(link)
                            
                except Exception as e:
                    print(f"爬取 {url} 时出错: {e}")
                    
            await context.close()
            await browser.close()
            
    async def extract_links(self, page, current_url):
        """提取页面中的链接"""
        links = await page.evaluate('''() => {
            const links = [];
            const anchors = document.querySelectorAll('a[href]');
            anchors.forEach(a => {
                links.push(a.href);
            });
            return links;
        }''')
        
        # 过滤和规范化链接
        valid_links = []
        for link in links:
            # 转换为绝对URL
            absolute_url = urljoin(current_url, link)
            
            # 只保留同域名下的链接
            if urlparse(absolute_url).netloc == urlparse(self.base_url).netloc:
                valid_links.append(absolute_url)
                
        return valid_links
        
    def save_html(self, url, html_content):
        """保存HTML到文件"""
        # 生成文件名
        parsed_url = urlparse(url)
        path = parsed_url.path
        
        if path == '/' or path == '':
            filename = 'index.html'
        else:
            # 使用URL的hash作为文件名，避免特殊字符问题
            filename = hashlib.md5(url.encode()).hexdigest() + '.html'
            
        filepath = os.path.join(self.output_dir, filename)
        
        # 处理HTML内容，使其可以本地查看
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 添加base标签，确保资源加载正确
        base_tag = soup.find('base')
        if not base_tag:
            base_tag = soup.new_tag('base', href=self.base_url)
            if soup.head:
                soup.head.insert(0, base_tag)
                
        # 保存处理后的HTML
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
            
        print(f"已保存: {filepath}")
        
        # 保存URL映射
        with open(os.path.join(self.output_dir, 'url_map.txt'), 'a', encoding='utf-8') as f:
            f.write(f"{url} -> {filename}\n")

async def main():
    url = "http://www.lvyatech.com:37788/web/#/39/539"
    print(f"目标网站: {url}")
    print("默认使用 Microsoft Edge 浏览器")
    print("-" * 50)
    
    crawler = WebCrawler(url)
    await crawler.crawl()
    print("\n爬取完成！")

if __name__ == "__main__":
    asyncio.run(main())