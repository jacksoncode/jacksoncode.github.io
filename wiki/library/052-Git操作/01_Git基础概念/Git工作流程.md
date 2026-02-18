# Git工作流程

## Git基本工作流程

Git的工作流程围绕三个主要区域展开：工作区、暂存区和Git目录。理解这些区域之间的数据流动是掌握Git的关键。

### 1. 基本工作流程图

```
+-------------+     git add     +--------------+     git commit     +-------------+
|             | -------------> |              | ---------------> |             |
|  工作区     |                |   暂存区     |                  |  Git目录    |
| (Working    | <------------- | (Staging     | <--------------- | (.git)      |
|  Directory) |   git checkout |   Area)      |   git reset     |             |
+-------------+                +--------------+                  +-------------+
       |                               |                               |
       | git diff                      | git diff --staged              | git log
       v                               v                               v
+-------------+                +--------------+                  +-------------+
|  文件修改   |                |  暂存变更    |                  |  历史记录   |
+-------------+                +--------------+                  +-------------+
```

### 2. 详细工作流程

#### 步骤1：在工作区修改文件

```bash
# 查看工作区状态
git status

# 查看文件修改内容
git diff filename
```

#### 步骤2：将修改添加到暂存区

```bash
# 添加单个文件到暂存区
git add filename

# 添加所有修改文件到暂存区
git add .

# 添加特定类型的文件
git add *.py
```

#### 步骤3：提交暂存区的修改

```bash
# 提交暂存区的修改
git commit -m "提交说明"

# 提交并显示详细修改信息
git commit -v

# 修改上一次提交
git commit --amend
```

#### 步骤4：推送到远程仓库（可选）

```bash
# 推送到远程仓库
git push origin branch-name

# 拉取远程仓库更新
git pull origin branch-name
```

## Git文件生命周期

### 文件状态转换

```
未跟踪 (Untracked) → [git add] → 已暂存 (Staged) → [git commit] → 已提交 (Committed)
     ↑                                      ↓
     └────── [删除文件] ←─── 已修改 (Modified) ←─── [修改文件] ←────┘
```

### 各状态详细说明

#### 1. 未跟踪（Untracked）
- 新创建的文件
- Git不管理这些文件
- 需要使用`git add`添加到暂存区

#### 2. 已暂存（Staged）
- 文件已添加到暂存区
- 准备包含在下一次提交中
- 可以使用`git reset HEAD`取消暂存

#### 3. 已修改（Modified）
- 已跟踪文件被修改
- 修改未添加到暂存区
- 需要使用`git add`重新暂存

#### 4. 已提交（Committed）
- 文件已安全保存在Git目录中
- 成为项目历史的一部分
- 可以通过`git checkout`恢复

## 常用Git工作流程模式

### 1. 基本工作流程

适用于个人项目或简单团队协作：

```bash
# 1. 克隆或初始化仓库
git clone <repository-url>
# 或
git init

# 2. 创建或修改文件
# ... 编辑文件 ...

# 3. 查看状态
git status

# 4. 添加修改到暂存区
git add .

# 5. 提交修改
git commit -m "描述修改内容"

# 6. 推送到远程仓库
git push origin main
```

### 2. 功能分支工作流程

适用于团队开发：

```bash
# 1. 创建功能分支
git checkout -b feature/new-feature main

# 2. 在功能分支上开发
# ... 修改文件 ...
git add .
git commit -m "添加新功能"

# 3. 推送功能分支
git push origin feature/new-feature

# 4. 创建Pull Request/Merge Request
# 在GitHub/GitLab上创建合并请求

# 5. 代码审查和合并
# 等待审查通过后合并到主分支

# 6. 删除功能分支（可选）
git branch -d feature/new-feature
git push origin --delete feature/new-feature
```

### 3. Git Flow工作流程

适用于复杂项目和发布管理：

```bash
# 1. 创建功能分支
git checkout -b feature/feature-name develop

# 2. 完成功能开发
git add .
git commit -m "完成功能开发"

# 3. 合并到develop分支
git checkout develop
git merge feature/feature-name

# 4. 创建发布分支
git checkout -b release/v1.0.0 develop

# 5. 测试和修复
# ... 测试和修复 ...
git add .
git commit -m "修复测试发现的问题"

# 6. 合并到main和develop
git checkout main
git merge release/v1.0.0
git checkout develop
git merge release/v1.0.0

# 7. 创建标签
git tag -a v1.0.0 -m "版本1.0.0发布"

# 8. 删除发布分支
git branch -d release/v1.0.0
```

### 4. GitHub Flow工作流程

适用于持续部署的项目：

```bash
# 1. 基于main创建分支
git checkout -b feature/branch-name main

# 2. 在分支上开发
git add .
git commit -m "添加功能"

# 3. 推送分支
git push origin feature/branch-name

# 4. 创建Pull Request
# 在GitHub上创建PR

# 5. 代码审查和部署测试
# 等待CI/CD自动部署测试环境

# 6. 合并到main
git checkout main
git merge feature/branch-name

# 7. 推送main并自动部署
git push origin main
```

## 工作流程最佳实践

### 1. 提交规范

- **原子提交**：每个提交只包含一个逻辑变更
- **清晰的消息**：使用简洁明了的提交消息
- **频繁提交**：小步快跑，避免大提交
- **测试通过**：确保提交的代码能正常工作

### 2. 分支管理

- **主分支保护**：保护main/master分支，直接提交需要权限
- **功能分支**：每个功能使用独立分支
- **定期同步**：定期从主分支同步最新代码
- **及时清理**：合并后及时删除无用分支

### 3. 协作规范

- **代码审查**：所有代码变更都需要经过审查
- **持续集成**：使用CI/CD自动测试和部署
- **文档更新**：代码变更同时更新相关文档
- **问题跟踪**：使用Issue跟踪问题和任务

### 4. 版本管理

- **语义化版本**：遵循语义化版本规范
- **标签管理**：为每个版本创建标签
- **变更日志**：维护详细的变更日志
- **向后兼容**：注意API的向后兼容性

## 常见问题与解决方案

### 1. 工作区混乱

**问题**：工作区有很多未提交的修改，需要清理。

**解决方案**：
```bash
# 查看状态
git status

# 暂存当前工作
git stash

# 清理工作区
git clean -fd

# 恢复暂存的工作
git stash pop
```

### 2. 错误提交到暂存区

**问题**：不小心将错误的文件添加到暂存区。

**解决方案**：
```bash
# 取消暂存单个文件
git reset HEAD filename

# 取消暂存所有文件
git reset HEAD
```

### 3. 提交消息错误

**问题**：提交消息写错了或遗漏了文件。

**解决方案**：
```bash
# 修改上一次提交的消息
git commit --amend -m "新的提交消息"

# 添加遗漏的文件到上一次提交
git add forgotten-file
git commit --amend --no-edit
```

## 总结

Git的工作流程虽然简单，但非常灵活。掌握基本的工作流程和常用的协作模式，将大大提高您的开发效率和团队协作能力。根据项目规模和团队需求选择合适的工作流程，并遵循最佳实践，将帮助您更好地管理项目版本控制。

在实际使用中，建议从小项目开始练习，逐步掌握Git的各种操作，然后再应用到更复杂的项目中。