# AI平台账单查询系统 - 快速使用指南

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 初始化配置
```bash
python3 get_bill.py --init
```

### 3. 编辑配置文件
编辑 `ai_billing_config.ini` 文件，填入您的API密钥：

```ini
[openai]
api_key = sk-your-openai-api-key
base_url = https://api.openai.com
enabled = true

[deepseek]
api_key = sk-your-deepseek-api-key
base_url = https://api.deepseek.com
enabled = true

[siliconflow]
api_key = sk-your-siliconflow-api-key
base_url = https://api.siliconflow.cn
enabled = true
```

### 4. 查询账单
```bash
# 查询所有平台
python3 get_bill.py --query

# 查询特定平台
python3 get_bill.py --platform openai

# 以JSON格式输出
python3 get_bill.py --query --format json

# 保存到文件
python3 get_bill.py --query --format csv --save report.csv
```

## 📊 演示功能

运行演示脚本查看功能展示：
```bash
python3 demo.py
```

## 🔧 支持的平台

- **国内**: DeepSeek, 硅基流动, Kimi, 豆包, 火山方舟, 智谱AI, 腾讯混元, 阿里云百炼, 百度百川
- **国际**: OpenAI, OpenRouter, Github Copilot
- **聚合**: AiHubMix, 魔塔社区, 派欧云, henAPI, O3, 阶跃星辰等

## 📝 Python代码调用

```python
from get_bill import *

# 创建平台实例
platform = OpenAIPlatform('your-api-key')
billing_info = platform.get_billing_info()

print(f"余额: {billing_info.balance}")
print(f"已使用: {billing_info.used_amount}")
```

## 🆘 帮助

```bash
python3 get_bill.py --help
```

更多详细信息请查看 README.md 文档。