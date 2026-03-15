/**
 * 全站搜索功能
 * 支持 URL 搜索、文章搜索、Wiki 搜索
 */

(function() {
    'use strict';
    
    // 搜索数据
    let searchData = {
        urls: [],
        articles: [],
        wiki: []
    };
    
    // 搜索配置
    const config = {
        minQueryLength: 2,
        maxResults: 10,
        debounceDelay: 300
    };
    
    // DOM 元素
    let searchOverlay = null;
    let searchInput = null;
    let searchResults = null;
    let searchSpinner = null;
    let isSearchOpen = false;
    
    // 初始化搜索
    function init() {
        if (document.querySelector('.search-overlay')) {
            return; // 已经初始化过
        }
        
        createSearchOverlay();
        loadSearchData();
        bindEvents();
    }
    
    // 创建搜索覆盖层
    function createSearchOverlay() {
        const overlay = document.createElement('div');
        overlay.className = 'search-overlay';
        overlay.innerHTML = `
            <div class="search-container">
                <div class="search-header">
                    <input type="text" class="search-input" placeholder="搜索网站内容..." autocomplete="off">
                    <button class="search-close" aria-label="关闭搜索">×</button>
                </div>
                <div class="search-spinner">
                    <div class="spinner"></div>
                </div>
                <div class="search-results">
                    <div class="search-empty">
                        <i class="fas fa-search"></i>
                        <p>输入关键词开始搜索</p>
                    </div>
                </div>
                <div class="search-footer">
                    <span class="search-shortcut">按 ESC 关闭</span>
                    <span class="search-hint">↑↓ 选择结果</span>
                </div>
            </div>
        `;
        
        document.body.appendChild(overlay);
        
        searchOverlay = overlay;
        searchInput = overlay.querySelector('.search-input');
        searchResults = overlay.querySelector('.search-results');
        searchSpinner = overlay.querySelector('.search-spinner');
        
        // 添加样式
        addSearchStyles();
    }
    
    // 添加搜索样式
    function addSearchStyles() {
        if (document.querySelector('#search-styles')) {
            return;
        }
        
        const style = document.createElement('style');
        style.id = 'search-styles';
        style.textContent = `
            .search-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.8);
                z-index: 10000;
                display: none;
                align-items: flex-start;
                justify-content: center;
                padding-top: 10vh;
                animation: fadeIn 0.2s ease;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            .search-overlay.active {
                display: flex;
            }
            
            .search-container {
                width: 90%;
                max-width: 700px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
                overflow: hidden;
                animation: slideDown 0.3s ease;
            }
            
            @keyframes slideDown {
                from { 
                    transform: translateY(-50px);
                    opacity: 0;
                }
                to { 
                    transform: translateY(0);
                    opacity: 1;
                }
            }
            
            .search-header {
                display: flex;
                align-items: center;
                padding: 20px;
                border-bottom: 1px solid #e5e7eb;
                gap: 12px;
            }
            
            .search-input {
                flex: 1;
                padding: 12px 16px;
                font-size: 16px;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                outline: none;
                transition: border-color 0.2s;
            }
            
            .search-input:focus {
                border-color: #3b82f6;
            }
            
            .search-close {
                width: 40px;
                height: 40px;
                border: none;
                background: #f3f4f6;
                border-radius: 8px;
                font-size: 24px;
                cursor: pointer;
                color: #6b7280;
                transition: all 0.2s;
            }
            
            .search-close:hover {
                background: #e5e7eb;
                color: #1f2937;
            }
            
            .search-spinner {
                display: none;
                padding: 40px;
                text-align: center;
            }
            
            .search-spinner.active {
                display: block;
            }
            
            .spinner {
                width: 40px;
                height: 40px;
                border: 4px solid #e5e7eb;
                border-top-color: #3b82f6;
                border-radius: 50%;
                animation: spin 0.8s linear infinite;
                margin: 0 auto;
            }
            
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
            
            .search-results {
                max-height: 400px;
                overflow-y: auto;
                padding: 0;
            }
            
            .search-empty {
                text-align: center;
                padding: 40px 20px;
                color: #9ca3af;
            }
            
            .search-empty i {
                font-size: 48px;
                margin-bottom: 12px;
                opacity: 0.5;
            }
            
            .search-item {
                padding: 16px 20px;
                border-bottom: 1px solid #f3f4f6;
                cursor: pointer;
                transition: background 0.2s;
                text-decoration: none;
                color: inherit;
                display: block;
            }
            
            .search-item:hover,
            .search-item.active {
                background: #f9fafb;
            }
            
            .search-item-title {
                font-weight: 600;
                color: #1f2937;
                margin-bottom: 4px;
            }
            
            .search-item-url {
                color: #6b7280;
                font-size: 13px;
                margin-bottom: 4px;
            }
            
            .search-item-desc {
                color: #9ca3af;
                font-size: 14px;
            }
            
            .search-item-highlight {
                background: #fef3c7;
                padding: 0 2px;
                border-radius: 2px;
            }
            
            .search-category {
                padding: 12px 20px;
                font-weight: 600;
                color: #6b7280;
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                background: #f9fafb;
            }
            
            .search-footer {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px 20px;
                background: #f9fafb;
                border-top: 1px solid #e5e7eb;
                font-size: 13px;
                color: #6b7280;
            }
            
            .dark-mode .search-overlay {
                background: rgba(0, 0, 0, 0.9);
            }
            
            .dark-mode .search-container {
                background: #1f2937;
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
            }
            
            .dark-mode .search-header {
                border-bottom-color: #374151;
            }
            
            .dark-mode .search-input {
                background: #374151;
                border-color: #4b5563;
                color: #f9fafb;
            }
            
            .dark-mode .search-input:focus {
                border-color: #3b82f6;
            }
            
            .dark-mode .search-close {
                background: #374151;
                color: #9ca3af;
            }
            
            .dark-mode .search-close:hover {
                background: #4b5563;
                color: #f9fafb;
            }
            
            .dark-mode .search-item {
                border-bottom-color: #374151;
            }
            
            .dark-mode .search-item:hover,
            .dark-mode .search-item.active {
                background: #374151;
            }
            
            .dark-mode .search-item-title {
                color: #f9fafb;
            }
            
            .dark-mode .search-item-url {
                color: #9ca3af;
            }
            
            .dark-mode .search-item-desc {
                color: #6b7280;
            }
            
            .dark-mode .search-item-highlight {
                background: #92400e;
            }
            
            .dark-mode .search-category {
                background: #374151;
                color: #9ca3af;
            }
            
            .dark-mode .search-footer {
                background: #374151;
                border-top-color: #4b5563;
            }
            
            /* 移动端适配 */
            @media (max-width: 768px) {
                .search-container {
                    width: 95%;
                    margin-top: 10vh;
                }
                
                .search-input {
                    font-size: 14px;
                }
                
                .search-results {
                    max-height: 50vh;
                }
            }
        `;
        
        document.head.appendChild(style);
    }
    
    // 加载搜索数据
    function loadSearchData() {
        // 加载导航数据
        fetch('/data/nav.json')
            .then(response => response.json())
            .then(data => {
                data.categories.forEach(category => {
                    category.links.forEach(link => {
                        searchData.urls.push({
                            title: link.name,
                            url: link.url,
                            category: category.name,
                            type: 'url'
                        });
                    });
                });
            })
            .catch(error => {
                console.error('加载导航数据失败:', error);
            });
        
        // 加载文章数据（这里可以扩展为实际的文章搜索）
        const articles = document.querySelectorAll('.post-card');
        articles.forEach(article => {
            const title = article.querySelector('.post-title')?.textContent || '';
            const url = article.getAttribute('href') || '';
            const desc = article.querySelector('.post-excerpt')?.textContent || '';
            
            if (title && url) {
                searchData.articles.push({
                    title: title,
                    url: url,
                    description: desc,
                    type: 'article'
                });
            }
        });
    }
    
    // 绑定事件
    function bindEvents() {
        // 键盘快捷键
        document.addEventListener('keydown', handleKeydown);
        
        // 搜索输入
        if (searchInput) {
            searchInput.addEventListener('input', debounce(handleSearch, config.debounceDelay));
            searchInput.addEventListener('keydown', handleSearchKeydown);
        }
        
        // 关闭按钮
        const closeBtn = searchOverlay?.querySelector('.search-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', closeSearch);
        }
        
        // 点击覆盖层关闭
        searchOverlay?.addEventListener('click', (e) => {
            if (e.target === searchOverlay) {
                closeSearch();
            }
        });
    }
    
    // 处理键盘事件
    function handleKeydown(e) {
        // Cmd/Ctrl + K 打开搜索
        if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
            e.preventDefault();
            toggleSearch();
        }
        
        // ESC 关闭搜索
        if (e.key === 'Escape' && isSearchOpen) {
            closeSearch();
        }
    }
    
    // 处理搜索输入
    function handleSearchKeydown(e) {
        const items = searchResults?.querySelectorAll('.search-item');
        if (!items.length) return;
        
        const activeItem = searchResults.querySelector('.search-item.active');
        const currentIndex = Array.from(items).indexOf(activeItem);
        
        // 向下箭头
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            const nextIndex = currentIndex < items.length - 1 ? currentIndex + 1 : 0;
            setActiveItem(items[nextIndex]);
        }
        
        // 向上箭头
        if (e.key === 'ArrowUp') {
            e.preventDefault();
            const prevIndex = currentIndex > 0 ? currentIndex - 1 : items.length - 1;
            setActiveItem(items[prevIndex]);
        }
        
        // Enter 选择结果
        if (e.key === 'Enter' && activeItem) {
            e.preventDefault();
            activeItem.click();
        }
    }
    
    // 设置激活项
    function setActiveItem(item) {
        searchResults.querySelectorAll('.search-item').forEach(i => {
            i.classList.remove('active');
        });
        item.classList.add('active');
        item.scrollIntoView({ block: 'nearest' });
    }
    
    // 执行搜索
    function handleSearch() {
        const query = searchInput.value.trim();
        
        if (!query || query.length < config.minQueryLength) {
            showEmptyState();
            return;
        }
        
        showSpinner();
        
        // 模拟搜索延迟
        setTimeout(() => {
            const results = performSearch(query);
            displayResults(results);
            hideSpinner();
        }, 300);
    }
    
    // 执行搜索
    function performSearch(query) {
        const results = [];
        const lowerQuery = query.toLowerCase();
        
        // 搜索 URL
        const urlResults = searchData.urls.filter(item => 
            item.title.toLowerCase().includes(lowerQuery) ||
            item.category.toLowerCase().includes(lowerQuery)
        ).slice(0, config.maxResults);
        
        if (urlResults.length > 0) {
            results.push({
                category: '网址导航',
                items: urlResults
            });
        }
        
        // 搜索文章
        const articleResults = searchData.articles.filter(item => 
            item.title.toLowerCase().includes(lowerQuery) ||
            (item.description && item.description.toLowerCase().includes(lowerQuery))
        ).slice(0, config.maxResults);
        
        if (articleResults.length > 0) {
            results.push({
                category: '文章',
                items: articleResults
            });
        }
        
        return results;
    }
    
    // 显示搜索结果
    function displayResults(results) {
        if (!results.length) {
            searchResults.innerHTML = `
                <div class="search-empty">
                    <i class="fas fa-search-minus"></i>
                    <p>未找到匹配 "${escapeHtml(searchInput.value)}" 的结果</p>
                </div>
            `;
            return;
        }
        
        let html = '';
        
        results.forEach(category => {
            html += `<div class="search-category">${category.category}</div>`;
            
            category.items.forEach(item => {
                const highlightedTitle = highlightText(item.title, searchInput.value);
                const highlightedDesc = item.description ? highlightText(item.description, searchInput.value) : '';
                
                html += `
                    <a href="${escapeHtml(item.url)}" class="search-item" target="${item.type === 'url' ? '_blank' : '_self'}">
                        <div class="search-item-title">${highlightedTitle}</div>
                        ${item.type === 'url' ? `<div class="search-item-url">${escapeHtml(item.category)}</div>` : ''}
                        ${highlightedDesc ? `<div class="search-item-desc">${highlightedDesc}</div>` : ''}
                    </a>
                `;
            });
        });
        
        searchResults.innerHTML = html;
    }
    
    // 高亮搜索词
    function highlightText(text, query) {
        if (!query) return escapeHtml(text);
        
        const regex = new RegExp(`(${escapeRegExp(query)})`, 'gi');
        return escapeHtml(text).replace(regex, '<span class="search-item-highlight">$1</span>');
    }
    
    // 转义正则表达式
    function escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }
    
    // 显示空状态
    function showEmptyState() {
        searchResults.innerHTML = `
            <div class="search-empty">
                <i class="fas fa-search"></i>
                <p>输入关键词开始搜索</p>
                <p style="font-size: 13px; margin-top: 8px;">至少输入 ${config.minQueryLength} 个字符</p>
            </div>
        `;
    }
    
    // 显示/隐藏加载动画
    function showSpinner() {
        if (searchSpinner) {
            searchSpinner.classList.add('active');
        }
    }
    
    function hideSpinner() {
        if (searchSpinner) {
            searchSpinner.classList.remove('active');
        }
    }
    
    // 打开搜索
    function openSearch() {
        if (searchOverlay) {
            searchOverlay.classList.add('active');
            isSearchOpen = true;
            
            if (searchInput) {
                setTimeout(() => searchInput.focus(), 100);
            }
            
            document.body.style.overflow = 'hidden';
        }
    }
    
    // 关闭搜索
    function closeSearch() {
        if (searchOverlay) {
            searchOverlay.classList.remove('active');
            isSearchOpen = false;
            
            if (searchInput) {
                searchInput.value = '';
                showEmptyState();
            }
            
            document.body.style.overflow = '';
        }
    }
    
    // 切换搜索
    function toggleSearch() {
        if (isSearchOpen) {
            closeSearch();
        } else {
            openSearch();
        }
    }
    
    // 防抖函数
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // HTML 转义
    function escapeHtml(text) {
        if (typeof text !== 'string') {
            return '';
        }
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
    
    // 暴露全局方法
    window.SiteSearch = {
        init: init,
        open: openSearch,
        close: closeSearch,
        toggle: toggleSearch
    };
    
    // 自动初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();