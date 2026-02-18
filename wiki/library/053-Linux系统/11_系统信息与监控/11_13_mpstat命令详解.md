# mpstat命令详解

## 1 命令概述

mpstat（Multiprocessor Statistics）是一个用于监控多处理器系统中各个CPU性能状况的命令行工具。它是sysstat包的一部分，可以提供每个CPU的详细使用率统计信息，帮助系统管理员分析系统性能瓶颈，特别是在多处理器或多核系统中。

### 1.1 功能特点

- 显示各个CPU或处理器核心的使用率统计
- 提供全局CPU使用率和每个CPU的使用率对比
- 监控CPU的用户空间、系统内核、I/O等待、空闲等时间占比
- 支持实时监控模式，可以定期刷新数据
- 可以显示CPU的中断、上下文切换等高级统计信息
- 适用于多处理器、多核和超线程系统

### 1.2 应用场景

mpstat命令在以下场景中特别有用：

- 分析多处理器系统中的CPU负载分布情况
- 识别是否存在CPU瓶颈或负载不均衡问题
- 监控系统在高负载情况下的CPU性能表现
- 调试与CPU相关的性能问题
- 评估系统升级或扩容的必要性
- 为系统性能优化提供数据支持

## 2 语法格式

mpstat命令的基本语法格式如下：

```bash
mpstat [选项] [间隔时间 [次数]]
```

其中：
- **选项**：控制输出格式和内容的参数
- **间隔时间**：指定数据刷新的时间间隔（秒）
- **次数**：指定刷新数据的次数，默认为连续刷新直到手动中断

如果不指定任何参数，mpstat将显示自系统启动以来的平均CPU统计信息。

## 3 常用选项

mpstat命令支持多种选项，用于控制输出的内容和格式。以下是一些最常用的选项：

| 选项 | 说明 |
|------|------|
| `-P {cpu\|ALL}` | 显示指定CPU或所有CPU的统计信息，其中cpu可以是CPU编号（从0开始），ALL表示所有CPU |
| `-u` | 显示CPU的使用率统计（默认选项） |
| `-I {SUM\|CPU\|SCPU\|ALL}` | 显示中断统计信息，包括总的中断次数或每个CPU的中断次数 |
| `-A` | 等同于同时使用`-u`、`-I ALL`、`-P ALL`选项，显示所有CPU的使用率和中断统计信息 |
| `-V` | 显示mpstat命令的版本信息 |
| `-x` | 在SMP模式下显示扩展的CPU统计信息 |
| `-o JSON` | 以JSON格式输出统计信息 |

### 3.1 选项组合示例

以下是一些常用的选项组合示例：

1. 显示所有CPU的使用率统计：
```bash
mpstat -P ALL
```

2. 显示特定CPU的使用率统计：
```bash
mpstat -P 0  # 显示CPU 0的统计信息
```

3. 显示所有CPU的使用率和中断统计信息：
```bash
mpstat -A
```

4. 以JSON格式显示所有CPU的统计信息：
```bash
mpstat -P ALL -o JSON
```

## 4 常用示例

### 4.1 显示所有CPU的平均使用率

**功能说明**：显示自系统启动以来所有CPU的平均使用率统计。

**命令示例**：
```bash
mpstat -P ALL
```

**输出示例**：
```
Linux 5.4.0-70-generic (server)     05/15/2023     _x86_64_    (8 CPU)

10:15:30     CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
10:15:30     all    2.34    0.01    1.22    0.08    0.00    0.05    0.00    0.00    0.00   96.30
10:15:30       0    2.45    0.01    1.25    0.08    0.00    0.07    0.00    0.00    0.00   96.14
10:15:30       1    2.21    0.01    1.19    0.08    0.00    0.04    0.00    0.00    0.00   96.47
10:15:30       2    2.39    0.01    1.24    0.08    0.00    0.06    0.00    0.00    0.00   96.22
10:15:30       3    2.41    0.01    1.25    0.08    0.00    0.06    0.00    0.00    0.00   96.20
10:15:30       4    2.29    0.01    1.20    0.08    0.00    0.04    0.00    0.00    0.00   96.38
10:15:30       5    2.35    0.01    1.23    0.08    0.00    0.05    0.00    0.00    0.00   96.28
10:15:30       6    2.30    0.01    1.21    0.08    0.00    0.05    0.00    0.00    0.00   96.35
10:15:30       7    2.38    0.01    1.22    0.08    0.00    0.05    0.00    0.00    0.00   96.26
```

