# Git高级技巧

## 高级技巧概述

Git高级技巧是指那些能够显著提高开发效率、解决复杂问题的高级用法和技巧。掌握这些技巧可以让开发者更加高效地使用Git。

### 高级技巧的价值

- **提高效率**：减少重复操作，提高工作效率
- **解决问题**：解决复杂的版本控制问题
- **优化流程**：优化开发流程和协作方式
- **减少错误**：减少人为错误和操作失误
- **提升技能**：提升Git使用技能和专业水平

### 适用场景

- **大型项目**：复杂的项目结构和历史
- **团队协作**：多人协作的复杂场景
- **问题修复**：复杂的问题修复和回滚
- **性能优化**：Git性能优化和调优
- **自动化**：自动化Git操作和流程

## 高级配置技巧

### Git配置优化

#### 1. 全局配置

```bash
# 设置用户信息
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 设置默认编辑器
git config --global core.editor "vim"

# 设置默认分支名称
git config --global init.defaultBranch main

# 设置凭证缓存
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=3600'

# 设置代理
git config --global http.proxy http://proxy.example.com:8080
git config --global https.proxy https://proxy.example.com:8080

# 设置换行符处理
git config --global core.autocrlf input  # Linux/Mac
git config --global core.autocrlf true   # Windows
```

#### 2. 项目配置

```bash
# 设置项目特定的用户信息
git config user.name "Project User"
git config user.email "project@example.com"

# 设置项目特定的忽略文件
git config core.excludesfile .gitignore

# 设置项目特定的合并工具
git config merge.tool vscode
git config mergetool.vscode.cmd "code --wait $MERGED"

# 设置项目特定的差异工具
git config diff.tool vscode
git config difftool.vscode.cmd "code --wait --diff $LOCAL $REMOTE"

# 设置项目特定的别名
git config alias.st status
git config alias.co checkout
git config alias.br branch
git config alias.ci commit
git config alias.di diff
```

#### 3. 系统配置

```bash
# 设置系统级别的配置（需要管理员权限）
git config --system core.pager "less -FRSX"
git config --system receive.denyNonFastForwards true
git config --system receive.denyDeletes true

# 设置系统级别的安全配置
git config --system safe.directory '*'

# 设置系统级别的性能配置
git config --system pack.threads "4"
git config --system pack.windowMemory "512m"
git config --system pack.packSizeLimit "512m"
```

### 别名配置

#### 1. 常用别名

```bash
# 基础命令别名
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.di diff

# 日志查看别名
git config --global alias.lg "log --oneline --graph --decorate --all"
git config --global alias.ll "log --oneline --graph"
git config --global alias.ls "log --stat"
git config --global alias.lt "log --oneline --graph --decorate"

# 分支管理别名
git config --global alias.ba "branch -a"
git config --global alias.bd "branch -d"
git config --global alias.bD "branch -D"
git config --global alias.bm "branch -m"
```

#### 2. 高级别名

```bash
# 复杂操作别名
git config --global alias.unstage "reset HEAD --"
git config --global alias.last "log -1 HEAD"
git config --global alias.uncommit "reset --soft HEAD~1"
git config --global alias.amend "commit --amend --no-edit"

# 查看特定内容别名
git config --global alias.filelog "log -u"
git config --global alias.fl "log -u"
git config --global alias.changes "show --stat --pretty=format:%h"

# 清理别名
git config --global alias.cleanup "!git branch --merged | grep -v '\*' | xargs git branch -d"
git config --global alias.prune "!git remote prune origin"
```

#### 3. 自定义函数别名

