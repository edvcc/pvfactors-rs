# CDR-008 — View Factor Non-negativity, Visibility and Hottel Orientation Policy

Status: **APPROVED**. Owner decision 2026-09-22, OD-LCB01-01..06; see [Owner record](LCB-01_OWNER_DECISIONS.en.md). DEV-028 covers the Full defect; DEV-029 independently covers Fast finite aggregation. This approved supplement governs VF/Fast geometric semantics without altering frozen P3/Geometry documents. Production numerical algorithms are not frozen.

Semantic side/outward normal and line-of-sight are authoritative; Hottel is an analytic realization. Adopt nonnegative finite physical exchange throughout the approved tilt domain. No global matrix abs, clamp, folding, side swap, Geometry adaptation to Reference or tolerance relaxation.

## Mathematical definition

For receiver segment i and source segment j, let p∈i, q∈j, r=q−p, Li>0 and actual unit normals ni,nj. Define V(p,q)=1 exactly when `ni·r>0`, `nj·(−r)>0`, and the open connecting segment meets no interior of another opaque PV row; otherwise V=0. Both front and back are named sides of the same opaque segment, not two obstacles. Ground has upward normal. Self, same-row, same-facing sides of the approved parallel-row geometry and ground-ground exchange are zero. Nearest-neighbor shortcuts require a geometric proof and do not define visibility.

```text
Eij = ∫i ∫j V(p,q) (ni·r)(−nj·r) / (2 |r|³) dsq dsp
Fij = Eij / Li
Eij = Eji; Fij >= 0
```

The kernel follows by integrating the 3D diffuse kernel along the invariant row direction: `∫ dz/(r²+z²)² = π/(2 r³)`. A receiving half-plane's entire angular measure is normalized to one, hence a finite visible source has F≤1. This is a physical definition, not a numerical clamp. The derivation assumes the approved infinite-along-axis, opaque, straight 2D rows; it introduces no new 3D model.

Only physically supported rays contribute. Positive Hottel magnitude for a wrong-facing or blocked surface does not create support. Actual normals retain front/back identity for >90°, including the downward front/upward back at180°. Tilt, `tilted_to_left`, `shadow_is_left`, high/low names and raw negative signs are not substitutes for normal/ray predicates.

## Unobstructed exchange

For fully mutually facing, wholly visible straight segments with endpoints a,b and c,d:

```text
Fij = abs(|a-d| + |b-c| - |a-c| - |b-d|) / (2 Li)
```

Here absolute value removes arbitrary endpoint parameter orientation after support has been established; it is not `abs(F_reference)`. Reversing either segment's endpoint enumeration does not change the result. If only part of the pair is supported, split the visible integration domain first. Do not take the magnitude of a cancellation across hidden and visible regions.

## Obstructed exchange and valid endpoint/string construction

For each receiver position p, determine source intervals whose rays satisfy both outward half-planes, then subtract intervals hidden by opaque row segments. Intersections of rays through blocker endpoints with the source line define interval endpoints. Visibility is decided by segment intersection, not by the sign of a string sum. A target interval need not be constant as p moves; one global clipped source segment is generally insufficient.

Partition the receiver at events where projected endpoint order/visibility changes: intersections with lines through source/blocker endpoint pairs, plus hemisphere boundaries. On each open cell, visible angular intervals are bounded by fixed vertices (source endpoints or silhouette endpoints). Their endpoint rays, rather than nominal “high/low”, determine the orientation of crossed strings. Multiple opaque rows are included; an optimization may prune only proven irrelevant rows.

For an interval bounded by unit rays uA,uB and tangent `R ni = (−ni_y, ni_x)`, the point-to-interval factor is:

```text
dFi(p) = 1/2 * abs((R ni) · (uB-uA))
```

This follows by integrating cos(theta)/2 over a visible angular interval inside the receiving hemisphere. It is nonnegative because of the supported angular order. Integrate this function over the receiver and divide by Li; this is the independent numerical route used in the candidate.

An exact endpoint-string route is also permitted. On a cell p(s)=p0+s*t with fixed boundary vertex v, `d|p-v|/ds = -t·u_v`. Therefore each angular-boundary term integrates to differences of distances from the **cell endpoints** to the **actual bounding vertices**. Assemble those string terms with the supported angular orientation, giving the nonnegative cell exchange; sum cells. A boundary at a receiving-horizon ray has a constant direction and a linear primitive. This is a derivation of valid obstructed strings, not blanket application of the four nominal endpoints to a partly hidden pair. Any shortcut/detour form must prove equality to this visible-domain measure, including its endpoint ordering and chosen obstruction endpoint.

