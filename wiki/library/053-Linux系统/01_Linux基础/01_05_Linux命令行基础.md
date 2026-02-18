# Linux命令行基础

## 1. 命令行概述

命令行界面（Command Line Interface，CLI）是用户与Linux系统交互的主要方式之一。通过命令行，用户可以输入命令并执行各种操作，如文件管理、系统配置、软件安装等。虽然图形用户界面（GUI）更加直观易用，但命令行界面具有更高的效率、更强的功能和更好的远程操作能力，是Linux系统管理和开发的必备技能。

### 命令行的优势

- **高效性**：熟练的用户可以通过命令行快速完成复杂的任务
- **自动化**：可以将命令组合成脚本，实现自动化操作
- **远程管理**：可以通过SSH等工具远程管理Linux服务器
- **资源占用少**：相比于图形界面，命令行占用的系统资源更少
- **功能强大**：许多高级功能和系统配置只能通过命令行完成

## 2. 命令行提示符

当你登录到Linux系统或打开终端时，首先看到的是命令行提示符。命令行提示符通常包含一些有用的信息，如当前用户名、主机名、当前工作目录等。

### 提示符的基本格式

```bash
username@hostname:current_directory$ 
```

例如：

```bash
john@ubuntu:~$ 
```

其中：
- `john`：当前登录的用户名
- `ubuntu`：主机名
- `~`：当前工作目录（波浪号表示用户主目录）
- `$`：普通用户的命令提示符（root用户的提示符是`#`）

### 自定义命令提示符

命令提示符的格式由环境变量`PS1`控制，可以通过修改`PS1`来自定义提示符的显示内容。

```bash
# 查看当前的PS1设置
echo $PS1

# 临时修改命令提示符
export PS1="[\u@\h:\w]\$ "

# 永久修改命令提示符，需要将设置添加到shell配置文件中
# 对于Bash，编辑~/.bashrc文件
vim ~/.bashrc
# 添加类似下面的行
export PS1="[\u@\h:\w]\$ "
# 保存后，重新加载配置文件
source ~/.bashrc
```

常用的PS1转义字符：

| 转义字符 | 描述 |
|---------|------|
| `\u` | 当前用户名 |
| `\h` | 主机名（不包含域名部分） |
| `\H` | 完整主机名 |
| `\w` | 当前工作目录的完整路径 |
| `\W` | 当前工作目录的基名 |
| `\$` | 普通用户显示`$`，root用户显示`#` |
| `\d` | 日期（格式：星期 月 日） |
| `\t` | 时间（24小时制，格式：HH:MM:SS） |
| `\T` | 时间（12小时制，格式：HH:MM:SS） |
| `\@` | 时间（12小时制，格式：AM/PM） |
| `\n` | 换行 |
| `\[` | 开始非打印字符序列（如颜色代码） |
| `\]` | 结束非打印字符序列 |

## 3. 命令的基本结构

Linux命令通常由命令名称、选项和参数三部分组成。

### 命令的基本格式

```bash
command [options] [arguments]
```

- `command`：要执行的命令名称
- `options`：命令的选项，用于修改命令的行为，通常以`-`或`--`开头
- `arguments`：命令的参数，通常是命令操作的对象，如文件、目录等

例如：

```bash
ls -l /home/user/Documents
```

在这个例子中：
- `ls`是命令名称，用于列出文件和目录
- `-l`是选项，表示以长格式显示
- `/home/user/Documents`是参数，指定要列出的目录

### 命令选项的两种形式

- **短选项**：以单个连字符`-`开头，后跟单个字母，如`-l`、`-a`
- **长选项**：以两个连字符`--`开头，后跟单词，如`--help`、`--verbose`

有些命令同时支持短选项和长选项，例如：

```bash
ls -l  # 短选项
ls --format=long  # 对应的长选项
```

### 组合选项

多个短选项可以组合在一起使用，例如：

```bash
ls -la  # 相当于 ls -l -a
```

## 4. 命令的类型

在Linux系统中，命令主要分为以下几类：

### 4.1 内部命令（Built-in Commands）

