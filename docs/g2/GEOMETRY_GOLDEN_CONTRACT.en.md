# Geometry Golden Contract

- Status: **Recommended for Approval**
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
   field records the raw value, corrected value, DEV ID, CDR ID, and explanation.

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

Tools write only to `reference/candidate`. `reference/approved` remains
`NOT APPROVED`. Approval must name the candidate manifest hash and approve
CDR-003, CDR-006, and the candidate. Until then G2 is
`CONDITIONALLY PASS`, Awaiting Repository Owner Approval.

