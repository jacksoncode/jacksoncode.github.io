#!/usr/bin/env python3
"""
ModelScope API 调测主程序 - 修正版
"""
import argparse
import json
import sys
import os
from datetime import datetime
from config import Config, validate_config
from model_manager_fixed import ModelManager
import logging

# 配置日志
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL), format=Config.LOG_FORMAT)
logger = logging.getLogger(__name__)

def print_json(data, title=None):
    """格式化打印JSON数据"""
    if title:
        print(f"\n=== {title} ===")
    print(json.dumps(data, ensure_ascii=False, indent=2))

def print_models_table(models, title="模型列表"):
    """以表格形式打印模型"""
    if not models:
        print(f"{title}: 无数据")
        return
    
    print(f"\n=== {title} ===")
    print(f"{'序号':<4} {'模型名称':<30} {'类型':<10} {'下载量':<10}")
    print("-" * 60)
    
    for i, model in enumerate(models, 1):
        name = model.get('name', 'Unknown')[:28]
        model_type = model.get('type', 'N/A')[:8]
        downloads = model.get('downloads', 0)
        downloads_str = f"{downloads:,}" if downloads else "N/A"
        print(f"{i:<4} {name:<30} {model_type:<10} {downloads_str:<10}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='ModelScope API 调测工具')
    parser.add_argument('--action', choices=['models', 'account', 'search', 'export', 'stats'], 
                       default='models', help='执行的操作')
    parser.add_argument('--keyword', help='搜索关键词')
    parser.add_argument('--platform', choices=['modelscope', 'dashscope', 'all'], 
                       default='all', help='指定平台')
    parser.add_argument('--output', help='输出文件名')
    parser.add_argument('--format', choices=['json', 'table'], default='table', help='输出格式')
    
    args = parser.parse_args()
    
    try:
        # 验证配置
        validate_config()
        
        # 初始化模型管理器
        manager = ModelManager(
            modelscope_key=Config.MODELSCOPE_API_KEY,
            dashscope_key=Config.DASHSCOPE_API_KEY
        )
        
        # 执行相应操作
        if args.action == 'models':
            all_models = manager.get_all_models()
            
            if args.format == 'json':
                print_json(all_models, "可用模型列表")
            else:
                if args.platform == 'all' or args.platform == 'modelscope':
                    print_models_table(all_models.get('modelscope', []), "ModelScope模型")
                
                if args.platform == 'all' or args.platform == 'dashscope':
                    print_models_table(all_models.get('dashscope', []), "DashScope模型")
        
        elif args.action == 'account':
            summary = manager.get_account_summary()
            print_json(summary, "账户信息摘要")
        
        elif args.action == 'search':
            if not args.keyword:
                print("错误: 搜索操作需要提供关键词 (--keyword)")
                sys.exit(1)
            
            result = manager.search_models(args.keyword)
            
            if args.format == 'json':
                print_json(result, f"搜索结果: {args.keyword}")
            else:
                print_models_table(result.get('modelscope', []), f"ModelScope搜索结果: {args.keyword}")
                print_models_table(result.get('dashscope', []), f"DashScope搜索结果: {args.keyword}")
        
        elif args.action == 'export':
            filename = manager.export_models_to_json(args.output)
            print(f"✓ 数据已导出到: {filename}")
        
        elif args.action == 'stats':
            stats = manager.get_statistics()
            print_json(stats, "统计信息")
        
    except Exception as e:
        logger.error(f"程序执行失败: {e}")
        sys.exit(1)

def interactive_mode():
    """交互模式"""
    print("=== ModelScope API 调测工具 ===")
    print("1. 查看可用模型")
    print("2. 查看账户信息")
    print("3. 搜索模型")
    print("4. 导出数据")
    print("5. 查看统计")
    print("6. 退出")
    
    try:
        validate_config()
        manager = ModelManager(
            modelscope_key=Config.MODELSCOPE_API_KEY,
            dashscope_key=Config.DASHSCOPE_API_KEY
        )
        
        while True:
            choice = input("\n请选择操作 (1-6): ").strip()
            
            if choice == '1':
                all_models = manager.get_all_models()
                print_models_table(all_models.get('modelscope', []), "ModelScope模型")
                print_models_table(all_models.get('dashscope', []), "DashScope模型")
                
                # 显示统计
                ms_count = len(all_models.get('modelscope', []))
                ds_count = len(all_models.get('dashscope', []))
                print(f"\n📊 统计: ModelScope {ms_count} 个模型, DashScope {ds_count} 个模型")
            
            elif choice == '2':
                summary = manager.get_account_summary()
                print_json(summary, "账户信息摘要")
            
            elif choice == '3':
                keyword = input("请输入搜索关键词: ").strip()
                if keyword:
                    result = manager.search_models(keyword)
                    print_models_table(result.get('modelscope', []), f"ModelScope搜索: {keyword}")
                    print_models_table(result.get('dashscope', []), f"DashScope搜索: {keyword}")
                else:
                    print("❌ 关键词不能为空")
            
            elif choice == '4':
                filename = input("请输入文件名 (留空使用默认名称): ").strip()
                try:
                    exported_file = manager.export_models_to_json(filename if filename else None)
                    print(f"✓ 数据已导出到: {exported_file}")
                except Exception as e:
                    print(f"❌ 导出失败: {e}")
            
            elif choice == '5':
                stats = manager.get_statistics()
                print_json(stats, "统计信息")
            
            elif choice == '6':
                print("�� 再见!")
                break
            
            else:
                print("❌ 无效选择，请重新输入")
    
    except Exception as e:
        logger.error(f"交互模式执行失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        # 没有命令行参数时启动交互模式
        interactive_mode()
    else:
        # 有命令行参数时执行命令行模式
        main()
