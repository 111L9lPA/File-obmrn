from pathlib import Path
import re,json,hashlib
root=Path(__file__).resolve().parents[1];d=root/'docs'
html=(d/'index.html').read_text();css=(d/'style.css').read_text()
code='\n'.join(re.sub(r'^import .*?;\s*','', (d/f).read_text(),flags=re.M).replace('export ','') for f in ['core.js','db.js','app.js'])
assert '</script>' not in code.lower()
portable=re.sub(r'<link rel="(manifest|icon)"[^>]*>','',html).replace('<link rel="stylesheet" href="style.css">','<style>'+css+'</style>').replace('<script type="module" src="app.js"></script>','<!--PORTABLE_BOOT--><script>'+code+'</script>')
(d/'portable-template.json').write_text(json.dumps({'html':portable},ensure_ascii=False))
files=['./','index.html','style.css','core.js','db.js','app.js','catalog.json','portable-template.json','manifest.webmanifest','assets/icon.svg','assets/icon-192.png','assets/icon-512.png']
ver=hashlib.sha256(''.join((d/f).read_text() for f in ['index.html','style.css','core.js','db.js','app.js','catalog.json']).encode()).hexdigest()[:12]
sw="""const CACHE='cnc-shell-VERSION';const FILES=FILES_VALUE;
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('cnc-shell-')&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);if(e.request.method!=='GET'||u.origin!==self.location.origin)return;
if(e.request.mode==='navigate'){e.respondWith(fetch(e.request).catch(()=>caches.match(new URL('./index.html',self.location.href))));return;}
e.respondWith(caches.match(e.request).then(cached=>cached||fetch(e.request)));});
""".replace('VERSION',ver).replace('FILES_VALUE',json.dumps(files))
(d/'sw.js').write_text(sw)
(d/'.nojekyll').touch()
print('Packaged portable template and service worker',ver)
