#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI平台账单查询系统
支持多个主流AI平台的API使用量、余额、账单等信息查询

支持的平台：
- 国内平台：轨迹流动、DeepSeek、Kimi、豆包、火山方舟、智谱、腾讯混元、阿里云百炼、百度百川等
- 国际平台：OpenAI、Github Copilot、OpenRouter等
- 聚合平台：AiHubMix、魔塔社区、派欧云、henAPI等

作者：AI助手
版本：1.0.0
"""

import json
import logging
import requests
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import configparser
import os
from pathlib import Path
import hashlib
import hmac
import base64
from urllib.parse import quote


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PlatformType(Enum):
    """平台类型枚举"""
    DEEPSEEK = "deepseek"
    KIMI = "kimi"
    DOUBAO = "doubao"
    HUOSHAN = "huoshan"
    ZHIPU = "zhipu"
    TENCENT_HUNYUAN = "tencent_hunyuan"
    OPENAI = "openai"
    AIHUBMIX = "aihubmix"
    ALIYUN_BAILIAN = "aliyun_bailian"
    BAIDU_BAICHUAN = "baidu_baichuan"
    O3 = "o3"
    STEPFUN = "stepfun"
    MODELTACOM = "modeltacom"
    OCOOLAI = "ocoolai"
    PAIEUYUN = "paieuyun"
    GITHUB = "github"
    OPENROUTER = "openrouter"
    TENCENT_T1 = "tencent_t1"
    TIANYI_CLOUD = "tianyi_cloud"
    TAVILY = "tavily"
    HENAPI = "henapi"
    SILICONFLOW = "siliconflow"


@dataclass
class BillingInfo:
    """账单信息数据类"""
    platform: str
    balance: float  # 余额
    used_amount: float  # 已使用金额
    total_quota: float  # 总额度
    free_quota: float  # 免费额度
    recharged_amount: float  # 已充值金额
    gift_amount: float  # 赠送金额
    currency: str = "USD"  # 币种
    last_update: str = ""  # 最后更新时间
    expiry_date: Optional[str] = None  # 过期时间
    usage_details: Optional[Dict] = None  # 使用详情
    
    def __post_init__(self):
        if not self.last_update:
            self.last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict:
        return asdict(self)


class AIBillingException(Exception):
    """AI账单查询异常"""
    pass


class RateLimitException(AIBillingException):
    """请求频率限制异常"""
    pass


class AuthenticationException(AIBillingException):
    """认证异常"""
    pass


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = "ai_billing_config.ini"):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file, encoding='utf-8')
        else:
            self.create_default_config()
    
    def create_default_config(self):
        """创建默认配置文件"""
        # 添加默认配置段
        sections = [
            'deepseek', 'kimi', 'doubao', 'huoshan', 'zhipu', 'tencent_hunyuan',
            'openai', 'aihubmix', 'aliyun_bailian', 'baidu_baichuan', 'o3',
            'stepfun', 'modeltacom', 'ocoolai', 'paieuyun', 'github',
            'openrouter', 'tencent_t1', 'tianyi_cloud', 'tavily', 'henapi', 'siliconflow'
        ]
        
        for section in sections:
            self.config.add_section(section)
            self.config.set(section, 'api_key', '')
            self.config.set(section, 'base_url', '')
            self.config.set(section, 'enabled', 'false')
        
        # 添加通用配置
        self.config.add_section('general')
        self.config.set('general', 'request_timeout', '30')
        self.config.set('general', 'max_retries', '3')
        self.config.set('general', 'retry_delay', '1')
        
        self.save_config()
    
    def save_config(self):
        """保存配置文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            self.config.write(f)
    
    def get_platform_config(self, platform: str) -> Dict[str, str]:
        """获取平台配置"""
        if platform not in self.config:
            return {}
        return dict(self.config[platform])
    
    def set_platform_config(self, platform: str, **kwargs):
        """设置平台配置"""
        if platform not in self.config:
            self.config.add_section(platform)
        
        for key, value in kwargs.items():
            self.config.set(platform, key, str(value))
        
        self.save_config()


class BasePlatform(ABC):
    """基础平台抽象类"""
    
    def __init__(self, api_key: str, base_url: str = "", **kwargs):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AI-Billing-Monitor/1.0.0'
        })
        
        # 从kwargs中获取其他配置
        self.timeout = kwargs.get('timeout', 30)
        self.max_retries = kwargs.get('max_retries', 3)
        self.retry_delay = kwargs.get('retry_delay', 1)
    
    @abstractmethod
    def get_billing_info(self) -> BillingInfo:
        """获取账单信息 - 抽象方法，子类必须实现"""
        pass
    
    @property
    @abstractmethod
    def platform_name(self) -> str:
        """平台名称"""
        pass
    
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """发起HTTP请求，包含重试机制"""
        kwargs.setdefault('timeout', self.timeout)
        
        last_exception = None
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.request(method, url, **kwargs)
                
                # 检查HTTP状态码
                if response.status_code == 429:
                    raise RateLimitException(f"请求频率超限: {response.text}")
                elif response.status_code == 401:
                    raise AuthenticationException(f"认证失败: {response.text}")
                elif response.status_code >= 400:
                    raise AIBillingException(
                        f"HTTP {response.status_code}: {response.text}"
                    )
                
                return response
                
            except (requests.RequestException, AIBillingException) as e:
                last_exception = e
                if attempt < self.max_retries:
                    logger.warning(
                        f"{self.platform_name} 请求失败 (尝试 {attempt + 1}/{self.max_retries + 1}): {e}"
                    )
                    time.sleep(self.retry_delay * (2 ** attempt))  # 指数退避
                else:
                    break
        
        raise AIBillingException(
            f"{self.platform_name} 请求最终失败: {last_exception}"
        )
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """获取认证头 - 默认实现"""
        return {'Authorization': f'Bearer {self.api_key}'}


class PlatformFactory:
    """平台工厂类"""
    
    _platforms = {}
    
    @classmethod
    def register_platform(cls, platform_type: PlatformType, platform_class):
        """注册平台类"""
        cls._platforms[platform_type] = platform_class
    
    @classmethod
    def create_platform(cls, platform_type: PlatformType, **kwargs) -> BasePlatform:
        """创建平台实例"""
        if platform_type not in cls._platforms:
            raise ValueError(f"不支持的平台类型: {platform_type}")
        
        return cls._platforms[platform_type](**kwargs)


class BillingManager:
    """账单管理器"""
    
    def __init__(self, config_manager: Optional[ConfigManager] = None):
        self.config_manager = config_manager or ConfigManager()
        self.platforms: Dict[str, BasePlatform] = {}
    
    def add_platform(self, platform_type: PlatformType, **kwargs):
        """添加平台"""
        # 从配置文件获取平台配置
        config = self.config_manager.get_platform_config(platform_type.value)
        
        # 合并配置和传入参数
        platform_config = {**config, **kwargs}
        
        if not platform_config.get('api_key'):
            logger.warning(f"平台 {platform_type.value} 缺少API密钥")
            return
        
        if not platform_config.get('enabled', '').lower() == 'true':
            logger.info(f"平台 {platform_type.value} 未启用")
            return
        
        platform = PlatformFactory.create_platform(platform_type, **platform_config)
        self.platforms[platform_type.value] = platform
        logger.info(f"已添加平台: {platform_type.value}")
    
    def get_all_billing_info(self) -> Dict[str, BillingInfo]:
        """获取所有平台的账单信息"""
        results = {}
        
        for platform_name, platform in self.platforms.items():
            try:
                billing_info = platform.get_billing_info()
                results[platform_name] = billing_info
                logger.info(f"成功获取 {platform_name} 账单信息")
            except Exception as e:
                logger.error(f"获取 {platform_name} 账单信息失败: {e}")
                # 创建错误信息对象
                results[platform_name] = BillingInfo(
                    platform=platform_name,
                    balance=0,
                    used_amount=0,
                    total_quota=0,
                    free_quota=0,
                    recharged_amount=0,
                    gift_amount=0,
                    currency="USD",
                    usage_details={"error": str(e)}
                )
        
        return results
    
    def get_platform_billing_info(self, platform_name: str) -> Optional[BillingInfo]:
        """获取指定平台的账单信息"""
        if platform_name not in self.platforms:
            raise ValueError(f"平台 {platform_name} 未配置")
        
        return self.platforms[platform_name].get_billing_info()


