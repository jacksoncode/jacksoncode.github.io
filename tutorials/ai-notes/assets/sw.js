const CACHE_NAME = 'ai-notes-v1';
const STATIC_ASSETS = [
  './',
  './assets/ai-notes.css',
  './assets/ai-notes.js',
  './assets/manifest.json',
  './assets/vendor/font-awesome/css/all.min.css',
  './assets/vendor/katex/katex.min.css',
  './assets/vendor/katex/katex.min.js',
  './assets/vendor/katex/auto-render.min.js',
  './assets/vendor/prismjs/prism-tomorrow.min.css',
  './assets/vendor/prismjs/prism.min.js'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
    ))
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;
      return fetch(event.request).then(response => {
        if (!response || response.status !== 200 || response.type !== 'basic') return response;
        const clone = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        return response;
      });
    }).catch(() => caches.match('./'))
  );
});
