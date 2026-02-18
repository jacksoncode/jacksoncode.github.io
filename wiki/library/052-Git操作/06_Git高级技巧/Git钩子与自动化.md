# Git钩子与自动化

## Git钩子概述

Git钩子（Git Hooks）是Git在特定事件发生时自动执行的脚本。这些钩子可以用于自动化工作流程、执行代码检查、运行测试、发送通知等任务。

### 钩子的类型

Git钩子分为客户端钩子和服务端钩子两大类：

#### 客户端钩子
- **pre-commit**：在提交前运行，用于检查提交内容
- **prepare-commit-msg**：在提交信息编辑器启动前运行，用于修改提交信息
- **commit-msg**：在提交信息编辑完成后运行，用于验证提交信息格式
- **post-commit**：在提交完成后运行，用于发送通知等
- **pre-rebase**：在变基前运行，用于阻止某些变基操作
- **post-checkout**：在检出后运行，用于设置工作目录
- **post-merge**：在合并后运行，用于处理合并后的任务
- **pre-push**：在推送前运行，用于检查推送内容
- **post-rewrite**：在重写历史后运行，用于处理重写后的任务

#### 服务端钩子
- **pre-receive**：在接收推送前运行，用于验证推送内容
- **update**：在更新分支时运行，用于控制分支更新
- **post-receive**：在接收推送后运行，用于部署等任务

### 钩子的工作原理

1. **触发机制**：Git在特定操作执行时自动触发相应的钩子
2. **执行环境**：钩子在Git的执行环境中运行，可以访问Git的环境变量
3. **返回值**：钩子的返回值决定了操作是否继续（0表示继续，非0表示中止）
4. **错误处理**：钩子执行失败时，Git会显示错误信息并中止操作

### 钩子的优势

- **自动化**：自动执行重复性任务
- **质量控制**：在代码进入仓库前进行质量检查
- **标准化**：强制执行团队规范和标准
- **效率提升**：减少手动操作，提高开发效率
- **一致性**：确保所有操作都符合预定义的规则

## 客户端钩子

### pre-commit钩子

#### 1. 基本用法

```bash
#!/bin/bash

# pre-commit钩子示例
# 检查代码风格、运行测试、检查大文件等

# 运行代码检查
if command -v npm &> /dev/null; then
    echo "运行代码检查..."
    npm run lint
    if [ $? -ne 0 ]; then
        echo "错误：代码检查失败"
        exit 1
    fi
fi

# 运行测试
if command -v npm &> /dev/null; then
    echo "运行测试..."
    npm test
    if [ $? -ne 0 ]; then
        echo "错误：测试失败"
        exit 1
    fi
fi

# 检查大文件
echo "检查大文件..."
MAX_SIZE=$((5 * 1024 * 1024))  # 5MB
git diff --cached --name-only | while read file; do
    if [ -f "$file" ]; then
        size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null)
        if [ $size -gt $MAX_SIZE ]; then
            echo "错误：文件 $file 大小超过限制 ($size bytes)"
            exit 1
        fi
    fi
done

# 检查敏感信息
echo "检查敏感信息..."
git diff --cached | grep -i "password\|secret\|key" > /dev/null
if [ $? -eq 0 ]; then
    echo "错误：提交中可能包含敏感信息"
    exit 1
fi

echo "pre-commit检查通过"
exit 0
```

#### 2. 高级用法

```bash
#!/bin/bash

# 高级pre-commit钩子
# 支持多种语言、并行检查、详细报告

# 配置
LINT_CMD="npm run lint"
TEST_CMD="npm test"
MAX_FILE_SIZE=$((10 * 1024 * 1024))  # 10MB
SENSITIVE_PATTERNS="password|secret|key|token|api_key"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 函数：输出带颜色的消息
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 函数：检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 函数：运行代码检查
run_lint() {
    if command_exists npm; then
        log_info "运行代码检查..."
        if eval "$LINT_CMD"; then
            log_info "代码检查通过"
        else
            log_error "代码检查失败"
            return 1
        fi
    else
        log_warn "npm未安装，跳过代码检查"
    fi
}

# 函数：运行测试
run_tests() {
    if command_exists npm; then
        log_info "运行测试..."
        if eval "$TEST_CMD"; then
            log_info "测试通过"
        else
            log_error "测试失败"
            return 1
        fi
    else
        log_warn "npm未安装，跳过测试"
    fi
}

# 函数：检查文件大小
check_file_sizes() {
    log_info "检查文件大小..."
    local has_large_file=false
    
    git diff --cached --name-only | while read file; do
        if [ -f "$file" ]; then
            local size
            if stat --version &>/dev/null; then
                # Linux
                size=$(stat -c%s "$file")
            else
                # macOS
                size=$(stat -f%z "$file")
            fi
            
            if [ $size -gt $MAX_FILE_SIZE ]; then
                log_error "文件 $file 大小超过限制 ($size bytes)"
                has_large_file=true
            fi
        fi
    done
    
    if [ "$has_large_file" = true ]; then
        return 1
    fi
}

# 函数：检查敏感信息
check_sensitive_info() {
    log_info "检查敏感信息..."
    if git diff --cached | grep -iE "$SENSITIVE_PATTERNS" > /dev/null; then
        log_error "提交中可能包含敏感信息"
        return 1
    fi
}

# 主函数
main() {
    log_info "开始pre-commit检查..."
    
    # 并行运行检查
    local pids=()
    local errors=0
    
    # 代码检查
    run_lint &
    pids+=($!)
    
    # 测试
    run_tests &
    pids+=($!)
    
    # 等待所有后台任务完成
    for pid in "${pids[@]}"; do
        wait "$pid"
        if [ $? -ne 0 ]; then
            ((errors++))
        fi
    done
    
    # 串行运行文件检查
    check_file_sizes
    if [ $? -ne 0 ]; then
        ((errors++))
    fi
    
    check_sensitive_info
    if [ $? -ne 0 ]; then
        ((errors++))
    fi
    
    if [ $errors -gt 0 ]; then
        log_error "pre-commit检查失败，发现 $errors 个错误"
        exit 1
    fi
    
    log_info "pre-commit检查通过"
    exit 0
}

# 运行主函数
main
```

### update钩子

#### 1. 基本用法

```bash
#!/bin/bash

# update钩子示例
# 在分支更新时运行

# 获取参数
refname="$1"
oldrev="$2"
newrev="$3"

echo "更新信息："
echo "  引用名: $refname"
echo "  旧版本: $oldrev"
echo "  新版本: $newrev"

# 提取分支名称
branch_name=$(echo "$refname" | sed 's|refs/heads/||')

# 检查分支保护
if [ "$branch_name" = "main" ]; then
    echo "检查主分支更新..."
    
    # 检查是否为强制推送
    if [ "$oldrev" != "0000000000000000000000000000000000000000" ]; then
        if ! git merge-base --is-ancestor "$oldrev" "$newrev"; then
            echo "错误：不允许强制推送到主分支"
            exit 1
        fi
    fi
    
    # 检查提交数量
    if [ "$oldrev" != "0000000000000000000000000000000000000000" ]; then
        commit_count=$(git rev-list --count $oldrev..$newrev)
        echo "提交数量: $commit_count"
        
        if [ $commit_count -gt 5 ]; then
            echo "错误：主分支提交数量过多 ($commit_count)"
            exit 1
        fi
    fi
fi

# 检查是否为删除分支
if [ "$newrev" = "0000000000000000000000000000000000000000" ]; then
    echo "检测到分支删除: $branch_name"
    
    # 检查是否为保护分支
    if [ "$branch_name" = "main" ] || [ "$branch_name" = "develop" ]; then
        echo "错误：不允许删除保护分支"
        exit 1
    fi
fi

echo "update检查通过"
exit 0
```

#### 2. 高级用法

```bash
#!/bin/bash

# 高级update钩子
# 支持细粒度权限控制、分支命名规范、详细日志

# 配置
PROTECTED_BRANCHES=("main" "develop" "release/*")
BRANCH_NAMING_PATTERN="^(feature|bugfix|hotfix|release)/[a-z0-9-]+$"
MAX_COMMIT_COUNT=5
ALLOWED_USERS=("admin" "lead-developer" "senior-developer")
LOG_FILE="/var/log/git/update.log"

# 函数：记录日志
log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
}

# 函数：检查是否为保护分支
is_protected_branch() {
    local branch="$1"
    
    for protected_branch in "${PROTECTED_BRANCHES[@]}"; do
        if [[ "$branch" == $protected_branch ]]; then
            return 0
        fi
    done
    
    return 1
}

# 函数：检查用户权限
check_user_permission() {
    local username="$1"
    local branch="$2"
    
    # 检查是否在允许用户列表中
    for allowed_user in "${ALLOWED_USERS[@]}"; do
        if [ "$username" = "$allowed_user" ]; then
            return 0
        fi
    done
    
    # 检查特定分支权限
    case $branch in
        "main")
            log "WARN" "用户 $username 尝试推送到主分支"
            return 1
            ;;
        "develop")
            log "WARN" "用户 $username 尝试推送到开发分支"
            return 1
            ;;
        *)
            return 0
            ;;
    esac
}

# 函数：检查分支命名规范
check_branch_naming() {
    local branch="$1"
    
    # 跳过保护分支检查
    if is_protected_branch "$branch"; then
        return 0
    fi
    
    if ! echo "$branch" | grep -qE "$BRANCH_NAMING_PATTERN"; then
        log "ERROR" "分支命名不符合规范: $branch"
        echo "错误：分支命名不符合规范"
        echo "支持的模式：feature/name, bugfix/name, hotfix/name, release/name"
        return 1
    fi
}

# 函数：检查提交数量
check_commit_count() {
    local oldrev="$1"
    local newrev="$2"
    local branch="$3"
    
    if [ "$oldrev" != "0000000000000000000000000000000000000000" ]; then
        local commit_count
        commit_count=$(git rev-list --count $oldrev..$newrev)
        log "INFO" "分支 $branch 提交数量: $commit_count"
        
        # 根据分支类型设置不同的提交数量限制
        local max_commits=$MAX_COMMIT_COUNT
        case $branch in
            "main")
                max_commits=3
                ;;
            "develop")
                max_commits=10
                ;;
            "release"*)
                max_commits=5
                ;;
        esac
        
        if [ $commit_count -gt $max_commits ]; then
            log "ERROR" "分支 $branch 提交数量过多 ($commit_count)，限制: $max_commits"
            echo "错误：提交数量过多 ($commit_count)，建议不超过 $max_commits 个"
            return 1
        fi
    fi
}

# 函数：检查提交信息格式
check_commit_messages() {
    local oldrev="$1"
    local newrev="$2"
    
    git rev-list $oldrev..$newrev | while read commit; do
        local message
        message=$(git log --format=%B -n 1 $commit)
        log "INFO" "检查提交: $commit"
        
        if ! echo "$message" | grep -qE "^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: "; then
            log "ERROR" "提交信息格式不正确: $message"
            echo "错误：提交信息格式不正确"
            echo "提交 $commit: $message"
            return 1
        fi
    done
}

# 函数：检查分支删除
check_branch_deletion() {
    local branch="$1"
    
    if [ "$branch" = "0000000000000000000000000000000000000000" ]; then
        return 0
    fi
    
    # 检查是否为保护分支
    if is_protected_branch "$branch"; then
        log "ERROR" "尝试删除保护分支: $branch"
        echo "错误：不允许删除保护分支"
        return 1
    fi
    
    # 检查分支是否有关联的Pull Request
    # 这里可以集成GitHub API或GitLab API来检查
    
    log "INFO" "分支删除检查通过: $branch"
}

# 函数：生成更新报告
generate_update_report() {
    local refname="$1"
    local oldrev="$2"
    local newrev="$3"
    
    local branch_name
    branch_name=$(echo "$refname" | sed 's|refs/heads/||')
    
    local author
    author=$(git log --format=%an -n 1 $newrev)
    
    echo ""
    echo "=== 更新报告 ==="
    echo "分支: $branch_name"
    echo "操作: $(if [ "$newrev" = "0000000000000000000000000000000000000000" ]; then echo "删除"; else echo "更新"; fi)"
    echo "作者: $author"
    echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
    
    if [ "$newrev" != "0000000000000000000000000000000000000000" ]; then
        echo "提交数量: $(git rev-list --count $oldrev..$newrev)"
        echo ""
        echo "提交详情："
        git log --oneline $oldrev..$newrev
    fi
    
    echo ""
    echo "=== 报告结束 ==="
}

# 主函数
main() {
    # 获取参数
    local refname="$1"
    local oldrev="$2"
    local newrev="$3"
    
    log "INFO" "开始update检查: refname=$refname, oldrev=$oldrev, newrev=$newrev"
    
    # 提取分支名称
    local branch_name
    branch_name=$(echo "$refname" | sed 's|refs/heads/||')
    
    # 获取提交者信息
    local author
    if [ "$newrev" != "0000000000000000000000000000000000000000" ]; then
        author=$(git log --format=%an -n 1 $newrev)
    else
        author="$(git log --format=%an -n 1 $oldrev)"
    fi
    
    log "INFO" "操作者: $author"
    
    # 检查分支删除
    if [ "$newrev" = "0000000000000000000000000000000000000000" ]; then
        check_branch_deletion "$branch_name"
        if [ $? -ne 0 ]; then
            exit 1
        fi
        
        log "INFO" "分支删除检查通过"
        exit 0
    fi
    
    # 检查分支命名规范
    check_branch_naming "$branch_name"
    if [ $? -ne 0 ]; then
        exit 1
    fi
    
    # 检查用户权限
    check_user_permission "$author" "$branch_name"
    if [ $? -ne 0 ]; then
        exit 1
    fi
    
    # 检查保护分支
    if is_protected_branch "$branch_name"; then
        log "INFO" "检查保护分支: $branch_name"
        
        # 检查是否为强制推送
        if [ "$oldrev" != "0000000000000000000000000000000000000000" ]; then
            if ! git merge-base --is-ancestor "$oldrev" "$newrev"; then
                log "ERROR" "检测到强制推送到保护分支"
                echo "错误：不允许强制推送到保护分支"
                exit 1
            fi
        fi
        
        # 检查提交数量
        check_commit_count "$oldrev" "$newrev" "$branch_name"
        if [ $? -ne 0 ]; then
            exit 1
        fi
        
        # 检查提交信息格式
        check_commit_messages "$oldrev" "$newrev"
        if [ $? -ne 0 ]; then
            exit 1
        fi
    fi
    
    # 生成更新报告
    generate_update_report "$refname" "$oldrev" "$newrev" >> "$LOG_FILE"
    
    log "INFO" "update检查通过"
    exit 0
}

# 运行主函数
main "$@"
```

