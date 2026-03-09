/**
 * 博客标签云和分类筛选功能
 * 用法：在博客列表页面引入此脚本
 */

(function() {
    'use strict';
    
    // 配置
    const CONFIG = {
        maxTags: 20,              // 最多显示标签数
        minFontSize: 14,          // 最小字体
        maxFontSize: 28,          // 最大字体
        animationDuration: 300    // 动画时长
    };
    
    // 标签数据
    let tagsData = {};
    let categoriesData = {};
    
    // 初始化
    function init() {
        collectTagsAndCategories();
        createTagCloud();
        createCategoryFilter();
        bindEvents();
        console.log('✅ 博客标签系统已加载');
    }
    
    // 收集标签和分类
    function collectTagsAndCategories() {
        const articles = document.querySelectorAll('.post-card, .article-item');
        
        articles.forEach(article => {
            // 收集标签
            const tagElements = article.querySelectorAll('.tag, .post-tag');
            tagElements.forEach(tagEl => {
                const tagName = tagEl.textContent.trim().toLowerCase();
                if (tagName) {
                    tagsData[tagName] = (tagsData[tagName] || 0) + 1;
                }
            });
            
            // 收集分类
            const category = article.getAttribute('data-category') || 
                           article.querySelector('.category')?.textContent.trim();
            if (category) {
                categoriesData[category] = (categoriesData[category] || 0) + 1;
            }
        });
    }
    
    // 创建标签云
    function createTagCloud() {
        const tagCloudContainer = document.getElementById('tag-cloud');
        if (!tagCloudContainer) return;
        
        // 按使用频率排序
        const sortedTags = Object.entries(tagsData)
            .sort((a, b) => b[1] - a[1])
            .slice(0, CONFIG.maxTags);
        
        if (sortedTags.length === 0) {
            tagCloudContainer.innerHTML = '<p class="no-tags">暂无标签</p>';
            return;
        }
        
        // 计算频率范围
        const maxCount = Math.max(...sortedTags.map(t => t[1]));
        const minCount = Math.min(...sortedTags.map(t => t[1]));
        
        // 生成标签云 HTML
        let html = '<div class="tag-cloud-items">';
        sortedTags.forEach(([tag, count]) => {
            const size = calculateFontSize(count, minCount, maxCount);
            html += `
                <span class="tag-cloud-item" 
                      data-tag="${tag}" 
                      style="font-size: ${size}px; cursor: pointer;"
                      title="${count} 篇文章">
                    ${tag} (${count})
                </span>
            `;
        });
        html += '</div>';
        
        tagCloudContainer.innerHTML = html;
    }
    
    // 计算字体大小
    function calculateFontSize(count, min, max) {
        if (max === min) return CONFIG.maxFontSize;
        const ratio = (count - min) / (max - min);
        return CONFIG.minFontSize + ratio * (CONFIG.maxFontSize - CONFIG.minFontSize);
    }
    
    // 创建分类筛选器
    function createCategoryFilter() {
        const categoryFilterContainer = document.getElementById('category-filter');
        if (!categoryFilterContainer) return;
        
        const sortedCategories = Object.entries(categoriesData)
            .sort((a, b) => b[1] - a[1]);
        
        let html = '<button class="category-btn active" data-category="all">全部</button>';
        
        sortedCategories.forEach(([category, count]) => {
            html += `<button class="category-btn" data-category="${category}">${category} (${count})</button>`;
        });
        
        categoryFilterContainer.innerHTML = html;
    }
    
    // 绑定事件
    function bindEvents() {
        // 标签云点击
        document.getElementById('tag-cloud')?.addEventListener('click', function(e) {
            const tagItem = e.target.closest('.tag-cloud-item');
            if (tagItem) {
                const tag = tagItem.getAttribute('data-tag');
                filterByTag(tag);
            }
        });
        
        // 分类筛选点击
        document.getElementById('category-filter')?.addEventListener('click', function(e) {
            const btn = e.target.closest('.category-btn');
            if (btn) {
                const category = btn.getAttribute('data-category');
                filterByCategory(category);
                
                // 更新激活状态
                document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            }
        });
        
        // URL 参数筛选
        const urlParams = new URLSearchParams(window.location.search);
        const tagParam = urlParams.get('tag');
        const categoryParam = urlParams.get('category');
        
        if (tagParam) {
            filterByTag(tagParam);
        } else if (categoryParam) {
            filterByCategory(categoryParam);
        }
    }
    
    // 按标签筛选
    function filterByTag(tag) {
        const articles = document.querySelectorAll('.post-card, .article-item');
        let visibleCount = 0;
        
        articles.forEach(article => {
            const tagElements = article.querySelectorAll('.tag, .post-tag');
            const hasTag = Array.from(tagElements).some(el => 
                el.textContent.trim().toLowerCase() === tag.toLowerCase()
            );
            
            if (hasTag) {
                showArticle(article);
                visibleCount++;
            } else {
                hideArticle(article);
            }
        });
        
        updateResultsCount(visibleCount);
        scrollToResults();
    }
    
    // 按分类筛选
    function filterByCategory(category) {
        const articles = document.querySelectorAll('.post-card, .article-item');
        let visibleCount = 0;
        
        articles.forEach(article => {
            if (category === 'all') {
                showArticle(article);
                visibleCount++;
            } else {
                const articleCategory = article.getAttribute('data-category') || 
                                      article.querySelector('.category')?.textContent.trim();
                
                if (articleCategory?.toLowerCase() === category.toLowerCase()) {
                    showArticle(article);
                    visibleCount++;
                } else {
                    hideArticle(article);
                }
            }
        });
        
        updateResultsCount(visibleCount);
        scrollToResults();
    }
    
    // 显示文章
    function showArticle(article) {
        article.style.display = 'block';
        article.style.opacity = '0';
        setTimeout(() => {
            article.style.transition = 'opacity 0.3s ease';
            article.style.opacity = '1';
        }, 50);
    }
    
    // 隐藏文章
    function hideArticle(article) {
        article.style.display = 'none';
    }
    
    // 更新结果计数
    function updateResultsCount(count) {
        const counter = document.getElementById('results-count');
        if (counter) {
            counter.textContent = `找到 ${count} 篇文章`;
        }
    }
    
    // 滚动到结果区域
    function scrollToResults() {
        const resultsSection = document.querySelector('.posts-container, .articles-list');
        if (resultsSection) {
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
    
    // 页面加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
