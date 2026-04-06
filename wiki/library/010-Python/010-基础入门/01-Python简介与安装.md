# Python 基础语法入门

## 1. Python 简介

Python 是一种高级、解释型、面向对象的编程语言，由 Guido van Rossum 于 1991 年创建。它以简洁易读的语法和强大的功能著称，广泛应用于：

- Web 开发（Django、Flask）
- 数据科学与机器学习（NumPy、Pandas、TensorFlow）
- 自动化脚本与 DevOps
- 人工智能与深度学习

## 2. 第一个 Python 程序

```python
# Hello World 程序
print("Hello, World!")

# 变量与数据类型
name = "Python"           # 字符串
version = 3.12           # 数字
is_popular = True        # 布尔值

print(f"Welcome to {name} {version}!")
```

## 3. 变量与数据类型

### 基本数据类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `int` | 整数 | `42`, `-17`, `0` |
| `float` | 浮点数 | `3.14`, `-0.5` |
| `str` | 字符串 | `"hello"`, `'world'` |
| `bool` | 布尔值 | `True`, `False` |
| `None` | 空值 | `None` |

### 类型转换

```python
# 字符串转整数
num = int("42")        # 42
# 整数转字符串
text = str(42)         # "42"
# 字符串转浮点数
pi = float("3.14")     # 3.14
# 转布尔值
is_valid = bool(1)     # True
is_empty = bool("")    # False
```

## 4. 运算符

### 算术运算符

```python
a, b = 10, 3

print(a + b)   # 13 - 加法
print(a - b)    # 7  - 减法
print(a * b)    # 30 - 乘法
print(a / b)    # 3.333... - 除法
print(a // b)   # 3  - 整除
print(a % b)    # 1  - 取余
print(a ** b)   # 1000 - 幂运算
```

### 比较运算符

```python
x = 5

print(x == 5)   # True  - 等于
print(x != 3)    # True  - 不等于
print(x > 3)     # True  - 大于
print(x < 10)    # True  - 小于
print(x >= 5)    # True  - 大于等于
print(x <= 5)    # True  - 小于等于
```

### 逻辑运算符

```python
a, b = True, False

print(a and b)  # False - 逻辑与
print(a or b)   # True  - 逻辑或
print(not a)    # False - 逻辑非
```

## 5. 字符串操作

### 字符串基本操作

```python
text = "Hello, Python!"

# 索引与切片
print(text[0])       # H
print(text[0:5])     # Hello
print(text[-6:])      # Python!

# 字符串方法
print(text.upper())           # HELLO, PYTHON!
print(text.lower())           # hello, python!
print(text.replace("Hello", "Hi"))  # Hi, Python!
print(text.split(", "))       # ['Hello', 'Python!']
print(len(text))              # 14
```

### 字符串格式化

```python
name = "Alice"
age = 25

# f-string (推荐)
print(f"My name is {name}, I'm {age} years old.")

# format 方法
print("My name is {}, I'm {} years old.".format(name, age))

# % 格式化
print("My name is %s, I'm %d years old." % (name, age))
```

## 6. 列表与元组

### 列表 (List)

```python
fruits = ["apple", "banana", "cherry"]

# 添加元素
fruits.append("date")
fruits.insert(1, "avocado")

# 删除元素
fruits.remove("banana")
popped = fruits.pop()  # 返回被删除的元素

# 列表操作
print(fruits[0])       # 第一个元素
print(fruits[-1])      # 最后一个元素
print(len(fruits))     # 列表长度
fruits.sort()          # 排序
```

### 元组 (Tuple)

```python
# 元组是不可变的
coordinates = (10, 20, 30)

# 解包
x, y, z = coordinates
print(f"X: {x}, Y: {y}, Z: {z}")

# 多重赋值
a, b = 1, 2
a, b = b, a  # 交换变量
```

## 7. 字典与集合

### 字典 (Dictionary)

```python
person = {
    "name": "Bob",
    "age": 30,
    "city": "Beijing"
}

# 访问与修改
print(person["name"])      # Bob
person["age"] = 31         # 修改值
person["email"] = "bob@example.com"  # 添加新键值对

# 常用方法
print(person.keys())       # 所有键
print(person.values())     # 所有值
print(person.items())      # 所有键值对
print(person.get("phone", "N/A"))  # 安全获取
```

### 集合 (Set)

```python
# 集合是无序且不重复的
a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}

print(a | b)   # 并集: {1, 2, 3, 4, 5, 6, 7, 8}
print(a & b)   # 交集: {4, 5}
print(a - b)   # 差集: {1, 2, 3}
print(a ^ b)   # 对称差集: {1, 2, 3, 6, 7, 8}
```

## 8. 注释与文档

```python
# 这是单行注释

"""
这是多行字符串
常用作文档字符串
"""

def add(a, b):
    """
    计算两个数的和
    
    Args:
        a: 第一个数
        b: 第二个数
    
    Returns:
        两数之和
    """
    return a + b
```

## 9. 实战练习

### 练习 1: 温度转换器

```python
def celsius_to_fahrenheit(celsius):
    """摄氏温度转华氏温度"""
    return celsius * 9/5 + 32

def fahrenheit_to_celsius(fahrenheit):
    """华氏温度转摄氏温度"""
    return (fahrenheit - 32) * 5/9

# 测试
print(celsius_to_fahrenheit(0))    # 32.0
print(fahrenheit_to_celsius(100)) # 37.777...
```

### 练习 2: 简单计算器

```python
def calculator(a, operator, b):
    """简单计算器"""
    operations = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y if y != 0 else "Error: Division by zero"
    }
    return operations.get(operator, lambda x, y: "Invalid operator")(a, b)

print(calculator(10, '+', 5))   # 15
print(calculator(10, '/', 0))  # Error: Division by zero
```

## 10. 下一步学习

- [Python 数据类型详解](./011-数据类型/01-数字类型.md)
- [Python 控制流程](./012-控制流程/01-条件语句.md)
- [Python 函数与模块](./013-函数与模块/01-函数定义.md)
