# Linux文件系统

## 1. Linux文件系统概述

Linux文件系统是Linux操作系统中用于管理和存储文件的机制，它决定了文件如何组织、命名、存储、检索和访问。与Windows不同，Linux采用树形结构的文件系统，所有文件和目录都从根目录（/）开始。

### 文件系统的基本概念

- **文件**：存储数据的基本单位，可以是文本、图像、程序等
- **目录**：特殊的文件，用于组织和管理其他文件和目录
- **路径**：文件或目录在文件系统中的位置表示
- **文件描述符**：内核用于标识打开文件的整数
- **inode**：存储文件元数据的数据结构，包含文件大小、权限、所有者、时间戳等信息
- **软链接**：指向另一个文件的特殊文件（类似于Windows的快捷方式）
- **硬链接**：指向同一个inode的多个目录项

## 2. Linux文件系统结构

Linux采用单一的树形目录结构，所有分区和设备都被挂载到这个树状结构中的某个目录下。以下是Linux系统中主要的目录及其功能：

### 2.1 根目录（/）

根目录是Linux文件系统的起点，所有其他目录都从根目录派生出来。

### 2.2 主要系统目录

| 目录 | 功能描述 | 示例 |
|------|---------|------|
| /bin | 存放基本的用户命令，所有用户都可以访问 | `ls /bin` 查看常用命令 |
| /sbin | 存放系统管理命令，通常需要root权限 | `ls /sbin` 查看系统命令 |
| /etc | 存放系统配置文件 | `cat /etc/passwd` 查看用户配置 |
| /home | 普通用户的主目录，每个用户有一个子目录 | `cd /home/username` 进入用户主目录 |
| /root | root用户的主目录 | `cd /root` 进入管理员主目录 |
| /var | 存放可变数据，如日志文件、缓存、数据库等 | `ls /var/log` 查看系统日志 |
| /tmp | 临时文件目录，系统重启后通常会清空 | `ls /tmp` 查看临时文件 |
| /usr | 存放用户程序和数据，是最庞大的目录之一 | `ls /usr/bin` 查看用户命令 |
| /lib | 存放系统库文件，支持/bin和/sbin中的程序 | `ls /lib` 查看系统库 |
| /dev | 存放设备文件，Linux将所有设备都视为文件 | `ls /dev/sda` 查看硬盘设备 |
| /proc | 虚拟文件系统，反映系统状态和进程信息 | `cat /proc/cpuinfo` 查看CPU信息 |
| /sys | 虚拟文件系统，用于访问系统硬件信息 | `ls /sys/class/net` 查看网络设备 |
| /media | 可移动媒体（如U盘、光盘）的挂载点 | `ls /media` 查看挂载的媒体设备 |
| /mnt | 临时挂载其他文件系统的挂载点 | `mount /dev/sdb1 /mnt` 挂载设备 |
| /opt | 可选的应用程序软件包 | `ls /opt` 查看可选软件 |
| /boot | 存放启动Linux所需的文件 | `ls /boot` 查看启动文件 |

## 3. Linux文件系统类型

Linux支持多种文件系统类型，每种类型都有其特定的用途和特点。

### 3.1 传统Linux文件系统

- **ext2（Second Extended File System）**：早期的Linux文件系统，不支持日志功能
- **ext3（Third Extended File System）**：在ext2基础上增加了日志功能
- **ext4（Fourth Extended File System）**：ext3的改进版，是大多数Linux发行版的默认文件系统

### 3.2 现代Linux文件系统

- **XFS**：高性能64位文件系统，适用于大文件和大容量存储
- **Btrfs（B-tree File System）**：新一代Linux文件系统，支持快照、校验和等高级功能
- **ZFS**：强大的文件系统，支持大容量存储、快照、数据完整性校验等
- **F2FS（Flash-Friendly File System）**：专为闪存存储设备优化的文件系统

### 3.3 其他文件系统

- **FAT32**：Windows常用的文件系统，Linux也支持读写
- **NTFS**：Windows的高级文件系统，Linux通过ntfs-3g驱动支持
- **ISO9660**：光盘文件系统
- **NFS（Network File System）**：网络文件系统，用于在网络上共享文件
- **SMB/CIFS**：Windows网络文件共享协议，Linux通过Samba支持
- **tmpfs**：基于内存的临时文件系统，速度极快

## 4. 文件和目录的基本操作

### 4.1 查看文件和目录

