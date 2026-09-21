# Geometry Golden Contract

- Status: **APPROVED**
- Candidate version: `geometry-golden-v0.1-candidate`
- Tolerance: `geometry-tolerance-v0.1`
- Reference: `pvlib/solarfactors` v1.6.1, `ecbfc863657e239817603a43898ae173c7ccad9c`

## Purpose and authority

The Geometry Golden is a development oracle for independent Rust
reimplementation. It is not a Python runtime dependency or permission to copy
Python/Shapely implementation structure. It records mathematical inputs,
observable reference behavior, explicit corrected expectations, and stable
topology. Candidate artifacts have no approved status until the Repository
Owner approves the named set.

## Three immutable classifications

1. `raw_reference` is a direct observation of the frozen reference, including
   exceptions, nonfinite values, and known defects.
2. `normalized_reference` converts the observation into deterministic,
   language-neutral canonical JSON. It defines ordering, units, numeric type,
   nonfinite mask, logical key, `ReferenceIndex`, and per-frame active map. It
   does not correct behavior.
3. `corrected_expectation` applies only named CDR/DEV decisions. Every changed
   field records its field-level path, raw value, corrected value, DEV ID, CDR
   ID, and explanation.

No generator may rewrite raw evidence to make comparison pass. A corrected
field without decision provenance invalidates the candidate.

## Canonical representation

Positions and lengths are f64 metres; angles are f64 degrees except explicitly
named radians; orientation vectors are dimensionless f64. JSON object keys are
sorted for hashing. NaN and infinities are encoded as `{"nonfinite":"..."}`
and listed by JSON path in `nonfinite_mask`; native non-standard JSON NaN is
forbidden. Python object repr and Shapely serialization are not contract data.

Every ordered-array artifact contains normalized input; rotation and solar 2D
vector; projection classification; row center/endpoints/normals/width/order;
raw and clipped ground shadow; ground cuts, shaded and illuminated elements;
PV and ground logical surfaces; coordinates, lengths, side, shade class,
`SurfaceKey`, `ReferenceIndex`, active state, and `ActiveIndex`. Invalid inputs
contain structured V1 errors and `panic=false`.

`SurfaceKey` is
`{kind, source, row, side, segment, illumination, ground_element, cut_interval}`.
It survives zero length. The exact reference and reconstruction order is fixed
by CDR-006; vector position is not an identity.

The corrected Geometry representation classifies solar zenith as
`direct_projection`, `horizon_no_direct_projection`, or
`below_horizon_no_direct_projection`. A no-direct artifact retains finite row
geometry and stable inactive ground-shadow logical slots, plus one active
illuminated surface spanning the configured finite extent. It contains no huge
or nonfinite direct shadow and does not decide the later simulation skip policy.

## Manifest and provenance

The manifest records reference version and commit, Python/NumPy/Shapely/pvlib
versions, environment identity, generator commit and digest, generation time,
case and catalog hashes, field name, axes, unit map, dtype, shape, payload hash,
nonfinite mask, classification, status, transformation, and license relevance.
Source license text is retained at `reference/PVLIB_LICENSE.txt`.

## Validation and reproducibility

Acceptance requires: case and artifact schema validation; direct frozen
reference capture; normalization; candidate generation; two independent runs
that are byte-identical for payload, topology, keys, `ReferenceIndex`, active
map and nonfinite classification; candidate comparison; independent row-side,
shade-bound, ground-coverage, finite-endpoint, active-threshold, identity and
full-mirror invariants; raw/corrected deviation audit; document-pair check; and
branch-safety evidence.

Generation determinism is exact in one frozen environment. Later Rust numeric
comparison may use `geometry-tolerance-v0.1`; that tolerance may not hide
generation nondeterminism or topology differences.

## Governance

Generation tools write only to `reference/candidate`; they never overwrite
`reference/approved`. The Repository Owner approved CDR-003, CDR-006,
`geometry-tolerance-v0.1`, and source candidate manifest
`efd2adf3037740b9788792c9f5be6122fb2e842d72f2ddbe2bb5552abc27141b` on
2026-09-22. The byte-identical approved corpus is immutable at
`reference/approved/geometry-golden-v0.1`. Any manifest change is a new
approval object requiring a new explicit Owner decision. G2 is `PASS`.
