# Git安装与配置

## Git安装

### Windows系统安装

#### 1. 下载Git安装包

访问Git官方网站下载最新版本的Git安装包：

```bash
# 官方网站
https://git-scm.com/download/win
```

#### 2. 安装步骤

1. **运行安装程序**
   - 双击下载的`.exe`文件
   - 选择语言（推荐选择中文）

2. **选择安装路径**
   - 默认路径：`C:\Program Files\Git`
   - 可以自定义安装路径

3. **选择组件**
   - **Git Bash Here**：右键菜单中添加Git Bash选项
   - **Git GUI Here**：右键菜单中添加Git GUI选项
   - **Git LFS (Large File Storage)**：大文件存储支持
   - **Associate .git* files**：关联.git配置文件

4. **选择启动菜单文件夹**
   - 默认创建"Git"文件夹
   - 可以选择不创建启动菜单项

5. **选择默认编辑器**
   - 推荐选择**Vim**或**Notepad++**
   - 也可以选择其他编辑器如VS Code

6. **调整PATH环境**
   - **Use Git from Git Bash only**：仅在Git Bash中使用Git
   - **Use Git from the Windows Command Prompt**：在命令提示符中使用Git
   - **Use Git and optional Unix tools from the Windows Command Prompt**：添加Unix工具（推荐）

7. **选择HTTPS后端传输**
   - **Use the OpenSSL library**：使用OpenSSL库
   - **Use the native Windows Secure Channel library**：使用Windows安全通道库

8. **配置行结束符转换**
   - **Checkout Windows-style, commit Unix-style line endings**：推荐选项
   - **Checkout as-is, commit Unix-style line endings**：不转换行结束符
   - **Checkout as-is, commit as-is**：完全不做转换

9. **配置终端模拟器**
   - **Use MinTTY**：使用MinTTY终端（推荐）
   - **Use Windows' default console window**：使用Windows默认控制台

10. **配置额外选项**
    - **Enable file system caching**：启用文件系统缓存
    - **Enable Git Credential Manager**：启用凭据管理器
    - **Enable symbolic links**：启用符号链接支持

11. **完成安装**
    - 点击"Install"开始安装
    - 等待安装完成
    - 点击"Finish"完成安装

#### 3. 验证安装

```bash
# 打开Git Bash或命令提示符
git --version

# 预期输出
git version 2.x.x.windows.x
```

### macOS系统安装

#### 1. 使用Homebrew安装（推荐）

```bash
# 安装Homebrew（如果未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装Git
brew install git
```

#### 2. 使用官方安装包

1. 访问Git官方网站：https://git-scm.com/download/mac
2. 下载最新的DMG安装包
3. 双击DMG文件，按照提示安装

#### 3. 验证安装

```bash
git --version
```

### Linux系统安装

#### Ubuntu/Debian系统

```bash
# 更新包管理器
sudo apt update

# 安装Git
sudo apt install git

# 验证安装
git --version
```

#### CentOS/RHEL系统

```bash
# 安装Git
sudo yum install git

# 或使用dnf（新版本）
sudo dnf install git

# 验证安装
git --version
```

#### Arch Linux系统

```bash
# 安装Git
sudo pacman -S git

# 验证安装
git --version
```

## Git配置

### 基本配置

#### 1. 设置用户信息

```bash
# 设置用户名
git config --global user.name "您的姓名"

# 设置邮箱地址
git config --global user.email "your.email@example.com"

# 验证配置
git config --global user.name
git config --global user.email
```

#### 2. 设置默认编辑器

```bash
# 设置为VS Code
git config --global core.editor "code --wait"

# 设置为Vim
git config --global core.editor "vim"

# 设置为Notepad++
git config --global core.editor "'C:/Program Files/Notepad++/notepad++.exe' -multiInst -notabbar -nosession -noPlugin"
```

#### 3. 设置默认分支名

```bash
# 设置默认分支名为main
git config --global init.defaultBranch main
```

### 高级配置

#### 1. 设置代理

```bash
# 设置HTTP代理
git config --global http.proxy http://proxy.server.com:8080

# 设置HTTPS代理
git config --global https.proxy https://proxy.server.com:8080

# 取消代理设置
git config --global --unset http.proxy
git config --global --unset https.proxy
```

#### 2. 设置凭据缓存

```bash
# 设置凭据缓存（默认15分钟）
git config --global credential.helper cache

# 设置缓存时间为1小时
git config --global credential.helper 'cache --timeout=3600'

# 使用系统凭据管理器（Windows）
git config --global credential.helper manager

# 使用系统钥匙串（macOS）
git config --global credential.helper osxkeychain
```

#### 3. 设置别名

```bash
# 常用别名设置
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.lg "log --oneline --graph --decorate --all"

# 查看所有别名
git config --global --get-regexp alias
```

#### 4. 设置行结束符

```bash
# Windows系统推荐设置
git config --global core.autocrlf true

# Linux/macOS系统推荐设置
git config --global core.autocrlf input

# 禁用行结束符转换
git config --global core.autocrlf false
```

#### 5. 设置文件权限

```bash
# 设置文件权限为可执行（Linux/macOS）
git config --global core.filemode true

# 禁用文件权限检查
git config --global core.filemode false
```

### 配置文件位置

Git配置文件有三个级别，按优先级从高到低：

#### 1. 本地配置（项目级别）

```bash
# 配置文件位置：.git/config
# 仅对当前项目有效

git config user.name "项目特定姓名"
git config user.email "项目特定邮箱"
```

