/**
 * 安全性测试套件
 * 测试 XSS 防护、输入验证和输出编码
 */

// 简单的测试框架
class TestRunner {
    constructor() {
        this.tests = [];
        this.results = [];
    }

    test(name, fn) {
        this.tests.push({ name, fn });
    }

    async run() {
        console.log('🧪 开始运行安全性测试...\n');
        
        for (const test of this.tests) {
            try {
                await test.fn();
                this.results.push({ name: test.name, status: '✅ 通过' });
                console.log(`✅ ${test.name}`);
            } catch (error) {
                this.results.push({ name: test.name, status: '❌ 失败', error: error.message });
                console.log(`❌ ${test.name}: ${error.message}`);
            }
        }
        
        this.printSummary();
    }

    printSummary() {
        const passed = this.results.filter(r => r.status === '✅ 通过').length;
        const failed = this.results.filter(r => r.status === '❌ 失败').length;
        
        console.log('\n📊 测试总结:');
        console.log(`总计: ${this.results.length} 个测试`);
        console.log(`通过: ${passed} 个`);
        console.log(`失败: ${failed} 个`);
        
        if (failed > 0) {
            console.log('\n❌ 失败的测试:');
            this.results.filter(r => r.status === '❌ 失败').forEach(r => {
                console.log(`  - ${r.name}: ${r.error}`);
            });
        }
    }
}

// 断言函数
function assert(condition, message) {
    if (!condition) {
        throw new Error(message || '断言失败');
    }
}

function assertEquals(actual, expected, message) {
    if (actual !== expected) {
        throw new Error(message || `期望 ${expected}，但得到 ${actual}`);
    }
}

// 模拟 DOMPurify
class DOMPurify {
    static sanitize(dirty, config = {}) {
        if (typeof dirty !== 'string') {
            return '';
        }
        
        // 移除危险的 HTML 标签和属性
        let clean = dirty
            .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
            .replace(/<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>/gi, '')
            .replace(/<object\b[^<]*(?:(?!<\/object>)<[^<]*)*<\/object>/gi, '')
            .replace(/<embed\b[^>]*>/gi, '')
            .replace(/javascript:/gi, '')
            .replace(/on\w+\s*=/gi, '');
        
        // 只允许配置的标签和属性
        if (config.ALLOWED_TAGS) {
            const tagRegex = /<\/?([a-z][a-z0-9]*)[^>]*>/gi;
            clean = clean.replace(tagRegex, (match, tag) => {
                if (config.ALLOWED_TAGS.includes(tag.toLowerCase())) {
                    return match;
                }
                return '';
            });
        }
        
        return clean;
    }
}

