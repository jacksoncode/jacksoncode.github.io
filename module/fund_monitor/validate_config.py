#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置验证和快速测试脚本
"""

import configparser
import os

def validate_config():
    """验证配置文件"""
    print("🔍 验证配置文件...")
    print("=" * 50)
    
    # 检查基金配置
    try:
        fund_config = configparser.ConfigParser()
        fund_config.read('config/fund_config.ini', encoding='utf-8')
        
        fund_codes = fund_config.get('MONITOR_FUNDS', 'fund_codes')
        codes_list = [code.strip() for code in fund_codes.split(',')]
        
        print(f"✅ 基金配置文件读取成功")
        print(f"   监控基金数量: {len(codes_list)}")
        print(f"   基金代码: {', '.join(codes_list[:5])}{'...' if len(codes_list) > 5 else ''}")
        
        # 验证指数基金主题
        index_themes = {
            '513500': '标普500',
            '159941': '纳斯达克100', 
            '588000': '科创50',
            '510500': '中证500',
            '515000': '红利指数',
            '161130': '港股红利'
        }
        
        print(f"\n📊 指数基金主题覆盖:")
        for code, theme in index_themes.items():
            if code in codes_list:
                print(f"   ✅ {theme}: {code}")
            else:
                print(f"   ❌ {theme}: {code} (未配置)")
                
    except Exception as e:
        print(f"❌ 基金配置文件错误: {e}")
        return False
    
    # 检查邮件配置
    try:
        email_config = configparser.ConfigParser()
        email_config.read('config/email_config.ini', encoding='utf-8')
        
        provider = email_config.get('SMTP', 'provider')
        username = email_config.get('SMTP', 'username')
        primary_recipients = email_config.get('RECIPIENTS', 'primary')
        
        print(f"\n📧 邮件配置验证:")
        print(f"   服务商: {provider}")
        print(f"   发送邮箱: {username}")
        print(f"   收件人: {primary_recipients}")
        
        if username == 'firfunneral_h@126.com':
            print("   ✅ 测试邮箱配置正确")
        else:
            print("   ❌ 测试邮箱配置错误")
            
        if 'firfunneral_h@126.com' in primary_recipients:
            print("   ✅ 收件人配置正确")
        else:
            print("   ❌ 收件人配置错误")
            
    except Exception as e:
        print(f"❌ 邮件配置文件错误: {e}")
        return False
    
    return True

def test_module_imports():
    """测试模块导入"""
    print("\n🔧 测试模块导入...")
    print("-" * 30)
    
    import sys
    sys.path.append('src')
    
    modules = [
        ('fund_crawler', 'FundCrawler'),
        ('email_sender', 'EmailSender'),
        ('data_processor', 'DataProcessor'),
        ('monitor_main', 'FundMonitor')
    ]
    
    success_count = 0
    
    for module_name, class_name in modules:
        try:
            module = __import__(module_name)
            cls = getattr(module, class_name)
            print(f"✅ {module_name}.{class_name}")
            success_count += 1
        except ImportError as e:
            print(f"❌ {module_name}.{class_name}: 导入失败 - {e}")
        except AttributeError as e:
            print(f"❌ {module_name}.{class_name}: 类不存在 - {e}")
        except Exception as e:
            print(f"❌ {module_name}.{class_name}: 其他错误 - {e}")
    
    print(f"\n模块导入成功率: {success_count}/{len(modules)} ({success_count/len(modules)*100:.1f}%)")
    return success_count == len(modules)

def create_test_data():
    """创建测试数据"""
    print("\n🧪 创建测试数据...")
    print("-" * 30)
    
    # 全球指数基金测试数据
    test_data = {
        '513500': {
            'fund_code': '513500',
            'fund_name': '标普500ETF',
            'net_value': 1.4567,
            'change_rate': 1.25,
            'change_amount': 0.018,
            'total_value': 1.4567,
            'update_time': '2024-08-30 15:00:00',
            'data_source': 'test'
        },
        '159941': {
            'fund_code': '159941', 
            'fund_name': '纳指100ETF',
            'net_value': 2.1234,
            'change_rate': 2.35,
            'change_amount': 0.048,
            'total_value': 2.1234,
            'update_time': '2024-08-30 15:00:00',
            'data_source': 'test'
        },
        '588000': {
            'fund_code': '588000',
            'fund_name': '科创50ETF', 
            'net_value': 0.8934,
            'change_rate': -1.85,
            'change_amount': -0.0168,
            'total_value': 0.8934,
            'update_time': '2024-08-30 15:00:00',
            'data_source': 'test'
        },
        '510500': {
            'fund_code': '510500',
            'fund_name': '中证500ETF',
            'net_value': 1.2456,
            'change_rate': 0.85,
            'change_amount': 0.0105,
            'total_value': 1.2456,
            'update_time': '2024-08-30 15:00:00',
            'data_source': 'test'
        },
        '515000': {
            'fund_code': '515000',
            'fund_name': '华夏中证红利ETF',
            'net_value': 1.1234,
            'change_rate': -0.35,
            'change_amount': -0.0039,
            'total_value': 1.1234,
            'update_time': '2024-08-30 15:00:00',
            'data_source': 'test'
        }
    }
    
    print(f"✅ 创建了 {len(test_data)} 个基金的测试数据")
    
    # 显示数据概览
    for code, data in test_data.items():
        change_indicator = "📈" if data['change_rate'] > 0 else "📉" if data['change_rate'] < 0 else "➡️"
        print(f"   {change_indicator} {code}: {data['fund_name']} ({data['change_rate']:+.2f}%)")
    
    return test_data

def simulate_data_processing(test_data):
    """模拟数据处理流程"""
    print("\n⚙️ 模拟数据处理流程...")
    print("-" * 30)
    
    try:
        import sys
        sys.path.append('src')
        from data_processor import DataProcessor
        
        processor = DataProcessor()
        
        # 处理数据
        processed_funds = processor.process_multiple_funds(test_data)
        print(f"✅ 数据处理成功，处理了 {len(processed_funds)} 个基金")
        
        # 生成汇总
        summary = processor.generate_summary(processed_funds)
        
        print(f"\n📊 汇总信息:")
        print(f"   总基金数: {summary['total_funds']}")
        print(f"   上涨基金数: {summary['rise_count']}")
        print(f"   下跌基金数: {summary['fall_count']}")
        print(f"   预警基金数: {summary['alert_count']}")
        
        if summary['alert_count'] > 0:
            print(f"\n⚠️ 预警基金:")
            for fund in summary['alert_funds']:
                print(f"   - {fund['fund_name']}: {fund['change_rate']:+.2f}%")
        
        return processed_funds
        
    except Exception as e:
        print(f"❌ 数据处理失败: {e}")
        return []

def simulate_email_generation(processed_funds):
    """模拟邮件生成"""
    print("\n📧 模拟邮件生成...")
    print("-" * 30)
    
    try:
        import sys
        sys.path.append('src')
        from email_sender import EmailSender
        
        sender = EmailSender()
        
        # 生成邮件内容
        content = sender._generate_email_content(processed_funds)
        
        print(f"✅ 邮件内容生成成功")
        print(f"   邮件长度: {len(content)} 字符")
        print(f"   包含HTML格式: {'是' if '<html>' in content else '否'}")
        print(f"   包含基金数据: {'是' if '基金监控日报' in content else '否'}")
        
        # 显示邮件预览(前200字符)
        preview = content.replace('\n', ' ').replace('\t', ' ')[:200] + "..."
        print(f"\n📝 邮件内容预览:")
        print(f"   {preview}")
        
        return True
        
    except Exception as e:
        print(f"❌ 邮件生成失败: {e}")
        return False

def main():
    """主函数"""
    print("🌟 全球指数基金监控系统 - 配置验证与测试")
    print("=" * 80)
    
    # 1. 验证配置
    config_ok = validate_config()
    
    # 2. 测试模块导入
    import_ok = test_module_imports()
    
    # 3. 创建测试数据
    test_data = create_test_data()
    
    # 4. 模拟数据处理
    processed_data = simulate_data_processing(test_data) if import_ok else []
    
    # 5. 模拟邮件生成
    email_ok = simulate_email_generation(processed_data) if processed_data else False
    
    # 总结
    print("\n" + "=" * 80)
    print("🏁 测试总结:")
    print(f"   ✅ 配置验证: {'通过' if config_ok else '失败'}")
    print(f"   ✅ 模块导入: {'通过' if import_ok else '失败'}")
    print(f"   ✅ 数据处理: {'通过' if processed_data else '失败'}")
    print(f"   ✅ 邮件生成: {'通过' if email_ok else '失败'}")
    
    if config_ok and import_ok and processed_data and email_ok:
        print("\n🎉 所有测试通过！系统准备就绪。")
        print("\n💡 下一步操作:")
        print("   1. 设置163邮箱的SMTP授权码")
        print("   2. 更新 config/email_config.ini 中的 password 字段")
        print("   3. 运行: python src/monitor_main.py --mode test")
        print("   4. 验证是否能收到测试邮件")
        print("\n📋 全球指数基金监控组合:")
        print("   🌎 标普500ETF (513500) - 美股大盘")
        print("   🚀 纳指100ETF (159941) - 美股科技")
        print("   🧪 科创50ETF (588000) - 中国科技创新")
        print("   📊 中证500ETF (510500) - 中盘成长") 
        print("   💰 华夏红利ETF (515000) - 红利价值")
        print("   🏙️ 易方达恒生ETF (161130) - 港股红利")
    else:
        print("\n⚠️ 部分测试失败，请检查错误信息并修复。")

if __name__ == '__main__':
    main()