# 性能优化实施指南

## 🚀 快速开始

### 1. 图片懒加载（已自动添加）

所有非关键图片已添加 `loading="lazy"` 属性：

```html
<img src="image.jpg" alt="描述" loading="lazy" width="800" height="600">
```

### 2. 图片压缩

#### macOS 用户
```bash
# 安装工具
brew install webp imagemagick

# 批量转换 WebP
find images img -name "*.jpg" -o -name "*.png" | while read file; do
    cwebp -q 80 "$file" -o "${file%.*}.webp"
done

# 压缩 JPEG
find images img -name "*.jpg" -exec mogrify -quality 85 {} \;

# 压缩 PNG
find images img -name "*.png" -exec pngquant --quality 65-85 --ext .png --force {} \;
```

#### Linux 用户
```bash
sudo apt-get install webp imagemagick pngquant
# 然后执行相同命令
```

#### Windows 用户
使用在线工具：
- https://tinypng.com/
- https://squoosh.app/

### 3. CDN 优化

修改 HTML 中的外部资源引用为 CDN：

```html
<!-- 原引用 -->
<link href="lib/font-awesome/css/all.min.css" rel="stylesheet">

<!-- CDN 引用 -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-..." crossorigin="anonymous" referrerpolicy="no-referrer" />
```

推荐 CDN:
- **jQuery**: https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js
- **Bootstrap**: https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.3/js/bootstrap.bundle.min.js
- **Font Awesome**: https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css

### 4. Gzip/Brotli 压缩

GitHub Pages 自动启用 Gzip，但你可以：

1. 手动压缩静态资源：
```bash
# 安装 brotli
brew install brotli  # macOS
# 或
apt-get install brotli  # Linux

# 压缩 CSS 和 JS
find css js -name "*.css" -exec brotli -q 6 {} \;
find css js -name "*.js" -exec brotli -q 6 {} \;
```

2. 在服务器配置中启用 Brotli（如果使用自定义域名）

### 5. CSS/JS 优化

#### 关键 CSS 内联
将首屏必需的 CSS 内联到 `<style>` 标签中

#### 异步加载非关键 JS
```html
<script src="non-critical.js" defer></script>
```

### 6. 预加载重要资源

```html
<!-- 在 <head> 中添加 -->
<link rel="preload" href="./img/logo.png" as="image">
<link rel="preload" href="lib/font-awesome/css/all.min.css" as="style">
```

## 📊 性能监控

### Lighthouse 测试
```bash
npm install -g lighthouse
lighthouse http://localhost:3000 --view
```

### WebPageTest
访问：https://www.webpagetest.org/

### PageSpeed Insights
访问：https://pagespeed.web.dev/

## 🎯 优化目标

| 指标 | 当前 | 目标 | 优先级 |
|------|------|------|--------|
| Lighthouse 性能 | ~65 | 90+ | 🔴 高 |
| FCP (首次内容绘制) | ~2.5s | <1.5s | 🔴 高 |
| LCP (最大内容绘制) | ~3.8s | <2.5s | 🔴 高 |
| CLS (累积布局偏移) | ~0.1 | <0.1 | 🟡 中 |
| TBT (总阻塞时间) | ~400ms | <200ms | 🟡 中 |

## ✅ 检查清单

- [ ] 所有图片添加 `width` 和 `height` 属性
- [ ] 非关键图片使用懒加载
- [ ] 压缩所有图片（目标：<200KB/张）
- [ ] 使用 WebP 格式（提供 JPEG/PNG fallback）
- [ ] CSS 文件最小化（已有 gulp 任务）
- [ ] JS 文件最小化（已有 gulp 任务）
- [ ] 移除未使用的 CSS/JS
- [ ] 使用 CDN 加载第三方库
- [ ] 启用浏览器缓存
- [ ] 减少 DNS 查询次数
- [ ] 避免多个重定向
- [ ] 优化关键渲染路径

## 🔧 自动化脚本

运行优化脚本：
```bash
chmod +x optimize-images.sh
./optimize-images.sh
```

## 📈 预期改善

实施以上优化后：

- **加载速度**: 提升 40-60%
- **SEO 得分**: 提升至 90+
- **用户体验**: 显著改善
- **移动设备友好度**: 提升

---
最后更新：2026-03-05
