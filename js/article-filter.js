class ArticleFilter {
    constructor() {
        this.articles = [];
        this.activeFilters = {
            category: null,
            difficulty: null,
            tags: [],
        };
        this.filterUI = null;
        this.init();
    }

    async init() {
        await this.loadArticles();
        this.createFilterUI();
        this.bindEvents();
        this.applyFilters();
    }

    async loadArticles() {
        try {
            const response = await fetch('./data/search-index.json');
            this.articles = await response.json();

            this.categories = this.extractCategories();
            this.difficulties = ['入门', '进阶', '高级'];
            this.allTags = this.extractTags();

            this.renderFilterUI();
        } catch (error) {
            console.error('加载文章失败:', error);
        }
    }

    extractCategories() {
        const categories = new Set();
        this.articles.forEach((article) => {
            if (article.category) categories.add(article.category);
        });
        return Array.from(categories).sort();
    }

    extractTags() {
        const tags = new Set();
        this.articles.forEach((article) => {
            if (article.keywords) {
                article.keywords.split(' ').forEach((tag) => {
                    if (tag.length > 1) tags.add(tag);
                });
            }
        });
        return Array.from(tags).sort();
    }

    createFilterUI() {
        const filterContainer = document.createElement('div');
        filterContainer.id = 'article-filter';
        filterContainer.className = 'article-filter-container';

        document.querySelector('.posts-section')?.prepend(filterContainer);

        this.filterUI = filterContainer;
    }

    renderFilterUI() {
        if (!this.filterUI) return;

        this.filterUI.innerHTML = `
      <div class="filter-wrapper">
        <div class="filter-section">
          <h4 class="filter-title">
            <i class="fas fa-filter"></i> 文章筛选
          </h4>
          
          <div class="filter-group">
            <label class="filter-label">类别:</label>
            <select id="category-filter" class="filter-select">
              <option value="">全部类别</option>
              ${this.categories.map((cat) => `<option value="${cat}">${cat}</option>`).join('')}
            </select>
          </div>
          
          <div class="filter-group">
            <label class="filter-label">难度:</label>
            <select id="difficulty-filter" class="filter-select">
              <option value="">全部难度</option>
              ${this.difficulties
                  .map((diff) => `<option value="${diff}">${diff}</option>`)
                  .join('')}
            </select>
          </div>
          
          <div class="filter-group">
            <label class="filter-label">标签:</label>
            <div id="tag-filter" class="tag-filter">
              ${this.allTags
                  .slice(0, 20)
                  .map((tag) => `<button class="tag-btn" data-tag="${tag}">${tag}</button>`)
                  .join('')}
            </div>
          </div>
          
          <div class="filter-actions">
            <button id="reset-filter" class="reset-btn">
              <i class="fas fa-redo"></i> 重置筛选
            </button>
            <span id="filter-count" class="filter-count"></span>
          </div>
        </div>
      </div>
      
      <style>
        .article-filter-container {
          background: var(--card-bg);
          padding: 24px;
          border-radius: 12px;
          margin-bottom: 24px;
          border: 1px solid var(--border-color);
        }
        
        .filter-title {
          margin: 0 0 16px 0;
          font-size: 18px;
          color: var(--text-primary);
          display: flex;
          align-items: center;
          gap: 8px;
        }
        
        .filter-group {
          margin-bottom: 16px;
        }
        
        .filter-label {
          display: block;
          margin-bottom: 8px;
          font-size: 14px;
          font-weight: 500;
          color: var(--text-secondary);
        }
        
        .filter-select {
          width: 100%;
          padding: 10px 12px;
          border: 1px solid var(--border-color);
          border-radius: 8px;
          background: var(--bg-color);
          color: var(--text-primary);
          font-size: 14px;
          cursor: pointer;
        }
        
        .tag-filter {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
        }
        
        .tag-btn {
          padding: 6px 12px;
          border: 1px solid var(--border-color);
          border-radius: 6px;
          background: var(--bg-color);
          color: var(--text-secondary);
          font-size: 13px;
          cursor: pointer;
          transition: all 0.2s;
        }
        
        .tag-btn.active {
          background: var(--primary-color);
          color: white;
          border-color: var(--primary-color);
        }
        
        .tag-btn:hover:not(.active) {
          border-color: var(--primary-color);
          color: var(--primary-color);
        }
        
        .filter-actions {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-top: 20px;
        }
        
        .reset-btn {
          padding: 8px 16px;
          border: 1px solid var(--border-color);
          border-radius: 8px;
          background: var(--bg-color);
          color: var(--text-secondary);
          font-size: 14px;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 6px;
          transition: all 0.2s;
        }
        
        .reset-btn:hover {
          border-color: var(--primary-color);
          color: var(--primary-color);
        }
        
        .filter-count {
          font-size: 14px;
          color: var(--text-muted);
        }
        
        .dark-mode .article-filter-container {
          background: #1f2937;
          border-color: #374151;
        }
        
        .dark-mode .filter-select {
          background: #374151;
          color: #f9fafb;
          border-color: #4b5563;
        }
        
        .dark-mode .tag-btn {
          background: #374151;
          color: #9ca3af;
          border-color: #4b5563;
        }
        
        .dark-mode .tag-btn:hover:not(.active) {
          border-color: #3b82f6;
          color: #3b82f6;
        }
        
        .dark-mode .reset-btn {
          background: #374151;
          color: #9ca3af;
          border-color: #4b5563;
        }
        
        @media (max-width: 768px) {
          .article-filter-container {
            padding: 16px;
          }
          
          .tag-filter {
            max-height: 100px;
            overflow-y: auto;
          }
        }
      </style>
    `;
    }

    bindEvents() {
        const categorySelect = document.getElementById('category-filter');
        const difficultySelect = document.getElementById('difficulty-filter');
        const tagButtons = document.querySelectorAll('.tag-btn');
        const resetButton = document.getElementById('reset-filter');

        categorySelect?.addEventListener('change', (e) => {
            this.activeFilters.category = e.target.value || null;
            this.applyFilters();
        });

        difficultySelect?.addEventListener('change', (e) => {
            this.activeFilters.difficulty = e.target.value || null;
            this.applyFilters();
        });

        tagButtons.forEach((btn) => {
            btn.addEventListener('click', () => {
                const tag = btn.dataset.tag;

                if (this.activeFilters.tags.includes(tag)) {
                    this.activeFilters.tags = this.activeFilters.tags.filter((t) => t !== tag);
                    btn.classList.remove('active');
                } else {
                    this.activeFilters.tags.push(tag);
                    btn.classList.add('active');
                }

                this.applyFilters();
            });
        });

        resetButton?.addEventListener('click', () => {
            this.resetFilters();
        });
    }

    applyFilters() {
        let filtered = [...this.articles];

        if (this.activeFilters.category) {
            filtered = filtered.filter(
                (article) => article.category === this.activeFilters.category
            );
        }

        if (this.activeFilters.difficulty) {
            filtered = filtered.filter(
                (article) => article.difficulty === this.activeFilters.difficulty
            );
        }

        if (this.activeFilters.tags.length > 0) {
            filtered = filtered.filter((article) =>
                this.activeFilters.tags.some((tag) => article.keywords?.includes(tag))
            );
        }

        this.renderFilteredArticles(filtered);
        this.updateFilterCount(filtered.length);
    }

    renderFilteredArticles(articles) {
        const postsList = document.querySelector('.post-list');
        if (!postsList) return;

        if (articles.length === 0) {
            postsList.innerHTML = `
        <div class="no-results">
          <i class="fas fa-search"></i>
          <p>未找到符合条件的文章</p>
          <button onclick="window.articleFilter?.resetFilters()">重置筛选</button>
        </div>
      `;
            return;
        }

        postsList.innerHTML = articles
            .map(
                (article) => `
      <a href="${article.url}" class="post-card">
        <div class="post-meta">
          <span class="post-category">${article.category || '未分类'}</span>
          ${article.difficulty ? `<span class="post-difficulty">${article.difficulty}</span>` : ''}
        </div>
        <h3 class="post-title">${article.title}</h3>
        <p class="post-excerpt">${article.description || '暂无描述'}</p>
        ${
            article.keywords
                ? `
          <div class="post-tags">
            ${article.keywords
                .split(' ')
                .slice(0, 3)
                .map((tag) => `<span class="post-tag">${tag}</span>`)
                .join('')}
          </div>
        `
                : ''
        }
      </a>
    `
            )
            .join('');
    }

    updateFilterCount(count) {
        const countElement = document.getElementById('filter-count');
        if (countElement) {
            countElement.textContent = `找到 ${count} 篇文章`;
        }
    }

    resetFilters() {
        this.activeFilters = {
            category: null,
            difficulty: null,
            tags: [],
        };

        document.getElementById('category-filter')?.value = '';
        document.getElementById('difficulty-filter')?.value = '';

        document.querySelectorAll('.tag-btn.active').forEach((btn) => {
            btn.classList.remove('active');
        });

        this.applyFilters();
    }
}

const articleFilter = new ArticleFilter();

if (typeof module !== 'undefined' && module.exports) {
    module.exports = ArticleFilter;
}
