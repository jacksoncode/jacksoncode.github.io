# 8.3 fdisk命令详解

## 1. 命令概述

fdisk（fixed disk）命令是Linux系统中用于管理磁盘分区的强大工具。它允许用户创建、删除、修改和查看硬盘分区表，是系统管理员配置存储设备的必备工具。fdisk主要用于MBR（Master Boot Record）分区表格式，但也支持GPT（GUID Partition Table）分区表的基本操作。

### 1.1 功能特点
- 创建、删除、修改磁盘分区
- 显示磁盘分区表信息
- 设置分区类型
- 激活或禁用分区引导标志
- 支持MBR和GPT分区表
- 调整分区大小
- 复制分区表
- 验证分区表

### 1.2 应用场景
- 新硬盘初始化和分区
- 调整现有磁盘的分区结构
- 修复损坏的分区表
- 创建多引导系统
- 为不同用途（如系统、数据、交换空间）划分磁盘空间
- 在救援模式下修复分区问题

## 2. 语法格式

fdisk命令的基本语法格式如下：

```bash
# 基本语法
$ sudo fdisk [选项] <设备>
```

### 2.1 语法说明
- **sudo**：fdisk命令需要管理员权限才能执行
- **fdisk**：命令名称，用于管理磁盘分区
- **选项**：控制命令行为的参数
- **设备**：指定要操作的磁盘设备，通常是`/dev/sda`、`/dev/sdb`等格式

> **警告**：fdisk命令直接操作磁盘分区表，错误使用可能导致数据丢失。在使用前，请确保备份重要数据，并谨慎操作。

## 3. 常用选项

fdisk命令提供了多种命令行选项和交互式命令。以下是常用的命令行选项：

### 3.1 命令行选项列表

| 选项 | 功能说明 |
|------|----------|
| `-l` | 列出所有磁盘的分区表信息 |
| `-s <分区>` | 显示指定分区的大小（以块为单位） |
| `-u` | 以扇区为单位显示分区表信息 |
| `-b <大小>` | 指定扇区大小（512、1024、2048或4096字节） |
| `-C <柱面数>` | 指定磁盘的柱面数 |
| `-H <磁头数>` | 指定磁盘的磁头数 |
| `-S <扇区数>` | 指定每个磁道的扇区数 |

### 3.2 交互式命令列表

进入fdisk交互式模式后，可以使用以下命令进行分区操作：

| 命令 | 功能说明 |
|------|----------|
| `m` | 显示帮助菜单 |
| `p` | 显示当前磁盘的分区表 |
| `n` | 创建新分区 |
| `d` | 删除分区 |
| `t` | 更改分区类型 |
| `w` | 保存更改并退出 |
| `q` | 放弃更改并退出 |
| `a` | 设置或取消分区的引导标志 |
| `l` | 列出所有支持的分区类型 |
| `c` | 切换DOS兼容性标志 |
| `u` | 切换显示单位（柱面/扇区） |
| `v` | 验证分区表 |
| `s` | 创建指定分区的Sun disklabel |
| `i` | 显示指定分区的详细信息 |
| `x` | 进入专家模式 |

### 3.3 选项详细解释

- **`-l`**: 列出所有磁盘的分区表信息，包括磁盘大小、分区数量、分区类型等详细信息。如果指定了设备，则只显示该设备的分区表。

- **`-s <分区>`**: 显示指定分区的大小，以块为单位（通常为1024字节）。

- **`-u`**: 以扇区为单位显示分区表信息，而不是默认的柱面单位，这在现代磁盘上更精确。

- **`p`**: 在交互式模式下，显示当前磁盘的分区表信息，包括分区号、起始位置、结束位置、大小和类型。

- **`n`**: 在交互式模式下，创建新分区。系统会提示选择分区类型（主分区或扩展分区）、分区号、起始扇区和结束扇区。

- **`d`**: 在交互式模式下，删除指定的分区。系统会提示输入要删除的分区号。

- **`t`**: 在交互式模式下，更改指定分区的类型。系统会提示输入分区号和分区类型代码。

- **`w`**: 在交互式模式下，保存所有更改并退出fdisk命令。

- **`q`**: 在交互式模式下，放弃所有更改并退出fdisk命令，不会保存任何修改。

- **`a`**: 在交互式模式下，设置或取消分区的引导标志，用于指定可引导的分区。

- **`l`**: 在交互式模式下，列出所有支持的分区类型及其对应的十六进制代码。

## 4. 常用示例

### 4.1 查看所有磁盘分区信息

显示系统中所有磁盘的分区表信息：

```bash
# 查看所有磁盘分区信息
$ sudo fdisk -l

Disk /dev/sda: 500.1 GB, 500107862016 bytes
255 heads, 63 sectors/track, 60801 cylinders, total 976773168 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disk identifier: 0x0003b4b5

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *        2048      499711      248832   83  Linux
/dev/sda2          501758   976771071   488134657    5  Extended
/dev/sda5          501760   976771071   488134656   8e  Linux LVM

Disk /dev/sdb: 1000.2 GB, 1000204886016 bytes
255 heads, 63 sectors/track, 121601 cylinders, total 1953525168 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disk identifier: 0x00000000

   Device Boot      Start         End      Blocks   Id  System
/dev/sdb1            2048  1953521663   976759808   83  Linux
```

### 4.2 查看特定磁盘分区信息

显示特定磁盘的分区表信息：

```bash
# 查看/dev/sda磁盘的分区表信息
$ sudo fdisk -l /dev/sda
```

### 4.3 进入fdisk交互式模式

进入指定磁盘的fdisk交互式操作模式：

```bash
# 进入/dev/sdb磁盘的fdisk交互式模式
$ sudo fdisk /dev/sdb

Welcome to fdisk (util-linux 2.27.1).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Command (m for help):
```

### 4.4 创建新分区

在交互式模式下创建新分区的步骤：

```bash
# 进入fdisk交互式模式
$ sudo fdisk /dev/sdb

Command (m for help): n  # 创建新分区
Partition type
   p   primary (0 primary, 0 extended, 4 free)
   e   extended (container for logical partitions)
Select (default p): p  # 创建主分区
Partition number (1-4, default 1): 1  # 分区号
First sector (2048-1953525167, default 2048):  # 默认起始扇区
Last sector, +sectors or +size{K,M,G,T,P} (2048-1953525167, default 1953525167): +100G  # 设置分区大小为100GB

Created a new partition 1 of type 'Linux' and of size 100 GiB.

Command (m for help): p  # 查看新创建的分区

Disk /dev/sdb: 1000.2 GB, 1000204886016 bytes
255 heads, 63 sectors/track, 121601 cylinders, total 1953525168 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disk identifier: 0x00000000

   Device Boot      Start         End      Blocks   Id  System
/dev/sdb1            2048   209717247   104857600   83  Linux

Command (m for help): w  # 保存并退出
The partition table has been altered!

Calling ioctl() to re-read partition table.
Syncing disks.
```

### 4.5 删除分区

在交互式模式下删除分区的步骤：

```bash
# 进入fdisk交互式模式
$ sudo fdisk /dev/sdb

Command (m for help): p  # 查看当前分区表

Disk /dev/sdb: 1000.2 GB, 1000204886016 bytes
255 heads, 63 sectors/track, 121601 cylinders, total 1953525168 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disk identifier: 0x00000000

   Device Boot      Start         End      Blocks   Id  System
/dev/sdb1            2048   209717247   104857600   83  Linux

Command (m for help): d  # 删除分区
Selected partition 1
Partition 1 is deleted

Command (m for help): p  # 确认分区已删除

Disk /dev/sdb: 1000.2 GB, 1000204886016 bytes
255 heads, 63 sectors/track, 121601 cylinders, total 1953525168 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disk identifier: 0x00000000

No partitions defined.

Command (m for help): w  # 保存并退出
The partition table has been altered!

Calling ioctl() to re-read partition table.
Syncing disks.
```

### 4.6 更改分区类型

在交互式模式下更改分区类型的步骤：

