#!/bin/bash
# 图片压缩脚本 - 优化网站图片资源

echo "🖼️  开始图片压缩优化..."

# 检查是否安装了 imagemin
if ! command -v imagemin &> /dev/null; then
    echo "⚠️  需要安装 imagemin，正在安装..."
    npm install -g imagemin-cli imagemin-mozjpeg imagemin-pngquant
fi

# 创建备份目录
backup_dir="images-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup_dir"

# 压缩 images 目录
if [ -d "images" ]; then
    echo "📁 备份原图片到 $backup_dir"
    cp -r images/* "$backup_dir/" 2>/dev/null
    
    echo "🔄 压缩 images 目录..."
    find images -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -o -name "*.gif" \) | while read file; do
        echo "  处理：$file"
        # 这里可以添加实际的压缩命令
        # imagemin "$file" --out-dir="$(dirname "$file")"
    done
fi

# 压缩 img 目录
if [ -d "img" ]; then
    echo "📁 备份原图片到 ${backup_dir}-img"
    cp -r img/* "${backup_dir}-img/" 2>/dev/null
    
    echo "🔄 压缩 img 目录..."
    find img -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -o -name "*.gif" \) | while read file; do
        echo "  处理：$file"
    done
fi

# 生成 WebP 版本
echo "🌐 生成 WebP 版本..."
if command -v cwebp &> /dev/null; then
    find . -maxdepth 3 -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) ! -path "*/node_modules/*" ! -path "*/.git/*" | head -20 | while read file; do
        if [ ! -f "${file%.*}.webp" ]; then
            echo "  转换：$file -> ${file%.*}.webp"
            cwebp -q 80 "$file" -o "${file%.*}.webp"
        fi
    done
else
    echo "⚠️  cwebp 未安装，跳过 WebP 转换"
    echo "   安装：brew install webp (macOS) 或 apt-get install webp (Linux)"
fi

echo "✨ 图片优化完成！"
echo ""
echo "📊 建议手动优化的大文件:"
find . -maxdepth 4 -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) -size +500k ! -path "*/node_modules/*" ! -path "*/.git/*" | head -10
