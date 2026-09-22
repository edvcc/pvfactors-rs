#!/usr/bin/env python3
"""Research VF invariants; PASS is never P4 acceptance or oracle approval.

epsilon is an explicit comparator allowance, never an algorithm clamp. This
module has no production physics and does not modify frozen G2 tooling.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path


def invariants(f,surfaces,epsilon):
    if not math.isfinite(epsilon) or not 0<=epsilon<=1e-8:
        raise ValueError('invalid research comparator epsilon')
    n=len(surfaces);errors=[]
    if len(f)!=n+1 or any(len(r)!=n+1 for r in f):
        return dict(status='FAIL',errors=['matrix shape'])
    if any(not isinstance(v,(int,float)) or isinstance(v,bool) or not math.isfinite(v) for r in f for v in r):
        return dict(status='FAIL',errors=['nonfinite/non-numeric entry'])
    active=[i for i,s in enumerate(surfaces) if s['active'][0]]
    bound_count=0;closure=0.;reciprocity=0.
    for i in range(n+1):
        for j in range(n+1):
            v=f[i][j]
            if i not in active or (j<n and j not in active):
                if v!=0: errors.append(f'inactive/sky source row nonzero {i},{j}')
                continue
            if v < -epsilon or v > 1+epsilon:
                errors.append(f'bound {i},{j}: {v}');bound_count+=1
            if j<n:
                ki=surfaces[i]['logical_key'];kj=surfaces[j]['logical_key']
                forbidden=(i==j or ki['kind']==kj['kind']=='ground' or
                           (ki['kind']==kj['kind']=='pvrow' and
                            (ki['row']==kj['row'] or ki['side']==kj['side'])))
                if forbidden and abs(v)>epsilon: errors.append(f'forbidden support {i},{j}')
                residual=abs(surfaces[i]['length_m'][0]*v-surfaces[j]['length_m'][0]*f[j][i])
                reciprocity=max(reciprocity,residual)
        if i in active: closure=max(closure,abs(math.fsum(f[i])-1))
    if closure>epsilon: errors.append('row closure')
    if reciprocity>epsilon: errors.append('length reciprocity')
    return dict(status='FAIL' if errors else 'PASS',errors=errors,bound_violations=bound_count,
                row_closure_max_error=closure,reciprocity_max_error=reciprocity)


def matrix(data):
    m=data['matrix'];n=len(data['surfaces'])+1
    if m['shape']!=[n,n] or m['omitted_value']!=0.: raise ValueError('matrix metadata')
    f=[[0.]*n for _ in range(n)];seen=set()
    for i,j,v in m['entries']:
        if type(i) is not int or type(j) is not int or not 0<=i<n or not 0<=j<n or (i,j) in seen:
            raise ValueError('duplicate or invalid matrix index')
        seen.add((i,j));f[i][j]=v
    return f


def verify(root):
    manifest=json.loads((root/'manifest.json').read_text());errors=[]
    if manifest['status']!='PROPOSED_UNAPPROVED': errors.append('candidate approval status changed')
    cases=manifest['cases']
    if not cases or len(cases)!=len(set(cases)): errors.append('empty/duplicate case inventory')
    actual_files={p.relative_to(root).as_posix() for p in root.rglob('*.json') if p.name!='manifest.json'}
    if actual_files!=set(manifest['files']): errors.append('manifest file inventory')
    repo=Path(__file__).resolve().parents[1]
    for rel,sha in manifest['generator_files'].items():
        p=repo/rel
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=sha: errors.append('generator changed '+rel)
    checker=manifest['comparator_file'];p=repo/checker['path']
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=checker['sha256']: errors.append('comparator changed')
    for rel,sha in manifest['files'].items():
        p=root/rel
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=sha: errors.append('missing/mutated '+rel)
    for phase in ('raw','normalized','corrected'):
        if {p.stem for p in (root/phase).glob('*.json')}!=set(cases): errors.append('case inventory '+phase)
    count=0
    for cid in cases:
        p=root/'corrected'/f'{cid}.json'
        if not p.is_file(): continue
        try:
            corrected=json.loads(p.read_text());raw=json.loads((root/'raw'/f'{cid}.json').read_text())
            normalized=json.loads((root/'normalized'/f'{cid}.json').read_text())
            if corrected['surfaces']!=raw['surfaces'] or normalized['surfaces']!=raw['surfaces']:
                errors.append('geometry changed '+cid)
            if normalized['matrix']!=raw['matrix']: errors.append('normalized Reference changed '+cid)
            r=invariants(matrix(corrected),corrected['surfaces'],manifest['candidate_comparator']['bounds_epsilon'])
            if r['status']!='PASS': errors.append('invariants '+cid)
            if corrected['convergence_max']>manifest['candidate_comparator']['expected_abs']: errors.append('unconverged '+cid)
            count+=1
        except (ValueError,KeyError,TypeError,OSError) as e: errors.append(cid+': '+str(e))
    return dict(status='FAIL' if errors or count!=len(cases) else 'PASS',cases_run=count,
                errors=errors,scope='CANDIDATE_RESEARCH_ONLY',approval='UNAPPROVED',p4_acceptance='NOT_READY')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('candidate',type=Path);args=parser.parse_args()
    try: report=verify(args.candidate)
    except (ValueError,KeyError,TypeError,OSError) as error: report=dict(status='FAIL',errors=[str(error)])
    print(json.dumps(report,indent=2));raise SystemExit(0 if report['status']=='PASS' else 1)
