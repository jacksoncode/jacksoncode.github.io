/**
 * RSS 订阅显示模块
 * 负责在页面上显示 RSS 订阅内容
 */

class RSSDisplay {
  constructor() {
    this.rssReader = rssReader;
    this.maxArticles = 10;
  }

  /**
   * 初始化 RSS 显示
   */
  async init() {
    console.log('初始化 RSS 显示...');

    const container = document.querySelector('.rss-feed-container');
    if (!container) {
      console.log('未找到 RSS 显示容器');
      return;
    }

    // 显示加载状态
    this.showLoading(container);

    try {
      // 获取 RSS 数据
      const articles = await this.rssReader.fetchAllFeeds();

      if (articles.length === 0) {
        this.showEmpty(container);
        return;
      }

      // 显示文章
      this.displayArticles(container, articles.slice(0, this.maxArticles));

      console.log(`RSS 显示完成，共 ${articles.length} 篇文章`);
    } catch (error) {
      console.error('RSS 显示失败:', error);
      this.showError(container);
    }
  }

  /**
   * 显示加载状态
   */
  showLoading(container) {
    container.innerHTML = `
      <div class="rss-loading">
        <i class="fa fa-spinner fa-spin"></i>
        <span>正在加载订阅内容...</span>
      </div>
    `;
  }

  /**
   * 显示错误信息
   */
  showError(container) {
    container.innerHTML = `
      <div class="rss-error">
        <i class="fa fa-exclamation-circle"></i>
        <span>无法加载订阅内容</span>
        <button class="retry-btn" onclick="rssDisplay.init()">
          <i class="fa fa-refresh"></i> 重试
        </button>
      </div>
    `;
  }

  /**
   * 显示空状态
   */
  showEmpty(container) {
    container.innerHTML = `
      <div class="rss-empty">
        <i class="fa fa-rss"></i>
        <span>暂无订阅内容</span>
        <p>敬请期待更多精彩文章</p>
      </div>
    `;
  }

  /**
   * 显示文章列表
   */
  displayArticles(container, articles) {
    const html = `
      <div class="rss-feed-header">
        <div class="rss-feed-title">
          <i class="fa fa-rss"></i>
          <span>最新订阅</span>
        </div>
        <div class="rss-feed-meta">
          <span class="article-count">${articles.length} 篇文章</span>
          <span class="last-update">更新于 ${new Date().toLocaleString('zh-CN')}</span>
        </div>
      </div>

      <div class="rss-articles-list">
        ${articles.map((article, index) => this.renderArticle(article, index)).join('')}
      </div>

      <div class="rss-feed-footer">
        <a href="./blog.html" class="view-all-link">
          查看全部文章 <i class="fa fa-arrow-right"></i>
        </a>
        <a href="./blog/feed.xml" class="rss-link" target="_blank" title="RSS 订阅">
          <i class="fa fa-rss"></i> RSS
        </a>
      </div>
    `;

    container.innerHTML = html;
    container.classList.remove('rss-loading');
  }

  /**
   * 渲染单篇文章
   */
  renderArticle(article, index) {
    const truncatedDesc = this.rssReader.truncate(article.description, 120);
    const formattedDate = this.rssReader.formatDate(article.pubDate);
    const animationDelay = index * 0.1;

    return `
      <article class="rss-article" style="animation-delay: ${animationDelay}s">
        <div class="article-header">
          <div class="article-category">${article.category || '未分类'}</div>
          <div class="article-date">
            <i class="fa fa-clock-o"></i>
            <time datetime="${article.pubDate.toISOString()}">${formattedDate}</time>
          </div>
        </div>

        <h3 class="article-title">
          <a href="${article.link}" title="${article.title}">
            ${article.title}
          </a>
        </h3>

        <p class="article-description">${truncatedDesc}</p>

        <div class="article-footer">
          <div class="article-author">
            <i class="fa fa-user"></i>
            <span>${article.author || 'Jackson'}</span>
          </div>
          <a href="${article.link}" class="read-more-link">
            阅读全文 <i class="fa fa-arrow-right"></i>
          </a>
        </div>
      </article>
    `;
  }

  /**
   * 创建 RSS 订阅按钮
   */
  createRSSButton() {
    const button = document.createElement('a');
    button.href = './blog/feed.xml';
    button.className = 'rss-subscribe-button';
    button.target = '_blank';
    button.title = '订阅 RSS';
    button.innerHTML = '<i class="fa fa-rss"></i> RSS 订阅';

    return button;
  }

  /**
   * 在指定位置插入 RSS 按钮
   */
  insertRSSButton(selector) {
    const container = document.querySelector(selector);
    if (container) {
      container.appendChild(this.createRSSButton());
    }
  }

  /**
   * 手动刷新
   */
  async refresh() {
    console.log('刷新 RSS 数据...');
    localStorage.removeItem('rss-feed-cache');
    await this.init();
  }

  /**
   * 设置最大文章数
   */
  setMaxArticles(count) {
    this.maxArticles = count;
  }
}

// 创建全局实例
const rssDisplay = new RSSDisplay();

// 页面加载完成后自动初始化
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => rssDisplay.init());
} else {
  rssDisplay.init();
}

// 导出供其他模块使用
if (typeof module !== 'undefined' && module.exports) {
  module.exports = RSSDisplay;
}