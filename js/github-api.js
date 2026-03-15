/**
 * GitHub API 集成模块
 * 用于获取 GitHub 仓库统计信息和动态数据
 */

class GitHubAPI {
  constructor(username = 'jacksoncode', repository = 'jacksoncode.github.io') {
    this.username = username;
    this.repository = repository;
    this.baseURL = 'https://api.github.com';
    this.cacheKey = 'github-data-cache';
    this.cacheExpiry = 15 * 60 * 1000; // 15分钟缓存
  }

  /**
   * 获取缓存的 GitHub 数据
   */
  getCachedData() {
    try {
      const cached = localStorage.getItem(this.cacheKey);
      if (!cached) return null;

      const data = JSON.parse(cached);
      const now = Date.now();

      // 检查缓存是否过期
      if (now - data.timestamp > this.cacheExpiry) {
        localStorage.removeItem(this.cacheKey);
        return null;
      }

      return data.content;
    } catch (error) {
      console.warn('读取缓存失败:', error);
      return null;
    }
  }

  /**
   * 缓存 GitHub 数据
   */
  cacheData(data) {
    try {
      const cacheEntry = {
        timestamp: Date.now(),
        content: data
      };
      localStorage.setItem(this.cacheKey, JSON.stringify(cacheEntry));
    } catch (error) {
      console.warn('缓存数据失败:', error);
    }
  }

  /**
   * 获取仓库基本信息
   */
  async getRepositoryInfo() {
    try {
      const response = await fetch(
        `${this.baseURL}/repos/${this.username}/${this.repository}`
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('获取仓库信息失败:', error);
      return null;
    }
  }

  /**
   * 获取仓库 star 数
   */
  async getStarCount() {
    try {
      const response = await fetch(
        `${this.baseURL}/repos/${this.username}/${this.repository}`
      );
      const data = await response.json();
      return data.stargazers_count || 0;
    } catch (error) {
      console.error('获取 star 数失败:', error);
      return 0;
    }
  }

  /**
   * 获取最新提交记录
   */
  async getRecentCommits(limit = 5) {
    try {
      const response = await fetch(
        `${this.baseURL}/repos/${this.username}/${this.repository}/commits?per_page=${limit}`
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('获取提交记录失败:', error);
      return [];
    }
  }

  /**
   * 获取 issues 数量
   */
  async getIssuesCount() {
    try {
      const response = await fetch(
        `${this.baseURL}/repos/${this.username}/${this.repository}`
      );
      const data = await response.json();
      return data.open_issues_count || 0;
    } catch (error) {
      console.error('获取 issues 数失败:', error);
      return 0;
    }
  }

  /**
   * 获取贡献者统计
   */
  async getContributors() {
    try {
      const response = await fetch(
        `${this.baseURL}/repos/${this.username}/${this.repository}/contributors`
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('获取贡献者失败:', error);
      return [];
    }
  }

  /**
   * 获取语言分布
   */
  async getLanguages() {
    try {
      const response = await fetch(
        `${this.baseURL}/repos/${this.username}/${this.repository}/languages`
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('获取语言分布失败:', error);
      return {};
    }
  }

  /**
   * 获取所有统计数据（带缓存）
   */
  async getAllStats() {
    // 尝试从缓存获取
    const cached = this.getCachedData();
    if (cached) {
      console.log('使用缓存的 GitHub 数据');
      return cached;
    }

    // 缓存未命中，获取新数据
    console.log('从 GitHub API 获取新数据');

    try {
      const [repoInfo, commits, contributors, languages] = await Promise.all([
        this.getRepositoryInfo(),
        this.getRecentCommits(),
        this.getContributors(),
        this.getLanguages()
      ]);

      const stats = {
        repository: {
          name: repoInfo?.full_name || '',
          description: repoInfo?.description || '',
          stars: repoInfo?.stargazers_count || 0,
          forks: repoInfo?.forks_count || 0,
          issues: repoInfo?.open_issues_count || 0,
          watchers: repoInfo?.subscribers_count || 0,
          createdAt: repoInfo?.created_at || '',
          updatedAt: repoInfo?.updated_at || '',
          url: repoInfo?.html_url || ''
        },
        recentCommits: commits.map(commit => ({
          sha: commit.sha.substring(0, 7),
          message: commit.commit.message.split('\n')[0],
          author: commit.commit.author.name,
          date: commit.commit.author.date,
          url: commit.html_url
        })),
        contributors: contributors.map(contributor => ({
          login: contributor.login,
          contributions: contributor.contributions,
          avatar: contributor.avatar_url,
          url: contributor.html_url
        })),
        languages: languages,
        lastUpdate: new Date().toISOString()
      };

      // 缓存数据
      this.cacheData(stats);

      return stats;
    } catch (error) {
      console.error('获取 GitHub 统计数据失败:', error);
      return null;
    }
  }

  /**
   * 格式化日期
   */
  formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return '今天';
    if (diffDays === 1) return '昨天';
    if (diffDays < 7) return `${diffDays}天前`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)}周前`;
    if (diffDays < 365) return `${Math.floor(diffDays / 30)}月前`;
    return `${Math.floor(diffDays / 365)}年前`;
  }

  /**
   * 格式化数字（添加千位分隔符）
   */
  formatNumber(num) {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
  }
}

// 创建全局实例
const githubAPI = new GitHubAPI();

// 导出供其他模块使用
if (typeof module !== 'undefined' && module.exports) {
  module.exports = GitHubAPI;
}