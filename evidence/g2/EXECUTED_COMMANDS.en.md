# G2 Approval Closure — Executed Command Evidence

Date: 2026-09-22. Commands ran on
`research/g2-owner-review-closure`; no command merged a branch or modified
`master`, `develop`, frozen upstream, tolerance values, or Golden payloads.

| Purpose | Command (material arguments preserved) | Result / evidence |
|---|---|---|
| Fetch refs | `git fetch --all --prune` | `origin/develop=ddee1f43...`, `origin/master=bc0b7ec1...` |
| Work branch | `git switch -c research/g2-owner-review-closure origin/develop` | Created from latest integration baseline |
| Minimal migration | `git cherry-pick 5050091 145f4a1 cf2fd83` | New commits `fc86112`, `8033eff`, `76015e1`; no conflict |
| CDR/case freeze | focused Revision 2 generator commit | Generator commit `01549e0...`; 55 concrete cases; explicit DEV-013 decision and corrected-field provenance |
| R0 image | `docker build --platform linux/amd64 -f reference/runtime/r0/Dockerfile -t pvfactors-rs-g2-r0:cp31214 .` | Image `sha256:677db45c...45ada3`; exact R0 match |
| Canonical candidate | R0 container: `python3.12 reference/tools/geometry_golden.py pipeline` | PASS; 55 cases / 165 artifacts; manifest `efd2adf3...141b` |
| Owner approval promotion | exact byte copy of approved candidate plus separate `APPROVAL.json` | PASS; 55 cases / 165 payload artifacts; source and approved manifest SHA `efd2adf3...141b`; 167 source files byte-identical |
| Source/shared verifier | R0 container: `python3.12 scripts/verify_g2.py` | PASS; 78 source blobs, exact case rebuild, candidate and approved schemas, 65 invariant reports, 47 deviation records, 8 document pairs, branch safety, approved governance, candidate/approved identity, and P3 contract |
| R0 reproducibility | R0 container: `python3.12 reference/compare/reproduce_geometry.py` | PASS; two byte-identical full generations |
| macOS comparison corpus | isolated macOS arm64 / CPython 3.12.12 pipeline, twice | PASS; 55/165 each; byte-identical; manifest `adc63fa3...c8cd` |
| Cross-runtime compare | `python3 reference/compare/compare_cross_runtime.py macos-candidate r0-candidate` | PASS; 24,391 exact topology checks; 0 exact/numerical violations |
| Unit/guardrail tests | `python3 -m unittest discover -s scripts/tests -p 'test_*.py' -v` | 19 passed, including predicate-value freeze, three new ±ULP families, DEV-013 nonzero index, canonical runtime, frozen bytes, branch modes, approved identity, and P3 activation |
| Candidate compare | `geometry_golden.py compare checked-in-candidate independent-r0-candidate` | PASS; byte-for-byte identical |

The superseded 39-case and 45-case manifests remain under
`evidence/g2/history/`. The Repository Owner approval dated 2026-09-22 is
recorded separately from the immutable generation manifest. Push, PR status,
and CI result are verified after the commit and reported outside this evidence
snapshot because recording a run for its own commit would create a new commit.
