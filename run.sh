#!/bin/bash

echo "选择爬虫方式："
echo "1. Playwright (支持JavaScript渲染)"
echo "2. wget (简单快速)"
read -p "请输入选择 (1/2): " choice

if [ "$choice" = "2" ]; then
    echo "使用 wget 爬取..."
    python wget_crawler.py
else
    # 使用uv创建虚拟环境
    echo "创建虚拟环境..."
    uv venv

    # 激活虚拟环境
    source .venv/bin/activate

    # 使用uv安装依赖
    echo "安装依赖..."
    uv pip install -r requirements.txt

    # 检查并安装Playwright浏览器
    echo "检查Playwright浏览器..."
    
    # 创建检查脚本
    cat > check_browsers.py << 'EOF'
import subprocess
import sys

def check_browser(browser_name):
    try:
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "--dry-run", browser_name],
            capture_output=True,
            text=True
        )
        # 如果输出包含 "already installed"，说明已安装
        return "already installed" in result.stdout.lower()
    except:
        return False

# 检查chromium
if not check_browser("chromium"):
    print("INSTALL_CHROMIUM")
    
# 检查msedge
if not check_browser("msedge"):
    print("INSTALL_MSEDGE")
EOF
    
    # 运行检查脚本
    INSTALL_BROWSERS=$(python check_browsers.py)
    
    # 根据检查结果安装浏览器
    # 优先安装 Edge 浏览器
    if echo "$INSTALL_BROWSERS" | grep -q "INSTALL_MSEDGE"; then
        echo "安装Edge浏览器..."
        python -m playwright install msedge
    else
        echo "Edge浏览器已安装"
    fi
    
    # Chromium 作为备用
    if echo "$INSTALL_BROWSERS" | grep -q "INSTALL_CHROMIUM"; then
        echo "安装Chromium浏览器（备用）..."
        python -m playwright install chromium
    else
        echo "Chromium浏览器已安装"
    fi
    
    # 清理临时文件
    rm -f check_browsers.py

    # 运行爬虫
    echo "开始爬取..."
    python crawler.py
fi