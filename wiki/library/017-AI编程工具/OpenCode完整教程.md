# OpenCode 完整使用指南

## 1. 简介

OpenCode 是由 Anthropic 推出的 AI 编程 CLI 工具，为开发者提供强大的智能编程辅助能力。它可以：

- 理解和分析代码库
- 生成、编辑、重构代码
- 执行命令行操作
- 运行测试和调试
- 自动化开发任务

## 2. 安装

### 环境要求

- Node.js 18.0 或更高版本
- npm 或 yarn 包管理器
- Anthropic API Key（或其他支持的模型 API Key）

### 安装步骤

```bash
# 使用 npm 全局安装
npm install -g opencode

# 验证安装
opencode --version

# 查看帮助
opencode --help
```

## 3. 快速开始

### 配置 API Key

```bash
# 设置 Anthropic API Key
opencode config set ANTHROPIC_API_KEY your_api_key

# 或设置 OpenAI API Key
opencode config set OPENAI_API_KEY your_api_key

# 查看当前配置
opencode config list
```

### 启动会话

```bash
# 在当前目录启动
opencode

# 指定项目目录
opencode /path/to/project

# 指定模型
opencode --model claude-3-5-sonnet-20241022
```

## 4. 核心功能

### 4.1 智能代码编辑

```bash
# 启动交互式编辑模式
opencode

# 在会话中请求代码生成
> 帮我创建一个 Flask REST API，包含用户认证

# 编辑现有代码
> 修改 app.py 中的登录函数，添加邮箱验证

# 代码重构
> 重构 UserService 类，提取接口
```

### 4.2 代码理解

```bash
# 解释代码
opencode explain /path/to/file.py

# 分析代码库结构
opencode analyze

# 查看项目依赖
opencode deps

# 查找特定功能
opencode search "authentication"
```

### 4.3 自动测试

```bash
# 为文件生成测试
opencode test /path/to/file.py

# 运行并分析测试结果
opencode test --watch

# 生成测试覆盖率报告
opencode test --coverage
```

### 4.4 代码审查

```bash
# 审查文件
opencode review /path/to/file.py

# 审查整个项目
opencode review

# 只关注安全问题
opencode review --security

# 输出审查报告
opencode review --output report.md
```

## 5. 命令参考

### 全局选项

| 选项 | 说明 |
|------|------|
| `--model` | 指定使用的模型 |
| `--temperature` | 设置创造性参数 (0-1) |
| `--max-tokens` | 最大输出 token 数 |
| `--output` | 输出到文件 |
| `--quiet` | 静默模式 |

### 子命令

| 命令 | 功能 |
|------|------|
| `opencode init` | 初始化新项目 |
| `opencode chat` | 交互式聊天模式 |
| `opencode task` | 执行特定任务 |
| `opencode explain` | 解释代码 |
| `opencode review` | 代码审查 |
| `opencode test` | 生成测试 |
| `opencode analyze` | 分析项目结构 |
| `opencode search` | 搜索代码 |
| `opencode config` | 管理配置 |
| `opencode skills` | 管理 Skills |

## 6. Skills 系统

OpenCode 支持 Skills 扩展系统，可以加载自定义技能。

### 内置 Skills

```bash
# 列出可用 Skills
opencode skills list

# 使用特定 Skill
opencode --skill python
```

### 自定义 Skills

```bash
# 安装 Skill
opencode skills install /path/to/skill

# 创建新 Skill
opencode skills create my-skill

# 查看 Skill 详情
opencode skills info my-skill
```

### Skill 文件结构

```
my-skill/
├── SKILL.md          # Skill 定义文件
├── prompts/          # 提示词模板
├── scripts/          # 执行脚本
└── config.json      # 配置文件
```

## 7. 配置

### 全局配置

配置文件位置：`~/.opencode/config.json`

```json
{
  "model": "claude-3-5-sonnet-20241022",
  "maxTokens": 4096,
  "temperature": 0.7,
  "projectContext": true,
  "autoSuggest": true,
  "skills": {
    "enabled": ["python", "web"]
  }
}
```