```bash
# 自定义函数别名
git config --global alias.count "!f() { git log --oneline $@ | wc -l; }; f"
git config --global alias.recent "!f() { git log --oneline --since='$1' --until='$2'; }; f"
git config --global alias.find "!f() { git log --grep='$1' --oneline; }; f"

# 统计别名
git config --global alias.stats "!git log --shortstat --author=\"$1\" | grep '\"files changed\"' | awk '{files+=$1; inserted+=$4; deleted+=$6} END {print \"files changed:\", files, \"insertions:\", inserted, \"deletions:\", deleted}'"

# 搜索别名
git config --global alias.search "!f() { git log -S\"$1\" --source --all; }; f"
git config --global alias.grep "!f() { git rev-list --all | xargs git grep \"$1\"; }; f"
```

### 钩子配置

#### 1. 客户端钩子

```bash
# 创建pre-commit钩子
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# 运行代码检查
npm run lint
if [ $? -ne 0 ]; then
    echo "代码检查失败，请修复错误后再提交"
    exit 1
fi

# 运行测试
npm test
if [ $? -ne 0 ]; then
    echo "测试失败，请修复错误后再提交"
    exit 1
fi

# 检查大文件
MAX_SIZE=$((5 * 1024 * 1024))  # 5MB
git diff --cached --name-only | while read file; do
    if [ -f "$file" ]; then
        size=$(stat -c%s "$file")
        if [ $size -gt $MAX_SIZE ]; then
            echo "错误：文件 $file 大小超过限制 ($size bytes)"
            exit 1
        fi
    fi
done

exit 0
EOF

chmod +x .git/hooks/pre-commit
```

#### 2. 服务端钩子

```bash
# 创建pre-receive钩子
cat > .git/hooks/pre-receive << 'EOF'
#!/bin/bash

# 读取推送信息
while read oldrev newrev refname; do
    # 检查分支保护
    if [ "$refname" = "refs/heads/main" ]; then
        # 检查是否为强制推送
        if [ "$oldrev" != "0000000000000000000000000000000000000000" ]; then
            # 检查提交数量
            commit_count=$(git rev-list --count $oldrev..$newrev)
            if [ $commit_count -gt 10 ]; then
                echo "错误：main分支提交数量过多 ($commit_count)"
                exit 1
            fi
        fi
    fi
    
    # 检查提交信息格式
    git rev-list $oldrev..$newrev | while read commit; do
        message=$(git log --format=%B -n 1 $commit)
        if ! echo "$message" | grep -qE "^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: "; then
            echo "错误：提交信息格式不正确"
            echo "提交 $commit: $message"
            exit 1
        fi
    done
done

exit 0
EOF

chmod +x .git/hooks/pre-receive
```

#### 3. 自定义钩子

```bash
# 创建commit-msg钩子
cat > .git/hooks/commit-msg << 'EOF'
#!/bin/bash

# 检查提交信息格式
message_file="$1"
message=$(cat "$message_file")

# 检查是否包含Issue编号
if ! echo "$message" | grep -qE "#[0-9]+"; then
    echo "警告：提交信息未包含Issue编号"
    echo "建议格式：type(scope): description #123"
    read -p "是否继续提交？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 检查提交信息长度
if [ ${#message} -gt 72 ]; then
    echo "警告：提交信息过长（${#message}字符）"
    echo "建议每行不超过72个字符"
fi

exit 0
EOF

chmod +x .git/hooks/commit-msg
```

## 高级日志技巧

### 日志格式化

#### 1. 基本格式化

```bash
# 简单单行格式
git log --oneline

# 带图形的单行格式
git log --oneline --graph

# 带装饰的单行格式
git log --oneline --decorate

# 带作者信息的格式
git log --pretty=format:"%h - %an, %ar : %s"

# 完整格式化
git log --pretty=format:"%H - %an (%ae), %ar : %s"
```

#### 2. 自定义格式化

```bash
# 自定义提交信息格式
git log --pretty=format:"%C(red)%h%C(reset) - %C(yellow)%an%C(reset), %C(green)%ar%C(reset) : %C(blue)%s%C(reset)"

# 带分支信息的格式
git log --pretty=format:"%C(red)%h%C(reset) - %C(yellow)%d%C(reset) %C(blue)%s%C(reset) %C(green)(%cr)%C(reset) %C(cyan)<%an>%C(reset)"

# 带文件变更的格式
git log --pretty=format:"%h %s" --name-status

# 带统计信息的格式
git log --pretty=format:"%h %s" --stat

# 带时间线的格式
git log --pretty=format:"%h %ad %s" --date=short --graph
```

