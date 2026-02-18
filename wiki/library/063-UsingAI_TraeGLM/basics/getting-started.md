# AI使用入门

## 账号注册和API申请

### OpenAI账号注册

#### 注册流程
1. **访问官网**：前往 [OpenAI官网](https://openai.com)
2. **点击注册**：点击"Sign up"按钮
3. **填写信息**：输入邮箱地址和密码
4. **邮箱验证**：查收验证邮件并点击验证链接
5. **手机验证**：输入手机号码接收验证码（需要海外手机号）
6. **完成注册**：设置个人信息，完成账号创建

#### API密钥申请
1. **登录账号**：使用注册的账号登录
2. **进入API页面**：点击右上角"Personal" → "View API keys"
3. **创建密钥**：点击"Create new secret key"
4. **保存密钥**：复制生成的API密钥并妥善保存

```python
# 配置OpenAI API
import openai

# 设置API密钥
openai.api_key = 'sk-your-api-key-here'

# 测试连接
try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print("API连接成功！")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"API连接失败：{e}")
```

### Google AI账号注册

#### 注册流程
1. **访问Google AI平台**：前往 [Google AI Studio](https://aistudio.google.com)
2. **Google账号登录**：使用Google账号登录
3. **选择服务**：选择需要使用的AI服务（如Gemini）
4. **同意条款**：阅读并同意服务条款
5. **获取API密钥**：在控制台中创建API密钥

#### API配置
```python
# 配置Google AI API
import google.generativeai as genai

# 设置API密钥
genai.configure(api_key='your-google-api-key')

# 测试连接
try:
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Hello!")
    print("Google AI连接成功！")
    print(response.text)
except Exception as e:
    print(f"Google AI连接失败：{e}")
```

### 国内AI平台注册

#### 百度文心一言
1. **访问官网**：[百度智能云](https://cloud.baidu.com)
2. **注册账号**：完成手机号注册和实名认证
3. **开通服务**：选择"文心一言"服务
4. **获取密钥**：在控制台创建API Key和Secret Key

#### 阿里通义千问
1. **访问阿里云**：[阿里云](https://aliyun.com)
2. **注册账号**：完成企业或个人认证
3. **开通服务**：选择"通义千问"服务
4. **配置权限**：设置API访问权限

## 基础操作指南

### 第一个AI程序

#### 文本生成示例
```python
# 简单的文本生成程序
import openai

def generate_text(prompt, model="gpt-3.5-turbo"):
    """使用AI生成文本"""
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一个有帮助的AI助手"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"错误：{e}"

# 使用示例
if __name__ == "__main__":
    user_input = input("请输入您的问题：")
    result = generate_text(user_input)
    print("\nAI回答：")
    print(result)
```

#### 图像生成示例
```python
# 简单的图像生成程序
import openai
import requests
import os

def generate_image(prompt, size="1024x1024"):
    """使用AI生成图像"""
    try:
        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size=size
        )
        
        image_url = response['data'][0]['url']
        
        # 下载图像
        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            filename = f"generated_image_{int(time.time())}.png"
            with open(filename, 'wb') as f:
                f.write(img_response.content)
            return filename
        else:
            return None
    except Exception as e:
        return f"错误：{e}"

# 使用示例
if __name__ == "__main__":
    prompt = input("请输入图像描述：")
    result = generate_image(prompt)
    if result:
        print(f"图像已保存为：{result}")
    else:
        print("图像生成失败")
```

### 对话系统开发

#### 简单对话机器人
```python
import openai

class SimpleChatBot:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        """初始化聊天机器人"""
        openai.api_key = api_key
        self.model = model
        self.conversation_history = []
    
    def add_message(self, role, content):
        """添加消息到对话历史"""
        self.conversation_history.append({"role": role, "content": content})
    
    def get_response(self, user_input):
        """获取AI回复"""
        self.add_message("user", user_input)
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.conversation_history
            )
            
            ai_response = response.choices[0].message.content
            self.add_message("assistant", ai_response)
            
            return ai_response
        except Exception as e:
            return f"错误：{e}"
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []

# 使用示例
if __name__ == "__main__":
    api_key = "your-api-key"
    bot = SimpleChatBot(api_key)
    
    print("简单聊天机器人（输入'quit'退出）")
    while True:
        user_input = input("\n你：")
        if user_input.lower() == 'quit':
            break
        
        response = bot.get_response(user_input)
        print(f"AI：{response}")
```

### 语音交互系统

#### 语音识别和合成
```python
import speech_recognition as sr
import pyttsx3
import threading
import openai

class VoiceAssistant:
    def __init__(self, api_key):
        """初始化语音助手"""
        openai.api_key = api_key
        
        # 初始化语音识别
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # 初始化语音合成
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        
        # 调整麦克风噪音
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
    
    def speak(self, text):
        """文本转语音"""
        print(f"AI说：{text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """语音转文本"""
        with self.microphone as source:
            print("请说话...")
            audio = self.recognizer.listen(source)
        
        try:
            text = self.recognizer.recognize_google(audio, language='zh-CN')
            print(f"你说：{text}")
            return text
        except sr.UnknownValueError:
            print("无法识别语音")
            return None
        except sr.RequestError as e:
            print(f"语音识别错误：{e}")
            return None
    
    def get_ai_response(self, text):
        """获取AI回复"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个语音助手，回答要简洁明了"},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"错误：{e}"
    
    def run(self):
        """运行语音助手"""
        self.speak("语音助手已启动，请说话")
        
        while True:
            user_input = self.listen()
            
            if user_input:
                if user_input.lower() in ['退出', '再见', 'quit']:
                    self.speak("再见")
                    break
                
                ai_response = self.get_ai_response(user_input)
                self.speak(ai_response)

# 使用示例
if __name__ == "__main__":
    api_key = "your-api-key"
    assistant = VoiceAssistant(api_key)
    assistant.run()
```

## 费用和限制说明

### OpenAI定价结构

#### GPT系列定价
| 模型 | 输入价格（每1K tokens） | 输出价格（每1K tokens） |
|------|----------------------|----------------------|
| GPT-4 | $0.03 | $0.06 |
| GPT-4 Turbo | $0.01 | $0.03 |
| GPT-3.5 Turbo | $0.0015 | $0.002 |
| GPT-3.5 Turbo 16K | $0.003 | $0.004 |

#### 其他服务定价
- **DALL-E 3**：$0.04/图像（1024x1024）
- **Whisper**：$0.006/分钟
- **TTS**：$15.00/1M字符

#### 免费额度
- **新用户**：$5免费额度（有效期为3个月）
- **GPT-4限制**：每分钟40次请求
- **GPT-3.5限制**：每分钟3500次请求

### 成本控制策略

#### Token计算
```python
import tiktoken

def count_tokens(text, model="gpt-4"):
    """计算文本的token数量"""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def estimate_cost(text, model="gpt-4"):
    """估算API调用成本"""
    tokens = count_tokens(text, model)
    
    pricing = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002}
    }
    
    # 假设输出长度与输入相同
    total_cost = (tokens / 1000) * (pricing[model]["input"] + pricing[model]["output"])
    return total_cost

# 使用示例
text = "这是一个测试文本，用于计算token数量和成本估算。"
tokens = count_tokens(text)
cost = estimate_cost(text)

print(f"Token数量：{tokens}")
print(f"估算成本：${cost:.6f}")
```

#### 预算管理
```python
import openai
from datetime import datetime, timedelta

class BudgetManager:
    def __init__(self, monthly_budget=100):
        """初始化预算管理器"""
        self.monthly_budget = monthly_budget
        self.used_budget = 0
        self.daily_usage = {}
        self.reset_date = datetime.now() + timedelta(days=30)
    
    def can_spend(self, amount):
        """检查是否可以花费指定金额"""
        return (self.used_budget + amount) <= self.monthly_budget
    
    def spend(self, amount):
        """记录花费"""
        if self.can_spend(amount):
            self.used_budget += amount
            today = datetime.now().date()
            if today not in self.daily_usage:
                self.daily_usage[today] = 0
            self.daily_usage[today] += amount
            return True
        return False
    
    def get_remaining_budget(self):
        """获取剩余预算"""
        return self.monthly_budget - self.used_budget
    
    def get_daily_average(self):
        """获取日均使用量"""
        days_used = len(self.daily_usage)
        if days_used == 0:
            return 0
        return self.used_budget / days_used

# 使用示例
budget_manager = BudgetManager(monthly_budget=50)

# 模拟API调用
def safe_api_call(prompt, budget_manager):
    """安全的API调用，考虑预算限制"""
    estimated_cost = estimate_cost(prompt)
    
    if not budget_manager.can_spend(estimated_cost):
        return "错误：预算不足"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        # 记录实际花费
        actual_cost = estimate_cost(prompt) + estimate_cost(response.choices[0].message.content)
        budget_manager.spend(actual_cost)
        
        return response.choices[0].message.content
    except Exception as e:
        return f"API调用失败：{e}"
```

### 使用限制和配额

#### 速率限制
```python
import time
import requests
from requests.exceptions import RequestException

class RateLimiter:
    def __init__(self, max_requests_per_minute):
        """初始化速率限制器"""
        self.max_requests = max_requests_per_minute
        self.requests = []
    
    def wait_if_needed(self):
        """如果需要，等待直到可以发送请求"""
        now = time.time()
        
        # 清理1分钟前的请求记录
        self.requests = [req_time for req_time in self.requests if now - req_time < 60]
        
        # 如果达到限制，等待
        if len(self.requests) >= self.max_requests:
            sleep_time = 60 - (now - self.requests[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        # 记录当前请求
        self.requests.append(time.time())

# 使用示例
rate_limiter = RateLimiter(max_requests_per_minute=20)  # GPT-4限制

def rate_limited_api_call(prompt):
    """带速率限制的API调用"""
    rate_limiter.wait_if_needed()
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"API调用失败：{e}"
```

#### 内容限制
- **敏感内容**：禁止生成违法、有害内容
- **版权内容**：避免生成受版权保护的内容
- **个人隐私**：不要输入敏感个人信息
- **商业机密**：避免使用机密商业信息

## 安全和隐私保护

### API密钥安全

#### 密钥管理最佳实践
```python
import os
from dotenv import load_dotenv
import hashlib
import base64

class APIKeyManager:
    def __init__(self):
        """初始化API密钥管理器"""
        load_dotenv()  # 加载环境变量
        self.encrypted_keys = {}
    
    def encrypt_key(self, api_key, encryption_key):
        """加密API密钥"""
        # 使用简单的加密方法（实际应用中应使用更安全的加密）
        key_bytes = api_key.encode('utf-8')
        encryption_bytes = encryption_key.encode('utf-8')
        
        # 简单的XOR加密
        encrypted = bytes([b1 ^ b2 for b1, b2 in zip(key_bytes, encryption_bytes * len(key_bytes))])
        return base64.b64encode(encrypted).decode('utf-8')
    
    def decrypt_key(self, encrypted_key, encryption_key):
        """解密API密钥"""
        encrypted_bytes = base64.b64decode(encrypted_key.encode('utf-8'))
        encryption_bytes = encryption_key.encode('utf-8')
        
        # XOR解密
        decrypted = bytes([b1 ^ b2 for b1, b2 in zip(encrypted_bytes, encryption_bytes * len(encrypted_bytes))])
        return decrypted.decode('utf-8')
    
    def store_key(self, service_name, api_key, encryption_key):
        """存储加密的API密钥"""
        encrypted = self.encrypt_key(api_key, encryption_key)
        self.encrypted_keys[service_name] = encrypted
    
    def get_key(self, service_name, encryption_key):
        """获取解密的API密钥"""
        if service_name in self.encrypted_keys:
            return self.decrypt_key(self.encrypted_keys[service_name], encryption_key)
        return None

# 使用示例
key_manager = APIKeyManager()
encryption_key = "my-secret-encryption-key"

# 存储密钥
key_manager.store_key("openai", "sk-your-openai-key", encryption_key)
key_manager.store_key("google", "your-google-api-key", encryption_key)

# 获取密钥
openai_key = key_manager.get_key("openai", encryption_key)
google_key = key_manager.get_key("google", encryption_key)

print(f"OpenAI Key: {openai_key[:10]}...")
print(f"Google Key: {google_key[:10]}...")
```

#### 环境变量配置
```python
# .env文件内容
OPENAI_API_KEY=sk-your-openai-key
GOOGLE_API_KEY=your-google-api-key
BAIDU_API_KEY=your-baidu-api-key
ENCRYPTION_KEY=your-encryption-key

# Python代码中使用
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取API密钥
openai_key = os.getenv('OPENAI_API_KEY')
google_key = os.getenv('GOOGLE_API_KEY')
baidu_key = os.getenv('BAIDU_API_KEY')

# 使用密钥
if openai_key:
    openai.api_key = openai_key
    print("OpenAI API密钥已配置")
else:
    print("警告：OpenAI API密钥未配置")
```

### 数据隐私保护

#### 数据脱敏
```python
import re

class DataSanitizer:
    def __init__(self):
        """初始化数据脱敏器"""
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.phone_pattern = re.compile(r'\b(?:\+?86)?1[3-9]\d{9}\b')
        self.id_pattern = re.compile(r'\b\d{17}[\dXx]\b')
        self.credit_card_pattern = re.compile(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b')
    
    def sanitize_email(self, text):
        """脱敏邮箱地址"""
        return self.email_pattern.sub(lambda m: m.group()[0] + '***@' + m.group().split('@')[1], text)
    
    def sanitize_phone(self, text):
        """脱敏手机号码"""
        return self.phone_pattern.sub(lambda m: m.group()[0:3] + '****' + m.group()[7:], text)
    
    def sanitize_id(self, text):
        """脱敏身份证号"""
        return self.id_pattern.sub(lambda m: m.group()[0:6] + '********' + m.group()[-4:], text)
    
    def sanitize_credit_card(self, text):
        """脱敏信用卡号"""
        return self.credit_card_pattern.sub(lambda m: m.group()[0:4] + '****' + m.group()[-4:], text)
    
    def sanitize_all(self, text):
        """脱敏所有敏感信息"""
        text = self.sanitize_email(text)
        text = self.sanitize_phone(text)
        text = self.sanitize_id(text)
        text = self.sanitize_credit_card(text)
        return text

# 使用示例
sanitizer = DataSanitizer()

original_text = """
用户信息：
姓名：张三
邮箱：zhangsan@example.com