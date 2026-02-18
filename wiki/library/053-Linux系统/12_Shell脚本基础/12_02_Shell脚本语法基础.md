# Shell脚本语法基础

## 1 变量与数据类型

### 1.1 变量定义与赋值

在Shell脚本中，变量定义不需要声明类型，直接赋值即可：

```bash
# 变量定义
name="Linux"
version=20.04
is_stable=true

# 注意：等号两边不能有空格
# 错误示例：name = "Linux"  ❌
```

### 1.2 变量命名规则

| 规则 | 示例 | 说明 |
|------|------|------|
| 只能包含字母、数字和下划线 | `user_name`, `var1` | ✅ 正确 |
| 不能以数字开头 | `1var` | ❌ 错误 |
| 区分大小写 | `Name` 和 `name` 是不同的变量 |
| 避免使用特殊字符 | `user-name` | ❌ 错误 |

### 1.3 变量类型

#### 1.3.1 字符串变量

```bash
# 字符串定义
str1="Hello World"
str2='Single quoted string'
str3=UnquotedString

# 字符串拼接
greeting="Hello"
name="Linux"
message="$greeting, $name!"
```

#### 1.3.2 整数变量

```bash
# 整数定义
num1=100
num2=-50

# 整数运算（使用$(())或let）
result=$((num1 + num2))
let "result = num1 * num2"
```

#### 1.3.3 数组变量

```bash
# 一维数组
fruits=("apple" "banana" "orange")
echo ${fruits[0]}  # 输出：apple

# 关联数组（需要bash 4.0+）
declare -A person
person[name]="John"
person[age]=30
```

## 2 特殊变量

### 2.1 位置参数变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `$0` | 脚本名称 | `./myscript.sh` |
| `$1`, `$2`, ... | 位置参数 | `$1` 是第一个参数 |
| `$#` | 参数个数 | 如果传入3个参数，值为3 |
| `$*` | 所有参数 | 所有参数作为一个字符串 |
| `$@` | 所有参数 | 每个参数作为独立的字符串 |

```bash
#!/bin/bash
echo "脚本名称：$0"
echo "第一个参数：$1"
echo "第二个参数：$2"
echo "参数总数：$#"
echo "所有参数：$*"
echo "所有参数（独立）：$@"
```

### 2.2 环境变量

```bash
# 常用环境变量
USER        # 当前用户名
HOME        # 用户主目录
PWD         # 当前工作目录
PATH        # 命令搜索路径
SHELL       # 当前Shell
HOSTNAME    # 主机名
```

### 2.3 特殊状态变量

```bash
$?  # 上一个命令的退出状态（0表示成功）
$$  # 当前脚本的进程ID
$!  # 最后一个后台进程的PID
```

## 3 引号的使用

### 3.1 双引号（""）

- 允许变量扩展
- 允许命令替换
- 保留空格和特殊字符

```bash
name="Linux"
echo "Hello, $name"          # 输出：Hello, Linux
echo "Today is $(date)"      # 输出：Today is 当前日期
```

### 3.2 单引号（''）

- 禁止变量扩展
- 禁止命令替换
- 所有内容按字面意义处理

```bash
name="Linux"
echo 'Hello, $name'          # 输出：Hello, $name
echo 'Today is $(date)'      # 输出：Today is $(date)
```

### 3.3 反引号（``）或$()

用于命令替换：

```bash
# 两种写法等价
current_date=`date`
current_date=$(date)

echo "当前日期：$current_date"
```

## 4 运算符

### 4.1 算术运算符

```bash
# 整数运算
a=10
b=3

echo $((a + b))   # 加法：13
echo $((a - b))   # 减法：7
echo $((a * b))   # 乘法：30
echo $((a / b))   # 除法：3
echo $((a % b))   # 取模：1

# 自增自减
((a++))           # a增加1
echo $a          # 输出：11
```

### 4.2 比较运算符

#### 4.2.1 字符串比较

| 运算符 | 说明 | 示例 |
|--------|------|------|
| `=` 或 `==` | 等于 | `[ "$a" = "$b" ]` |
| `!=` | 不等于 | `[ "$a" != "$b" ]` |
| `-z` | 字符串长度为0 | `[ -z "$a" ]` |
| `-n` | 字符串长度不为0 | `[ -n "$a" ]` |
| `<` | 小于（ASCII顺序） | `[[ "$a" < "$b" ]]` |
| `>` | 大于（ASCII顺序） | `[[ "$a" > "$b" ]]` |

#### 4.2.2 数值比较

| 运算符 | 说明 | 示例 |
|--------|------|------|
| `-eq` | 等于 | `[ "$a" -eq "$b" ]` |
| `-ne` | 不等于 | `[ "$a" -ne "$b" ]` |
| `-lt` | 小于 | `[ "$a" -lt "$b" ]` |
| `-le` | 小于等于 | `[ "$a" -le "$b" ]` |
| `-gt` | 大于 | `[ "$a" -gt "$b" ]` |
| `-ge` | 大于等于 | `[ "$a" -ge "$b" ]` |

#### 4.2.3 文件测试运算符

| 运算符 | 说明 | 示例 |
|--------|------|------|
| `-e` | 文件存在 | `[ -e "$file" ]` |
| `-f` | 是普通文件 | `[ -f "$file" ]` |
| `-d` | 是目录 | `[ -d "$dir" ]` |
| `-r` | 文件可读 | `[ -r "$file" ]` |
| `-w` | 文件可写 | `[ -w "$file" ]` |
| `-x` | 文件可执行 | `[ -x "$file" ]` |
| `-s` | 文件大小大于0 | `[ -s "$file" ]` |

