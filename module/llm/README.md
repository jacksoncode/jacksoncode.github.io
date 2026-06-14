# AI平台账单查询系统

一个强大的Python工具，支持自动获取多个主流AI模型平台的API使用量、余额、账单等信息。

## 🌟 功能特性

- **多平台支持**: 支持20+主流AI平台
- **统一接口**: 提供一致的数据结构和API接口
- **多种输出格式**: 支持JSON、表格、CSV、Markdown、HTML等格式
- **配置管理**: 灵活的配置文件管理系统
- **错误处理**: 完善的异常处理和重试机制
- **命令行工具**: 友好的命令行界面
- **扩展性**: 易于添加新的平台支持

## 🎯 支持的平台

### 国内平台

- **轨迹流动/DeepSeek**: 深度求索AI平台
- **硅基流动**: SiliconFlow AI推理平台
- **Kimi**: 月之暗面智能助手
- **豆包**: 字节跳动AI平台
- **火山方舟**: 火山引擎AI平台
- **智谱AI**: 智谱清言GLM系列
- **腾讯混元**: 腾讯云混元大模型
- **阿里云百炼**: 阿里云大模型服务
- **百度百川**: 百度智能云文心系列

### 国际平台

- **OpenAI**: GPT系列模型
- **OpenRouter**: AI模型聚合平台
- **Github Copilot**: 代码辅助工具

### 聚合平台

- **AiHubMix**: AI模型聚合服务
- **魔塔社区**: ModelScope平台
- **派欧云**: AI服务聚合
- **henAPI**: API聚合服务
- **O3**: AI模型平台
- **阶跃星辰**: Step AI平台
- **腾讯T1**: 腾讯AI服务
- **天翼云**: 中国电信AI平台
- **Tavily**: 搜索AI平台
- **ocoolAI**: AI服务平台

## 📦 安装与依赖

### 基础依赖

```bash
pip install requests configparser
```

### 可选依赖（用于更好的表格显示）

```bash
pip install tabulate
```

## 🚀 快速开始

### 1. 初始化配置

```bash
python get_bill.py --init
```

这会创建一个 `ai_billing_config.ini` 配置文件模板。

### 2. 配置API密钥

编辑 `ai_billing_config.ini` 文件，填入您的API密钥：

```ini
[deepseek]
api_key = sk-your-deepseek-api-key
base_url = https://api.deepseek.com
enabled = true

[openai]
api_key = sk-your-openai-api-key
base_url = https://api.openai.com
enabled = true

[kimi]
api_key = your-kimi-api-key
base_url = https://api.moonshot.cn
enabled = true

[siliconflow]
api_key = sk-your-siliconflow-api-key
base_url = https://api.siliconflow.cn
enabled = true
```

### 3. 查询账单

```bash
# 查询所有平台账单
python get_bill.py --query

# 以JSON格式输出
python get_bill.py --query --format json

# 查询特定平台
python get_bill.py --platform openai

# 保存结果到文件
python get_bill.py --query --format csv --save report.csv
```

## 💻 使用方法

### 命令行界面

```bash
# 显示帮助信息
python get_bill.py --help

# 初始化配置文件
python get_bill.py --init

# 查询所有平台
python get_bill.py --query

# 指定输出格式
python get_bill.py --query --format [json|table|csv|markdown|html]

# 查询特定平台
python get_bill.py --platform <平台名称>

# 显示汇总信息
python get_bill.py --summary

# 生成详细报告
python get_bill.py --detailed-report ./reports

# 显示详细日志
python get_bill.py --query --verbose
```

### Python代码调用

#### 基本使用

```python
from get_bill import *

# 创建配置管理器
config_manager = ConfigManager()

# 设置平台配置
config_manager.set_platform_config('openai',
    api_key='your-api-key',
    base_url='https://api.openai.com',
    enabled='true')

# 创建账单管理器
billing_manager = BillingManager(config_manager)
billing_manager.add_platform(PlatformType.OPENAI)

# 查询账单信息
billing_data = billing_manager.get_all_billing_info()

# 格式化输出
formatter = BillingFormatter()
print(formatter.format(billing_data, OutputFormat.TABLE))
```

#### 单平台查询

```python
# 直接创建平台实例
platform = OpenAIPlatform('your-api-key')
billing_info = platform.get_billing_info()

print(f"余额: {billing_info.balance}")
print(f"已使用: {billing_info.used_amount}")
```

#### 自定义平台

```python
class MyPlatform(BasePlatform):
    @property
    def platform_name(self) -> str:
        return "我的平台"

    def get_billing_info(self) -> BillingInfo:
        # 实现获取账单逻辑
        return BillingInfo(
            platform=self.platform_name,
            balance=100.0,
            used_amount=50.0,
            total_quota=150.0,
            # ... 其他字段
        )
```

