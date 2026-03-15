/**
 * GitHub 数据显示模块
 * 负责在页面上显示 GitHub 统计信息
 */

class GitHubDisplay {
  constructor() {
    this.githubAPI = githubAPI;
    this.containerSelectors = {
      stats: '.github-stats',
      commits: '.github-commits',
      contributors: '.github-contributors',
      languages: '.github-languages'
    };
  }

  /**
   * 初始化 GitHub 数据显示
   */
  async init() {
    console.log('初始化 GitHub 数据显示...');

    // 显示加载状态
    this.showLoadingState();

    try {
      // 获取统计数据
      const stats = await this.githubAPI.getAllStats();

      if (!stats) {
        this.showError();
        return;
      }

      // 更新所有显示区域
      this.updateStats(stats);
      this.updateRecentCommits(stats);
      this.updateContributors(stats);
      this.updateLanguages(stats);

      console.log('GitHub 数据显示完成');
    } catch (error) {
      console.error('GitHub 数据显示失败:', error);
      this.showError();
    }
  }

  /**
   * 显示加载状态
   */
  showLoadingState() {
    const containers = document.querySelectorAll('.github-stats-loading');
    containers.forEach(container => {
      container.innerHTML = `
        <div class="github-loading">
          <i class="fa fa-spinner fa-spin"></i>
          <span>正在加载 GitHub 数据...</span>
        </div>
      `;
    });
  }

  /**
   * 显示错误信息
   */
  showError() {
    const containers = document.querySelectorAll('.github-stats-loading');
    containers.forEach(container => {
      container.innerHTML = `
        <div class="github-error">
          <i class="fa fa-exclamation-circle"></i>
          <span>无法加载 GitHub 数据</span>
          <button class="retry-btn" onclick="githubDisplay.init()">
            <i class="fa fa-refresh"></i> 重试
          </button>
        </div>
      `;
    });
  }

  /**
   * 更新统计数据显示
   */
  updateStats(stats) {
    const container = document.querySelector(this.containerSelectors.stats);
    if (!container) return;

    const repo = stats.repository;

    container.innerHTML = `
      <div class="github-stats-container">
        <h3 class="github-stats-title">
          <i class="fa fa-github"></i>
          GitHub 仓库统计
        </h3>

        <div class="github-stats-grid">
          <div class="stat-item">
            <i class="fa fa-star-o"></i>
            <div class="stat-content">
              <div class="stat-number">${this.githubAPI.formatNumber(repo.stars)}</div>
              <div class="stat-label">Stars</div>
            </div>
          </div>

          <div class="stat-item">
            <i class="fa fa-code-fork"></i>
            <div class="stat-content">
              <div class="stat-number">${this.githubAPI.formatNumber(repo.forks)}</div>
              <div class="stat-label">Forks</div>
            </div>
          </div>

          <div class="stat-item">
            <i class="fa fa-eye"></i>
            <div class="stat-content">
              <div class="stat-number">${this.githubAPI.formatNumber(repo.watchers)}</div>
              <div class="stat-label">Watchers</div>
            </div>
          </div>

          <div class="stat-item">
            <i class="fa fa-exclamation-circle"></i>
            <div class="stat-content">
              <div class="stat-number">${this.githubAPI.formatNumber(repo.issues)}</div>
              <div class="stat-label">Issues</div>
            </div>
          </div>
        </div>

        <div class="github-repo-info">
          <p class="repo-description">${repo.description}</p>
          <div class="repo-meta">
            <span><i class="fa fa-calendar"></i> 创建于 ${this.githubAPI.formatDate(repo.createdAt)}</span>
            <span><i class="fa fa-clock-o"></i> 更新于 ${this.githubAPI.formatDate(repo.updatedAt)}</span>
          </div>
          <a href="${repo.url}" target="_blank" class="btn-github">
            <i class="fa fa-github"></i> 查看仓库
          </a>
        </div>
      </div>
    `;

    container.classList.remove('github-stats-loading');
  }