## Git钩子最佳实践

### 1. 钩子开发原则

#### 可靠性
- **错误处理**：确保钩子脚本有完善的错误处理机制
- **日志记录**：详细记录钩子执行过程，便于调试和审计
- **性能优化**：避免钩子执行时间过长，影响开发体验
- **兼容性**：确保钩子在不同操作系统和Git版本下都能正常工作

#### 可维护性
- **模块化设计**：将复杂功能拆分为独立的函数或模块
- **配置外部化**：将可配置项提取到外部配置文件
- **文档完善**：为钩子脚本添加详细的注释和文档
- **版本控制**：将钩子脚本纳入版本控制管理

#### 安全性
- **权限控制**：限制钩子脚本的执行权限
- **输入验证**：对所有输入参数进行严格验证
- **敏感信息保护**：避免在钩子中硬编码敏感信息
- **审计日志**：记录所有关键操作，便于安全审计

### 2. 钩子部署策略

#### 本地部署
```bash
#!/bin/bash

# 钩子部署脚本
# 自动安装和配置Git钩子

# 钩子目录
HOOK_DIR=".git/hooks"

# 源钩子目录
SOURCE_HOOK_DIR="githooks"

# 创建钩子目录
mkdir -p "$HOOK_DIR"

# 复制钩子文件
copy_hooks() {
    local hook_files=("pre-commit" "commit-msg" "pre-push")
    
    for hook_file in "${hook_files[@]}"; do
        local source_file="$SOURCE_HOOK_DIR/$hook_file"
        local target_file="$HOOK_DIR/$hook_file"
        
        if [ -f "$source_file" ]; then
            echo "安装钩子: $hook_file"
            cp "$source_file" "$target_file"
            chmod +x "$target_file"
        else
            echo "警告：钩子文件不存在: $source_file"
        fi
    done
}

# 配置钩子
configure_hooks() {
    echo "配置钩子..."
    
    # 设置钩子配置
    git config core.hooksPath "$HOOK_DIR"
    
    # 启用钩子
    git config hooks.allowunannotated false
    git config hooks.allowdeletebranch false
    git config hooks.allowmultiplecommits false
}

# 验证钩子
verify_hooks() {
    echo "验证钩子..."
    
    local hook_files=("pre-commit" "commit-msg" "pre-push")
    
    for hook_file in "${hook_files[@]}"; do
        local target_file="$HOOK_DIR/$hook_file"
        
        if [ -f "$target_file" ] && [ -x "$target_file" ]; then
            echo "✓ 钩子 $hook_file 已正确安装"
        else
            echo "✗ 钩子 $hook_file 安装失败"
            return 1
        fi
    done
}

# 主函数
main() {
    echo "开始部署Git钩子..."
    
    copy_hooks
    configure_hooks
    verify_hooks
    
    if [ $? -eq 0 ]; then
        echo "Git钩子部署成功"
    else
        echo "Git钩子部署失败"
        exit 1
    fi
}

# 运行主函数
main
```

#### 团队部署
```bash
#!/bin/bash

# 团队钩子部署脚本
# 使用Git子模块管理团队钩子

# 钩子子模块URL
HOOKS_REPO_URL="https://github.com/your-team/git-hooks.git"
HOOKS_REPO_PATH=".git/hooks"

# 初始化钩子子模块
init_hooks_submodule() {
    echo "初始化钩子子模块..."
    
    # 检查是否已存在子模块
    if [ -d "$HOOKS_REPO_PATH/.git" ]; then
        echo "钩子子模块已存在"
        return 0
    fi
    
    # 添加子模块
    git submodule add "$HOOKS_REPO_URL" "$HOOKS_REPO_PATH"
    
    # 初始化子模块
    git submodule update --init --recursive
}

# 更新钩子
update_hooks() {
    echo "更新钩子..."
    
    # 拉取最新钩子
    cd "$HOOKS_REPO_PATH"
    git pull origin main
    cd - > /dev/null
}

# 安装钩子
install_hooks() {
    echo "安装钩子..."
    
    # 设置钩子路径
    git config core.hooksPath "$HOOKS_REPO_PATH"
    
    # 设置执行权限
    chmod +x "$HOOKS_REPO_PATH"/*
}

# 验证钩子
verify_hooks() {
    echo "验证钩子..."
    
    local required_hooks=("pre-commit" "commit-msg" "pre-push")
    
    for hook in "${required_hooks[@]}"; do
        local hook_path="$HOOKS_REPO_PATH/$hook"
        
        if [ -f "$hook_path" ] && [ -x "$hook_path" ]; then
            echo "✓ 钩子 $hook 已正确安装"
        else
            echo "✗ 钩子 $hook 安装失败"
            return 1
        fi
    done
}

# 主函数
main() {
    echo "开始部署团队Git钩子..."
    
    init_hooks_submodule
    update_hooks
    install_hooks
    verify_hooks
    
    if [ $? -eq 0 ]; then
        echo "团队Git钩子部署成功"
        echo "请提交子模块更改: git add .git/hooks && git commit -m 'Add git hooks submodule'"
    else
        echo "团队Git钩子部署失败"
        exit 1
    fi
}

# 运行主函数
main
```

### 3. 钩子测试策略

#### 单元测试
```bash
#!/bin/bash

# 钩子测试框架
# 为Git钩子提供单元测试支持

# 测试框架配置
TEST_DIR="tests"
TEMP_REPO_DIR="/tmp/test-repo-$$"

# 函数：创建测试仓库
create_test_repo() {
    echo "创建测试仓库..."
    
    mkdir -p "$TEMP_REPO_DIR"
    cd "$TEMP_REPO_DIR"
    
    git init
    git config user.name "Test User"
    git config user.email "test@example.com"
    
    # 创建测试文件
    echo "测试内容" > test.txt
    git add test.txt
    git commit -m "Initial commit"
}

# 函数：清理测试仓库
cleanup_test_repo() {
    echo "清理测试仓库..."
    rm -rf "$TEMP_REPO_DIR"
}

# 函数：测试钩子
test_hook() {
    local hook_name="$1"
    local hook_script="$2"
    local test_description="$3"
    local expected_result="$4"
    
    echo "测试钩子: $hook_name - $test_description"
    
    # 安装钩子
    cp "$hook_script" "$TEMP_REPO_DIR/.git/hooks/$hook_name"
    chmod +x "$TEMP_REPO_DIR/.git/hooks/$hook_name"
    
    # 执行测试
    cd "$TEMP_REPO_DIR"
    
    case $hook_name in
        "pre-commit")
            echo "新的测试内容" >> test.txt
            git add test.txt
            if git commit -m "Test commit" 2>/dev/null; then
                actual_result=0
            else
                actual_result=1
            fi
            ;;
        "commit-msg")
            echo "Invalid commit message" > commit_msg.txt
            if git commit -F commit_msg.txt 2>/dev/null; then
                actual_result=0
            else
                actual_result=1
            fi
            ;;
        "pre-push")
            # 模拟推送测试
            actual_result=0
            ;;
    esac
    
    # 验证结果
    if [ $actual_result -eq $expected_result ]; then
        echo "✓ 测试通过"
        return 0
    else
        echo "✗ 测试失败"
        echo "  期望结果: $expected_result"
        echo "  实际结果: $actual_result"
        return 1
    fi
}

# 函数：运行所有测试
run_all_tests() {
    echo "运行所有钩子测试..."
    
    local total_tests=0
    local passed_tests=0
    
    # 测试pre-commit钩子
    if test_hook "pre-commit" "../hooks/pre-commit" "代码检查" 1; then
        ((passed_tests++))
    fi
    ((total_tests++))
    
    # 测试commit-msg钩子
    if test_hook "commit-msg" "../hooks/commit-msg" "提交信息验证" 1; then
        ((passed_tests++))
    fi
    ((total_tests++))
    
    # 测试pre-push钩子
    if test_hook "pre-push" "../hooks/pre-push" "推送检查" 0; then
        ((passed_tests++))
    fi
    ((total_tests++))
    
    echo ""
    echo "测试结果: $passed_tests/$total_tests 通过"
    
    if [ $passed_tests -eq $total_tests ]; then
        return 0
    else
        return 1
    fi
}

# 主函数
main() {
    echo "开始Git钩子测试..."
    
    create_test_repo
    
    if run_all_tests; then
        echo "所有测试通过"
        cleanup_test_repo
        exit 0
    else
        echo "部分测试失败"
        cleanup_test_repo
        exit 1
    fi
}

# 运行主函数
main
```

#### 集成测试
```bash
#!/bin/bash

# 钩子集成测试
# 测试钩子在实际开发流程中的表现

# 测试配置
TEST_PROJECT_DIR="/tmp/test-project-$$"
TEMPLATE_REPO="https://github.com/your-team/project-template.git"

# 函数：创建测试项目
create_test_project() {
    echo "创建测试项目..."
    
    git clone "$TEMPLATE_REPO" "$TEST_PROJECT_DIR"
    cd "$TEST_PROJECT_DIR"
    
    # 安装钩子
    ./scripts/install-hooks.sh
}

# 函数：模拟开发工作流
simulate_development_workflow() {
    echo "模拟开发工作流..."
    
    # 创建功能分支
    git checkout -b feature/test-feature
    
    # 修改代码
    echo "新的功能代码" > feature.js
    
    # 测试pre-commit钩子
    echo "测试pre-commit钩子..."
    git add feature.js
    if git commit -m "feat: add test feature"; then
        echo "✓ pre-commit钩子工作正常"
    else
        echo "✗ pre-commit钩子失败"
        return 1
    fi
    
    # 测试commit-msg钩子
    echo "测试commit-msg钩子..."
    if git commit --amend -m "feat: add test feature #123"; then
        echo "✓ commit-msg钩子工作正常"
    else
        echo "✗ commit-msg钩子失败"
        return 1
    fi
    
    # 测试pre-push钩子
    echo "测试pre-push钩子..."
    if git push origin feature/test-feature; then
        echo "✓ pre-push钩子工作正常"
    else
        echo "✗ pre-push钩子失败"
        return 1
    fi
}

# 函数：模拟代码审查流程
simulate_code_review() {
    echo "模拟代码审查流程..."
    
    # 创建Pull Request
    echo "创建Pull Request..."
    # 这里可以集成GitHub API或GitLab API
    
    # 等待审查
    echo "等待代码审查..."
    sleep 2
    
    # 模拟审查通过
    echo "模拟审查通过"
    
    # 合并到主分支
    git checkout main
    git pull origin main
    git merge feature/test-feature
    
    # 测试post-receive钩子
    echo "测试post-receive钩子..."
    if git push origin main; then
        echo "✓ post-receive钩子工作正常"
    else
        echo "✗ post-receive钩子失败"
        return 1
    fi
}

# 函数：清理测试项目
cleanup_test_project() {
    echo "清理测试项目..."
    rm -rf "$TEST_PROJECT_DIR"
}

# 函数：生成测试报告
generate_test_report() {
    echo "生成测试报告..."
    
    local report_file="test-report-$(date +%Y%m%d_%H%M%S).md"
    
    cat > "$report_file" << EOF
# Git钩子集成测试报告

## 测试时间
$(date '+%Y-%m-%d %H:%M:%S')

## 测试项目
$TEST_PROJECT_DIR

## 测试结果

### 开发工作流测试
- [x] pre-commit钩子
- [x] commit-msg钩子  
- [x] pre-push钩子

### 代码审查流程测试
- [x] Pull Request创建
- [x] 代码审查等待
- [x] 分支合并
- [x] post-receive钩子

## 结论
所有集成测试通过，Git钩子工作正常。
EOF
    
    echo "测试报告已生成: $report_file"
}

# 主函数
main() {
    echo "开始Git钩子集成测试..."
    
    create_test_project
    
    if simulate_development_workflow; then
        echo "开发工作流测试通过"
    else
        echo "开发工作流测试失败"
        cleanup_test_project
        exit 1
    fi
    
    if simulate_code_review; then
        echo "代码审查流程测试通过"
    else
        echo "代码审查流程测试失败"
        cleanup_test_project
        exit 1
    fi
    
    generate_test_report
    cleanup_test_project
    
    echo "所有集成测试通过"
    exit 0
}

# 运行主函数
main
```

### 4. 钩子性能优化

