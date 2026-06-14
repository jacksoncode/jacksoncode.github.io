class AIContentEnhancer {
    constructor() {
        this.articles = [];
        this.apiEndpoint = null;
        this.init();
    }

    async init() {
        await this.loadArticles();
        this.createSummaryWidget();
        this.createRecommendationWidget();
    }

    async loadArticles() {
        try {
            const response = await fetch('./data/search-index.json');
            this.articles = await response.json();
        } catch (error) {
            console.error('加载文章数据失败:', error);
        }
    }

    createSummaryWidget() {
        if (!this.isArticlePage()) return;

        const summaryWidget = document.createElement('div');
        summaryWidget.className = 'ai-summary-widget';
        summaryWidget.innerHTML = `
      <div class="summary-header">
        <i class="fas fa-robot"></i>
        <h4>AI 智能摘要</h4>
      </div>
      <div class="summary-content">
        <div class="summary-loading">
          <i class="fas fa-spinner fa-spin"></i>
          <span>正在生成摘要...</span>
        </div>
        <div class="summary-text" style="display: none;"></div>
      </div>
      <div class="summary-actions">
        <button class="regenerate-btn">
          <i class="fas fa-sync"></i> 重新生成
        </button>
        <button class="copy-btn">
          <i class="fas fa-copy"></i> 复制摘要
        </button>
      </div>
    `;

        const articleContent =
            document.querySelector('.article-content') || document.querySelector('.post-content');

        if (articleContent) {
            articleContent.insertBefore(summaryWidget, articleContent.firstChild);
            this.summaryWidget = summaryWidget;
            this.addSummaryStyles();
            this.generateSummary();
        }
    }

    isArticlePage() {
        return (
            window.location.pathname.includes('/blog/') &&
            window.location.pathname.endsWith('.html')
        );
    }

    addSummaryStyles() {
        const style = document.createElement('style');
        style.textContent = `
      .ai-summary-widget {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 24px;
        color: white;
        position: relative;
        overflow: hidden;
      }
      
      .ai-summary-widget::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        transform: translate(30%, -30%);
      }
      
      .summary-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
      }
      
      .summary-header i {
        font-size: 24px;
      }
      
      .summary-header h4 {
        margin: 0;
        font-size: 18px;
      }
      
      .summary-content {
        margin-bottom: 16px;
        min-height: 60px;
      }
      
      .summary-loading {
        display: flex;
        align-items: center;
        gap: 12px;
        opacity: 0.8;
      }
      
      .summary-text {
        font-size: 15px;
        line-height: 1.6;
        opacity: 0.95;
      }
      
      .summary-actions {
        display: flex;
        gap: 12px;
      }
      
      .regenerate-btn,
      .copy-btn {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 14px;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 6px;
        transition: all 0.2s;
      }
      
      .regenerate-btn:hover,
      .copy-btn:hover {
        background: rgba(255, 255, 255, 0.3);
        border-color: rgba(255, 255, 255, 0.4);
      }
      
      .dark-mode .ai-summary-widget {
        background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 100%);
      }
      
      @media (max-width: 768px) {
        .ai-summary-widget {
          padding: 16px;
        }
        
        .summary-actions {
          flex-direction: column;
        }
        
        .regenerate-btn,
        .copy-btn {
          width: 100%;
          justify-content: center;
        }
      }
    `;
        document.head.appendChild(style);
    }

    async generateSummary() {
        const articleContent =
            document.querySelector('.article-content') || document.querySelector('.post-content');

        if (!articleContent) return;

        const text = articleContent.textContent.trim();
        const keywords = this.extractKeywords(text);

        const summary = this.createBasicSummary(text, keywords);

        const loadingElement = this.summaryWidget?.querySelector('.summary-loading');
        const textElement = this.summaryWidget?.querySelector('.summary-text');

        if (loadingElement && textElement) {
            setTimeout(() => {
                loadingElement.style.display = 'none';
                textElement.style.display = 'block';
                textElement.textContent = summary;
            }, 1000);
        }

        this.bindSummaryActions(summary);
    }

    extractKeywords(text) {
        const words = text.split(/\s+/);
        const frequency = {};

        words.forEach((word) => {
            if (word.length > 2) {
                frequency[word] = (frequency[word] || 0) + 1;
            }
        });

        return Object.entries(frequency)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 10)
            .map((entry) => entry[0]);
    }

    createBasicSummary(text, keywords) {
        const sentences = text.split(/[.!?。!?]+/).filter((s) => s.trim().length > 20);
        const importantSentences = sentences.slice(0, 3);

        return importantSentences.join(' ').substring(0, 300) + '...';
    }

    bindSummaryActions(summary) {
        this.summaryWidget?.querySelector('.regenerate-btn')?.addEventListener('click', () => {
            this.generateSummary();
        });

        this.summaryWidget?.querySelector('.copy-btn')?.addEventListener('click', () => {
            navigator.clipboard.writeText(summary).then(() => {
                alert('摘要已复制到剪贴板!');
            });
        });
    }

    createRecommendationWidget() {
        const currentUrl = window.location.pathname;
        const currentArticle = this.articles.find((a) => a.url === currentUrl);

        if (!currentArticle) return;

        const recommendations = this.findRelatedArticles(currentArticle);

        if (recommendations.length === 0) return;

        const widget = document.createElement('div');
        widget.className = 'recommendation-widget';
        widget.innerHTML = `
      <div class="recommendation-header">
        <i class="fas fa-lightbulb"></i>
        <h4>相关推荐</h4>
      </div>
      <div class="recommendation-list">
        ${recommendations
            .map(
                (article) => `
          <a href="${article.url}" class="recommendation-item">
            <div class="recommendation-category">${article.category}</div>
            <div class="recommendation-title">${article.title}</div>
            <div class="recommendation-desc">${article.description || ''}</div>
            <div class="recommendation-tags">
              ${article.keywords
                  ?.split(' ')
                  .slice(0, 3)
                  .map((tag) => `<span class="recommendation-tag">${tag}</span>`)
                  .join('')}
            </div>
          </a>
        `
            )
            .join('')}
      </div>
    `;

        const footer = document.querySelector('.footer');
        if (footer) {
            footer.parentElement.insertBefore(widget, footer);
            this.addRecommendationStyles();
        }
    }

    findRelatedArticles(currentArticle) {
        const currentKeywords = currentArticle.keywords?.split(' ') || [];
        const currentCategory = currentArticle.category;

        return this.articles
            .filter((article) => article.url !== currentArticle.url)
            .map((article) => {
                const articleKeywords = article.keywords?.split(' ') || [];
                const commonKeywords = currentKeywords.filter((k) => articleKeywords.includes(k));

                const similarityScore =
                    commonKeywords.length * 2 + (article.category === currentCategory ? 5 : 0);

                return {
                    ...article,
                    similarityScore,
                };
            })
            .filter((article) => article.similarityScore > 0)
            .sort((a, b) => b.similarityScore - a.similarityScore)
            .slice(0, 5);
    }

    addRecommendationStyles() {
        const style = document.createElement('style');
        style.textContent = `
      .recommendation-widget {
        background: var(--bg-secondary-color);
        padding: 24px;
        border-radius: 12px;
        margin-top: 40px;
        border: 1px solid var(--border-color);
      }
      
      .recommendation-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
        color: var(--primary-color);
      }
      
      .recommendation-header h4 {
        margin: 0;
        font-size: 20px;
        color: var(--text-color);
      }
      
      .recommendation-list {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 16px;
      }
      
      .recommendation-item {
        background: var(--bg-color);
        padding: 16px;
        border-radius: 8px;
        border: 1px solid var(--border-color);
        text-decoration: none;
        transition: all 0.2s;
        display: block;
      }
      
      .recommendation-item:hover {
        border-color: var(--primary-color);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
      }
      
      .recommendation-category {
        font-size: 12px;
        color: var(--primary-color);
        font-weight: 500;
        margin-bottom: 8px;
      }
      
      .recommendation-title {
        font-size: 16px;
        font-weight: 600;
        color: var(--text-color);
        margin-bottom: 8px;
      }
      
      .recommendation-desc {
        font-size: 14px;
        color: var(--text-secondary-color);
        line-height: 1.5;
        margin-bottom: 12px;
      }
      
      .recommendation-tags {
        display: flex;
        gap: 8px;
      }
      
      .recommendation-tag {
        background: rgba(59, 130, 246, 0.1);
        color: var(--primary-color);
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
      }
      
      .dark-mode .recommendation-widget {
        background: #1f2937;
        border-color: #374151;
      }
      
      .dark-mode .recommendation-item {
        background: #374151;
        border-color: #4b5563;
      }
      
      .dark-mode .recommendation-item:hover {
        border-color: #60a5fa;
      }
      
      .dark-mode .recommendation-title {
        color: #f9fafb;
      }
      
      .dark-mode .recommendation-desc {
        color: #9ca3af;
      }
      
      .dark-mode .recommendation-tag {
        background: rgba(96, 165, 250, 0.2);
        color: #60a5fa;
      }
      
      @media (max-width: 768px) {
        .recommendation-list {
          grid-template-columns: 1fr;
        }
        
        .recommendation-widget {
          padding: 16px;
        }
      }
    `;
        document.head.appendChild(style);
    }
}

const aiContentEnhancer = new AIContentEnhancer();

if (typeof module !== 'undefined' && module.exports) {
    module.exports = AIContentEnhancer;
}
