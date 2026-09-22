# DEV-028 — Exact Negative-Horizontal PV–Ground View Factor Endpoint-Orientation Defect

- Status: **PROPOSED / UNAPPROVED**
- Date: 2026-09-22
- Owner: Repository Owner
- Reference: `pvlib/solarfactors` v1.6.1, `ecbfc863657e239817603a43898ae173c7ccad9c`
- Related investigation: LCB-01
- Proposed decision record: CDR-008

## Classification

Confirmed Reference behavior defect / endpoint-orientation singularity.

This is not a Geometry defect and not a general `tilt > 90°` limitation.

## Trigger and observed domain

The confirmed trigger is the Frozen Reference state where:

- the PV surface becomes exactly horizontal at `rotation_vec = -180°`;
- the numerical PV surface endpoints have exactly equal y;
- `highest_point` resolves the tie to `b1`, reversing the one-sided endpoint ordering seen immediately below 180°;
- PV-ground evaluation enters the right-side `_vf_hottel_gnd_surf()` path;
- the signed crossed/uncrossed expression is returned without orientation-invariant magnitude normalization.

In the designed scan, bound failures were observed for `N=2/3/11` at the exact canonical 180° case and not for `N=1`, the mirrored +180° orientation, or non-endpoint >90° cases.

## Evidence

Named blocker pair:

- receiver ReferenceIndex 3;
- source ReferenceIndex 28;
- Frozen Reference: approximately `-0.2038204263767998`;
- independent 100-digit result:
  `+0.2038204263767998815712607034283142448398871848600639686444912994513033510331848965536530463636382979`.

The exact canonical audit found 28 negative raw Hottel calls; all 28 used four direct, unobstructed strings.

The candidate magnitude primitive eliminates the 14/36/492 bound failures for N=2/3/11 and matches the Frozen Reference one-sided limit at `nextafter(180°,0)` to a maximum absolute difference of approximately `3.8e-15`.

## Corrected expectation

V1 must not reproduce negative physical view factors from this Reference singularity.

For the analytic Hottel path, crossed/uncrossed endpoint pairing is an implementation construction; endpoint reversal may exchange pairing labels but must not change the physical magnitude. Physical side identity and visibility must be evaluated separately.

The corrected finite-pair expectation is nonnegative and must satisfy the CDR-008 contract. Sky is recomputed only after finite factors are valid.

## Forbidden compatibility shortcuts

Do not:

- fold tilt above 90°;
- swap front/back semantic identity;
- modify approved Geometry to force a preferred endpoint order;
- clamp invalid Reference entries;
- apply `abs()` to the final assembled matrix;
- refresh approved Geometry Golden or tolerance to hide the defect.

## Raw/corrected evidence policy

Frozen Reference outputs remain immutable raw evidence.

Corrected oracle material must be separately labeled as candidate/approved corrected expectation and must never overwrite the raw Reference capture.

## Approval effect if accepted

Acceptance of DEV-028 authorizes the Rust implementation and P4 oracle work to treat the negative exact--180° Reference VF as a named incompatibility defect rather than a compatibility target.

It does not approve P4, Full-Project Launch Closure, or Full Implementation by itself.
