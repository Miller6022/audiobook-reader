#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF文本提取脚本 - 用于带音频精读阅读器
从PDF文件中提取文本内容，输出为JSON格式，便于后续按章节划分和生成HTML。

用法:
    python extract_pdf.py <pdf_path> [--output <output_json>] [--start <start_page>] [--end <end_page>]

参数:
    pdf_path: PDF文件路径
    --output: 输出JSON文件路径（默认：同目录下 <pdf名>_content.json）
    --start: 起始页码（默认：1）
    --end: 结束页码（默认：最后一页）

输出:
    JSON文件，包含每页的文本内容：
    {
        "book": "书名",
        "total_pages": 总页数,
        "pages": [
            {"page": 页码, "text": "文本内容"},
            ...
        ]
    }
"""

import argparse
import json
import os
import sys


def extract_pdf_text(pdf_path, start_page=1, end_page=None):
    """
    从PDF中提取文本内容

    Args:
        pdf_path: PDF文件路径
        start_page: 起始页码（从1开始）
        end_page: 结束页码（None表示到最后一页）

    Returns:
        dict: 包含书名、总页数、每页文本的字典
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("错误：需要安装 PyMuPDF 库")
        print("请运行：pip install pymupdf")
        sys.exit(1)

    if not os.path.exists(pdf_path):
        print(f"错误：文件不存在 - {pdf_path}")
        sys.exit(1)

    doc = fitz.open(pdf_path)
    total_pages = len(doc)

    if end_page is None or end_page > total_pages:
        end_page = total_pages

    if start_page < 1:
        start_page = 1

    book_name = os.path.splitext(os.path.basename(pdf_path))[0]
    pages = []

    print(f"正在提取PDF文本：{book_name}")
    print(f"总页数：{total_pages}，提取范围：第{start_page}-{end_page}页")

    for page_num in range(start_page - 1, end_page):
        page = doc[page_num]
        text = page.get_text()
        # 清理多余空白
        text = text.strip()
        pages.append({
            "page": page_num + 1,
            "text": text
        })
        if (page_num + 1) % 10 == 0:
            print(f"  已提取 {page_num + 1 - start_page + 1}/{end_page - start_page + 1} 页...")

    doc.close()

    result = {
        "book": book_name,
        "total_pages": total_pages,
        "extracted_pages": len(pages),
        "pages": pages
    }

    return result


def main():
    parser = argparse.ArgumentParser(description='PDF文本提取工具 - 带音频精读阅读器')
    parser.add_argument('pdf_path', help='PDF文件路径')
    parser.add_argument('--output', '-o', help='输出JSON文件路径')
    parser.add_argument('--start', type=int, default=1, help='起始页码（默认：1）')
    parser.add_argument('--end', type=int, help='结束页码（默认：最后一页）')

    args = parser.parse_args()

    # 提取文本
    result = extract_pdf_text(args.pdf_path, args.start, args.end)

    # 确定输出路径
    if args.output:
        output_path = args.output
    else:
        pdf_dir = os.path.dirname(os.path.abspath(args.pdf_path))
        pdf_name = os.path.splitext(os.path.basename(args.pdf_path))[0]
        output_path = os.path.join(pdf_dir, f"{pdf_name}_content.json")

    # 写入JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n提取完成！")
    print(f"输出文件：{output_path}")
    print(f"提取页数：{result['extracted_pages']}")
    print(f"总字符数：{sum(len(p['text']) for p in result['pages'])}")


if __name__ == '__main__':
    main()
