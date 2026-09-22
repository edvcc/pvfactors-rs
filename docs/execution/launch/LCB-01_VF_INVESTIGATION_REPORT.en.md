**Historical research document.** Pre-approval status statements and old verification receipts below are superseded by [Owner decisions](LCB-01_OWNER_DECISIONS.en.md) and [current closure handoff](LCB-01_CLOSURE_HANDOFF.en.md). The66-case scientific results remain evidence. Current verification requires `--actual` fresh reconstruction; a candidate path alone returns NOT_READY.

# LCB-01 View Factor investigation

Date: 2026-09-22. **LCB-01 — READY FOR OWNER DECISION**. Research authorization only; no production implementation, approval, P4 acceptance or full-project launch.

Branch: `research/vf-lcb01-compatibility`. Base: `d5bc38ebd6ba853c4cec530e4787d1ab6168203d`. Frozen Reference: `ecbfc863657e239817603a43898ae173c7ccad9c`. P3 approved baseline remains `c2bc8572a976279abacbcd1d4f9c460233785bdb`. The final commit is the commit containing this report; verification receipts identify their tested checkpoint separately.

## Judgment and scope

The Full matrix defect is a **Reference implementation bug**: a signed obstruction formula relies on a strict high/low endpoint order that rounded horizontal subsegments do not satisfy. All 408 significantly negative PV-to-ground helper results in this scan have an exact endpoint-height tie. Reciprocal entries inherit the sign and residual sky inherits the excess. This does not require a Geometry change.

Across the seven named helper paths, the broader classification is **Mixed**: the preceding bug plus Fast finite-ground proxy/domain and numerical limitations. A Fast edge helper returns positive `0.5` for an upward-facing back at 180°; absolute value cannot fix it. Interior Fast proxies also differ from finite-ground exchange away from 180°. These are recorded separately, not conflated with negative Full entries or automatically declared approved corrections.

The default recommendation is [DEV-028](DEV-028_VIEW_FACTOR_ORIENTATION_CANDIDATE.en.md) and [CDR-008](CDR-008_VIEW_FACTOR_VISIBILITY_HOTTEL_POLICY.en.md): define geometric F from actual normals and unobstructed rays over the unchanged finite Geometry, using orientation-independent visible-domain integration. Approve the deviation and exact candidate objects before treating corrected values as acceptance expectations. Do not repair a matrix by clipping or taking its absolute value.

## First divergence, with a hand-checkable example

`VF053` is exactly Approved Geometry `TILT_180`: N=3, width=height=1 m, gcr=0.5, axis=180°, solar zenith=45°, solar/surface azimuth=270°, tilt=180°. All serialized surface records equal the approved payload, including indices, keys, coordinates and normals; see `geometry-equality.json`.

| Field | Ground receiver 3 | PV source 28 |
|---|---|---|
| SurfaceKey | kind=ground, source=shadow, ground_element=0, cut_interval=3, row/side/segment=null, illumination=shaded | kind=pvrow, source=pvrow, row=0, side=front, segment=0, ground_element/cut_interval=null, illumination=illuminated |
| Coordinates (m) | [−1.4999999999999996,0] → [−0.4999999999999998,0] | [−0.5,1] → [0.5,1] |
| Length (m) | 0.9999999999999998 | 1 |
| Normal | raw null; physical ground normal [0,1] | [1.1102230246251565e−16,−1] |

The branch sequence is:

1. `rotation=-180`, `tilted_to_left=false`. Ground cut point is `x=-8165619676597684`. The ground segment is **left of the physical row**, but **right of its extended-line cut point**. Those are different meanings of “right”. The approved coordinates/partition remain unchanged.
2. `vf_pvrow_surf_to_gnd_surf_obstruction_hottel` uses `is_left=false`; row 0 is not the right array edge, so it selects the obstruction helper and row 1's lowest full-row point `(1.5,0.9999999999999999)`.
3. Full row 0 has endpoints `(0.5,1)` and `(−0.5,0.9999999999999999)`. Its front subsegment has two y=1 endpoints after construction/rounding. Approved tie semantics give `high=(-0.5,1)`, `low=(0.5,1)`. This differs from the strictly descending high/low orientation assumed by the signed string branch. Geometry's tie rule itself is not changed.
4. `_hottel_string_length` uses direct lengths for all four rays here: the selected neighboring row is physically to their right, so none crosses it. The first wrong sign arises when `_vf_hottel_gnd_surf` assigns crossed/uncrossed roles from `shadow_is_left=false` and these high/low labels (vfmethods.py lines 523–536), not in the distances or final reciprocal assignment.

| String | Endpoint pair | Frozen value |
|---|---|---:|
| l1 | high → ground right | 1.0 |
| l2 | low → ground left | 2.2360679774997894 |
| d1 | high → ground left | 1.4142135623730947 |
| d2 | low → ground right | 1.414213562373095 |

`(d1+d2-l1-l2)/(2*1) = -0.20382042637679976`. The front/right filter retains it. Reciprocity divides by the ground length, producing `F[3,28] = -0.2038204263767998`. The points face each other and every joining ray is unobstructed; physical exchange is positive.

Independent Decimal90, using the exact binary64 coordinates, gives:

```text
0.203820426376799881571260703428314244839887184860063968644491299451303351033184896553653049
```

Decimal110 agrees beyond 88 decimal places. Independent visible-angle/line integration gives `0.20382042637679987`. A separate direct double-line cosine quadrature converges as follows:

| Gauss order on each segment | F[3,28] |
|---:|---:|
| 2 | 0.20526498482540437 |
| 4 | 0.20381945497162346 |
| 8 | 0.2038204263816811 |
| 16 | 0.20382042637679984 |
| 32 | 0.20382042637679987 |
| 64 | 0.2038204263767998 |
| 128 | 0.20382042637680015 |

See [minimal-counterexample.json](../../../evidence/execution/launch-closure/lcb-01/minimal-counterexample.json); it preserves every value above, the geometry, Reference intermediates and independent outputs.

## Domain and taxonomy

66 cases form a bounded covering set: all requested tilt points, both axis±90° azimuths with mirrored sun, N=1/2/3/11, cut=1/2 and additional cut=4 near 180°. Width/height=1, gcr=0.5, ground=[−100,100]. This is not an exhaustive search over height, scale, pitch, shading states, clearance or all continuous inputs. The trigger is the endpoint-order condition, not an asserted universal angular threshold.

| Case | Tilt | Azimuth | N | Cut | Differing Full entries | Bounds failures |
|---|---:|---:|---:|---:|---:|---:|
| VF052 | 180 | 270 | 2 | 2 | 27 | 25 |
| VF053 | 180 | 270 | 3 | 1 | 37 | 36 |
| VF054 | 180 | 270 | 3 | 2 | 67 | 66 |
| VF055 | 180 | 270 | 11 | 1 | 493 | 492 |
| VF062 | 179.99999999999997 | 90 | 3 | 4 | 67 | 63 |
| VF063 | 179.99999999999997 | 270 | 3 | 4 | 37 | 30 |
| VF064 | 180 | 90 | 3 | 4 | 67 | 63 |
| VF065 | 180 | 270 | 3 | 4 | 127 | 126 |

8/66 cases contain 922 Full mismatches: 408 PV→ground, 408 ground→PV, 70 ground→residual-sky and 36 PV→residual-sky. No significant PV→PV mismatch was found. The other 58 cases agree within the candidate comparator; that is sampled evidence, not a proof that every >90° configuration is correct. In particular, the exact-180/azimuth90/cut1 cases pass while cut4 fails. At `180−1 ULP`, cut1 passes while cut4 fails in both orientations. An angle-only patch is insufficient.

