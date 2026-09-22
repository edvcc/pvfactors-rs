# LCB-01 — View Factor Compatibility Deviation Investigation

- Status: **LCB-01 — READY FOR OWNER DECISION**
- Date: 2026-09-22
- Repository: `edvcc/pvfactors-rs`
- Research branch: `research/vf-lcb01-compatibility`
- Base checkpoint: `d5bc38ebd6ba853c4cec530e4787d1ab6168203d`
- Frozen Reference: `pvlib/solarfactors` v1.6.1, `ecbfc863657e239817603a43898ae173c7ccad9c`
- Scope: Reference deviation investigation only; no production Rust VF implementation.

## Conclusion

LCB-01 is a confirmed Frozen Reference endpoint-orientation defect in the PV-ground Hottel path at the exact negative horizontal endpoint.

The observed failure is **not** a general `tilt > 90°` defect and is **not** caused by a real obstruction in the failing strings. In the designed scan, the bound failure appears only when the Reference reaches exact `rotation_vec = -180°` with at least two PV rows and enters the right-side `_vf_hottel_gnd_surf()` branch. The exact horizontal PV surface has equal endpoint y values; `TsLineCoords.highest_point` resolves the tie to `b1`, while the one-sided limit immediately below 180° resolves the higher endpoint to `b2`. The signed crossed/uncrossed grouping in `_vf_hottel_gnd_surf()` assumes the nondegenerate high/low orientation, so the numerator changes sign at the tie.

The first incorrect numerical result is therefore the **signed Hottel string-difference result after endpoint tie reversal**. The Geometry coordinates, stable surface identity, front/back identity, and approved Geometry Golden remain valid and must not be changed.

## Reference source evidence

The Frozen Reference uses two materially different primitives:

1. `_vf_surface_to_surface()` computes the Hottel string difference and applies `abs(...)`, making the geometric magnitude endpoint-orientation invariant.
2. `_vf_hottel_gnd_surf()` computes `(d1 + d2 - l1 - l2) / (2 * width)` without a magnitude operation and relies on `high_pt_pv`, `low_pt_pv`, `shadow_is_left`, and the obstruction-point branch to preserve the intended crossed/uncrossed orientation.

The failing case enters the second primitive.

## Exact endpoint discontinuity

For the canonical `N=3` case:

| Surface tilt | Rotation | PV b1.y | PV b2.y | high endpoint | PV→ground target VF | PV→sky VF | bound violations |
|---|---:|---:|---:|---|---:|---:|---:|
| `nextafter(180°, 0)` = `179.99999999999997°` | `-179.99999999999997°` | 0.9999999999999998 | 1.0000000000000002 | b2 | +0.20382042637679965 | ~4.99975e-5 | 0 |
| `180°` | `-180°` | 1.0 | 1.0 | b1 by tie rule | −0.20382042637679976 | 1.999950002499975 | 36 |

The physical geometry changes only by floating-point endpoint degeneracy; a sign flip and sky jump of approximately 2 are not a physical limit.

## Independent oracle for the named blocker pair

Named pair:

- receiver `ReferenceIndex = 3` (ground shadow 0)
- source `ReferenceIndex = 28` (row 0 front)

Using the exact binary floating-point coordinates emitted by the Frozen Geometry and 100-digit arithmetic:

`F_ground→pv = 0.2038204263767998815712607034283142448398871848600639686444912994513033510331848965536530463636382979`

The reciprocal PV-to-ground value is:

`F_pv→ground = 0.2038204263767998363140346529403541283845537638530083543871196631595168203537032258281470128079206528`

An independent 2-D diffuse numerical integration at Gauss order 128 gives approximately:

- PV→ground: `0.2038204263768001`
- ground→PV: `0.20382042637680012`

The high-precision analytic Hottel result and the numerical integral agree to floating-point precision and both reject the Reference negative value.

## Obstruction audit

For the exact canonical `-180°` case, the raw `_vf_hottel_gnd_surf()` audit recorded:

- raw calls: 28
- negative calls: 28
- negative calls with **zero** obstructed strings: 28
- negative calls with any obstruction: 0

Therefore the observed LCB-01 sign defect is not caused by the obstruction-point path-length replacement. The function is named/used as an obstructed Hottel path, but the failing strings themselves all remain direct.

## Domain scan

The primary scan covered 33 designed cases including:

- tilt: 0, 1e-10, 1, 45, 89.9, near-90 on both sides, 90, 100, 120, 150, 179, 179.9, 179.999999, near-180, 180;
- row counts: 1, 2, 3, 11;
- canonical and mirrored surface azimuths;
- front/back, PV-ground, ground-PV, PV-PV, edge/middle, and mirror behavior through the assembled matrix.

Observed Reference bound failures:

- `N=2, tilt=180°, surface_azimuth=270°`: 14 violations;
- `N=3, tilt=180°, surface_azimuth=270°`: 36 violations;
- `N=11, tilt=180°, surface_azimuth=270°`: 492 violations.

No bound failure was observed for the scanned `tilt > 90°` non-endpoint cases, the `N=1` exact-180 control, or the exact-180 mirrored `surface_azimuth=90°` controls.

The supported conclusion is therefore **exact negative-horizontal endpoint singularity**, not “all tilt > 90° is broken.”

## Candidate correction evidence

