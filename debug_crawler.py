import asyncio
from playwright.async_api import async_playwright

async def debug_website():
    """调试网站连接问题"""
    url = "http://www.lvyatech.com:37788/web/#/39/539"
    
    async with async_playwright() as p:
        print("启动浏览器...")
        # 默认使用 Edge 浏览器
        try:
            browser = await p.chromium.launch(channel="msedge", headless=False)
            print("使用 Edge 浏览器")
        except Exception as e:
            print(f"Edge 浏览器启动失败: {e}")
            print("使用 Chromium 浏览器")
            browser = await p.chromium.launch(headless=False)
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
        )
        
        page = await context.new_page()
        
        # 启用请求日志
        page.on("request", lambda request: print(f">> 请求: {request.method} {request.url}"))
        page.on("response", lambda response: print(f"<< 响应: {response.status} {response.url}"))
        page.on("pageerror", lambda error: print(f"!! 页面错误: {error}"))
        
        try:
            print(f"\n尝试访问: {url}")
            
            # 尝试不同的等待策略
            response = await page.goto(url, wait_until='commit', timeout=30000)
            
            if response:
                print(f"\n响应状态: {response.status}")
                print(f"响应头: {response.headers}")
            else:
                print("\n没有收到响应")
                
            print("\n等待用户交互...")
            await page.wait_for_timeout(5000)
            
            # 获取页面内容
            content = await page.content()
            print(f"\n页面内容长度: {len(content)} 字符")
            
            # 保存内容供分析
            with open("debug_output.html", "w", encoding="utf-8") as f:
                f.write(content)
            print("已保存到 debug_output.html")
            
            # 等待用户查看
            input("\n按回车键关闭浏览器...")
            
        except Exception as e:
            print(f"\n错误详情: {type(e).__name__}: {e}")
            input("\n按回车键关闭浏览器...")
            
        await context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_website())