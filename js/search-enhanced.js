/**
 * 增强搜索功能
 * 支持搜索历史、自动建议和智能搜索
 */

class EnhancedSearch {
  constructor() {
    this.searchHistoryKey = 'search-history';
    this.maxHistoryItems = 10;
    this.searchHistory = this.loadSearchHistory();
    this.suggestionsCache = {};
    this.searchData = [];
    this.init();
  }

  /**
   * 初始化
   */
  init() {
    this.loadSearchData();
    this.setupSearchUI();
    this.setupKeyboardShortcuts();
  }

  /**
   * 加载搜索数据
   */
  async loadSearchData() {
    try {
      // 从 JSON 数据加载
      const response = await fetch('./data/search-index.json');
      if (response.ok) {
        this.searchData = await response.json();
        console.log(`加载了 ${this.searchData.length} 条搜索数据`);
      } else {
        // 如果没有搜索索引，使用导航数据
        const navResponse = await fetch('./data/nav.json');
        const navData = await navResponse.json();
        this.searchData = this.extractSearchData(navData);
        console.log(`从导航数据提取了 ${this.searchData.length} 条搜索数据`);
      }
    } catch (error) {
      console.error('加载搜索数据失败:', error);
    }
  }

  /**
   * 从导航数据提取搜索数据
   */
  extractSearchData(navData) {
    const results = [];

    if (navData.categories) {
      navData.categories.forEach(category => {
        if (category.links) {
          category.links.forEach(link => {
            results.push({
              title: link.name,
              url: link.url,
              category: category.name,
              description: link.description || `来自 ${category.name}`,
              keywords: [link.name, category.name].join(' '),
              type: 'link'
            });
          });
        }
      });
    }

    return results;
  }

  /**
   * 加载搜索历史
   */
  loadSearchHistory() {
    try {
      const history = localStorage.getItem(this.searchHistoryKey);
      return history ? JSON.parse(history) : [];
    } catch (error) {
      console.error('加载搜索历史失败:', error);
      return [];
    }
  }

  /**
   * 保存搜索历史
   */
  saveSearchHistory() {
    try {
      localStorage.setItem(this.searchHistoryKey, JSON.stringify(this.searchHistory));
    } catch (error) {
      console.error('保存搜索历史失败:', error);
    }
  }

  /**
   * 添加搜索历史
   */
  addSearchHistory(query) {
    const trimmedQuery = query.trim();
    if (!trimmedQuery) return;

    // 移除重复项
    this.searchHistory = this.searchHistory.filter(item => item !== trimmedQuery);

    // 添加到开头
    this.searchHistory.unshift(trimmedQuery);

    // 限制数量
    if (this.searchHistory.length > this.maxHistoryItems) {
      this.searchHistory = this.searchHistory.slice(0, this.maxHistoryItems);
    }

    this.saveSearchHistory();
  }

  /**
   * 清除搜索历史
   */
  clearSearchHistory() {
    this.searchHistory = [];
    this.saveSearchHistory();
  }

  /**
   * 设置搜索 UI
   */
  setupSearchUI() {
    // 查找或创建搜索框
    const searchInput = document.getElementById('search-input') || document.querySelector('.search-input');
    if (searchInput) {
      this.setupSearchInput(searchInput);
    }

    // 创建搜索建议容器
    this.createSuggestionsContainer();
  }

  /**
   * 设置搜索输入框
   */
  setupSearchInput(input) {
    this.searchInput = input;

    // 输入事件
    input.addEventListener('input', (e) => {
      this.handleInput(e.target.value);
    });

    // 焦点事件
    input.addEventListener('focus', () => {
      this.showSuggestions();
    });

    // 失去焦点事件（延迟隐藏）
    input.addEventListener('blur', () => {
      setTimeout(() => this.hideSuggestions(), 200);
    });

    // 键盘事件
    input.addEventListener('keydown', (e) => {
      this.handleKeydown(e);
    });
  }

