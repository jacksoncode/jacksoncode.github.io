# 网络命令之-netstat

### 查看某个端口是否被占用

如果你遇到“Address already in use”的错误，那么你就需要好好看看是不是端口已经被占用了。**-a（all）参数用于列出所有监听和非监听状态的连接**。

````bash
$ netstat -a|grep 6379
tcp        0      0 *:6379                  *:*                     LISTEN     
tcp6       0      0 [::]:6379               [::]:*                  LISTEN 
````

这里我们可以看到，有一个tcp连接使用了6379端口，并且当前处于LISTEN状态，这些状态信息对于分析网络连接问题非常有帮助，我们将会在后面的文章中看到它们大放异彩。

当然你也可以使用lsof命令中的方法来查看。关于grep的用法，也可以参考《grep命令详解》，这里就不展开了，我们后面会在很多地方用到。

### 查找占用端口的进程

前面虽然知道已经有进程使用了6379端口，但是不知道是哪个进程，因此, **为了知道进程信息，需要使用-p(program)参数**：

````bash
$ netstat -ap|grep 6379
tcp        0      0 *:6379                  *:*                     LISTEN      10011/redis-server 
tcp6       0      0 [::]:6379               [::]:*                  LISTEN      10011/redis-server
````

这个时候就可以看到是进程id为10011的redis-server进程占用了6379端口，至此要杀要剐就随你便了。

### 查看指定协议的连接

我们都知道，除了TCP之外还有UDP，如果我们想查看指定类型的连接呢？

````bash
$ netstat -at   #-t,查看tcp连接
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 192.168.0.103:42468     113.96.233.139:https    ESTABLISHED
tcp        0      0 192.168.0.103:59326     123.58.182.252:https    TIME_WAIT  
tcp        0      0 192.168.0.103:59328     123.58.182.252:https    TIME_WAIT  
（未显示完全）
````

以此种方式，可以看到所有的TCP连接，而对于UDP连接，只需要使用-u(UDP):

````bash
$ netstat -au
udp        0      0 *:36305                 *:*
udp        0      0 127.0.1.1:domain        *:*
udp        0      0 *:bootpc                *:*
udp        0      0 *:ipp                   *:*

(未显示完全))
````

当然了，这两个参数也是可以一起用的。

除此之外，还可以使用-4或-6来指定查看ipv4还是ipv6的连接.

### 查看处于监听状态的连接

对于还没有建立完整连接的服务器来说，它启动后正常的状态是LISTEN状态，**如果只想查看处于该状态的连接，则可以使用-l（LISTEN）参数**：

````bash
$ netstat -l
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 127.0.1.1:domain        *:*                     LISTEN
tcp        0      0 localhost:5941          *:*                     LISTEN
tcp        0      0 localhost:ipp           *:*                     LISTEN
tcp        0      0 localhost:socks         *:*                     LISTEN
tcp        0      0 *:6379                  *:*                     LISTEN
（未显示完全）
````

这个时候记得**不要带上-a参数**，它会列出所有。

而你如果要查看其他状态的连接，只需要结合grep使用即可，例如，查看ESTABLISHED状态的连接：

````bash
$ netstat -anp |grep ESTAB
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp        0      0 192.168.0.103:42468     113.96.233.139:443      ESTABLISHED 2613/chrome     
tcp        0      0 192.168.0.103:38024     108.177.125.188:443     ESTABLISHED 2613/chrome
````

### 不解析主机，端口等信息

不知道你有没有发现，在执行前面的命令的时候，速度很慢，让你一度怀疑是不是自己电脑太卡了。实际上，你观察前面的输出结果就会发现，很多连接的主机名和端口对应的应用都解析出来了，例如：

````bash
123.58.182.252:https
````

所以慢是因为它需要做解析，使用``-n``（numeric）参数就可以快速显示原始数字端口或地址了：

````bash
$ netstat -anp
````

一定要自己尝试一下奥！

### 持续输出连接信息

你在定位网络相关问题的时候，总不想执行一次观察一次吧？能不能自动反复执行查看呢？当然可以啦！可以使用-c（continuous）参数：

````bash
$ netstat -npc
````

这样，它就会每隔一秒执行一次。当然你完全可以使用watch命令，关于watch命令的使用可以参考《解放你的双手-watch》。

### 查看用户和连接的iNode

这条连接是哪个用户建立的呢？unix下一切皆文件，那么这个连接的iNode是多少呢？借助-e(extend)参数可以看到这些信息：

````bash
$ netstat -ent
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       User       Inode      
tcp        0      0 192.168.0.103:42468     113.96.233.139:443      ESTABLISHED 1000       134891     
tcp        0      0 192.168.0.103:46556     121.9.246.106:443       TIME_WAIT   0          0          
````

可以看到在使用-e参数后，多了最后两列，分别是user和Inode。而使用id命令可以知道该user到底是谁：

````bash
$ id 1000
uid=1000(hyb) gid=1000(hyb) groups=1000(hyb),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),113(lpadmin),128(sambashare)
````

### 查看连接相关的定时器

使用-o可以查看和连接相的定时器信息:

````bash
$ netstat -nto
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       Timer
tcp        0      0 192.168.0.103:42468     113.96.233.139:443      ESTABLISHED keepalive (18.69/0/0)
tcp        1      1 192.168.0.103:43718     113.96.233.139:443      LAST_ACK    on (19.97/7/0)
tcp        0      0 192.168.0.103:38024     108.177.125.188:443     ESTABLISHED keepalive (34.76/0/0)
tcp        0      0 192.168.0.103:60362     123.58.182.252:443      TIME_WAIT   timewait (6.70/0/0)
tcp6       0      0 127.0.0.1:9614          127.0.0.1:59736         ESTABLISHED off (0.00/0/0)
````

最后的timer列相关字段含义如下：

* ``keepalive`` keepalive的时间计时
* ``on`` 重发的时间计时
* ``off`` 没有时间计时
* ``timewait`` 等待时间计时

关于定时器的含义，需要对TCP协议有较多理解，这里就不展开了。查看数据包统计信息各种协议的数据包的收发情况如何呢？连接数量如何呢是用``-s``(statistics)参数可以查看：

````bash
$ netstat -s
（仅显示了TCP协议的结果）
Tcp:
    3067 active connections openings
    1 passive connection openings
    173 failed connection attempts
    587 connection resets received
    10 connections established
    657576 segments received
    456349 segments send out
    2700 segments retransmited
    16 bad segments received.
    1321 resets sent
````

### 查看路由信息

使用``-r``(route)参数可以查看路由相关信息，例如：

````bash
$ netstat -r
Kernel IP routing table
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
default         192.168.0.1     0.0.0.0         UG        0 0          0 wlp3s0
link-local      *               255.255.0.0     U         0 0          0 wlp3s0
192.168.0.0     *               255.255.255.0   U         0 0          0 wlp3s0
````

当然你也可以借助``route``命令完成这样简单的工作。

### 总结

``netstat``命令是我们定位网络相关问题的利器，如果你还不会使用，那么最好花几分钟学习一下。``netstat``更详细的字段解释可以参考其手册。