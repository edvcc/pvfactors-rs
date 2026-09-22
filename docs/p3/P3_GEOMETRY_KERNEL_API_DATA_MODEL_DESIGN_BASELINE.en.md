# P3 Geometry Kernel API and Data Model Design Baseline

- Status: **DRAFT — AWAITING REPOSITORY OWNER REVIEW**
- Date: 2026-09-22
- Scope: P3 `solarfactors-core` math and Geometry API/data model design
- Approved Golden: `geometry-golden-v0.1`
- Governing decisions: CDR-003, CDR-006
- Related clarification: `CDR-006_IMPLEMENTATION_CLARIFICATION_FRAME_TOPOLOGY.en.md`
- Implementation state: **NOT STARTED BY THIS DOCUMENT**

## 1. Purpose and authority

This document freezes a design baseline for the next, separately authorized Rust
module/type-skeleton task. It is an engineering specification, not an
implementation and not approval to start Geometry algorithms.

The baseline consolidates the approved Geometry contracts, corrected Golden
expectations, and Rust ownership boundaries. If this document conflicts with an
approved CDR or the immutable Approved Golden, the approved evidence wins and
the conflict is a `P3 DESIGN BLOCKER`; it must not be resolved by editing the
Golden, widening a tolerance, or copying an accidental Python object model.

The design target is:

```text
Algorithm Reconstruction
+ Independent Rust Domain Model
+ Approved Reference Compatibility
+ Stable Identity
+ Explicit Numerical Semantics
```

The priority order is:

```text
Correctness
> Reference Verifiability
> Numerical Stability
> API Clarity
> Maintainability
> Performance
```

P3 reconstructs approved behavior in an independent, pure-Rust model. It does
not reproduce the Python object graph, introduce Python/pvlib/Shapely/GEOS at
runtime, or let Golden JSON become the production API.

## 2. Evidence baseline and interpretation rules

This baseline is derived from:

- `docs/05_GEOMETRY_REIMPLEMENTATION_SPEC.md` through the relevant P3 material
  in `docs/12_PHASE_GATE_IMPLEMENTATION_PLAN.md`;
- approved CDR-003 and CDR-006, their bilingual texts, the active P3 Entry
  Contract, the Geometry Golden Contract, and Geometry Tolerance Profile v0.1;
- the immutable `reference/approved/geometry-golden-v0.1` corpus; and
- the policy implementation and Owner Review checks in
  `reference/tools/geometry_golden.py`.

The evidence layers remain distinct:

1. `raw_reference` records frozen upstream observations, including defects.
2. `normalized_reference` provides deterministic, language-neutral ordering
   and representation without correcting behavior.
3. `corrected_expectation` applies only approved CDR/DEV decisions.
4. This Rust design selects a production representation that can reproduce the
   approved semantics without copying the Golden DTO shape.

Comparison tolerance never changes topology or an algorithm predicate.
Topology, keys, ordering, index mappings, classification, and nonfinite class
are exact.

## 3. Architecture and lifecycle

```text
ArrayLayout
    │
    ├── immutable static physical layout
    │
    └── GeometryFrameInput
             │
             ▼
         build_frame
             │
             ├── deterministic validation
             ├── RowGeometry[]
             ├── ProjectionClass
             ├── RowDirectShading[]
             ├── FrameTopology
             ├── SurfaceGeometry[]
             └── ActiveMap
                     │
                     ▼
                FrameGeometry
```

```text
SurfaceKey != ReferenceIndex != ActiveIndex != FrameIndex
```

`ArrayLayout` is constructed and validated once for a static configuration.
`GeometryFrameInput` is a typed raw frame value. `build_frame` validates their
combination and returns an owned `FrameGeometry`. The result is immutable by
public API and can be borrowed by later View Factor and irradiance stages.
Builder scratch, cut points, raw projections, and validation intermediates do
not outlive the build unless a future, separately approved trace contract says
otherwise.

