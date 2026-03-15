/**
 * 用户行为统计系统
 * 追踪用户行为和页面统计数据
 */

class Analytics {
  constructor() {
    this.storageKey = 'analytics-data';
    this.sessionKey = 'analytics-session';
    this.analyticsData = this.loadAnalyticsData();
    this.sessionData = this.initSession();
    this.enabled = true;
    this.init();
  }

  /**
   * 初始化
   */
  init() {
    this.trackPageView();
    this.setupEventTracking();
    this.setupPerformanceTracking();
    this.startSessionTimer();
  }

  /**
   * 加载分析数据
   */
  loadAnalyticsData() {
    try {
      const data = localStorage.getItem(this.storageKey);
      return data ? JSON.parse(data) : {
        pageViews: {},
        searchTerms: [],
        clicks: [],
        sessions: [],
        firstVisit: new Date().toISOString(),
        lastVisit: new Date().toISOString()
      };
    } catch (error) {
      console.error('加载分析数据失败:', error);
      return this.getDefaultData();
    }
  }

  /**
   * 获取默认数据
   */
  getDefaultData() {
    return {
      pageViews: {},
      searchTerms: [],
      clicks: [],
      sessions: [],
      firstVisit: new Date().toISOString(),
      lastVisit: new Date().toISOString()
    };
  }