**输出解释**：
- **CPU**: CPU编号，all表示所有CPU的平均值
- **%usr**: 用户空间程序占用CPU的百分比
- **%nice**: 运行nice优先级进程占用CPU的百分比
- **%sys**: 系统内核占用CPU的百分比
- **%iowait**: CPU等待I/O操作完成的时间百分比
- **%irq**: 处理硬中断占用CPU的百分比
- **%soft**: 处理软中断占用CPU的百分比
- **%steal**: 虚拟化环境中，被其他虚拟机占用的CPU百分比
- **%guest**: 运行虚拟CPU的时间百分比
- **%gnice**: 运行niced guest的时间百分比
- **%idle**: CPU空闲时间的百分比

### 4.2 实时监控CPU使用率

**功能说明**：每2秒刷新一次所有CPU的使用率统计，共刷新5次。

**命令示例**：
```bash
mpstat -P ALL 2 5
```

**输出示例**：
```
Linux 5.4.0-70-generic (server)     05/15/2023     _x86_64_    (8 CPU)

10:18:22     CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
10:18:24     all    3.25    0.00    1.50    0.12    0.00    0.06    0.00    0.00    0.00   95.07
10:18:24       0    3.45    0.00    1.55    0.12    0.00    0.08    0.00    0.00    0.00   94.80
10:18:24       1    3.10    0.00    1.45    0.12    0.00    0.05    0.00    0.00    0.00   95.28
...
```

**使用场景**：此命令适用于实时监控系统的CPU负载变化，特别是在进行性能测试或排查性能问题时非常有用。通过观察不同CPU核心的负载情况，可以判断系统是否存在负载不均衡的问题。

### 4.3 监控特定CPU的使用率

**功能说明**：监控特定CPU（如CPU 0）的使用率，每1秒刷新一次。

**命令示例**：
```bash
mpstat -P 0 1
```

**输出示例**：
```
Linux 5.4.0-70-generic (server)     05/15/2023     _x86_64_    (8 CPU)

10:20:45     CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
10:20:46       0    3.65    0.00    1.62    0.12    0.00    0.09    0.00    0.00    0.00   94.52
10:20:47       0    3.58    0.00    1.59    0.12    0.00    0.08    0.00    0.00    0.00   94.63
...
```

**使用场景**：当需要专注于监控某个特定CPU核心的性能时，可以使用此命令。这对于排查与特定进程或线程绑定到特定CPU相关的性能问题非常有用。

### 4.4 显示中断统计信息

**功能说明**：显示所有CPU的中断统计信息。

**命令示例**：
```bash
mpstat -I ALL
```

**输出示例**：
```
Linux 5.4.0-70-generic (server)     05/15/2023     _x86_64_    (8 CPU)

10:23:15     CPU    intr/s
10:23:15     all   1275.42
10:23:15       0    163.43
10:23:15       1    162.15
10:23:15       2    161.82
10:23:15       3    162.36
10:23:15       4    162.05
10:23:15       5    161.93
10:23:15       6    161.78
10:23:15       7    160.90

10:23:15     CPU        soft
10:23:15     all      146.38
10:23:15       0       18.92
10:23:15       1       18.24
10:23:15       2       18.36
10:23:15       3       18.29
10:23:15       4       18.31
10:23:15       5       18.27
10:23:15       6       18.24
10:23:15       7       18.05
```

**输出解释**：
- **intr/s**: 每秒发生的中断次数
- **soft**: 每秒发生的软中断次数

**使用场景**：中断是系统中常见的事件，过多的中断可能会导致CPU使用率升高。通过监控中断统计信息，可以识别是否存在中断风暴或中断不均衡的问题。

### 4.5 显示所有CPU的完整统计信息

