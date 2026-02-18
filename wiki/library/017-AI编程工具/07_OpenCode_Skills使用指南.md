# OpenCode Skills 使用指南

Skills（技能）是 OpenCode 的扩展机制，允许开发者创建自定义的指令集和工作流自动化。

## Skills 概述

Skills 是打包的指令和脚本，用于扩展 Claude/OpenCode 的能力。每个 Skill 包含：
- SKILL.md - 技能定义文件
- scripts/ - 可执行脚本目录
- 配置文件

## 目录结构

```
skills/
  {skill-name}/           # 技能目录（kebab-case 命名）
    SKILL.md              # 必需：技能定义
    scripts/              # 必需：脚本目录
      {script-name}.sh    # Bash 脚本
  {skill-name}.zip       # 必需：分发用的压缩包
```

## SKILL.md 格式

```markdown
---
name: {skill-name}
description: {描述何时使用此技能，包含触发短语}
---

# {技能标题}

{简要描述技能功能}

## 工作原理

{编号列表解释技能工作流程}

## 使用方法

```bash
bash /mnt/skills/user/{skill-name}/scripts/{script}.sh [参数]
```

**参数：**
- arg1 - 描述（默认为 X）

**示例：**
{展示 2-3 个常用用法}

## 输出

{展示用户将看到的示例输出}

## 常见问题

{常见问题及解决方案}
```

## 创建自定义 Skill

### 1. 创建目录结构

```bash
mkdir -p my-skill/scripts
```

### 2. 编写 SKILL.md

```markdown
---
name: my-skill
description: 当用户说"运行我的任务"时触发此技能
---

# 我的自定义技能

帮助用户执行自定义任务。

## 使用方法

bash /mnt/skills/user/my-skill/run.sh
```

### 3. 编写脚本

```bash
#!/bin/bash
set -e

echo "正在执行任务..." >&2
echo '{"status": "success", "message": "任务完成"}'
```

### 4. 创建压缩包

```bash
cd skills
zip -r my-skill.zip my-skill/
```

## 安装 Skill

### Claude Code

```bash
cp -r skills/my-skill ~/.claude/skills/
```

### claude.ai

将 SKILL.md 内容添加到项目知识或粘贴到对话中。

## 现有 Skills 列表

| Skill | 描述 |
|-------|------|
| ai-sdk-5 | Vercel AI SDK 5 模式 |
| angular | Angular 性能优化 |
| api-designer | REST API 设计 |
| backend-standards | 后端编码标准 |
| debug-helper | 调试助手 |
| django-drf | Django REST Framework |
| frontend-standards | 前端编码标准 |
| github-pr | GitHub PR 创建 |
| jira-task | Jira 任务创建 |
| nextjs-15 | Next.js 15 App Router |
| playwright | Playwright E2E 测试 |
| react-19 | React 19 模式 |
| tailwind-4 | Tailwind CSS 4 |
| testing-best-practices | 测试最佳实践 |
| typescript | TypeScript 严格模式 |
| zustand-5 | Zustand 5 状态管理 |

## 最佳实践

1. **保持 SKILL.md 简洁** - 少于 500 行，详细内容放入单独文件
2. **编写具体描述** - 帮助 AI 准确判断何时激活技能
3. **使用渐进式披露** - 引用需要时才读取的支持文件
4. **优先使用脚本** - 脚本执行不消耗上下文
5. **错误处理** - 使用 `set -e` 实现快速失败

## 调试 Skill

```bash
# 测试脚本
bash -x scripts/your-script.sh

# 检查输出格式
bash scripts/your-script.sh | jq .
```

## 常见问题

### Q: Skill 不生效怎么办？

1. 确认 SKILL.md 格式正确
2. 检查脚本是否有执行权限
3. 验证压缩包是否正确打包

### Q: 如何更新已安装的 Skill？

```bash
# 重新复制
cp -r skills/updated-skill ~/.claude/skills/
```
