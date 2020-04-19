# netstat的替代者-ss命令详解

### 为什么使用ss

值得注意的是，**几乎所有的linux系统都默认支持netstat命令，而并不一定支持ss**，从这一点来说，netstat通常还是不二选择。

但是不得不承认的是，``ss``命令更加快捷高效。``netstat``从``proc``文件系统（可参考linux中不可错过的信息宝库）获取所需要的信息，而``ss``利用``netlink``机制，与内核通信，通过TCP 协议栈中 ``tcp_diag`` 模块获取第一手的内核信息。当然这些都不是我们关注的重点，我们来看看ss命令到底如何使用。

### 查看TCP/UDP连接

使用-t（TCP）参数查看TCP连接，而使用-u(UDP)参数查看UDP socket：

````bash
$ ss -t
State       Recv-Q Send-Q                             Local Address:Port                                      Peer Address:Port
ESTAB       0      0                                  192.168.0.103:56296                                     113.107.216.82:https
ESTAB       0      0                                  192.168.0.103:56540                                     185.199.108.153:https
ESTAB       0      0                                     127.0.0.1:socks                                      127.0.0.1:44452
ESTAB       0      0                                     127.0.0.1:42150                                      127.0.0.1:9614 
````

其中``state``显示了当前连接的状态，例如结果的第一行是``ESTABLISHED``状态，``Local Address:port``代表本地连接的ip和端口号。另外,**使用-n参数显示数字形式的ip和端口**。

### 查看socket进程信息

查看到某个连接后，怎么知道是哪个进程的连接呢？使用-p（processes）即可，例如：

````bash
$ ss -tp
State       Recv-Q Send-Q                                     Local Address:Port                                                      Peer Address:Port                
ESTAB       0      0                                              127.0.0.1:42150                                                        127.0.0.1:9614                  users:(("chrome",pid=2578,fd=347))
ESTAB       0      0                                              127.0.0.1:41910                                                        127.0.0.1:9614                  users:(("chrome",pid=2578,fd=383))
````

拖动滚动条到最后可以看到，-p参数显示了这条连接的进程信息，例如，对于第一条结果，可以看到，该进程是chrome，进程id为2578，并且这条连接的文件描述符为383。

````bash
users:(("chrome",pid=2578,fd=383))
````

### 查看处于特定状态的socket

我们知道，对于TCP连接来讲，在不同的阶段它的状态不同，常见状态有

* ``ESTABLISHED``  已建立
* ``CLOSED``   已关闭
* ``LISTENING`` 正在监听
* ``FIN-WAIT-2`` 等待连接关闭
* ``TIME-WAIT`` 等待足够时间，确保服务器正常关闭该连接
* ……

这里还有很多其他状态，我们会留到介绍TCP的时候展开。如何查看处于特定状态的连接呢？例如，要查看处于LISTENING状态的连接：

````bash
$ ss -t state LISTENING
Recv-Q Send-Q                                          Local Address:Port                                                           Peer Address:Port                
0      5                                                   127.0.1.1:domain                                                                    *:*                    
0      128                                                 127.0.0.1:5941                                                                      *:*                    
0      5                                                   127.0.0.1:ipp                                                                       *:*
````

使用state选项即可查看。当然对于``LISTENING``状态，也可以使用``-l``参数。

除此之外，还有以下参数，用于查看某类状态，例如：

* ``all`` 所有类型
* ``connected``  除 ``closed`` 和 ``listen`` 状态以外已连接的状态
* ``synchronized``  除了``syn-sent`` 外的状态
 

### 查看TCP相关定时器信息

我们知道在TCP中，有很多定时器，和``netstat``一样，可以使用-o参数显示定时器相关信息：

````bash
$ ss -to
State       Recv-Q Send-Q                                     Local Address:Port                                                      Peer Address:Port                
ESTAB       0      0                                              127.0.0.1:44660                                                        127.0.0.1:socks                 timer:(keepalive,4min42sec,0)
ESTAB       0      0                                          192.168.0.103:60306                                                    203.208.41.37:https                 timer:(keepalive,9.956ms,0)
ESTAB       0      0  
````

例如上面显示的keepalive定时器剩余时间：

