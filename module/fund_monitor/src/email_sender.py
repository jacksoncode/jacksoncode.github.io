#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件发送模块
支持多种SMTP服务商，发送HTML格式的基金监控报告
"""

import smtplib
import ssl
import logging
import configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import os
import time


class EmailSender:
    """邮件发送器"""
    
    def __init__(self, config_file: str = "config/email_config.ini"):
        """
        初始化邮件发送器
        
        Args:
            config_file: 邮件配置文件路径
        """
        self.config = configparser.ConfigParser()
        self.config.read(config_file, encoding='utf-8')
        
        # 配置日志
        self._setup_logging()
        
        # SMTP配置
        self.smtp_configs = self._load_smtp_configs()
        
        # 获取当前邮箱配置
        self.provider = self.config.get('SMTP', 'provider', fallback='qq')
        self.username = self.config.get('SMTP', 'username', fallback='')
        self.password = self.config.get('SMTP', 'password', fallback='')
        self.from_name = self.config.get('SMTP', 'from_name', fallback='基金监控系统')
        
        # 邮件设置
        self.enable_tls = self.config.getboolean('SMTP', 'enable_tls', fallback=True)
        self.enable_ssl = self.config.getboolean('SMTP', 'enable_ssl', fallback=False)
        self.retry_count = self.config.getint('EMAIL_SETTINGS', 'retry_count', fallback=3)
        self.retry_interval = self.config.getint('EMAIL_SETTINGS', 'retry_interval', fallback=5)
        
        # 收件人配置
        self.primary_recipients = self._parse_recipients('primary')
        self.secondary_recipients = self._parse_recipients('secondary')
        self.bcc_recipients = self._parse_recipients('bcc')
        
        # 邮件内容配置
        self.subject_template = self.config.get('EMAIL_SETTINGS', 'subject_template', 
                                               fallback='【基金监控】{date} 基金涨跌报告')
        self.enable_html = self.config.getboolean('EMAIL_SETTINGS', 'enable_html', fallback=True)
        self.charset = self.config.get('EMAIL_SETTINGS', 'charset', fallback='utf-8')
        
        # 邮件模板路径
        import os
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.template_path = os.path.join(current_dir, "templates", "email_template.html")
        
        self.logger.info("邮件发送器初始化完成")
    
    def _setup_logging(self):
        """设置日志配置"""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def _load_smtp_configs(self) -> Dict[str, Dict[str, Any]]:
        """加载SMTP服务器配置"""
        configs = {
            'qq': {
                'host': self.config.get('SMTP_SERVERS', 'qq_host', fallback='smtp.qq.com'),
                'port': self.config.getint('SMTP_SERVERS', 'qq_port', fallback=587),
                'ssl_port': self.config.getint('SMTP_SERVERS', 'qq_ssl_port', fallback=465)
            },
            '163': {
                'host': self.config.get('SMTP_SERVERS', '163_host', fallback='smtp.163.com'),
                'port': self.config.getint('SMTP_SERVERS', '163_port', fallback=25),
                'ssl_port': self.config.getint('SMTP_SERVERS', '163_ssl_port', fallback=465)
            },
            '126': {
                'host': self.config.get('SMTP_SERVERS', '126_host', fallback='smtp.126.com'),
                'port': self.config.getint('SMTP_SERVERS', '126_port', fallback=25),
                'ssl_port': self.config.getint('SMTP_SERVERS', '126_ssl_port', fallback=465)
            },
            'gmail': {
                'host': self.config.get('SMTP_SERVERS', 'gmail_host', fallback='smtp.gmail.com'),
                'port': self.config.getint('SMTP_SERVERS', 'gmail_port', fallback=587),
                'ssl_port': self.config.getint('SMTP_SERVERS', 'gmail_ssl_port', fallback=465)
            },
            'outlook': {
                'host': self.config.get('SMTP_SERVERS', 'outlook_host', fallback='smtp-mail.outlook.com'),
                'port': self.config.getint('SMTP_SERVERS', 'outlook_port', fallback=587),
                'ssl_port': self.config.getint('SMTP_SERVERS', 'outlook_ssl_port', fallback=465)
            }
        }
        return configs
    
    def _parse_recipients(self, recipient_type: str) -> List[str]:
        """解析收件人列表"""
        recipients_str = self.config.get('RECIPIENTS', recipient_type, fallback='')
        if not recipients_str:
            return []
        
        return [email.strip() for email in recipients_str.split(',') if email.strip()]
    
    def _get_smtp_config(self) -> Dict[str, Any]:
        """获取当前SMTP配置"""
        if self.provider not in self.smtp_configs:
            raise ValueError(f"不支持的邮件服务商: {self.provider}")
        
        config = self.smtp_configs[self.provider].copy()
        
        # 根据SSL/TLS设置选择端口
        if self.enable_ssl:
            config['port'] = config['ssl_port']
        
        return config
    
    def _create_smtp_connection(self) -> smtplib.SMTP:
        """创建SMTP连接"""
        smtp_config = self._get_smtp_config()
        
        try:
            if self.enable_ssl:
                # SSL连接
                context = ssl.create_default_context()
                server = smtplib.SMTP_SSL(str(smtp_config['host']), int(smtp_config['port']), context=context)
            else:
                # 普通连接
                server = smtplib.SMTP(str(smtp_config['host']), int(smtp_config['port']))
                
                if self.enable_tls:
                    # 启用TLS
                    server.starttls()
            
            # 登录
            server.login(self.username, self.password)
            
            self.logger.info(f"SMTP连接成功 - {self.provider}:{smtp_config['host']}:{smtp_config['port']}")
            return server
            
        except Exception as e:
            self.logger.error(f"SMTP连接失败: {str(e)}")
            raise
    
    def _load_email_template(self) -> str:
        """加载邮件模板"""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            self.logger.warning(f"邮件模板文件未找到: {self.template_path}")
            return self._get_default_template()
        except Exception as e:
            self.logger.error(f"加载邮件模板失败: {str(e)}")
            return self._get_default_template()
    
    def _get_default_template(self) -> str:
        """获取默认邮件模板"""
        return '''
        <html>
        <body>
        <h2>📊 基金监控日报 - {report_date}</h2>
        
        <h3>📈 监控汇总</h3>
        <p>总监控基金数: {total_funds}</p>
        <p>上涨基金数: {rise_count}</p>
        <p>下跌基金数: {fall_count}</p>
        <p>预警基金数: {alert_count}</p>
        
        <h3>📋 详细数据</h3>
        {fund_rows}
        
        <p><small>{data_source_note} | 报告时间: {report_time}</small></p>
        <p><small>{disclaimer}</small></p>
        <p><small>{signature}</small></p>
        </body>
        </html>
        '''
    
    def _generate_fund_table_rows(self, funds_data: List[Dict[str, Any]]) -> str:
        """生成基金数据表格行"""
        if not funds_data:
            return '<tr><td colspan="6">暂无基金数据</td></tr>'
        
        rows = []
        for fund in funds_data:
            # 判断是否为预警基金
            is_alert = fund.get('is_alert', False)
            row_class = 'alert-row' if is_alert else ''
            
            # 格式化涨跌幅
            change_rate = fund.get('change_rate', 0)
            change_rate_str = f"{change_rate:+.2f}%"
            change_rate_class = 'rise' if change_rate > 0 else 'fall' if change_rate < 0 else 'neutral'
            
            # 格式化涨跌额
            change_amount = fund.get('change_amount', 0)
            change_amount_str = f"{change_amount:+.4f}"
            
            # 状态显示
            status = '⚠️预警' if is_alert else '正常'
            status_class = 'status-alert' if is_alert else 'status-normal'
            
            row = '''
            <tr class="{row_class}">
                <td>{fund_name}</td>
                <td>{net_value:.4f}</td>
                <td class="{change_rate_class}">{change_rate_str}</td>
                <td class="{change_rate_class}">{change_amount_str}</td>
                <td>{update_time}</td>
                <td class="{status_class}">{status}</td>
            </tr>
            '''.format(
                row_class=row_class,
                fund_name=fund.get('fund_name', 'N/A'),
                net_value=fund.get('net_value', 0),
                change_rate_class=change_rate_class,
                change_rate_str=change_rate_str,
                change_amount_str=change_amount_str,
                update_time=fund.get('update_time', 'N/A'),
                status_class=status_class,
                status=status
            )
            rows.append(row)
        
        return ''.join(rows)
    
    def _generate_email_content(self, funds_data: List[Dict[str, Any]]) -> str:
        """生成邮件内容"""
        # 计算统计数据
        total_funds = len(funds_data)
        rise_count = sum(1 for fund in funds_data if fund.get('change_rate', 0) > 0)
        fall_count = sum(1 for fund in funds_data if fund.get('change_rate', 0) < 0)
        alert_count = sum(1 for fund in funds_data if fund.get('is_alert', False))
        
        # 生成表格行
        fund_rows = self._generate_fund_table_rows(funds_data)
        
        # 获取邮件内容配置
        signature = self.config.get('EMAIL_CONTENT', 'signature', 
                                   fallback='此邮件由基金监控系统自动发送，请勿回复。')
        disclaimer = self.config.get('EMAIL_CONTENT', 'disclaimer',
                                    fallback='基金投资有风险，投资需谨慎。本系统仅提供数据监控服务，不构成投资建议。')
        data_source_note = self.config.get('EMAIL_CONTENT', 'data_source_note',
                                          fallback='数据来源：天天基金网等第三方平台')
        
        # 加载模板并替换变量
        template = self._load_email_template()
        
        content = template.format(
            report_date=datetime.now().strftime('%Y年%m月%d日'),
            total_funds=total_funds,
            rise_count=rise_count,
            fall_count=fall_count,
            alert_count=alert_count,
            fund_rows=fund_rows,
            report_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            signature=signature,
            disclaimer=disclaimer,
            data_source_note=data_source_note
        )
        
        return content
    
    def _create_message(self, subject: str, content: str, recipients: List[str]) -> MIMEMultipart:
        """创建邮件消息"""
        msg = MIMEMultipart('alternative')
        
        # 设置邮件头
        msg['From'] = f'{self.from_name} <{self.username}>'
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = str(Header(subject, self.charset))
        
        # 添加抄送和密送
        if self.secondary_recipients:
            msg['Cc'] = ', '.join(self.secondary_recipients)
        
        # 添加邮件内容
        if self.enable_html:
            html_part = MIMEText(content, 'html', self.charset)
            msg.attach(html_part)
        else:
            # 如果不启用HTML，则创建纯文本版本
            text_content = self._html_to_text(content)
            text_part = MIMEText(text_content, 'plain', self.charset)
            msg.attach(text_part)
        
        return msg
    
    def _html_to_text(self, html_content: str) -> str:
        """将HTML内容转换为纯文本"""
        import re
        
        # 简单的HTML到文本转换
        text = re.sub(r'<[^>]+>', '', html_content)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def send_fund_report(self, funds_data: List[Dict[str, Any]], 
                        custom_subject: Optional[str] = None) -> bool:
        """
        发送基金监控报告
        
        Args:
            funds_data: 基金数据列表
            custom_subject: 自定义邮件主题
            
        Returns:
            发送是否成功
        """
        if not self.primary_recipients:
            self.logger.error("未配置收件人")
            return False
        
        # 检查是否仅在预警时发送
        alert_only = self.config.getboolean('EMAIL_SETTINGS', 'alert_only', fallback=False)
        if alert_only:
            has_alert = any(fund.get('is_alert', False) for fund in funds_data)
            if not has_alert:
                self.logger.info("未检测到预警基金，跳过邮件发送")
                return True
        
        # 生成邮件主题
        if custom_subject:
            subject = custom_subject
        else:
            subject = self.subject_template.format(
                date=datetime.now().strftime('%Y-%m-%d')
            )
        
        # 生成邮件内容
        content = self._generate_email_content(funds_data)
        
        # 合并所有收件人
        all_recipients = self.primary_recipients + self.secondary_recipients + self.bcc_recipients
        
        # 尝试发送邮件
        for attempt in range(self.retry_count):
            try:
                with self._create_smtp_connection() as server:
                    msg = self._create_message(subject, content, self.primary_recipients)
                    
                    # 发送邮件
                    server.send_message(msg, to_addrs=all_recipients)
                    
                    self.logger.info(f"邮件发送成功到 {len(all_recipients)} 个收件人")
                    return True
                    
            except Exception as e:
                self.logger.error(f"第 {attempt + 1} 次邮件发送失败: {str(e)}")
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_interval)
                continue
        
        self.logger.error("邮件发送最终失败")
        return False
    
    def send_test_email(self) -> bool:
        """发送测试邮件"""
        test_data = [
            {
                'fund_code': '000001',
                'fund_name': '华夏成长混合',
                'net_value': 1.2340,
                'change_rate': 2.15,
                'change_amount': 0.026,
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'is_alert': False
            }
        ]
        
        subject = "【基金监控】测试邮件"
        return self.send_fund_report(test_data, subject)
    
    def validate_config(self) -> bool:
        """验证邮件配置"""
        errors = []
        
        # 检查必要配置
        if not self.username:
            errors.append("未配置发送邮箱用户名")
        
        if not self.password:
            errors.append("未配置SMTP密码")
        
        if not self.primary_recipients:
            errors.append("未配置收件人")
        
        if self.provider not in self.smtp_configs:
            errors.append(f"不支持的邮件服务商: {self.provider}")
        
        # 检查邮件模板文件
        if not os.path.exists(self.template_path):
            self.logger.warning(f"邮件模板文件不存在: {self.template_path}，将使用默认模板")
        
        if errors:
            for error in errors:
                self.logger.error(f"配置错误: {error}")
            return False
        
        self.logger.info("邮件配置验证通过")
        return True


if __name__ == "__main__":
    # 测试代码
    sender = EmailSender()
    
    # 验证配置
    if sender.validate_config():
        # 发送测试邮件
        print("发送测试邮件...")
        success = sender.send_test_email()
        print(f"测试邮件发送{'成功' if success else '失败'}")
    else:
        print("邮件配置验证失败，请检查配置文件")