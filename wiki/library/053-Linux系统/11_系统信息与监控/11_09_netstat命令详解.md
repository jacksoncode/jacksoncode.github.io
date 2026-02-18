# 11.9 netstat命令详解

## 1. 命令概述

netstat（Network Statistics）命令是Linux/Unix系统中用于显示网络状态信息的命令。它可以显示网络连接、路由表、接口统计、伪装连接和多播成员等网络相关信息。netstat命令是网络管理员进行网络监控、故障排查和安全分析的重要工具。

### 1.1 功能特点
- 显示所有活动的网络连接（TCP、UDP、RAW等）
- 显示监听中的端口和套接字信息
- 显示路由表信息
- 显示网络接口的统计数据
- 显示网络协议的统计信息
- 支持过滤和排序显示特定类型的连接
- 可以显示连接的进程ID（PID）和程序名称

### 1.2 应用场景
- 监控系统的网络连接状态
- 查看哪些端口正在被监听
- 检查网络连接的状态和属性
- 排查网络连接问题和故障
- 分析网络流量和性能
- 识别潜在的网络安全问题
- 查看路由表和网络接口信息
- 在系统维护和故障排查中使用

## 2. 语法格式

netstat命令的基本语法格式如下：

```bash
# 显示网络状态信息
$ netstat [选项]

# 组合使用多个选项
$ netstat -tuln
$ netstat -anp
```

### 2.1 语法说明
- **netstat**：命令名称
- **选项**：可选参数，用于控制显示内容、格式和筛选条件
- netstat命令提供了多种选项，可以根据需要组合使用
- 默认情况下，netstat命令会显示所有活动的套接字连接

## 3. 常用选项

netstat命令提供了丰富的选项，用于定制其显示内容和格式。以下是netstat命令的常用选项：

### 3.1 选项列表

| 选项 | 功能说明 |
|------|----------|
| `-a`, `--all` | 显示所有套接字连接，包括监听和非监听状态 |
| `-t`, `--tcp` | 仅显示TCP连接 |
| `-u`, `--udp` | 仅显示UDP连接 |
| `-l`, `--listening` | 仅显示监听状态的套接字 |
| `-n`, `--numeric` | 以数字形式显示地址和端口号，不进行DNS解析 |
| `-p`, `--program` | 显示每个套接字所属的进程ID和程序名称 |
| `-r`, `--route` | 显示路由表信息 |
| `-i`, `--interfaces` | 显示网络接口的统计信息 |
| `-s`, `--statistics` | 显示网络协议的统计信息 |
| `-c`, `--continuous` | 持续显示网络状态信息，每秒更新一次 |
| `-e`, `--extend` | 显示额外的信息（如用户ID） |
| `-o`, `--timers` | 显示计时器信息（如保持活动计时器） |
| `--ip`, `--inet` | 显示IPv4协议的连接（默认） |
| `--inet6` | 显示IPv6协议的连接 |

### 3.2 常用选项组合

| 组合 | 功能说明 |
|------|----------|
| `netstat -tuln` | 显示所有TCP和UDP的监听端口（以数字形式） |
| `netstat -anp` | 显示所有连接和监听端口，包括进程信息 |
| `netstat -rn` | 显示路由表信息（以数字形式） |
| `netstat -i` | 显示网络接口的统计信息 |
| `netstat -s` | 显示网络协议的统计信息 |
| `netstat -atunp` | 显示所有TCP和UDP连接，包括进程信息（以数字形式） |
| `netstat -lntp` | 显示所有TCP监听端口，包括进程信息（以数字形式） |

## 4. 常用示例

### 4.1 显示所有监听端口

使用-tuln选项显示所有TCP和UDP的监听端口：

```bash
# 显示所有TCP和UDP的监听端口
$ netstat -tuln
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN      
tcp6       0      0 :::80                   :::*                    LISTEN      
tcp6       0      0 :::22                   :::*                    LISTEN      
tcp6       0      0 ::1:25                  :::*                    LISTEN      
udp        0      0 0.0.0.0:5353            0.0.0.0:*                           
udp        0      0 0.0.0.0:68              0.0.0.0:*                           
udp6       0      0 :::5353                 :::*                                

# 输出解释：
# Proto: 协议类型（TCP或UDP）
# Recv-Q: 接收队列中的字节数
# Send-Q: 发送队列中的字节数
# Local Address: 本地地址和端口号
# Foreign Address: 远程地址和端口号
# State: 连接状态（对于TCP连接）
```