```bash
# 进入fdisk交互式模式
$ sudo fdisk /dev/sdb

Command (m for help): p  # 查看当前分区表

Disk /dev/sdb: 1000.2 GB, 1000204886016 bytes
255 heads, 63 sectors/track, 121601 cylinders, total 1953525168 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disk identifier: 0x00000000

   Device Boot      Start         End      Blocks   Id  System
/dev/sdb1            2048   209717247   104857600   83  Linux

Command (m for help): t  # 更改分区类型
Selected partition 1
Partition type (type L to list all types): L  # 列出所有分区类型

 0  Empty           24  NEC DOS         81  Minix / old Lin bf  Solaris        
 1  FAT12           27  Hidden NTFS Win 82  Linux swap / So c1  DRDOS/sec (FAT- 
 2  XENIX root      39  Plan 9          83  Linux           c4  DRDOS/sec (FAT- 
 3  XENIX usr       3c  PartitionMagic  84  OS/2 hidden C:  c6  DRDOS/sec (FAT- 
 4  FAT16 <32M      40  Venix 80286     85  Linux extended  c7  Syrinx         
 5  Extended        41  PPC PReP Boot   86  NTFS volume set da  Non-FS data    
 6  FAT16           42  SFS             87  NTFS volume set db  CP/M / CTOS / .
 7  HPFS/NTFS/exFAT 4d  QNX4.x          88  Linux plaintext de  Dell Utility   
 8  AIX             4e  QNX4.x 2nd part 89  Linux raid auto df  BootIt         
 9  AIX bootable    4f  QNX4.x 3rd part 8a  OS/2 Boot Manag e1  DOS access     
 a  OS/2 Boot Manag 50  OnTrack DM      8b  W95 FAT32       e2  DOS secondary  
 b  W95 FAT32       51  OnTrack DM6 Aux 8c  W95 FAT32 (LBA) e3  DOS R/O        
 c  W95 FAT32 (LBA) 52  CP/M            8e  Linux LVM       e4  SpeedStor      
 e  W95 FAT16 (LBA) 53  OnTrack DM6 Aux 93  Amoeba          e5  CRC32 partition
 f  W95 Ext'd (LBA) 54  OnTrackDM6      94  Amoeba BBT      e6  DOS access     
10  OPUS            55  EZ-Drive        9f  BSD/OS          e7  GPT            
11  Hidden FAT12    56  Golden Bow      a0  IBM Thinkpad hi eb  BeOS fs        
12  Compaq diagnost 5c  Priam Edisk     a5  FreeBSD         ee  GPT            
14  Hidden FAT16 <3 61  SpeedStor       a6  OpenBSD         ef  EFI (FAT-12/16/
16  Hidden FAT16    63  GNU HURD or Sys a7  NeXTSTEP        f0  Linux/PA-RISC b
17  Hidden HPFS/NTF 64  Novell Netware  a8  Darwin UFS      f1  SpeedStor      
18  AST SmartSleep  65  Novell Netware  a9  NetBSD          f4  SpeedStor      
1b  Hidden W95 FAT3 70  DiskSecure Mult b7  BSDI fs         f2  DOS secondary  
1c  Hidden W95 FAT3 75  PC/IX           b8  BSDI swap       fb  VMware VMFS    
1e  Hidden W95 FAT1 80  Old Minix       bb  Boot Wizard hid fc  VMware VMKCORE 

Partition type (type L to list all types): 8e  # 选择Linux LVM类型
Changed type of partition 'Linux' to 'Linux LVM'.

Command (m for help): p  # 确认分区类型已更改

Disk /dev/sdb: 1000.2 GB, 1000204886016 bytes
255 heads, 63 sectors/track, 121601 cylinders, total 1953525168 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disk identifier: 0x00000000

   Device Boot      Start         End      Blocks   Id  System
/dev/sdb1            2048   209717247   104857600   8e  Linux LVM

Command (m for help): w  # 保存并退出
The partition table has been altered!

Calling ioctl() to re-read partition table.
Syncing disks.
```

### 4.7 设置分区引导标志

在交互式模式下设置分区引导标志的步骤：

```bash
# 进入fdisk交互式模式
$ sudo fdisk /dev/sda

Command (m for help): p  # 查看当前分区表

Disk /dev/sda: 500.1 GB, 500107862016 bytes
255 heads, 63 sectors/track, 60801 cylinders, total 976773168 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disk identifier: 0x0003b4b5

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1            2048      499711      248832   83  Linux
/dev/sda2          501758   976771071   488134657    5  Extended
/dev/sda5          501760   976771071   488134656   8e  Linux LVM

Command (m for help): a  # 设置引导标志
Partition number (1-5, default 5): 1  # 选择分区1
The bootable flag on partition 1 is enabled now.

Command (m for help): p  # 确认引导标志已设置

Disk /dev/sda: 500.1 GB, 500107862016 bytes
255 heads, 63 sectors/track, 60801 cylinders, total 976773168 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disk identifier: 0x0003b4b5

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *        2048      499711      248832   83  Linux  # 注意Boot列的*号
/dev/sda2          501758   976771071   488134657    5  Extended
/dev/sda5          501760   976771071   488134656   8e  Linux LVM

Command (m for help): w  # 保存并退出
The partition table has been altered!

Calling ioctl() to re-read partition table.
Syncing disks.
```

### 4.8 显示分区详细信息

在交互式模式下显示特定分区的详细信息：

```bash
# 进入fdisk交互式模式
$ sudo fdisk /dev/sda

Command (m for help): i  # 显示分区详细信息
Partition number (1-5): 1  # 选择分区1

         Device: /dev/sda1
          Start: 2048
            End: 499711
        Sectors: 497664
     Cylinders: 30
       Memories: 16
    Sectors/track: 63
          Bytes: 254,803,968
          Type: Linux
         Boot: *
```

### 4.9 验证分区表

在交互式模式下验证分区表的正确性：

```bash
# 进入fdisk交互式模式
$ sudo fdisk /dev/sda

Command (m for help): v  # 验证分区表
No errors found.
61 unallocated sectors.
```

### 4.10 使用扇区单位显示

以扇区为单位显示分区表信息，而不是默认的柱面单位：

```bash
# 以扇区为单位显示分区表
$ sudo fdisk -lu /dev/sda

Disk /dev/sda: 500.1 GB, 500107862016 bytes
255 heads, 63 sectors/track, 60801 cylinders, total 976773168 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disk identifier: 0x0003b4b5

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *        2048      499711      248832   83  Linux
/dev/sda2          501758   976771071   488134657    5  Extended
/dev/sda5          501760   976771071   488134656   8e  Linux LVM
```

### 4.11 复制分区表到另一个磁盘

将一个磁盘的分区表复制到另一个磁盘：

```bash
# 备份分区表到文件
$ sudo fdisk -l /dev/sda > sda_partition_table.txt

# 或者使用sfdisk命令更精确地备份和恢复
$ sudo sfdisk -d /dev/sda > sda_partition_table.bin

# 恢复分区表到另一个磁盘
$ sudo sfdisk /dev/sdb < sda_partition_table.bin
```

> **注意**：使用sfdisk复制分区表时，目标磁盘的大小应大于或等于源磁盘。

### 4.12 查看分区大小

使用fdisk命令查看特定分区的大小（以块为单位）：

```bash
# 查看/dev/sda1分区的大小（以块为单位）
$ sudo fdisk -s /dev/sda1
248832
```

## 5. 高级用法

### 5.1 磁盘分区自动化脚本

创建一个自动化脚本，用于对新磁盘进行标准分区：

