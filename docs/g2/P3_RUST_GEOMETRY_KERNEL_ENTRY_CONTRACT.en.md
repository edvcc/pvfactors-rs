# P3 Rust Geometry Kernel Entry Contract

- Status: **ACTIVE**
- Gate: **G2 PASS**
- P3 Implementation: **NOT STARTED**
- Approved Golden: `geometry-golden-v0.1`
- Source candidate: `geometry-golden-v0.1-candidate`
- Approved manifest: `efd2adf3037740b9788792c9f5be6122fb2e842d72f2ddbe2bb5552abc27141b`
- Approved tolerance: `geometry-tolerance-v0.1`
- Approval date: 2026-09-22

## Activation fields

- `approved_case_ids =` all 55 IDs in the Approved case IDs section
- `approved_golden_version = geometry-golden-v0.1`
- `approved_manifest_sha256 = efd2adf3037740b9788792c9f5be6122fb2e842d72f2ddbe2bb5552abc27141b`
- `approved_cdrs = [CDR-003, CDR-006]`
- `approved_tolerance = geometry-tolerance-v0.1`

The Repository Owner populated these fields through `G2 Approval Closure Task
v1.0` dated 2026-09-22. This activates the entry contract but does not itself
start or implement P3.

## Semantics to freeze on activation

Finite closed ground extent with reference-compatible default `[-100,100]`;
rows inside/on extent; projected ground clipping; strict clearance above
`1e-10 m`; finite modulo-normalized azimuths; non-flat surface azimuth at
axis±90°; tilt `[0°,180°]` without folding or side exchange; exact-flat
distinction; solar zenith representation `[0°,180°]` with `direct_projection`,
`horizon_no_direct_projection`, and `below_horizon_no_direct_projection` states;
finite strictly positive GCR without a `<=1` proxy cap; actual geometry
conflicts checked by their own rules; typed parallel and coincident geometric
projection; structured non-panic errors; interval-correct
subtraction; strict active and snap thresholds; scale-aware orientation and
offset predicates; stable `SurfaceKey`, separate `ReferenceIndex` and
per-frame `ActiveIndex`; exact reconstruction order with inactive slots.
Every frame-selecting lookup evaluates its requested index; the frozen
Reference's DEV-013 `idx -> 0` ground-adapter defect is not reproduced.

## Approved case IDs

The activation decision approves all 55 IDs below:

`C01`, `C02`, `C03`, `C04`, `TILT_LEFT`, `TILT_FLAT`, `TILT_1e-10`,
`TILT_NEAR_LEFT`, `TILT_90.0`, `SHADING_NONE_CANDIDATE`,
`SHADING_PARTIAL_CANDIDATE`, `SHADING_HIGH_CANDIDATE`, `SUN_90.0`,
`SUN_ALONG_AXIS`, `CUT_2`, `CUT_8`, `CUT_ASYMMETRIC`, `UNDERGROUND`,
`CUT_ZERO`, `TILT_120`, `TILT_180`, `GCR_GT_1`, `SUN_BELOW_HORIZON`,
`INVALID_TILT_NEGATIVE`, `INVALID_TILT_GT_180`,
`MULTI_TIMESTEP_NONZERO_INDEX`, `GROUND_NORMAL_EXTENT`,
`GROUND_BOUNDARY_ENDPOINT`, `GROUND_NEAR_BOUNDARY`, `MIRROR_BASE`,
`MIRROR_IMAGE`, `INVALID_AXIS_AZIMUTH`, `INVALID_SURFACE_AZIMUTH`,
`INVALID_NAN`, `INVALID_INF`, `INVALID_EXTENT_REVERSED`,
`PRIM_COMPLETE_COVER_DIFFERENCE`, `PRIM_ENDPOINT_TOUCH`, `PRIM_POINT_TOUCH`,
`PRIM_POSITIVE_OVERLAP`, `PRIM_ZERO_LENGTH`, `PRIM_PARALLEL_PROJECTION`,
`PRIM_COINCIDENT_PROJECTION`, `PRIM_ACTIVE_TOL_MINUS_ULP`,
`PRIM_ACTIVE_TOL_EXACT`, `PRIM_ACTIVE_TOL_PLUS_ULP`,
`PRIM_ENDPOINT_SNAP_MINUS_ULP`, `PRIM_ENDPOINT_SNAP_EXACT`,
`PRIM_ENDPOINT_SNAP_PLUS_ULP`, `PRIM_ORIENTATION_MINUS_ULP`,
`PRIM_ORIENTATION_EXACT`, `PRIM_ORIENTATION_PLUS_ULP`,
`PRIM_LINE_OFFSET_MINUS_ULP`, `PRIM_LINE_OFFSET_EXACT`,
`PRIM_LINE_OFFSET_PLUS_ULP`.

The approved set covers row counts 1/2/3/11; left,
right, flat, positive/negative near-zero, 90°, 120°, and 180°; GCR above one;
direct, horizon, and below-horizon solar states; no/partial/high shade; cut
1/2/8 and 3/5; finite/boundary ground extent; invalid inputs; complete cover;
touch/overlap; tolerance ±ULP; parallel/coincident; and full mirror.
The minimum set must also cover endpoint snap, normalized orientation, and
line-offset ±ULP boundaries plus a multi-timestep nonzero-index lookup.

## Required invariants

Each side's illuminated plus shaded length equals row width; shade is within
`[0,width]`; finite ground is completely covered without positive overlap or
unexplained gaps; active endpoints are finite; active length is strictly above
threshold; key/side/coordinates agree; external identity does not depend on
vector position; full mirror transforms row geometry, sun vector, normals,
extent, row order and side interpretation together.

## Permitted reference deviations

Only deviations named by the activated approval are permitted. The current
candidate proposes DEV-004/CDR-003 for finite configurable extent,
DEV-013/CDR-006 for requested-frame ground lookup,
DEV-016/CDR-006 for complete-cover difference, and DEV-027/CDR-003 for explicit
projection state and no-direct policy topology. Raw reference artifacts remain
immutable. No other output may differ under a generic "robustness" waiver.

## Exact P3 implementation scope

P3 may implement Rust value types (`Point2`, vectors, segments, intervals),
geometry input validation and structured errors, rotation and row construction,
solar 2D projection classification, shadow projection/clipping, PV side
partition, ground partition, stable `SurfaceKey` / `ReferenceIndex` /
`ActiveIndex`, and Geometry-only tests and differential comparison. It may add
only dependencies justified by real consumers.

P3 must not implement View Factor, Perez, Radiosity, irradiance aggregation,
solver selection, Python binding, serial/parallel planner, Adaptive Planner,
SIMD, or GPU. It must not depend on Python, pvlib, Shapely, or GEOS at runtime.

## Forbidden behavior changes

No reinterpretation of approved semantics; no use of `Vec` position as stable
identity; no widening predicates to pass Golden; no correction of raw fixtures;
no merging across source/side/normal/material/visibility; no second algorithm
for parallel execution; no unregistered reference deviation.

## Entry preconditions

All entry preconditions are satisfied: CDR-003, CDR-006, the exact Golden
manifest, and the Geometry-only tolerance are approved; Canonical Runtime R0
and cross-runtime comparison pass. This contract is `ACTIVE` and may be used by
a separately authorized P3 implementation task. `develop` is the integration
baseline, but the current pull request is not merge authority. This G2 closure
did not start P3 implementation.
