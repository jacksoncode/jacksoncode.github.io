# Claude Code 使用指南

## 安装
```powershell
npm install -g @anthropic-ai/claude-code
```

## 配置
```bash
# 基础认证配置
export ANTHROPIC_API_KEY="your-api-key"

# 多模型配置
export CLAUDE_MODELS="claude-3-opus,claude-3-sonnet,claude-3-haiku"
export ANTHROPIC_DEFAULT_MODEL="claude-3-sonnet"

# 切换模型
claude config set model=claude-3-haiku

# 查看可用模型列表
claude models list

# 为不同项目设置不同模型
claude project set --model=claude-3-opus --project-name="complex-project"
claude project set --model=claude-3-haiku --project-name="simple-project"

# 设置模型参数
claude config set max_tokens=4000
claude config set temperature=0.3
```

## 使用技巧
1. 使用 `/plan` 模式进行任务分步规划
2. 利用 `Ctrl + R` 快速调出历史记录
3. 通过 `// @context` 注释提供代码上下文

## 常见问题
<mcfile name="常见问题" path="d:\BaiduSyncdisk\Creator\AI_Coding_wiki\01_Claude_Code.md"></mcfile>

## 示例
```claude
/create 实现JWT身份验证中间件
使用express框架，有效期24小时
包含token刷新机制
```