### 4.2 显示所有连接和进程信息

使用-anp选项显示所有连接和监听端口，包括进程信息：

```bash
# 显示所有连接和进程信息
$ netstat -anp
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name     
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      1234/sshd            
tcp        0      0 192.168.1.100:22        192.168.1.200:54321     ESTABLISHED 5678/sshd: user [pr 
tcp6       0      0 :::80                   :::*                    LISTEN      9012/apache2         
tcp6       0      0 :::22                   :::*                    LISTEN      1234/sshd            
udp        0      0 0.0.0.0:5353            0.0.0.0:*                           3456/avahi-daemon: r
udp        0      0 0.0.0.0:68              0.0.0.0:*                           6789/dhclient        

# 输出中增加了PID/Program name列，显示每个连接所属的进程ID和程序名称
# 注意：可能需要root权限才能查看所有进程信息
```

### 4.3 显示路由表信息

使用-rn选项显示路由表信息：

```bash
# 显示路由表信息
$ netstat -rn
Kernel IP routing table
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
0.0.0.0         192.168.1.1     0.0.0.0         UG        0 0          0 eth0
192.168.1.0     0.0.0.0         255.255.255.0   U         0 0          0 eth0
172.17.0.0      0.0.0.0         255.255.0.0     U         0 0          0 docker0

# 输出解释：
# Destination: 目标网络或主机
# Gateway: 网关地址
# Genmask: 网络掩码
# Flags: 路由标志（U=活动，G=网关，H=主机等）
# MSS: 最大段大小
# Window: 窗口大小
# irtt: 初始往返时间
# Iface: 网络接口

# 也可以使用route命令显示路由表
$ route -n
```

### 4.4 显示网络接口的统计信息

使用-i选项显示网络接口的统计信息：

```bash
# 显示网络接口的统计信息
$ netstat -i
Kernel Interface table
Iface      MTU    RX-OK RX-ERR RX-DRP RX-OVR    TX-OK TX-ERR TX-DRP TX-OVR Flg
eth0      1500   12345     0     0       0     6789     0     0       0 BMRU
lo       65536    4567     0     0       0     4567     0     0       0 LRU
docker0   1500      0     0     0       0       0     0     0       0 BMU

# 输出解释：
# Iface: 网络接口名称
# MTU: 最大传输单元
# RX-OK: 成功接收的数据包数
# RX-ERR: 接收错误的数据包数
# RX-DRP: 丢弃的接收数据包数
# RX-OVR: 接收溢出的数据包数
# TX-OK: 成功发送的数据包数
# TX-ERR: 发送错误的数据包数
# TX-DRP: 丢弃的发送数据包数
# TX-OVR: 发送溢出的数据包数
# Flg: 接口标志（B=广播，M=多播，R=运行，U=启用等）

# 使用-e选项显示更详细的接口信息
$ netstat -ie
```

### 4.5 显示网络协议的统计信息

使用-s选项显示网络协议的统计信息：

```bash
# 显示网络协议的统计信息
$ netstat -s
Ip:
    12345 total packets received
    0 forwarded
    0 incoming packets discarded
    12345 incoming packets delivered
    6789 requests sent out
Icmp:
    0 ICMP messages received
    0 input ICMP message failed.
    ...
Tcp:
    567 active connections openings
    0 passive connection openings
    0 failed connection attempts
    0 connection resets received
    0 connections established
    4567 segments received
    3456 segments send out
    0 segments retransmited
    ...
Udp:
    789 packets received
    0 packets to unknown port received.
    0 packet receive errors
    654 packets sent
    ...

# 输出显示了IP、ICMP、TCP、UDP等协议的详细统计信息
# 这些信息对于分析网络性能和排查网络问题非常有用
```

### 4.6 显示特定协议的连接

显示特定协议（如TCP或UDP）的连接：

```bash
# 显示所有TCP连接
$ netstat -atn
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      
tcp        0      0 192.168.1.100:22        192.168.1.200:54321     ESTABLISHED 
tcp6       0      0 :::80                   :::*                    LISTEN      
tcp6       0      0 :::22                   :::*                    LISTEN      

# 显示所有UDP连接
$ netstat -aun
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       
udp        0      0 0.0.0.0:5353            0.0.0.0:*                           
udp        0      0 0.0.0.0:68              0.0.0.0:*                           
udp6       0      0 :::5353                 :::*                                
```

