/**
 * 回到顶部按钮功能
 * 用法：在页面底部添加按钮元素，引入此脚本
 */

(function() {
    'use strict';
    
    // 配置
    const CONFIG = {
        showOnScroll: 300,        // 滚动多少像素后显示
        scrollDuration: 800,      // 滚动动画时长 (ms)
        buttonSize: 50,           // 按钮大小
        bottomPosition: 100,      // 距离底部位置
        rightPosition: 30         // 距离右侧位置
    };
    
    // 创建回到顶部按钮
    function createBackToTopButton() {
        // 检查是否已存在
        if (document.getElementById('backToTop')) {
            return;
        }
        
        const button = document.createElement('button');
        button.id = 'backToTop';
        button.className = 'back-to-top';
        button.setAttribute('aria-label', '回到顶部');
        button.setAttribute('title', '回到顶部');
        button.innerHTML = '<i class="fas fa-arrow-up"></i>';
        
        document.body.appendChild(button);
        
        // 绑定点击事件
        button.addEventListener('click', scrollToTop);
        
        // 绑定滚动事件
        window.addEventListener('scroll', handleScroll, { passive: true });
    }
    
    // 处理滚动
    let scrollTimeout;
    function handleScroll() {
        // 使用防抖优化性能
        if (scrollTimeout) {
            clearTimeout(scrollTimeout);
        }
        
        scrollTimeout = setTimeout(() => {
            const button = document.getElementById('backToTop');
            if (!button) return;
            
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (scrollTop > CONFIG.showOnScroll) {
                button.classList.add('visible');
            } else {
                button.classList.remove('visible');
            }
        }, 100);
    }
    
    // 滚动到顶部
    function scrollToTop() {
        const start = window.pageYOffset || document.documentElement.scrollTop;
        const change = -start;
        const duration = CONFIG.scrollDuration;
        let startTime = null;
        
        function animation(currentTime) {
            if (startTime === null) startTime = currentTime;
            
            const timeElapsed = currentTime - startTime;
            const progress = Math.min(timeElapsed / duration, 1);
            const ease = easeInOutCubic(progress);
            
            window.scrollTo(0, start + change * ease);
            
            if (timeElapsed < duration) {
                requestAnimationFrame(animation);
            }
        }
        
        requestAnimationFrame(animation);
    }
    
    // 缓动函数 - Cubic Bezier
    function easeInOutCubic(t) {
        return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }
    
    // 添加样式
    function addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .back-to-top {
                position: fixed;
                bottom: ${CONFIG.bottomPosition}px;
                right: ${CONFIG.rightPosition}px;
                width: ${CONFIG.buttonSize}px;
                height: ${CONFIG.buttonSize}px;
                border-radius: 50%;
                background: var(--primary-color, #3b82f6);
                color: white;
                border: none;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20px;
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
                opacity: 0;
                visibility: hidden;
                transform: translateY(20px);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                z-index: 998;
            }
            
            .back-to-top.visible {
                opacity: 1;
                visibility: visible;
                transform: translateY(0);
            }
            
            .back-to-top:hover {
                background: var(--primary-hover, #2563eb);
                transform: translateY(-4px);
                box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5);
            }
            
            .back-to-top:active {
                transform: translateY(-2px);
            }
            
            /* 移动端适配 */
            @media (max-width: 768px) {
                .back-to-top {
                    bottom: ${CONFIG.bottomPosition - 20}px;
                    right: ${CONFIG.rightPosition - 10}px;
                    width: ${CONFIG.buttonSize - 6}px;
                    height: ${CONFIG.buttonSize - 6}px;
                    font-size: 18px;
                }
            }
            
            /* 暗色模式适配 */
            .dark-mode .back-to-top {
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.6);
            }
        `;
        
        document.head.appendChild(style);
    }
    
    // 初始化
    function init() {
        addStyles();
        createBackToTopButton();
        console.log('✅ 回到顶部功能已加载');
    }
    
    // 页面加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
