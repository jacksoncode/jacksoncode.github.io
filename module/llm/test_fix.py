#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek和硅基流动平台问题修复测试脚本
"""

import sys
import os
import json
from datetime import datetime

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from get_bill import *
except ImportError as e:
    print(f"导入失败: {e}")
    print("请确保已安装requests库: pip install requests")
    sys.exit(1)


def test_deepseek_platform():
    """测试DeepSeek平台修复"""
    print("=== 测试DeepSeek平台 ===")
    
    # 从配置文件读取API密钥
    config_manager = ConfigManager("ai_billing_config.ini")
    deepseek_config = config_manager.get_platform_config('deepseek')
    
    if not deepseek_config.get('api_key') or deepseek_config.get('enabled') != 'true':
        print("❌ DeepSeek平台未配置或未启用")
        return False
    
    try:
        platform = DeepSeekPlatform(
            api_key=deepseek_config['api_key'],
            base_url=deepseek_config.get('base_url', 'https://api.deepseek.com')
        )
        
        print(f"✓ 创建DeepSeek平台实例成功")
        print(f"  API Key: {deepseek_config['api_key'][:10]}...")
        print(f"  Base URL: {deepseek_config.get('base_url')}")
        
        # 测试账单查询
        billing_info = platform.get_billing_info()
        
        print(f"✓ DeepSeek账单查询成功")
        print(f"  平台: {billing_info.platform}")
        print(f"  余额: {billing_info.balance} {billing_info.currency}")
        print(f"  已使用: {billing_info.used_amount} {billing_info.currency}")
        print(f"  总额度: {billing_info.total_quota} {billing_info.currency}")
        print(f"  更新时间: {billing_info.last_update}")
        
        # 检查是否有错误
        if billing_info.usage_details and 'error' in billing_info.usage_details:
            print(f"⚠️  包含错误信息: {billing_info.usage_details['error']}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ DeepSeek测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_siliconflow_platform():
    """测试硅基流动平台修复"""
    print("\n=== 测试硅基流动平台 ===")
    
    # 从配置文件读取API密钥
    config_manager = ConfigManager("ai_billing_config.ini")
    siliconflow_config = config_manager.get_platform_config('siliconflow')
    
    if not siliconflow_config.get('api_key') or siliconflow_config.get('enabled') != 'true':
        print("❌ 硅基流动平台未配置或未启用")
        return False
    
    try:
        platform = SiliconFlowPlatform(
            api_key=siliconflow_config['api_key'],
            base_url=siliconflow_config.get('base_url', 'https://api.siliconflow.cn')
        )
        
        print(f"✓ 创建硅基流动平台实例成功")
        print(f"  API Key: {siliconflow_config['api_key'][:10]}...")
        print(f"  Base URL: {siliconflow_config.get('base_url')}")
        
        # 测试账单查询
        billing_info = platform.get_billing_info()
        
        print(f"✓ 硅基流动账单查询成功")
        print(f"  平台: {billing_info.platform}")
        print(f"  余额: {billing_info.balance} {billing_info.currency}")
        print(f"  已使用: {billing_info.used_amount} {billing_info.currency}")
        print(f"  总额度: {billing_info.total_quota} {billing_info.currency}")
        print(f"  更新时间: {billing_info.last_update}")
        
        # 检查是否有错误
        if billing_info.usage_details and 'error' in billing_info.usage_details:
            print(f"⚠️  包含错误信息: {billing_info.usage_details['error']}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 硅基流动测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_both_platforms():
    """测试两个平台的完整集成"""
    print("\n=== 完整集成测试 ===")
    
    try:
        # 创建账单管理器
        billing_manager = create_billing_manager_from_config()
        
        # 获取所有账单信息
        all_billing = billing_manager.get_all_billing_info()
        
        success_count = 0
        total_count = len(all_billing)
        
        print(f"✓ 成功查询 {total_count} 个平台的账单信息")
        
        for platform_name, billing_info in all_billing.items():
            has_error = billing_info.usage_details and 'error' in billing_info.usage_details
            status = "❌" if has_error else "✓"
            print(f"  {status} {platform_name}: {billing_info.balance} {billing_info.currency}")
            
            if not has_error:
                success_count += 1
        
        print(f"\n统计: {success_count}/{total_count} 平台查询成功")
        
        # 生成报告
        reporter = BillingReporter(billing_manager)
        summary = reporter.generate_summary()
        
        print(f"\n=== 汇总信息 ===")
        print(f"成功查询: {summary['成功查询']}")
        print(f"查询失败: {summary['查询失败']}")
        print(f"总余额: {summary['总余额']}")
        
        return success_count > 0
        
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")
        return False


def main():
    """主函数"""
    print("DeepSeek和硅基流动平台问题修复测试")
    print("=" * 50)
    
    # 检查配置文件
    if not os.path.exists("ai_billing_config.ini"):
        print("❌ 配置文件 ai_billing_config.ini 不存在")
        print("请先运行: python3 get_bill.py --init")
        return False
    
    success_tests = 0
    total_tests = 3
    
    # 单独测试每个平台
    if test_deepseek_platform():
        success_tests += 1
    
    if test_siliconflow_platform():
        success_tests += 1
    
    # 集成测试
    if test_both_platforms():
        success_tests += 1
    
    print("\n" + "=" * 50)
    print(f"测试完成: {success_tests}/{total_tests} 项测试通过")
    
    if success_tests == total_tests:
        print("🎉 所有测试通过！修复成功！")
        return True
    else:
        print("⚠️  部分测试失败，请检查错误信息")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)