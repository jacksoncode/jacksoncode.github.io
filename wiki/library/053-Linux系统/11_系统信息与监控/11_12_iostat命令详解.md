# iostat命令详解

## 1 命令概述

iostat（Input/Output statistics）是一个用于监控系统输入/输出设备负载的系统监控工具，它能够报告CPU使用率和磁盘、分区、网络文件系统等设备的I/O统计信息。iostat命令生成的报告可以帮助用户更好地平衡系统负载和优化I/O设备性能。

### 1.1 功能特点

- 提供CPU使用率统计信息
- 提供设备和分区的I/O统计信息
- 可以监控特定设备或所有设备
- 支持实时监控模式
- 可以设置报告间隔和次数
- 支持显示扩展的设备统计信息
- 支持以不同的单位显示数据
- 可以显示设备的分区信息

### 1.2 应用场景

- 监控系统整体I/O性能
- 识别I/O瓶颈和性能问题
- 分析磁盘读写性能和负载
- 监控特定设备的I/O活动
- 系统性能调优和容量规划
- 排查与I/O相关的应用程序性能问题

## 2 语法格式

iostat命令的基本语法格式如下：

```bash
iostat [选项] [设备] [间隔时间 [次数]]
```

其中：
- **选项**：控制iostat命令的行为和输出格式
- **设备**：可选参数，指定要监控的设备名称，多个设备用空格分隔
- **间隔时间**：可选参数，指定两次报告之间的时间间隔（秒）
- **次数**：可选参数，指定报告的次数，与间隔时间一起使用

## 3 常用选项

iostat命令提供了多种选项来控制其行为和输出格式。以下是一些常用的选项：

| 选项 | 描述 |
|------|------|
|-c| 仅显示CPU使用率统计信息 |
|-d| 仅显示设备I/O统计信息 |
|-h| 以人类可读的格式显示输出（例如，KB、MB、GB等） |
|-k| 以KB为单位显示数据传输量 |
|-m| 以MB为单位显示数据传输量 |
|-t| 在输出中包含时间戳 |
|-V| 显示iostat的版本信息并退出 |
|-x| 显示扩展的I/O统计信息 |
|-y| 跳过第一次报告（通常包含自系统启动以来的统计信息） |
|-p [设备]| 显示设备及其所有分区的统计信息，可指定设备 |
|-N| 显示LVM2逻辑卷名称而不是设备名称 |
|-z| 仅显示活动的设备（即有I/O活动的设备） |

### 3.1 选项组合

iostat命令的选项可以组合使用，以满足不同的监控需求：

| 选项组合 | 功能描述 |
|---------|---------|
|`iostat -c`| 仅显示CPU使用率统计信息 |
|`iostat -d`| 仅显示设备I/O统计信息 |
|`iostat -dx`| 显示设备的扩展I/O统计信息 |
|`iostat -dk`| 以KB为单位显示设备I/O统计信息 |
|`iostat -dm`| 以MB为单位显示设备I/O统计信息 |
|`iostat -dt`| 显示设备I/O统计信息并包含时间戳 |
|`iostat -p sda`| 显示sda设备及其所有分区的统计信息 |
|`iostat -xy 2 5`| 每2秒显示一次扩展的设备I/O统计信息，共显示5次，并跳过第一次报告 |

## 4 常用示例

### 4.1 显示基本的CPU和设备I/O统计信息

**命令格式**：
```bash
iostat
```

**功能说明**：显示系统启动以来的CPU使用率和所有设备的I/O统计信息。

**示例输出**：
```
Linux 5.4.0-70-generic (hostname)     06/10/2023     _x86_64_    (4 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.23    0.01    0.56    0.23    0.00   98.97

device             tps    kB_read/s    kB_wrtn/s    kB_read    kB_wrtn
sda               0.89         5.67        12.34      12345      67890
sdb               0.45         2.34         5.67       5432      34567
```

**输出解释**：
- `avg-cpu`: CPU使用率统计信息
  - `%user`: 用户空间程序使用的CPU百分比
  - `%nice`: 运行优先级为nice的进程使用的CPU百分比
  - `%system`: 系统内核使用的CPU百分比
  - `%iowait`: CPU等待I/O完成的时间百分比
  - `%steal`: 虚拟机被其他虚拟机占用CPU的时间百分比
  - `%idle`: CPU空闲时间百分比
- `device`: 设备I/O统计信息
  - `tps`: 每秒传输次数（I/O操作次数）
  - `kB_read/s`: 每秒读取的数据量（KB）
  - `kB_wrtn/s`: 每秒写入的数据量（KB）
  - `kB_read`: 总共读取的数据量（KB）
  - `kB_wrtn`: 总共写入的数据量（KB）

### 4.2 仅显示设备I/O统计信息

**命令格式**：
```bash
iostat -d
```

**功能说明**：仅显示所有设备的I/O统计信息，不显示CPU使用率。

### 4.3 仅显示CPU使用率统计信息

**命令格式**：
```bash
iostat -c
```

**功能说明**：仅显示CPU使用率统计信息，不显示设备I/O统计信息。

### 4.4 显示扩展的设备I/O统计信息

**命令格式**：
```bash
iostat -x
```

**功能说明**：显示设备的扩展I/O统计信息，包括更详细的性能指标。

**示例输出**：
```
Linux 5.4.0-70-generic (hostname)     06/10/2023     _x86_64_    (4 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.23    0.01    0.56    0.23    0.00   98.97

device            r/s     w/s     rkB/s     wkB/s   avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
sda              0.56    0.33      5.67     12.34     38.45     0.01    2.34    3.45    1.23   0.56   0.05
sdb              0.23    0.22      2.34      5.67     35.67     0.00    1.23    2.34    0.56   0.34   0.01
```

**输出解释**（扩展字段）：
- `r/s`: 每秒完成的读请求次数
- `w/s`: 每秒完成的写请求次数
- `rkB/s`: 每秒读取的数据量（KB）
- `wkB/s`: 每秒写入的数据量（KB）
- `avgrq-sz`: 平均I/O请求大小（扇区）
- `avgqu-sz`: 平均I/O请求队列长度
- `await`: 平均I/O请求等待时间（毫秒）
- `r_await`: 平均读请求等待时间（毫秒）
- `w_await`: 平均写请求等待时间（毫秒）
- `svctm`: 平均I/O请求服务时间（毫秒）
- `%util`: 设备利用率百分比

### 4.5 实时监控设备I/O统计信息

**命令格式**：
```bash
iostat -dx 2 5
```

**功能说明**：每2秒显示一次扩展的设备I/O统计信息，共显示5次。

### 4.6 监控特定设备的I/O统计信息

**命令格式**：
```bash
iostat -dx sda 2
```

**功能说明**：每2秒显示一次sda设备的扩展I/O统计信息，直到手动终止。

### 4.7 显示设备及其分区的I/O统计信息

**命令格式**：
```bash
iostat -p sda
```

**功能说明**：显示sda设备及其所有分区的I/O统计信息。

### 4.8 以人类可读的格式显示I/O统计信息

**命令格式**：
```bash
iostat -h
```

**功能说明**：以人类可读的格式（如KB、MB、GB等）显示I/O统计信息。

### 4.9 显示带有时间戳的I/O统计信息

**命令格式**：
```bash
iostat -dt 2
```

**功能说明**：每2秒显示一次设备I/O统计信息，并在输出中包含时间戳。

### 4.10 仅显示活动设备的I/O统计信息

**命令格式**：
```bash
iostat -dz
```

**功能说明**：仅显示有I/O活动的设备的统计信息。

## 5 高级用法

### 5.1 系统I/O性能监控与告警系统

以下是一个基于iostat命令的系统I/O性能监控与告警系统的完整shell脚本实现。这个脚本可以监控系统的I/O性能，并在检测到异常时发送告警通知。

