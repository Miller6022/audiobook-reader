#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML生成脚本 - 带音频精读阅读器
根据模板和章节数据生成最终的HTML阅读文件。

用法:
    python generate_html.py --config <config_json> --output <output_html>

配置文件格式 (JSON):
{
    "book_title": "书名",
    "book_subtitle": "副标题",
    "author": "作者",
    "translator": "译者",
    "cover_label": "封面标签（如：EFFORTLESS · 精 读 版）",
    "footer_text": "页脚文字",
    "storage_key": "localStorage存储键（如：effortless）",
    "chapters": [
        {
            "id": "chapter1",
            "num": "CHAPTER 01",
            "title": "章节标题",
            "subtitle": "章节副标题",
            "content_html": "<p>章节HTML内容...</p>",
            "audios": [
                {"label": "第1段（慢语速）", "url": "https://..."},
                {"label": "第2段（慢语速）", "url": "https://..."}
            ]
        }
    ]
}
"""

import argparse
import json
import os
import sys


def generate_html(config, template_path):
    """
    根据配置和模板生成HTML内容

    Args:
        config: 配置字典
        template_path: 模板文件路径

    Returns:
        str: 生成的HTML内容
    """
    # 读取模板
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # 生成目录项
    toc_items = ''
    for i, ch in enumerate(config['chapters']):
        num_str = f"{i:02d}"
        toc_items += f'<a href="#{ch["id"]}"><span class="num">{num_str}</span>{ch["title"]}</a>\n  '

    # 生成章节HTML
    chapters_html = ''
    for ch in config['chapters']:
        chapters_html += f'''    <div class="chapter" id="{ch['id']}">
      <div class="chapter-header">
        <div class="chapter-num">{ch['num']}</div>
        <div class="chapter-title">{ch['title']}</div>
        <div class="chapter-subtitle">{ch['subtitle']}</div>
      </div>
      <div class="chapter-content">
        {ch['content_html']}
      </div>
    </div>

'''

    # 生成音频数据JSON
    audio_data = {}
    chapter_names = {}
    for ch in config['chapters']:
        audio_data[ch['id']] = ch.get('audios', [])
        chapter_names[ch['id']] = ch['title']

    audio_data_json = json.dumps(audio_data, ensure_ascii=False, indent=2)
    chapter_names_json = json.dumps(chapter_names, ensure_ascii=False, indent=2)

    # 替换模板占位符
    html = template
    html = html.replace('{{BOOK_TITLE}}', config.get('book_title', ''))
    html = html.replace('{{BOOK_SUBTITLE}}', config.get('book_subtitle', ''))
    html = html.replace('{{AUTHOR}}', config.get('author', ''))
    html = html.replace('{{TRANSLATOR}}', config.get('translator', ''))
    html = html.replace('{{COVER_LABEL}}', config.get('cover_label', ''))
    html = html.replace('{{FOOTER_TEXT}}', config.get('footer_text', ''))
    html = html.replace('{{STORAGE_KEY}}', config.get('storage_key', 'default'))
    html = html.replace('{{TOC_ITEMS}}', toc_items)
    html = html.replace('{{CHAPTERS_HTML}}', chapters_html)
    html = html.replace('{{AUDIO_DATA}}', audio_data_json)
    html = html.replace('{{CHAPTER_NAMES}}', chapter_names_json)

    return html


def main():
    parser = argparse.ArgumentParser(description='HTML生成工具 - 带音频精读阅读器')
    parser.add_argument('--config', '-c', required=True, help='配置JSON文件路径')
    parser.add_argument('--output', '-o', required=True, help='输出HTML文件路径')
    parser.add_argument('--template', '-t', help='模板文件路径（默认使用skill内置模板）')

    args = parser.parse_args()

    # 读取配置
    if not os.path.exists(args.config):
        print(f"错误：配置文件不存在 - {args.config}")
        sys.exit(1)

    with open(args.config, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # 确定模板路径
    if args.template:
        template_path = args.template
    else:
        # 默认使用skill内置模板
        script_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(script_dir, '..', 'assets', 'template.html')

    if not os.path.exists(template_path):
        print(f"错误：模板文件不存在 - {template_path}")
        sys.exit(1)

    # 生成HTML
    print(f"正在生成HTML...")
    print(f"  书籍：{config.get('book_title', '')}")
    print(f"  章节数：{len(config.get('chapters', []))}")

    html = generate_html(config, template_path)

    # 写入文件
    output_dir = os.path.dirname(os.path.abspath(args.output))
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n生成完成！")
    print(f"输出文件：{args.output}")
    print(f"文件大小：{os.path.getsize(args.output) / 1024:.1f} KB")


if __name__ == '__main__':
    main()