```bash
#!/bin/bash
# 磁盘分区自动化脚本

# 配置参数
DISK=${1:-"/dev/sdb"}  # 默认为/dev/sdb
BOOT_SIZE="512M"       # 引导分区大小
SWAP_SIZE="8G"         # 交换分区大小
ROOT_SIZE="40G"        # 根分区大小
DATA_SIZE="100G"       # 数据分区大小

# 显示帮助信息
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo "用法: $0 [磁盘设备]"
    echo "自动化分区指定磁盘，创建引导分区、交换分区、根分区和数据分区"
    echo "默认磁盘: $DISK"
    exit 0
fi

# 检查磁盘是否存在
if [ ! -b "$DISK" ]; then
    echo "错误：磁盘设备 $DISK 不存在"
exit 1
fi

# 警告用户
echo "警告：此脚本将完全重新分区 $DISK，所有现有数据将被删除！"
echo -n "是否继续？(y/N): "
read CONFIRM
if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "操作已取消"
exit 0
fi

# 获取磁盘大小信息
DISK_SIZE=$(fdisk -l "$DISK" | grep "Disk $DISK" | awk '{print $3}')
DISK_UNIT=$(fdisk -l "$DISK" | grep "Disk $DISK" | awk '{print $4}')
echo "开始对 $DISK_SIZE $DISK_UNIT 磁盘进行分区..."

# 使用fdisk进行分区
(echo o;  # 创建新的空DOS分区表
echo n;  # 创建新分区
echo p;  # 主分区
echo 1;  # 分区号
 echo;    # 默认起始扇区
echo +$BOOT_SIZE;  # 引导分区大小
echo t;  # 更改分区类型
echo 83; # Linux类型
 echo a;  # 设置引导标志
 echo 1;  # 分区1
 echo n;  # 创建新分区
echo p;  # 主分区
echo 2;  # 分区号
 echo;    # 默认起始扇区
echo +$SWAP_SIZE;  # 交换分区大小
echo t;  # 更改分区类型
 echo 2;  # 分区2
echo 82; # Linux swap类型
 echo n;  # 创建新分区
echo p;  # 主分区
echo 3;  # 分区号
 echo;    # 默认起始扇区
echo +$ROOT_SIZE;  # 根分区大小
echo t;  # 更改分区类型
 echo 3;  # 分区3
echo 83; # Linux类型
 echo n;  # 创建新分区
echo p;  # 主分区
echo 4;  # 分区号
 echo;    # 默认起始扇区
echo +$DATA_SIZE;  # 数据分区大小
echo t;  # 更改分区类型
 echo 4;  # 分区4
echo 83; # Linux类型
 echo w;  # 保存并退出
) | sudo fdisk "$DISK"

# 检查分区是否成功
if [ $? -ne 0 ]; then
    echo "错误：分区过程失败"
exit 1
fi

# 重新读取分区表
sudo partprobe "$DISK"

# 格式化分区
echo "正在格式化分区..."
sudo mkfs.ext4 "${DISK}1" -L boot
sudo mkswap "${DISK}2" -L swap
sudo swapon "${DISK}2"
sudo mkfs.ext4 "${DISK}3" -L root
sudo mkfs.ext4 "${DISK}4" -L data

# 显示结果
echo -e "\n分区完成！以下是新的分区表："
sudo fdisk -l "$DISK"

echo -e "\n分区挂载信息："
echo "引导分区: ${DISK}1 (${BOOT_SIZE}) - 已格式化为ext4"
echo "交换分区: ${DISK}2 (${SWAP_SIZE}) - 已格式化为swap并激活"
echo "根分区: ${DISK}3 (${ROOT_SIZE}) - 已格式化为ext4"
echo "数据分区: ${DISK}4 (${DATA_SIZE}) - 已格式化为ext4"

echo -e "\n使用以下命令挂载分区："
echo "sudo mount ${DISK}1 /mnt/boot"
echo "sudo mount ${DISK}3 /mnt"
echo "sudo mkdir -p /mnt/data"
echo "sudo mount ${DISK}4 /mnt/data"
```

### 5.2 GPT分区表操作

使用fdisk工具操作GPT分区表：

```bash
#!/bin/bash
# GPT分区表操作脚本

# 配置参数
DISK=${1:-"/dev/sdb"}  # 默认为/dev/sdb

# 显示帮助信息
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo "用法: $0 [磁盘设备]"
    echo "使用fdisk创建GPT分区表并进行分区操作"
    exit 0
fi

# 检查磁盘是否存在
if [ ! -b "$DISK" ]; then
    echo "错误：磁盘设备 $DISK 不存在"
exit 1
fi

# 警告用户
echo "警告：此脚本将在 $DISK 上创建GPT分区表，所有现有数据将被删除！"
echo -n "是否继续？(y/N): "
read CONFIRM
if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "操作已取消"
exit 0
fi

# 使用fdisk创建GPT分区表并分区
(echo g;  # 创建新的空GPT分区表
echo n;  # 创建新分区
echo 1;  # 分区号
 echo;    # 默认起始扇区
echo +512M;  # EFI分区大小
echo t;  # 更改分区类型
 echo 1;  # 分区1
 echo 1;  # EFI系统分区类型
 echo n;  # 创建新分区
echo 2;  # 分区号
 echo;    # 默认起始扇区
echo +8G;  # 交换分区大小
echo t;  # 更改分区类型
 echo 2;  # 分区2
 echo 19;  # Linux交换分区类型
 echo n;  # 创建新分区
echo 3;  # 分区号
 echo;    # 默认起始扇区
echo +40G;  # 根分区大小
echo t;  # 更改分区类型
 echo 3;  # 分区3
 echo 20;  # Linux文件系统分区类型
 echo w;  # 保存并退出
) | sudo fdisk "$DISK"

# 检查分区是否成功
if [ $? -ne 0 ]; then
    echo "错误：GPT分区过程失败"
exit 1
fi

# 重新读取分区表
sudo partprobe "$DISK"

# 格式化GPT分区
echo "正在格式化GPT分区..."
sudo mkfs.fat -F32 "${DISK}1" -n EFI
sudo mkswap "${DISK}2" -L swap
sudo swapon "${DISK}2"
sudo mkfs.ext4 "${DISK}3" -L root

# 显示结果
echo -e "\nGPT分区完成！以下是新的分区表："
sudo fdisk -l "$DISK"

echo -e "\nGPT分区信息："
echo "EFI分区: ${DISK}1 - 已格式化为FAT32"
echo "交换分区: ${DISK}2 - 已格式化为swap并激活"
echo "根分区: ${DISK}3 - 已格式化为ext4"
```

### 5.3 分区表备份与恢复工具

创建一个工具脚本，用于备份和恢复分区表：

