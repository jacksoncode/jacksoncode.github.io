/**
 * Lunr.js 全文搜索引擎集成
 * 提供高性能的全文搜索能力
 */

class LunrSearch {
    constructor() {
        this.lunrIndex = null;
        this.searchData = [];
        this.searchIndexUrl = './data/lunr-index.json';
        this.init();
    }

    /**
     * 初始化
     */
    async init() {
        try {
            // 动态加载 Lunr.js
            await this.loadLunrLibrary();

            // 加载搜索数据
            await this.loadSearchData();

            // 构建或加载索引
            await this.buildOrLoadIndex();

            console.log('Lunr 搜索引擎已初始化');
        } catch (error) {
            console.error('初始化 Lunr 搜索失败:', error);
            // 降级到原有搜索
            this.fallbackToDefaultSearch();
        }
    }

    /**
     * 加载 Lunr.js 库
     */
    async loadLunrLibrary() {
        if (window.lunr) {
            return Promise.resolve();
        }

        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = 'https://cdnjs.cloudflare.com/ajax/libs/lunr.js/2.3.9/lunr.min.js';
            script.integrity =
                'sha512-6oK5HxNcyN3XTFFH3ArYOfxYkT6N8sJhZvVwJ6n/qEFgho9kVJn3V9Z1I6AxnlhLd7w31JQl5y7VHklSr6Zufzw==';
            script.crossOrigin = 'anonymous';

            script.onload = () => {
                console.log('Lunr.js 库加载成功');
                resolve();
            };

            script.onerror = () => {
                reject(new Error('Lunr.js 库加载失败'));
            };

            document.head.appendChild(script);
        });
    }

    /**
     * 加载搜索数据
     */
    async loadSearchData() {
        try {
            // 加载导航数据
            const navResponse = await fetch('./data/nav.json');
            const navData = await navResponse.json();

            // 加载文章索引
            const articlesResponse = await fetch('./data/search-index.json');
            const articlesData = await articlesResponse.json();

            // 合并数据
            this.searchData = [...this.extractNavData(navData), ...articlesData];

            console.log(`加载了 ${this.searchData.length} 条搜索数据`);
        } catch (error) {
            console.error('加载搜索数据失败:', error);
            this.searchData = [];
        }
    }

    /**
     * 提取导航数据
     */
    extractNavData(navData) {
        const results = [];

        if (navData.categories) {
            navData.categories.forEach((category) => {
                if (category.links) {
                    category.links.forEach((link) => {
                        results.push({
                            id: `nav-${results.length}`,
                            title: link.name,
                            url: link.url,
                            category: category.name,
                            description: link.description || `${category.name} 类别下的网站`,
                            type: 'link',
                            keywords: [link.name, category.name].join(' '),
                        });
                    });
                }
            });
        }

        return results;
    }

    /**
     * 构建或加载索引
     */
    async buildOrLoadIndex() {
        try {
            // 尝试加载预构建的索引
            const response = await fetch(this.searchIndexUrl);
            if (response.ok) {
                const indexData = await response.json();
                this.lunrIndex = lunr.Index.load(indexData);
                console.log('从缓存加载 Lunr 索引');
                return;
            }
        } catch (error) {
            console.log('没有预构建索引，将构建新索引');
        }

        // 构建新索引
        this.buildIndex();

        // 保存索引（可选）
        this.saveIndex();
    }

    /**
     * 构建 Lunr 索引
     */
    buildIndex() {
        this.lunrIndex = lunr(
            function () {
                // 配置字段
                this.ref('id');
                this.field('title', { boost: 10 });
                this.field('description', { boost: 5 });
                this.field('keywords', { boost: 3 });
                this.field('category', { boost: 2 });

                // 添加文档
                this.searchData.forEach((doc) => {
                    this.add(doc);
                });
            }.bind(this)
        );

        console.log('Lunr 索引构建完成');
    }

    /**
     * 保存索引到文件（需要后端支持）
     */
    async saveIndex() {
        try {
            const indexData = this.lunrIndex.toJSON();
            const blob = new Blob([JSON.stringify(indexData)], { type: 'application/json' });

            // 本地存储作为缓存
            localStorage.setItem(
                'lunr-index-cache',
                JSON.stringify({
                    data: indexData,
                    timestamp: Date.now(),
                })
            );

            console.log('索引已缓存到本地存储');
        } catch (error) {
            console.error('保存索引失败:', error);
        }
    }

    /**
     * 执行搜索
     */
    search(query, options = {}) {
        if (!this.lunrIndex || !query.trim()) {
            return [];
        }

        // 默认配置
        const config = {
            limit: options.limit || 10,
            minScore: options.minScore || 0.1,
            boost: options.boost || {},
        };

        // 添加模糊搜索
        let searchQuery = query.trim();

        // 执行搜索
        const results = this.lunrIndex.search(searchQuery);

        // 过滤和排序
        const filteredResults = results
            .filter((result) => result.score >= config.minScore)
            .slice(0, config.limit)
            .map((result) => {
                const doc = this.searchData.find((d) => d.id === result.ref);
                return {
                    ...doc,
                    score: result.score,
                    matchData: result.matchData.metadata,
                };
            });

        return filteredResults;
    }

    /**
     * 高级搜索功能
     */
    advancedSearch(query, filters = {}) {
        if (!this.lunrIndex) {
            return [];
        }

        // 构建搜索查询
        let searchQuery = query.trim();

        // 添加类别过滤
        if (filters.category) {
            searchQuery += ` category:${filters.category}`;
        }

        // 添加类型过滤
        if (filters.type) {
            searchQuery += ` type:${filters.type}`;
        }

        return this.search(searchQuery, filters);
    }

    /**
     * 搜索建议
     */
    getSuggestions(query) {
        if (!query.trim()) {
            return [];
        }

        // 提取关键词
        const keywords = query.split(/\s+/).filter((k) => k.length > 1);

        // 使用前缀匹配
        const suggestions = [];
        keywords.forEach((keyword) => {
            const results = this.lunrIndex.query((q) => {
                q.term(keyword, { usePipeline: false });
                q.term(keyword + '*', { usePipeline: false });
            });

            results.forEach((result) => {
                const doc = this.searchData.find((d) => d.id === result.ref);
                if (doc && !suggestions.find((s) => s.id === doc.id)) {
                    suggestions.push(doc);
                }
            });
        });

        return suggestions.slice(0, 5);
    }

    /**
     * 相关搜索
     */
    getRelatedDocuments(docId, limit = 5) {
        const doc = this.searchData.find((d) => d.id === docId);
        if (!doc) {
            return [];
        }

        // 使用文档关键词搜索相关内容
        const keywords = doc.keywords || doc.title;
        const results = this.search(keywords, { limit: limit + 1 });

        // 排除自身
        return results.filter((r) => r.id !== docId).slice(0, limit);
    }

    /**
     * 搜索统计
     */
    getSearchStats() {
        return {
            totalDocuments: this.searchData.length,
            indexSize: this.lunrIndex ? JSON.stringify(this.lunrIndex.toJSON()).length : 0,
            categories: this.getCategories(),
        };
    }

    /**
     * 获取所有类别
     */
    getCategories() {
        const categories = new Set();
        this.searchData.forEach((doc) => {
            if (doc.category) {
                categories.add(doc.category);
            }
        });
        return Array.from(categories);
    }

    /**
     * 降级到默认搜索
     */
    fallbackToDefaultSearch() {
        console.log('降级到默认搜索');

        // 使用原有的搜索功能
        if (window.SiteSearch) {
            window.SiteSearch.init();
        }

        // 提供基本的搜索功能
        this.search = (query, options) => {
            return this.searchData
                .filter(
                    (doc) =>
                        doc.title.toLowerCase().includes(query.toLowerCase()) ||
                        (doc.description &&
                            doc.description.toLowerCase().includes(query.toLowerCase()))
                )
                .slice(0, options.limit || 10);
        };
    }

    /**
     * 导出搜索接口
     */
    exportAPI() {
        window.LunrSearchAPI = {
            search: this.search.bind(this),
            advancedSearch: this.advancedSearch.bind(this),
            getSuggestions: this.getSuggestions.bind(this),
            getRelatedDocuments: this.getRelatedDocuments.bind(this),
            getSearchStats: this.getSearchStats.bind(this),
        };
    }
}

// 创建全局实例
const lunrSearch = new LunrSearch();

// 导出
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LunrSearch;
}
