"""Independent stdlib/Decimal launch evidence; no production physics API.

90-digit Taylor trig and exact rational interval checks are separate from R0.
Inputs are exact binary floats lifted into Decimal. Angles are bounded before
conversion. Error propagation explicitly assumes <=2 ulp library trig error;
experiments test this assumption on sampled platforms, not every possible libm.
"""
from __future__ import annotations

import argparse
from decimal import Decimal as D, localcontext
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
PI = D('3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679')
EPS = sys.float_info.epsilon
DELTA = 64 * EPS


def trig(deg, cosine=False):
    with localcontext() as c:
        c.prec = 90
        x = D.from_float(float(deg)) * PI / D(180)
        x = (x + PI) % (2 * PI) - PI
        term = D(1) if cosine else x
        total = term
        n = 0
        while True:
            n += 1
            a = 2 * n - (1 if cosine else 0)
            term *= -x * x / (a * (a + 1))
            total += term
            if abs(term) < D('1e-85'):
                return +total


def hp_mu(beta, zenith, difference):
    with localcontext() as c:
        c.prec = 80
        return +(trig(beta, True) * trig(zenith, True) +
                 trig(beta) * trig(zenith) * trig(difference, True))


def classify(value, delta):
    return 'front' if value > delta else 'back' if value < -delta else 'grazing'


def grazing_rows():
    inputs = []
    for beta in [0., .125, 1., 5., 15., 30., 45., 60., 75., 89., 90.]:
        z = 90 - beta
        for dz in [math.nextafter(z, -math.inf), z, math.nextafter(z, math.inf)]:
            if 0 <= dz <= 180:
                inputs += [(beta, dz, 180.), (180-beta, dz, 0.)]
    for beta, z, a in itertools.product([0., 1e-12, 45., 90., 120., 179.999999999, 180.],
                                       [0., .01, 45., 89.999999999, 90., 120., 180.],
                                       [0., math.nextafter(90.,0.), 90., math.nextafter(90.,180.), 180., 270., 360.]):
        inputs.append((beta,z,a))
    return list(dict.fromkeys(inputs))


def grazing(rust=True):
    inputs = grazing_rows()
    rust_values = None
    compiler = None
    if rust:
        with tempfile.TemporaryDirectory(prefix='grazing-probe-') as tmp:
            binary = Path(tmp) / ('probe.exe' if sys.platform == 'win32' else 'probe')
            subprocess.run(['rustc', '--edition=2024', '-O', str(ROOT/'reference/launch-closure/probes/grazing.rs'),
                            '-o', str(binary)], check=True, capture_output=True)
            run = subprocess.run([str(binary)], input='\n'.join(','.join(repr(x) for x in row) for row in inputs),
                                 text=True, capture_output=True, check=True)
            rust_values = [float(x) for x in run.stdout.splitlines()]
            compiler = subprocess.check_output(['rustc','--version'], text=True).strip()
    rows=[]
    for i,(b,z,a) in enumerate(inputs):
        value = rust_values[i] if rust_values is not None else (
            math.cos(math.radians(b))*math.cos(math.radians(z)) +
            math.sin(math.radians(b))*math.sin(math.radians(z))*math.cos(math.radians(a)))
        ref=hp_mu(b,z,a)
        error=float(abs(D.from_float(value)-ref))
        rows.append({'angles_degree':[b,z,a],'high_precision_reference':str(ref), 'f64_mu':value,
                     'absolute_error':error,'no_band':classify(value,0.),'band':classify(value,DELTA),
                     'normal_reversal_from_same_mu':classify(-value,DELTA),'error_bound':DELTA})
    special=[{'mu':x,'no_band':classify(x,0),'band':classify(x,DELTA)} for x in
             [0.,math.nextafter(0.,math.inf), math.nextafter(0.,-math.inf),-1.,math.nextafter(-1.,0.),
              math.nextafter(1.,0.),1.,-DELTA,DELTA,math.nextafter(-DELTA,-math.inf),math.nextafter(DELTA,math.inf)]]
    # Unit roundoff u=eps/2. Five trig evaluations; degree conversion uses at
    # most three roundings. Sum of angle magnitudes <=6*pi for this dot formula.
    u=EPS/2
    bound=(18*math.pi+24)*u/(1-32*u)
    assert bound < DELTA
    maximum=max(r['absolute_error'] for r in rows)
    assert maximum <= bound
    return {'status':'PASS','platform':platform.platform(),'machine':platform.machine(),'compiler':compiler,
            'engine':'Rust f64' if rust else 'CPython math f64','python':sys.version,'precision_digits':80,
            'classifier':'single signed mu, clamp [-1,1], front if mu>delta, back if mu<-delta, else grazing',
            'recommended_delta':DELTA,'delta_eps':64,'derived_conditional_bound':bound,
            'bound_assumption':'bounded normalized degree inputs; <=2 ulp sin/cos; ordinary non-fast-math operations',
            'maximum_sample_error':maximum,'tests_run':len(rows)+len(special),'rows':rows,'classifier_specials':special,
            'scientific_limit':'Finite sampled libm validation; not a universal correctly-rounded transcendental proof.'}


