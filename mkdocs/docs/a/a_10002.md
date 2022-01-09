# Markdown 中增加徽章

### 什么是徽章？

看下这张图：

![](assets/003/04-6d25c18c.png)

其他人的 **Readme** 文件中都有，显示工程的收藏数、fork数、问题数、软件包的下载量、License等。
是不是很炫？

就是长下面这个样子的：

[![](https://img.shields.io/github/stars/jacksoncode/jacksoncode.github.io.svg?style=social&label=Star)](https://github.com/jacksoncode/jacksoncode.github.io "GitHub Stars")
[![](https://img.shields.io/github/forks/jacksoncode/jacksoncode.github.io.svg?style=social&label=Fork)](https://github.com/jacksoncode/jacksoncode.github.io "GitHub Forks")
[![](https://img.shields.io/github/issues-raw/jacksoncode/jacksoncode.github.io.svg)](https://github.com/jacksoncode/jacksoncode.github.io "GitHub Open Issues")
[![](https://img.shields.io/github/issues-closed-raw/jacksoncode/jacksoncode.github.io.svg)](https://github.com/jacksoncode/jacksoncode.github.io "GitHub Closed Issues")
[![](https://img.shields.io/github/contributors/jacksoncode/jacksoncode.github.io.svg)](https://github.com/jacksoncode/jacksoncode.github.io "GitHub Contributors")

[![apm](https://img.shields.io/apm/v/amWiki.svg)](https://atom.io/packages/amWiki "Apm Version")
[![apm](https://img.shields.io/apm/dm/amWiki.svg)](https://atom.io/packages/amWiki "Apm Downloads")
[![Packagist](https://img.shields.io/packagist/l/doctrine/orm.svg)](https://github.com/jacksoncode/jacksoncode.github.io "MIT License")

### 怎么搞？

下面就来详细说一下这个徽章怎么做。

**star** 、**fork** 、**issues** 这些事类似的，下面以 **start** 为例介绍一下。
Markdown代码如下：

``[![](https://img.shields.io/github/stars/username/projectname.svg?style=social&label=Star)](projecturl "GitHub Stars")``

> 上面的代码应该很明显了，**username** 填你的``GitHub``用户名，**projectname** 为你需要显示 **star** 数量的工程，后面**projecturl** 是你的工程连接，方便别人直接点击的。

其他徽章可以查看[GitHub徽章][d8f5d914]网站

  [d8f5d914]: https://shields.io/ "GitHub徽章"
