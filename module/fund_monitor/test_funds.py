#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全球指数基金测试脚本
"""

import sys
import os
sys.path.append('src')

def test_fund_data():
    """测试基金数据获取"""
    try:
        from fund_crawler import FundCrawler
        
        print('🚀 开始测试全球指数基金数据获取...')
        print('=' * 60)
        
        crawler = FundCrawler()
        
        # 测试基金列表 - 全球指数主题
        test_funds = [
            ('513500', '标普500ETF'),
            ('159941', '纳指100ETF'),
            ('588000', '科创50ETF'),
            ('510500', '中证500ETF'),
            ('515000', '华夏中证红利ETF')
        ]
        
        success_count = 0
        results = []
        
        for fund_code, fund_name in test_funds:
            print(f'\n📊 测试基金: {fund_code} - {fund_name}')
            
            try:
                fund_data = crawler.get_fund_data(fund_code)
                
                if fund_data and crawler._is_valid_response(fund_data):
                    print(f'✅ 成功获取数据:')
                    print(f'   基金名称: {fund_data.get("fund_name", "N/A")}')
                    print(f'   净值: {fund_data.get("net_value", "N/A")}')
                    print(f'   涨跌幅: {fund_data.get("change_rate", "N/A")}%')
                    print(f'   数据源: {fund_data.get("data_source", "N/A")}')
                    
                    results.append(fund_data)
                    success_count += 1
                else:
                    print(f'❌ 数据获取失败或无效')
                    
            except Exception as e:
                print(f'💥 异常: {str(e)}')
        
        print('\n' + '=' * 60)
        print(f'📈 测试结果汇总:')
        print(f'总测试基金数: {len(test_funds)}')
        print(f'成功获取数据: {success_count}')
        print(f'成功率: {success_count/len(test_funds)*100:.1f}%')
        
        crawler.close()
        
        return results
        
    except ImportError as e:
        print(f'❌ 模块导入失败: {e}')
        return []
    except Exception as e:
        print(f'💥 测试异常: {e}')
        return []

def test_data_processing():
    """测试数据处理功能"""
    try:
        from data_processor import DataProcessor
        
        print('\n🔄 测试数据处理功能...')
        print('-' * 40)
        
        processor = DataProcessor()
        
        # 模拟基金数据
        test_data = {
            '513500': {
                'fund_code': '513500',
                'fund_name': '标普500ETF',
                'net_value': 1.4567,
                'change_rate': 1.25,
                'change_amount': 0.018,
                'total_value': 1.4567,
                'update_time': '2024-08-30 15:00:00'
            },
            '588000': {
                'fund_code': '588000',
                'fund_name': '科创50ETF',
                'net_value': 0.8934,
                'change_rate': -2.15,
                'change_amount': -0.0196,
                'total_value': 0.8934,
                'update_time': '2024-08-30 15:00:00'
            }
        }
        
        # 处理数据
        processed_funds = processor.process_multiple_funds(test_data)
        
        print(f'✅ 数据处理成功，处理了 {len(processed_funds)} 个基金')
        
        # 生成汇总
        summary = processor.generate_summary(processed_funds)
        
        print(f'📊 汇总信息:')
        print(f'   总基金数: {summary["total_funds"]}')
        print(f'   上涨基金: {summary["rise_count"]}')
        print(f'   下跌基金: {summary["fall_count"]}') 
        print(f'   预警基金: {summary["alert_count"]}')
        
        return processed_funds
        
    except ImportError as e:
        print(f'❌ 数据处理模块导入失败: {e}')
        return []
    except Exception as e:
        print(f'💥 数据处理异常: {e}')
        return []

def test_email_config():
    """测试邮件配置"""
    try:
        from email_sender import EmailSender
        
        print('\n📧 测试邮件配置...')
        print('-' * 40)
        
        sender = EmailSender()
        
        print(f'✅ 邮件发送器初始化成功')
        print(f'   邮件服务商: {sender.provider}')
        print(f'   发送邮箱: {sender.username}')
        print(f'   主要收件人: {sender.primary_recipients}')
        
        # 验证配置（但不实际发送邮件）
        print('\n🔍 配置验证结果：')
        if sender.username == 'firfunneral_h@126.com':
            print('✅ 测试邮箱配置正确')
        else:
            print('❌ 测试邮箱配置不正确')
            
        if 'firfunneral_h@126.com' in sender.primary_recipients:
            print('✅ 收件人配置正确')
        else:
            print('❌ 收件人配置不正确')
            
        return True
        
    except ImportError as e:
        print(f'❌ 邮件模块导入失败: {e}')
        return False
    except Exception as e:
        print(f'💥 邮件配置异常: {e}')
        return False

if __name__ == '__main__':
    print('🧪 全球指数基金监控系统测试')
    print('=' * 80)
    
    # 测试基金数据获取
    fund_results = test_fund_data()
    
    # 测试数据处理
    processed_results = test_data_processing()
    
    # 测试邮件配置
    email_ok = test_email_config()
    
    print('\n' + '=' * 80)
    print('🏁 测试总结:')
    print(f'   基金数据获取: {"✅ 成功" if fund_results else "❌ 失败"}')
    print(f'   数据处理功能: {"✅ 成功" if processed_results else "❌ 失败"}')
    print(f'   邮件配置检查: {"✅ 成功" if email_ok else "❌ 失败"}')
    
    if fund_results and processed_results and email_ok:
        print('\n🎉 所有功能测试通过！系统已准备就绪。')
        print('\n💡 下一步：')
        print('   1. 在 config/email_config.ini 中设置正确的 SMTP 密码')
        print('   2. 运行: python src/monitor_main.py --mode test')
        print('   3. 发送测试邮件验证完整流程')
    else:
        print('\n⚠️ 部分功能存在问题，请检查配置和网络连接。')