### 4.7 显示监听状态的TCP端口和进程信息

显示监听状态的TCP端口和进程信息：

```bash
# 显示监听状态的TCP端口和进程信息
$ netstat -lntp
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name     
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      1234/sshd            
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN      5678/master          
tcp6       0      0 :::80                   :::*                    LISTEN      9012/apache2         
tcp6       0      0 :::22                   :::*                    LISTEN      1234/sshd            
tcp6       0      0 ::1:25                  :::*                    LISTEN      5678/master          

# 这个命令对于查看哪些服务正在运行以及它们使用的端口非常有用
# 注意：可能需要root权限才能查看所有进程信息
```

### 4.8 持续显示网络状态信息

使用-c选项持续显示网络状态信息，每秒更新一次：

```bash
# 持续显示网络状态信息
$ netstat -tc
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       
tcp        0      0 192.168.1.100:22        192.168.1.200:54321     ESTABLISHED 
tcp        0      0 192.168.1.100:80        10.0.0.1:12345          ESTABLISHED 

# 按Ctrl+C停止显示
# 这个命令对于实时监控网络连接变化非常有用
```

### 4.9 显示特定端口的连接

使用grep命令过滤显示特定端口的连接：

```bash
# 显示使用80端口的连接
$ netstat -anp | grep :80
tcp6       0      0 :::80                   :::*                    LISTEN      9012/apache2         
tcp6       0      0 192.168.1.100:80        10.0.0.1:12345          ESTABLISHED 9012/apache2         
tcp6       0      0 192.168.1.100:80        203.0.113.45:54321      ESTABLISHED 9012/apache2         

# 显示使用22端口的连接
$ netstat -anp | grep :22
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      1234/sshd            
tcp        0      0 192.168.1.100:22        192.168.1.200:54321     ESTABLISHED 5678/sshd: user [pr 
tcp6       0      0 :::22                   :::*                    LISTEN      1234/sshd            

# 显示处于ESTABLISHED状态的连接
$ netstat -anp | grep ESTABLISHED
tcp        0      0 192.168.1.100:22        192.168.1.200:54321     ESTABLISHED 5678/sshd: user [pr 
tcp6       0      0 192.168.1.100:80        10.0.0.1:12345          ESTABLISHED 9012/apache2         
```

### 4.10 在脚本中使用netstat命令

在Shell脚本中获取和处理网络连接信息：