#### 3. 复杂格式化

```bash
# 创建自定义日志格式
git config --global alias.lg1 "log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(bold yellow)%d%C(reset)' --all"

git config --global alias.lg2 "log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold cyan)%aD%C(reset) %C(bold green)(%ar)%C(reset)%C(bold yellow)%d%C(reset)%n''          %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(dim white) (%ae)%C(reset)' --all"

git config --global alias.lg3 "log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold cyan)%aD%C(reset) %C(bold green)(%ar)%C(reset)%C(bold yellow)%d%C(reset)%n''          %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(dim white) (%ae)%C(reset)'"

# 使用自定义格式
git lg1
git lg2
git lg3
```

### 日志过滤

#### 1. 按时间过滤

```bash
# 显示最近7天的提交
git log --since="7 days ago"

# 显示特定日期范围的提交
git log --since="2024-01-01" --until="2024-01-31"

# 显示昨天的提交
git log --since="yesterday"

# 显示本周的提交
git log --since="Monday"

# 显示上个月的提交
git log --since="1 month ago"
```

#### 2. 按作者过滤

```bash
# 显示特定作者的提交
git log --author="John Doe"

# 显示多个作者的提交
git log --author="John\|Jane"

# 显示不包含特定作者的提交
git log --author="^John"

# 显示作者邮箱包含特定域名的提交
git log --author="@example.com"

# 显示作者姓名包含特定字符串的提交
git log --author="Doe"
```

#### 3. 按内容过滤

```bash
# 显示包含特定字符串的提交
git log -S"function_name"

# 显示修改特定文件的提交
git log -- path/to/file.js

# 显示修改特定目录的提交
git log -- src/components/

# 显示合并提交
git log --merges

# 显示非合并提交
git log --no-merges

# 显示特定类型的提交
git log --grep="fix" --grep="feat" --grep="docs"
```

### 日志分析

#### 1. 统计分析

```bash
# 统计每个作者的提交数量
git shortlog -s -n

# 统计每个作者的代码行数
git log --numstat --format="%an" | awk 'NF==3 {plus+=$1; minus+=$2} NF==1 {author=$0} END {print author, "+" plus, "-" minus}'

# 统计文件变更数量
git log --numstat --format="%H" | awk '{if(NF==3) files++} END {print "Files changed:", files}'

# 统计提交频率
git log --format="%ad" --date=short | sort | uniq -c

# 统计每日提交数量
git log --format="%ad" --date=format:"%Y-%m-%d" | sort | uniq -c
```

#### 2. 贡献分析

```bash
# 分析代码贡献者
git log --format="%an" | sort | uniq -c | sort -nr

# 分析文件贡献者
git blame path/to/file.js | awk '{print $2}' | sort | uniq -c | sort -nr

# 分析特定时间段的贡献
git log --since="2024-01-01" --until="2024-01-31" --format="%an" | sort | uniq -c | sort -nr

# 分析分支贡献
git log main..feature-branch --format="%an" | sort | uniq -c | sort -nr

# 分析标签贡献
git log v1.0.0..v2.0.0 --format="%an" | sort | uniq -c | sort -nr
```

#### 3. 趋势分析

```bash
# 分析提交趋势
git log --format="%ad" --date=format:"%Y-%m" | sort | uniq -c | awk '{print $2, $1}' | sort

# 分析代码增长趋势
git log --format="%H" --numstat | awk '{if(NF==3) {plus+=$1; minus+=$2}} END {print "Net change:", plus-minus, "(+" plus, "-" minus ")"}'

# 分析文件大小变化
git log --format="%H" --numstat | awk '{if(NF==3) {files++}} END {print "Total files changed:", files}'

# 分析团队活跃度
git log --format="%ad %an" --date=format:"%Y-%m-%d" | awk '{print $1}' | sort | uniq -c | sort -nr

# 分析项目进度
git log --format="%s" | grep -E "(feat|fix)" | wc -l
```

