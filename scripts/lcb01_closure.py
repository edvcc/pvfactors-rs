"""Small receipt gate: Owner approval alone cannot replace verified provenance."""
import hashlib
import json
from pathlib import Path
import subprocess

SUMMARY='evidence/execution/launch-closure/lcb-01/verification-summary.json'
RECEIPTS='evidence/execution/launch-closure/lcb-01/owner-closure/receipts/'


def check(root):
    errors=[]
    try:
        data=json.loads((root/SUMMARY).read_text())
        if data.get('status')!='LCB-01 — CLOSED': raise ValueError('closure receipt not complete')
        content=data['tested_content_commit'];receipt=data['receipt_commit']
        if data['tested_checkpoint']!=content or not data['clean_at_verification']: raise ValueError('tested content identity')
        def git(*args): return subprocess.check_output(['git',*args],cwd=root,text=True,stderr=subprocess.DEVNULL).strip()
        for sha in (content,receipt):
            if git('rev-parse',sha+'^{commit}')!=sha: raise ValueError('not an exact commit')
        if subprocess.run(['git','merge-base','--is-ancestor',content,receipt],cwd=root,capture_output=True).returncode:
            raise ValueError('receipt does not descend from content')
        changed=git('diff','--name-only',content,receipt).splitlines()
        if not changed or any(not p.startswith(RECEIPTS) for p in changed): raise ValueError('receipt commit changes tested content')
        for rel,sha in data['tested_object_hashes'].items():
            p=root/rel
            if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=sha: errors.append('tested object changed '+rel)
        for rel,sha in data['receipt_hashes'].items():
            p=root/rel
            if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=sha: errors.append('receipt changed '+rel)
        remote=json.loads((root/data['remote_proof']).read_text())
        resolved={x['resolved_sha'] for x in remote['commits'] if x['remote_resolvable'] and x['http_status']==200}
        if not {content,receipt}<=resolved or not data['remote_resolvable']: errors.append('remote provenance incomplete')
        for key in ('candidate_verifier','harness_self_tests','independent_oracle','baseline_integrity'):
            if data['verification'][key]!='PASS': errors.append(key+' not PASS')
        if data['production_implementation_started']: errors.append('production started')
    except (OSError,KeyError,ValueError,TypeError,subprocess.CalledProcessError) as error:
        errors.append(str(error))
    return {'status':'NOT_READY' if errors else 'PASS','errors':errors}