```bash
#!/bin/bash
# 分区表备份与恢复工具

# 配置参数
BACKUP_DIR="$HOME/partition_backups"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 显示帮助信息
show_help() {
    echo "分区表备份与恢复工具"
    echo "用法: $0 [选项] <设备>"
    echo "选项:"
    echo "  -b, --backup     备份指定设备的分区表"
    echo "  -r, --restore    恢复指定设备的分区表"
    echo "  -l, --list       列出所有备份"
    echo "  -h, --help       显示此帮助信息"
    echo "示例:"
    echo "  $0 -b /dev/sda     备份/dev/sda的分区表"
    echo "  $0 -r /dev/sda     恢复/dev/sda的分区表"
}

# 备份分区表
backup_partition_table() {
    local device=$1
    local device_name=$(basename "$device")
    local backup_file="$BACKUP_DIR/${device_name}_partition_table_$DATE.bin"
    local info_file="$BACKUP_DIR/${device_name}_partition_table_$DATE.txt"
    
    # 检查设备是否存在
    if [ ! -b "$device" ]; then
        echo "错误：设备 $device 不存在"
        return 1
    fi
    
    # 检查是否有root权限
    if [ "$(id -u)" != "0" ]; then
        echo "错误：需要root权限来备份分区表"
        echo "请使用sudo运行此命令"
        return 1
    fi
    
    echo "正在备份 $device 的分区表..."
    
    # 使用sfdisk备份分区表（更精确）
    if sudo sfdisk -d "$device" > "$backup_file"; then
        echo "分区表二进制备份已保存至：$backup_file"
    else
        echo "错误：sfdisk备份失败"
        return 1
    fi
    
    # 使用fdisk备份分区表信息（人类可读）
    if sudo fdisk -l "$device" > "$info_file"; then
        echo "分区表信息备份已保存至：$info_file"
    else
        echo "警告：fdisk信息备份失败，但二进制备份可能已成功"
    fi
    
    # 添加MD5校验和
    md5sum "$backup_file" > "$backup_file.md5"
    echo "MD5校验和已保存至：$backup_file.md5"
    
    echo "分区表备份完成！"
    return 0
}

# 恢复分区表
restore_partition_table() {
    local device=$1
    local device_name=$(basename "$device")
    
    # 检查设备是否存在
    if [ ! -b "$device" ]; then
        echo "错误：设备 $device 不存在"
        return 1
    fi
    
    # 检查是否有root权限
    if [ "$(id -u)" != "0" ]; then
        echo "错误：需要root权限来恢复分区表"
        echo "请使用sudo运行此命令"
        return 1
    fi
    
    # 列出可用的备份
    echo "可用的 $device_name 分区表备份："
    ls -l "$BACKUP_DIR/${device_name}_partition_table_*.bin" | sort -r
    
    if [ $? -ne 0 ]; then
        echo "错误：没有找到 $device_name 的分区表备份"
        return 1
    fi
    
    # 让用户选择备份文件
    echo -n "请输入要恢复的备份文件名（完整路径）: "
    read backup_file
    
    # 验证备份文件是否存在
    if [ ! -f "$backup_file" ]; then
        echo "错误：备份文件 $backup_file 不存在"
        return 1
    fi
    
    # 验证MD5校验和
    if [ -f "$backup_file.md5" ]; then
        echo "正在验证备份文件的完整性..."
        md5sum -c "$backup_file.md5"
        if [ $? -ne 0 ]; then
            echo "错误：备份文件已损坏或被修改"
            return 1
        fi
    else
        echo "警告：未找到MD5校验和文件，无法验证备份文件的完整性"
    fi
    
    # 警告用户
    echo -e "\n警告：此操作将覆盖 $device 上的所有分区表和数据！"
echo -n "是否确认恢复？(y/N): "
    read CONFIRM
    if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
        echo "恢复操作已取消"
        return 0
    fi
    
    # 恢复分区表
    echo "正在恢复分区表到 $device..."
    if sudo sfdisk "$device" < "$backup_file"; then
        echo "分区表恢复成功！"
        # 重新读取分区表
        sudo partprobe "$device"
        return 0
    else
        echo "错误：分区表恢复失败"
        return 1
    fi
}

# 列出所有备份
list_backups() {
    echo "所有分区表备份："
    ls -l "$BACKUP_DIR"/*.{bin,txt} | sort -r
    return 0
}

# 主函数
main() {
    if [ $# -lt 1 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
        show_help
        return 0
    fi
    
    case "$1" in
        -b|--backup)
            if [ $# -ne 2 ]; then
                echo "错误：请指定要备份的设备"
                show_help
                return 1
            fi
            backup_partition_table "$2"
            ;;
        -r|--restore)
            if [ $# -ne 2 ]; then
                echo "错误：请指定要恢复的设备"
                show_help
                return 1
            fi
            restore_partition_table "$2"
            ;;
        -l|--list)
            list_backups
            ;;
        *)
            echo "错误：未知选项 $1"
            show_help
            return 1
            ;;
    esac
}

# 执行主函数
main "$@"
```

### 5.4 磁盘分区最佳实践工具

创建一个脚本，根据磁盘大小和用途自动推荐最佳分区方案：

