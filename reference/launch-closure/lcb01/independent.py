"""Independent research oracle, NOT a runtime implementation or approved oracle.

Derivation: integrate the diffuse 3-D cosine kernel along the invariant row
axis to get (ni.r)*(-nj.r)/(2*|r|**3). At a fixed receiver point, integrate
cos(theta)/2 over visible source angular intervals; use adaptive numerical
quadrature along the receiver. No pvfactors imports or Hottel helpers.
Endpoint-string Decimal calculation is a separate analytic cross-check.
"""
from decimal import Decimal, localcontext
from itertools import combinations
import math

from scipy.integrate import quad


def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def at(a,d,t): return (a[0]+d[0]*t,a[1]+d[1]*t)
def norm(v): return math.hypot(*v)
def unit(v):
    l=norm(v)
    return (v[0]/l,v[1]/l)


def intersection_parameter(a,d,b,e):
    den=cross(d,e)
    return None if den==0 else cross(sub(b,a),e)/den


def blocked(p,q,blockers):
    v=sub(q,p)
    for a,b in blockers:
        d=sub(b,a); den=cross(v,d)
        if den==0:
            continue  # collinear grazing has zero angular measure
        ap=sub(a,p); t=cross(ap,d)/den; s=cross(ap,v)/den
        if 0<t<1 and 0<s<1:
            return True
    return False


def visible_intervals(p,source,ni,nj,blockers):
    a,b=source; d=sub(b,a)
    # A planar source's outward hemisphere contains p or contains no p.
    if dot(nj,sub(p,a))<=0:
        return []
    ts=[0.,1.]
    den=dot(ni,d)
    if den!=0:
        t=-dot(ni,sub(a,p))/den
        if 0<t<1: ts.append(t)
    for blocker in blockers:
        for endpoint in blocker:
            t=intersection_parameter(a,d,p,sub(endpoint,p))
            if t is not None and 0<t<1: ts.append(t)
    ts=sorted(set(ts)); result=[]
    for lo,hi in zip(ts,ts[1:]):
        q=at(a,d,(lo+hi)/2)
        if dot(ni,sub(q,p))>0 and not blocked(p,q,blockers):
            result.append((at(a,d,lo),at(a,d,hi)))
    return result


def point_factor(p,source,ni,nj,blockers):
    tangent=(-ni[1],ni[0]); total=0.
    for a,b in visible_intervals(p,source,ni,nj,blockers):
        ua=unit(sub(a,p)); ub=unit(sub(b,p))
        total+=abs(dot(tangent,sub(ub,ua)))/2
    return total


def line_factor(receiver,source,ni,nj,blockers=(),eps=1e-11):
    """Return F, quadrature error estimate, evaluation count; no clamping."""
    a,b=receiver; d=sub(b,a); ni=unit(ni); nj=unit(nj)
    if norm(d)==0 or norm(sub(source[1],source[0]))==0:
        return 0.,0.,0
    if max(dot(nj,sub(p,source[0])) for p in receiver)<=0:
        return 0.,0.,0
    if max(dot(ni,sub(q,p)) for p in receiver for q in source)<=0:
        return 0.,0.,0
    # Visibility changes only on rays through endpoint pairs. Split receiver
    # at those events; ordinary quadrature cannot silently miss narrow support.
    vertices=[*source,*[p for seg in blockers for p in seg]]
    cuts={0.,1.}
    for p,q in combinations(vertices,2):
        t=intersection_parameter(a,d,p,sub(q,p))
        if t is not None and 0<t<1: cuts.add(t)
    for q in source:
        den=dot(ni,d)
        if den!=0:
            t=dot(ni,sub(q,a))/den
            if 0<t<1: cuts.add(t)
    # Coalesce numerically indistinguishable quadrature breakpoints without
    # deleting any integration domain. This changes quadrature partitioning,
    # never the visibility predicate or the supplied Geometry coordinates.
    merged=[0.]
    for t in sorted(cuts):
        if t-merged[-1]>64*math.ulp(1.) and 1.-t>64*math.ulp(1.): merged.append(t)
    cuts=[*merged,1.]; value=0.; error=0.; neval=0
    for lo,hi in zip(cuts,cuts[1:]):
        out=quad(lambda t: point_factor(at(a,d,t),source,ni,nj,blockers),lo,hi,
                 epsabs=eps*(hi-lo),epsrel=eps,limit=200,full_output=1)
        if len(out)!=3:
            raise ArithmeticError(out[3])
        value+=out[0];error+=out[1];neval+=out[2]['neval']
    return value,error,neval


def decimal_hottel(receiver,source,precision=90):
    """Exact binary64 inputs, Decimal sqrt; valid only after visibility proof."""
    with localcontext() as ctx:
        ctx.prec=precision
        def distance(a,b):
            return sum((Decimal.from_float(float(x))-Decimal.from_float(float(y)))**2
                       for x,y in zip(a,b)).sqrt()
        a,b=receiver;c,d=source
        return str(abs(distance(a,d)+distance(b,c)-distance(a,c)-distance(b,d))/(2*distance(a,b)))


def normal(surface):
    return (0.,1.) if surface['logical_key']['kind']=='ground' else unit(surface['normal'][0])


def pair(data,i,j,eps=1e-11):
    si,sj=data['surfaces'][i],data['surfaces'][j]
    ki,kj=si['logical_key'],sj['logical_key']
    if not si['active'][0] or not sj['active'][0] or i==j:
        return 0.,0.,0
    if ki['kind']==kj['kind']=='ground' or (ki['kind']==kj['kind']=='pvrow' and ki['row']==kj['row']):
        return 0.,0.,0
    blockers=[row for r,row in enumerate(data['opaque_rows']) if r not in (ki['row'],kj['row'])]
    try:
        return line_factor(si['coordinates_m'][0],sj['coordinates_m'][0],normal(si),normal(sj),blockers,eps)
    except ArithmeticError as error:
        raise ArithmeticError(f'pair {i},{j}: {error}') from error