## 4. Module boundary

The first public modules are:

```rust
pub mod math;
pub mod geometry;
```

The crate root should not initially re-export the full public surface.
Callers use paths such as:

```rust
solarfactors_core::math::Point2
solarfactors_core::geometry::ArrayLayout
```

`math` owns domain-independent two-dimensional primitives and basic algebra.
It does not own solarfactors identity, active/snap policy, Geometry validation,
or differential-comparison tolerance. `geometry` owns the solarfactors domain,
approved numerical predicates, frame construction, stable topology, and
structured Geometry errors.

The initial mathematical primitives are `Point2`, `Vec2`, `Segment2`, and
`Interval`. `Normal2`, `Direction2`, and `UnitVec2` are not introduced until a
real consumer demonstrates that their invariants remove ambiguity.

## 5. Mathematical value model

### 5.1 `Point2`

`Point2` is a position in two-dimensional Euclidean space. The candidate
public representation is:

```rust
pub struct Point2 {
    pub x: f64,
    pub y: f64,
}
```

It supports construction, finite inspection, point/vector arithmetic,
distance, and midpoint. It does not carry surface identity, endpoint snap,
approximate equality, or any Geometry tolerance.

### 5.2 `Vec2`

`Vec2` supports dot product, cross product, norm, squared norm, scalar
operations, finite inspection, and fallible normalization. Expected
mathematical degeneracy is returned as a typed outcome; normalization of a
zero or nonfinite vector must not manufacture NaN/Inf as a sentinel.

### 5.3 `Segment2`

`Segment2` is a finite segment formed by two **ordered** endpoints. It preserves
caller order and never automatically reorders left/right, high/low, or
orientation. `a == b` is a valid zero-length mathematical segment. It is not,
by that fact alone, an active Geometry surface.

### 5.4 `Interval`

`Interval` is a finite closed interval with encapsulated fields and the
invariant `lo <= hi`. `lo == hi` is valid. The normal constructor rejects NaN,
infinity, and reversed bounds. An explicit `from_unordered` may canonicalize
bounds when the caller requests that behavior. `IntervalError` reports
construction failure, and `IntervalDifference` represents zero, one, or two
ordered result intervals without using a sentinel value.

### 5.5 Finite and degeneracy policy

`Point2`, `Vec2`, and `Segment2` do not use a `FiniteF64` wrapper. They expose
`is_finite()`, but ordinary algebra is not claimed to preserve finiteness for
every input. Any value entering persistent Geometry state is checked at the
Geometry validation boundary. `Interval` is the exception because its ordering
invariant requires finite values.

Parallel, coincident, point touch, endpoint touch, positive overlap, and zero
length are mathematical outcomes, not automatically Geometry errors. Expected
degeneracy is represented by typed outcomes rather than NaN/Inf. Exact outcome
type spelling and visibility, other than the public `IntervalDifference`, are
implementation choices to be justified by consumers.

There is no universal `EPS`, `GEOMETRY_EPSILON`, `approx_eq`, or
`almost_equals` in `math`. Active length, endpoint snap, orientation,
line-offset, and differential comparison remain separate named policies.

## 6. Static input model

### 6.1 `ArrayLayout`

`ArrayLayout` describes values that do not change across frames in one Geometry
batch or simulation configuration:

```text
n_pvrows
pvrow_width_m
pvrow_height_m
gcr
axis_azimuth_deg
ground_extent
row_cuts
```

`pitch = pvrow_width_m / gcr` is derived and must not be a second input source
of truth. A successfully constructed layout is immutable by public API. There
is no `ArrayLayout::default()` because no single PV array is a meaningful
domain default.

Static invariants include: finite scalars; `n_pvrows >= 1`; positive width;
finite `gcr > 0`; valid finite extent; exactly one validated `RowCuts` value per
row; and normalized axis azimuth. GCR greater than one is not rejected as a
proxy rule; actual row intersection is checked from constructed frame geometry.