```bash
#!/bin/bash
# 磁盘分区最佳实践工具

# 配置参数
DISK=${1}

# 显示帮助信息
show_help() {
    echo "磁盘分区最佳实践工具"
    echo "用法: $0 <磁盘设备>"
    echo "示例: $0 /dev/sdb"
    exit 0
}

# 检查参数
if [ $# -ne 1 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    show_help
fi

# 检查磁盘是否存在
if [ ! -b "$DISK" ]; then
    echo "错误：磁盘设备 $DISK 不存在"
exit 1
fi

# 获取磁盘大小信息
DISK_INFO=$(fdisk -l "$DISK" | grep "Disk $DISK")
DISK_SIZE=$(echo "$DISK_INFO" | awk '{print $3}')
DISK_UNIT=$(echo "$DISK_INFO" | awk '{print $4}')

# 转换磁盘大小为GB以便计算
if [ "$DISK_UNIT" = "GB" ]; then
    SIZE_GB=$DISK_SIZE
elif [ "$DISK_UNIT" = "TB" ]; then
    SIZE_GB=$(echo "$DISK_SIZE * 1024" | bc)
elif [ "$DISK_UNIT" = "MB" ]; then
    SIZE_GB=$(echo "$DISK_SIZE / 1024" | bc)
else
    echo "错误：无法识别的磁盘大小单位: $DISK_UNIT"
exit 1
fi

# 输出磁盘信息
cat << EOF
==================================
磁盘分区最佳实践建议
==================================
磁盘: $DISK
大小: $DISK_SIZE $DISK_UNIT ($SIZE_GB GB)
检测时间: $(date)
==================================
EOF

# 根据磁盘大小和用途推荐分区方案
if (( $(echo "$SIZE_GB < 100" | bc -l) )); then
    # 小型磁盘（<100GB）：适合作为系统盘或小型服务器
    cat << EOF
推荐方案（小型系统盘）:

1. 引导分区 (/boot): 512MB - ext4
   用途: 存储启动加载程序和内核文件

2. 交换分区 (swap): $(echo "$SIZE_GB/4" | bc)GB - swap
   用途: 虚拟内存，建议为物理内存的1-2倍（最大不超过8GB）

3. 根分区 (/): 剩余空间 - ext4或xfs
   用途: 系统和应用程序安装

适用场景: 小型服务器、个人电脑、虚拟机

分区命令示例:

sudo fdisk $DISK
   o (创建DOS分区表)
   n, p, 1, [回车], +512M (创建引导分区)
   t, 1, 83 (设置为Linux类型)
   a, 1 (设置引导标志)
   n, p, 2, [回车], +$(echo "$SIZE_GB/4" | bc)G (创建交换分区)
   t, 2, 82 (设置为swap类型)
   n, p, 3, [回车], [回车] (创建根分区)
   t, 3, 83 (设置为Linux类型)
   w (保存并退出)

sudo mkfs.ext4 ${DISK}1 -L boot
sudo mkswap ${DISK}2 -L swap && sudo swapon ${DISK}2
sudo mkfs.ext4 ${DISK}3 -L root
EOF
elif (( $(echo "$SIZE_GB >= 100 && $SIZE_GB < 500" | bc -l) )); then
    # 中型磁盘（100GB-500GB）：适合一般服务器或桌面系统
    cat << EOF
推荐方案（中型通用服务器）:

1. 引导分区 (/boot): 1GB - ext4
   用途: 存储启动加载程序和内核文件

2. 交换分区 (swap): $(echo "$SIZE_GB/8" | bc)GB - swap (最大8GB)
   用途: 虚拟内存

3. 根分区 (/): 50GB - ext4或xfs
   用途: 系统和应用程序安装

4. 数据分区 (/data): 剩余空间 - ext4或xfs
   用途: 存储用户数据和应用数据

适用场景: 中小型服务器、开发环境、个人工作站

分区命令示例:

sudo fdisk $DISK
   o (创建DOS分区表)
   n, p, 1, [回车], +1G (创建引导分区)
   t, 1, 83 (设置为Linux类型)
   a, 1 (设置引导标志)
   n, p, 2, [回车], +$(echo "if ($SIZE_GB/8 > 8) 8 else $SIZE_GB/8" | bc)G (创建交换分区)
   t, 2, 82 (设置为swap类型)
   n, p, 3, [回车], +50G (创建根分区)
   t, 3, 83 (设置为Linux类型)
   n, p, 4, [回车], [回车] (创建数据分区)
   t, 4, 83 (设置为Linux类型)
   w (保存并退出)

sudo mkfs.ext4 ${DISK}1 -L boot
sudo mkswap ${DISK}2 -L swap && sudo swapon ${DISK}2
sudo mkfs.ext4 ${DISK}3 -L root
sudo mkfs.ext4 ${DISK}4 -L data
EOF
elif (( $(echo "$SIZE_GB >= 500 && $SIZE_GB < 2000" | bc -l) )); then
    # 大型磁盘（500GB-2TB）：适合数据服务器或应用服务器
    cat << EOF
推荐方案（大型数据服务器）:

1. 引导分区 (/boot): 1GB - ext4
   用途: 存储启动加载程序和内核文件

2. 交换分区 (swap): 8GB - swap
   用途: 虚拟内存（对于大内存服务器，可减少或省略）

3. 根分区 (/): 100GB - ext4或xfs
   用途: 系统和应用程序安装

4. 应用分区 (/opt): 200GB - ext4或xfs
   用途: 安装第三方应用程序

5. 数据分区 (/data): 剩余空间 - ext4或xfs
   用途: 存储大量数据

适用场景: 数据服务器、应用服务器、数据库服务器

分区命令示例:

sudo fdisk $DISK
   g (创建GPT分区表)
   n, 1, [回车], +1G (创建引导分区)
   t, 1, 20 (设置为Linux文件系统类型)
   n, 2, [回车], +8G (创建交换分区)
   t, 2, 19 (设置为swap类型)
   n, 3, [回车], +100G (创建根分区)
   t, 3, 20 (设置为Linux文件系统类型)
   n, 4, [回车], +200G (创建应用分区)
   t, 4, 20 (设置为Linux文件系统类型)
   n, 5, [回车], [回车] (创建数据分区)
   t, 5, 20 (设置为Linux文件系统类型)
   w (保存并退出)

sudo mkfs.ext4 ${DISK}1 -L boot
sudo mkswap ${DISK}2 -L swap && sudo swapon ${DISK}2
sudo mkfs.ext4 ${DISK}3 -L root
sudo mkfs.ext4 ${DISK}4 -L opt
sudo mkfs.ext4 ${DISK}5 -L data
EOF
else
    # 超大型磁盘（>=2TB）：适合存储服务器或数据中心
    cat << EOF
推荐方案（超大型存储服务器）:

1. 引导分区 (/boot): 1GB - ext4
   用途: 存储启动加载程序和内核文件

2. 交换分区 (swap): 8GB - swap
   用途: 虚拟内存

3. 根分区 (/): 100GB - ext4或xfs
   用途: 系统和应用程序安装

4. LVM物理卷: 剩余空间
   用途: 创建逻辑卷组，灵活管理存储空间

适用场景: 存储服务器、数据中心、大容量存储需求

分区命令示例:

sudo fdisk $DISK
   g (创建GPT分区表)
   n, 1, [回车], +1G (创建引导分区)
   t, 1, 20 (设置为Linux文件系统类型)
   n, 2, [回车], +8G (创建交换分区)
   t, 2, 19 (设置为swap类型)
   n, 3, [回车], +100G (创建根分区)
   t, 3, 20 (设置为Linux文件系统类型)
   n, 4, [回车], [回车] (创建LVM物理卷分区)
   t, 4, 30 (设置为Linux LVM类型)
   w (保存并退出)

sudo mkfs.ext4 ${DISK}1 -L boot
sudo mkswap ${DISK}2 -L swap && sudo swapon ${DISK}2
sudo mkfs.ext4 ${DISK}3 -L root
sudo pvcreate ${DISK}4
sudo vgcreate vg_data ${DISK}4

# 根据需要创建逻辑卷，例如:
# sudo lvcreate -L 500G -n lv_database vg_data
# sudo lvcreate -L 1T -n lv_backup vg_data
# sudo mkfs.xfs /dev/vg_data/lv_database
# sudo mkfs.xfs /dev/vg_data/lv_backup
EOF
fi

cat << EOF

==================================
分区最佳实践建议
==================================
1. 始终备份重要数据，然后再进行分区操作
2. 对于新磁盘，建议使用GPT分区表而不是MBR
   - GPT支持大于2TB的磁盘
   - GPT支持更多分区（最多128个）
   - GPT更可靠，包含备份分区表
3. 选择合适的文件系统:
   - ext4: 通用文件系统，稳定性好
   - xfs: 适合大型文件和高吞吐量
   - btrfs: 支持快照和校验和，但生产环境中需谨慎
4. 考虑使用LVM进行灵活的存储空间管理
5. 为系统盘预留足够的空间，避免根分区空间耗尽
6. 定期检查分区健康状态和可用空间
EOF
```

## 6. 常见问题与解决方案

### 6.1 无法识别新创建的分区

**问题**：使用fdisk创建分区后，系统无法识别新分区。

**解决方案**：
使用partprobe命令刷新分区表，让系统识别新创建的分区：

```bash
# 刷新分区表
sudo partprobe

# 如果仍然无法识别，可以尝试重启系统
# 或者使用以下命令重新加载分区表
sudo blockdev --rereadpt /dev/sdb
```

### 6.2 无法删除扩展分区

**问题**：尝试删除扩展分区时，出现错误或无法删除。

**解决方案**：
必须先删除扩展分区中的所有逻辑分区，然后才能删除扩展分区本身：

```bash
# 进入fdisk交互式模式
sudo fdisk /dev/sdb

Command (m for help): p  # 查看当前分区表
# 假设/dev/sdb2是扩展分区，包含/dev/sdb5和/dev/sdb6逻辑分区

Command (m for help): d  # 删除分区
Partition number (1-6): 5  # 先删除逻辑分区5
Partition 5 is deleted

Command (m for help): d  # 删除分区
Partition number (1-6): 6  # 再删除逻辑分区6
Partition 6 is deleted

Command (m for help): d  # 删除分区
Partition number (1-6): 2  # 最后删除扩展分区2
Partition 2 is deleted

Command (m for help): w  # 保存并退出
```

### 6.3 磁盘空间大于2TB无法使用全部空间

**问题**：使用MBR分区表的磁盘大于2TB，无法使用全部磁盘空间。

**解决方案**：
MBR分区表最多支持2TB的磁盘空间，需要转换为GPT分区表来支持更大的磁盘：

```bash
# 备份所有数据（转换分区表会丢失所有数据）

# 进入fdisk交互式模式
sudo fdisk /dev/sdb

Command (m for help): g  # 转换为GPT分区表
Created a new GPT disklabel (GUID: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX).

# 重新创建分区
Command (m for help): n  # 创建新分区
# 按照提示创建分区...

Command (m for help): w  # 保存并退出
```

> **注意**：转换分区表会丢失所有数据，请务必先备份重要数据。

### 6.4 分区类型错误导致无法挂载

**问题**：创建分区后，无法挂载或格式化分区。

**解决方案**：
检查并确保分区类型正确设置：

```bash
# 查看分区类型
sudo fdisk -l /dev/sdb

# 如果分区类型不正确，进入fdisk修改
sudo fdisk /dev/sdb

Command (m for help): t  # 更改分区类型
Partition number (1-4): 1  # 选择要修改的分区
Partition type (type L to list all types): 83  # 设置为Linux类型

Command (m for help): w  # 保存并退出
```

### 6.5 fdisk命令卡住或无响应

**问题**：运行fdisk命令时，命令卡住或无响应。

**解决方案**：
- 检查磁盘连接是否正常
- 检查磁盘是否有硬件故障
- 尝试使用其他分区工具如parted
- 如果是虚拟机中的磁盘，确保虚拟机配置正确

```bash
# 尝试使用parted工具替代fdisk
sudo parted /dev/sdb
```

## 7. 实践练习

### 练习1：基本磁盘分区操作

1. 使用fdisk查看系统中的磁盘信息
2. 为一个新磁盘创建分区表
3. 创建2个主分区和1个交换分区
4. 格式化并挂载这些分区

