#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动生成 sitemap.xml 脚本
扫描所有 HTML 文件并生成站点地图
"""

import os
from datetime import datetime
from pathlib import Path

# 配置
BASE_URL = "https://jacksoncode.github.io"
EXCLUDE_DIRS = {
    'node_modules', '__pycache__', '.git', 'venv', 'ENV', 'env', 
    'myenv', '_includes', 'includes', 'module', 'non_wiki', 
    'Coder', 'wiki', 'mkdocs', 'note'
}

def get_last_modified(file_path):
    """获取文件最后修改时间"""
    timestamp = os.path.getmtime(file_path)
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

def scan_html_files(root_dir):
    """扫描所有 HTML 文件"""
    html_files = []
    
    for root, dirs, files in os.walk(root_dir):
        # 排除指定目录
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        
        for file in files:
            if file.endswith(('.html', '.htm')) and file != '404.html':
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, root_dir)
                
                # 跳过临时文件
                if '.backup.' in file or file.startswith('.'):
                    continue
                
                last_mod = get_last_modified(full_path)
                
                # 确定优先级
                priority = '0.5'
                if file == 'index.html':
                    priority = '1.0'
                elif file in ['nav.html', 'about.html', 'contact.html', 'book.html']:
                    priority = '0.8'
                elif '/blog/' in rel_path:
                    priority = '0.7'
                
                html_files.append({
                    'path': rel_path.replace('\\', '/'),
                    'lastmod': last_mod,
                    'priority': priority,
                    'changefreq': 'weekly' if file == 'index.html' else 'monthly'
                })
    
    return html_files

def generate_sitemap(files):
    """生成 sitemap XML"""
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n\n'
    
    for file in sorted(files, key=lambda x: x['priority'], reverse=True):
        url = f"{BASE_URL}/{file['path']}"
        xml += '  <url>\n'
        xml += f'    <loc>{url}</loc>\n'
        xml += f'    <lastmod>{file["lastmod"]}</lastmod>\n'
        xml += f'    <changefreq>{file["changefreq"]}</changefreq>\n'
        xml += f'    <priority>{file["priority"]}</priority>\n'
        xml += '  </url>\n\n'
    
    xml += '</urlset>'
    return xml

def main():
    """主函数"""
    print("🗺️  开始生成 sitemap.xml...")
    print("=" * 60)
    
    # 扫描文件
    current_dir = os.path.dirname(os.path.abspath(__file__))
    files = scan_html_files(current_dir)
    
    print(f"✅ 找到 {len(files)} 个 HTML 页面")
    
    # 生成 sitemap
    sitemap_xml = generate_sitemap(files)
    
    # 保存文件
    output_path = os.path.join(current_dir, 'sitemap.xml')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(sitemap_xml)
    
    print(f"📄 已保存到：{output_path}")
    print("=" * 60)
    print("✨ sitemap.xml 生成完成！")
    print("")
    print("📝 下一步:")
    print("  1. 验证 sitemap: https://www.google.com/webmasters/tools/sitemap-url")
    print("  2. 提交到 Google Search Console")
    print("  3. 提交到 Bing Webmaster Tools")
    print("  4. 提交到百度站长平台")

if __name__ == '__main__':
    main()
