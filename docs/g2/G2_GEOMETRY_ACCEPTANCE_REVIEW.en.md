# G2 Geometry Acceptance Review

- Review date: 2026-09-21
- Verdict: **CONDITIONALLY PASS**
- Gate statement: **Technical package complete with recorded baseline conditions; Awaiting Repository Owner Approval.**
- Candidate: `geometry-golden-v0.1-candidate`
- Manifest SHA-256: `7136955917cc1c418b6f103800c74019bca63567b034eb42d2a4c023411ccfbf`
- Tolerance: `geometry-tolerance-v0.1`

## Decision

CDR-003 and CDR-006 are complete approval candidates. The candidate pipeline
captures row geometry, projection, raw/clipped shadow, PV/ground partitions,
stable logical keys, `ReferenceIndex`, and active maps; separates raw,
normalized, and corrected artifacts; and passes schema, invariant, deviation,
comparison, and same-environment reproducibility checks. No unknown Geometry
semantic blocker was found inside the tested scope.

G2 cannot be `PASS`: the Repository Owner has not approved CDR-003, CDR-006,
or the Golden candidate. In addition, two baseline/governance conditions need
owner resolution: the supplied baseline claims unavailable CPython 3.12.14
while execution used 3.12.12 with all 29 package versions matched; and no remote
`develop` branch existed, so the work branch starts from unchanged
`origin/master` rather than a develop tip.

## Verified

- Input ZIP SHA-256 and 121 internal hashes: PASS.
- Frozen upstream source 78 Git-blob hashes: PASS.
- Upstream reference suite: 102 passed / 11 warnings / 0 failed.
- Concrete G2 catalog: 39 cases; derived families are expanded into inputs.
- Generated corpus: 117 artifacts plus manifest and validation summary.
- Case and artifact JSON Schema: PASS.
- Independent invariants: row-side conservation, shade bounds, ground complete
  coverage without positive overlap or gaps, finite active endpoints, active
  threshold, exact identity/order/map, corrected finite extent, structured
  invalid errors, primitive expectations, and full mirror: PASS.
- Two independent complete generations: byte-identical, PASS.
- Official candidate versus fresh generation: byte-identical, PASS.
- Raw versus corrected provenance: PASS; only named DEV-004/CDR-003 and
  DEV-016/CDR-006 field differences.
- Branch safety: work occurred on `research/g2-geometry-acceptance`; local and
  remote-tracking master remain `bc0b7ec1cb17938be9f4d53c83e1fb80a1abd9ba`.
- Rust Geometry Core, solver, Python binding, execution planner, SIMD, and GPU:
  not implemented, as required.

## Recommended

- CDR-003: **Recommended for Approval**.
- CDR-006: **Recommended for Approval**.
- `geometry-tolerance-v0.1`: **Recommended for Approval** for Geometry only.
- `geometry-golden-v0.1-candidate`: **Recommended for Approval after the
  runtime/develop baseline conditions are corrected or explicitly accepted**.

## Awaiting Owner Approval

1. Approve or reject CDR-003.
2. Approve or reject CDR-006.
3. Resolve the canonical Python version discrepancy and approve the exact
   candidate manifest hash, or require regeneration in the corrected runtime.
4. Designate/create the integration `develop` baseline and decide the PR path.

`reference/approved` remains `NOT APPROVED`. No candidate was promoted and no
merge or push was performed.

## Not verified

- CPython 3.12.14 execution: not possible in the available environment.
- Linux/Windows or other macOS architecture generation: not executed.
- Native Rust differential results: out of scope because P3 is blocked.
- Browser, IDE, packaging, Python binding, View Factor, Perez, Radiosity,
  aggregate irradiance, parallelism, and performance: out of scope.
- Owner identity/signature and approval evidence: not present.

## Gate transition

Phase 0–1 input evidence is accepted with recorded conditions. P2 / G2
technical work is complete as a review package, but P3 remains blocked. G2 may
be upgraded to `PASS` only after owner approval of all three governed objects
and resolution/acceptance of the two recorded baseline conditions.
