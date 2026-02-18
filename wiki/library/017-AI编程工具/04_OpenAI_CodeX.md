# OpenAI CodeX 使用指南

## 安装
```powershell
pip install openai-codex-cli
```

## 配置
```bash
# 基础认证配置
export OPENAI_API_KEY="sk-your-key-here"
codex config set engine="davinci-codex"

# 多模型配置
export CODEX_MODELS="davinci-codex,cushman-codex,code-davinci-002,code-cushman-001"
export CODEX_DEFAULT_MODEL="davinci-codex"

# 切换模型
codex config set engine="code-davinci-002"

# 查看可用模型列表
codex models list

# 为不同编程语言设置不同模型
codex config set --language=python --model="davinci-codex"
codex config set --language=javascript --model="cushman-codex"

# 设置模型参数
codex config set temperature=0.5
codex config set max_tokens=2000
```

## 高效技巧
1. 使用 `--temperature 0.3` 控制输出创造性
2. 通过 `@context:file.js` 语法附加代码上下文
3. 使用批处理模式处理多个请求

## 常见问题
<mcfile name="API限制" path="d:\BaiduSyncdisk\Creator\AI_Coding_wiki\04_OpenAI_CodeX.md"></mcfile>

## 示例
```bash
codex generate "用Python实现快速排序 要求生成单元测试" --max-tokens 1500
```