# G2 Owner Review Revision 1 — Executed Command Evidence

Date: 2026-09-22. Commands ran on
`research/g2-owner-review-closure`; no command merged a branch or modified
`master`, `develop`, frozen upstream, tolerance, or `reference/approved`.

| Purpose | Command (material arguments preserved) | Result / evidence |
|---|---|---|
| Fetch refs | `git fetch --all --prune` | `origin/develop=ddee1f43...`, `origin/master=bc0b7ec1...` |
| Work branch | `git switch -c research/g2-owner-review-closure origin/develop` | Created from latest integration baseline |
| Minimal migration | `git cherry-pick 5050091 145f4a1 cf2fd83` | New commits `fc86112`, `8033eff`, `76015e1`; no conflict |
| CDR/case freeze | two focused generator commits | Final generator commit `75b31ff0...`; 45 concrete cases; complete corrected-field provenance |
| R0 image | `docker build --platform linux/amd64 -f reference/runtime/r0/Dockerfile -t pvfactors-rs-g2-r0:cp31214 .` | Image `sha256:677db45c...45ada3`; exact R0 match |
| Canonical candidate | R0 container: `python3.12 reference/tools/geometry_golden.py pipeline` | PASS; 45 cases / 135 artifacts; manifest `d8052625...1417` |
| Source/shared verifier | R0 container: `python3.12 scripts/verify_g2.py` | PASS; 78 source blobs, exact case rebuild, schemas, 54 invariant reports, 39 provenance records, 8 document pairs, branch and approved safety |
| R0 reproducibility | R0 container: `python3.12 reference/compare/reproduce_geometry.py` | PASS; two byte-identical full generations |
| macOS comparison corpus | isolated macOS arm64 / CPython 3.12.12 pipeline, twice | PASS; 45/135 each; byte-identical; manifest `9e6d23ab...0c21` |
| Cross-runtime compare | `python3 reference/compare/compare_cross_runtime.py macos-candidate r0-candidate` | PASS; 23,528 exact topology checks; 0 exact/numerical violations |
| Unit/guardrail tests | `python3 -m unittest discover -s scripts/tests -v` | 14 passed, including domain revision, canonical runtime, frozen bytes, and branch modes |
| Candidate compare | `geometry_golden.py compare checked-in-candidate independent-r0-candidate` | PASS; byte-for-byte identical |
| Remote publication | branch push and new PR to `develop` | Pending at the time this evidence file was committed; final URL/result is reported outside the immutable generation manifest |

The superseded 39-case manifest `5afcc7e2...57e3f` remains under
`evidence/g2/history/`. R0 and cross-runtime PASS do not imply owner approval.