内部命令是Shell内置的命令，它们是Shell程序的一部分，执行速度较快。常见的内部命令包括`cd`、`echo`、`pwd`、`export`、`source`、`alias`等。

```bash
# 查看一个命令是否为内部命令
type cd
# 输出：cd is a shell builtin

# 查看所有内部命令
enable
```

### 4.2 外部命令（External Commands）

外部命令是独立于Shell的可执行程序，它们通常位于`/bin`、`/usr/bin`、`/sbin`、`/usr/sbin`等目录中。常见的外部命令包括`ls`、`cp`、`mv`、`rm`、`grep`、`find`等。

```bash
# 查看一个命令是否为外部命令，并显示其路径
type ls
# 输出：ls is hashed (/bin/ls)

# 显示命令的完整路径
which ls
# 输出：/bin/ls
```

### 4.3 Shell函数（Shell Functions）

Shell函数是一组命令的集合，可以像命令一样被调用。函数可以简化复杂的命令序列，提高脚本的可读性和复用性。

```bash
# 定义一个简单的函数
my_function() {
    echo "Hello, this is a shell function!"
    echo "Current directory: $(pwd)"
}

# 调用函数
my_function
```

### 4.4 别名（Aliases）

别名是用户为常用命令创建的简短替代名称，可以提高工作效率。

```bash
# 创建别名
alias ll='ls -l'

# 使用别名
ll

# 查看别名
alias ll
# 输出：alias ll='ls -l'

# 查看所有别名
alias
```

## 5. 命令帮助系统

Linux提供了多种获取命令帮助信息的方法，这对于学习和使用Linux命令非常重要。

### 5.1 man命令（Manual Pages）

`man`命令是最常用的命令帮助工具，它提供了命令的详细说明、选项、参数等信息。

```bash
# 查看命令的手册页
man command_name

# 示例：查看ls命令的手册页
man ls

# 查看特定章节的手册页
man 5 passwd  # 查看passwd配置文件的手册页
```

手册页的章节划分：
1. 普通用户命令
2. 系统调用
3. C库函数
4. 设备文件
5. 配置文件
6. 游戏
7. 杂项
8. 系统管理命令

在man页面中，可以使用以下按键进行导航：
- 空格键：向下翻页
- `b`键：向上翻页
- `/`键：搜索
- `n`键：查找下一个匹配项
- `N`键：查找上一个匹配项
- `q`键：退出man页面

### 5.2 info命令

`info`命令提供了更详细、更结构化的帮助信息，特别是对于GNU项目的软件。

```bash
# 查看命令的info页面
info command_name

# 示例：查看bash命令的info页面
info bash
```

### 5.3 --help选项

大多数命令都支持`--help`选项，用于显示命令的简要帮助信息。

```bash
# 显示命令的简要帮助信息
command_name --help

# 示例：查看ls命令的简要帮助信息
ls --help
```

### 5.4 whatis命令

`whatis`命令用于显示命令的简短描述。

```bash
# 显示命令的简短描述
whatis command_name

# 示例：查看ls命令的简短描述
whatis ls
# 输出：ls (1)               - list directory contents
```

### 5.5 apropos命令

`apropos`命令用于根据关键字搜索相关的命令。

```bash
# 根据关键字搜索命令
apropos keyword

# 示例：搜索与文件复制相关的命令
apropos "copy file"
```

## 6. 命令行编辑和历史

Linux命令行提供了强大的编辑功能，可以帮助用户更高效地输入和修改命令。

### 6.1 命令历史

Shell会记录用户执行过的命令，用户可以通过上下箭头键来查看和重复执行历史命令。

```bash
# 查看命令历史
history

# 执行历史中的第n条命令
!n

# 执行上一条命令
!!

# 执行最近一条以特定字符串开头的命令
!string

# 搜索命令历史
Ctrl+r  # 进入搜索模式，输入关键字进行搜索

# 清除命令历史
history -c

# 删除历史中的特定命令
history -d n  # 删除第n条历史命令
```

### 6.2 命令补全

命令补全是一项非常实用的功能，可以帮助用户快速输入命令、文件名和目录名。