```bash
# 解决方案示例

# 查看系统中的磁盘信息
sudo fdisk -l

# 选择一个未使用的磁盘（假设为/dev/sdb）
sudo fdisk /dev/sdb

# 创建新的分区表（MBR）
Command (m for help): o

# 创建第一个主分区（10GB）
Command (m for help): n
Partition type
   p   primary (0 primary, 0 extended, 4 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (1-4, default 1): 1
First sector (2048-1953525167, default 2048):
Last sector, +sectors or +size{K,M,G,T,P} (2048-1953525167, default 1953525167): +10G

# 创建第二个主分区（20GB）
Command (m for help): n
Partition type
   p   primary (1 primary, 0 extended, 3 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (2-4, default 2): 2
First sector (20973568-1953525167, default 20973568):
Last sector, +sectors or +size{K,M,G,T,P} (20973568-1953525167, default 1953525167): +20G

# 创建交换分区（4GB）
Command (m for help): n
Partition type
   p   primary (2 primary, 0 extended, 2 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (3-4, default 3): 3
First sector (62916608-1953525167, default 62916608):
Last sector, +sectors or +size{K,M,G,T,P} (62916608-1953525167, default 1953525167): +4G

# 更改分区类型为swap
Command (m for help): t
Partition number (1-3, default 3): 3
Partition type (type L to list all types): 82

# 保存并退出
Command (m for help): w

# 格式化分区
sudo mkfs.ext4 /dev/sdb1
sudo mkfs.ext4 /dev/sdb2
sudo mkswap /dev/sdb3

sudo swapon /dev/sdb3  # 激活交换分区

sudo mkdir -p /mnt/data1 /mnt/data2  # 创建挂载点
sudo mount /dev/sdb1 /mnt/data1  # 挂载第一个分区
sudo mount /dev/sdb2 /mnt/data2  # 挂载第二个分区

echo "挂载完成，请检查："
df -h | grep sdb
echo "交换空间状态："
free -h
```

### 练习2：GPT分区表操作

1. 为一个大于2TB的磁盘创建GPT分区表
2. 创建多个分区用于不同用途
3. 设置适当的分区类型

```bash
#!/bin/bash
# GPT分区表操作练习脚本

# 定义颜色
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # 无颜色

# 检查是否有root权限
if [ "$(id -u)" != "0" ]; then
    echo -e "${YELLOW}警告：此脚本需要root权限才能执行所有操作。${NC}"
echo "请使用sudo运行此脚本。"
exit 1
fi

# 让用户选择磁盘
echo -e "${BLUE}可用磁盘列表：${NC}"
sudo fdisk -l | grep "Disk /dev/" | grep -v "Disk /dev/loop"
echo -n "请输入要进行GPT分区的磁盘设备（如/dev/sdb）: "
read DISK

# 检查磁盘是否存在
if [ ! -b "$DISK" ]; then
    echo -e "${YELLOW}错误：磁盘设备 $DISK 不存在。${NC}"
exit 1
fi

# 警告用户
echo -e "${YELLOW}\n警告：此操作将在 $DISK 上创建GPT分区表，所有现有数据将被删除！${NC}"
echo -n "是否继续？(y/N): "
read CONFIRM
if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo -e "${GREEN}\n操作已取消。${NC}"
exit 0
fi

# 获取磁盘大小
DISK_SIZE=$(sudo fdisk -l "$DISK" | grep "Disk $DISK" | awk '{print $3}')
DISK_UNIT=$(sudo fdisk -l "$DISK" | grep "Disk $DISK" | awk '{print $4}')

# 创建GPT分区表
(echo g;  # 创建GPT分区表
echo p;  # 显示当前分区表
echo n;  # 创建EFI分区
 echo;    # 默认分区号
 echo;    # 默认起始扇区
echo +512M;  # EFI分区大小
 echo t;  # 更改分区类型
 echo 1;  # EFI系统分区类型
echo n;  # 创建根分区
 echo;    # 默认分区号
 echo;    # 默认起始扇区
echo +50G;  # 根分区大小
 echo t;  # 更改分区类型
 echo 2;  # 选择分区2
 echo 20;  # Linux文件系统类型
 echo n;  # 创建数据分区
 echo;    # 默认分区号
 echo;    # 默认起始扇区
echo +200G;  # 数据分区大小
 echo t;  # 更改分区类型
 echo 3;  # 选择分区3
 echo 20;  # Linux文件系统类型
 echo n;  # 创建LVM分区（剩余空间）
 echo;    # 默认分区号
 echo;    # 默认起始扇区
 echo;    # 默认结束扇区（剩余空间）
 echo t;  # 更改分区类型
 echo 4;  # 选择分区4
 echo 30;  # Linux LVM类型
 echo p;  # 显示最终分区表
echo w;  # 保存并退出
) | sudo fdisk "$DISK"

# 检查分区是否成功
if [ $? -eq 0 ]; then
    echo -e "${GREEN}\nGPT分区表创建成功！${NC}"
else
    echo -e "${YELLOW}\n错误：GPT分区表创建失败。${NC}"
exit 1
fi

# 重新读取分区表
sudo partprobe "$DISK"

# 格式化分区
echo -e "${BLUE}\n正在格式化分区...${NC}"
sudo mkfs.fat -F32 "${DISK}1" -n EFI
sudo mkfs.ext4 "${DISK}2" -n root
sudo mkfs.ext4 "${DISK}3" -n data
sudo pvcreate "${DISK}4"

echo -e "${GREEN}\n分区格式化完成！${NC}"

# 显示最终结果
echo -e "${BLUE}\n最终分区表：${NC}"
sudo fdisk -l "$DISK"

echo -e "${GREEN}\nGPT分区表操作练习完成！${NC}"
echo -e "${YELLOW}注意：此练习仅供学习使用，实际生产环境中请先备份数据。${NC}"
```

### 练习3：分区表备份与恢复

1. 备份现有磁盘的分区表
2. 模拟分区表损坏
3. 恢复分区表

```bash
#!/bin/bash
# 分区表备份与恢复练习脚本

# 配置参数
BACKUP_FILE="partition_table_backup.bin"
DISK=${1}

# 显示帮助信息
if [ $# -ne 1 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo "用法: $0 <磁盘设备>"
    echo "示例: $0 /dev/sdb"
    exit 0
fi

# 检查磁盘是否存在
if [ ! -b "$DISK" ]; then
    echo "错误：磁盘设备 $DISK 不存在"
exit 1
fi

# 检查是否有root权限
if [ "$(id -u)" != "0" ]; then
    echo "错误：需要root权限来操作分区表"
exit 1
fi

# 警告用户
read -p "警告：此练习将修改 $DISK 的分区表，仅在测试环境中使用！按Enter继续..."

# 步骤1：备份分区表
echo -e "\n=== 步骤1：备份分区表 ==="
echo "正在备份 $DISK 的分区表..."
sudo sfdisk -d "$DISK" > "$BACKUP_FILE"
if [ $? -eq 0 ]; then
    echo "分区表备份成功：$BACKUP_FILE"
    md5sum "$BACKUP_FILE" > "$BACKUP_FILE.md5"
    echo "MD5校验和已保存：$BACKUP_FILE.md5"
else
    echo "错误：分区表备份失败"
exit 1
fi

# 显示当前分区表
echo -e "\n当前分区表："
sudo fdisk -l "$DISK"

# 步骤2：模拟分区表损坏
echo -e "\n=== 步骤2：模拟分区表损坏 ==="
read -p "按Enter模拟分区表损坏..."

# 创建一个新的空分区表
echo -e "o\nw" | sudo fdisk "$DISK" > /dev/null 2>&1

# 显示损坏后的分区表
echo -e "\n模拟损坏后的分区表："
sudo fdisk -l "$DISK"

# 步骤3：恢复分区表
echo -e "\n=== 步骤3：恢复分区表 ==="
read -p "按Enter恢复分区表..."

# 验证备份文件
md5sum -c "$BACKUP_FILE.md5"
if [ $? -ne 0 ]; then
    echo "错误：备份文件已损坏，无法恢复"
exit 1
fi

# 恢复分区表
sudo sfdisk "$DISK" < "$BACKUP_FILE"
if [ $? -eq 0 ]; then
    echo "分区表恢复成功！"
else
    echo "错误：分区表恢复失败"
exit 1
fi

# 重新读取分区表
sudo partprobe "$DISK"

# 显示恢复后的分区表
echo -e "\n恢复后的分区表："
sudo fdisk -l "$DISK"

# 清理
read -p "是否删除备份文件？(y/N): " DEL_BACKUP
if [ "$DEL_BACKUP" = "y" ] || [ "$DEL_BACKUP" = "Y" ]; then
    rm -f "$BACKUP_FILE" "$BACKUP_FILE.md5"
    echo "备份文件已删除"
fi

echo -e "\n分区表备份与恢复练习完成！"
```