**功能说明**：显示所有CPU的使用率和中断统计信息。

**命令示例**：
```bash
mpstat -A
```

**输出示例**：
```
Linux 5.4.0-70-generic (server)     05/15/2023     _x86_64_    (8 CPU)

10:25:37     CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
10:25:37     all    2.85    0.01    1.32    0.09    0.00    0.05    0.00    0.00    0.00   95.68
10:25:37       0    2.98    0.01    1.36    0.09    0.00    0.07    0.00    0.00    0.00   95.50
...

10:25:37     CPU    intr/s
10:25:37     all   1275.42
10:25:37       0    163.43
...

10:25:37     CPU        soft
10:25:37     all      146.38
10:25:37       0       18.92
...
```

**使用场景**：当需要全面了解系统中所有CPU的性能状况时，可以使用此命令。它提供了最完整的CPU统计信息，包括使用率和中断统计。

### 4.6 以JSON格式输出统计信息

**功能说明**：以JSON格式输出所有CPU的使用率统计信息，便于程序处理。

**命令示例**：
```bash
mpstat -P ALL -o JSON
```

**输出示例**：
```json
{
   "sysstat": {
      "hosts": [
         {
            "nodename": "server",
            "sysname": "Linux",
            "release": "5.4.0-70-generic",
            "machine": "x86_64",
            "number-of-cpus": 8,
            "date": "2023-05-15",
            "statistics": [
               {
                  "timestamp": "10:28:42",
                  "cpu-load": [
                     {
                        "cpu": "all",
                        "usr": 2.85,
                        "nice": 0.01,
                        "sys": 1.32,
                        "iowait": 0.09,
                        "irq": 0.00,
                        "soft": 0.05,
                        "steal": 0.00,
                        "guest": 0.00,
                        "gnice": 0.00,
                        "idle": 95.68
                     },
                     {
                        "cpu": "0",
                        "usr": 2.98,
                        "nice": 0.01,
                        "sys": 1.36,
                        "iowait": 0.09,
                        "irq": 0.00,
                        "soft": 0.07,
                        "steal": 0.00,
                        "guest": 0.00,
                        "gnice": 0.00,
                        "idle": 95.50
                     },
                     ...
                  ]
               }
            ]
         }
      ]
   }
}
```

**使用场景**：当需要将mpstat的输出结果用于自动化监控脚本或与其他程序集成时，可以使用JSON格式输出。这种格式易于被程序解析和处理。

### 4.7 监控CPU的上下文切换

**功能说明**：显示CPU的上下文切换统计信息。

**命令示例**：
```bash
mpstat -u -I CPU 1
```

**输出示例**：
```
Linux 5.4.0-70-generic (server)     05/15/2023     _x86_64_    (8 CPU)

10:30:15     CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
10:30:16     all    3.12    0.00    1.45    0.10    0.00    0.06    0.00    0.00    0.00   95.27
...
```

**使用场景**：上下文切换是CPU从一个进程或线程切换到另一个的过程，过多的上下文切换可能会导致系统性能下降。通过监控上下文切换，可以识别是否存在进程调度相关的性能问题。

### 4.8 显示CPU的软中断统计

**功能说明**：显示CPU的软中断统计信息。

**命令示例**：
```bash
mpstat -I SCPU 1
```

**输出示例**：
```
Linux 5.4.0-70-generic (server)     05/15/2023     _x86_64_    (8 CPU)

10:32:45     CPU        soft
10:32:46     all      146.52
10:32:46       0       18.95
10:32:46       1       18.26
10:32:46       2       18.38
10:32:46       3       18.31
10:32:46       4       18.33
10:32:46       5       18.29
10:32:46       6       18.26
10:32:46       7       18.04
...
```

**使用场景**：软中断是由软件触发的中断，通常用于处理延时要求不那么严格的任务。过高的软中断率可能会导致CPU使用率升高，通过监控软中断统计，可以识别是否存在相关的性能问题。

### 4.9 对比全局CPU和单个CPU的使用率

**功能说明**：显示全局CPU平均值和每个CPU的使用率，便于对比分析。

**命令示例**：
```bash
mpstat -P ALL 2
```

