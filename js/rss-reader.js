/**
 * RSS/Atom 订阅阅读器
 * 支持解析和展示 RSS/Atom feed 内容
 */

class RSSReader {
  constructor() {
    this.cacheKey = 'rss-feed-cache';
    this.cacheExpiry = 30 * 60 * 1000; // 30分钟缓存
    this.feedUrls = [
      {
        name: '技术博客',
        url: './blog/feed.xml',
        enabled: true
      },
      {
        name: '精选文章',
        url: './blog/featured-feed.xml',
        enabled: false
      }
    ];
  }

  /**
   * 获取缓存的 RSS 数据
   */
  getCachedData(url) {
    try {
      const cached = localStorage.getItem(`${this.cacheKey}-${url}`);
      if (!cached) return null;

      const data = JSON.parse(cached);
      const now = Date.now();

      if (now - data.timestamp > this.cacheExpiry) {
        localStorage.removeItem(`${this.cacheKey}-${url}`);
        return null;
      }

      return data.content;
    } catch (error) {
      console.warn('读取 RSS 缓存失败:', error);
      return null;
    }
  }

  /**
   * 缓存 RSS 数据
   */
  cacheData(url, data) {
    try {
      const cacheEntry = {
        timestamp: Date.now(),
        content: data
      };
      localStorage.setItem(`${this.cacheKey}-${url}`, JSON.stringify(cacheEntry));
    } catch (error) {
      console.warn('缓存 RSS 数据失败:', error);
    }
  }

  /**
   * 解析 XML 字符串为 DOM 对象
   */
  parseXML(xmlString) {
    const parser = new DOMParser();
    return parser.parseFromString(xmlString, 'text/xml');
  }

  /**
   * 解析 RSS feed
   */
  parseRSS(xmlDoc) {
    const items = xmlDoc.querySelectorAll('item');
    const articles = [];

    items.forEach(item => {
      const title = item.querySelector('title')?.textContent || '';
      const link = item.querySelector('link')?.textContent || '';
      const description = item.querySelector('description')?.textContent || '';
      const pubDate = item.querySelector('pubDate')?.textContent || '';
      const author = item.querySelector('author')?.textContent || '';
      const category = item.querySelector('category')?.textContent || '';

      // 从描述中提取纯文本
      const plainDescription = this.stripHTML(description);

      articles.push({
        title: title.trim(),
        link: link.trim(),
        description: plainDescription.trim(),
        pubDate: pubDate ? new Date(pubDate) : new Date(),
        author: author.trim(),
        category: category.trim(),
        type: 'rss'
      });
    });

    return articles;
  }

  /**
   * 解析 Atom feed
   */
  parseAtom(xmlDoc) {
    const entries = xmlDoc.querySelectorAll('entry');
    const articles = [];

    entries.forEach(entry => {
      const title = entry.querySelector('title')?.textContent || '';
      const link = entry.querySelector('link')?.getAttribute('href') || '';
      const content = entry.querySelector('content')?.textContent || entry.querySelector('summary')?.textContent || '';
      const published = entry.querySelector('published')?.textContent || entry.querySelector('updated')?.textContent || '';
      const author = entry.querySelector('author name')?.textContent || '';
      const category = entry.querySelector('category')?.getAttribute('term') || '';

      const plainDescription = this.stripHTML(content);

      articles.push({
        title: title.trim(),
        link: link.trim(),
        description: plainDescription.trim(),
        pubDate: published ? new Date(published) : new Date(),
        author: author.trim(),
        category: category.trim(),
        type: 'atom'
      });
    });

    return articles;
  }

  /**
   * 去除 HTML 标签，提取纯文本
   */
  stripHTML(html) {
    const temp = document.createElement('div');
    temp.innerHTML = html;
    return temp.textContent || temp.innerText || '';
  }