- 按下`Tab`键：补全命令、文件名或目录名
- 按下`Tab`键两次：显示所有可能的补全选项

```bash
# 输入ls -l /u，然后按Tab键，系统会自动补全为ls -l /usr
ls -l /u[TAB]

# 输入c，然后按Tab键两次，系统会显示所有以c开头的命令
c[TAB][TAB]
```

### 6.3 光标移动快捷键

在输入命令时，可以使用以下快捷键来移动光标：

| 快捷键 | 功能 |
|--------|------|
| Left/Right Arrow | 向左/向右移动一个字符 |
| Ctrl+Left Arrow | 向左移动一个单词 |
| Ctrl+Right Arrow | 向右移动一个单词 |
| Home/Ctrl+A | 移动到命令行开头 |
| End/Ctrl+E | 移动到命令行结尾 |

### 6.4 文本编辑快捷键

在输入命令时，可以使用以下快捷键来编辑文本：

| 快捷键 | 功能 |
|--------|------|
| Backspace | 删除光标前的字符 |
| Delete | 删除光标后的字符 |
| Ctrl+U | 删除光标前的所有字符 |
| Ctrl+K | 删除光标后的所有字符 |
| Ctrl+W | 删除光标前的一个单词 |
| Ctrl+Y | 粘贴之前删除的文本 |
| Ctrl+L | 清屏 |
| Ctrl+C | 中断当前命令 |
| Ctrl+D | 退出当前Shell会话 |
| Ctrl+Z | 暂停当前进程 |

## 7. 文件和目录路径

在Linux系统中，路径用于表示文件或目录在文件系统中的位置。

### 7.1 绝对路径和相对路径

- **绝对路径**：从根目录（/）开始的完整路径，如`/home/user/Documents`
- **相对路径**：相对于当前工作目录的路径，如`Documents/reports`或`../Downloads`

```bash
# 使用绝对路径
cd /home/user/Documents

# 使用相对路径
cd Documents
cd ..
cd ../Downloads
```

### 7.2 特殊路径符号

| 符号 | 含义 |
|------|------|
| `/` | 根目录 |
| `.` | 当前目录 |
| `..` | 父目录 |
| `~` | 用户主目录 |
| `-` | 上一个工作目录 |

```bash
# 切换到根目录
cd /

# 在当前目录中执行命令
./script.sh

# 切换到父目录
cd ..

# 切换到用户主目录
cd ~

# 切换到上一个工作目录
cd -
```

### 7.3 显示和更改工作目录

```bash
# 显示当前工作目录
pwd

# 切换工作目录
cd directory_path

# 示例
cd /home/user/Documents
cd ~/Downloads
cd ..
cd -
```

## 8. 环境变量和Shell配置文件

环境变量是在操作系统中用来指定操作系统运行环境的一些参数，它们对于Shell的运行和命令的执行起着重要的作用。

### 8.1 查看环境变量

```bash
# 查看所有环境变量
env
export
printenv

# 查看特定环境变量
echo $PATH
echo $HOME
echo $USER
echo $SHELL
echo $PWD
echo $LANG
echo $TERM
```

### 8.2 设置环境变量

```bash
# 设置临时环境变量
export VAR_NAME=value

# 设置永久环境变量，需要将设置添加到Shell配置文件中
# 编辑配置文件
vim ~/.bashrc  # 对于Bash
vim ~/.zshrc   # 对于Zsh

# 添加环境变量
export VAR_NAME=value

# 保存后，重新加载配置文件
source ~/.bashrc
```

### 8.3 常用环境变量

- **PATH**：命令搜索路径，包含一系列目录，Shell会在这些目录中查找可执行文件
- **HOME**：用户主目录
- **USER**：当前用户名
- **SHELL**：当前使用的Shell
- **PWD**：当前工作目录
- **LANG**：当前语言和字符编码设置
- **TERM**：终端类型
- **PS1**：命令提示符格式
- **HISTFILE**：命令历史文件路径
- **HISTSIZE**：命令历史的最大条数

### 8.4 Shell配置文件

Shell配置文件用于自定义Shell的行为和环境，不同的Shell有不同的配置文件。对于Bash来说，常见的配置文件包括：

