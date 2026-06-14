class ReadingProgress {
    constructor() {
        this.progressBar = null;
        this.tocNav = null;
        this.headings = [];
        this.currentHeadingIndex = -1;
        this.init();
    }

    init() {
        if (this.isArticlePage()) {
            this.createProgressBar();
            this.createTableOfContents();
            this.collectHeadings();
            this.bindEvents();
            this.updateProgress();
        }
    }

    isArticlePage() {
        const path = window.location.pathname;
        return path.includes('/blog/') && path.endsWith('.html');
    }

    createProgressBar() {
        const progressBar = document.createElement('div');
        progressBar.className = 'reading-progress-bar';
        progressBar.innerHTML = `
      <div class="progress-fill"></div>
      <div class="progress-text">0%</div>
    `;

        document.body.prepend(progressBar);
        this.progressBar = progressBar;

        this.addProgressBarStyles();
    }

    addProgressBarStyles() {
        const style = document.createElement('style');
        style.textContent = `
      .reading-progress-bar {
        position: fixed;
        top: 64px;
        left: 0;
        right: 0;
        height: 3px;
        background: rgba(0, 0, 0, 0.1);
        z-index: 999;
      }
      
      .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        width: 0%;
        transition: width 0.2s;
      }
      
      .progress-text {
        position: absolute;
        right: 20px;
        top: -25px;
        font-size: 12px;
        color: #6b7280;
        background: rgba(255, 255, 255, 0.9);
        padding: 2px 8px;
        border-radius: 4px;
      }
      
      .dark-mode .reading-progress-bar {
        background: rgba(255, 255, 255, 0.1);
      }
      
      .dark-mode .progress-text {
        background: rgba(31, 41, 55, 0.9);
        color: #9ca3af;
      }
      
      @media (max-width: 768px) {
        .progress-text {
          display: none;
        }
      }
    `;
        document.head.appendChild(style);
    }

    createTableOfContents() {
        const tocContainer = document.createElement('div');
        tocContainer.className = 'table-of-contents';
        tocContainer.innerHTML = `
      <div class="toc-header">
        <h4><i class="fas fa-list"></i> 目录导航</h4>
        <button class="toc-toggle" aria-label="切换目录">
          <i class="fas fa-chevron-left"></i>
        </button>
      </div>
      <div class="toc-body">
        <nav class="toc-nav"></nav>
      </div>
      <div class="toc-footer">
        <div class="reading-time">
          <i class="fas fa-clock"></i>
          <span class="time-text">预计阅读时间: --分钟</span>
        </div>
      </div>
    `;

        const articleContent =
            document.querySelector('.article-content') ||
            document.querySelector('.post-content') ||
            document.querySelector('main');

        if (articleContent) {
            articleContent.parentElement.insertBefore(tocContainer, articleContent);
            this.tocNav = tocContainer;
            this.addTocStyles();
        }
    }

    addTocStyles() {
        const style = document.createElement('style');
        style.textContent = `
      .table-of-contents {
        position: fixed;
        right: 20px;
        top: 80px;
        width: 280px;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        transition: all 0.3s;
        z-index: 100;
        max-height: calc(100vh - 100px);
      }
      
      .toc-header {
        padding: 16px 20px;
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        display: flex;
        align-items: center;
        justify-content: space-between;
      }
      
      .toc-header h4 {
        margin: 0;
        font-size: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
        color: #1e293b;
      }
      
      .toc-toggle {
        background: transparent;
        border: none;
        color: #6b7280;
        cursor: pointer;
        padding: 4px 8px;
        border-radius: 4px;
      }
      
      .toc-toggle:hover {
        background: rgba(0, 0, 0, 0.05);
      }
      
      .toc-body {
        padding: 12px 20px;
        max-height: 400px;
        overflow-y: auto;
      }
      
      .toc-nav {
        display: flex;
        flex-direction: column;
        gap: 4px;
      }
      
      .toc-link {
        padding: 8px 12px;
        border-radius: 6px;
        color: #4b5563;
        text-decoration: none;
        font-size: 14px;
        transition: all 0.2s;
        display: block;
        border-left: 2px solid transparent;
      }
      
      .toc-link:hover {
        background: rgba(59, 130, 246, 0.1);
        color: #3b82f6;
        border-left-color: #3b82f6;
      }
      
      .toc-link.active {
        background: rgba(59, 130, 246, 0.15);
        color: #3b82f6;
        border-left-color: #3b82f6;
        font-weight: 500;
      }
      
      .toc-link.level-2 {
        padding-left: 24px;
        font-size: 13px;
      }
      
      .toc-link.level-3 {
        padding-left: 36px;
        font-size: 12px;
      }
      
      .toc-footer {
        padding: 12px 20px;
        border-top: 1px solid rgba(0, 0, 0, 0.05);
        font-size: 13px;
        color: #6b7280;
      }
      
      .reading-time {
        display: flex;
        align-items: center;
        gap: 6px;
      }
      
      .table-of-contents.collapsed {
        width: 50px;
        overflow: hidden;
      }
      
      .table-of-contents.collapsed .toc-header h4,
      .table-of-contents.collapsed .toc-body,
      .table-of-contents.collapsed .toc-footer {
        display: none;
      }
      
      .table-of-contents.collapsed .toc-toggle i {
        transform: rotate(180deg);
      }
      
      .dark-mode .table-of-contents {
        background: rgba(31, 41, 55, 0.95);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
      }
      
      .dark-mode .toc-header {
        border-bottom-color: rgba(255, 255, 255, 0.1);
      }
      
      .dark-mode .toc-header h4 {
        color: #f9fafb;
      }
      
      .dark-mode .toc-toggle {
        color: #9ca3af;
      }
      
      .dark-mode .toc-toggle:hover {
        background: rgba(255, 255, 255, 0.1);
      }
      
      .dark-mode .toc-link {
        color: #9ca3af;
      }
      
      .dark-mode .toc-link:hover {
        background: rgba(59, 130, 246, 0.2);
        color: #60a5fa;
        border-left-color: #60a5fa;
      }
      
      .dark-mode .toc-link.active {
        background: rgba(59, 130, 246, 0.25);
        color: #60a5fa;
        border-left-color: #60a5fa;
      }
      
      .dark-mode .toc-footer {
        border-top-color: rgba(255, 255, 255, 0.1);
        color: #9ca3af;
      }
      
      @media (max-width: 1400px) {
        .table-of-contents {
          width: 240px;
        }
      }
      
      @media (max-width: 1024px) {
        .table-of-contents {
          position: static;
          width: 100%;
          margin-bottom: 24px;
          max-height: none;
        }
        
        .toc-body {
          max-height: 300px;
        }
      }
    `;
        document.head.appendChild(style);
    }

    collectHeadings() {
        const articleContent =
            document.querySelector('.article-content') ||
            document.querySelector('.post-content') ||
            document.querySelector('main');

        if (!articleContent) return;

        this.headings = Array.from(articleContent.querySelectorAll('h1, h2, h3, h4')).map(
            (heading) => ({
                element: heading,
                level: parseInt(heading.tagName.charAt(1)),
                text: heading.textContent.trim(),
                id: heading.id || this.generateHeadingId(heading),
            })
        );

        this.renderTableOfContents();
        this.calculateReadingTime();
    }

    generateHeadingId(heading) {
        const id = heading.textContent
            .trim()
            .toLowerCase()
            .replace(/[^\w\s-]/g, '')
            .replace(/\s+/g, '-')
            .substring(0, 50);

        heading.id = id;
        return id;
    }

    renderTableOfContents() {
        const tocNav = this.tocNav?.querySelector('.toc-nav');
        if (!tocNav || this.headings.length === 0) return;

        tocNav.innerHTML = this.headings
            .map(
                (heading) => `
      <a href="#${heading.id}" 
         class="toc-link level-${heading.level}"
         data-heading-index="${this.headings.indexOf(heading)}">
        ${heading.text}
      </a>
    `
            )
            .join('');
    }

    calculateReadingTime() {
        const articleContent =
            document.querySelector('.article-content') ||
            document.querySelector('.post-content') ||
            document.querySelector('main');

        if (!articleContent) return;

        const text = articleContent.textContent.trim();
        const wordCount = text.split(/\s+/).length;
        const chineseCount = (text.match(/[\u4e00-\u9fa5]/g) || []).length;

        const totalWords = wordCount + chineseCount;
        const readingSpeed = 200;
        const minutes = Math.ceil(totalWords / readingSpeed);

        const timeText = this.tocNav?.querySelector('.time-text');
        if (timeText) {
            timeText.textContent = `预计阅读时间: ${minutes}分钟`;
        }
    }

    bindEvents() {
        window.addEventListener('scroll', this.handleScroll.bind(this));

        this.tocNav?.querySelector('.toc-toggle')?.addEventListener('click', () => {
            this.tocNav.classList.toggle('collapsed');
        });

        this.tocNav?.querySelectorAll('.toc-link').forEach((link) => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);

                if (targetElement) {
                    const offsetTop = targetElement.offsetTop - 80;
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth',
                    });
                }
            });
        });
    }

    handleScroll() {
        this.updateProgress();
        this.updateActiveHeading();
    }

    updateProgress() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const scrollHeight =
            document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const progress = (scrollTop / scrollHeight) * 100;

        const progressFill = this.progressBar?.querySelector('.progress-fill');
        const progressText = this.progressBar?.querySelector('.progress-text');

        if (progressFill) {
            progressFill.style.width = `${progress}%`;
        }

        if (progressText) {
            progressText.textContent = `${Math.round(progress)}%`;
        }
    }

    updateActiveHeading() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        let activeIndex = -1;
        this.headings.forEach((heading, index) => {
            const headingTop = heading.element.offsetTop - 100;
            if (scrollTop >= headingTop) {
                activeIndex = index;
            }
        });

        if (activeIndex !== this.currentHeadingIndex) {
            this.currentHeadingIndex = activeIndex;

            this.tocNav?.querySelectorAll('.toc-link').forEach((link, index) => {
                link.classList.toggle('active', index === activeIndex);
            });
        }
    }
}

const readingProgress = new ReadingProgress();

if (typeof module !== 'undefined' && module.exports) {
    module.exports = ReadingProgress;
}
