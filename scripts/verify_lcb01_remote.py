#!/usr/bin/env python3
"""Read-only GitHub commit-resolution receipt. Never prints credentials."""
import argparse
import datetime
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.error
import urllib.request

BRANCH='research/vf-lcb01-compatibility'
API='https://api.github.com/repos/edvcc/pvfactors-rs'


def verify(commits):
    if any(not re.fullmatch('[0-9a-f]{40}',s) for s in commits):
        raise ValueError('commit must be an exact SHA-1 commit ID')
    credential=subprocess.run(['git','credential','fill'],input='protocol=https\nhost=github.com\n\n',
        text=True,capture_output=True,env={**os.environ,'GIT_TERMINAL_PROMPT':'0'},timeout=30)
    fields=dict(x.split('=',1) for x in credential.stdout.splitlines() if '=' in x)
    headers={'Accept':'application/vnd.github+json','User-Agent':'pvfactors-lcb01-provenance','X-GitHub-Api-Version':'2022-11-28'}
    if fields.get('password'): headers['Authorization']='Bearer '+fields['password']
    def get(path):
        try:
            with urllib.request.urlopen(urllib.request.Request(API+path,headers=headers),timeout=30) as r:
                return r.status,json.load(r)
        except urllib.error.HTTPError as error:
            return error.code,json.loads(error.read())
    status,body=get('/git/ref/heads/'+BRANCH)
    head=body.get('object',{}).get('sha')
    rows=[]
    for sha in commits:
        code,data=get('/commits/'+sha)
        rows.append(dict(requested_sha=sha,http_status=code,resolved_sha=data.get('sha'),
            remote_resolvable=code==200 and data.get('sha')==sha,
            url='https://github.com/edvcc/pvfactors-rs/commit/'+sha))
    return dict(status='PASS' if status==200 and all(x['remote_resolvable'] for x in rows) else 'FAIL',
        observed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),repository='edvcc/pvfactors-rs',
        branch=BRANCH,remote_head=head,commits=rows)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--commit',action='append',required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    report=verify(a.commit);a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
    raise SystemExit(0 if report['status']=='PASS' else 1)
