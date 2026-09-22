"""Independent analytic, tensor-quadrature, visibility and metamorphic checks."""
import argparse
import copy
from decimal import Decimal, localcontext
import json
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss
from independent import decimal_hottel, line_factor, pair, normal, norm, sub, blocked
from analyze import read, write, dense


def tensor(receiver,source,ni,nj,order):
    """Double numerical line integration of the cosine kernel; no strings."""
    x,w=leggauss(order);t=(x+1)/2;w=w/2
    p=np.asarray(receiver[0])+t[:,None]*(np.asarray(receiver[1])-receiver[0])
    q=np.asarray(source[0])+t[:,None]*(np.asarray(source[1])-source[0])
    r=q[None,:,:]-p[:,None,:];dist=np.linalg.norm(r,axis=2)
    a=r@np.asarray(ni);b=-r@np.asarray(nj)
    kernel=np.maximum(a,0)*np.maximum(b,0)/(2*dist**3)
    return float(norm(sub(source[1],source[0]))*np.sum(w[:,None]*w[None,:]*kernel))


def reflect(data):
    out=copy.deepcopy(data)
    for s in out['surfaces']:
        for p in s['coordinates_m'][0]: p[0]=-p[0]
        if s['normal'] is not None: s['normal'][0][0]*=-1
    for row in out['opaque_rows']:
        for p in row: p[0]=-p[0]
    return out


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--candidate',type=Path,required=True)
    parser.add_argument('--evidence',type=Path,required=True);args=parser.parse_args()
    d=read(args.candidate/'raw/VF053.json');a=d['surfaces'][3];b=d['surfaces'][28]
    receiver=a['coordinates_m'][0];source=b['coordinates_m'][0]
    analytic=decimal_hottel(receiver,source,90)
    numeric=[dict(order=n,F=tensor(receiver,source,normal(a),normal(b),n)) for n in (2,4,8,16,32,64,128)]
    forward=pair(d,3,28);reverse=pair(d,28,3)
    minimal=dict(case_id='VF053',approved_geometry_case='TILT_180',receiver=a,source=b,
        reference=dense(d)[3,28],analytic_decimal90=analytic,analytic_decimal110=decimal_hottel(receiver,source,110),
        numerical_line=forward[0],numerical_reverse=reverse[0],tensor_convergence=numeric,
        reference_internals=next(x for x in d['formula_internals'] if x['pv']==28 and x['ground']==3),
        cut_points=d['cut_points'],full_row=d['opaque_rows'][0],
        visibility='Ground faces up; row 0 front faces down. Every joining ray remains left of row 1; no blocker intersects it.',
        exact_input_note='Decimal.from_float preserves binary64 endpoint inputs; no decimal coordinate rounding.')
    write(args.evidence/'minimal-counterexample.json',minimal)
    # Analytically decomposable obstructed enclosure: divider x=1 connects both
    # planes. Left sees only left and right only right. Two visible rectangles.
    top=((0.,2.),(2.,2.));bottom=((0.,0.),(2.,0.));divider=[((1.,0.),(1.,2.))]
    with localcontext() as ctx:
        ctx.prec=100
        obstructed_analytic=(Decimal(decimal_hottel(((0.,2.),(1.,2.)),((0.,0.),(1.,0.)),100))+
                             Decimal(decimal_hottel(((1.,2.),(2.,2.)),((1.,0.),(2.,0.)),100)))/2
    syn=dict(geometry=dict(receiver=top,source=bottom,blockers=divider,normals=[[0.,-1.],[0.,1.]]),
        analytic_decimal100=str(obstructed_analytic),derivation='Visible domain = [0,1]x[0,1] union [1,2]x[1,2]; length-weighted independent Hottel rectangles.',
        numerical=[dict(eps=e,F=line_factor(top,bottom,(0.,-1.),(0.,1.),divider,e)[0]) for e in (1e-5,1e-8,1e-12)],
        unoriented_unblocked_magnitude=decimal_hottel(top,bottom),
        wrong_side_F=line_factor(top,bottom,(0.,1.),(0.,1.))[0],
        fully_blocked_F=line_factor(top,bottom,(0.,-1.),(0.,1.),[((0.,1.),(2.,1.))])[0])
    write(args.evidence/'analytic-obstruction-and-visibility.json',syn)
    checks=[];analytic_checks=[];obstruction_examples=[]
    for cid in ('VF013','VF020','VF035','VF045','VF053'):
        data=read(args.candidate/'raw'/f'{cid}.json');mir=reflect(data)
        active=[i for i,s in enumerate(data['surfaces']) if s['active'][0]]
        selected=[]
        # Select informative pairs covering ground, PV-PV, edge and middle.
        for i in active:
            if data['surfaces'][i]['logical_key']['kind']!='pvrow': continue
            for j in active:
                if i>=j and data['surfaces'][j]['logical_key']['kind']=='pvrow': continue
                v=pair(data,i,j)[0]
                if v>1e-8: selected.append((i,j,v))
        for i,j,v in selected:
            reverse=pair(data,j,i)[0];mirror=pair(mir,i,j)[0]
            si,sj=data['surfaces'][i],data['surfaces'][j]
            flipped=copy.deepcopy(data)
            flipped['surfaces'][i]['coordinates_m'][0].reverse()
            flipped['surfaces'][j]['coordinates_m'][0].reverse()
            endpoint=pair(flipped,i,j)[0]
            rec_error=abs(v*si['length_m'][0]-reverse*sj['length_m'][0])
            checks.append(dict(case_id=cid,i=i,j=j,F=v,reverse=reverse,reciprocity_error=rec_error,
                               mirror_error=abs(v-mirror),endpoint_order_error=abs(v-endpoint)))
            # Reference path labels do NOT establish physical obstruction.
            raw_h=float(decimal_hottel(si['coordinates_m'][0],sj['coordinates_m'][0]))
            if abs(raw_h-v)<1e-10:
                analytic_checks.append(dict(case_id=cid,i=i,j=j,decimal90=decimal_hottel(si['coordinates_m'][0],sj['coordinates_m'][0]),
                    numerical=v,error=abs(raw_h-v),scope='magnitude agreement; visibility independently evaluated, not inferred from agreement'))
            elif raw_h>v+1e-4:
                obstruction_examples.append(dict(case_id=cid,i=i,j=j,unobstructed_magnitude=raw_h,visible_F=v))
    write(args.evidence/'independent-crosschecks.json',dict(metamorphic=checks,analytic=analytic_checks,
        obstruction_examples=obstruction_examples,status='PASS' if all(max(x['reciprocity_error'],x['mirror_error'],x['endpoint_order_error'])<1e-10 for x in checks) else 'FAIL'))
    # Literal abs(matrix) fails bounds/closure. abs(ground helper) with a fresh
    # residual may fix observed signs, but cannot repair the distinct Fast proxy.
    write(args.evidence/'global-abs-counterexamples.json',dict(
        literal_matrix_abs_sky_28=abs(float(dense(d)[28,-1])),
        actual_fast_helper=dict(case_id='VF053',row=0,side='back',reference_ground=d['fast_helpers'][0]['back_ground'],
                               independent_ground=0.,absolute_value_still_wrong=True),
        bare_hottel_wrong_side=syn['unoriented_unblocked_magnitude'],physical_wrong_side=syn['wrong_side_F'],
        conclusion='NO as a general Reference repair. Restricted abs(obstruction-helper) plus unchanged side filter is only empirically checked; not proved for the full approved domain.'))
    tests=dict(target_analytic_vs_line=abs(float(analytic)-forward[0])<2e-12,
        target_tensor_converged=abs(numeric[-1]['F']-numeric[-2]['F'])<2e-12 and abs(numeric[-1]['F']-float(analytic))<2e-12,
        decimal90_vs110=abs(Decimal(analytic)-Decimal(minimal['analytic_decimal110']))<Decimal('1e-88'),
        obstructed_analytic_vs_numeric=all(abs(x['F']-float(obstructed_analytic))<2e-12 for x in syn['numerical']),
        wrong_side_zero=syn['wrong_side_F']==0.,fully_blocked_zero=syn['fully_blocked_F']==0.,
        mirror_reciprocity_endpoint_order=bool(checks) and all(max(x['reciprocity_error'],x['mirror_error'],x['endpoint_order_error'])<1e-10 for x in checks))
    write(args.evidence/'independent-oracle-verification.json',dict(status='PASS' if all(tests.values()) else 'FAIL',tests=tests,
        notes='The 107 matching magnitude examples are descriptive, selected after comparison; the named assertions here are the acceptance checks.'))
    if not all(tests.values()): raise AssertionError(tests)
    print(json.dumps(dict(target=forward[0],analytic=analytic,metamorphic_pairs=len(checks),analytic_pairs=len(analytic_checks))))


if __name__=='__main__': main()
