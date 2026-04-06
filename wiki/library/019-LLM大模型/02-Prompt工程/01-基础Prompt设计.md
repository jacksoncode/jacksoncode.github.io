# Prompt 工程技巧

## 1. Prompt 工程概述

Prompt 工程（Prompt Engineering）是设计与优化输入提示词，以获得理想输出的实践技巧。好的 Prompt 能显著提升 LLM 的输出质量。

### 核心原则

1. **清晰具体**：明确说明需要什么
2. **结构化**：使用清晰的分段和格式
3. **提供上下文**：给出足够的背景信息
4. **指定格式**：说明期望的输出格式
5. **迭代优化**：根据输出不断调整

## 2. 基本 Prompt 模式

### 零样本 Prompt

```python
"""
最基本的 Prompt 方式，直接提问
"""
prompt = "将以下英文翻译成中文：Hello, how are you?"
```

### 少样本 Prompt (Few-shot)

```python
"""
提供几个示例，帮助模型理解任务
"""
prompt = """
将以下句子翻译成中文：

示例：
"Hello" -> "你好"
"Good morning" -> "早上好"
"The weather is nice today" -> 

请翻译：
"I love learning programming"
"""
```

### 思维链 Prompt (Chain of Thought)

```python
"""
引导模型展示推理过程
"""
prompt = """
问题：小明有10个苹果，送给朋友5个，又买了8个，现在有多少个苹果？

解决步骤：
1. 起始：10个苹果
2. 送出：10 - 5 = 5个
3. 新买：5 + 8 = 13个

答案：13个

---

问题：小红有15本书，借给同学6本，又买了9本，现在有多少本书？
"""
```

## 3. 结构化 Prompt

### 系统提示 + 用户提示

```python
"""
分离角色定义和具体任务
"""
messages = [
    {
        "role": "system",
        "content": """你是一位资深Python后端工程师，擅长使用FastAPI构建高性能API。
你的特点：
- 代码简洁规范，遵循PEP 8
- 提供完整的代码和详细解释
- 包含错误处理和测试用例
- 考虑性能和安全性"""
    },
    {
        "role": "user", 
        "content": "用FastAPI实现一个用户认证API，包含注册和登录功能"
    }
]
```

### XML/JSON 标签格式

```python
"""
使用标签结构化输入输出
"""
prompt = """
<task>代码审查</task>
<language>Python</language>
<code>
def calculate_discount(price, discount):
    return price - price * discount
</code>

<review_focus>
1. 边界情况处理
2. 安全性问题
3. 性能优化建议
</review_focus>

<output_format>JSON</output_format>
"""
```

## 4. 高级技巧

### 角色扮演

```python
"""
指定AI扮演特定角色
"""
messages = [
    {
        "role": "system",
        "content": """你扮演一位面试官，面试一位Python后端开发工程师。
要求：
- 问题由浅入深
- 对回答进行点评和追问
- 评估候选人的技术深度和广度
- 最后给出评估意见"""
    },
    {"role": "user", "content": "面试开始吧"}
]
```

### 指令分隔

```python
"""
使用清晰的分隔符区分不同部分
"""
prompt = """
## 任务
分析以下代码的性能问题

---
## 代码
```python
def find_duplicates(lst):
    duplicates = []
    for i in range(len(lst)):
        for j in range(i+1, len(lst)):
            if lst[i] == lst[j] and lst[i] not in duplicates:
                duplicates.append(lst[i])
    return duplicates
```
---

## 输出要求
1. 识别时间复杂度
2. 提出优化方案
3. 给出优化后的代码
"""
```

### 约束条件

```python
"""
添加明确的约束条件
"""
prompt = """
写一个Python函数，判断是否为质数。

约束：
- 输入必须是正整数
- 输出为布尔值
- 不能使用第三方库
- 代码需要包含类型注解
- 至少包含3个测试用例
"""
```

## 5. 迭代优化策略

### 渐进式提示

