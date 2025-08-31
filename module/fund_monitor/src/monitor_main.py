#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金监控系统主程序
整合数据爬取、处理和邮件发送功能，实现完整的基金监控流程
"""

import os
import sys
import logging
import configparser
import schedule
import time
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# 添加模块路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fund_crawler import FundCrawler
from email_sender import EmailSender
from data_processor import DataProcessor


class FundMonitor:
    """基金监控系统主类"""
    
    def __init__(self, fund_config_file: str = "config/fund_config.ini",
                 email_config_file: str = "config/email_config.ini"):
        """
        初始化基金监控系统
        
        Args:
            fund_config_file: 基金配置文件路径
            email_config_file: 邮件配置文件路径
        """
        self.fund_config_file = fund_config_file
        self.email_config_file = email_config_file
        
        # 加载配置
        self.config = configparser.ConfigParser()
        self.config.read(fund_config_file, encoding='utf-8')
        
        # 配置日志
        self._setup_logging()
        
        # 初始化各模块
        self.crawler: Optional[FundCrawler] = None
        self.email_sender: Optional[EmailSender] = None
        self.processor: Optional[DataProcessor] = None
        
        self._initialize_modules()
        
        # 运行状态
        self.is_running = False
        self.last_run_time = None
        
        self.logger.info("基金监控系统初始化完成")
    
    def _setup_logging(self):
        """设置日志配置"""
        # 获取日志配置
        log_level = self.config.get('LOGGING', 'log_level', fallback='INFO')
        log_file = self.config.get('LOGGING', 'log_file', fallback='logs/monitor.log')
        console_output = self.config.getboolean('LOGGING', 'console_output', fallback=True)
        
        # 确保日志目录存在
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # 创建logger
        self.logger = logging.getLogger('FundMonitor')
        self.logger.setLevel(getattr(logging, log_level))
        
        # 清除已有的处理器
        self.logger.handlers.clear()
        
        # 文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # 控制台处理器
        if console_output:
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
    
    def _initialize_modules(self):
        """初始化各功能模块"""
        try:
            # 初始化数据爬取器
            self.crawler = FundCrawler(self.fund_config_file)
            self.logger.info("数据爬取器初始化成功")
            
            # 初始化邮件发送器
            self.email_sender = EmailSender(self.email_config_file)
            self.logger.info("邮件发送器初始化成功")
            
            # 初始化数据处理器
            self.processor = DataProcessor(self.fund_config_file)
            self.logger.info("数据处理器初始化成功")
            
        except Exception as e:
            self.logger.error(f"模块初始化失败: {str(e)}")
            raise
    
    def run_monitor(self) -> bool:
        """
        执行一次完整的基金监控流程
        
        Returns:
            监控是否成功完成
        """
        start_time = datetime.now()
        self.logger.info("=" * 50)
        self.logger.info("开始基金监控任务")
        
        try:
            # 1. 获取基金数据
            self.logger.info("步骤1: 获取基金数据")
            if not self.crawler:
                self.logger.error("数据爬取器未初始化")
                return False
            raw_funds_data = self.crawler.get_fund_info_from_config()
            
            if not raw_funds_data:
                self.logger.error("未获取到任何基金数据")
                return False
            
            self.logger.info(f"成功获取 {len(raw_funds_data)} 个基金数据")
            
            # 2. 处理数据
            self.logger.info("步骤2: 处理基金数据")
            if not self.processor:
                self.logger.error("数据处理器未初始化")
                return False
            processed_funds = self.processor.process_multiple_funds(raw_funds_data)
            
            if not processed_funds:
                self.logger.error("基金数据处理失败")
                return False
            
            # 3. 生成汇总信息
            summary = self.processor.generate_summary(processed_funds)
            self.logger.info(f"数据汇总: {summary['total_funds']}个基金, "
                           f"{summary['rise_count']}涨{summary['fall_count']}跌, "
                           f"{summary['alert_count']}个预警")
            
            # 4. 保存历史数据
            self.logger.info("步骤3: 保存历史数据")
            save_success = self.processor.save_history_data(processed_funds)
            if save_success:
                self.logger.info("历史数据保存成功")
            else:
                self.logger.warning("历史数据保存失败")
            
            # 5. 发送邮件报告
            self.logger.info("步骤4: 发送邮件报告")
            if not self.email_sender:
                self.logger.error("邮件发送器未初始化")
                return False
            email_success = self.email_sender.send_fund_report(processed_funds)
            
            if email_success:
                self.logger.info("邮件报告发送成功")
            else:
                self.logger.error("邮件报告发送失败")
                return False
            
            # 6. 更新运行状态
            self.last_run_time = start_time
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.logger.info(f"基金监控任务完成，耗时 {duration:.2f} 秒")
            self.logger.info("=" * 50)
            
            return True
            
        except Exception as e:
            self.logger.error(f"基金监控任务失败: {str(e)}")
            return False
        finally:
            # 清理资源
            if self.crawler:
                self.crawler.close()
    
    def setup_schedule(self):
        """设置定时任务"""
        # 获取监控时间配置
        monitor_times_str = self.config.get('SCHEDULE', 'monitor_times', 
                                           fallback='09:30,11:30,15:00')
        monitor_times = [time.strip() for time in monitor_times_str.split(',')]
        
        # 周末和节假日配置
        weekend_monitor = self.config.getboolean('SCHEDULE', 'weekend_monitor', fallback=False)
        holiday_monitor = self.config.getboolean('SCHEDULE', 'holiday_monitor', fallback=False)
        
        self.logger.info(f"配置定时任务: {monitor_times}")
        
        # 为每个时间点设置任务
        for monitor_time in monitor_times:
            try:
                if self._is_valid_time_format(monitor_time):
                    if weekend_monitor:
                        # 包括周末
                        schedule.every().day.at(monitor_time).do(self._scheduled_run)
                    else:
                        # 仅工作日
                        schedule.every().monday.at(monitor_time).do(self._scheduled_run)
                        schedule.every().tuesday.at(monitor_time).do(self._scheduled_run)
                        schedule.every().wednesday.at(monitor_time).do(self._scheduled_run)
                        schedule.every().thursday.at(monitor_time).do(self._scheduled_run)
                        schedule.every().friday.at(monitor_time).do(self._scheduled_run)
                    
                    self.logger.info(f"已设置定时任务: {monitor_time}")
                else:
                    self.logger.warning(f"无效的时间格式: {monitor_time}")
                    
            except Exception as e:
                self.logger.error(f"设置定时任务失败 - {monitor_time}: {str(e)}")
    
    def _is_valid_time_format(self, time_str: str) -> bool:
        """验证时间格式是否正确"""
        try:
            datetime.strptime(time_str, '%H:%M')
            return True
        except ValueError:
            return False
    
    def _scheduled_run(self):
        """定时任务执行函数"""
        # 检查是否在交易时间
        if not self._is_trading_time():
            self.logger.info("当前不在交易时间，跳过监控")
            return
        
        # 执行监控
        success = self.run_monitor()
        if success:
            self.logger.info("定时监控任务执行成功")
        else:
            self.logger.error("定时监控任务执行失败")
    
    def _is_trading_time(self) -> bool:
        """检查是否在交易时间"""
        now = datetime.now()
        
        # 检查是否为工作日
        if now.weekday() >= 5:  # 周六周日
            weekend_monitor = self.config.getboolean('SCHEDULE', 'weekend_monitor', fallback=False)
            if not weekend_monitor:
                return False
        
        # 这里可以添加更多的交易时间检查逻辑
        # 例如：检查是否为节假日、是否在开盘时间等
        
        return True
    
    def start_daemon(self):
        """启动守护进程模式"""
        self.logger.info("启动基金监控守护进程")
        self.is_running = True
        
        # 设置定时任务
        self.setup_schedule()
        
        try:
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
                
        except KeyboardInterrupt:
            self.logger.info("接收到停止信号")
        except Exception as e:
            self.logger.error(f"守护进程异常: {str(e)}")
        finally:
            self.stop_daemon()
    
    def stop_daemon(self):
        """停止守护进程"""
        self.logger.info("停止基金监控守护进程")
        self.is_running = False
        
        # 清理资源
        if self.crawler:
            self.crawler.close()
    
    def get_status(self) -> Dict[str, Any]:
        """获取监控状态"""
        return {
            'is_running': self.is_running,
            'last_run_time': self.last_run_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_run_time else None,
            'next_scheduled_runs': [str(job) for job in schedule.jobs],
            'modules_status': {
                'crawler': self.crawler is not None,
                'email_sender': self.email_sender is not None,
                'processor': self.processor is not None
            }
        }
    
    def validate_configuration(self) -> bool:
        """验证配置"""
        self.logger.info("验证系统配置...")
        
        errors = []
        
        # 验证基金配置
        fund_codes_str = self.config.get('MONITOR_FUNDS', 'fund_codes', fallback='')
        if not fund_codes_str.strip():
            errors.append("未配置监控基金代码")
        
        # 验证邮件配置
        if self.email_sender and not self.email_sender.validate_config():
            errors.append("邮件配置验证失败")
        
        # 验证目录权限
        required_dirs = ['logs', 'data']
        for dir_name in required_dirs:
            try:
                os.makedirs(dir_name, exist_ok=True)
            except Exception as e:
                errors.append(f"无法创建目录 {dir_name}: {str(e)}")
        
        if errors:
            for error in errors:
                self.logger.error(f"配置错误: {error}")
            return False
        
        self.logger.info("配置验证通过")
        return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='基金监控系统')
    parser.add_argument('--mode', choices=['once', 'daemon', 'test', 'status'], 
                       default='once', help='运行模式')
    parser.add_argument('--fund-config', default='config/fund_config.ini',
                       help='基金配置文件路径')
    parser.add_argument('--email-config', default='config/email_config.ini',
                       help='邮件配置文件路径')
    
    args = parser.parse_args()
    
    try:
        # 初始化监控系统
        monitor = FundMonitor(args.fund_config, args.email_config)
        
        # 验证配置
        if not monitor.validate_configuration():
            print("配置验证失败，请检查配置文件")
            return 1
        
        if args.mode == 'once':
            # 单次运行模式
            print("执行单次基金监控...")
            success = monitor.run_monitor()
            return 0 if success else 1
            
        elif args.mode == 'daemon':
            # 守护进程模式
            print("启动基金监控守护进程...")
            monitor.start_daemon()
            return 0
            
        elif args.mode == 'test':
            # 测试模式
            print("测试邮件发送...")
            if monitor.email_sender:
                success = monitor.email_sender.send_test_email()
                print(f"测试邮件发送{'成功' if success else '失败'}")
                return 0 if success else 1
            else:
                print("邮件发送器初始化失败")
                return 1
                
        elif args.mode == 'status':
            # 状态查看模式
            status = monitor.get_status()
            print("基金监控系统状态:")
            for key, value in status.items():
                print(f"  {key}: {value}")
            return 0
            
    except Exception as e:
        print(f"程序运行失败: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())