#### 性能监控
```bash
#!/bin/bash

# 钩子性能监控
# 监控钩子执行时间和资源使用情况

# 监控配置
MONITOR_LOG="/var/log/git/hook-performance.log"
MONITOR_DIR="/var/log/git/hook-monitor"
ALERT_THRESHOLD=5  # 5秒

# 函数：记录性能数据
log_performance() {
    local hook_name="$1"
    local execution_time="$2"
    local memory_usage="$3"
    
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] Hook: $hook_name, Time: ${execution_time}s, Memory: ${memory_usage}MB" >> "$MONITOR_LOG"
    
    # 检查是否超过阈值
    if (( $(echo "$execution_time > $ALERT_THRESHOLD" | bc -l) )); then
        send_alert "$hook_name" "$execution_time"
    fi
}

# 函数：发送警报
send_alert() {
    local hook_name="$1"
    local execution_time="$2"
    
    local message="警告：钩子 $hook_name 执行时间过长 (${execution_time}s)"
    
    # 发送邮件
    echo "$message" | mail -s "Git钩子性能警报" admin@example.com
    
    # 发送Slack通知
    if [ -n "$SLACK_WEBHOOK" ]; then
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\": \"$message\"}" \
            "$SLACK_WEBHOOK" > /dev/null 2>&1
    fi
}

# 函数：生成性能报告
generate_performance_report() {
    local report_file="$MONITOR_DIR/performance-report-$(date +%Y%m%d).html"
    
    mkdir -p "$MONITOR_DIR"
    
    cat > "$report_file" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Git钩子性能报告</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .warning { color: red; }
    </style>
</head>
<body>
    <h1>Git钩子性能报告</h1>
    <p>生成时间: $(date '+%Y-%m-%d %H:%M:%S')</p>
    
    <table>
        <tr>
            <th>时间</th>
            <th>钩子名称</th>
            <th>执行时间(秒)</th>
            <th>内存使用(MB)</th>
        </tr>
EOF
    
    # 添加性能数据
    tail -n 100 "$MONITOR_LOG" | while read line; do
        local timestamp=$(echo "$line" | sed 's/\[\([^]]*\)\].*/\1/')
        local hook_name=$(echo "$line" | sed 's/.*Hook: \([^,]*\).*/\1/')
        local execution_time=$(echo "$line" | sed 's/.*Time: \([^s]*\)s.*/\1/')
        local memory_usage=$(echo "$line" | sed 's/.*Memory: \([^ ]*\)MB.*/\1/')
        
        local row_class=""
        if (( $(echo "$execution_time > $ALERT_THRESHOLD" | bc -l) )); then
            row_class="class='warning'"
        fi
        
        cat >> "$report_file" << EOF
        <tr $row_class>
            <td>$timestamp</td>
            <td>$hook_name</td>
            <td>$execution_time</td>
            <td>$memory_usage</td>
        </tr>
EOF
    done
    
    cat >> "$report_file" << EOF
    </table>
</body>
</html>
EOF
    
    echo "性能报告已生成: $report_file"
}

# 函数：包装钩子执行
wrap_hook_execution() {
    local hook_name="$1"
    shift
    
    local start_time=$(date +%s.%N)
    local start_memory=$(ps -o rss= -p $$)
    
    # 执行原始钩子
    "$@"
    local exit_code=$?
    
    local end_time=$(date +%s.%N)
    local end_memory=$(ps -o rss= -p $$)
    
    # 计算执行时间和内存使用
    local execution_time=$(echo "$end_time - $start_time" | bc)
    local memory_usage=$(echo "scale=2; ($end_memory - $start_memory) / 1024" | bc)
    
    # 记录性能数据
    log_performance "$hook_name" "$execution_time" "$memory_usage"
    
    return $exit_code
}

# 主函数
main() {
    local hook_name="$1"
    shift
    
    # 如果是性能监控模式
    if [ "$1" = "--monitor" ]; then
        generate_performance_report
        exit 0
    fi
    
    # 包装钩子执行
    wrap_hook_execution "$hook_name" "$@"
}

# 运行主函数
main "$@"
```

#### 性能优化技巧

1. **减少不必要的检查**
   - 只在必要时运行昂贵的操作
   - 使用缓存机制避免重复计算
   - 根据文件类型选择性地执行检查

2. **并行处理**
   - 使用后台进程并行执行独立任务
   - 利用多核CPU提高处理速度
   - 合理设置并发数量避免资源耗尽

3. **增量检查**
   - 只检查发生变化的文件
   - 使用Git的diff功能获取变更范围
   - 维护文件状态缓存避免重复检查

4. **资源管理**
   - 及时释放不再需要的资源
   - 使用临时文件处理大数据
   - 限制内存使用防止系统过载

## 常见问题与解决方案

### 1. 钩子不执行

#### 问题描述
钩子脚本已正确安装，但在相应操作时没有执行。

#### 可能原因
1. 钩子脚本没有执行权限
2. 钩子脚本路径错误
3. 钩子脚本语法错误
4. Git配置禁用了钩子

#### 解决方案
```bash
#!/bin/bash

# 钩子诊断脚本
# 诊断和修复钩子不执行的问题

# 函数：检查钩子权限
check_hook_permissions() {
    local hook_dir=".git/hooks"
    
    echo "检查钩子权限..."
    
    if [ ! -d "$hook_dir" ]; then
        echo "错误：钩子目录不存在: $hook_dir"
        return 1
    fi
    
    local hooks=("pre-commit" "commit-msg" "pre-push")
    
    for hook in "${hooks[@]}"; do
        local hook_path="$hook_dir/$hook"
        
        if [ -f "$hook_path" ]; then
            if [ -x "$hook_path" ]; then
                echo "✓ 钩子 $hook 有执行权限"
            else
                echo "✗ 钩子 $hook 没有执行权限"
                chmod +x "$hook_path"
                echo "  已修复执行权限"
            fi
        else
            echo "✗ 钩子 $hook 不存在"
        fi
    done
}

# 函数：检查钩子语法
check_hook_syntax() {
    local hook_dir=".git/hooks"
    
    echo "检查钩子语法..."
    
    local hooks=("pre-commit" "commit-msg" "pre-push")
    
    for hook in "${hooks[@]}"; do
        local hook_path="$hook_dir/$hook"
        
        if [ -f "$hook_path" ]; then
            echo "检查钩子 $hook 语法..."
            
            # 检查shebang
            if ! head -n 1 "$hook_path" | grep -q "^#!"; then
                echo "✗ 钩子 $hook 缺少shebang"
                echo "  添加shebang: #!/bin/bash"
                sed -i '1i#!/bin/bash' "$hook_path"
            fi
            
            # 检查语法
            if bash -n "$hook_path" 2>/dev/null; then
                echo "✓ 钩子 $hook 语法正确"
            else
                echo "✗ 钩子 $hook 语法错误"
                echo "  请检查脚本语法"
            fi
        fi
    done
}

# 函数：检查Git配置
check_git_config() {
    echo "检查Git配置..."
    
    # 检查hooksPath配置
    local hooks_path=$(git config core.hooksPath)
    
    if [ -n "$hooks_path" ]; then
        echo "Git hooksPath: $hooks_path"
        
        if [ ! -d "$hooks_path" ]; then
            echo "✗ hooksPath目录不存在: $hooks_path"
            echo "  重置hooksPath配置"
            git config --unset core.hooksPath
        fi
    else
        echo "使用默认钩子路径: .git/hooks"
    fi
    
    # 检查是否禁用钩子
    if git config --get-regexp "^hooks\." | grep -q "false"; then
        echo "警告：检测到禁用的钩子配置"
        git config --get-regexp "^hooks\."
    fi
}

# 函数：测试钩子执行
test_hook_execution() {
    echo "测试钩子执行..."
    
    # 创建测试文件
    echo "测试内容" > test.txt
    git add test.txt
    
    # 测试pre-commit钩子
    echo "测试pre-commit钩子..."
    if git commit -m "Test commit" 2>/dev/null; then
        echo "✓ pre-commit钩子执行成功"
    else
        echo "✗ pre-commit钩子执行失败"
        echo "  请检查钩子脚本和错误信息"
    fi
    
    # 清理测试文件
    git reset HEAD test.txt
    rm test.txt
}

# 函数：生成诊断报告
generate_diagnosis_report() {
    echo "生成诊断报告..."
    
    local report_file="hook-diagnosis-$(date +%Y%m%d_%H%M%S).txt"
    
    {
        echo "Git钩子诊断报告"
        echo "生成时间: $(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
        echo "Git版本: $(git --version)"
        echo "当前分支: $(git branch --show-current)"
        echo "仓库路径: $(pwd)"
        echo ""
        echo "Git配置:"
        git config --list | grep -E "(core\.hooksPath|hooks\.)"
        echo ""
        echo "钩子目录内容:"
        ls -la .git/hooks/
        echo ""
        echo "钩子脚本内容:"
        for hook in .git/hooks/*; do
            if [ -f "$hook" ] && [ -x "$hook" ]; then
                echo "=== $hook ==="
                head -n 10 "$hook"
                echo ""
            fi
        done
    } > "$report_file"
    
    echo "诊断报告已生成: $report_file"
}

# 主函数
main() {
    echo "开始Git钩子诊断..."
    echo ""
    
    check_hook_permissions
    echo ""
    
    check_hook_syntax
    echo ""
    
    check_git_config
    echo ""
    
    test_hook_execution
    echo ""
    
    generate_diagnosis_report
    
    echo ""
    echo "诊断完成"
    echo "如果问题仍然存在，请查看诊断报告或联系技术支持"
}

# 运行主函数
main
```

### 2. 钩子执行失败

#### 问题描述
钩子脚本执行时出现错误，导致Git操作被中止。

#### 可能原因
1. 钩子脚本逻辑错误
2. 依赖命令不存在
3. 权限不足
4. 环境变量问题
5. 网络连接问题

#### 解决方案
```bash
#!/bin/bash

# 钩子调试脚本
# 帮助调试钩子执行失败的问题

# 调试配置
DEBUG_LOG="hook-debug.log"
VERBOSE=false

# 函数：启用调试模式
enable_debug_mode() {
    echo "启用调试模式..."
    
    # 设置调试环境变量
    export GIT_TRACE=1
    export GIT_TRACE_PACK_ACCESS=1
    export GIT_TRACE_PACKET=1
    export GIT_CURL_VERBOSE=1
    
    echo "调试环境变量已设置"
}

# 函数：检查依赖命令
check_dependencies() {
    echo "检查依赖命令..."
    
    local commands=("bash" "git" "grep" "sed" "awk")
    
    for cmd in "${commands[@]}"; do
        if command -v "$cmd" >/dev/null 2>&1; then
            echo "✓ $cmd: $(command -v "$cmd")"
        else
            echo "✗ $cmd: 未找到"
        fi
    done
}

# 函数：检查环境变量
check_environment() {
    echo "检查环境变量..."
    
    # 显示相关环境变量
    echo "PATH: $PATH"
    echo "HOME: $HOME"
    echo "PWD: $PWD"
    echo "SHELL: $SHELL"
    echo "USER: $USER"
    
    # 检查Git相关环境变量
    echo ""
    echo "Git环境变量:"
    env | grep -i git || echo "无Git相关环境变量"
}

# 函数：手动执行钩子
manual_hook_execution() {
    local hook_name="$1"
    
    echo "手动执行钩子: $hook_name"
    
    local hook_path=".git/hooks/$hook_name"
    
    if [ ! -f "$hook_path" ]; then
        echo "错误：钩子不存在: $hook_path"
        return 1
    fi
    
    echo "钩子路径: $hook_path"
    echo "钩子权限: $(ls -la "$hook_path")"
    
    # 根据钩子类型准备参数
    case $hook_name in
        "pre-commit")
            echo "执行pre-commit钩子..."
            "$hook_path"
            ;;
        "commit-msg")
            echo "创建测试提交信息..."
            echo "Test commit message" > test_msg.txt
            echo "执行commit-msg钩子..."
            "$hook_path" test_msg.txt
            rm test_msg.txt
            ;;
        "pre-push")
            echo "执行pre-push钩子..."
            echo "refs/heads/main 0000000000000000000000000000000000000000 refs/heads/main $(git rev-parse main)" | "$hook_path" stdin
            ;;
        *)
            echo "执行钩子..."
            "$hook_path"
            ;;
    esac
    
    local exit_code=$?
    echo "钩子退出码: $exit_code"
    
    return $exit_code
}

# 函数：分析钩子日志
analyze_hook_logs() {
    echo "分析钩子日志..."
    
    # 检查系统日志
    echo "系统日志:"
    if [ -f "/var/log/syslog" ]; then
        grep -i git /var/log/syslog | tail -n 10
    elif [ -f "/var/log/messages" ]; then
        grep -i git /var/log/messages | tail -n 10
    else
        echo "未找到系统日志"
    fi
    
    echo ""
    echo "Git日志:"
    git log --oneline -n 5
    
    echo ""
    echo "钩子执行日志:"
    if [ -f "$DEBUG_LOG" ]; then
        tail -n 20 "$DEBUG_LOG"
    else
        echo "未找到调试日志"
    fi
}

# 函数：生成调试报告
generate_debug_report() {
    echo "生成调试报告..."
    
    local report_file="hook-debug-$(date +%Y%m%d_%H%M%S).txt"
    
    {
        echo "Git钩子调试报告"
        echo "生成时间: $(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
        echo "系统信息:"
        uname -a
        echo ""
        echo "Git信息:"
        git --version
        git config --list
        echo ""
        echo "环境变量:"
        env
        echo ""
        echo "钩子脚本:"
        for hook in .git/hooks/*; do
            if [ -f "$hook" ] && [ -x "$hook" ]; then
                echo "=== $hook ==="
                cat "$hook"
                echo ""
            fi
        done
    } > "$report_file"
    
    echo "调试报告已生成: $report_file"
}

# 主函数
main() {
    local hook_name="$1"
    
    echo "开始Git钩子调试..."
    echo ""
    
    enable_debug_mode
    echo ""
    
    check_dependencies
    echo ""
    
    check_environment
    echo ""
    
    if [ -n "$hook_name" ]; then
        manual_hook_execution "$hook_name"
        echo ""
    fi
    
    analyze_hook_logs
    echo ""
    
    generate_debug_report
    
    echo ""
    echo "调试完成"
    echo "如果问题仍然存在，请查看调试报告或检查钩子脚本逻辑"
}

# 运行主函数
main "$@"
```

#### 3. 多语言支持

##### 问题描述
钩子脚本需要支持多种编程语言，以适应不同团队的技术栈和需求。