Use Eij once and produce the reverse by `Fji=Eij/Lj`; independent reverse integration remains a verification check. Numerical quadrature or robust closed forms are implementation choices only if their accuracy is demonstrated against approved oracles. This investigation implements a research oracle, not a production algorithm or a performance choice.

## Degeneracy, exact structure and boundary source

- Keep Geometry activity, coordinate values, lengths, keys, indices and normals unchanged. Normalize a nonzero normal for cosine evaluation without changing its direction/identity. The candidate explicitly uses upward ground normal where raw serialization has null.
- Inactive/zero-length surfaces have zero rows/columns and no division. Do not reactivate a slot to manufacture a VF.
- Coplanar self/same-row/ground pairs contribute zero. Isolated tangencies and endpoint-only contacts have zero angular measure. Collinear grazing contributes zero; touching configurations must be handled as supported-measure limits, not a singular 0/0. Approved positive ground clearance avoids crossing ground; arbitrary intersecting topology is outside this contract.
- Topology, SurfaceKey, ReferenceIndex and visibility classification are not made “approximately equal” by acceptance epsilon. Robust/adaptive predicates may resolve arithmetic uncertainty, but may not enlarge visible domains. If approved Geometry itself cannot define a valid physical domain, stop for a new conflict; do not mutate it.
- Physical rows retain the existing `F_i,sky=1−sum(physical F_i,*)`; sky row stays zero and has no length reciprocity. With finite ground this is an open-boundary residual and includes escape outside the ground extent, even for downward receivers. This decision does not silently reinterpret it as only the astronomical upper hemisphere. Check nonnegativity and closure; do not clamp an invalid residual.

## Full/Fast compatibility and API

Full F uses the preceding definition. Approved Fast ground/PV/shaded/illuminated geometric groups use sums of those same finite exchanges; for a union of receiver segments, use length-weighted aggregation. Direct group computation is allowed if proved equivalent. This replaces the finite-inconsistent low-endpoint proxy and out-of-domain edge segments; it does not alter Fast's one-bounce approximation into a Full solve or close CDR-007 by implication.

Public Geometry APIs and identities do not change. F dimensions, receiver/source axes, inactive slots and residual boundary remain stable. Physical numerical results intentionally change in DEV-028 Full cases and DEV-029 finite Fast groups; preserve per-field deviations. AOI G is a separate operator and is not constrained to F's [0,1] rule by this CDR. No claim is made that all P4/P5/P6/P7 fixtures or public result-availability decisions are now approved.

## Approved seed and verification boundary

The existing 66-case/198-artifact corpus is **APPROVED_TARGETED_ORACLE_SEED** only: LCB-01 corrected geometric F plus finite Fast groups, not complete P4/VF Golden or AOI coverage. Its physical numeric payload is unchanged by approval. Raw/normalized Reference is retained; matrix provenance cites DEV-028/CDR-008, Fast provenance DEV-029/CDR-008. Exact object hashes are in LCB-01_OWNER_DECISIONS.json.

Comparator status: **APPROVED FOR LCB-01 TARGETED ORACLE SEED**; **NOT YET FINAL P4 CROSS-PLATFORM TOLERANCE**. Bounds epsilon1e-10, expected_abs2e-9, length-reciprocity1e-10 and closure1e-10 are unchanged targeted acceptance budgets. Geometry tolerance is unchanged. Final P4 tolerances need independent evidence and explicit approval; never relax them silently to pass an implementation.

Retain bounds, support, reciprocity, closure, high-precision analytic, independent line/angular integration, tensor convergence, obstruction, wrong-side/fully-blocked zero, mirror, endpoint reversal and independent reverse checks. Candidate verification must compare a fresh reconstruction and recompute Fast finite aggregation. Negative-but-reciprocal, closure-pass-invalid and >1 mutations remain required.

CDR-008 approval does not close CDR-007, equate Fast with Full, freeze a production numerical algorithm, complete P4–P7 or launch implementation. [Closure handoff](LCB-01_CLOSURE_HANDOFF.en.md) and its verification receipt determine whether LCB-01 is CLOSED; otherwise closure remains blocked.