```bash
# 列出当前目录下的文件和目录
ls

# 列出当前目录下的所有文件（包括隐藏文件）
ls -a

# 以长格式列出文件和目录（显示权限、所有者、大小、修改时间等）
ls -l

# 以人类可读的方式显示文件大小
ls -lh

# 按修改时间排序显示文件
ls -lt

# 递归列出目录内容
ls -R

# 查看当前所在目录
pwd
```

### 4.2 创建和删除文件/目录

```bash
# 创建空文件
touch filename

# 创建目录
mkdir directory_name

# 创建多级目录
mkdir -p path/to/directory

# 删除文件
rm filename

# 删除空目录
rmdir directory_name

# 递归删除目录及其内容（谨慎使用）
rm -r directory_name

# 强制删除（不提示）
rm -rf directory_name
```

### 4.3 复制和移动文件/目录

```bash
# 复制文件
cp source_file destination_file

# 复制目录
cp -r source_directory destination_directory

# 移动或重命名文件/目录
mv source destination

# 交互式移动（覆盖前提示）
mv -i source destination
```

### 4.4 查看文件内容

```bash
# 显示文件全部内容
cat filename

# 分页显示文件内容
less filename
more filename

# 显示文件前几行
head filename
head -n 20 filename  # 显示前20行

# 显示文件后几行
tail filename
tail -n 20 filename  # 显示后20行

# 实时显示文件更新
tail -f filename
```

### 4.5 搜索文件和内容

```bash
# 按名称搜索文件
find /path/to/search -name "filename"
find /path/to/search -name "*.txt"  # 搜索所有txt文件

# 按类型搜索
find /path/to/search -type f  # 搜索普通文件
find /path/to/search -type d  # 搜索目录

# 按大小搜索
find /path/to/search -size +10M  # 搜索大于10MB的文件

# 按修改时间搜索
find /path/to/search -mtime -7  # 搜索7天内修改过的文件

# 在文件中搜索内容
grep "search_text" filename
grep -r "search_text" /path/to/search  # 递归搜索

grep -i "search_text" filename  # 忽略大小写
grep -n "search_text" filename  # 显示行号

grep -v "search_text" filename  # 显示不包含搜索文本的行
```

## 5. 文件权限和所有权

### 5.1 文件权限表示

Linux使用9个字符表示文件或目录的权限，每3个字符为一组，分别表示所有者、所属组和其他用户的权限。

权限字符表示：
- `r`：读权限
- `w`：写权限
- `x`：执行权限（对于目录是访问权限）
- `-`：无权限

例如：`-rw-r--r--` 表示：
- 文件所有者有读写权限
- 所属组用户有读权限
- 其他用户有读权限

### 5.2 更改文件权限

```bash
# 使用符号方式更改权限
chmod u+r filename  # 给所有者添加读权限
chmod g-w filename  # 移除所属组的写权限
chmod o+x filename  # 给其他用户添加执行权限
chmod a+rwx filename  # 给所有用户添加读写执行权限

# 使用数字方式更改权限
chmod 644 filename  # 设置权限为-rw-r--r--
chmod 755 filename  # 设置权限为-rwxr-xr-x
chmod 777 filename  # 设置权限为-rwxrwxrwx
```

权限数字对应关系：
- `r` = 4
- `w` = 2
- `x` = 1
- `-` = 0

所以：
- 644 = rw- r-- r--
- 755 = rwx r-x r-x
- 777 = rwx rwx rwx

### 5.3 更改文件所有权

```bash
# 更改文件所有者
chown username filename

# 同时更改所有者和所属组
chown username:groupname filename

# 只更改所属组
chgrp groupname filename

# 递归更改目录及其内容的所有权
chown -R username:groupname directory
```

## 6. 链接文件

Linux支持两种类型的链接：硬链接和软链接（符号链接）。

### 6.1 硬链接

硬链接是指向同一个inode的多个目录项，它们共享相同的文件内容和权限。

```bash
# 创建硬链接
ln source_file link_name
```

硬链接的特点：
- 不能跨文件系统创建
- 不能链接到目录
- 删除源文件后，链接仍然有效

### 6.2 软链接（符号链接）

软链接是一个特殊的文件，它指向另一个文件或目录的路径。

```bash
# 创建软链接
ln -s source_file link_name
```

软链接的特点：
- 可以跨文件系统创建
- 可以链接到目录
- 删除源文件后，链接失效

## 7. 文件系统操作