  /**
   * 截取文本
   */
  truncate(text, maxLength = 150) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength).trim() + '...';
  }

  /**
   * 格式化日期
   */
  formatDate(date) {
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) {
      const diffHours = Math.floor(diffTime / (1000 * 60 * 60));
      if (diffHours === 0) {
        const diffMinutes = Math.floor(diffTime / (1000 * 60));
        return diffMinutes <= 1 ? '刚刚' : `${diffMinutes}分钟前`;
      }
      return `${diffHours}小时前`;
    }
    if (diffDays === 1) return '昨天';
    if (diffDays < 7) return `${diffDays}天前`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)}周前`;
    if (diffDays < 365) return `${Math.floor(diffDays / 30)}月前`;
    return `${Math.floor(diffDays / 365)}年前`;
  }

  /**
   * 获取单个 feed
   */
  async fetchFeed(feedConfig) {
    try {
      // 检查缓存
      const cached = this.getCachedData(feedConfig.url);
      if (cached) {
        console.log(`使用缓存的 RSS 数据: ${feedConfig.name}`);
        return cached;
      }

      // 获取新数据
      console.log(`从 URL 获取 RSS 数据: ${feedConfig.url}`);
      const response = await fetch(feedConfig.url);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const xmlText = await response.text();
      const xmlDoc = this.parseXML(xmlText);

      // 检测 feed 类型
      const isRSS = xmlDoc.querySelector('rss');
      const isAtom = xmlDoc.querySelector('feed');

      let articles = [];
      if (isRSS) {
        articles = this.parseRSS(xmlDoc);
      } else if (isAtom) {
        articles = this.parseAtom(xmlDoc);
      } else {
        console.warn('无法识别的 feed 格式');
        return [];
      }

      // 缓存数据
      this.cacheData(feedConfig.url, articles);

      return articles;
    } catch (error) {
      console.error(`获取 RSS feed 失败 (${feedConfig.name}):`, error);
      return [];
    }
  }

  /**
   * 获取所有 feeds
   */
  async fetchAllFeeds() {
    const promises = this.feedUrls
      .filter(feed => feed.enabled)
      .map(feed => this.fetchFeed(feed));

    const results = await Promise.all(promises);

    // 合并所有文章并按日期排序
    const allArticles = results.flat().sort((a, b) => b.pubDate - a.pubDate);

    return allArticles;
  }

  /**
   * 生成 feed XML (用于创建 RSS feed)
   */
  generateFeedXML(articles, config = {}) {
    const { title = 'CodeClub Blog', description = '技术博客', link = 'https://jacksoncode.github.io/blog/' } = config;

    let xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>${title}</title>
    <description>${description}</description>
    <link>${link}</link>
    <atom:link href="${link}feed.xml" rel="self" type="application/rss+xml"/>
    <language>zh-CN</language>
    <lastBuildDate>${new Date().toUTCString()}</lastBuildDate>
`;

    articles.forEach(article => {
      xml += `    <item>
      <title><![CDATA[${article.title}]]></title>
      <link>${article.link}</link>
      <description><![CDATA[${article.description}]]></description>
      <pubDate>${article.pubDate.toUTCString()}</pubDate>
      <author>${article.author}</author>
      <category><![CDATA[${article.category}]]></category>
    </item>
`;
    });

    xml += `  </channel>
</rss>`;

    return xml;
  }

  /**
   * 从 HTML 页面提取文章信息
   */
  extractArticlesFromHTML(htmlContent) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(htmlContent, 'text/html');
    const articles = [];

    // 提取文章卡片
    const articleCards = doc.querySelectorAll('.post-card, .blog-post, article');

    articleCards.forEach(card => {
      const titleEl = card.querySelector('h1, h2, h3, .post-title, .blog-title');
      const linkEl = card.querySelector('a[href]');
      const excerptEl = card.querySelector('.post-excerpt, .blog-excerpt, p');
      const dateEl = card.querySelector('.post-date, .blog-date, time');
      const categoryEl = card.querySelector('.post-category, .blog-category');

      if (titleEl && linkEl) {
        articles.push({
          title: titleEl.textContent.trim(),
          link: linkEl.getAttribute('href'),
          description: excerptEl ? excerptEl.textContent.trim() : '',
          pubDate: dateEl ? new Date(dateEl.textContent.trim()) : new Date(),
          author: 'Jackson',
          category: categoryEl ? categoryEl.textContent.trim() : '技术博客',
          type: 'html'
        });
      }
    });

    return articles;
  }

  /**
   * 自动生成 RSS feed
   */
  async generateRSSFromBlogPages() {
    try {
      const response = await fetch('./blog.html');
      const htmlContent = await response.text();

      const articles = this.extractArticlesFromHTML(htmlContent);

      if (articles.length === 0) {
        console.warn('未找到文章信息');
        return;
      }

      // 生成 RSS XML
      const rssXML = this.generateFeedXML(articles, {
        title: 'CodeClub 技术博客',
        description: '分享编程心得、技术文章和学习笔记',
        link: 'https://jacksoncode.github.io/blog/'
      });

      return rssXML;
    } catch (error) {
      console.error('生成 RSS feed 失败:', error);
      return null;
    }
  }
}

// 创建全局实例
const rssReader = new RSSReader();

// 导出供其他模块使用
if (typeof module !== 'undefined' && module.exports) {
  module.exports = RSSReader;
}