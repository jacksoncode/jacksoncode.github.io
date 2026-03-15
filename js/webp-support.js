/**
 * WebP 图片格式支持
 * 自动检测浏览器支持并选择最佳图片格式
 */

(function() {
    'use strict';
    
    // 检测 WebP 支持
    function checkWebPSupport() {
        return new Promise((resolve) => {
            const webP = new Image();
            webP.onload = webP.onerror = function() {
                resolve(webP.height === 2);
            };
            webP.src = 'data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA';
        });
    }
    
    // 优化图片标签
    function optimizeImages() {
        // 查找所有 img 标签
        const images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"], img[src$=".png"]');
        
        images.forEach(img => {
            const src = img.src;
            const ext = src.split('.').pop().toLowerCase();
            
            // 创建 WebP 版本的 URL
            const webpSrc = src.replace(`.${ext}`, '.webp');
            
            // 创建 picture 元素
            const picture = document.createElement('picture');
            
            // 添加 WebP 源
            const sourceWebP = document.createElement('source');
            sourceWebP.type = 'image/webp';
            sourceWebP.srcset = webpSrc;
            
            // 添加原始格式源
            const sourceOriginal = document.createElement('source');
            sourceOriginal.type = ext === 'png' ? 'image/png' : 'image/jpeg';
            sourceOriginal.srcset = src;
            
            // 克隆原始 img 元素
            const clonedImg = img.cloneNode(true);
            
            // 组装 picture 元素
            picture.appendChild(sourceWebP);
            picture.appendChild(sourceOriginal);
            picture.appendChild(clonedImg);
            
            // 替换原始 img
            img.parentNode.replaceChild(picture, img);
        });
    }
    
    // 延迟加载优化
    function optimizeLazyLoading() {
        // 如果浏览器支持原生懒加载，确保正确配置
        if ('loading' in HTMLImageElement.prototype) {
            const lazyImages = document.querySelectorAll('img[data-src]');
            lazyImages.forEach(img => {
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
            });
        }
    }
    
    // 图片尺寸优化
    function optimizeImageSizes() {
        const images = document.querySelectorAll('img[width][height]');
        
        images.forEach(img => {
            // 添加 loading="lazy" 属性
            if (!img.loading) {
                img.loading = 'lazy';
            }
            
            // 确保 width 和 height 是响应式的
            img.style.maxWidth = '100%';
            img.style.height = 'auto';
        });
    }
    
    // 为主页背景图片添加 WebP 支持
    function optimizeHeroBackgrounds() {
        // 这里可以为主页的英雄区域背景添加 WebP 支持
        const heroSection = document.querySelector('.hero');
        if (heroSection) {
            const computedStyle = window.getComputedStyle(heroSection);
            const bgImage = computedStyle.backgroundImage;
            
            // 检查是否有背景图片
            if (bgImage && bgImage !== 'none') {
                // 这里可以根据需要实现背景图片的 WebP 替换
                console.log('检测到背景图片，可以进一步优化');
            }
        }
    }
    
    // 添加响应式图片支持
    function addResponsiveImages() {
        const heroImg = document.querySelector('.hero img, .index-banner');
        if (heroImg && heroImg.src) {
            // 创建 srcset 属性
            const src = heroImg.src;
            const ext = src.split('.').pop().toLowerCase();
            
            if (ext === 'jpg' || ext === 'jpeg' || ext === 'png') {
                // 添加不同尺寸的图片
                const sizes = '(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw';
                const webpSrc = src.replace(`.${ext}`, '.webp');
                
                // 创建 picture 元素
                const picture = document.createElement('picture');
                
                const sourceWebP = document.createElement('source');
                sourceWebP.type = 'image/webp';
                sourceWebP.srcset = `${webpSrc} 1x, ${webpSrc} 2x`;
                
                const sourceOriginal = document.createElement('source');
                sourceOriginal.type = ext === 'png' ? 'image/png' : 'image/jpeg';
                sourceOriginal.srcset = `${src} 1x, ${src} 2x`;
                
                const clonedImg = heroImg.cloneNode(true);
                clonedImg.sizes = sizes;
                
                picture.appendChild(sourceWebP);
                picture.appendChild(sourceOriginal);
                picture.appendChild(clonedImg);
                
                heroImg.parentNode.replaceChild(picture, heroImg);
            }
        }
    }
    
    // 监听图片加载错误
    function handleImageErrors() {
        document.addEventListener('error', function(e) {
            if (e.target.tagName === 'IMG') {
                const img = e.target;
                const src = img.src;
                
                // 如果 WebP 加载失败，回退到原始格式
                if (src.includes('.webp')) {
                    const originalSrc = src.replace('.webp', '');
                    console.warn(`WebP 加载失败，回退到: ${originalSrc}`);
                    img.src = originalSrc;
                }
            }
        }, true);
    }
    
    // 主初始化函数
    async function init() {
        try {
            // 检查 WebP 支持
            const webpSupported = await checkWebPSupport();
            
            if (webpSupported) {
                console.log('✅ 浏览器支持 WebP 格式');
                
                // 等待 DOM 加载完成后优化图片
                if (document.readyState === 'loading') {
                    document.addEventListener('DOMContentLoaded', () => {
                        optimizeImages();
                        addResponsiveImages();
                        optimizeHeroBackgrounds();
                    });
                } else {
                    optimizeImages();
                    addResponsiveImages();
                    optimizeHeroBackgrounds();
                }
            } else {
                console.log('⚠️  浏览器不支持 WebP 格式');
            }
            
            // 通用优化
            optimizeLazyLoading();
            optimizeImageSizes();
            handleImageErrors();
            
        } catch (error) {
            console.error('图片优化初始化失败:', error);
        }
    }
    
    // 暴露全局方法
    window.WebPSupport = {
        init: init,
        check: checkWebPSupport,
        optimize: optimizeImages
    };
    
    // 自动初始化
    init();
    
})();