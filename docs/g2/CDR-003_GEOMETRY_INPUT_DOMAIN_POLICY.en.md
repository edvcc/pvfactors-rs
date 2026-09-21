# CDR-003 — Geometry Input and Domain Boundary Policy

- Status: **Recommended for Approval**
- Revision: **Owner Review Revision 1 incorporated**
- Date: 2026-09-22
- Scope: P2 / G2 Geometry only
- Reference: `pvlib/solarfactors` v1.6.1, `ecbfc863657e239817603a43898ae173c7ccad9c`
- Related deviations: DEV-002, DEV-004, DEV-026, DEV-027

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

V1 accepts tilt in the closed interval `[0°, 180°]`. Exact `0°`, signed-zero
reference behavior, positive and negative near-flat rotations, exact `90°`,
`120°`, and exact `180°` are distinct fixtures. A tilt above `90°` is neither
folded into `[0°,90°]` nor allowed to exchange front/back identity. `TILT_180`
records the boundary as a legal, finite, full-orientation reversal: the row
segment retains its width and stable front/back keys, so no new degeneracy CDR
is required by the observed case. Tilt below `0°` or above `180°` returns
`GEOMETRY_TILT_UNSUPPORTED`.

Solar zenith is representable in `[0°, 180°]` by the Geometry Gate. Values
below `90°` are `direct_projection`. At exactly `90°`, the state is
`horizon_no_direct_projection`. Values above `90°` through `180°` are
`below_horizon_no_direct_projection`. In both no-direct states row geometry
remains defined, direct-shadow logical slots are retained but inactive, no huge
finite or nonfinite shadow is manufactured, and the finite ground is one
illuminated direct-projection partition. Geometry does not decide whether the
complete simulation skips a time step; night, light and irradiance policy
remains for CDR-001. Zenith below `0°` or above `180°` is invalid. Parallel
non-coincident and coincident geometric projection are still distinct typed
outcomes. Exact flatness means rotation equals zero; near-flat values are not
coerced to zero.

All scalar geometry inputs, angles, and derived values must be finite. Row
count must be at least one, width must be positive, GCR must be finite and
strictly positive, and every cut count must be an integer at least one. GCR
above one is not rejected as a proxy for an engineering convention. An actual
row intersection, clearance violation, or other geometric conflict is assessed
as that conflict. `GCR_GT_1` (GCR 1.25, three rows, tilt 45°) is a legal instance
whose row segments do not intersect. Invalid extent, shape, nonfinite input,
cut, azimuth relationship, unsupported tilt, or impossible clearance returns a
structured error containing `code`, `field`, and `message`. No recoverable
input error uses panic.

## Compatibility consequence

The default extent reproduces the reference convention. Configurable extents,
pre-construction rejection, the expanded tilt/GCR input domain, and the three
solar projection states are intentional V1 contract decisions. DEV-027 is a
representation gap, not an upstream bug: DEV-003 concerns Engine skip-mask
behavior and cannot supply the Geometry-layer state. Raw reference evidence is
preserved; corrected expectations carry field-level path, raw value, corrected
value, CDR, DEV, and explanation instead of rewriting the raw oracle.

## Approval effect

Owner approval would freeze this policy for P3. Until then it remains a
recommendation and G2 remains `CONDITIONALLY PASS`, Awaiting Repository Owner Approval.