  /**
   * 更新最近提交记录
   */
  updateRecentCommits(stats) {
    const container = document.querySelector(this.containerSelectors.commits);
    if (!container) return;

    const commits = stats.recentCommits;

    container.innerHTML = `
      <div class="github-commits-container">
        <h3 class="github-commits-title">
          <i class="fa fa-code"></i>
          最近提交
        </h3>

        <div class="commits-list">
          ${commits.map(commit => `
            <div class="commit-item">
              <div class="commit-sha">
                <a href="${commit.url}" target="_blank">${commit.sha}</a>
              </div>
              <div class="commit-message">${commit.message}</div>
              <div class="commit-meta">
                <span class="commit-author">
                  <i class="fa fa-user"></i> ${commit.author}
                </span>
                <span class="commit-date">
                  <i class="fa fa-clock-o"></i> ${this.githubAPI.formatDate(commit.date)}
                </span>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  /**
   * 更新贡献者显示
   */
  updateContributors(stats) {
    const container = document.querySelector(this.containerSelectors.contributors);
    if (!container) return;

    const contributors = stats.contributors.slice(0, 10); // 显示前10名

    container.innerHTML = `
      <div class="github-contributors-container">
        <h3 class="github-contributors-title">
          <i class="fa fa-users"></i>
          贡献者
        </h3>

        <div class="contributors-list">
          ${contributors.map(contributor => `
            <div class="contributor-item">
              <a href="${contributor.url}" target="_blank" title="${contributor.login}">
                <img src="${contributor.avatar}" alt="${contributor.login}" class="contributor-avatar">
                <div class="contributor-info">
                  <div class="contributor-name">${contributor.login}</div>
                  <div class="contributor-count">${contributor.contributions} 次提交</div>
                </div>
              </a>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  /**
   * 更新语言分布显示
   */
  updateLanguages(stats) {
    const container = document.querySelector(this.containerSelectors.languages);
    if (!container) return;

    const languages = stats.languages;
    const totalBytes = Object.values(languages).reduce((sum, bytes) => sum + bytes, 0);

    // 计算百分比并排序
    const languageStats = Object.entries(languages)
      .map(([name, bytes]) => ({
        name,
        bytes,
        percentage: ((bytes / totalBytes) * 100).toFixed(1)
      }))
      .sort((a, b) => b.percentage - a.percentage);

    container.innerHTML = `
      <div class="github-languages-container">
        <h3 class="github-languages-title">
          <i class="fa fa-code"></i>
          编程语言
        </h3>

        <div class="languages-bar">
          ${languageStats.map(lang => `
            <div class="language-segment" style="width: ${lang.percentage}%; background-color: ${this.getLanguageColor(lang.name)}" title="${lang.name}: ${lang.percentage}%"></div>
          `).join('')}
        </div>

        <div class="languages-legend">
          ${languageStats.map(lang => `
            <div class="language-item">
              <div class="language-color" style="background-color: ${this.getLanguageColor(lang.name)}"></div>
              <div class="language-name">${lang.name}</div>
              <div class="language-percentage">${lang.percentage}%</div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  /**
   * 获取语言对应的颜色
   */
  getLanguageColor(language) {
    const colors = {
      'JavaScript': '#f1e05a',
      'TypeScript': '#2b7489',
      'Python': '#3572A5',
      'Java': '#b07219',
      'C++': '#f34b7d',
      'C': '#555555',
      'C#': '#239120',
      'Ruby': '#701516',
      'PHP': '#4F5D95',
      'Swift': '#ffac45',
      'Go': '#00ADD8',
      'Rust': '#dea584',
      'HTML': '#e34c26',
      'CSS': '#563d7c',
      'Shell': '#89e051',
      'Dockerfile': '#384d54',
      'Markdown': '#083fa1'
    };

    return colors[language] || '#999999';
  }

  /**
   * 手动刷新数据
   */
  async refresh() {
    console.log('刷新 GitHub 数据...');
    localStorage.removeItem('github-data-cache');
    await this.init();
  }
}

// 创建全局实例
const githubDisplay = new GitHubDisplay();

// 页面加载完成后自动初始化
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => githubDisplay.init());
} else {
  githubDisplay.init();
}

// 导出供其他模块使用
if (typeof module !== 'undefined' && module.exports) {
  module.exports = GitHubDisplay;
}