/**
 * 分析仪表板
 * 显示用户行为统计和分析数据
 */

class AnalyticsDashboard {
  constructor() {
    this.analytics = window.analytics;
    this.container = null;
  }

  /**
   * 初始化仪表板
   */
  init(containerSelector = '.analytics-dashboard') {
    this.container = document.querySelector(containerSelector);
    if (!this.container) {
      console.log('未找到分析仪表板容器');
      return;
    }

    this.render();
  }

  /**
   * 渲染仪表板
   */
  render() {
    const stats = this.analytics.getStats();

    this.container.innerHTML = `
      <div class="analytics-header">
        <h2 class="analytics-title">
          <i class="fa fa-chart-line"></i>
          用户行为统计
        </h2>
        <div class="analytics-actions">
          <button class="btn-export" onclick="analyticsDashboard.exportData()">
            <i class="fa fa-download"></i> 导出数据
          </button>
          <button class="btn-clear" onclick="analyticsDashboard.clearData()">
            <i class="fa fa-trash-o"></i> 清除数据
          </button>
        </div>
      </div>

      <div class="analytics-overview">
        ${this.renderOverviewCards(stats)}
      </div>

      <div class="analytics-charts">
        <div class="chart-section">
          <h3 class="chart-title">
            <i class="fa fa-file-text-o"></i>
            热门页面
          </h3>
          <div class="chart-content">
            ${this.renderTopPages(stats.topPages)}
          </div>
        </div>

        <div class="chart-section">
          <h3 class="chart-title">
            <i class="fa fa-search"></i>
            搜索关键词
          </h3>
          <div class="chart-content">
            ${this.renderTopSearchTerms(stats.topSearchTerms)}
          </div>
        </div>
      </div>

      <div class="analytics-details">
        <div class="detail-section">
          <h3 class="detail-title">
            <i class="fa fa-clock-o"></i>
            访问信息
          </h3>
          <div class="detail-content">
            ${this.renderVisitInfo(stats)}
          </div>
        </div>

        <div class="detail-section">
          <h3 class="detail-title">
            <i class="fa fa-desktop"></i>
            会话信息
          </h3>
          <div class="detail-content">
            ${this.renderSessionInfo()}
          </div>
        </div>
      </div>
    `;
  }

  /**
   * 渲染概览卡片
   */
  renderOverviewCards(stats) {
    const cards = [
      {
        icon: 'fa-eye',
        title: '总浏览量',
        value: stats.totalViews,
        color: '#3498db'
      },
      {
        icon: 'fa-file-o',
        title: '页面数',
        value: stats.totalPages,
        color: '#2ecc71'
      },
      {
        icon: 'fa-search',
        title: '搜索次数',
        value: stats.totalSearches,
        color: '#f39c12'
      },
      {
        icon: 'fa-mouse-pointer',
        title: '点击次数',
        value: stats.totalClicks,
        color: '#e74c3c'
      },
      {
        icon: 'fa-users',
        title: '会话数',
        value: stats.sessions,
        color: '#9b59b6'
      }
    ];

    return cards.map(card => `
      <div class="overview-card" style="border-left-color: ${card.color}">
        <div class="card-icon" style="background-color: ${card.color}20">
          <i class="fa ${card.icon}" style="color: ${card.color}"></i>
        </div>
        <div class="card-content">
          <div class="card-value">${this.formatNumber(card.value)}</div>
          <div class="card-title">${card.title}</div>
        </div>
      </div>
    `).join('');
  }

  /**
   * 渲染热门页面
   */
  renderTopPages(topPages) {
    if (!topPages || topPages.length === 0) {
      return '<div class="no-data">暂无数据</div>';
    }

    const maxViews = Math.max(...topPages.map(([, page]) => page.count));

    return `
      <div class="top-list">
        ${topPages.map(([path, page], index) => `
          <div class="top-item">
            <div class="top-rank">${index + 1}</div>
            <div class="top-content">
              <div class="top-name">
                <a href="${path}" title="${page.title}">${page.title}</a>
              </div>
              <div class="top-path">${path}</div>
            </div>
            <div class="top-value">${page.count}</div>
            <div class="top-bar">
              <div class="bar-fill" style="width: ${(page.count / maxViews) * 100}%"></div>
            </div>
          </div>
        `).join('')}
      </div>
    `;
  }

