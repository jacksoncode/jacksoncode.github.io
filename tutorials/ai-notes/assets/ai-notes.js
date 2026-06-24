/* AI学习笔记 - 共享脚本 */
(function() {
  'use strict';

  // ========== 进度追踪 ==========
  const STORAGE_KEY = 'ai-notes-progress';
  const STORAGE_EVENT = 'ai-notes-progress-updated';

  function getProgress() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
    } catch { return {}; }
  }

  function setProgress(chapterId, completed) {
    const progress = getProgress();
    if (completed) progress[chapterId] = Date.now();
    else delete progress[chapterId];
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
    window.dispatchEvent(new StorageEvent(STORAGE_EVENT, { key: STORAGE_KEY }));
  }

  function markChapterComplete(chapterId) {
    setProgress(chapterId, true);
    const btn = document.querySelector('.ai-complete-btn');
    if (btn) {
      btn.classList.add('done');
      btn.innerHTML = '<i class="fas fa-check-circle"></i> 已完成';
    }
  }

  function isChapterComplete(chapterId) {
    return !!getProgress()[chapterId];
  }

  function updateProgressUI() {
    const chapters = document.querySelectorAll('[data-chapter-id]');
    chapters.forEach(el => {
      const id = el.dataset.chapterId;
      if (isChapterComplete(id)) el.classList.add('completed');
    });
    const btn = document.querySelector('.ai-complete-btn');
    if (btn) {
      const cid = btn.dataset.chapterId;
      if (isChapterComplete(cid)) {
        btn.classList.add('done');
        btn.innerHTML = '<i class="fas fa-check-circle"></i> 已完成';
      }
    }
  }

  // ========== 移动端TOC抽屉 ==========
  function initMobileTOC() {
    const overlay = document.querySelector('.ai-mobile-toc-overlay');
    const drawer = document.querySelector('.ai-mobile-toc');
    const toggle = document.querySelector('.ai-mobile-toc-toggle');
    const closeBtn = document.querySelector('.ai-mobile-toc-close');
    if (!drawer || !toggle) return;

    function openTOC() {
      drawer.classList.add('show');
      overlay && overlay.classList.add('show');
      document.body.style.overflow = 'hidden';
    }
    function closeTOC() {
      drawer.classList.remove('show');
      overlay && overlay.classList.remove('show');
      document.body.style.overflow = '';
    }

    toggle.addEventListener('click', openTOC);
    overlay && overlay.addEventListener('click', closeTOC);
    closeBtn && closeBtn.addEventListener('click', closeTOC);
    drawer.querySelectorAll('a').forEach(a => a.addEventListener('click', closeTOC));
  }

  // ========== TOC滚动高亮 ==========
  function initTOCScrollSpy() {
    const tocLinks = document.querySelectorAll('.ai-toc a');
    if (tocLinks.length === 0) return;
    const sections = [];
    tocLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (href && href.startsWith('#')) {
        const target = document.getElementById(href.slice(1));
        if (target) sections.push({ link, target });
      }
    });
    function onScroll() {
      let current = sections[0];
      for (const s of sections) {
        if (s.target.getBoundingClientRect().top <= 120) current = s;
      }
      tocLinks.forEach(l => l.classList.remove('active'));
      if (current) current.link.classList.add('active');
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // ========== 代码复制按钮 ==========
  function initCopyButtons() {
    document.querySelectorAll('.ai-code-header .copy-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const code = btn.closest('.ai-code').querySelector('code');
        if (!code) return;
        navigator.clipboard.writeText(code.textContent).then(() => {
          const orig = btn.innerHTML;
          btn.innerHTML = '<i class="fas fa-check"></i> 已复制';
          setTimeout(() => { btn.innerHTML = orig; }, 2000);
        });
      });
    });
  }

  // ========== 移动端导航菜单 ==========
  function initMobileNav() {
    const toggle = document.querySelector('.ai-nav-toggle');
    const links = document.querySelector('.ai-nav-links');
    if (!toggle || !links) return;
    toggle.addEventListener('click', () => links.classList.toggle('active'));
    document.addEventListener('click', e => {
      if (!e.target.closest('.ai-nav')) links.classList.remove('active');
    });
  }

  // ========== 页面搜索功能 ==========
  let searchMatches = [];
  let currentMatchIndex = -1;
  let searchOverlay = null;

  function initSearch() {
    // 创建搜索UI
    const nav = document.querySelector('.ai-nav');
    if (!nav) return;

    // 添加搜索按钮到导航栏
    const searchBtn = document.createElement('button');
    searchBtn.className = 'ai-search-toggle';
    searchBtn.innerHTML = '<i class="fas fa-search"></i>';
    searchBtn.style.cssText = 'background:none;border:none;font-size:1.2rem;color:var(--ai-gray-600);cursor:pointer;padding:0.5rem;';
    nav.appendChild(searchBtn);

    // 创建搜索框overlay
    searchOverlay = document.createElement('div');
    searchOverlay.className = 'ai-search-overlay';
    searchOverlay.innerHTML = `
      <div class="ai-search-box">
        <input type="text" class="ai-search-input" placeholder="搜索当前页面...">
        <span class="ai-search-count"></span>
        <button class="ai-search-prev"><i class="fas fa-chevron-up"></i></button>
        <button class="ai-search-next"><i class="fas fa-chevron-down"></i></button>
        <button class="ai-search-close"><i class="fas fa-times"></i></button>
      </div>
    `;
    searchOverlay.style.cssText = 'position:fixed;top:80px;left:50%;transform:translateX(-50%);z-index:1100;display:none;';
    document.body.appendChild(searchOverlay);

    // 添加样式
    const style = document.createElement('style');
    style.textContent = `
      .ai-search-box { display:flex;align-items:center;gap:0.5rem;background:#fff;padding:0.75rem 1rem;border-radius:12px;box-shadow:0 4px 20px rgba(0,0,0,0.15); }
      .ai-search-input { border:1px solid var(--ai-gray-300);border-radius:8px;padding:0.5rem 1rem;font-size:0.95rem;width:300px;outline:none; }
      .ai-search-input:focus { border-color:var(--ai-primary); }
      .ai-search-count { font-size:0.85rem;color:var(--ai-gray-500);min-width:60px; }
      .ai-search-prev, .ai-search-next, .ai-search-close { background:none;border:none;color:var(--ai-gray-600);cursor:pointer;font-size:1rem;padding:0.25rem; }
      .ai-search-prev:hover, .ai-search-next:hover { color:var(--ai-primary); }
      .ai-search-close:hover { color:var(--ai-error); }
      .ai-search-highlight { background:var(--ai-warning-light);border:2px solid var(--ai-warning);padding:2px;border-radius:2px; }
      .ai-search-highlight.current { background:var(--ai-warning);color:#fff; }
    `;
    document.head.appendChild(style);

    // 事件绑定
    searchBtn.addEventListener('click', () => {
      searchOverlay.style.display = 'block';
      searchOverlay.querySelector('.ai-search-input').focus();
    });

    const input = searchOverlay.querySelector('.ai-search-input');
    const prevBtn = searchOverlay.querySelector('.ai-search-prev');
    const nextBtn = searchOverlay.querySelector('.ai-search-next');
    const closeBtn = searchOverlay.querySelector('.ai-search-close');

    input.addEventListener('input', (e) => performSearch(e.target.value));
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') navigateMatch(e.shiftKey ? -1 : 1);
      if (e.key === 'Escape') closeSearch();
    });

    prevBtn.addEventListener('click', () => navigateMatch(-1));
    nextBtn.addEventListener('click', () => navigateMatch(1));
    closeBtn.addEventListener('click', closeSearch);
  }

  function performSearch(query) {
    // 清除旧高亮
    clearHighlights();
    searchMatches = [];
    currentMatchIndex = -1;

    if (!query.trim()) {
      updateSearchCount();
      return;
    }

    // 搜索主内容区域
    const mainContent = document.querySelector('.ai-main') || document.body;
    const walker = document.createTreeWalker(mainContent, NodeFilter.SHOW_TEXT, null, false);
    const regex = new RegExp(query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');

    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (node.parentElement.tagName === 'SCRIPT' || node.parentElement.tagName === 'STYLE') continue;
      
      const matches = node.textContent.match(regex);
      if (matches) {
        const range = document.createRange();
        let startIndex = 0;
        
        matches.forEach(() => {
          const matchIndex = node.textContent.indexOf(matches[0], startIndex);
          if (matchIndex >= 0) {
            range.setStart(node, matchIndex);
            range.setEnd(node, matchIndex + query.length);
            
            const highlight = document.createElement('span');
            highlight.className = 'ai-search-highlight';
            range.surroundContents(highlight);
            searchMatches.push(highlight);
            
            startIndex = matchIndex + query.length;
          }
        });
      }
    }

    updateSearchCount();
    if (searchMatches.length > 0) navigateMatch(1);
  }

  function clearHighlights() {
    document.querySelectorAll('.ai-search-highlight').forEach(el => {
      const parent = el.parentNode;
      parent.replaceChild(document.createTextNode(el.textContent), el);
      parent.normalize();
    });
  }

  function navigateMatch(direction) {
    if (searchMatches.length === 0) return;

    currentMatchIndex += direction;
    if (currentMatchIndex < 0) currentMatchIndex = searchMatches.length - 1;
    if (currentMatchIndex >= searchMatches.length) currentMatchIndex = 0;

    searchMatches.forEach(m => m.classList.remove('current'));
    const current = searchMatches[currentMatchIndex];
    current.classList.add('current');
    current.scrollIntoView({ behavior: 'smooth', block: 'center' });

    updateSearchCount();
  }

  function updateSearchCount() {
    const countEl = searchOverlay?.querySelector('.ai-search-count');
    if (countEl) {
      if (searchMatches.length === 0) {
        countEl.textContent = '无结果';
      } else {
        countEl.textContent = `${currentMatchIndex + 1}/${searchMatches.length}`;
      }
    }
  }

  function closeSearch() {
    if (searchOverlay) {
      searchOverlay.style.display = 'none';
      clearHighlights();
      searchMatches = [];
      currentMatchIndex = -1;
    }
  }

  // ========== 初始化 ==========
  document.addEventListener('DOMContentLoaded', () => {
    initMobileTOC();
    initTOCScrollSpy();
    initCopyButtons();
    initMobileNav();
    initSearch();
    updateProgressUI();

    // 监听其他标签页的进度更新
    window.addEventListener(STORAGE_EVENT, updateProgressUI);

    // 完成按钮事件
    const btn = document.querySelector('.ai-complete-btn');
    if (btn) {
      btn.addEventListener('click', () => {
        const cid = btn.dataset.chapterId;
        if (cid) markChapterComplete(cid);
      });
    }
  });

  // 导出供外部使用
  window.AINotes = { markChapterComplete, isChapterComplete, getProgress, performSearch };
})();