  /**
   * 保存分析数据
   */
  saveAnalyticsData() {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(this.analyticsData));
    } catch (error) {
      console.error('保存分析数据失败:', error);
    }
  }

  /**
   * 初始化会话
   */
  initSession() {
    const sessionId = this.generateSessionId();
    const session = {
      id: sessionId,
      startTime: new Date().toISOString(),
      endTime: null,
      pageViews: 0,
      duration: 0,
      referrer: document.referrer || 'direct',
      userAgent: navigator.userAgent,
      screen: {
        width: window.screen.width,
        height: window.screen.height
      },
      language: navigator.language,
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
    };

    sessionStorage.setItem(this.sessionKey, JSON.stringify(session));
    return session;
  }

  /**
   * 生成会话 ID
   */
  generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  }

  /**
   * 获取当前会话
   */
  getCurrentSession() {
    try {
      const session = sessionStorage.getItem(this.sessionKey);
      return session ? JSON.parse(session) : this.sessionData;
    } catch (error) {
      return this.sessionData;
    }
  }

  /**
   * 更新会话
   */
  updateSession(updates) {
    this.sessionData = { ...this.sessionData, ...updates };
    sessionStorage.setItem(this.sessionKey, JSON.stringify(this.sessionData));
  }

  /**
   * 开始会话计时器
   */
  startSessionTimer() {
    setInterval(() => {
      const session = this.getCurrentSession();
      const duration = Date.now() - new Date(session.startTime).getTime();
      this.updateSession({ duration });
    }, 1000);
  }

  /**
   * 追踪页面浏览
   */
  trackPageView() {
    const path = window.location.pathname;
    const title = document.title;

    // 更新页面浏览统计
    if (!this.analyticsData.pageViews[path]) {
      this.analyticsData.pageViews[path] = {
        count: 0,
        title: title,
        firstVisit: new Date().toISOString(),
        lastVisit: new Date().toISOString()
      };
    }

    this.analyticsData.pageViews[path].count++;
    this.analyticsData.pageViews[path].lastVisit = new Date().toISOString();
    this.analyticsData.lastVisit = new Date().toISOString();

    // 更新会话
    this.updateSession({ pageViews: this.sessionData.pageViews + 1 });

    this.saveAnalyticsData();
    console.log(`页面浏览追踪: ${path} (${title})`);
  }

  /**
   * 追踪搜索
   */
  trackSearch(query) {
    if (!query || !query.trim()) return;

    const searchTerm = {
      query: query.trim(),
      timestamp: new Date().toISOString(),
      results: 0,
      path: window.location.pathname
    };

    this.analyticsData.searchTerms.push(searchTerm);

    // 限制搜索历史数量
    if (this.analyticsData.searchTerms.length > 100) {
      this.analyticsData.searchTerms = this.analyticsData.searchTerms.slice(-100);
    }

    this.saveAnalyticsData();
  }

  /**
   * 追踪点击事件
   */
  trackClick(element, context = '') {
    if (!this.enabled) return;

    const clickData = {
      element: this.getElementIdentifier(element),
      text: element.textContent?.substring(0, 50) || '',
      href: element.href || '',
      context: context,
      timestamp: new Date().toISOString(),
      path: window.location.pathname
    };

    this.analyticsData.clicks.push(clickData);

    // 限制点击历史数量
    if (this.analyticsData.clicks.length > 200) {
      this.analyticsData.clicks = this.analyticsData.clicks.slice(-200);
    }

    this.saveAnalyticsData();
  }

  /**
   * 获取元素标识符
   */
  getElementIdentifier(element) {
    if (element.id) return `#${element.id}`;
    if (element.className) return `.${element.className.split(' ').join('.')}`;
    return element.tagName.toLowerCase();
  }

  /**
   * 设置事件追踪
   */
  setupEventTracking() {
    // 追踪所有链接点击
    document.addEventListener('click', (e) => {
      const link = e.target.closest('a');
      if (link) {
        this.trackClick(link, 'link');
      }
    });

    // 追踪搜索输入
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
      searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          this.trackSearch(searchInput.value);
        }
      });
    }

    // 追踪按钮点击
    document.addEventListener('click', (e) => {
      const button = e.target.closest('button');
      if (button) {
        this.trackClick(button, 'button');
      }
    });
  }

  /**
   * 设置性能追踪
   */
  setupPerformanceTracking() {
    if ('performance' in window && 'getEntriesByType' in window.performance) {
      window.addEventListener('load', () => {
        setTimeout(() => {
          const perfData = window.performance.getEntriesByType('navigation')[0];
          if (perfData) {
            this.trackPerformance(perfData);
          }
        }, 0);
      });
    }
  }

  /**
   * 追踪性能数据
   */
  trackPerformance(perfData) {
    const performanceMetrics = {
      domContentLoaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
      loadComplete: perfData.loadEventEnd - perfData.loadEventStart,
      firstPaint: this.getMetric('first-paint'),
      firstContentfulPaint: this.getMetric('first-contentful-paint'),
      timestamp: new Date().toISOString(),
      path: window.location.pathname
    };

    if (!this.analyticsData.performance) {
      this.analyticsData.performance = [];
    }

    this.analyticsData.performance.push(performanceMetrics);

    // 限制性能数据数量
    if (this.analyticsData.performance.length > 50) {
      this.analyticsData.performance = this.analyticsData.performance.slice(-50);
    }

    this.saveAnalyticsData();
    console.log('性能追踪:', performanceMetrics);
  }

  /**
   * 获取性能指标
   */
  getMetric(name) {
    const entry = window.performance.getEntriesByType('paint').find(e => e.name === name);
    return entry ? entry.startTime : null;
  }

  /**
   * 结束会话
   */
  endSession() {
    const session = this.getCurrentSession();
    session.endTime = new Date().toISOString();

    if (!this.analyticsData.sessions) {
      this.analyticsData.sessions = [];
    }

    this.analyticsData.sessions.push(session);

    // 限制会话历史数量
    if (this.analyticsData.sessions.length > 50) {
      this.analyticsData.sessions = this.analyticsData.sessions.slice(-50);
    }

    this.saveAnalyticsData();
    sessionStorage.removeItem(this.sessionKey);
  }

  /**
   * 获取统计数据
   */
  getStats() {
    const totalPages = Object.keys(this.analyticsData.pageViews).length;
    const totalViews = Object.values(this.analyticsData.pageViews)
      .reduce((sum, page) => sum + page.count, 0);

    const topPages = Object.entries(this.analyticsData.pageViews)
      .sort((a, b) => b[1].count - a[1].count)
      .slice(0, 10);

    const topSearchTerms = this.analyticsData.searchTerms
      .reduce((acc, term) => {
        acc[term.query] = (acc[term.query] || 0) + 1;
        return acc;
      }, {})
      .entries();

    return {
      totalPages,
      totalViews,
      totalSearches: this.analyticsData.searchTerms.length,
      totalClicks: this.analyticsData.clicks.length,
      topPages,
      topSearchTerms,
      firstVisit: this.analyticsData.firstVisit,
      lastVisit: this.analyticsData.lastVisit,
      sessions: this.analyticsData.sessions?.length || 0
    };
  }

  /**
   * 获取页面浏览统计
   */
  getPageStats(path) {
    return this.analyticsData.pageViews[path] || null;
  }

  /**
   * 清除所有数据
   */
  clearAllData() {
    localStorage.removeItem(this.storageKey);
    sessionStorage.removeItem(this.sessionKey);
    this.analyticsData = this.getDefaultData();
    console.log('已清除所有分析数据');
  }

  /**
   * 导出数据
   */
  exportData() {
    const data = {
      analytics: this.analyticsData,
      session: this.sessionData,
      stats: this.getStats(),
      exportDate: new Date().toISOString()
    };

    const dataStr = JSON.stringify(data, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);

    const link = document.createElement('a');
    link.href = url;
    link.download = `analytics-export-${new Date().toISOString().split('T')[0]}.json`;
    link.click();

    URL.revokeObjectURL(url);
  }

  /**
   * 启用/禁用追踪
   */
  setEnabled(enabled) {
    this.enabled = enabled;
    console.log(`分析追踪已${enabled ? '启用' : '禁用'}`);
  }
}

// 页面卸载时结束会话
window.addEventListener('beforeunload', () => {
  if (window.analytics) {
    window.analytics.endSession();
  }
});

// 创建全局实例
const analytics = new Analytics();

// 导出供其他模块使用
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Analytics;
}