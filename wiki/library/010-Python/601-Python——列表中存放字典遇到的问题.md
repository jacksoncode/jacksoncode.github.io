# Python——列表中存放字典遇到的问题
使用列表、字典之间的相互嵌套可以很容易的实现json数据格式，但是昨天在往列表中装入字典时遇到了问题：

````py
movieInfo = {"name":"000", "rate":"", "location":"location", "category":"category", "info_link":"", "cover_link":""}
movieList = []
for i in range(0,3):
    movieInfo["name"] = i
    movieList.append(movieInfo)
    print(movieList)
````
**输出结果：**
````py
[{'cover_link': '', 'category': 'category', 'name': 2, 'rate': '', 'location': 'location', 'info_link': ''}, {'cover_link': '', 'category': 'category', 'name': 2, 'rate': '', 'location': 'location', 'info_link': ''}, {'cover_link': '', 'category': 'category', 'name': 2, 'rate': '', 'location': 'location', 'info_link': ''}]
````

可以发现列表中的三个字典中的name值全都是2，也就是说前面插入的被后面插入的替换了。

直接使用append方法将字典添加到列表中，如果需要更改字典中的数据，那么列表中的内容也会发生改变，这是因为dict在Python里是object，不属于primitive type（即int、float、string、None、bool)。这意味着一般操控的是一个指向object（对象）的指针，而非object本身。下面是改善方法：使用copy()

````py
movieInfo = {"name":"000", "rate":"", "location":"location", "category":"category", "info_link":"", "cover_link":""}
movieList = []
for i in range(0,3):
    movieInfo["name"] = i
    movieList.append(movieInfo.copy())   # ←此处使用copy()
    print(movieList)
````

**输出结果：**
````py
[{'location': 'location', 'info_link': '', 'name': 0, 'rate': '', 'cover_link': '', 'category': 'category'}, {'location': 'location', 'info_link': '', 'name': 1, 'rate': '', 'cover_link': '', 'category': 'category'}, {'location': 'location', 'info_link': '', 'name': 2, 'rate': '', 'cover_link': '', 'category': 'category'}]
````