```bash
#!/bin/bash

# 网络连接监控脚本

# 检查特定端口是否开放
check_port() {
    local port=$1
    local protocol=$2
    
    if [ -z "$protocol" ]; then
        protocol="tcp"
    fi
    
    echo "检查$protocol协议的$port端口是否开放..."
    local result=$(netstat -an | grep "$protocol" | grep ":$port " | grep LISTEN)
    
    if [ -n "$result" ]; then
        echo "端口 $port ($protocol) 已开放"
        echo "详细信息: $result"
        return 0
    else
        echo "端口 $port ($protocol) 未开放"
        return 1
    fi
}

# 显示所有开放的端口
show_open_ports() {
    echo "=== 所有开放的TCP端口 ==="
    netstat -tuln | grep tcp | awk '{print $4}' | awk -F: '{print $NF}' | sort -n | uniq
    
    echo "\n=== 所有开放的UDP端口 ==="
    netstat -tuln | grep udp | awk '{print $4}' | awk -F: '{print $NF}' | sort -n | uniq
}

# 显示外部连接统计
show_external_connections() {
    echo "=== 外部连接统计 ==="
    
    # 统计来自不同IP的连接数
    echo "\n按IP地址统计的连接数:"
    netstat -ant | grep ESTABLISHED | awk '{print $5}' | awk -F: '{print $1}' | sort | uniq -c | sort -rn | head -10
    
    # 统计连接到不同端口的连接数
    echo "\n按本地端口统计的连接数:"
    netstat -ant | grep ESTABLISHED | awk '{print $4}' | awk -F: '{print $NF}' | sort | uniq -c | sort -rn | head -10
}

# 检查异常连接
check_abnormal_connections() {
    echo "=== 异常连接检查 ==="
    
    # 检查TIME_WAIT状态过多的连接
    local time_wait_count=$(netstat -ant | grep TIME_WAIT | wc -l)
    echo "TIME_WAIT状态的连接数: $time_wait_count"
    
    if [ $time_wait_count -gt 1000 ]; then
        echo "警告: TIME_WAIT状态的连接数过多，可能存在连接泄漏"
    fi
    
    # 检查CLOSE_WAIT状态的连接
    local close_wait_count=$(netstat -ant | grep CLOSE_WAIT | wc -l)
    echo "CLOSE_WAIT状态的连接数: $close_wait_count"
    
    if [ $close_wait_count -gt 100 ]; then
        echo "警告: CLOSE_WAIT状态的连接数过多，可能存在应用程序没有正确关闭连接"
    fi
    
    # 检查SYN_RECV状态的连接（可能是SYN洪水攻击）
    local syn_recv_count=$(netstat -ant | grep SYN_RECV | wc -l)
    echo "SYN_RECV状态的连接数: $syn_recv_count"
    
    if [ $syn_recv_count -gt 50 ]; then
        echo "警告: SYN_RECV状态的连接数过多，可能正在遭受SYN洪水攻击"
    fi
}

# 主函数
main() {
    echo "网络连接监控报告"
    echo "生成时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    
    # 检查常用端口是否开放
    echo "=== 检查常用服务端口 ==="
    check_port 22
    check_port 80
    check_port 443
    check_port 53 udp
    echo ""
    
    # 显示所有开放的端口
    show_open_ports
    echo ""
    
    # 显示外部连接统计
    show_external_connections
    echo ""
    
    # 检查异常连接
    check_abnormal_connections
    echo ""
    
    # 显示网络接口统计
    echo "=== 网络接口统计 ==="
    netstat -i | head -n 1 && netstat -i | grep -v lo
}

# 调用主函数
main
```

## 5. 高级用法

### 5.1 网络连接监控与告警

创建脚本监控网络连接并在发现异常时发送告警：

