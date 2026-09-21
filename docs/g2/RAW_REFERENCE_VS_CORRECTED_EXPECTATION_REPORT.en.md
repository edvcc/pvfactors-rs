# Raw Reference vs Corrected Expectation Report

- Status: **Recommended for Approval**
- Candidate: `geometry-golden-v0.1-candidate`
- Machine-readable evidence: `evidence/g2/raw-vs-corrected.json`

Five field-level differences are present; every difference has both a DEV and a
CDR. No raw artifact was modified.

| Case | Field | Raw reference | Corrected expectation | Provenance |
|---|---|---|---|---|
| `GROUND_NORMAL_EXTENT` | `ground.extent` | `[-100,100]` | `[-10,10]` | DEV-004 / CDR-003 |
| `GROUND_BOUNDARY_ENDPOINT` | `ground.extent` | `[-100,100]` | `[-0.5,0.5]` | DEV-004 / CDR-003 |
| `GROUND_NEAR_BOUNDARY` | `ground.extent` | `[-100,100]` | `[-0.500000000001,0.500000000001]` | DEV-004 / CDR-003 |
| `INVALID_EXTENT_REVERSED` | `ground.extent` | `[-100,100]` | structured invalid-extent outcome for `[1,-1]` | DEV-004 / CDR-003 |
| `PRIM_COMPLETE_COVER_DIFFERENCE` | `result.length_m` | `1.0` | `0.0` / empty | DEV-016 / CDR-006 |

The first four differences separate the hard-coded reference numerical extent
from the V1 public finite-extent contract. The final difference corrects a
confirmed complete-cover subtraction defect using interval set semantics. All
other candidate corrected artifacts either equal normalized reference geometry,
apply the structured invalid-input contract, or apply the named horizon state.
They are not represented as silent numeric waivers.

The report remains a candidate decision input. `CONDITIONALLY PASS`, Awaiting Repository Owner Approval.
