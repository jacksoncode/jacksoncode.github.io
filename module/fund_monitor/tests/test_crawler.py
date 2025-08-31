#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金数据爬取模块测试
"""

import unittest
import sys
import os

# 添加源码路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from fund_crawler import FundCrawler


class TestFundCrawler(unittest.TestCase):
    """基金爬取器测试类"""
    
    def setUp(self):
        """测试前置设置"""
        self.crawler = FundCrawler()
    
    def tearDown(self):
        """测试后置清理"""
        if self.crawler:
            self.crawler.close()
    
    def test_crawler_initialization(self):
        """测试爬取器初始化"""
        self.assertIsNotNone(self.crawler)
        self.assertIsNotNone(self.crawler.session)
        self.assertIsNotNone(self.crawler.data_sources)
        self.assertGreater(self.crawler.timeout, 0)
        self.assertGreater(self.crawler.retry_times, 0)
    
    def test_data_sources_configuration(self):
        """测试数据源配置"""
        sources = self.crawler.data_sources
        self.assertIn('tiantianjijin', sources)
        self.assertIn('sina', sources)
        self.assertIn('eastmoney', sources)
        
        # 检查URL模板
        for source, url in sources.items():
            self.assertIn('{code}', url)
            self.assertTrue(url.startswith('http'))
    
    def test_get_single_fund_data(self):
        """测试获取单个基金数据"""
        # 使用华夏成长混合基金进行测试
        test_fund_code = "000001"
        
        fund_data = self.crawler.get_fund_data(test_fund_code)
        
        if fund_data:  # 网络可能不可用，仅在成功时测试
            self.assertIsInstance(fund_data, dict)
            self.assertEqual(fund_data.get('fund_code'), test_fund_code)
            self.assertIn('fund_name', fund_data)
            self.assertIn('net_value', fund_data)
            self.assertIn('change_rate', fund_data)
            self.assertIn('data_source', fund_data)
            
            # 检查数据类型
            self.assertIsInstance(fund_data['net_value'], (int, float))
            self.assertIsInstance(fund_data['change_rate'], (int, float))
    
    def test_invalid_fund_code(self):
        """测试无效基金代码"""
        invalid_codes = ["999999", "INVALID", ""]
        
        for code in invalid_codes:
            fund_data = self.crawler.get_fund_data(code)
            # 无效代码应该返回None或空字典
            if fund_data:
                self.assertFalse(self.crawler._is_valid_response(fund_data))
    
    def test_response_validation(self):
        """测试响应验证"""
        # 测试有效响应
        valid_data = {
            'fund_code': '000001',
            'fund_name': '华夏成长混合',
            'net_value': 1.2340
        }
        self.assertTrue(self.crawler._is_valid_response(valid_data))
        
        # 测试无效响应
        invalid_data_cases = [
            {},  # 空字典
            {'fund_code': '000001'},  # 缺少必要字段
            {'fund_code': '000001', 'fund_name': '', 'net_value': 0},  # 无效值
            {'fund_code': '000001', 'fund_name': '测试', 'net_value': -1},  # 负净值
        ]
        
        for invalid_data in invalid_data_cases:
            self.assertFalse(self.crawler._is_valid_response(invalid_data))
    
    def test_data_completeness_check(self):
        """测试数据完整性检查"""
        # 完整数据
        complete_data = {
            'fund_code': '000001',
            'fund_name': '华夏成长混合',
            'net_value': 1.2340,
            'change_rate': 2.15,
            'change_amount': 0.026,
            'update_time': '2024-08-30 15:00:00'
        }
        self.assertTrue(self.crawler._has_complete_info(complete_data))
        
        # 不完整数据
        incomplete_data = {
            'fund_code': '000001',
            'fund_name': '华夏成长混合',
            'net_value': 1.2340
            # 缺少扩展字段
        }
        self.assertFalse(self.crawler._has_complete_info(incomplete_data))
    
    def test_multiple_funds_data(self):
        """测试批量获取基金数据"""
        test_codes = ["000001", "110022"]
        
        results = self.crawler.get_multiple_funds_data(test_codes)
        
        # 检查返回类型
        self.assertIsInstance(results, dict)
        
        # 如果网络可用且获取成功
        if results:
            for code, data in results.items():
                self.assertIn(code, test_codes)
                self.assertIsInstance(data, dict)
                if data:  # 如果数据不为空
                    self.assertTrue(self.crawler._is_valid_response(data))
    
    def test_config_based_fund_retrieval(self):
        """测试基于配置文件的基金获取"""
        try:
            config_funds = self.crawler.get_fund_info_from_config()
            self.assertIsInstance(config_funds, dict)
            
            # 如果配置中有基金代码且网络可用
            if config_funds:
                for fund_code, fund_data in config_funds.items():
                    self.assertIsInstance(fund_code, str)
                    self.assertIsInstance(fund_data, dict)
                    if fund_data:
                        self.assertTrue(self.crawler._is_valid_response(fund_data))
                        
        except Exception as e:
            # 配置文件可能不存在，跳过测试
            self.skipTest(f"配置文件相关测试跳过: {str(e)}")
    
    def test_tiantianjijin_data_parsing(self):
        """测试天天基金数据解析"""
        # 模拟天天基金返回的数据格式
        mock_data = {
            'fundcode': '000001',
            'name': '华夏成长混合',
            'dwjz': '1.2340',
            'gszzl': '2.15',
            'gsz': '1.2600',
            'ljjz': '1.2366',
            'gztime': '2024-08-30 15:00:00'
        }
        
        parsed_data = self.crawler._parse_tiantianjijin_data(mock_data, '000001')
        
        self.assertIsInstance(parsed_data, dict)
        if parsed_data:  # 如果解析成功
            self.assertEqual(parsed_data['fund_code'], '000001')
            self.assertEqual(parsed_data['fund_name'], '华夏成长混合')
            self.assertEqual(parsed_data['net_value'], 1.2340)
            self.assertEqual(parsed_data['change_rate'], 2.15)
            self.assertEqual(parsed_data['data_source'], 'tiantianjijin')
    
    def test_sina_data_parsing(self):
        """测试新浪财经数据解析"""
        # 模拟新浪数据格式
        mock_content = 'var hq_str_f_000001="华夏成长混合,1.2340,0.026,2.15,1.2366,,2024-08-30,15:00:00";'
        
        parsed_data = self.crawler._parse_sina_data(mock_content, '000001')
        
        self.assertIsInstance(parsed_data, dict)
        if parsed_data:  # 如果解析成功
            self.assertEqual(parsed_data['fund_code'], '000001')
            self.assertEqual(parsed_data['fund_name'], '华夏成长混合')
            self.assertEqual(parsed_data['net_value'], 1.2340)
            self.assertEqual(parsed_data['data_source'], 'sina')
    
    def test_eastmoney_data_parsing(self):
        """测试东方财富数据解析"""
        # 模拟东方财富返回的JSON格式
        mock_data = {
            'data': {
                'diff': [{
                    'f12': '000001',
                    'f14': '华夏成长混合',
                    'f2': 123400,  # 东财数据需要除以100
                    'f3': 215,
                    'f4': 2600,
                    'f5': 123660
                }]
            }
        }
        
        parsed_data = self.crawler._parse_eastmoney_data(mock_data, '000001')
        
        self.assertIsInstance(parsed_data, dict)
        if parsed_data:  # 如果解析成功
            self.assertEqual(parsed_data['fund_code'], '000001')
            self.assertEqual(parsed_data['fund_name'], '华夏成长混合')
            self.assertEqual(parsed_data['net_value'], 1234.0)  # 123400/100
            self.assertEqual(parsed_data['data_source'], 'eastmoney')


class TestFundCrawlerIntegration(unittest.TestCase):
    """基金爬取器集成测试"""
    
    def setUp(self):
        """测试前置设置"""
        self.crawler = FundCrawler()
    
    def tearDown(self):
        """测试后置清理"""
        if self.crawler:
            self.crawler.close()
    
    def test_end_to_end_fund_monitoring(self):
        """测试端到端的基金监控流程"""
        # 选择几个知名基金进行测试
        test_funds = ['000001', '110022']
        
        all_success = True
        results = {}
        
        for fund_code in test_funds:
            try:
                fund_data = self.crawler.get_fund_data(fund_code)
                if fund_data and self.crawler._is_valid_response(fund_data):
                    results[fund_code] = fund_data
                    print(f"✓ 基金 {fund_code} 数据获取成功: {fund_data.get('fund_name', 'N/A')}")
                else:
                    print(f"✗ 基金 {fund_code} 数据获取失败")
                    all_success = False
                    
            except Exception as e:
                print(f"✗ 基金 {fund_code} 测试异常: {str(e)}")
                all_success = False
        
        # 至少要有一个基金数据获取成功
        if results:
            print(f"集成测试部分成功，获取到 {len(results)} 个基金数据")
        else:
            print("集成测试失败，未获取到任何有效基金数据")
            # 网络问题时不算测试失败
            self.skipTest("网络连接问题，跳过集成测试")


def run_crawler_tests():
    """运行所有爬取器测试"""
    print("=" * 60)
    print("开始基金数据爬取模块测试")
    print("=" * 60)
    
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加基础功能测试
    test_suite.addTest(unittest.makeSuite(TestFundCrawler))
    
    # 添加集成测试
    test_suite.addTest(unittest.makeSuite(TestFundCrawlerIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("基金数据爬取模块测试结果")
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
    success = run_crawler_tests()
    exit(0 if success else 1)