### 项目级配置

在项目根目录创建 `.opencode.json`：

```json
{
  "model": "claude-3-5-sonnet-20241022",
  "exclude": ["node_modules", "dist", ".git"],
  "skills": ["python", "fastapi"],
  "rules": {
    "maxFileSize": "1MB",
    "autoFormat": true
  }
}
```

## 8. 使用技巧

### 8.1 有效提问

```bash
# ❌ 太模糊
> 帮我改一下代码

# ✅ 具体明确
> 在 UserService 类中添加分页功能，
# 接受 page 和 pageSize 参数，返回分页结果

# ❌ 缺少上下文
> 这个错误怎么修复

# ✅ 提供完整信息
> 修复这个错误：
# TypeError: Cannot read property 'map' of undefined
# at processData (app.js:45)
# 数据来源是 API 返回的 JSON
```

### 8.2 组合任务

```bash
# 一次性完成多个任务
> 1. 创建 User 模型
> 2. 实现 CRUD 接口
> 3. 添加单元测试

# 使用分步骤
> 第一步：创建 User 模型
> 确认后继续下一步
```

### 8.3 利用上下文

```bash
# 引用文件
> 分析 @src/auth/login.ts 的逻辑

# 引用多个文件
> 比较 @src/service/user.ts 和 @src/service/admin.ts 的差异

# 引用错误
> 帮我调试这个错误：
> [粘贴完整错误日志]
```

## 9. 集成工具

### 9.1 Git 集成

```bash
# 在提交前审查
git add .
opencode review --diff

# 生成提交信息
opencode git commit "实现了用户认证功能"

# 分析代码变更
opencode git analyze --diff
```

### 9.2 VS Code 集成

安装 VS Code 扩展后：

- 内联代码建议
- 侧边栏聊天面板
- 终端快速访问

### 9.3 CI/CD 集成

```yaml
# GitHub Actions 示例
name: Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run OpenCode Review
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          npx opencode review --output review.md
      - name: Upload Review
        uses: actions/upload-artifact@v3
        with:
          name: code-review
          path: review.md
```

## 10. 常见问题

### Q: 如何切换模型？

```bash
opencode config set model claude-3-opus-20240229
```

### Q: 如何查看历史对话？

```bash
opencode history
opencode history --session <session-id>
```

### Q: 如何导出对话记录？

```bash
opencode export --session <session-id> --format md
```

### Q: 如何禁用自动建议？

```bash
opencode config set autoSuggest false
```

### Q: 支持哪些 API 提供商？

- Anthropic (Claude)
- OpenAI (GPT-4)
- Google (Gemini)
- 本地模型 (Ollama)

## 11. 与 Claude Code 的关系

| 特性 | OpenCode | Claude Code |
|------|----------|-------------|
| CLI 工具 | ✅ | ✅ |
| 深度 Git 集成 | 中等 | 强 |
| 代码编辑能力 | ✅ | ✅ |
| Skill 系统 | ✅ | ✅ |
| MCP 支持 | ✅ | ✅ |
| 开发者 | Anthropic | Anthropic |

> **说明**：OpenCode 是 Claude Code 的开源版本，核心能力相同，但 Claude Code 在 Git 集成和 IDE 深度集成方面更强。

## 12. 最佳实践

1. **提供清晰上下文**：包含文件名、代码片段、错误信息
2. **分步骤执行**：复杂任务分解为多个步骤
3. **利用 Skills**：使用专门的 Skill 处理特定任务
4. **代码审查**：重要功能提交前进行审查
5. **迭代优化**：根据结果不断调整需求

## 13. 相关资源

- [官方文档](https://opencode.ai/docs)
- [GitHub 仓库](https://github.com/anthropics/opencode)
- [Skills 市场](https://opencode.ai/skills)
- [Discord 社区](https://discord.gg/opencode)