##### 解决方案
```bash
#!/bin/bash

# 多语言钩子支持框架
# 支持Python、Node.js、Ruby等多种语言的钩子脚本

# 配置
HOOK_CONFIG_DIR="hook-config"
HOOK_SCRIPTS_DIR="hook-scripts"
LOG_FILE="multilang-hook.log"

# 函数：检测脚本语言
detect_script_language() {
    local script_file="$1"
    
    if [ ! -f "$script_file" ]; then
        echo "unknown"
        return 1
    fi
    
    # 检查文件扩展名
    case "$script_file" in
        *.py)
            echo "python"
            ;;
        *.js)
            echo "nodejs"
            ;;
        *.rb)
            echo "ruby"
            ;;
        *.pl)
            echo "perl"
            ;;
        *.php)
            echo "php"
            ;;
        *)
            # 检查shebang
            local shebang=$(head -n 1 "$script_file")
            case "$shebang" in
                *python*)
                    echo "python"
                    ;;
                *node*|*nodejs*)
                    echo "nodejs"
                    ;;
                *ruby*)
                    echo "ruby"
                    ;;
                *perl*)
                    echo "perl"
                    ;;
                *php*)
                    echo "php"
                    ;;
                *)
                    echo "unknown"
                    ;;
            esac
            ;;
    esac
}

# 函数：检查语言环境
check_language_environment() {
    local language="$1"
    
    case "$language" in
        "python")
            if command -v python3 >/dev/null 2>&1; then
                echo "python3"
            elif command -v python >/dev/null 2>&1; then
                echo "python"
            else
                echo ""
            fi
            ;;
        "nodejs")
            if command -v node >/dev/null 2>&1; then
                echo "node"
            else
                echo ""
            fi
            ;;
        "ruby")
            if command -v ruby >/dev/null 2>&1; then
                echo "ruby"
            else
                echo ""
            fi
            ;;
        "perl")
            if command -v perl >/dev/null 2>&1; then
                echo "perl"
            else
                echo ""
            fi
            ;;
        "php")
            if command -v php >/dev/null 2>&1; then
                echo "php"
            else
                echo ""
            fi
            ;;
        *)
            echo ""
            ;;
    esac
}

# 函数：执行Python脚本
execute_python_script() {
    local script_file="$1"
    shift
    
    local python_cmd=$(check_language_environment "python")
    
    if [ -z "$python_cmd" ]; then
        echo "错误：未找到Python环境" >&2
        return 1
    fi
    
    echo "使用 $python_cmd 执行Python脚本: $script_file" >> "$LOG_FILE"
    "$python_cmd" "$script_file" "$@"
}

# 函数：执行Node.js脚本
execute_nodejs_script() {
    local script_file="$1"
    shift
    
    local node_cmd=$(check_language_environment "nodejs")
    
    if [ -z "$node_cmd" ]; then
        echo "错误：未找到Node.js环境" >&2
        return 1
    fi
    
    echo "使用 $node_cmd 执行Node.js脚本: $script_file" >> "$LOG_FILE"
    "$node_cmd" "$script_file" "$@"
}

# 函数：执行Ruby脚本
execute_ruby_script() {
    local script_file="$1"
    shift
    
    local ruby_cmd=$(check_language_environment "ruby")
    
    if [ -z "$ruby_cmd" ]; then
        echo "错误：未找到Ruby环境" >&2
        return 1
    fi
    
    echo "使用 $ruby_cmd 执行Ruby脚本: $script_file" >> "$LOG_FILE"
    "$ruby_cmd" "$script_file" "$@"
}

# 函数：执行Perl脚本
execute_perl_script() {
    local script_file="$1"
    shift
    
    local perl_cmd=$(check_language_environment "perl")
    
    if [ -z "$perl_cmd" ]; then
        echo "错误：未找到Perl环境" >&2
        return 1
    fi
    
    echo "使用 $perl_cmd 执行Perl脚本: $script_file" >> "$LOG_FILE"
    "$perl_cmd" "$script_file" "$@"
}

# 函数：执行PHP脚本
execute_php_script() {
    local script_file="$1"
    shift
    
    local php_cmd=$(check_language_environment "php")
    
    if [ -z "$php_cmd" ]; then
        echo "错误：未找到PHP环境" >&2
        return 1
    fi
    
    echo "使用 $php_cmd 执行PHP脚本: $script_file" >> "$LOG_FILE"
    "$php_cmd" "$script_file" "$@"
}

# 函数：执行多语言钩子
execute_multilang_hook() {
    local hook_name="$1"
    shift
    
    echo "执行多语言钩子: $hook_name" >> "$LOG_FILE"
    
    # 查找钩子脚本
    local script_file=""
    local languages=("py" "js" "rb" "pl" "php")
    
    for ext in "${languages[@]}"; do
        local candidate="$HOOK_SCRIPTS_DIR/$hook_name.$ext"
        if [ -f "$candidate" ]; then
            script_file="$candidate"
            break
        fi
    done
    
    if [ -z "$script_file" ]; then
        echo "错误：未找到钩子脚本: $hook_name" >&2
        return 1
    fi
    
    # 检测脚本语言
    local language=$(detect_script_language "$script_file")
    
    if [ "$language" = "unknown" ]; then
        echo "错误：无法识别脚本语言: $script_file" >&2
        return 1
    fi
    
    echo "检测到脚本语言: $language" >> "$LOG_FILE"
    
    # 根据语言执行脚本
    case "$language" in
        "python")
            execute_python_script "$script_file" "$@"
            ;;
        "nodejs")
            execute_nodejs_script "$script_file" "$@"
            ;;
        "ruby")
            execute_ruby_script "$script_file" "$@"
            ;;
        "perl")
            execute_perl_script "$script_file" "$@"
            ;;
        "php")
            execute_php_script "$script_file" "$@"
            ;;
        *)
            echo "错误：不支持的语言: $language" >&2
            return 1
            ;;
    esac
}

# 函数：加载配置
load_config() {
    local config_file="$HOOK_CONFIG_DIR/config.json"
    
    if [ -f "$config_file" ]; then
        echo "加载配置文件: $config_file" >> "$LOG_FILE"
        # 这里可以添加JSON解析逻辑
        # 或者使用jq等工具
    else
        echo "使用默认配置" >> "$LOG_FILE"
    fi
}

# 函数：初始化环境
init_environment() {
    echo "初始化多语言钩子环境..." >> "$LOG_FILE"
    
    # 创建必要的目录
    mkdir -p "$HOOK_CONFIG_DIR"
    mkdir -p "$HOOK_SCRIPTS_DIR"
    
    # 初始化日志文件
    echo "=== $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"
    
    # 加载配置
    load_config
}

# 主函数
main() {
    local hook_name="$1"
    shift
    
    # 初始化环境
    init_environment
    
    # 执行多语言钩子
    execute_multilang_hook "$hook_name" "$@"
    
    local exit_code=$?
    
    echo "钩子执行完成，退出码: $exit_code" >> "$LOG_FILE"
    
    return $exit_code
}

# 运行主函数
main "$@"
```

### 4. 钩子版本控制

#### 问题描述
钩子脚本需要版本控制，以便跟踪变更、回滚问题和团队协作。

#### 解决方案
```bash
#!/bin/bash

# 钩子版本控制管理
# 管理钩子脚本的版本控制和部署

# 配置
HOOK_REPO_URL="https://github.com/your-team/git-hooks.git"
HOOK_REPO_DIR="/var/git/hooks-repo"
HOOK_DEPLOY_DIR="/var/git/hooks-deploy"
VERSION_FILE="version.txt"
CHANGELOG="CHANGELOG.md"

# 函数：初始化钩子仓库
init_hook_repo() {
    echo "初始化钩子仓库..."
    
    if [ -d "$HOOK_REPO_DIR" ]; then
        echo "钩子仓库已存在"
        return 0
    fi
    
    # 克隆钩子仓库
    git clone "$HOOK_REPO_URL" "$HOOK_REPO_DIR"
    
    if [ $? -ne 0 ]; then
        echo "错误：克隆钩子仓库失败"
        return 1
    fi
    
    echo "钩子仓库初始化成功"
}

# 函数：更新钩子仓库
update_hook_repo() {
    echo "更新钩子仓库..."
    
    cd "$HOOK_REPO_DIR"
    
    # 获取最新变更
    git fetch origin
    
    # 检查是否有更新
    local local_hash=$(git rev-parse HEAD)
    local remote_hash=$(git rev-parse origin/main)
    
    if [ "$local_hash" = "$remote_hash" ]; then
        echo "钩子仓库已是最新版本"
        return 0
    fi
    
    # 拉取最新代码
    git pull origin main
    
    if [ $? -ne 0 ]; then
        echo "错误：更新钩子仓库失败"
        return 1
    fi
    
    echo "钩子仓库更新成功"
}

# 函数：获取当前版本
get_current_version() {
    if [ -f "$HOOK_REPO_DIR/$VERSION_FILE" ]; then
        cat "$HOOK_REPO_DIR/$VERSION_FILE"
    else
        echo "1.0.0"
    fi
}

# 函数：部署钩子
deploy_hooks() {
    echo "部署钩子..."
    
    local version=$(get_current_version)
    local deploy_dir="$HOOK_DEPLOY_DIR/$version"
    
    # 创建部署目录
    mkdir -p "$deploy_dir"
    
    # 复制钩子文件
    cp -r "$HOOK_REPO_DIR/hooks/"* "$deploy_dir/"
    
    # 设置执行权限
    chmod +x "$deploy_dir"/*
    
    # 创建符号链接到最新版本
    ln -sfn "$deploy_dir" "$HOOK_DEPLOY_DIR/latest"
    
    echo "钩子部署成功，版本: $version"
}

# 函数：回滚版本
rollback_version() {
    local target_version="$1"
    
    if [ -z "$target_version" ]; then
        echo "错误：请指定目标版本"
        return 1
    fi
    
    echo "回滚到版本: $target_version"
    
    local target_dir="$HOOK_DEPLOY_DIR/$target_version"
    
    if [ ! -d "$target_dir" ]; then
        echo "错误：目标版本不存在: $target_version"
        return 1
    fi
    
    # 更新符号链接
    ln -sfn "$target_dir" "$HOOK_DEPLOY_DIR/latest"
    
    echo "版本回滚成功"
}

# 函数：列出可用版本
list_versions() {
    echo "可用版本:"
    
    if [ ! -d "$HOOK_DEPLOY_DIR" ]; then
        echo "无可用版本"
        return 1
    fi
    
    local current_version=$(get_current_version)
    
    for version_dir in "$HOOK_DEPLOY_DIR"/*; do
        if [ -d "$version_dir" ]; then
            local version=$(basename "$version_dir")
            local marker=""
            
            if [ "$version" = "$current_version" ]; then
                marker=" (当前)"
            fi
            
            echo "  $version$marker"
        fi
    done
}

# 函数：生成变更日志
generate_changelog() {
    echo "生成变更日志..."
    
    cd "$HOOK_REPO_DIR"
    
    local changelog_file="$HOOK_REPO_DIR/$CHANGELOG"
    
    {
        echo "# 钩子变更日志"
        echo ""
        echo "最后更新: $(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
        
        # 获取最近的提交
        echo "## 最近变更"
        echo ""
        git log --oneline -n 10 | while read commit; do
            echo "- $commit"
        done
        
        echo ""
        echo "## 版本历史"
        echo ""
        
        # 获取标签版本
        git tag --sort=-version:refname | while read version; do
            echo "### $version"
            echo ""
            git show --no-patch --format="%ad%n%n%s%n%n%b" "$version" | sed 's/^/    /'
            echo ""
        done
        
    } > "$changelog_file"
    
    echo "变更日志已生成: $changelog_file"
}

# 函数：创建新版本
create_version() {
    local version="$1"
    local message="$2"
    
    if [ -z "$version" ] || [ -z "$message" ]; then
        echo "错误：请指定版本号和提交信息"
        echo "用法: $0 create-version <version> <message>"
        return 1
    fi
    
    echo "创建新版本: $version"
    
    cd "$HOOK_REPO_DIR"
    
    # 更新版本文件
    echo "$version" > "$VERSION_FILE"
    
    # 提交变更
    git add "$VERSION_FILE"
    git commit -m "版本更新: $version - $message"
    
    # 创建标签
    git tag -a "$version" -m "$message"
    
    # 推送到远程仓库
    git push origin main
    git push origin "$version"
    
    echo "版本创建成功: $version"
}

# 函数：显示帮助信息
show_help() {
    echo "钩子版本控制管理工具"
    echo ""
    echo "用法: $0 <command> [options]"
    echo ""
    echo "命令:"
    echo "  init                    初始化钩子仓库"
    echo "  update                  更新钩子仓库"
    echo "  deploy                  部署钩子"
    echo "  rollback <version>      回滚到指定版本"
    echo "  list-versions           列出可用版本"
    echo "  generate-changelog      生成变更日志"
    echo "  create-version <v> <m>  创建新版本"
    echo "  help                    显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 init"
    echo "  $0 update"
    echo "  $0 deploy"
    echo "  $0 rollback 1.0.0"
    echo "  $0 create-version 1.1.0 '修复pre-commit钩子问题'"
}

# 主函数
main() {
    local command="$1"
    shift
    
    case "$command" in
        "init")
            init_hook_repo
            ;;
        "update")
            update_hook_repo
            ;;
        "deploy")
            update_hook_repo
            deploy_hooks
            ;;
        "rollback")
            rollback_version "$1"
            ;;
        "list-versions")
            list_versions
            ;;
        "generate-changelog")
            generate_changelog
            ;;
        "create-version")
            create_version "$1" "$2"
            ;;
        "help"|"--help"|"-h")
            show_help
            ;;
        *)
            echo "错误：未知命令: $command"
            show_help
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"
```

### 5. 钩子安全性考虑

#### 问题描述
钩子脚本可能存在安全风险，需要确保其安全性和可靠性。