  /**
   * 渲染热门搜索词
   */
  renderTopSearchTerms(topSearchTerms) {
    if (!topSearchTerms || topSearchTerms.length === 0) {
      return '<div class="no-data">暂无数据</div>';
    }

    const maxCount = Math.max(...topSearchTerms.map(([, count]) => count));

    return `
      <div class="top-list">
        ${topSearchTerms.slice(0, 10).map(([term, count], index) => `
          <div class="top-item">
            <div class="top-rank">${index + 1}</div>
            <div class="top-content">
              <div class="top-name">${term}</div>
            </div>
            <div class="top-value">${count}</div>
            <div class="top-bar">
              <div class="bar-fill" style="width: ${(count / maxCount) * 100}%"></div>
            </div>
          </div>
        `).join('')}
      </div>
    `;
  }

  /**
   * 渲染访问信息
   */
  renderVisitInfo(stats) {
    const firstVisit = new Date(stats.firstVisit);
    const lastVisit = new Date(stats.lastVisit);
    const now = new Date();

    return `
      <div class="info-list">
        <div class="info-item">
          <div class="info-label">首次访问</div>
          <div class="info-value">${this.formatDate(firstVisit)}</div>
        </div>
        <div class="info-item">
          <div class="info-label">最近访问</div>
          <div class="info-value">${this.formatDate(lastVisit)}</div>
        </div>
        <div class="info-item">
          <div class="info-label">访问时长</div>
          <div class="info-value">${this.calculateDuration(firstVisit, now)}</div>
        </div>
        <div class="info-item">
          <div class="info-label">当前日期</div>
          <div class="info-value">${now.toLocaleDateString('zh-CN')}</div>
        </div>
      </div>
    `;
  }

  /**
   * 渲染会话信息
   */
  renderSessionInfo() {
    const session = this.analytics.getCurrentSession();

    if (!session) {
      return '<div class="no-data">无活跃会话</div>';
    }

    return `
      <div class="info-list">
        <div class="info-item">
          <div class="info-label">会话 ID</div>
          <div class="info-value">${session.id}</div>
        </div>
        <div class="info-item">
          <div class="info-label">开始时间</div>
          <div class="info-value">${this.formatDate(new Date(session.startTime))}</div>
        </div>
        <div class="info-item">
          <div class="info-label">浏览页面</div>
          <div class="info-value">${session.pageViews}</div>
        </div>
        <div class="info-item">
          <div class="info-label">会话时长</div>
          <div class="info-value">${this.formatDuration(session.duration)}</div>
        </div>
        <div class="info-item">
          <div class="info-label">来源</div>
          <div class="info-value">${session.referrer || '直接访问'}</div>
        </div>
        <div class="info-item">
          <div class="info-label">屏幕分辨率</div>
          <div class="info-value">${session.screen.width} × ${session.screen.height}</div>
        </div>
      </div>
    `;
  }

  /**
   * 格式化数字
   */
  formatNumber(num) {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
  }

  /**
   * 格式化日期
   */
  formatDate(date) {
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  /**
   * 计算时长
   */
  calculateDuration(start, end) {
    const diff = end - start;
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));

    if (days > 0) return `${days}天${hours}小时`;
    if (hours > 0) return `${hours}小时${minutes}分钟`;
    return `${minutes}分钟`;
  }

  /**
   * 格式化时长
   */
  formatDuration(ms) {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);

    if (hours > 0) return `${hours}小时${minutes % 60}分钟`;
    if (minutes > 0) return `${minutes}分钟${seconds % 60}秒`;
    return `${seconds}秒`;
  }

  /**
   * 导出数据
   */
  exportData() {
    if (confirm('确定要导出分析数据吗？')) {
      this.analytics.exportData();
    }
  }

  /**
   * 清除数据
   */
  clearData() {
    if (confirm('确定要清除所有分析数据吗？此操作不可恢复！')) {
      this.analytics.clearAllData();
      this.render();
    }
  }

  /**
   * 刷新数据
   */
  refresh() {
    this.render();
  }
}

// 创建全局实例
const analyticsDashboard = new AnalyticsDashboard();

// 导出供其他模块使用
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AnalyticsDashboard;
}