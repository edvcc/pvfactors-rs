# Geometry Golden Approval Record

- Record status: **Recommended for Approval**
- Golden status: **CANDIDATE — NOT APPROVED**
- Candidate: `geometry-golden-v0.1-candidate`
- Manifest SHA-256: `efd2adf3037740b9788792c9f5be6122fb2e842d72f2ddbe2bb5552abc27141b`
- Generator commit: `01549e07c16bfe10a82d2889b1b62c58ef6861e7`
- Reference: `pvlib/solarfactors` v1.6.1, `ecbfc863657e239817603a43898ae173c7ccad9c`
- Tolerance: `geometry-tolerance-v0.1`

## Candidate set

The set has 55 concrete cases and 165 artifacts: one `raw_reference`, one
`normalized_reference`, and one `corrected_expectation` per case.

`C01`, `C02`, `C03`, `C04`, `TILT_LEFT`, `TILT_FLAT`, `TILT_1e-10`,
`TILT_NEAR_LEFT`, `TILT_90.0`, `SHADING_NONE_CANDIDATE`,
`SHADING_PARTIAL_CANDIDATE`, `SHADING_HIGH_CANDIDATE`, `SUN_90.0`,
`SUN_ALONG_AXIS`, `CUT_2`, `CUT_8`, `CUT_ASYMMETRIC`, `UNDERGROUND`,
`CUT_ZERO`, `TILT_120`, `TILT_180`, `GCR_GT_1`, `SUN_BELOW_HORIZON`,
`INVALID_TILT_NEGATIVE`, `INVALID_TILT_GT_180`, `GROUND_NORMAL_EXTENT`,
`GROUND_BOUNDARY_ENDPOINT`, `GROUND_NEAR_BOUNDARY`, `MIRROR_BASE`,
`MIRROR_IMAGE`, `INVALID_AXIS_AZIMUTH`, `INVALID_SURFACE_AZIMUTH`,
`INVALID_NAN`, `INVALID_INF`, `INVALID_EXTENT_REVERSED`,
`PRIM_COMPLETE_COVER_DIFFERENCE`, `PRIM_ENDPOINT_TOUCH`, `PRIM_POINT_TOUCH`,
`PRIM_POSITIVE_OVERLAP`, `PRIM_ZERO_LENGTH`, `PRIM_PARALLEL_PROJECTION`,
`PRIM_COINCIDENT_PROJECTION`, `PRIM_ACTIVE_TOL_MINUS_ULP`,
`PRIM_ACTIVE_TOL_EXACT`, `PRIM_ACTIVE_TOL_PLUS_ULP`,
`MULTI_TIMESTEP_NONZERO_INDEX`, `PRIM_ENDPOINT_SNAP_MINUS_ULP`,
`PRIM_ENDPOINT_SNAP_EXACT`, `PRIM_ENDPOINT_SNAP_PLUS_ULP`,
`PRIM_ORIENTATION_MINUS_ULP`, `PRIM_ORIENTATION_EXACT`,
`PRIM_ORIENTATION_PLUS_ULP`, `PRIM_LINE_OFFSET_MINUS_ULP`,
`PRIM_LINE_OFFSET_EXACT`, `PRIM_LINE_OFFSET_PLUS_ULP`.

## Executed results

- Frozen source snapshot: all 78 Git-blob hashes passed.
- Canonical Reference Runtime R0: PASS on Linux x86_64 / glibc 2.39 /
  CPython 3.12.14 with all 29 pinned package versions, GEOS 3.13.1, and all
  four determinism environment variables matched; environment ID
  `031158a1d1be8cdb9093`.
- Case and artifact schemas: PASS.
- Independent invariants: PASS, 65 reports including structured invalid-input,
  primitive-expectation, corrected-extent, mirror, `TILT_120`, `TILT_180`,
  `GCR_GT_1`, horizon, and below-horizon checks.
- Reproducibility: PASS; two independent full R0 generations were byte-identical.
- Cross-runtime comparison against macOS arm64 / CPython 3.12.12: PASS. All
  24,391 topology/key/side/index/active-state checks were exact. Numerical
  maximum absolute differences were 0 degrees for angles,
  `5.551115123125783e-16 m` for lengths, `5.551115123125783e-17` for
  orientation, and `8.881784197001252e-16 m` for positions, all within the
  unchanged `geometry-tolerance-v0.1`; violation count was zero.
- Raw/corrected audit: PASS; all 47 deviation records contain DEV, CDR,
  field-level path, raw value, corrected value, and explanation. DEV-004 covers
  four extent records, DEV-013 one nonzero-index record, DEV-016 one
  complete-cover record, and DEV-027 41 explicit projection state/no-direct
  records. No unproven correction is hidden.
- Approved directory safety: PASS; it contains only its `NOT APPROVED` README.

## Recorded conditions

The Canonical Runtime condition remains closed. The current candidate was
generated in R0, has `canonical_environment_match=true`, and passed the expanded
cross-runtime payload comparison. The macOS arm64 / CPython 3.12.12 manifest,
validation, verification, reproducibility, and comparison records remain under
`evidence/g2/cross-runtime/`.

The superseded 39-case and 45-case R0 manifests are preserved under
`evidence/g2/history/` and are not the current approval hash.
The closure branch `research/g2-owner-review-closure` started from the latest
`origin/develop` commit `ddee1f43d78dc4060c7f20f0b9d3777b07ddc914`.
The three unintegrated canonical-runtime commits after `182dbb54...` were
cherry-picked in topological order. This task did not modify `master` or
`develop` and did not merge a pull request.

## Recommendation and owner decision

The content is **Recommended for Approval**. Approval must identify this
manifest hash and separately approve CDR-003 and CDR-006.

- CDR-003 owner decision: Pending
- CDR-006 owner decision: Pending
- Geometry Golden owner decision: Pending
- Reviewer identity/evidence: Pending

Until those decisions exist: `CONDITIONALLY PASS`, Awaiting Repository Owner Approval.