#### 解决方案
```bash
#!/bin/bash

# 钩子安全检查框架
# 确保钩子脚本的安全性和可靠性

# 配置
SECURITY_LOG="hook-security.log"
ALLOWED_COMMANDS=("git" "grep" "sed" "awk" "python" "node" "ruby" "php" "perl")
RESTRICTED_PATTERNS=("rm -rf" "/dev/null" "> /" "wget" "curl" "nc" "netcat")
MAX_FILE_SIZE=1048576  # 1MB
MAX_EXECUTION_TIME=30  # 30秒

# 函数：检查脚本权限
check_script_permissions() {
    local script_file="$1"
    
    echo "检查脚本权限: $script_file"
    
    # 检查文件权限
    local perms=$(stat -c "%a" "$script_file")
    
    # 不允许其他用户有写权限
    if [[ "$perms" =~ [0-7][0-7][2367] ]]; then
        echo "警告：脚本文件权限过于宽松: $perms"
        return 1
    fi
    
    # 检查文件所有者
    local owner=$(stat -c "%U" "$script_file")
    if [ "$owner" != "root" ] && [ "$owner" != "$USER" ]; then
        echo "警告：脚本文件所有者不是当前用户: $owner"
        return 1
    fi
    
    echo "✓ 脚本权限检查通过"
    return 0
}

# 函数：检查脚本内容
check_script_content() {
    local script_file="$1"
    
    echo "检查脚本内容: $script_file"
    
    # 检查文件大小
    local file_size=$(stat -c "%s" "$script_file")
    if [ $file_size -gt $MAX_FILE_SIZE ]; then
        echo "警告：脚本文件过大: $file_size bytes"
        return 1
    fi
    
    # 检查危险模式
    for pattern in "${RESTRICTED_PATTERNS[@]}"; do
        if grep -q "$pattern" "$script_file"; then
            echo "警告：检测到危险模式: $pattern"
            return 1
        fi
    done
    
    # 检查网络访问
    if grep -qE "(wget|curl|nc|netcat|telnet|ssh)" "$script_file"; then
        echo "警告：检测到网络访问命令"
        return 1
    fi
    
    # 检查系统命令
    if grep -qE "(sudo|su|passwd|useradd|groupadd)" "$script_file"; then
        echo "警告：检测到系统管理命令"
        return 1
    fi
    
    echo "✓ 脚本内容检查通过"
    return 0
}

# 函数：检查依赖命令
check_dependencies_secure() {
    local script_file="$1"
    
    echo "检查依赖命令: $script_file"
    
    # 提取脚本中的命令
    local commands=$(grep -oE "[a-zA-Z0-9_-]+" "$script_file" | sort | uniq)
    
    for cmd in $commands; do
        # 跳过内置命令和变量
        if [[ "$cmd" =~ ^(if|then|else|fi|for|while|do|done|case|esac|function|local|echo|printf|return|exit)$ ]]; then
            continue
        fi
        
        # 检查是否为允许的命令
        local allowed=false
        for allowed_cmd in "${ALLOWED_COMMANDS[@]}"; do
            if [ "$cmd" = "$allowed_cmd" ]; then
                allowed=true
                break
            fi
        done
        
        if [ "$allowed" = false ]; then
            # 检查命令是否存在
            if command -v "$cmd" >/dev/null 2>&1; then
                echo "警告：使用未授权的命令: $cmd"
            else
                echo "错误：依赖命令不存在: $cmd"
                return 1
            fi
        fi
    done
    
    echo "✓ 依赖命令检查通过"
    return 0
}

# 函数：沙箱执行
execute_in_sandbox() {
    local script_file="$1"
    shift
    
    echo "在沙箱中执行脚本: $script_file"
    
    # 创建临时工作目录
    local temp_dir=$(mktemp -d)
    
    # 复制脚本到临时目录
    cp "$script_file" "$temp_dir/script.sh"
    
    # 设置资源限制
    ulimit -t $MAX_EXECUTION_TIME  # CPU时间限制
    ulimit -f 100                 # 文件大小限制（块）
    ulimit -v 1048576             # 内存限制（KB）
    
    # 切换到临时目录
    cd "$temp_dir"
    
    # 执行脚本
    timeout $MAX_EXECUTION_TIME bash "script.sh" "$@"
    local exit_code=$?
    
    # 清理临时目录
    cd - > /dev/null
    rm -rf "$temp_dir"
    
    return $exit_code
}

# 函数：监控脚本执行
monitor_execution() {
    local script_file="$1"
    shift
    
    echo "监控脚本执行: $script_file"
    
    # 记录开始时间
    local start_time=$(date +%s)
    
    # 监控进程
    local pid=$!
    
    # 监控循环
    while kill -0 "$pid" 2>/dev/null; do
        local current_time=$(date +%s)
        local elapsed=$((current_time - start_time))
        
        if [ $elapsed -gt $MAX_EXECUTION_TIME ]; then
            echo "警告：脚本执行超时，终止进程"
            kill -9 "$pid"
            return 1
        fi
        
        # 检查资源使用
        local memory_usage=$(ps -o rss= -p "$pid")
        if [ $memory_usage -gt 1048576 ]; then  # 1GB
            echo "警告：脚本内存使用过高，终止进程"
            kill -9 "$pid"
            return 1
        fi
        
        sleep 1
    done
    
    # 获取退出码
    wait "$pid"
    local exit_code=$?
    
    return $exit_code
}

# 函数：记录安全日志
log_security_event() {
    local event_type="$1"
    local script_file="$2"
    local message="$3"
    
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local user=$(whoami)
    local pid=$$
    
    echo "[$timestamp] [$event_type] [User: $user] [PID: $pid] [Script: $script_file] $message" >> "$SECURITY_LOG"
}

# 函数：安全执行钩子
execute_hook_secure() {
    local hook_name="$1"
    local script_file="$2"
    shift 2
    
    echo "安全执行钩子: $hook_name"
    
    # 记录开始事件
    log_security_event "START" "$script_file" "开始执行钩子: $hook_name"
    
    # 检查脚本权限
    if ! check_script_permissions "$script_file"; then
        log_security_event "ERROR" "$script_file" "脚本权限检查失败"
        return 1
    fi
    
    # 检查脚本内容
    if ! check_script_content "$script_file"; then
        log_security_event "ERROR" "$script_file" "脚本内容检查失败"
        return 1
    fi
    
    # 检查依赖命令
    if ! check_dependencies_secure "$script_file"; then
        log_security_event "ERROR" "$script_file" "依赖命令检查失败"
        return 1
    fi
    
    # 在沙箱中执行脚本
    execute_in_sandbox "$script_file" "$@" &
    local script_pid=$!
    
    # 监控脚本执行
    monitor_execution "$script_file" "$@"
    local exit_code=$?
    
    # 记录结束事件
    if [ $exit_code -eq 0 ]; then
        log_security_event "SUCCESS" "$script_file" "钩子执行成功"
    else
        log_security_event "FAILURE" "$script_file" "钩子执行失败，退出码: $exit_code"
    fi
    
    return $exit_code
}

# 函数：生成安全报告
generate_security_report() {
    echo "生成安全报告..."
    
    local report_file="security-report-$(date +%Y%m%d).html"
    
    {
        echo "<!DOCTYPE html>"
        echo "<html>"
        echo "<head>"
        echo "    <title>Git钩子安全报告</title>"
        echo "    <style>"
        echo "        body { font-family: Arial, sans-serif; margin: 20px; }"
        echo "        table { border-collapse: collapse; width: 100%; }"
        echo "        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }"
        echo "        th { background-color: #f2f2f2; }"
        echo "        .error { color: red; }"
        echo "        .warning { color: orange; }"
        echo "        .success { color: green; }"
        echo "    </style>"
        echo "</head>"
        echo "<body>"
        echo "    <h1>Git钩子安全报告</h1>"
        echo "    <p>生成时间: $(date '+%Y-%m-%d %H:%M:%S')</p>"
        echo ""
        echo "    <h2>安全事件统计</h2>"
        echo "    <table>"
        echo "        <tr>"
        echo "            <th>事件类型</th>"
        echo "            <th>数量</th>"
        echo "        </tr>"
        
        # 统计事件类型
        for event_type in "START" "SUCCESS" "ERROR" "FAILURE"; do
            local count=$(grep -c "\[$event_type\]" "$SECURITY_LOG" 2>/dev/null || echo 0)
            echo "        <tr>"
            echo "            <td>$event_type</td>"
            echo "            <td>$count</td>"
            echo "        </tr>"
        done
        
        echo "    </table>"
        echo ""
        echo "    <h2>最近的安全事件</h2>"
        echo "    <table>"
        echo "        <tr>"
        echo "            <th>时间</th>"
        echo "            <th>类型</th>"
        echo "            <th>用户</th>"
        echo "            <th>脚本</th>"
        echo "            <th>消息</th>"
        echo "        </tr>"
        
        # 显示最近的事件
        tail -n 20 "$SECURITY_LOG" 2>/dev/null | while read line; do
            local timestamp=$(echo "$line" | sed 's/\[\([^]]*\)\].*/\1/')
            local event_type=$(echo "$line" | sed 's/.*\[\([^]]*\)\].*/\1/')
            local user=$(echo "$line" | sed 's/.*\[User: \([^]]*\)\].*/\1/')
            local script=$(echo "$line" | sed 's/.*\[Script: \([^]]*\)\].*/\1/')
            local message=$(echo "$line" | sed 's/.*] \([^ ]*\) \(.*\)/\2/')
            
            local css_class=""
            case "$event_type" in
                "ERROR"|"FAILURE") css_class="error" ;;
                "WARNING") css_class="warning" ;;
                "SUCCESS") css_class="success" ;;
            esac
            
            echo "        <tr class='$css_class'>"
            echo "            <td>$timestamp</td>"
            echo "            <td>$event_type</td>"
            echo "            <td>$user</td>"
            echo "            <td>$script</td>"
            echo "            <td>$message</td>"
            echo "        </tr>"
        done
        
        echo "    </table>"
        echo "</body>"
        echo "</html>"
    } > "$report_file"
    
    echo "安全报告已生成: $report_file"
}

# 主函数
main() {
    local hook_name="$1"
    local script_file="$2"
    shift 2
    
    # 如果是安全报告模式
    if [ "$hook_name" = "--security-report" ]; then
        generate_security_report
        exit 0
    fi
    
    # 安全执行钩子
    execute_hook_secure "$hook_name" "$script_file" "$@"
}

# 运行主函数
main "$@"
```

## 总结

Git钩子是自动化工作流程和强制执行代码质量的强大工具。通过本文档的学习，您应该已经掌握了：

### 主要知识点

1. **Git钩子基础**
   - 理解Git钩子的工作原理和类型
   - 掌握客户端和服务器端钩子的区别
   - 学会基本的钩子配置和使用方法

2. **客户端钩子**
   - pre-commit：代码检查和格式化
   - commit-msg：提交信息验证
   - pre-push：推送前检查
   - 其他常用客户端钩子的使用

3. **服务器端钩子**
   - pre-receive：接收前验证
   - post-receive：接收后处理
   - update：分支更新控制
   - 服务器端钩子的部署和管理

4. **最佳实践**
   - 钩子开发原则：可靠性、可维护性、安全性
   - 部署策略：本地部署和团队部署
   - 测试策略：单元测试和集成测试
   - 性能优化：监控和优化技巧

5. **问题解决**
   - 钩子不执行的诊断和修复
   - 钩子执行失败的调试方法
   - 多语言支持的实现
   - 版本控制和安全性考虑

### 实际应用建议

1. **逐步实施**
   - 从简单的pre-commit钩子开始
   - 逐步添加更复杂的检查和自动化
   - 根据团队反馈调整钩子策略

2. **团队协作**
   - 建立钩子开发和管理规范
   - 定期审查和更新钩子脚本
   - 提供充分的文档和培训

3. **持续改进**
   - 监控钩子执行效果
   - 收集用户反馈
   - 不断优化和完善钩子功能

### 进阶学习方向

1. **CI/CD集成**
   - 将Git钩子与CI/CD流程结合
   - 实现更复杂的自动化工作流

2. **工具链整合**
   - 集成代码质量检查工具
   - 结合项目管理工具

3. **自定义开发**
   - 开发专门的钩子管理工具
   - 创建团队特定的钩子解决方案

通过合理使用Git钩子，您可以显著提高开发效率、代码质量和团队协作水平。希望本文档能够帮助您更好地理解和应用Git钩子技术。

```bash
#!/bin/bash

# 多语言pre-commit钩子
# 支持JavaScript、Python、Java、Go等

# 配置
PROJECT_TYPE=$(node -p "require('./package.json').type" 2>/dev/null || echo "unknown")

# 函数：检测项目类型
detect_project_type() {
    if [ -f "package.json" ]; then
        echo "nodejs"
    elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
        echo "python"
    elif [ -f "pom.xml" ] || [ -f "build.gradle" ]; then
        echo "java"
    elif [ -f "go.mod" ]; then
        echo "go"
    else
        echo "unknown"
    fi
}

# 函数：运行JavaScript检查
run_js_checks() {
    echo "运行JavaScript检查..."
    
    # ESLint
    if command -v eslint &> /dev/null; then
        echo "运行ESLint..."
        eslint . --ext .js,.jsx,.ts,.tsx
        if [ $? -ne 0 ]; then
            echo "ESLint检查失败"
            return 1
        fi
    fi
    
    # Prettier
    if command -v prettier &> /dev/null; then
        echo "运行Prettier..."
        prettier --check .
        if [ $? -ne 0 ]; then
            echo "Prettier检查失败"
            return 1
        fi
    fi
    
    # 测试
    if command -v npm &> /dev/null; then
        echo "运行测试..."
        npm test
        if [ $? -ne 0 ]; then
            echo "测试失败"
            return 1
        fi
    fi
}

# 函数：运行Python检查
run_python_checks() {
    echo "运行Python检查..."
    
    # Flake8
    if command -v flake8 &> /dev/null; then
        echo "运行Flake8..."
        flake8 .
        if [ $? -ne 0 ]; then
            echo "Flake8检查失败"
            return 1
        fi
    fi
    
    # Black
    if command -v black &> /dev/null; then
        echo "运行Black..."
        black --check .
        if [ $? -ne 0 ]; then
            echo "Black检查失败"
            return 1
        fi
    fi
    
    # 测试
    if command -v pytest &> /dev/null; then
        echo "运行测试..."
        pytest
        if [ $? -ne 0 ]; then
            echo "测试失败"
            return 1
        fi
    fi
}

# 函数：运行Java检查
run_java_checks() {
    echo "运行Java检查..."
    
    # Maven
    if [ -f "pom.xml" ] && command -v mvn &> /dev/null; then
        echo "运行Maven检查..."
        mvn clean compile
        if [ $? -ne 0 ]; then
            echo "Maven编译失败"
            return 1
        fi
        
        mvn test
        if [ $? -ne 0 ]; then
            echo "Maven测试失败"
            return 1
        fi
    fi
    
    # Gradle
    if [ -f "build.gradle" ] && command -v gradle &> /dev/null; then
        echo "运行Gradle检查..."
        gradle build
        if [ $? -ne 0 ]; then
            echo "Gradle构建失败"
            return 1
        fi
    fi
}

# 函数：运行Go检查
run_go_checks() {
    echo "运行Go检查..."
    
    # Go fmt
    echo "运行go fmt..."
    go fmt ./...
    if [ $? -ne 0 ]; then
        echo "go fmt失败"
        return 1
    fi
    
    # Go vet
    echo "运行go vet..."
    go vet ./...
    if [ $? -ne 0 ]; then
        echo "go vet失败"
        return 1
    fi
    
    # 测试
    echo "运行测试..."
    go test ./...
    if [ $? -ne 0 ]; then
        echo "测试失败"
        return 1
    fi
}

# 主函数
main() {
    echo "开始pre-commit检查..."
    
    local project_type
    project_type=$(detect_project_type)
    
    case $project_type in
        "nodejs")
            run_js_checks
            ;;
        "python")
            run_python_checks
            ;;
        "java")
            run_java_checks
            ;;
        "go")
            run_go_checks
            ;;
        *)
            echo "未知项目类型，跳过检查"
            ;;
    esac
    
    if [ $? -ne 0 ]; then
        echo "pre-commit检查失败"
        exit 1
    fi
    
    echo "pre-commit检查通过"
    exit 0
}

# 运行主函数
main
```

