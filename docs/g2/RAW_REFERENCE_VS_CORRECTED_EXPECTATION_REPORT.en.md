# Raw Reference vs Corrected Expectation Report

- Status: **APPROVED G2 EVIDENCE**
- Candidate: `geometry-golden-v0.1-candidate`
- Machine-readable evidence: `evidence/g2/raw-vs-corrected.json`

There are 45 machine-readable correction records. Every record contains a DEV
ID, CDR ID, field-level path, raw value, corrected value, and explanation. No
raw or normalized artifact was modified to obtain a corrected result.

| Records | Path / scope | Raw reference | Corrected expectation | Provenance |
|---:|---|---|---|---|
| 4 | `$.result.ground.corrected_extent_m` | hard-coded `[-100,100]` | requested finite extent | DEV-004 / CDR-003 |
| 1 | `$.result.nonzero_index_ground_lookup` | `idx=1` adapter evaluates frame 0 | evaluate requested frame 1 | DEV-013 / CDR-006 |
| 1 | `$.result.length_m` | complete-cover difference length `1.0` | empty / `0.0` | DEV-016 / CDR-006 |
| 26 | `$.result.projection[*].classification` | Reference-derived `regular` or `parallel_ground` | explicit direct/horizon/below-horizon state | DEV-027 / CDR-003 |
| 4 | front/back shaded-length paths | Reference horizon/below-horizon direct shading | zero direct shaded length | DEV-027 / CDR-003 |
| 2 | `$.result.ground` | Reference direct-shadow partition | inactive shadow slots plus full finite illuminated ground | DEV-027 / CDR-003 |
| 2 | `$.result.topology` | Reference projection topology | stable no-direct policy topology | DEV-027 / CDR-003 |
| 2 | `$.result.surfaces` | Reference projection surfaces | materialized no-direct policy surfaces | DEV-027 / CDR-003 |
| 2 | `$.result.outcome` | `captured` | `classified_state` | DEV-027 / CDR-003 |
| 2 | `$.result.state` | absent | explicit horizon/below-horizon state | DEV-027 / CDR-003 |

DEV-027 is a representation gap, not a claim that upstream has a new bug.
DEV-003 concerns Engine skip-mask behavior; it cannot express the Geometry
layer's projection state, retained row geometry, inactive direct-shadow slots,
or finite ground partition. Invalid inputs continue to use the structured
non-panic error contract and are not concealed as numeric waivers.

The Repository Owner accepted this raw/corrected evidence on 2026-09-22 as
part of the exact approved Geometry Golden. G2 is `PASS`; raw Reference evidence
remains unchanged.