## 📊 输出格式

### 表格格式（默认）

```
------------------------------------------------------------
平台            余额          已使用        总额度        ...
------------------------------------------------------------
OpenAI         25.0000      75.0000      100.0000      ...
DeepSeek       50.0000      30.0000       80.0000      ...
------------------------------------------------------------
```

### JSON格式

```json
{
  "openai": {
    "platform": "OpenAI",
    "balance": 25.0,
    "used_amount": 75.0,
    "total_quota": 100.0,
    "currency": "USD",
    "last_update": "2024-01-01 12:00:00"
  }
}
```

### 汇总信息

```json
{
  "总平台数": 3,
  "成功查询": 2,
  "查询失败": 1,
  "总余额": {
    "USD": 125.0,
    "CNY": 200.0
  },
  "总已使用": {
    "USD": 175.0,
    "CNY": 80.0
  }
}
```

## ⚙️ 配置说明

### 配置文件结构

```ini
[general]
request_timeout = 30
max_retries = 3
retry_delay = 1

[platform_name]
api_key = your-api-key
base_url = https://api.example.com
enabled = true
# 其他平台特定配置...
```

### 平台特定配置

#### DeepSeek

```ini
[deepseek]
api_key = sk-xxx
base_url = https://api.deepseek.com
enabled = true
```

#### 火山方舟（支持AK/SK认证）

```ini
[huoshan]
api_key = your-api-key
access_key = your-access-key
secret_key = your-secret-key
base_url = https://ark.cn-beijing.volces.com
enabled = true
```

#### 百度（需要API Key和Secret Key）

```ini
[baidu_baichuan]
api_key = your-api-key
secret_key = your-secret-key
base_url = https://aip.baidubce.com
enabled = true
```

## 🛠️ 扩展开发

### 添加新平台支持

1. 继承BasePlatform类：

```python
class NewPlatform(BasePlatform):
    @property
    def platform_name(self) -> str:
        return "新平台"

    def get_billing_info(self) -> BillingInfo:
        # 实现API调用逻辑
        headers = self._get_auth_headers()
        response = self._make_request("GET", f"{self.base_url}/billing", headers=headers)
        data = response.json()

        return BillingInfo(
            platform=self.platform_name,
            balance=data.get('balance', 0),
            # ... 解析其他字段
        )
```

2. 注册到工厂：

```python
# 添加到PlatformType枚举
class PlatformType(Enum):
    NEW_PLATFORM = "new_platform"

# 注册平台
PlatformFactory.register_platform(PlatformType.NEW_PLATFORM, NewPlatform)
```

## 🔧 故障排除

### 常见问题

#### 1. API密钥无效

```
错误: 认证失败: 401 Unauthorized
解决: 检查配置文件中的API密钥是否正确
```

#### 2. 请求频率限制

```
错误: 请求频率超限: 429 Too Many Requests
解决: 程序会自动重试，如持续失败请检查API限额
```

#### 3. 平台未配置

```
错误: 平台 'xxx' 未配置或未启用
解决: 检查配置文件中enabled是否为true，API密钥是否填写
```

#### 4. 网络连接问题

```
错误: 请求最终失败: Connection timeout
解决: 检查网络连接，可能需要代理设置
```

### 调试模式

```bash
python get_bill.py --query --verbose
```

使用 `--verbose` 参数可以显示详细的调试信息。

## 📄 数据结构

### BillingInfo字段说明

- `platform`: 平台名称
- `balance`: 当前余额
- `used_amount`: 已使用金额
- `total_quota`: 总额度
- `free_quota`: 免费额度
- `recharged_amount`: 已充值金额
- `gift_amount`: 赠送金额
- `currency`: 币种（USD/CNY等）
- `last_update`: 最后更新时间
- `expiry_date`: 过期时间（可选）
- `usage_details`: 详细使用信息（原始API响应）

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

### 贡献新平台支持

1. Fork项目
2. 创建新的平台实现类
3. 添加相应的测试
4. 更新文档
5. 提交Pull Request

## 📜 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙋 常见用例

### 监控API使用情况

```bash
# 定时执行，监控余额变化
*/30 * * * * /usr/bin/python /path/to/get_bill.py --query --save /var/log/api_usage.json
```

### 批量导出报告

```bash
# 生成全格式报告
python get_bill.py --detailed-report ./monthly_reports
```

### CI/CD集成

```bash
# 在部署脚本中检查API余额
python get_bill.py --summary | grep -q "成功查询.*[1-9]" || exit 1
```

---

**注意**: 使用前请确保您有相应平台的API访问权限，并妥善保管API密钥。某些平台的API可能需要特殊权限或付费订阅。
