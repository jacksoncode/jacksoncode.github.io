# 第一个Shell脚本

## 创建简单的Shell脚本

让我们从一个最简单的Shell脚本开始。Shell脚本本质上是一个包含一系列Shell命令的文本文件。

### 第一个脚本：Hello World

创建一个名为`hello.sh`的文件：

```bash
#!/bin/bash
# 这是一个简单的Shell脚本示例
echo "Hello, World!"
```

让我们逐步解释这个脚本：

1. `#!/bin/bash`：这是Shebang（也叫Hashbang），它告诉系统这个脚本应该使用哪个解释器来执行。在这个例子中，我们指定使用bash解释器。
2. `# 这是一个简单的Shell脚本示例`：以`#`开头的行是注释，不会被解释执行。
3. `echo "Hello, World!"`：这是实际执行的命令，会输出"Hello, World!"。

### 使脚本可执行

创建完脚本文件后，需要给它添加执行权限：

```bash
chmod +x hello.sh
```

### 运行脚本

有几种方式可以运行这个脚本：

1. 直接执行（需要有执行权限）：
```bash
./hello.sh
```

2. 使用bash命令执行：
```bash
bash hello.sh
```

3. 使用sh命令执行：
```bash
sh hello.sh
```

## Shell脚本的基本结构

一个完整的Shell脚本通常包含以下几个部分：

### 1. Shebang行
```bash
#!/bin/bash
```

### 2. 注释
```bash
# 脚本描述
# 作者信息
# 创建日期
# 版本信息
```

### 3. 变量定义
```bash
# 定义变量
name="张三"
age=25
```

### 4. 函数定义
```bash
# 定义函数
greet() {
    echo "你好，$1"
}
```

### 5. 主要逻辑
```bash
# 主要执行逻辑
echo "欢迎使用本脚本"
greet $name
```

## 更完整的示例

让我们创建一个更完整的脚本示例，名为`system_info.sh`：

```bash
#!/bin/bash

# 脚本名称: system_info.sh
# 描述: 显示系统基本信息
# 作者: example
# 版本: 1.0

# 定义颜色变量
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 定义函数
print_header() {
    echo -e "${GREEN}========== 系统信息报告 ==========${NC}"
}

get_system_info() {
    echo -e "${YELLOW}系统信息:${NC}"
    echo "操作系统: $(uname -s)"
    echo "内核版本: $(uname -r)"
    echo "主机名: $(hostname)"
    echo ""
}

get_user_info() {
    echo -e "${YELLOW}用户信息:${NC}"
    echo "当前用户: $(whoami)"
    echo "用户ID: $(id -u)"
    echo "组ID: $(id -g)"
    echo ""
}

get_disk_info() {
    echo -e "${YELLOW}磁盘使用情况:${NC}"
    df -h | head -5
    echo ""
}

get_memory_info() {
    echo -e "${YELLOW}内存使用情况:${NC}"
    free -h
    echo ""
}

# 主程序
print_header
get_system_info
get_user_info
get_disk_info
get_memory_info

echo -e "${GREEN}========== 报告结束 ==========${NC}"
```

运行这个脚本：
```bash
chmod +x system_info.sh
./system_info.sh
```

## 脚本参数处理

Shell脚本可以接收命令行参数，这些参数在脚本中通过特殊变量访问：

- `$0`：脚本名称
- `$1`、`$2`...：第1个、第2个...参数
- `$#`：参数个数
- `$@`：所有参数列表
- `$*`：所有参数作为一个字符串

创建一个示例脚本`greet.sh`：

```bash
#!/bin/bash

# 检查参数个数
if [ $# -eq 0 ]; then
    echo "用法: $0 <姓名> [年龄]"
    exit 1
fi

# 获取参数
name=$1
age=$2

# 输出问候语
echo "你好, $name!"

# 如果提供了年龄，则输出年龄信息
if [ -n "$age" ]; then
    echo "你的年龄是 $age 岁。"
fi

# 显示所有参数
echo "所有参数: $@"
echo "参数个数: $#"
```

运行示例：
```bash
chmod +x greet.sh
./greet.sh 张三
./greet.sh 张三 25
```

## 错误处理和退出码

良好的Shell脚本应该包含错误处理机制：

```bash
#!/bin/bash

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 检查文件是否存在
if [ ! -f "/etc/passwd" ]; then
    echo "错误: /etc/passwd 文件不存在"
    exit 1
fi

# 检查命令是否存在
if ! command_exists curl; then
    echo "错误: curl 命令未安装"
    exit 1
fi

# 正常退出
exit 0
```

## 调试Shell脚本

### 使用set命令调试

```bash
# 显示执行的命令
set -x

# 你的脚本内容
echo "调试模式开启"

# 关闭调试模式
set +x
```

### 使用bash -x运行脚本

```bash
bash -x your_script.sh
```

### 在脚本中添加调试信息

```bash
#!/bin/bash

debug() {
    if [ "$DEBUG" = "1" ]; then
        echo "DEBUG: $*" >&2
    fi
}

debug "脚本开始执行"
name="张三"
debug "变量name的值为: $name"
echo "你好, $name!"
debug "脚本执行完毕"
```

运行时开启调试：
```bash
DEBUG=1 ./your_script.sh
```

## 最佳实践

### 1. 总是在脚本开头添加Shebang
```bash
#!/bin/bash
```

### 2. 添加错误处理
```bash
set -e  # 遇到错误时退出
set -u  # 使用未定义变量时退出
set -o pipefail  # 管道中任何命令失败时退出
```

### 3. 使用函数组织代码
```bash
# 定义函数
check_requirements() {
    # 检查依赖
}

main() {
    # 主要逻辑
}

# 调用主函数
main "$@"
```

### 4. 添加帮助信息
```bash
usage() {
    echo "用法: $0 [选项]"
    echo "选项:"
    echo "  -h, --help    显示帮助信息"
    echo "  -v, --verbose 增加输出详细程度"
}
```

## 总结

创建和运行Shell脚本是Linux系统管理和自动化的重要技能。通过本章的学习，你应该能够：

1. 创建简单的Shell脚本
2. 给脚本添加执行权限
3. 运行Shell脚本
4. 理解脚本的基本结构
5. 处理命令行参数
6. 进行基本的错误处理
7. 调试Shell脚本

随着学习的深入，你将能够编写更复杂和实用的Shell脚本来自动化各种任务。