#!/usr/bin/env python3
"""
批量SEO优化脚本 - 更新ch34-ch69章节
添加: canonical, Open Graph, Twitter Card, JSON-LD
"""

import re
import os

# 章节标题映射（与实际 HTML 文件的 <title> 和 meta description 保持一致）
# 注意：ch59-ch63 的旧 <title> 标签与正文 H2 不一致，此处以正文内容为准
CHAPTER_INFO = {
    34: ("企业级AI架构认知", "企业级AI架构认知 - 理解企业AI应用的技术架构全景、部署模式和选型策略"),
    35: ("AI架构设计原则", "AI架构设计原则 - 分层架构、模块化设计、可扩展性与可维护性考量"),
    36: ("MCP协议标准", "MCP协议标准 - Model Context Protocol核心概念、架构设计与企业应用"),
    37: ("MCP服务器开发实战", "MCP服务器开发实战 - 使用Python和TypeScript构建MCP Server"),
    38: ("Skills技能体系", "Skills技能体系 - AI能力的模块化封装与管理"),
    39: ("Skills开发实战", "Skills开发实战 - 从零构建测试报告生成Skill完整示例"),
    40: ("Agent智能体架构", "Agent智能体架构 - ReAct循环、规划能力与工具链集成"),
    41: ("Agent开发实战", "Agent开发实战 - 使用LangChain和Claude构建测试执行Agent"),
    42: ("Harness框架", "Harness框架 - Agent执行与评估的标准化框架"),
    43: ("开发者平台生态", "开发者平台生态 - AI开发工具链全景图"),
    44: ("Claude Code实战", "Claude Code实战 - Anthropic官方AI编程助手的完整使用指南"),
    45: ("开源vs商业平台对比", "开源vs商业AI平台对比 - 选型决策指南"),
    46: ("Hugging Face生态", "Hugging Face生态 - 开源AI模型中心完整指南"),
    47: ("向量数据库选型", "向量数据库选型 - RAG系统存储方案对比"),
    48: ("团队协作工具", "团队协作工具 - AI时代测试团队协作最佳实践"),
    49: ("企业AI治理", "企业AI治理 - 安全合规与最佳实践框架"),
    50: ("测试用例生成", "测试用例生成 - AI驱动的智能测试用例设计"),
    51: ("测试脚本生成", "测试脚本生成 - AI自动化测试脚本编写"),
    52: ("测试数据生成", "测试数据生成 - AI智能测试数据构建"),
    53: ("缺陷分析", "缺陷分析 - AI辅助缺陷根因分析"),
    54: ("测试报告生成", "测试报告生成 - AI自动化测试报告编写"),
    55: ("回归测试执行", "回归测试执行 - AI辅助回归测试管理"),
    56: ("性能测试分析", "性能测试分析 - AI辅助性能测试结果分析"),
    57: ("安全测试辅助", "安全测试辅助 - AI辅助渗透测试与安全审计"),
    58: ("合规测试辅助", "合规测试辅助 - AI辅助GDPR/ISO等合规审计"),
    59: ("移动端测试", "移动端测试 - AI辅助App测试最佳实践"),
    60: ("Web测试", "Web测试 - AI辅助Web应用测试实战"),
    61: ("API测试", "API测试 - AI辅助接口测试实战"),
    62: ("数据库测试", "数据库测试 - AI辅助SQL与数据验证"),
    63: ("文档测试", "文档测试 - AI辅助文档审核与一致性验证"),
    64: ("多模态AI测试", "多模态AI - 图像/视频/音频AI测试实战"),
    65: ("AI推理测试", "AI推理测试 - AI逻辑推理能力评估"),
    66: ("AI教育应用测试", "AI教育应用 - AI在测试培训中的应用"),
    67: ("AI医疗应用测试", "AI医疗应用 - 医疗AI测试验证实践"),
    68: ("AI金融应用测试", "AI金融应用 - 金融AI测试与合规验证"),
    69: ("AI未来趋势与测试挑战", "AI未来趋势 - AI测试技术发展展望"),
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