### 6.2 `RowCuts`

`RowCuts` stores independent positive cut counts for the front and back of a
row. The canonical validated layout representation is per-row; it must express
`CUT_ASYMMETRIC`, where row 1 has front `3` and back `5`, without a global-only
shortcut. An internal `NonZeroUsize` is appropriate after validation, while the
public constructor may accept ordinary integer counts and return a structured
error. The exact collection/container choice is an implementation choice.

### 6.3 `GroundExtent`

`GroundExtent` is a Geometry domain value, not a type alias for `Interval`.
Its invariant is finite `min_x < max_x`, in metres. Its approved default is
`[-100, 100]`. Row endpoints must be inside or on the extent under the approved
position predicate; rows are rejected rather than clipped. Projected ground
shadows and ground partitions may be clipped to the extent.

Only `GroundExtent::default()` is recommended. The exact constructor/getter
names are implementation choices; mutation that can invalidate the invariant
is not public.

## 7. Dynamic input and validation boundary

`GeometryFrameInput` contains only:

```text
surface_tilt_deg
surface_azimuth_deg
solar_zenith_deg
solar_azimuth_deg
```

It excludes DNI, DHI, GHI, albedo, reflectivity, transmissivity, day of year,
timestamp, Perez configuration, solver configuration, and execution policy.
There is no `GeometryFrameInput::default()`.

`GeometryFrameInput` is a typed raw frame input, not proof that the frame is
valid for a particular layout. Complete validation occurs at:

```text
ArrayLayout + GeometryFrameInput -> build_frame
```

A valid static layout does not make every frame valid.

### 7.1 Deterministic fail-fast order

Static layout validation order is frozen as:

```text
1. finite static scalars
2. row count
3. width
4. gcr
5. extent
6. cuts
7. axis azimuth normalization
```

Frame validation/build order is frozen as:

```text
1. finite frame scalars
2. tilt domain
3. solar zenith domain
4. normalize azimuths
5. surface-axis relation
6. row construction
7. clearance
8. extent containment
9. actual row intersection
10. projection / partition
11. numerical + invariant validation
```

Validation stops at the first failure in this order. The order is observable
through `code` and `field`; changing it requires review because an input may
violate more than one rule.

## 8. Error contract

Public error types are `GeometryError` and `GeometryErrorCode`.
`GeometryError` contains at least:

```text
code
field
frame?  (FrameIndex)
row?
message
```

External programs use `code` and `field`; `message` is human diagnostic text
and is not a parseable protocol. Recoverable input errors never panic.
`panic=false` belongs to the Golden adapter, not to the Rust error object.

The exact approved compatibility codes are:

```text
GEOMETRY_CLEARANCE
GEOMETRY_CUT
GEOMETRY_TILT_UNSUPPORTED
GEOMETRY_NONFINITE
GEOMETRY_AZIMUTH_RELATION
GEOMETRY_EXTENT
```

The implementation may add the following only when a real validation branch
consumes them:

```text
GEOMETRY_ROW_COUNT
GEOMETRY_WIDTH
GEOMETRY_GCR
GEOMETRY_SOLAR_ZENITH_UNSUPPORTED
GEOMETRY_ROW_INTERSECTION
GEOMETRY_ROW_OUTSIDE_EXTENT
GEOMETRY_NUMERICAL_FAILURE
GEOMETRY_INVARIANT_VIOLATION
```

An unexpected nonfinite derived from otherwise legal input is
`GEOMETRY_NUMERICAL_FAILURE`, not a user nonfinite-input error. A broken
topology or active-map invariant is `GEOMETRY_INVARIANT_VIOLATION`.

The first implementation uses manual `Display` and `std::error::Error`; it does
not add `thiserror`.

## 9. Projection classification and no-direct behavior

`ProjectionClass` is a public closed enum:

```text
DirectProjection
HorizonNoDirectProjection
BelowHorizonNoDirectProjection
```

