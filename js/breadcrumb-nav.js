class BreadcrumbNav {
    constructor() {
        this.breadcrumbs = [];
        this.init();
    }

    init() {
        this.generateBreadcrumbs();
        this.renderBreadcrumb();
    }

    generateBreadcrumbs() {
        const path = window.location.pathname;
        const parts = path.split('/').filter((part) => part);

        this.breadcrumbs = [{ name: '首页', url: '/index.html', icon: 'fa-home' }];

        const pathMap = {
            blog: { name: '博客', url: '/blog/', icon: 'fa-blog' },
            'nav.html': { name: '网址导航', url: '/nav.html', icon: 'fa-compass' },
            'book.html': { name: '图书推荐', url: '/book.html', icon: 'fa-book' },
            'about.html': { name: '关于我', url: '/about.html', icon: 'fa-user' },
            'contact.html': { name: '联系我', url: '/contact.html', icon: 'fa-envelope' },
            wiki: { name: 'Wiki', url: '/wiki/index.html', icon: 'fa-book-open' },
            tutorials: { name: '教程', url: '/tutorials/index.html', icon: 'fa-graduation-cap' },
            note: { name: '笔记', url: '/note/', icon: 'fa-sticky-note' },
        };

        parts.forEach((part, index) => {
            if (pathMap[part]) {
                this.breadcrumbs.push(pathMap[part]);
            } else if (part.endsWith('.html')) {
                const title =
                    document
                        .querySelector('h1, .post-title, .article-title')
                        ?.textContent?.trim() || part;
                this.breadcrumbs.push({
                    name: title,
                    url: path,
                    icon: 'fa-file-alt',
                    isCurrent: true,
                });
            } else if (index === parts.length - 1 && !part.endsWith('.html')) {
                this.breadcrumbs.push({
                    name: part.charAt(0).toUpperCase() + part.slice(1),
                    url: path,
                    icon: 'fa-folder',
                    isCurrent: true,
                });
            }
        });
    }

    renderBreadcrumb() {
        if (this.breadcrumbs.length <= 1) return;

        const breadcrumbContainer = document.createElement('nav');
        breadcrumbContainer.className = 'breadcrumb-nav';
        breadcrumbContainer.setAttribute('aria-label', '面包屑导航');

        breadcrumbContainer.innerHTML = `
      <ol class="breadcrumb-list">
        ${this.breadcrumbs
            .map(
                (item, index) => `
          <li class="breadcrumb-item ${item.isCurrent ? 'current' : ''}">
            ${
                index < this.breadcrumbs.length - 1
                    ? `
              <a href="${item.url}" class="breadcrumb-link">
                ${item.icon ? `<i class="fas ${item.icon}"></i>` : ''}
                <span>${item.name}</span>
              </a>
              <i class="fas fa-chevron-right breadcrumb-separator"></i>
            `
                    : `
              <span class="breadcrumb-current">
                ${item.icon ? `<i class="fas ${item.icon}"></i>` : ''}
                <span>${item.name}</span>
              </span>
            `
            }
          </li>
        `
            )
            .join('')}
      </ol>
    `;

        const mainContent =
            document.querySelector('main') || document.querySelector('.container') || document.body;

        mainContent.insertBefore(breadcrumbContainer, mainContent.firstChild);

        this.addBreadcrumbStyles();
    }

    addBreadcrumbStyles() {
        const style = document.createElement('style');
        style.textContent = `
      .breadcrumb-nav {
        background: var(--bg-secondary-color);
        padding: 12px 24px;
        border-radius: 8px;
        margin-bottom: 24px;
        overflow-x: auto;
      }
      
      .breadcrumb-list {
        display: flex;
        align-items: center;
        list-style: none;
        margin: 0;
        padding: 0;
        gap: 8px;
        flex-wrap: wrap;
      }
      
      .breadcrumb-item {
        display: flex;
        align-items: center;
        gap: 8px;
      }
      
      .breadcrumb-link {
        color: var(--text-secondary-color);
        text-decoration: none;
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 6px;
        transition: color 0.2s;
      }
      
      .breadcrumb-link:hover {
        color: var(--primary-color);
      }
      
      .breadcrumb-link i {
        font-size: 12px;
      }
      
      .breadcrumb-separator {
        color: var(--text-muted-color);
        font-size: 10px;
        margin: 0 4px;
      }
      
      .breadcrumb-current {
        color: var(--text-color);
        font-size: 14px;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 6px;
      }
      
      .breadcrumb-current i {
        font-size: 12px;
      }
      
      .breadcrumb-item.current {
        pointer-events: none;
      }
      
      .dark-mode .breadcrumb-nav {
        background: #374151;
      }
      
      .dark-mode .breadcrumb-link {
        color: #9ca3af;
      }
      
      .dark-mode .breadcrumb-link:hover {
        color: #60a5fa;
      }
      
      .dark-mode .breadcrumb-separator {
        color: #6b7280;
      }
      
      .dark-mode .breadcrumb-current {
        color: #f9fafb;
      }
      
      .eye-care-mode .breadcrumb-nav {
        background: #e8f5e9;
      }
      
      .eye-care-mode .breadcrumb-link {
        color: #558b2f;
      }
      
      .eye-care-mode .breadcrumb-link:hover {
        color: #2e7d32;
      }
      
      @media (max-width: 768px) {
        .breadcrumb-nav {
          padding: 10px 16px;
          margin-bottom: 16px;
        }
        
        .breadcrumb-link span,
        .breadcrumb-current span {
          font-size: 13px;
        }
        
        .breadcrumb-list {
          gap: 6px;
        }
      }
    `;
        document.head.appendChild(style);
    }
}

const breadcrumbNav = new BreadcrumbNav();

if (typeof module !== 'undefined' && module.exports) {
    module.exports = BreadcrumbNav;
}
