# GitHub-fork的仓库与原仓库保持同步
要让fork的仓库与原仓库保持同步，主要有两种方法：

### 方式一：GitHub网页操作：反向Pull Request

1. 打开pull request，点新建pull request。

  ![](assets/050/600-1573964987819.png)

2. 左边选择自己的仓库，右边选择原仓库。

  ![](assets/050/600-1573965120714.png)

3. 此时会出现forked仓库和原仓库的区别，点新建pull request。
4. 回到自己仓库，merged 这个request就可以了。


### 方式二：本地Git操作：直接Pull

1. 查看现有的远程仓库：
````git
$ git remote -v
origin  https://github.com/YOUR_USERNAME/YOUR_FORK.git (fetch)
origin  https://github.com/YOUR_USERNAME/YOUR_FORK.git (push)
````
2. 添加指向原仓库的upstream：
````
$ git remote add upstream https://github.com/ORIGINAL_OWNER/ORIGINAL_REPOSITORY.git
````
3. 查看origin和upstream
````
$ git remote -v
origin    https://github.com/YOUR_USERNAME/YOUR_FORK.git (fetch)
origin    https://github.com/YOUR_USERNAME/YOUR_FORK.git (push)
upstream  https://github.com/ORIGINAL_OWNER/ORIGINAL_REPOSITORY.git (fetch)
upstream  https://github.com/ORIGINAL_OWNER/ORIGINAL_REPOSITORY.git (push)
````
4. 直接从原仓库的master分支拉取代码并直接合并代码，其中pull=fetch+merge.
````
git pull upstream master
````