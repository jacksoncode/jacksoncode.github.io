# 使用批处理脚本创建html文件

有的时候我们需要通过批处理创建一些日志文件、并且能够通过浏览器浏览。普通的txt文件太过单调，希望能够增加一些html样式。那么就需要通过批处理来创建html文件。

html文件本身就是个文本，通过批处理创建没啥问题。但是里面的标签怎么办呢？我们知道，批处理中的“<>”都是有意义的，那么就需要对他们转义，批处理中转义使用^符号。

比如创建一个``<html>``标签，可以这么写：
````
echo ^<html^> >>test.html
````

echo加两个>就是把这段内容换行并写入test.html文件中，如果是一个>则表示清空文本中的内容，重新写入一行。

**例子，创建一个空的html：**

````batch
echo off
set filepath=e:\test

echo ^<!DOCTYPE html^> >>%filepath%\index.html
echo ^<html lang="en"^> >>%filepath%\index.html
echo ^<head^> >>%filepath%\index.html
rem 如果html中有中文，下面的编码可以改成国标或者ANSI
echo ^<meta charset="UTF-8"^> >>%filepath%\index.html
echo ^<link rel="stylesheet" href="css/index.css"^> >>%filepath%\index.html
echo ^<script type="text/javascript" src="js/index.js"^>^</script^> >>%filepath%\index.html
echo ^<title^>Document^</title^> >>%filepath%\index.html
echo ^</head^> >>%filepath%\index.html
echo ^<body^> >>%filepath%\index.html
    
    rem 这里可以放需要展示的html内容。

echo ^</body^> >>%filepath%\index.html
echo ^</html^> >>%filepath%\index.html
````