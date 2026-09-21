# Geometry Golden Approval Record

- Record status: **Recommended for Approval**
- Golden status: **CANDIDATE — NOT APPROVED**
- Candidate: `geometry-golden-v0.1-candidate`
- Manifest SHA-256: `5afcc7e2cbc761ef883a422dd596e972cda603313a27f8425278dd067be57e3f`
- Generator commit: `50500914c227aaeaf738b785eea3a20d96e8ee28`
- Reference: `pvlib/solarfactors` v1.6.1, `ecbfc863657e239817603a43898ae173c7ccad9c`
- Tolerance: `geometry-tolerance-v0.1`

## Candidate set

The set has 39 concrete cases and 117 artifacts: one `raw_reference`, one
`normalized_reference`, and one `corrected_expectation` per case.

`C01`, `C02`, `C03`, `C04`, `TILT_LEFT`, `TILT_FLAT`, `TILT_1e-10`,
`TILT_NEAR_LEFT`, `TILT_90.0`, `SHADING_NONE_CANDIDATE`,
`SHADING_PARTIAL_CANDIDATE`, `SHADING_HIGH_CANDIDATE`, `SUN_90.0`,
`SUN_ALONG_AXIS`, `CUT_2`, `CUT_8`, `CUT_ASYMMETRIC`, `UNDERGROUND`,
`CUT_ZERO`, `GROUND_NORMAL_EXTENT`, `GROUND_BOUNDARY_ENDPOINT`,
`GROUND_NEAR_BOUNDARY`, `MIRROR_BASE`, `MIRROR_IMAGE`,
`INVALID_AXIS_AZIMUTH`, `INVALID_SURFACE_AZIMUTH`, `INVALID_NAN`,
`INVALID_INF`, `INVALID_EXTENT_REVERSED`,
`PRIM_COMPLETE_COVER_DIFFERENCE`, `PRIM_ENDPOINT_TOUCH`, `PRIM_POINT_TOUCH`,
`PRIM_POSITIVE_OVERLAP`, `PRIM_ZERO_LENGTH`, `PRIM_PARALLEL_PROJECTION`,
`PRIM_COINCIDENT_PROJECTION`, `PRIM_ACTIVE_TOL_MINUS_ULP`,
`PRIM_ACTIVE_TOL_EXACT`, `PRIM_ACTIVE_TOL_PLUS_ULP`.

## Executed results

- Input ZIP SHA-256: `2aca31b43080431a026f421e7d28ae86a814430fe27d60c0cf6e1aef2f4f5729`;
  all 121 internal manifest entries passed.
- Frozen source snapshot: all 78 Git-blob hashes passed.
- Canonical Reference Runtime R0: PASS on Linux x86_64 / glibc 2.39 /
  CPython 3.12.14 with all 29 pinned package versions, GEOS 3.13.1, and all
  four determinism environment variables matched.
- Upstream suite: 102 passed, 11 warnings on this macOS capture. Six warnings
  are divide-by-zero reference behavior already seen in the baseline; five are
  non-interactive plotting warnings. No test failed.
- Case and artifact schemas: PASS.
- Independent invariants: PASS, 43 reports including structured invalid-input,
  primitive-expectation, corrected-extent, and mirror checks.
- Reproducibility: PASS; two independent full generations were byte-identical.
- Cross-runtime comparison against the preserved macOS arm64 / CPython 3.12.12
  candidate: PASS. All 19,511 topology/key/side/index/active-state checks were
  exact. Numerical maximum absolute differences were 0 degrees for angles,
  `1.1102230246251565e-16 m` for lengths, `5.551115123125783e-17` for
  orientation, and `5.551115123125783e-17 m` for positions, all within the
  unchanged `geometry-tolerance-v0.1`.
- Raw/corrected audit: PASS; DEV-004 affects four extent cases and DEV-016
  affects the complete-cover difference case. No unproven correction is hidden.
- Approved directory safety: PASS; it contains only its `NOT APPROVED` README.

## Recorded conditions

The Canonical Runtime condition is closed. The current candidate was generated
in R0, has `canonical_environment_match=true`, and passed the cross-runtime
payload comparison. The prior CPython 3.12.12 macOS arm64 manifest, validation
summary, verification, reproducibility, and comparison records remain under
`evidence/g2/cross-runtime/`; its complete corpus remains retrievable from Git
commit `182dbb54d351db733ff40ba40dd4f119767b1ee4`.

No remote `develop` branch existed when the work branch was created, so it
started from the unchanged `origin/master` commit
`bc0b7ec1cb17938be9f4d53c83e1fb80a1abd9ba`. GitHub records that PR #1 was
later merged externally into `develop` at
`ddee1f43d78dc4060c7f20f0b9d3777b07ddc914`, before this runtime-closure push.
This task did not modify `develop`; owner confirmation of the intended P3
integration baseline remains a governance action.

## Recommendation and owner decision

The content is **Recommended for Approval**. Approval must identify this
manifest hash and separately approve CDR-003 and CDR-006. The remaining
`develop` designation is an integration-governance condition, not an unresolved
Canonical Runtime condition.

- CDR-003 owner decision: Pending
- CDR-006 owner decision: Pending
- Geometry Golden owner decision: Pending
- Reviewer identity/evidence: Pending

Until those decisions exist: `CONDITIONALLY PASS`, Awaiting Repository Owner Approval.
