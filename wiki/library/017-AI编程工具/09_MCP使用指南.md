# MCP (Model Context Protocol) 使用指南

MCP（Model Context Protocol）是一个开放协议，允许 AI 模型与外部服务和工具进行标准化交互。

## 什么是 MCP

MCP 是 Anthropic 推出的协议，旨在：
- 标准化 AI 与工具的交互方式
- 简化工具集成流程
- 支持多种外部服务

## MCP 架构

### 1. MCP Host

运行 AI 应用的程序（如 Claude Code）

### 2. MCP Client

与 MCP Server 通信的客户端

### 3. MCP Server

提供工具和资源的外部服务

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  MCP Host   │────▶│ MCP Client  │────▶│ MCP Server  │
│ (Claude)    │     │             │     │ (工具服务)   │
└─────────────┘     └─────────────┘     └─────────────┘
```

## 安装 MCP Server

### 使用 npm 安装

```bash
# 安装 MCP Server
npm install -g @modelcontextprotocol/server

# 查看可用服务器
npm search @modelcontextprotocol
```

### 常用 MCP Servers

| Server | 用途 |
|--------|------|
| @modelcontextprotocol/server-filesystem | 文件系统操作 |
| @modelcontextprotocol/server-github | GitHub API |
| @modelcontextprotocol/server-slack | Slack 集成 |
| @modelcontextprotocol/server-git | Git 操作 |
| @modelcontextprotocol/server-brave-search | 网页搜索 |

## 配置 MCP

### 1. 配置文件位置

```
~/.claude/mcp.json
```

### 2. 基本配置

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
    },
    "github": {
      "command": "npx", 
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}
```

### 3. 环境变量

```bash
# 设置 GitHub Token
export GITHUB_TOKEN=your_token_here

# 设置 API Keys
export MCP_API_KEYS='{"service1": "key1", "service2": "key2"}'
```

## 使用 MCP Tools

### 在 Claude Code 中使用

```
# 查看可用工具
/tools

# 使用文件系统工具
读取 /path/to/file.txt 的内容

# 使用 GitHub 工具
列出我的 GitHub 仓库

# 使用搜索工具
搜索关于 React 18 的最新资讯
```

### 可用工具示例

#### 文件系统

```
- read_file: 读取文件
- write_file: 写入文件  
- list_directory: 列出目录
- create_directory: 创建目录
- move_file: 移动/重命名文件
- delete_file: 删除文件
- search_files: 搜索文件
```

#### GitHub

```
- get_repository: 获取仓库信息
- list_pull_requests: 列出 PR
- create_issue: 创建 Issue
- search_code: 搜索代码
```

#### Slack

```
- send_message: 发送消息
- list_channels: 列出频道
- search_messages: 搜索消息
```

## 创建自定义 MCP Server

### 1. 项目结构

```
my-mcp-server/
├── package.json
├── src/
│   └── index.ts
└── tsconfig.json
```

### 2. 编写 Server

```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

const server = new Server(
  {
    name: 'my-custom-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// 定义工具
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'my_tool',
        description: '我的自定义工具',
        inputSchema: {
          type: 'object',
          properties: {
            param: { type: 'string', description: '参数描述' }
          },
          required: ['param']
        }
      }
    ]
  };
});

// 处理工具调用
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  if (name === 'my_tool') {
    // 实现工具逻辑
    return { content: [{ type: 'text', text: '结果' }] };
  }
  
  throw new Error(`Unknown tool: ${name}`);
});

// 启动服务器
const transport = new StdioServerTransport();
await server.connect(transport);
```

### 3. 打包发布

```bash
npm publish
```

## 最佳实践

### 1. 安全性

- 限制文件系统访问范围
- 使用环境变量存储敏感信息
- 定期轮换 API Keys
- 审核工具权限

### 2. 性能

- 缓存频繁访问的数据
- 实现请求重试机制
- 设置合理的超时时间
- 批量处理请求

### 3. 错误处理

```typescript
try {
  // 工具逻辑
} catch (error) {
  return {
    content: [{
      type: 'text',
      text: `错误: ${error.message}`
    }],
    isError: true
  };
}
```

## 常见问题

### Q: MCP Server 启动失败？

检查：
1. Node.js 版本是否满足要求
2. 依赖是否正确安装
3. 配置文件格式是否正确

### Q: 工具调用超时？

增加超时配置：
```json
{
  "timeout": 60000
}
```

### Q: 如何调试 MCP？

```bash
# 启用调试日志
export DEBUG=mcp:*
```

### Q: 支持哪些编程语言？

MCP SDK 支持：
- TypeScript/JavaScript（官方）
- Python（非官方）
- Go（非官方）
- Rust（非官方）

## 相关资源

- [MCP 官方文档](https://modelcontextprotocol.io)
- [MCP SDK GitHub](https://github.com/modelcontextprotocol)
- [MCP Servers 列表](https://github.com/modelcontextprotocol/servers)
