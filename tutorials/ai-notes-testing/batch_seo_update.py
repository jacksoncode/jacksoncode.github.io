#!/usr/bin/env python3
"""
批量SEO优化脚本 - 更新ch34-ch69章节
添加: canonical, Open Graph, Twitter Card, JSON-LD
"""

import re
import os

# 章节标题映射
CHAPTER_INFO = {
    34: ("企业级AI架构认知", "理解企业AI应用的技术架构全景、部署模式和选型策略"),
    35: ("MCP协议核心原理", "深入解析MCP协议的设计理念、核心组件和通信机制"),
    36: ("MCP客户端开发实战", "从零构建MCP客户端，实现与AI服务的标准化通信"),
    37: ("MCP服务端开发实战", "构建MCP服务端，暴露工具、资源和提示词给AI客户端"),
    38: ("MCP调试与监控", "MCP协议调试工具、日志分析和性能监控最佳实践"),
    39: ("Skills体系架构认知", "理解Skills的设计哲学、模块化架构和扩展机制"),
    40: ("Skills开发实战", "创建自定义Skills，实现AI能力模块化封装"),
    41: ("Skills编排与组合", "多Skills协作模式、依赖管理和编排策略"),
    42: ("错误处理与容错机制", "企业级AI系统的错误分类、处理策略和容错设计"),
    43: ("调试工具链构建", "构建完整的AI调试工具链，包括日志、追踪和诊断"),
    44: ("日志系统设计", "AI系统日志架构、收集策略和分析最佳实践"),
    45: ("性能监控与优化", "AI系统性能指标、监控方法和优化技巧"),
    46: ("自动化测试框架", "构建AI系统自动化测试框架，覆盖单元、集成和E2E测试"),
    47: ("持续集成实践", "AI系统CI/CD流程、测试自动化和发布策略"),
    48: ("代码质量与静态分析", "AI代码质量标准、静态分析工具和审查流程"),
    49: ("文档与知识管理", "AI项目文档架构、知识库建设和维护策略"),
    50: ("Prompt测试方法论", "Prompt测试策略、评估指标和优化方法"),
    51: ("模型能力边界测试", "测试AI模型的能力边界、限制和失败模式"),
    52: ("上下文管理测试", "测试AI系统的上下文处理、记忆和状态管理"),
    53: ("工具调用可靠性测试", "测试AI工具调用的可靠性、错误处理和回退机制"),
    54: ("多轮对话测试", "测试AI多轮对话的连贯性、一致性和上下文保持"),
    55: ("响应质量评估", "AI响应质量评估标准、方法和自动化测试"),
    56: ("并发与负载测试", "AI系统并发测试、负载模拟和性能基准"),
    57: ("安全测试实践", "AI系统安全测试策略、漏洞检测和防护验证"),
    58: ("合规性测试", "AI系统合规测试框架、标准验证和审计准备"),
    59: ("回归测试策略", "AI系统回归测试策略、变更影响分析和自动化"),
    60: ("测试报告与可视化", "AI测试报告生成、数据可视化和结果呈现"),
    61: ("A/B测试在AI中的应用", "AI系统A/B测试设计、实施和数据分析"),
    62: ("用户反馈收集与分析", "AI系统用户反馈收集、分析和改进闭环"),
    63: ("测试自动化进阶", "高级测试自动化技术、智能测试和自适应策略"),
    64: ("多模态AI测试", "测试多模态AI系统的图像、语音和文本融合能力"),
    65: ("AI推理测试", "测试AI推理能力、逻辑链验证和结论正确性"),
    66: ("AI教育应用测试", "测试AI教育应用的适应性、个性化和学习效果"),
    67: ("AI医疗应用测试", "测试AI医疗应用的准确性、安全性和合规性"),
    68: ("AI金融应用测试", "测试AI金融应用的准确性、风险控制和合规性"),
    69: ("AI未来趋势与测试挑战", "展望AI技术发展趋势和测试领域的新挑战"),
}

def add_seo_elements(filepath, chapter_num):
    """添加SEO元素到章节文件"""
    
    title, desc = CHAPTER_INFO.get(chapter_num, ("AI测试实战", "企业级AI架构与测试应用"))
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 添加canonical tag (在title之前)
    canonical = f'<link rel="canonical" href="https://jacksoncode.github.io/tutorials/ai-notes-testing/ch{chapter_num}.html">\n    '
    content = re.sub(r'(<title>)', canonical + r'\1', content)
    
    # 2. 添加Open Graph和Twitter Card (在author meta之后)
    og_twitter = f'''
    <!-- Open Graph -->
    <meta property="og:title" content="第{chapter_num}章：{title} - AI测试实战">
    <meta property="og:description" content="{desc}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://jacksoncode.github.io/tutorials/ai-notes-testing/ch{chapter_num}.html">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="第{chapter_num}章：{title}">
    <meta name="twitter:description" content="{desc}">
    
    <!-- Robots -->
    <meta name="robots" content="index, follow">
'''
    content = re.sub(r'(</head>)', og_twitter + '\n</head>', content)
    
    # 3. 添加JSON-LD BlogPosting schema (在</head>之前)
    jsonld = f'''
    <!-- Structured Data -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": "第{chapter_num}章：{title}",
        "description": "{desc}",
        "author": {{ "@type": "Person", "name": "AI Tester" }},
        "datePublished": "2026-06-22",
        "mainEntityOfPage": {{
            "@type": "WebPage",
            "@id": "https://jacksoncode.github.io/tutorials/ai-notes-testing/ch{chapter_num}.html"
        }},
        "isPartOf": {{
            "@type": "Course",
            "name": "AI测试实战",
            "url": "https://jacksoncode.github.io/tutorials/ai-notes-testing/"
        }}
    }}
    </script>
'''
    content = re.sub(r'(</head>)', jsonld + '</head>', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """批量更新所有章节"""
    base_dir = "/Users/pengzhang/Downloads/Github/jacksoncode.github.io/tutorials/ai-notes-testing"
    
    success_count = 0
    fail_count = 0
    
    for chapter_num in range(34, 70):
        filepath = os.path.join(base_dir, f"ch{chapter_num}.html")
        
        if os.path.exists(filepath):
            try:
                add_seo_elements(filepath, chapter_num)
                print(f"✓ ch{chapter_num}.html 已更新SEO元素")
                success_count += 1
            except Exception as e:
                print(f"✗ ch{chapter_num}.html 更新失败: {e}")
                fail_count += 1
        else:
            print(f"✗ ch{chapter_num}.html 文件不存在")
            fail_count += 1
    
    print(f"\n=== 批量SEO更新完成 ===")
    print(f"成功: {success_count} 个文件")
    print(f"失败: {fail_count} 个文件")

if __name__ == "__main__":
    main()