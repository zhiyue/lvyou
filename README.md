# LvyaTech 文档爬虫

这个爬虫用于抓取 LvyaTech 文档网站的所有页面，并保存为本地 MHTML 或 HTML 文件。

## 工作原理

1. 通过 API 接口获取网站的完整菜单结构
2. 递归遍历所有页面和目录
3. 使用 Playwright 加载每个页面，等待动态内容渲染完成
4. 保存为 MHTML 格式（包含所有资源）或 HTML 格式
5. 按照原网站的目录结构组织文件

## MHTML vs HTML 格式

- **MHTML（默认）**：保存完整的页面，包括 HTML、CSS、JavaScript、图片等所有资源，离线查看效果与在线一致
- **HTML**：仅保存处理后的 HTML 内容，体积小但可能缺少样式和交互功能

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
# 默认运行（无头模式，保存为 MHTML）
uv run python lvyatech_scraper.py

# 保存为 HTML 格式（不包含资源文件）
uv run python lvyatech_scraper.py --html

# 调试模式（显示浏览器窗口）
uv run python lvyatech_scraper.py --show-browser

# 组合使用
uv run python lvyatech_scraper.py --show-browser --html
```

## 输出结果

爬取的内容将保存在 `lvyatech_html_docs` 目录中：

- 每个页面保存为独立的 MHTML 或 HTML 文件
- 文件名格式：
  - MHTML：`{page_id}_{page_title}.mhtml`
  - HTML：`{page_id}_{page_title}.html`
- 每个目录都有 `index.html` 文件，方便浏览
- 主目录的 `index.html` 包含整个文档结构的导航

## 目录结构示例

```
lvyatech_html_docs/
├── index.html                          # 主索引页
├── site_structure.json                 # 网站结构元数据
├── 539_简介.mhtml                     # 根目录页面（MHTML格式）
├── 540_版本变更.mhtml
├── 硬件安装/                          # 子目录
│   ├── index.html                     # 目录索引
│   ├── 541_开发板硬件介绍.mhtml
│   └── 542_电源头规格说明.mhtml
└── ...
```

## 查看 MHTML 文件

MHTML 文件可以直接在 Chrome、Edge 等现代浏览器中打开，保留完整的页面样式和功能。

## 注意事项

1. **推荐使用 MHTML 格式**（默认）
   - 保存所有资源（CSS、JavaScript、图片、字体等）
   - 离线查看效果与在线完全一致
   - 文件体积较大但完整性好

2. 爬虫会等待页面动态内容加载完成
   - 等待网络空闲
   - 检测内容容器出现
   - 等待图片加载
   - 检测加载指示器消失
   - 智能检测内容是否加载完成（检查文本长度、特殊元素等）

3. 性能相关
   - 每个页面之间有 1 秒延迟，避免请求过快
   - MHTML 格式需要更多时间保存（包含所有资源）
   
4. 调试
   - 如果页面没有正确渲染，可以使用 `--show-browser` 参数查看实际加载过程
   - 查看控制台输出了解爬取进度和内容长度