## 高级分支技巧

### 分支操作

#### 1. 分支创建与管理

```bash
# 基于特定提交创建分支
git branch feature/new-feature abc1234

# 基于标签创建分支
git branch release/v1.0.0 v1.0.0

# 基于远程分支创建本地分支
git branch feature/local-feature origin/feature/remote-feature

# 创建孤儿分支（没有历史记录）
git checkout --orphan new-branch

# 创建并切换到新分支
git checkout -b feature/new-feature

# 创建跟踪远程分支的本地分支
git checkout -b feature/local-feature origin/feature/remote-feature
```

#### 2. 分支比较

```bash
# 比较两个分支的差异
git diff branch1..branch2

# 比较分支的统计信息
git diff --stat branch1..branch2

# 比较分支的文件列表
git diff --name-status branch1..branch2

# 比较分支的共同祖先
git merge-base branch1 branch2

# 比较分支的三向差异
git diff branch1...branch2

# 比较分支的特定文件
git diff branch1..branch2 -- path/to/file.js
```

#### 3. 分支清理

```bash
# 删除已合并的本地分支
git branch --merged | grep -v '\*' | xargs git branch -d

# 删除已合并的远程分支
git branch -r --merged | grep -v '\*/main' | sed 's/origin\///' | xargs -I {} git push origin --delete {}

# 删除所有包含特定模式的分支
git branch | grep 'feature/' | xargs git branch -D

# 清理过时的远程分支引用
git remote prune origin

# 删除不存在的远程分支的本地引用
git fetch --prune

# 清理所有分支（保留main和当前分支）
git branch | grep -v '\*' | grep -v 'main' | xargs git branch -D
```

### 分支策略

#### 1. 功能分支策略

```bash
# 功能分支工作流程
# 1. 创建功能分支
git checkout -b feature/user-authentication main

# 2. 开发功能
git add .
git commit -m "feat(auth): add user authentication"

# 3. 同步主分支
git fetch origin
git rebase origin/main

# 4. 推送分支
git push origin feature/user-authentication

# 5. 创建Pull Request
# 在GitHub上创建PR

# 6. 合并分支
git checkout main
git merge --no-ff feature/user-authentication
git push origin main

# 7. 删除分支
git branch -d feature/user-authentication
git push origin --delete feature/user-authentication
```

#### 2. 发布分支策略

```bash
# 发布分支工作流程
# 1. 创建发布分支
git checkout -b release/v1.0.0 main

# 2. 发布准备
git add .
git commit -m "release: prepare v1.0.0"

# 3. 合并到主分支
git checkout main
git merge --no-ff release/v1.0.0
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin main
git push origin --tags

# 4. 合并到开发分支
git checkout develop
git merge --no-ff release/v1.0.0
git push origin develop

# 5. 删除发布分支
git branch -d release/v1.0.0
```

#### 3. 热修复分支策略

```bash
# 热修复分支工作流程
# 1. 创建热修复分支
git checkout -b hotfix/security-patch main

# 2. 修复问题
git add .
git commit -m "fix(security): patch security vulnerability"

# 3. 合并到主分支
git checkout main
git merge --no-ff hotfix/security-patch
git tag -a v1.0.1 -m "Version 1.0.1"
git push origin main
git push origin --tags

# 4. 合并到开发分支
git checkout develop
git merge --no-ff hotfix/security-patch
git push origin develop

# 5. 删除热修复分支
git branch -d hotfix/security-patch
```

### 分支保护

#### 1. 分支保护设置

