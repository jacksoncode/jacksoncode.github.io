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

  // ========== 初始化 ==========
  document.addEventListener('DOMContentLoaded', () => {
    initMobileTOC();
    initTOCScrollSpy();
    initCopyButtons();
    initMobileNav();
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
  window.AINotes = { markChapterComplete, isChapterComplete, getProgress };
})();
