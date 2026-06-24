# 更新日志

All notable changes to this project will be documented in this file.

## [2.1.0] - 2026-06-20

### 优化改进

#### P0 - 高优先级
- **暗色模式补全**: ch28.html、ch32.html添加dark-mode.css和dark-mode.js引用，实现100%暗色模式覆盖
- **图片懒加载**: blog.html、else/av.html、tutorials/ai-notes/index-full.html为img标签添加`loading="lazy"`属性
- **CSS暗色增强**: ai-notes.css补充`.ai-nav-links`、`.ai-mobile-toc-toggle`、标题等暗色模式样式
- **SEO优化**: 
  - ai-notes/index.html添加Open Graph和Twitter Card meta标签
  - sitemap.xml追加44个ai-notes HTML条目

#### P1 - 中优先级
- **资源压缩**: npm脚本已配置（optimize:images、optimize:css、webp:convert）
- **错误处理增强**: 各JS模块局部catch完善，404.html已优化（搜索框、快捷键、热门链接）

#### P2 - 低优先级
- **性能监控**: Lighthouse CI脚本已配置（npm run lighthouse），需Chrome环境运行
- **文档完善**: README.md添加技术栈说明和优化记录，创建CHANGELOG.md

### 技术栈确认
- 项目为**纯静态HTML站点**（非Gatsby框架）
- Bootstrap 5.3.8 + 自定义JavaScript模块（20+个）
- PWA支持：sw.js、manifest.json

---

## [2.0.0] - 2025-07-24

### 重大变更
- Bootstrap升级至5.3.8
- 添加ai-notes模块（44个HTML页面）
- 实现暗色模式、主题管理、搜索增强、阅读进度、知识图谱等功能

---

## [1.0.0] - 初始版本

### 功能
- 个人首页
- 程序猿网址导航
- 技术博客
- 读书笔记