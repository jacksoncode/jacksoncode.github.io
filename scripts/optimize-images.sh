#!/bin/bash
# 统一图片优化脚本
# 整合了图片压缩、WebP 转换、大图片检测功能
# 用法: ./scripts/optimize-images.sh [--webp] [--compress] [--check]

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 配置
IMG_DIRS=("images" "img")
QUALITY=80
BACKUP_DIR="images-backup-$(date +%Y%m%d-%H%M%S)"

log() { echo -e "${GREEN}✅ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
info() { echo -e "${BLUE}📌 $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; }

# 创建备份
create_backup() {
    info "创建图片备份到 $BACKUP_DIR"
    mkdir -p "$BACKUP_DIR"
    for dir in "${IMG_DIRS[@]}"; do
        if [ -d "$dir" ]; then
            cp -r "$dir" "$BACKUP_DIR/" 2>/dev/null || true
        fi
    done
    log "备份完成"
}

# 检查大图片
check_large_images() {
    info "查找大于 500KB 的图片..."
    local found=false
    for dir in "${IMG_DIRS[@]}"; do
        if [ -d "$dir" ]; then
            while IFS= read -r file; do
                if [ -n "$file" ]; then
                    found=true
                    size=$(du -h "$file" | cut -f1)
                    echo "  $file ($size)"
                fi
            done < <(find "$dir" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) -size +500k 2>/dev/null)
        fi
    done
    if [ "$found" = false ]; then
        log "没有发现大于 500KB 的图片"
    fi
}

# 创建 WebP 版本
convert_to_webp() {
    if ! command -v cwebp &> /dev/null; then
        warn "cwebp 未安装，跳过 WebP 转换"
        info "安装方法: brew install webp (macOS) 或 apt-get install webp (Linux)"
        return
    fi

    info "开始 WebP 转换 (质量: $QUALITY)..."
    local count=0
    for dir in "${IMG_DIRS[@]}"; do
        if [ -d "$dir" ]; then
            while IFS= read -r file; do
                local webp="${file%.*}.webp"
                if [ ! -f "$webp" ] || [ "$file" -nt "$webp" ]; then
                    cwebp -q "$QUALITY" "$file" -o "$webp" 2>/dev/null && ((count++)) || true
                fi
            done < <(find "$dir" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) 2>/dev/null)
        fi
    done
    log "创建了 $count 个 WebP 文件"
}

# 使用 ImageMagick 压缩
compress_with_imagemagick() {
    if ! command -v convert &> /dev/null; then
        warn "ImageMagick 未安装，跳过压缩"
        info "安装方法: brew install imagemagick (macOS)"
        return
    fi

    info "开始图片压缩 (质量: 75%)..."
    local count=0
    local total_saved=0
    for dir in "${IMG_DIRS[@]}"; do
        if [ -d "$dir" ]; then
            while IFS= read -r file; do
                original_size=$(du -k "$file" | cut -f1)
                convert "$file" -quality 75 -strip "$file" 2>/dev/null || continue
                new_size=$(du -k "$file" | cut -f1)
                saved=$((original_size - new_size))
                total_saved=$((total_saved + saved))
                ((count++))
            done < <(find "$dir" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) 2>/dev/null)
        fi
    done
    log "压缩了 $count 张图片，节省 ${total_saved}KB"
}

# 显示统计
show_stats() {
    echo ""
    info "图片统计:"
    echo "============"
    local total=0
    for dir in "${IMG_DIRS[@]}"; do
        if [ -d "$dir" ]; then
            count=$(find "$dir" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -o -name "*.gif" -o -name "*.webp" \) 2>/dev/null | wc -l | tr -d ' ')
            total=$((total + count))
        fi
    done
    echo "总图片数: $total"
    du -sh "${IMG_DIRS[@]}" 2>/dev/null | while read size dir; do
        echo "  $dir: $size"
    done
}

# 主流程
main() {
    echo -e "${GREEN}🖼️  图片优化脚本${NC}"
    echo "=================="
    echo ""

    create_backup
    check_large_images

    # 解析参数
    if [[ "$1" == "--compress" ]]; then
        compress_with_imagemagick
    fi
    if [[ "$1" == "--webp" || -z "$1" ]]; then
        convert_to_webp
    fi

    show_stats
    echo ""
    log "图片优化完成！"
    info "备份位置: $BACKUP_DIR"
}

main "$@"
