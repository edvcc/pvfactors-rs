"""Package unapproved research receipts; never promotes an oracle."""
import collections
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
C=ROOT/'reference/candidate/vf-lcb01-v0.1'
E=ROOT/'evidence/execution/launch-closure/lcb-01'
def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x): p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')


def crosses_pair_interior(receiver,source,blockers):
    """Positive-measure ray obstruction for these fully facing segment pairs.

    A row intersects the interior of their convex hull iff it intersects an
    open set of joining rays. Boundary-only contacts have zero measure.
    Used for anomaly taxonomy only, never to generate candidate F.
    """
    def cross(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    pts=sorted(set(tuple(p) for p in [*receiver,*source]))
    def half(seq):
        h=[]
        for p in seq:
            while len(h)>1 and cross(h[-2],h[-1],p)<=0: h.pop()
            h.append(p)
        return h
    hull=half(pts)[:-1]+half(pts[::-1])[:-1]
    if len(hull)<3: return False
    for p,q in blockers:
        lo,hi=0.,1.
        for a,b in zip(hull,hull[1:]+hull[:1]):
            u=cross(a,b,p);v=cross(a,b,q)-u
            if v==0:
                if u<=0: hi=lo;break
            elif v>0: lo=max(lo,-u/v)
            else: hi=min(hi,-u/v)
        if lo<hi: return True
    return False


def main():
    if (C/'manifest.json').exists() and read(C/'manifest.json')['status']=='APPROVED_TARGETED_ORACLE_SEED':
        raise ValueError('Historical research packager cannot refresh the Owner-approved targeted seed')
    scan=read(E/'domain-scan.json');cases=[x['case_id'] for x in scan['cases']]
    fast=[];signs=[];abs_remaining=[]
    for summary in scan['cases']:
        cid=summary['case_id'];raw=read(C/'raw'/f'{cid}.json');corrected=read(C/'corrected'/f'{cid}.json')
        corrected['fast_group_candidate']=summary['fast_helpers']
        changes=corrected['field_provenance']['changed_above_candidate_comparator']
        changes[:]=[x for x in changes if not x['path'].startswith('/fast_helpers/')]
        for item in summary['fast_helpers']:
            for field in ('back_ground','back_pv'):
                independent=item['independent_'+field]
                if abs(item[field]-independent)>2e-9:
                    record=dict(case_id=cid,tilt=summary['tilt'],surface_azimuth=summary['surface_azimuth'],
                        row=item['row'],field=field,reference=item[field],candidate=independent,
                        receiver_side='back',source_kind='ground' if field=='back_ground' else 'pvrow')
                    fast.append(record)
                    changes.append(dict(path=f"/fast_helpers/{item['row']}/{field}",reference=item[field],corrected=independent,
                        provenance=['DEV-028 PROPOSED','CDR-008 PROPOSED','finite physical matrix aggregation']))
        # Same canonical compact serialization as the numerical generator.
        (C/'corrected'/f'{cid}.json').write_text(json.dumps(corrected,separators=(',',':'),allow_nan=False)+'\n')
        cv={(i,j):v for i,j,v in corrected['matrix']['entries']}
        for x in raw['formula_internals']:
            if x['after_side_filter'] < -1e-10:
                signs.append(dict(case_id=cid,**x,height_tie=x['high'][1]==x['low'][1]))
            if abs(abs(x['after_side_filter'])-cv.get((x['pv'],x['ground']),0.))>2e-9:
                abs_remaining.append(dict(case_id=cid,**x,candidate=cv.get((x['pv'],x['ground']),0.)))
    write(E/'formula-sign-diagnostics.json',dict(negative_pv_ground_helper_count=len(signs),
        all_negative_helpers_have_exact_height_tie=all(x['height_tie'] for x in signs),entries=signs,
        restricted_abs_helper_mismatches=abs_remaining,
        scope='Restricted abs empirical result only; not proof of general visibility or Fast correctness.'))
    write(E/'fast-helper-comparison.json',dict(affected_case_count=len({x['case_id'] for x in fast}),
        affected_field_count=len(fast),entries=fast,
        scope='Fast group geometry only, not a Fast irradiance simulation or approved compatibility change.'))
    anomalies=read(E/'anomaly-taxonomy.json')
    for case in anomalies:
        raw=read(C/'raw'/f"{case['case_id']}.json");surfaces=raw['surfaces']
        for entry in case['entries']:
            i,j=entry['receiver_reference_index'],entry['source_reference_index']
            if j==len(surfaces):
                entry['physical_obstruction']='NOT_APPLICABLE_RESIDUAL';entry['physical_ground_side']=None
                continue
            a,b=surfaces[i],surfaces[j];ki,kj=a['logical_key'],b['logical_key']
            blockers=[row for r,row in enumerate(raw['opaque_rows']) if r not in (ki['row'],kj['row'])]
            entry['physical_obstruction']='OBSTRUCTED' if crosses_pair_interior(a['coordinates_m'][0],b['coordinates_m'][0],blockers) else 'UNOBSTRUCTED'
            g,pv=(a,b) if ki['kind']=='ground' else (b,a)
            gx=[p[0] for p in g['coordinates_m'][0]];px=[p[0] for p in pv['coordinates_m'][0]]
            entry['physical_ground_side']='LEFT' if max(gx)<=min(px) else ('RIGHT' if min(gx)>=max(px) else 'OVERLAPS_ROW_PROJECTION')
    write(E/'anomaly-taxonomy.json',anomalies)
    approved=read(ROOT/'reference/approved/geometry-golden-v0.1/corrected/TILT_180.json')
    raw=read(C/'raw/VF053.json')
    equality=raw['surfaces']==approved['result']['surfaces']
    write(E/'geometry-equality.json',dict(case_id='VF053',approved_case='TILT_180',all_surface_records_exact=equality,
        approved_artifact_sha256=sha(ROOT/'reference/approved/geometry-golden-v0.1/corrected/TILT_180.json')))
    assert equality
    repeat=ROOT/'reference/work/lcb01-recapture'
    receipts=[]
    for rel in [f'raw/{x}.json' for x in cases]:
        receipts.append(dict(path=rel,first=sha(C/rel),second=sha(repeat/rel)))
    write(E/'raw-reproducibility.json',dict(status='PASS' if all(x['first']==x['second'] for x in receipts) else 'FAIL',
        artifacts=len(receipts),receipts=receipts,
        metadata_boundary='Incremental capture warning inventory excludes earlier cases; canonical capture.json is the complete rerun receipt. Raw case bytes are independently identical.'))
    assert all(x['first']==x['second'] for x in receipts)
    policy=dict(id='vf-lcb01-research-comparator-v0.1',status='PROPOSED_UNAPPROVED',bounds_epsilon=1e-10,
        expected_abs=2e-9,reciprocity_absolute_length=1e-10,closure_abs=1e-10,
        rationale='Quadrature requested 1e-11; allow 10x for scalar bounds/closure and 200x for candidate comparison. Observed estimates <1e-14 and independent checks <3e-15. Research budget, not a certified cross-platform bound.',
        exact=['SurfaceKey','ReferenceIndex','active','coordinates','normal','matrix shape','case inventory'],
        forbidden='No clamp, no topology tolerance, no geometry-tolerance-v0.1 modification; Owner must approve any future acceptance policy.')
    write(C/'comparator-policy.json',policy)
    manifest=dict(schema_version=1,status='PROPOSED_UNAPPROVED',candidate_id='vf-lcb01-v0.1',
        base_sha='d5bc38ebd6ba853c4cec530e4787d1ab6168203d',reference_revision='ecbfc863657e239817603a43898ae173c7ccad9c',
        environment_id=read(C/'capture.json')['environment']['runtime']['environment_id'],
        cases=cases,case_count=len(cases),artifact_count=3*len(cases),
        scope='LCB-01 geometric F and finite Fast group candidates only; not complete P4/AOI oracle coverage',
        candidate_comparator=policy,provenance=['DEV-028 PROPOSED / UNAPPROVED','CDR-008 PROPOSED — AWAITING OWNER REVIEW'],
        files={p.relative_to(C).as_posix():sha(p) for p in sorted(C.rglob('*.json')) if p.name!='manifest.json'},
        generator_files={p.relative_to(ROOT).as_posix():sha(p) for p in sorted((ROOT/'reference/launch-closure/lcb01').glob('*.py'))},
        comparator_file=dict(path='scripts/verify_vf_candidate.py',sha256=sha(ROOT/'scripts/verify_vf_candidate.py')))
    write(C/'manifest.json',manifest)
    write(E/'candidate-index.json',dict(manifest='reference/candidate/vf-lcb01-v0.1/manifest.json',sha256=sha(C/'manifest.json'),
         cases=len(cases),artifacts=3*len(cases),approval='UNAPPROVED'))
    print(json.dumps(dict(cases=len(cases),negative_helpers=len(signs),fast_differences=len(fast),manifest_sha256=sha(C/'manifest.json'))))


if __name__=='__main__': main()