```bash
#!/bin/bash

# 网络连接监控与告警脚本

# 配置参数
LOG_FILE="/var/log/network_monitor.log"
ALERT_EMAIL="admin@example.com"
CHECK_INTERVAL=60  # 检查间隔（秒）
MAX_CONNECTIONS=200  # 最大连接数阈值
MAX_SYN_RECV=50  # 最大SYN_RECV状态连接数阈值
MAX_TIME_WAIT=1000  # 最大TIME_WAIT状态连接数阈值
MAX_CLOSE_WAIT=100  # 最大CLOSE_WAIT状态连接数阈值
MONITORED_PORTS=(22 80 443)  # 监控的端口列表

# 确保日志文件存在
touch $LOG_FILE
chmod 644 $LOG_FILE

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> $LOG_FILE
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"  # 同时输出到控制台
}

# 发送告警邮件
send_alert() {
    local subject="$1"
    local message="$2"
    
    log "发送告警邮件: $subject"
    log "告警内容: $message"
    
    # 发送邮件（需要配置邮件服务）
    # echo "$message" | mail -s "[网络告警] $subject" $ALERT_EMAIL
}

# 监控总连接数
monitor_total_connections() {
    local total_connections=$(netstat -an | grep -c ESTABLISHED)
    
    if [ $total_connections -gt $MAX_CONNECTIONS ]; then
        local message="总连接数 ($total_connections) 超过阈值 ($MAX_CONNECTIONS)\n\n当前连接最多的IP:$(netstat -ant | grep ESTABLISHED | awk '{print $5}' | awk -F: '{print $1}' | sort | uniq -c | sort -rn | head -5)"
        send_alert "连接数过多告警" "$message"
    fi
    
    log "总ESTABLISHED连接数: $total_connections"
}

# 监控异常连接状态
monitor_abnormal_connections() {
    # 监控SYN_RECV状态连接（可能是SYN洪水攻击）
    local syn_recv_count=$(netstat -ant | grep -c SYN_RECV)
    if [ $syn_recv_count -gt $MAX_SYN_RECV ]; then
        local message="SYN_RECV状态连接数 ($syn_recv_count) 超过阈值 ($MAX_SYN_RECV)\n\n可能正在遭受SYN洪水攻击""
        send_alert "SYN_RECV连接过多告警" "$message"
    fi
    log "SYN_RECV连接数: $syn_recv_count"
    
    # 监控TIME_WAIT状态连接
    local time_wait_count=$(netstat -ant | grep -c TIME_WAIT)
    if [ $time_wait_count -gt $MAX_TIME_WAIT ]; then
        local message="TIME_WAIT状态连接数 ($time_wait_count) 超过阈值 ($MAX_TIME_WAIT)\n\n可能存在连接泄漏或系统参数需要调整""
        send_alert "TIME_WAIT连接过多告警" "$message"
    fi
    log "TIME_WAIT连接数: $time_wait_count"
    
    # 监控CLOSE_WAIT状态连接
    local close_wait_count=$(netstat -ant | grep -c CLOSE_WAIT)
    if [ $close_wait_count -gt $MAX_CLOSE_WAIT ]; then
        local message="CLOSE_WAIT状态连接数 ($close_wait_count) 超过阈值 ($MAX_CLOSE_WAIT)\n\n可能存在应用程序没有正确关闭连接的问题""
        send_alert "CLOSE_WAIT连接过多告警" "$message"
    fi
    log "CLOSE_WAIT连接数: $close_wait_count"
}

# 监控特定端口的连接数
monitor_port_connections() {
    for port in "${MONITORED_PORTS[@]}"; do
        local port_connections=$(netstat -ant | grep ESTABLISHED | grep ":$port " | wc -l)
        log "端口 $port 的连接数: $port_connections"
        
        # 可以为特定端口设置不同的阈值
        if [ $port_connections -gt 100 ]; then  # 这里使用简单的阈值，实际应根据情况调整
            local message="端口 $port 的连接数 ($port_connections) 超过阈值 (100)\n\n可能存在异常访问或攻击""
            send_alert "端口 $port 连接过多告警" "$message"
        fi
    done
}

# 监控特定IP的连接数
monitor_ip_connections() {
    local top_ips=$(netstat -ant | grep ESTABLISHED | awk '{print $5}' | awk -F: '{print $1}' | sort | uniq -c | sort -rn | head -5)
    
    # 检查是否有单个IP连接数过多
    echo "$top_ips" | while read line; do
        local count=$(echo $line | awk '{print $1}')
        local ip=$(echo $line | awk '{print $2}')
        
        if [ $count -gt 50 ]; then  # 阈值：单个IP最多50个连接
            local message="IP $ip 的连接数 ($count) 超过阈值 (50)\n\n可能存在异常访问或攻击""
            send_alert "IP $ip 连接过多告警" "$message"
        fi
    done
}

# 主监控循环
log "网络连接监控脚本启动"

while true; do
    log "开始网络连接监控检查"
    
    # 执行各项监控
    monitor_total_connections
    monitor_abnormal_connections
    monitor_port_connections
    monitor_ip_connections
    
    log "网络连接监控检查完成"
    log "------------------------------------"
    
    # 等待下一次检查
    sleep $CHECK_INTERVAL
done

# 使用方法: 将脚本保存为network_monitor.sh，然后运行：nohup ./network_monitor.sh &
```

### 5.2 网络流量分析

使用netstat结合其他工具进行网络流量分析：

