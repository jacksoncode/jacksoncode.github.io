#!/bin/bash
# 统一页面优化脚本 - 整合 CDN 替换、SEO 标签、preconnect 等功能
# 用法: ./scripts/optimize-pages.sh [--cdn] [--seo] [--all]

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}✅ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
info() { echo -e "${GREEN}📄 $1${NC}"; }

# 更新 CDN 链接
update_cdn() {
    local files=("about.html" "contact.html" "book.html")
    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            cp "$file" "${file}.bak" 2>/dev/null || true
            sed -i '' 's|<link href="lib/font-awesome/css/all.min.css" rel="stylesheet">|<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" crossorigin="anonymous" referrerpolicy="no-referrer" />|g' "$file"
            sed -i '' 's|<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>|<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n    <link rel="preconnect" href="https://cdnjs.cloudflare.com">|g' "$file"
            log "CDN 优化: $file"
        fi
    done
}

# 更新 SEO 标签
update_seo() {
    local files=("nav.html" "about.html" "contact.html" "book.html" "blog.html")
    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            cp "$file" "${file}.bak" 2>/dev/null || true
            sed -i '' 's|<meta name="author" content="Jackson">|<meta name="author" content="Jackson">\n    <meta name="robots" content="index, follow">\n    <meta property="og:type" content="website">\n    <meta property="og:locale" content="zh_CN">\n    <meta property="og:site_name" content="CodeClub">|g' "$file"
            log "SEO 优化: $file"
        fi
    done
}

# 主流程
main() {
    echo -e "${GREEN}🔄 页面优化脚本${NC}"
    echo "=================="

    if [[ "$1" == "--cdn" || "$1" == "--all" || -z "$1" ]]; then
        update_cdn
    fi
    if [[ "$1" == "--seo" || "$1" == "--all" || -z "$1" ]]; then
        update_seo
    fi

    log "页面优化完成！"
    warn "请手动检查页面并删除 .bak 备份文件"
}

main "$@"
