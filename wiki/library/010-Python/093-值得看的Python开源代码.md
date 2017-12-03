# 值得看的Python开源代码

### 知乎-刘志军

个人推荐看 Kenneth Reitz 大神的成名之作 Requests，感受一下什么是真正的Pythonic代码，什么是 Keep It Simple and Stupid

有网友已经整理了一份Requests源码阅读清单，内容幽默诙谐有趣，推荐看一看

*   [Requests v0.2.0 Birth!](https://link.zhihu.com/?target=https%3A//github.com/wangshunping/read_requests/blob/master/doc/Requests_v0.2.0.md) 2016-03-14
*   [Requests v0.3.0 Be frinendly](https://link.zhihu.com/?target=https%3A//github.com/wangshunping/read_requests/blob/master/doc/Requests_v0.3.0.md) 2016-03-16
*   [Requests v0.4.0 Amazing tour ](https://link.zhihu.com/?target=https%3A//github.com/wangshunping/read_requests/blob/master/doc/Requests_v0.4.0.md)2016-03-17
*   [Requests v0.5.0 Context Manager ](https://link.zhihu.com/?target=https%3A//github.com/wangshunping/read_requests/blob/master/doc/Requests_v0.5.0.md)2016-03-18
*   [Reuqests v0.6.0 Captain Hook! ](https://link.zhihu.com/?target=https%3A//github.com/wangshunping/read_requests/blob/master/doc/Requests_v0.6.0.md)2016-03-19
*   [Reuqests v0.7.0 awesome gevent](https://link.zhihu.com/?target=https%3A//github.com/wangshunping/read_requests/blob/master/doc/Requests_v0.7.0.md) 2016-03-22
*   [Reuqests v0.8.0 ](https://link.zhihu.com/?target=https%3A//github.com/wangshunping/read_requests/blob/master/doc/Requests_v0.8.0.md)2016-03-??

還有老外分享的一個PPT，手把手教你如何阅读源码，也是拿Requests作为参考例子 [<span class="invisible">https://www.</span><span class="visible">slideshare.net/onceupon</span><span class="invisible">atimeforever/lets-read-code</span><span class="ellipsis"></span>](https://link.zhihu.com/?target=https%3A//www.slideshare.net/onceuponatimeforever/lets-read-code) ，没有梯子的在这里下载 [<span class="invisible">https://</span><span class="visible">pan.baidu.com/s/1i5ggKj</span><span class="invisible">r</span><span class="ellipsis"></span>](https://link.zhihu.com/?target=https%3A//pan.baidu.com/s/1i5ggKjr)

下面是Kenneth Reitz大神自己推薦的源碼閱讀清單，來源：[Reading Great Code](https://link.zhihu.com/?target=http%3A//python-guide-pt-br.readthedocs.io/en/latest/writing/reading/)

*   [Howdoi](https://link.zhihu.com/?target=https%3A//github.com/gleitz/howdoi) Howdoi is a code search tool, written in Python
*   [Flask](https://link.zhihu.com/?target=https%3A//github.com/mitsuhiko/flask) Flask is a microframework for Python based on Werkzeug and Jinja2. It’s intended for getting started very quickly and was developed with best intentions in mind.
*   [Diamond](https://link.zhihu.com/?target=https%3A//github.com/python-diamond/Diamond) Diamond is a python daemon that collects metrics and publishes them to Graphite or other backends. It is capable of collecting cpu, memory, network, i/o, load and disk metrics. Additionally, it features an API for implementing custom collectors for gathering metrics from almost any source.
*   [Werkzeug](https://link.zhihu.com/?target=https%3A//github.com/mitsuhiko/werkzeug) Werkzeug started as simple collection of various utilities for WSGI applications and has become one of the most advanced WSGI utility modules. It includes a powerful debugger, full-featured request and response objects, HTTP utilities to handle entity tags, cache control headers, HTTP dates, cookie handling, file uploads, a powerful URL routing system and a bunch of community-contributed addon modules.
*   [Requests](https://link.zhihu.com/?target=https%3A//github.com/kennethreitz/requests) Requests is an Apache2 Licensed HTTP library, written in Python, for human beings.
*   [Tablib](https://link.zhihu.com/?target=https%3A//github.com/kennethreitz/tablib) Tablib is a format-agnostic tabular dataset library, written in Python.</span>

#### 知乎-董伟明

推荐阅读我的专栏文章：[教你阅读Python开源项目代码 - Python之美 - 知乎专栏](https://zhuanlan.zhihu.com/p/22275595?refer=python-cn)。 我摘录一部分：

**我个人的喜好**

和工作中看别人代码差不多，基本每个人、每个项目、每个团队都有自己写代码的风格，比如变量命名风格、某些语言特性使用方式、代码规范要求、目录风格等，其实开源项目的作者也是一样。看代码，如看人（团队）。 首先介绍下我的喜好（排名分先后）：

1. [kennethreitz](https://link.zhihu.com/?target=https%3A//github.com/kennethreitz)。requests和python-guide作者。他还有一个非常励志的故事，有兴趣的可以看 [谁说程序员不是潜力股？](https://zhuanlan.zhihu.com/p/22332669)

2. [mitsuhiko](https://link.zhihu.com/?target=https%3A//github.com/mitsuhiko)。flask、Jinja2、werkzeug和flask-sqlalchemy作者。

3. [sigmavirus24](https://link.zhihu.com/?target=https%3A//github.com/sigmavirus24)。flake8、pycodestyle（原pep8）、requests、urllib3等项目的主要贡献者和维护者。

4. [ask](https://link.zhihu.com/?target=https%3A//github.com/ask)。Celery及相关依赖的作者。

5. [ajdavis](https://link.zhihu.com/?target=https%3A//github.com/ajdavis)。mongo-python-driver（pymongo）、tornado等项目的主要贡献者。

6. [bitprophet](https://link.zhihu.com/?target=https%3A//github.com/bitprophet)。fabric、paramiko（Python的ssh库）作者。

前2个是公认的Python领域代码写的最好的、最有创意的工程师。

**初学者推荐阅读项目**

初学者可以先阅读一些代码量比较少的，最好是单文件的项目：

1. [GitHub - kennethreitz/pip-pop: Tools for managing requirements files.](https://link.zhihu.com/?target=https%3A//github.com/kennethreitz/pip-pop)

2. [GitHub - kennethreitz/envoy: Python Subprocesses for Humans™.](https://link.zhihu.com/?target=https%3A//github.com/kennethreitz/envoy)

3. [GitHub - kennethreitz/records: SQL for Humans™](https://link.zhihu.com/?target=https%3A//github.com/kennethreitz/records)

4. [GitHub - mitsuhiko/pluginbase: A simple but flexible plugin system for Python.](https://link.zhihu.com/?target=https%3A//github.com/mitsuhiko/pluginbase)

5. [GitHub - mitsuhiko/pipsi: pip script installer](https://link.zhihu.com/?target=https%3A//github.com/mitsuhiko/pipsi/)

6. [GitHub - mitsuhiko/unp: Unpacks things.](https://link.zhihu.com/?target=https%3A//github.com/mitsuhiko/unp)

7. [GitHub - chrisallenlane/cheat](https://link.zhihu.com/?target=https%3A//github.com/chrisallenlane/cheat/)

8. [GitHub - jek/blinker: A fast Python in-process signal/event dispatching system.](https://link.zhihu.com/?target=https%3A//github.com/jek/blinker)

9. [GitHub - mitsuhiko/platter: A useful helper for wheel deployments.](https://link.zhihu.com/?target=https%3A//github.com/mitsuhiko/platter/)

10. [GitHub - kennethreitz/tablib: Python Module for Tabular Datasets in XLS, CSV, JSON, YAML, &amp;amp;amp;amp;c.](https://link.zhihu.com/?target=https%3A//github.com/kennethreitz/tablib)

看代码主要是了解别人写代码的方式，语法实践这些内容。看完之后，你可以针对这些项目能解决的问题自己写个项目，写完之后和上述项目去对比一下，看看哪些方面做的不好。

**进阶阅读项目**

进阶的时候就要阅读一些相对复杂的项目，它们能帮助你提升Python编程技巧：

1. [faif/python-patterns](https://link.zhihu.com/?target=https%3A//github.com/faif/python-patterns)。使用Python实现一些设计模式的例子。

2. [pallets/werkzeug](https://link.zhihu.com/?target=https%3A//github.com/pallets/werkzeug)。flask的WSGI工具集。其中包含了实现非常好的LocalProxy、cached_property、import_string、find_modules、TypeConversionDict等。

3. [bottlepy/bottle](https://link.zhihu.com/?target=https%3A//github.com/bottlepy/bottle)。阅读一个Web框架对Web开发就会有更深刻的理解，flask太大，bottle就4k多行，当然如果你有毅力和兴趣直接看flask是最好了的。

4. [msiemens/tinydb](https://link.zhihu.com/?target=https%3A//github.com/msiemens/tinydb)。了解用Python实现数据库。

5. [coleifer/peewee](https://link.zhihu.com/?target=https%3A//github.com/coleifer/peewee)。了解ORM的实现。

6. [pallets/click](https://link.zhihu.com/?target=https%3A//github.com/pallets/click)。click已经内置于在flask 0.11里，提供命令行功能，值得阅读。

7. [mitsuhiko/flask-sqlalchemy](https://link.zhihu.com/?target=https%3A//github.com/mitsuhiko/flask-sqlalchemy)。了解一个flask插件是怎么实现的。

除此之外Web开发者可以阅读一些相关的项目：

1. [runscope/httpbin](https://link.zhihu.com/?target=https%3A//github.com/Runscope/httpbin)。使用flask，网站是[httpbin(1): HTTP Client Testing Service](https://link.zhihu.com/?target=http%3A//httpbin.org/)。

2. [jahaja/psdash](https://link.zhihu.com/?target=https%3A//github.com/Jahaja/psdash)。使用flask和psutils的获取Linux系统信息的面板应用。

3. [pallets/flask-website](https://link.zhihu.com/?target=https%3A//github.com/pallets/flask-website)。 flask官方网站应用。

4. [pypa/warehouse](https://link.zhihu.com/?target=https%3A//github.com/pypa/warehouse)。如果你使用pyramid，这个[新版的PYPI网站](https://link.zhihu.com/?target=https%3A//pypi.org/)，可以帮助你理解很多。

当然，2个学习flask重要的资源必须爆一爆：

1. [GitHub - realpython/discover-flask: Full Stack Web Development with Flask](https://link.zhihu.com/?target=https%3A//github.com/realpython/discover-flask)。

2. [The Flask Mega-Tutorial](https://link.zhihu.com/?target=http%3A//blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)。 这个就是《Flask Web开发：基于Python的Web应用开发实战》的原始博客。

**500lines**

推荐一个非常厉害的项目 [GitHub - aosabook/500lines: 500 Lines or Less](https://link.zhihu.com/?target=https%3A//github.com/aosabook/500lines), 它里面包含了22个由该领域的专家完成，用不到500行的代码实现一个特定功能的子项目。连Guido van Rossum都亲自来写基于asyncio爬虫了，Nick Coghlan、ajdavis也出场了。更具体的介绍可以看[Python 的练手项目有哪些值得推荐？ - 小小搬运工的回答](https://www.zhihu.com/question/29372574/answer/88624507)。

**欢迎关注本人的微信公众号获取更多Python相关的内容（也可以直接搜索「Python之美」）：**

#### 知乎-码云

**谢邀，已经有很多优秀的答案了，在才补充几个Python开源项目作为补充，供大家交流学习。**

**Ps：答案显示违规了，应该是那个爬虫网站的问题，敏感词，特删除重发。**

**1. 项目名称： **Openerp-China

**项目简介：**OpenERP中国版，降低OpenERP中国社区项目的参与门槛。

**参与开发**

*   在openerp-china项目上点击fork按钮，形成你自己的项目；
*   clone你自己的项目到本地；
*   添加 osbzr 的 remote 只需要做一次 git remote add osbzr；
*   拉主干代码到本地 git fetch osbzr；
*   合并 主干代码到本地 git merge osbzr/master；
*   推送本地合并后的代码到 fork 项目 git push origin master；
*   向主项目提交合并请求。

**项目地址：**[开阖软件 Jeff Wang/openerp-china - 码云](https://link.zhihu.com/?target=https%3A//gitee.com/osbzr/openerp-china)

**2. 项目名称：**CheungSSH

**项目简介：**Linux自动化运维堡垒机 国产中文系统。

**项目地址：**[张其川/CheungSSH - 码云](https://link.zhihu.com/?target=https%3A//gitee.com/CheungSSH_OSC/CheungSSH)

**3. 项目名称：**Lepus

**项目简介：**简洁、直观、强大的开源企业级数据库监控系统，MySQL/Oracle/MongoDB/Redis一站式监控，让数据库监控更简单。支持邮件告警、短信告警、AWR性能报告、慢查询分析等专业功能。

**项目地址：**[灰太狼。/Lepus - 码云](https://link.zhihu.com/?target=https%3A//git.oschina.net/ruzuojun/Lepus)

**4. 项目名称：**Quicklib

**项目简介：**期货、A股等国内程序化python交易框架和工具.

**项目地址：**[量化林/Quicklib - 码云](https://link.zhihu.com/?target=https%3A//git.oschina.net/quicklib/Quicklib)

**5. 项目名称：**RQAlpha

**项目简介：**

*   从数据获取、算法交易、回测引擎，实盘模拟，实盘交易到数据分析，为程序化交易者提供了全套解决方案。
*   灵活的配置方式，强大的扩展性，用户可以非常容易地定制专属于自己的程序化交易系统。
*   所有的策略都可以直接在 [Ricequant](https://link.zhihu.com/?target=https%3A//www.ricequant.com/algorithms) 上进行回测和实盘模拟，并且可以通过微信和邮件实时推送您的交易信号。
*   一个开放的量化算法交易社区，为程序化交易者提供免费的回测和实盘模拟环境，并且会不间断举行实盘资金投入的量化比赛。

**特点：**

*   易于使用，让您集中于策略的开发，一行简单的命令就可以执行您的策略；
*   完善的文档，您可以直接访问 [RQAlpha 文档](https://link.zhihu.com/?target=http%3A//rqalpha.readthedocs.io/zh_CN/latest/) 或者 [Ricequant 文档](https://link.zhihu.com/?target=https%3A//www.ricequant.com/api/python/chn) 来获取您需要的信息。
*   活跃的社区，您可以通过访问 [Ricequant 社区](https://link.zhihu.com/?target=https%3A//www.ricequant.com/community/category/all/) 获取和询问有关 RQAlpha 的一切问题，有很多优秀的童鞋会解答您的问题。
*   稳定的环境，每天都有会大量的算法交易在 Ricequant 上运行，无论是 RQAlpha，还是数据，我们能会做到问题秒处理，秒解决。
*   灵活的配置，您可以使用多种方式来配置和运行策略，只需简单的配置就可以构建适合自己的交易系统；
*   强大的扩展性，开发者可以基于我们提供的 Mod Hook 接口来进行扩展。

**项目地址：**[Ricequant/RQAlpha - 码云](https://link.zhihu.com/?target=https%3A//gitee.com/Ricequant/rqalpha)

> 来**码云** [<span class="invisible">http://</span><span class="visible">Gitee.com</span><span class="invisible"></span>](https://link.zhihu.com/?target=http%3A//Gitee.com)
> 发现更多优质**开源项目：**[最新推荐 - 码云 - 开源中国](https://link.zhihu.com/?target=https%3A//gitee.com/explore/recommend%3Fzhihu)
> 让**团队**流畅、高效开发：[码云企业版 - 码云 - 开源中国](https://link.zhihu.com/?target=https%3A//gitee.com/enterprises%3Fzhihu)
