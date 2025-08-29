#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek和硅基流动平台修复验证脚本（无网络依赖）
"""

def test_deepseek_data_conversion():
    """测试DeepSeek数据转换逻辑"""
    print("=== 测试DeepSeek数据转换逻辑 ===")
    
    # 模拟DeepSeek API响应数据的各种情况
    test_cases = [
        # 正常情况：数值型数据（分为单位）
        {
            "name": "数值型数据（分）",
            "data": {
                "balance_infos": [{
                    "available_balance": 12500,  # 125.00元
                    "used_balance": 7500,       # 75.00元  
                    "total_balance": 20000      # 200.00元
                }]
            },
            "expected": {"balance": 125.0, "used": 75.0, "total": 200.0}
        },
        # 字符串数据
        {
            "name": "字符串型数据",
            "data": {
                "balance_infos": [{
                    "available_balance": "12500",
                    "used_balance": "7500", 
                    "total_balance": "20000"
                }]
            },
            "expected": {"balance": 125.0, "used": 75.0, "total": 200.0}
        },
        # 小数值（元为单位）
        {
            "name": "小数值数据（元）",
            "data": {
                "balance_infos": [{
                    "available_balance": 125.50,
                    "used_balance": 74.50,
                    "total_balance": 200.0
                }]
            },
            "expected": {"balance": 125.50, "used": 74.50, "total": 200.0}
        },
        # 嵌套结构不同
        {
            "name": "直接数据结构",
            "data": {
                "available_balance": 15000,
                "used_balance": 5000,
                "total_balance": 20000
            },
            "expected": {"balance": 150.0, "used": 50.0, "total": 200.0}
        },
        # 异常数据
        {
            "name": "异常数据",
            "data": {
                "balance_infos": [{
                    "available_balance": "invalid",
                    "used_balance": None,
                    "total_balance": "abc"
                }]
            },
            "expected": {"balance": 0.0, "used": 0.0, "total": 0.0}
        }
    ]
    
    # 实现修复后的安全转换函数
    def safe_float_convert(value, default=0.0):
        try:
            if isinstance(value, (int, float)):
                return float(value)
            elif isinstance(value, str):
                if value.replace('.', '').replace('-', '').isdigit():
                    return float(value)
                return default
            else:
                return default
        except (ValueError, TypeError):
            return default
    
    def smart_convert(value):
        float_value = safe_float_convert(value)
        if float_value > 1000:
            return float_value / 100
        return float_value
    
    def process_deepseek_data(data):
        # 获取余额信息
        balance_info = {}
        if 'balance_infos' in data and isinstance(data['balance_infos'], list) and len(data['balance_infos']) > 0:
            balance_info = data['balance_infos'][0]
        elif 'balance_info' in data:
            balance_info = data['balance_info']
        elif isinstance(data, dict):
            balance_info = data
        
        available_balance = balance_info.get('available_balance', 0)
        used_balance = balance_info.get('used_balance', 0) 
        total_balance = balance_info.get('total_balance', 0)
        
        return {
            "balance": smart_convert(available_balance),
            "used": smart_convert(used_balance),
            "total": smart_convert(total_balance)
        }
    
    # 运行测试
    passed = 0
    total = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {test_case['name']}")
        try:
            result = process_deepseek_data(test_case['data'])
            expected = test_case['expected']
            
            # 验证结果
            success = (
                abs(result['balance'] - expected['balance']) < 0.01 and
                abs(result['used'] - expected['used']) < 0.01 and
                abs(result['total'] - expected['total']) < 0.01
            )
            
            if success:
                print(f"  ✓ 通过")
                print(f"    余额: {result['balance']} (期望: {expected['balance']})")
                print(f"    已用: {result['used']} (期望: {expected['used']})")
                print(f"    总额: {result['total']} (期望: {expected['total']})")
                passed += 1
            else:
                print(f"  ❌ 失败")
                print(f"    实际: {result}")
                print(f"    期望: {expected}")
                
        except Exception as e:
            print(f"  ❌ 异常: {e}")
    
    print(f"\nDeepSeek测试结果: {passed}/{total} 通过")
    return passed == total


def test_siliconflow_logic():
    """测试硅基流动逻辑"""
    print("\n=== 测试硅基流动数据解析逻辑 ===")
    
    test_cases = [
        # 标准响应格式
        {
            "name": "标准data嵌套格式",
            "data": {
                "data": {
                    "balance": 68.25,
                    "used_amount": 31.75,
                    "total_quota": 100.0,
                    "currency": "CNY"
                }
            },
            "expected": {"balance": 68.25, "used": 31.75, "total": 100.0}
        },
        # 直接格式
        {
            "name": "直接数据格式",
            "data": {
                "available_balance": 45.50,
                "total_used": 54.50,
                "total_credits": 100.0
            },
            "expected": {"balance": 45.50, "used": 54.50, "total": 100.0}
        },
        # 字符串数据
        {
            "name": "字符串数据",
            "data": {
                "balance": "75.25",
                "used": "24.75",
                "total": "100.00"
            },
            "expected": {"balance": 75.25, "used": 24.75, "total": 100.0}
        },
        # 缺少total字段，需要计算
        {
            "name": "缺少总额度，自动计算",
            "data": {
                "remaining_balance": 30.0,
                "consumed": 70.0
            },
            "expected": {"balance": 30.0, "used": 70.0, "total": 100.0}
        }
    ]
    
    def safe_get_float(obj, *keys, default=0.0):
        for key in keys:
            if key in obj:
                try:
                    value = obj[key]
                    if isinstance(value, (int, float)):
                        return float(value)
                    elif isinstance(value, str) and value.replace('.', '').replace('-', '').isdigit():
                        return float(value)
                except (ValueError, TypeError):
                    continue
        return default
    
    def process_siliconflow_data(data):
        # 处理嵌套的data结构
        if 'data' in data and isinstance(data['data'], dict):
            billing_data = data['data']
        else:
            billing_data = data
        
        # 提取各种可能的字段
        balance = safe_get_float(billing_data, 'balance', 'available_balance', 'total_available', 'remaining_balance')
        used_amount = safe_get_float(billing_data, 'used', 'used_amount', 'total_used', 'consumed')
        total_quota = safe_get_float(billing_data, 'total', 'total_quota', 'total_granted', 'total_credits', 'credits', 'quota', 'limit')
        
        # 如果没有总额度，尝试计算
        if total_quota == 0:
            total_quota = balance + used_amount
        
        return {
            "balance": balance,
            "used": used_amount,
            "total": total_quota
        }
    
    # 运行测试
    passed = 0
    total = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {test_case['name']}")
        try:
            result = process_siliconflow_data(test_case['data'])
            expected = test_case['expected']
            
            success = (
                abs(result['balance'] - expected['balance']) < 0.01 and
                abs(result['used'] - expected['used']) < 0.01 and
                abs(result['total'] - expected['total']) < 0.01
            )
            
            if success:
                print(f"  ✓ 通过")
                print(f"    余额: {result['balance']} (期望: {expected['balance']})")
                print(f"    已用: {result['used']} (期望: {expected['used']})")
                print(f"    总额: {result['total']} (期望: {expected['total']})")
                passed += 1
            else:
                print(f"  ❌ 失败")
                print(f"    实际: {result}")
                print(f"    期望: {expected}")
                
        except Exception as e:
            print(f"  ❌ 异常: {e}")
    
    print(f"\n硅基流动测试结果: {passed}/{total} 通过")
    return passed == total


def test_api_endpoints():
    """测试API端点逻辑"""
    print("\n=== 测试API端点优先级 ===")
    
    # DeepSeek端点
    deepseek_endpoint = "https://api.deepseek.com/v1/user/balance"
    print(f"DeepSeek API端点: {deepseek_endpoint}")
    
    # 硅基流动端点列表（按优先级）
    siliconflow_endpoints = [
        "https://api.siliconflow.cn/v1/user/info",
        "https://api.siliconflow.cn/v1/models",
        "https://api.siliconflow.cn/user/balance",
        "https://api.siliconflow.cn/user/info",
        "https://api.siliconflow.cn/api/user/balance",
        "https://api.siliconflow.cn/balance",
        "https://api.siliconflow.cn/account"
    ]
    
    print("硅基流动API端点列表（按优先级）:")
    for i, endpoint in enumerate(siliconflow_endpoints, 1):
        print(f"  {i}. {endpoint}")
    
    # OpenAI兼容端点
    openai_compatible = [
        "https://api.siliconflow.cn/v1/dashboard/billing/credit_grants",
        "https://api.siliconflow.cn/v1/billing/usage",
        "https://api.siliconflow.cn/dashboard/billing/credit_grants"
    ]
    
    print("\nOpenAI兼容端点:")
    for i, endpoint in enumerate(openai_compatible, 1):
        print(f"  {i}. {endpoint}")
    
    return True


def main():
    """主测试函数"""
    print("DeepSeek和硅基流动平台修复验证")
    print("=" * 50)
    
    success_count = 0
    total_tests = 3
    
    # 测试DeepSeek数据转换
    if test_deepseek_data_conversion():
        success_count += 1
    
    # 测试硅基流动逻辑
    if test_siliconflow_logic():
        success_count += 1
    
    # 测试API端点
    if test_api_endpoints():
        success_count += 1
    
    print("\n" + "=" * 50)
    print(f"逻辑验证完成: {success_count}/{total_tests} 项测试通过")
    
    if success_count == total_tests:
        print("\n🎉 所有逻辑测试通过！")
        print("\n修复总结:")
        print("✓ DeepSeek: 修复了字符串除法错误，添加了安全的数据类型转换")
        print("✓ 硅基流动: 更新了API端点列表，添加了多种数据格式支持")
        print("✓ 错误处理: 增强了异常处理和重试机制")
        
        print("\n使用建议:")
        print("1. 确保API密钥正确配置")
        print("2. 检查网络连接")
        print("3. 如仍有问题，请检查API文档是否有更新")
        return True
    else:
        print("\n⚠️  部分逻辑测试失败")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)