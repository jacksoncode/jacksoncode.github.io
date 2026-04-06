#!/usr/bin/env python3
"""Scrape tutorials from liaoxuefeng.com and Anthropic Academy, convert to markdown/HTML."""

import json
import os
import re
import ssl
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urljoin

BASE_URL = "https://liaoxuefeng.com"
TUTORIALS_DIR = Path("tutorials")

ssl._create_default_https_context = ssl._create_unverified_context


# Common header template matching site style
def make_header(title, depth=1):
    pfx = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="CodeClub - {title}">
    <meta name="author" content="Jackson">
    <title>{title} - CodeClub</title>
    <link rel="icon" type="image/x-icon" href="{pfx}img/logo.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <link rel="stylesheet" href="{pfx}css/main.css">
    <link rel="stylesheet" href="{pfx}css/dark-mode.css">
    <link rel="stylesheet" href="{pfx}css/mobile-optimizations.css">
    <link rel="stylesheet" href="{pfx}css/tutorial.css">
    <style>
    .tutorial-container {{ max-width: 960px; margin: 70px auto 40px; padding: 0 20px; }}
    .tutorial-sidebar {{ position: fixed; top: 70px; left: 20px; width: 260px; max-height: calc(100vh - 90px); overflow-y: auto; background: var(--bg-secondary, #fff); border-radius: 8px; padding: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
    .tutorial-sidebar h3 {{ font-size: 16px; margin-bottom: 12px; color: var(--text-primary, #1a1a2e); }}
    .tutorial-sidebar a {{ display: block; padding: 6px 10px; color: var(--text-secondary, #666); text-decoration: none; font-size: 14px; border-radius: 4px; }}
    .tutorial-sidebar a:hover, .tutorial-sidebar a.active {{ background: var(--primary, #3b82f6); color: #fff; }}
    .tutorial-sidebar .sub-link {{ padding-left: 24px; font-size: 13px; }}
    .tutorial-content {{ margin-left: 300px; background: var(--bg-secondary, #fff); border-radius: 8px; padding: 32px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
    .tutorial-content h1 {{ font-size: 28px; margin-bottom: 20px; color: var(--text-primary, #1a1a2e); border-bottom: 2px solid var(--primary, #3b82f6); padding-bottom: 12px; }}
    .tutorial-content h2 {{ font-size: 22px; margin: 24px 0 16px; color: var(--text-primary, #1a1a2e); }}
    .tutorial-content h3 {{ font-size: 18px; margin: 20px 0 12px; }}
    .tutorial-content p {{ line-height: 1.8; margin: 12px 0; color: var(--text-secondary, #333); }}
    .tutorial-content pre {{ background: #1e1e2e; color: #cdd6f4; padding: 16px; border-radius: 8px; overflow-x: auto; margin: 16px 0; }}
    .tutorial-content code {{ font-family: 'Fira Code', 'Cascadia Code', monospace; font-size: 14px; }}
    .tutorial-content p code {{ background: #f1f5f9; padding: 2px 6px; border-radius: 4px; color: #e83e8c; }}
    .tutorial-content blockquote {{ border-left: 4px solid var(--primary, #3b82f6); padding: 12px 20px; margin: 16px 0; background: #f8fafc; border-radius: 0 8px 8px 0; }}
    .tutorial-content ul, .tutorial-content ol {{ padding-left: 24px; margin: 12px 0; }}
    .tutorial-content li {{ margin: 6px 0; line-height: 1.7; }}
    .tutorial-content img {{ max-width: 100%; border-radius: 8px; margin: 16px 0; }}
    .tutorial-nav {{ display: flex; justify-content: space-between; margin-top: 32px; padding-top: 20px; border-top: 1px solid var(--border, #e5e7eb); }}
    .tutorial-nav a {{ color: var(--primary, #3b82f6); text-decoration: none; font-weight: 500; }}
    .tutorial-nav a:hover {{ text-decoration: underline; }}
    .tutorial-index {{ max-width: 960px; margin: 70px auto 40px; padding: 0 20px; }}
    .tutorial-card {{ background: var(--bg-secondary, #fff); border-radius: 12px; padding: 24px; margin: 16px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: transform 0.2s; }}
    .tutorial-card:hover {{ transform: translateY(-2px); }}
    .tutorial-card h3 {{ margin: 0 0 8px; color: var(--text-primary, #1a1a2e); }}
    .tutorial-card p {{ color: var(--text-secondary, #666); margin: 0 0 12px; }}
    .tutorial-card .badge {{ display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; margin-right: 8px; }}
    .badge-python {{ background: #3b82f6; color: #fff; }}
    .badge-git {{ background: #f97316; color: #fff; }}
    .badge-ai {{ background: #8b5cf6; color: #fff; }}
    @media (max-width: 768px) {{
        .tutorial-sidebar {{ display: none; }}
        .tutorial-content {{ margin-left: 0; }}
    }}
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="navbar-container">
            <a class="navbar-brand" href="{pfx}index.html">
                <img src="{pfx}img/logo.png" alt="CodeClub" width="32" height="32">
                <span>CodeClub</span>
            </a>
            <button class="mobile-menu-toggle" aria-label="切换导航菜单">
                <span></span><span></span><span></span>
            </button>
            <ul class="navbar-nav">
                <li><a class="nav-link" href="{pfx}index.html">首页</a></li>
                <li><a class="nav-link" href="{pfx}nav.html">网址导航</a></li>
                <li><a class="nav-link" href="{pfx}blog/">博客</a></li>
                <li><a class="nav-link" href="{pfx}wiki/index.html" target="_blank">WiKi</a></li>
                <li><a class="nav-link active" href="{pfx}tutorials/index.html">教程</a></li>
                <li><a class="nav-link" href="{pfx}book.html">图书</a></li>
                <li><a class="nav-link" href="{pfx}contact.html">联系我</a></li>
                <li><a class="nav-link" href="{pfx}about.html">关于我</a></li>
            </ul>
        </div>
    </nav>
"""


def make_footer(depth=1):
    pfx = "../" * depth
    return f"""
    <footer class="footer">
        <div class="footer-content">
            <p>&copy; 2024 CodeClub. All rights reserved.</p>
        </div>
    </footer>
    <script src="{pfx}js/dark-mode.js"></script>
    <script src="{pfx}js/mobile-menu.js"></script>
</body>
</html>"""



class LiaoxuefengParser(HTMLParser):
    """Extract tutorial content from liaoxuefeng.com HTML."""

    def __init__(self):
        super().__init__()
        self.in_content = False
        self.in_toc = False
        self.in_nav = False
        self.in_header = False
        self.in_footer = False
        self.in_comment = False
        self.current_tag = None
        self.content_parts = []
        self.toc_items = []
        self.title = ""
        self.in_title = False
        self.title_buf = ""
        self.skip_depth = 0
        self.attrs_stack = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self.attrs_stack.append(attrs_dict)

        if self.skip_depth > 0:
            self.skip_depth += 1
            return

        cls = attrs_dict.get("class", "") or ""

        if (
            tag in ("nav",)
            or "navbar" in cls
            or "footer" in cls
            or "comment" in cls.lower()
        ):
            self.skip_depth = 1
            return

        if tag == "h1" and not self.in_content:
            self.in_title = True
            self.title_buf = ""
            self.skip_depth = 1
            return

        # Main content area
        if cls and (
            "x-content" in cls or "content" in cls or "tutorial-content" in cls
        ):
            self.in_content = True
            return

        # Table of contents
        if cls and ("toc" in cls or "sidebar" in cls or "menu" in cls):
            if "x-toc" in cls or "toc" in cls:
                self.in_toc = True
                return

        if self.in_content:
            self.content_parts.append(f"<{tag}")
            for k, v in attrs:
                if k in ("class", "id", "href", "src", "alt", "title"):
                    if k == "href" and v and v.startswith("/"):
                        v = f"https://liaoxuefeng.com{v}"
                    self.content_parts[-1] += f' {k}="{v}"'
            self.content_parts[-1] += ">"
            self.current_tag = tag

    def handle_endtag(self, tag):
        if self.skip_depth > 0:
            self.skip_depth -= 1
            return

        if tag == "h1" and self.in_title:
            self.in_title = False
            self.title = self.title_buf.strip()
            return

        if self.in_content:
            self.content_parts.append(f"</{tag}>")

    def handle_data(self, data):
        if self.skip_depth > 0:
            return
        if self.in_title:
            self.title_buf += data
            return
        if self.in_content:
            self.content_parts.append(data)

    def get_content(self):
        return "".join(self.content_parts)


def fetch_page(url):
    """Fetch a page with proper headers."""
    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        },
    )
    try:
        with urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8")
    except Exception as e:
        print(f"  ⚠️  Failed to fetch {url}: {e}")
        return None


def extract_toc(html):
    """Extract table of contents from tutorial index page."""
    toc = []
    seen = set()
    pattern = r'<div class="gsc-index-item[^"]*">\s*<a class="truncate" href="(/books/[^"]+)"[^>]*>.*?<span class="gsc-index-item-marker">([^<]*)</span>\s*<span class="gsc-index-item-title">([^<]+)</span>'
    for m in re.finditer(pattern, html, re.DOTALL):
        href = m.group(1)
        marker = m.group(2).strip()
        title = m.group(3).strip()
        key = f"{marker}{title}"
        if title and href and key not in seen:
            seen.add(key)
            toc.append(
                {"title": f"{marker} {title}", "url": f"https://liaoxuefeng.com{href}"}
            )
    return toc


def extract_content(html):
    """Extract main content from a tutorial page."""
    parser = LiaoxuefengParser()
    try:
        parser.feed(html)
    except Exception:
        pass
    return parser.get_content(), parser.title


def extract_content_html(html):
    """Extract content from content.html endpoint (gsi-chapter-content)."""
    m = re.search(
        r'<div id="gsi-chapter-content">(.*?)</div>\s*</div>\s*</div>', html, re.DOTALL
    )
    if m:
        content = m.group(1)
    else:
        m = re.search(r'<div id="gsi-chapter-content">', html, re.DOTALL)
        if m:
            content = html[m.end() :]
        else:
            return ""

    for marker in ["x-discuss", "gsi-chapter-discuss", "评论"]:
        idx = content.find(marker)
        if idx > 0:
            content = content[:idx]
            break

    for m2 in re.finditer(r"<p[^>]*>(.*?)</p>", content, re.DOTALL):
        if "svg" not in m2.group(1).lower() and len(m2.group(1).strip()) > 10:
            content = content[m2.start() :]
            break

    content = content.strip()
    content = re.sub(r"\s*<div>\s*</div>\s*$", "", content)
    return content


def clean_content(html_content):
    """Clean up extracted HTML content."""
    html_content = re.sub(
        r"<script[^>]*>.*?</script>", "", html_content, flags=re.DOTALL
    )
    html_content = re.sub(r"<style[^>]*>.*?</style>", "", html_content, flags=re.DOTALL)
    html_content = re.sub(r"<!--.*?-->", "", html_content, flags=re.DOTALL)
    return html_content.strip()


def generate_tutorial_page(
    title,
    content,
    prev_url=None,
    prev_title=None,
    next_url=None,
    next_title=None,
    rel_path="",
):
    """Generate a complete HTML tutorial page."""
    html = make_header(title, depth=2)
    html += f"""
    <div style="max-width: 1200px; margin: 70px auto 40px; padding: 0 20px; display: flex; gap: 20px;">
        <div style="flex: 1; min-width: 0;">
            <div style="background: var(--bg-secondary, #fff); border-radius: 8px; padding: 32px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                <h1 style="font-size: 26px; margin-bottom: 16px; color: var(--text-primary, #1a1a2e); border-bottom: 2px solid var(--primary, #3b82f6); padding-bottom: 12px;">{title}</h1>
                <div style="font-size: 15px; line-height: 1.8; color: var(--text-secondary, #333);">
                    {content}
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--border, #e5e7eb);">
    """
    if prev_url:
        html += f'<a href="{prev_url}" style="color: var(--primary, #3b82f6); text-decoration: none; font-weight: 500;">&larr; {prev_title}</a>'
    else:
        html += "<span></span>"

    if next_url:
        html += f'<a href="{next_url}" style="color: var(--primary, #3b82f6); text-decoration: none; font-weight: 500;">{next_title} &rarr;</a>'
    else:
        html += "<span></span>"

    html += """
            </div>
        </div>
    </div>
    """
    html += make_footer(depth=2)
    return html


def generate_index_page():
    """Generate tutorials index page."""
    html = make_header("技术教程", depth=1)
    html += """
    <div class="tutorial-index">
        <div style="text-align: center; margin-bottom: 40px;">
            <h1 style="font-size: 32px; margin-bottom: 12px; color: var(--text-primary, #1a1a2e);">📖 技术教程</h1>
            <p style="color: var(--text-secondary, #666); font-size: 16px;">精选编程教程，从入门到进阶</p>
        </div>
        
        <div class="tutorial-card">
            <span class="badge badge-python">Python</span>
            <h3><a href="python/index.html" style="color: var(--text-primary, #1a1a2e); text-decoration: none;">Python 教程</a></h3>
            <p>廖雪峰的 Python 新手教程，中文、免费、零起点，基于最新的 Python 3 版本。包含数据类型、函数、面向对象、网络编程等完整内容。</p>
            <a href="python/index.html" style="color: var(--primary, #3b82f6); text-decoration: none; font-weight: 500;">开始学习 →</a>
        </div>
        
        <div class="tutorial-card">
            <span class="badge badge-git">Git</span>
            <h3><a href="git/index.html" style="color: var(--text-primary, #1a1a2e); text-decoration: none;">Git 教程</a></h3>
            <p>史上最浅显易懂的 Git 教程！面向初学者，实用性超强，边学边练。包含版本库、分支管理、远程仓库等完整内容。</p>
            <a href="git/index.html" style="color: var(--primary, #3b82f6); text-decoration: none; font-weight: 500;">开始学习 →</a>
        </div>
        
        <div class="tutorial-card">
            <span class="badge badge-ai">AI / LLM</span>
            <h3><a href="anthropic/index.html" style="color: var(--text-primary, #1a1a2e); text-decoration: none;">Anthropic 官方教程</a></h3>
            <p>Anthropic 官方的 Claude 101 系列教程，包含 AI 基础、Claude 使用指南、API 开发等。另有 Anthropic Academy 系统课程可获取证书。</p>
            <a href="anthropic/index.html" style="color: var(--primary, #3b82f6); text-decoration: none; font-weight: 500;">开始学习 →</a>
        </div>
    </div>
    """
    html += make_footer(depth=2)
    return html


def scrape_tutorial(course, tutorial_name, output_dir):
    """Scrape a full tutorial and generate HTML pages."""
    index_url = f"{BASE_URL}/books/{course}/introduction/index.html"
    print(f"📚 Fetching {tutorial_name} index: {index_url}")

    html = fetch_page(index_url)
    if not html:
        return False

    # Extract TOC
    toc = extract_toc(html)
    if not toc:
        print(f"  ⚠️  No TOC found for {tutorial_name}")
        return False

    print(f"  Found {len(toc)} chapters")

    # Fetch each chapter via content.html endpoint
    pages = []
    for i, item in enumerate(toc):
        print(f"  [{i + 1}/{len(toc)}] {item['title']}")
        # Use content.html endpoint instead of index.html
        content_url = item["url"].replace("/index.html", "/content.html")
        content_html = fetch_page(content_url)
        if content_html:
            content = extract_content_html(content_html)
            content = clean_content(content)
            title = item["title"]
            pages.append(
                {
                    "title": title,
                    "content": content,
                    "url": item["url"],
                }
            )
        else:
            pages.append(
                {
                    "title": item["title"],
                    "content": "<p>内容加载失败，请访问原文查看。</p>",
                    "url": item["url"],
                }
            )

    # Generate index page for this tutorial
    index_content = '<div class="toc-list">'
    for i, page in enumerate(pages):
        indent = "    " if "." in page["title"][:3] else ""
        index_content += f'<p style="{indent}padding-left: 16px;"><a href="{i}.html" style="color: var(--primary, #3b82f6); text-decoration: none;">{page["title"]}</a></p>'
    index_content += "</div>"

    # Generate TOC sidebar
    toc_sidebar = '<div class="tutorial-sidebar"><h3>目录</h3>'
    for i, page in enumerate(pages):
        toc_sidebar += f'<a href="{i}.html">{page["title"]}</a>'
    toc_sidebar += "</div>"

    # Generate individual pages
    out_path = TUTORIALS_DIR / output_dir
    out_path.mkdir(parents=True, exist_ok=True)

    # Index page
    with open(out_path / "index.html", "w") as f:
        html = make_header(f"{tutorial_name}", depth=2)
        html += f'<div class="tutorial-container" style="max-width: 960px; margin: 80px auto 40px; padding: 0 20px;">'
        html += toc_sidebar
        html += f'<div class="tutorial-content"><h1>{tutorial_name}</h1>{index_content}'
        html += f'<p style="margin-top: 20px; color: var(--text-secondary, #666);">原文来源：<a href="{BASE_URL}/books/{course}/" style="color: var(--primary, #3b82f6);">廖雪峰的官方网站</a></p>'
        html += "</div></div>"
        html += make_footer(depth=2)
        f.write(html)

    # Chapter pages
    for i, page in enumerate(pages):
        prev_url = f"{i - 1}.html" if i > 0 else None
        prev_title = pages[i - 1]["title"] if i > 0 else None
        next_url = f"{i + 1}.html" if i < len(pages) - 1 else None
        next_title = pages[i + 1]["title"] if i < len(pages) - 1 else None

        page_html = make_header(page["title"], depth=2)
        page_html += f'<div class="tutorial-container" style="max-width: 960px; margin: 80px auto 40px; padding: 0 20px;">'
        page_html += toc_sidebar
        page_html += f'<div class="tutorial-content">'
        page_html += f"<h1>{page['title']}</h1>"
        page_html += f'<div class="tutorial-body">{page["content"]}</div>'

        # Navigation
        page_html += '<div style="display: flex; justify-content: space-between; margin-top: 32px; padding-top: 20px; border-top: 1px solid var(--border, #e5e7eb);">'
        if prev_url:
            page_html += f'<a href="{prev_url}" style="color: var(--primary, #3b82f6); text-decoration: none; font-weight: 500;">&larr; {prev_title}</a>'
        else:
            page_html += "<span></span>"
        if next_url:
            page_html += f'<a href="{next_url}" style="color: var(--primary, #3b82f6); text-decoration: none; font-weight: 500;">{next_title} &rarr;</a>'
        else:
            page_html += "<span></span>"
        page_html += "</div>"

        page_html += f'<p style="margin-top: 16px; font-size: 13px; color: var(--text-secondary, #999);">原文：<a href="{page["url"]}" style="color: var(--primary, #3b82f6);">廖雪峰 - {page["title"]}</a></p>'
        page_html += "</div></div>"
        page_html += make_footer(depth=2)

        with open(out_path / f"{i}.html", "w") as f:
            f.write(page_html)

    print(f"  ✅ Generated {len(pages)} pages for {tutorial_name}")
    return True


def generate_anthropic_pages():
    """Generate Anthropic Academy tutorial pages."""
    out_path = TUTORIALS_DIR / "anthropic"
    out_path.mkdir(parents=True, exist_ok=True)

    courses = [
        {
            "name": "Claude 101",
            "desc": "Anthropic 官方入门教程，学习 Claude 的基础用法和最佳实践",
            "url": "https://anthropic.skilljar.com/introduction-to-claude-cowork",
            "icon": "🎓",
        },
        {
            "name": "Claude Code in Action",
            "desc": "Anthropic 官方实战教程，学习如何在实际项目中使用 Claude Code",
            "url": "https://anthropic.skilljar.com/claude-code-in-action",
            "icon": "💻",
        },
        {
            "name": "Anthropic Academy",
            "desc": "Anthropic 官方学习平台，提供 API 开发、MCP 协议、企业部署等系统课程，完成可获得证书",
            "url": "https://anthropic.skilljar.com/",
            "icon": "🏫",
        },
        {
            "name": "Claude API 文档",
            "desc": "Claude API 的完整开发文档，包含消息、工具调用、流式输出等接口说明",
            "url": "https://platform.claude.com/docs",
            "icon": "📡",
        },
        {
            "name": "Prompt Engineering Guide",
            "desc": "系统化的 Prompt 工程指南，学习如何编写高效的 Prompt 来引导 Claude 输出",
            "url": "https://www.promptingguide.ai/",
            "icon": "✍️",
        },
        {
            "name": "OpenAI Cookbook",
            "desc": "OpenAI 官方的代码示例集，包含各种 LLM 应用的最佳实践",
            "url": "https://cookbook.openai.com/",
            "icon": "📖",
        },
    ]

    # Index page
    html = make_header("Anthropic 官方教程")
    html += '<div class="tutorial-container" style="max-width: 960px; margin: 80px auto 40px; padding: 0 20px;">'
    html += '<div class="tutorial-content">'
    html += "<h1>🤖 Anthropic 官方教程</h1>"
    html += '<p style="margin-bottom: 24px; color: var(--text-secondary, #666); line-height: 1.8;">以下教程来源于 Anthropic 官方资源，帮助你系统学习 AI 和 Claude 的使用方法。</p>'

    for course in courses:
        html += f'''
        <div style="padding: 20px; margin: 16px 0; background: var(--bg-primary, #f8fafc); border-radius: 8px; border-left: 4px solid #8b5cf6;">
            <h3 style="margin: 0 0 8px;"><a href="{course["url"]}" target="_blank" style="color: var(--text-primary, #1a1a2e); text-decoration: none;">{course["icon"]} {course["name"]}</a></h3>
            <p style="margin: 0 0 12px; color: var(--text-secondary, #666);">{course["desc"]}</p>
            <a href="{course["url"]}" target="_blank" style="color: #8b5cf6; text-decoration: none; font-weight: 500; font-size: 14px;">前往学习 →</a>
        </div>'''

    html += "</div></div>"
    html += make_footer(depth=2)

    with open(out_path / "index.html", "w") as f:
        f.write(html)

    print(f"  ✅ Generated Anthropic tutorials index")


def main():
    print("🚀 Starting tutorial scraper...\n")

    # Generate index page
    with open(TUTORIALS_DIR / "index.html", "w") as f:
        f.write(generate_index_page())
    print("✅ Generated tutorials/index.html\n")

    # Scrape Python tutorial
    print("🐍 Scraping Python tutorial...")
    scrape_tutorial("python", "Python 教程", "python")
    print()

    # Scrape Git tutorial
    print("📦 Scraping Git tutorial...")
    scrape_tutorial("git", "Git 教程", "git")
    print()

    # Generate Anthropic pages
    print("🤖 Generating Anthropic tutorial pages...")
    generate_anthropic_pages()
    print()

    print("✅ All tutorials generated!")


if __name__ == "__main__":
    main()
