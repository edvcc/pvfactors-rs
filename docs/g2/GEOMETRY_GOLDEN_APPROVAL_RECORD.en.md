# Geometry Golden Approval Record

- Record status: **Recommended for Approval**
- Golden status: **CANDIDATE — NOT APPROVED**
- Candidate: `geometry-golden-v0.1-candidate`
- Manifest SHA-256: `b51e626e19734fce0d27e7c7a85c929f16a082e34e56343617b0dc6b83e76920`
- Generator commit: `0376dafc0019be3d4045c124f1f83c9a9f94bead`
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
- Upstream suite: 102 passed, 11 warnings on this macOS capture. Six warnings
  are divide-by-zero reference behavior already seen in the baseline; five are
  non-interactive plotting warnings. No test failed.
- Case and artifact schemas: PASS.
- Independent invariants: PASS, 43 reports including structured invalid-input,
  primitive-expectation, corrected-extent, and mirror checks.
- Reproducibility: PASS; two independent full generations were byte-identical.
- Candidate compare against a further fresh generation: PASS, no differences.
- Raw/corrected audit: PASS; DEV-004 affects four extent cases and DEV-016
  affects the complete-cover difference case. No unproven correction is hidden.
- Approved directory safety: PASS; it contains only its `NOT APPROVED` README.

## Recorded conditions

The 29 pinned package versions match. Capture ran on CPython 3.12.12 macOS
arm64, while the Phase 0–1 package claims CPython 3.12.14. That claimed patch
version was not available in this execution environment. The owner must either
correct/replace the canonical runtime declaration and regenerate, or explicitly
accept a new canonical runtime before approval.

No remote `develop` branch existed after fetch; only `origin/master` was
available. The work branch was therefore created from the unchanged
`origin/master` commit `bc0b7ec1cb17938be9f4d53c83e1fb80a1abd9ba`. Integration
into a newly established or owner-designated `develop` remains a human
governance action.

## Recommendation and owner decision

The content is **Recommended for Approval after the two recorded baseline
conditions are resolved or explicitly accepted**. Approval must identify this
manifest hash and separately approve CDR-003 and CDR-006.

- CDR-003 owner decision: Pending
- CDR-006 owner decision: Pending
- Geometry Golden owner decision: Pending
- Reviewer identity/evidence: Pending

Until those decisions exist: `CONDITIONALLY PASS`, Awaiting Repository Owner Approval.
