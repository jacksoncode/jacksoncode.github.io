#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI平台账单查询系统演示脚本
演示基本功能，不依赖外部网络请求
"""

import sys
import os
import json
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, Optional, Any
from abc import ABC, abstractmethod
from enum import Enum

# 简化版本的数据结构和基础类

class PlatformType(Enum):
    """平台类型枚举"""
    DEMO_PLATFORM1 = "demo_platform1"
    DEMO_PLATFORM2 = "demo_platform2"


@dataclass
class BillingInfo:
    """账单信息数据类"""
    platform: str
    balance: float
    used_amount: float
    total_quota: float
    free_quota: float
    recharged_amount: float
    gift_amount: float
    currency: str = "USD"
    last_update: str = ""
    usage_details: Optional[Dict] = None
    
    def __post_init__(self):
        if not self.last_update:
            self.last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict:
        return asdict(self)


class OutputFormat(Enum):
    """输出格式枚举"""
    JSON = "json"
    TABLE = "table"


class DemoPlatform1:
    """演示平台1"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.platform_name = "演示平台1"
    
    def get_billing_info(self) -> BillingInfo:
        """模拟获取账单信息"""
        return BillingInfo(
            platform=self.platform_name,
            balance=158.75,
            used_amount=41.25,
            total_quota=200.0,
            free_quota=50.0,
            recharged_amount=150.0,
            gift_amount=50.0,
            currency="USD",
            usage_details={
                "requests_count": 1250,
                "tokens_used": 125000,
                "last_request": "2024-01-15 10:30:00"
            }
        )


class DemoPlatform2:
    """演示平台2"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.platform_name = "演示平台2"
    
    def get_billing_info(self) -> BillingInfo:
        """模拟获取账单信息"""
        return BillingInfo(
            platform=self.platform_name,
            balance=89.50,
            used_amount=110.50,
            total_quota=200.0,
            free_quota=30.0,
            recharged_amount=170.0,
            gift_amount=30.0,
            currency="CNY",
            usage_details={
                "requests_count": 2100,
                "tokens_used": 210000,
                "last_request": "2024-01-15 11:15:00"
            }
        )


class DemoSiliconFlowPlatform:
    """硅基流动演示平台"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.platform_name = "硅基流动(演示)"
    
    def get_billing_info(self) -> BillingInfo:
        """模拟获取硅基流动账单信息"""
        return BillingInfo(
            platform=self.platform_name,
            balance=68.25,
            used_amount=31.75,
            total_quota=100.0,
            free_quota=15.0,
            recharged_amount=85.0,
            gift_amount=15.0,
            currency="CNY",
            usage_details={
                "requests_count": 850,
                "tokens_used": 95000,
                "last_request": "2024-01-15 09:45:00",
                "api_version": "v1",
                "models_used": ["Qwen/Qwen2-72B-Instruct", "01-ai/Yi-34B-Chat"]
            }
        )


class BillingFormatter:
    """账单信息格式化器"""
    
    @staticmethod
    def format_as_json(billing_data: Dict[str, BillingInfo], indent: int = 2) -> str:
        """格式化为JSON"""
        json_data = {}
        for platform, info in billing_data.items():
            json_data[platform] = info.to_dict()
        return json.dumps(json_data, indent=indent, ensure_ascii=False)
    
    @staticmethod
    def format_as_table(billing_data: Dict[str, BillingInfo]) -> str:
        """格式化为简单表格"""
        lines = []
        lines.append("-" * 100)
        lines.append(f"{'平台':<15} {'余额':<10} {'已使用':<10} {'总额度':<10} {'币种':<6} {'更新时间':<20}")
        lines.append("-" * 100)
        
        for platform, info in billing_data.items():
            lines.append(
                f"{info.platform:<15} "
                f"{info.balance:<10.2f} "
                f"{info.used_amount:<10.2f} "
                f"{info.total_quota:<10.2f} "
                f"{info.currency:<6} "
                f"{info.last_update:<20}"
            )
        
        lines.append("-" * 100)
        
        # 添加统计信息
        lines.append("\n=== 统计信息 ===")
        total_balance_usd = sum(info.balance for info in billing_data.values() if info.currency == "USD")
        total_balance_cny = sum(info.balance for info in billing_data.values() if info.currency == "CNY")
        
        if total_balance_usd > 0:
            lines.append(f"总余额 (USD): {total_balance_usd:.2f}")
        if total_balance_cny > 0:
            lines.append(f"总余额 (CNY): {total_balance_cny:.2f}")
        
        lines.append(f"平台数量: {len(billing_data)}")
        
        return "\n".join(lines)
    
    @classmethod
    def format(cls, billing_data: Dict[str, BillingInfo], output_format: OutputFormat) -> str:
        """根据指定格式格式化数据"""
        if output_format == OutputFormat.JSON:
            return cls.format_as_json(billing_data)
        elif output_format == OutputFormat.TABLE:
            return cls.format_as_table(billing_data)
        else:
            raise ValueError(f"不支持的输出格式: {output_format}")


