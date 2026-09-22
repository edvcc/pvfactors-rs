# Long-task Executability Audit

2026-09-22: cross-check of docs/00-14, all bilingual G2/P3 contracts, approved 55-case corpus, tools/comparison/schema/runtime, Cargo/workflows/tests, licenses and live GitHub state. CLOSED means interpretation/decision closed, never Rust implementation or acceptance passed. Machine inventory: `contract-audit.json`.

| ID | Status | Closure / follow-up |
|---|---|---|
| CDR-001 | OWNER_DECISION_REQUIRED | OD-02; Proposed in doc08, never assumed accepted. |
| CDR-002 | OWNER_DECISION_REQUIRED | OD-03; Proposed in doc08, never assumed accepted. |
| CDR-003 | CLOSED | ; Approved G2 policy. |
| CDR-004 | OWNER_DECISION_REQUIRED | OD-04; Proposed in doc08, never assumed accepted. |
| CDR-005 | OWNER_DECISION_REQUIRED | OD-05; Proposed in doc08, never assumed accepted. |
| CDR-006 | CLOSED | OD-01; CDR-006 approved semantics remain intact; additive public IntervalDifference clarification required. |
| CDR-007 | OWNER_DECISION_REQUIRED | OD-06; Proposed in doc08, never assumed accepted. |

## Blocking findings

BF-01: public IntervalDifference lacks a distinction between residual spans and strict open-endpoint set difference. OD-01 supplies complete semantics, counterexamples and an additive approval object. It does not overturn G2 complete-cover correction and cannot be chosen privately.

BF-02: no-direct FrameTopology lacks PV slots. A later nonzero diffuse calculation cannot consume it directly and promise PV irradiance. OD-02 recommends a named upstream zero/reject policy, separating Geometry representation domain from Simulation calculation domain. Twilight requires another physical design. This blocks P5/P7; it does not rewrite P3/G2.

## Boundary stress checks and historical text discrepancies

Point/endpoint membership is observable in Interval; zero measure does not erase public semantics. Positive-length shading and topology key/active/index remain exact. FrameTopology lifetime is already closed by the approved clarification. P3 first-error order governs multi-invalid input, rather than the generator cumulative error list; current invalid Golden cases have one compatible code/field, and future multi-error fixtures follow P3 order. Error message is diagnostic, not a parseable contract.

CDR-003 wording mentions angle comparison tolerance, while policy evidence uses a fixed 5e-11 degree relationship predicate. Production must name/freeze that predicate separately at the same value, not read a mutable acceptance profile; changing comparator tolerance must not change the input domain. This separates implementation responsibilities without changing 5e-11 or its boundary.

The bilingual historical G2 raw/corrected report says 45 records, while approved manifest/deviation evidence has 47. Record the correction here; do not edit frozen history. Tolerance JSON retains a recommendation label, while separate APPROVAL.json/Owner records approve its exact hash; a stale embedded label does not revoke or newly approve G2. The older doc12 P3 mention of CDR-002 is scoped by the later Geometry-only CDR-003/P3 Entry; CDR-002 still blocks irradiance, not independent geometry.

## All 60 algorithm items