```bash
#!/bin/bash
# io_monitor.sh
# 系统I/O性能监控与告警系统

# 配置参数
MONITOR_INTERVAL=5                 # 监控间隔（秒）
LOG_FILE="/var/log/io_monitor.log"  # 日志文件路径
ALERT_EMAIL="admin@example.com"     # 告警邮件地址
# I/O性能阈值（根据实际情况调整）
CPU_IOWAIT_THRESHOLD=10            # CPU I/O等待时间阈值（%）
DISK_UTIL_THRESHOLD=90             # 磁盘利用率阈值（%）
DISK_AWAIT_THRESHOLD=20            # 平均I/O等待时间阈值（毫秒）
AVERAGE_CALC_INTERVAL=3            # 计算平均值的采样次数

# 确保必要的工具已安装
check_dependencies() {
    local missing_tools=()
    
    if ! command -v iostat &> /dev/null; then
        missing_tools+=('iostat')
    fi
    
    if ! command -v awk &> /dev/null; then
        missing_tools+=('awk')
    fi
    
    if ! command -v mail &> /dev/null; then
        echo "警告: 未找到mail工具，邮件告警功能将不可用"
        ALERT_EMAIL=""
    fi
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        echo "错误: 缺少必要的工具: ${missing_tools[*]}"
        exit 1
    fi
}

# 创建日志文件
create_log_file() {
    touch $LOG_FILE
    chmod 644 $LOG_FILE
    echo "日志文件已创建: $LOG_FILE"
}

# 记录日志
log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "[$timestamp] [$level] $message" >> $LOG_FILE
    
    # 控制台输出
    if [ "$level" = "ERROR" ] || [ "$level" = "ALERT" ]; then
        echo "[$timestamp] [$level] $message" >&2
    elif [ "$VERBOSE" = true ]; then
        echo "[$timestamp] [$level] $message"
    fi
}

# 发送告警邮件
send_alert_email() {
    local subject="$1"
    local body="$2"
    
    if [ -n "$ALERT_EMAIL" ]; then
        echo "$body" | mail -s "$subject" $ALERT_EMAIL
        if [ $? -eq 0 ]; then
            log "INFO" "告警邮件已发送至 $ALERT_EMAIL"
        else
            log "ERROR" "告警邮件发送失败"
        fi
    fi
}

# 监控CPU I/O等待时间
monitor_cpu_iowait() {
    local cpu_iowait=$(iostat -c | tail -n 1 | awk '{print $4}')
    local cpu_iowait_float=$(echo "$cpu_iowait" | awk '{print ($1 == "%iowait") ? 0 : $1}')
    
    # 记录CPU I/O等待时间到临时文件用于计算平均值
    echo $cpu_iowait_float >> "/tmp/io_monitor_cpu_iowait.$$"
    
    # 只保留最近AVERAGE_CALC_INTERVAL个样本
    tail -n $AVERAGE_CALC_INTERVAL "/tmp/io_monitor_cpu_iowait.$$" > "/tmp/io_monitor_cpu_iowait_temp.$$"
    mv "/tmp/io_monitor_cpu_iowait_temp.$$" "/tmp/io_monitor_cpu_iowait.$$"
    
    # 计算平均CPU I/O等待时间
    local avg_cpu_iowait=$(awk '{sum+=$1} END {print sum/NR}' "/tmp/io_monitor_cpu_iowait.$$")
    
    # 检查是否超过阈值
    if (( $(echo "$avg_cpu_iowait > $CPU_IOWAIT_THRESHOLD" | bc -l) )); then
        local alert_subject="[I/O告警] CPU I/O等待时间过高"
        local alert_body="检测到CPU I/O等待时间超过阈值！\n\n"
        alert_body+="当前平均值: $avg_cpu_iowait%\n"
        alert_body+="阈值: $CPU_IOWAIT_THRESHOLD%\n"
        alert_body+="时间: $(date '+%Y-%m-%d %H:%M:%S')\n"
        alert_body+="主机: $(hostname)\n"
        
        log "ALERT" "CPU I/O等待时间过高: $avg_cpu_iowait% (阈值: $CPU_IOWAIT_THRESHOLD%)"
        send_alert_email "$alert_subject" "$alert_body"
    fi
    
    # 记录正常的CPU I/O等待时间
    if [ "$VERBOSE" = true ]; then
        log "INFO" "CPU I/O等待时间: $cpu_iowait_float%, 平均值: $avg_cpu_iowait%"
    fi
}

# 监控磁盘I/O性能
monitor_disk_io() {
    # 获取所有磁盘的扩展I/O统计信息
    local disk_stats=$(iostat -dx | tail -n +4)
    
    while read -r line; do
        # 跳过空行
        if [ -z "$line" ]; then
            continue
        fi
        
        # 跳过平均值行
        if [[ $line == *"%util"* ]]; then
            continue
        fi
        
        # 提取磁盘信息
        local device=$(echo $line | awk '{print $1}')
        local util=$(echo $line | awk '{print $NF}')
        local await=$(echo $line | awk '{print $(NF-3)}')
        
        # 检查设备利用率是否超过阈值
        if (( $(echo "$util > $DISK_UTIL_THRESHOLD" | bc -l) )); then
            local alert_subject="[I/O告警] 磁盘利用率过高"
            local alert_body="检测到磁盘 $device 利用率超过阈值！\n\n"
            alert_body+="当前利用率: $util%\n"
            alert_body+="阈值: $DISK_UTIL_THRESHOLD%\n"
            alert_body+="时间: $(date '+%Y-%m-%d %H:%M:%S')\n"
            alert_body+="主机: $(hostname)\n"
            
            log "ALERT" "磁盘 $device 利用率过高: $util% (阈值: $DISK_UTIL_THRESHOLD%)"
            send_alert_email "$alert_subject" "$alert_body"
        fi
        
        # 检查I/O等待时间是否超过阈值
        if (( $(echo "$await > $DISK_AWAIT_THRESHOLD" | bc -l) )); then
            local alert_subject="[I/O告警] 磁盘I/O等待时间过高"
            local alert_body="检测到磁盘 $device I/O等待时间超过阈值！\n\n"
            alert_body+="当前等待时间: $await ms\n"
            alert_body+="阈值: $DISK_AWAIT_THRESHOLD ms\n"
            alert_body+="时间: $(date '+%Y-%m-%d %H:%M:%S')\n"
            alert_body+="主机: $(hostname)\n"
            
            log "ALERT" "磁盘 $device I/O等待时间过高: $await ms (阈值: $DISK_AWAIT_THRESHOLD ms)"
            send_alert_email "$alert_subject" "$alert_body"
        fi
        
        # 记录正常的磁盘I/O性能
        if [ "$VERBOSE" = true ]; then
            log "INFO" "磁盘 $device 利用率: $util%, I/O等待时间: $await ms"
        fi
    done <<< "$disk_stats"
}

# 生成每日I/O性能报告
generate_daily_report() {
    local report_file="/tmp/io_performance_report_$(date +%Y%m%d).log"
    local subject="[I/O报告] 每日I/O性能摘要"
    
    echo "==================== 每日I/O性能报告 ====================" > $report_file
    echo "报告生成时间: $(date '+%Y-%m-%d %H:%M:%S')" >> $report_file
    echo "主机名: $(hostname)" >> $report_file
    echo "=====================================================" >> $report_file
    echo "" >> $report_file
    
    # 添加当前CPU和磁盘I/O统计信息
    echo "--- 当前系统I/O状态 ---" >> $report_file
    iostat -dx >> $report_file
    echo "" >> $report_file
    
    # 添加磁盘空间使用情况
    echo "--- 磁盘空间使用情况 ---" >> $report_file
    df -h >> $report_file
    echo "" >> $report_file
    
    # 添加告警统计信息（从日志文件中提取）
    echo "--- 今日告警统计 ---" >> $report_file
    local today=$(date '+%Y-%m-%d')
    local alert_count=$(grep "$today" $LOG_FILE | grep "ALERT" | wc -l)
    echo "今日告警总数: $alert_count" >> $report_file
    
    if [ $alert_count -gt 0 ]; then
        echo "告警详情:" >> $report_file
        grep "$today" $LOG_FILE | grep "ALERT" >> $report_file
    fi
    echo "" >> $report_file
    
    # 添加系统负载信息
    echo "--- 系统负载信息 ---" >> $report_file
    uptime >> $report_file
    echo "" >> $report_file
    
    # 发送每日报告邮件
    if [ -n "$ALERT_EMAIL" ]; then
        cat $report_file | mail -s "$subject" $ALERT_EMAIL
        if [ $? -eq 0 ]; then
            log "INFO" "每日I/O性能报告已发送至 $ALERT_EMAIL"
        else
            log "ERROR" "每日I/O性能报告发送失败"
        fi
    fi
    
    # 清理临时报告文件
    rm -f $report_file
}

# 显示帮助信息
show_help() {
    echo "系统I/O性能监控与告警系统"
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -h, --help            显示帮助信息"
    echo "  -i, --interval <n>    设置监控间隔(秒) (默认: $MONITOR_INTERVAL)"
    echo "  -l, --log <file>      设置日志文件路径 (默认: $LOG_FILE)"
    echo "  -e, --email <email>   设置告警邮件地址 (默认: $ALERT_EMAIL)"
    echo "  -v, --verbose         启用详细输出模式"
    echo "  --cpu-threshold <n>   设置CPU I/O等待时间阈值(%) (默认: $CPU_IOWAIT_THRESHOLD)"
    echo "  --disk-threshold <n>  设置磁盘利用率阈值(%) (默认: $DISK_UTIL_THRESHOLD)"
    echo "  --await-threshold <n> 设置I/O等待时间阈值(ms) (默认: $DISK_AWAIT_THRESHOLD)"
    echo "  --generate-report     立即生成并发送I/O性能报告"
    echo "  --test-alert          发送测试告警邮件"
    echo ""
    echo "示例:"
    echo "  # 以默认配置启动监控"
    echo "  $0"
    echo ""
    echo "  # 每10秒监控一次，并启用详细输出模式"
    echo "  $0 -i 10 -v"
    echo ""
    echo "  # 自定义告警阈值"
    echo "  $0 --cpu-threshold 15 --disk-threshold 95 --await-threshold 25"
    echo ""
}

# 主函数
main() {
    # 默认配置
    VERBOSE=false
    
    # 解析命令行参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -i|--interval)
                MONITOR_INTERVAL=$2
                shift 2
                ;;
            -l|--log)
                LOG_FILE=$2
                shift 2
                ;;
            -e|--email)
                ALERT_EMAIL=$2
                shift 2
                ;;
            -v|--verbose)
                VERBOSE=true
                shift 1
                ;;
            --cpu-threshold)
                CPU_IOWAIT_THRESHOLD=$2
                shift 2
                ;;
            --disk-threshold)
                DISK_UTIL_THRESHOLD=$2
                shift 2
                ;;
            --await-threshold)
                DISK_AWAIT_THRESHOLD=$2
                shift 2
                ;;
            --generate-report)
                generate_daily_report
                exit 0
                ;;
            --test-alert)
                log "INFO" "发送测试告警邮件"
                send_alert_email "[测试] I/O监控系统告警" "这是一封测试邮件，用于验证I/O监控系统的告警功能正常工作。\n\n时间: $(date '+%Y-%m-%d %H:%M:%S')\n主机: $(hostname)"
                exit 0
                ;;
            *)
                echo "未知选项: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 检查依赖工具
    check_dependencies
    
    # 创建日志文件
    if [ ! -f $LOG_FILE ]; then
        create_log_file
    fi
    
    # 记录启动信息
    log "INFO" "系统I/O性能监控与告警系统已启动"
    log "INFO" "监控间隔: $MONITOR_INTERVAL 秒"
    log "INFO" "CPU I/O等待时间阈值: $CPU_IOWAIT_THRESHOLD%"
    log "INFO" "磁盘利用率阈值: $DISK_UTIL_THRESHOLD%"
    log "INFO" "I/O等待时间阈值: $DISK_AWAIT_THRESHOLD ms"
    
    if [ -n "$ALERT_EMAIL" ]; then
        log "INFO" "告警邮件将发送至: $ALERT_EMAIL"
    else
        log "INFO" "告警邮件功能已禁用"
    fi
    
    # 创建临时文件
    touch "/tmp/io_monitor_cpu_iowait.$$"
    
    # 注册退出信号处理
    trap "log 'INFO' '系统I/O性能监控与告警系统已停止'; rm -f '/tmp/io_monitor_cpu_iowait.$$'; exit 0" SIGINT SIGTERM
    
    # 记录上次生成报告的日期
    local last_report_date=""
    
    # 主监控循环
    while true; do
        # 监控CPU I/O等待时间
        monitor_cpu_iowait
        
        # 监控磁盘I/O性能
        monitor_disk_io
        
        # 每天生成一次性能报告
        local current_date=$(date '+%Y-%m-%d')
        if [ "$current_date" != "$last_report_date" ]; then
            generate_daily_report
            last_report_date=$current_date
        fi
        
        # 等待下一次监控
        sleep $MONITOR_INTERVAL
    done
}

# 执行主函数
main "$@"

### 5.2 磁盘I/O性能分析工具

以下是一个基于iostat命令的磁盘I/O性能分析工具的完整shell脚本实现。这个脚本可以帮助您深入分析系统的磁盘I/O性能，并生成详细的性能报告。

```bash
#!/bin/bash
# disk_io_analyzer.sh
# 磁盘I/O性能分析工具