The mapping is exact: solar zenith below `90°`, equal to `90°`, and above
`90°` through `180°`, respectively. Successful construction stores the class;
downstream code must not infer it again from solar zenith.

For either no-direct class:

- row entity geometry remains present and finite;
- every row has front and back direct-shading length `0`;
- direct-projection PV surfaces are not materialized in the selected
  `FrameTopology`;
- there are `N` inactive ground-shadow logical slots and one active full-ground
  illuminated slot; and
- no huge or nonfinite shadow is manufactured.

For N=3, the Approved `SUN_90.0` and `SUN_BELOW_HORIZON` corrected expectations
therefore have `logical_surface_count = 4` and `active_surface_count = 1`.
Changing this to a 40-slot inactive universe requires a new CDR/Golden approval.

Geometry classification does not decide whether a later Simulation stage skips
a timestep.

## 10. Stable identity and index model

### 10.1 `SurfaceKey`

`SurfaceKey` is logical semantic identity. It contains no coordinate, length,
normal, active state, floating-point value, or frame index. The production
model is a sum type:

```rust
pub enum SurfaceKey {
    Ground {
        source: GroundSource,
        element: usize,
        cut_interval: usize,
    },
    PvRow {
        row: usize,
        side: PvSide,
        segment: usize,
        illumination: Illumination,
    },
}
```

Associated public closed enums are:

```text
GroundSource = Shadow | Illumination
PvSide = Front | Back
Illumination = Illuminated | Shaded
```

The Golden adapter maps this enum to the flat nullable DTO. Production types do
not acquire multiple `Option` fields to imitate JSON.

`SurfaceKey` is stable whenever that logical surface is materialized. It is not
a claim that every projection state materializes the same surface universe.

### 10.2 `ReferenceIndex`

`ReferenceIndex` is a distinct newtype: the index of a logical surface in one
specific `FrameTopology`, ordered according to Approved Reference
reconstruction. Its numeric value is readable, but arbitrary external
construction is not public. It is not a semantic alias for `usize` and is not
implicitly convertible to `ActiveIndex`.

### 10.3 `ActiveIndex`

`ActiveIndex` is a distinct newtype for dense active-compressed order in one
frame. It is always frame-local. An inactive logical surface has no
`ActiveIndex`.

### 10.4 `FrameIndex`

`FrameIndex` is a distinct newtype used wherever a caller or internal test
selects a frame. It prevents an integer intended as a frame from being confused
with a surface index and protects the DEV-013 rule: every frame lookup evaluates
the requested frame, including a nonzero one.

### 10.5 Stability rule

The full interpretation is normative in the companion CDR-006 implementation
clarification:

- `SurfaceKey` is stable semantic identity when materialized;
- `FrameTopology` is a projection-state-specific logical surface universe;
- `ReferenceIndex` belongs to one `FrameTopology`;
- frames with the same logical topology preserve the exact
  `SurfaceKey <-> ReferenceIndex` reconstruction order; and
- a projection-state transition may select another approved `FrameTopology`.

## 11. Row and shading model

### 11.1 `RowGeometry`

`RowGeometry` is the physical two-dimensional geometry of one PV row in one
frame. It stores only:

```text
center
ordered segment (b1 -> b2)
rotation_deg
front_normal
back_normal
```

It does not duplicate width, height, row ID, highest point, or lowest point.
Width is derivable from the segment; row position in the frame's row collection
supplies row identity; high/low endpoints are derived using the approved tie
rule. The ordered segment preserves `b1 -> b2` exactly.

### 11.2 `RowDirectShading`

`RowDirectShading` is separate from the row entity and stores:

```text
front_length_m
back_length_m
```

It is a result of row geometry, solar geometry, and neighbor relationships.
Both lengths are zero in no-direct states. They must remain within
`[0, pvrow_width_m]` under the approved predicates.

## 12. Surface, topology, and active map

### 12.1 `SurfaceGeometry`

