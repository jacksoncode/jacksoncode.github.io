#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML链接连通性检测工具
用于检测HTML文件中的HTTPS链接是否可以正常访问

作者: Jackson
日期: 2025-08-27
"""

import urllib.request
import urllib.error
import re
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse
import argparse
from pathlib import Path
import ssl

class LinkChecker:
    def __init__(self, timeout=10, max_workers=10):
        """
        初始化链接检查器
        :param timeout: 请求超时时间（秒）
        :param max_workers: 最大并发线程数
        """
        self.timeout = timeout
        self.max_workers = max_workers
        
        # 创建SSL上下文，允许未验证的证书（用于测试）
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        
    def extract_links_from_html(self, html_file):
        """
        从HTML文件中提取所有的HTTPS链接
        :param html_file: HTML文件路径
        :return: HTTPS链接列表
        """
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
            return []
            
        # 使用正则表达式提取href和src中的HTTPS链接
        https_pattern = r'(?:href|src)=["\']?(https://[^"\'\s>]+)["\']?'
        matches = re.findall(https_pattern, content, re.IGNORECASE)
        
        # 去重并返回
        unique_links = list(set(matches))
        return unique_links
        
    def check_single_link(self, url):
        """
        检查单个链接的连通性
        :param url: 要检查的URL
        :return: (url, status, response_time, error_msg)
        """
        start_time = time.time()
        try:
            # 创建请求对象
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
            )
            
            # 发送请求
            with urllib.request.urlopen(req, timeout=self.timeout, context=self.ssl_context) as response:
                response_time = time.time() - start_time
                if response.getcode() == 200:
                    return (url, 'OK', response_time, None)
                else:
                    return (url, 'ERROR', response_time, f'HTTP {response.getcode()}')
                    
        except urllib.error.HTTPError as e:
            response_time = time.time() - start_time
            return (url, 'ERROR', response_time, f'HTTP {e.code}: {e.reason}')
        except urllib.error.URLError as e:
            response_time = time.time() - start_time
            if 'timeout' in str(e.reason).lower():
                return (url, 'TIMEOUT', response_time, '请求超时')
            else:
                return (url, 'CONNECTION_ERROR', response_time, f'连接错误: {e.reason}')
        except Exception as e:
            response_time = time.time() - start_time
            return (url, 'ERROR', response_time, f'未知错误: {str(e)}')
    
    def check_links(self, links):
        """
        并发检查多个链接
        :param links: 链接列表
        :return: 检查结果列表
        """
        results = []
        
        print(f"🔍 开始检查 {len(links)} 个HTTPS链接...")
        print("=" * 80)
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            future_to_url = {executor.submit(self.check_single_link, url): url for url in links}
            
            # 收集结果
            for i, future in enumerate(as_completed(future_to_url), 1):
                url, status, response_time, error_msg = future.result()
                results.append((url, status, response_time, error_msg))
                
                # 实时显示进度
                status_icon = {
                    'OK': '✅',
                    'ERROR': '❌', 
                    'TIMEOUT': '⏰',
                    'CONNECTION_ERROR': '🔌'
                }.get(status, '❓')
                
                print(f"[{i:3d}/{len(links)}] {status_icon} {status:15} {response_time:6.2f}s - {url}")
                if error_msg:
                    print(f"      ↳ {error_msg}")
                    
        return results
    
    def generate_report(self, results):
        """
        生成检查报告
        :param results: 检查结果列表
        """
        print("\n" + "=" * 80)
        print("📊 检查报告")
        print("=" * 80)
        
        total = len(results)
        ok_count = sum(1 for _, status, _, _ in results if status == 'OK')
        error_count = sum(1 for _, status, _, _ in results if status == 'ERROR')
        timeout_count = sum(1 for _, status, _, _ in results if status == 'TIMEOUT')
        connection_error_count = sum(1 for _, status, _, _ in results if status == 'CONNECTION_ERROR')
        
        print(f"✅ 正常访问: {ok_count:3d} ({ok_count/total*100:5.1f}%)")
        print(f"❌ 访问错误: {error_count:3d} ({error_count/total*100:5.1f}%)")  
        print(f"⏰ 请求超时: {timeout_count:3d} ({timeout_count/total*100:5.1f}%)")
        print(f"🔌 连接错误: {connection_error_count:3d} ({connection_error_count/total*100:5.1f}%)")
        print(f"📈 总计链接: {total:3d}")
        
        # 显示问题链接
        problem_results = [(url, status, error_msg) for url, status, _, error_msg in results if status != 'OK']
        
        if problem_results:
            print(f"\n⚠️  发现 {len(problem_results)} 个问题链接:")
            print("-" * 80)
            for url, status, error_msg in problem_results:
                status_icon = {'ERROR': '❌', 'TIMEOUT': '⏰', 'CONNECTION_ERROR': '🔌'}.get(status, '❓')
                print(f"{status_icon} {url}")
                if error_msg:
                    print(f"   ↳ {error_msg}")
        else:
            print(f"\n🎉 所有链接都可以正常访问！")


def main():
    parser = argparse.ArgumentParser(description='HTML链接连通性检测工具')
    parser.add_argument('html_file', nargs='?', default='nav.html', 
                       help='要检查的HTML文件路径 (默认: nav.html)')
    parser.add_argument('--timeout', '-t', type=int, default=10,
                       help='请求超时时间(秒) (默认: 10)')
    parser.add_argument('--workers', '-w', type=int, default=10,
                       help='最大并发线程数 (默认: 10)')
    
    args = parser.parse_args()
    
    # 检查HTML文件是否存在
    html_path = Path(args.html_file)
    if not html_path.exists():
        print(f"❌ 文件不存在: {args.html_file}")
        sys.exit(1)
    
    print(f"🌐 HTML链接连通性检测工具")
    print(f"📄 文件: {args.html_file}")
    print(f"⏱️  超时: {args.timeout}秒")
    print(f"🔄 并发: {args.workers}线程")
    print()
    
    # 创建链接检查器
    checker = LinkChecker(timeout=args.timeout, max_workers=args.workers)
    
    # 提取链接
    links = checker.extract_links_from_html(args.html_file)
    
    if not links:
        print("❌ 未找到任何HTTPS链接")
        sys.exit(0)
        
    # 检查链接
    results = checker.check_links(links)
    
    # 生成报告
    checker.generate_report(results)


if __name__ == '__main__':
    main()