"""Minimal frozen-reference VF domain conflict evidence; no correction applied."""
import argparse
import json
from pathlib import Path
import sys
import warnings

import numpy as np

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'upstream/solarfactors'))
sys.path.insert(0,str(ROOT/'reference/tools'))
from pvfactors.geometry import OrderedPVArray
from pvfactors.viewfactors import VFCalculator
from geometry_golden import ordered_surface_records, environment_report

parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
rows=[]
with warnings.catch_warnings(record=True) as ws:
    warnings.simplefilter('always')
    for tilt in [0.,45.,90.,120.,179.999999,180.]:
        p=OrderedPVArray(n_pvrows=3,pvrow_height=1.,pvrow_width=1.,axis_azimuth=180.,gcr=.5)
        p.fit(np.array([45.]),np.array([270.]),np.array([tilt]),np.array([270.]))
        F=VFCalculator().build_ts_vf_matrix(p)[:,:,0]
        L=np.array([s.length[0] for s in p.all_ts_surfaces])
        active=np.flatnonzero(L>1e-8)
        surfaces=ordered_surface_records(p)
        violations=[]
        for i in active:
            for j in [*active,len(L)]:
                if F[i,j]<-1e-12 or F[i,j]>1+1e-12:
                    violations.append({'receiver':surfaces[i]['logical_key'],'receiver_reference_index':int(i),
                        'receiver_length':float(L[i]),'source':'sky' if j==len(L) else surfaces[j]['logical_key'],
                        'source_reference_index':int(j),'F':float(F[i,j])})
        rows.append({'tilt':tilt,'active_reference_indices':active.tolist(),'surfaces':surfaces,
            'matrix_axes':['receiver','source'],'F':F.tolist(),'active_violations':violations,
            'active_row_closure_max_error':float(np.max(abs(F[active,:].sum(axis=1)-1))),
            'reciprocity_max_error':float(np.max(abs(L[:,None]*F[:-1,:-1]-L[None,:]*F[:-1,:-1].T))),
            'ground_physical_extent':[float(min(s.coords.b1.x[0] for s in p.ts_ground.all_ts_surfaces)),
                                      float(max(s.coords.b2.x[0] for s in p.ts_ground.all_ts_surfaces))]})
report={'status':'CONFLICT_OBSERVED' if any(x['active_violations'] for x in rows) else 'NO_CONFLICT',
    'reference_revision':'ecbfc863657e239817603a43898ae173c7ccad9c','environment':environment_report(),
    'input':{'n_pvrows':3,'pvrow_height':1.,'pvrow_width':1.,'axis_azimuth':180.,'gcr':.5,
             'solar_zenith':45.,'solar_azimuth':270.,'surface_azimuth':270.},
    'independent_constraint':'For nonnegative projected solid-angle measure over visible surfaces, 0<=F_ij<=1. This bound is not a floating-point comparator tolerance.',
    'warning_boundary':'No clamping, geometry patch or candidate expected values are generated.',
    'cases':rows,'warnings':sorted(set(str(w.message) for w in ws))}
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
print(json.dumps({'status':report['status'],'active_violations':{str(x['tilt']):len(x['active_violations']) for x in rows}}))