```bash
# 设置分支保护规则
git config branch.main.protection true

# 禁止直接推送到主分支
git config branch.main.protection.requirePullRequest true

# 要求CI检查通过
git config branch.main.protection.requireCI true

# 要求代码审查
git config branch.main.protection.requireReview true

# 设置审查者数量
git config branch.main.protection.requiredReviewers 2

# 设置状态检查
git config branch.main.protection.requiredStatusChecks "ci/test,ci/lint"
```

#### 2. GitHub分支保护

```bash
# 使用GitHub CLI设置分支保护
gh api repos/:owner/:repo/branches/main/protection \
  -X PUT \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{
    "required_status_checks": {
      "strict": true,
      "contexts": ["ci/test", "ci/lint"]
    },
    "enforce_admins": true,
    "required_pull_request_reviews": {
      "required_approving_review_count": 2,
      "dismiss_stale_reviews": true
    },
    "restrictions": null
  }'
```

#### 3. GitLab分支保护

```bash
# 使用GitLab API设置分支保护
curl --request POST \
  --header "PRIVATE-TOKEN: your-token" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "main",
    "push_access_level": 0,
    "merge_access_level": 30,
    "unprotect_access_level": 40
  }' \
  "https://gitlab.example.com/api/v4/projects/:id/protected_branches"
```

## 高级合并技巧

### 合并策略

#### 1. 快进合并

```bash
# 快进合并（当可能时）
git merge --ff-only feature-branch

# 强制快进合并
git merge --ff feature-branch

# 检查是否可以快进合并
git merge-base --is-ancestor feature-branch main

# 执行快进合并
git checkout main
git merge feature-branch
```

#### 2. 三向合并

```bash
# 三向合并（创建合并提交）
git merge --no-ff feature-branch

# 压缩合并（将多个提交合并为一个）
git merge --squash feature-branch

# 递归合并（处理复杂合并）
git merge --recursive feature-branch

# 策略合并（指定合并策略）
git merge -s recursive -X theirs feature-branch
git merge -s recursive -X ours feature-branch
```

#### 3. 高级合并策略

```bash
# 子树合并
git merge -s subtree feature-branch

# 章节合并（合并特定提交）
git merge --cherry-pick feature-branch

# 八爪鱼合并（处理多个共同祖先）
git merge -s octopus branch1 branch2 branch3

# 策略选择合并
git merge -X patience feature-branch
git merge -X histinfo feature-branch
```

### 合并冲突解决

#### 1. 基本冲突解决

```bash
# 查看冲突状态
git status

# 查看冲突文件
git diff --name-only --diff-filter=U

# 查看冲突内容
git diff --diff-filter=U

# 手动解决冲突
vim conflicted-file.js

# 标记冲突已解决
git add conflicted-file.js

# 完成合并
git commit -m "解决合并冲突"
```

#### 2. 使用合并工具

```bash
# 配置合并工具
git config merge.tool vscode
git config mergetool.vscode.cmd "code --wait $MERGED"

# 使用合并工具解决冲突
git mergetool

# 使用特定合并工具
git mergetool --tool=vimdiff

# 自动解决简单冲突
git checkout --ours path/to/file.js  # 保留当前分支版本
git checkout --theirs path/to/file.js  # 保留合并分支版本

# 查看合并基础
git merge-base HEAD MERGE_HEAD
```

#### 3. 高级冲突解决

```bash
# 使用git rerere记录冲突解决方案
git config --global rerere.enabled true
git config --global rerere.autoupdate true

# 查看rerere状态
git rerere status

# 查看rerere解决方案
git rerere diff

# 放弃合并
git merge --abort

# 继续合并
git merge --continue

# 重新开始合并
git merge --abort
git merge feature-branch
```

### 合并优化

#### 1. 合并前准备

```bash
# 在合并前同步主分支
git checkout feature-branch
git fetch origin
git rebase origin/main

# 检查合并冲突
git merge --no-commit --no-ff origin/main
git merge --abort

# 清理提交历史
git rebase -i origin/main

# 运行测试
git checkout feature-branch
npm test
```

