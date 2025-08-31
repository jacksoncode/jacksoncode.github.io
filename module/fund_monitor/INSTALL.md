# 基金监控系统 - 安装和使用指南

## 📋 环境要求

- **Python版本**: 3.7 或更高版本
- **操作系统**: Linux, macOS, Windows
- **网络环境**: 稳定的互联网连接
- **邮箱服务**: 支持SMTP的邮箱账号（QQ邮箱、163邮箱、Gmail等）

## 🚀 快速开始

### 1. 环境准备

#### 创建虚拟环境（推荐）
```bash
# 创建虚拟环境
python3 -m venv fund_monitor_env

# 激活虚拟环境
# Linux/macOS:
source fund_monitor_env/bin/activate
# Windows:
# fund_monitor_env\Scripts\activate
```

#### 安装依赖
```bash
# 进入项目目录
cd module/fund_monitor

# 安装所需依赖
pip install -r requirements.txt
```

### 2. 配置设置

#### 基金配置 (config/fund_config.ini)
```ini
[MONITOR_FUNDS]
# 基金代码列表，用逗号分隔
fund_codes = 000001,110022,161725

[FUND_000001]
name = 华夏成长混合
alert_threshold = 3.0  # 涨跌幅预警阈值(%)

[SCHEDULE]
# 监控时间设置
monitor_times = 09:30,11:30,15:00
weekend_monitor = false
```

#### 邮件配置 (config/email_config.ini)
```ini
[SMTP]
provider = qq  # 邮件服务商: qq, 163, gmail, outlook
username = your_email@qq.com  # 发送邮箱
password = your_smtp_password  # SMTP授权码
from_name = 基金监控系统

[RECIPIENTS]
# 收件人列表
primary = user1@example.com,user2@example.com
secondary = backup@example.com
```

**重要提醒**: 
- 请将配置文件中的邮箱和密码替换为您的真实信息
- QQ邮箱需要开启SMTP服务并获取授权码
- 163邮箱同样需要开启SMTP服务

### 3. 运行程序

#### 单次执行
```bash
# 执行一次基金监控
python src/monitor_main.py --mode once
```

#### 测试邮件发送
```bash
# 测试邮件配置是否正确
python src/monitor_main.py --mode test
```

#### 守护进程模式
```bash
# 启动定时监控（按配置时间自动执行）
python src/monitor_main.py --mode daemon
```

#### 查看状态
```bash
# 查看监控系统状态
python src/monitor_main.py --mode status
```

## 🧪 运行测试

### 运行所有测试
```bash
cd tests
python run_tests.py
```

### 运行特定模块测试
```bash
# 测试数据爬取模块
python run_tests.py --module crawler

# 测试邮件发送模块
python run_tests.py --module email

# 测试数据处理模块
python run_tests.py --module processor

# 测试主程序集成
python run_tests.py --module integration
```

### 检查测试环境
```bash
python run_tests.py --check-env
```

## 📁 项目结构说明

```
fund_monitor/
├── config/                 # 配置文件目录
│   ├── fund_config.ini     # 基金监控配置
│   └── email_config.ini    # 邮件发送配置
├── src/                    # 源码目录
│   ├── fund_crawler.py     # 基金数据爬取模块
│   ├── email_sender.py     # 邮件发送模块
│   ├── data_processor.py   # 数据处理模块
│   └── monitor_main.py     # 主程序入口
├── templates/              # 邮件模板
│   └── email_template.html # HTML邮件模板
├── tests/                  # 测试文件目录
│   ├── test_crawler.py     # 爬取模块测试
│   ├── test_email.py       # 邮件模块测试
│   ├── test_processor.py   # 处理模块测试
│   ├── test_integration.py # 集成测试
│   └── run_tests.py        # 测试运行脚本
├── logs/                   # 日志文件目录
├── data/                   # 数据存储目录
├── requirements.txt        # 依赖包列表
├── README.md              # 项目说明文档
└── INSTALL.md             # 本安装指南
```

## ⚙️ 高级配置

### 定时任务设置

#### Linux/macOS 使用 crontab
```bash
# 编辑crontab
crontab -e

# 添加定时任务（每天9:30、11:30、15:00执行）
30 9,11,15 * * 1-5 cd /path/to/fund_monitor && python src/monitor_main.py --mode once

# 查看已设置的任务
crontab -l
```

#### Windows 使用任务计划程序
1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器为"每天"
4. 设置操作为运行程序，程序路径指向Python脚本

### 邮箱授权码获取

#### QQ邮箱
1. 登录QQ邮箱 → 设置 → 账户
2. 开启SMTP服务
3. 获取授权码并保存

#### 163邮箱
1. 登录163邮箱 → 设置 → POP3/SMTP/IMAP
2. 开启SMTP服务
3. 获取授权码

#### Gmail
1. 开启两步验证
2. 生成应用程序专用密码
3. 使用专用密码作为SMTP密码

## 🔧 故障排除

### 常见问题

#### 1. 模块导入错误
```bash
# 确保在正确的目录中运行
cd /path/to/fund_monitor

# 检查Python路径
python -c "import sys; print(sys.path)"
```

#### 2. 网络连接问题
- 检查网络连接是否正常
- 确认防火墙没有阻止Python程序
- 尝试更换数据源（在配置中修改primary_source）

#### 3. 邮件发送失败
- 验证邮箱地址和密码是否正确
- 确认SMTP服务已开启并获取了授权码
- 检查邮件服务商的SMTP设置

#### 4. 基金数据获取失败
- 检查基金代码是否正确
- 尝试手动访问数据源URL
- 查看logs目录下的日志文件获取详细错误信息

### 日志查看
```bash
# 查看最新日志
tail -f logs/monitor.log

# 查看错误日志
grep "ERROR" logs/monitor.log
```

## 📊 监控结果示例

### 控制台输出
```
2024-08-30 09:30:05 - INFO: 开始基金监控任务
2024-08-30 09:30:06 - INFO: 成功获取 3 个基金数据
2024-08-30 09:30:07 - INFO: 数据汇总: 3个基金, 2涨1跌, 1个预警
2024-08-30 09:30:08 - INFO: 邮件报告发送成功
2024-08-30 09:30:08 - INFO: 基金监控任务完成，耗时 3.2 秒
```

### 邮件报告示例
收到的邮件将包含：
- 📊 基金监控日报标题
- 📈 监控汇总统计
- 📋 详细的基金数据表格
- ⚠️ 预警基金特别标记
- 🕐 数据来源和时间信息

## 🤝 支持与反馈

如果您在使用过程中遇到问题或有改进建议：

1. 查看项目文档和常见问题
2. 检查日志文件中的错误信息
3. 通过网站联系表单提交问题反馈

## 📄 许可证

本项目基于 MIT 许可证开源。

---

*基金投资有风险，投资需谨慎。本系统仅提供数据监控服务，不构成投资建议。*