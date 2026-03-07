/**
 * 移动端汉堡菜单脚本
 * 用法：在页面底部引入此脚本
 * <script src="./js/mobile-menu.js"></script>
 */

document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const navbarNav = document.querySelector('.navbar-nav');
    
    if (menuToggle && navbarNav) {
        // 切换菜单
        menuToggle.addEventListener('click', function() {
            this.classList.toggle('active');
            navbarNav.classList.toggle('active');
            this.setAttribute('aria-expanded', 
                this.classList.contains('active') ? 'true' : 'false');
        });
        
        // 点击导航链接后关闭菜单
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', function() {
                menuToggle.classList.remove('active');
                navbarNav.classList.remove('active');
            });
        });
        
        // ESC 键关闭菜单
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && menuToggle.classList.contains('active')) {
                menuToggle.classList.remove('active');
                navbarNav.classList.remove('active');
            }
        });
        
        // 点击菜单外部区域关闭
        document.addEventListener('click', function(e) {
            if (menuToggle.classList.contains('active') && 
                !navbarNav.contains(e.target) && 
                !menuToggle.contains(e.target)) {
                menuToggle.classList.remove('active');
                navbarNav.classList.remove('active');
            }
        });
    }
});