# 配置参数
OUTPUT_FORMAT="table"  # 输出格式: table, csv, json
REPORT_FILE="disk_io_report.txt"  # 报告文件路径
ANALYSIS_DURATION=60  # 分析持续时间(秒)
SAMPLE_INTERVAL=5     # 采样间隔(秒)

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # 无颜色

# 确保必要的工具已安装
check_dependencies() {
    local missing_tools=()
    
    if ! command -v iostat &> /dev/null; then
        missing_tools+=('iostat')
    fi
    
    if ! command -v awk &> /dev/null; then
        missing_tools+=('awk')
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
    echo "磁盘I/O性能分析工具"
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -h, --help            显示帮助信息"
    echo "  -o, --output <format> 设置输出格式(table, csv, json) (默认: $OUTPUT_FORMAT)"
    echo "  -f, --file <file>     设置报告文件路径 (默认: $REPORT_FILE)"
    echo "  -d, --duration <sec>  设置分析持续时间(秒) (默认: $ANALYSIS_DURATION)"
    echo "  -i, --interval <sec>  设置采样间隔(秒) (默认: $SAMPLE_INTERVAL)"
    echo "  -v, --verbose         启用详细输出模式"
    echo "  -s, --show-only       仅显示结果，不保存到文件"
    echo ""
    echo "示例:"
    echo "  # 以默认配置运行分析"
    echo "  $0"
    echo ""
    echo "  # 运行120秒分析，每2秒采样一次，输出为CSV格式"
    echo "  $0 -d 120 -i 2 -o csv"
    echo ""
    echo "  # 仅显示分析结果，不保存到文件"
    echo "  $0 -s"
    echo ""
}

