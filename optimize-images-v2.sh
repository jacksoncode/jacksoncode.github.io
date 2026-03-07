#!/bin/bash
# 图片压缩优化脚本 - 第三阶段

echo "🖼️  开始图片压缩优化..."
echo ""

# 检查大图片
echo "📊 查找大于 500KB 的图片..."
large_images=$(find images img -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) -size +500k 2>/dev/null)

if [ -z "$large_images" ]; then
    echo "✅ 没有发现大于 500KB 的图片"
else
    echo "⚠️  以下图片需要压缩:"
    echo "$large_images"
    echo ""
fi

# 创建 WebP 版本
echo "🌐 为重要图片创建 WebP 版本..."
webp_count=0

for img in img/logo.png img/favicon*.png images/logo/*.jpg; do
    if [ -f "$img" ] && [ ! -f "${img%.*}.webp" ]; then
        if command -v cwebp &> /dev/null; then
            cwebp -q 80 "$img" -o "${img%.*}.webp" 2>/dev/null && ((webp_count++))
        fi
    fi
done

echo "✅ 创建了 $webp_count 个 WebP 文件"
echo ""

# 显示图片统计
echo "📈 图片统计:"
echo "============"
total_images=$(find images img -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -o -name "*.gif" \) 2>/dev/null | wc -l)
total_size=$(du -sh images img 2>/dev/null | awk '{sum+=$1} END {print sum}')
avg_size=$(find images img -type f \( -name "*.jpg" -o -name "*.png" \) -exec du -k {} + 2>/dev/null | awk '{sum+=$1; count++} END {if(count>0) print int(sum/count); else print 0}')

echo "总图片数：$total_images"
echo "总大小：约 ${total_size}MB"
echo "平均大小：约 ${avg_size}KB/张"
echo ""

# 提供优化建议
echo "💡 优化建议:"
echo "============"
echo "1. 使用在线工具压缩大图片:"
echo "   - TinyPNG: https://tinypng.com/"
echo "   - Squoosh: https://squoosh.app/"
echo ""
echo "2. 批量转换 WebP (需要先安装):"
echo "   brew install webp  # macOS"
echo "   apt-get install webp  # Linux"
echo ""
echo "3. 推荐图片尺寸:"
echo "   - Logo: 192x192px 或 512x512px"
echo "   - Banner: 1920x600px (压缩后 <200KB)"
echo "   - 内容图片：800x600px (压缩后 <100KB)"
echo ""

# 如果需要，可以运行以下命令压缩所有图片
echo "🔧 自动压缩选项:"
echo "==============="
read -p "是否要使用 ImageOptim CLI 压缩所有图片？(y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v imagemin &> /dev/null; then
        echo "🔄 开始压缩..."
        # imagemin 'images/*.{jpg,png}' --out-dir=images-optimized
        echo "⚠️  需要先配置 imagemin"
    else
        echo "⚠️  imagemin 未安装"
        echo "   安装：npm install -g imagemin-cli"
    fi
fi

echo ""
echo "✨ 图片优化分析完成！"
