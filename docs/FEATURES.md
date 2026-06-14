# 📘 功能扩展使用文档

## 🎯 功能概览

本项目新增了以下功能模块，提升用户体验和网站性能。

---

## 📦 P0 - 性能优化功能

### 1. Lunr.js 全文搜索

**文件**: `js/lunr-search.js`

**功能**:
- ✅ 高性能全文搜索引擎
- ✅ 智能搜索建议
- ✅ 搜索历史记录
- ✅ 相关内容推荐

**使用方法**:
```javascript
// 执行搜索
LunrSearchAPI.search('关键词', { limit: 10 });

// 高级搜索
LunrSearchAPI.advancedSearch('关键词', { category: 'Python' });

// 获取建议
LunrSearchAPI.getSuggestions('部分关键词');

// 相关文档
LunrSearchAPI.getRelatedDocuments('文档ID', 5);
```

**快捷键**:
- `Ctrl/Cmd + K`: 打开搜索
- `ESC`: 关闭搜索
- `↑/↓`: 选择结果
- `Enter`: 打开结果

---

### 2. 文章分类筛选系统

**文件**: `js/article-filter.js`

**功能**:
- ✅ 类别筛选 (Python, 前端, React等)
- ✅ 难度筛选 (入门, 进阶, 高级)
- ✅ 标签多选
- ✅ 实时计数统计

**使用场景**:
- 博客页面自动加载筛选面板
- 支持多条件组合筛选
- 响应式设计，移动端友好

---

### 3. 搜索历史增强

**文件**: `js/search-enhanced.js`

**功能**:
- ✅ 自动保存搜索历史
- ✅ 热门搜索推荐
- ✅ 一键清除历史
- ✅ LocalStorage持久化

---

## 🎨 P1 - 体验优化功能

### 4. 阅读进度条 + 目录导航

**文件**: `js/reading-progress.js`

**功能**:
- ✅ 页面顶部进度条 (0-100%)
- ✅ 侧边目录导航 (H2-H4标题)
- ✅ 阅读时间估算
- ✅ 当前章节高亮
- ✅ 平滑滚动定位

**自动显示**:
- 仅在文章页面激活
- 自动提取文章标题生成目录
- 响应式折叠设计

---

### 5. 三主题切换系统

**文件**: `js/theme-manager.js`

**主题选项**:
1. **亮色模式** - 白色背景，适合白天使用
2. **暗色模式** - 深色背景，适合夜间使用，保护眼睛
3. **护眼模式** - 绿色背景，减少蓝光，长时间阅读推荐

**使用方法**:
```javascript
// 切换主题
ThemeManagerAPI.applyTheme('dark');

// 循环切换
ThemeManagerAPI.cycleTheme();

// 获取当前主题
ThemeManagerAPI.getCurrentTheme();
```

**快捷操作**:
- 点击导航栏主题按钮切换
- 下拉菜单选择具体主题
- 自动保存用户偏好

---

### 6. 面包屑导航

**文件**: `js/breadcrumb-nav.js`

**功能**:
- ✅ 自动生成页面层级导航
- ✅ 首页 > 博客 > 文章标题
- ✅ 快速返回上级页面
- ✅ SEO友好结构

**自动位置**:
- 页面顶部显示
- 响应式适配

---

## 🤖 P2 - AI特色功能

### 7. AI智能摘要生成器

**文件**: `js/ai-enhancer.js`

**功能**:
- ✅ 自动生成文章摘要
- ✅ 关键词提取
- ✅ 一键复制摘要
- ✅ 重新生成功能
- ✅ 渐变背景卡片设计

**使用场景**:
- 文章页面顶部显示
- 快速了解文章核心内容
- 支持复制分享

---

### 8. 相关文章智能推荐

**文件**: `js/ai-enhancer.js`

**算法**:
- 关键词匹配权重 × 2
- 类别相同权重 + 5
- 按相似度排序
- 推荐5篇最相关文章

**显示位置**:
- 文章页面底部
- 网格卡片布局
- 标签高亮显示

---

## 📊 P3 - 高级可视化功能

### 9. 知识图谱可视化

**文件**: `js/knowledge-graph.js`

**功能**:
- ✅ D3.js力导向图
- ✅ 知识节点可视化
- ✅ 关联关系展示
- ✅ 节点拖拽交互
- ✅ 缩放控制
- ✅ 类别颜色编码

**交互操作**:
- 拖拽节点调整位置
- 点击节点跳转文章
- 放大/缩小按钮控制
- 重置布局按钮

**显示位置**:
- 导航页面(nav.html)底部
- 600px高度画布

---

## 🔧 功能管理器

**文件**: `js/feature-manager.js`

**功能状态监控**:
```javascript
// 查看所有功能状态
FeatureManagerAPI.getAllStatus();

// 启用/禁用功能
FeatureManagerAPI.enable('knowledgeGraph');
FeatureManagerAPI.disable('aiEnhancer');

// 查看单个功能状态
FeatureManagerAPI.getStatus('lunrSearch');
```

---

## 🎛️ 配置选项

### 功能开关
所有功能默认启用，可通过FeatureManagerAPI动态控制。

### 页面限制
- `readingProgress`: 仅文章页面
- `aiEnhancer`: 仅文章页面
- `knowledgeGraph`: 仅导航页面

### 性能优化
- Lunr索引本地缓存
- 懒加载非必要功能
- 响应式资源适配

---

## 🚀 快速测试

### 1. 搜索功能测试
```bash
# 打开首页
# 按 Ctrl/Cmd + K 打开搜索
# 输入关键词测试
```

### 2. 主题切换测试
```bash
# 点击导航栏主题按钮
# 切换到护眼模式
# 检查背景颜色变化
```

### 3. 知识图谱测试
```bash
# 访问 nav.html
# 查看页面底部知识图谱
# 拖拽节点测试交互
```

---

## 📝 文件清单

| 文件 | 大小 | 功能 |
|------|------|------|
| lunr-search.js | 8.5KB | 全文搜索 |
| article-filter.js | 10.5KB | 文章筛选 |
| reading-progress.js | 11.5KB | 阅读进度+目录 |
| theme-manager.js | 6.6KB | 三主题切换 |
| breadcrumb-nav.js | 5.7KB | 面包屑导航 |
| ai-enhancer.js | 11.3KB | AI摘要+推荐 |
| knowledge-graph.js | 11.8KB | 知识图谱 |
| feature-manager.js | 4.5KB | 功能管理器 |

---

## 🔗 API接口汇总

```javascript
// Lunr搜索API
LunrSearchAPI.search(query, options)
LunrSearchAPI.advancedSearch(query, filters)
LunrSearchAPI.getSuggestions(query)

// 主题管理API
ThemeManagerAPI.applyTheme(themeName)
ThemeManagerAPI.cycleTheme()
ThemeManagerAPI.getCurrentTheme()

// 功能管理API
FeatureManagerAPI.enable(featureName)
FeatureManagerAPI.disable(featureName)
FeatureManagerAPI.getStatus(featureName)
FeatureManagerAPI.getAllStatus()
```

---

## 🎯 下一步建议

1. **测试所有功能** - 在本地环境运行测试
2. **性能优化** - 使用Lighthouse评估
3. **用户反馈** - 收集使用体验
4. **持续迭代** - 根据反馈改进功能

---

## 📞 支持与反馈

如有问题或建议，请:
- 查看浏览器Console日志
- 检查FeatureManagerAPI.getAllStatus()
- 提交Issue到GitHub仓库

---

**版本**: 2.1.0+
**更新日期**: 2026年6月7日
**维护者**: Jackson