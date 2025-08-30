# 失败平台Base URL修复指南

基于真实API调测结果，以下是针对连接失败平台的具体修复建议：

---

## 🔧 豆包火山方舟 (doubao)

### 当前配置
```ini
[doubao]
api_key = 31219422-2f24-40d4-a8b6-5a2b19c39df6
base_url = https://ark.cn-beijing.volces.com
```

### 问题分析
- 所有尝试的API端点都返回404错误
- 可能的原因：API地址变更、认证方式不正确

### 修复建议
1. **更新base_url**（按优先级尝试）：
   ```ini
   # 选项1：新版API地址
   base_url = https://ark.cn-beijing.volces.com/api/v3
   
   # 选项2：通用端点
   base_url = https://open.volcengine.com/api/v1
   
   # 选项3：区域化端点
   base_url = https://ark.volces.com
   ```

2. **检查认证方式**：
   - 当前使用的是API Key，可能需要AK/SK认证
   - 在火山引擎控制台确认认证方式

3. **官方文档**：
   - 查看：https://www.volcengine.com/docs/82379
   - 确认最新的API规范和端点

---

## 🔧 智谱AI (zhipu) 

### 当前配置
```ini
[zhipu]
api_key = 8e12aed140fe43b88a96660f03053de4.FzEddkIBT4PE33Cs
base_url = https://open.bigmodel.cn
```

### 问题分析
- 多个API端点都返回404/500错误
- API密钥格式正确，但可能端点路径有变化

### 修复建议
1. **更新base_url**（按优先级尝试）：
   ```ini
   # 选项1：新版API地址（推荐）
   base_url = https://open.bigmodel.cn/api/paas/v4
   
   # 选项2：简化地址
   base_url = https://api.bigmodel.cn
   
   # 选项3：兼容地址
   base_url = https://open.bigmodel.cn/api/v1
   ```

2. **API端点说明**：
   - 智谱AI可能不提供标准的账单查询API
   - 建议在控制台查看账户信息：https://open.bigmodel.cn/usercenter/apikeys

3. **替代方案**：
   - 使用模型列表API验证连接性
   - 通过控制台手动查看账单信息

---

## 🔧 OpenAI (openai)

### 当前配置  
```ini
[openai]
api_key = sk-6O48HR8lE5tBuFCeabayCiicRxLQaINyGBqbIMOWbvAUtUTu
base_url = https://api.openai.com
```

### 问题分析
- 连接超时，可能是网络环境限制
- base_url本身是正确的

### 修复建议
1. **网络环境检查**：
   ```bash
   # 测试连接性
   curl -I https://api.openai.com
   
   # 如果需要代理
   export https_proxy=http://your-proxy:port
   ```

2. **替代base_url**（如果需要代理）：
   ```ini
   # 使用代理服务
   base_url = https://your-proxy-domain.com/v1
   
   # 或使用第三方OpenAI兼容服务
   base_url = https://api.openai-proxy.com/v1
   ```

3. **验证方法**：
   ```bash
   # 简单连接测试
   curl -H "Authorization: Bearer YOUR_API_KEY" \
        https://api.openai.com/v1/models
   ```

---

## 📝 快速修复配置文件

基于测试结果，建议的配置文件更新：

```ini
# 豆包火山 - 尝试新的API端点
[doubao]
api_key = 31219422-2f24-40d4-a8b6-5a2b19c39df6
base_url = https://ark.cn-beijing.volces.com/api/v3
enabled = true

# 智谱AI - 使用新版API路径
[zhipu]  
api_key = 8e12aed140fe43b88a96660f03053de4.FzEddkIBT4PE33Cs
base_url = https://open.bigmodel.cn/api/paas/v4
enabled = true

# OpenAI - 保持原配置，解决网络问题
[openai]
api_key = sk-6O48HR8lE5tBuFCeabayCiicRxLQaINyGBqbIMOWbvAUtUTu  
base_url = https://api.openai.com
enabled = true
```

---

## ⚡ 验证步骤

更新配置后，使用以下命令重新测试：

```bash
# 激活虚拟环境
source venv/bin/activate

# 重新运行测试
python test_real_api.py

# 或测试单个平台
python get_bill.py --platform doubao --format table
```

---

## 📚 官方文档链接

- **豆包火山**: https://www.volcengine.com/docs/82379
- **智谱AI**: https://open.bigmodel.cn/dev/api  
- **OpenAI**: https://platform.openai.com/docs/api-reference

建议在修复前先查阅最新的官方文档，确认API地址和认证方式的变更。