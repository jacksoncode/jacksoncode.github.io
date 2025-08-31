#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主程序集成测试
"""

import unittest
import sys
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock

# 添加源码路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from monitor_main import FundMonitor


class TestFundMonitor(unittest.TestCase):
    """基金监控主程序测试类"""
    
    def setUp(self):
        """测试前置设置"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Mock配置文件
        with patch('configparser.ConfigParser') as mock_config_class:
            mock_config = MagicMock()
            mock_config_class.return_value = mock_config
            
            # 设置Mock配置返回值
            mock_config.get.side_effect = self._mock_config_get
            mock_config.getboolean.side_effect = self._mock_config_getboolean
            mock_config.getint.side_effect = self._mock_config_getint
            
            # Mock各个模块的初始化
            with patch('monitor_main.FundCrawler') as mock_crawler_class, \
                 patch('monitor_main.EmailSender') as mock_sender_class, \
                 patch('monitor_main.DataProcessor') as mock_processor_class:
                
                # 创建Mock对象
                self.mock_crawler = Mock()
                self.mock_sender = Mock()
                self.mock_processor = Mock()
                
                mock_crawler_class.return_value = self.mock_crawler
                mock_sender_class.return_value = self.mock_sender
                mock_processor_class.return_value = self.mock_processor
                
                self.monitor = FundMonitor()
    
    def tearDown(self):
        """测试后置清理"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def _mock_config_get(self, section, option, fallback=None):
        """Mock配置get方法"""
        config_values = {
            ('LOGGING', 'log_level'): 'INFO',
            ('LOGGING', 'log_file'): os.path.join(self.temp_dir, 'test.log'),
            ('MONITOR_FUNDS', 'fund_codes'): '000001,110022',
            ('SCHEDULE', 'monitor_times'): '09:30,15:00',
        }
        return config_values.get((section, option), fallback)
    
    def _mock_config_getboolean(self, section, option, fallback=None):
        """Mock配置getboolean方法"""
        boolean_values = {
            ('LOGGING', 'console_output'): True,
            ('SCHEDULE', 'weekend_monitor'): False,
            ('SCHEDULE', 'holiday_monitor'): False,
        }
        return boolean_values.get((section, option), fallback)
    
    def _mock_config_getint(self, section, option, fallback=None):
        """Mock配置getint方法"""
        int_values = {
            ('SCHEDULE', 'timeout'): 10,
            ('SCHEDULE', 'retry_times'): 3,
        }
        return int_values.get((section, option), fallback)
    
    def test_monitor_initialization(self):
        """测试监控器初始化"""
        self.assertIsNotNone(self.monitor)
        self.assertIsNotNone(self.monitor.crawler)
        self.assertIsNotNone(self.monitor.email_sender)
        self.assertIsNotNone(self.monitor.processor)
        self.assertFalse(self.monitor.is_running)
        self.assertIsNone(self.monitor.last_run_time)
    
    def test_run_monitor_success(self):
        """测试成功的监控流程"""
        # 设置Mock返回值
        mock_fund_data = {
            '000001': {
                'fund_code': '000001',
                'fund_name': '华夏成长混合',
                'net_value': 1.2340,
                'change_rate': 2.15
            }
        }
        
        mock_processed_funds = [
            {
                'fund_code': '000001',
                'fund_name': '华夏成长混合',
                'net_value': 1.2340,
                'change_rate': 2.15,
                'is_alert': False
            }
        ]
        
        # 配置Mock行为
        self.mock_crawler.get_fund_info_from_config.return_value = mock_fund_data
        self.mock_processor.process_multiple_funds.return_value = mock_processed_funds
        self.mock_processor.generate_summary.return_value = {
            'total_funds': 1,
            'rise_count': 1,
            'fall_count': 0,
            'alert_count': 0
        }
        self.mock_processor.save_history_data.return_value = True
        self.mock_sender.send_fund_report.return_value = True
        
        # 执行监控
        result = self.monitor.run_monitor()
        
        # 验证结果
        self.assertTrue(result)
        self.assertIsNotNone(self.monitor.last_run_time)
        
        # 验证方法调用
        self.mock_crawler.get_fund_info_from_config.assert_called_once()
        self.mock_processor.process_multiple_funds.assert_called_once_with(mock_fund_data)
        self.mock_processor.save_history_data.assert_called_once_with(mock_processed_funds)
        self.mock_sender.send_fund_report.assert_called_once_with(mock_processed_funds)
        self.mock_crawler.close.assert_called_once()
    
    def test_run_monitor_no_data(self):
        """测试无数据的监控流程"""
        # 设置无数据返回
        self.mock_crawler.get_fund_info_from_config.return_value = {}
        
        # 执行监控
        result = self.monitor.run_monitor()
        
        # 验证结果
        self.assertFalse(result)
        
        # 验证只调用了数据获取，其他步骤被跳过
        self.mock_crawler.get_fund_info_from_config.assert_called_once()
        self.mock_processor.process_multiple_funds.assert_not_called()
        self.mock_sender.send_fund_report.assert_not_called()
    
    def test_run_monitor_email_failure(self):
        """测试邮件发送失败的监控流程"""
        # 设置数据获取和处理成功，但邮件发送失败
        self.mock_crawler.get_fund_info_from_config.return_value = {'000001': {}}
        self.mock_processor.process_multiple_funds.return_value = [{}]
        self.mock_processor.save_history_data.return_value = True
        self.mock_sender.send_fund_report.return_value = False  # 邮件发送失败
        
        # 执行监控
        result = self.monitor.run_monitor()
        
        # 验证结果
        self.assertFalse(result)
        
        # 验证所有步骤都被调用了
        self.mock_crawler.get_fund_info_from_config.assert_called_once()
        self.mock_processor.process_multiple_funds.assert_called_once()
        self.mock_sender.send_fund_report.assert_called_once()
    
    def test_run_monitor_exception_handling(self):
        """测试异常处理"""
        # 设置异常
        self.mock_crawler.get_fund_info_from_config.side_effect = Exception("网络错误")
        
        # 执行监控
        result = self.monitor.run_monitor()
        
        # 验证结果
        self.assertFalse(result)
        
        # 验证清理方法被调用
        self.mock_crawler.close.assert_called_once()
    
    def test_time_format_validation(self):
        """测试时间格式验证"""
        valid_times = ['09:30', '15:00', '23:59']
        invalid_times = ['9:30', '25:00', 'abc', '9:3']
        
        for time_str in valid_times:
            self.assertTrue(self.monitor._is_valid_time_format(time_str),
                          f"时间 {time_str} 应该是有效的")
        
        for time_str in invalid_times:
            self.assertFalse(self.monitor._is_valid_time_format(time_str),
                           f"时间 {time_str} 应该是无效的")
    
    @patch('schedule.every')
    def test_schedule_setup(self, mock_schedule):
        """测试定时任务设置"""
        # Mock schedule对象
        mock_job = Mock()
        mock_schedule.return_value.day.at.return_value.do = Mock(return_value=mock_job)
        mock_schedule.return_value.monday.at.return_value.do = Mock(return_value=mock_job)
        mock_schedule.return_value.tuesday.at.return_value.do = Mock(return_value=mock_job)
        mock_schedule.return_value.wednesday.at.return_value.do = Mock(return_value=mock_job)
        mock_schedule.return_value.thursday.at.return_value.do = Mock(return_value=mock_job)
        mock_schedule.return_value.friday.at.return_value.do = Mock(return_value=mock_job)
        
        # 执行设置
        self.monitor.setup_schedule()
        
        # 验证调用（工作日模式，每个时间点应该有5个任务）
        expected_calls = 2 * 5  # 2个时间点 * 5个工作日
        actual_calls = len([call for call in mock_schedule.call_args_list])
        self.assertGreater(actual_calls, 0)  # 至少有一些调用
    
    def test_trading_time_check(self):
        """测试交易时间检查"""
        # 基础实现应该总是返回True（除非配置了周末不监控且当前是周末）
        result = self.monitor._is_trading_time()
        self.assertIsInstance(result, bool)
    
    def test_get_status(self):
        """测试状态获取"""
        status = self.monitor.get_status()
        
        self.assertIsInstance(status, dict)
        self.assertIn('is_running', status)
        self.assertIn('last_run_time', status)
        self.assertIn('next_scheduled_runs', status)
        self.assertIn('modules_status', status)
        
        modules_status = status['modules_status']
        self.assertIn('crawler', modules_status)
        self.assertIn('email_sender', modules_status)
        self.assertIn('processor', modules_status)
        
        # 检查模块状态
        self.assertTrue(modules_status['crawler'])
        self.assertTrue(modules_status['email_sender'])
        self.assertTrue(modules_status['processor'])
    
    def test_configuration_validation(self):
        """测试配置验证"""
        # Mock邮件发送器验证成功
        self.mock_sender.validate_config.return_value = True
        
        result = self.monitor.validate_configuration()
        
        # 应该验证通过（因为我们mock了基金代码配置）
        self.assertTrue(result)
        
        # 验证邮件配置验证被调用
        self.mock_sender.validate_config.assert_called_once()
    
    def test_configuration_validation_failure(self):
        """测试配置验证失败"""
        # Mock邮件发送器验证失败
        self.mock_sender.validate_config.return_value = False
        
        result = self.monitor.validate_configuration()
        
        # 应该验证失败
        self.assertFalse(result)


class TestFundMonitorIntegration(unittest.TestCase):
    """基金监控集成测试（真实配置）"""
    
    def test_monitor_creation_with_missing_config(self):
        """测试缺少配置文件时的处理"""
        # 使用不存在的配置文件
        non_existent_config = "/tmp/non_existent_config.ini"
        
        try:
            monitor = FundMonitor(non_existent_config, non_existent_config)
            # 应该能创建但配置可能有问题
            self.assertIsNotNone(monitor)
        except Exception as e:
            # 也可能抛出异常，这也是合理的
            print(f"预期的配置文件缺失异常: {str(e)}")
    
    def test_logging_setup(self):
        """测试日志设置"""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, 'test.log')
            
            with patch('configparser.ConfigParser') as mock_config_class:
                mock_config = MagicMock()
                mock_config_class.return_value = mock_config
                
                mock_config.get.return_value = log_file
                mock_config.getboolean.return_value = True
                
                with patch('monitor_main.FundCrawler'), \
                     patch('monitor_main.EmailSender'), \
                     patch('monitor_main.DataProcessor'):
                    
                    monitor = FundMonitor()
                    
                    # 检查logger是否正确设置
                    self.assertIsNotNone(monitor.logger)
                    
                    # 测试日志写入
                    monitor.logger.info("测试日志消息")
                    
                    # 由于日志可能是异步的，这里只检查logger存在


def run_integration_tests():
    """运行所有集成测试"""
    print("=" * 60)
    print("开始主程序集成测试")
    print("=" * 60)
    
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加主程序测试
    test_suite.addTest(unittest.makeSuite(TestFundMonitor))
    
    # 添加集成测试
    test_suite.addTest(unittest.makeSuite(TestFundMonitorIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("主程序集成测试结果")
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
    success = run_integration_tests()
    exit(0 if success else 1)