```bash
#!/bin/bash

# 网络流量分析脚本

# 确保安装了必要的工具
echo "检查必要的工具是否安装..."
for tool in netstat awk sort head tail grep ifconfig; do
    if ! command -v $tool &> /dev/null; then
        echo "错误: 工具 $tool 未安装，请先安装" >&2
        exit 1
    fi
done

# 创建临时目录存储分析结果
temp_dir=$(mktemp -d)
echo "使用临时目录: $temp_dir"

# 收集网络连接数据
echo "收集网络连接数据..."
netstat -anp > $temp_dir/netstat_output.txt

# 分析TCP连接状态
echo "\n=== TCP连接状态分析 ==="
tcp_states=$(grep 'tcp' $temp_dir/netstat_output.txt | awk '{print $6}' | sort | uniq -c | sort -rn)
echo "TCP连接状态分布:"
echo "$tcp_states"

# 计算总TCP连接数
total_tcp=$(grep -c 'tcp' $temp_dir/netstat_output.txt)
echo "总TCP连接数: $total_tcp"

# 分析UDP连接
echo "\n=== UDP连接分析 ==="
total_udp=$(grep -c 'udp' $temp_dir/netstat_output.txt)
echo "总UDP连接数: $total_udp"

# 分析网络接口流量
echo "\n=== 网络接口流量分析 ==="
# 第一次采集接口统计信息
netstat -i > $temp_dir/if_stats_1.txt
sleep 5  # 等待5秒
# 第二次采集接口统计信息
netstat -i > $temp_dir/if_stats_2.txt

# 计算接口流量变化
interfaces=$(grep -v 'Iface' $temp_dir/if_stats_1.txt | awk '{print $1}')

for iface in $interfaces; do
    if [ $iface != "lo" ]; then  # 跳过回环接口
        # 获取第一次采集的接收和发送数据包数
        rx1=$(grep $iface $temp_dir/if_stats_1.txt | awk '{print $3}')
        tx1=$(grep $iface $temp_dir/if_stats_1.txt | awk '{print $7}')
        
        # 获取第二次采集的接收和发送数据包数
        rx2=$(grep $iface $temp_dir/if_stats_2.txt | awk '{print $3}')
        tx2=$(grep $iface $temp_dir/if_stats_2.txt | awk '{print $7}')
        
        # 计算差值
        rx_diff=$((rx2 - rx1))
        tx_diff=$((tx2 - tx1))
        
        # 计算速率（每秒数据包数）
        rx_rate=$((rx_diff / 5))
        tx_rate=$((tx_diff / 5))
        
        echo "接口 $iface:"
        echo "  接收速率: $rx_rate 包/秒"
        echo "  发送速率: $tx_rate 包/秒"
    fi
done

# 分析常用端口使用情况
echo "\n=== 常用端口使用情况 ==="
common_ports=(21 22 23 25 53 80 110 443 3306 8080)

for port in "${common_ports[@]}"; do
    count=$(grep -c ":$port " $temp_dir/netstat_output.txt)
    if [ $count -gt 0 ]; then
        echo "端口 $port: $count 个连接"
        # 显示这些连接的状态
        grep ":$port " $temp_dir/netstat_output.txt | awk '{print "  " $6}' | sort | uniq -c | sort -rn
    fi
done

# 分析外部连接源IP
echo "\n=== 外部连接源IP分析 ==="
external_ips=$(grep 'ESTABLISHED' $temp_dir/netstat_output.txt | awk '{print $5}' | awk -F: '{print $1}' | grep -v '127.0.0.1' | grep -v '192.168' | grep -v '10.' | grep -v '172.1[6-9]' | grep -v '172.2[0-9]' | grep -v '172.3[0-1]')

if [ -n "$external_ips" ]; then
    echo "外部连接源IP分布:"
    echo "$external_ips" | sort | uniq -c | sort -rn | head -10
else
    echo "未发现外部连接"
fi

# 检查异常连接
echo "\n=== 异常连接检查 ==="
# 检查SYN_RECV状态过多的连接
syn_recv_count=$(grep -c 'SYN_RECV' $temp_dir/netstat_output.txt)
echo "SYN_RECV状态连接数: $syn_recv_count"
if [ $syn_recv_count -gt 50 ]; then
    echo "警告: SYN_RECV状态连接数过多，可能正在遭受SYN洪水攻击"
fi

# 检查TIME_WAIT状态过多的连接
time_wait_count=$(grep -c 'TIME_WAIT' $temp_dir/netstat_output.txt)
echo "TIME_WAIT状态连接数: $time_wait_count"
if [ $time_wait_count -gt 1000 ]; then
    echo "警告: TIME_WAIT状态连接数过多，可能存在连接泄漏"
fi

# 检查CLOSE_WAIT状态的连接
close_wait_count=$(grep -c 'CLOSE_WAIT' $temp_dir/netstat_output.txt)
echo "CLOSE_WAIT状态连接数: $close_wait_count"
if [ $close_wait_count -gt 100 ]; then
    echo "警告: CLOSE_WAIT状态连接数过多，可能存在应用程序没有正确关闭连接"
fi

# 清理临时文件
echo "\n清理临时文件..."
rm -rf $temp_dir

echo "\n网络流量分析完成！"
```

### 5.3 服务端口监控与自动恢复

创建脚本监控关键服务端口，并在服务不可用时尝试自动恢复：

