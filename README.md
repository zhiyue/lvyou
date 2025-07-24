# LvyaTech 文档爬虫

这个爬虫用于抓取 LvyaTech 文档网站的所有页面，并保存为本地 HTML 文件。

## 工作原理

1. 通过 API 接口获取网站的完整菜单结构
2. 递归遍历所有页面和目录
3. 使用 Playwright 加载每个页面，等待动态内容渲染完成
4. 保存渲染后的完整 HTML 内容
5. 按照原网站的目录结构组织文件

## API 调用说明

- API 端点：`http://www.lvyatech.com:37788/server/index.php?s=/api/item/info`
- 固定参数：`item_id=39&keyword=&default_page_id=539`
- 页面 URL 格式：`http://www.lvyatech.com:37788/web/#/{item_id}/{page_id}`

## 安装依赖

```bash
# 使用 uv 安装 Python 依赖
uv pip install playwright requests beautifulsoup4 lxml

# 安装 Playwright 浏览器
uv run playwright install chromium
```

## 运行爬虫

```bash
# 正常运行（无头模式）
uv run python lvyatech_scraper.py

# 调试模式（显示浏览器窗口）
uv run python lvyatech_scraper.py --show-browser
```

## 输出结果

爬取的内容将保存在 `lvyatech_html_docs` 目录中：

- 每个页面保存为独立的 HTML 文件
- 文件名格式：`{page_id}_{page_title}.html`
- 每个目录都有 `index.html` 文件，方便浏览
- 主目录的 `index.html` 包含整个文档结构的导航

## 目录结构示例

```
lvyatech_html_docs/
├── index.html                          # 主索引页
├── site_structure.json                 # 网站结构元数据
├── 539_简介.html                      # 根目录页面
├── 540_版本变更.html
├── 硬件安装/                          # 子目录
│   ├── index.html                     # 目录索引
│   ├── 541_开发板硬件介绍.html
│   └── 542_电源头规格说明.html
└── ...
```

## 注意事项

1. 爬虫会等待页面动态内容加载完成
   - 等待网络空闲
   - 检测内容容器出现
   - 等待图片加载
   - 检测加载指示器消失
   - 智能检测内容是否加载完成（检查文本长度、特殊元素等）
2. 每个页面之间有 1 秒延迟，避免请求过快
3. 所有相对链接都会转换为绝对链接
4. 页面元数据（ID、标题、作者等）保存在 HTML 的 meta 标签中
5. 如果页面没有正确渲染，可以使用 `--show-browser` 参数查看实际加载过程