````bash
timer:(keepalive,9.956ms,0)
````

### 查看socket详细信息

如果想要查看连接更加详细信息呢？比如收到多少数据？上一个ACK是什么时候？``mss``是多大？拥塞窗口大小是多少？这些信息在分析理解TCP的时候非常有帮助，而查看这些信息只需要使用``-i``(information)参数即可：

````bash
$ ss -ti  #(内容很长，省略了很多信息，可执行尝试)
cubic wscale:7,7 rto:204 rtt:2.302/4.528 ato:40 mss:23488 cwnd:10 bytes_acked:1560 bytes_received:3907 segs_out:18 segs_in:20 send 816.3Mbps lastsnd:1384 lastrcv:1384 lastack:1384 pacing_rate 1632.1Mbps rcv_rtt:546 rcv_space:43690
````

由于显示的内容比较多，这里就不贴出来了，可自行尝试，里面展示了TCP很多关键信息。

### 查看socket内存使用情况

使用``-m``（memory）参数可以查看连接使用内存信息：

````bash
$ ss -tm  #只显示内存部分信息
skmem:(r0,rb374400,t0,tb46080,f0,w0,o0,bl0)
````

由于信息较多，这里只显示内存部分，括号内从左到右分别代表：

* 接收报文分配的内存
* 接收报文可分配的内存
* 发送报文分配的内存
* 发送报文可分配的内存
* socket使用的缓存
* 为将要发送的报文分配的内存
* 保存socket选项使用的内存
* 连接队列使用的内存 

### 根据IP或端口过滤socket信息

你可以使用grep命令（可参考《Linux下的文本查找技巧》）来获取你需要的信息，但是ss本身提供一些参数用来过滤信息。例如，查看本地ip为192.168.0.103的连接：

````bash
$ ss -t src 192.168.0.103
State       Recv-Q Send-Q                                     Local Address:Port                                                      Peer Address:Port                
ESTAB       0      0                                          192.168.0.103:44528                                                  185.199.109.153:https  
$ ss -t src 192.168.0.103:35418
State       Recv-Q Send-Q                                     Local Address:Port                                                      Peer Address:Port                
ESTAB       0      0                                          192.168.0.103:35418                                                  111.230.120.127:https 
````

src后面跟本地ip:port，而也可以使用dst根据远端ip来过滤信息。

同样还可以根据协议类型（端口）来过滤，例如查看https socket信息：

````bash
$ ss -t '( dport = :https or sport = :https )'
State       Recv-Q Send-Q                                     Local Address:Port                                                      Peer Address:Port                
ESTAB       0      0                                          192.168.0.103:44528                                                  185.199.109.153:https                
ESTAB       0      0                                          192.168.0.103:35418                                                  111.230.120.127:https     
$ ss -t dport = :https
State       Recv-Q Send-Q                                     Local Address:Port                                                      Peer Address:Port                
CLOSE-WAIT  32     0                                          192.168.0.103:46626                                                   123.58.182.252:https
$ ss -t sport \> :44550   #显示本地端口大于44550的连接
State       Recv-Q Send-Q                                     Local Address:Port                                                      Peer Address:Port                
ESTAB       390    0                                              127.0.0.1:46468                                                        127.0.0.1:socks                
ESTAB       0      0                                              127.0.0.1:46382                                                        127.0.0.1:socks                
ESTAB       0      0                                              127.0.0.1:46490                                                        127.0.0.1:socks
````

其中dport，指定本地协议，sport指定远端协议。

### 显示socket统计信息

使用-s(summary)查看整体统计信息。

````bash
$ ss -s
Total: 1379 (kernel 2907)
TCP:   68 (estab 58, closed 1, orphaned 0, synrecv 0, timewait 1/0), ports 0

Transport Total     IP        IPv6
*      2907      -         -        
RAW      1         0         1        
UDP      13        8         5        
TCP      67        47        20       
INET      81        55        26       
FRAG      0         0         0        
````

从统计结果中可以看到，共有67个TCP连接。

### 总结

本文介绍了ss命令一些实用的用法，为后面介绍网络编程相关内容打下基础，更多ss用法可查看帮助手册。




