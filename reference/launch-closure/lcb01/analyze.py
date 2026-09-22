"""Reconstruct candidate geometric F from independent visible angular measure.

Research-only; no automatic approval. Matrices use ReferenceIndex axes, with
sky last. Reciprocity supplies the reverse after independently integrating
the shorter PV receiver; it is consequently NOT an independent check here.
"""
import argparse
import copy
import json
from pathlib import Path
import sys

import numpy as np
from independent import pair, normal, decimal_hottel, line_factor

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts'))
from verify_vf_candidate import invariants


def read(p): return json.loads(p.read_text())
def write(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,separators=(',',':'),allow_nan=False)+'\n')
def dense(raw):
    f=np.zeros(raw['matrix']['shape'])
    for i,j,v in raw['matrix']['entries']: f[i,j]=v
    return f
def sparse(f):
    return dict(shape=list(f.shape),omitted_value=0.,entries=[[int(i),int(j),float(f[i,j])] for i,j in zip(*np.nonzero(f))])


def reconstruct(data,eps):
    surfaces=data['surfaces'];active=[i for i,s in enumerate(surfaces) if s['active'][0]]
    f=np.zeros((len(surfaces)+1,len(surfaces)+1));error=0.;neval=0
    for ix,i in enumerate(active):
        for j in active[ix+1:]:
            a,b=(j,i) if surfaces[i]['logical_key']['kind']=='ground' else (i,j)
            v,e,n=pair(data,a,b,eps);error=max(error,e);neval+=n
            f[a,b]=v;f[b,a]=v*surfaces[a]['length_m'][0]/surfaces[b]['length_m'][0]
    for i in active: f[i,-1]=1-f[i,:-1].sum()
    return f,error,neval


def taxonomy(data,i,j):
    s=data['surfaces'];ki=s[i]['logical_key'];kj=s[j]['logical_key'] if j<len(s) else dict(kind='sky',side=None,row=None,ground_element=None)
    pv=i if ki['kind']=='pvrow' else j;g=j if ki['kind']=='pvrow' else i
    internals=next((x for x in data['formula_internals'] if x['pv']==pv and x['ground']==g),None)
    return dict(pair_type=ki['kind']+'->'+kj['kind'],receiver_key=ki,source_key=kj,
                receiver_row=ki['row'],source_row=kj['row'],receiver_side=ki['side'],source_side=kj['side'],
                ground_element=(ki if ki['kind']=='ground' else kj).get('ground_element'),
                reference_path=internals['path'] if internals else 'pv_pair_or_residual',
                ground_side=internals['ground_side'] if internals else None)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--candidate',type=Path,required=True)
    parser.add_argument('--evidence',type=Path,required=True);parser.add_argument('--cases',nargs='*')
    parser.add_argument('--resume',action='store_true')
    args=parser.parse_args(); rows=[]; all_anomalies=[]
    if (args.candidate/'manifest.json').exists() and read(args.candidate/'manifest.json')['status']=='APPROVED_TARGETED_ORACLE_SEED':
        raise ValueError('Use a fresh work directory; never overwrite an approved targeted seed')
    if args.resume:
        rows=read(args.evidence/'domain-scan.json')['cases']
        all_anomalies=read(args.evidence/'anomaly-taxonomy.json')
    completed={x['case_id'] for x in rows}
    for path in sorted((args.candidate/'raw').glob('VF*.json')):
        cid=path.stem
        if cid in completed: continue
        if args.cases and cid not in args.cases: continue
        data=read(path);ref=dense(data);s=data['surfaces'];active=[i for i,x in enumerate(s) if x['active'][0]]
        f,error,n=reconstruct(data,1e-11)
        normalized=dict(case_id=cid,surfaces=s,matrix=data['matrix'])
        write(args.candidate/'normalized'/path.name,normalized)
        # A separately executed looser quadrature validates numerical stability;
        # this is not a second physical oracle. Decimal Hottel is checked separately.
        coarse,ce,cn=reconstruct(data,1e-7)
        convergence=float(np.max(abs(f-coarse)))
        changes=[];anomalies=[]
        for i in active:
            for j in [*active,len(s)]:
                delta=float(f[i,j]-ref[i,j]);v=float(ref[i,j])
                if abs(delta)>2e-9 or v < -1e-10 or v > 1+1e-10:
                    record=dict(receiver_reference_index=i,source_reference_index=j,
                        reference=v,candidate=float(f[i,j]),delta=delta,**taxonomy(data,i,j))
                    anomalies.append(record)
                    changes.append(dict(path=f'/matrix/{i}/{j}',reference=v,corrected=float(f[i,j]),
                        provenance=['DEV-028 APPROVED','CDR-008 APPROVED','independent visible-angle line integration']))
        rawinv=invariants(ref.tolist(),s,1e-10)
        newinv=invariants(f.tolist(),s,1e-10)
        fast=[]
        for item in data['fast_helpers']:
            ids=[i for i in active if s[i]['logical_key']['row']==item['row'] and s[i]['logical_key']['side']=='back']
            values={}
            for kind in ('ground','pvrow'):
                value=sum(s[i]['length_m'][0]*sum(f[i,j] for j in active if s[j]['logical_key']['kind']==kind) for i in ids)
                values[kind]=float(value)
            fast.append(dict(**item,independent_back_ground=values['ground'],independent_back_pv=values['pvrow']))
            for field,kind in (('back_ground','ground'),('back_pv','pvrow')):
                if abs(item[field]-values[kind])>2e-9:
                    changes.append(dict(path=f"/fast_helpers/{item['row']}/{field}",reference=item[field],
                        corrected=values[kind],provenance=['DEV-029 APPROVED','CDR-008 APPROVED','finite physical matrix aggregation']))
        write(args.candidate/'corrected'/path.name,dict(case_id=cid,status='PROPOSED_UNAPPROVED',
            surfaces=s,matrix=sparse(f),numeric_method='visible-angle/receiver quadrature eps=1e-11',
            field_provenance=dict(all_matrix_fields='independent angular integral; reverse by length reciprocity; sky residual',
                                  changed_above_candidate_comparator=changes),
            fast_group_candidate=fast,
            quadrature_error_estimate_max=error,convergence_max=convergence,invariants=newinv))
        row=dict(**data['input'],reference_invariants=rawinv,candidate_invariants=newinv,
                 anomalous_entries=len(anomalies),convergence_max=convergence,quadrature_error_estimate_max=error,
                 evaluation_count=n+cn,fast_helpers=fast)
        rows.append(row);all_anomalies.append(dict(case_id=cid,entries=anomalies))
        print(cid,'anomalies',len(anomalies),'candidate',newinv['status'],'convergence',convergence,flush=True)
    write(args.evidence/'domain-scan.json',dict(cases=rows,case_count=len(rows),
        affected_case_count=sum(x['anomalous_entries']>0 for x in rows),
        affected_entry_count=sum(x['anomalous_entries'] for x in rows),
        note='Observed covering-set domain, not an exhaustive proof over continuous inputs.'))
    write(args.evidence/'anomaly-taxonomy.json',all_anomalies)


if __name__=='__main__': main()
