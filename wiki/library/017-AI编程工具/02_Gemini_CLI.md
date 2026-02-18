# Gemini CLI 使用指南

## 安装
```powershell
npm install -g @google/gemini-cli
```

## 配置
```bash
# 基础认证配置
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"
gemini auth login

# 多模型配置
export GEMINI_MODELS="gemini-pro,gemini-1.5-pro,gemini-1.5-flash"
export GEMINI_DEFAULT_MODEL="gemini-pro"

# 切换模型
gemini config set model=gemini-1.5-pro

# 查看可用模型列表
gemini models list
```

## 高效技巧
1. 使用 `--stream` 参数实时查看生成过程
2. 通过 `--model=gemini-pro` 指定模型版本
3. 使用 `>> output.txt` 重定向输出结果

## 常见问题
<mcfile name="网络问题" path="d:\BaiduSyncdisk\Creator\AI_Coding_wiki\02_Gemini_CLI.md"></mcfile>

## 示例
```bash
gemini generate "实现Python异步日志记录 要求JSON格式 包含调用堆栈"
```