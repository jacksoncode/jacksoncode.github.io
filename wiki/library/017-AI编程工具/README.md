# AI编程助手指南

## 简介

本指南全面介绍了当前主流的AI编程助手工具，帮助开发者了解、安装、配置和使用这些工具来提高编程效率。每个工具都有其独特的优势和适用场景，选择合适的工具可以显著提升开发体验。

## 文档内容

### 1. [Claude Code指南](01_Claude_Code.md)
Claude Code是Anthropic公司推出的AI编程助手，基于Claude模型系列。本指南包含：
- 安装和配置方法
- 多模型配置与切换（claude-3-opus、claude-3-sonnet、claude-3-haiku）
- 使用技巧和最佳实践
- 常见问题解决方案
- 实际应用示例

### 2. [Gemini CLI指南](02_Gemini_CLI.md)
Gemini CLI是Google提供的命令行工具，基于Gemini模型系列。本指南包含：
- 安装和认证配置
- 多模型配置与切换（gemini-pro、gemini-1.5-pro、gemini-1.5-flash）
- 高效使用技巧
- 常见问题解决方案
- 实际应用示例

### 3. [Qwen Code指南](03_Qwen_Code.md)
Qwen Code是阿里巴巴通义千问系列的编程助手工具。本指南包含：
- 安装和配置方法
- 多模型配置与切换（qwen-turbo、qwen-plus、qwen-max、qwen-coder）
- 高效使用技巧
- 常见问题解决方案
- 实际应用示例

### 4. [OpenAI CodeX指南](04_OpenAI_CodeX.md)
OpenAI CodeX是基于OpenAI的Codex模型的编程助手工具。本指南包含：
- 安装和配置方法
- 多模型配置与切换（davinci-codex、cushman-codex、code-davinci-002、code-cushman-001）
- 高效使用技巧
- 常见问题解决方案
- 实际应用示例

### 5. [iFlow CLI指南](05_iFlow_CLI.md)
iFlow CLI是一个多模型集成的AI编程助手工具。本指南包含：
- 安装和配置方法
- 多模型配置与切换（claude、gemini、qwen、codex）
- 高效使用技巧
- 常见问题解决方案
- 实际应用示例

## 如何查询本地安装了哪些工具

### Windows系统

#### 方法一：使用PowerShell命令
```powershell
# 检查npm包
Get-InstalledModule -Name "*claude*" -ErrorAction SilentlyContinue
Get-InstalledModule -Name "*gemini*" -ErrorAction SilentlyContinue
Get-InstalledModule -Name "*iflow*" -ErrorAction SilentlyContinue

# 检查Python包
pip list | Select-String -Pattern "(qwen|openai|codex)"

# 检查命令是否可用
Get-Command -Name "claude" -ErrorAction SilentlyContinue
Get-Command -Name "gemini" -ErrorAction SilentlyContinue
Get-Command -Name "qwen-code" -ErrorAction SilentlyContinue
Get-Command -Name "codex" -ErrorAction SilentlyContinue
Get-Command -Name "iflow" -ErrorAction SilentlyContinue
```

#### 方法二：使用命令提示符(CMD)
```cmd
# 检查npm包
npm list -g | findstr "claude gemini iflow"

# 检查Python包
pip list | findstr "qwen openai codex"

# 检查命令是否可用
where claude
where gemini
where qwen-code
where codex
where iflow
```

#### 方法三：创建检查脚本
创建一个PowerShell脚本 `check_ai_tools.ps1`：
```powershell
Write-Host "检查已安装的AI编程助手工具..." -ForegroundColor Green

$tools = @(
    @{Name="Claude Code"; Command="claude"; CheckCmd="claude --version"}
    @{Name="Gemini CLI"; Command="gemini"; CheckCmd="gemini --version"}
    @{Name="Qwen Code"; Command="qwen-code"; CheckCmd="qwen-code --version"}
    @{Name="OpenAI CodeX"; Command="codex"; CheckCmd="codex --version"}
    @{Name="iFlow CLI"; Command="iflow"; CheckCmd="iflow --version"}
)

foreach ($tool in $tools) {
    $command = Get-Command -Name $tool.Command -ErrorAction SilentlyContinue
    if ($command) {
        Write-Host "✓ $($tool.Name) 已安装: $($command.Source)" -ForegroundColor Green
        try {
            $version = Invoke-Expression $tool.CheckCmd 2>$null
            if ($version) {
                Write-Host "  版本信息: $version" -ForegroundColor Cyan
            }
        } catch {
            Write-Host "  无法获取版本信息" -ForegroundColor Yellow
        }
    } else {
        Write-Host "✗ $($tool.Name) 未安装" -ForegroundColor Red
    }
}
```

### Linux/macOS系统

#### 方法一：使用Shell命令
```bash
# 检查npm包
npm list -g | grep -E "(claude|gemini|iflow)"

# 检查Python包
pip list | grep -E "(qwen|openai|codex)"

# 检查命令是否可用
which claude
which gemini
which qwen-code
which codex
which iflow
```

#### 方法二：创建检查脚本
创建一个Shell脚本 `check_ai_tools.sh`：
```bash
#!/bin/bash

echo "检查已安装的AI编程助手工具..."

tools=(
    "Claude Code:claude:claude --version"
    "Gemini CLI:gemini:gemini --version"
    "Qwen Code:qwen-code:qwen-code --version"
    "OpenAI CodeX:codex:codex --version"
    "iFlow CLI:iflow:iflow --version"
)

for tool in "${tools[@]}"; do
    IFS=':' read -r name cmd version_cmd <<< "$tool"
    if command -v "$cmd" &> /dev/null; then
        echo "✓ $name 已安装: $(which $cmd)"
        version=$(eval "$version_cmd" 2>/dev/null)
        if [ -n "$version" ]; then
            echo "  版本信息: $version"
        else
            echo "  无法获取版本信息"
        fi
    else
        echo "✗ $name 未安装"
    fi
done
```

## 通用技巧

### 多工具协作工作流
- 根据任务类型选择最适合的工具
- 使用iFlow CLI组合多个工具的输出
- 在不同项目中使用不同的默认模型

### 配置同步方案
- 使用环境变量统一管理API密钥
- 创建配置模板便于快速部署
- 使用版本控制管理配置文件

### 安全最佳实践
- 不要将API密钥提交到版本控制系统
- 定期轮换API密钥
- 使用配置文件限制访问权限

## 如何开始

1. 阅读本README了解整体内容
2. 根据需求选择合适的工具
3. 按照相应工具的指南进行安装和配置
4. 运行检查脚本确认工具安装状态
5. 开始使用AI编程助手提升开发效率

## 贡献

欢迎提交Issue和Pull Request来改进本指南。如果您有新的工具推荐或使用技巧，请随时分享。

## 许可证

本指南采用MIT许可证，详见LICENSE文件。