  /**
   * 创建建议容器
   */
  createSuggestionsContainer() {
    const container = document.createElement('div');
    container.className = 'search-suggestions-container';
    container.id = 'search-suggestions';
    document.body.appendChild(container);

    this.suggestionsContainer = container;
  }

  /**
   * 处理输入
   */
  handleInput(value) {
    if (value.trim()) {
      this.showSuggestions(value);
    } else {
      this.showSuggestions();
    }
  }

  /**
   * 显示建议
   */
  showSuggestions(query = '') {
    if (!this.suggestionsContainer) return;

    let suggestionsHTML = '';

    // 搜索建议
    if (query.trim()) {
      const suggestions = this.getSuggestions(query);
      if (suggestions.length > 0) {
        suggestionsHTML += `
          <div class="suggestions-section">
            <div class="suggestions-header">搜索建议</div>
            <div class="suggestions-list">
              ${suggestions.map(item => this.renderSuggestionItem(item)).join('')}
            </div>
          </div>
        `;
      }
    }

    // 搜索历史
    if (this.searchHistory.length > 0 && !query.trim()) {
      suggestionsHTML += `
        <div class="suggestions-section">
          <div class="suggestions-header">
            <span>搜索历史</span>
            <button class="clear-history-btn" onclick="enhancedSearch.clearSearchHistory()">
              <i class="fa fa-trash-o"></i> 清除
            </button>
          </div>
          <div class="suggestions-list history-list">
            ${this.searchHistory.map(item => this.renderHistoryItem(item)).join('')}
          </div>
        </div>
      `;
    }

    // 热门搜索
    if (!query.trim()) {
      const popularSearches = this.getPopularSearches();
      if (popularSearches.length > 0) {
        suggestionsHTML += `
          <div class="suggestions-section">
            <div class="suggestions-header">热门搜索</div>
            <div class="suggestions-list popular-list">
              ${popularSearches.map(item => this.renderPopularItem(item)).join('')}
            </div>
          </div>
        `;
      }
    }

    this.suggestionsContainer.innerHTML = suggestionsHTML;
    this.suggestionsContainer.style.display = 'block';
  }

  /**
   * 隐藏建议
   */
  hideSuggestions() {
    if (this.suggestionsContainer) {
      this.suggestionsContainer.style.display = 'none';
    }
  }

  /**
   * 获取搜索建议
   */
  getSuggestions(query) {
    const lowerQuery = query.toLowerCase();
    return this.searchData
      .filter(item =>
        item.title.toLowerCase().includes(lowerQuery) ||
        (item.description && item.description.toLowerCase().includes(lowerQuery)) ||
        (item.keywords && item.keywords.toLowerCase().includes(lowerQuery))
      )
      .slice(0, 5);
  }

  /**
   * 获取热门搜索
   */
  getPopularSearches() {
    return [
      { title: 'Python', url: '#' },
      { title: 'JavaScript', url: '#' },
      { title: 'React', url: '#' },
      { title: 'Vue.js', url: '#' },
      { title: 'Docker', url: '#' }
    ];
  }

  /**
   * 渲染建议项
   */
  renderSuggestionItem(item) {
    return `
      <a href="${item.url}" class="suggestion-item" onclick="enhancedSearch.performSearch('${item.title}')">
        <div class="suggestion-icon">
          <i class="fa fa-${item.type === 'link' ? 'link' : 'search'}"></i>
        </div>
        <div class="suggestion-content">
          <div class="suggestion-title">${this.highlightMatch(item.title)}</div>
          <div class="suggestion-description">${item.description || ''}</div>
        </div>
      </a>
    `;
  }

  /**
   * 渲染历史项
   */
  renderHistoryItem(query) {
    return `
      <div class="suggestion-item history-item" onclick="enhancedSearch.performSearch('${query}')">
        <div class="suggestion-icon">
          <i class="fa fa-clock-o"></i>
        </div>
        <div class="suggestion-content">
          <div class="suggestion-title">${query}</div>
        </div>
      </div>
    `;
  }

