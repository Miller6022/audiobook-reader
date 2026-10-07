# audiobook-reader

带音频精读阅读器 SKILL —— 将书籍/PDF/文本转化为左右两栏布局的交互式HTML精读页面。

## 功能特性

- **左右两栏布局**：左侧书本文字，右侧慢语速朗读音频播放器
- **用户自行高亮**：开启高亮模式后，选中文本即可标注，自动保存
- **章节连续播放**：一个章节多段音频，播完自动连播下一段
- **侧边目录导航**：快速跳转到任意章节
- **预设金句标注**：核心观点高亮，重要金句用引用卡片突出
- **响应式适配**：电脑端左右布局，手机端自动切换上下布局

## 目录结构

```
audiobook-reader/
├── SKILL.md                    # 核心说明文档
├── assets/
│   └── template.html           # HTML阅读页面模板
├── scripts/
│   ├── extract_pdf.py          # PDF文本提取工具
│   └── generate_html.py        # HTML生成工具
├── references/
│   └── workflow.md             # 详细工作流程
└── audiobook-reader-skill.zip  # 打包备份
```

## 使用方法

1. 将此SKILL放置在用户技能目录（`.user_skills/audiobook-reader/`）
2. 向AI发送书籍PDF或文本，并说"做成带音频的书"
3. AI会自动调用此SKILL，生成带音频的HTML精读页面

## 音频说明

由于音频生成工具单次最长2分钟，一个章节会拆分为多个2分钟片段，在HTML中通过自动连续播放实现完整章节体验。

## 许可证

MIT