```bash
#!/bin/bash

# 服务端口监控与自动恢复脚本

# 配置参数
LOG_FILE="/var/log/service_port_monitor.log"
CHECK_INTERVAL=30  # 检查间隔（秒）
RESTART_MAX=3  # 最大重启次数
RESTART_INTERVAL=300  # 重启计数时间窗口（秒）

# 定义要监控的服务和端口
declare -A services=( 
    ["sshd"]="22" 
    ["apache2"]="80" 
    ["mysql"]="3306" 
    ["nginx"]="8080" 
)

# 定义服务重启命令
declare -A restart_commands=( 
    ["sshd"]="systemctl restart sshd" 
    ["apache2"]="systemctl restart apache2" 
    ["mysql"]="systemctl restart mysql" 
    ["nginx"]="systemctl restart nginx" 
)

# 确保日志文件存在
touch $LOG_FILE
chmod 644 $LOG_FILE

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> $LOG_FILE
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"  # 同时输出到控制台
}

# 检查服务端口是否开放
check_service_port() {
    local service=$1
    local port=$2
    
    # 使用netstat检查端口是否开放
    local result=$(netstat -tuln | grep ":$port " | grep LISTEN)
    
    if [ -n "$result" ]; then
        log "服务 $service (端口 $port) 运行正常"
        return 0
    else
        log "警告: 服务 $service (端口 $port) 未运行或端口未开放"
        return 1
    fi
}

# 重启服务
restart_service() {
    local service=$1
    local command=${restart_commands[$service]}
    
    if [ -z "$command" ]; then
        log "错误: 未找到服务 $service 的重启命令"
        return 1
    fi
    
    log "尝试重启服务 $service: $command"
    $command
    
    if [ $? -eq 0 ]; then
        log "服务 $service 重启成功"
        return 0
    else
        log "错误: 服务 $service 重启失败"
        return 1
    fi
}

# 统计服务重启次数
count_restarts() {
    local service=$1
    local now=$(date +%s)
    local window_start=$((now - RESTART_INTERVAL))
    
    # 从日志文件中统计重启次数
    local restart_count=$(grep "尝试重启服务 $service" $LOG_FILE | tail -n 50 | awk -v start=$window_start '{split($1,a,"["); split(a[2],b,"-"); split(b[3],c,":"); timestamp=mktime(b[1] " " b[2] " " c[1] " " c[2] " " c[3] " " 0); if (timestamp > start) count++} END {print count}')
    
    echo $restart_count
}

# 主监控循环
log "服务端口监控脚本启动"

while true; do
    log "开始服务端口检查"
    
    for service in "${!services[@]}"; do
        local port=${services[$service]}
        
        # 检查服务端口
        if ! check_service_port $service $port; then
            # 检查重启次数是否超过限制
            restart_count=$(count_restarts $service)
            
            if [ $restart_count -lt $RESTART_MAX ]; then
                log "在过去 $RESTART_INTERVAL 秒内已重启 $restart_count 次，尝试再次重启（最大 $RESTART_MAX 次）"
                
                # 尝试重启服务
                if restart_service $service; then
                    # 等待服务启动
                    sleep 10
                    
                    # 再次检查服务端口
                    if check_service_port $service $port; then
                        log "服务 $service 恢复成功"
                    else
                        log "警告: 服务 $service 重启后端口 $port 仍未开放"
                    fi
                fi
            else
                log "错误: 在过去 $RESTART_INTERVAL 秒内已重启 $restart_count 次，超过最大限制 $RESTART_MAX 次，停止自动重启"
            fi
        fi
    done
    
    log "服务端口检查完成"
    log "------------------------------------"
    
    # 等待下一次检查
    sleep $CHECK_INTERVAL
done

# 使用方法: 将脚本保存为service_port_monitor.sh，然后运行：nohup ./service_port_monitor.sh &
```

## 6. 常见问题与解决方案

### 6.1 netstat命令显示的信息不完整

**问题**：使用netstat命令只能看到部分连接信息，无法看到所有进程的连接。

**解决方案**：
1. 使用root权限运行netstat命令，普通用户可能无法查看所有进程的连接信息
2. 使用`netstat -a`选项显示所有连接，包括监听和非监听状态
3. 确保使用了正确的协议选项，如-t（TCP）、-u（UDP）等
4. 在某些系统上，可能需要安装net-tools包才能使用netstat命令
5. 注意某些系统可能默认隐藏了某些类型的连接

### 6.2 netstat命令执行速度慢

**问题**：netstat命令执行速度很慢，特别是使用-p选项时。

