"""
模型管理器 - 修正版
"""
import json
from typing import Dict, List, Any
from datetime import datetime
from final_client import ModelScopeClient, DashScopeClient
import logging

logger = logging.getLogger(__name__)

class ModelManager:
    """模型管理器"""
    
    def __init__(self, modelscope_key: str = None, dashscope_key: str = None):
        self.modelscope_client = None
        self.dashscope_client = None
        
        # 初始化ModelScope客户端
        try:
            self.modelscope_client = ModelScopeClient(modelscope_key)
            logger.info("ModelScope客户端初始化成功")
        except Exception as e:
            logger.warning(f"ModelScope客户端初始化失败: {e}")
        
        # 初始化DashScope客户端
        if dashscope_key:
            try:
                self.dashscope_client = DashScopeClient(dashscope_key)
                logger.info("DashScope客户端初始化成功")
            except Exception as e:
                logger.warning(f"DashScope客户端初始化失败: {e}")
    
    def get_all_models(self) -> Dict[str, List[Dict[str, Any]]]:
        """获取所有平台的模型列表"""
        result = {
            'modelscope': [],
            'dashscope': []
        }
        
        if self.modelscope_client:
            try:
                result['modelscope'] = self.modelscope_client.get_models()
                logger.info(f"获取到 {len(result['modelscope'])} 个ModelScope模型")
            except Exception as e:
                logger.error(f"获取ModelScope模型失败: {e}")
        
        if self.dashscope_client:
            try:
                result['dashscope'] = self.dashscope_client.get_models()
                logger.info(f"获取到 {len(result['dashscope'])} 个DashScope模型")
            except Exception as e:
                logger.error(f"获取DashScope模型失败: {e}")
        
        return result
    
    def get_account_summary(self) -> Dict[str, Any]:
        """获取账户摘要信息"""
        summary = {
            'modelscope': {},
            'dashscope': {},
            'timestamp': datetime.now().isoformat()
        }
        
        if self.modelscope_client:
            try:
                account_info = self.modelscope_client.get_account_info()
                balance_info = self.modelscope_client.get_balance()
                usage_info = self.modelscope_client.get_usage_stats()
                
                summary['modelscope'] = {
                    'account': account_info,
                    'balance': balance_info,
                    'usage': usage_info
                }
                logger.info("获取ModelScope账户摘要成功")
            except Exception as e:
                logger.error(f"获取ModelScope账户信息失败: {e}")
                summary['modelscope']['error'] = str(e)
        
        if self.dashscope_client:
            try:
                usage_info = self.dashscope_client.get_usage_info()
                test_result = self.dashscope_client.test_connection()
                
                summary['dashscope'] = {
                    'usage': usage_info,
                    'connection_test': test_result
                }
                logger.info("获取DashScope账户摘要成功")
            except Exception as e:
                logger.error(f"获取DashScope使用信息失败: {e}")
                summary['dashscope']['error'] = str(e)
        
        return summary
    
    def search_models(self, keyword: str) -> Dict[str, List[Dict[str, Any]]]:
        """搜索模型"""
        result = {
            'modelscope': [],
            'dashscope': []
        }
        
        # 搜索ModelScope模型
        if self.modelscope_client:
            try:
                result['modelscope'] = self.modelscope_client.search_models(keyword)
                logger.info(f"ModelScope搜索'{keyword}'结果: {len(result['modelscope'])} 个")
            except Exception as e:
                logger.error(f"ModelScope搜索失败: {e}")
        
        # 搜索DashScope模型
        if self.dashscope_client:
            try:
                all_ds_models = self.dashscope_client.get_models()
                keyword_lower = keyword.lower()
                result['dashscope'] = [
                    model for model in all_ds_models
                    if keyword_lower in model.get('name', '').lower() or
                       keyword_lower in model.get('id', '').lower()
                ]
                logger.info(f"DashScope搜索'{keyword}'结果: {len(result['dashscope'])} 个")
            except Exception as e:
                logger.error(f"DashScope搜索失败: {e}")
        
        return result
    
    def get_model_details(self, model_id: str, platform: str = 'modelscope') -> Dict[str, Any]:
        """获取模型详细信息"""
        if platform == 'modelscope' and self.modelscope_client:
            try:
                return self.modelscope_client.get_model_info(model_id)
            except Exception as e:
                logger.error(f"获取ModelScope模型详情失败: {e}")
                return {'error': str(e)}
        elif platform == 'dashscope' and self.dashscope_client:
            try:
                models = self.dashscope_client.get_models()
                for model in models:
                    if model['id'] == model_id:
                        return model
                return {'error': f'未找到模型: {model_id}'}
            except Exception as e:
                logger.error(f"获取DashScope模型详情失败: {e}")
                return {'error': str(e)}
        else:
            return {'error': f'不支持的平台: {platform}'}
    
    def export_models_to_json(self, filename: str = None) -> str:
        """导出模型列表到JSON文件"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'models_export_{timestamp}.json'
        
        models_data = {
            'export_time': datetime.now().isoformat(),
            'models': self.get_all_models(),
            'account_summary': self.get_account_summary()
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(models_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"模型数据已导出到: {filename}")
            return filename
        except Exception as e:
            logger.error(f"导出失败: {e}")
            raise
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        all_models = self.get_all_models()
        
        # ModelScope统计
        ms_models = all_models.get('modelscope', [])
        ms_stats = {
            'total_models': len(ms_models),
            'total_downloads': sum(model.get('downloads', 0) for model in ms_models),
            'model_types': {}
        }
        
        for model in ms_models:
            model_type = model.get('type', 'unknown')
            ms_stats['model_types'][model_type] = ms_stats['model_types'].get(model_type, 0) + 1
        
        # DashScope统计
        ds_models = all_models.get('dashscope', [])
        ds_stats = {
            'total_models': len(ds_models),
            'model_types': {}
        }
        
        for model in ds_models:
            model_type = model.get('type', 'unknown')
            ds_stats['model_types'][model_type] = ds_stats['model_types'].get(model_type, 0) + 1
        
        return {
            'modelscope': ms_stats,
            'dashscope': ds_stats,
            'total_models': ms_stats['total_models'] + ds_stats['total_models']
        }
