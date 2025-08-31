#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金数据爬取模块
支持多数据源获取基金信息，包含智能字段映射和异常处理机制
"""

import requests
import json
import re
import logging
import time
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import configparser
from urllib.parse import quote


class FundCrawler:
    """基金数据爬取器"""
    
    def __init__(self, config_file: str = "config/fund_config.ini"):
        """
        初始化基金爬取器
        
        Args:
            config_file: 配置文件路径
        """
        self.config = configparser.ConfigParser()
        self.config.read(config_file, encoding='utf-8')
        
        # 配置日志
        self._setup_logging()
        
        # 数据源配置
        self.data_sources = self._load_data_sources()
        
        # 请求配置
        self.timeout = self.config.getint('SCHEDULE', 'timeout', fallback=10)
        self.retry_times = self.config.getint('SCHEDULE', 'retry_times', fallback=3)
        
        # 请求会话
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        self.logger.info("基金爬取器初始化完成")
    
    def _setup_logging(self):
        """设置日志配置"""
        log_level = self.config.get('LOGGING', 'log_level', fallback='INFO')
        
        # 创建logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(getattr(logging, log_level))
        
        # 创建handler
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def _load_data_sources(self) -> Dict[str, str]:
        """加载数据源配置"""
        sources = {}
        
        if self.config.has_section('DATA_SOURCES'):
            sources['tiantianjijin'] = self.config.get('DATA_SOURCES', 'tiantianjijin_url', 
                                                      fallback='https://fundgz.1234567.com.cn/js/{code}.js')
            sources['sina'] = self.config.get('DATA_SOURCES', 'sina_url', 
                                              fallback='https://hq.sinajs.cn/list=f_{code}')
            sources['eastmoney'] = self.config.get('DATA_SOURCES', 'eastmoney_url', 
                                                   fallback='https://push2.eastmoney.com/api/qt/ulist.np/get')
        
        return sources
    
    def get_fund_data(self, fund_code: str) -> Optional[Dict[str, Any]]:
        """
        获取基金数据，支持多源切换
        
        Args:
            fund_code: 基金代码
            
        Returns:
            基金数据字典或None
        """
        self.logger.info(f"开始获取基金 {fund_code} 数据")
        
        # 按优先级尝试数据源
        primary_source = self.config.get('DATA_SOURCES', 'primary_source', fallback='tiantianjijin')
        backup_sources = self.config.get('DATA_SOURCES', 'backup_sources', fallback='sina,eastmoney').split(',')
        
        # 首先尝试主要数据源
        fund_data = self._try_get_fund_data(fund_code, primary_source.strip())
        if fund_data and self._is_valid_response(fund_data):
            return fund_data
        
        # 尝试备用数据源
        for source in backup_sources:
            source = source.strip()
            if source == primary_source:
                continue
                
            self.logger.warning(f"主数据源失败，尝试备用数据源: {source}")
            fund_data = self._try_get_fund_data(fund_code, source)
            if fund_data and self._is_valid_response(fund_data):
                return fund_data
        
        self.logger.error(f"所有数据源都无法获取基金 {fund_code} 的数据")
        return None
    
    def _try_get_fund_data(self, fund_code: str, source: str) -> Optional[Dict[str, Any]]:
        """
        尝试从指定数据源获取基金数据
        
        Args:
            fund_code: 基金代码
            source: 数据源名称
            
        Returns:
            基金数据字典或None
        """
        for attempt in range(self.retry_times):
            try:
                if source == 'tiantianjijin':
                    return self._get_from_tiantianjijin(fund_code)
                elif source == 'sina':
                    return self._get_from_sina(fund_code)
                elif source == 'eastmoney':
                    return self._get_from_eastmoney(fund_code)
                else:
                    self.logger.error(f"未知数据源: {source}")
                    return None
                    
            except Exception as e:
                self.logger.warning(f"第 {attempt + 1} 次尝试失败 - {source}: {str(e)}")
                if attempt < self.retry_times - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                continue
        
        return None
    
    def _get_from_tiantianjijin(self, fund_code: str) -> Optional[Dict[str, Any]]:
        """从天天基金网获取数据"""
        url = self.data_sources['tiantianjijin'].format(code=fund_code)
        
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        
        # 解析JSONP响应
        content = response.text
        if not content:
            return None
            
        # 提取JSON部分
        json_match = re.search(r'jsonpgz\((.*)\)', content)
        if not json_match:
            return None
            
        data = json.loads(json_match.group(1))
        
        # 解析基金信息
        return self._parse_tiantianjijin_data(data, fund_code)
    
    def _get_from_sina(self, fund_code: str) -> Optional[Dict[str, Any]]:
        """从新浪财经获取数据"""
        url = self.data_sources['sina'].format(code=fund_code)
        
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        
        content = response.text
        if not content or 'FAILED' in content:
            return None
            
        # 解析新浪数据格式
        return self._parse_sina_data(content, fund_code)
    
    def _get_from_eastmoney(self, fund_code: str) -> Optional[Dict[str, Any]]:
        """从东方财富获取数据"""
        # 东方财富API需要特殊参数
        params = {
            'fields': 'f12,f13,f14,f3,f4,f5,f6',
            'fid': 'f3',
            'secids': f'0.{fund_code}'
        }
        
        response = self.session.get(self.data_sources['eastmoney'], 
                                  params=params, timeout=self.timeout)
        response.raise_for_status()
        
        data = response.json()
        return self._parse_eastmoney_data(data, fund_code)
    
    def _parse_tiantianjijin_data(self, data: Dict[str, Any], fund_code: str) -> Dict[str, Any]:
        """解析天天基金网数据"""
        try:
            return {
                'fund_code': fund_code,
                'fund_name': data.get('name', ''),
                'net_value': float(data.get('dwjz', 0)),  # 当日净值
                'change_rate': float(data.get('gszzl', 0)),  # 涨跌幅
                'change_amount': float(data.get('gsz', 0)) - float(data.get('dwjz', 0)),  # 涨跌额
                'total_value': float(data.get('ljjz', 0)),  # 累计净值
                'update_time': data.get('gztime', ''),  # 更新时间
                'data_source': 'tiantianjijin',
                'raw_data': data
            }
        except (ValueError, TypeError) as e:
            self.logger.error(f"解析天天基金数据失败: {str(e)}")
            return {}
    
    def _parse_sina_data(self, content: str, fund_code: str) -> Dict[str, Any]:
        """解析新浪财经数据"""
        try:
            # 新浪数据格式: var hq_str_f_基金代码="数据1,数据2,..."
            pattern = r'var hq_str_f_' + fund_code + r'="([^"]*)"'
            match = re.search(pattern, content)
            
            if not match:
                return {}
                
            data_str = match.group(1)
            data_parts = data_str.split(',')
            
            if len(data_parts) < 10:
                return {}
            
            return {
                'fund_code': fund_code,
                'fund_name': data_parts[0],
                'net_value': float(data_parts[1]) if data_parts[1] else 0,
                'change_rate': float(data_parts[3]) if data_parts[3] else 0,
                'change_amount': float(data_parts[2]) if data_parts[2] else 0,
                'total_value': float(data_parts[4]) if data_parts[4] else 0,
                'update_time': data_parts[6] if len(data_parts) > 6 else '',
                'data_source': 'sina',
                'raw_data': data_parts
            }
        except (ValueError, IndexError) as e:
            self.logger.error(f"解析新浪数据失败: {str(e)}")
            return {}
    
    def _parse_eastmoney_data(self, data: Dict[str, Any], fund_code: str) -> Dict[str, Any]:
        """解析东方财富数据"""
        try:
            if not data.get('data') or not data['data'].get('diff'):
                return {}
                
            fund_info = data['data']['diff'][0] if data['data']['diff'] else {}
            
            return {
                'fund_code': fund_code,
                'fund_name': fund_info.get('f14', ''),
                'net_value': float(fund_info.get('f2', 0)) / 100,  # 东财数据需要除以100
                'change_rate': float(fund_info.get('f3', 0)) / 100,
                'change_amount': float(fund_info.get('f4', 0)) / 100,
                'total_value': float(fund_info.get('f5', 0)) / 100,
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data_source': 'eastmoney',
                'raw_data': fund_info
            }
        except (ValueError, KeyError, IndexError) as e:
            self.logger.error(f"解析东方财富数据失败: {str(e)}")
            return {}
    
    def _is_valid_response(self, data: Dict[str, Any]) -> bool:
        """检查响应数据有效性"""
        if not data:
            return False
            
        # 检查必要字段
        required_fields = ['fund_code', 'fund_name', 'net_value']
        for field in required_fields:
            if field not in data or not data[field]:
                return False
        
        # 检查数值有效性
        try:
            net_value = float(data.get('net_value', 0))
            if net_value <= 0:
                return False
        except (ValueError, TypeError):
            return False
            
        return True
    
    def _has_complete_info(self, data: Dict[str, Any]) -> bool:
        """确保基金数据完整性"""
        if not self._is_valid_response(data):
            return False
            
        # 检查扩展字段
        extended_fields = ['change_rate', 'change_amount', 'update_time']
        complete_count = sum(1 for field in extended_fields if data.get(field))
        
        # 至少要有2个扩展字段有值
        return complete_count >= 2
    
    def get_multiple_funds_data(self, fund_codes: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        批量获取多个基金数据
        
        Args:
            fund_codes: 基金代码列表
            
        Returns:
            基金数据字典 {基金代码: 基金数据}
        """
        results = {}
        
        self.logger.info(f"开始批量获取 {len(fund_codes)} 个基金数据")
        
        for fund_code in fund_codes:
            try:
                fund_data = self.get_fund_data(fund_code)
                if fund_data:
                    results[fund_code] = fund_data
                    self.logger.info(f"成功获取基金 {fund_code} 数据")
                else:
                    self.logger.warning(f"获取基金 {fund_code} 数据失败")
                    
                # 添加请求间隔，避免被限制
                time.sleep(0.5)
                
            except Exception as e:
                self.logger.error(f"获取基金 {fund_code} 数据异常: {str(e)}")
                continue
        
        self.logger.info(f"批量获取完成，成功 {len(results)}/{len(fund_codes)} 个基金")
        return results
    
    def get_fund_info_from_config(self) -> Dict[str, Dict[str, Any]]:
        """
        从配置文件获取基金信息
        
        Returns:
            基金信息字典
        """
        fund_codes_str = self.config.get('MONITOR_FUNDS', 'fund_codes', fallback='')
        fund_codes = [code.strip() for code in fund_codes_str.split(',') if code.strip()]
        
        if not fund_codes:
            self.logger.warning("配置文件中未找到基金代码")
            return {}
        
        return self.get_multiple_funds_data(fund_codes)
    
    def close(self):
        """关闭会话"""
        if hasattr(self, 'session'):
            self.session.close()
            self.logger.info("基金爬取器会话已关闭")


if __name__ == "__main__":
    # 测试代码
    crawler = FundCrawler()
    
    # 测试单个基金
    test_fund = "000001"
    result = crawler.get_fund_data(test_fund)
    if result:
        print(f"基金 {test_fund} 数据:")
        for key, value in result.items():
            if key != 'raw_data':
                print(f"  {key}: {value}")
    
    # 测试配置文件获取
    all_funds = crawler.get_fund_info_from_config()
    print(f"\n配置文件中的基金数量: {len(all_funds)}")
    
    crawler.close()