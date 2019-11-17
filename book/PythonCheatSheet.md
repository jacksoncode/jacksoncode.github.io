# Python新手小抄秘籍

## 概述

#### 变量和字符串（Variable and String）

> “变量用来存储具体的值，“字符串”由一连串的字符组成，并用单引号或者双引号括起来。

打印 Hello World

````python
print("Hello World!")
````

Hello World 存储在变量里

````python
msg = "Hello World!"
print(msg)
````

字符串连接

````python
first_name = 'albert'
last_name = 'einstein'
full_name = first_name + ' ' + last_name
print(full_name)
````

#### 列表（Lists）

> 列表将元素按照一定顺序存储起来，用户可以使用索引 index 或者循环 loop 来对元素进行操作。

创建一个列表
````python
bikes = ['trek', 'redline', 'giant']
````
获取列表的第一个元素
````python
first_bike = bikes[0]
````
获取列表的最后一个元素
````python
first_bike = bikes[-1]
````
遍历列表（相当于把列表中所有元素撸一遍）
````python
for bike in bikes:
    print(bike)
````
向列表中增加元素
````python
bikes = []
bikes.append('trek')
bikes.append('redline')
bikes.append('giant')
````
创建数值列表
````python
squares = []
for x in range(1, 11):
    squares.append(x**2)
````
列表的推导
````python
squares = [x**2 for x in range(1, 11)]
````
列表的切片
````python
finishers = ['sam', 'bob', 'ada', 'bea']
first_two = finishers[:2]
````
列表的复制

````python
copy_of_bikes = bikes[:]
````

#### 元组（Tuples）

> 元组类似于列表，只不过元组中的元素不能够被操作。

创建一个元素

````python
dimensions = (1920, 1080)
````

#### If语句

#### 字典

#### 用户输入

> 程序提示用户需要输入，所有的输入都被存储在字符串中。

提示输入值

````python
name = input("What's your name? ")
print("Hello, " + name + "!")
````

#### while循环

#### 函数

#### 类

#### 学以致用

#### 文件files操作

#### 异常处理 Exceptions

#### Python 的佛性

## 列表 Lists

## 字典 Dictionaries

## if语句和while循环

## 函数Functions

## 文件和异常



