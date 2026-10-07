# 智能体提示词：创建「带音频精读阅读器」SKILL

> 使用方法：将以下提示词完整复制给任意 AI 智能体（ChatGPT/Claude/ 豆包等），即可生成一个功能完整的 audiobook-reader SKILL。



***

## 提示词正文

你是一位专业的 SKILL 开发者。请创建一个名为 **audiobook-reader** 的 SKILL，用于将书籍 / PDF / 文本转化为带音频的交互式 HTML 精读阅读页面。

### 一、SKILL 核心功能

这个 SKILL 需要实现以下功能：



1. **左右两栏布局**：左侧展示书本文字，右侧放置音频播放器面板（sticky 固定，随滚动保持可见）

2. **慢语速朗读音频**：为每个章节生成温暖沉稳中年男声的慢语速朗读（语速比正常慢 30%），音频按章节分组，播完一段自动连播下一段

3. **用户自行高亮**：用户可开启 "高亮模式"，选中文本后点击浮动工具栏的 "高亮" 按钮进行标注；点击已高亮文字可取消；高亮内容保存在浏览器 localStorage，刷新不丢失

4. **侧边目录导航**：点击 "目录" 按钮滑出侧边栏，点击章节快速跳转

5. **预设金句标注**：书中核心观点用浅黄色高亮标注，重要金句用引用卡片（带引号装饰）突出显示

6. **响应式适配**：电脑端左右布局，手机端自动切换为上下布局

7. **统一书籍风格**：暖色调（米白背景 #faf6f0、陶土橙强调色 #c47a3a）、衬线字体（Noto Serif SC）、舒适的阅读排版

### 二、SKILL 目录结构

请在用户技能目录下创建以下结构：



```
audiobook-reader/
├── SKILL.md                    # 核心说明文档（必需）
├── assets/
│   └── template.html           # HTML阅读页面模板
├── scripts/
│   ├── extract_pdf.py          # PDF文本提取脚本
│   └── generate_html.py        # HTML生成脚本
└── references/
    └── workflow.md             # 详细工作流程文档
```

### 三、各文件详细要求

#### 1. SKILL.md

YAML frontmatter 必须包含：



* `name`: audiobook-reader

* `description`: 详细描述功能和触发场景，包含关键词："带音频的书"" 边听边看 ""听书阅读页面"" 陪我读书 ""把书做成 HTML 加朗读" 等

正文内容需包含：



* 概述：SKILL 做什么

* 使用场景：什么时候触发

* 核心功能表格：列出 7 大功能及说明

* 前置条件：输入要求（PDF / 文本）、工具依赖（text\_to\_audio\_plus、pdf skill）、重要限制（音频单次最长 2 分钟，需拆分为多段连续播放）

* 快速开始：5 步流程（提取文本→划分章节→生成音频→格式化 HTML→生成 HTML→自检交付）

* 详细工作流程指引：指向 references/workflow.md

* 资源文件说明：每个脚本 / 模板 / 参考文档的用途和调用命令

* 输出目录约定：在书籍目录下创建 `<书名>-带音频阅读/` 子目录

#### 2. assets/template.html

这是核心模板，必须是单文件自包含（CSS 内联在`<style>`，JS 内联在`<script>`），包含以下占位符：



* `{{BOOK_TITLE}}` - 书名

* `{{BOOK_SUBTITLE}}` - 副标题

* `{{AUTHOR}}` - 作者

* `{{TRANSLATOR}}` - 译者

* `{{COVER_LABEL}}` - 封面标签（如 "EFFORTLESS・精 读 版"）

* `{{FOOTER_TEXT}}` - 页脚文字

* `{{STORAGE_KEY}}` - localStorage 存储键（每本书不同）

* `{{TOC_ITEMS}}` - 目录项 HTML

* `{{CHAPTERS_HTML}}` - 章节内容 HTML

* `{{AUDIO_DATA}}` - 音频数据 JSON 对象

* `{{CHAPTER_NAMES}}` - 章节名称映射 JSON

模板必须实现的 JavaScript 功能：



* `renderAudioPanels()`: 根据 chapterAudios 对象渲染右侧音频面板

* 音频`ended`事件监听：自动播放同章节下一段

* `toggleHighlightMode()`: 切换高亮模式

* 鼠标`mouseup`事件：选中文本后显示浮动工具栏

* `applyHighlight()`: 应用高亮（创建 span.user-highlight 元素）

* `saveHighlights()` / `loadHighlights()`: localStorage 持久化

* `toggleToc()`: 侧边目录滑入滑出

* IntersectionObserver: 滚动时同步高亮当前章节对应的音频面板