A research-only diagnostic replaced only the signed output of `_vf_hottel_gnd_surf()` by its geometric magnitude before matrix assembly and normal sky closure.

Results:

- `N=2` exact canonical 180°: 14 → 0 bound violations;
- `N=3`: 36 → 0;
- `N=11`: 492 → 0;
- exact mirrored controls remain unchanged;
- non-endpoint representative cases show no material change above 1e-12;
- candidate exact-180 matrix vs Frozen Reference at `nextafter(180°, 0)`: max absolute difference `3.774758283725532e-15`;
- candidate exact-180 matrix: min 0, max 1, closure error 0, reciprocity error 0 for the canonical N=3 candidate oracle.

This supports an orientation-invariant Hottel magnitude at the analytic primitive, but it is **not** evidence that an arbitrary post-processing `abs()` is correct.

## Why whole-matrix abs is rejected

Applying `abs()` to the already assembled Reference matrix is an explicit counterexample:

- row-0 front sum becomes `2.99990000499995`;
- its sky entry remains `1.999950002499975`;
- closure error becomes approximately `1.99990000499995`;
- eight active sky entries remain > 1.

Therefore the correction must be made at the finite-pair geometric primitive/visibility semantics before sky closure, not by taking absolute values of the final matrix.

## Unified mathematical contract candidate

The primary physical definition for active 2-D diffuse line surfaces is:

[
F_{i\to j}
=
\frac{1}{L_i}
\int_i \int_j
V(s,t)
\frac{
\max(0, n_i\cdot \hat r)
\max(0, -n_j\cdot \hat r)
}{
2r
}
\, dt\, ds
]

where `V(s,t)` is physical line-of-sight visibility. This definition is nonnegative by construction.

Hottel is an analytic optimization of the same measure. For a valid Hottel construction, straight or taut-around-obstruction path lengths form the two endpoint pairings and the geometric result is the orientation-invariant magnitude:

[
F_{i\to j}
=
\frac{
\left|\Sigma L_{crossed}-\Sigma L_{uncrossed}\right|
}{
2L_i
}
]

Endpoint reversal may swap which pairing is called crossed versus uncrossed; it must not change the physical sign.

Front/back identity and physical visibility remain separate semantic inputs. They must not be repaired by folding tilt, swapping sides, or changing approved Geometry.

## Answers to the required investigation questions

1. **First wrong branch/formula:** the signed return of `_vf_hottel_gnd_surf()` after exact-horizontal high/low tie reversal in the right-side branch.
2. **Only tilt=180?** Within the designed valid-domain scan, the failure is isolated to the exact negative-horizontal endpoint; no non-endpoint tilt failure was found.
3. **All tilt>90?** No. 100°, 120°, 150°, 179°, 179.9°, 179.999999° and the next representable float below 180° are valid in the scanned canonical case.
4. **Unobstructed Hottel:** no defect was found in `_vf_surface_to_surface()`; its magnitude form matches the analytic/numerical oracle for the blocker geometry.
5. **Ordering/high-low/visibility/sign?** Root cause is a combination of endpoint tie ordering plus a signed crossed/uncrossed return. Visibility obstruction is not causal in the observed negative calls.
6. **Global abs counterexample?** Yes for `abs(final_matrix)`; it violates closure and leaves sky > 1. No counterexample was found in the designed scan to the narrower candidate “take the geometric magnitude inside the Hottel primitive,” but this is a semantic formula decision, not permission to post-process matrices.
7. **Preserving front/back above 90°:** keep the existing semantic `SurfaceKey` side and normal; compute visibility from those semantics. Do not fold tilt or swap front/back. Endpoint labels used for Hottel are local analytic construction details only.
8. **Unified VF contract:** nonnegative visibility integral is normative; Hottel is an orientation-invariant analytic realization; reciprocity and closure are secondary invariants, not substitutes for entry bounds.

## New invariant requirement

For every active finite receiver/source pair:

`0 <= F_ij <= 1`

and, where applicable:

- reciprocity;
- closure;
- visibility;
- mirror invariance.

Mutation self-tests in the research harness explicitly catch:

- a negative but reciprocal matrix;
- a closure-passing matrix with an invalid entry;
- an entry greater than one.

All three mutation checks pass.

## Geometry impact

**None.**

No P3 Geometry coordinate, topology, `SurfaceKey`, `ReferenceIndex`, `ActiveIndex`, front/back identity, Golden payload, or geometry tolerance requires modification.

If implementation later appears to require a Geometry change, that is a new escalation and must not be folded into DEV-028.

## Environment note

The original blocker is already captured under the approved executable R0 evidence with environment ID `031158a1d1be8cdb9093`.

The new GitHub Actions research run uses the exact canonical requirements/runtime fields and reports `canonical_environment_match=true`, but its runtime fingerprint differs because the hosted Linux kernel/platform string differs. It is supplemental cross-host evidence, not a redefinition of R0 and not an attempt to change dependency or environment policy.

## Owner decisions requested

1. Accept or reject proposed **DEV-028** classification and corrected expectation.
2. Accept or reject proposed **CDR-008** VF magnitude/visibility contract.
3. Accept or reject `view-factor-lcb01-oracle-v0.1` as the corrected P4 oracle seed.
4. If accepted, authorize resumption of Full-Project Launch Closure from LCB-01; do not activate Full Implementation yet.