```python
"""
初始 Prompt
"""
prompt_v1 = "写一个网站"

"""
改进版 v2 - 更具体
"""
prompt_v2 = "写一个Todo应用的HTML/CSS/JS代码"

"""
改进版 v3 - 包含详细要求
"""
prompt_v3 = """
创建一个待办事项Web应用：

技术要求：
- 纯HTML/CSS/JS，无框架
- 响应式设计，支持移动端
- 使用localStorage存储数据

功能要求：
- 添加、删除、完成待办
- 数据持久化
- 简洁美观的UI

请提供完整的代码。
"""
```

### 输出格式控制

```python
# JSON 格式
prompt = """
查询用户信息，返回JSON格式

<schema>
{
    "name": "string",
    "age": "number",
    "email": "string",
    "tags": ["string"]
}
</schema>

用户：Alice
"""

# Markdown 表格
prompt = """
对比分析以下三种数据库，按以下维度：
| 数据库 | 适用场景 | 优势 | 劣势 |
|--------|----------|------|------|

1. MySQL
2. PostgreSQL
3. MongoDB
"""

# 代码 + 注释
prompt = """
写一个快速排序算法，要求：
1. 包含详细注释
2. 解释时间复杂度
3. 提供测试代码
"""
```

## 6. 常用 Prompt 模板

### 代码生成模板

```python
CODE_GENERATION_TEMPLATE = """
## 任务
{task_description}

## 技术栈
- 语言：{language}
- 框架：{framework}
- 版本要求：{version_requirements}

## 功能需求
{requirements}

## 代码规范
- 遵循{convention}
- 包含类型注解
- 添加docstring

## 输出格式
```代码块
{code}
```
"""

# 使用示例
prompt = CODE_GENERATION_TEMPLATE.format(
    task_description="实现用户认证",
    language="Python",
    framework="FastAPI",
    version_requirements="Python 3.10+",
    requirements="支持JWT认证，包含登录和注册",
    convention="PEP 8"
)
```

### 分析总结模板

```python
ANALYSIS_TEMPLATE = """
## 分析目标
{topic}

## 分析维度
{dimensions}

## 原始内容
{content}

## 输出格式
1. 核心发现（3-5条）
2. 详细分析
3. 建议/结论

## 风格要求
- 简洁专业
- 使用数据支撑观点
- 包含具体例子
"""
```

## 7. 避免常见错误

```python
# ❌ 模糊不清
prompt = "帮我写代码"

# ✅ 清晰具体
prompt = "用Python写一个函数，接收一个列表，返回去重后的列表，保持原顺序"

# ❌ 缺少上下文
prompt = "这段代码有问题"

# ✅ 提供完整上下文
prompt = """
这是一个Flask API的路由函数，用户反馈登录接口返回500错误。
请帮我找出问题并修复。

代码：
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.get(data['username'])
    if user.password == data['password']:
        return jsonify({'token': generate_token(user)})
"""
```

## 8. 实用技巧

### 关键词强调

```python
# 使用强调词突出重点
prompt = """
重要：请务必在代码中添加错误处理。
同时，错误处理使用 try-except，不要用 if-else。
关键点：
1. 处理网络错误
2. 处理超时
3. 处理数据格式错误
"""
```

### 示例引导

```python
# 清晰的输入输出示例
prompt = """
你是一个翻译助手，以下是对应关系：

英文 -> 中文：
"Hello" -> "你好"
"I love you" -> "我爱你"
"The quick brown fox" -> "敏捷的棕色狐狸"

现在请翻译：
"Thank you for your help"
"""
```

### 分步骤执行

```python
# 让模型分步骤完成任务
prompt = """
请帮我完成以下任务，按步骤进行：

步骤1：分析以下CSV文件的结构
步骤2：清理数据中的缺失值
步骤3：进行数据可视化
步骤4：生成分析报告

数据文件：sales_data.csv
"""
```

## 9. 最佳实践总结

1. **明确角色**：给AI一个明确的身份
2. **具体描述**：避免歧义，提供具体细节
3. **格式化输出**：指定期望的输出格式
4. **提供示例**：用Few-shot帮助理解
5. **分解任务**：复杂任务分解为多个步骤
6. **迭代优化**：根据输出不断改进Prompt
7. **测试验证**：用多个案例测试Prompt效果
