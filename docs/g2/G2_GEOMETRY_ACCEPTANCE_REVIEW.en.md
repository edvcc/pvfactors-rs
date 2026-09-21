# G2 Geometry Acceptance Review

- Review date: 2026-09-22
- Verdict: **CONDITIONALLY PASS**
- Gate statement: **Technical package complete with recorded baseline conditions; Awaiting Repository Owner Approval.**
- Candidate: `geometry-golden-v0.1-candidate`
- Manifest SHA-256: `efd2adf3037740b9788792c9f5be6122fb2e842d72f2ddbe2bb5552abc27141b`
- Tolerance: `geometry-tolerance-v0.1`

## Decision

CDR-003 Owner Review Revision 1 and the explicit CDR-006 DEV-013 decision are
incorporated; predicate values and tolerance are unchanged. Both CDRs remain
approval candidates. The candidate pipeline
captures row geometry, projection, raw/clipped shadow, PV/ground partitions,
stable logical keys, `ReferenceIndex`, and active maps; separates raw,
normalized, and corrected artifacts; and passes schema, invariant, deviation,
comparison, and same-environment reproducibility checks. No unknown Geometry
semantic blocker was found inside the tested scope.

G2 cannot be `PASS`: the Repository Owner has not approved CDR-003, CDR-006,
or the Golden candidate. `develop` is the integration baseline for this closure
work, but this task does not modify or merge it. The Canonical Runtime blocker
is closed: the current candidate was generated under R0 and passed comparison
against the independently regenerated 3.12.12 run.

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

## Recommended

- CDR-003: **Recommended for Approval**.
- CDR-006: **Recommended for Approval**.
- `geometry-tolerance-v0.1`: **Recommended for Approval** for Geometry only.
- `geometry-golden-v0.1-candidate`: **Recommended for Approval**. It remains a
  candidate and was not automatically approved.

## Awaiting Owner Approval

1. Approve or reject CDR-003.
2. Approve or reject CDR-006.
3. Approve or reject the exact R0-generated candidate manifest hash.
4. Review the new pull request to `develop`; do not merge until all governed
   decisions are explicit.

`reference/approved` remains `NOT APPROVED`. No candidate was promoted and no
merge was performed.

## Not verified

- Windows and Linux kernels/libc variants other than R0: not executed.
- Native Rust differential results: out of scope because P3 is blocked.
- Browser, IDE, packaging, Python binding, View Factor, Perez, Radiosity,
  aggregate irradiance, parallelism, and performance: out of scope.
- Owner identity/signature and approval evidence: not present.

## Gate transition

Phase 0–1 input evidence is accepted with recorded conditions. P2 / G2
technical work is complete as a review package, and the Runtime blocker is
closed, but P3 remains blocked. G2 may be upgraded to `PASS` only after owner
approval of all three governed objects. The existing `develop` branch is the
integration baseline; this task does not merge into it.
