# LvyaTech 文档爬虫

这个爬虫用于抓取 LvyaTech 文档网站的所有页面，并保存为本地 MHTML、HTML 或 Markdown 文件。

## 工作原理

1. 通过 API 接口获取网站的完整菜单结构
2. 递归遍历所有页面和目录
3. 使用 Playwright 加载每个页面，等待动态内容渲染完成
4. 根据选择的格式保存内容
5. 按照原网站的目录结构组织文件

## 支持的格式

- **MHTML（默认）**：保存完整的页面，包括 HTML、CSS、JavaScript、图片等所有资源，离线查看效果与在线一致
- **HTML**：仅保存处理后的 HTML 内容，体积小但可能缺少样式和交互功能
- **Markdown**：直接通过 API 获取原始 Markdown 内容，速度快，无需浏览器渲染，自动下载图片到本地

## API 调用说明

- 网站结构 API：`http://www.lvyatech.com:37788/server/index.php?s=/api/item/info`
  - 固定参数：`item_id=39&keyword=&default_page_id=539`
- 页面内容 API（Markdown 格式专用）：`http://www.lvyatech.com:37788/server/index.php?s=/api/page/info`
  - 参数：`page_id={页面ID}`
- 页面 URL 格式：`http://www.lvyatech.com:37788/web/#/{item_id}/{page_id}`

## 安装依赖

```bash
# 使用 uv 安装 Python 依赖
uv pip install playwright requests beautifulsoup4 lxml markdownify aiofiles aiohttp

# 安装 Playwright 浏览器
uv run playwright install chromium
```

## 运行爬虫

```bash
# 默认运行（无头模式，保存为 MHTML）
uv run python lvyatech_scraper.py

# 保存为 HTML 格式（不包含资源文件）
uv run python lvyatech_scraper.py --html

# 保存为 Markdown 格式（下载图片到本地）
uv run python lvyatech_scraper.py --markdown
# 或使用简写
uv run python lvyatech_scraper.py --md

# 调试模式（显示浏览器窗口）
uv run python lvyatech_scraper.py --show-browser

# 组合使用
uv run python lvyatech_scraper.py --show-browser --markdown
```

## 输出结果

爬取的内容将保存在 `lvyatech_html_docs` 目录中：

- 每个页面保存为独立的文件
- 文件名格式：
  - MHTML：`{page_id}_{page_title}.mhtml`
  - HTML：`{page_id}_{page_title}.html`
  - Markdown：`{page_id}_{page_title}.md`
- 每个目录都有 `index.html` 文件，方便浏览
- 主目录的 `index.html` 包含整个文档结构的导航
- Markdown 格式时，所有图片保存在 `images/` 目录中

## 目录结构示例

### MHTML/HTML 格式
```
lvyatech_html_docs/
├── index.html                          # 主索引页
├── site_structure.json                 # 网站结构元数据
├── 539_简介.mhtml                     # 根目录页面
├── 540_版本变更.mhtml
├── 硬件安装/                          # 子目录
│   ├── index.html                     # 目录索引
│   ├── 541_开发板硬件介绍.mhtml
│   └── 542_电源头规格说明.mhtml
└── ...
```

### Markdown 格式
```
lvyatech_html_docs/
├── index.html                          # 主索引页
├── site_structure.json                 # 网站结构元数据
├── images/                             # 所有图片
│   ├── a1b2c3d4_logo.png
│   ├── e5f6g7h8_diagram.jpg
│   └── ...
├── 539_简介.md                        # 根目录页面
├── 540_版本变更.md
├── 硬件安装/                          # 子目录
│   ├── index.html                     # 目录索引
│   ├── 541_开发板硬件介绍.md
│   └── 542_电源头规格说明.md
└── ...
```

## 查看 MHTML 文件

MHTML 文件可以直接在 Chrome、Edge 等现代浏览器中打开，保留完整的页面样式和功能。

## 使用 AI 助手

可以将 `@lvyatech_complete_documentation.md` 文件添加到 Gemini 等 AI 助手中，让 AI 充当绿邮开发板的技术支持专家。

### 推荐提示词

```
作为一名资深的开发专家，你的职责是为用户提供关于绿邮开发板的详细文档、技术支持和开发建议。你的回复应专业、准确且易于理解。如果你不确定某个特定信息，请告知用户并提供寻找相关资源的指导。专注于提供实际的解决方案和代码示例，以帮助用户高效地使用绿邮开发板。保持耐心和乐于助人的态度，即使面对初级用户的问题也要保持专业性。

目的和目标：

* 为用户提供绿邮开发板的全面技术支持，包括硬件规格、软件环境配置和常见问题解答。
* 针对用户的开发需求，提供实际的代码示例和最佳实践，帮助他们高效利用开发板功能。
* 引导用户找到官方文档、社区论坛或其他可靠资源，以获取更深入的信息或解决特定问题。
* 培养用户对绿邮开发板的理解和使用能力，促进其项目成功。

行为和规则：

1. 初始互动：
   a) 询问用户目前遇到的具体问题或希望实现的目标，以便快速理解其需求。
   b) 如果用户问题模糊，请通过提问进一步明确，例如：'您正在使用哪个型号的绿邮开发板？'或'您希望实现什么功能？'

2. 提供支持：
   a) 针对用户的问题，提供准确、清晰且分步的解决方案或建议。
   b) 在可能的情况下，提供可以直接运行或参考的代码片段、配置示例或电路图。
   c) 解释技术概念时，使用易于理解的语言，避免过于复杂的术语。
   d) 如果需要用户提供更多信息（例如错误日志、硬件连接照片），请明确指出并解释原因。
   e) 如果某个问题超出您的知识范围，诚实告知用户，并建议他们去查阅绿邮官方文档、社区论坛或联系官方技术支持。

3. 专业性和耐心：
   a) 始终保持耐心和专业的态度，即使面对重复性问题或初级用户。
   b) 避免使用带有情绪色彩的词语或表达，保持中立和客观。
   c) 鼓励用户提问，并在问题解决后进行确认。
   d) 每轮对话回复不超过三句话，保持简洁高效。

整体语气：

* 专业、权威且值得信赖。
* 乐于助人、耐心且富有同情心。
* 清晰、简洁且注重实效。
```

## 注意事项

1. **格式选择建议**
   - **MHTML**（默认）：需要完整保留页面样式和交互功能时使用
   - **Markdown**：需要编辑文档内容或在 Markdown 编辑器中查看时使用（推荐）
   - **HTML**：只需要基本内容，不需要样式和资源时使用

2. **Markdown 格式特点**
   - **速度快**：直接通过 API 获取原始 Markdown 内容，无需浏览器渲染
   - **无需 Playwright**：不启动浏览器，节省资源
   - **内容纯净**：获取的是原始文档内容，没有导航菜单等干扰
   - 自动下载所有图片到本地 `images/` 目录
   - 图片链接自动修正为相对路径
   - 适合在 Obsidian、Typora 等 Markdown 编辑器中查看
   - 页面元数据保存在文档开头

3. 爬虫会等待页面动态内容加载完成
   - 等待网络空闲
   - 检测内容容器出现
   - 等待图片加载
   - 检测加载指示器消失
   - 智能检测内容是否加载完成（检查文本长度、特殊元素等）

4. 性能相关
   - 每个页面之间有 1 秒延迟，避免请求过快
   - MHTML 格式需要更多时间保存（包含所有资源）
   - Markdown 格式需要额外时间下载图片
   
5. 调试
   - 如果页面没有正确渲染，可以使用 `--show-browser` 参数查看实际加载过程
   - 查看控制台输出了解爬取进度和内容长度