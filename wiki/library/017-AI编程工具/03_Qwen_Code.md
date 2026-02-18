# Qwen Code 使用指南

## 安装
```powershell
pip install qwen-code
```

## 配置
```bash
# 基础认证配置
export QWEN_API_KEY="your_api_key"
qwen-code init --model=qwen-plus

# 多模型配置
export QWEN_MODELS="qwen-turbo,qwen-plus,qwen-max,qwen-coder"
export QWEN_DEFAULT_MODEL="qwen-plus"

# 切换模型
qwen-code config set model=qwen-max

# 查看可用模型列表
qwen-code models list

# 为不同项目设置不同模型
qwen-code project set --model=qwen-coder --project-name="my-coding-project"
```

## 高效技巧
1. 使用 `--context-file` 参数加载代码上下文
2. 通过 `@retry` 注解实现自动重试
3. 使用交互式调试模式 `qwen-code debug`

## 常见问题
<mcfile name="模型加载问题" path="d:\BaiduSyncdisk\Creator\AI_Coding_wiki\03_Qwen_Code.md"></mcfile>

## 示例
```bash
qwen-code generate "编写Python异步爬虫 支持代理池和UserAgent轮换"
```