CSS 必须实现的样式类：



* `.highlight` - 预设金句高亮（浅黄背景 #fff3c4）

* `.user-highlight` - 用户高亮（亮黄背景 #ffe066）

* `.quote-card` - 引用卡片（白底 + 边框 + 左上大引号装饰）

* `.key-points` - 要点块（浅橙背景 + 左侧色条）

* `.audio-panel` - 右侧音频面板

* `.highlight-toolbar` - 浮动高亮工具栏

#### 3. scripts/extract\_pdf.py

PDF 文本提取工具，功能：



* 使用 PyMuPDF（fitz）库提取 PDF 文本

* 支持指定起始页 / 结束页

* 输出 JSON 格式：`{"book": "书名", "total_pages": N, "pages": [{"page": 页码, "text": "文本"}]}`

* 命令行参数：`pdf_path`（必需）、`--output`、`--start`、`--end`

* 包含错误处理：文件不存在、PyMuPDF 未安装时给出明确提示

#### 4. scripts/generate\_html.py

HTML 生成工具，功能：



* 读取 JSON 配置文件（包含书籍元数据 + 章节列表）

* 读取 template.html 模板

* 替换所有占位符，生成最终 HTML

* 自动生成目录项（根据章节列表）

* 命令行参数：`--config`（必需）、`--output`（必需）、`--template`（可选，默认使用 skill 内置模板）

配置文件格式：



```
{
  "book_title": "书名",
  "book_subtitle": "副标题",
  "author": "作者",
  "translator": "译者",
  "cover_label": "封面标签",
  "footer_text": "页脚文字",
  "storage_key": "存储键",
  "chapters": [
    {
      "id": "chapter1",
      "num": "CHAPTER 01",
      "title": "章节标题",
      "subtitle": "章节副标题",
      "content_html": "<p>章节HTML内容</p>",
      "audios": [{"label": "第1段", "url": "https://..."}]
    }
  ]
}
```

#### 5. references/workflow.md

详细工作流程文档，包含：



* 整体流程概览（6 步流程图）

* 第一步：内容提取与整理（PDF 提取命令、文本清理规范）

* 第二步：章节划分（划分原则：每章 2000-5000 字、按原书结构、音频分段策略）

* 第三步：音频生成（工具限制说明、prompt 模板："温暖沉稳的中年男性声音，舒缓慢速朗读，像睡前讲故事一样，语速比正常慢 30%，停顿自然，有节奏感。朗读以下内容：<文本>"、每段 400-500 字、duration≤120 秒）

* 第四步：HTML 内容格式化（普通段落`<p>`、金句`<span class="highlight">`、引用卡片`<div class="quote-card">`、要点块`<div class="key-points">`的使用场景和示例）

* 第五步：生成 HTML 文件（配置文件格式、生成命令）

* 第六步：自检与交付（使用 html skill 的 shot.py 自检、检查要点、交付说明模板）

* 常见问题解答（音频时长限制、高亮保存、PDF 质量差等）

### 四、重要约束



1. **音频工具限制**：必须在 SKILL.md 中明确说明 —— 音频生成工具单次最长只能生成 120 秒（2 分钟），因此一个章节需拆分为多个 2 分钟片段，在 HTML 中通过`ended`事件实现自动连续播放，用户体验上等同完整章节音频

2. **单文件自包含**：template.html 必须是单文件，CSS 和 JS 全部内联，不引用外部 JS/CSS 文件（字体除外，可使用 Google Fonts 镜像）

3. **高亮持久化**：用户高亮必须保存在 localStorage，每本书用不同的`storage_key`区分

4. **音频 URL**：音频使用在线 URL（如[aka.doubaocdn.com](https://aka.doubaocdn.com)域名），不嵌入本地音频文件

5. **SKILL.md 的 description 字段**：必须写得足够详细，包含所有触发关键词，确保智能体在用户说 "做成带音频的书"" 陪我读书 ""边听边看" 等时能正确触发这个 SKILL

### 五、输出要求



1. 创建完整的目录结构和所有文件

2. 所有 Python 脚本必须可直接运行（包含`if __name__ == '__main__'`入口）

3. template.html 必须是完整可运行的，用占位符代替实际内容

4. 完成后列出所有创建的文件路径，并简要说明每个文件的用途

5. 给出一个使用示例：如何调用这个 SKILL 将一本书制作成带音频的 HTML



***

## 提示词结束

> 以上提示词可直接复制给任意 AI 智能体使用。生成的 SKILL 放置在用户技能目录后，即可在后续对话中自动触发调用。