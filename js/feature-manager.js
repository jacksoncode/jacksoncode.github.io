class FeatureManager {
    constructor() {
        this.features = {
            lunrSearch: { enabled: true, loaded: false },
            articleFilter: { enabled: true, loaded: false },
            readingProgress: { enabled: true, loaded: false, articlePagesOnly: true },
            themeManager: { enabled: true, loaded: false },
            breadcrumbNav: { enabled: true, loaded: false },
            aiEnhancer: { enabled: true, loaded: false, articlePagesOnly: true },
            knowledgeGraph: { enabled: true, loaded: false, navPageOnly: true },
        };

        this.init();
    }

    init() {
        this.waitForDependencies();
    }

    waitForDependencies() {
        const checkDependencies = setInterval(() => {
            const allLoaded = this.checkAllDependencies();

            if (allLoaded) {
                clearInterval(checkDependencies);
                this.initializeFeatures();
            }
        }, 100);

        setTimeout(() => {
            clearInterval(checkDependencies);
            console.warn('部分功能加载超时');
        }, 5000);
    }

    checkAllDependencies() {
        const dependencies = {
            lunrSearch: typeof LunrSearch !== 'undefined',
            articleFilter: typeof ArticleFilter !== 'undefined',
            readingProgress: typeof ReadingProgress !== 'undefined',
            themeManager: typeof ThemeManager !== 'undefined',
            breadcrumbNav: typeof BreadcrumbNav !== 'undefined',
            aiEnhancer: typeof AIContentEnhancer !== 'undefined',
            knowledgeGraph: typeof KnowledgeGraphVisualizer !== 'undefined',
        };

        Object.keys(dependencies).forEach((key) => {
            this.features[key].loaded = dependencies[key];
        });

        return Object.values(dependencies).every((dep) => dep);
    }

    initializeFeatures() {
        const currentPage = this.getCurrentPageType();

        Object.keys(this.features).forEach((featureName) => {
            const feature = this.features[featureName];

            if (!feature.enabled || !feature.loaded) {
                return;
            }

            if (feature.articlePagesOnly && currentPage !== 'article') {
                return;
            }

            if (feature.navPageOnly && currentPage !== 'nav') {
                return;
            }

            console.log(`初始化功能: ${featureName}`);
        });

        this.addFeatureStatusIndicator();
    }

    getCurrentPageType() {
        const path = window.location.pathname;

        if (path.includes('/blog/') && path.endsWith('.html')) {
            return 'article';
        }

        if (path.includes('nav.html')) {
            return 'nav';
        }

        if (path.includes('index.html') || path === '/') {
            return 'home';
        }

        return 'other';
    }

    addFeatureStatusIndicator() {
        const enabledFeatures = Object.keys(this.features).filter(
            (key) => this.features[key].enabled && this.features[key].loaded
        ).length;

        const totalFeatures = Object.keys(this.features).length;

        console.log(`功能加载完成: ${enabledFeatures}/${totalFeatures}`);

        if (enabledFeatures < totalFeatures) {
            const missing = Object.keys(this.features)
                .filter((key) => !this.features[key].loaded)
                .join(', ');

            console.warn(`未加载的功能: ${missing}`);
        }
    }

    enableFeature(featureName) {
        if (this.features[featureName]) {
            this.features[featureName].enabled = true;
            console.log(`已启用功能: ${featureName}`);
        }
    }

    disableFeature(featureName) {
        if (this.features[featureName]) {
            this.features[featureName].enabled = false;
            console.log(`已禁用功能: ${featureName}`);
        }
    }

    getFeatureStatus(featureName) {
        return this.features[featureName] || null;
    }

    getAllFeaturesStatus() {
        return this.features;
    }
}

const featureManager = new FeatureManager();

window.FeatureManagerAPI = {
    enable: featureManager.enableFeature.bind(featureManager),
    disable: featureManager.disableFeature.bind(featureManager),
    getStatus: featureManager.getFeatureStatus.bind(featureManager),
    getAllStatus: featureManager.getAllFeaturesStatus.bind(featureManager),
};

if (typeof module !== 'undefined' && module.exports) {
    module.exports = FeatureManager;
}
