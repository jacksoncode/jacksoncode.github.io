/**
 * 暗色模式切换脚本
 * 功能：
 * 1. 切换亮色/暗色模式
 * 2. 保存用户偏好到 localStorage
 * 3. 跟随系统偏好
 * 4. 创建切换按钮
 */

(function() {
    'use strict';
    
    // 主题配置
    const THEME_KEY = 'codeclub-theme';
    const DARK_THEME = 'dark';
    const LIGHT_THEME = 'light';
    
    // 获取保存的主题或检测系统偏好
    function getPreferredTheme() {
        const savedTheme = localStorage.getItem(THEME_KEY);
        if (savedTheme) {
            return savedTheme;
        }
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? DARK_THEME : LIGHT_THEME;
    }
    
    // 应用主题
    function applyTheme(theme) {
        if (theme === DARK_THEME) {
            document.documentElement.classList.add('dark-mode');
        } else {
            document.documentElement.classList.remove('dark-mode');
        }
        updateThemeIcon(theme);
    }
    
    // 更新图标
    function updateThemeIcon(theme) {
        const toggleBtn = document.querySelector('.theme-toggle');
        if (!toggleBtn) return;
        
        const icon = toggleBtn.querySelector('i');
        if (!icon) return;
        
        if (theme === DARK_THEME) {
            icon.className = 'fas fa-sun';
            toggleBtn.setAttribute('aria-label', '切换到亮色模式');
            toggleBtn.setAttribute('title', '切换到亮色模式');
        } else {
            icon.className = 'fas fa-moon';
            toggleBtn.setAttribute('aria-label', '切换到暗色模式');
            toggleBtn.setAttribute('title', '切换到暗色模式');
        }
    }
    
    // 切换主题
    function toggleTheme() {
        const currentTheme = document.documentElement.classList.contains('dark-mode') ? DARK_THEME : LIGHT_THEME;
        const newTheme = currentTheme === DARK_THEME ? LIGHT_THEME : DARK_THEME;
        
        applyTheme(newTheme);
        localStorage.setItem(THEME_KEY, newTheme);
        
        // 添加动画效果
        document.body.style.opacity = '0.99';
        setTimeout(() => {
            document.body.style.opacity = '1';
        }, 150);
    }
    
    // 创建切换按钮
    function createThemeToggle() {
        // 检查是否已存在
        if (document.querySelector('.theme-toggle')) {
            return;
        }
        
        const toggleBtn = document.createElement('button');
        toggleBtn.className = 'theme-toggle';
        toggleBtn.setAttribute('aria-label', '切换主题');
        toggleBtn.setAttribute('title', '切换主题');
        toggleBtn.innerHTML = '<i class="fas fa-moon"></i>';
        
        toggleBtn.addEventListener('click', toggleTheme);
        
        document.body.appendChild(toggleBtn);
    }
    
    // 初始化
    function init() {
        // 应用保存的主题
        const preferredTheme = getPreferredTheme();
        applyTheme(preferredTheme);
        
        // 监听系统主题变化
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem(THEME_KEY)) {
                applyTheme(e.matches ? DARK_THEME : LIGHT_THEME);
            }
        });
        
        // DOM 加载完成后创建切换按钮
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', createThemeToggle);
        } else {
            createThemeToggle();
        }
    }
    
    // 立即执行
    init();
    
    // 暴露全局方法（可选）
    window.CodeClubTheme = {
        toggle: toggleTheme,
        set: applyTheme,
        get: getPreferredTheme
    };
})();
