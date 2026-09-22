# CDR-008 — View Factor Geometric Magnitude, Visibility, and Degenerate Endpoint Policy

- Status: **PROPOSED / UNAPPROVED**
- Date: 2026-09-22
- Owner: Repository Owner
- Related deviation: DEV-028
- Related investigation: LCB-01

## Decision candidate

The V1 View Factor contract separates three concerns:

1. semantic surface side and outward normal;
2. physical visibility/occlusion;
3. analytic evaluation of the nonnegative geometric measure.

Endpoint ordering used by a Hottel implementation is not surface identity and may not determine the sign of a physical View Factor.

## Normative physical definition

For active 2-D diffuse line surfaces:

[
F_{i\to j}
=
\frac{1}{L_i}
\int_i \int_j
V(s,t)
\frac{
\max(0,n_i\cdot\hat r)
\max(0,-n_j\cdot\hat r)
}{
2r
}
\,dt\,ds
]

The mathematical View Factor therefore satisfies `F_ij >= 0`. For the supported enclosure geometry, active pair factors must also satisfy `F_ij <= 1`.

## Hottel analytic realization

When the Hottel crossed-string construction is applicable:

[
F_{i\to j}
=
\frac{
\left|\Sigma L_{crossed}-\Sigma L_{uncrossed}\right|
}{
2L_i
}
]

For blocked configurations, the relevant path lengths may be taut paths around the blocking boundary according to the chosen visibility construction. Reversing an endpoint orientation may exchange the two pairing labels but may not change the physical magnitude.

The Rust implementation may use a different, clearer internal construction than the Frozen Reference. It must preserve the mathematical result and validated compatibility behavior, not the Reference's high/low endpoint artifact.

## Semantic side policy

- `SurfaceKey::PvRow.side` remains authoritative front/back identity.
- `tilt > 90°` is not folded.
- Front/back are not swapped at 90° or 180°.
- Visibility is derived from semantic side/normal and occlusion geometry, not from whichever endpoint is numerically “highest.”
- Exact horizontal or equal-y endpoint cases are ordinary degenerate analytic cases, not permission to change surface identity.

## Matrix assembly policy

1. Evaluate finite active-pair View Factors.
2. Check pair bounds and visibility invariants.
3. Check reciprocity where applicable.
4. Only after finite factors are valid, derive sky/enclosure remainder by closure.
5. If finite factors make closure physically impossible beyond the comparison policy, report an invariant/algorithm failure. Do not hide it by clamping or by a compensating sky value.

A full-matrix `abs()` operation is explicitly forbidden.

## Invariants

Required checks include:

- active entry bound: `0 <= F_ij <= 1`;
- reciprocity: `L_i F_ij ≈ L_j F_ji`;
- closure for the completed enclosure;
- visibility consistency;
- mirror/metamorphic consistency where defined.

Entry bounds are primary. Reciprocity and closure may pass for a physically invalid signed matrix and therefore are not sufficient by themselves.

## LCB-01 acceptance evidence

The proposed analytic magnitude treatment:

- removes all observed exact--180° bound failures for N=2/3/11;
- preserves the mirrored exact-180 controls;
- does not materially alter scanned non-endpoint cases;
- matches the one-sided Frozen Reference limit within approximately `3.8e-15`;
- restores the N=3 candidate oracle to min 0, max 1, exact closure, and exact reciprocity at double precision.

The named blocker pair independently matches 100-digit Hottel and numerical integration.

## Geometry boundary

CDR-008 requires **no change** to the approved P3 Geometry baseline.

If a future implementation needs a Geometry change to satisfy this contract, that is a new decision/blocker and must be escalated.

## Verification consequences if accepted

P4 must add:

- entry-bound checks before closure acceptance;
- negative-but-reciprocal mutation;
- closure-pass/invalid-entry mutation;
- `F > 1` mutation;
- exact -180° and one-sided-limit cases;
- mirrored +180° controls;
- genuinely obstructed cases validating the same magnitude/visibility separation;
- cross-language/tolerance comparison against approved corrected oracles.

## Non-decisions

This CDR does not approve:

- a specific Rust data structure;
- a final P4 numerical tolerance profile;
- a production implementation;
- Full-Project Launch Closure;
- activation of the full autonomous implementation task.
