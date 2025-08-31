# 基金每日监控系统

> 一个用于获取指定基金每日涨跌情况及关键指标，并自动发送监控报告到指定邮箱的Python程序。

## 📋 项目概述

### 功能目标
- 获取指定基金的每日涨跌情况及关键指标
- 定时监控基金数据变化
- 自动发送监控报告到指定邮箱
- 支持多基金同时监控

### 核心特性
- **多数据源支持**: 天天基金、新浪财经等多个数据源
- **智能数据解析**: 自动适配不同API数据格式
- **灵活邮件配置**: 支持HTML格式美观报告
- **错误重试机制**: 多重重试保障数据获取
- **详细日志记录**: 完整的运行状态追踪

## 🏗️ 技术架构

### 技术选型
- **开发语言**: Python 3.7+
- **网络请求**: requests库
- **邮件发送**: smtplib + email
- **数据解析**: json + re
- **定时任务**: schedule库
- **配置管理**: configparser
- **日志系统**: logging

### 项目结构
```
module/fund_monitor/
├── config/
│   ├── fund_config.ini      # 基金配置文件
│   └── email_config.ini     # 邮件配置文件
├── src/
│   ├── fund_crawler.py      # 基金数据爬取
│   ├── email_sender.py      # 邮件发送模块
│   ├── data_processor.py    # 数据处理模块
│   └── monitor_main.py      # 主程序入口
├── templates/
│   └── email_template.html  # 邮件模板
├── logs/
│   └── monitor.log         # 日志文件
├── tests/
│   ├── test_crawler.py     # 测试文件
│   └── test_email.py
├── requirements.txt        # 依赖包
└── README.md              # 项目说明
```

## 🔧 核心模块设计

### 数据获取模块 (fund_crawler.py)
负责从多个数据源获取基金信息，支持自动切换和数据验证。

**主要功能:**
- 多数据源配置和切换
- 基金数据解析和验证
- 网络异常处理和重试
- 数据格式标准化

**支持的数据源:**
- 天天基金网 API
- 新浪财经 API
- 其他第三方基金数据接口

### 邮件发送模块 (email_sender.py)
支持多种SMTP服务商，发送HTML格式的基金监控报告。

**主要功能:**
- 多SMTP服务商支持（QQ、163、Gmail等）
- HTML邮件模板渲染
- 多收件人配置
- 发送状态监控

**SMTP配置:**
```python
smtp_configs = {
    'qq': {'host': 'smtp.qq.com', 'port': 587},
    '163': {'host': 'smtp.163.com', 'port': 25},
    'gmail': {'host': 'smtp.gmail.com', 'port': 587}
}
```

### 数据处理模块 (data_processor.py)
处理基金数据，计算关键指标和生成监控汇总。

**关键指标:**
- 净值 (net_value)
- 涨跌幅 (change_rate)
- 涨跌额 (change_amount)
- 累计净值 (total_value)
- 更新时间 (update_time)

## ⚙️ 配置文件

### 基金配置 (config/fund_config.ini)
```ini
[MONITOR_FUNDS]
# 基金代码列表，用逗号分隔
fund_codes = 000001,110022,161725

[FUND_000001]
name = 华夏成长混合
alert_threshold = 3.0  # 涨跌幅预警阈值(%)

[FUND_110022]
name = 易方达消费行业股票
alert_threshold = 5.0

[FUND_161725]
name = 招商中证白酒指数分级
alert_threshold = 4.0

[SCHEDULE]
# 监控时间设置
monitor_times = 09:30,11:30,15:00
weekend_monitor = false
holiday_monitor = false
```

### 邮件配置 (config/email_config.ini)
```ini
[SMTP]
provider = qq
username = your_email@qq.com
password = your_smtp_password
from_name = 基金监控系统

[RECIPIENTS]
# 收件人列表
primary = user1@example.com,user2@example.com
secondary = backup@example.com

[EMAIL_SETTINGS]
subject_template = 【基金监控】{date} 基金涨跌报告
enable_html = true
attach_chart = false
alert_only = false  # 是否仅在触发预警时发送
```

## 📧 邮件模板

系统使用HTML模板生成美观的监控报告：

### 邮件内容包含:
- **监控汇总**: 总基金数、上涨/下跌基金数量
- **详细数据表格**: 基金名称、净值、涨跌幅、涨跌额、更新时间
- **预警提醒**: 超过阈值的基金特别标记
- **数据来源**: 数据获取时间和来源标注

### 样式特性:
- 响应式表格设计
- 涨跌颜色区分（红涨绿跌）
- 预警基金高亮显示
- 移动端友好显示

