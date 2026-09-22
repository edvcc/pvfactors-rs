"""LCB-01 frozen R0 capture only; no Reference or Geometry modifications.

Reference behavior/provenance: vfmethods.py at frozen ecbfc863. Raw matrices
use lossless sparse JSON (all omitted entries are exactly zero, not small).
"""
import argparse
import json
import math
from pathlib import Path
import sys
import warnings

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / 'upstream/solarfactors'), str(ROOT / 'reference/tools')]
from geometry_golden import environment_report, ordered_surface_records, coords_at
from pvfactors.geometry import OrderedPVArray
from pvfactors.viewfactors import VFCalculator


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, separators=(',', ':'), allow_nan=False) + '\n')


def inventory():
    tilts = [0., 1e-10, 1., 45., 89.9, 90., math.nextafter(90., math.inf),
             90.00000001, 100., 120., 150., 179., 179.9,
             math.nextafter(180., -math.inf), 180.]
    specs = {(t, a, 3, 1) for t in tilts for a in (90., 270.)}
    # Bounded covering set, not the full tilt x N x cut Cartesian product.
    specs |= {(t, a, n, c) for t in (45., 120., 180.)
              for a in (90., 270.) for n, c in ((1, 1), (2, 2), (3, 2), (11, 1))}
    specs |= {(90., a, 11, 2) for a in (90., 270.)}
    extension = {(t,a,3,cut) for t in (179.9999999999,179.999999999999,
              179.9999999999999,math.nextafter(180.,-math.inf),180.)
              for a in (90.,270.) for cut in (4,)}
    return sorted(specs)+sorted(extension-specs)


def point(p):
    return [float(x) if math.isfinite(float(x)) else ('+Infinity' if x>0 else '-Infinity')
            for x in (p.x[0],p.y[0])]


def internals(p, surfaces):
    """Read actual helper outputs/branch inputs, without monkey-patching source."""
    m = VFCalculator().vf_ts_methods
    out = []
    for ps in p.all_ts_surfaces:
        pk = surfaces[ps.index]['logical_key']
        if pk['kind'] != 'pvrow' or ps.length[0] <= 1e-8:
            continue
        row = pk['row']
        for side in ('left', 'right'):
            left = side == 'left'
            edge = (left and row == 0) or (not left and row == len(p.ts_pvrows)-1)
            op = None if edge else p.ts_pvrows[row + (-1 if left else 1)].full_pvrow_coords.lowest_point
            for gs in p.ts_ground.ts_surfaces_side_of_cut_point(side, row):
                if gs.length[0] <= 1e-8:
                    continue
                hi, lo = ps.highest_point, ps.lowest_point
                a, b = gs.b1, gs.b2
                pairs = ((hi,a),(lo,b),(hi,b),(lo,a)) if left else ((hi,b),(lo,a),(hi,a),(lo,b))
                strings = [float(m._hottel_string_length(x,y,op,left)[0]) for x,y in pairs]
                signed = (strings[2]+strings[3]-strings[0]-strings[1])/(2*float(ps.length[0]))
                pre = float(m._vf_surface_to_surface(ps.coords, gs, ps.length)[0]) if edge else signed
                result, reverse = m.vf_pvrow_surf_to_gnd_surf_obstruction_hottel(
                    ps,row,len(p.ts_pvrows),p.rotation_vec>0,p.ts_pvrows,gs,ps.length,
                    is_back=pk['side']=='back',is_left=left)
                out.append(dict(pv=ps.index,ground=gs.index,ground_side=side,
                    path='unobstructed' if edge else 'obstruction_helper',
                    high=point(hi),low=point(lo),obstruction=point(op) if op else None,
                    l1=strings[0],l2=strings[1],d1=strings[2],d2=strings[3],
                    signed=signed,before_side_filter=pre,after_side_filter=float(result[0]),
                    reverse=float(reverse[0])))
    return out


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--only-new',action='store_true')
    args=parser.parse_args(); cases=[]
    existing_manifest=args.output/'manifest.json'
    if existing_manifest.exists() and json.loads(existing_manifest.read_text())['status']=='APPROVED_TARGETED_ORACLE_SEED':
        raise ValueError('Use a fresh work directory; never overwrite an approved targeted seed')
    environment=environment_report()
    if not environment['canonical_environment_match'] or environment['runtime']['environment_id']!='031158a1d1be8cdb9093':
        raise RuntimeError('LCB-01 raw capture requires the frozen R0 environment')
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter('always')
        for number,(tilt,azimuth,n,cut) in enumerate(inventory()):
            cid=f'VF{number:03d}'
            existing=args.output/'raw'/f'{cid}.json'
            if args.only_new and existing.exists():
                cases.append(json.loads(existing.read_text())['input'])
                continue
            p=OrderedPVArray(n_pvrows=n,pvrow_height=1.,pvrow_width=1.,axis_azimuth=180.,gcr=.5,
                cut={i:{'front':cut,'back':cut} for i in range(n)})
            p.fit(np.array([45.]),np.array([azimuth]),np.array([tilt]),np.array([azimuth]))
            f=VFCalculator().build_ts_vf_matrix(p)[:,:,0]
            surfaces=ordered_surface_records(p)
            rows=[coords_at(r.full_pvrow_coords,0) for r in p.ts_pvrows]
            # Fast Reference helpers are captured separately, not confused with F.
            calc=VFCalculator(); m=calc.vf_ts_methods; fast=[]
            for row,r in enumerate(p.ts_pvrows):
                g=m.calculate_vf_to_gnd(r.full_pvrow_coords,row,n,1,p.ts_ground.y_ground,
                    p.ts_ground.cut_point_coords[row],r.full_pvrow_coords.length,p.rotation_vec>0,p.ts_pvrows)
                pv,sh=m.calculate_vf_to_pvrow(r.full_pvrow_coords,row,n,1,p.ts_pvrows,
                    r.full_pvrow_coords.length,p.rotation_vec>0,1.,p.rotation_vec)
                fast.append(dict(row=row,back_ground=float(g[0]),back_pv=float(pv[0]),back_shaded_pv=float(sh[0])))
            spec=dict(case_id=cid,tilt=tilt,surface_azimuth=azimuth,solar_azimuth=azimuth,
                      solar_zenith=45.,n_pvrows=n,cut=cut,pvrow_height=1.,pvrow_width=1.,gcr=.5,
                      axis_azimuth=180.,ground_extent=[-100.,100.])
            data=dict(input=spec,rotation=float(p.rotation_vec[0]),tilted_to_left=bool(p.rotation_vec[0]>0),
                surfaces=surfaces,opaque_rows=rows,cut_points=[point(x) for x in p.ts_ground.cut_point_coords],
                matrix=dict(shape=list(f.shape),omitted_value=0.,entries=[[int(i),int(j),float(f[i,j])] for i,j in zip(*np.nonzero(f))]),
                formula_internals=internals(p,surfaces),fast_helpers=fast)
            write(args.output/'raw'/f'{cid}.json',data);cases.append(spec)
            print(cid,tilt,azimuth,n,cut,flush=True)
    write(args.output/'capture.json',dict(reference_revision='ecbfc863657e239817603a43898ae173c7ccad9c',
          environment=environment,cases=cases,warnings=sorted(set(str(w.message) for w in ws))))


if __name__=='__main__':
    main()
