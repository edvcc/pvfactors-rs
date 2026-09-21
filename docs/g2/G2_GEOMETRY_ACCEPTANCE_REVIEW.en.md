# G2 Geometry Acceptance Review

- Review date: 2026-09-22
- Verdict: **PASS**
- Gate statement: **Technical Gate PASS; Owner Approval PASS; Canonical Runtime R0 PASS; Golden Approval PASS.**
- Approved Golden: `geometry-golden-v0.1`
- Source candidate: `geometry-golden-v0.1-candidate`
- Approved manifest SHA-256: `efd2adf3037740b9788792c9f5be6122fb2e842d72f2ddbe2bb5552abc27141b`
- Tolerance: `geometry-tolerance-v0.1`

## Decision

CDR-003 Owner Review Revision 1 and the explicit CDR-006 DEV-013 decision are
incorporated; predicate values and tolerance are unchanged. The Repository
Owner approved CDR-003, CDR-006, `geometry-tolerance-v0.1`, and the exact
Geometry Golden manifest on 2026-09-22. The candidate pipeline
captures row geometry, projection, raw/clipped shadow, PV/ground partitions,
stable logical keys, `ReferenceIndex`, and active maps; separates raw,
normalized, and corrected artifacts; and passes schema, invariant, deviation,
comparison, and same-environment reproducibility checks. No unknown Geometry
semantic blocker was found inside the tested scope.

G2 is `PASS`: technical verification, Owner approval, Canonical Runtime R0,
CDR, tolerance, and Golden approval conditions are all closed. The approved
corpus is a byte-identical promotion of the named candidate. `develop` remains
the integration baseline; this task does not directly modify or merge it.

## Verified

- Input ZIP SHA-256 and 121 internal hashes: PASS.
- Frozen upstream source 78 Git-blob hashes: PASS.
- Upstream reference suite: 102 passed / 11 warnings / 0 failed.
- Concrete G2 catalog: 55 cases; derived families are expanded into inputs,
  including `TILT_120`, `TILT_180`, `GCR_GT_1`, `SUN_BELOW_HORIZON`, and two
  closed-domain invalid-tilt probes, nine new predicate ±ULP probes, and one
  two-frame nonzero-index DEV-013 probe.
- Generated corpus: 165 artifacts plus manifest and validation summary.
- Canonical Runtime R0: Linux x86_64 / glibc 2.39 / CPython 3.12.14; all 29
  pinned packages, GEOS 3.13.1, and determinism variables matched: PASS.
- Case and artifact JSON Schema: PASS.
- Independent invariants: 65 reports covering row-side conservation, shade bounds, ground complete
  coverage without positive overlap or gaps, finite active endpoints, active
  threshold, exact identity/order/map, corrected finite extent, structured
  invalid errors, primitive expectations, and full mirror: PASS.
- Two independent complete generations: byte-identical, PASS.
- Cross-runtime payload comparison against macOS arm64 / CPython 3.12.12:
  PASS; all 24,391 topology/key/side/index/active-state checks were exact, with
  zero exact-payload or out-of-tolerance numerical differences. Maximum absolute
  differences: angle 0, length `5.551115123125783e-16 m`, orientation
  `5.551115123125783e-17`, position `8.881784197001252e-16 m`.
- Raw versus corrected provenance: PASS; all 47 deviation records have complete
  field-level provenance for named DEV-004/CDR-003, DEV-013/CDR-006,
  DEV-016/CDR-006, or DEV-027/CDR-003.
- Branch safety: work occurred on `research/g2-owner-review-closure`, created
  from `origin/develop` `ddee1f43...`; authoritative `origin/master` remains
  `bc0b7ec1cb17938be9f4d53c83e1fb80a1abd9ba`.
- Rust Geometry Core, solver, Python binding, execution planner, SIMD, and GPU:
  not implemented, as required.

## Approved

- CDR-003: **APPROVED**.
- CDR-006: **APPROVED**.
- `geometry-tolerance-v0.1`: **APPROVED** for Geometry only.
- `geometry-golden-v0.1`: **APPROVED** at the exact manifest hash above.
- P3 Entry Contract: **ACTIVE**.

## Governance boundary

`reference/approved/geometry-golden-v0.1` is the immutable approved baseline.
Future candidates cannot overwrite it; a changed manifest requires a new
explicit Owner approval. PR #2 remains subject to normal review and was not
merged by this task. P3 implementation was not started.

## Not verified

- Windows and Linux kernels/libc variants other than R0: not executed.
- Native Rust differential results: out of scope because P3 implementation has
  not started.
- Browser, IDE, packaging, Python binding, View Factor, Perez, Radiosity,
  aggregate irradiance, parallelism, and performance: out of scope.
- P3 implementation results: not present; this closure activates only the
  entry contract.

## Gate transition

Phase 0–1 input evidence is accepted with recorded conditions. P2 / G2
technical work, Runtime verification, and governance approval are complete.
G2 is `PASS`; the P3 Entry Contract is `ACTIVE`, while P3 implementation remains
`NOT STARTED`. The existing `develop` branch is the integration baseline; this
task does not merge into it.
