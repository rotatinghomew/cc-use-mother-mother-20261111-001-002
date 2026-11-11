from __future__ import annotations
import hashlib,json,re
from collections import defaultdict,deque
from typing import Any,Mapping
def stable(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(v): return hashlib.sha256(stable(v).encode()).hexdigest()
class BusinessError(ValueError): pass

from evidence_mesh.versions.snapshot_store import process_fixture
TAG=re.compile(r'<[^>]+>'); SPACE=re.compile(r'\s+')
def canonical(text): return SPACE.sub(' ',TAG.sub(' ',str(text)).replace('&nbsp;',' ').replace('&amp;','&')).strip()
def run(raw,database):
 p=raw.get('payload',raw); url=str(p.get('url','https://local.invalid/guideline')); body=canonical(p.get('body','')); old=canonical(p.get('old_body',''))
 new_tokens=body.split(); old_tokens=old.split(); old_set=set(old_tokens); new_set=set(new_tokens)
 added=[x for x in new_tokens if x not in old_set]; removed=[x for x in old_tokens if x not in new_set]
 similarity=len(old_set&new_set)/len(old_set|new_set) if old_set|new_set else 1.0
 snapshot={'url':url,'canonical_body':body,'content_key':digest(body),'added':added,'removed':removed,'similarity':similarity,'material':bool(added or removed),'redirects':min(5,int(p.get('redirects',0))),'citation':f"{url}#{digest(body)[:12]}"}
 stored=process_fixture(database,{'subject_id':url,'request_key':snapshot['content_key'],'payload':snapshot})
 return {'snapshot':snapshot,'stored':stored}
