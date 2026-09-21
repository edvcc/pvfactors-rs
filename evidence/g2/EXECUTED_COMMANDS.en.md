# G2 Owner Review Revision 2 — Executed Command Evidence

Date: 2026-09-22. Commands ran on
`research/g2-owner-review-closure`; no command merged a branch or modified
`master`, `develop`, frozen upstream, tolerance, or `reference/approved`.

| Purpose | Command (material arguments preserved) | Result / evidence |
|---|---|---|
| Fetch refs | `git fetch --all --prune` | `origin/develop=ddee1f43...`, `origin/master=bc0b7ec1...` |
| Work branch | `git switch -c research/g2-owner-review-closure origin/develop` | Created from latest integration baseline |
| Minimal migration | `git cherry-pick 5050091 145f4a1 cf2fd83` | New commits `fc86112`, `8033eff`, `76015e1`; no conflict |
| CDR/case freeze | focused Revision 2 generator commit | Generator commit `01549e0...`; 55 concrete cases; explicit DEV-013 decision and corrected-field provenance |
| R0 image | `docker build --platform linux/amd64 -f reference/runtime/r0/Dockerfile -t pvfactors-rs-g2-r0:cp31214 .` | Image `sha256:677db45c...45ada3`; exact R0 match |
| Canonical candidate | R0 container: `python3.12 reference/tools/geometry_golden.py pipeline` | PASS; 55 cases / 165 artifacts; manifest `efd2adf3...141b` |
| Source/shared verifier | R0 container: `python3.12 scripts/verify_g2.py` | PASS; 78 source blobs, exact case rebuild, schemas, 65 invariant reports, 47 deviation records, 8 document pairs, branch and approved safety |
| R0 reproducibility | R0 container: `python3.12 reference/compare/reproduce_geometry.py` | PASS; two byte-identical full generations |
| macOS comparison corpus | isolated macOS arm64 / CPython 3.12.12 pipeline, twice | PASS; 55/165 each; byte-identical; manifest `adc63fa3...c8cd` |
| Cross-runtime compare | `python3 reference/compare/compare_cross_runtime.py macos-candidate r0-candidate` | PASS; 24,391 exact topology checks; 0 exact/numerical violations |
| Unit/guardrail tests | `python3 -m unittest discover -s scripts/tests -v` | 17 passed, including predicate-value freeze, three new ±ULP families, DEV-013 nonzero index, canonical runtime, frozen bytes, and branch modes |
| Candidate compare | `geometry_golden.py compare checked-in-candidate independent-r0-candidate` | PASS; byte-for-byte identical |
| Remote publication | branch push and new PR to `develop` | Pending at the time this evidence file was committed; final URL/result is reported outside the immutable generation manifest |

The superseded 39-case and 45-case manifests remain under
`evidence/g2/history/`. R0 and cross-runtime PASS do not imply owner approval.
