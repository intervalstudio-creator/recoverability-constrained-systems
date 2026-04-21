const CACHE = "recovs-cache-v1";
const ASSETS = ["./","index.html","style.css","app.js","manifest.webmanifest","assets/icon-192.png","assets/icon-512.png"];
self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(cache => cache.addAll(ASSETS)));
  self.skipWaiting();
});
self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
  );
  self.clients.claim();
});
self.addEventListener("fetch", e => {
  if(e.request.method !== "GET") return;
  e.respondWith(
    caches.match(e.request).then(resp => resp || fetch(e.request).then(networkResp => {
      const copy = networkResp.clone();
      caches.open(CACHE).then(cache => cache.put(e.request, copy));
      return networkResp;
    }).catch(() => caches.match("index.html")))
  );
});