#### 2. 合并后处理

```bash
# 验证合并结果
git checkout main
git merge feature-branch

# 运行测试
npm test

# 检查构建
npm run build

# 如果有问题，回滚合并
git reset --hard HEAD~1

# 或者使用revert
git revert -m 1 HEAD
```

#### 3. 合并最佳实践

```bash
# 定期合并主分支
git checkout feature-branch
git fetch origin
git rebase origin/main

# 保持分支简洁
git rebase -i origin/main

# 使用有意义的提交信息
git commit -m "feat(auth): add user authentication"

# 合并前测试
git checkout feature-branch
npm test

# 合并后验证
git checkout main
git merge feature-branch
npm test
```

## 高级重置技巧

### 重置操作

#### 1. 软重置

```bash
# 软重置（保留工作目录和暂存区）
git reset --soft HEAD~1

# 软重置到特定提交
git reset --soft abc1234

# 软重置后重新提交
git reset --soft HEAD~1
git commit -m "新的提交信息"

# 查看软重置后的状态
git status
git diff --cached
```

#### 2. 混合重置

```bash
# 混合重置（保留工作目录，清空暂存区）
git reset --mixed HEAD~1

# 混合重置到特定提交
git reset --mixed abc1234

# 混合重置后重新暂存
git reset --mixed HEAD~1
git add .
git commit -m "重新提交"

# 查看混合重置后的状态
git status
git diff
```

#### 3. 硬重置

```bash
# 硬重置（清空工作目录和暂存区）
git reset --hard HEAD~1

# 硬重置到特定提交
git reset --hard abc1234

# 硬重置到远程分支
git reset --hard origin/main

# 警告：硬重置会丢失未提交的更改
# 确保已保存重要更改后再执行
```

### 变基操作

#### 1. 基本变基

```bash
# 变基到主分支
git checkout feature-branch
git rebase main

# 变基到特定提交
git rebase abc1234

# 交互式变基
git rebase -i main

# 变基时跳过提交
git rebase --skip

# 放弃变基
git rebase --abort
```

#### 2. 高级变基

```bash
# 变基时自动解决冲突
git rebase --continue

# 变基时保留提交信息
git rebase --preserve-merges main

# 变基时压缩提交
git rebase -i main
# 在编辑器中将pick改为squash

# 变基时重新排序提交
git rebase -i main
# 在编辑器中重新排序提交

# 变基时编辑提交
git rebase -i main
# 在编辑器中将pick改为edit
```

#### 3. 变基策略

```bash
# 变基前同步主分支
git checkout feature-branch
git fetch origin
git rebase origin/main

# 变基后强制推送
git push --force-with-lease origin feature-branch

# 变基时避免冲突
git rebase -X theirs main
git rebase -X ours main

# 变基时保留空提交
git rebase --empty=keep main

# 变基时跳过空提交
git rebase --empty=drop main
```

### 撤销操作

#### 1. 撤销提交

```bash
# 撤销最后一次提交（保留更改）
git reset --soft HEAD~1

# 撤销最后一次提交（丢弃更改）
git reset --hard HEAD~1

# 撤销特定提交
git revert abc1234

# 撤销合并提交
git revert -m 1 HEAD

# 撤销多个提交
git revert HEAD~3..HEAD
```

#### 2. 撤销合并

```bash
# 撤销合并提交
git revert -m 1 HEAD

# 撤销合并并保留更改
git reset --soft HEAD~1

# 撤销合并并丢弃更改
git reset --hard HEAD~1

# 撤销合并后重新合并
git revert -m 1 HEAD
git merge feature-branch

# 撤销合并后变基
git reset --hard HEAD~1
git rebase main
```

#### 3. 撤销推送

