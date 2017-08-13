# Waka Time安装方法

官网：https://wakatime.com/dashboard


## eclipse

#### **Install**

1. Click `Help → Eclipse Marketplace…` then search for wakatime.
2. Click `File → WakaTime → API Key` and enter your API key, then click `OK`.
3. Use Eclipse and your coding activity will be displayed on your WakaTime Dashboard.

#### **Upgrading**

1. Inside Eclipse select `Help → Check for Updates`.

#### **Uninstalling**

1. Inside Eclipse, select `Help → About`.
1. Click `Installation Details` button. 
1. Select WakaTime from the list and press `Uninstall…` button and confirm the uninstalling by click `Finish`. 
1. Re-launch Eclipse.


## Notepad++

#### **Installing**

1. Download the latest plugin dll from [GitHub](https://github.com/wakatime/notepadpp-wakatime/releases/latest "GitHub").
1. Save the downloaded .dll to `C:\Program Files\Notepad++\plugins`
1. Create an empty `allowAppDataPlugins.xml` file in your `C:\Program Files\Notepad++` directory.
1. Restart Notepad++.
1. Enter your API key, then press `**enter**`.
1. Use Notepad++ like you normally do and your time will be tracked for you automatically.
1. Visit https://wakatime.com/dashboard to see your coding activity.

#### **Upgrading**
1. Download the latest plugin dll from [GitHub](https://github.com/wakatime/notepadpp-wakatime/releases/latest "GitHub").
1. Save the downloaded .dll to `C:\Program Files\Notepad++\plugins` on overwrite the old one.
1. Relaunch Notepad++.

#### **Uninstalling**
1. Go to `C:\Program Files\Notepad++\plugins`
1. Delete the `WakaTime.dll`.
1. Re-launch Notepad++.

## Atom

1. Inside Atom, navigate to `Preferences` (or `Settings`) → Install and search for `wakatime`.
1. Click the `Install` button.
1. Click the `Settings` button inside the wakatime package.
1. Enter your API key.
1. Use Atom like you normally do and your coding activity will be displayed on your WakaTime Dashboard.
>> Note: The leet way to install WakaTime is with this Terminal command:
    `apm install wakatime`


## Sublime

1. Install Package Control.
1. Inside Sublime, select Tools → Command Palette…
1. Type install, then select Package Control: Install Package and press Enter.
1. Type wakatime, then select WakaTime and press Enter.
1. Enter your API key, then press Enter.
1. Use Sublime and your coding activity will be displayed on your WakaTime Dashboard.

## Pycharm

1. Inside PyCharm, select `Preferences` → `Plugins` → `Browse Repositories…`.
1. Search for `wakatime`.
1. Click the green `Install Plugin` button and confirm the installation.
1. Re-launch PyCharm.
1. Enter your API key, then click `Save`.
1. Use PyCharm like you normally do and your coding activity will be displayed on your WakaTime Dashboard.

> 上面的方法貌似错了。

1. `file > Settings`，然后找到``Plugins``，搜索**waka**。
2. 然后点在线搜索。
3. 重启工具。
4. `Tools > waka time setting`，输入API Key。

## IntelliJ IDEA

与PyCharm安装方法一致。

## WebStorm

与PyCharm安装方法一致。

## NetBeans

1. Download the `.nbm` plugin from [GitHub releases](https://github.com/wakatime/netbeans-wakatime/releases/latest)
1. Inside Netbeans select `Tools → Plugins → Downloaded → Add Plugins…`
1. Select the downloaded nbm file.
1. Check `WakaTime` and click the `Install` button.
1. Follow the wizard instructions to complete the installation.
1. Enter your API key, then click `OK`.
1. Use your IDE like you normally do and your time will be tracked for you automatically.
1. Visit https://wakatime.com/dashboard to see your coding activity.

## VS Code

1. Press `F1` or `CMD + Shift + P` and type `install`. Pick `Extensions: Install Extension`.
1. Type `wakatime` and hit `enter`.
1. Restart Visual Studio Code.
1. Enter your API key, then press `enter`.
1. (If you already have a WakaTime plugin installed, you won't be prompted for your api key.)
1. Use VS Code like you normally do and your coding activity will be displayed on your WakaTime Dashboard.

## Hbuilder

理论上应该和eclipse一样，但实际安装失败。

选择手动安装，输入下面地址。
http://update.dcloud.net.cn/test/plugin_for_test

但貌似里面也没哟waka time？如何破？继续寻找方法。

貌似是h自带的eclipse版本不是最新的，到这里下载匹配的版本试试

https://github.com/wakatime/eclipse-wakatime/tree/master/update-site/plugins

http://marketplace.eclipse.org/content/wakatime

## 安装记录

- eclipse-js		done
- eclipse-java		done
- Hbuilder
- Notepad++			done
- Atom				done
- VSCode			done
- WebStorm			done
- IntelliJ IDEA		done
- PyCharm			done
- Sublime			done