### 练习4：磁盘分区规划工具

创建一个交互式工具，帮助用户根据需求规划磁盘分区：

```bash
#!/bin/bash
# 磁盘分区规划工具

#!/bin/bash
# 磁盘分区规划工具

# 定义颜色
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # 无颜色

# 全局变量
DISK=""
PARTITION_SCHEME="mbr"  # 默认使用MBR分区表
PARTITIONS=()
TOTAL_SIZE=0
TOTAL_ALLOCATED=0

# 显示欢迎信息
show_welcome() {
    clear
    echo -e "${BLUE}====================================${NC}"
    echo -e "${BLUE}      Linux磁盘分区规划工具         ${NC}"
    echo -e "${BLUE}====================================${NC}"
    echo -e "${YELLOW}此工具将帮助您规划磁盘分区方案。${NC}"
    echo -e "${RED}注意：此工具仅提供规划建议，不会实际执行分区操作。${NC}"
    echo -e "${BLUE}====================================${NC}\n"
}

# 选择磁盘\ nselect_disk() {
    echo -e "${BLUE}可用磁盘列表：${NC}"
    sudo fdisk -l | grep "Disk /dev/" | grep -v "Disk /dev/loop" | awk '{print $2, $3, $4}' | sed 's/://'
    
    echo -n "请输入要规划的磁盘设备（如/dev/sdb）: "
    read DISK
    
    # 检查磁盘是否存在
    if [ ! -b "$DISK" ]; then
        echo -e "${RED}错误：磁盘设备 $DISK 不存在。${NC}"
        return 1
    fi
    
    # 获取磁盘大小
    DISK_INFO=$(sudo fdisk -l "$DISK" | grep "Disk $DISK")
    DISK_SIZE=$(echo "$DISK_INFO" | awk '{print $3}')
    DISK_UNIT=$(echo "$DISK_INFO" | awk '{print $4}')
    
    # 转换磁盘大小为GB以便计算
    if [ "$DISK_UNIT" = "GB" ]; then
        TOTAL_SIZE=$DISK_SIZE
    elif [ "$DISK_UNIT" = "TB" ]; then
        TOTAL_SIZE=$(echo "$DISK_SIZE * 1024" | bc)
    elif [ "$DISK_UNIT" = "MB" ]; then
        TOTAL_SIZE=$(echo "$DISK_SIZE / 1024" | bc)
    else
        echo -e "${RED}错误：无法识别的磁盘大小单位: $DISK_UNIT${NC}"
        return 1
    fi
    
    echo -e "${GREEN}已选择磁盘：$DISK，大小：$DISK_SIZE $DISK_UNIT ($TOTAL_SIZE GB)${NC}\n"
    return 0
}

# 选择分区表类型
select_partition_scheme() {
    echo -e "${BLUE}选择分区表类型：${NC}"
    echo "1. MBR分区表（最大支持2TB磁盘，最多4个主分区）"
    echo "2. GPT分区表（支持大于2TB磁盘，最多128个分区）"
    
    echo -n "请选择 [1-2]（默认1）: "
    read CHOICE
    
    if [ -z "$CHOICE" ] || [ "$CHOICE" = "1" ]; then
        PARTITION_SCHEME="mbr"
        echo -e "${GREEN}已选择MBR分区表。${NC}\n"
    elif [ "$CHOICE" = "2" ]; then
        PARTITION_SCHEME="gpt"
        echo -e "${GREEN}已选择GPT分区表。${NC}\n"
    else
        echo -e "${RED}无效选择，默认使用MBR分区表。${NC}\n"
        PARTITION_SCHEME="mbr"
    fi
    
    return 0
}

# 添加分区
add_partition() {
    echo -e "${BLUE}添加新分区：${NC}"
    
    # 获取分区挂载点
    echo -n "请输入挂载点（如/boot, /, /home等）: "
    read MOUNT_POINT
    
    # 获取分区大小
    echo -n "请输入分区大小（单位GB）: "
    read SIZE
    
    # 验证分区大小
    if ! [[ "$SIZE" =~ ^[0-9]+$ ]] || [ "$SIZE" -le 0 ]; then
        echo -e "${RED}错误：无效的分区大小，请输入正整数。${NC}\n"
        return 1
    fi
    
    # 检查剩余空间
    if (( $(echo "$TOTAL_ALLOCATED + $SIZE > $TOTAL_SIZE" | bc -l) )); then
        echo -e "${RED}错误：空间不足！已分配 $TOTAL_ALLOCATED GB，请求 $SIZE GB，总大小 $TOTAL_SIZE GB。${NC}\n"
        return 1
    fi
    
    # 获取文件系统类型
    echo -e "${BLUE}选择文件系统类型：${NC}"
    echo "1. ext4（通用文件系统，稳定性好）"
    echo "2. xfs（适合大型文件和高吞吐量）"
    echo "3. swap（交换分区）"
    echo "4. btrfs（支持快照和校验和）"
    
    echo -n "请选择 [1-4]（默认1）: "
    read FS_CHOICE
    
    case "$FS_CHOICE" in
        1|"") FS_TYPE="ext4" ;;
        2) FS_TYPE="xfs" ;;
        3) FS_TYPE="swap" ;;
        4) FS_TYPE="btrfs" ;;
        *) echo -e "${RED}无效选择，默认使用ext4。${NC}"; FS_TYPE="ext4" ;;
    esac
    
    # 添加到分区列表
    PARTITION_NUM=$((${#PARTITIONS[@]} + 1))
    PARTITIONS+=([$PARTITION_NUM]="$MOUNT_POINT $SIZE $FS_TYPE")
    TOTAL_ALLOCATED=$(echo "$TOTAL_ALLOCATED + $SIZE" | bc)
    
    echo -e "${GREEN}分区已添加：挂载点=$MOUNT_POINT，大小=${SIZE}GB，文件系统=$FS_TYPE${NC}\n"
    return 0
}

# 显示分区计划
show_partition_plan() {
    echo -e "${BLUE}\n====================================${NC}"
    echo -e "${BLUE}          分区规划方案              ${NC}"
    echo -e "${BLUE}====================================${NC}"
    echo -e "${GREEN}磁盘：$DISK，大小：$TOTAL_SIZE GB${NC}"
    echo -e "${GREEN}分区表类型：$PARTITION_SCHEME${NC}"
    echo -e "${BLUE}------------------------------------${NC}"
    echo -e "${YELLOW}分区号\t挂载点\t大小(GB)\t文件系统${NC}"
    echo -e "${BLUE}------------------------------------${NC}"
    
    for i in "${!PARTITIONS[@]}"; do
        MOUNT_POINT=$(echo "${PARTITIONS[$i]}" | awk '{print $1}')
        SIZE=$(echo "${PARTITIONS[$i]}" | awk '{print $2}')
        FS_TYPE=$(echo "${PARTITIONS[$i]}" | awk '{print $3}')
        echo -e "$i\t$MOUNT_POINT\t$SIZE\t$FS_TYPE"
    done
    
    echo -e "${BLUE}------------------------------------${NC}"
    echo -e "${YELLOW}已分配：$TOTAL_ALLOCATED GB${NC}"
    echo -e "${YELLOW}剩余空间：$(echo "$TOTAL_SIZE - $TOTAL_ALLOCATED" | bc) GB${NC}"
    echo -e "${BLUE}====================================${NC}\n"
}

# 生成分区命令
generate_partition_commands() {
    echo -e "${BLUE}\n====================================${NC}"
    echo -e "${BLUE}        分区命令参考               ${NC}"
    echo -e "${BLUE}====================================${NC}"
    echo -e "${RED}注意：在执行以下命令前，请确保备份所有重要数据！${NC}\n"
    
    echo -e "${YELLOW}1. 执行fdisk命令：${NC}"
    echo "sudo fdisk $DISK"
    
    # MBR分区表命令
    if [ "$PARTITION_SCHEME" = "mbr" ]; then
        echo -e "${YELLOW}\n2. 创建MBR分区表：${NC}"
        echo "Command (m for help): o"
        
        # 为每个分区生成命令
        for i in "${!PARTITIONS[@]}"; do
            MOUNT_POINT=$(echo "${PARTITIONS[$i]}" | awk '{print $1}')
            SIZE=$(echo "${PARTITIONS[$i]}" | awk '{print $2}')
            FS_TYPE=$(echo "${PARTITIONS[$i]}" | awk '{print $3}')
            
            echo -e "${YELLOW}\n3. 创建分区 $i ($MOUNT_POINT):${NC}"
            echo "Command (m for help): n"
            echo "Partition type"
            echo "   p   primary (0 primary, 0 extended, 4 free)"
            echo "   e   extended (container for logical partitions)"
            echo "Select (default p): p"
            echo "Partition number ($i-4, default $i): $i"
            echo "First sector (2048-XXXXXXXXX, default 2048):"
            echo "Last sector, +sectors or +size{K,M,G,T,P} (2048-XXXXXXXXX, default XXXXXXXXX): +${SIZE}G"
            
            # 设置分区类型
            if [ "$FS_TYPE" = "swap" ]; then
                echo -e "${YELLOW}\n4. 设置分区类型为swap:${NC}"
                echo "Command (m for help): t"
                echo "Partition number (1-4): $i"
                echo "Partition type (type L to list all types): 82"
            elif [ "$MOUNT_POINT" = "/boot" ]; then
                # 设置/boot分区为可引导
                echo -e "${YELLOW}\n4. 设置分区为可引导:${NC}"
                echo "Command (m for help): a"
                echo "Partition number (1-4): $i"
            fi
        done
        
        echo -e "${YELLOW}\n5. 保存并退出:${NC}"
        echo "Command (m for help): w"
    fi
    
    # GPT分区表命令
    if [ "$PARTITION_SCHEME" = "gpt" ]; then
        echo -e "${YELLOW}\n2. 创建GPT分区表：${NC}"
        echo "Command (m for help): g"
        
        # 为每个分区生成命令
        for i in "${!PARTITIONS[@]}"; do
            MOUNT_POINT=$(echo "${PARTITIONS[$i]}" | awk '{print $1}')
            SIZE=$(echo "${PARTITIONS[$i]}" | awk '{print $2}')
            FS_TYPE=$(echo "${PARTITIONS[$i]}" | awk '{print $3}')
            
            echo -e "${YELLOW}\n3. 创建分区 $i ($MOUNT_POINT):${NC}"
            echo "Command (m for help): n"
            echo "Partition number ($i-128, default $i): $i"
            echo "First sector (2048-XXXXXXXXX, default 2048):"
            echo "Last sector, +sectors or +size{K,M,G,T,P} (2048-XXXXXXXXX, default XXXXXXXXX): +${SIZE}G"
            
            # 设置分区类型
            echo -e "${YELLOW}\n4. 设置分区类型:${NC}"
            echo "Command (m for help): t"
            echo "Partition number (1-128): $i"
            
            if [ "$FS_TYPE" = "swap" ]; then
                echo "Partition type (type L to list all types): 19"  # Linux swap
            else
                echo "Partition type (type L to list all types): 20"  # Linux filesystem
            fi
        done
        
        echo -e "${YELLOW}\n5. 保存并退出:${NC}"
        echo "Command (m for help): w"
    fi
    
    # 格式化命令
    echo -e "${YELLOW}\n====================================${NC}"
    echo -e "${YELLOW}        格式化命令参考            ${NC}"
    echo -e "${YELLOW}====================================${NC}\n"
    
    for i in "${!PARTITIONS[@]}"; do
        MOUNT_POINT=$(echo "${PARTITIONS[$i]}" | awk '{print $1}')
        FS_TYPE=$(echo "${PARTITIONS[$i]}" | awk '{print $3}')
        
        if [ "$FS_TYPE" = "swap" ]; then
            echo "sudo mkswap ${DISK}${i} -L swap_${MOUNT_POINT//\//_}"
            echo "sudo swapon ${DISK}${i}"
        elif [ "$FS_TYPE" = "ext4" ]; then
            echo "sudo mkfs.ext4 ${DISK}${i} -L ${MOUNT_POINT//\//_}"
        elif [ "$FS_TYPE" = "xfs" ]; then
            echo "sudo mkfs.xfs ${DISK}${i} -L ${MOUNT_POINT//\//_}"
        elif [ "$FS_TYPE" = "btrfs" ]; then
            echo "sudo mkfs.btrfs ${DISK}${i} -L ${MOUNT_POINT//\//_}"
        fi
        
        if [ "$FS_TYPE" != "swap" ]; then
            echo "sudo mkdir -p $MOUNT_POINT"
            echo "sudo mount ${DISK}${i} $MOUNT_POINT"
        fi
        echo
    done
    
    echo -e "${YELLOW}====================================${NC}\n"
    echo -e "${GREEN}分区命令参考生成完成！${NC}\n"
}

# 主菜单
show_menu() {
    echo -e "${BLUE}主菜单：${NC}"
    echo "1. 选择磁盘"
    echo "2. 选择分区表类型"
    echo "3. 添加分区"
    echo "4. 查看分区计划"
    echo "5. 生成分区命令参考"
    echo "6. 退出"
    
    echo -n "请选择 [1-6]: "
    read MENU_CHOICE
    
    return 0
}

# 主函数
main() {
    show_welcome
    
    while true; do
        show_menu
        
        case "$MENU_CHOICE" in
            1) 
                while ! select_disk; do
                    read -p "按Enter键重试..."
                done
                ;;
            2) 
                select_partition_scheme
                ;;
            3) 
                if [ -z "$DISK" ]; then
                    echo -e "${RED}请先选择磁盘！${NC}\n"
                else
                    while ! add_partition; do
                        read -p "按Enter键重试..."
                    done
                fi
                ;;
            4) 
                if [ ${#PARTITIONS[@]} -eq 0 ]; then
                    echo -e "${RED}还没有添加任何分区！${NC}\n"
                else
                    show_partition_plan
                fi
                ;;
            5) 
                if [ ${#PARTITIONS[@]} -eq 0 ]; then
                    echo -e "${RED}还没有添加任何分区！${NC}\n"
                else
                    generate_partition_commands
                fi
                ;;
            6) 
                echo -e "${GREEN}感谢使用磁盘分区规划工具，再见！${NC}\n"
                exit 0
                ;;
            *) 
                echo -e "${RED}无效选择，请重新输入！${NC}\n"
                ;;
        esac
        
        read -p "按Enter键继续..."
        clear
    done
}

# 执行主函数
main
```

通过完成以上练习，您将能够熟练掌握fdisk命令的各种用法，并能够在实际工作中应用它来管理Linux系统的磁盘分区。无论是新硬盘的初始化、现有磁盘分区的调整，还是分区表的备份和恢复，fdisk都是一个功能强大的工具。

需要注意的是，fdisk命令直接操作磁盘分区表，错误使用可能导致数据丢失。因此，在使用fdisk进行任何操作之前，请务必备份重要数据，并确保您了解每个操作的后果。