### commit-msg钩子

#### 1. 基本用法

```bash
#!/bin/bash

# commit-msg钩子示例
# 验证提交信息格式

# 获取提交信息文件
commit_msg_file="$1"
commit_msg=$(cat "$commit_msg_file")

# 检查提交信息是否为空
if [ -z "$commit_msg" ]; then
    echo "错误：提交信息不能为空"
    exit 1
fi

# 检查提交信息长度
if [ ${#commit_msg} -gt 72 ]; then
    echo "错误：提交信息过长（${#commit_msg}字符），建议不超过72个字符"
    exit 1
fi

# 检查提交信息格式（Conventional Commits）
if ! echo "$commit_msg" | grep -qE "^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: "; then
    echo "错误：提交信息格式不正确"
    echo "建议格式：type(scope): description"
    echo "支持的类型：feat, fix, docs, style, refactor, test, chore"
    exit 1
fi

# 检查是否包含Issue编号
if ! echo "$commit_msg" | grep -qE "#[0-9]+"; then
    echo "警告：提交信息未包含Issue编号"
    echo "建议格式：type(scope): description #123"
    read -p "是否继续提交？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "提交信息检查通过"
exit 0
```

#### 2. 高级用法

```bash
#!/bin/bash

# 高级commit-msg钩子
# 支持多种格式、详细验证、自动修复

# 配置
COMMIT_MSG_FILE="$1"
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函数：输出带颜色的消息
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_debug() {
    echo -e "${BLUE}[DEBUG]${NC} $1"
}

# 函数：检查提交信息是否为空
check_empty_message() {
    if [ -z "$COMMIT_MSG" ]; then
        log_error "提交信息不能为空"
        return 1
    fi
}

# 函数：检查提交信息长度
check_message_length() {
    local max_length=72
    local length=${#COMMIT_MSG}
    
    if [ $length -gt $max_length ]; then
        log_error "提交信息过长（$length字符），建议不超过$max_length个字符"
        return 1
    fi
}

# 函数：检查提交信息格式（Conventional Commits）
check_conventional_format() {
    local pattern="^(feat|fix|docs|style|refactor|test|chore|perf|build|ci|revert)(\(.+\))?: .+"
    
    if ! echo "$COMMIT_MSG" | grep -qE "$pattern"; then
        log_error "提交信息格式不正确"
        echo "支持的格式："
        echo "  feat: 新功能"
        echo "  fix: 修复bug"
        echo "  docs: 文档更新"
        echo "  style: 代码格式化"
        echo "  refactor: 重构"
        echo "  test: 测试相关"
        echo "  chore: 构建或辅助工具变动"
        echo "  perf: 性能优化"
        echo "  build: 构建相关"
        echo "  ci: CI相关"
        echo "  revert: 回滚"
        echo ""
        echo "示例：feat(auth): add user authentication"
        return 1
    fi
}

# 函数：检查Issue编号
check_issue_number() {
    if ! echo "$COMMIT_MSG" | grep -qE "#[0-9]+"; then
        log_warn "提交信息未包含Issue编号"
        echo "建议格式：type(scope): description #123"
        read -p "是否继续提交？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return 1
        fi
    fi
}

# 函数：检查破坏性变更
check_breaking_change() {
    if echo "$COMMIT_MSG" | grep -q "BREAKING CHANGE"; then
        log_warn "提交包含破坏性变更"
        read -p "确认要提交破坏性变更吗？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return 1
        fi
    fi
}

# 函数：自动修复提交信息
auto_fix_message() {
    log_info "尝试自动修复提交信息..."
    
    # 移除多余的空格
    local fixed_msg=$(echo "$COMMIT_MSG" | sed 's/^[ \t]*//;s/[ \t]*$//')
    
    # 如果修复后的消息与原消息不同，则更新文件
    if [ "$fixed_msg" != "$COMMIT_MSG" ]; then
        echo "$fixed_msg" > "$COMMIT_MSG_FILE"
        log_info "已自动修复提交信息"
        COMMIT_MSG="$fixed_msg"
    fi
}

# 函数：生成提交信息建议
generate_suggestions() {
    echo ""
    echo "提交信息建议："
    echo "  feat: 添加新功能"
    echo "  fix: 修复bug"
    echo "  docs: 更新文档"
    echo "  style: 格式化代码"
    echo "  refactor: 重构代码"
    echo "  test: 添加或修改测试"
    echo "  chore: 构建或辅助工具变动"
    echo ""
    echo "示例："
    echo "  feat(auth): 添加用户认证功能 #123"
    echo "  fix(button): 修复按钮点击事件 #124"
    echo "  docs(readme): 更新README文档 #125"
}

# 主函数
main() {
    log_info "开始验证提交信息..."
    log_debug "提交信息: $COMMIT_MSG"
    
    # 检查空消息
    check_empty_message
    if [ $? -ne 0 ]; then
        generate_suggestions
        exit 1
    fi
    
    # 自动修复消息
    auto_fix_message
    
    # 检查消息长度
    check_message_length
    if [ $? -ne 0 ]; then
        generate_suggestions
        exit 1
    fi
    
    # 检查格式
    check_conventional_format
    if [ $? -ne 0 ]; then
        generate_suggestions
        exit 1
    fi
    
    # 检查Issue编号
    check_issue_number
    if [ $? -ne 0 ]; then
        exit 1
    fi
    
    # 检查破坏性变更
    check_breaking_change
    if [ $? -ne 0 ]; then
        exit 1
    fi
    
    log_info "提交信息验证通过"
    exit 0
}

# 运行主函数
main
```

#### 3. 团队规范

```bash
#!/bin/bash

# 团队规范commit-msg钩子
# 支持团队特定的提交规范

# 配置
COMMIT_MSG_FILE="$1"
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")
TEAM_CONFIG=".git/team-config.json"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 函数：输出带颜色的消息
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 函数：加载团队配置
load_team_config() {
    if [ -f "$TEAM_CONFIG" ]; then
        if command -v jq &> /dev/null; then
            echo $(jq -r '.' "$TEAM_CONFIG")
        else
            log_warn "jq未安装，使用默认配置"
            echo '{"commit_types":["feat","fix","docs","style","refactor","test","chore"],"max_length":72,"require_issue":true,"allow_breaking":true}'
        fi
    else
        log_info "未找到团队配置文件，使用默认配置"
        echo '{"commit_types":["feat","fix","docs","style","refactor","test","chorge"],"max_length":72,"require_issue":true,"allow_breaking":true}'
    fi
}

# 函数：检查提交类型
check_commit_type() {
    local config="$1"
    local types=$(echo "$config" | jq -r '.commit_types[]' | tr '\n' '|')
    local pattern="^(${types%|})(\(.+\))?: "
    
    if ! echo "$COMMIT_MSG" | grep -qE "$pattern"; then
        log_error "提交类型不正确"
        echo "支持的类型：$(echo "$config" | jq -r '.commit_types[]' | tr '\n' ', ')"
        return 1
    fi
}

# 函数：检查提交长度
check_commit_length() {
    local config="$1"
    local max_length=$(echo "$config" | jq -r '.max_length')
    local length=${#COMMIT_MSG}
    
    if [ $length -gt $max_length ]; then
        log_error "提交信息过长（$length字符），建议不超过$max_length个字符"
        return 1
    fi
}

# 函数：检查Issue编号
check_issue_number() {
    local config="$1"
    local require_issue=$(echo "$config" | jq -r '.require_issue')
    
    if [ "$require_issue" = "true" ]; then
        if ! echo "$COMMIT_MSG" | grep -qE "#[0-9]+"; then
            log_warn "提交信息未包含Issue编号"
            echo "建议格式：type(scope): description #123"
            read -p "是否继续提交？(y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                return 1
            fi
        fi
    fi
}

# 函数：检查破坏性变更
check_breaking_change() {
    local config="$1"
    local allow_breaking=$(echo "$config" | jq -r '.allow_breaking')
    
    if echo "$COMMIT_MSG" | grep -q "BREAKING CHANGE"; then
        if [ "$allow_breaking" = "false" ]; then
            log_error "不允许提交破坏性变更"
            return 1
        else
            log_warn "提交包含破坏性变更"
            read -p "确认要提交破坏性变更吗？(y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                return 1
            fi
        fi
    fi
}

# 函数：检查团队特定规则
check_team_rules() {
    local config="$1"
    
    # 检查是否包含团队标识
    if echo "$config" | jq -e '.team_id' > /dev/null; then
        local team_id=$(echo "$config" | jq -r '.team_id')
        if ! echo "$COMMIT_MSG" | grep -q "$team_id"; then
            log_warn "提交信息未包含团队标识: $team_id"
        fi
    fi
    
    # 检查是否包含组件标识
    if echo "$config" | jq -e '.require_component' > /dev/null; then
        local require_component=$(echo "$config" | jq -r '.require_component')
        if [ "$require_component" = "true" ]; then
            if ! echo "$COMMIT_MSG" | grep -qE "\(.+\):"; then
                log_warn "提交信息未包含组件标识"
                echo "建议格式：type(component): description"
            fi
        fi
    fi
}

# 主函数
main() {
    log_info "开始验证团队提交规范..."
    
    # 加载团队配置
    local config
    config=$(load_team_config)
    
    # 检查提交类型
    check_commit_type "$config"
    if [ $? -ne 0 ]; then
        exit 1
    fi
    
    # 检查提交长度
    check_commit_length "$config"
    if [ $? -ne 0 ]; then
        exit 1
    fi
    
    # 检查Issue编号
    check_issue_number "$config"
    if [ $? -ne 0 ]; then
        exit 1
    fi
    
    # 检查破坏性变更
    check_breaking_change "$config"
    if [ $? -ne 0 ]; then
        exit 1
    fi
    
    # 检查团队特定规则
    check_team_rules "$config"
    if [ $? -ne 0 ]; then
        exit 1
    fi
    
    log_info "团队提交规范验证通过"
    exit 0
}

# 运行主函数
main
```

### pre-push钩子

#### 1. 基本用法

```bash
#!/bin/bash

# pre-push钩子示例
# 在推送前运行检查

# 获取推送信息
while read local_ref local_sha remote_ref remote_sha; do
    echo "推送信息："
    echo "  本地引用: $local_ref"
    echo "  本地SHA: $local_sha"
    echo "  远程引用: $remote_ref"
    echo "  远程SHA: $remote_sha"
    
    # 检查是否推送到主分支
    if [ "$remote_ref" = "refs/heads/main" ]; then
        echo "检查推送到主分支..."
        
        # 检查提交数量
        if [ "$local_sha" != "0000000000000000000000000000000000000000" ]; then
            commit_count=$(git rev-list --count $remote_sha..$local_sha)
            echo "提交数量: $commit_count"
            
            if [ $commit_count -gt 10 ]; then
                echo "错误：主分支提交数量过多 ($commit_count)"
                exit 1
            fi
        fi
        
        # 检查提交信息格式
        git rev-list $remote_sha..$local_sha | while read commit; do
            message=$(git log --format=%B -n 1 $commit)
            if ! echo "$message" | grep -qE "^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: "; then
                echo "错误：提交信息格式不正确"
                echo "提交 $commit: $message"
                exit 1
            fi
        done
    fi
    
    # 检查是否推送到保护分支
    if [[ "$remote_ref" =~ refs/heads/(main|develop|release) ]]; then
        echo "检查推送到保护分支..."
        
        # 检查是否有未完成的Pull Request
        if command -v gh &> /dev/null; then
            open_prs=$(gh pr list --state open --json number | jq length)
            if [ $open_prs -gt 0 ]; then
                echo "警告：存在未完成的Pull Request ($open_prs个)"
                read -p "是否继续推送？(y/N): " -n 1 -r
                echo
                if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                    exit 1
                fi
            fi
        fi
    fi
    
    # 运行测试
    echo "运行测试..."
    if command -v npm &> /dev/null; then
        npm test
        if [ $? -ne 0 ]; then
            echo "错误：测试失败"
            exit 1
        fi
    fi
    
    # 检查构建
    echo "检查构建..."
    if command -v npm &> /dev/null; then
        npm run build
        if [ $? -ne 0 ]; then
            echo "错误：构建失败"
            exit 1
        fi
    fi
    
    echo "pre-push检查通过"
done

exit 0
```

#### 2. 高级用法