# =============================================================================
# 平台实现类 - 国内主流平台
# =============================================================================

class DeepSeekPlatform(BasePlatform):
    """DeepSeek平台"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com", **kwargs):
        super().__init__(api_key, base_url, **kwargs)
    
    @property
    def platform_name(self) -> str:
        return "DeepSeek"
    
    def get_billing_info(self) -> BillingInfo:
        """获取DeepSeek账单信息"""
        headers = self._get_auth_headers()
        
        # 获取账户信息
        url = f"{self.base_url}/v1/user/balance"
        response = self._make_request("GET", url, headers=headers)
        data = response.json()
        
        # 安全的数据提取和类型转换
        def safe_float_convert(value, default=0.0):
            try:
                if isinstance(value, (int, float)):
                    return float(value)
                elif isinstance(value, str):
                    # 尝试转换字符串为数字
                    if value.replace('.', '').replace('-', '').isdigit():
                        return float(value)
                    return default
                else:
                    return default
            except (ValueError, TypeError):
                return default
        
        # 获取余额信息，支持多种数据结构
        balance_info = {}
        if 'balance_infos' in data and isinstance(data['balance_infos'], list) and len(data['balance_infos']) > 0:
            balance_info = data['balance_infos'][0]
        elif 'balance_info' in data:
            balance_info = data['balance_info']
        elif isinstance(data, dict):
            balance_info = data
        
        # 安全提取各个字段，同时处理分和元的转换
        available_balance = balance_info.get('available_balance', 0)
        used_balance = balance_info.get('used_balance', 0) 
        total_balance = balance_info.get('total_balance', 0)
        
        # DeepSeek可能返回分为单位，需要转换为元
        # 但需要先检查数值大小来判断是否需要转换
        def smart_convert(value):
            float_value = safe_float_convert(value)
            # 如果数值大于1000，可能是分为单位，需要除以100
            if float_value > 1000:
                return float_value / 100
            return float_value
        
        balance = smart_convert(available_balance)
        used_amount = smart_convert(used_balance)
        total_quota = smart_convert(total_balance)
        
        return BillingInfo(
            platform=self.platform_name,
            balance=balance,
            used_amount=used_amount,
            total_quota=total_quota,
            free_quota=0,
            recharged_amount=total_quota,
            gift_amount=0,
            currency="CNY",
            usage_details=data
        )


class KimiPlatform(BasePlatform):
    """Kimi平台"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.moonshot.cn", **kwargs):
        super().__init__(api_key, base_url, **kwargs)
    
    @property
    def platform_name(self) -> str:
        return "Kimi"
    
    def get_billing_info(self) -> BillingInfo:
        """获取Kimi账单信息"""
        headers = self._get_auth_headers()
        
        # 获取账户信息
        url = f"{self.base_url}/v1/users/me"
        response = self._make_request("GET", url, headers=headers)
        data = response.json()
        
        # 获取使用情况
        usage_url = f"{self.base_url}/v1/users/me/balance"
        usage_response = self._make_request("GET", usage_url, headers=headers)
        usage_data = usage_response.json()
        
        return BillingInfo(
            platform=self.platform_name,
            balance=usage_data.get('available_balance', 0),
            used_amount=usage_data.get('used_amount', 0),
            total_quota=usage_data.get('total_granted', 0),
            free_quota=usage_data.get('free_quota', 0),
            recharged_amount=usage_data.get('recharged_amount', 0),
            gift_amount=usage_data.get('gift_amount', 0),
            currency="CNY",
            usage_details={**data, **usage_data}
        )


class DoubaoHuoshanPlatform(BasePlatform):
    """豆包火山方舟平台"""
    
    def __init__(self, api_key: str, base_url: str = "https://ark.cn-beijing.volces.com", **kwargs):
        super().__init__(api_key, base_url, **kwargs)
        self.access_key = kwargs.get('access_key', '')
        self.secret_key = kwargs.get('secret_key', '')
    
    @property
    def platform_name(self) -> str:
        return "豆包火山方舟"
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """获取火山方舟认证头"""
        # 火山方舟支持多种认证方式
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'AI-Billing-Monitor/1.0.0'
        }
        
        if self.access_key and self.secret_key:
            # 使用AK/SK认证
            timestamp = str(int(time.time()))
            headers.update({
                'Authorization': f'VOLC-HMAC-SHA256 Credential={self.access_key}, SignedHeaders=, Signature=placeholder',
                'X-Date': timestamp
            })
        else:
            # 使用API Key认证
            headers['Authorization'] = f'Bearer {self.api_key}'
        
        return headers
    
    def get_billing_info(self) -> BillingInfo:
        """获取豆包火山方舟账单信息"""
        headers = self._get_auth_headers()
        
        # 火山方舟的可能API端点列表
        possible_endpoints = [
            # 标准账单端点
            f"{self.base_url}/api/v3/billing",
            f"{self.base_url}/api/v2/billing", 
            f"{self.base_url}/api/v1/billing",
            # 用户信息端点
            f"{self.base_url}/api/v1/user/info",
            f"{self.base_url}/api/v1/user/balance",
            # 服务信息端点
            f"{self.base_url}/api/v1/service/balance",
            f"{self.base_url}/api/v1/account",
            # OpenAI兼容端点
            f"{self.base_url}/api/v1/chat/completions",  # 可能包含限额信息
            f"{self.base_url}/v1/models",  # 模型列表
            f"{self.base_url}/v1/usage",
            # 新的端点
            f"{self.base_url}/open-api/v2/billing",
            f"{self.base_url}/open/api/v1/billing"
        ]
        
        for endpoint in possible_endpoints:
            try:
                logger.debug(f"尝试火山方舟端点: {endpoint}")
                
                # 对于模型列表，使用GET方法
                response = self._make_request("GET", endpoint, headers=headers)
                data = response.json()
                
                # 检查响应是否包含有效信息
                if self._is_valid_doubao_response(data):
                    return self._parse_doubao_data(data)
                
                # 如果是模型列表或有效响应，返回默认信息
                if ('models' in endpoint and 'data' in data) or ('completions' in endpoint):
                    logger.info(f"火山方舟 API连接正常，但无账单信息")
                    return BillingInfo(
                        platform=self.platform_name,
                        balance=0,
                        used_amount=0,
                        total_quota=0,
                        free_quota=0,
                        recharged_amount=0,
                        gift_amount=0,
                        currency="CNY",
                        usage_details={"note": "API连接正常，但无法获取账单信息", "endpoint": endpoint}
                    )
                
            except Exception as e:
                logger.debug(f"火山方舟端点 {endpoint} 失败: {e}")
                continue
        
        # 所有端点都失败
        return BillingInfo(
            platform=self.platform_name,
            balance=0,
            used_amount=0,
            total_quota=0,
            free_quota=0,
            recharged_amount=0,
            gift_amount=0,
            currency="CNY",
            usage_details={"error": "无法找到有效的账单API端点，请检查API密钥或查看火山引擎控制台"}
        )
    
    def _is_valid_doubao_response(self, data: dict) -> bool:
        """检查响应是否包含有效的账单信息"""
        if not isinstance(data, dict):
            return False
        
        billing_fields = [
            'balance', 'used_amount', 'total_quota', 'free_quota',
            'quota', 'usage', 'credit', 'limit', 'remaining',
            'account_balance', 'consumed', 'available'
        ]
        
        # 检查多层结构
        check_datas = [data]
        if 'data' in data:
            check_datas.append(data['data'])
        if 'result' in data:
            check_datas.append(data['result'])
        
        for check_data in check_datas:
            if isinstance(check_data, dict) and any(field in check_data for field in billing_fields):
                return True
        
        return False
    
    def _parse_doubao_data(self, data: dict) -> BillingInfo:
        """解析火山方舟数据"""
        # 处理多层嵌套结构
        billing_data = data
        if 'data' in data and isinstance(data['data'], dict):
            billing_data = data['data']
        elif 'result' in data and isinstance(data['result'], dict):
            billing_data = data['result']
        
        def safe_get_float(obj, *keys, default=0.0):
            for key in keys:
                if key in obj:
                    try:
                        value = obj[key]
                        if isinstance(value, (int, float)):
                            return float(value)
                        elif isinstance(value, str) and value.replace('.', '').replace('-', '').isdigit():
                            return float(value)
                    except (ValueError, TypeError):
                        continue
            return default
        
        balance = safe_get_float(billing_data, 'balance', 'account_balance', 'available', 'remaining')
        used_amount = safe_get_float(billing_data, 'used_amount', 'consumed', 'usage', 'used')
        total_quota = safe_get_float(billing_data, 'total_quota', 'quota', 'limit', 'credit', 'total')
        
        if total_quota == 0:
            total_quota = balance + used_amount
        
        return BillingInfo(
            platform=self.platform_name,
            balance=balance,
            used_amount=used_amount,
            total_quota=total_quota,
            free_quota=safe_get_float(billing_data, 'free_quota', 'free_credit'),
            recharged_amount=safe_get_float(billing_data, 'recharged_amount', 'paid_credit', default=total_quota),
            gift_amount=safe_get_float(billing_data, 'gift_amount', 'gift_credit', 'bonus'),
            currency="CNY",
            usage_details=data
        )


