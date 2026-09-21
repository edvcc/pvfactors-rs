import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import sys,json,pathlib,warnings
import numpy as np
import pandas as pd
R=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(R/'upstream/solarfactors'))
from shapely.geometry import LineString
from pvfactors.geometry.utils import difference,are_2d_vecs_collinear
from pvfactors.geometry import OrderedPVArray
from pvfactors.engine import PVEngine
from pvfactors.irradiance import HybridPerezOrdered
from pvfactors.viewfactors import VFCalculator
u=LineString([(0,0),(1,0)]);v=LineString([(-1,0),(2,0)])
fn=lambda a:np.full_like(a,.8,dtype=float)
p=OrderedPVArray(n_pvrows=3,pvrow_height=1,pvrow_width=1,gcr=.5,axis_azimuth=180)
e=PVEngine(p,irradiance_model=HybridPerezOrdered(faoi_fn_front=fn,faoi_fn_back=fn),vf_calculator=VFCalculator(faoi_fn_front=fn,faoi_fn_back=fn))
with warnings.catch_warnings():
 warnings.simplefilter('ignore')
 e.fit(pd.to_datetime(['2019-06-01T12:00:00Z']),np.array([600.]),np.array([100.]),np.array([45.]),np.array([270.]),np.array([45.]),np.array([270.]),np.array([.25]))
 F=e.vf_calculator.build_ts_vf_matrix(p).copy();e.run_full_mode()
gnd=[s for s in p.ts_ground.all_ts_surfaces if s.length[0]>1e-8]
idx=[s.index for s in gnd]
err=[float(s.get_param('qabs')[0]-.75*s.get_param('qinc')[0]) for s in gnd]
out={'difference_full_cover':{'u':list(u.coords),'v':list(v.coords),'returned_wkt':difference(u,v).wkt,'returned_length':difference(u,v).length,'expected_length':0.},'collinearity_is_not_normalized':{'unscaled':bool(are_2d_vecs_collinear(np.array([1.,0.]),np.array([1.,1e-6]))),'scaled100':bool(are_2d_vecs_collinear(np.array([100.,0.]),np.array([100.,1e-4])))},'custom_aoi_ground':{'active_ground_indices':idx,'max_G_minus_F':float(np.max(np.abs(p.ts_vf_aoi_matrix[idx,:,:]-F[idx,:,:]))),'qabs_minus_075qinc':err,'maximum_absorption_excess':max(err)}}
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--output-file',type=pathlib.Path,required=True)
args=parser.parse_args()
with args.output_file.open('x') as f: json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
