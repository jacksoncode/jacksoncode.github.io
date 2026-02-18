# iFlow CLI 使用指南

## 安装
```powershell
npm install -g iflow-cli
```

## 配置
```bash
# 基础API配置
iflow config set --api-endpoint=https://api.iflow.ai/v2

# 多模型配置
iflow config set models="claude,gemini,qwen,codex"
iflow config set default-model="claude"

# 切换模型
iflow config set model="gemini"

# 查看可用模型列表
iflow models list

# 配置不同模型的API密钥
iflow config set claude-api-key="your-claude-key"
iflow config set gemini-api-key="your-gemini-key"
iflow config set qwen-api-key="your-qwen-key"
iflow config set openai-api-key="your-openai-key"

# 为不同项目设置不同模型
iflow workspace create --name="web-project" --model="claude"
iflow workspace create --name="mobile-project" --model="qwen"

# 模型优先级设置
iflow config set model-priority="claude,gemini,qwen,codex"
```

## 高效技巧
1. 使用工作区(workspace)管理多项目上下文
2. 通过管道组合多个AI工具输出
3. 使用 `--watch` 模式实时重构代码

## 常见问题
<mcfile name="依赖冲突" path="d:\BaiduSyncdisk\Creator\AI_Coding_wiki\05_iFlow_CLI.md"></mcfile>

## 示例
```bash
iflow compose "claude:实现登录功能" "qwen:生成单元测试" --output login-module
```