# Github+Jekyll添加评论支持

现在，可以非常方便的使用Jekyll+Guthub制作个人静态网站。具体可以[参考Github官方教程][da70f265]。

  [da70f265]: https://help.github.com/articles/using-jekyll-as-a-static-site-generator-with-github-pages/ "Github Pages官方教程"

这里介绍怎么给文章、网页添加评论支持。

**选择评论系统（commenting system）**

主流的评论系统有Disqus, Facebook comment, IntenseDebate, Livefyre等。提供的功能和服务都大同小异，可以根据个人爱好选择。这里已[IntenseDebate](https://intensedebate.com/)为例，主要原因是其它几个要么国内访问不了，要么访问速度极慢，可以自己体验。

先去IntenseDebate注册一个账号。

**在Jekyll站点的_includes目录下创建intense debate-comments.html文件**

文件内容如下。

在``{% if page.comments != false %}``和``{% endif %}``之间就是**IntenseDebate**注册完以后得到的脚步代码。如果使用其他评论系统，代码类似。

````
  {% if page.comments != false %}
      <script>
      var idcomments_acct = 'xxxx50b9b39';
      var idcomments_post_id = '{{ page.url }}';
      var idcomments_post_url;
      </script>
      <span id="IDCommentsPostTitle" style="display:none"></span>
      <script type='text/javascript' src='https://www.intensedebate.com/js/genericCommentWrapperV2.js'></script>
  {% endif %}
````

**在站点配置文件中添加评论配置参数，方便灵活的enable/disable评论功能。**

     intensedebate_comments: true

**在post.html文件末尾后面添加代码引用intensedebate-comments.html来显示评论框。**

````
    {% if site.intensedebate_comments %}
      {% include intensedebate-comments.html %}
    {% endif %}

````