**解决方案**：
1. 使用-n选项以数字形式显示地址和端口，避免DNS解析
2. 限制显示的连接类型，如使用-t只显示TCP连接
3. 使用过滤器减少输出量，如使用grep过滤特定端口
4. 对于定期监控，可以考虑使用ss命令（netstat的替代品，速度更快）
5. 检查系统负载和网络状态，系统负载过高也可能导致netstat命令执行缓慢

### 6.3 无法找到特定端口的监听进程

**问题**：netstat命令显示某个端口正在被监听，但无法看到对应的进程信息。

**解决方案**：
1. 使用root权限运行netstat命令
2. 确保使用了-p选项显示进程信息
3. 检查端口是否被系统服务或内核模块占用
4. 尝试使用lsof命令查看端口占用情况：`lsof -i :port_number`
5. 在某些情况下，可能需要重启系统才能释放被占用的端口

### 6.4 netstat命令不显示新的连接状态

**问题**：netstat命令显示的连接状态不更新，或者不显示新建立的连接。

**解决方案**：
1. 使用-c选项持续显示网络状态信息
2. 确保使用了正确的选项组合，如-atn或-anp
3. 检查网络连接是否确实存在，可以使用ping或telnet命令测试
4. 在某些系统上，可能需要刷新网络缓存或重启网络服务
5. 对于短暂的连接，可能需要使用tcpdump等工具进行捕获

### 6.5 netstat命令在较新的Linux发行版中不可用

**问题**：在较新的Linux发行版中，默认没有安装netstat命令。

**解决方案**：
1. 安装net-tools包：`sudo apt-get install net-tools`（Debian/Ubuntu）或`sudo yum install net-tools`（CentOS/RHEL）
2. 使用替代命令ss，它是iproute2包的一部分，功能类似但更高效：`ss -tuln`（相当于netstat -tuln）
3. 使用lsof命令查看打开的文件和网络连接：`lsof -i`
4. 使用ip命令查看网络接口和路由信息：`ip addr`和`ip route`
5. 对于端口扫描，可以使用nmap命令

### 6.6 netstat命令显示大量TIME_WAIT状态的连接

**问题**：netstat命令显示系统中有大量处于TIME_WAIT状态的连接，可能影响系统性能。

**解决方案**：
1. 了解TIME_WAIT状态的作用：确保网络连接正常关闭，防止延迟的数据包被错误处理
2. 调整内核参数，减少TIME_WAIT超时时间：`sudo sysctl -w net.ipv4.tcp_fin_timeout=30`
3. 启用TIME_WAIT连接复用：`sudo sysctl -w net.ipv4.tcp_tw_reuse=1`
4. 启用TIME_WAIT快速回收：`sudo sysctl -w net.ipv4.tcp_tw_recycle=1`（注意：在NAT环境中可能导致问题）
5. 增加系统允许的TIME_WAIT连接数：`sudo sysctl -w net.ipv4.tcp_max_tw_buckets=5000`
6. 从应用层面优化，确保连接正确关闭，避免过多的短连接

## 7. 总结与注意事项

### 7.1 总结

netstat命令是Linux/Unix系统中用于显示网络状态信息的重要工具，提供了关于网络连接、路由表、接口统计和协议统计等方面的详细信息。通过netstat命令，系统管理员可以监控网络连接状态、排查网络故障、分析网络流量和性能，以及识别潜在的网络安全问题。netstat命令支持丰富的选项和过滤功能，可以根据需要定制显示内容和格式。虽然在较新的Linux发行版中，ss命令逐渐取代了netstat，但netstat仍然是一个广泛使用的网络管理工具。

### 7.2 注意事项

- netstat命令显示的是网络状态的快照，而不是实时数据流
- 使用root权限运行netstat命令可以查看所有进程的连接信息
- 使用-n选项可以加快命令执行速度，避免DNS解析
- 在较新的Linux发行版中，可能需要安装net-tools包才能使用netstat命令
- 对于高负载系统，考虑使用ss命令代替netstat，以获得更好的性能
- 定期监控网络连接状态有助于及时发现和解决网络问题
- 注意保护网络连接信息的安全性，特别是在多用户环境中
- 不同版本和发行版的netstat命令可能存在细微差别，使用前应查阅相关文档
- 对于复杂的网络分析需求，可以结合tcpdump、wireshark等工具使用