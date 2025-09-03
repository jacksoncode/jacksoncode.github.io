#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件生成测试脚本
"""

import sys
import os
sys.path.append('src')

def test_email_generation():
    """测试邮件生成功能"""
    print("🧪 邮件生成功能测试")
    print("=" * 50)
    
    try:
        from email_sender import EmailSender
        
        # 创建邮件发送器
        print("📧 初始化邮件发送器...")
        sender = EmailSender()
        print(f"✅ 邮件发送器初始化成功")
        print(f"   模板路径: {sender.template_path}")
        print(f"   模板文件存在: {'是' if os.path.exists(sender.template_path) else '否'}")
        
        # 模拟基金数据
        test_funds = [
            {
                'fund_code': '513500',
                'fund_name': '标普500ETF',
                'net_value': 1.4567,
                'change_rate': 1.25,
                'change_amount': 0.018,
                'update_time': '2024-08-30 15:00:00',
                'is_alert': False
            },
            {
                'fund_code': '588000',
                'fund_name': '科创50ETF',
                'net_value': 0.8934,
                'change_rate': -2.15,
                'change_amount': -0.0196,
                'update_time': '2024-08-30 15:00:00',
                'is_alert': True
            },
            {
                'fund_code': '510500',
                'fund_name': '中证500ETF',
                'net_value': 1.2456,
                'change_rate': 0.85,
                'change_amount': 0.0105,
                'update_time': '2024-08-30 15:00:00',
                'is_alert': False
            }
        ]
        
        print(f"\n📊 使用 {len(test_funds)} 个基金数据测试...")
        for fund in test_funds:
            status_icon = "⚠️" if fund['is_alert'] else "✅"
            change_icon = "📈" if fund['change_rate'] > 0 else "📉" if fund['change_rate'] < 0 else "➡️"
            print(f"   {status_icon} {change_icon} {fund['fund_name']}: {fund['change_rate']:+.2f}%")
        
        # 测试表格行生成
        print(f"\n🔧 测试表格行生成...")
        fund_rows = sender._generate_fund_table_rows(test_funds)
        print(f"✅ 表格行生成成功，长度: {len(fund_rows)} 字符")
        
        # 测试邮件内容生成
        print(f"\n📝 测试完整邮件内容生成...")
        content = sender._generate_email_content(test_funds)
        print(f"✅ 邮件内容生成成功")
        print(f"   内容长度: {len(content)} 字符")
        print(f"   包含HTML: {'是' if '<html>' in content.lower() else '否'}")
        print(f"   包含基金数据: {'是' if '基金监控日报' in content else '否'}")
        
        # 显示内容预览
        print(f"\n📄 邮件内容预览 (前300字符):")
        preview = content.replace('\n', ' ').replace('\t', ' ')[:300]
        print(f"   {preview}...")
        
        # 测试邮件消息创建
        print(f"\n📮 测试邮件消息创建...")
        subject = "【测试】全球指数基金监控报告"
        recipients = ["test@example.com"]
        
        msg = sender._create_message(subject, content, recipients)
        print(f"✅ 邮件消息创建成功")
        print(f"   主题: {msg['Subject']}")
        print(f"   发件人: {msg['From']}")
        print(f"   收件人: {msg['To']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 邮件生成测试失败: {type(e).__name__}: {str(e)}")
        import traceback
        print("\n详细错误信息:")
        traceback.print_exc()
        return False

def test_template_loading():
    """测试模板加载"""
    print("\n🔍 模板加载测试")
    print("-" * 30)
    
    try:
        import sys
        sys.path.append('src')
        from email_sender import EmailSender
        
        sender = EmailSender()
        
        print(f"模板路径: {sender.template_path}")
        print(f"文件存在: {'是' if os.path.exists(sender.template_path) else '否'}")
        
        if os.path.exists(sender.template_path):
            with open(sender.template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            print(f"模板长度: {len(template_content)} 字符")
            print(f"包含变量: {template_content.count('{')}/{template_content.count('}')}")
        
        # 测试模板加载
        template = sender._load_email_template()
        print(f"✅ 模板加载成功，长度: {len(template)} 字符")
        
        # 检查必要的变量
        required_vars = ['{report_date}', '{total_funds}', '{rise_count}', 
                        '{fall_count}', '{alert_count}', '{fund_rows}', '{report_time}']
        
        missing_vars = []
        for var in required_vars:
            if var not in template:
                missing_vars.append(var)
        
        if missing_vars:
            print(f"⚠️ 缺少变量: {', '.join(missing_vars)}")
        else:
            print(f"✅ 所有必要变量都存在")
            
        return True
        
    except Exception as e:
        print(f"❌ 模板加载测试失败: {str(e)}")
        return False

if __name__ == '__main__':
    print("🌟 邮件系统功能测试")
    print("=" * 80)
    
    # 测试模板加载
    template_ok = test_template_loading()
    
    # 测试邮件生成
    generation_ok = test_email_generation()
    
    print("\n" + "=" * 80)
    print("🏁 测试总结:")
    print(f"   模板加载: {'✅ 成功' if template_ok else '❌ 失败'}")
    print(f"   邮件生成: {'✅ 成功' if generation_ok else '❌ 失败'}")
    
    if template_ok and generation_ok:
        print("\n🎉 邮件系统测试通过！现在可以正常发送邮件了。")
        print("\n💡 下一步测试:")
        print("   python3 src/monitor_main.py --mode test")
    else:
        print("\n⚠️ 邮件系统存在问题，请检查错误信息。")