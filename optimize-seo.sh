#!/bin/bash
# SEO 优化脚本 - 为主要 HTML 页面添加 SEO 标签

echo "🚀 开始 SEO 优化..."

# 定义要更新的文件
files=("nav.html" "about.html" "contact.html" "book.html" "blog.html")

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "📄 处理：$file"
        
        # 创建临时文件
        temp_file=$(mktemp)
        
        # 读取文件内容并插入 SEO 标签
        awk '
        /<meta name="author" content="Jackson">/ {
            print $0
            print "    <meta name=\"robots\" content=\"index, follow\">"
            print ""
            print "    <!-- Open Graph -->"
            print "    <meta property=\"og:type\" content=\"website\">"
            print "    <meta property=\"og:locale\" content=\"zh_CN\">"
            print "    <meta property=\"og:site_name\" content=\"CodeClub\">"
            next
        }
        /<title>/ && !og_title_added {
            print "    <meta property=\"og:title\" content=\"" title "\">"
            og_title_added = 1
            next
        }
        /<link rel=\"icon\"/ && !canonical_added {
            print "    <link rel=\"canonical\" href=\"https://jacksoncode.github.io/\">"
            print "    <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">"
            print "    <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>"
            canonical_added = 1
            next
        }
        { print }
        ' "$file" > "$temp_file"
        
        # 替换原文件
        mv "$temp_file" "$file"
        echo "✅ 完成：$file"
    else
        echo "⚠️  文件不存在：$file"
    fi
done

echo "✨ SEO 优化完成！"