`anomaly-taxonomy.json` gives each anomalous directed entry's receiver/source keys, side, row, ground element, helper path, cut-point side, raw and candidate values. “obstruction_helper” labels a Reference branch, not proof of physical obstruction. The taxonomy independently marks all 816 anomalous physical pairs UNOBSTRUCTED, with the 106 residual entries not applicable; convex-hull interior intersection classifies positive-measure blockers for these mutually facing pairs. Physical ground left/right/overlap is recorded separately from cut-point side. Physical support is determined separately by ray intersections; `independent-crosschecks.json` includes 30 pairs where occlusion reduces the bare string magnitude. Shaded/illuminated, edge/middle ground and both sides occur in the inventory. Candidate matrices include every active pair, all inactive zero slots and the boundary row.

## Review of all requested functions

| Function | Finding |
|---|---|
| vf_pvrow_surf_to_gnd_surf_obstruction_hottel | Branches by cut-point side/array edge; retains the negative intermediate and propagates reciprocity. Its side mask is not itself the first divergence in VF053. |
| _vf_hottel_gnd_surf | Signed endpoint assignment fails at rounded high/low ties; all 408 negative helper observations meet this trigger. |
| _hottel_string_length | Individual Euclidean/detour lengths are nonnegative. The selected low obstruction point is unnecessary for VF053 and introduces no detour there. Full ordered-row assumptions must be proved before reusing this angle test. |
| _vf_surface_to_surface | A nonnegative magnitude, not a side/visibility oracle. It agrees for mutually facing, unobstructed tested segments. Reversing a normal or inserting a blocker makes the same bare magnitude wrong. |
| vf_pvrow_to_pvrow | Uses nearest-neighbor and side masks. No significant mismatch in this scan, including >90°. Candidate semantics nevertheless require actual normals; no identity exchange. |
| calculate_vf_to_gnd | Distinct Fast issue: at VF053 row0, a one-sided `min` makes the supposed left-ground segment run from −100 to approximately −8.17e15, outside the finite extent and in reverse order. Cancellation yields 0.5 for the upward back. Interior low-endpoint proxy also represents more than finite ground. |
| calculate_vf_to_pvrow | No significant aggregate back→PV mismatch in the scan. Its back-side/nearest-neighbor choice and constructed shaded endpoints remain assumptions requiring future Fast coverage; this investigation does not certify all Fast source terms. |

Fast ground group comparisons differ in 139 fields across 53 cases. Many are finite-extent proxy differences even at 0°/45°/120°, distinct from the Full sign bug. The 180° edge error and a near-180° positive cancellation artifact demonstrate that “take abs” does not repair all paths. [fast-helper-comparison.json](../../../evidence/execution/launch-closure/lcb-01/fast-helper-comparison.json) separates these results. Recommendation: finite-F aggregation for Fast geometric groups, subject to explicit Owner compatibility approval; this does not change Fast into Full radiosity.

## Independent evidence and limits