# 分析磁盘I/O性能
analyze_disk_io() {
    local devices=()
    local device_data=()
    local sample_count=0
    local max_samples=$((ANALYSIS_DURATION / SAMPLE_INTERVAL))
    
    echo -e "${BLUE}开始磁盘I/O性能分析，持续时间: ${ANALYSIS_DURATION}秒，采样间隔: ${SAMPLE_INTERVAL}秒${NC}"
    
    # 确定要监控的设备
    local initial_devices=$(iostat -d | tail -n +4 | grep -v '^$' | awk '{print $1}')
    
    # 转换为数组
    while IFS= read -r line; do
        if [[ ! "$line" =~ ^(Linux|avg-cpu|device|$) ]]; then
            devices+=($line)
        fi
    done <<< "$initial_devices"
    
    if [ ${#devices[@]} -eq 0 ]; then
        echo -e "${RED}错误: 未检测到任何磁盘设备${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}监控的设备: ${devices[*]}${NC}"
    
    # 初始化设备数据数组
    for device in "${devices[@]}"; do
        device_data["${device}_r"]=""
        device_data["${device}_w"]=""
        device_data["${device}_rkB"]=""
        device_data["${device}_wkB"]=""
        device_data["${device}_avgrq"]=""
        device_data["${device}_avgqu"]=""
        device_data["${device}_await"]=""
        device_data["${device}_svctm"]=""
        device_data["${device}_util"]=""
    done
    
    # 采样循环
    while [ $sample_count -lt $max_samples ]; do
        local current_time=$(date '+%Y-%m-%d %H:%M:%S')
        echo -ne "${YELLOW}采样进度: ${sample_count}/${max_samples} [${current_time}]\r${NC}"
        
        # 获取扩展的I/O统计信息
        local stats=$(iostat -dx $SAMPLE_INTERVAL 1 | tail -n +4)
        
        # 解析并存储统计信息
        while IFS= read -r line; do
            if [[ "$line" == *"%util"* || -z "$line" ]]; then
                continue
            fi
            
            local device=$(echo "$line" | awk '{print $1}')
            local r=$(echo "$line" | awk '{print $2}')       # r/s
            local w=$(echo "$line" | awk '{print $3}')       # w/s
            local rkB=$(echo "$line" | awk '{print $4}')     # rkB/s
            local wkB=$(echo "$line" | awk '{print $5}')     # wkB/s
            local avgrq=$(echo "$line" | awk '{print $6}')   # avgrq-sz
            local avgqu=$(echo "$line" | awk '{print $7}')   # avgqu-sz
            local await=$(echo "$line" | awk '{print $8}')   # await
            local svctm=$(echo "$line" | awk '{print $(NF-1)}') # svctm
            local util=$(echo "$line" | awk '{print $NF}')   # %util
            
            if [[ "${devices[*]}" == *"$device"* ]]; then
                device_data["${device}_r"]+="$r "
                device_data["${device}_w"]+="$w "
                device_data["${device}_rkB"]+="$rkB "
                device_data["${device}_wkB"]+="$wkB "
                device_data["${device}_avgrq"]+="$avgrq "
                device_data["${device}_avgqu"]+="$avgqu "
                device_data["${device}_await"]+="$await "
                device_data["${device}_svctm"]+="$svctm "
                device_data["${device}_util"]+="$util "
            fi
        done <<< "$stats"
        
        ((sample_count++))
    done
    
    echo -e "\n${GREEN}分析完成，开始生成报告...${NC}"
    
    # 生成报告
    generate_report "${devices[@]}" "${device_data[@]}"
}

# 计算数组的统计信息（最小值、最大值、平均值）
calculate_stats() {
    local values=($1)
    local min=${values[0]}
    local max=${values[0]}
    local sum=0
    local count=${#values[@]}
    
    for val in "${values[@]}"; do
        # 跳过非数字值
        if ! [[ "$val" =~ ^[0-9.]+$ ]]; then
            continue
        fi
        
        # 更新最小值
        if (( $(echo "$val < $min" | bc -l) )); then
            min=$val
        fi
        
        # 更新最大值
        if (( $(echo "$val > $max" | bc -l) )); then
            max=$val
        fi
        
        # 累加求和
        sum=$(echo "$sum + $val" | bc -l)
    done
    
    # 计算平均值
    local avg=$(echo "scale=2; $sum / $count" | bc -l)
    
    # 返回统计信息（最小值、最大值、平均值）
    echo "$min $max $avg"
}

# 评估I/O性能状态
evaluate_performance() {
    local metric="$1"
    local value="$2"
    local status=""
    
    case $metric in
        "util") # %util
            if (( $(echo "$value < 50" | bc -l) )); then
                status="${GREEN}良好${NC}"
            elif (( $(echo "$value < 80" | bc -l) )); then
                status="${YELLOW}中等${NC}"
            else
                status="${RED}严重${NC}"
            fi
            ;;
        "await") # await (ms)
            if (( $(echo "$value < 10" | bc -l) )); then
                status="${GREEN}良好${NC}"
            elif (( $(echo "$value < 20" | bc -l) )); then
                status="${YELLOW}中等${NC}"
            else
                status="${RED}严重${NC}"
            fi
            ;;
        "avgqu") # avgqu-sz
            if (( $(echo "$value < 0.1" | bc -l) )); then
                status="${GREEN}良好${NC}"
            elif (( $(echo "$value < 1" | bc -l) )); then
                status="${YELLOW}中等${NC}"
            else
                status="${RED}严重${NC}"
            fi
            ;;
        *)
            status="${BLUE}N/A${NC}"
            ;;
    esac
    
    echo "$status"
}

