# MCP/Skills 企业实战补充内容

## 背景

内容审阅Agent发现现有章节(ch35-ch42)缺少以下企业级实战内容：
1. MCP服务离线检测与handshake验证
2. Skills动态路由（避免硬编码路径）
3. Skill链式调用的commit/rollback模式
4. 资源隔离（Docker/Web Workers沙箱）
5. 负向测试、并发测试、状态一致性测试

---

## 一、MCP Handshake验证与离线检测

### 问题场景
企业环境中MCP Server可能因部署、网络、负载等原因离线，客户端需优雅处理。

### 解决方案代码（补充到ch36）

```python
import asyncio
import httpx
from typing import Optional

class MCPHealthChecker:
    MCP_HANDSHAKE_TIMEOUT = 5.0
    
    async def check_server_health(
        self, 
        server_url: str,
        retry_count: int = 3,
        retry_delay: float = 1.0
    ) -> dict:
        for attempt in range(retry_count):
            try:
                async with httpx.AsyncClient(timeout=self.MCP_HANDSHAKE_TIMEOUT) as client:
                    response = await client.get(
                        f"{server_url}/health",
                        headers={"X-MCP-Protocol": "1.0"}
                    )
                    if response.status_code == 200:
                        return {
                            "status": "healthy",
                            "protocol_version": response.headers.get("X-MCP-Version"),
                            "latency_ms": response.elapsed.total_seconds() * 1000
                        }
            except httpx.TimeoutException:
                if attempt < retry_count - 1:
                    await asyncio.sleep(retry_delay * (attempt + 1))
                continue
            except httpx.ConnectError:
                return {"status": "offline", "error": "connection_refused"}
        
        return {"status": "unhealthy", "error": "timeout_after_retries"}

class MCPClientWithFallback:
    def __init__(self, primary_servers: list, fallback_servers: list):
        self.primary = primary_servers
        self.fallback = fallback_servers
        self.checker = MCPHealthChecker()
    
    async def get_available_server(self) -> Optional[str]:
        for server_url in self.primary:
            health = await self.checker.check_server_health(server_url)
            if health["status"] == "healthy":
                return server_url
        
        for server_url in self.fallback:
            health = await self.checker.check_server_health(server_url)
            if health["status"] == "healthy":
                return server_url
        
        return None
```

### 测试要点

| 测试类型 | 测试场景 | 验证点 |
|---------|---------|--------|
| 正向测试 | Server正常在线 | handshake成功，返回protocol_version |
| 超时测试 | Server响应超时 | retry机制生效，记录超时错误 |
| 离线测试 | Server完全离线 | 返回offline状态，fallback生效 |
| 协议不匹配 | Server版本不一致 | 提示protocol_version mismatch |
| 并发测试 | 100个并发health check | 不超过5s全部完成，无阻塞 |

---

## 二、Skills动态路由机制

### 问题场景
硬编码Skill路径导致：
- 部署变更时需重新修改代码
- 多环境(dev/staging/prod)难以切换
- Skill热更新困难

### 解决方案代码（补充到ch41）

```python
import json
from pathlib import Path
from typing import Dict, Callable

class SkillRouter:
    def __init__(self, config_path: str = "./skill_routes.json"):
        self.routes: Dict[str, str] = {}
        self.skill_cache: Dict[str, Callable] = {}
        self.load_routes(config_path)
    
    def load_routes(self, config_path: str):
        config = Path(config_path)
        if config.exists():
            with open(config) as f:
                self.routes = json.load(f)
        else:
            self.routes = self._discover_routes()
    
    def _discover_routes(self) -> Dict[str, str]:
        skills_dir = Path("./skills")
        discovered = {}
        for skill_file in skills_dir.glob("**/*.py"):
            skill_name = skill_file.stem
            discovered[skill_name] = str(skill_file)
        return discovered
    
    def get_skill(self, skill_name: str) -> Callable:
        if skill_name in self.skill_cache:
            return self.skill_cache[skill_name]
        
        if skill_name not in self.routes:
            raise SkillNotFoundError(f"Skill '{skill_name}' not in routes")
        
        skill_path = self.routes[skill_name]
        skill_module = self._load_skill_module(skill_path)
        self.skill_cache[skill_name] = skill_module
        return skill_module
    
    def reload_routes(self):
        self.routes.clear()
        self.skill_cache.clear()
        self.load_routes("./skill_routes.json")

class SkillNotFoundError(Exception):
    pass
```

### skill_routes.json 示例