class ZhipuPlatform(BasePlatform):
    """智谱AI平台"""
    
    def __init__(self, api_key: str, base_url: str = "https://open.bigmodel.cn", **kwargs):
        super().__init__(api_key, base_url, **kwargs)
    
    @property
    def platform_name(self) -> str:
        return "智谱AI"
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """获取智谱AI认证头"""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'AI-Billing-Monitor/1.0.0'
        }
    
    def get_billing_info(self) -> BillingInfo:
        """获取智谱AI账单信息"""
        headers = self._get_auth_headers()
        
        # 智谱AI的可能API端点列表
        possible_endpoints = [
            # 标准账单端点
            f"{self.base_url}/api/paas/v4/billing/usage",
            f"{self.base_url}/api/paas/v4/billing/credit",
            f"{self.base_url}/api/paas/v3/billing/usage",
            f"{self.base_url}/api/paas/v3/billing/credit", 
            # 用户信息端点
            f"{self.base_url}/api/paas/v4/user/info",
            f"{self.base_url}/api/paas/v4/account",
            # 新版本API
            f"{self.base_url}/api/v4/billing",
            f"{self.base_url}/api/v4/usage",
            f"{self.base_url}/api/v4/account",
            # OpenAI兼容端点
            f"{self.base_url}/api/paas/v4/chat/completions",  # 可能包含限额信息
            f"{self.base_url}/api/paas/v4/models",  # 模型列表
            # 简化端点
            f"{self.base_url}/v4/billing",
            f"{self.base_url}/v4/usage",
            f"{self.base_url}/billing",
            f"{self.base_url}/usage"
        ]
        
        # 先尝试获取余额信息
        balance_data = None
        usage_data = None
        
        for endpoint in possible_endpoints:
            try:
                logger.debug(f"尝试智谱AI端点: {endpoint}")
                
                response = self._make_request("GET", endpoint, headers=headers)
                data = response.json()
                
                # 检查是否为有效响应
                if self._is_valid_zhipu_response(data):
                    # 区分余额信息和使用信息
                    if 'credit' in endpoint or 'balance' in endpoint.lower() or self._has_balance_info(data):
                        balance_data = data
                    else:
                        usage_data = data
                    
                    # 如果已经有了完整信息，直接返回
                    if self._has_complete_info(data):
                        return self._parse_zhipu_data(data, data)
                
                # 如果是模型列表或有效响应，记录但继续尝试
                if ('models' in endpoint and 'data' in data) or ('completions' in endpoint):
                    logger.info(f"智谱AI API连接正常: {endpoint}")
                    
            except Exception as e:
                logger.debug(f"智谱AI端点 {endpoint} 失败: {e}")
                continue
        
        # 如果有部分数据，尝试组合
        if balance_data or usage_data:
            return self._parse_zhipu_data(balance_data or {}, usage_data or {})
        
        # 所有端点都失败
        return BillingInfo(
            platform=self.platform_name,
            balance=0,
            used_amount=0,
            total_quota=0,
            free_quota=0,
            recharged_amount=0,
            gift_amount=0,
            currency="CNY",
            usage_details={"error": "无法找到有效的账单API端点，请检查API密钥或查看智谱AI控制台"}
        )
    
    def _is_valid_zhipu_response(self, data: dict) -> bool:
        """检查响应是否有效"""
        if not isinstance(data, dict):
            return False
        
        # 检查常见的账单字段
        billing_fields = [
            'balance', 'total_usage', 'total_credits', 'free_credits', 'paid_credits',
            'used_amount', 'quota', 'limit', 'credit', 'usage', 'remaining'
        ]
        
        # 检查多层结构
        check_datas = [data]
        if 'data' in data:
            check_datas.append(data['data'])
        if 'result' in data:
            check_datas.append(data['result'])
        
        for check_data in check_datas:
            if isinstance(check_data, dict) and any(field in check_data for field in billing_fields):
                return True
        
        return False
    
    def _has_balance_info(self, data: dict) -> bool:
        """检查是否包含余额信息"""
        balance_fields = ['balance', 'total_credits', 'free_credits', 'paid_credits', 'credit']
        
        check_datas = [data]
        if 'data' in data:
            check_datas.append(data['data'])
        
        for check_data in check_datas:
            if isinstance(check_data, dict) and any(field in check_data for field in balance_fields):
                return True
        return False
    
    def _has_complete_info(self, data: dict) -> bool:
        """检查是否包含完整信息"""
        required_fields = ['balance', 'total_usage']
        
        check_datas = [data]
        if 'data' in data:
            check_datas.append(data['data'])
        
        for check_data in check_datas:
            if isinstance(check_data, dict):
                has_balance = any(field in check_data for field in ['balance', 'total_credits', 'credit'])
                has_usage = any(field in check_data for field in ['total_usage', 'used_amount', 'usage'])
                if has_balance and has_usage:
                    return True
        return False
    
    def _parse_zhipu_data(self, balance_data: dict, usage_data: dict) -> BillingInfo:
        """解析智谱AI数据"""
        def safe_get_float(obj, *keys, default=0.0):
            if not isinstance(obj, dict):
                return default
            
            # 检查多层结构
            check_datas = [obj]
            if 'data' in obj:
                check_datas.append(obj['data'])
            if 'result' in obj:
                check_datas.append(obj['result'])
            
            for check_data in check_datas:
                if isinstance(check_data, dict):
                    for key in keys:
                        if key in check_data:
                            try:
                                value = check_data[key]
                                if isinstance(value, (int, float)):
                                    return float(value)
                                elif isinstance(value, str) and value.replace('.', '').replace('-', '').isdigit():
                                    return float(value)
                            except (ValueError, TypeError):
                                continue
            return default
        
        # 从余额数据中提取
        balance = safe_get_float(balance_data, 'balance', 'total_available')
        total_credits = safe_get_float(balance_data, 'total_credits', 'credit', 'quota')
        free_credits = safe_get_float(balance_data, 'free_credits', 'free_quota')
        paid_credits = safe_get_float(balance_data, 'paid_credits', 'recharged_amount')
        gift_credits = safe_get_float(balance_data, 'gift_credits', 'gift_amount')
        
        # 从使用数据中提取
        total_usage = safe_get_float(usage_data, 'total_usage', 'used_amount', 'usage')
        
        # 如果没有总余额，尝试计算
        if total_credits == 0:
            total_credits = balance + total_usage
        
        return BillingInfo(
            platform=self.platform_name,
            balance=balance,
            used_amount=total_usage,
            total_quota=total_credits,
            free_quota=free_credits,
            recharged_amount=paid_credits if paid_credits > 0 else total_credits,
            gift_amount=gift_credits,
            currency="CNY",
            usage_details={"balance_data": balance_data, "usage_data": usage_data}
        )


