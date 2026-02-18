# Agent Teams 使用指南

Agent Teams 是 OpenCode/Claude Code 的高级功能，允许你同时运行多个 AI Agent 协同工作，完成复杂任务。

## 什么是 Agent Teams

Agent Teams 让你能够：
- 同时协调多个专业 Agent
- 分工协作处理复杂任务
- 串联不同能力的 Agent
- 并行执行独立子任务

## 基本概念

### 1. Team Leader（团队领导）

负责协调其他 Agent 的主 Agent，分配任务并整合结果。

### 2. Specialist Agents（专业 Agent）

具有特定技能的 Agent，如：
- 代码审查 Agent
- 测试 Agent
- 文档 Agent
- 部署 Agent

### 3. Task Queue（任务队列）

管理待处理任务的队列，支持优先级和依赖关系。

## 使用方法

### 启动 Agent Team

```bash
# 使用预定义团队
opencode team frontend

# 自定义团队配置
opencode team --config my-team.json
```

### 团队配置文件

```json
{
  "name": "my-team",
  "leader": "coordinator",
  "agents": [
    {
      "name": "coder",
      "role": "代码开发",
      "skills": ["react", "typescript"]
    },
    {
      "name": "reviewer",
      "role": "代码审查",
      "skills": ["security", "best-practices"]
    },
    {
      "name": "tester",
      "role": "测试",
      "skills": ["playwright", "testing"]
    }
  ]
}
```

## 工作流程

### 1. 任务分配

团队领导分析任务，拆分为子任务：

```
用户请求 → 任务分析 → 子任务拆分 → 分配给专业 Agent
```

### 2. 并行执行

独立任务可以并行处理：

```
Agent A: 编写前端代码  ─┐
Agent B: 编写后端代码  ─┼─→ 结果整合
Agent C: 编写测试    ─┘
```

### 3. 顺序执行

有依赖关系的任务按顺序执行：

```
Agent A: 编写核心逻辑 → Agent B: 添加测试 → Agent C: 文档生成
```

### 4. 结果整合

团队领导整合所有 Agent 的输出，形成最终结果。

## 配置示例

### 全栈开发团队

```json
{
  "name": "fullstack-team",
  "leader": "coordinator",
  "agents": [
    {
      "name": "frontend-dev",
      "role": "前端开发",
      "capabilities": ["react", "css", "animations"]
    },
    {
      "name": "backend-dev", 
      "role": "后端开发",
      "capabilities": ["api", "database", "auth"]
    },
    {
      "name": "qa-engineer",
      "role": "质量保证",
      "capabilities": ["testing", "security-scan"]
    }
  ],
  "workflow": "parallel"
}
```

### 代码审查团队

```json
{
  "name": "review-team",
  "leader": "review-coordinator",
  "agents": [
    {
      "name": "security-reviewer",
      "role": "安全审查"
    },
    {
      "name": "performance-reviewer",
      "role": "性能审查"
    },
    {
      "name": "style-reviewer",
      "role": "代码风格审查"
    }
  ]
}
```

## 高级功能

### 1. 自定义 Agent 行为

```yaml
agent:
  name: custom-agent
  model: claude-3-opus
  temperature: 0.5
  max_iterations: 10
  timeout: 300
```

### 2. Agent 通信

Agents 可以相互通信和共享上下文：

```bash
# Agent A 完成后通知 Agent B
@agent-b continue_with context_from_agent_a
```

### 3. 条件触发

根据条件启动特定 Agent：

```yaml
triggers:
  - condition: "files_changed > 10"
    agent: "batch-processor"
  - condition: "has_security_changes"  
    agent: "security-reviewer"
```

## 最佳实践

### 1. 明确角色分工

每个 Agent 应有清晰的职责：
- 避免功能重叠
- 明确输入输出格式
- 设置合理的超时时间

### 2. 合理拆分任务

- 大任务拆分为独立子任务
- 识别任务间的依赖关系
- 设置合适的并行度

### 3. 错误处理

- 为每个 Agent 设置重试机制
- 建立降级策略
- 记录详细的执行日志

### 4. 监控与调试

```bash
# 查看团队执行状态
opencode team status

# 查看特定 Agent 日志
opencode team logs --agent coder

# 调试模式
opencode team debug --verbose
```

## 常见问题

### Q: Agent 之间如何共享数据？

通过团队领导协调，使用共享上下文或消息队列。

### Q: 如何控制执行成本？

设置 `max_tokens` 和 `max_iterations` 限制每个 Agent 的资源使用。

### Q: Agent 任务失败怎么办？

配置重试策略和降级方案，确保团队整体稳定性。

## 相关链接

- [OpenCode 官方文档](https://opencode.ai)
- [Claude Code 文档](https://docs.anthropic.com)