| ID | Algorithm | Status | Decision |
|---|---|---|---|
| MATH-01 | Degree trigonometry | CLOSED | G2/P3 |
| MATH-02 | Rotation convention | CLOSED | G2/P3 |
| MATH-03 | Solar vector | CLOSED | G2/P3 |
| MATH-04 | Tolerance predicates | CLOSED | G2/P3 |
| GEO-01 | Point/Vec/Segment | CLOSED | G2/P3 |
| GEO-02 | PVSurface | CLOSED | G2/P3 |
| GEO-03 | PVSegment | CLOSED | G2/P3 |
| GEO-04 | ShadeCollection | CLOSED | G2/P3 |
| GEO-05 | PVRow & normals | CLOSED | G2/P3 |
| GEO-06 | OrderedPVArray | CLOSED | G2/P3 |
| GEO-07 | Timeseries geometry | CLOSED | G2/P3 |
| GEO-08 | Surface indexing | CLOSED | G2/P3 |
| GEO-09 | PV cut/discretization | CLOSED | G2/P3 |
| GEO-10 | Inter-row direct shading | CLOSED | G2/P3 |
| GEO-11 | Ground shadow projection | CLOSED | G2/P3 |
| GEO-12 | Ground cut projection | CLOSED | G2/P3 |
| GEO-13 | Overlap & complement | CLOSED | G2/P3 |
| GEO-14 | Ground per-cut slots | CLOSED | G2/P3 |
| GEO-15 | Containment | CLOSED | G2/P3 |
| GEO-16 | Collinearity | CLOSED | G2/P3 |
| GEO-17 | Line difference | BLOCKING_CONTRACT_CONFLICT | OD-01 |
| GEO-18 | Projection/intersection | CLOSED | G2/P3 |
| GEO-19 | Cast/cut/merge | CLOSED | G2/P3 |
| GEO-20 | Ground snapshot/degeneracy | CLOSED | G2/P3 |
| VF-01 | Hottel crossed-string | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| VF-02 | PV→PV | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| VF-03 | Obstructed strings | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| VF-04 | PV→Ground | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| VF-05 | Reciprocity / ground→PV | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| VF-06 | Sky / VF matrix | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| VF-07 | AOI quadrature basis | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| VF-08 | AOI wedge / obstruction | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| VF-09 | AOI sky | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| VF-10 | AOI matrix | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| VF-11 | Effective reflectivity | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| VF-12 | Fast grouped VF | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| IRR-01 | Input normalization | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| IRR-02 | Extraterrestrial radiation | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| IRR-03 | Relative airmass | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| IRR-04 | AOI / hemisphere | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| IRR-05 | Perez decomposition | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| IRR-06 | Luminance/back conversion | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| IRR-07 | IsotropicOrdered | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| IRR-08 | HybridPerezOrdered | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| IRR-09 | Transmission/albedo/rho | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| IRR-10 | Horizon band shading | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| IRR-11 | Circumsolar disk/Gaussian | FUTURE / OUT OF SCOPE | G2/P3 |
| IRR-12 | Absorbed source/AOI | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| IRR-13 | SAPM convenience | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| ENG-01 | Transform to surfaces | OWNER_DECISION_REQUIRED | OD-02,OD-04,OD-06,OD-07,OD-08 |
| ENG-02 | Irradiance/rho matrices | OWNER_DECISION_REQUIRED | OD-02,OD-04,OD-06,OD-07,OD-08 |
| ENG-03 | Full radiosity solve | OWNER_DECISION_REQUIRED | OD-02,OD-04,OD-06,OD-07,OD-08 |
| ENG-04 | Incident decomposition | OWNER_DECISION_REQUIRED | OD-02,OD-04,OD-06,OD-07,OD-08 |
| ENG-05 | qabs/surface update | OWNER_DECISION_REQUIRED | OD-02,OD-04,OD-06,OD-07,OD-08 |
| ENG-06 | Fast/row/segment selection | OWNER_DECISION_REQUIRED | OD-02,OD-04,OD-06,OD-07,OD-08 |
| ENG-07 | Weighted aggregation | OWNER_DECISION_REQUIRED | OD-02,OD-04,OD-06,OD-07,OD-08 |
| ENG-08 | Skip/input status | OWNER_DECISION_REQUIRED | OD-02,OD-04,OD-06,OD-07,OD-08 |
| EXEC-01 | Serial execution | IMPLEMENTATION_CHOICE | OD-07,OD-12 |
| EXEC-02 | Multiprocessing split | IMPLEMENTATION_CHOICE | OD-07,OD-12 |
| EXEC-03 | Report merge | IMPLEMENTATION_CHOICE | OD-07,OD-12 |

## All 27 deviations