class TencentHunyuanPlatform(BasePlatform):
    """腾讯混元平台"""
    
    def __init__(self, api_key: str, base_url: str = "https://hunyuan.tencentcloudapi.com", **kwargs):
        super().__init__(api_key, base_url, **kwargs)
        self.secret_id = kwargs.get('secret_id', '')
        self.secret_key = kwargs.get('secret_key', '')
    
    @property
    def platform_name(self) -> str:
        return "腾讯混元"
    
    def get_billing_info(self) -> BillingInfo:
        """获取腾讯混元账单信息"""
        # 腾讯云需要特殊的认证方式
        headers = {
            'Authorization': self._get_tencent_auth(),
            'Content-Type': 'application/json'
        }
        
        # 获取账单信息 - 这里需要根据腾讯云实际API调整
        url = f"{self.base_url}/billing/usage"
        try:
            response = self._make_request("GET", url, headers=headers)
            data = response.json()
            
            return BillingInfo(
                platform=self.platform_name,
                balance=data.get('balance', 0),
                used_amount=data.get('used_amount', 0),
                total_quota=data.get('total_quota', 0),
                free_quota=data.get('free_quota', 0),
                recharged_amount=data.get('recharged_amount', 0),
                gift_amount=data.get('gift_amount', 0),
                currency="CNY",
                usage_details=data
            )
        except Exception as e:
            # 如果API不可用，返回占位符数据
            return BillingInfo(
                platform=self.platform_name,
                balance=0,
                used_amount=0,
                total_quota=0,
                free_quota=0,
                recharged_amount=0,
                gift_amount=0,
                currency="CNY",
                usage_details={"error": f"API暂不可用: {str(e)}"}
            )
    
    def _get_tencent_auth(self) -> str:
        """获取腾讯云认证字符串"""
        # 简化的认证实现，实际使用时需要完整的腾讯云签名算法
        return f"TC3-HMAC-SHA256 Credential={self.secret_id}, SignedHeaders=, Signature=placeholder"


class AliyunBailianPlatform(BasePlatform):
    """阿里云百炼平台"""
    
    def __init__(self, api_key: str, base_url: str = "https://dashscope.aliyuncs.com", **kwargs):
        super().__init__(api_key, base_url, **kwargs)
        self.access_key_id = kwargs.get('access_key_id', '')
        self.access_key_secret = kwargs.get('access_key_secret', '')
    
    @property
    def platform_name(self) -> str:
        return "阿里云百炼"
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """获取阿里云百炼认证头"""
        # 阿里云百炼使用X-DashScope-API-Key进行认证
        return {
            'Authorization': f'Bearer {self.api_key}',
            'X-DashScope-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }
    
    def get_billing_info(self) -> BillingInfo:
        """获取阿里云百炼账单信息"""
        headers = self._get_auth_headers()
        
        # 阿里云百炼的可能API端点列表
        possible_endpoints = [
            f"{self.base_url}/compatible-mode/v1/dashboard/billing/usage",
            f"{self.base_url}/api/v1/services/aigc/text-generation/generation",  # 可能包含用户信息
            f"{self.base_url}/api/v1/apps",  # 应用列表可能包含用户信息
            f"{self.base_url}/api/v1/usage",
            f"{self.base_url}/v1/billing",
            f"{self.base_url}/v1/usage",
            f"{self.base_url}/compatible-mode/v1/models",  # 模型列表
            # 兼容OpenAI的端点
            f"{self.base_url}/compatible-mode/v1/dashboard/billing/credit_grants",
            f"{self.base_url}/compatible-mode/v1/chat/completions",  # 可能包含限额信息
        ]
        
        for endpoint in possible_endpoints:
            try:
                logger.debug(f"尝试阿里云百炼端点: {endpoint}")
                
                # 对于模型列表类型的端点，用GET方法
                if 'models' in endpoint or 'apps' in endpoint:
                    response = self._make_request("GET", endpoint, headers=headers)
                else:
                    # 其他端点尝试GET方法
                    response = self._make_request("GET", endpoint, headers=headers)
                
                data = response.json()
                
                # 检查响应是否包含有效信息
                if self._is_valid_response(data):
                    return self._parse_aliyun_data(data)
                
                # 如果是模型列表，返回默认信息
                if 'models' in endpoint and isinstance(data, dict) and ('data' in data or 'model' in str(data).lower()):
                    logger.info(f"阿里云百炼 API连接正常，但无账单信息")
                    return BillingInfo(
                        platform=self.platform_name,
                        balance=0,
                        used_amount=0,
                        total_quota=0,
                        free_quota=0,
                        recharged_amount=0,
                        gift_amount=0,
                        currency="CNY",
                        usage_details={"note": "API连接正常，但无法获取账单信息", "endpoint": endpoint}
                    )
                    
            except Exception as e:
                logger.debug(f"阿里云百炼端点 {endpoint} 失败: {e}")
                continue
        
        # 所有端点都失败
        return BillingInfo(
            platform=self.platform_name,
            balance=0,
            used_amount=0,
            total_quota=0,
            free_quota=0,
            recharged_amount=0,
            gift_amount=0,
            currency="CNY",
            usage_details={"error": "无法找到有效的账单API端点，请检查API密钥或查看阿里云控制台"}
        )
    
    def _is_valid_response(self, data: dict) -> bool:
        """检查响应是否包含有效的账单信息"""
        if not isinstance(data, dict):
            return False
        
        # 检查常见的账单字段
        billing_fields = [
            'balance', 'used_amount', 'total_quota', 'free_quota',
            'credit', 'usage', 'quota', 'limit', 'remaining',
            'total_usage', 'available_balance'
        ]
        
        # 检查data或data.data中是否包含账单字段
        check_data = data
        if 'data' in data and isinstance(data['data'], dict):
            check_data = data['data']
        
        return any(field in check_data for field in billing_fields)
    
    def _parse_aliyun_data(self, data: dict) -> BillingInfo:
        """解析阿里云百炼数据"""
        # 处理嵌套的data结构
        if 'data' in data and isinstance(data['data'], dict):
            billing_data = data['data']
        else:
            billing_data = data
        
        # 安全的数值提取函数
        def safe_get_float(obj, *keys, default=0.0):
            for key in keys:
                if key in obj:
                    try:
                        value = obj[key]
                        if isinstance(value, (int, float)):
                            return float(value)
                        elif isinstance(value, str) and value.replace('.', '').replace('-', '').isdigit():
                            return float(value)
                    except (ValueError, TypeError):
                        continue
            return default
        
        balance = safe_get_float(billing_data, 'balance', 'available_balance', 'remaining')
        used_amount = safe_get_float(billing_data, 'used_amount', 'total_usage', 'usage')
        total_quota = safe_get_float(billing_data, 'total_quota', 'quota', 'limit', 'credit')
        
        if total_quota == 0:
            total_quota = balance + used_amount
        
        return BillingInfo(
            platform=self.platform_name,
            balance=balance,
            used_amount=used_amount,
            total_quota=total_quota,
            free_quota=safe_get_float(billing_data, 'free_quota', 'free_credit'),
            recharged_amount=safe_get_float(billing_data, 'recharged_amount', 'paid_credit', default=total_quota),
            gift_amount=safe_get_float(billing_data, 'gift_amount', 'gift_credit'),
            currency="CNY",
            usage_details=data
        )


class BaiduBaichuanPlatform(BasePlatform):
    """百度百川平台"""
    
    def __init__(self, api_key: str, base_url: str = "https://aip.baidubce.com", **kwargs):
        super().__init__(api_key, base_url, **kwargs)
        self.secret_key = kwargs.get('secret_key', '')
    
    @property
    def platform_name(self) -> str:
        return "百度百川"
    
    def get_billing_info(self) -> BillingInfo:
        """获取百度百川账单信息"""
        # 获取access token
        token_url = f"https://aip.baidubce.com/oauth/2.0/token"
        token_params = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.secret_key
        }
        
        try:
            token_response = self._make_request("POST", token_url, data=token_params)
            token_data = token_response.json()
            access_token = token_data.get('access_token', '')
            
            if not access_token:
                raise AuthenticationException("无法获取access token")
            
            # 获取账单信息
            headers = {'Content-Type': 'application/json'}
            url = f"{self.base_url}/rest/2.0/wenxin/v1/billing/usage?access_token={access_token}"
            response = self._make_request("GET", url, headers=headers)
            data = response.json()
            
            return BillingInfo(
                platform=self.platform_name,
                balance=data.get('result', {}).get('balance', 0),
                used_amount=data.get('result', {}).get('used_amount', 0),
                total_quota=data.get('result', {}).get('total_quota', 0),
                free_quota=data.get('result', {}).get('free_quota', 0),
                recharged_amount=data.get('result', {}).get('recharged_amount', 0),
                gift_amount=data.get('result', {}).get('gift_amount', 0),
                currency="CNY",
                usage_details=data
            )
        except Exception as e:
            return BillingInfo(
                platform=self.platform_name,
                balance=0,
                used_amount=0,
                total_quota=0,
                free_quota=0,
                recharged_amount=0,
                gift_amount=0,
                currency="CNY",
                usage_details={"error": f"API暂不可用: {str(e)}"}
            )


