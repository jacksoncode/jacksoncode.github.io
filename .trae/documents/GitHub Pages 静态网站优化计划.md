## 优化计划

### 1. 安全性优化
- **创建 `.gitignore`** - 排除 `.env`、`__pycache__/`、`venv/`、`.idea/` 等敏感/缓存文件

### 2. SEO 优化
- **修复 HTML 语言** - 将 `lang="en"` 改为 `lang="zh-CN"`
- **添加 meta 描述** - 为每个页面添加合适的 description 和 keywords
- **图片 alt 属性** - 为 book.html 中的图书封面添加 alt 描述

### 3. 功能完善
- **完善 book.js** - 实现图书分类筛选功能（前端 JavaScript 实现）
- **优化联系表单** - 使用 Formspree/Static Forms 等免费静态表单服务

### 4. 涉及文件
- 新建: `.gitignore`
- 修改: `index.html`, `about.html`, `book.html`, `contact.html`, `nav.html`, `blog.html`
- 修改: `js/book.js`
- 修改: `css/book.css`（如需要）