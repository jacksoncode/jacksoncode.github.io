#!/usr/bin/env python3
"""Scrape tutorials from runoob.com and generate local HTML pages."""

import re
import ssl
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

BASE = "https://www.runoob.com"
OUT = Path("tutorials/runoob")
ssl._create_default_https_context = ssl._create_unverified_context


def fetch(url):
    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        },
    )
    try:
        with urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8")
    except Exception as e:
        print(f"  ⚠️  {url}: {e}")
        return None


def extract_toc(html, allowed_prefixes):
    """Extract chapter links from left sidebar, filtered by allowed prefixes."""
    links = []
    seen = set()
    for m in re.finditer(r'href="(/[^"]+\.html)"[^>]*>\s*([^<]+?)\s*</a>', html):
        href, title = m.group(1).strip(), m.group(2).strip()
        if not any(href.startswith(p) for p in allowed_prefixes):
            continue
        if title in ("首页", "Linux 测验"):
            continue
        if href not in seen:
            seen.add(href)
            links.append({"title": title, "url": f"{BASE}{href}"})
    return links


def html_to_markdown(html_content):
    """Convert HTML content block to markdown."""
    md = html_content

    # Remove ads, scripts, styles
    md = re.sub(r"<script[^>]*>.*?</script>", "", md, flags=re.DOTALL)
    md = re.sub(r"<style[^>]*>.*?</style>", "", md, flags=re.DOTALL)
    md = re.sub(r"<!--.*?-->", "", md, flags=re.DOTALL)

    # Remove ad divs
    md = re.sub(
        r'<div class="article-heading-ad[^"]*">.*?</div>', "", md, flags=re.DOTALL
    )
    md = re.sub(r'<div class="archive-list[^"]*">.*?</div>', "", md, flags=re.DOTALL)
    md = re.sub(r'<div class="sidebar-box[^"]*">.*?</div>', "", md, flags=re.DOTALL)
    md = re.sub(
        r'<div class="previous-next-links[^"]*">.*?</div>', "", md, flags=re.DOTALL
    )
    md = re.sub(r'<div class="tutintro[^"]*">', "<div>", md)

    # Remove img tags with runoob branding
    md = re.sub(r'<img[^>]*src="[^"]*logo[^"]*"[^>]*/?>', "", md)

    # Convert images
    md = re.sub(r'<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"[^>]*/?>', r"![\2](\1)", md)
    md = re.sub(r'<img[^>]*src="([^"]+)"[^>]*/?>', r"![](\1)", md)

    # Convert headings
    md = re.sub(r"<h1([^>]*)>(.*?)</h1>", r"\n# \2\n", md, flags=re.DOTALL)
    md = re.sub(r"<h2([^>]*)>(.*?)</h2>", r"\n## \2\n", md, flags=re.DOTALL)
    md = re.sub(r"<h3([^>]*)>(.*?)</h3>", r"\n### \2\n", md, flags=re.DOTALL)
    md = re.sub(r"<h4([^>]*)>(.*?)</h4>", r"\n#### \2\n", md, flags=re.DOTALL)

    # Convert code blocks
    md = re.sub(
        r"<pre><code[^>]*>(.*?)</code></pre>", r"\n```\n\1\n```\n", md, flags=re.DOTALL
    )
    md = re.sub(r"<pre>(.*?)</pre>", r"\n```\n\1\n```\n", md, flags=re.DOTALL)
    md = re.sub(r"<code>(.*?)</code>", r"`\1`", md, flags=re.DOTALL)

    # Convert links
    md = re.sub(
        r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', r"[\2](\1)", md, flags=re.DOTALL
    )

    # Convert bold/strong
    md = re.sub(r"<strong[^>]*>(.*?)</strong>", r"**\1**", md, flags=re.DOTALL)
    md = re.sub(r"<b[^>]*>(.*?)</b>", r"**\1**", md, flags=re.DOTALL)
    md = re.sub(r"<em[^>]*>(.*?)</em>", r"*\1*", md, flags=re.DOTALL)

    # Convert lists
    md = re.sub(r"<li>", "\n- ", md)
    md = re.sub(r"</li>", "", md)
    md = re.sub(r"</?ul[^>]*>", "\n", md)
    md = re.sub(r"</?ol[^>]*>", "\n", md)

    # Convert paragraphs and line breaks
    md = re.sub(r"</p>", "\n\n", md)
    md = re.sub(r"<p[^>]*>", "", md)
    md = re.sub(r"<br\s*/?>", "\n", md)
    md = re.sub(r"<hr\s*/?>", "\n---\n", md)

    # Remove remaining tags
    md = re.sub(r"<[^>]+>", "", md)

    # Clean up whitespace
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r" +\n", "\n", md)
    return md.strip()


class RunoobContentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_content = False
        self.in_sidebar = False
        self.skip = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if self.skip > 0:
            self.skip += 1
            return
        d = dict(attrs)
        cls = d.get("class", "") or ""
        if "article-intro" in cls or "tutintro" in cls:
            self.in_content = True
            return
        if (
            "left-column" in cls
            or "sidebar-tree" in cls
            or "right-column" in cls
            or "article-heading-ad" in cls
            or "archive-list" in cls
            or "previous-next-links" in cls
            or "sidebar-box" in cls
        ):
            self.skip = 1
            return
        if self.in_content:
            self.parts.append(f"<{tag}")
            for k, v in attrs:
                if k in ("class", "id", "href", "src", "alt", "width", "height"):
                    if k == "href" and v and not v.startswith("http"):
                        v = f"{BASE}{v}"
                    self.parts[-1] += f' {k}="{v}"'
            self.parts[-1] += ">"

    def handle_endtag(self, tag):
        if self.skip > 0:
            self.skip -= 1
            return
        if self.in_content:
            self.parts.append(f"</{tag}>")

    def handle_data(self, data):
        if self.skip > 0:
            return
        if self.in_content:
            self.parts.append(data)

    def get(self):
        return "".join(self.parts)


def extract_content_html(html):
    parser = RunoobContentParser()
    try:
        parser.feed(html)
    except Exception:
        pass
    return parser.get()


