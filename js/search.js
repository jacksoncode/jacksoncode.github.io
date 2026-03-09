/**
 * 本地搜索功能 - Lunr.js 实现
 * 无需后端，纯前端全文搜索
 */

(function() {
    'use strict';
    
    // 搜索配置
    const SEARCH_CONFIG = {
        minQueryLength: 2,          // 最小搜索长度
        maxResults: 10,             // 最大结果显示
        searchDelay: 300,           // 搜索延迟（防抖）
        highlightClass: 'search-highlight'
    };
    
    // 搜索数据索引
    let searchIndex = null;
    let searchData = [];
    
    // 初始化搜索
    function initSearch() {
        // 检查是否已加载 Lunr
        if (typeof lunr === 'undefined') {
            console.warn('Lunr.js 未加载，搜索功能不可用');
            return;
        }
        
        // 构建搜索索引
        buildIndex();
        
        // 绑定搜索事件
        bindSearchEvents();
        
        console.log('✅ 搜索功能已初始化');
    }
    
    // 构建搜索索引
    function buildIndex() {
        // 从页面收集可搜索内容
        const pages = collectSearchableContent();
        
        searchIndex = lunr(function() {
            this.ref('id');
            this.field('title', { boost: 10 });
            this.field('description', { boost: 5 });
            this.field('content', { boost: 1 });
            this.field('url');
            
            pages.forEach((page, index) => {
                page.id = index;
                this.add(page);
                searchData.push(page);
            });
        });
        
        console.log(`📚 已索引 ${pages.length} 个页面`);
    }
    
    // 收集可搜索内容
    function collectSearchableContent() {
        const pages = [];
        
        // 收集导航链接
        document.querySelectorAll('.nav-link-item').forEach(link => {
            pages.push({
                title: link.textContent.trim(),
                description: '',
                content: '',
                url: link.href
            });
        });
        
        // 收集文章卡片
        document.querySelectorAll('.post-card, .feature-card').forEach(card => {
            const title = card.querySelector('h3, h2')?.textContent || '';
            const desc = card.querySelector('p')?.textContent || '';
            const url = card.closest('a')?.href || '';
            
            pages.push({
                title,
                description: desc,
                content: title + ' ' + desc,
                url
            });
        });
        
        // 收集分类标题
        document.querySelectorAll('.category-title').forEach(title => {
            pages.push({
                title: title.textContent.trim(),
                description: '分类',
                content: '',
                url: '#' + title.closest('.category-card')?.id
            });
        });
        
        return pages;
    }
    
    // 执行搜索
    function performSearch(query) {
        if (!searchIndex || query.length < SEARCH_CONFIG.minQueryLength) {
            return [];
        }
        
        try {
            const results = searchIndex.search(query);
            return results.slice(0, SEARCH_CONFIG.maxResults);
        } catch (error) {
            console.error('搜索出错:', error);
            return [];
        }
    }
    
    // 显示搜索结果
    function showResults(results, query) {
        removeExistingResults();
        
        if (results.length === 0) {
            showNoResults(query);
            return;
        }
        
        const resultsContainer = createResultsContainer();
        
        results.forEach(result => {
            const item = searchData[result.ref];
            const resultElement = createResultItem(item, result.matchData.metadata);
            resultsContainer.appendChild(resultElement);
        });
        
        document.querySelector('.main-content')?.before(resultsContainer);
    }
    
    // 创建结果容器
    function createResultsContainer() {
        let container = document.getElementById('search-results');
        if (!container) {
            container = document.createElement('div');
            container.id = 'search-results';
            container.className = 'search-results-container';
        }
        return container;
    }
    
    // 创建结果项
    function createResultItem(item, metadata) {
        const div = document.createElement('div');
        div.className = 'search-result-item';
        
        const title = document.createElement('h3');
        title.textContent = item.title;
        
        const link = document.createElement('a');
        link.href = item.url;
        link.target = '_blank';
        link.appendChild(title);
        
        if (item.description) {
            const desc = document.createElement('p');
            desc.textContent = item.description;
            link.appendChild(desc);
        }
        
        div.appendChild(link);
        return div;
    }
    
    // 显示无结果
    function showNoResults(query) {
        removeExistingResults();
        
        const container = createResultsContainer();
        container.innerHTML = `
            <div class="no-results">
                <i class="fas fa-search"></i>
                <p>未找到关于 "${escapeHtml(query)}" 的结果</p>
            </div>
        `;
        
        document.querySelector('.main-content')?.before(container);
    }
    
    // 移除现有结果
    function removeExistingResults() {
        const existing = document.getElementById('search-results');
        if (existing) {
            existing.remove();
        }
    }
    
    // 绑定搜索事件
    function bindSearchEvents() {
        const searchInput = document.getElementById('searchInput');
        if (!searchInput) return;
        
        let timeoutId = null;
        
        searchInput.addEventListener('input', function(e) {
            const query = e.target.value.trim();
            
            clearTimeout(timeoutId);
            
            if (query.length < SEARCH_CONFIG.minQueryLength) {
                removeExistingResults();
                return;
            }
            
            timeoutId = setTimeout(() => {
                const results = performSearch(query);
                showResults(results, query);
            }, SEARCH_CONFIG.searchDelay);
        });
        
        // ESC 键清除搜索
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                searchInput.value = '';
                removeExistingResults();
                searchInput.blur();
            }
        });
    }
    
    // HTML 转义
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // 页面加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSearch);
    } else {
        initSearch();
    }
})();
