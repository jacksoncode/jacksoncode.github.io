#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI平台账单查询系统 - 真实API调测脚本
使用配置文件中的真实API密钥进行连接测试和base_url验证
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
import time
import requests
from datetime import datetime
from get_bill import (
    ConfigManager, BillingManager, PlatformType, 
    DeepSeekPlatform, KimiPlatform, DoubaoHuoshanPlatform,
    ZhipuPlatform, AliyunBailianPlatform, OpenAIPlatform,
    SiliconFlowPlatform
)


class APITester:
    """API连接测试器"""
    
    def __init__(self, config_file="ai_billing_config.ini"):
        self.config_manager = ConfigManager(config_file)
        self.test_results = {}
        self.start_time = datetime.now()
    
    def test_platform_connectivity(self, platform_name, platform_class, config):
        """测试单个平台的连接性"""
        print(f"\n{'='*60}")
        print(f"测试平台: {platform_name}")
        print(f"Base URL: {config.get('base_url', 'N/A')}")
        print(f"API Key: {config.get('api_key', 'N/A')[:20]}...")
        print(f"{'='*60}")
        
        result = {
            "platform": platform_name,
            "base_url": config.get('base_url', ''),
            "api_key_prefix": config.get('api_key', '')[:20] if config.get('api_key') else '',
            "test_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "connection_test": False,
            "billing_data": None,
            "error_message": None,
            "response_time": 0,
            "recommendations": []
        }
        
        try:
            # 记录开始时间
            test_start = time.time()
            
            # 创建平台实例
            platform = platform_class(**config)
            
            # 尝试获取账单信息
            print("正在测试API连接...")
            billing_info = platform.get_billing_info()
            
            # 记录响应时间
            result["response_time"] = round(time.time() - test_start, 2)
            
            # 检查是否成功获取数据
            if billing_info and not (billing_info.usage_details and 'error' in billing_info.usage_details):
                result["connection_test"] = True
                result["billing_data"] = billing_info.to_dict()
                
                print(f"✅ 连接成功! (响应时间: {result['response_time']}秒)")
                print(f"   余额: {billing_info.balance} {billing_info.currency}")
                print(f"   已使用: {billing_info.used_amount} {billing_info.currency}")
                print(f"   总额度: {billing_info.total_quota} {billing_info.currency}")
                
                if billing_info.balance > 0:
                    result["recommendations"].append("账户有余额，可正常使用")
                else:
                    result["recommendations"].append("账户余额为0，请及时充值")
                    
            else:
                error_msg = "连接失败"
                if billing_info and billing_info.usage_details and 'error' in billing_info.usage_details:
                    error_msg = billing_info.usage_details['error']
                
                result["error_message"] = error_msg
                print(f"❌ 连接失败: {error_msg}")
                
                # 分析错误并给出建议
                self._analyze_error_and_suggest(result, error_msg)
                
        except Exception as e:
            result["response_time"] = round(time.time() - test_start, 2)
            result["error_message"] = str(e)
            print(f"❌ 测试异常: {e}")
            
            # 分析错误并给出建议
            self._analyze_error_and_suggest(result, str(e))
        
        return result
    
    def _analyze_error_and_suggest(self, result, error_msg):
        """分析错误信息并给出建议"""
        error_lower = error_msg.lower()
        
        if "404" in error_msg or "not found" in error_lower:
            result["recommendations"].extend([
                "API端点可能已变更，请检查官方文档",
                "建议联系平台技术支持确认最新API地址"
            ])
        elif "401" in error_msg or "unauthorized" in error_lower:
            result["recommendations"].extend([
                "API密钥可能无效或过期",
                "请检查API密钥格式是否正确",
                "建议重新生成API密钥"
            ])
        elif "403" in error_msg or "forbidden" in error_lower:
            result["recommendations"].extend([
                "API密钥权限不足",
                "请检查密钥是否有账单查询权限"
            ])
        elif "timeout" in error_lower or "连接超时" in error_msg:
            result["recommendations"].extend([
                "网络连接超时，请检查网络状况",
                "可能是服务器负载过高，建议稍后重试"
            ])
        elif "ssl" in error_lower or "certificate" in error_lower:
            result["recommendations"].extend([
                "SSL证书问题，请检查系统时间是否正确",
                "可能需要更新CA证书包"
            ])
        else:
            result["recommendations"].extend([
                "请检查网络连接",
                "确认API密钥和base_url配置正确",
                "查看平台官方文档是否有API变更"
            ])
    
    def test_all_enabled_platforms(self):
        """测试所有启用的平台"""
        print("AI平台账单查询系统 - 真实API连接测试")
        print(f"测试开始时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # 平台映射
        platform_mapping = {
            'deepseek': DeepSeekPlatform,
            'kimi': KimiPlatform,
            'doubao': DoubaoHuoshanPlatform,
            'zhipu': ZhipuPlatform,
            'aliyun_bailian': AliyunBailianPlatform,
            'openai': OpenAIPlatform,
            'siliconflow': SiliconFlowPlatform
        }
        
        enabled_platforms = []
        
        # 检查所有启用的平台
        for platform_name in platform_mapping.keys():
            config = self.config_manager.get_platform_config(platform_name)
            if config and config.get('enabled', '').lower() == 'true' and config.get('api_key'):
                enabled_platforms.append((platform_name, platform_mapping[platform_name], config))
        
        if not enabled_platforms:
            print("❌ 没有找到启用的平台配置")
            print("请检查 ai_billing_config.ini 文件中的配置")
            return
        
        print(f"发现 {len(enabled_platforms)} 个启用的平台:")
        for platform_name, _, config in enabled_platforms:
            print(f"  - {platform_name}: {config.get('base_url', 'N/A')}")
        
        # 逐个测试平台
        successful_tests = 0
        total_tests = len(enabled_platforms)
        
        for platform_name, platform_class, config in enabled_platforms:
            result = self.test_platform_connectivity(platform_name, platform_class, config)
            self.test_results[platform_name] = result
            
            if result["connection_test"]:
                successful_tests += 1
            
            # 在测试之间稍作停顿，避免频率限制
            time.sleep(1)
        
        # 生成测试报告
        self._generate_test_report(successful_tests, total_tests)
    
    def _generate_test_report(self, successful_tests, total_tests):
        """生成测试报告"""
        end_time = datetime.now()
        total_duration = (end_time - self.start_time).total_seconds()
        
        print(f"\n{'='*80}")
        print("测试完成 - 汇总报告")
        print(f"{'='*80}")
        print(f"测试时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')} - {end_time.strftime('%H:%M:%S')}")
        print(f"测试耗时: {total_duration:.2f} 秒")
        print(f"测试结果: {successful_tests}/{total_tests} 平台连接成功")
        
        # 成功的平台
        if successful_tests > 0:
            print(f"\n✅ 连接成功的平台 ({successful_tests}个):")
            for platform_name, result in self.test_results.items():
                if result["connection_test"]:
                    billing = result["billing_data"]
                    print(f"  - {platform_name}:")
                    print(f"    Base URL: {result['base_url']}")
                    print(f"    余额: {billing['balance']} {billing['currency']}")
                    print(f"    响应时间: {result['response_time']}秒")
        
        # 失败的平台
        failed_tests = total_tests - successful_tests
        if failed_tests > 0:
            print(f"\n❌ 连接失败的平台 ({failed_tests}个):")
            for platform_name, result in self.test_results.items():
                if not result["connection_test"]:
                    print(f"  - {platform_name}:")
                    print(f"    Base URL: {result['base_url']}")
                    print(f"    错误: {result['error_message']}")
                    print(f"    建议: {'; '.join(result['recommendations'])}")
        
        # base_url验证总结
        print(f"\n📋 Base URL验证总结:")
        for platform_name, result in self.test_results.items():
            status = "✅ 正确" if result["connection_test"] else "❌ 需要检查"
            print(f"  - {platform_name}: {result['base_url']} - {status}")
        
        # 保存详细报告
        self._save_detailed_report()
    
    def _save_detailed_report(self):
        """保存详细的测试报告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"api_test_report_{timestamp}.json"
        
        report_data = {
            "test_summary": {
                "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_platforms": len(self.test_results),
                "successful_connections": sum(1 for r in self.test_results.values() if r["connection_test"]),
                "failed_connections": sum(1 for r in self.test_results.values() if not r["connection_test"])
            },
            "platform_results": self.test_results,
            "recommendations": self._generate_overall_recommendations()
        }
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n📄 详细测试报告已保存: {report_file}")
        except Exception as e:
            print(f"\n⚠️  保存报告失败: {e}")
    
    def _generate_overall_recommendations(self):
        """生成总体建议"""
        recommendations = []
        
        successful_count = sum(1 for r in self.test_results.values() if r["connection_test"])
        total_count = len(self.test_results)
        
        if successful_count == total_count:
            recommendations.append("所有平台连接正常，base_url配置正确")
            recommendations.append("建议定期检查账户余额")
        elif successful_count > total_count // 2:
            recommendations.append("大部分平台连接正常")
            recommendations.append("请重点检查失败平台的API密钥和base_url")
        else:
            recommendations.append("多数平台连接失败，请检查:")
            recommendations.append("1. 网络连接是否正常")
            recommendations.append("2. API密钥是否正确和有效")
            recommendations.append("3. base_url是否为最新地址")
        
        # 检查是否有404错误
        has_404_errors = any("404" in (r.get("error_message") or "") for r in self.test_results.values())
        if has_404_errors:
            recommendations.append("检测到404错误，强烈建议:")
            recommendations.append("- 查阅各平台最新API文档")
            recommendations.append("- 联系平台技术支持确认API地址")
        
        return recommendations


def main():
    """主函数"""
    try:
        # 创建API测试器
        tester = APITester()
        
        # 执行测试
        tester.test_all_enabled_platforms()
        
        print(f"\n🔍 测试完成！")
        print("如需查看更详细的信息，请检查生成的JSON报告文件。")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()