def make_page(title, content_md, chapters, current_idx, tutorial_name):
    """Generate HTML page with markdown content rendered via marked.js."""
    # Escape for JS
    js_md = (
        content_md.replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("'", "\\'")
        .replace("\n", "\\n")
        .replace("\r", "")
    )

    prev_link = ""
    if current_idx > 0:
        c = chapters[current_idx - 1]
        prev_link = f'<a href="{current_idx - 1}.html" class="page-nav-link">&larr; {c["title"]}</a>'
    else:
        prev_link = "<span></span>"

    next_link = ""
    if current_idx < len(chapters) - 1:
        c = chapters[current_idx + 1]
        next_link = f'<a href="{current_idx + 1}.html" class="page-nav-link">{c["title"]} &rarr;</a>'
    else:
        next_link = "<span></span>"

    sidebar_links = ""
    for i, c in enumerate(chapters):
        active = 'class="active"' if i == current_idx else ""
        sidebar_links += f'<a href="{i}.html" {active}>{c["title"]}</a>\n'

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="CodeClub - {title}">
    <meta name="author" content="Jackson">
    <title>{title} - CodeClub</title>
    <link rel="icon" type="image/x-icon" href="../../img/logo.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <link rel="stylesheet" href="../../css/main.css">
    <link rel="stylesheet" href="../../css/dark-mode.css">
    <link rel="stylesheet" href="../../css/mobile-optimizations.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.1/github-markdown.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.0/marked.min.js"></script>
    <style>
    .tutorial-page {{ max-width: 1200px; margin: 70px auto 40px; padding: 0 20px; display: flex; gap: 20px; }}
    .tutorial-sidebar {{ width: 240px; flex-shrink: 0; position: sticky; top: 70px; max-height: calc(100vh - 90px); overflow-y: auto; background: var(--bg-secondary, #fff); border-radius: 8px; padding: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
    .tutorial-sidebar h3 {{ font-size: 15px; margin: 0 0 12px; color: var(--text-primary, #1a1a2e); padding-bottom: 8px; border-bottom: 2px solid var(--primary, #3b82f6); }}
    .tutorial-sidebar a {{ display: block; padding: 5px 8px; color: var(--text-secondary, #666); text-decoration: none; font-size: 13px; border-radius: 4px; line-height: 1.4; }}
    .tutorial-sidebar a:hover {{ background: var(--primary, #3b82f6); color: #fff; }}
    .tutorial-sidebar a.active {{ background: var(--primary, #3b82f6); color: #fff; font-weight: 600; }}
    .tutorial-main {{ flex: 1; min-width: 0; }}
    .tutorial-article {{ background: var(--bg-secondary, #fff); border-radius: 8px; padding: 32px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
    .tutorial-article h1 {{ font-size: 26px; margin-bottom: 16px; color: var(--text-primary, #1a1a2e); border-bottom: 2px solid var(--primary, #3b82f6); padding-bottom: 12px; }}
    .markdown-body {{ font-size: 15px; line-height: 1.8; color: var(--text-secondary, #333); }}
    .markdown-body h1 {{ font-size: 24px; border-bottom: 1px solid var(--border, #e5e7eb); padding-bottom: 8px; }}
    .markdown-body h2 {{ font-size: 20px; border-bottom: 1px solid var(--border, #e5e7eb); padding-bottom: 6px; }}
    .markdown-body h3 {{ font-size: 17px; }}
    .markdown-body pre {{ background: #1e1e2e; color: #cdd6f4; padding: 16px; border-radius: 8px; overflow-x: auto; }}
    .markdown-body code {{ font-family: 'Fira Code', 'Cascadia Code', monospace; font-size: 14px; }}
    .markdown-body p code {{ background: #f1f5f9; padding: 2px 6px; border-radius: 4px; color: #e83e8c; }}
    .markdown-body blockquote {{ border-left: 4px solid var(--primary, #3b82f6); padding: 12px 20px; margin: 16px 0; background: #f8fafc; border-radius: 0 8px 8px 0; }}
    .markdown-body img {{ max-width: 100%; border-radius: 8px; }}
    .page-navigation {{ display: flex; justify-content: space-between; margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--border, #e5e7eb); }}
    .page-nav-link {{ color: var(--primary, #3b82f6); text-decoration: none; font-weight: 500; font-size: 14px; }}
    .page-nav-link:hover {{ text-decoration: underline; }}
    .source-link {{ margin-top: 16px; font-size: 13px; color: var(--text-secondary, #999); }}
    .source-link a {{ color: var(--primary, #3b82f6); }}
    @media (max-width: 768px) {{
        .tutorial-page {{ flex-direction: column; }}
        .tutorial-sidebar {{ width: 100%; position: static; max-height: 200px; }}
    }}
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="navbar-container">
            <a class="navbar-brand" href="../../index.html">
                <img src="../../img/logo.png" alt="CodeClub" width="32" height="32">
                <span>CodeClub</span>
            </a>
            <button class="mobile-menu-toggle" aria-label="切换导航菜单"><span></span><span></span><span></span></button>
            <ul class="navbar-nav">
                <li><a class="nav-link" href="../../index.html">首页</a></li>
                <li><a class="nav-link" href="../../nav.html">网址导航</a></li>
                <li><a class="nav-link" href="../../blog/">博客</a></li>
                <li><a class="nav-link" href="../../wiki/index.html" target="_blank">WiKi</a></li>
                <li><a class="nav-link active" href="../index.html">教程</a></li>
                <li><a class="nav-link" href="../../book.html">图书</a></li>
                <li><a class="nav-link" href="../../contact.html">联系我</a></li>
                <li><a class="nav-link" href="../../about.html">关于我</a></li>
            </ul>
        </div>
    </nav>
    <div class="tutorial-page">
        <div class="tutorial-sidebar">
            <h3>📖 {tutorial_name}</h3>
            {sidebar_links}
        </div>
        <div class="tutorial-main">
            <div class="tutorial-article">
                <div class="markdown-body" id="md-content"></div>
                <div class="page-navigation">
                    {prev_link}
                    {next_link}
                </div>
                <div class="source-link">原文来源：<a href="{BASE}" target="_blank">菜鸟教程</a></div>
            </div>
        </div>
    </div>
    <footer class="footer">
        <div class="footer-content"><p>&copy; 2024 CodeClub. All rights reserved.</p></div>
    </footer>
    <script src="../../js/dark-mode.js"></script>
    <script src="../../js/mobile-menu.js"></script>
    <script>
    const md = `{js_md}`;
    document.getElementById('md-content').innerHTML = marked.parse(md);
    </script>
</body>
</html>"""


def scrape_tutorial(name, index_url, out_dir, allowed_prefixes):
    """Scrape a full tutorial from runoob.com."""
    print(f"📚 {name}: {index_url}")
    html = fetch(index_url)
    if not html:
        return

    chapters = extract_toc(html, allowed_prefixes)
    if not chapters:
        print(f"  ⚠️  No TOC found")
        return

    # Deduplicate - keep first occurrence
    seen_urls = set()
    unique = []
    for c in chapters:
        if c["url"] not in seen_urls:
            seen_urls.add(c["url"])
            unique.append(c)
    chapters = unique

    print(f"  Found {len(chapters)} chapters")

    out = OUT / out_dir
    out.mkdir(parents=True, exist_ok=True)

    for i, ch in enumerate(chapters):
        print(f"  [{i + 1}/{len(chapters)}] {ch['title']}")
        ch_html = fetch(ch["url"])
        if ch_html:
            content = extract_content_html(ch_html)
            md = html_to_markdown(content)
        else:
            md = f"内容加载失败，请查看[原文]({ch['url']})"

        page = make_page(ch["title"], md, chapters, i, name)
        (out / f"{i}.html").write_text(page, encoding="utf-8")

    # Generate index page
    index_links = ""
    for i, ch in enumerate(chapters):
        index_links += f'<a href="{i}.html">{ch["title"]}</a>\n'

    index_page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{name} - CodeClub</title>
    <link rel="icon" type="image/x-icon" href="../../img/logo.png">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <link rel="stylesheet" href="../../css/main.css">
    <link rel="stylesheet" href="../../css/dark-mode.css">
    <link rel="stylesheet" href="../../css/mobile-optimizations.css">
    <style>
    .tutorial-page {{ max-width: 1200px; margin: 70px auto 40px; padding: 0 20px; display: flex; gap: 20px; }}
    .tutorial-sidebar {{ width: 240px; flex-shrink: 0; position: sticky; top: 70px; max-height: calc(100vh - 90px); overflow-y: auto; background: var(--bg-secondary, #fff); border-radius: 8px; padding: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
    .tutorial-sidebar h3 {{ font-size: 15px; margin: 0 0 12px; color: var(--text-primary, #1a1a2e); padding-bottom: 8px; border-bottom: 2px solid var(--primary, #3b82f6); }}
    .tutorial-sidebar a {{ display: block; padding: 5px 8px; color: var(--text-secondary, #666); text-decoration: none; font-size: 13px; border-radius: 4px; line-height: 1.4; }}
    .tutorial-sidebar a:hover {{ background: var(--primary, #3b82f6); color: #fff; }}
    .tutorial-sidebar a.active {{ background: var(--primary, #3b82f6); color: #fff; font-weight: 600; }}
    .tutorial-main {{ flex: 1; min-width: 0; }}
    .tutorial-article {{ background: var(--bg-secondary, #fff); border-radius: 8px; padding: 32px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
    .toc-list a {{ display: block; padding: 6px 10px; color: var(--primary, #3b82f6); text-decoration: none; border-radius: 4px; }}
    .toc-list a:hover {{ background: var(--primary, #3b82f6); color: #fff; }}
    @media (max-width: 768px) {{ .tutorial-page {{ flex-direction: column; }} .tutorial-sidebar {{ width: 100%; position: static; max-height: 200px; }} }}
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="navbar-container">
            <a class="navbar-brand" href="../../index.html"><img src="../../img/logo.png" alt="CodeClub" width="32" height="32"><span>CodeClub</span></a>
            <button class="mobile-menu-toggle" aria-label="切换导航菜单"><span></span><span></span><span></span></button>
            <ul class="navbar-nav">
                <li><a class="nav-link" href="../../index.html">首页</a></li>
                <li><a class="nav-link" href="../../nav.html">网址导航</a></li>
                <li><a class="nav-link" href="../../blog/">博客</a></li>
                <li><a class="nav-link" href="../../wiki/index.html" target="_blank">WiKi</a></li>
                <li><a class="nav-link active" href="../index.html">教程</a></li>
                <li><a class="nav-link" href="../../book.html">图书</a></li>
                <li><a class="nav-link" href="../../contact.html">联系我</a></li>
                <li><a class="nav-link" href="../../about.html">关于我</a></li>
            </ul>
        </div>
    </nav>
    <div class="tutorial-page">
        <div class="tutorial-sidebar"><h3>📖 {name}</h3>{index_links}</div>
        <div class="tutorial-main">
            <div class="tutorial-article">
                <h1 style="font-size: 26px; margin-bottom: 16px; color: var(--text-primary, #1a1a2e); border-bottom: 2px solid var(--primary, #3b82f6); padding-bottom: 12px;">{name}</h1>
                <div class="toc-list">{index_links}</div>
            </div>
        </div>
    </div>
    <footer class="footer"><div class="footer-content"><p>&copy; 2024 CodeClub. All rights reserved.</p></div></footer>
    <script src="../../js/dark-mode.js"></script>
    <script src="../../js/mobile-menu.js"></script>
</body>
</html>"""
    (out / "index.html").write_text(index_page, encoding="utf-8")
    print(f"  ✅ Generated {len(chapters)} pages")


def main():
    tutorials = [
        ("Linux", f"{BASE}/linux/linux-tutorial.html", "linux", ["/linux/"]),
        ("Shell", f"{BASE}/linux/linux-shell.html", "shell", ["/linux/"]),
        ("Docker", f"{BASE}/docker/docker-tutorial.html", "docker", ["/docker/"]),
        ("AI Agent", f"{BASE}/ai-agent/ai-agent-tutorial.html", "ai-agent", ["/ai-agent/"]),
        ("Claude Code", f"{BASE}/claude-code/claude-code-tutorial.html", "claude-code", ["/claude-code/"]),
        ("OpenCode", f"{BASE}/opencode/opencode-tutorial.html", "opencode", ["/opencode/"]),
    ]

    for name, url, d, prefixes in tutorials:
        scrape_tutorial(name, url, d, prefixes)
        print()

    print("✅ All runoob tutorials generated!")


if __name__ == "__main__":
    main()
