#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金监控系统测试套件
运行所有模块的测试
"""

import sys
import os
import unittest
from datetime import datetime

# 添加测试路径
sys.path.insert(0, os.path.dirname(__file__))

# 导入各个测试模块
try:
    from test_crawler import run_crawler_tests
    from test_email import run_email_tests
    from test_processor import run_processor_tests
    from test_integration import run_integration_tests
except ImportError as e:
    print(f"导入测试模块失败: {e}")
    sys.exit(1)


def run_all_tests():
    """运行所有测试"""
    print("🚀 基金监控系统测试套件")
    print("=" * 80)
    print(f"测试开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    test_results = []
    
    # 运行各模块测试
    test_modules = [
        ("数据爬取模块", run_crawler_tests),
        ("邮件发送模块", run_email_tests),
        ("数据处理模块", run_processor_tests),
        ("主程序集成", run_integration_tests),
    ]
    
    for module_name, test_function in test_modules:
        print(f"\n📋 正在测试: {module_name}")
        print("-" * 60)
        
        try:
            success = test_function()
            test_results.append((module_name, success))
            
            if success:
                print(f"✅ {module_name} 测试通过")
            else:
                print(f"❌ {module_name} 测试失败")
                
        except Exception as e:
            print(f"💥 {module_name} 测试异常: {str(e)}")
            test_results.append((module_name, False))
    
    # 输出总结
    print("\n" + "=" * 80)
    print("📊 测试结果总结")
    print("=" * 80)
    
    passed_count = 0
    failed_count = 0
    
    for module_name, success in test_results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {module_name:<20} {status}")
        
        if success:
            passed_count += 1
        else:
            failed_count += 1
    
    print("-" * 80)
    print(f"总测试模块数: {len(test_results)}")
    print(f"通过模块数:   {passed_count}")
    print(f"失败模块数:   {failed_count}")
    
    # 总体结果
    overall_success = failed_count == 0
    
    if overall_success:
        print("🎉 所有测试模块通过！")
    else:
        print("⚠️  部分测试模块失败，请检查具体错误信息")
    
    print(f"\n测试结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    return overall_success


def run_specific_test(test_name):
    """运行特定测试"""
    test_mapping = {
        'crawler': ('数据爬取模块', run_crawler_tests),
        'email': ('邮件发送模块', run_email_tests),
        'processor': ('数据处理模块', run_processor_tests),
        'integration': ('主程序集成', run_integration_tests),
    }
    
    if test_name not in test_mapping:
        print(f"未知的测试模块: {test_name}")
        print(f"可用的测试模块: {', '.join(test_mapping.keys())}")
        return False
    
    module_name, test_function = test_mapping[test_name]
    
    print(f"🔍 运行特定测试: {module_name}")
    print("=" * 60)
    
    try:
        success = test_function()
        
        if success:
            print(f"✅ {module_name} 测试通过")
        else:
            print(f"❌ {module_name} 测试失败")
        
        return success
        
    except Exception as e:
        print(f"💥 {module_name} 测试异常: {str(e)}")
        return False


def check_test_environment():
    """检查测试环境"""
    print("🔧 检查测试环境...")
    
    issues = []
    
    # 检查Python版本
    if sys.version_info < (3, 6):
        issues.append("Python版本过低，建议使用Python 3.6+")
    
    # 检查必要的模块
    required_modules = ['unittest', 'configparser', 'json', 'datetime']
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            issues.append(f"缺少必要模块: {module}")
    
    # 检查项目结构
    project_dirs = ['../src', '../config', '../templates']
    for dir_path in project_dirs:
        full_path = os.path.join(os.path.dirname(__file__), dir_path)
        if not os.path.exists(full_path):
            issues.append(f"项目目录不存在: {dir_path}")
    
    if issues:
        print("⚠️  发现以下问题:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ 测试环境检查通过")
        return True


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='基金监控系统测试套件')
    parser.add_argument('--module', '-m', 
                       choices=['crawler', 'email', 'processor', 'integration'],
                       help='运行特定模块的测试')
    parser.add_argument('--check-env', action='store_true',
                       help='检查测试环境')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='详细输出')
    
    args = parser.parse_args()
    
    # 检查测试环境
    if args.check_env:
        success = check_test_environment()
        return 0 if success else 1
    
    # 设置详细输出
    if args.verbose:
        os.environ['PYTHONPATH'] = os.path.join(os.path.dirname(__file__), '..')
    
    try:
        if args.module:
            # 运行特定测试
            success = run_specific_test(args.module)
        else:
            # 运行所有测试
            success = run_all_tests()
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n\n⛔ 测试被用户中断")
        return 130
    except Exception as e:
        print(f"\n\n💥 测试运行异常: {str(e)}")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)