# LLM 大语言模型基础

## 1. 什么是大语言模型 (LLM)

大语言模型（Large Language Model）是一种基于深度学习的自然语言处理模型，具有以下特点：

- **大规模参数**：通常包含数十亿到数千亿个参数
- **预训练**：在大规模文本语料上进行无监督预训练
- **涌现能力**：展现出惊人的推理和生成能力
- **通用性**：可应用于多种自然语言任务

### 主要 LLM 模型

| 模型 | 开发者 | 参数量 | 特点 |
|------|--------|--------|------|
| GPT-4 | OpenAI | ~1.8万亿 | 强大的推理能力 |
| Claude 3 | Anthropic | - | 长上下文、安全性强 |
| Gemini | Google | - | 多模态支持 |
| Llama 3 | Meta | 8B-70B | 开源可商用 |
| Qwen | 阿里云 | 7B-110B | 中文优化 |
| DeepSeek | 深度求索 | 7B-67B | 高性价比 |

## 2. LLM 的工作原理

### Transformer 架构

```python
"""
Transformer 核心组件示意
实际实现请参考 transformers 库
"""

# 自注意力机制 (Self-Attention)
class SelfAttention:
    """
    Q (Query): 当前词想要查询的内容
    K (Key): 每个词的"索引标签"
    V (Value): 每个词的实际内容
    """
    def attention(self, Q, K, V):
        # 计算注意力分数
        scores = torch.matmul(Q, K.transpose(-2, -1))
        scores = scores / math.sqrt(self.d_k)
        
        # Softmax 归一化
        attention_weights = F.softmax(scores, dim=-1)
        
        # 加权求和
        output = torch.matmul(attention_weights, V)
        return output
```

### 生成过程

```python
"""
LLM 文本生成示意
"""
# 1. 输入处理
input_text = "今天天气真好"
tokens = tokenize(input_text)  # 分词

# 2. 前向传播
embeddings = model.embed(tokens)
logits = model.forward(embeddings)

# 3. 采样生成
next_token_probs = F.softmax(logits[-1], dim=-1)
# 常用策略:
# - Greedy: 选择概率最高的 token
# - Temperature: 调整概率分布的"温度"
# - Top-k: 只从前 k 个最高概率中选择
# - Top-p (Nucleus): 选择累积概率达到 p 的 token
next_token = sample(next_token_probs, strategy="top_p", p=0.9)

# 4. 循环生成直到结束
```

## 3. API 调用基础

### OpenAI API

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "你是一个有帮助的助手"},
        {"role": "user", "content": "解释量子计算的基本原理"}
    ],
    temperature=0.7,
    max_tokens=1000
)

print(response.choices[0].message.content)
```

### Anthropic API (Claude)

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "用中文解释什么是机器学习"}
    ],
    system="你是一位专业的AI专家，用通俗易懂的语言解释技术概念"
)

print(message.content[0].text)
```

### Google Gemini API

```python
import google.generativeai as genai

genai.configure(api_key="your-api-key")
model = genai.GenerativeModel('gemini-pro')

response = model.generate_content(
    "解释什么是深度学习"
)

print(response.text)
```

## 4. Token 与成本计算

```python
import tiktoken

# 使用 tiktoken 计算 token 数
enc = tiktoken.get_encoding("cl100k_base")  # GPT-4/ChatGPT 用

text = "Hello, world! 这是一段中文测试文本。"
tokens = enc.encode(text)

print(f"文本长度: {len(text)} 字符")
print(f"Token 数量: {len(tokens)}")
print(f"Token IDs: {tokens}")

# 反向解码
decoded = enc.decode(tokens)
print(f"解码结果: {decoded}")
```

### Token 估算规则（经验值）

| 文本类型 | 每 token 约等于 |
|----------|----------------|
| 英文单词 | 0.75 个单词 |
| 中文字符 | 1-2 个字符 |
| 代码 | 约 4 个字符 |

## 5. 模型参数调优

### Temperature

```python
"""
Temperature 控制输出的随机性
- 低 temperature (0.1-0.3): 更确定、更保守的输出
- 中 temperature (0.5-0.7): 平衡创造性和确定性
- 高 temperature (0.9-1.0): 更随机、更有创造性的输出
"""

# 确定性回答
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "1+1等于几？"}],
    temperature=0.1
)

# 创造性回答
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "写一首关于春天的诗"}],
    temperature=0.9
)
```

### Max Tokens

```python
"""
限制生成的最大 token 数
设置太小可能截断回答
设置太大会浪费 tokens
"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "详细介绍Python"}],
    max_tokens=500  # 限制在约 500 tokens
)
```

## 6. 上下文窗口

```python
"""
不同模型的上下文窗口大小
"""

CONTEXT_WINDOWS = {
    "gpt-4": 128000,           # 128K tokens
    "gpt-3.5-turbo": 16385,    # 16K tokens
    "claude-3-opus": 200000,   # 200K tokens
    "claude-3-sonnet": 200000, # 200K tokens
    "gemini-pro": 128000,      # 128K tokens
}

# 使用长上下文
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": very_long_context},
        {"role": "user", "content": "基于以上内容回答：..."}
    ],
    max_tokens=1000
)
```

## 7. 常见错误处理

```python
import time

def call_with_retry(client, messages, max_retries=3):
    """带重试的 API 调用"""
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages
            )
            return response
        
        except RateLimitError:
            # 速率限制，等待后重试
            wait_time = 2 ** attempt
            print(f"速率限制，等待 {wait_time} 秒...")
            time.sleep(wait_time)
        
        except APIError as e:
            # API 错误，可能需要调整请求
            print(f"API 错误: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
    
    raise Exception("重试次数用尽")
```

## 8. 下一步学习

- [Prompt 工程技巧](./02-Prompt工程/01-基础Prompt设计.md)
- [LLM 应用开发](./03-大模型应用/01-RAG应用开发.md)
- [模型部署](./04-模型部署/01-本地部署Ollama.md)