`SurfaceGeometry` stores only a `Segment2`. Length is always derived by
`segment.length()`. It does not duplicate active state, `ActiveIndex`, normal,
side, source, illumination, `SurfaceKey`, or `ReferenceIndex`.

PV normals are derived from `SurfaceKey` row/side plus `RowGeometry`. Ground
normal remains absent at the P3 Geometry Golden layer; a later physical module
may derive it from surface kind if needed.

### 12.2 `FrameTopology`

The production representation is an ordered collection of `SurfaceKey`. An
additional public `LogicalSurface` wrapper is unnecessary. The invariants are:

```text
SurfaceKey values are unique
ReferenceIndex values are dense 0..len-1
position i safely derives ReferenceIndex(i) inside this topology
ordering follows the approved reconstruction order
```

The vector position is an internal representation invariant. Identity remains
the `SurfaceKey`.

For direct projection, ordering is exact:

1. ground shadow elements by projected row, then cut interval;
2. ground illuminated elements in ground order, then cut interval;
3. rows in row order, front then back, segment order, illuminated then shaded.

Inactive logical slots remain in the selected direct-projection topology.

For no-direct projection, ordering is exactly N inactive ground-shadow keys
followed by the one active illuminated full-ground key. PV projection keys are
not materialized in that topology.

### 12.3 `ActiveMap`

`ActiveMap` stores both directions:

```text
reference_to_active: ReferenceIndex -> Option<ActiveIndex>
active_to_reference: ActiveIndex -> ReferenceIndex
```

It must satisfy dense active indices, bidirectional consistency, and
`inactive -> None`. An active surface has finite endpoints and length strictly
greater than `1e-8 m`. Filtering or merging may create an active view only when
the complete logical mapping remains available, and positive-length surfaces
with different source, side, normal, material, or visibility are not merged.

### 12.4 `FrameGeometry`

The logical result is:

```text
FrameGeometry
├── ProjectionClass
├── RowGeometry[]
├── RowDirectShading[]
├── FrameTopology
├── SurfaceGeometry[]
└── ActiveMap
```

Its core invariant is:

```text
FrameTopology.len
== SurfaceGeometry.len
== ActiveMap.reference_to_active.len
```

The row and shading collections also have exactly `ArrayLayout.n_pvrows`
entries in row order. `FrameGeometry` is owned output and immutable by public
API.

## 13. Stored versus derived values

| Concept | Stored | Derived / reason |
|---|---|---|
| `RowGeometry.center` | Yes | Frame entity state |
| `RowGeometry.segment` | Yes | Canonical ordered row coordinates |
| `RowGeometry.rotation_deg` | Yes | Approved orientation result |
| Front/back row normals | Yes | Shared once per row, not per cut surface |
| Row width and height | No | Width from segment; static height belongs to layout input |
| Highest/lowest endpoint | No | Derived with approved tie rule |
| `RowDirectShading` lengths | Yes | Frame result, not row entity state |
| `ProjectionClass` | Yes | Prevents downstream reclassification |
| `FrameTopology` key order | Yes | Exact logical reconstruction contract |
| `ReferenceIndex` | No separate field | Derived from topology position |
| `SurfaceGeometry.segment` | Yes | Minimal numerical surface state |
| Surface length | No | Derived from `segment.length()` |
| Surface active boolean | No separate source | Derived by approved active predicate and represented in `ActiveMap` |
| `ActiveMap` | Yes | Dense compression is not derivable from geometry without policy |
| PV surface normal | No | Derived from row, side, and `RowGeometry` |
| Side/source/illumination | No duplicate | Derived from `SurfaceKey` |
| Golden flat DTO fields | No | Test/reference adapter concern |

The purpose is one source of truth per fact. Cached derived values require a
future measured consumer and an explicit consistency strategy.

## 14. Public and internal API matrix

