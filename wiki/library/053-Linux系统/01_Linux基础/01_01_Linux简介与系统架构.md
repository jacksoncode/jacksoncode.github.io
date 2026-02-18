# Linux简介与系统架构

## 1. Linux简介

Linux是一种自由和开源的类Unix操作系统，由芬兰计算机科学家林纳斯·托瓦兹（Linus Torvalds）于1991年首次发布。Linux以其稳定性、安全性和灵活性而闻名，被广泛应用于服务器、嵌入式系统、移动设备和个人电脑等领域。

### Linux的特点
- **开源免费**：任何人都可以查看、修改和分发Linux源代码
- **多用户多任务**：支持多个用户同时使用系统，并且可以同时运行多个程序
- **稳定性高**：可以长时间运行而不需要重启
- **安全性强**：内置了强大的安全机制，如用户权限管理、防火墙等
- **高度可定制**：用户可以根据自己的需求定制系统
- **广泛的硬件支持**：支持各种硬件平台
- **强大的网络功能**：内置了丰富的网络协议和工具

### Linux的应用领域
- **服务器领域**：Web服务器、数据库服务器、邮件服务器等
- **嵌入式系统**：智能手机（如Android）、路由器、智能电视等
- **科学计算**：高性能计算集群、数据分析等
- **桌面应用**：个人电脑桌面环境（如Ubuntu、Fedora等）
- **云计算**：云服务提供商（如AWS、阿里云等）的基础设施
- **容器技术**：Docker、Kubernetes等容器平台的基础

## 2. Linux系统架构

Linux系统采用分层架构，主要包括内核层、系统调用层、Shell层和应用层。

### 2.1 内核层（Kernel）
内核是Linux系统的核心，负责管理系统的硬件资源、提供基本的系统服务。它是连接硬件和软件的桥梁，主要功能包括：
- **进程管理**：负责进程的创建、调度和终止
- **内存管理**：管理系统的物理内存和虚拟内存
- **文件系统**：提供文件的存储、访问和管理功能
- **设备驱动程序**：管理和控制各种硬件设备
- **网络协议栈**：实现各种网络协议

### 2.2 系统调用层（System Call Interface）
系统调用是应用程序与内核交互的接口，提供了一组标准的函数，让应用程序能够访问内核提供的服务。常见的系统调用包括文件操作、进程控制、内存管理、网络通信等。

### 2.3 Shell层
Shell是用户与Linux系统交互的接口，它接收用户输入的命令，然后调用相应的程序来执行。Linux支持多种Shell，如Bash（Bourne Again Shell）、Tcsh、Zsh等，其中Bash是最常用的。

### 2.4 应用层
应用层是用户直接使用的各种应用程序，如文本编辑器、浏览器、办公软件、开发工具等。

## 3. Linux文件系统结构

Linux采用树形文件系统结构，所有文件和目录都从根目录（/）开始。以下是Linux系统中常见的目录及其功能：

| 目录 | 功能 | 示例 |
|------|------|------|
| / | 根目录，文件系统的起点 | `ls /` 查看根目录下的内容 |
| /bin | 存放基本的用户命令，所有用户都可以使用 | `ls /bin` 查看常用命令 |
| /sbin | 存放系统管理命令，通常需要root权限 | `ls /sbin` 查看系统命令 |
| /etc | 存放系统配置文件 | `ls /etc/passwd` 查看用户配置 |
| /home | 普通用户的主目录 | `cd /home/username` 进入用户主目录 |
| /root | root用户的主目录 | `cd /root` 进入管理员主目录 |
| /var | 存放可变数据，如日志文件、缓存等 | `ls /var/log` 查看系统日志 |
| /tmp | 临时文件目录，系统重启后会清空 | `ls /tmp` 查看临时文件 |
| /usr | 存放用户程序和数据 | `ls /usr/bin` 查看用户命令 |
| /lib | 存放系统库文件 | `ls /lib` 查看系统库 |
| /dev | 存放设备文件 | `ls /dev/sda` 查看硬盘设备 |
| /proc | 虚拟文件系统，反映系统状态 | `cat /proc/cpuinfo` 查看CPU信息 |
| /sys | 虚拟文件系统，用于访问系统硬件信息 | `ls /sys/class/net` 查看网络设备 |

## 4. Linux内核版本

