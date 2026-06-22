#!/usr/bin/env python3
"""
JSON-LD验证脚本 - 检查所有章节的结构化数据合规性
"""

import json
import re
import os
from pathlib import Path

def extract_jsonld(html_content):
    """从HTML提取JSON-LD脚本内容"""
    pattern = r'<script type="application/ld\+json">(.*?)</script>'
    matches = re.findall(pattern, html_content, re.DOTALL)
    return [json.loads(m.strip()) for m in matches]

def validate_course_schema(data):
    """验证Course schema必需字段"""
    required_fields = ["@context", "@type", "name", "description", "provider"]
    errors = []
    
    for field in required_fields:
        if field not in data:
            errors.append(f"缺少必需字段: {field}")
    
    if "@type" in data and data["@type"] != "Course":
        errors.append(f"@type应为Course，实际为{data['@type']}")
    
    if "provider" in data:
        if "@type" not in data["provider"]:
            errors.append("provider缺少@type")
        if "name" not in data["provider"]:
            errors.append("provider缺少name")
    
    return errors

def validate_blogposting_schema(data):
    """验证BlogPosting schema必需字段"""
    required_fields = ["@context", "@type", "headline", "description", "author", "datePublished"]
    errors = []
    
    for field in required_fields:
        if field not in data:
            errors.append(f"缺少必需字段: {field}")
    
    if "@type" in data and data["@type"] != "BlogPosting":
        errors.append(f"@type应为BlogPosting，实际为{data['@type']}")
    
    if "author" in data:
        if "@type" not in data["author"]:
            errors.append("author缺少@type")
        if "name" not in data["author"]:
            errors.append("author缺少name")
    
    if "mainEntityOfPage" in data:
        if "@type" not in data["mainEntityOfPage"]:
            errors.append("mainEntityOfPage缺少@type")
        if "@id" not in data["mainEntityOfPage"]:
            errors.append("mainEntityOfPage缺少@id")
    
    return errors

def validate_file(filepath):
    """验证单个HTML文件的JSON-LD"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    jsonld_data = extract_jsonld(content)
    
    results = {
        "file": os.path.basename(filepath),
        "count": len(jsonld_data),
        "schemas": [],
        "errors": []
    }
    
    for data in jsonld_data:
        schema_type = data.get("@type", "Unknown")
        results["schemas"].append(schema_type)
        
        if schema_type == "Course":
            errors = validate_course_schema(data)
            results["errors"].extend(errors)
        elif schema_type == "BlogPosting":
            errors = validate_blogposting_schema(data)
            results["errors"].extend(errors)
        else:
            results["errors"].append(f"未知的schema类型: {schema_type}")
    
    return results

def main():
    base_dir = Path("/Users/pengzhang/Downloads/Github/jacksoncode.github.io/tutorials/ai-notes-testing")
    
    print("=== JSON-LD结构化数据验证 ===\n")
    
    all_valid = True
    results_summary = []
    
    for chapter_num in range(34, 70):
        filepath = base_dir / f"ch{chapter_num}.html"
        if filepath.exists():
            result = validate_file(filepath)
            results_summary.append(result)
            
            status = "✓" if not result["errors"] else "✗"
            print(f"{status} ch{chapter_num}.html: {result['count']} JSON-LD, schemas: {result['schemas']}")
            
            if result["errors"]:
                all_valid = False
                for error in result["errors"]:
                    print(f"   - {error}")
    
    index_path = base_dir / "index.html"
    if index_path.exists():
        result = validate_file(index_path)
        results_summary.append(result)
        status = "✓" if not result["errors"] else "✗"
        print(f"{status} index.html: {result['count']} JSON-LD, schemas: {result['schemas']}")
        if result["errors"]:
            all_valid = False
            for error in result["errors"]:
                print(f"   - {error}")
    
    print(f"\n=== 验证结果汇总 ===")
    valid_count = sum(1 for r in results_summary if not r["errors"])
    print(f"合规文件: {valid_count}/{len(results_summary)}")
    
    if all_valid:
        print("\n✓ 所有JSON-LD结构化数据验证通过")
        print("\n下一步验证:")
        print("1. Google Rich Results Test: https://search.google.com/test/rich-results")
        print("2. Schema.org Validator: https://validator.schema.org/")
        print("3. 复制任一章节URL测试: https://jacksoncode.github.io/tutorials/ai-notes-testing/ch34.html")
    else:
        print("\n✗ 存在验证错误，请检查上述错误信息")
    
    return all_valid

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)