| Component | Visibility | Reason |
|---|---|---|
| `Point2` | public | Stable two-dimensional math value |
| `Vec2` | public | Stable vector algebra value |
| `Segment2` | public | Ordered finite-segment value |
| `Interval` | public | Reusable finite closed interval |
| `IntervalError` | public | Constructor failure contract |
| `IntervalDifference` | public | Typed set-operation result |
| `ArrayLayout` | public | Primary static Geometry input |
| `RowCuts` | public | Per-row front/back discretization input |
| `GroundExtent` | public | Validated Geometry domain extent |
| `GeometryFrameInput` | public | Typed raw frame input |
| `SurfaceKey` and associated enums | public | Stable semantic identity |
| `ReferenceIndex` | public, restricted constructor | Observable reconstruction index |
| `ActiveIndex` | public, restricted constructor | Observable compressed index |
| `FrameIndex` | public | Prevents frame/surface index confusion |
| `ProjectionClass` | public | Explicit successful-build classification |
| `RowGeometry` | public | Physical row result |
| `RowDirectShading` | public | Direct-shading result |
| `FrameTopology` | public | Ordered logical surface universe |
| `SurfaceGeometry` | public | Minimal numerical surface geometry |
| `ActiveMap` | public | Exact logical/active mapping |
| `FrameGeometry` | public | Primary Geometry result |
| `GeometryError`, `GeometryErrorCode` | public | Stable failure contract |
| `build_frame` | public | Single primary P3 algorithm entry |
| Numerical predicate helpers | crate-private | Approved algorithm policy, not independent API |
| `ValidatedFrameInput`, `SolarSection` | crate-private | Build intermediates |
| Cut/shade/projection builders | private or crate-private | Implementation pipeline |
| Partition/topology/active-map builders | private or crate-private | Preserve one public entry and invariants |
| `GeometryBuildTrace` | private unless separately approved | No public trace contract yet |
| Golden DTO/reference adapter | test-only | Development oracle concern |

## 15. Main API and forbidden public surface

The single primary P3 calculation entry is:

```rust
pub fn build_frame(
    layout: &ArrayLayout,
    input: &GeometryFrameInput,
) -> Result<FrameGeometry, GeometryError>;
```

P3 does not add `GeometryEngine`, `GeometryCalculator`, `GeometryContext`, or
`GeometryService`. It does not yet define `GeometryBatch`, `GeometrySeries`, or
`build_frames`; DEV-013 is verified with crate-internal/test multi-frame
facilities until the later Simulation `InputBatch` contract is designed.

The following are not public: `ValidatedFrameInput`, `SolarSection`,
`CutPoint`, `GeometryBuildTrace`, predicate/snap helpers, row/projection/shade/
PV-partition/ground-partition/topology/active-map builders, Golden DTOs, and
reference adapters.

## 16. Serialization, defaults, and evolvability

Public domain types do not derive `serde::Serialize` or `Deserialize` merely to
read Golden JSON. Serialization belongs in test support. No `serde` dependency
is introduced by this baseline.

Only `GroundExtent::default()` is recommended. `ArrayLayout` and
`GeometryFrameInput` have no domain-meaningful default.

`#[non_exhaustive]` is an implementation-time recommendation for likely-to-grow
`GeometryErrorCode` and `SurfaceKey`. It should be evaluated when the actual
type declarations are reviewed because it affects downstream matching and
construction. Stable closed enums such as `PvSide`, `Illumination`, and
`ProjectionClass` do not receive it mechanically. This document does not claim
that any attribute is already implemented.

## 17. Numerical policy boundaries

The approved Geometry predicates are:

```text
active length:        length > 1e-8 m
endpoint snap:        distance < 1e-8 m
orientation cross:    <= max(1e-12, 64 * f64_epsilon)
line offset:           <= max(1e-10 m,
                              64 * f64_epsilon * max(1 m, coordinate_scale))
```

