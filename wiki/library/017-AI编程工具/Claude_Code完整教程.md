# Claude Code 完整使用指南

## 1. 简介

Claude Code 是 Anthropic 官方推出的命令行工具，为开发者提供强大的 AI 编程辅助能力。它深度集成 Claude 模型，可以帮助你：

- 编写、编辑、重构代码
- 解释代码逻辑
- 运行测试和调试
- 执行 Git 操作
- 自动化重复任务

## 2. 安装与配置

### 安装

```bash
# 使用 npm 安装
npm install -g @anthropic-ai/claude-code

# 或使用 Homebrew (macOS)
brew install claude-code

# 验证安装
claude --version
```

### 配置 API Key

```bash
# 设置 Anthropic API Key
export ANTHROPIC_API_KEY="sk-ant-xxxxx"

# 永久保存到配置文件
echo 'export ANTHROPIC_API_KEY="your-key"' >> ~/.bashrc
source ~/.bashrc
```

## 3. 基本使用

### 启动会话

```bash
# 在当前目录启动
claude

# 指定项目目录
claude /path/to/project

# 指定模型
claude --model claude-3-opus

# 查看帮助
claude --help
```

### 交互式会话

```
用户: @claude 你好
Claude: 你好！我是 Claude Code，有什么可以帮你的？

用户: 帮我创建一个新的 Python Flask 项目
Claude: 我来帮你创建一个 Flask 项目...
```

## 4. 核心命令

### 文件操作

```bash
# 创建文件
/claude 创建 app.py 文件，使用 Flask 实现一个 REST API

# 编辑文件
/claude 修改 app.py 添加错误处理

# 查看文件
/claude 解释 main.py 的代码逻辑

# 搜索文件
/claude 找到项目中所有的配置文件
```

### Git 操作

```bash
# 提交代码
/claude 提交这次修改，commit message 写 "添加用户认证功能"

/claude 创建新分支 feature/payment

/claude 合并 feature/payment 到 main
```

### 代码执行

```bash
# 运行测试
/claude 运行所有测试

# 执行脚本
/claude 运行 python main.py

# 安装依赖
/claude 安装项目依赖
```

## 5. 模式与技巧

### Plan 模式

用于大型任务的规划和分解：

```bash
# 启动规划模式
/plan

# 输入任务描述
用户: 实现一个用户认证系统，包括登录、注册、密码重置

# Claude 会分析任务，创建计划
Claude: 我来为你规划这个用户认证系统的实现：

## 实现计划

### 阶段 1: 基础设置
- [ ] 创建用户数据模型
- [ ] 设置数据库连接
- [ ] 配置密码哈希

### 阶段 2: 核心功能
- [ ] 实现注册接口
- [ ] 实现登录接口
- [ ] 实现 JWT 认证

### 阶段 3: 高级功能
- [ ] 密码重置邮件
- [ ] 双因素认证
- [ ] 登录日志

确认后我将开始实现...
```

### /claude 命令参考

| 命令 | 功能 | 示例 |
|------|------|------|
| `/claude` | 开始新任务 | `/claude 实现登录功能` |
| `/plan` | 规划模式 | `/plan` |
| `/review` | 代码审查 | `/review` |
| `/test` | 生成测试 | `/test` |
| `/fix` | 修复错误 | `/fix <错误信息>` |
| `/explain` | 解释代码 | `/explain` |
| `/refactor` | 重构代码 | `/refactor` |
| `/git` | Git 操作 | `/git commit` |

## 6. 代码上下文

### @ 引用文件

```bash
# 引用单个文件
/claude @app.py 解释这个文件的结构

# 引用多个文件
/claude @app.py @models/user.py 实现用户模块

# 引用文件夹
/claude @src/ 重构这个模块
```

### @ 引用 git diff

```bash
# 引用当前更改
git diff | /claude 审查这次修改

# 引用特定提交
git diff abc123..def456 | /claude 分析代码变更
```

### @ 引用错误信息

```bash
# 粘贴错误日志
/claude 修复这个错误：
Error: TypeError: Cannot read property 'map' of undefined
    at Array.map (<anonymous>)
    at processData (app.js:45)
```

## 7. 高级配置

### 模型选择

```bash
# 命令行指定
claude --model claude-3-opus

# 会话中切换
Claude: 请切换到 haiku 模型，这个简单任务不需要 opus
/model claude-3-haiku
```

### 模型参数

```bash
# 设置温度（创造性）
/config temperature=0.7

# 设置最大 token
/config max_tokens=4000

# 查看当前配置
/config list
```

### 项目级配置

```bash
# 为项目创建配置
claude project init

# 设置项目级模型
claude project set --model=claude-3-sonnet --project-name="my-project"

# 查看项目列表
claude projects list
```

## 8. 工作流集成

### VS Code 集成

```bash
# 安装 VS Code 扩展
code --install-extension anthropic.claude-code

# 扩展功能：
# - 内联代码建议
# - 聊天面板
# - 终端集成
```

### Git Hooks

```bash
# 在 pre-commit 时自动审查
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
claude --review --quiet
EOF
chmod +x .git/hooks/pre-commit
```

### CI/CD 集成

```yaml
# .github/workflows/ci.yml
name: Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Claude Code Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude --review --output=review.md
          cat review.md
```

## 9. 最佳实践

### 1. 提供清晰的上下文

```bash
# ❌ 太模糊
/实现登录功能

# ✅ 具体明确
/实现用户登录功能：
- 使用 JWT 认证
- 包含邮箱/密码验证
- 实现"记住我"功能
- 返回用户信息和 token
```

### 2. 分步骤处理复杂任务

```bash
# ❌ 一次性完成所有功能
/实现整个电商系统

# ✅ 分步骤进行
/plan
# 阶段1: 用户模块
# 阶段2: 商品模块
# 阶段3: 订单模块
```

### 3. 利用代码审查

```bash
# 提交前审查
/git commit ...
/review
```

### 4. 组合使用命令

```bash
# 一次性完成多个操作
/claude @app.py 重构这个文件，添加类型注解，然后运行测试
```

## 10. 常见问题

### Q: 如何切换模型？

```bash
/model claude-3-sonnet
```

### Q: 如何查看对话历史？

```bash
# Ctrl + R 打开历史记录
Ctrl + R
```

### Q: 如何终止正在执行的任务？

```bash
Ctrl + C
```

### Q: 如何保存会话？

```bash
# Claude Code 会自动保存会话
# 查看历史会话
claude sessions list

# 恢复会话
claude session resume <session-id>
```

## 11. 与 OpenCode 的区别

| 特性 | Claude Code | OpenCode |
|------|-------------|----------|
| 开发者 | Anthropic | Anthropic |
| 集成度 | 更深入 | 基础集成 |
| 文件编辑 | 强 | 中等 |
| Git 集成 | 强 | 中等 |
| Skill 系统 | 支持 | 支持 |

> **提示**：OpenCode 是 Claude Code 的 CLI 版本，功能略有差异但核心能力相同。

## 12. 相关资源

- [官方文档](https://docs.anthropic.com/claude-code)
- [GitHub 仓库](https://github.com/anthropics/claude-code)
- [提示词模板](https://github.com/anthropics/claude-code/tree/main/prompts)