```json
{
  "code_review": "./skills/analysis/code_review.py",
  "test_generator": "./skills/testing/test_gen.py",
  "doc_writer": "./skills/docs/doc_writer.py",
  "_env_override": {
    "production": {
      "code_review": "/opt/skills/code_review.py"
    }
  }
}
```

### 测试要点

| 测试类型 | 测试场景 | 验证点 |
|---------|---------|--------|
| 配置加载 | routes文件存在 | 正确加载所有路由 |
| 自动发现 | routes文件不存在 | 自动扫描skills目录 |
| 动态重载 | routes文件更新后reload | 新路由生效，旧缓存清除 |
| 环境切换 | 环境变量ENV=production | 使用production路由 |
| 错误处理 | Skill不存在 | 抛出SkillNotFoundError |
| 性能测试 | 调用同一Skill100次 | 缓存生效，无重复加载 |

---

## 三、Skill链Commit/Rollback模式

### 问题场景
多Skill协作时，中途失败需回滚已执行操作：
- Skill A: 创建测试文件
- Skill B: 运行测试（失败）
- 需回滚Skill A创建的文件

### 解决方案代码（补充到ch41）

```python
from typing import List, Any
from dataclasses import dataclass
from enum import Enum

class SkillExecutionState(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

@dataclass
class SkillExecutionRecord:
    skill_name: str
    input_data: Any
    output_data: Any
    rollback_action: Callable
    state: SkillExecutionState = SkillExecutionState.PENDING

class SkillChainExecutor:
    def __init__(self):
        self.execution_history: List[SkillExecutionRecord] = []
    
    def execute_chain(self, skill_chain: list, input_data: Any) -> dict:
        for skill_spec in skill_chain:
            skill_name = skill_spec["name"]
            rollback_handler = skill_spec.get("rollback")
            
            try:
                result = self._execute_skill(skill_name, input_data)
                record = SkillExecutionRecord(
                    skill_name=skill_name,
                    input_data=input_data,
                    output_data=result,
                    rollback_action=rollback_handler,
                    state=SkillExecutionState.SUCCESS
                )
                self.execution_history.append(record)
                input_data = result
            except Exception as e:
                self._rollback_all()
                return {"status": "failed", "error": str(e), "rolled_back": True}
        
        return {"status": "success", "result": input_data, "rolled_back": False}
    
    def _execute_skill(self, skill_name: str, data: Any) -> Any:
        import importlib
        skill_module = importlib.import_module(f"skills.{skill_name}")
        return skill_module.execute(data)
    
    def _rollback_all(self):
        for record in reversed(self.execution_history):
            if record.state == SkillExecutionState.SUCCESS and record.rollback_action:
                try:
                    record.rollback_action(record.output_data)
                    record.state = SkillExecutionState.ROLLED_BACK
                except Exception as e:
                    print(f"Rollback failed for {record.skill_name}: {e}")
        self.execution_history.clear()
```

### 使用示例

```python
chain = [
    {
        "name": "create_test_file",
        "rollback": lambda output: Path(output["file_path"]).unlink(missing_ok=True)
    },
    {
        "name": "run_tests",
        "rollback": lambda output: None
    },
    {
        "name": "generate_report",
        "rollback": lambda output: Path(output["report_path"]).unlink(missing_ok=True)
    }
]

executor = SkillChainExecutor()
result = executor.execute_chain(chain, {"test_name": "unit_test_001"})
```

### 测试要点

| 测试类型 | 测试场景 | 验证点 |
|---------|---------|--------|
| 全成功 | 3个Skill全部成功 | 返回success，无rollback |
| 中间失败 | 第2个Skill失败 | rollback第1个，返回failed |
| Rollback失败 | 第1个rollback异常 | 记录失败，继续rollback其他 |
| 空链 | chain=[] | 返回success，result=input |
| 并发执行 | 10个chain并发 | 各chain独立，history隔离 |
| 状态查询 | 执行后查询history | 正确记录SUCCESS/ROLLED_BACK |

---

## 四、资源隔离与沙箱机制

### 问题场景
Skill执行可能：
- 消耗过多内存/CPU
- 访问敏感文件
- 阻塞主进程

### 解决方案（补充到ch42）

#### 方案A: Docker容器隔离