# 生成性能报告
generate_report() {
    local devices=($1)
    local report_content=""
    local report_header=""
    local current_time=$(date '+%Y-%m-%d %H:%M:%S')
    
    # 生成报告头部
    case $OUTPUT_FORMAT in
        "table")
            report_header="==================== 磁盘I/O性能分析报告 =======================\n"
            report_header+="报告生成时间: $current_time\n"
            report_header+="分析持续时间: ${ANALYSIS_DURATION}秒\n"
            report_header+="采样间隔: ${SAMPLE_INTERVAL}秒\n"
            report_header+="主机名: $(hostname)\n"
            report_header+="=============================================================\n"
            ;;
        "csv")
            report_header="设备名称,r/s(最小),r/s(最大),r/s(平均),w/s(最小),w/s(最大),w/s(平均),"
            report_header+="rkB/s(最小),rkB/s(最大),rkB/s(平均),wkB/s(最小),wkB/s(最大),wkB/s(平均),"
            report_header+="avgrq-sz(最小),avgrq-sz(最大),avgrq-sz(平均),avgqu-sz(最小),avgqu-sz(最大),avgqu-sz(平均),"
            report_header+="await(最小),await(最大),await(平均),svctm(最小),svctm(最大),svctm(平均),"
            report_header+="%util(最小),%util(最大),%util(平均),await状态,avgqu状态,util状态\n"
            ;;
        "json")
            report_content="{\n  \"report_time\": \"$current_time\",\n"
            report_content+="  \"duration\": $ANALYSIS_DURATION,\n"
            report_content+="  \"interval\": $SAMPLE_INTERVAL,\n"
            report_content+="  \"hostname\": \"$(hostname)\",\n"
            report_content+="  \"devices\": {\n"
            ;;
    esac
    
    report_content+="$report_header"
    
    local device_count=${#devices[@]}
    local current_device=0
    
    # 生成设备性能数据
    for device in "${devices[@]}"; do
        ((current_device++))
        
        # 计算每个指标的统计信息
        local r_stats=($(calculate_stats "${!device_data[@]:1:1}")) # ${device_data["${device}_r"]}
        local w_stats=($(calculate_stats "${!device_data[@]:2:1}")) # ${device_data["${device}_w"]}
        local rkB_stats=($(calculate_stats "${!device_data[@]:3:1}")) # ${device_data["${device}_rkB"]}
        local wkB_stats=($(calculate_stats "${!device_data[@]:4:1}")) # ${device_data["${device}_wkB"]}
        local avgrq_stats=($(calculate_stats "${!device_data[@]:5:1}")) # ${device_data["${device}_avgrq"]}
        local avgqu_stats=($(calculate_stats "${!device_data[@]:6:1}")) # ${device_data["${device}_avgqu"]}
        local await_stats=($(calculate_stats "${!device_data[@]:7:1}")) # ${device_data["${device}_await"]}
        local svctm_stats=($(calculate_stats "${!device_data[@]:8:1}")) # ${device_data["${device}_svctm"]}
        local util_stats=($(calculate_stats "${!device_data[@]:9:1}")) # ${device_data["${device}_util"]}
        
        # 评估性能状态
        local await_status=$(evaluate_performance "await" ${await_stats[2]})
        local avgqu_status=$(evaluate_performance "avgqu" ${avgqu_stats[2]})
        local util_status=$(evaluate_performance "util" ${util_stats[2]})
        
        # 格式化设备数据
        case $OUTPUT_FORMAT in
            "table")
                report_content+="\n设备: ${BLUE}$device${NC}\n"
                report_content+="--------------------------------------------------------------------------------\n"
                report_content+="指标           最小值     最大值     平均值     状态\n"
                report_content+="--------------------------------------------------------------------------------\n"
                report_content+="读取请求(次/秒)  ${r_stats[0]}       ${r_stats[1]}       ${r_stats[2]}       ${BLUE}N/A${NC}\n"
                report_content+="写入请求(次/秒)  ${w_stats[0]}       ${w_stats[1]}       ${w_stats[2]}       ${BLUE}N/A${NC}\n"
                report_content+="读取速度(KB/秒)  ${rkB_stats[0]}       ${rkB_stats[1]}       ${rkB_stats[2]}       ${BLUE}N/A${NC}\n"
                report_content+="写入速度(KB/秒)  ${wkB_stats[0]}       ${wkB_stats[1]}       ${wkB_stats[2]}       ${BLUE}N/A${NC}\n"
                report_content+="平均请求大小     ${avgrq_stats[0]}       ${avgrq_stats[1]}       ${avgrq_stats[2]}       ${BLUE}N/A${NC}\n"
                report_content+="平均队列长度     ${avgqu_stats[0]}       ${avgqu_stats[1]}       ${avgqu_stats[2]}       $avgqu_status\n"
                report_content+="平均等待时间(ms) ${await_stats[0]}       ${await_stats[1]}       ${await_stats[2]}       $await_status\n"
                report_content+="平均服务时间(ms) ${svctm_stats[0]}       ${svctm_stats[1]}       ${svctm_stats[2]}       ${BLUE}N/A${NC}\n"
                report_content+="设备利用率(%)   ${util_stats[0]}       ${util_stats[1]}       ${util_stats[2]}       $util_status\n"
                report_content+="--------------------------------------------------------------------------------\n"
                ;;
            "csv")
                report_content+="$device,${r_stats[0]},${r_stats[1]},${r_stats[2]},${w_stats[0]},${w_stats[1]},${w_stats[2]},"
                report_content+="${rkB_stats[0]},${rkB_stats[1]},${rkB_stats[2]},${wkB_stats[0]},${wkB_stats[1]},${wkB_stats[2]},"
                report_content+="${avgrq_stats[0]},${avgrq_stats[1]},${avgrq_stats[2]},${avgqu_stats[0]},${avgqu_stats[1]},${avgqu_stats[2]},"
                report_content+="${await_stats[0]},${await_stats[1]},${await_stats[2]},${svctm_stats[0]},${svctm_stats[1]},${svctm_stats[2]},"
                report_content+="${util_stats[0]},${util_stats[1]},${util_stats[2]},$(echo $await_status | sed 's/\x1b\[[0-9;]*m//g'),"
                report_content+="$(echo $avgqu_status | sed 's/\x1b\[[0-9;]*m//g'),$(echo $util_status | sed 's/\x1b\[[0-9;]*m//g')\n"
                ;;
            "json")
                report_content+="    \"$device\": {\n"
                report_content+="      \"r\": {\"min\": ${r_stats[0]}, \"max\": ${r_stats[1]}, \"avg\": ${r_stats[2]}},\n"
                report_content+="      \"w\": {\"min\": ${w_stats[0]}, \"max\": ${w_stats[1]}, \"avg\": ${w_stats[2]}},\n"
                report_content+="      \"rkB\": {\"min\": ${rkB_stats[0]}, \"max\": ${rkB_stats[1]}, \"avg\": ${rkB_stats[2]}},\n"
                report_content+="      \"wkB\": {\"min\": ${wkB_stats[0]}, \"max\": ${wkB_stats[1]}, \"avg\": ${wkB_stats[2]}},\n"
                report_content+="      \"avgrq\": {\"min\": ${avgrq_stats[0]}, \"max\": ${avgrq_stats[1]}, \"avg\": ${avgrq_stats[2]}},\n"
                report_content+="      \"avgqu\": {\"min\": ${avgqu_stats[0]}, \"max\": ${avgqu_stats[1]}, \"avg\": ${avgqu_stats[2]}},\n"
                report_content+="      \"await\": {\"min\": ${await_stats[0]}, \"max\": ${await_stats[1]}, \"avg\": ${await_stats[2]}},\n"
                report_content+="      \"svctm\": {\"min\": ${svctm_stats[0]}, \"max\": ${svctm_stats[1]}, \"avg\": ${svctm_stats[2]}},\n"
                report_content+="      \"util\": {\"min\": ${util_stats[0]}, \"max\": ${util_stats[1]}, \"avg\": ${util_stats[2]}},\n"
                report_content+="      \"status\": {\n"
                report_content+="        \"await\": \"$(echo $await_status | sed 's/\x1b\[[0-9;]*m//g')\",\n"
                report_content+="        \"avgqu\": \"$(echo $avgqu_status | sed 's/\x1b\[[0-9;]*m//g')\",\n"
                report_content+="        \"util\": \"$(echo $util_status | sed 's/\x1b\[[0-9;]*m//g')\"\n"
                report_content+="      }\n"
                report_content+="    }"
                
                # 添加逗号分隔符（除了最后一个设备）
                if [ $current_device -lt $device_count ]; then
                    report_content+=","
                fi
                
                report_content+="\n"
                ;;
        esac
    done
    
    # 完成JSON格式
    if [ "$OUTPUT_FORMAT" = "json" ]; then
        report_content+="  }\n}"
    fi
    
    # 显示和/或保存报告
    if [ "$SHOW_ONLY" = true ]; then
        echo -e "\n$report_content"
    else
        echo -e "$report_content" > $REPORT_FILE
        echo -e "${GREEN}报告已保存至: $REPORT_FILE${NC}"
        
        # 如果是表格格式，也显示在控制台
        if [ "$OUTPUT_FORMAT" = "table" ]; then
            echo -e "\n$report_content"
        fi
    fi
    
    # 生成性能分析建议
    generate_recommendations "${devices[@]}" "${device_data[@]}"
}