  /**
   * 渲染热门项
   */
  renderPopularItem(item) {
    return `
      <a href="${item.url}" class="suggestion-item popular-item">
        <div class="suggestion-icon">
          <i class="fa fa-fire"></i>
        </div>
        <div class="suggestion-content">
          <div class="suggestion-title">${item.title}</div>
        </div>
      </a>
    `;
  }

  /**
   * 高亮匹配文本
   */
  highlightMatch(text, query) {
    if (!this.searchInput) return text;
    const queryText = this.searchInput.value.trim();
    if (!queryText) return text;

    const regex = new RegExp(`(${queryText})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
  }

  /**
   * 执行搜索
   */
  performSearch(query) {
    if (!query) return;

    // 添加到搜索历史
    this.addSearchHistory(query);

    // 更新搜索框
    if (this.searchInput) {
      this.searchInput.value = query;
    }

    // 隐藏建议
    this.hideSuggestions();

    // 执行实际搜索
    this.executeSearch(query);
  }

  /**
   * 执行搜索
   */
  executeSearch(query) {
    // 调用原有的搜索功能
    if (window.performSearch) {
      window.performSearch(query);
    } else {
      // 默认搜索行为
      const results = this.searchData.filter(item =>
        item.title.toLowerCase().includes(query.toLowerCase()) ||
        (item.description && item.description.toLowerCase().includes(query.toLowerCase()))
      );

      console.log(`搜索 "${query}" 找到 ${results.length} 个结果`);
      this.displaySearchResults(results);
    }
  }

  /**
   * 显示搜索结果
   */
  displaySearchResults(results) {
    const resultsContainer = document.getElementById('search-results') || document.querySelector('.search-results');
    if (resultsContainer) {
      if (results.length === 0) {
        resultsContainer.innerHTML = '<div class="no-results">未找到相关结果</div>';
      } else {
        resultsContainer.innerHTML = `
          <div class="results-count">找到 ${results.length} 个结果</div>
          <div class="results-list">
            ${results.map(item => `
              <a href="${item.url}" class="result-item">
                <div class="result-title">${item.title}</div>
                <div class="result-description">${item.description || ''}</div>
                <div class="result-category">${item.category || ''}</div>
              </a>
            `).join('')}
          </div>
        `;
      }
    }
  }

  /**
   * 处理键盘事件
   */
  handleKeydown(e) {
    const suggestions = this.suggestionsContainer?.querySelectorAll('.suggestion-item');
    if (!suggestions || suggestions.length === 0) return;

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      // 移动到下一个建议
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      // 移动到上一个建议
    } else if (e.key === 'Enter') {
      e.preventDefault();
      // 执行搜索
      this.performSearch(this.searchInput.value);
    } else if (e.key === 'Escape') {
      // 隐藏建议
      this.hideSuggestions();
    }
  }

  /**
   * 设置键盘快捷键
   */
  setupKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
      // Cmd/Ctrl + K 打开搜索
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (this.searchInput) {
          this.searchInput.focus();
          this.showSuggestions();
        }
      }

      // Escape 关闭搜索
      if (e.key === 'Escape' && this.searchInput === document.activeElement) {
        this.searchInput.blur();
        this.hideSuggestions();
      }
    });
  }

  /**
   * 获取搜索统计
   */
  getSearchStats() {
    return {
      totalSearches: this.searchHistory.length,
      recentSearches: this.searchHistory.slice(0, 5),
      dataCount: this.searchData.length
    };
  }
}

// 创建全局实例
const enhancedSearch = new EnhancedSearch();

// 导出供其他模块使用
if (typeof module !== 'undefined' && module.exports) {
  module.exports = EnhancedSearch;
}