# =============================================================================
# 平台实现类 - 国际平台
# =============================================================================

class OpenAIPlatform(BasePlatform):
    """OpenAI平台"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com", **kwargs):
        super().__init__(api_key, base_url, **kwargs)
    
    @property
    def platform_name(self) -> str:
        return "OpenAI"
    
    def get_billing_info(self) -> BillingInfo:
        """获取OpenAI账单信息"""
        headers = self._get_auth_headers()
        
        # 获取账单信息
        billing_url = f"{self.base_url}/v1/dashboard/billing/credit_grants"
        usage_url = f"{self.base_url}/v1/dashboard/billing/usage"
        
        try:
            # 获取余额信息
            billing_response = self._make_request("GET", billing_url, headers=headers)
            billing_data = billing_response.json()
            
            # 获取使用情况
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            usage_params = {'start_date': start_date, 'end_date': end_date}
            
            usage_response = self._make_request("GET", usage_url, headers=headers, params=usage_params)
            usage_data = usage_response.json()
            
            total_granted = billing_data.get('total_granted', 0)
            total_used = billing_data.get('total_used', 0)
            total_available = billing_data.get('total_available', 0)
            
            return BillingInfo(
                platform=self.platform_name,
                balance=total_available,
                used_amount=total_used,
                total_quota=total_granted,
                free_quota=0,
                recharged_amount=total_granted,
                gift_amount=0,
                currency="USD",
                usage_details={**billing_data, **usage_data}
            )
        except Exception as e:
            return BillingInfo(
                platform=self.platform_name,
                balance=0,
                used_amount=0,
                total_quota=0,
                free_quota=0,
                recharged_amount=0,
                gift_amount=0,
                currency="USD",
                usage_details={"error": f"API暂不可用: {str(e)}"}
            )


class OpenRouterPlatform(BasePlatform):
    """OpenRouter平台"""
    
    def __init__(self, api_key: str, base_url: str = "https://openrouter.ai", **kwargs):
        super().__init__(api_key, base_url, **kwargs)
    
    @property
    def platform_name(self) -> str:
        return "OpenRouter"
    
    def get_billing_info(self) -> BillingInfo:
        """获取OpenRouter账单信息"""
        headers = self._get_auth_headers()
        
        # 获取账单信息
        url = f"{self.base_url}/api/v1/auth/key"
        
        try:
            response = self._make_request("GET", url, headers=headers)
            data = response.json()
            
            # OpenRouter返回的数据结构
            usage = data.get('data', {})
            
            return BillingInfo(
                platform=self.platform_name,
                balance=usage.get('usage', 0),
                used_amount=usage.get('usage', 0),
                total_quota=usage.get('limit', 0),
                free_quota=0,
                recharged_amount=usage.get('limit', 0),
                gift_amount=0,
                currency="USD",
                usage_details=data
            )
        except Exception as e:
            return BillingInfo(
                platform=self.platform_name,
                balance=0,
                used_amount=0,
                total_quota=0,
                free_quota=0,
                recharged_amount=0,
                gift_amount=0,
                currency="USD",
                usage_details={"error": f"API暂不可用: {str(e)}"}
            )


class GithubPlatform(BasePlatform):
    """Github Copilot平台"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.github.com", **kwargs):
        super().__init__(api_key, base_url, **kwargs)
    
    @property
    def platform_name(self) -> str:
        return "Github Copilot"
    
    def get_billing_info(self) -> BillingInfo:
        """获取Github Copilot账单信息"""
        headers = {
            'Authorization': f'token {self.api_key}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        try:
            # 获取用户信息
            user_url = f"{self.base_url}/user"
            user_response = self._make_request("GET", user_url, headers=headers)
            user_data = user_response.json()
            
            # Github Copilot账单信息通常需要组织级别权限
            # 这里返回基本信息
            return BillingInfo(
                platform=self.platform_name,
                balance=0,  # Github Copilot通常是订阅制
                used_amount=0,
                total_quota=0,
                free_quota=0,
                recharged_amount=0,
                gift_amount=0,
                currency="USD",
                usage_details={"user": user_data, "note": "Github Copilot使用订阅制计费"}
            )
        except Exception as e:
            return BillingInfo(
                platform=self.platform_name,
                balance=0,
                used_amount=0,
                total_quota=0,
                free_quota=0,
                recharged_amount=0,
                gift_amount=0,
                currency="USD",
                usage_details={"error": f"API暂不可用: {str(e)}"}
            )


# =============================================================================
# 聚合平台实现
# =============================================================================

class AiHubMixPlatform(BasePlatform):
    """AiHubMix聚合平台"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.aihubmix.com", **kwargs):
        super().__init__(api_key, base_url, **kwargs)
    
    @property
    def platform_name(self) -> str:
        return "AiHubMix"
    
    def get_billing_info(self) -> BillingInfo:
        """获取AiHubMix账单信息"""
        headers = self._get_auth_headers()
        
        try:
            # 获取账单信息
            url = f"{self.base_url}/v1/billing/usage"
            response = self._make_request("GET", url, headers=headers)
            data = response.json()
            
            return BillingInfo(
                platform=self.platform_name,
                balance=data.get('balance', 0),
                used_amount=data.get('used', 0),
                total_quota=data.get('total', 0),
                free_quota=data.get('free_quota', 0),
                recharged_amount=data.get('recharged', 0),
                gift_amount=data.get('gift', 0),
                currency="USD",
                usage_details=data
            )
        except Exception as e:
            return BillingInfo(
                platform=self.platform_name,
                balance=0,
                used_amount=0,
                total_quota=0,
                free_quota=0,
                recharged_amount=0,
                gift_amount=0,
                currency="USD",
                usage_details={"error": f"API暂不可用: {str(e)}"}
            )


class StepfunPlatform(BasePlatform):
    """阶跃星辰平台"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.stepfun.com", **kwargs):
        super().__init__(api_key, base_url, **kwargs)
    
    @property
    def platform_name(self) -> str:
        return "阶跃星辰"
    
    def get_billing_info(self) -> BillingInfo:
        """获取阶跃星辰账单信息"""
        headers = self._get_auth_headers()
        
        try:
            # 获取账单信息
            url = f"{self.base_url}/v1/billing/credit_grants"
            response = self._make_request("GET", url, headers=headers)
            data = response.json()
            
            return BillingInfo(
                platform=self.platform_name,
                balance=data.get('total_available', 0),
                used_amount=data.get('total_used', 0),
                total_quota=data.get('total_granted', 0),
                free_quota=data.get('free_quota', 0),
                recharged_amount=data.get('recharged_amount', 0),
                gift_amount=data.get('gift_amount', 0),
                currency="CNY",
                usage_details=data
            )
        except Exception as e:
            return BillingInfo(
                platform=self.platform_name,
                balance=0,
                used_amount=0,
                total_quota=0,
                free_quota=0,
                recharged_amount=0,
                gift_amount=0,
                currency="CNY",
                usage_details={"error": f"API暂不可用: {str(e)}"}
            )