# 生成性能分析建议
generate_recommendations() {
    local devices=($1)
    local recommendations=""
    local has_recommendations=false
    
    echo -e "\n${BLUE}===== 性能优化建议 =====${NC}"
    
    # 分析每个设备的性能
    for device in "${devices[@]}"; do
        # 获取设备的平均指标
        local r_stats=($(calculate_stats "${!device_data[@]:1:1}")) # ${device_data["${device}_r"]}
        local w_stats=($(calculate_stats "${!device_data[@]:2:1}")) # ${device_data["${device}_w"]}
        local rkB_stats=($(calculate_stats "${!device_data[@]:3:1}")) # ${device_data["${device}_rkB"]}
        local wkB_stats=($(calculate_stats "${!device_data[@]:4:1}")) # ${device_data["${device}_wkB"]}
        local avgqu_stats=($(calculate_stats "${!device_data[@]:6:1}")) # ${device_data["${device}_avgqu"]}
        local await_stats=($(calculate_stats "${!device_data[@]:7:1}")) # ${device_data["${device}_await"]}
        local util_stats=($(calculate_stats "${!device_data[@]:9:1}")) # ${device_data["${device}_util"]}
        
        # 检查是否需要建议
        if (( $(echo "${util_stats[2]} > 80" | bc -l) )); then
            recommendations+="\n设备 $device 的利用率过高 (${util_stats[2]}%)。建议：\n"
            recommendations+="  1. 考虑将部分I/O负载迁移到其他磁盘\n"
            recommendations+="  2. 检查是否有进程在进行大量的读写操作\n"
            recommendations+="  3. 考虑使用更快的存储设备\n"
            has_recommendations=true
        fi
        
        if (( $(echo "${await_stats[2]} > 20" | bc -l) )); then
            recommendations+="\n设备 $device 的I/O等待时间过长 (${await_stats[2]} ms)。建议：\n"
            recommendations+="  1. 检查是否有大量随机I/O操作\n"
            recommendations+="  2. 考虑优化文件系统参数\n"
            recommendations+="  3. 检查存储设备的健康状态\n"
            has_recommendations=true
        fi
        
        if (( $(echo "${avgqu_stats[2]} > 1" | bc -l) )); then
            recommendations+="\n设备 $device 的I/O队列过长 (${avgqu_stats[2]})。建议：\n"
            recommendations+="  1. 减少并发I/O操作的数量\n"
            recommendations+="  2. 考虑使用I/O调度器优化队列\n"
            recommendations+="  3. 检查是否有进程阻塞I/O\n"
            has_recommendations=true
        fi
        
        # 检查读写平衡
        local total_ops=$(echo "${r_stats[2]} + ${w_stats[2]}" | bc -l)
        if (( $(echo "$total_ops > 0" | bc -l) )); then
            local read_percent=$(echo "scale=2; ${r_stats[2]} / $total_ops * 100" | bc -l)
            local write_percent=$(echo "scale=2; ${w_stats[2]} / $total_ops * 100" | bc -l)
            
            if (( $(echo "$read_percent > 90" | bc -l) )); then
                recommendations+="\n设备 $device 的读写比例不平衡，读取操作占主导 ($read_percent%)。建议：\n"
                recommendations+="  1. 考虑使用缓存机制减少读取操作\n"
                recommendations+="  2. 优化数据访问模式，减少随机读取\n"
                has_recommendations=true
            elif (( $(echo "$write_percent > 90" | bc -l) )); then
                recommendations+="\n设备 $device 的读写比例不平衡，写入操作占主导 ($write_percent%)。建议：\n"
                recommendations+="  1. 考虑批处理写入操作\n"
                recommendations+="  2. 优化应用程序的写入模式\n"
                has_recommendations=true
            fi
        fi
    done
    
    # 显示建议
    if [ "$has_recommendations" = true ]; then
        echo -e "$recommendations"
        
        # 如果保存报告，也保存建议
        if [ "$SHOW_ONLY" != true ]; then
            echo -e "$recommendations" >> $REPORT_FILE
        fi
    else
        echo -e "${GREEN}所有设备的I/O性能指标均在正常范围内，无需特殊优化。${NC}"
    fi
}

# 主函数
main() {
    # 默认配置
    VERBOSE=false
    SHOW_ONLY=false
    
    # 解析命令行参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -o|--output)
                if [[ "$2" == "table" || "$2" == "csv" || "$2" == "json" ]]; then
                    OUTPUT_FORMAT=$2
                else
                    echo -e "${RED}错误: 不支持的输出格式 '$2'，支持的格式为: table, csv, json${NC}"
                    show_help
                    exit 1
                fi
                shift 2
                ;;
            -f|--file)
                REPORT_FILE=$2
                shift 2
                ;;
            -d|--duration)
                if [[ $2 =~ ^[0-9]+$ && $2 -gt 0 ]]; then
                    ANALYSIS_DURATION=$2
                else
                    echo -e "${RED}错误: 分析持续时间必须是正整数${NC}"
                    show_help
                    exit 1
                fi
                shift 2
                ;;
            -i|--interval)
                if [[ $2 =~ ^[0-9]+$ && $2 -gt 0 ]]; then
                    SAMPLE_INTERVAL=$2
                else
                    echo -e "${RED}错误: 采样间隔必须是正整数${NC}"
                    show_help
                    exit 1
                fi
                shift 2
                ;;
            -v|--verbose)
                VERBOSE=true
                shift 1
                ;;
            -s|--show-only)
                SHOW_ONLY=true
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
    
    # 分析磁盘I/O性能
    analyze_disk_io
}

# 执行主函数
main "$@"
```

### 5.3 I/O性能可视化仪表盘

以下是一个基于iostat命令的I/O性能可视化仪表盘的完整shell脚本实现。这个脚本可以实时监控并以ASCII图表的形式展示系统的I/O性能。

```bash
#!/bin/bash
# io_dashboard.sh
# I/O性能可视化仪表盘

# 配置参数
REFRESH_INTERVAL=2         # 刷新间隔（秒）
CHART_HEIGHT=10            # 图表高度
DISK_UTIL_THRESHOLD=90     # 磁盘利用率阈值（%）
DISPLAY_DEVICES=""          # 要显示的设备，逗号分隔，空表示所有设备
SHOW_CPU_IO=false          # 是否显示CPU I/O等待时间

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # 无颜色

# 确保必要的工具已安装
check_dependencies() {
    local missing_tools=()
    
    if ! command -v iostat &> /dev/null; then
        missing_tools+=('iostat')
    fi
    
    if ! command -v awk &> /dev/null; then
        missing_tools+=('awk')
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
    echo "I/O性能可视化仪表盘"
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -h, --help            显示帮助信息"
    echo "  -i, --interval <n>    设置刷新间隔(秒) (默认: $REFRESH_INTERVAL)"
    echo "  -H, --height <n>      设置图表高度 (默认: $CHART_HEIGHT)"
    echo "  -d, --devices <devs>  指定要显示的设备，逗号分隔 (默认: 所有设备)"
    echo "  -c, --cpu             显示CPU I/O等待时间"
    echo "  -t, --threshold <n>   设置磁盘利用率警告阈值(%) (默认: $DISK_UTIL_THRESHOLD)"
    echo ""
    echo "示例:"
    echo "  # 以默认配置启动仪表盘"
    echo "  $0"
    echo ""
    echo "  # 每1秒刷新一次，显示CPU I/O等待时间"
    echo "  $0 -i 1 -c"
    echo ""
    echo "  # 只显示sda和sdb设备，图表高度为15"
    echo "  $0 -d sda,sdb -H 15"
    echo ""
}

# 清屏
clear_screen() {
    printf "\033[2J\033[H"
}

# 绘制水平条形图
draw_horizontal_bar() {
    local value=$1
    local max_value=$2
    local width=$3
    local color=$4
    
    # 计算条形图的长度
    local bar_length=$(echo "scale=0; $value * $width / $max_value" | bc -l)
    bar_length=${bar_length%.*} # 取整
    
    # 确保条形图长度在合理范围内
    if [ $bar_length -lt 0 ]; then
        bar_length=0
    elif [ $bar_length -gt $width ]; then
        bar_length=$width
    fi
    
    # 绘制条形图
    echo -n "${color}"
    for ((i=0; i<bar_length; i++)); do
        echo -n "█"
    done
    echo -n "${NC}"
    
    # 填充剩余空间
    for ((i=bar_length; i<width; i++)); do
        echo -n " "
    done
}