```bash
#!/bin/bash

# 高级pre-push钩子
# 支持分支保护、CI检查、详细报告

# 配置
PROTECTED_BRANCHES=("main" "develop" "release")
MAX_COMMIT_COUNT=10
REQUIRE_CI_CHECK=true
REQUIRE_CODE_REVIEW=true

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函数：输出带颜色的消息
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_debug() {
    echo -e "${BLUE}[DEBUG]${NC} $1"
}

# 函数：检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 函数：检查是否为保护分支
is_protected_branch() {
    local branch="$1"
    for protected_branch in "${PROTECTED_BRANCHES[@]}"; do
        if [ "$branch" = "$protected_branch" ]; then
            return 0
        fi
    done
    return 1
}

# 函数：检查提交数量
check_commit_count() {
    local remote_sha="$1"
    local local_sha="$2"
    
    if [ "$local_sha" != "0000000000000000000000000000000000000000" ]; then
        local commit_count
        commit_count=$(git rev-list --count $remote_sha..$local_sha)
        log_debug "提交数量: $commit_count"
        
        if [ $commit_count -gt $MAX_COMMIT_COUNT ]; then
            log_error "提交数量过多 ($commit_count)，建议不超过 $MAX_COMMIT_COUNT 个"
            return 1
        fi
    fi
}

# 函数：检查提交信息格式
check_commit_messages() {
    local remote_sha="$1"
    local local_sha="$2"
    
    git rev-list $remote_sha..$local_sha | while read commit; do
        local message
        message=$(git log --format=%B -n 1 $commit)
        log_debug "检查提交: $commit"
        
        if ! echo "$message" | grep -qE "^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: "; then
            log_error "提交信息格式不正确"
            echo "提交 $commit: $message"
            return 1
        fi
    done
}

# 函数：检查CI状态
check_ci_status() {
    if [ "$REQUIRE_CI_CHECK" = "true" ] && command_exists gh; then
        log_info "检查CI状态..."
        
        # 获取当前分支
        local current_branch
        current_branch=$(git rev-parse --abbrev-ref HEAD)
        
        # 检查是否有未完成的CI检查
        local ci_status
        ci_status=$(gh run list --branch "$current_branch" --status in_progress --json status | jq length)
        
        if [ $ci_status -gt 0 ]; then
            log_warn "存在未完成的CI检查"
            read -p "是否继续推送？(y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                return 1
            fi
        fi
    fi
}

# 函数：检查代码审查
check_code_review() {
    if [ "$REQUIRE_CODE_REVIEW" = "true" ] && command_exists gh; then
        log_info "检查代码审查..."
        
        # 获取当前分支
        local current_branch
        current_branch=$(git rev-parse --abbrev-ref HEAD)
        
        # 检查是否有未审查的Pull Request
        local pr_count
        pr_count=$(gh pr list --head "$current_branch" --state open --json number | jq length)
        
        if [ $pr_count -gt 0 ]; then
            log_warn "存在未审查的Pull Request ($pr_count个)"
            read -p "是否继续推送？(y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                return 1
            fi
        fi
    fi
}

# 函数：运行测试
run_tests() {
    log_info "运行测试..."
    
    if command_exists npm; then
        if npm test; then
            log_info "测试通过"
        else
            log_error "测试失败"
            return 1
        fi
    elif command_exists python; then
        if python -m pytest; then
            log_info "测试通过"
        else
            log_error "测试失败"
            return 1
        fi
    else
        log_warn "未找到测试命令，跳过测试"
    fi
}

# 函数：检查构建
check_build() {
    log_info "检查构建..."
    
    if command_exists npm; then
        if npm run build; then
            log_info "构建成功"
        else
            log_error "构建失败"
            return 1
        fi
    else
        log_warn "未找到构建命令，跳过构建检查"
    fi
}

# 函数：生成推送报告
generate_push_report() {
    local remote_ref="$1"
    local remote_sha="$2"
    local local_sha="$3"
    
    echo ""
    echo "=== 推送报告 ==="
    echo "远程分支: $remote_ref"
    echo "远程SHA: $remote_sha"
    echo "本地SHA: $local_sha"
    
    if [ "$local_sha" != "0000000000000000000000000000000000000000" ]; then
        echo ""
        echo "提交详情："
        git log --oneline $remote_sha..$local_sha
    fi
    
    echo ""
    echo "=== 报告结束 ==="
}

# 主函数
main() {
    log_info "开始pre-push检查..."
    
    # 读取推送信息
    while read local_ref local_sha remote_ref remote_sha; do
        log_info "推送信息："
        log_info "  本地引用: $local_ref"
        log_info "  本地SHA: $local_sha"
        log_info "  远程引用: $remote_ref"
        log_info "  远程SHA: $remote_sha"
        
        # 提取分支名称
        local branch_name
        branch_name=$(echo "$remote_ref" | sed 's|refs/heads/||')
        
        # 检查保护分支
        if is_protected_branch "$branch_name"; then
            log_info "检查保护分支: $branch_name"
            
            # 检查提交数量
            check_commit_count "$remote_sha" "$local_sha"
            if [ $? -ne 0 ]; then
                exit 1
            fi
            
            # 检查提交信息格式
            check_commit_messages "$remote_sha" "$local_sha"
            if [ $? -ne 0 ]; then
                exit 1
            fi
            
            # 检查CI状态
            check_ci_status
            if [ $? -ne 0 ]; then
                exit 1
            fi
            
            # 检查代码审查
            check_code_review
            if [ $? -ne 0 ]; then
                exit 1
            fi
        fi
        
        # 运行测试
        run_tests
        if [ $? -ne 0 ]; then
            exit 1
        fi
        
        # 检查构建
        check_build
        if [ $? -ne 0 ]; then
            exit 1
        fi
        
        # 生成推送报告
        generate_push_report "$remote_ref" "$remote_sha" "$local_sha"
        
        log_info "pre-push检查通过"
    done
    
    exit 0
}

# 运行主函数
main
```

#### 3. 集成CI/CD

```bash
#!/bin/bash

# 集成CI/CD的pre-push钩子
# 与GitHub Actions、GitLab CI等集成

# 配置
CI_PLATFORM="github"  # github, gitlab, jenkins
CI_TOKEN=""
REQUIRE_CI_SUCCESS=true
REQUIRE_DEPLOYMENT_READY=false

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函数：输出带颜色的消息
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_debug() {
    echo -e "${BLUE}[DEBUG]${NC} $1"
}

# 函数：检查GitHub Actions状态
check_github_actions() {
    if ! command_exists gh; then
        log_warn "GitHub CLI未安装，跳过CI检查"
        return 0
    fi
    
    # 获取当前分支
    local current_branch
    current_branch=$(git rev-parse --abbrev-ref HEAD)
    
    log_info "检查GitHub Actions状态..."
    
    # 获取最近的workflow运行
    local workflow_status
    workflow_status=$(gh run list --branch "$current_branch" --limit 1 --json status,conclusion --jq '.[0] | {status: .status, conclusion: .conclusion}')
    
    local status=$(echo "$workflow_status" | jq -r '.status')
    local conclusion=$(echo "$workflow_status" | jq -r '.conclusion')
    
    log_debug "Workflow状态: $status, 结论: $conclusion"
    
    if [ "$status" = "in_progress" ] || [ "$status" = "queued" ]; then
        log_warn "GitHub Actions正在运行中"
        read -p "是否继续推送？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return 1
        fi
    elif [ "$conclusion" = "failure" ] || [ "$conclusion" = "cancelled" ]; then
        log_error "GitHub Actions运行失败"
        return 1
    elif [ "$conclusion" = "success" ]; then
        log_info "GitHub Actions运行成功"
    else
        log_warn "GitHub Actions状态未知"
    fi
}

# 函数：检查GitLab CI状态
check_gitlab_ci() {
    if ! command_exists curl; then
        log_warn "curl未安装，跳过GitLab CI检查"
        return 0
    fi
    
    # 获取GitLab配置
    local gitlab_url
    local project_id
    gitlab_url=$(git config --get remote.origin.url | sed 's|git@||;s|https://||;s|:.*||;s|\.git$||')
    project_id=$(git config --get remote.origin.url | sed 's|.*/||;s|\.git$||')
    
    log_info "检查GitLab CI状态..."
    
    # 获取pipeline状态
    local pipeline_status
    pipeline_status=$(curl -s "https://$gitlab_url/api/v4/projects/$project_id/pipelines?per_page=1" | jq -r '.[0].status')
    
    log_debug "Pipeline状态: $pipeline_status"
    
    if [ "$pipeline_status" = "running" ] || [ "$pipeline_status" = "pending" ]; then
        log_warn "GitLab CI正在运行中"
        read -p "是否继续推送？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return 1
        fi
    elif [ "$pipeline_status" = "failed" ] || [ "$pipeline_status" = "canceled" ]; then
        log_error "GitLab CI运行失败"
        return 1
    elif [ "$pipeline_status" = "success" ]; then
        log_info "GitLab CI运行成功"
    else
        log_warn "GitLab CI状态未知"
    fi
}

# 函数：检查Jenkins状态
check_jenkins() {
    if ! command_exists curl; then
        log_warn "curl未安装，跳过Jenkins检查"
        return 0
    fi
    
    # 获取Jenkins配置
    local jenkins_url
    local job_name
    jenkins_url=$(git config --get jenkins.url)
    job_name=$(git config --get jenkins.job)
    
    if [ -z "$jenkins_url" ] || [ -z "$job_name" ]; then
        log_warn "Jenkins配置未设置，跳过Jenkins检查"
        return 0
    fi
    
    log_info "检查Jenkins状态..."
    
    # 获取构建状态
    local build_status
    build_status=$(curl -s "$jenkins_url/job/$job_name/lastBuild/api/json" | jq -r '.result')
    
    log_debug "构建状态: $build_status"
    
    if [ "$build_status" = "null" ] || [ "$build_status" = "RUNNING" ] || [ "$build_status" = "PENDING" ]; then
        log_warn "Jenkins正在运行中"
        read -p "是否继续推送？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return 1
        fi
    elif [ "$build_status" = "FAILURE" ] || [ "$build_status" = "ABORTED" ]; then
        log_error "Jenkins运行失败"
        return 1
    elif [ "$build_status" = "SUCCESS" ]; then
        log_info "Jenkins运行成功"
    else
        log_warn "Jenkins状态未知"
    fi
}

# 函数：检查部署准备状态
check_deployment_ready() {
    if [ "$REQUIRE_DEPLOYMENT_READY" = "false" ]; then
        return 0
    fi
    
    log_info "检查部署准备状态..."
    
    # 检查是否有部署配置
    if [ ! -f "deploy.yml" ] && [ ! -f "deployment.yaml" ]; then
        log_warn "未找到部署配置文件"
        read -p "是否继续推送？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return 1
        fi
    fi
    
    # 检查环境变量
    if [ -z "$DEPLOY_ENV" ]; then
        log_warn "未设置部署环境变量"
        read -p "是否继续推送？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return 1
    fi
    
    log_info "部署准备检查通过"
}

# 函数：触发CI/CD流水线
trigger_ci_pipeline() {
    log_info "触发CI/CD流水线..."
    
    case $CI_PLATFORM in
        "github")
            if command_exists gh; then
                gh workflow run
                log_info "GitHub Actions流水线已触发"
            fi
            ;;
        "gitlab")
            if command_exists curl; then
                local gitlab_url
                local project_id
                gitlab_url=$(git config --get remote.origin.url | sed 's|git@||;s|https://||;s|:.*||;s|\.git$||')
                project_id=$(git config --get remote.origin.url | sed 's|.*/||;s|\.git$||')
                curl -X POST "https://$gitlab_url/api/v4/projects/$project_id/pipeline"
                log_info "GitLab CI流水线已触发"
            fi
            ;;
        "jenkins")
            if command_exists curl; then
                local jenkins_url
                local job_name
                jenkins_url=$(git config --get jenkins.url)
                job_name=$(git config --get jenkins.job)
                curl -X POST "$jenkins_url/job/$job_name/build"
                log_info "Jenkins流水线已触发"
            fi
            ;;
    esac
}

# 主函数
main() {
    log_info "开始CI/CD集成检查..."
    
    # 读取推送信息
    while read local_ref local_sha remote_ref remote_sha; do
        log_info "推送信息："
        log_info "  本地引用: $local_ref"
        log_info "  本地SHA: $local_sha"
        log_info "  远程引用: $remote_ref"
        log_info "  远程SHA: $remote_sha"
        
        # 检查CI状态
        if [ "$REQUIRE_CI_SUCCESS" = "true" ]; then
            case $CI_PLATFORM in
                "github")
                    check_github_actions
                    ;;
                "gitlab")
                    check_gitlab_ci
                    ;;
                "jenkins")
                    check_jenkins
                    ;;
            esac
            
            if [ $? -ne 0 ]; then
                exit 1
            fi
        fi
        
        # 检查部署准备状态
        check_deployment_ready
        if [ $? -ne 0 ]; then
            exit 1
        fi
        
        # 触发CI/CD流水线
        trigger_ci_pipeline
        
        log_info "CI/CD集成检查通过"
    done
    
    exit 0
}

# 运行主函数
main
```

## 服务端钩子

### pre-receive钩子

#### 1. 基本用法

```bash
#!/bin/bash

# pre-receive钩子示例
# 在接收推送前运行检查

# 读取推送信息
while read oldrev newrev refname; do
    echo "推送信息："
    echo "  旧版本: $oldrev"
    echo "  新版本: $newrev"
    echo "  引用名: $refname"
    
    # 检查分支保护
    if [ "$refname" = "refs/heads/main" ]; then
        echo "检查主分支推送..."
        
        # 检查是否为强制推送
        if [ "$oldrev" != "0000000000000000000000000000000000000000" ]; then
            # 检查是否为快进推送
            if ! git merge-base --is-ancestor "$oldrev" "$newrev"; then
                echo "错误：不允许强制推送到主分支"
                exit 1
            fi
        fi
        
        # 检查提交数量
        if [ "$oldrev" != "0000000000000000000000000000000000000000" ]; then
            commit_count=$(git rev-list --count $oldrev..$newrev)
            echo "提交数量: $commit_count"
            
            if [ $commit_count -gt 10 ]; then
                echo "错误：主分支提交数量过多 ($commit_count)"
                exit 1
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
    fi
    
    # 检查是否推送到保护分支
    if [[ "$refname" =~ refs/heads/(main|develop|release) ]]; then
        echo "检查保护分支推送..."
        
        # 检查提交者权限
        author=$(git log --format=%an -n 1 $newrev)
        echo "提交者: $author"
        
        # 这里可以添加权限检查逻辑
        # 例如检查提交者是否在允许的列表中
        
        # 检查文件大小限制
        git diff-tree --no-commit-id --name-only -r $newrev | while read file; do
            if [ -f "$file" ]; then
                size=$(git cat-file -s "$newrev:$file")
                if [ $size -gt $((10 * 1024 * 1024)) ]; then  # 10MB
                    echo "错误：文件 $file 大小超过限制 ($size bytes)"
                    exit 1
                fi
            fi
        done
    fi
    
    echo "pre-receive检查通过"
done

exit 0
```