```python
import docker
import json

class DockerSkillRunner:
    def __init__(self):
        self.client = docker.from_env()
        self.image_name = "skill-runner:latest"
    
    def run_in_container(
        self,
        skill_name: str,
        input_data: dict,
        timeout: int = 60,
        memory_limit: str = "512m"
    ) -> dict:
        container = self.client.containers.run(
            self.image_name,
            command=f"python -c 'from skills.{skill_name} import execute; import json; print(json.dumps(execute(json.loads(\"{json.dumps(input_data)}\"))))'",
            detach=True,
            mem_limit=memory_limit,
            cpu_period=100000,
            cpu_quota=50000,
            network_disabled=True,
            volumes={"./workspace": {"bind": "/workspace", "mode": "ro"}},
            remove=True
        )
        
        try:
            result = container.wait(timeout=timeout)
            logs = container.logs().decode()
            return json.loads(logs)
        except docker.errors.APIError:
            container.kill()
            raise SkillTimeoutError(f"Skill {skill_name} exceeded {timeout}s")
```

#### 方案B: Web Workers (浏览器环境)

```javascript
class SkillWorkerPool {
  constructor(poolSize = 4) {
    this.workers = [];
    this.taskQueue = [];
    for (let i = 0; i < poolSize; i++) {
      const worker = new Worker('skill-worker.js');
      worker.onmessage = (e) => this.handleWorkerResult(e);
      this.workers.push({ worker, busy: false });
    }
  }

  async executeSkill(skillName, inputData) {
    const availableWorker = this.workers.find(w => !w.busy);
    if (!availableWorker) {
      return new Promise(resolve => {
        this.taskQueue.push({ skillName, inputData, resolve });
      });
    }

    availableWorker.busy = true;
    availableWorker.worker.postMessage({ skillName, inputData });
    return new Promise(resolve => {
      availableWorker.currentResolve = resolve;
    });
  }

  handleWorkerResult(event) {
    const { workerId, result } = event.data;
    const worker = this.workers[workerId];
    worker.busy = false;
    worker.currentResolve(result);

    if (this.taskQueue.length > 0) {
      const nextTask = this.taskQueue.shift();
      this.executeSkill(nextTask.skillName, nextTask.inputData)
        .then(nextTask.resolve);
    }
  }
}
```

### 测试要点

| 测试类型 | Docker隔离 | Web Worker隔离 |
|---------|-----------|---------------|
| 内存限制 | 512m超限自动终止 | 无(浏览器限制) |
| CPU限制 | 50% quota限制 | 无(浏览器限制) |
| 网络隔离 | network_disabled | 无外部请求 |
| 文件访问 | 只读挂载 | 无文件系统 |
| 超时测试 | timeout=60s生效 | Worker.terminate() |
| 并发测试 | 10容器并行 | poolSize=4队列 |

---

## 五、测试用例补充清单

### MCP章节(ch35-ch38)应添加测试

| 章节 | 测试类型 | 用例 |
|-----|---------|-----|
| ch35 | 协议验证 | 协议版本不匹配、无效JSON-RPC格式 |
| ch36 | 负向测试 | Server返回error、超时、连接断开 |
| ch37 | 边界测试 | Tool参数类型错误、空参数、超大参数 |
| ch38 | 性能测试 | 高并发请求、大负载响应、长连接保持 |

### Skills章节(ch39-ch41)应添加测试

| 章节 | 测试类型 | 用例 |
|-----|---------|-----|
| ch39 | 加载测试 | Skill不存在、配置文件损坏、热重载 |
| ch40 | 执行测试 | Skill异常退出、依赖缺失、环境变量错误 |
| ch41 | 协作测试 | Skill循环依赖、链式rollback失败、并发冲突 |

### Harness章节(ch42)应添加测试

| 测试类型 | 用例 |
|---------|-----|
| 状态一致性 | 同一Dataset执行10次，成功率差异<5% |
| 隔离测试 | 多Harness并行，环境不互相干扰 |
| 恢复测试 | Executor崩溃后自动恢复执行 |

---

## 实施建议

### 优先级排序
1. **高优先级**：MCP Handshake验证（ch36）、Skill动态路由（ch41）
2. **中优先级**：Commit/Rollback模式（ch41）、负向测试补充
3. **低优先级**：Docker隔离（现有Harness已覆盖）

### 文件修改清单
- ch36.html: 添加Section 5.1 MCPHealthChecker
- ch41.html: 添加Section 4 SkillRouter动态路由
- ch41.html: 添加Section 5 SkillChainExecutor
- ch42.html: 添加Section 6 Docker/Web Worker隔离

---

## 验证命令

```bash
grep -l "MCPHealthChecker\|SkillRouter\|SkillChainExecutor\|DockerSkillRunner" ch*.html
```

---

生成时间: 2026-06-22
审阅来源: ses_112b5f146ffejRQxI6fO1NKbY5