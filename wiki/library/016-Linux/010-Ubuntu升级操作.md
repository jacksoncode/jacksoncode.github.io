# Ubuntu升级操作

* 查看内核: ``uname -a``
* 查看系统版本: ``lsb_release -a``
* 更新资源: ``sudo apt update``
* 更新软件: ``sudo apt upgrade``
* 删除软件包: ``sudo apt autoremove``
* 更新系统版本: ``sudo apt-get dist-upgrade``
* 升级非LTS版本：
    1. 执行: ``sudo dpkg --force depends -P lxd; sudo dpkg --force depends -P lxd-client``
    2. 执行: ``sudo nano /etc/update-manager/release-upgrades``
    3. 把``Prompt``的值由 ``lts`` 修改成 ``normal``；默认是LTS，只升级到最新的LTS版本；
    4. 按``Ctrl+X`` 保存，再按``Enter``确认文件名。
    5. 执行: ``sudo do-release-upgrade``