#### 2. 高级用法

```bash
#!/bin/bash

# 高级pre-receive钩子
# 支持分支保护、权限控制、详细日志

# 配置
PROTECTED_BRANCHES=("main" "develop" "release")
MAX_COMMIT_COUNT=10
MAX_FILE_SIZE=$((10 * 1024 * 1024))  # 10MB
REQUIRE_CODE_REVIEW=true
REQUIRE_CI_CHECK=true
ALLOWED_USERS=("admin" "lead-developer")

# 日志文件
LOG_FILE="/var/log/git/pre-receive.log"

# 函数：记录日志
log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
}

# 函数：检查是否为保护分支
is_protected_branch() {
    local branch="$1"
    for protected_branch in "${PROTECTED_BRANCHES[@]}"; do
        if [ "$branch" = "$protected_branch" ]; then
            return 0
        fi
    done
    return 1
}

# 函数：检查用户权限
check_user_permission() {
    local username="$1"
    
    for allowed_user in "${ALLOWED_USERS[@]}"; do
        if [ "$username" = "$allowed_user" ]; then
            return 0
        fi
    done
    
    return 1
}

# 函数：检查提交数量
check_commit_count() {
    local oldrev="$1"
    local newrev="$2"
    
    if [ "$oldrev" != "0000000000000000000000000000000000000000" ]; then
        local commit_count
        commit_count=$(git rev-list --count $oldrev..$newrev)
        log "INFO" "提交数量: $commit_count"
        
        if [ $commit_count -gt $MAX_COMMIT_COUNT ]; then
            log "ERROR" "提交数量过多 ($commit_count)，限制: $MAX_COMMIT_COUNT"
            echo "错误：提交数量过多 ($commit_count)，建议不超过 $MAX_COMMIT_COUNT 个"
            return 1
        fi
    fi
}

# 函数：检查提交信息格式
check_commit_messages() {
    local oldrev="$1"
    local newrev="$2"
    
    git rev-list $oldrev..$newrev | while read commit; do
        local message
        message=$(git log --format=%B -n 1 $commit)
        log "INFO" "检查提交: $commit"
        
        if ! echo "$message" | grep -qE "^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: "; then
            log "ERROR" "提交信息格式不正确: $message"
            echo "错误：提交信息格式不正确"
            echo "提交 $commit: $message"
            return 1
        fi
    done
}

# 函数：检查文件大小
check_file_sizes() {
    local newrev="$1"
    
    git diff-tree --no-commit-id --name-only -r $newrev | while read file; do
        if [ -f "$file" ]; then
            local size
            size=$(git cat-file -s "$newrev:$file")
            log "INFO" "检查文件: $file, 大小: $size"
            
            if [ $size -gt $MAX_FILE_SIZE ]; then
                log "ERROR" "文件大小超过限制: $file ($size bytes)"
                echo "错误：文件 $file 大小超过限制 ($size bytes)"
                return 1
            fi
        fi
    done
}

# 函数：检查敏感信息
check_sensitive_info() {
    local oldrev="$1"
    local newrev="$2"
    
    git diff $oldrev..$newrev | grep -i "password\|secret\|key\|token" > /dev/null
    if [ $? -eq 0 ]; then
        log "ERROR" "提交中可能包含敏感信息"
        echo "错误：提交中可能包含敏感信息"
        return 1
    fi
}

# 函数：检查代码审查
check_code_review() {
    if [ "$REQUIRE_CODE_REVIEW" = "false" ]; then
        return 0
    fi
    
    # 这里可以集成代码审查系统
    # 例如检查是否有对应的Pull Request
    # 检查审查者数量等
    
    log "INFO" "代码审查检查通过"
}

# 函数：检查CI状态
check_ci_status() {
    if [ "$REQUIRE_CI_CHECK" = "false" ]; then
        return 0
    fi
    
    # 这里可以集成CI系统
    # 例如检查CI是否通过
    # 检查测试覆盖率等
    
    log "INFO" "CI状态检查通过"
}

# 函数：生成推送报告
generate_push_report() {
    local oldrev="$1"
    local newrev="$2"
    local refname="$3"
    
    echo ""
    echo "=== 推送报告 ==="
    echo "分支: $refname"
    echo "旧版本: $oldrev"
    echo "新版本: $newrev"
    
    if [ "$oldrev" != "0000000000000000000000000000000000000000" ]; then
        echo ""
        echo "提交详情："
        git log --oneline $oldrev..$newrev
    fi
    
    echo ""
    echo "=== 报告结束 ==="
}

# 主函数
main() {
    log "INFO" "开始pre-receive检查"
    
    # 读取推送信息
    while read oldrev newrev refname; do
        log "INFO" "推送信息: oldrev=$oldrev, newrev=$newrev, refname=$refname"
        
        # 提取分支名称
        local branch_name
        branch_name=$(echo "$refname" | sed 's|refs/heads/||')
        
        # 获取提交者信息
        local author
        author=$(git log --format=%an -n 1 $newrev)
        local email
        email=$(git log --format=%ae -n 1 $newrev)
        
        log "INFO" "提交者: $author ($email)"
        
        # 检查保护分支
        if is_protected_branch "$branch_name"; then
            log "INFO" "检查保护分支: $branch_name"
            
            # 检查用户权限
            if ! check_user_permission "$author"; then
                log "ERROR" "用户 $author 没有权限推送到保护分支 $branch_name"
                echo "错误：您没有权限推送到保护分支 $branch_name"
                exit 1
            fi
            
            # 检查是否为强制推送
            if [ "$oldrev" != "0000000000000000000000000000000000000000" ]; then
                if ! git merge-base --is-ancestor "$oldrev" "$newrev"; then
                    log "ERROR" "检测到强制推送到保护分支"
                    echo "错误：不允许强制推送到保护分支"
                    exit 1
                fi
            fi
            
            # 检查提交数量
            check_commit_count "$oldrev" "$newrev"
            if [ $? -ne 0 ]; then
                exit 1
            fi
            
            # 检查提交信息格式
            check_commit_messages "$oldrev" "$newrev"
            if [ $? -ne 0 ]; then
                exit 1
            fi
            
            # 检查代码审查
            check_code_review
            if [ $? -ne 0 ]; then
                exit 1
            fi
            
            # 检查CI状态
            check_ci_status
            if [ $? -ne 0 ]; then
                exit 1
            fi
        fi
        
        # 检查文件大小
        check_file_sizes "$newrev"
        if [ $? -ne 0 ]; then
            exit 1
        fi
        
        # 检查敏感信息
        check_sensitive_info "$oldrev" "$newrev"
        if [ $? -ne 0 ]; then
            exit 1
        fi
        
        # 生成推送报告
        generate_push_report "$oldrev" "$newrev" "$refname"
        
        log "INFO" "pre-receive检查通过"
    done
    
    exit 0
}

# 运行主函数
main
```

#### 3. 集成外部系统

```bash
#!/bin/bash

# 集成外部系统的pre-receive钩子
# 集成JIRA、Slack、邮件通知等

# 配置
JIRA_URL="https://your-company.atlassian.net"
JIRA_USER="jira-bot"
JIRA_TOKEN=""
SLACK_WEBHOOK=""
EMAIL_RECIPIENTS="team@example.com"

# 日志文件
LOG_FILE="/var/log/git/pre-receive.log"

# 函数：记录日志
log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
}

# 函数：发送Slack通知
send_slack_notification() {
    local message="$1"
    local color="$2"
    
    if [ -n "$SLACK_WEBHOOK" ]; then
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\": \"$message\", \"color\": \"$color\"}" \
            "$SLACK_WEBHOOK" > /dev/null 2>&1
    fi
}

# 函数：发送邮件通知
send_email_notification() {
    local subject="$1"
    local body="$2"
    
    if [ -n "$EMAIL_RECIPIENTS" ]; then
        echo "$body" | mail -s "$subject" "$EMAIL_RECIPIENTS"
    fi
}

# 函数：验证JIRA Issue
validate_jira_issue() {
    local issue_key="$1"
    
    if [ -z "$JIRA_URL" ] || [ -z "$JIRA_USER" ] || [ -z "$JIRA_TOKEN" ]; then
        log "WARN" "JIRA配置不完整，跳过Issue验证"
        return 0
    fi
    
    # 检查Issue是否存在
    local response
    response=$(curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
        "$JIRA_URL/rest/api/2/issue/$issue_key")
    
    if echo "$response" | grep -q "errorMessages"; then
        log "ERROR" "JIRA Issue不存在: $issue_key"
        return 1
    fi
    
    # 检查Issue状态
    local issue_status
    issue_status=$(echo "$response" | jq -r '.fields.status.name')
    
    if [ "$issue_status" = "Closed" ] || [ "$issue_status" = "Done" ]; then
        log "ERROR" "JIRA Issue已关闭: $issue_key (状态: $issue_status)"
        return 1
    fi
    
    log "INFO" "JIRA Issue验证通过: $issue_key (状态: $issue_status)"
    return 0
}

# 函数：更新JIRA Issue
update_jira_issue() {
    local issue_key="$1"
    local comment="$2"
    local transition="$3"
    
    if [ -z "$JIRA_URL" ] || [ -z "$JIRA_USER" ] || [ -z "$JIRA_TOKEN" ]; then
        log "WARN" "JIRA配置不完整，跳过Issue更新"
        return 0
    fi
    
    # 添加评论
    if [ -n "$comment" ]; then
        curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
            -X POST \
            -H "Content-Type: application/json" \
            -d "{\"body\": \"$comment\"}" \
            "$JIRA_URL/rest/api/2/issue/$issue_key/comment" > /dev/null 2>&1
    fi
    
    # 更新状态
    if [ -n "$transition" ]; then
        # 获取可用的转换
        local transitions
        transitions=$(curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
            "$JIRA_URL/rest/api/2/issue/$issue_key/transitions")
        
        # 查找转换ID
        local transition_id
        transition_id=$(echo "$transitions" | jq -r ".transitions[] | select(.to.name == \"$transition\") | .id")
        
        if [ -n "$transition_id" ]; then
            curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
                -X POST \
                -H "Content-Type: application/json" \
                -d "{\"transition\": {\"id\": $transition_id}}" \
                "$JIRA_URL/rest/api/2/issue/$issue_key/transitions" > /dev/null 2>&1
        fi
    fi
}

# 函数：检查提交中的JIRA Issue
check_jira_issues() {
    local oldrev="$1"
    local newrev="$2"
    
    git rev-list $oldrev..$newrev | while read commit; do
        local message
        message=$(git log --format=%B -n 1 $commit)
        
        # 提取Issue Key
        local issue_keys
        issue_keys=$(echo "$message" | grep -oE '[A-Z]+-[0-9]+' | sort | uniq)
        
        if [ -n "$issue_keys" ]; then
            for issue_key in $issue_keys; do
                if ! validate_jira_issue "$issue_key"; then
                    echo "错误：JIRA Issue无效或已关闭: $issue_key"
                    return 1
                fi
            done
        else
            log "WARN" "提交未包含JIRA Issue: $commit"
        fi
    done
}

# 函数：处理推送完成后的操作
post_push_actions() {
    local oldrev="$1"
    local newrev="$2"
    local refname="$3"
    
    local branch_name
    branch_name=$(echo "$refname" | sed 's|refs/heads/||')
    
    local author
    author=$(git log --format=%an -n 1 $newrev)
    
    # 发送Slack通知
    local slack_message="🚀 新代码推送: $author 推送了 $branch_name"
    send_slack_notification "$slack_message" "good"
    
    # 发送邮件通知
    local email_subject="新代码推送: $branch_name"
    local email_body="作者: $author\n分支: $branch_name\n提交: $(git rev-list --count $oldrev..$newrev) 个"
    send_email_notification "$email_subject" "$email_body"
    
    # 更新JIRA Issues
    git rev-list $oldrev..$newrev | while read commit; do
        local message
        message=$(git log --format=%B -n 1 $commit)
        
        # 提取Issue Key
        local issue_keys
        issue_keys=$(echo "$message" | grep -oE '[A-Z]+-[0-9]+' | sort | uniq)
        
        if [ -n "$issue_keys" ]; then
            for issue_key in $issue_keys; do
                local comment="代码已推送到 $branch_name 分支\n提交: $commit\n作者: $author"
                update_jira_issue "$issue_key" "$comment" "In Progress"
            done
        fi
    done
}

# 主函数
main() {
    log "INFO" "开始pre-receive检查"
    
    # 读取推送信息
    while read oldrev newrev refname; do
        log "INFO" "推送信息: oldrev=$oldrev, newrev=$newrev, refname=$refname"
        
        # 提取分支名称
        local branch_name
        branch_name=$(echo "$refname" | sed 's|refs/heads/||')
        
        # 获取提交者信息
        local author
        author=$(git log --format=%an -n 1 $newrev)
        local email
        email=$(git log --format=%ae -n 1 $newrev)
        
        log "INFO" "提交者: $author ($email)"
        
        # 检查JIRA Issues
        check_jira_issues "$oldrev" "$newrev"
        if [ $? -ne 0 ]; then
            exit 1
        fi
        
        # 处理推送完成后的操作
        post_push_actions "$oldrev" "$newrev" "$refname"
        
        log "INFO" "pre-receive检查通过"
    done
    
    exit 0
}

# 运行主函数
main