#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# 添加src路径
sys.path.append('src')

print("🔍 邮件模板路径检查")
print("=" * 40)

# 检查当前工作目录
print(f"当前工作目录: {os.getcwd()}")

# 检查相对路径
relative_path = "templates/email_template.html"
print(f"相对路径: {relative_path}")
print(f"相对路径存在: {'是' if os.path.exists(relative_path) else '否'}")

# 检查绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
absolute_path = os.path.join(current_dir, "templates", "email_template.html")
print(f"绝对路径: {absolute_path}")
print(f"绝对路径存在: {'是' if os.path.exists(absolute_path) else '否'}")

# 测试EmailSender的路径
try:
    from email_sender import EmailSender
    sender = EmailSender()
    print(f"EmailSender模板路径: {sender.template_path}")
    print(f"EmailSender模板存在: {'是' if os.path.exists(sender.template_path) else '否'}")
    
    # 尝试加载模板
    template = sender._load_email_template()
    print(f"✅ 模板加载成功，长度: {len(template)} 字符")
    
except Exception as e:
    print(f"❌ EmailSender测试失败: {e}")

print("\n🧪 测试邮件内容生成...")
try:
    # 简单测试数据
    test_data = [{'fund_name': '测试基金', 'net_value': 1.0, 'change_rate': 1.0, 
                  'change_amount': 0.01, 'update_time': '15:00:00', 'is_alert': False}]
    
    content = sender._generate_email_content(test_data)
    print(f"✅ 邮件内容生成成功，长度: {len(content)} 字符")
    print("🎉 邮件生成问题已修复！")
    
except Exception as e:
    print(f"❌ 邮件内容生成失败: {e}")
    import traceback
    traceback.print_exc()