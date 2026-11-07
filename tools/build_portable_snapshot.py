"""Build clean portable HTML from committed catalog/files, never browser test data."""
from pathlib import Path
import json,base64,hashlib,mimetypes,urllib.parse,datetime
root=Path(__file__).resolve().parents[1];d=root/'docs';cat=json.loads((d/'catalog.json').read_text());template=json.loads((d/'portable-template.json').read_text());records={}
for p in cat['projects']:
 for o in p['operations']:
  b=(root/o['filename']).read_bytes();assert hashlib.sha256(b).hexdigest()==o['sha256']
  records['blob:'+o['sha256']]={'base64':base64.b64encode(b).decode(),'type':'application/octet-stream','name':o['filename']}
 for im in p['images']:
  f=d/im['url'];b=f.read_bytes();assert hashlib.sha256(b).hexdigest()==im['sha256']
  records['blob:'+im['sha256']]={'base64':base64.b64encode(b).decode(),'type':mimetypes.guess_type(f.name)[0] or 'image/png','name':f.name}
  im['url']=urllib.parse.urljoin('https://111l9lpa.github.io/File-obmrn/',im['url'])
backup={'format':'cnc-library-backup-v1','exportedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'catalog':cat,'records':list(records.items())}
def safe(obj):return json.dumps(obj,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
boot='<script>window.PORTABLE_DATA='+safe(backup)+';window.PORTABLE_TEMPLATE='+safe(template)+';</script>'
html=template['html'].replace('<!--PORTABLE_BOOT-->',boot,1)
out=root/'CNC_LIBRARY_OFFLINE.html';out.write_text(html)
Path('/workspace/shared/downloads/CNC_LIBRARY_OFFLINE.html').write_text(html)
print('Clean portable snapshot:',out.stat().st_size,'bytes;',len(records),'verified assets; no test reports')
