#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的邮件配置检查脚本
"""

import configparser

def check_email_config():
    """检查邮件配置"""
    print("🔍 检查邮件配置文件...")
    print("=" * 40)
    
    try:
        # 读取邮件配置
        email_config = configparser.ConfigParser()
        email_config.read('config/email_config.ini', encoding='utf-8')
        
        # 获取配置项
        provider = email_config.get('SMTP', 'provider')
        username = email_config.get('SMTP', 'username')
        password = email_config.get('SMTP', 'password')
        primary_recipients = email_config.get('RECIPIENTS', 'primary')
        
        print(f"📧 邮件配置详情:")
        print(f"   服务商: {provider}")
        print(f"   发送邮箱: {username}")
        print(f"   密码/授权码: {'已设置' if password != 'your_smtp_authorization_code' else '未设置（需要配置）'}")
        print(f"   收件人: {primary_recipients}")
        
        print(f"\n🔍 配置验证:")
        
        # 检查发送邮箱
        if username == 'firfunneral_h@126.com':
            print("   ✅ 发送邮箱配置正确")
        else:
            print(f"   ❌ 发送邮箱配置错误: 期望 firfunneral_h@126.com，实际 {username}")
            
        # 检查收件人
        if 'firfunneral_h@126.com' in primary_recipients:
            print("   ✅ 收件人配置正确")
        else:
            print(f"   ❌ 收件人配置错误: 期望包含 firfunneral_h@126.com，实际 {primary_recipients}")
            
        # 检查服务商
        if provider == '163':
            print("   ✅ 邮件服务商配置正确 (163)")
        else:
            print(f"   ⚠️ 邮件服务商: {provider} (建议使用163匹配126邮箱)")
            
        # 检查密码
        if password == 'your_smtp_authorization_code':
            print("   ⚠️ SMTP授权码未设置，需要配置163邮箱的授权码")
        else:
            print("   ✅ SMTP授权码已设置")
            
        print(f"\n📋 总结:")
        config_issues = []
        
        if username != 'firfunneral_h@126.com':
            config_issues.append("发送邮箱不正确")
        if 'firfunneral_h@126.com' not in primary_recipients:
            config_issues.append("收件人不正确")
        if password == 'your_smtp_authorization_code':
            config_issues.append("需要设置SMTP授权码")
            
        if not config_issues:
            print("   🎉 邮件配置完全正确！")
            return True
        else:
            print(f"   ❌ 发现 {len(config_issues)} 个问题:")
            for issue in config_issues:
                print(f"      - {issue}")
            return False
            
    except Exception as e:
        print(f"❌ 配置文件读取失败: {e}")
        return False

if __name__ == '__main__':
    success = check_email_config()
    
    if not success:
        print(f"\n💡 修复建议:")
        print(f"   1. 确保发送邮箱为: firfunneral_h@126.com")
        print(f"   2. 确保收件人包含: firfunneral_h@126.com")
        print(f"   3. 获取163邮箱的SMTP授权码并配置到password字段")
        print(f"   4. 确认服务商设置为163")