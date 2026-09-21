# P3 Rust Geometry Kernel Entry Contract

- Status: **Recommended for Approval — NOT ACTIVE**
- Gate: `CONDITIONALLY PASS`, Awaiting Repository Owner Approval
- Candidate Golden: `geometry-golden-v0.1-candidate`
- Candidate tolerance: `geometry-tolerance-v0.1`

## Activation fields

- `approved_case_ids = []`
- `approved_golden_version = null`
- `approved_manifest_sha256 = null`
- `approved_cdrs = []`

These fields are intentionally empty. They may be populated only by a
Repository Owner decision that names CDR-003, CDR-006, and the candidate
manifest. Until then no P3 implementation may begin.

## Semantics to freeze on activation

Finite closed ground extent with reference-compatible default `[-100,100]`;
rows inside/on extent; projected ground clipping; strict clearance above
`1e-10 m`; finite modulo-normalized azimuths; non-flat surface azimuth at
axis±90°; tilt `[0°,90°]`; exact-flat distinction; typed horizon, parallel, and
coincident projection; structured non-panic errors; interval-correct
subtraction; strict active and snap thresholds; scale-aware orientation and
offset predicates; stable `SurfaceKey`, separate `ReferenceIndex` and
per-frame `ActiveIndex`; exact reconstruction order with inactive slots.

## Candidate case IDs

The activation decision may approve all 39 IDs listed in the Geometry Golden
Approval Record or an explicit subset. It must not refer only to a family name.
The minimum activated set must continue to cover row counts 1/2/3/11; left,
right, flat, positive/negative near-zero and 90°; no/partial/high shade; cut
1/2/8 and 3/5; finite/boundary ground extent; invalid inputs; complete cover;
touch/overlap; tolerance ±ULP; parallel/coincident; and full mirror.

## Required invariants

Each side's illuminated plus shaded length equals row width; shade is within
`[0,width]`; finite ground is completely covered without positive overlap or
unexplained gaps; active endpoints are finite; active length is strictly above
threshold; key/side/coordinates agree; external identity does not depend on
vector position; full mirror transforms row geometry, sun vector, normals,
extent, row order and side interpretation together.

## Permitted reference deviations

Only deviations named by the activated approval are permitted. The current
candidate proposes DEV-004/CDR-003 for finite configurable extent and
DEV-016/CDR-006 for complete-cover difference. Raw reference artifacts remain
immutable. No other output may differ under a generic "robustness" waiver.

## Exact P3 implementation scope

P3 may implement Rust value types (`Point2`, vectors, segments, intervals),
input validation and structured errors, rotation and row construction, solar
2D projection classification, shadow projection/clipping, PV side partition,
ground partition, stable topology keys/order/maps, and Geometry-only tests and
comparators. It may add only dependencies justified by real consumers.

P3 must not implement View Factor, Perez, Radiosity, irradiance aggregation,
solver selection, Python binding, serial/parallel planner, adaptive execution,
SIMD, or GPU. It must not depend on Python, pvlib, Shapely, or GEOS at runtime.

## Forbidden behavior changes

No reinterpretation of approved semantics; no use of `Vec` position as stable
identity; no widening predicates to pass Golden; no correction of raw fixtures;
no merging across source/side/normal/material/visibility; no second algorithm
for parallel execution; no unregistered reference deviation.

## Entry preconditions

Owner approval of CDR-003, CDR-006, exact Golden manifest and tolerance;
resolution/acceptance of the Python runtime discrepancy; designation of the
`develop` integration baseline; and a P3 task created only after those records
exist. This contract does not itself authorize implementation.