**输出示例**：
```
Linux 5.4.0-70-generic (server)     05/15/2023     _x86_64_    (8 CPU)

10:35:12     CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
10:35:14     all    3.05    0.00    1.42    0.10    0.00    0.06    0.00    0.00    0.00   95.37
10:35:14       0    3.25    0.00    1.47    0.10    0.00    0.08    0.00    0.00    0.00   95.10
10:35:14       1    2.98    0.00    1.39    0.10    0.00    0.05    0.00    0.00    0.00   95.48
...
```

**使用场景**：通过对比全局CPU平均值和单个CPU的使用率，可以快速识别是否存在某个CPU负载过高或过低的情况，这对于排查负载不均衡问题非常有用。

### 4.10 监控虚拟化环境中的CPU性能

**功能说明**：在虚拟化环境中监控CPU的steal时间，了解虚拟机被宿主系统抢占的情况。

**命令示例**：
```bash
mpstat -P ALL 1
```

**输出示例**：
```
Linux 5.4.0-70-generic (vm-server)     05/15/2023     _x86_64_    (4 CPU)

10:37:28     CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
10:37:29     all    4.25    0.00    1.85    0.15    0.00    0.08    2.15    0.00    0.00   91.52
10:37:29       0    4.32    0.00    1.88    0.15    0.00    0.09    2.18    0.00    0.00   91.38
...
```

**使用场景**：在虚拟化环境中，%steal值表示虚拟机被宿主系统抢占CPU时间的百分比。过高的%steal值可能会导致虚拟机性能下降，通过监控这个值，可以了解虚拟化环境的资源争用情况。

## 5 高级用法

### 5.1 CPU性能监控与告警系统

以下是一个基于mpstat命令的CPU性能监控与告警系统的完整shell脚本实现。这个脚本可以帮助您实时监控系统的CPU性能，并在发现异常时发送告警通知。

