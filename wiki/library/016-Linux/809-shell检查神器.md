# shell检查神器

写过shell脚本的人都知道，即便出现一些简单的语法错误，运行的时候也可能没有办法发现。有些看似运行正确的脚本，实际上可能在某些分支，某些场景下仍然出现错误，而有的写法可能运行正常，但是却不符合POSIX标准，不具备可移植性。

诚然，shell脚本是解释运行，没有办法向C/C++那样严格检查，但是我们仍然可以借助一些工具帮助我们提前发现一些错误。

### shellcheck

shellcheck就是这样的一个工具。它可以在多种场景下使用，包括在线，命令行检查，编辑器配置，下面逐一介绍。

### 在线使用

顾名思义，它提供了一个在线的检查地址，https://www.shellcheck.net/，进入网址即可使用。
例如，你输入你的脚本内容：

````bash
#!/bin/sh
for n in {1..$RANDOM}
do
  str=""
  if (( n % 3 == 0 ))
  then
    str="fizz"
  fi
  if [ $[n%5] == 0 ]
  then
    str="$strbuzz"
  fi
  if [[ ! $str ]]
  then
    str="$n"
  fi
  echo "$str"
done
````

它会给出错误提示或者建议：

````bash
Line 2:
for n in {1..$RANDOM}
         ^-- SC2039: In POSIX sh, brace expansion is undefined.
             ^-- SC2039: In POSIX sh, RANDOM is undefined.

Line 5:
  if (( n % 3 == 0 ))
     ^-- SC2039: In POSIX sh, standalone ((..)) is undefined.

Line 9:
  if [ $[n%5] == 0 ]
       ^-- SC2039: In POSIX sh, $[..] in place of $((..)) is undefined.
       ^-- SC2007: Use $((..)) instead of deprecated $[..]
              ^-- SC2039: In POSIX sh, == in place of = is undefined.

Line 11:
    str="$strbuzz"
         ^-- SC2154: strbuzz is referenced but not assigned.

Line 13:
  if [[ ! $str ]]
     ^-- SC2039: In POSIX sh, [[ ]] is undefined.
````

怎么样，是不是很给力，每个可能的错误都提示了。新手写shell出现莫名的报错时，可以尝试使用奥。当然例子中很多并不是真的错误，而是某种写法不符合POSIX标准，这种情况也应该避免。

关于shell的基本内容，也可以参考《shell必备基础知识》。

### 命令行使用
命令行安装也很简单(记得使用root权限)，ubuntu下：

````bash
$ apt-get install shellcheck
````

centos下：

````bash
$ yum -y install epel-release
````

Fedora下：

````bash
$ dnf install ShellCheck
````

使用方法也很简单了：

````bash
$ shellcheck myscript.sh
````

举个例子，下面的写法是新手最容易出错的地方之一：

````bash
#!/bin/bash
if[ $# -eq 0 ]
then
    echo "no para"
else
    echo "$# para"
fi
exit 0
````

看运行报错：

````bash
./test.sh: line 4: if[ 0 -eq 0 ]: command not found
./test.sh: line 5: syntax error near unexpected token `then'
./test.sh: line 5: `then'
````

只是告诉你在then附近有语法问题，到底什么问题呢？我们用**shellcheck**看看：

````bash
$ shellcheck test.sh
In test.sh line 4:
if[ $# -eq 0 ]
  ^-- SC1069: You need a space before the [.
````

这么一看，就很清楚了，原来[前面少了空格。

### 编辑器中使用

当然也可以把它安装到你熟悉的编辑器中，虽然它们本身都有语法高亮的功能，但是并没有直接的信息提示，安装**shellcheck**类工具，达到编写即提示的效果。

* Emacs, 可以使用 Flycheck.
* Sublime,可以使用 SublimeLinter.
* Atom，可以使用 Linter.
* vim ,可以使用ale或者syntastic

当然了，现代很多IDE都有这样检查功能，这里只说编辑器。

这里以**syntastic**为例，实际上它支持多种语言的语法检查。

**安装过程：**

1. 安装pathogen.vim

````bash
$ mkdir -p ~/.vim/autoload ~/.vim/bundle && \
curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim
````

并且在vimrc文件中配置以下内容：

````bash
execute pathogen#infect()
````

2. 安装 Install syntastic

````bash
cd ~/.vim/bundle && \
git clone --depth=1 https://github.com/vim-syntastic/syntastic.git
````

3. 测试安装情况

打开vim，输入以下内容

````bash
:Helptags
````

如果没有报错，说明安装正常。
在vimrc中配置以下内容：

````bash
set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*

let g:syntastic_always_populate_loc_list = 1
let g:syntastic_auto_loc_list = 1
let g:syntastic_check_on_open = 1
````

常用：

````bash
:Errors 显示错误面板
:lnext  到下一个错误
:lprevious 到上一个错误
````

更多安装详情也可以参考https://github.com/vim-syntastic/syntastic。

以上是官网推荐的安装方式，也可以在安装了Vundle（这是一种老旧的插件管理方式，你可以尝试vim-plug等其他插件管理工具）的前提下，通过在配置文件中加入：

````bash
Plugin 'scrooloose/syntastic'
````

打开vim输入：

````bash
：PluginInstall
````

即可安装，具体安装方式可以参考《vim完整开发环境配置--老旧版》。

使用效果：

shell检查：

![](assets/016/809-1587301915149.png)

C语言语法检查：

![](assets/016/809-1587301921380.png)

实际上它可以支持几乎所有常见编程语言的语法检查。

具体可以查看这里
https://github.com/vim-syntastic/syntastic/blob/master/doc/syntastic-checkers.txt

不知道vimrc文件在哪里？
打开vim，输入：

````bash
：version
````

就可以看到啦：

````bash
   system vimrc file: "$VIM/vimrc"
     user vimrc file: "$HOME/.vimrc"
 2nd user vimrc file: "~/.vim/vimrc"
      user exrc file: "$HOME/.exrc"
  system gvimrc file: "$VIM/gvimrc"
    user gvimrc file: "$HOME/.gvimrc"
2nd user gvimrc file: "~/.vim/gvimrc"
    system menu file: "$VIMRUNTIME/menu.vim"
````

它们区别在于生效范围不一样，对于用户的vimrc，自然只是对特定用户生效。

### 总结

工欲善其事必先利其器，有好的工具，自然就该用起来。