# CDR-003 — Geometry Input and Domain Boundary Policy

- Status: **Recommended for Approval**
- Date: 2026-09-21
- Scope: P2 / G2 Geometry only
- Reference: `pvlib/solarfactors` v1.6.1, `ecbfc863657e239817603a43898ae173c7ccad9c`
- Related deviations: DEV-002, DEV-004, DEV-026

## Recommended decision

V1 uses a finite, closed `GroundExtent { min_x, max_x }` in metres. Both values
must be finite and `min_x < max_x`. The reference-compatible default is
`[-100, 100]`; it is a numerical convention, not a physical statement. Every
row endpoint must lie inside or on the extent after applying the position
predicate. Projected ground shadows and ground partitions are clipped to the
extent. A row outside the extent is rejected rather than clipped. Exact
infinite ground is deferred to a separately versioned model.

Every row must remain strictly above `y=0`. The minimum clearance must be
greater than `1e-10 m`; touching and crossing ground are invalid. Validation is
performed before projection or partition construction and returns
`GEOMETRY_CLEARANCE`, never a recoverable-input panic.

Axis and surface azimuth inputs must be finite. They are normalized with
Euclidean modulo into `[0, 360)`. For nonzero tilt, surface azimuth must be
`axis ± 90° (mod 360)` within the angle comparison tolerance. At exactly zero
tilt, surface azimuth does not select a different physical plane and the
relationship check is waived, while the normalized value remains recorded.

V1 accepts tilt in the closed interval `[0°, 90°]`. Exact `0°`, signed-zero
reference behavior, positive and negative near-flat rotations, exact `90°`, and
near-`90°` are distinct fixtures. Tilt above `90°` is rejected as
`GEOMETRY_TILT_UNSUPPORTED`; it is not silently folded or treated as covered by
the current tests.

Solar zenith is accepted in `[0°, 90°]` for the Geometry Gate. At exactly
`90°`, the state is `horizon_no_direct_projection`: row geometry remains
defined, direct ground projection is not represented by a huge finite shadow,
direct-shadow surfaces are inactive, and the finite ground is illuminated for
the direct-projection layer. Zenith above `90°` is outside this contract.
Parallel non-coincident and coincident projection are distinct typed outcomes.
Exact flatness means rotation equals zero; near-flat values are not coerced to
zero.

All scalar geometry inputs, angles, and derived values must be finite. Row
count must be at least one, width and GCR must be positive, V1 GCR must not
exceed one, and every cut count must be an integer at least one. Invalid extent,
shape, nonfinite input, cut, azimuth relationship, unsupported tilt, or
impossible clearance returns a structured error containing `code`, `field`,
and `message`. No recoverable input error uses panic.

## Compatibility consequence

The default extent reproduces the reference convention. Configurable extents,
pre-construction rejection, and the `z=90°` classified state are intentional V1
contract decisions. Raw reference evidence is preserved; corrected expectations
carry CDR and DEV provenance instead of rewriting the raw oracle.

## Approval effect

Owner approval would freeze this policy for P3. Until then it remains a
recommendation and G2 remains `CONDITIONALLY PASS`, Awaiting Repository Owner Approval.