#### 2. 全局配置（用户级别）

```bash
# 配置文件位置：~/.gitconfig（Linux/macOS）或 ~/.gitconfig（Windows）
# 对当前用户所有项目有效

git config --global user.name "全局用户名"
git config --global user.email "全局邮箱"
```

#### 3. 系统配置（系统级别）

```bash
# 配置文件位置：/etc/gitconfig（Linux/macOS）或 C:\Program Files\Git\etc\gitconfig（Windows）
# 对系统所有用户有效

git config --system core.editor "vim"
```

### 查看配置

```bash
# 查看所有配置
git config --list

# 查看特定配置
git config user.name

# 查看配置文件位置
git config --global --edit

# 查看本地配置
git config --local --list

# 查看全局配置
git config --global --list

# 查看系统配置
git config --system --list
```

## SSH密钥配置

### 生成SSH密钥

#### 1. 生成新的SSH密钥

```bash
# 生成RSA密钥（推荐）
ssh-keygen -t rsa -b 4096 -C "your.email@example.com"

# 生成ED25519密钥（更安全）
ssh-keygen -t ed25519 -C "your.email@example.com"
```

#### 2. 设置密钥密码（可选）

```bash
# 生成密钥时会提示设置密码
# 建议设置密码以提高安全性
```

### 添加SSH密钥到ssh-agent

#### 1. 启动ssh-agent

```bash
# Linux/macOS
eval "$(ssh-agent -s)"

# Windows (Git Bash)
eval $(ssh-agent -s)
```

#### 2. 添加私钥到ssh-agent

```bash
# 添加默认密钥
ssh-add ~/.ssh/id_rsa

# 添加特定密钥
ssh-add ~/.ssh/id_ed25519
```

### 添加SSH公钥到Git服务

#### 1. 查看公钥内容

```bash
# 查看RSA公钥
cat ~/.ssh/id_rsa.pub

# 查看ED25519公钥
cat ~/.ssh/id_ed25519.pub
```

#### 2. 复制公钥到剪贴板

```bash
# Linux/macOS
cat ~/.ssh/id_rsa.pub | pbcopy  # macOS
cat ~/.ssh/id_rsa.pub | xclip -sel clip  # Linux

# Windows (Git Bash)
cat ~/.ssh/id_rsa.pub | clip
```

#### 3. 在Git服务中添加公钥

**GitHub**：
1. 登录GitHub
2. 点击右上角头像 → Settings
3. 左侧菜单点击SSH and GPG keys
4. 点击New SSH key
5. 粘贴公钥内容并保存

**GitLab**：
1. 登录GitLab
2. 点击右上角头像 → Settings
3. 左侧菜单点击SSH Keys
4. 粘贴公钥内容并保存

**Gitee**：
1. 登录Gitee
2. 点击右上角头像 → 设置
3. 左侧菜单点击SSH公钥
4. 粘贴公钥内容并保存

### 测试SSH连接

```bash
# 测试GitHub连接
ssh -T git@github.com

# 测试GitLab连接
ssh -T git@gitlab.com

# 测试Gitee连接
ssh -T git@gitee.com
```

## 常见问题与解决方案

### 1. Git命令找不到

**问题**：在命令提示符中输入`git`命令提示"'git' 不是内部或外部命令"。

**解决方案**：
```bash
# 检查PATH环境变量
echo %PATH%

# 确保Git安装路径在PATH中
# 通常为：C:\Program Files\Git\cmd
```

### 2. SSH连接失败

**问题**：使用SSH连接Git服务时失败。

**解决方案**：
```bash
# 检查SSH代理状态
eval "$(ssh-agent -s)"

# 添加密钥
ssh-add ~/.ssh/id_rsa

# 测试连接
ssh -T git@github.com

# 查看详细错误信息
ssh -vT git@github.com
```

### 3. 权限问题

**问题**：Git操作时出现权限错误。

**解决方案**：
```bash
# 检查文件权限
ls -la ~/.ssh/

# 设置正确的权限
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
```

### 4. 配置不生效

**问题**：修改配置后不生效。

**解决方案**：
```bash
# 检查配置文件位置
git config --list --show-origin

# 确保配置在正确的级别
# 本地配置会覆盖全局配置
```

## 最佳实践

### 1. 配置管理

- **统一用户信息**：在全局配置中设置统一的用户名和邮箱
- **项目特定配置**：对于需要不同身份的项目，使用本地配置
- **定期备份**：备份配置文件以便在新环境中快速恢复

### 2. 安全性

- **使用SSH**：优先使用SSH协议而不是HTTPS
- **密钥保护**：为SSH私钥设置密码
- **凭据管理**：使用安全的凭据管理器

### 3. 性能优化

- **启用缓存**：启用文件系统缓存提高性能
- **合理设置**：根据网络环境设置合适的代理和缓存策略
- **定期清理**：定期清理不必要的文件和缓存

## 总结

Git的安装和配置是使用Git的第一步，也是最重要的一步。正确的安装和配置能够确保后续的Git操作顺利进行。本章节详细介绍了在不同操作系统上安装Git的方法，以及Git的基本配置和高级配置选项。

建议您按照本章节的指导完成Git的安装和配置，并根据实际需求调整相关设置。良好的配置习惯将为您后续的Git使用打下坚实的基础。

在下一章节中，我们将学习Git的基础命令，开始实际使用Git进行版本控制。