The strict versus inclusive operators are part of the contract. The
differential profiles (`orientation`, `position`, `length`, `angle`) only judge
numeric agreement; they cannot decide activity, snapping, orientation, or
topology.

Collinear interval subtraction is normative. Complete coverage returns an
empty difference, as approved for `PRIM_COMPLETE_COVER_DIFFERENCE`. Point touch
and endpoint touch create no positive-length shade. Parallel non-coincident and
coincident projection are distinct typed outcomes.

## 18. Invariants and forbidden states

A successful `FrameGeometry` must satisfy all applicable invariants:

- every stored point, vector, coordinate, angle, and derived scalar is finite;
- each row segment preserves approved endpoint order and width;
- every row remains strictly above the approved clearance and within extent;
- row segments do not actually intersect;
- illuminated plus shaded length equals width on each PV side;
- shade length lies in `[0, width]`;
- finite ground is covered without positive overlap or unexplained gaps;
- topology keys are unique and reconstruction indices are dense;
- active-map directions are exact inverses for active surfaces;
- active endpoints are finite and active length is strictly above threshold;
- key, side, coordinates, row geometry, and derived normal agree; and
- full mirror transforms row geometry, solar vector, normals, extent, row
  order, and side interpretation together.

Forbidden states include nonfinite persistent Geometry state, duplicate
`SurfaceKey` in one topology, an active surface with no reverse map, an inactive
surface with an `ActiveIndex`, a `ReferenceIndex` from another topology used
without explicit remapping, a row clipped into validity, or a changed topology
hidden by numeric tolerance.

## 19. Dependency and ownership policy

Normal dependencies remain zero for the first implementation. In particular,
this design does not require `thiserror`, `serde`, `serde_json`, `proptest`,
`approx`, `nalgebra`, `geo`, `ndarray`, or `ordered-float`. A dependency may be
reconsidered only when an implemented consumer and its trade-offs are reviewed.

Inputs are borrowed by `build_frame`; output owns the values required by later
stages. No Python object, Shapely geometry, global mutable configuration, or
solver/execution state enters the Geometry model.

## 20. Approved evidence anchors

The next implementation and tests must retain at least these observable anchors:

- `CUT_ASYMMETRIC`: row 1 front segments `0..2`, back segments `0..4`, with
  illuminated then shaded slots per segment;
- `MULTI_TIMESTEP_NONZERO_INDEX`: requested frame 1 is actually evaluated while
  logical/reference identity remains stable for the same topology;
- `SUN_90.0`: horizon no-direct topology with three inactive shadow slots and
  one active full-ground illuminated slot;
- `SUN_BELOW_HORIZON`: the same topology shape with below-horizon classification;
- `PRIM_COMPLETE_COVER_DIFFERENCE`: complete cover produces an empty result;
- the ±ULP active, snap, orientation, and line-offset cases preserve their
  exact predicate boundary operators.

## 21. Implementation choices and blockers

The following are non-blocking `Implementation Choice` items for the next task:

- physical file count and internal module layout;
- constructor and getter spelling;
- the concrete collection used for validated per-row cuts;
- private typed-outcome names for mathematical degeneracy;
- allocation and scratch reuse strategy; and
- whether a cached lookup accelerates `SurfaceKey` access while preserving the
  ordered topology as the source of truth.

No new `P3 DESIGN BLOCKER` was found while consolidating this baseline. If
implementation evidence later conflicts with an approved CDR or Golden field,
work must stop at that conflict; it must not silently select new semantics.

## 22. Review and change control

This document is a draft until the Repository Owner approves it. Approval of
this document would authorize it as input to a separate Math + Geometry Module
Skeleton and Public Type Declaration Bootstrap task; it would not by itself
approve algorithm correctness or G3.

Any change to projection classification, no-direct topology, stable identity,
predicate values/operators, validation order, or approved error compatibility
requires explicit review and, when it changes approved semantics, a new or
superseding CDR/Golden object. Implementation details listed above do not become
CDRs unless they change an observable contract.