## 5 条件语句

### 5.1 if语句

#### 5.1.1 基本语法

```bash
# 基本if语句
if [ 条件 ]; then
    命令
fi

# if-else语句
if [ 条件 ]; then
    命令1
else
    命令2
fi

# if-elif-else语句
if [ 条件1 ]; then
    命令1
elif [ 条件2 ]; then
    命令2
else
    命令3
fi
```

#### 5.1.2 使用示例

```bash
#!/bin/bash
# 判断文件类型

file="$1"

if [ -z "$file" ]; then
    echo "用法：$0 文件名"
    exit 1
fi

if [ ! -e "$file" ]; then
    echo "文件不存在：$file"
elif [ -d "$file" ]; then
    echo "$file 是一个目录"
elif [ -f "$file" ]; then
    echo "$file 是一个普通文件"
else
    echo "$file 是其他类型的文件"
fi
```

### 5.2 case语句

#### 5.2.1 基本语法

```bash
case 变量 in
    模式1)
        命令1
        ;;
    模式2)
        命令2
        ;;
    *)
        默认命令
        ;;
esac
```

#### 5.2.2 使用示例

```bash
#!/bin/bash
# 根据文件扩展名判断文件类型

filename="$1"
extension="${filename##*.}"

case "$extension" in
    txt|log|conf)
        echo "这是一个文本文件"
        ;;
    jpg|jpeg|png|gif)
        echo "这是一个图片文件"
        ;;
    sh|bash)
        echo "这是一个Shell脚本"
        ;;
    py)
        echo "这是一个Python脚本"
        ;;
    *)
        echo "未知文件类型"
        ;;
esac
```

## 6 循环结构

### 6.1 for循环

#### 6.1.1 基本语法

```bash
# 语法1：遍历列表
for 变量 in 列表; do
    命令
done

# 语法2：C语言风格
for (( 初始值; 条件; 增量 )); do
    命令
done
```

#### 6.1.2 使用示例

```bash
#!/bin/bash
# 遍历数组

fruits=("apple" "banana" "orange" "grape")

for fruit in "${fruits[@]}"; do
    echo "水果：$fruit"
done

# 遍历数字序列
for i in {1..5}; do
    echo "数字：$i"
done

# C语言风格循环
for ((i=1; i<=10; i++)); do
    echo "计数：$i"
done
```

### 6.2 while循环

#### 6.2.1 基本语法

```bash
while [ 条件 ]; do
    命令
done
```

#### 6.2.2 使用示例

```bash
#!/bin/bash
# 读取用户输入

count=0
while [ $count -lt 5 ]; do
    read -p "请输入一个数字（输入q退出）：" input
    
    if [ "$input" = "q" ]; then
        break
    fi
    
    echo "你输入的是：$input"
    ((count++))
done

echo "循环结束，共输入了 $count 次"
```

### 6.3 until循环

```bash
#!/bin/bash
# until循环示例

counter=1
until [ $counter -gt 5 ]; do
    echo "计数器：$counter"
    ((counter++))
done
```

## 7 输入输出重定向

### 7.1 标准输入输出

| 描述符 | 名称 | 默认设备 |
|--------|------|----------|
| 0 | 标准输入（stdin） | 键盘 |
| 1 | 标准输出（stdout） | 屏幕 |
| 2 | 标准错误（stderr） | 屏幕 |

### 7.2 重定向操作符

```bash
# 输出重定向
echo "Hello" > file.txt      # 覆盖写入
echo "World" >> file.txt     # 追加写入

# 错误重定向
ls /nonexistent 2> error.log  # 错误信息重定向

# 同时重定向输出和错误
command > output.log 2>&1    # 合并重定向

# 输入重定向
cat < file.txt               # 从文件读取输入
```

### 7.3 Here文档

```bash
#!/bin/bash
# Here文档示例

cat << EOF
这是一个Here文档示例
可以包含多行文本
变量会被解析：$USER
当前目录：$(pwd)
EOF
```

## 8 综合示例：文件备份脚本

```bash
#!/bin/bash
# file_backup.sh
# 文件备份脚本

# 检查参数
if [ $# -ne 2 ]; then
    echo "用法：$0 <源文件> <备份目录>"
    exit 1
fi

source_file="$1"
backup_dir="$2"
timestamp=$(date +%Y%m%d_%H%M%S)
backup_file="${backup_dir}/$(basename "$source_file")_${timestamp}.bak"

# 检查源文件是否存在
if [ ! -f "$source_file" ]; then
    echo "错误：源文件不存在：$source_file"
    exit 1
fi

# 检查备份目录是否存在，不存在则创建
if [ ! -d "$backup_dir" ]; then
    mkdir -p "$backup_dir"
    echo "创建备份目录：$backup_dir"
fi

# 执行备份
cp "$source_file" "$backup_file"

if [ $? -eq 0 ]; then
    echo "备份成功：$backup_file"
else
    echo "备份失败"
    exit 1
fi
```

## 9 调试技巧

### 9.1 启用调试模式

```bash
#!/bin/bash -x  # 在Shebang中添加-x
# 或者在脚本中使用
set -x  # 开启调试
set +x  # 关闭调试
```

### 9.2 检查语法

```bash
bash -n script.sh    # 检查语法错误
```

### 9.3 跟踪执行

```bash
bash -v script.sh   # 详细模式，显示执行的每一行
bash -x script.sh   # 调试模式，显示变量展开后的命令
```