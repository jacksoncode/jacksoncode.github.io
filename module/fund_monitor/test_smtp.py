#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SMTP连接测试脚本
用于独立测试邮箱配置是否正确
"""

import smtplib
import ssl
import configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_smtp_connection():
    """测试SMTP连接"""
    print("🔧 开始测试SMTP连接...")
    
    # 读取配置
    config = configparser.ConfigParser()
    config.read('config/email_config.ini', encoding='utf-8')
    
    provider = config.get('SMTP', 'provider')
    username = config.get('SMTP', 'username')
    password = config.get('SMTP', 'password')
    enable_tls = config.getboolean('SMTP', 'enable_tls', fallback=True)
    enable_ssl = config.getboolean('SMTP', 'enable_ssl', fallback=False)
    
    print(f"📧 邮箱服务商: {provider}")
    print(f"📧 发送邮箱: {username}")
    print(f"🔐 TLS加密: {enable_tls}")
    print(f"🔐 SSL加密: {enable_ssl}")
    
    # 获取SMTP配置
    if provider == '126':
        host = config.get('SMTP_SERVERS', '126_host', fallback='smtp.126.com')
        port = config.getint('SMTP_SERVERS', '126_port', fallback=25)
        ssl_port = config.getint('SMTP_SERVERS', '126_ssl_port', fallback=465)
    elif provider == '163':
        host = config.get('SMTP_SERVERS', '163_host', fallback='smtp.163.com')
        port = config.getint('SMTP_SERVERS', '163_port', fallback=25)
        ssl_port = config.getint('SMTP_SERVERS', '163_ssl_port', fallback=465)
    else:
        print(f"❌ 不支持的邮件服务商: {provider}")
        return False
    
    # 选择正确的端口
    actual_port = ssl_port if enable_ssl else port
    
    print(f"🌐 SMTP服务器: {host}")
    print(f"🔌 连接端口: {actual_port}")
    
    try:
        if enable_ssl:
            print("🔐 使用SSL连接...")
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL(host, actual_port, context=context)
        else:
            print("🔗 使用普通连接...")
            server = smtplib.SMTP(host, actual_port)
            
            if enable_tls:
                print("🔐 启用TLS加密...")
                server.starttls()
        
        print("🔑 尝试登录...")
        server.login(username, password)
        
        print("✅ SMTP连接成功！")
        
        # 发送测试邮件
        print("📨 发送测试邮件...")
        
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = username  # 发送给自己
        msg['Subject'] = "SMTP测试邮件"
        
        body = """
        这是一封SMTP连接测试邮件。
        
        如果您收到这封邮件，说明SMTP配置正确！
        
        发送时间：{datetime}
        """.format(datetime=__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        server.send_message(msg)
        server.quit()
        
        print("✅ 测试邮件发送成功！")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ 认证失败: {e}")
        print("💡 请检查：")
        print("   1. 邮箱地址是否正确")
        print("   2. 授权码是否正确（不是邮箱登录密码）")
        print("   3. 是否已开启SMTP服务")
        return False
        
    except smtplib.SMTPConnectError as e:
        print(f"❌ 连接失败: {e}")
        print("💡 请检查：")
        print("   1. 网络连接是否正常")
        print("   2. SMTP服务器地址和端口是否正确")
        return False
        
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def show_help():
    """显示帮助信息"""
    print("\n📖 126邮箱SMTP配置帮助：")
    print("1. 登录126邮箱网页版")
    print("2. 进入 设置 -> POP3/SMTP/IMAP")
    print("3. 开启SMTP服务")
    print("4. 生成授权码（不是邮箱密码）")
    print("5. 在配置文件中使用授权码作为password")
    print("\n🔧 推荐配置：")
    print("   host: smtp.126.com")
    print("   port: 465 (SSL) 或 25 (TLS)")
    print("   enable_ssl: true （推荐）")
    print("   enable_tls: false")

if __name__ == "__main__":
    success = test_smtp_connection()
    
    if not success:
        show_help()