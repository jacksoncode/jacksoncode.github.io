# 本地部署 Ollama

## 1. 简介

Ollama 是一个本地大模型运行框架，让你可以在自己的电脑上运行各种开源 LLM：

- **无需网络**：完全离线运行
- **隐私安全**：数据不会上传
- **成本为零**：不需要 API 费用
- **易于部署**：一条命令启动模型

## 2. 安装

### macOS

```bash
# 使用 Homebrew 安装
brew install ollama

# 或下载安装包
# https://ollama.com/download
```

### Linux

```bash
# 一键安装
curl -fsSL https://ollama.com/install.sh | sh
```

### Windows

```bash
# 下载安装包
# https://ollama.com/download
```

### Docker

```bash
# 使用 Docker 运行
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

## 3. 快速开始

```bash
# 启动 Ollama 服务
ollama serve

# 测试运行
ollama run llama3

# 模型会下载并启动，尝试对话：
# >>> 你好
# 你好！有什么我可以帮助你的？
```

## 4. 模型管理

### 下载模型

```bash
# 查看可用模型
ollama list

# 拉取模型
ollama pull llama3      # 最新的 llama3
ollama pull llama3:70b  # 指定参数版本
ollama pull mistral    # Mistral 模型
ollama pull codellama  # 代码模型

# 删除模型
ollama rm llama3
```

### 常用模型推荐

| 模型 | 参数量 | 用途 | 命令 |
|------|--------|------|------|
| Llama 3 | 8B | 通用对话 | `ollama pull llama3` |
| Llama 3 | 70B | 高质量对话 | `ollama pull llama3:70b` |
| Mistral | 7B | 轻量快速 | `ollama pull mistral` |
| CodeLlama | 7B | 代码生成 | `ollama pull codellama` |
| Qwen | 7B | 中文优化 | `ollama pull qwen` |
| DeepSeek | 7B | 高性价比 | `ollama pull deepseek-coder` |
| Phi-3 | 3.8B | 超轻量 | `ollama pull phi3` |

## 5. API 使用

### REST API

```bash
# 基础对话 API
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "为什么天空是蓝色的？"
}'

# 流式响应
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "写一个 Python 快速排序",
  "stream": false
}'

# 聊天 API
curl http://localhost:11434/api/chat -d '{
  "model": "llama3",
  "messages": [
    {"role": "user", "content": "你好"}
  ]
}'
```

### Python SDK

```bash
pip install ollama
```

```python
import ollama

# 基础对话
response = ollama.generate(
    model='llama3',
    prompt='解释什么是机器学习'
)
print(response['response'])

# 聊天
chat = ollama.chat(
    model='llama3',
    messages=[
        {'role': 'system', 'content': '你是一个专业的Python导师'},
        {'role': 'user', 'content': '什么是装饰器？'}
    ]
)
print(chat['message']['content'])

# 流式响应
for chunk in ollama.generate(
    model='llama3',
    prompt='写一个斐波那契函数',
    stream=True
):
    print(chunk['response'], end='', flush=True)
```

## 6. 自定义模型

### Modelfile

```dockerfile
# Modelfile 示例：定制 Llama3
FROM llama3

# 设置系统提示
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_ctx 4096

SYSTEM """
你是一个专业的代码导师，擅长 Python 编程。
回答要简洁清晰，包含代码示例。
"""

# 设置模板
TEMPLATE """
{{ if .System }}{{ .System }}{{ end }}
{{ range .Messages }}{{ if eq .Role "user" }}
User: {{ .Content }}{{ else }}
Assistant: {{ .Content }}{{ end }}{{ end }}
Assistant: """
```

### 创建自定义模型

```bash
# 创建自定义模型
ollama create python-tutor -f Modelfile

# 使用自定义模型
ollama run python-tutor
```

## 7. 集成到应用

### LangChain 集成

```python
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# 初始化 Ollama LLM
llm = Ollama(model="llama3", base_url="http://localhost:11434")

# 创建链
prompt = PromptTemplate(
    input_variables=["topic"],
    template="用简洁的话解释{topic}，最多3句话"
)

chain = LLMChain(llm=llm, prompt=prompt)

# 运行
result = chain.run("Python 装饰器")
print(result)
```

### 与 RAG 结合

```python
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# 使用 Ollama 的 embedding
embeddings = OllamaEmbeddings(
    model="nomic-embed-text",  # 需要单独拉取
    base_url="http://localhost:11434"
)

# 创建向量数据库
vectorstore = Chroma(
    client=chromadb.PersistentClient(path="./db"),
    embedding_function=embeddings
)

# 使用 Ollama LLM 进行问答
llm = Ollama(model="llama3")

# RAG 链
from langchain.chains import RetrievalQA
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever()
)
```

## 8. GPU 加速

### NVIDIA GPU

```bash
# 确保安装了 nvidia-container-toolkit
# ollama 会自动使用 GPU

# 查看 GPU 使用
nvidia-smi
```

### Apple Silicon (MPS)

```bash
# 设置使用 MPS
export OLLAMA_HOST=0.0.0.0
export CUDA_VISIBLE_DEVICES=""  # 禁用 CUDA
```

## 9. 性能优化

### 参数调优

```python
# 调整生成参数
response = ollama.generate(
    model='llama3',
    prompt='写一首诗',
    options={
        'temperature': 0.8,      # 创造性 (0-1)
        'top_p': 0.9,           # 采样阈值
        'num_ctx': 4096,        # 上下文长度
        'repeat_penalty': 1.1,  # 重复惩罚
        'seed': 42,             # 随机种子
        'num_gpu': 1,           # GPU 数量
        'num_thread': 8         # CPU 线程数
    }
)
```

### 内存优化

```bash
# 查看模型内存占用
ollama show llama3

# 选择更小的模型
ollama pull phi3  # 约 2GB
ollama pull llama3:3.8b  # 约 4GB
```

## 10. 常见问题

### Q: 模型下载很慢？

```bash
# 使用代理
export HTTP_PROXY="http://your-proxy:port"
export HTTPS_PROXY="http://your-proxy:port"
ollama pull llama3
```

### Q: 内存不足？

```bash
# 使用更小的量化模型
ollama pull llama3:8b-instruct-q4_0  # 量化版本，更小更快

# 或使用更小的模型
ollama pull phi3
```

### Q: 如何保持模型运行？

```bash
# 启动后台服务
ollama serve &

# 或使用 systemd (Linux)
sudo systemctl enable ollama
sudo systemctl start ollama
```

## 11. 与 OpenCode 集成

```bash
# 配置 OpenCode 使用本地 Ollama
opencode config set OLLAMA_BASE_URL http://localhost:11434
opencode config set model llama3

# 或使用 Claude Code
export ANTHROPIC_API_KEY=local
claude --model llama3
```

## 12. 相关资源

- [Ollama 官网](https://ollama.com)
- [Ollama 模型库](https://ollama.com/library)
- [GitHub 仓库](https://github.com/ollama/ollama)
- [API 文档](https://github.com/ollama/ollama/blob/main/docs/api.md)