- **~/.bashrc**：用户特定的Bash配置文件，通常包含别名、函数和环境变量等设置
- **~/.profile**：用户特定的登录配置文件，在用户登录时执行
- **~/.bash_profile**：类似于~/.profile，但只在Bash登录时执行
- **~/.bash_logout**：在用户退出登录时执行
- **/etc/bashrc**：系统范围的Bash配置文件
- **/etc/profile**：系统范围的登录配置文件

```bash
# 编辑用户的Bash配置文件
vim ~/.bashrc

# 添加别名、函数或环境变量
# 例如：
alias ll='ls -la'
export PATH=$PATH:~/bin

# 保存后，重新加载配置文件
source ~/.bashrc
```

## 9. 命令执行优先级

当用户在命令行中输入一个命令时，Shell会按照以下优先级来确定要执行的命令：

1. 别名（Alias）
2. Shell函数（Function）
3. 内部命令（Built-in Command）
4. 外部命令（External Command，按照PATH环境变量中指定的顺序查找）

```bash
# 查看命令的类型和优先级
type -a command_name

# 示例
type -a ls
# 输出可能类似于：
# ls is aliased to `ls --color=auto'
# ls is /bin/ls
```

## 10. 实践练习

### 练习1：基本命令行操作

```bash
# 打开终端
# 在大多数Linux发行版中，可以使用快捷键Ctrl+Alt+T打开终端

# 查看当前目录
pwd

# 列出当前目录中的文件和目录
ls
ls -la

# 查看命令的帮助信息
ls --help
man ls

# 切换目录
cd /
pwd
cd ~
pwd

# 使用命令历史
# 输入一些命令，然后使用上下箭头键查看历史命令
# 使用!n执行特定的历史命令
# 使用!!执行上一条命令

# 使用命令补全
# 输入命令或路径的前几个字符，然后按Tab键进行补全
# 如果有多个可能的补全选项，按Tab键两次查看所有选项
```

### 练习2：环境变量操作

```bash
# 查看环境变量
echo $PATH
echo $HOME
echo $USER
env

# 设置临时环境变量
export MY_VAR="Hello, Linux!"
echo $MY_VAR

# 编辑Shell配置文件，设置永久环境变量
vim ~/.bashrc
# 添加以下行
export MY_PERMANENT_VAR="This is a permanent variable"
# 保存并退出

# 重新加载配置文件
source ~/.bashrc

echo $MY_PERMANENT_VAR
```

### 练习3：创建和使用别名

```bash
# 创建临时别名
alias ll='ls -la'
alias update='sudo apt update && sudo apt upgrade'

# 使用别名
ll

# 查看别名
alias ll
alias

# 编辑Shell配置文件，添加永久别名
vim ~/.bashrc
# 添加以下行
alias ll='ls -la'
alias update='sudo apt update && sudo apt upgrade'
alias ..='cd ..'
alias ...='cd ../..'
# 保存并退出

# 重新加载配置文件
source ~/.bashrc

# 测试永久别名
ll
..
pwd
...
pwd
```

### 练习4：命令行编辑

```bash
# 在命令行中输入一段文本，然后练习使用以下快捷键：
# Left/Right Arrow：移动光标
# Ctrl+Left Arrow/Ctrl+Right Arrow：移动一个单词
# Home/Ctrl+A：移动到行首
# End/Ctrl+E：移动到行尾
# Ctrl+U：删除光标前的所有字符
# Ctrl+K：删除光标后的所有字符
# Ctrl+W：删除光标前的一个单词
# Ctrl+Y：粘贴之前删除的文本
# Ctrl+L：清屏
# Ctrl+C：中断当前命令
```

通过本章的学习，我们掌握了Linux命令行的基础知识，包括命令的基本结构、命令的类型、命令帮助系统、命令行编辑和历史、文件和目录路径、环境变量和Shell配置文件等。这些知识是使用Linux命令行的基础，掌握这些知识可以帮助我们更高效地使用Linux系统。在后续章节中，我们将继续学习Linux的各种常用命令和高级功能。