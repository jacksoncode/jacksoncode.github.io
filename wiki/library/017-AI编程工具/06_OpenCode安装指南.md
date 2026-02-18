# OpenCode 安装及使用指南

OpenCode 是一个由 Anthropic 推出的 AI 编程助手 CLI 工具，集成在 Claude Code 中，为开发者提供强大的编码辅助能力。

## 安装

### 环境要求

- Node.js 18+
- npm 或 yarn

### 安装步骤

```bash
# 使用 npm 全局安装
npm install -g opencode

# 验证安装
opencode --version
```

### 配置

首次使用需要配置 API Key：

```bash
# 设置 Anthropic API Key
opencode config set ANTHROPIC_API_KEY your_api_key
```

## 基本使用

### 启动 OpenCode

```bash
# 在当前目录启动
opencode

# 指定项目目录
opencode /path/to/project
```

### 常用命令

```bash
# 查看帮助
opencode --help

# 初始化新项目
opencode init

# 运行特定任务
opencode task "你的任务描述"

# 交互式模式
opencode chat
```

## 核心功能

### 1. 智能代码补全

OpenCode 能够理解项目上下文，提供精准的代码补全建议。

### 2. 代码解释与重构

```bash
# 解释代码功能
opencode explain /path/to/file

# 建议代码改进
opencode review /path/to/file
```

### 3. 自动生成测试

```bash
# 为文件生成测试
opencode test /path/to/file
```

### 4. 项目分析

```bash
# 分析项目结构
opencode analyze

# 查看项目依赖
opencode deps
```

## 配置选项

OpenCode 配置文件位于 `~/.opencode/config.json`：

```json
{
  "model": "claude-3-5-sonnet-20241022",
  "maxTokens": 4096,
  "temperature": 0.7,
  "projectContext": true
}
```

## 常见问题

### Q: 如何切换模型？

```bash
opencode config set model claude-3-opus-20240229
```

### Q: 如何查看当前配置？

```bash
opencode config list
```

### Q: 如何更新 OpenCode？

```bash
npm update -g opencode
```

## 与 Claude Code 集成

OpenCode 与 Claude Code 深度集成，可以通过以下方式调用：

```
在 Claude Code 中使用 /opencode 命令启动 OpenCode
```

## 最佳实践

1. **项目初始化时使用** - 让 OpenCode 了解项目结构
2. **复杂任务使用 task 命令** - 获得更详细的处理
3. **定期更新** - 保持最新功能和安全修复
4. **配置项目级设置** - 在项目根目录创建 `.opencode.json`

## 相关链接

- [OpenCode 官方文档](https://opencode.ai)
- [Anthropic API 文档](https://docs.anthropic.com)
