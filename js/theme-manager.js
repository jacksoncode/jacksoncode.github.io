class ThemeManager {
    constructor() {
        this.themes = {
            light: {
                name: '亮色模式',
                icon: 'fa-sun',
                colors: {
                    bg: '#ffffff',
                    bgSecondary: '#f8fafc',
                    text: '#1e293b',
                    textSecondary: '#64748b',
                    border: '#e2e8f0',
                    primary: '#3b82f6',
                },
            },
            dark: {
                name: '暗色模式',
                icon: 'fa-moon',
                colors: {
                    bg: '#1f2937',
                    bgSecondary: '#111827',
                    text: '#f9fafb',
                    textSecondary: '#9ca3af',
                    border: '#374151',
                    primary: '#60a5fa',
                },
            },
            eyeCare: {
                name: '护眼模式',
                icon: 'fa-eye',
                colors: {
                    bg: '#c7edcc',
                    bgSecondary: '#e8f5e9',
                    text: '#2e7d32',
                    textSecondary: '#558b2f',
                    border: '#a5d6a7',
                    primary: '#43a047',
                },
            },
        };

        this.currentTheme = this.loadTheme();
        this.init();
    }

    init() {
        this.applyTheme(this.currentTheme);
        this.createThemeSwitcher();
        this.bindEvents();
    }

    loadTheme() {
        return localStorage.getItem('theme') || 'light';
    }

    saveTheme(theme) {
        localStorage.setItem('theme', theme);
    }

    applyTheme(themeName) {
        const theme = this.themes[themeName];
        if (!theme) return;

        document.documentElement.setAttribute('data-theme', themeName);

        Object.entries(theme.colors).forEach(([key, value]) => {
            document.documentElement.style.setProperty(`--${key}-color`, value);
        });

        document.body.classList.remove('light-mode', 'dark-mode', 'eye-care-mode');
        document.body.classList.add(`${themeName}-mode`);

        this.currentTheme = themeName;
        this.saveTheme(themeName);

        this.updateThemeIcon();
    }

    createThemeSwitcher() {
        const switcher = document.createElement('div');
        switcher.className = 'theme-switcher';
        switcher.innerHTML = `
      <button class="theme-btn" aria-label="切换主题">
        <i class="fas ${this.themes[this.currentTheme].icon}"></i>
      </button>
      <div class="theme-dropdown">
        ${Object.entries(this.themes)
            .map(
                ([key, theme]) => `
          <button class="theme-option ${key === this.currentTheme ? 'active' : ''}" 
                  data-theme="${key}">
            <i class="fas ${theme.icon}"></i>
            <span>${theme.name}</span>
          </button>
        `
            )
            .join('')}
      </div>
    `;

        const navbar = document.querySelector('.navbar-container');
        if (navbar) {
            navbar.appendChild(switcher);
        }

        this.switcher = switcher;
        this.addSwitcherStyles();
    }

    addSwitcherStyles() {
        const style = document.createElement('style');
        style.textContent = `
      .theme-switcher {
        position: relative;
        margin-left: 12px;
      }
      
      .theme-btn {
        width: 40px;
        height: 40px;
        border-radius: 8px;
        border: 1px solid var(--border-color);
        background: var(--bg-secondary-color);
        color: var(--text-color);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
      }
      
      .theme-btn:hover {
        background: var(--primary-color);
        color: white;
        border-color: var(--primary-color);
      }
      
      .theme-dropdown {
        position: absolute;
        top: 100%;
        right: 0;
        margin-top: 8px;
        background: var(--bg-color);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        display: none;
        min-width: 160px;
        z-index: 1000;
      }
      
      .theme-switcher:hover .theme-dropdown {
        display: block;
      }
      
      .theme-option {
        width: 100%;
        padding: 12px 16px;
        border: none;
        background: transparent;
        color: var(--text-color);
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 12px;
        transition: all 0.2s;
        text-align: left;
      }
      
      .theme-option:hover {
        background: rgba(59, 130, 246, 0.1);
        color: var(--primary-color);
      }
      
      .theme-option.active {
        background: rgba(59, 130, 246, 0.15);
        color: var(--primary-color);
      }
      
      .theme-option i {
        width: 20px;
      }
      
      .eye-care-mode {
        background-color: #c7edcc !important;
      }
      
      .eye-care-mode * {
        background-color: inherit;
      }
      
      .eye-care-mode .navbar,
      .eye-care-mode .card,
      .eye-care-mode .post-card {
        background: #e8f5e9;
      }
      
      @media (max-width: 768px) {
        .theme-switcher {
          margin-left: 8px;
        }
        
        .theme-btn {
          width: 36px;
          height: 36px;
        }
        
        .theme-dropdown {
          right: -10px;
        }
      }
    `;
        document.head.appendChild(style);
    }

    updateThemeIcon() {
        const iconElement = this.switcher?.querySelector('.theme-btn i');
        if (iconElement) {
            iconElement.className = `fas ${this.themes[this.currentTheme].icon}`;
        }

        this.switcher?.querySelectorAll('.theme-option').forEach((option) => {
            option.classList.toggle('active', option.dataset.theme === this.currentTheme);
        });
    }

    bindEvents() {
        this.switcher?.querySelectorAll('.theme-option').forEach((option) => {
            option.addEventListener('click', () => {
                const themeName = option.dataset.theme;
                this.applyTheme(themeName);
            });
        });

        this.switcher?.querySelector('.theme-btn')?.addEventListener('click', () => {
            const themeKeys = Object.keys(this.themes);
            const currentIndex = themeKeys.indexOf(this.currentTheme);
            const nextIndex = (currentIndex + 1) % themeKeys.length;
            this.applyTheme(themeKeys[nextIndex]);
        });
    }

    cycleTheme() {
        const themeKeys = Object.keys(this.themes);
        const currentIndex = themeKeys.indexOf(this.currentTheme);
        const nextIndex = (currentIndex + 1) % themeKeys.length;
        this.applyTheme(themeKeys[nextIndex]);
    }
}

const themeManager = new ThemeManager();

window.ThemeManagerAPI = {
    applyTheme: themeManager.applyTheme.bind(themeManager),
    cycleTheme: themeManager.cycleTheme.bind(themeManager),
    getCurrentTheme: () => themeManager.currentTheme,
};

if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThemeManager;
}
