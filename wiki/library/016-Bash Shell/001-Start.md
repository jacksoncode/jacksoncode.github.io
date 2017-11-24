# Start

在Windows上敲Linux命令？准确的说应该是Unix命令，怎么做？可以安装一下Git，然后运行``Git Bash``:

![](assets/016/20171124-488463a9.png)

### 查看目录文件

* 可以直接``cd``到目标目录，然后``ls``。
* 也可以在上一层``ls Pictures``
* 还可以``ls Pictures/../Pictures``

另外，``cd Pictures; ls``意思就是先``cd``到这个目录，在执行``ls``。

### 其他命令

* ``pwd``查看当前完整目录
* ``ls .``查看当前所在目录
* ``ls ~``列出主目录
* ``ls desktop*``列出所有desktop开头的文件

> ``* ``是通配符

### 移动文件
将 epub 文件从 Documents/Books 移回到 Documents，当前工作目录在主目录，即Documents的父层。

**三种方法：**

* ``mv 'Documents/Books' Documents``
* ``cd Documents; mv 'Books'/*.epub .``
* ``cd 'Documents/Books'; mv * ..``

### 下载文件

``curl``命令

``curl -o baidu.html -L'https://www.baidu.com'``

``curl -L -o dictionary.txt 'https://tinyurl.com/zeyq9vc'``

将百度这个网页保存到本地baidu.html文件中。

### 查看文件

* ``cat dictionary.txt`` 显示出文本的全部内容，但直接显示到结尾
* ``less dictionary.txt``单屏显示文本的内容，按空格切换下一屏，或者上下键来滚动
* 查看状态可以输入``/google``来查找内容google
* 按``q``退出查看状态

### 创建和删除文件
文件名尽量都用单引号包围。

* 创建目录：``mkdir fordername``
* 删除单个文件：``rm 'test'``
* 删除两个文件：``rm 'BadFile' 'GoodFile'``
* 通删除多个文件：``rm *'Bad F'*``，所有文件名中包含这段内容的，都会被删掉。前后的*代表这段文字前后的其他内容，用通配符（*）代替。

### 搜索

``grep shell dictionary.txt | less``

这个命令中``|``的作用：

把前面一段命令，发给后面的命令来执行。``grep shell``是查找包含``shell``字段的内容，然后通过``less``方式来执行.

另一个例子：

``curl -L 'https://tinyurl.com/zeyq9vc' | grep fish``，从这个网页中获取包含``fish``字段的内容。

### 计数
**第一种方式：**
  ``wc:word count``

``curl -L 'https://tinyurl.com/zeyq9vc' | grep fish | wc -l`` 后面的``-l``是统计行数（lines）

**第二种方式：**

语法：``grep -c xxx``

举例：

``curl -L 'https://tinyurl.com/zeyq9vc' | grep -c fish``

### 变量和Shell

Shell和编程语言一样，也有变量，变量的声明和赋值：

````bash
numbers='one two three'
echo $numbers  //打印变量numbers
````

shell中的变量有两种：shell变量和环境变量。

* shell变量是shell内部存在的，比如$LINES、$COLUMNS
* 环境变量是运行的程序共享的变量，比如$PATH、$PWD

添加一个新的环境变量：

* ``PATH=$PATH:/new/dir/here``  这种方式添加的环境变量仅在当前终端关闭前有效，一旦关闭就没用了
* Windows（git bash）或者MAC将上面命令添加在``.bash_profile``文件中，Linux可以添加在``.bashrc``文件中

### 别名

设置一个短命令，代替命令加参数：

````bash
alias la='ls -la'
````

这样之后执行``la``就等于在执行长命令``ls -la``了。

直接执行``alias``可以查看已经设置了哪些别名：

````bash
$ alias
alias la='ll -la'
alias ll='ls -l'
alias ls='ls -F --color=auto --show-control-chars'
````

但是别名和环境变量一样，只在当前窗口生效，如果想在下次启动时依然生效，也可以同样的加入到**.bash_profile**文件中。

![](assets/016/20171124-41cffc4e.png)

最后一条比较有用，为什么这么说呢？有时候手误把``ls``敲成了``sl``，这时依然生效，是不是很机智？