def remainder(a,b):
    lo,hi=map(Fraction,a);x,y=map(Fraction,b)
    if lo==hi:return []
    if x==y or min(hi,y)<=max(lo,x):return [[lo,hi]]
    return [[p,q] for p,q in [(lo,min(x,hi)),(max(y,lo),hi)] if q>p]


def interval_evidence():
    points=list(map(Fraction,[-1,0,.5,1,2,3]))
    intervals=[list(v) for v in itertools.combinations_with_replacement(points,2)]
    rows=[]
    for a,b in itertools.product(intervals,repeat=2):
        r=remainder(a,b)
        overlap=max(Fraction(0),min(a[1],b[1])-max(a[0],b[0]))
        assert sum(q-p for p,q in r)==a[1]-a[0]-overlap
        assert all(a[0]<=p<q<=a[1] for p,q in r)
        assert len(r)<=2
        if len(r)==2:assert r[0][1]<=r[1][0]
        rows.append({'minuend':list(map(float,a)),'subtrahend':list(map(float,b)),
                     'expected':[[float(p),float(q)] for p,q in r]})
    return {'status':'PASS','tests_run':len(rows),'oracle':'exact Fraction length conservation and ordered positive residual spans',
            'endpoint_rule':'Closed representations; no strict-set difference or shading-area inference from shared endpoints', 'cases':rows}


def horizon_geometry(rotation,row,n,side,position=.5,width=1.,height=1.,pitch=2.,band=15.):
    # Independent vector construction from centered equal rows; no R0 code copy.
    r=math.radians(rotation)
    v=(math.cos(r),math.sin(r))
    nx=-v[1] * (1 if side=='front' else -1)
    center=(row*pitch+(position-.5)*width*v[0],height+(position-.5)*width*v[1])
    if rotation in (0.,180.,-180.):return {'neighbor':None,'angle_degree':0.,'fraction':0.,'centroid':center,'top':None}
    neighbor=row+(1 if nx>0 else -1)
    if not 0<=neighbor<n:return {'neighbor':None,'angle_degree':0.,'fraction':0.,'centroid':center,'top':None}
    ends=[(neighbor*pitch+s*width*v[0]/2,height+s*width*v[1]/2) for s in (-1,1)]
    top=max(ends,key=lambda p:p[1])
    theta=max(0.,math.degrees(math.atan2(top[1]-center[1],abs(top[0]-center[0]))))
    return {'neighbor':neighbor,'angle_degree':theta,'fraction':min(1.,theta/band),'centroid':center,'top':top}


def horizon_evidence():
    rows=[]
    for tilt,row,side,pos,band in itertools.product([0.,45.,90.,120.,180.],range(3),['front','back'],[.1,.5,.9],[5.,15.]):
        observed=horizon_geometry(-tilt,row,3,side,pos,band=band)
        mirror=horizon_geometry(tilt,2-row,3,side,1-pos,band=band)
        assert abs(observed['fraction']-mirror['fraction'])<1e-12
        assert 0<=observed['fraction']<=1
        rows.append({'tilt':tilt,'row':row,'side':side,'position':pos,'band_degree':band,
                     'corrected':observed,'mirror':mirror,'front_omission_multiplier':1.,
                     'low_high_sun':'Shading multiplier independent of sun zenith; horizon amplitude depends on Perez inputs'})
    limits=[]
    for band in [5.,15.]:
        for fraction in [0.,.25,.5,1.,2.]:
            theta=band*fraction
            recovered=math.degrees(math.atan2(2*math.tan(math.radians(theta)),2))
            h=min(1.,max(0.,recovered)/band)
            assert abs(h-min(1.,fraction))<1e-14
            limits.append({'band_degree':band,'constructed_angle':theta,'expected_fraction':min(1.,fraction),'actual':h})
    return {'status':'PASS','tests_run':len(rows)+len(limits),'model_revision':'HybridPerezTwoSidedExplicitBand-v1-candidate',
            'band_default':None,'band_contract':'explicit finite elevation band in (0,90] degrees; no scientifically claimed 6.5-degree default',
            'formula':'h=min(1,max(0,atan2(y_top-y_centroid,abs(dx)) in degrees)/band); H=abs(P_horizon)*(1-h)',
            'limitation':'Uniform angular-band software approximation; geometry tests do not calibrate sky radiance or prove empirical accuracy.',
            'cases':rows,'limits':limits}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--python-only',action='store_true');a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=True)
    for name,data in [('grazing',grazing(not a.python_only)),('interval',interval_evidence()),('horizon',horizon_evidence())]:
        (a.output/f'{name}.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
        print(name,data['status'],data['tests_run'])