### 7.1 挂载和卸载文件系统

```bash
# 挂载文件系统
mount /dev/sdb1 /mnt  # 将/dev/sdb1挂载到/mnt
mount -t ext4 /dev/sdb1 /mnt  # 指定文件系统类型

# 查看已挂载的文件系统
mount
df -h

# 卸载文件系统
umount /mnt
umount /dev/sdb1

# 强制卸载（当文件系统被占用时）
umount -f /mnt
```

### 7.2 自动挂载

通过编辑`/etc/fstab`文件，可以实现系统启动时自动挂载文件系统。

```bash
# 查看fstab文件
cat /etc/fstab

# 编辑fstab文件（需要root权限）
sudo vim /etc/fstab

# 添加挂载条目（示例）
/dev/sdb1  /mnt/data  ext4  defaults  0  2
```

fstab文件格式：`设备 挂载点 文件系统类型 挂载选项 dump fsck顺序`

### 7.3 检查和修复文件系统

```bash
# 检查文件系统（需要先卸载）
fsck /dev/sdb1

# 自动修复文件系统错误
fsck -y /dev/sdb1

# 检查ext系列文件系统
ext2fsck /dev/sdb1

ext4fsck /dev/sdb1
```

### 7.4 磁盘空间管理

```bash
# 查看磁盘空间使用情况
df -h

# 查看目录空间使用情况
du -h /path/to/directory

du -sh /path/to/directory  # 显示总大小

# 找出占用空间大的文件和目录
du -h / | sort -rh | head -10
```

## 8. 特殊文件和设备

### 8.1 设备文件

Linux将所有设备都视为文件，这些文件存放在`/dev`目录下。常见的设备文件包括：

- `/dev/sda`、`/dev/sdb`等：SATA、SCSI或USB硬盘设备
- `/dev/hda`、`/dev/hdb`等：IDE硬盘设备
- `/dev/cdrom`、`/dev/dvd`等：光盘设备
- `/dev/null`：空设备，写入的数据会被丢弃
- `/dev/zero`：零设备，提供无限的空字符流
- `/dev/random`、`/dev/urandom`：随机数生成器
- `/dev/tty`：终端设备

### 8.2 虚拟文件系统

Linux包含几个特殊的虚拟文件系统，它们不占用实际的磁盘空间，而是用于提供系统信息或临时存储：

- `/proc`：提供系统和进程信息的虚拟文件系统
- `/sys`：提供硬件设备信息的虚拟文件系统
- `/dev/shm`：基于内存的临时文件系统

## 9. 实践练习

### 练习1：探索Linux文件系统结构

```bash
# 从根目录开始，探索Linux文件系统
cd /
ls -l

# 查看重要系统目录的内容
ls -l /bin | head -10
ls -l /etc | head -10
ls -l /dev | head -10
ls -l /proc | head -10

# 查看系统信息文件
cat /proc/cpuinfo
cat /proc/meminfo
cat /proc/version
cat /proc/loadavg

# 查看磁盘分区和挂载信息
df -h
cat /etc/fstab
```

### 练习2：文件和目录操作

```bash
# 创建一个测试目录
mkdir ~/linux_test
cd ~/linux_test

# 创建一些测试文件
touch file1.txt file2.txt
mkdir subdir

# 查看当前目录内容
ls -l

# 向文件中写入内容
echo "Hello Linux" > file1.txt
echo "Linux File System" > file2.txt

# 查看文件内容
cat file1.txt
cat file2.txt

# 复制和移动文件
cp file1.txt file1_copy.txt
mv file2.txt subdir/

# 创建链接
ln file1.txt file1_hardlink
ln -s file1.txt file1_symlink
ln -s subdir subdir_symlink

# 查看链接信息
ls -l

# 更改文件权限
chmod 600 file1.txt
ls -l file1.txt

# 查看磁盘使用情况
du -sh .
```

### 练习3：搜索和查找

```bash
# 在当前目录及其子目录中搜索包含特定内容的文件
grep -r "Linux" .

# 查找所有.txt文件
find . -name "*.txt"

# 查找最近24小时内修改过的文件
find . -mtime -1

# 查找大小超过1KB的文件
find . -size +1k
```

通过本章的学习，我们了解了Linux文件系统的基本概念、结构、类型和操作方法。掌握Linux文件系统对于有效地管理和使用Linux系统至关重要。在后续章节中，我们将继续深入学习Linux的各种命令和功能。