## 🛡️ 安全与可靠性

### 安全措施
- **配置加密**: 敏感信息（如邮箱密码）建议使用环境变量
- **请求头伪装**: 避免被反爬虫机制识别
- **频率限制**: 控制API请求频率，避免被封禁
- **异常捕获**: 全面的异常处理机制

### 可靠性保障
- **多重重试**: 网络请求失败时自动重试
- **降级策略**: 部分数据获取失败时的优雅处理
- **详细日志**: 记录所有操作和异常信息
- **状态监控**: 监控程序运行状态和健康度

### 数据验证机制
```python
def _is_valid_response(self, response_data):
    """检查响应数据有效性"""
    # 验证数据完整性和格式正确性
    
def _has_complete_info(self, fund_data):
    """确保基金数据完整性"""
    # 检查必要字段是否存在
```

## 🚀 快速开始

### 环境要求
- Python 3.7+
- 稳定的网络连接
- SMTP邮箱服务

### 安装依赖
```bash
pip install -r requirements.txt
```

### 配置设置
1. 复制配置模板并修改参数
2. 配置基金代码和监控设置
3. 设置邮箱SMTP信息

### 运行方式

#### 手动执行
```bash
python src/monitor_main.py
```

#### 定时任务 (Linux/Mac)
```bash
# 添加到crontab
30 9,11,15 * * 1-5 /usr/bin/python3 /path/to/monitor_main.py
```

#### 定时任务 (Windows)
使用Windows任务计划程序设置定时执行。

## 📊 监控示例

### 控制台输出
```
[2024-08-30 09:30:05] INFO: 开始基金监控...
[2024-08-30 09:30:06] INFO: 获取基金 000001 数据成功
[2024-08-30 09:30:07] INFO: 获取基金 110022 数据成功  
[2024-08-30 09:30:08] INFO: 获取基金 161725 数据成功
[2024-08-30 09:30:09] WARNING: 基金 161725 涨幅 4.2% 超过预警阈值 4.0%
[2024-08-30 09:30:10] INFO: 邮件发送成功到 user@example.com
[2024-08-30 09:30:10] INFO: 监控完成，耗时 5.2 秒
```

### 邮件报告预览
```
📊 基金监控日报 - 2024-08-30

📈 监控汇总
总监控基金数: 3
上涨基金数: 2  
下跌基金数: 1

📋 详细数据
┌──────────────────┬────────┬─────────┬─────────┬─────────────┬────────┐
│ 基金名称         │ 净值   │ 涨跌幅  │ 涨跌额  │ 更新时间    │ 状态   │
├──────────────────┼────────┼─────────┼─────────┼─────────────┼────────┤
│ 华夏成长混合     │ 1.2340 │ +2.15%  │ +0.026  │ 09:30:00   │ 正常   │
│ 易方达消费行业   │ 2.1580 │ -1.23%  │ -0.027  │ 09:30:00   │ 正常   │  
│ 招商中证白酒指数 │ 0.8760 │ +4.20%  │ +0.035  │ 09:30:00   │ ⚠️预警 │
└──────────────────┴────────┴─────────┴─────────┴─────────────┴────────┘

数据来源: 天天基金网 | 报告时间: 2024-08-30 09:30:10
```

## 🧪 测试

### 运行测试
```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python -m pytest tests/test_crawler.py
python -m pytest tests/test_email.py
```

### 测试覆盖范围
- 数据爬取功能测试
- 邮件发送功能测试
- 配置文件解析测试
- 异常处理机制测试

## 📝 开发规范

### 代码规范
- 遵循PEP 8 Python编码规范
- 使用类型注解提升代码可读性
- 编写完整的文档字符串
- 进行充分的单元测试

### 提交规范
- 每次提交前运行测试套件
- 使用语义化的提交信息
- 及时更新文档和配置

## 🔄 版本历史

### v1.0.0 (计划中)
- [x] 基础框架设计
- [x] 多数据源支持
- [x] 邮件发送功能
- [ ] 数据爬取实现
- [ ] 配置管理完善
- [ ] 测试用例编写

## 📄 许可证

本项目基于 MIT 许可证开源 - 查看 [LICENSE.md](../../LICENSE.md) 了解详情。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进项目！

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 项目主页: [jacksoncode.github.io](https://jacksoncode.github.io)
- 邮箱: 通过网站联系表单发送

---

*此项目是 jacksoncode.github.io 个人技术项目的一部分，专注于为程序员和技术学习者提供实用的工具和资源。*