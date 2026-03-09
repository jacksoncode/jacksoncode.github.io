# 🖼️ OG 分享图片生成指南

## 什么是 OG 图片？

OG (Open Graph) 图片是社交媒体分享时显示的预览图，影响点击率和传播效果。

**推荐尺寸**: 1200 x 630 pixels (1.91:1 比例)

---

## 🎨 设计方案

### 方案一：使用 Canva（推荐）

1. 访问 https://www.canva.com/
2. 搜索 "Facebook Link Preview" 模板
3. 自定义设计：
   - 背景：渐变蓝色 (#3b82f6 → #2563eb)
   - 标题：CodeClub - 程序员的技术分享空间
   - 副标题：技术博客 | 学习资源 | 图书推荐
   - Logo：放在左上角或居中
4. 下载为 PNG 格式
5. 保存为 `img/og-image.png`

### 方案二：使用 Figma

1. 访问 https://www.figma.com/
2. 创建新文件，尺寸 1200x630
3. 设计元素：
   ```
   背景：线性渐变
   - 左上：#667eea
   - 右下：#764ba2
   
   文字内容：
   - 主标题：CodeClub (字体大小：72px, 粗体)
   - 副标题：程序员的技术分享空间 (字体大小：36px)
   - 标签：技术博客 · 学习资源 · AI工具 (字体大小：24px)
   
   Logo: 
   - 位置：右下角或居中顶部
   - 尺寸：120x120px
   ```
4. 导出为 PNG

### 方案三：使用 Photoshop

新建文档设置：
- 宽度：1200px
- 高度：630px
- 分辨率：72 dpi
- 颜色模式：RGB

设计建议：
- 使用品牌色（蓝色系）
- 保持简洁，留白适当
- 文字清晰可读
- 添加网站 Logo

---

## 🛠️ 自动生成工具

### 使用 Vercel OG Image

访问：https://og-playground.vercel.app/

代码示例：
```jsx
<div style={{
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  height: '100%',
  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  color: 'white',
  padding: '60px'
}}>
  <div style={{ textAlign: 'center' }}>
    <h1 style={{ fontSize: '72px', margin: '0 0 20px 0' }}>CodeClub</h1>
    <p style={{ fontSize: '36px', margin: '0 0 20px 0' }}>程序员的技术分享空间</p>
    <p style={{ fontSize: '24px', opacity: 0.8 }}>技术博客 · 学习资源 · AI工具</p>
  </div>
</div>
```

### 使用 Python + PIL

```python
from PIL import Image, ImageDraw, ImageFont

# 创建图片
img = Image.new('RGB', (1200, 630), color=(59, 130, 246))
draw = ImageDraw.Draw(img)

# 添加文字
font_title = ImageFont.truetype("arial.ttf", 72)
font_subtitle = ImageFont.truetype("arial.ttf", 36)

draw.text((600, 250), "CodeClub", fill="white", anchor="mm", font=font_title)
draw.text((600, 350), "程序员的技术分享空间", fill="lightblue", anchor="mm", font=font_subtitle)

# 保存图片
img.save('og-image.png')
```

---

## 📝 文案建议

### 版本 1 - 简洁版
```
主标题：CodeClub
副标题：程序员的技术分享空间
标签：技术博客 · 学习资源 · 图书推荐
```

### 版本 2 - 功能版
```
主标题：CodeClub
副标题：技术博客 | AI工具导航 | 编程学习
网址：jacksoncode.github.io
```

### 版本 3 - 特色版
```
主标题：CodeClub
副标题：记录学习笔记 · 分享编程心得 · 推荐优质资源
标语：程序员的成长伙伴
```

---

## ✅ 上传步骤

1. 生成图片后保存到本地
2. 重命名为 `og-image.png`
3. 上传到网站的 `img/` 目录
4. 验证 HTML 中的引用：
   ```html
   <meta property="og:image" content="https://jacksoncode.github.io/img/og-image.png">
   <meta name="twitter:image" content="https://jacksoncode.github.io/img/og-image.png">
   ```

---

## 🧪 测试工具

生成后使用以下工具验证：

1. **Facebook Debugger**
   https://developers.facebook.com/tools/debug/

2. **Twitter Card Validator**
   https://cards-dev.twitter.com/validator

3. **LinkedIn Post Inspector**
   https://www.linkedin.com/post-inspector/

4. **Social Share Preview**
   https://www.socialsharepreview.com/

---

## 💡 最佳实践

- ✅ 图片大小控制在 200KB 以内
- ✅ 使用清晰的无衬线字体
- ✅ 保持高对比度（深色背景 + 浅色文字）
- ✅ 包含品牌 Logo
- ✅ 文字精简（不超过 3 行）
- ✅ 符合品牌色调
- ✅ 移动端友好（在小屏幕上也清晰）

---

## 🎯 快速模板

### 纯色背景模板
```
背景：#3b82f6（蓝色）
文字：白色
内容：居中显示标题和副标题
```

### 渐变背景模板
```
背景：线性渐变 135deg
- 起始：#667eea
- 结束：#764ba2
文字：白色带阴影
```

### 图案背景模板
```
背景：品牌色 + 几何图案（透明度 10%）
文字：白色居中
Logo: 右上角或底部居中
```

---

**最后更新**: 2026-03-05  
**预计完成时间**: 30 分钟