class SiliconFlowPlatform(BasePlatform):
    """硅基流动平台"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.siliconflow.cn", **kwargs):
        super().__init__(api_key, base_url, **kwargs)
    
    @property
    def platform_name(self) -> str:
        return "硅基流动"
    
    def get_billing_info(self) -> BillingInfo:
        """获取硅基流动账单信息"""
        headers = self._get_auth_headers()
        
        try:
            # 硅基流动的正确 API 端点列表（按优先级排序）
            possible_endpoints = [
                f"{self.base_url}/v1/user/info",
                f"{self.base_url}/v1/models",  # 可能包含用户信息
                f"{self.base_url}/user/balance",
                f"{self.base_url}/user/info",
                f"{self.base_url}/api/user/balance",
                f"{self.base_url}/balance",
                f"{self.base_url}/account"
            ]
            
            # 先尝试获取用户信息
            for endpoint in possible_endpoints:
                try:
                    response = self._make_request("GET", endpoint, headers=headers)
                    data = response.json()
                    
                    # 检查响应是否包含有用信息
                    if self._is_valid_billing_response(data):
                        return self._parse_siliconflow_data(data)
                    
                except Exception as e:
                    logger.debug(f"端点 {endpoint} 失败: {e}")
                    continue
            
            # 如果所有端点都失败，尝试使用通用方法
            logger.info("尝试使用通用OpenAI兼容接口...")
            
            # 通用 OpenAI 兼容端点
            openai_endpoints = [
                f"{self.base_url}/v1/dashboard/billing/credit_grants",
                f"{self.base_url}/v1/billing/usage",
                f"{self.base_url}/dashboard/billing/credit_grants"
            ]
            
            for endpoint in openai_endpoints:
                try:
                    response = self._make_request("GET", endpoint, headers=headers)
                    data = response.json()
                    
                    if self._is_valid_billing_response(data):
                        return self._parse_siliconflow_data(data)
                        
                except Exception as e:
                    logger.debug(f"OpenAI兼容端点 {endpoint} 失败: {e}")
                    continue
            
            # 都失败后返回默认数据
            raise Exception("无法找到有效的账单API端点")
            
        except Exception as e:
            return BillingInfo(
                platform=self.platform_name,
                balance=0,
                used_amount=0,
                total_quota=0,
                free_quota=0,
                recharged_amount=0,
                gift_amount=0,
                currency="CNY",
                usage_details={"error": f"API暂不可用: {str(e)}"}
            )
    
    def _is_valid_billing_response(self, data: dict) -> bool:
        """检查响应是否包含有效的账单信息"""
        if not isinstance(data, dict):
            return False
        
        # 检查常见的账单字段
        billing_fields = [
            'balance', 'available_balance', 'total_available', 'remaining_balance',
            'used', 'used_amount', 'total_used', 'consumed',
            'total', 'total_quota', 'total_granted', 'total_credits',
            'credits', 'quota', 'limit'
        ]
        
        # 检查data或data.data中是否包含账单字段
        check_data = data
        if 'data' in data and isinstance(data['data'], dict):
            check_data = data['data']
        
        return any(field in check_data for field in billing_fields)
    
    def _parse_siliconflow_data(self, data: dict) -> BillingInfo:
        """解析硅基流动的数据"""
        # 处理嵌套的data结构
        if 'data' in data and isinstance(data['data'], dict):
            billing_data = data['data']
        else:
            billing_data = data
        
        # 安全的数值提取函数
        def safe_get_float(obj, *keys, default=0.0):
            for key in keys:
                if key in obj:
                    try:
                        value = obj[key]
                        if isinstance(value, (int, float)):
                            return float(value)
                        elif isinstance(value, str) and value.replace('.', '').replace('-', '').isdigit():
                            return float(value)
                    except (ValueError, TypeError):
                        continue
            return default
        
        # 提取各种可能的字段
        balance = safe_get_float(billing_data, 'balance', 'available_balance', 'total_available', 'remaining_balance')
        used_amount = safe_get_float(billing_data, 'used', 'used_amount', 'total_used', 'consumed')
        total_quota = safe_get_float(billing_data, 'total', 'total_quota', 'total_granted', 'total_credits', 'credits', 'quota', 'limit')
        
        # 如果没有总额度，尝试计算
        if total_quota == 0:
            total_quota = balance + used_amount
        
        return BillingInfo(
            platform=self.platform_name,
            balance=balance,
            used_amount=used_amount,
            total_quota=total_quota,
            free_quota=safe_get_float(billing_data, 'free_quota', 'free_credits'),
            recharged_amount=safe_get_float(billing_data, 'recharged_amount', 'paid_credits', default=total_quota),
            gift_amount=safe_get_float(billing_data, 'gift_amount', 'gift_credits', 'bonus'),
            currency=billing_data.get('currency', 'CNY'),
            usage_details=data
        )


# 通用平台类，适用于大多数遵循OpenAI API规范的平台
class GenericOpenAIPlatform(BasePlatform):
    """通用OpenAI兼容平台"""
    
    def __init__(self, api_key: str, base_url: str, platform_name: str, **kwargs):
        super().__init__(api_key, base_url, **kwargs)
        self._platform_name = platform_name
    
    @property
    def platform_name(self) -> str:
        return self._platform_name
    
    def get_billing_info(self) -> BillingInfo:
        """获取通用平台账单信息"""
        headers = self._get_auth_headers()
        
        # 常见的账单API端点
        possible_endpoints = [
            f"{self.base_url}/v1/billing/usage",
            f"{self.base_url}/v1/billing/credit_grants",
            f"{self.base_url}/v1/dashboard/billing/credit_grants",
            f"{self.base_url}/api/v1/billing",
            f"{self.base_url}/billing"
        ]
        
        for endpoint in possible_endpoints:
            try:
                response = self._make_request("GET", endpoint, headers=headers)
                data = response.json()
                
                # 尝试解析常见的数据结构
                balance = (
                    data.get('balance', 0) or 
                    data.get('total_available', 0) or
                    data.get('available_balance', 0) or
                    0
                )
                
                used = (
                    data.get('used', 0) or
                    data.get('used_amount', 0) or
                    data.get('total_used', 0) or
                    0
                )
                
                total = (
                    data.get('total', 0) or
                    data.get('total_quota', 0) or
                    data.get('total_granted', 0) or
                    balance + used
                )
                
                return BillingInfo(
                    platform=self.platform_name,
                    balance=balance,
                    used_amount=used,
                    total_quota=total,
                    free_quota=data.get('free_quota', 0),
                    recharged_amount=data.get('recharged_amount', total),
                    gift_amount=data.get('gift_amount', 0),
                    currency=data.get('currency', 'USD'),
                    usage_details=data
                )
                
            except Exception:
                continue
        
        # 如果所有端点都失败，返回错误信息
        return BillingInfo(
            platform=self.platform_name,
            balance=0,
            used_amount=0,
            total_quota=0,
            free_quota=0,
            recharged_amount=0,
            gift_amount=0,
            currency="USD",
            usage_details={"error": "无法找到有效的账单API端点"}
        )


# 注册平台类到工厂
PlatformFactory.register_platform(PlatformType.DEEPSEEK, DeepSeekPlatform)
PlatformFactory.register_platform(PlatformType.KIMI, KimiPlatform)
PlatformFactory.register_platform(PlatformType.DOUBAO, DoubaoHuoshanPlatform)
PlatformFactory.register_platform(PlatformType.HUOSHAN, DoubaoHuoshanPlatform)
PlatformFactory.register_platform(PlatformType.ZHIPU, ZhipuPlatform)
PlatformFactory.register_platform(PlatformType.TENCENT_HUNYUAN, TencentHunyuanPlatform)
PlatformFactory.register_platform(PlatformType.ALIYUN_BAILIAN, AliyunBailianPlatform)
PlatformFactory.register_platform(PlatformType.BAIDU_BAICHUAN, BaiduBaichuanPlatform)
PlatformFactory.register_platform(PlatformType.OPENAI, OpenAIPlatform)
PlatformFactory.register_platform(PlatformType.OPENROUTER, OpenRouterPlatform)
PlatformFactory.register_platform(PlatformType.GITHUB, GithubPlatform)
PlatformFactory.register_platform(PlatformType.AIHUBMIX, AiHubMixPlatform)
PlatformFactory.register_platform(PlatformType.STEPFUN, StepfunPlatform)
PlatformFactory.register_platform(PlatformType.SILICONFLOW, SiliconFlowPlatform)

# 为其他平台创建通用实现
def create_generic_platform(platform_type: PlatformType, **kwargs):
    """为通用平台创建实例"""
    platform_configs = {
        PlatformType.MODELTACOM: {"platform_name": "魔塔社区", "base_url": "https://api.modelscope.cn"},
        PlatformType.OCOOLAI: {"platform_name": "ocoolAI", "base_url": "https://api.ocool.ai"},
        PlatformType.PAIEUYUN: {"platform_name": "派欧云", "base_url": "https://api.paieuyun.com"},
        PlatformType.HENAPI: {"platform_name": "henAPI", "base_url": "https://api.henapi.com"},
        PlatformType.O3: {"platform_name": "O3", "base_url": "https://api.o3.com"},
        PlatformType.TENCENT_T1: {"platform_name": "腾讯T1", "base_url": "https://api.tencent-t1.com"},
        PlatformType.TIANYI_CLOUD: {"platform_name": "天翼云", "base_url": "https://api.ctyun.cn"},
        PlatformType.TAVILY: {"platform_name": "Tavily", "base_url": "https://api.tavily.com"}
    }
    
    config = platform_configs.get(platform_type, {})
    merged_config = {**config, **kwargs}
    
    return GenericOpenAIPlatform(**merged_config)

# 注册通用平台
for platform_type in [PlatformType.MODELTACOM, PlatformType.OCOOLAI, PlatformType.PAIEUYUN, 
                      PlatformType.HENAPI, PlatformType.O3, PlatformType.TENCENT_T1, 
                      PlatformType.TIANYI_CLOUD, PlatformType.TAVILY]:
    def make_generic_creator(pt):
        return lambda **kwargs: create_generic_platform(pt, **kwargs)
    
    PlatformFactory.register_platform(platform_type, make_generic_creator(platform_type))


# =============================================================================
# 数据格式化和展示功能
# =============================================================================

class OutputFormat(Enum):
    """输出格式枚举"""
    JSON = "json"
    TABLE = "table"
    CSV = "csv"
    MARKDOWN = "markdown"
    HTML = "html"


class BillingFormatter:
    """账单信息格式化器"""
    
    @staticmethod
    def format_as_json(billing_data: Dict[str, BillingInfo], indent: int = 2) -> str:
        """格式化为JSON"""
        json_data = {}
        for platform, info in billing_data.items():
            json_data[platform] = info.to_dict()
        
        return json.dumps(json_data, indent=indent, ensure_ascii=False)
    
    @staticmethod
    def format_as_table(billing_data: Dict[str, BillingInfo]) -> str:
        """格式化为表格"""
        try:
            from tabulate import tabulate
        except ImportError:
            return BillingFormatter._format_as_simple_table(billing_data)
        
        headers = ['平台', '余额', '已使用', '总额度', '免费额度', '已充值', '赠送', '币种', '更新时间']
        rows = []
        
        for platform, info in billing_data.items():
            rows.append([
                info.platform,
                f"{info.balance:.4f}",
                f"{info.used_amount:.4f}",
                f"{info.total_quota:.4f}",
                f"{info.free_quota:.4f}",
                f"{info.recharged_amount:.4f}",
                f"{info.gift_amount:.4f}",
                info.currency,
                info.last_update
            ])
        
        return tabulate(rows, headers=headers, tablefmt='grid')
    
    @staticmethod
    def _format_as_simple_table(billing_data: Dict[str, BillingInfo]) -> str:
        """简单表格格式（不依赖tabulate库）"""
        lines = []
        lines.append("-" * 120)
        lines.append(f"{'平台':<15} {'余额':<12} {'已使用':<12} {'总额度':<12} {'免费额度':<12} {'已充值':<12} {'赠送':<12} {'币种':<6} {'更新时间':<20}")
        lines.append("-" * 120)
        
        for platform, info in billing_data.items():
            lines.append(
                f"{info.platform:<15} "
                f"{info.balance:<12.4f} "
                f"{info.used_amount:<12.4f} "
                f"{info.total_quota:<12.4f} "
                f"{info.free_quota:<12.4f} "
                f"{info.recharged_amount:<12.4f} "
                f"{info.gift_amount:<12.4f} "
                f"{info.currency:<6} "
                f"{info.last_update:<20}"
            )
        
        lines.append("-" * 120)
        return "\n".join(lines)
    
    @staticmethod
    def format_as_csv(billing_data: Dict[str, BillingInfo]) -> str:
        """格式化为CSV"""
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        
        # 写入表头
        writer.writerow(['平台', '余额', '已使用', '总额度', '免费额度', '已充值', '赠送', '币种', '更新时间'])
        
        # 写入数据
        for platform, info in billing_data.items():
            writer.writerow([
                info.platform,
                info.balance,
                info.used_amount,
                info.total_quota,
                info.free_quota,
                info.recharged_amount,
                info.gift_amount,
                info.currency,
                info.last_update
            ])
        
        return output.getvalue()
    
    @staticmethod
    def format_as_markdown(billing_data: Dict[str, BillingInfo]) -> str:
        """格式化为Markdown表格"""
        lines = []
        lines.append("| 平台 | 余额 | 已使用 | 总额度 | 免费额度 | 已充值 | 赠送 | 币种 | 更新时间 |")
        lines.append("|------|------|--------|--------|----------|--------|------|------|----------|")
        
        for platform, info in billing_data.items():
            lines.append(
                f"| {info.platform} "
                f"| {info.balance:.4f} "
                f"| {info.used_amount:.4f} "
                f"| {info.total_quota:.4f} "
                f"| {info.free_quota:.4f} "
                f"| {info.recharged_amount:.4f} "
                f"| {info.gift_amount:.4f} "
                f"| {info.currency} "
                f"| {info.last_update} |"
            )
        
        return "\n".join(lines)
    
    @staticmethod
    def format_as_html(billing_data: Dict[str, BillingInfo]) -> str:
        """格式化为HTML表格"""
        html = ["<table border='1' style='border-collapse: collapse; width: 100%;'>"]
        html.append("<tr style='background-color: #f2f2f2;'>")
        html.append("<th>平台</th><th>余额</th><th>已使用</th><th>总额度</th><th>免费额度</th><th>已充值</th><th>赠送</th><th>币种</th><th>更新时间</th>")
        html.append("</tr>")
        
        for platform, info in billing_data.items():
            html.append("<tr>")
            html.append(f"<td>{info.platform}</td>")
            html.append(f"<td>{info.balance:.4f}</td>")
            html.append(f"<td>{info.used_amount:.4f}</td>")
            html.append(f"<td>{info.total_quota:.4f}</td>")
            html.append(f"<td>{info.free_quota:.4f}</td>")
            html.append(f"<td>{info.recharged_amount:.4f}</td>")
            html.append(f"<td>{info.gift_amount:.4f}</td>")
            html.append(f"<td>{info.currency}</td>")
            html.append(f"<td>{info.last_update}</td>")
            html.append("</tr>")
        
        html.append("</table>")
        return "\n".join(html)
    
    @classmethod
    def format(cls, billing_data: Dict[str, BillingInfo], output_format: OutputFormat) -> str:
        """根据指定格式格式化数据"""
        formatters = {
            OutputFormat.JSON: cls.format_as_json,
            OutputFormat.TABLE: cls.format_as_table,
            OutputFormat.CSV: cls.format_as_csv,
            OutputFormat.MARKDOWN: cls.format_as_markdown,
            OutputFormat.HTML: cls.format_as_html
        }
        
        formatter = formatters.get(output_format)
        if formatter:
            return formatter(billing_data)
        else:
            raise ValueError(f"不支持的输出格式: {output_format}")


class BillingReporter:
    """账单报告生成器"""
    
    def __init__(self, billing_manager: BillingManager):
        self.billing_manager = billing_manager
        self.formatter = BillingFormatter()
    
    def generate_report(self, output_format: OutputFormat = OutputFormat.TABLE, 
                       save_to_file: Optional[str] = None) -> str:
        """生成账单报告"""
        billing_data = self.billing_manager.get_all_billing_info()
        report_content = self.formatter.format(billing_data, output_format)
        
        if save_to_file:
            with open(save_to_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            logger.info(f"报告已保存到: {save_to_file}")
        
        return report_content
    
    def generate_summary(self) -> Dict[str, Any]:
        """生成汇总信息"""
        billing_data = self.billing_manager.get_all_billing_info()
        
        summary = {
            "总平台数": len(billing_data),
            "成功查询": sum(1 for info in billing_data.values() 
                         if info.usage_details and 'error' not in info.usage_details),
            "查询失败": sum(1 for info in billing_data.values() 
                         if info.usage_details and 'error' in info.usage_details),
            "总余额": {},
            "总已使用": {},
            "平台列表": list(billing_data.keys()),
            "生成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 按币种统计
        for platform, info in billing_data.items():
            currency = info.currency
            if currency not in summary["总余额"]:
                summary["总余额"][currency] = 0
                summary["总已使用"][currency] = 0
            
            summary["总余额"][currency] += info.balance
            summary["总已使用"][currency] += info.used_amount
        
        return summary
    
    def save_detailed_report(self, output_dir: str = "./billing_reports"):
        """保存详细报告"""
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存各种格式的报告
        formats = {
            "json": OutputFormat.JSON,
            "csv": OutputFormat.CSV,
            "md": OutputFormat.MARKDOWN,
            "html": OutputFormat.HTML
        }
        
        saved_files = []
        for ext, fmt in formats.items():
            filename = f"billing_report_{timestamp}.{ext}"
            filepath = os.path.join(output_dir, filename)
            self.generate_report(fmt, filepath)
            saved_files.append(filepath)
        
        # 保存汇总信息
        summary_file = os.path.join(output_dir, f"billing_summary_{timestamp}.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(self.generate_summary(), f, indent=2, ensure_ascii=False)
        saved_files.append(summary_file)
        
        logger.info(f"详细报告已保存到 {output_dir}，包含文件: {saved_files}")
        return saved_files


# =============================================================================
# 命令行接口和使用示例
# =============================================================================

def setup_sample_config():
    """设置示例配置文件"""
    config_manager = ConfigManager()
    
    # 示例配置（需要用户填入真实API密钥）
    sample_configs = {
        'deepseek': {
            'api_key': 'sk-your-deepseek-api-key',
            'base_url': 'https://api.deepseek.com',
            'enabled': 'false'  # 默认禁用，需要用户手动启用
        },
        'openai': {
            'api_key': 'sk-your-openai-api-key',
            'base_url': 'https://api.openai.com',
            'enabled': 'false'
        },
        'kimi': {
            'api_key': 'your-kimi-api-key',
            'base_url': 'https://api.moonshot.cn',
            'enabled': 'false'
        },
        'siliconflow': {
            'api_key': 'sk-your-siliconflow-api-key',
            'base_url': 'https://api.siliconflow.cn',
            'enabled': 'false'
        }
    }
    
    for platform, config in sample_configs.items():
        config_manager.set_platform_config(platform, **config)
    
    logger.info(f"示例配置文件已创建: {config_manager.config_file}")
    logger.info("请编辑配置文件填入真实API密钥并设置 enabled=true")
    
    return config_manager


def create_billing_manager_from_config(config_file: Optional[str] = None) -> BillingManager:
    """从配置文件创建BillingManager"""
    if config_file:
        config_manager = ConfigManager(config_file)
    else:
        config_manager = ConfigManager()
    
    billing_manager = BillingManager(config_manager)
    
    # 添加所有支持的平台
    for platform_type in PlatformType:
        try:
            billing_manager.add_platform(platform_type)
        except Exception as e:
            logger.debug(f"添加平台 {platform_type.value} 失败: {e}")
    
    return billing_manager


def main():
    """主函数 - 命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='AI平台账单查询工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s --init                    # 初始化配置文件
  %(prog)s --query                   # 查询所有平台账单
  %(prog)s --query --format json     # 以JSON格式输出
  %(prog)s --query --save report.csv # 保存为CSV文件
  %(prog)s --platform openai         # 只查询OpenAI平台
  %(prog)s --summary                 # 显示汇总信息
        """
    )
    
    parser.add_argument('--init', action='store_true', help='初始化配置文件')
    parser.add_argument('--config', type=str, help='指定配置文件路径')
    parser.add_argument('--query', action='store_true', help='查询账单信息')
    parser.add_argument('--platform', type=str, help='指定查询的平台')
    parser.add_argument('--format', choices=['json', 'table', 'csv', 'markdown', 'html'], 
                       default='table', help='输出格式')
    parser.add_argument('--save', type=str, help='保存结果到文件')
    parser.add_argument('--summary', action='store_true', help='显示汇总信息')
    parser.add_argument('--detailed-report', type=str, help='生成详细报告到指定目录')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细日志')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # 初始化配置
        if args.init:
            setup_sample_config()
            print("配置文件已创建，请编辑 ai_billing_config.ini 文件填入API密钥")
            return
        
        # 创建账单管理器
        billing_manager = create_billing_manager_from_config(args.config)
        
        if not billing_manager.platforms:
            print("警告: 没有配置任何平台，请先运行 --init 初始化配置")
            return
        
        # 查询单个平台
        if args.platform:
            if args.platform not in billing_manager.platforms:
                print(f"错误: 平台 '{args.platform}' 未配置或未启用")
                print(f"可用平台: {list(billing_manager.platforms.keys())}")
                return
            
            try:
                info = billing_manager.get_platform_billing_info(args.platform)
                if info is None:
                    print(f"错误: 无法获取平台 {args.platform} 的账单信息")
                    return
                
                output_format = OutputFormat(args.format)
                result = BillingFormatter.format({args.platform: info}, output_format)
                
                if args.save:
                    with open(args.save, 'w', encoding='utf-8') as f:
                        f.write(result)
                    print(f"结果已保存到: {args.save}")
                else:
                    print(result)
                    
            except Exception as e:
                print(f"查询平台 {args.platform} 失败: {e}")
                return
        
        # 查询所有平台
        elif args.query:
            reporter = BillingReporter(billing_manager)
            output_format = OutputFormat(args.format)
            
            result = reporter.generate_report(output_format, args.save)
            
            if not args.save:
                print(result)
        
        # 显示汇总信息
        elif args.summary:
            reporter = BillingReporter(billing_manager)
            summary = reporter.generate_summary()
            print(json.dumps(summary, indent=2, ensure_ascii=False))
        
        # 生成详细报告
        elif args.detailed_report:
            reporter = BillingReporter(billing_manager)
            saved_files = reporter.save_detailed_report(args.detailed_report)
            print(f"详细报告已生成，包含文件: {saved_files}")
        
        else:
            # 默认显示表格格式的简单结果
            reporter = BillingReporter(billing_manager)
            result = reporter.generate_report(OutputFormat.TABLE)
            print(result)
            print("\n提示: 使用 --help 查看更多选项")
    
    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        logger.error(f"程序运行错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()


# =============================================================================
# 使用示例函数
# =============================================================================

def example_basic_usage():
    """基本使用示例"""
    print("=== AI平台账单查询 - 基本使用示例 ===")
    
    # 1. 创建配置管理器
    config_manager = ConfigManager()
    
    # 2. 配置平台（示例 - 需要用真实API密钥替换）
    config_manager.set_platform_config('openai', 
                                      api_key='sk-your-openai-api-key',
                                      base_url='https://api.openai.com',
                                      enabled='true')
    
    # 3. 创建账单管理器
    billing_manager = BillingManager(config_manager)
    
    # 4. 添加平台
    billing_manager.add_platform(PlatformType.OPENAI)
    
    # 5. 查询账单信息
    try:
        billing_info = billing_manager.get_all_billing_info()
        
        # 6. 显示结果
        formatter = BillingFormatter()
        print(formatter.format(billing_info, OutputFormat.TABLE))
        
    except Exception as e:
        print(f"查询失败: {e}")


def example_multiple_platforms():
    """多平台使用示例"""
    print("=== AI平台账单查询 - 多平台示例 ===")
    
    # 1. 直接创建平台实例
    platforms = {
        'openai': OpenAIPlatform('sk-your-openai-api-key'),
        'deepseek': DeepSeekPlatform('sk-your-deepseek-api-key'),
        'kimi': KimiPlatform('your-kimi-api-key')
    }
    
    results = {}
    
    # 2. 逐个查询
    for name, platform in platforms.items():
        try:
            billing_info = platform.get_billing_info()
            results[name] = billing_info
            print(f"✓ {name}: 查询成功")
        except Exception as e:
            print(f"✗ {name}: 查询失败 - {e}")
    
    # 3. 生成报告
    if results:
        formatter = BillingFormatter()
        print("\n=== 账单汇总 ===\n")
        print(formatter.format(results, OutputFormat.TABLE))
        
        # 保存为多种格式
        for fmt, ext in [(OutputFormat.JSON, 'json'), (OutputFormat.CSV, 'csv')]:
            filename = f"billing_report.{ext}"
            content = formatter.format(results, fmt)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"报告已保存: {filename}")


def example_custom_platform():
    """自定义平台示例"""
    print("=== AI平台账单查询 - 自定义平台示例 ===")
    
    class MyCustomPlatform(BasePlatform):
        @property
        def platform_name(self) -> str:
            return "我的自定义平台"
        
        def get_billing_info(self) -> BillingInfo:
            # 自定义实现
            return BillingInfo(
                platform=self.platform_name,
                balance=100.0,
                used_amount=50.0,
                total_quota=150.0,
                free_quota=20.0,
                recharged_amount=130.0,
                gift_amount=20.0,
                currency="USD"
            )
    
    # 使用自定义平台
    platform = MyCustomPlatform(api_key="test")
    billing_info = platform.get_billing_info()
    
    formatter = BillingFormatter()
    result = formatter.format({platform.platform_name: billing_info}, OutputFormat.TABLE)
    print(result)


if __name__ == "__main__":
    # 如果直接运行脚本，启动命令行接口
    main()