// 输入验证函数
function escapeHtml(unsafe) {
    if (typeof unsafe !== 'string') {
        return '';
    }
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function sanitizeUrl(url) {
    try {
        const parsedUrl = new URL(url);
        if (parsedUrl.protocol !== 'http:' && parsedUrl.protocol !== 'https:') {
            return '#';
        }
        return escapeHtml(url);
    } catch (e) {
        return '#';
    }
}

// 创建测试运行器
const runner = new TestRunner();

// XSS 防护测试
runner.test('escapeHtml 应该转义 HTML 特殊字符', () => {
    const input = '<script>alert("XSS")</script>';
    const output = escapeHtml(input);
    assert(!output.includes('<script>'), '应该转义 script 标签');
    assert(output.includes('&lt;'), '应该包含 &lt;');
});

runner.test('escapeHtml 应该处理空值', () => {
    assertEquals(escapeHtml(null), '');
    assertEquals(escapeHtml(undefined), '');
    assertEquals(escapeHtml(''), '');
});

runner.test('escapeHtml 应该处理非字符串输入', () => {
    assertEquals(escapeHtml(123), '123');
    assertEquals(escapeHtml({}), '[object Object]');
});

runner.test('sanitizeUrl 应该只允许 http 和 https 协议', () => {
    assertEquals(sanitizeUrl('https://example.com'), 'https://example.com');
    assertEquals(sanitizeUrl('http://example.com'), 'http://example.com');
    assertEquals(sanitizeUrl('javascript:alert(1)'), '#');
    assertEquals(sanitizeUrl('data:text/html,<script>alert(1)</script>'), '#');
});

runner.test('sanitizeUrl 应该处理无效 URL', () => {
    assertEquals(sanitizeUrl('not-a-url'), '#');
    assertEquals(sanitizeUrl(''), '#');
});

// DOMPurify 集成测试
runner.test('DOMPurify.sanitize 应该移除 script 标签', () => {
    const dirty = '<div><script>alert("XSS")</script><p>内容</p></div>';
    const clean = DOMPurify.sanitize(dirty);
    assert(!clean.includes('<script>'), '应该移除 script 标签');
    assert(!clean.includes('alert'), '应该移除 alert 内容');
});

runner.test('DOMPurify.sanitize 应该移除 iframe 标签', () => {
    const dirty = '<div><iframe src="evil.com"></iframe><p>内容</p></div>';
    const clean = DOMPurify.sanitize(dirty);
    assert(!clean.includes('<iframe>'), '应该移除 iframe 标签');
});

runner.test('DOMPurify.sanitize 应该移除 JavaScript 协议', () => {
    const dirty = '<a href="javascript:alert(1)">点击</a>';
    const clean = DOMPurify.sanitize(dirty);
    assert(!clean.includes('javascript:'), '应该移除 javascript: 协议');
});

runner.test('DOMPurify.sanitize 应该移除事件处理器', () => {
    const dirty = '<div onclick="alert(1)">点击</div>';
    const clean = DOMPurify.sanitize(dirty);
    assert(!clean.includes('onclick'), '应该移除 onclick 属性');
});

runner.test('DOMPurify.sanitize 应该只允许配置的标签', () => {
    const dirty = '<div><span>允许</span><p>不允许</p></div>';
    const clean = DOMPurify.sanitize(dirty, { ALLOWED_TAGS: ['div', 'span'] });
    assert(clean.includes('<span>'), '应该包含允许的 span 标签');
    assert(!clean.includes('<p>'), '不应该包含不允许的 p 标签');
});

// 综合安全测试
runner.test('完整的 URL 渲染应该是安全的', () => {
    const linkData = {
        name: '<script>alert("XSS")</script>测试链接',
        url: 'javascript:alert(1)'
    };
    
    const safeUrl = sanitizeUrl(linkData.url);
    const safeName = escapeHtml(linkData.name);
    
    const html = `<a href="${safeUrl}">${safeName}</a>`;
    const cleanHtml = DOMPurify.sanitize(html, { ALLOWED_TAGS: ['a'], ALLOWED_ATTR: ['href'] });
    
    assert(!cleanHtml.includes('<script>'), '最终 HTML 不应该包含 script 标签');
    assert(!cleanHtml.includes('javascript:'), '最终 HTML 不应该包含 javascript: 协议');
    assert(cleanHtml.includes('#'), '危险 URL 应该被替换为 #');
});

runner.test('搜索功能应该是安全的', () => {
    const searchTerms = [
        '<script>alert("XSS")</script>',
        'javascript:alert(1)',
        '<img src=x onerror=alert(1)>',
        '"><script>alert("XSS")</script>'
    ];
    
    searchTerms.forEach(term => {
        const safeTerm = escapeHtml(term);
        assert(!safeTerm.includes('<script>'), `搜索词 "${term}" 应该被安全转义`);
        assert(!safeTerm.includes('javascript:'), `搜索词 "${term}" 应该移除 javascript: 协议`);
    });
});

// 性能测试
runner.test('安全函数应该在合理时间内完成', () => {
    const start = performance.now();
    
    // 测试大量数据处理
    for (let i = 0; i < 1000; i++) {
        escapeHtml('<script>alert("XSS")</script>');
        sanitizeUrl('javascript:alert(1)');
        DOMPurify.sanitize('<div><script>alert(1)</script></div>');
    }
    
    const end = performance.now();
    const duration = end - start;
    
    assert(duration < 100, `1000次处理应该在100ms内完成，实际用了 ${duration}ms`);
});

// 运行测试
if (typeof window !== 'undefined') {
    // 浏览器环境
    window.runSecurityTests = () => runner.run();
} else {
    // Node.js 环境
    runner.run().catch(console.error);
}