# 绘制垂直条形图
draw_vertical_chart() {
    local values=($1)        # 值数组
    local labels=($2)        # 标签数组
    local max_value=$3       # 最大值
    local chart_title=$4     # 图表标题
    local value_unit=$5      # 值单位
    
    local num_values=${#values[@]}
    local chart_width=$((num_values * 3)) # 每个柱子占用3个字符宽度
    
    # 打印图表标题
    printf "%s\n" "${CYAN}${chart_title}${NC}"
    
    # 从顶部到底部绘制图表
    for ((h=CHART_HEIGHT; h>=0; h--)); do
        # 计算当前行的高度百分比
        local height_percent=$(echo "scale=2; $h * 100 / $CHART_HEIGHT" | bc -l)
        local height_value=$(echo "scale=2; $h * $max_value / $CHART_HEIGHT" | bc -l)
        
        # 打印Y轴刻度
        printf "%5.1f %s  " "$height_value" "$value_unit"
        
        # 绘制每个柱子
        for ((i=0; i<num_values; i++)); do
            local value=${values[$i]}
            
            # 确定使用的颜色
            local color=$GREEN
            if (( $(echo "$value > 0.8 * $max_value" | bc -l) )); then
                color=$RED
            elif (( $(echo "$value > 0.5 * $max_value" | bc -l) )); then
                color=$YELLOW
            fi
            
            # 绘制柱子部分
            if (( $(echo "$value >= $height_value" | bc -l) )); then
                echo -ne "${color}██${NC} "
            else
                echo -ne "   "
            fi
        done
        echo ""
    done
    
    # 打印X轴
    printf "%8s" ""
    for ((i=0; i<chart_width; i++)); do
        echo -n "-"
    done
    echo ""
    
    # 打印X轴标签
    printf "%8s" ""
    for label in "${labels[@]}"; do
        printf "%-3s" "$label"
    done
    echo "\n"
}

# 获取设备列表
get_device_list() {
    local all_devices=()
    local filtered_devices=()
    
    # 获取所有设备
    local device_lines=$(iostat -d | tail -n +4 | grep -v '^$')
    
    while IFS= read -r line; do
        if [[ ! "$line" =~ ^(Linux|avg-cpu|device|$) ]]; then
            local device=$(echo "$line" | awk '{print $1}')
            all_devices+=($device)
        fi
    done <<< "$device_lines"
    
    # 过滤设备
    if [ -z "$DISPLAY_DEVICES" ]; then
        filtered_devices=(${all_devices[@]})
    else
        IFS=',' read -ra selected_devices <<< "$DISPLAY_DEVICES"
        for dev in "${selected_devices[@]}"; do
            if [[ "${all_devices[*]}" == *"$dev"* ]]; then
                filtered_devices+=($dev)
            fi
        done
    fi
    
    echo "${filtered_devices[@]}"
}

# 监控I/O性能并显示仪表盘
monitor_io_performance() {
    local devices=($(get_device_list))
    
    if [ ${#devices[@]} -eq 0 ]; then
        echo -e "${RED}错误: 未检测到任何磁盘设备${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}I/O性能可视化仪表盘已启动，按Ctrl+C退出...${NC}\n"
    
    # 注册退出信号处理
    trap "echo -e '\n${GREEN}仪表盘已停止${NC}'; exit 0" SIGINT SIGTERM
    
    # 历史数据，用于图表显示
    local history_data=()
    local history_size=10 # 保存10个历史数据点
    
    # 初始化历史数据
    for ((i=0; i<history_size; i++)); do
        history_data[$i]="0 $(printf '0 %.0s' $(seq 1 $((${#devices[@]}-1))))"
    done
    
    # 主监控循环
    while true; do
        clear_screen
        
        # 获取当前时间
        local current_time=$(date '+%Y-%m-%d %H:%M:%S')
        
        # 打印标题和时间
        echo -e "${WHITE}==================================== I/O性能仪表盘 ====================================${NC}"
        echo -e "${CYAN}时间: $current_time${NC}"
        echo -e "${WHITE}======================================================================================${NC}\n"
        
        # 获取I/O统计信息
        local io_stats=$(iostat -dx)
        
        # 如果启用CPU I/O等待时间显示
        if [ "$SHOW_CPU_IO" = true ]; then
            local cpu_io_wait=$(echo "$io_stats" | grep -A1 'avg-cpu' | tail -n 1 | awk '{print $4}')
            echo -e "${MAGENTA}CPU I/O等待时间:${NC}"
            draw_horizontal_bar $cpu_io_wait 100 50 "$CYAN"
            echo -e " ${cpu_io_wait}%"
            echo ""
        fi
        
        # 打印设备I/O统计信息表格
        echo -e "${WHITE}设备名称    读取(KB/s)    写入(KB/s)    利用率(%)    状态${NC}"
        echo -e "${WHITE}--------------------------------------------------------------------------------${NC}"
        
        # 解析并显示设备统计信息
        local current_util_values=()
        local current_rkB_values=()
        local current_wkB_values=()
        
        while IFS= read -r line; do
            if [[ "$line" == *"%util"* || -z "$line" ]]; then
                continue
            fi
            
            local device=$(echo "$line" | awk '{print $1}')
            
            # 检查是否在要显示的设备列表中
            if [[ ! "${devices[*]}" == *"$device"* ]]; then
                continue
            fi
            
            local rkB=$(echo "$line" | awk '{print $4}')     # rkB/s
            local wkB=$(echo "$line" | awk '{print $5}')     # wkB/s
            local util=$(echo "$line" | awk '{print $NF}')   # %util
            
            # 保存当前值用于图表
            current_util_values+=($util)
            current_rkB_values+=($rkB)
            current_wkB_values+=($wkB)
            
            # 确定状态颜色
            local status_color=$GREEN
            local status_text="正常"
            
            if (( $(echo "$util > $DISK_UTIL_THRESHOLD" | bc -l) )); then
                status_color=$RED
                status_text="警告"
            elif (( $(echo "$util > 0.7 * $DISK_UTIL_THRESHOLD" | bc -l) )); then
                status_color=$YELLOW
                status_text="注意"
            fi
            
            # 打印设备信息
            printf "%-10s %-12.2f %-12.2f %-12.2f ${status_color}%-8s${NC}\n" "$device" "$rkB" "$wkB" "$util" "$status_text"
        done <<< "$io_stats"
        
        echo -e "${WHITE}--------------------------------------------------------------------------------${NC}\n"
        
        # 更新历史数据
        history_data=(${history_data[@]:1}) # 移除最旧的数据
        history_data+=($(IFS=' '; echo "${current_util_values[*]}")) # 添加新数据
        
        # 准备图表数据
        local chart_labels=(${devices[@]})
        local chart_values=(${current_util_values[@]})
        local max_value=100 # 利用率的最大值是100%
        
        # 绘制设备利用率垂直图表
        draw_vertical_chart "${chart_values[*]}" "${chart_labels[*]}" $max_value "设备利用率 (%)" "%"
        
        # 显示图例和说明
        echo -e "${WHITE}图例:${NC}"
        echo -e "  ${GREEN}█${NC}: 利用率 < 70%"
        echo -e "  ${YELLOW}█${NC}: 70% ≤ 利用率 < $DISK_UTIL_THRESHOLD%"
        echo -e "  ${RED}█${NC}: 利用率 ≥ $DISK_UTIL_THRESHOLD%"
        echo ""
        echo -e "${CYAN}按 Ctrl+C 退出仪表盘${NC}"
        
        # 等待下一次刷新
        sleep $REFRESH_INTERVAL
    done
}

# 主函数
main() {
    # 解析命令行参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -i|--interval)
                if [[ $2 =~ ^[0-9]+$ && $2 -gt 0 ]]; then
                    REFRESH_INTERVAL=$2
                else
                    echo -e "${RED}错误: 刷新间隔必须是正整数${NC}"
                    show_help
                    exit 1
                fi
                shift 2
                ;;
            -H|--height)
                if [[ $2 =~ ^[0-9]+$ && $2 -gt 0 ]]; then
                    CHART_HEIGHT=$2
                else
                    echo -e "${RED}错误: 图表高度必须是正整数${NC}"
                    show_help
                    exit 1
                fi
                shift 2
                ;;
            -d|--devices)
                DISPLAY_DEVICES=$2
                shift 2
                ;;
            -c|--cpu)
                SHOW_CPU_IO=true
                shift 1
                ;;
            -t|--threshold)
                if [[ $2 =~ ^[0-9]+$ && $2 -gt 0 && $2 -le 100 ]]; then
                    DISK_UTIL_THRESHOLD=$2
                else
                    echo -e "${RED}错误: 阈值必须是1-100之间的整数${NC}"
                    show_help
                    exit 1
                fi
                shift 2
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
    
    # 监控I/O性能并显示仪表盘
    monitor_io_performance
}

