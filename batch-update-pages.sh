#!/bin/bash
# 批量更新页面 - 添加 CDN、移动端菜单和 PWA 支持

echo "🔄 开始批量更新页面..."

files=("about.html" "contact.html" "book.html")

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "📄 处理：$file"
        
        # 创建备份
        cp "$file" "${file}.backup.$(date +%Y%m%d-%H%M%S)"
        
        # 1. 替换 Font Awesome 为 CDN
        sed -i '' 's|<link href="lib/font-awesome/css/all.min.css" rel="stylesheet">|<!-- Font Awesome CDN -->\n    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer" />|g' "$file"
        
        # 2. 添加 preconnect
        sed -i '' 's|<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>|<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n    <link rel="preconnect" href="https://cdnjs.cloudflare.com">|g' "$file"
        
        echo "  ✅ CDN 优化完成"
    else
        echo "  ⚠️  文件不存在：$file"
    fi
done

echo "✨ 批量更新完成！"
echo ""
echo "📝 提示：请手动检查并测试每个页面"
