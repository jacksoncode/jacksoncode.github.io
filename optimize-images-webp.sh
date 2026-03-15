#!/bin/bash

# 图片 WebP 格式转换脚本
# 将现有 JPG/PNG 图片转换为 WebP 格式，提升加载性能

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置
IMG_DIR="./img"
IMAGES_DIR="./images"
QUALITY=85  # WebP 质量 (0-100)

echo -e "${GREEN}🚀 开始图片 WebP 格式转换...${NC}"

# 检查是否安装了 cwebp
if ! command -v cwebp &> /dev/null; then
    echo -e "${YELLOW}⚠️  cwebp 未安装，正在安装...${NC}"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install webp
        else
            echo -e "${RED}❌ 请先安装 Homebrew: https://brew.sh/${NC}"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo apt-get update && sudo apt-get install -y webp
    else
        echo -e "${RED}❌ 不支持的操作系统${NC}"
        exit 1
    fi
fi

# 转换函数
convert_to_webp() {
    local file=$1
    local dir=$(dirname "$file")
    local filename=$(basename "$file")
    local name="${filename%.*}"
    local webp_file="${dir}/${name}.webp"
    
    # 跳过已经是 WebP 的文件
    if [[ "$filename" == *.webp ]]; then
        echo -e "${YELLOW}⊘ 跳过 WebP 文件: $filename${NC}"
        return
    fi
    
    # 检查是否已经存在 WebP 版本
    if [[ -f "$webp_file" ]]; then
        # 比较文件修改时间
        if [[ "$file" -nt "$webp_file" ]]; then
            echo -e "${YELLOW}🔄 更新 WebP 文件: $filename${NC}"
        else
            echo -e "${GREEN}✓ WebP 已存在: $filename${NC}"
            return
        fi
    fi
    
    echo -e "${GREEN}🔄 转换: $filename -> ${name}.webp${NC}"
    cwebp -q "$QUALITY" "$file" -o "$webp_file" 2>/dev/null || {
        echo -e "${RED}❌ 转换失败: $filename${NC}"
        return 1
    }
    
    # 显示文件大小对比
    if [[ -f "$webp_file" ]]; then
        local original_size=$(du -h "$file" | cut -f1)
        local webp_size=$(du -h "$webp_file" | cut -f1)
        echo -e "${GREEN}  → $original_size -> $webp_size${NC}"
    fi
}

# 主处理流程
echo -e "${YELLOW}📂 处理 img/ 目录...${NC}"
if [[ -d "$IMG_DIR" ]]; then
    find "$IMG_DIR" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) | while read -r file; do
        convert_to_webp "$file"
    done
else
    echo -e "${RED}❌ 目录不存在: $IMG_DIR${NC}"
fi

echo -e "${YELLOW}📂 处理 images/ 目录...${NC}"
if [[ -d "$IMAGES_DIR" ]]; then
    find "$IMAGES_DIR" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) | while read -r file; do
        convert_to_webp "$file"
    done
else
    echo -e "${RED}❌ 目录不存在: $IMAGES_DIR${NC}"
fi

echo -e "${GREEN}✅ WebP 转换完成！${NC}"
echo -e "${YELLOW}💡 提示：记得在 HTML 中添加 picture 标签或使用 WebP 文件${NC}"