Linux内核版本通常由三部分组成：主版本号、次版本号和修订号。例如，在版本号4.15.0中，4是主版本号，15是次版本号，0是修订号。

### 查看Linux内核版本的命令

```bash
# 查看完整的内核版本信息
uname -a

# 示例输出
# Linux ubuntu 4.15.0-142-generic #146-Ubuntu SMP Tue Apr 13 01:11:19 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux

# 仅查看内核版本号
uname -r

# 示例输出
# 4.15.0-142-generic

# 查看操作系统版本信息
cat /etc/os-release

# 示例输出（Ubuntu系统）
# NAME="Ubuntu"
# VERSION="18.04.5 LTS (Bionic Beaver)"
# ID=ubuntu
# ID_LIKE=debian
# PRETTY_NAME="Ubuntu 18.04.5 LTS"
# VERSION_ID="18.04"
# HOME_URL="https://www.ubuntu.com/"
# SUPPORT_URL="https://help.ubuntu.com/"
# BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
# PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
# VERSION_CODENAME=bionic
# UBUNTU_CODENAME=bionic

# 查看Linux发行版信息
lsb_release -a

# 示例输出
# No LSB modules are available.
# Distributor ID: Ubuntu
# Description:    Ubuntu 18.04.5 LTS
# Release:        18.04
# Codename:       bionic
```

## 5. Linux系统安装（简要步骤）

以下是Linux系统安装的简要步骤，以Ubuntu为例：

1. **下载ISO镜像文件**：从官方网站下载Ubuntu的ISO镜像文件
2. **制作安装介质**：使用工具（如Rufus）将ISO镜像写入U盘或光盘
3. **设置启动顺序**：重启计算机，进入BIOS设置，将安装介质设为第一启动项
4. **开始安装**：选择"Install Ubuntu"，按照向导提示进行安装
5. **选择语言和地区**：根据个人需求选择语言和地区
6. **分区设置**：可以选择自动分区或手动分区
7. **创建用户**：设置用户名和密码
8. **完成安装**：等待安装完成，重启计算机

## 6. Linux命令行基础

Linux命令行是与Linux系统交互的主要方式，掌握基本的命令行操作对于使用Linux至关重要。

### 命令行提示符

当你登录到Linux系统后，会看到类似下面的命令行提示符：

```bash
username@hostname:~$ 
```

其中：
- `username` 是当前登录的用户名
- `hostname` 是主机名
- `~` 表示当前所在的目录（用户主目录）
- `$` 是普通用户的命令行提示符（root用户的提示符是`#`）

### 常用的命令行快捷键

| 快捷键 | 功能 |
|--------|------|
| Tab | 自动补全命令或文件名 |
| Ctrl+C | 中断当前正在执行的命令 |
| Ctrl+D | 退出当前Shell会话 |
| Ctrl+L | 清屏 |
| Ctrl+A | 光标移到命令行开头 |
| Ctrl+E | 光标移到命令行结尾 |
| Ctrl+U | 删除光标前的内容 |
| Ctrl+K | 删除光标后的内容 |
| Ctrl+Z | 暂停当前进程 |
| 上/下箭头 | 查看历史命令 |

## 7. 实践练习

### 练习1：查看系统信息

```bash
# 查看内核版本
uname -a

# 查看操作系统版本
cat /etc/os-release

# 查看CPU信息
cat /proc/cpuinfo | head -n 20

# 查看内存信息
free -h

# 查看硬盘使用情况
df -h
```

### 练习2：浏览文件系统

```bash
# 查看当前目录
pwd

# 列出当前目录下的文件和目录
ls

# 列出当前目录下的所有文件（包括隐藏文件）
ls -a

# 以长格式列出文件和目录
ls -l

# 切换到根目录
cd /

# 查看根目录下的内容
ls -l

# 切换到用户主目录
cd ~

# 创建一个测试目录
mkdir test_dir

# 切换到测试目录
cd test_dir

# 创建一个测试文件
touch test_file.txt

# 查看当前目录下的内容
ls -l

# 返回上一级目录
cd ..

# 删除测试目录及其内容
rm -rf test_dir
```

通过以上内容，我们对Linux的基本概念、系统架构、文件系统结构和命令行基础有了初步的了解。在后续的章节中，我们将详细介绍Linux的各种常用命令及其使用方法。