```bash
# 撤销已推送的提交
git reset --hard HEAD~1
git push --force-with-lease origin main

# 撤销多个已推送的提交
git reset --hard HEAD~3
git push --force-with-lease origin main

# 撤销推送并重新提交
git reset --soft HEAD~1
git commit -m "修正提交"
git push --force-with-lease origin main

# 撤销推送并变基
git reset --hard HEAD~1
git rebase main
git push --force-with-lease origin main
```

## 高级搜索技巧

### 内容搜索

#### 1. 搜索文件内容

```bash
# 搜索包含特定字符串的文件
git grep "search_string"

# 搜索特定文件类型
git grep "search_string" -- *.js

# 搜索特定目录
git grep "search_string" -- src/

# 搜索并显示行号
git grep -n "search_string"

# 搜索并显示文件名
git grep -l "search_string"
```

#### 2. 搜索提交历史

```bash
# 搜索提交信息
git log --grep="search_string"

# 搜索特定作者的提交
git log --author="author_name"

# 搜索特定时间段的提交
git log --since="2024-01-01" --until="2024-01-31"

# 搜索修改特定文件的提交
git log -- path/to/file.js

# 搜索包含特定字符串的提交
git log -S"search_string"
```

#### 3. 高级搜索

```bash
# 搜索并统计
git grep -c "search_string"

# 搜索并显示上下文
git grep -C 3 "search_string"

# 搜索并显示前后行
git grep -A 2 -B 2 "search_string"

# 搜索并忽略大小写
git grep -i "search_string"

# 搜索并使用正则表达式
git grep -E "regex_pattern"
```

### 文件搜索

#### 1. 搜索文件名

```bash
# 搜索特定文件名
git ls-files | grep "filename"

# 搜索特定扩展名的文件
git ls-files "*.js"

# 搜索特定目录的文件
git ls-files "src/"

# 搜索被删除的文件
git ls-files --deleted

# 搜索被修改的文件
git ls-files --modified
```

#### 2. 搜索文件状态

```bash
# 搜索未跟踪的文件
git ls-files --others

# 搜索已暂存的文件
git ls-files --cached

# 搜索被忽略的文件
git ls-files --ignored

# 搜索冲突的文件
git ls-files --unmerged

# 搜索特定状态的文件
git ls-files --stage
```

#### 3. 搜索文件历史

```bash
# 搜索文件的历史版本
git log --follow path/to/file.js

# 搜索文件的重命名历史
git log --follow --name-status path/to/file.js

# 搜索文件的删除历史
git log --diff-filter=D -- path/to/file.js

# 搜索文件的创建历史
git log --diff-filter=A -- path/to/file.js

# 搜索文件的修改历史
git log -- path/to/file.js
```

### 提交搜索

#### 1. 搜索提交信息

```bash
# 搜索包含特定关键词的提交
git log --grep="keyword"

# 搜索多个关键词
git log --grep="keyword1" --grep="keyword2"

# 搜索不包含特定关键词的提交
git log --grep="keyword" --invert-grep

# 搜索特定类型的提交
git log --grep="^feat:" --grep="^fix:"

# 搜索包含Issue编号的提交
git log --grep="#123"
```

#### 2. 搜索提交内容

```bash
# 搜索添加特定字符串的提交
git log -S"added_string"

# 搜索删除特定字符串的提交
git log -S"removed_string"

# 搜索修改特定字符串的提交
git log -G"modified_pattern"

# 搜索修改特定文件的提交
git log -- path/to/file.js

# 搜索修改特定函数的提交
git log -L :function_name:path/to/file.js
```

#### 3. 搜索提交范围

```bash
# 搜索两个提交之间的差异
git log commit1..commit2

# 搜索包含特定提交的分支
git branch --contains commit_hash

# 搜索不包含特定提交的分支
git branch --no-contains commit_hash

# 搜索特定标签的提交
git log v1.0.0..v2.0.0

# 搜索特定时间段的提交
git log --since="2024-01-01" --until="2024-01-31"
```

## 高级性能优化

### 仓库优化

#### 1. 垃圾回收

