"""Small reference-analysis probes; no Rust or replacement physics implementation."""
import os
for k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[k] = '1'
import sys, json, pathlib, warnings, platform, importlib.metadata as md, contextlib, io
import numpy as np
import pandas as pd
import shapely
ROOT = pathlib.Path(__file__).resolve().parents[2]
import argparse, datetime
parser=argparse.ArgumentParser()
parser.add_argument('--output-dir',type=pathlib.Path,required=True)
args=parser.parse_args()
DEST=args.output_dir.resolve()
DEST.mkdir(parents=True,exist_ok=False)
sys.path.insert(0, str(ROOT / 'upstream/solarfactors'))
from pvfactors.geometry import OrderedPVArray
from pvfactors.engine import PVEngine
from pvfactors.irradiance import HybridPerezOrdered, IsotropicOrdered
from pvfactors.viewfactors import VFCalculator
from pvfactors.irradiance.utils import perez_diffuse_luminance

def clean(x):
    if isinstance(x, np.ndarray): return clean(x.tolist())
    if isinstance(x, np.generic): return clean(x.item())
    if isinstance(x, dict): return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x, (list,tuple)): return [clean(v) for v in x]
    if isinstance(x,float) and not np.isfinite(x): return 'NaN' if np.isnan(x) else ('+Inf' if x>0 else '-Inf')
    return x

def run(name, model='hybrid', fast=False, aoi=False, **kw):
    geom=dict(n_pvrows=3,pvrow_height=1.,pvrow_width=1.,axis_azimuth=180.,gcr=.5)
    for key in list(kw):
        if key in geom or key=='cut': geom[key]=kw.pop(key)
    model_kw=kw.pop('model_kw', {})
    data=dict(DNI=600., DHI=100., solar_zenith=45.,solar_azimuth=270.,surface_tilt=45.,surface_azimuth=270.,albedo=.25)
    data.update(kw)
    data={k:np.atleast_1d(v).astype(float) for k,v in data.items()}
    fn=lambda angles: np.full_like(angles, .8, dtype=float)
    if aoi: model_kw.update(faoi_fn_front=fn,faoi_fn_back=fn)
    irr=(HybridPerezOrdered if model=='hybrid' else IsotropicOrdered)(**model_kw)
    vf=VFCalculator(faoi_fn_front=fn,faoi_fn_back=fn) if aoi else VFCalculator()
    p=OrderedPVArray(**geom); e=PVEngine(p,irradiance_model=irr,vf_calculator=vf)
    result=dict(name=name,geometry=geom,inputs=data,model=model,mode='fast' if fast else 'full',aoi=aoi)
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter('always')
        try:
            e.fit(pd.to_datetime(['2019-06-01 12:00+00:00']),**data)
            result['skip_step']=e.skip_step
            E,rho,inv,total=irr.get_full_ts_modeling_vectors(p)
            F=vf.build_ts_vf_matrix(p).copy()
            if fast: e.run_fast_mode(pvrow_index=min(1,geom['n_pvrows']-1))
            else: e.run_full_mode()
            result['n_surfaces']=p.n_ts_surfaces
            result['active_surfaces']=sum(s.length[0]>1e-8 for s in p.all_ts_surfaces)
            result['row_results']=[{side:{field:getattr(row,side).get_param_weighted(field) for field in (['qinc'] if fast else ['q0','qinc','qabs','isotropic','reflection'])} for side in (['back'] if fast else ['front','back'])} for row in (p.ts_pvrows[min(1,geom['n_pvrows']-1):min(1,geom['n_pvrows']-1)+1] if fast else p.ts_pvrows)]
            result['ground_length']=p.ts_ground.length
            result['minimum_y']=min(row.full_pvrow_coords.lowest_point.y[0] for row in p.ts_pvrows)
            result['F_mutated_by_AOI']=float(np.max(np.abs(F-p.ts_vf_matrix))) if not fast else None
            if not fast:
                B=np.eye(len(rho))-F[:,:,0]*rho[:,0][None,:]
                inc=np.linalg.solve(B,E[:,0])
                reference_inc=np.array([s.get_param('qinc')[0] for s in p.all_ts_surfaces]+[E[-1,0]])
                result['incident_form_difference_max']=float(np.max(np.abs(inc-reference_inc)))
                result['incident_form_residual']=float(np.max(np.abs(B@inc-E[:,0])))
                result['incident_form_row1_back']=float(sum(s.length[0]*inc[s.index] for s in p.ts_pvrows[min(1,geom['n_pvrows']-1)].back.all_ts_surfaces)/geom['pvrow_width'])
            if name=='nominal':
                np.savez_compressed(DEST/'nominal-trace.npz', E=E,rho=rho,inv_rho=inv,F=F,F_aoi=p.ts_vf_aoi_matrix.copy(),qinc=reference_inc,q0=np.array([s.get_param('q0')[0] for s in p.all_ts_surfaces]+[E[-1,0]]),A=np.diag(inv[:,0])-F[:,:,0],coords=np.array([s.coords.as_array for s in p.all_ts_surfaces]),lengths=np.array([s.length for s in p.all_ts_surfaces]))
        except Exception as ex:
            result['exception']=dict(type=type(ex).__name__,message=str(ex))
        result['warnings']=sorted(set(str(w.message) for w in ws))
    return result

probes=[run('nominal'),run('isotropic',model='isotropic'),run('zero_light'),run('zero_light_hybrid',DNI=0,DHI=0),run('zero_light_iso',model='isotropic',DNI=0,DHI=0),run('zero_dhi',DHI=0),run('zero_dni',DNI=0),run('zero_albedo',albedo=0),run('low_sun_back',solar_zenith=89.9,solar_azimuth=90),run('flat',surface_tilt=0),run('underground',pvrow_width=3,surface_tilt=80),run('horizon5',model_kw={'horizon_band_angle':5}),run('horizon15',model_kw={'horizon_band_angle':15}),run('circumsolar5',model_kw={'circumsolar_angle':5}),run('circumsolar60',model_kw={'circumsolar_angle':60}),run('aoi_constant',aoi=True),run('fast_hybrid',fast=True),run('fast_iso',model='isotropic',fast=True),run('one_row',n_pvrows=1),run('eleven_rows',n_pvrows=11),run('cuts',cut={1:{'front':3,'back':5}}),run('night',solar_zenith=100),run('negative_dni',DNI=-1)]
probes=[p for p in probes if p['name']!='zero_light']
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    try:
        perez_diffuse_luminance(['2020-01-02 15:00:00+00:00'],[86.43564127244697],[312.7],[78.53023197697105],[221.9758276910072],[100],[50])
        recursion='not reproduced'
    except Exception as ex: recursion=type(ex).__name__
out=dict(probes=probes,issue6=recursion)
(DEST/'probe-results.json').write_text(json.dumps(clean(out),indent=2,allow_nan=False))
env=dict(python=sys.version,platform=platform.platform(),machine=platform.machine(),libc=platform.libc_ver(),geos=shapely.geos_version_string,thread_env={k:os.environ[k] for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS')},packages={p:md.version(p) for p in ('numpy','scipy','pandas','pvlib','shapely','matplotlib','pytest','pytest-mock','mock')})
f=io.StringIO()
with contextlib.redirect_stdout(f):np.show_config()
env['numpy_config']=f.getvalue()
(DEST/'runtime.json').write_text(json.dumps(env,indent=2))
for p in probes:print(p['name'],p.get('exception',p.get('row_results')),p.get('F_mutated_by_AOI'))
print('issue6',recursion)