```bash
#!/bin/bash
# cpu_monitor.sh
# CPU性能监控与告警系统

# 配置参数
MONITOR_INTERVAL=5            # 监控间隔（秒）
CPU_USAGE_THRESHOLD=90        # CPU使用率告警阈值（%）
IO_WAIT_THRESHOLD=20          # I/O等待时间告警阈值（%）
STEAL_TIME_THRESHOLD=10       # 虚拟化steal时间告警阈值（%）
ALERT_EMAIL="admin@example.com"  # 告警邮件地址
ALERT_SUBJECT="CPU性能告警"
LOG_FILE="/var/log/cpu_monitor.log"
HISTORY_FILE="/var/log/cpu_history.log"
HISTORY_RETENTION_DAYS=7      # 历史数据保留天数

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # 无颜色

# 确保必要的工具已安装
check_dependencies() {
    local missing_tools=()
    
    if ! command -v mpstat &> /dev/null; then
        missing_tools+=('mpstat')
    fi
    
    if ! command -v awk &> /dev/null; then
        missing_tools+=('awk')
    fi
    
    if ! command -v mail &> /dev/null; then
        missing_tools+=('mail')
    fi
    
    if ! command -v bc &> /dev/null; then
        missing_tools+=('bc')
    fi
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        echo -e "${RED}错误: 缺少必要的工具: ${missing_tools[*]}${NC}"
        exit 1
    fi
}

# 显示帮助信息
show_help() {
    echo "CPU性能监控与告警系统"
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -h, --help            显示帮助信息"
    echo "  -i, --interval <n>    设置监控间隔(秒) (默认: $MONITOR_INTERVAL)"
    echo "  -u, --usage <n>       设置CPU使用率告警阈值(%) (默认: $CPU_USAGE_THRESHOLD)"
    echo "  -w, --iowait <n>      设置I/O等待时间告警阈值(%) (默认: $IO_WAIT_THRESHOLD)"
    echo "  -s, --steal <n>       设置虚拟化steal时间告警阈值(%) (默认: $STEAL_TIME_THRESHOLD)"
    echo "  -e, --email <email>   设置告警邮件地址 (默认: $ALERT_EMAIL)"
    echo "  -l, --log <file>      设置日志文件路径 (默认: $LOG_FILE)"
    echo "  -H, --history <file>  设置历史数据文件路径 (默认: $HISTORY_FILE)"
    echo "  -r, --retention <n>   设置历史数据保留天数 (默认: $HISTORY_RETENTION_DAYS)"
    echo "  -t, --test            测试告警功能"
    echo "  -d, --daemon          以守护进程模式运行"
    echo ""
    echo "示例:"
    echo "  # 以默认配置运行监控"
    echo "  $0"
    echo ""
    echo "  # 每10秒监控一次，CPU使用率阈值设为95%"
    echo "  $0 -i 10 -u 95"
    echo ""
    echo "  # 以守护进程模式运行"
    echo "  $0 --daemon"
    echo ""
}

# 记录日志
log_message() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # 根据日志级别选择颜色
    local color=$NC
    case $level in
        "INFO")
            color=$GREEN
            ;;
        "WARNING")
            color=$YELLOW
            ;;
        "ERROR")
            color=$RED
            ;;
        "ALERT")
            color=$RED
            ;;
    esac
    
    # 输出到控制台
    echo -e "${color}[${timestamp}] [${level}] ${message}${NC}"
    
    # 写入日志文件
    echo "[${timestamp}] [${level}] ${message}" >> $LOG_FILE
}

# 发送告警邮件
send_alert_email() {
    local subject=$1
    local message=$2
    local hostname=$(hostname)
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # 构建邮件内容
    local email_content="主机名: $hostname\n"
    email_content+="时间: $timestamp\n"
    email_content+="告警级别: 严重\n"
    email_content+="告警内容:\n$message\n"
    email_content+="\n请及时处理!"
    
    # 发送邮件
    echo -e "$email_content" | mail -s "$subject ($hostname)" $ALERT_EMAIL
    
    if [ $? -eq 0 ]; then
        log_message "INFO" "告警邮件已发送至 $ALERT_EMAIL"
    else
        log_message "ERROR" "发送告警邮件失败，请检查邮件配置"
    fi
}

# 保存历史数据
save_history() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local cpu_stats=$(mpstat -P ALL 1 1 | grep -A $(($(nproc) + 1)) 'all' | tail -n $(($(nproc) + 1)))
    
    # 将CPU统计信息写入历史文件
    echo "== $timestamp ==" >> $HISTORY_FILE
    echo "$cpu_stats" >> $HISTORY_FILE
    echo "" >> $HISTORY_FILE
    
    # 清理过期的历史数据
    find $HISTORY_FILE -mtime +$HISTORY_RETENTION_DAYS -exec truncate -s 0 {} \;
}

# 检查CPU使用率
check_cpu_usage() {
    local alert_triggered=false
    local alert_message=""
    
    # 获取CPU统计信息
    local cpu_stats=$(mpstat -P ALL 1 1 | grep -A $(($(nproc) + 1)) 'all' | tail -n $(($(nproc) + 1)))
    
    # 解析全局CPU使用率
    local all_cpu_line=$(echo "$cpu_stats" | grep 'all')
    local all_usr=$(echo "$all_cpu_line" | awk '{print $3}')
    local all_nice=$(echo "$all_cpu_line" | awk '{print $4}')
    local all_sys=$(echo "$all_cpu_line" | awk '{print $5}')
    local all_iowait=$(echo "$all_cpu_line" | awk '{print $6}')
    local all_steal=$(echo "$all_cpu_line" | awk '{print $9}')
    local all_idle=$(echo "$all_cpu_line" | awk '{print $12}')
    
    # 计算总的CPU使用率
    local all_usage=$(echo "100 - $all_idle" | bc -l)
    all_usage=$(printf "%.2f" $all_usage)
    
    # 检查全局CPU使用率
    if (( $(echo "$all_usage > $CPU_USAGE_THRESHOLD" | bc -l) )); then
        alert_triggered=true
        alert_message+="全局CPU使用率过高: ${all_usage}% (阈值: ${CPU_USAGE_THRESHOLD}%)\n"
        alert_message+="  - 用户空间: ${all_usr}%\n"
        alert_message+="  - 系统内核: ${all_sys}%\n"
        alert_message+="  - I/O等待: ${all_iowait}%\n"
        alert_message+="  - 虚拟化steal: ${all_steal}%\n"
    fi
    
    # 检查I/O等待时间
    if (( $(echo "$all_iowait > $IO_WAIT_THRESHOLD" | bc -l) )); then
        alert_triggered=true
        alert_message+="全局I/O等待时间过高: ${all_iowait}% (阈值: ${IO_WAIT_THRESHOLD}%)\n"
    fi
    
    # 检查虚拟化steal时间
    if (( $(echo "$all_steal > $STEAL_TIME_THRESHOLD" | bc -l) )); then
        alert_triggered=true
        alert_message+="虚拟化steal时间过高: ${all_steal}% (阈值: ${STEAL_TIME_THRESHOLD}%)\n"
        alert_message+="这可能表明虚拟机资源争用严重\n"
    fi
    
    # 检查各个CPU的使用率
    local high_cpu_cores=()
    while IFS= read -r line; do
        if [[ "$line" == *"all"* ]]; then
            continue
        fi
        
        local cpu_id=$(echo "$line" | awk '{print $2}')
        local cpu_idle=$(echo "$line" | awk '{print $12}')
        local cpu_usage=$(echo "100 - $cpu_idle" | bc -l)
        cpu_usage=$(printf "%.2f" $cpu_usage)
        
        if (( $(echo "$cpu_usage > $CPU_USAGE_THRESHOLD" | bc -l) )); then
            high_cpu_cores+=($cpu_id)
        fi
    done <<< "$cpu_stats"
    
    # 如果有多个CPU核心负载过高，添加到告警信息
    if [ ${#high_cpu_cores[@]} -gt 1 ]; then
        alert_triggered=true
        alert_message+="多个CPU核心负载过高: ${high_cpu_cores[*]}\n"
        alert_message+="这可能表明系统存在负载不均衡问题\n"
    fi
    
    # 如果有告警触发，记录日志并发送告警邮件
    if [ "$alert_triggered" = true ]; then
        log_message "ALERT" "CPU性能告警\n$alert_message"
        send_alert_email "$ALERT_SUBJECT" "$alert_message"
    else
        # 记录正常的CPU使用率
        log_message "INFO" "CPU使用率正常: ${all_usage}% 空闲: ${all_idle}%"
    fi
    
    # 保存历史数据
    save_history
}

# 测试告警功能
test_alert() {
    log_message "INFO" "测试告警功能..."
    
    # 构建测试告警信息
    local test_message="这是一条测试告警消息\n"
    test_message+="\nCPU使用率: 95.5% (阈值: 90%)\n"
    test_message+="I/O等待时间: 15.2% (阈值: 20%)\n"
    test_message+="虚拟化steal时间: 5.3% (阈值: 10%)\n"
    test_message+="\n此消息仅用于测试告警功能是否正常工作。"
    
    # 发送测试告警邮件
    send_alert_email "[测试] $ALERT_SUBJECT" "$test_message"
    
    log_message "INFO" "告警测试完成，请检查邮箱是否收到测试邮件"
    exit 0
}

# 以守护进程模式运行
run_as_daemon() {
    log_message "INFO" "CPU性能监控与告警系统已启动 (守护进程模式)"
    log_message "INFO" "监控间隔: ${MONITOR_INTERVAL}秒"
    log_message "INFO" "CPU使用率阈值: ${CPU_USAGE_THRESHOLD}%"
    log_message "INFO" "I/O等待时间阈值: ${IO_WAIT_THRESHOLD}%"
    log_message "INFO" "虚拟化steal时间阈值: ${STEAL_TIME_THRESHOLD}%"
    log_message "INFO" "告警邮件地址: $ALERT_EMAIL"
    
    # 主监控循环
    while true; do
        check_cpu_usage
        sleep $MONITOR_INTERVAL
    done
}

# 主函数
main() {
    # 默认配置
    RUN_AS_DAEMON=false
    
    # 解析命令行参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -i|--interval)
                if [[ $2 =~ ^[0-9]+$ && $2 -gt 0 ]]; then
                    MONITOR_INTERVAL=$2
                else
                    echo -e "${RED}错误: 监控间隔必须是正整数${NC}"
                    show_help
                    exit 1
                fi
                shift 2
                ;;
            -u|--usage)
                if [[ $2 =~ ^[0-9]+$ && $2 -gt 0 && $2 -lt 100 ]]; then
                    CPU_USAGE_THRESHOLD=$2
                else
                    echo -e "${RED}错误: CPU使用率阈值必须是1-99之间的整数${NC}"
                    show_help
                    exit 1
                fi
                shift 2
                ;;
            -w|--iowait)
                if [[ $2 =~ ^[0-9]+$ && $2 -ge 0 && $2 -lt 100 ]]; then
                    IO_WAIT_THRESHOLD=$2
                else
                    echo -e "${RED}错误: I/O等待时间阈值必须是0-99之间的整数${NC}"
                    show_help
                    exit 1
                fi
                shift 2
                ;;
            -s|--steal)
                if [[ $2 =~ ^[0-9]+$ && $2 -ge 0 && $2 -lt 100 ]]; then
                    STEAL_TIME_THRESHOLD=$2
                else
                    echo -e "${RED}错误: 虚拟化steal时间阈值必须是0-99之间的整数${NC}"
                    show_help
                    exit 1
                fi
                shift 2
                ;;
            -e|--email)
                if [[ $2 =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
                    ALERT_EMAIL=$2
                else
                    echo -e "${RED}错误: 无效的电子邮件地址${NC}"
                    show_help
                    exit 1
                fi
                shift 2
                ;;
            -l|--log)
                LOG_FILE=$2
                shift 2
                ;;
            -H|--history)
                HISTORY_FILE=$2
                shift 2
                ;;
            -r|--retention)
                if [[ $2 =~ ^[0-9]+$ && $2 -gt 0 ]]; then
                    HISTORY_RETENTION_DAYS=$2
                else
                    echo -e "${RED}错误: 历史数据保留天数必须是正整数${NC}"
                    show_help
                    exit 1
                fi
                shift 2
                ;;
            -t|--test)
                test_alert
                exit 0
                ;;
            -d|--daemon)
                RUN_AS_DAEMON=true
                shift 1
                ;;
            *)
                echo -e "${RED}未知选项: $1${NC}"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 检查依赖工具
    check_dependencies
    
    # 创建日志文件目录（如果不存在）
    mkdir -p $(dirname $LOG_FILE)
    mkdir -p $(dirname $HISTORY_FILE)
    
    # 检查日志文件是否可写
    if [ ! -w $(dirname $LOG_FILE) ]; then
        echo -e "${RED}错误: 无法写入日志文件目录 $(dirname $LOG_FILE)${NC}"
        exit 1
    fi
    
    if [ ! -w $(dirname $HISTORY_FILE) ]; then
        echo -e "${RED}错误: 无法写入历史数据文件目录 $(dirname $HISTORY_FILE)${NC}"
        exit 1
    fi
    
    # 如果以守护进程模式运行，将输出重定向到日志文件
    if [ "$RUN_AS_DAEMON" = true ]; then
        # 检查是否有root权限
        if [ $EUID -ne 0 ]; then
            echo -e "${RED}警告: 建议以root用户运行守护进程模式，以便访问系统日志目录${NC}"
        fi
        
        # 以守护进程模式运行
        run_as_daemon &
        echo -e "${GREEN}CPU性能监控与告警系统已在后台运行，进程ID: $!${NC}"
        echo -e "${GREEN}日志文件: $LOG_FILE${NC}"
    else
        # 交互式运行
        log_message "INFO" "CPU性能监控与告警系统已启动 (交互式模式)"
        log_message "INFO" "按Ctrl+C退出..."
        
        # 注册退出信号处理
        trap "log_message 'INFO' 'CPU性能监控与告警系统已停止'; exit 0" SIGINT SIGTERM
        
        # 主监控循环
        while true; do
            check_cpu_usage
            sleep $MONITOR_INTERVAL
        done
    fi
}

# 执行主函数
main "$@"
```