const CACHE='cnc-shell-76a0133cb001';const FILES=["./", "index.html", "style.css", "core.js", "db.js", "app.js", "catalog.json", "portable-template.json", "manifest.webmanifest", "assets/icon.svg", "assets/icon-192.png", "assets/icon-512.png"];
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('cnc-shell-')&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);if(e.request.method!=='GET'||u.origin!==self.location.origin)return;
if(e.request.mode==='navigate'){e.respondWith(fetch(e.request).catch(()=>caches.match(new URL('./index.html',self.location.href))));return;}
e.respondWith(caches.match(e.request).then(cached=>cached||fetch(e.request)));});
