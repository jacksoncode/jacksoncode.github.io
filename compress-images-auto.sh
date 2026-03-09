#!/bin/bash
# 自动化图片压缩脚本 - 第四阶段

echo "🖼️  开始自动化图片压缩..."
echo ""

# 定义需要压缩的大图
large_images=(
    "images/logo/web.jpg"
    "img/book-bg.jpg"
    "img/temp-bg.jpg"
    "img/nav-bg.jpg"
    "img/index-banner.jpg"
    "img/blog-bg.jpg"
)

# 创建备份目录
backup_dir="images-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup_dir"

echo "📁 创建备份目录：$backup_dir"
cp -r img/* "$backup_dir/img/" 2>/dev/null
cp -r images/* "$backup_dir/images/" 2>/dev/null

compressed_count=0
total_saved=0

echo ""
echo "🔄 开始压缩图片..."
echo "=================="

for img in "${large_images[@]}"; do
    if [ -f "$img" ]; then
        # 获取原始大小
        original_size=$(du -k "$img" | cut -f1)
        
        echo ""
        echo "处理：$img"
        echo "  原始大小：${original_size}KB"
        
        # 使用 ImageMagick 压缩（如果已安装）
        if command -v convert &> /dev/null; then
            # 压缩 JPEG，质量 75%
            convert "$img" -quality 75 -strip "${img%.jpg}-optimized.jpg"
            
            # 替换原文件
            mv "${img%.jpg}-optimized.jpg" "$img"
            
            # 获取新大小
            new_size=$(du -k "$img" | cut -f1)
            saved=$((original_size - new_size))
            total_saved=$((total_saved + saved))
            ((compressed_count++))
            
            echo "  ✅ 压缩后：${new_size}KB (节省：${saved}KB)"
        else
            echo "  ⚠️  ImageMagick 未安装，跳过自动压缩"
            echo "  💡 建议手动压缩：https://tinypng.com/ 或 https://squoosh.app/"
        fi
        
        # 创建 WebP 版本（如果 cwebp 已安装）
        if command -v cwebp &> /dev/null && [[ "$img" == *.jpg ]]; then
            echo "  🌐 生成 WebP 版本..."
            cwebp -q 75 "$img" -o "${img%.jpg}.webp" 2>/dev/null
            if [ $? -eq 0 ]; then
                webp_size=$(du -k "${img%.jpg}.webp" | cut -f1)
                echo "     WebP 大小：${webp_size}KB"
            fi
        fi
    else
        echo ""
        echo "⚠️  文件不存在：$img"
    fi
done

echo ""
echo "=================="
echo "📊 压缩完成统计:"
echo "  压缩图片数：$compressed_count"
echo "  总节省空间：${total_saved}KB ($(echo "scale=2; $total_saved/1024" | bc)MB)"
echo ""

if [ $compressed_count -gt 0 ]; then
    echo "✨ 图片压缩完成！"
    echo ""
    echo "📝 下一步操作:"
    echo "  1. 检查网站图片显示是否正常"
    echo "  2. 如需要恢复，从备份目录复制："
    echo "     cp $backup_dir/img/* img/"
    echo "     cp $backup_dir/images/* images/"
else
    echo "⚠️  没有图片被压缩"
    echo ""
    echo "💡 建议:"
    echo "  1. 安装 ImageMagick:"
    echo "     macOS: brew install imagemagick"
    echo "     Linux: apt-get install imagemagick"
    echo "  2. 或使用在线工具手动压缩:"
    echo "     - https://tinypng.com/"
    echo "     - https://squoosh.app/"
fi

echo ""
