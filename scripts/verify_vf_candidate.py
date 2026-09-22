#!/usr/bin/env python3
"""Approved LCB-01 targeted seed verification; never complete P4 acceptance.

epsilon is an explicit comparator allowance, never an algorithm clamp. This
module has no production physics and does not modify frozen G2 tooling.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SEED_STATUS='APPROVED_TARGETED_ORACLE_SEED'
POLICY_STATUS='APPROVED FOR LCB-01 TARGETED ORACLE SEED'


def read(path):
    def reject(value): raise ValueError('non-standard JSON constant '+value)
    return json.loads(path.read_text(),parse_constant=reject)


def exact(a,b):
    return json.dumps(a,sort_keys=True,separators=(',',':'))==json.dumps(b,sort_keys=True,separators=(',',':'))


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


def fast_group_errors(data,raw,epsilon):
    """Check finite exchange aggregation, not Fast irradiance/simulation."""
    errors=[];f=matrix(data);surfaces=data['surfaces']
    rows=sorted({s['logical_key']['row'] for s in surfaces if s['logical_key']['kind']=='pvrow'})
    groups=data.get('fast_group_candidate',[])
    if [x.get('row') for x in groups]!=rows: return ['Fast row inventory']
    raw_by_row={x['row']:x for x in raw['fast_helpers']}
    for group in groups:
        row=group['row'];receivers=[i for i,s in enumerate(surfaces) if s['active'][0]
            and s['logical_key']['row']==row and s['logical_key']['side']=='back']
        length=math.fsum(surfaces[i]['length_m'][0] for i in receivers)
        if length<=0: errors.append('Fast empty receiver');continue
        for field in ('back_ground','back_pv','back_shaded_pv'):
            if not exact(group[field],raw_by_row[row][field]): errors.append('Fast raw provenance '+field)
        for kind,field in (('ground','independent_back_ground'),('pvrow','independent_back_pv')):
            expected=math.fsum(surfaces[i]['length_m'][0]*math.fsum(f[i][j] for j,s in enumerate(surfaces)
                if s['active'][0] and s['logical_key']['kind']==kind) for i in receivers)/length
            observed=group[field]
            if not isinstance(observed,(float,int)) or not math.isfinite(observed) or abs(expected-observed)>epsilon:
                errors.append(f'Fast finite aggregation row={row} {field}')
    return errors


def compare_payload(expected,actual,epsilon):
    errors=[]
    if not exact(expected['surfaces'],actual['surfaces']): return ['exact Geometry mismatch']
    a,b=matrix(expected),matrix(actual)
    if any(not math.isfinite(y) or abs(x-y)>epsilon for ar,br in zip(a,b) for x,y in zip(ar,br)):
        errors.append('expected geometric F mismatch')
    eg=expected.get('fast_group_candidate',[]);ag=actual.get('fast_group_candidate',[])
    if [g['row'] for g in eg]!=[g['row'] for g in ag]: return errors+['expected Fast inventory mismatch']
    for x,y in zip(eg,ag):
        for k in ('independent_back_ground','independent_back_pv'):
            if not math.isfinite(y[k]) or abs(x[k]-y[k])>epsilon: errors.append('expected Fast mismatch')
    return errors


def verify(root,actual=None):
    manifest=read(root/'manifest.json');errors=[]
    if manifest['status']!=SEED_STATUS: errors.append('seed approval status changed')
    owner=read(ROOT/'docs/execution/launch/LCB-01_OWNER_DECISIONS.json')
    objects=owner['approved_objects']
    for name,path in [('manifest_sha256',root/'manifest.json'),('comparator_policy_sha256',root/'comparator-policy.json')]:
        if hashlib.sha256(path.read_bytes()).hexdigest()!=objects[name]: errors.append('Owner approval hash '+name)
    policy=read(root/'comparator-policy.json')
    if policy['status']!=POLICY_STATUS or policy['production_tolerance_status']!='NOT YET FINAL P4 CROSS-PLATFORM TOLERANCE':
        errors.append('targeted comparator approval scope')
    if not exact(policy,manifest['candidate_comparator']): errors.append('comparator manifest mismatch')
    cases=manifest['cases']
    if not cases or len(cases)!=len(set(cases)): errors.append('empty/duplicate case inventory')
    actual_files={p.relative_to(root).as_posix() for p in root.rglob('*.json') if p.name!='manifest.json'}
    if actual_files!=set(manifest['files']): errors.append('manifest file inventory')
    repo=ROOT
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
        if actual is not None and {p.stem for p in (actual/phase).glob('*.json')}!=set(cases): errors.append('actual case inventory '+phase)
    if len(cases)!=66 or manifest['case_count']!=66 or manifest['artifact_count']!=198: errors.append('approved 66/198 inventory')
    count=0
    for cid in cases:
        p=root/'corrected'/f'{cid}.json'
        if not p.is_file(): continue
        try:
            corrected=read(p);raw=read(root/'raw'/f'{cid}.json')
            normalized=read(root/'normalized'/f'{cid}.json')
            if corrected['status']!=SEED_STATUS: errors.append('corrected approval status '+cid)
            if not exact(corrected['surfaces'],raw['surfaces']) or not exact(normalized['surfaces'],raw['surfaces']):
                errors.append('geometry changed '+cid)
            if normalized['matrix']!=raw['matrix']: errors.append('normalized Reference changed '+cid)
            r=invariants(matrix(corrected),corrected['surfaces'],manifest['candidate_comparator']['bounds_epsilon'])
            if r['status']!='PASS': errors.append('invariants '+cid)
            if corrected['convergence_max']>manifest['candidate_comparator']['expected_abs']: errors.append('unconverged '+cid)
            errors.extend(cid+': '+x for x in fast_group_errors(corrected,raw,policy['expected_abs']))
            if actual is not None:
                observed=read(actual/'corrected'/f'{cid}.json')
                if (actual/'raw'/f'{cid}.json').read_bytes()!=(root/'raw'/f'{cid}.json').read_bytes(): errors.append('raw recapture changed '+cid)
                if not exact(read(actual/'normalized'/f'{cid}.json'),normalized): errors.append('normalized recapture changed '+cid)
                errors.extend(cid+': '+x for x in compare_payload(corrected,observed,policy['expected_abs']))
                errors.extend(cid+': '+x for x in fast_group_errors(observed,raw,policy['expected_abs']))
                if invariants(matrix(observed),observed['surfaces'],policy['bounds_epsilon'])['status']!='PASS': errors.append('actual invariants '+cid)
            count+=1
        except (ValueError,KeyError,TypeError,OSError) as e: errors.append(cid+': '+str(e))
    return dict(status='FAIL' if errors or count!=len(cases) else ('PASS' if actual is not None else 'NOT_READY'),cases_run=count,
                errors=errors,scope='LCB01_TARGETED_ORACLE_SEED',approval=SEED_STATUS,p4_acceptance='NOT_READY',
                expected_comparison='PASS' if actual is not None and not errors else ('FAIL' if actual is not None else 'NOT_RUN'),
                fast_group_policy='PASS' if not errors else 'FAIL')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('candidate',type=Path)
    parser.add_argument('--actual',type=Path,help='fresh independent reconstruction with all raw/normalized/corrected artifacts')
    args=parser.parse_args()
    try: report=verify(args.candidate,args.actual)
    except (ValueError,KeyError,TypeError,OSError) as error: report=dict(status='FAIL',errors=[str(error)])
    print(json.dumps(report,indent=2));raise SystemExit({'PASS':0,'FAIL':1,'NOT_READY':2}[report['status']])
