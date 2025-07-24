import os
import subprocess
import time

def crawl_with_wget(url, output_dir="static_html_wget"):
    """使用 wget 爬取网站"""
    os.makedirs(output_dir, exist_ok=True)
    
    # wget 参数说明：
    # -r: 递归下载
    # -l 2: 递归深度为2层
    # -k: 转换链接为本地链接
    # -p: 下载页面所需的所有资源
    # -E: 给HTML文件添加.html扩展名
    # --no-parent: 不爬取父目录
    # --random-wait: 随机等待时间
    # --user-agent: 设置用户代理
    
    cmd = [
        "wget",
        "-r",  # 递归下载
        "-l", "2",  # 递归深度
        "-k",  # 转换链接
        "-p",  # 下载所有资源
        "-E",  # 添加.html扩展名
        "--no-parent",  # 不爬取父目录
        "--random-wait",  # 随机等待
        "--wait=2",  # 等待2秒
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "--header=Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "--header=Accept-Language: zh-CN,zh;q=0.9,en;q=0.8",
        "--header=Accept-Encoding: gzip, deflate",
        "--header=Cache-Control: no-cache",
        "--header=Pragma: no-cache",
        "-P", output_dir,  # 输出目录
        "--timeout=30",  # 超时时间
        "--tries=3",  # 重试次数
        url
    ]
    
    print(f"开始使用 wget 爬取: {url}")
    print(f"输出目录: {output_dir}")
    print("命令:", " ".join(cmd))
    
    try:
        subprocess.run(cmd, check=True)
        print("爬取完成！")
    except subprocess.CalledProcessError as e:
        print(f"爬取失败: {e}")
    except FileNotFoundError:
        print("错误: 未找到 wget 命令，请先安装 wget")

if __name__ == "__main__":
    url = "http://www.lvyatech.com:37788/web/"
    crawl_with_wget(url)