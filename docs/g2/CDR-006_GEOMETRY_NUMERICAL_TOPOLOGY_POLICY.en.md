# CDR-006 — Geometry Numerical Predicate and Stable Topology Policy

- Status: **Recommended for Approval**
- Date: 2026-09-21
- Reference: `pvlib/solarfactors` v1.6.1, `ecbfc863657e239817603a43898ae173c7ccad9c`
- Related deviations: DEV-013, DEV-016, DEV-026

## Reference tolerance audit

`DISTANCE_TOLERANCE = 1e-8 m` participates in endpoint containment and snap,
zero/active classification, surface filtering, and cleanup. Those branches are
observable compatibility behavior. `TOL_COLLINEAR = 1e-5` is applied to
unnormalized dot/cross-like quantities; scaling an otherwise identical vector
can change the result. That constant is a Python/reference implementation
artifact and is not a dimensionless physical tolerance. Buffer-based Shapely
cleanup is also not the V1 physical definition.

## Recommended predicates

- Active numerical surface: `length > 1e-8 m` (strict). A length equal to the
  threshold is inactive. This retains the initial reference topology boundary.
- Endpoint snap: snap to the canonical original endpoint when distance is
  strictly `< 1e-8 m`; equality does not snap. Snapping changes coordinates
  and length only within the named branch and must not reorder logical keys.
- Orientation/parallelism: use normalized absolute cross product with
  `max(1e-12, 64 * f64_epsilon)` as the threshold. Do not apply it to distance,
  activity, or comparison acceptance.
- Positional offset from a supporting line uses
  `max(1e-10 m, 64 * f64_epsilon * max(1 m, coordinate_scale))`.
- Comparison tolerances in `geometry-tolerance-v0.1` never replace an
  algorithm predicate and may not change topology.

The scale-aware terms apply only to orientation and line-offset predicates.
They do not scale the active-length or endpoint-snap boundaries. Any reference
topology difference caused by replacing `TOL_COLLINEAR` must be a named
field/case deviation, not absorbed by a wider comparator.

## Set operations and touch taxonomy

For collinear subtraction, interval arithmetic is normative. If `v` completely
covers `u`, `u - v` is empty. The frozen reference result for
`PRIM_COMPLETE_COVER_DIFFERENCE` has length `1 m`; the corrected expectation is
empty and is traced as DEV-016 / CDR-006. Raw evidence is not edited.

Point touch is a single non-endpoint intersection; endpoint touch is a shared
canonical endpoint; positive-length overlap has intersection length above the
active threshold; tolerance touch is a point/endpoint whose distance is within
the named snap or line-offset predicate. Point and endpoint touch do not create
positive-length shade. Coincident and parallel projection remain separate
typed outcomes.

## Stable identity and ordering

`LogicalSurfaceIdentity` is a stable `SurfaceKey`:

`{kind, source, row, side, segment, illumination, ground_element, cut_interval}`.

It exists even when its numerical length is zero. `ReferenceIndex` is the
frozen reference matrix order and is recorded separately. `ActiveIndex` is a
per-frame optional mapping for surfaces with `length > 1e-8 m`; it is not an
identity. A temporary `Vec` position is never an external identifier.

External/reconstruction order is exact: ground shadow elements by projected
row and cut interval; ground illuminated elements in ground order and cut
interval; rows left-to-right, front then back, segment order, illuminated then
shaded. Inactive slots remain in the logical order. Filtering or merging may
produce an active view only if the complete key-to-active map remains available
and positive-length regions with different source, side, normal, material, or
visibility are not merged.

## Approval effect

Owner approval would freeze these predicates and topology semantics for P3.
Until then G2 remains `CONDITIONALLY PASS`, Awaiting Repository Owner Approval.