| ID | Status | Decision / note |
|---|---|---|
| DEV-001 | OWNER_DECISION_REQUIRED | OD-03 |
| DEV-002 | CLOSED | Follow approved G2/P3 and fixed reference; preserve historical observations. |
| DEV-003 | OWNER_DECISION_REQUIRED | OD-02 |
| DEV-004 | CLOSED | Follow approved G2/P3 and fixed reference; preserve historical observations. |
| DEV-005 | OWNER_DECISION_REQUIRED | OD-05 |
| DEV-006 | IMPLEMENTATION_CHOICE | Preserve source evidence and close linked policy before implementing corrected behavior. |
| DEV-007 | OWNER_DECISION_REQUIRED | OD-02 |
| DEV-008 | OWNER_DECISION_REQUIRED | OD-04 |
| DEV-009 | OWNER_DECISION_REQUIRED | OD-04 |
| DEV-010 | OWNER_DECISION_REQUIRED | OD-04 |
| DEV-011 | OWNER_DECISION_REQUIRED | OD-04,OD-08 |
| DEV-012 | OWNER_DECISION_REQUIRED | OD-05 |
| DEV-013 | CLOSED | Follow approved G2/P3 and fixed reference; preserve historical observations. |
| DEV-014 | FUTURE / OUT OF SCOPE | Preserve source evidence and close linked policy before implementing corrected behavior. |
| DEV-015 | OWNER_DECISION_REQUIRED | OD-06 |
| DEV-016 | CLOSED | G2 complete-cover correction closed; public residual endpoint semantics remain BF-01. |
| DEV-017 | OWNER_DECISION_REQUIRED | OD-07 |
| DEV-018 | OWNER_DECISION_REQUIRED | OD-07 |
| DEV-019 | OWNER_DECISION_REQUIRED | OD-05,OD-08 |
| DEV-020 | CLOSED | Follow approved G2/P3 and fixed reference; preserve historical observations. |
| DEV-021 | CLOSED | Follow approved G2/P3 and fixed reference; preserve historical observations. |
| DEV-022 | OWNER_DECISION_REQUIRED | OD-05 |
| DEV-023 | CLOSED | Historical R0/G2 reproducibility closure; current host environment is checked separately. |
| DEV-024 | OWNER_DECISION_REQUIRED | OD-05 |
| DEV-025 | IMPLEMENTATION_CHOICE | Preserve source evidence and close linked policy before implementing corrected behavior. |
| DEV-026 | CLOSED | Follow approved G2/P3 and fixed reference; preserve historical observations. |
| DEV-027 | CLOSED | Follow approved G2/P3 and fixed reference; preserve historical observations. |

## PRE-LONG-TASK DECISIONS

| ID | Required closure |
|---|---|
| OD-01 | IntervalDifference residual semantics |
| OD-02 | CDR-001 input / zero / horizon / night |
| OD-03 | CDR-002 hemisphere without recursion |
| OD-04 | CDR-004 incident solve and absorption |
| OD-05 | CDR-005 named Perez corrections |
| OD-06 | CDR-007 Fast transmission |
| OD-07 | Native/Python result and optics contract |
| OD-08 | Later oracles, tolerance and approval stops |
| OD-09 | Supported platforms and wheels |
| OD-10 | V1 endpoint and autonomous authority |
| OD-11 | Branch protection and Agent permissions |
| OD-12 | Resources, Auto and performance acceptance |

## AUTHORIZED IMPLEMENTATION CHOICES

| Choice | Boundary |
|---|---|
| Private helpers/files/temporary structs | No observable API/error-order/physics change |
| Scratch/allocation/iterators/internal layout | Keep memory budget, axes/keys and numerical contract |
| Test organization/regressions/implementation order | Keep every required test/case and dependency gate |
| Dependency/backend/binding-version evaluation | Real consumer, license/MSRV/features/lock; core independent; P3 normal dependencies zero |
| Ordinary refactoring and compile/Clippy/test fixes | Never change accepted expected/tolerance to validate the same fix |
