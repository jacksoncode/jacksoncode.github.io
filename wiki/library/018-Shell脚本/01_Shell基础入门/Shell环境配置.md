# Shell环境配置

## 检查当前Shell环境

在开始配置Shell环境之前，首先需要了解当前系统中可用的Shell以及你正在使用的Shell。

### 查看系统中可用的Shell
```bash
cat /etc/shells
```

### 查看当前使用的Shell
```bash
echo $SHELL
```

或者使用：
```bash
ps -p $$
```

## 更改默认Shell

如果你想更改默认Shell，可以使用`chsh`命令：

```bash
chsh -s /bin/bash
```

这会将默认Shell更改为Bash。更改后需要重新登录或重启终端才能生效。

## Shell配置文件

不同的Shell有不同的配置文件，这些配置文件在Shell启动时会被读取和执行。

### Bash的配置文件

1. **/etc/profile**：系统级配置文件，对所有用户生效
2. **/etc/bashrc**：系统级Bash配置文件
3. **~/.bash_profile**：用户级配置文件，登录时执行
4. **~/.bashrc**：用户级Bash配置文件，每次启动新的Shell时执行
5. **~/.bash_logout**：用户注销时执行的命令

### 配置文件的加载顺序

1. 系统级配置：/etc/profile → /etc/bashrc
2. 用户级配置：~/.bash_profile → ~/.bashrc

## 环境变量配置

环境变量是Shell配置中的重要部分，它们影响着Shell和程序的行为。

### 查看环境变量

```bash
# 查看所有环境变量
env

# 查看特定环境变量
echo $PATH

# 使用printenv命令
printenv PATH
```

### 设置环境变量

```bash
# 设置临时环境变量（仅在当前Shell会话中有效）
export MY_VAR="hello world"

# 设置并立即使用
export TEMP_VAR="temporary" && echo $TEMP_VAR
```

### 在配置文件中永久设置环境变量

编辑~/.bashrc文件：
```bash
vim ~/.bashrc
```

在文件末尾添加：
```bash
export MY_VAR="hello world"
export PATH=$PATH:/new/path
```

使配置生效：
```bash
source ~/.bashrc
```

## 自定义Shell提示符

Shell提示符可以通过修改PS1环境变量来自定义。

### 查看当前提示符
```bash
echo $PS1
```

### 临时修改提示符
```bash
export PS1="[\u@\h \W]# "
```

### 永久修改提示符
在~/.bashrc中添加：
```bash
export PS1="[\u@\h \W]# "
```

其中：
- `\u`：当前用户名
- `\h`：主机名
- `\W`：当前工作目录
- `\$`：普通用户显示`$`，root用户显示`#`

## 别名设置

别名可以让你用简短的命令替代复杂的命令。

### 查看别名
```bash
alias
```

### 设置临时别名
```bash
alias ll='ls -alF'
alias ..='cd ..'
```

### 永久设置别名
在~/.bashrc中添加：
```bash
alias ll='ls -alF'
alias ..='cd ..'
alias grep='grep --color=auto'
```

### 删除别名
```bash
unalias ll
```

## 历史命令配置

Shell会保存执行过的命令历史，可以通过以下方式配置：

### 查看历史命令数量
```bash
echo $HISTSIZE
```

### 设置历史命令数量
在~/.bashrc中添加：
```bash
export HISTSIZE=1000
export HISTFILESIZE=2000
```

### 历史命令相关命令
```bash
# 查看历史命令
history

# 查看最近10条命令
history 10

# 执行历史命令中的第n条
!n

# 执行最近一次的ls命令
!ls

# 执行上一条命令
!!
```

## 自动补全配置

Bash支持命令和文件名的自动补全功能。

### 启用可编程补全
在~/.bashrc中确保有以下内容：
```bash
if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
    . /etc/bash_completion
fi
```

### 安装bash-completion（如果未安装）
```bash
# Ubuntu/Debian
sudo apt-get install bash-completion

# CentOS/RHEL
sudo yum install bash-completion
```

## 终端设置

### 设置终端标题
在~/.bashrc中添加：
```bash
case "$TERM" in
xterm*|rxvt*)
    PROMPT_COMMAND='echo -ne "\033]0;${USER}@${HOSTNAME}: ${PWD}\007"'
    ;;
*)
    ;;
esac
```

### 设置终端颜色
可以在~/.bashrc中添加颜色定义：
```bash
# 颜色定义
export CLICOLOR=1
export LSCOLORS=GxFxCxDxBxegedabagaced

# 或者使用更详细的定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 使用示例
echo -e "${RED}This is red text${NC}"
```

## 常用Shell配置示例

以下是一个完整的~/.bashrc配置示例：

```bash
# ~/.bashrc: executed by bash(1) for non-login shells.

# 如果不是交互式Shell，直接返回
case $- in
    *i*) ;;
      *) return;;
esac

# 不记录重复的命令和空命令
HISTCONTROL=ignoreboth

# 增大历史命令记录数量
HISTSIZE=1000
HISTFILESIZE=2000

# 自动追加历史命令
shopt -s histappend

# 检查窗口大小
shopt -s checkwinsize

# 启用可编程补全
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

# 设置别名
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'

# 设置PS1提示符
if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# 启用颜色支持
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi
```

## 总结

正确的Shell环境配置可以大大提高工作效率。通过配置环境变量、别名、提示符等，可以让你的Shell使用体验更加个性化和高效。记住在修改配置文件后要使用`source`命令使其生效，或者重新打开终端。