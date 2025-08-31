#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据处理模块测试
"""

import unittest
import sys
import os
import json
import tempfile
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# 添加源码路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_processor import DataProcessor


class TestDataProcessor(unittest.TestCase):
    """数据处理器测试类"""
    
    def setUp(self):
        """测试前置设置"""
        # 使用临时目录进行测试
        self.temp_dir = tempfile.mkdtemp()
        
        # 创建测试配置
        with patch('configparser.ConfigParser') as mock_config_class:
            mock_config = MagicMock()
            mock_config_class.return_value = mock_config
            
            # 设置Mock配置
            mock_config.get.side_effect = self._mock_config_get
            mock_config.getfloat.side_effect = self._mock_config_getfloat
            mock_config.has_section.return_value = True
            
            self.processor = DataProcessor()
            # 重定向历史数据路径到临时目录
            self.processor.history_data_path = os.path.join(self.temp_dir, 'test_history.json')
    
    def tearDown(self):
        """测试后置清理"""
        # 清理临时文件
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def _mock_config_get(self, section, option, fallback=None):
        """Mock配置get方法"""
        return fallback
    
    def _mock_config_getfloat(self, section, option, fallback=None):
        """Mock配置getfloat方法"""
        # 为不同基金返回不同的预警阈值
        if section == 'FUND_000001':
            return 3.0
        elif section == 'FUND_110022':
            return 5.0
        return fallback if fallback is not None else 5.0
    
    def test_processor_initialization(self):
        """测试处理器初始化"""
        self.assertIsNotNone(self.processor)
        self.assertIsNotNone(self.processor.config)
        self.assertIsNotNone(self.processor.logger)
    
    def test_calculate_indicators_basic(self):
        """测试基础指标计算"""
        # 测试数据
        fund_data = {
            'fund_code': '000001',
            'fund_name': '华夏成长混合',
            'net_value': 1.2340,
            'change_rate': 2.15,
            'change_amount': 0.026,
            'total_value': 1.2366,
            'update_time': '2024-08-30 15:00:00'
        }
        
        result = self.processor.calculate_indicators(fund_data)
        
        # 检查基础字段保持不变
        self.assertEqual(result['fund_code'], '000001')
        self.assertEqual(result['fund_name'], '华夏成长混合')
        
        # 检查数值处理
        self.assertEqual(result['net_value'], 1.2340)
        self.assertEqual(result['change_rate'], 2.15)
        self.assertEqual(result['change_amount'], 0.026)
        self.assertEqual(result['total_value'], 1.2366)
        
        # 检查新增字段
        self.assertIn('abs_change_rate', result)
        self.assertIn('performance_level', result)
        self.assertIn('trend_direction', result)
        self.assertIn('is_alert', result)
        self.assertIn('process_time', result)
        
        # 检查计算结果
        self.assertEqual(result['abs_change_rate'], 2.15)
        self.assertEqual(result['performance_level'], 'good')  # 2.15% 应该是 good
        self.assertEqual(result['trend_direction'], 'up')      # 正值应该是 up
    
    def test_calculate_indicators_invalid_data(self):
        """测试无效数据处理"""
        # 测试无效数据
        invalid_data = {
            'fund_code': '999999',
            'fund_name': '无效基金',
            'net_value': 'invalid',
            'change_rate': None,
            'change_amount': 'abc'
        }
        
        result = self.processor.calculate_indicators(invalid_data)
        
        # 应该有默认值
        self.assertEqual(result['net_value'], 0.0)
        self.assertEqual(result['change_rate'], 0.0)
        self.assertEqual(result['change_amount'], 0.0)
        self.assertEqual(result['performance_level'], 'unknown')
        self.assertEqual(result['trend_direction'], 'flat')
        self.assertFalse(result['is_alert'])
    
    def test_performance_level_calculation(self):
        """测试表现等级计算"""
        test_cases = [
            (6.0, 'excellent'),   # >= 5.0
            (3.5, 'good'),        # >= 2.0
            (1.0, 'average'),     # >= -2.0
            (-3.0, 'poor'),       # >= -5.0
            (-6.0, 'terrible'),   # < -5.0
        ]
        
        for change_rate, expected_level in test_cases:
            level = self.processor._get_performance_level(change_rate)
            self.assertEqual(level, expected_level, 
                           f"涨跌幅 {change_rate}% 应该是 {expected_level}，实际是 {level}")
    
    def test_trend_direction_calculation(self):
        """测试趋势方向计算"""
        test_cases = [
            (2.0, 'up'),      # > 0.5
            (0.3, 'flat'),    # -0.5 <= x <= 0.5
            (-0.3, 'flat'),   # -0.5 <= x <= 0.5
            (-2.0, 'down'),   # < -0.5
        ]
        
        for change_rate, expected_direction in test_cases:
            direction = self.processor._get_trend_direction(change_rate)
            self.assertEqual(direction, expected_direction,
                           f"涨跌幅 {change_rate}% 应该是 {expected_direction}，实际是 {direction}")
    
    def test_alert_condition_checking(self):
        """测试预警条件检查"""
        # 测试超过阈值的情况
        fund_data_alert = {
            'fund_code': '000001',  # 阈值 3.0%
            'fund_name': '华夏成长混合'
        }
        
        # 超过阈值
        self.assertTrue(self.processor._check_alert_condition(fund_data_alert, 3.5))
        self.assertTrue(self.processor._check_alert_condition(fund_data_alert, -3.5))
        
        # 未超过阈值
        self.assertFalse(self.processor._check_alert_condition(fund_data_alert, 2.5))
        self.assertFalse(self.processor._check_alert_condition(fund_data_alert, -2.5))
    
    def test_alert_reason_generation(self):
        """测试预警原因生成"""
        fund_data = {
            'fund_code': '000001',  # 阈值 3.0%
            'fund_name': '华夏成长混合'
        }
        
        # 上涨预警
        reason_up = self.processor._get_alert_reason(fund_data, 3.5)
        self.assertIn('涨幅', reason_up)
        self.assertIn('3.50%', reason_up)
        self.assertIn('3.0%', reason_up)
        
        # 下跌预警
        reason_down = self.processor._get_alert_reason(fund_data, -3.5)
        self.assertIn('跌幅', reason_down)
        self.assertIn('3.50%', reason_down)
        self.assertIn('3.0%', reason_down)
    
    def test_multiple_funds_processing(self):
        """测试批量基金数据处理"""
        funds_data = {
            '000001': {
                'fund_code': '000001',
                'fund_name': '华夏成长混合',
                'net_value': 1.2340,
                'change_rate': 2.15,
                'change_amount': 0.026
            },
            '110022': {
                'fund_code': '110022',
                'fund_name': '易方达消费行业',
                'net_value': 2.1580,
                'change_rate': -1.23,
                'change_amount': -0.027
            }
        }
        
        processed_funds = self.processor.process_multiple_funds(funds_data)
        
        # 检查处理结果
        self.assertEqual(len(processed_funds), 2)
        
        # 检查排序（应该按涨跌幅降序）
        self.assertEqual(processed_funds[0]['fund_code'], '000001')  # 2.15% 排在前面
        self.assertEqual(processed_funds[1]['fund_code'], '110022')  # -1.23% 排在后面
        
        # 检查每个基金都被正确处理
        for fund in processed_funds:
            self.assertIn('performance_level', fund)
            self.assertIn('trend_direction', fund)
            self.assertIn('is_alert', fund)
    
    def test_summary_generation(self):
        """测试汇总信息生成"""
        processed_funds = [
            {
                'fund_code': '000001',
                'fund_name': '华夏成长混合',
                'change_rate': 2.15,
                'performance_level': 'good',
                'is_alert': False
            },
            {
                'fund_code': '110022',
                'fund_name': '易方达消费行业',
                'change_rate': -1.23,
                'performance_level': 'average',
                'is_alert': False
            },
            {
                'fund_code': '161725',
                'fund_name': '招商中证白酒指数',
                'change_rate': 4.20,
                'performance_level': 'good',
                'is_alert': True
            }
        ]
        
        summary = self.processor.generate_summary(processed_funds)
        
        # 检查统计数据
        self.assertEqual(summary['total_funds'], 3)
        self.assertEqual(summary['rise_count'], 2)  # 2.15%, 4.20%
        self.assertEqual(summary['fall_count'], 1)  # -1.23%
        self.assertEqual(summary['flat_count'], 0)
        self.assertEqual(summary['alert_count'], 1)
        
        # 检查最大涨跌幅基金
        self.assertEqual(summary['max_rise_fund']['code'], '161725')  # 4.20%
        self.assertEqual(summary['max_fall_fund']['code'], '110022')  # -1.23%
        
        # 检查平均涨跌幅
        expected_avg = (2.15 - 1.23 + 4.20) / 3
        self.assertAlmostEqual(summary['avg_change_rate'], expected_avg, places=2)
        
        # 检查表现分布
        distribution = summary['performance_distribution']
        self.assertEqual(distribution['good'], 2)
        self.assertEqual(distribution['average'], 1)
        
        # 检查预警基金列表
        alert_funds = summary['alert_funds']
        self.assertEqual(len(alert_funds), 1)
        self.assertEqual(alert_funds[0]['fund_code'], '161725')
    
    def test_empty_summary_generation(self):
        """测试空数据汇总生成"""
        summary = self.processor.generate_summary([])
        
        self.assertEqual(summary['total_funds'], 0)
        self.assertEqual(summary['rise_count'], 0)
        self.assertEqual(summary['fall_count'], 0)
        self.assertEqual(summary['alert_count'], 0)
        self.assertIsNone(summary['max_rise_fund'])
        self.assertIsNone(summary['max_fall_fund'])
        self.assertEqual(summary['avg_change_rate'], 0.0)
    
    def test_performance_distribution(self):
        """测试表现分布统计"""
        processed_funds = [
            {'performance_level': 'excellent'},
            {'performance_level': 'good'},
            {'performance_level': 'good'},
            {'performance_level': 'average'},
            {'performance_level': 'poor'},
            {'performance_level': 'terrible'},
            {'performance_level': 'unknown'}
        ]
        
        distribution = self.processor._get_performance_distribution(processed_funds)
        
        self.assertEqual(distribution['excellent'], 1)
        self.assertEqual(distribution['good'], 2)
        self.assertEqual(distribution['average'], 1)
        self.assertEqual(distribution['poor'], 1)
        self.assertEqual(distribution['terrible'], 1)
        self.assertEqual(distribution['unknown'], 1)
    
    def test_history_data_saving(self):
        """测试历史数据保存"""
        processed_funds = [
            {
                'fund_code': '000001',
                'fund_name': '华夏成长混合',
                'change_rate': 2.15,
                'is_alert': False
            }
        ]
        
        # 保存历史数据
        success = self.processor.save_history_data(processed_funds)
        self.assertTrue(success)
        
        # 检查文件是否创建
        self.assertTrue(os.path.exists(self.processor.history_data_path))
        
        # 检查文件内容
        with open(self.processor.history_data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        today = datetime.now().strftime('%Y-%m-%d')
        self.assertIn(today, data)
        self.assertIn('funds', data[today])
        self.assertIn('summary', data[today])
        self.assertEqual(len(data[today]['funds']), 1)
    
    def test_history_data_loading(self):
        """测试历史数据加载"""
        # 创建测试历史数据
        test_data = {
            '2024-08-30': {
                'date': '2024-08-30',
                'funds': [
                    {
                        'fund_code': '000001',
                        'fund_name': '华夏成长混合',
                        'net_value': 1.2340,
                        'change_rate': 2.15
                    }
                ]
            }
        }
        
        # 保存测试数据
        with open(self.processor.history_data_path, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        # 加载数据
        loaded_data = self.processor._load_history_data()
        
        self.assertEqual(loaded_data, test_data)
        self.assertIn('2024-08-30', loaded_data)
    
    def test_historical_comparison(self):
        """测试历史对比"""
        # 创建多天历史数据
        history_data = {
            '2024-08-28': {
                'funds': [
                    {'fund_code': '000001', 'net_value': 1.2000, 'change_rate': 1.0}
                ]
            },
            '2024-08-29': {
                'funds': [
                    {'fund_code': '000001', 'net_value': 1.2200, 'change_rate': 1.67}
                ]
            },
            '2024-08-30': {
                'funds': [
                    {'fund_code': '000001', 'net_value': 1.2340, 'change_rate': 1.15}
                ]
            }
        }
        
        # 保存历史数据
        with open(self.processor.history_data_path, 'w', encoding='utf-8') as f:
            json.dump(history_data, f)
        
        # 获取历史对比
        comparison = self.processor.get_historical_comparison('000001', days=3)
        
        self.assertIsNotNone(comparison)
        self.assertEqual(comparison['fund_code'], '000001')
        self.assertEqual(len(comparison['records']), 3)
        
        # 检查趋势分析
        trend_analysis = comparison['trend_analysis']
        self.assertIn('trend', trend_analysis)
        self.assertIn('avg_change_rate', trend_analysis)
        self.assertIn('volatility', trend_analysis)
    
    def test_trend_analysis(self):
        """测试趋势分析"""
        # 上升趋势数据
        rising_records = [
            {'change_rate': 2.0},
            {'change_rate': 2.5},
            {'change_rate': 1.8}
        ]
        
        trend = self.processor._analyze_trend(rising_records)
        self.assertEqual(trend['trend'], 'rising')
        
        # 下降趋势数据
        falling_records = [
            {'change_rate': -2.0},
            {'change_rate': -1.5},
            {'change_rate': -2.5}
        ]
        
        trend = self.processor._analyze_trend(falling_records)
        self.assertEqual(trend['trend'], 'falling')
        
        # 稳定趋势数据
        stable_records = [
            {'change_rate': 0.5},
            {'change_rate': -0.3},
            {'change_rate': 0.2}
        ]
        
        trend = self.processor._analyze_trend(stable_records)
        self.assertEqual(trend['trend'], 'stable')
    
    def test_volatility_calculation(self):
        """测试波动率计算"""
        # 低波动率数据
        low_volatility_records = [
            {'change_rate': 1.0},
            {'change_rate': 1.1},
            {'change_rate': 0.9}
        ]
        
        volatility = self.processor._calculate_volatility(low_volatility_records)
        self.assertLess(volatility, 1.0)  # 应该是低波动率
        
        # 高波动率数据
        high_volatility_records = [
            {'change_rate': 5.0},
            {'change_rate': -3.0},
            {'change_rate': 4.0}
        ]
        
        volatility = self.processor._calculate_volatility(high_volatility_records)
        self.assertGreater(volatility, 2.0)  # 应该是高波动率


def run_processor_tests():
    """运行所有数据处理模块测试"""
    print("=" * 60)
    print("开始数据处理模块测试")
    print("=" * 60)
    
    # 创建测试套件
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestDataProcessor))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("数据处理模块测试结果")
    print("=" * 60)
    print(f"运行测试数: {result.testsRun}")
    print(f"失败数: {len(result.failures)}")
    print(f"错误数: {len(result.errors)}")
    print(f"跳过数: {len(result.skipped)}")
    
    if result.failures:
        print("\n失败的测试:")
        for test, error in result.failures:
            print(f"  - {test}: {error}")
    
    if result.errors:
        print("\n错误的测试:")
        for test, error in result.errors:
            print(f"  - {test}: {error}")
    
    # 返回测试是否成功
    return len(result.failures) == 0 and len(result.errors) == 0


if __name__ == '__main__':
    success = run_processor_tests()
    exit(0 if success else 1)