The independent oracle imports no pvfactors VF helper. It derives the infinite-row 2D kernel from the 3D diffuse cosine integral and explicitly intersects rays with opaque row segments. Inner angular integration and outer SciPy quadrature are different from four-endpoint Hottel. The underlying physical cosine integral and obstruction requirement are supported by [COMSOL's radiation derivation](https://www.comsol.com/blogs/introduction-to-computing-radiative-heat-exchange); the 2D reduction, visibility-cell formulation and this implementation are independently derived here. [NASA's view-factor report](https://ntrs.nasa.gov/api/citations/19950020924/downloads/19950020924.pdf) provides additional method context. Neither is used as an approval or an unexamined numerical fixture.

An analytically decomposable obstruction case uses two length-2 parallel segments at y=0 and y=2, divided by an opaque vertical segment x=1. Only left-left and right-right halves exchange. Decimal100 length-weighted Hottel gives `sqrt(5)-2 = 0.236067977499789696409…`; visible-angle integration at requested errors 1e−5, 1e−8 and 1e−12 gives `0.2360679774997897`. Bare unoccluded magnitude is `sqrt(2)-1 = 0.414213562373095…`. With a wrong-facing receiver or a complete intermediate blocker, the physical value is zero while bare magnitude remains positive. This synthetic oracle validation is explicitly separate from approved Geometry cases.

All 66 full matrices were independently integrated at 1e−7 and 1e−11 requested error; both executions returned the same binary64 results here (smooth event-split integrands), with maximum estimated quadrature error below 9.92e−15. These are numerical estimates, not certified intervals. The direct tensor refinement above supplies a nontrivial convergence sequence. 138 representative pairs were also independently integrated in reverse and after reflecting the entire physical domain or reversing endpoint order; max exchange reciprocity error is 2.91e−15 and max endpoint-order error 7.78e−16. Mirror checks reflect finite ground too; opposite-azimuth arrays in the fixed asymmetric-about-array extent are not incorrectly asserted to be exact full-domain mirrors.

Candidate matrix reciprocity is generated by exchange symmetry and sky closure by residual, so their PASS is not independent proof. Bounds, support checks, analytic cases, reverse integrations and mutation tests provide the additional evidence. The 107 matching bare-Hottel magnitude examples are descriptive and selected after comparison; they are not counted as 107 independent acceptance tests.

Global abs judgment: **NO as a general repair**. `abs(matrix)` leaves sky near 2 and breaks closure; Fast's positive 0.5 remains wrong; unsigned Hottel alone cannot identify a visible side. The narrower patch `abs(obstruction-helper)` with the existing mask and recomputed residual happens to match all 66 sampled Full matrices, but is **NOT PROVEN** across the approved domain. These statements are deliberately distinguished.

## Candidate, verification and next gate

- `reference/candidate/vf-lcb01-v0.1/manifest.json`: 66 cases, 198 raw/normalized/corrected artifacts; lossless sparse raw F omits only exact zeros. Infinity appears only as an explicit string in raw cut-point diagnostics. Matrix axes remain receiver/source ReferenceIndex plus last sky.
- `comparator-policy.json`: PROPOSED/UNAPPROVED bounds epsilon 1e−10, expected absolute comparison 2e−9, closure and length-reciprocity allowance 1e−10. Budgets derive from requested quadrature accuracy; they are not fitted to Reference's large errors or approved as a universal platform bound. Geometry tolerance remains frozen.
- `candidate-index.json` pins the exact candidate manifest hash. Every changed field above the research comparator has Reference/corrected values and DEV/CDR/oracle provenance; all matrix fields also identify their independent generator. Fast group proposals are separate fields.
- 66 raw cases were recaptured byte-identically in R0 `031158a1d1be8cdb9093`. Incremental metadata had a narrower warning inventory; the complete rerun metadata is canonical and the earlier receipt is retained. No warning was represented as a production pass.
- `python scripts/verify_vf_candidate.py reference/candidate/vf-lcb01-v0.1` checks candidate hashes, inventory, exact Geometry preservation and invariants. Its PASS is research-only and explicitly reports P4 NOT_READY. `python -m unittest discover -s scripts/tests -v` includes the four required mutation classes and additional invalid/support/zero-matrix checks.
- Current verification receipts and evidence hashes are under `evidence/execution/launch-closure/lcb-01/`. Canonical `verify_project.py assets` continues to verify the original 491 frozen files/G2. Launch preflight remains NOT_READY pending Owner approval and the remaining launch package.

Review the DEV, CDR, comparator and exact manifest together. Owner may approve the unified visibility policy and candidate scope, request revisions, or retain raw Reference compatibility only as a named diagnostic mode outside corrected physical F. Default recommendation is the unified corrected policy, including finite Fast group geometry. Reject domain narrowing, identity swaps or tolerance relaxation. Approval of this investigation does not approve all P4–P7 fixtures or authorize implementation.

This task stops here as instructed. LCB-01 remains open for launch until Owner closes it; full-project closure remains BLOCKED. No master/develop/P3 branch, frozen source, approved Geometry, P3 design, Geometry tolerance or production Rust source was changed. No remote push, PR, merge, tag or release is part of this investigation.
