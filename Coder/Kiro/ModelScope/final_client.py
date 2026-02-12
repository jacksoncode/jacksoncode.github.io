"""
最终工作版本的API客户端
"""
import requests
import json
import logging
from typing import Dict, List, Any
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class ModelScopeClient:
    """ModelScope客户端 - 使用示例数据"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('MODELSCOPE_API_KEY')
        logger.info("ModelScope客户端初始化")
    
    def get_models(self, page_size: int = 20) -> List[Dict[str, Any]]:
        """获取模型列表"""
        models = [
            {
                'id': 'damo/nlp_structbert_backbone_base_std',
                'name': 'StructBERT Base',
                'description': '结构化BERT模型，适用于自然语言理解任务',
                'type': 'nlp',
                'downloads': 15420,
                'tags': ['bert', 'nlp', 'chinese']
            },
            {
                'id': 'damo/cv_resnet50_image-classification_imagenet',
                'name': 'ResNet50 ImageNet',
                'description': 'ResNet50图像分类模型，在ImageNet数据集上预训练',
                'type': 'cv',
                'downloads': 8930,
                'tags': ['resnet', 'classification', 'imagenet']
            },
            {
                'id': 'damo/nlp_bert_document-classification_chinese',
                'name': 'BERT 中文文档分类',
                'description': 'BERT模型用于中文文档分类任务',
                'type': 'nlp',
                'downloads': 12350,
                'tags': ['bert', 'classification', 'chinese']
            },
            {
                'id': 'damo/cv_vitb16_classification_imagenet',
                'name': 'Vision Transformer Base',
                'description': 'Vision Transformer模型用于图像分类',
                'type': 'cv',
                'downloads': 6780,
                'tags': ['vit', 'transformer', 'classification']
            },
            {
                'id': 'damo/nlp_gpt3_text-generation_chinese',
                'name': 'GPT-3 中文文本生成',
                'description': 'GPT-3模型用于中文文本生成任务',
                'type': 'nlp',
                'downloads': 23450,
                'tags': ['gpt', 'generation', 'chinese']
            },
            {
                'id': 'damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
                'name': 'Paraformer 语音识别',
                'description': '达摩院语音识别模型，支持中文',
                'type': 'speech',
                'downloads': 9876,
                'tags': ['asr', 'speech', 'chinese']
            },
            {
                'id': 'damo/cv_ddpm_image-generation_celebahq',
                'name': 'DDPM 图像生成',
                'description': '扩散模型用于图像生成',
                'type': 'cv',
                'downloads': 5432,
                'tags': ['diffusion', 'generation', 'image']
            }
        ]
        return models[:page_size]
    
    def search_models(self, query: str, page_size: int = 20) -> List[Dict[str, Any]]:
        """搜索模型"""
        all_models = self.get_models(100)
        query_lower = query.lower()
        
        results = []
        for model in all_models:
            if (query_lower in model.get('name', '').lower() or 
                query_lower in model.get('id', '').lower() or
                query_lower in model.get('description', '').lower() or
                any(query_lower in tag.lower() for tag in model.get('tags', []))):
                results.append(model)
        
        return results[:page_size]
    
    def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """获取模型信息"""
        models = self.get_models(100)
        for model in models:
            if model['id'] == model_id:
                return model
        
        return {
            'id': model_id,
            'name': f'Model {model_id}',
            'description': f'模型 {model_id} 的详细信息',
            'type': 'unknown',
            'downloads': 0,
            'error': 'Model not found'
        }
    
    def get_account_info(self) -> Dict[str, Any]:
        """获取账户信息"""
        if not self.api_key:
            return {
                'error': 'no_api_key',
                'message': '需要API密钥才能获取账户信息'
            }
        
        return {
            'user_id': 'demo_user',
            'username': 'ModelScope用户',
            'message': 'ModelScope账户信息需要通过网页控制台查看',
            'suggestion': '请访问 https://www.modelscope.cn 登录查看账户详情'
        }
    
    def get_balance(self) -> Dict[str, Any]:
        """获取余额"""
        return {
            'balance': 'N/A',
            'currency': 'CNY',
            'message': 'ModelScope余额信息需要通过网页控制台查看',
            'suggestion': '请访问 https://www.modelscope.cn 查看账户余额'
        }
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """获取使用统计"""
        return {
            'current_month_usage': 'N/A',
            'total_requests': 'N/A',
            'message': 'ModelScope使用统计需要通过网页控制台查看',
            'suggestion': '请访问 https://www.modelscope.cn 查看详细使用情况'
        }


class DashScopeClient:
    """DashScope客户端"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('DASHSCOPE_API_KEY')
        self.base_url = "https://dashscope.aliyuncs.com/api/v1"
        
        if not self.api_key:
            raise ValueError("DashScope API密钥不能为空")
    
    def get_models(self) -> List[Dict[str, Any]]:
        """获取DashScope模型"""
        return [
            {
                'id': 'qwen-turbo',
                'name': '通义千问-Turbo',
                'type': 'text-generation',
                'description': '通义千问超大规模语言模型，支持中文英文等不同语言输入',
                'max_tokens': 8000,
                'pricing': '按token计费'
            },
            {
                'id': 'qwen-plus',
                'name': '通义千问-Plus',
                'type': 'text-generation',
                'description': '通义千问超大规模语言模型增强版，性能更强',
                'max_tokens': 32000,
                'pricing': '按token计费'
            },
            {
                'id': 'qwen-max',
                'name': '通义千问-Max',
                'type': 'text-generation',
                'description': '通义千问超大规模语言模型旗舰版，最强性能',
                'max_tokens': 8000,
                'pricing': '按token计费'
            },
            {
                'id': 'qwen-vl-plus',
                'name': '通义千问-VL-Plus',
                'type': 'multimodal',
                'description': '通义千问视觉理解模型，支持图文理解',
                'max_tokens': 8000,
                'pricing': '按token计费'
            },
            {
                'id': 'qwen-audio-turbo',
                'name': '通义千问-Audio-Turbo',
                'type': 'audio',
                'description': '通义千问音频理解模型',
                'max_tokens': 8000,
                'pricing': '按token计费'
            }
        ]
    
    def test_connection(self) -> Dict[str, Any]:
        """测试连接"""
        try:
            url = f"{self.base_url}/services/aigc/text-generation/generation"
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
                'X-DashScope-SSE': 'disable'
            }
            
            data = {
                'model': 'qwen-turbo',
                'input': {
                    'messages': [{'role': 'user', 'content': 'hello'}]
                },
                'parameters': {'max_tokens': 10}
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'status': 'success',
                    'message': '连接测试成功',
                    'response': result
                }
            else:
                return {
                    'status': 'error',
                    'message': f'HTTP {response.status_code}: {response.text}'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'连接测试失败: {str(e)}'
            }
    
    def get_usage_info(self) -> Dict[str, Any]:
        """获取使用信息"""
        return {
            'message': 'DashScope使用信息和费用需要通过阿里云控制台查看',
            'suggestion': '请访问阿里云DashScope控制台查看详细使用情况和账单'
        }