def demo_basic_usage():
    """基本使用演示"""
    print("=== AI平台账单查询系统 - 基本功能演示 ===\n")
    
    # 1. 创建平台实例
    platform1 = DemoPlatform1(api_key="demo-key-1")
    platform2 = DemoPlatform2(api_key="demo-key-2")
    siliconflow_platform = DemoSiliconFlowPlatform(api_key="demo-siliconflow-key")
    
    # 2. 查询账单信息
    billing_data = {}
    
    print("正在查询平台账单信息...")
    
    platforms = [platform1, platform2, siliconflow_platform]
    
    for platform in platforms:
        try:
            billing_info = platform.get_billing_info()
            billing_data[platform.platform_name] = billing_info
            print(f"✓ {platform.platform_name}: 查询成功")
        except Exception as e:
            print(f"✗ {platform.platform_name}: 查询失败 - {e}")
    
    # 3. 格式化并显示结果
    if billing_data:
        formatter = BillingFormatter()
        
        print(f"\n=== 账单信息汇总 ===\n")
        table_result = formatter.format(billing_data, OutputFormat.TABLE)
        print(table_result)
        
        # 4. 显示详细信息
        print(f"\n=== 详细信息 (JSON格式) ===\n")
        json_result = formatter.format(billing_data, OutputFormat.JSON)
        print(json_result)
        
        # 5. 保存到文件
        output_file = "demo_billing_report.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(json_result)
        print(f"\n✓ 详细报告已保存到: {output_file}")
        
    else:
        print("\n❌ 没有成功查询到任何平台的账单信息")


def demo_individual_platform():
    """单平台查询演示"""
    print("\n" + "="*60)
    print("=== 单平台查询演示 ===\n")
    
    platform = DemoPlatform1(api_key="demo-key")
    billing_info = platform.get_billing_info()
    
    print(f"平台名称: {billing_info.platform}")
    print(f"当前余额: {billing_info.balance} {billing_info.currency}")
    print(f"已使用金额: {billing_info.used_amount} {billing_info.currency}")
    print(f"总额度: {billing_info.total_quota} {billing_info.currency}")
    print(f"免费额度: {billing_info.free_quota} {billing_info.currency}")
    print(f"已充值金额: {billing_info.recharged_amount} {billing_info.currency}")
    print(f"赠送金额: {billing_info.gift_amount} {billing_info.currency}")
    print(f"更新时间: {billing_info.last_update}")
    
    if billing_info.usage_details:
        print(f"\n详细使用情况:")
        for key, value in billing_info.usage_details.items():
            print(f"  {key}: {value}")


def demo_error_handling():
    """错误处理演示"""
    print("\n" + "="*60)
    print("=== 错误处理演示 ===\n")
    
    class ErrorPlatform:
        def __init__(self, api_key: str):
            self.api_key = api_key
            self.platform_name = "错误平台"
        
        def get_billing_info(self) -> BillingInfo:
            raise Exception("模拟API调用失败")
    
    error_platform = ErrorPlatform(api_key="error-key")
    
    try:
        billing_info = error_platform.get_billing_info()
        print("✗ 应该抛出异常，但没有")
    except Exception as e:
        print(f"✓ 成功捕获异常: {e}")
        
        # 创建错误信息对象
        error_billing_info = BillingInfo(
            platform=error_platform.platform_name,
            balance=0,
            used_amount=0,
            total_quota=0,
            free_quota=0,
            recharged_amount=0,
            gift_amount=0,
            currency="USD",
            usage_details={"error": str(e)}
        )
        
        print("\n生成错误信息对象:")
        print(f"平台: {error_billing_info.platform}")
        print(f"错误详情: {error_billing_info.usage_details}")


def main():
    """主函数"""
    print("AI平台账单查询系统演示")
    print("版本: 1.0.0")
    print("作者: AI助手")
    print("-" * 60)
    
    try:
        # 运行各种演示
        demo_basic_usage()
        demo_individual_platform()
        demo_error_handling()
        
        print("\n" + "="*60)
        print("=== 演示完成 ===")
        print("\n💡 提示:")
        print("1. 在实际使用中，需要安装 requests 库: pip install requests")
        print("2. 需要配置真实的API密钥才能查询真实数据")
        print("3. 支持的平台请参考 README.md 文档")
        print("4. 使用 --help 参数查看完整命令行选项")
        
    except Exception as e:
        print(f"\n❌ 演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)