# 执行主函数
main "$@"
```

## 6 常见问题与解决方案

### 6.1 iostat命令不可用或未找到

**问题描述**：在运行iostat命令时，系统提示"iostat: command not found"。

**解决方案**：

1. 在Debian/Ubuntu系统上安装sysstat包：
```bash
sudo apt-get update && sudo apt-get install sysstat
```

2. 在CentOS/RHEL系统上安装sysstat包：
```bash
sudo yum install sysstat
```

3. 在Fedora系统上安装sysstat包：
```bash
sudo dnf install sysstat
```

4. 安装完成后，可能需要启动sysstat服务：
```bash
sudo systemctl enable sysstat
sudo systemctl start sysstat
```

### 6.2 iostat显示的CPU使用率与实际情况不符

**问题描述**：iostat显示的CPU使用率与其他工具（如top、htop）显示的不一致。

**解决方案**：

1. 了解不同工具计算CPU使用率的方法不同：
   - iostat显示的是自上一次报告以来的平均使用率
   - top默认显示的是实时使用率

2. 使用iostat的实时监控模式来获取更准确的近期使用率：
```bash
iostat 1 5  # 每1秒显示一次，共显示5次
```

3. 注意iostat中的%idle包括了空闲CPU时间和iowait时间，而有些工具将这两部分分开计算。

### 6.3 iostat无法识别某些设备

**问题描述**：iostat命令无法显示系统中某些存储设备的I/O统计信息。

**解决方案**：

1. 确认设备是否被系统正确识别：
```bash
sudo fdisk -l
lsblk
```

2. 尝试使用扩展选项来显示更多设备：
```bash
iostat -x
```

3. 对于LVM逻辑卷，可以使用-N选项来显示卷名：
```bash
iostat -N
```

4. 对于网络存储设备，可能需要额外的工具或驱动程序才能监控其I/O性能。

### 6.4 iostat输出中的某些值为0

**问题描述**：iostat输出中的某些I/O统计值始终为0。

**解决方案**：

1. 确认设备是否有I/O活动：如果设备没有任何读写操作，某些值自然为0。

2. 尝试使用更长的监控间隔，以捕捉到I/O活动：
```bash
iostat 5
```

3. 检查是否使用了正确的设备名称：确保指定的设备名称存在于系统中。

4. 对于新安装的设备，可能需要重启系统或重新加载相关模块才能被iostat正确识别。

### 6.5 如何理解iostat中的%util值

**问题描述**：不理解iostat输出中的%util字段表示什么，以及如何根据这个值判断设备性能。

**解决方案**：

1. %util表示设备的利用率百分比，理论上如果达到100%，表示设备已经饱和。

2. 注意：现代存储设备（如SSD）可能支持并行I/O操作，即使%util接近100%，仍可能有处理能力。

3. 判断设备是否饱和时，还应结合await（平均等待时间）和avgqu-sz（平均队列长度）等指标：
   - 如果%util高，且await和avgqu-sz也高，通常表示设备已饱和
   - 如果%util高，但await和avgqu-sz较低，可能是设备支持并行操作

4. 一般建议：
   - %util < 50%：设备性能良好
   - 50% ≤ %util < 80%：设备负载中等
   - %util ≥ 80%：设备负载较重，可能成为性能瓶颈

### 6.6 iostat监控的I/O性能数据不准确

**问题描述**：iostat显示的I/O性能数据与实际应用程序的性能表现不一致。

**解决方案**：

1. 使用多次采样的平均值来减少波动：
```bash
iostat 1 10 | tail -n +4 | awk '{sum += $NF} END {print "平均利用率: " sum/NR "%"}'
```

2. 同时使用多个工具进行监控，如iotop、sar等，综合分析系统I/O性能。

3. 注意文件系统缓存可能会影响iostat的测量结果，某些写入操作可能先被缓存，然后才真正写入磁盘。

4. 对于虚拟化环境，注意宿主机和虚拟机之间的资源争用可能会影响iostat的测量准确性。

### 6.7 如何监控特定进程的I/O活动

**问题描述**：iostat只能监控设备级别的I/O统计，无法直接显示特定进程的I/O活动。

**解决方案**：

1. 使用iotop工具来监控进程级别的I/O活动：
```bash
sudo iotop
```

2. 使用pidstat命令监控特定进程的I/O统计：
```bash
sudo pidstat -d 1
```

3. 结合使用iostat和其他工具来分析系统I/O性能：
   - 使用iostat监控设备级别的性能
   - 使用iotop或pidstat监控进程级别的活动
   - 使用top或htop监控整体系统性能

4. 对于长期监控，可以使用sar命令收集和分析历史I/O数据：
```bash
sar -d 1 10 > iostat.log
```

### 6.8 如何导出iostat数据用于进一步分析

**问题描述**：需要将iostat的输出数据保存为文件，以便进行进一步分析或生成图表。

**解决方案**：

1. 将iostat的输出重定向到文件：
```bash
iostat -dx 1 100 > iostat_data.txt
```

2. 使用csv格式输出（通过5.2节的disk_io_analyzer.sh工具）：
```bash
bash disk_io_analyzer.sh -o csv -f iostat_data.csv
```

3. 使用JSON格式输出以便程序处理：
```bash
bash disk_io_analyzer.sh -o json -f iostat_data.json
```

4. 对于实时数据，可以使用脚本定期收集并保存到数据库中，例如：
```bash
while true; do
echo "$(date '+%Y-%m-%d %H:%M:%S'),$(iostat -d sda | tail -n 1 | awk '{print $2,$3,$4,$5}')" >> iostat_history.csv
sleep 60
done
```

## 7 总结与注意事项

### 7.1 功能总结

iostat命令是一个功能强大的系统I/O性能监控工具，它能够提供：

- 全面的CPU使用率统计信息，包括用户空间、系统内核和I/O等待时间
- 详细的设备I/O统计信息，包括读写速度、传输次数和设备利用率
- 扩展的I/O性能指标，如平均请求大小、队列长度和等待时间
- 支持实时监控和历史数据分析
- 灵活的输出格式和选项，适应不同的监控需求

通过iostat命令，系统管理员可以全面了解系统的I/O性能状况，识别潜在的性能瓶颈，并采取相应的优化措施。

### 7.2 使用注意事项

在使用iostat命令监控系统I/O性能时，需要注意以下几点：

1. **正确理解输出指标**：iostat输出中的各个指标（如%util、await、avgqu-sz等）都有其特定含义，需要正确理解这些指标才能准确评估系统性能。

2. **结合多个指标分析**：不应仅依靠单个指标来判断系统性能，应结合多个指标进行综合分析。例如，高%util值不一定表示设备已饱和，还需要看await和avgqu-sz等指标。

3. **考虑系统缓存的影响**：文件系统缓存可能会影响iostat的测量结果，某些写入操作可能先被缓存，然后才真正写入磁盘。

4. **区分物理设备和逻辑设备**：在使用LVM或软件RAID的系统中，需要注意区分物理设备和逻辑设备的I/O统计信息。

5. **注意采样频率**：采样频率过高可能会增加系统开销，过低可能会错过重要的性能变化。一般建议根据监控需求选择合适的采样频率。

6. **长期监控与趋势分析**：对于系统性能优化，长期监控和趋势分析比短期快照更有价值，可以使用sar等工具结合iostat进行长期监控。

### 7.3 最佳实践

为了更有效地使用iostat命令监控系统I/O性能，建议遵循以下最佳实践：

1. **定期监控**：建立定期监控机制，及时发现系统I/O性能问题。

2. **基准测试**：在系统正常运行时建立性能基准，以便在出现问题时进行对比分析。

3. **阈值设置**：根据系统特点和应用需求，设置合理的性能阈值，当超过阈值时及时告警。

4. **综合分析**：结合其他监控工具（如top、iotop、sar等）进行综合分析，全面了解系统性能状况。

5. **自动化监控**：利用脚本（如本文提供的io_monitor.sh、disk_io_analyzer.sh和io_dashboard.sh）实现自动化监控和告警。

6. **性能优化**：根据监控结果，采取相应的性能优化措施，如调整I/O调度器、优化文件系统参数、增加缓存或升级存储设备等。

通过正确使用iostat命令和相关工具，系统管理员可以有效地监控和优化系统I/O性能，提高系统的稳定性和响应速度。