```bash
# 运行垃圾回收
git gc

# 激进垃圾回收
git gc --aggressive

# 清理未引用的对象
git prune

# 清理过时的远程分支
git remote prune origin

# 清理未跟踪的文件
git clean -fd
```

#### 2. 仓库压缩

```bash
# 压缩仓库
git repack -a -d --depth=250 --window=250

# 深度压缩
git repack -a -d --depth=50 --window=50

# 优化包文件
git pack-refs --all

# 清理历史
git filter-branch --prune-empty --subdirectory-filter path/to/subdir

# 重写历史
git filter-repo --force path/to/subdir
```

#### 3. 仓库维护

```bash
# 检查仓库完整性
git fsck

# 检查并修复损坏的对象
git fsck --full

# 检查未引用的对象
git fsck --unreachable

# 检查丢失的对象
git fsck --lost-found

# 检查 dangling的对象
git fsck --dangling
```

### 网络优化

#### 1. 克隆优化

```bash
# 浅克隆（只获取最新提交）
git clone --depth 1 https://github.com/user/repo.git

# 单分支克隆
git clone --branch main --single-branch https://github.com/user/repo.git

# 部分克隆（只获取特定文件）
git clone --filter=blob:none https://github.com/user/repo.git

# 稀疏克隆（只获取特定目录）
git clone --sparse https://github.com/user/repo.git
cd repo
git sparse-checkout init --cone
git sparse-checkout set path/to/directory
```

#### 2. 推送优化

```bash
# 并行推送
git config --global push.default matching
git config --global fetch.parallel 8

# 增量推送
git push --progress

# 压缩推送
git config --global pack.compression 9

# 推送特定分支
git push origin main

# 推送所有分支
git push --all origin
```

#### 3. 拉取优化

```bash
# 并行拉取
git config --global fetch.parallel 8

# 增量拉取
git pull --progress

# 压缩拉取
git config --global pack.compression 9

# 拉取特定分支
git pull origin main

# 拉取所有分支
git fetch --all
```

### 内存优化

#### 1. 配置优化

```bash
# 设置内存限制
git config --global pack.windowMemory 512m
git config --global pack.packSizeLimit 512m
git config --global pack.threads 4

# 设置缓存大小
git config --global core.packedGitLimit 512m
git config --global core.packedGitWindowSize 32k

# 设置Delta缓存
git config --global core.deltaBaseCacheLimit 512m

# 设置文件监视器
git config --global core.fileMode false
```

#### 2. 操作优化

```bash
# 使用索引文件
git update-index --index-info

# 优化索引
git update-index --refresh

# 清理索引
git read-tree --empty
git read-tree HEAD

# 优化引用
git pack-refs --all

# 优化对象存储
git repack -a -d
```

#### 3. 监控优化

```bash
# 监控内存使用
git count-objects -v

# 监控包文件
git verify-pack -v .git/objects/pack/*.idx

# 监控引用
git show-ref

# 监控索引
git ls-files --stage

# 监控配置
git config --list
```

## 总结

Git高级技巧涵盖了从配置优化到性能调优的各个方面。掌握这些技巧可以让开发者更加高效地使用Git，解决复杂问题，优化开发流程。

### 关键要点

1. **配置优化**：通过合理的配置提高Git使用效率
2. **日志分析**：使用高级日志技巧分析项目历史
3. **分支管理**：掌握高级分支操作和策略
4. **合并技巧**：熟练使用各种合并策略和冲突解决方法
5. **性能优化**：通过优化提高Git操作性能

### 实践建议

- **循序渐进**：从基础技巧开始，逐步学习高级技巧
- **实践为主**：在实际项目中应用这些技巧
- **持续学习**：Git不断发展，持续学习新功能
- **分享经验**：与团队成员分享Git使用经验
- **工具辅助**：使用合适的工具辅助Git操作

通过掌握这些高级技巧，开发者可以显著提高Git使用效率，更好地管理项目版本控制，解决复杂问题，为团队协作提供更好的支持。