#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据处理模块
处理基金数据，计算关键指标和生成监控汇总
"""

import logging
import configparser
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import json
import os


class DataProcessor:
    """数据处理器"""
    
    def __init__(self, config_file: str = "config/fund_config.ini"):
        """
        初始化数据处理器
        
        Args:
            config_file: 配置文件路径
        """
        self.config = configparser.ConfigParser()
        self.config.read(config_file, encoding='utf-8')
        
        # 配置日志
        self._setup_logging()
        
        # 历史数据存储路径
        self.history_data_path = "data/fund_history.json"
        
        # 确保数据目录存在
        os.makedirs(os.path.dirname(self.history_data_path), exist_ok=True)
        
        self.logger.info("数据处理器初始化完成")
    
    def _setup_logging(self):
        """设置日志配置"""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def calculate_indicators(self, fund_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        计算基金关键指标
        
        Args:
            fund_data: 原始基金数据
            
        Returns:
            处理后的基金数据
        """
        processed_data = fund_data.copy()
        
        try:
            # 基础数据验证和转换
            net_value = float(fund_data.get('net_value', 0))
            change_rate = float(fund_data.get('change_rate', 0))
            change_amount = float(fund_data.get('change_amount', 0))
            total_value = float(fund_data.get('total_value', 0))
            
            # 数据合理性检查
            if net_value <= 0:
                self.logger.warning(f"基金 {fund_data.get('fund_code')} 净值异常: {net_value}")
                net_value = 0
            
            # 计算扩展指标
            processed_data.update({
                'net_value': round(net_value, 4),
                'change_rate': round(change_rate, 2),
                'change_amount': round(change_amount, 4),
                'total_value': round(total_value, 4),
                'abs_change_rate': round(abs(change_rate), 2),  # 绝对涨跌幅
                'performance_level': self._get_performance_level(change_rate),  # 表现等级
                'trend_direction': self._get_trend_direction(change_rate),  # 趋势方向
                'process_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
            # 检查预警条件
            is_alert = self._check_alert_condition(fund_data, change_rate)
            processed_data['is_alert'] = is_alert
            
            if is_alert:
                processed_data['alert_reason'] = self._get_alert_reason(fund_data, change_rate)
            
        except (ValueError, TypeError) as e:
            self.logger.error(f"计算指标失败 - {fund_data.get('fund_code', 'Unknown')}: {str(e)}")
            # 设置默认值
            processed_data.update({
                'net_value': 0.0,
                'change_rate': 0.0,
                'change_amount': 0.0,
                'total_value': 0.0,
                'abs_change_rate': 0.0,
                'performance_level': 'unknown',
                'trend_direction': 'flat',
                'is_alert': False,
                'process_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return processed_data
    
    def _get_performance_level(self, change_rate: float) -> str:
        """获取表现等级"""
        if change_rate >= 5.0:
            return 'excellent'  # 优秀
        elif change_rate >= 2.0:
            return 'good'       # 良好
        elif change_rate >= -2.0:
            return 'average'    # 一般
        elif change_rate >= -5.0:
            return 'poor'       # 较差
        else:
            return 'terrible'   # 很差
    
    def _get_trend_direction(self, change_rate: float) -> str:
        """获取趋势方向"""
        if change_rate > 0.5:
            return 'up'         # 上涨
        elif change_rate < -0.5:
            return 'down'       # 下跌
        else:
            return 'flat'       # 平稳
    
    def _check_alert_condition(self, fund_data: Dict[str, Any], change_rate: float) -> bool:
        """检查预警条件"""
        fund_code = fund_data.get('fund_code', '')
        
        # 从配置文件获取预警阈值
        section_name = f"FUND_{fund_code}"
        if self.config.has_section(section_name):
            threshold = self.config.getfloat(section_name, 'alert_threshold', fallback=5.0)
        else:
            threshold = 5.0  # 默认阈值
        
        # 检查是否超过阈值
        return abs(change_rate) >= threshold
    
    def _get_alert_reason(self, fund_data: Dict[str, Any], change_rate: float) -> str:
        """获取预警原因"""
        fund_code = fund_data.get('fund_code', '')
        section_name = f"FUND_{fund_code}"
        
        if self.config.has_section(section_name):
            threshold = self.config.getfloat(section_name, 'alert_threshold', fallback=5.0)
        else:
            threshold = 5.0
        
        if change_rate >= threshold:
            return f"涨幅 {change_rate:.2f}% 超过预警阈值 {threshold:.1f}%"
        elif change_rate <= -threshold:
            return f"跌幅 {abs(change_rate):.2f}% 超过预警阈值 {threshold:.1f}%"
        else:
            return "未知预警原因"
    
    def process_multiple_funds(self, funds_data: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        批量处理多个基金数据
        
        Args:
            funds_data: 基金数据字典 {基金代码: 基金数据}
            
        Returns:
            处理后的基金数据列表
        """
        processed_funds = []
        
        self.logger.info(f"开始处理 {len(funds_data)} 个基金数据")
        
        for fund_code, fund_data in funds_data.items():
            try:
                processed_data = self.calculate_indicators(fund_data)
                processed_funds.append(processed_data)
                
                self.logger.debug(f"处理基金 {fund_code} 完成")
                
            except Exception as e:
                self.logger.error(f"处理基金 {fund_code} 失败: {str(e)}")
                continue
        
        # 按涨跌幅排序（降序）
        processed_funds.sort(key=lambda x: x.get('change_rate', 0), reverse=True)
        
        self.logger.info(f"基金数据处理完成，成功处理 {len(processed_funds)} 个基金")
        return processed_funds
    
    def generate_summary(self, processed_funds: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成监控汇总信息
        
        Args:
            processed_funds: 处理后的基金数据列表
            
        Returns:
            汇总信息字典
        """
        if not processed_funds:
            return {
                'total_funds': 0,
                'rise_count': 0,
                'fall_count': 0,
                'flat_count': 0,
                'alert_count': 0,
                'max_rise_fund': None,
                'max_fall_fund': None,
                'avg_change_rate': 0.0,
                'generate_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        
        # 统计数据
        total_funds = len(processed_funds)
        rise_count = sum(1 for fund in processed_funds if fund.get('change_rate', 0) > 0)
        fall_count = sum(1 for fund in processed_funds if fund.get('change_rate', 0) < 0)
        flat_count = total_funds - rise_count - fall_count
        alert_count = sum(1 for fund in processed_funds if fund.get('is_alert', False))
        
        # 找出最大涨幅和跌幅基金
        max_rise_fund = max(processed_funds, key=lambda x: x.get('change_rate', 0))
        max_fall_fund = min(processed_funds, key=lambda x: x.get('change_rate', 0))
        
        # 计算平均涨跌幅
        total_change_rate = sum(fund.get('change_rate', 0) for fund in processed_funds)
        avg_change_rate = round(total_change_rate / total_funds, 2) if total_funds > 0 else 0.0
        
        # 生成汇总信息
        summary = {
            'total_funds': total_funds,
            'rise_count': rise_count,
            'fall_count': fall_count,
            'flat_count': flat_count,
            'alert_count': alert_count,
            'max_rise_fund': {
                'code': max_rise_fund.get('fund_code', ''),
                'name': max_rise_fund.get('fund_name', ''),
                'change_rate': max_rise_fund.get('change_rate', 0)
            },
            'max_fall_fund': {
                'code': max_fall_fund.get('fund_code', ''),
                'name': max_fall_fund.get('fund_name', ''),
                'change_rate': max_fall_fund.get('change_rate', 0)
            },
            'avg_change_rate': avg_change_rate,
            'performance_distribution': self._get_performance_distribution(processed_funds),
            'alert_funds': [fund for fund in processed_funds if fund.get('is_alert', False)],
            'generate_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.logger.info(f"汇总信息生成完成: {total_funds}个基金, {rise_count}涨{fall_count}跌, {alert_count}个预警")
        return summary
    
    def _get_performance_distribution(self, processed_funds: List[Dict[str, Any]]) -> Dict[str, int]:
        """获取表现分布统计"""
        distribution = {
            'excellent': 0,
            'good': 0,
            'average': 0,
            'poor': 0,
            'terrible': 0,
            'unknown': 0
        }
        
        for fund in processed_funds:
            level = fund.get('performance_level', 'unknown')
            if level in distribution:
                distribution[level] += 1
        
        return distribution
    
    def save_history_data(self, processed_funds: List[Dict[str, Any]]) -> bool:
        """
        保存历史数据
        
        Args:
            processed_funds: 处理后的基金数据列表
            
        Returns:
            保存是否成功
        """
        try:
            # 加载现有历史数据
            history_data = self._load_history_data()
            
            # 添加今日数据
            today = datetime.now().strftime('%Y-%m-%d')
            history_data[today] = {
                'date': today,
                'funds': processed_funds,
                'summary': self.generate_summary(processed_funds),
                'save_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 清理过期数据（保留最近30天）
            cutoff_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            history_data = {date: data for date, data in history_data.items() if date >= cutoff_date}
            
            # 保存到文件
            with open(self.history_data_path, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"历史数据保存成功: {self.history_data_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"保存历史数据失败: {str(e)}")
            return False
    
    def _load_history_data(self) -> Dict[str, Any]:
        """加载历史数据"""
        try:
            if os.path.exists(self.history_data_path):
                with open(self.history_data_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.warning(f"加载历史数据失败: {str(e)}")
        
        return {}
    
    def get_historical_comparison(self, fund_code: str, days: int = 7) -> Optional[Dict[str, Any]]:
        """
        获取基金历史对比数据
        
        Args:
            fund_code: 基金代码
            days: 对比天数
            
        Returns:
            历史对比数据
        """
        history_data = self._load_history_data()
        
        if not history_data:
            return None
        
        # 获取最近几天的数据
        dates = sorted(history_data.keys(), reverse=True)[:days]
        
        historical_records = []
        for date in dates:
            day_data = history_data[date]
            funds = day_data.get('funds', [])
            
            # 查找指定基金
            fund_record = next((fund for fund in funds if fund.get('fund_code') == fund_code), None)
            if fund_record:
                historical_records.append({
                    'date': date,
                    'net_value': fund_record.get('net_value', 0),
                    'change_rate': fund_record.get('change_rate', 0)
                })
        
        if not historical_records:
            return None
        
        # 计算趋势
        return {
            'fund_code': fund_code,
            'records': historical_records,
            'trend_analysis': self._analyze_trend(historical_records)
        }
    
    def _analyze_trend(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析趋势"""
        if len(records) < 2:
            return {'trend': 'insufficient_data'}
        
        # 计算平均涨跌幅
        avg_change = sum(record['change_rate'] for record in records) / len(records)
        
        # 判断趋势
        recent_changes = [record['change_rate'] for record in records[:3]]
        recent_avg = sum(recent_changes) / len(recent_changes)
        
        if recent_avg > 1.0:
            trend = 'rising'
        elif recent_avg < -1.0:
            trend = 'falling'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'avg_change_rate': round(avg_change, 2),
            'recent_avg_change': round(recent_avg, 2),
            'volatility': round(self._calculate_volatility(records), 2)
        }
    
    def _calculate_volatility(self, records: List[Dict[str, Any]]) -> float:
        """计算波动率"""
        if len(records) < 2:
            return 0.0
        
        changes = [record['change_rate'] for record in records]
        mean_change = sum(changes) / len(changes)
        
        variance = sum((change - mean_change) ** 2 for change in changes) / len(changes)
        return variance ** 0.5


if __name__ == "__main__":
    # 测试代码
    processor = DataProcessor()
    
    # 测试数据
    test_funds_data = {
        '000001': {
            'fund_code': '000001',
            'fund_name': '华夏成长混合',
            'net_value': 1.2340,
            'change_rate': 2.15,
            'change_amount': 0.026,
            'total_value': 1.2366,
            'update_time': '2024-08-30 15:00:00'
        },
        '110022': {
            'fund_code': '110022',
            'fund_name': '易方达消费行业股票',
            'net_value': 2.1580,
            'change_rate': -1.23,
            'change_amount': -0.027,
            'total_value': 2.1553,
            'update_time': '2024-08-30 15:00:00'
        }
    }
    
    # 处理数据
    processed_funds = processor.process_multiple_funds(test_funds_data)
    print(f"处理了 {len(processed_funds)} 个基金数据")
    
    # 生成汇总
    summary = processor.generate_summary(processed_funds)
    print(f"汇总信息: {summary['total_funds']}个基金, {summary['rise_count']}涨{summary['fall_count']}跌")
    
    # 保存历史数据
    success = processor.save_history_data(processed_funds)
    print(f"历史数据保存{'成功' if success else '失败'}")