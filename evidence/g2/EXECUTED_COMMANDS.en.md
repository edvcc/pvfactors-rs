# G2 Executed Command Evidence

Date: 2026-09-21. Commands ran on
`research/g2-geometry-acceptance`; no command merged a branch. Branch pushes
serve PR validation only.

| Purpose | Command (material arguments preserved) | Result / evidence |
|---|---|---|
| Fetch refs | `git fetch --all --prune` | Completed; only `origin/master` was present |
| ZIP identity | `shasum -a 256 Solarfactors_Phase0_1_Baseline.zip` | `2aca31b4...f5729` |
| ZIP internal integrity | `shasum -a 256 -c SHA256SUMS` inside extracted ZIP | 121/121 OK; `zip-integrity.json` |
| Work branch | `git switch -c research/g2-geometry-acceptance` | Created from `bc0b7ec...` |
| Preserved prior environment | isolated macOS arm64 / CPython 3.12.12 run | Manifest, summary, verifier and reproducibility records preserved under `evidence/g2/cross-runtime/` |
| R0 image | `docker build --platform linux/amd64 -f reference/runtime/r0/Dockerfile -t pvfactors-rs-g2-r0:cp31214 .` | Image `sha256:677db45c...45ada3`; R0 exact match, 29/29 packages |
| Case construction | `python reference/tools/build_g2_cases.py` | 39 concrete cases; generator-exact rebuild PASS |
| Canonical candidate pipeline | R0 container: `python3.12 reference/tools/geometry_golden.py pipeline --output /output/geometry-golden-v0.1` | PASS; 39 cases / 117 artifacts; manifest `5afcc7e2...57e3f` |
| R0 reproducibility | R0 container: `python3.12 reference/compare/reproduce_geometry.py --report /output/reproducibility-r0.json` | PASS; two byte-identical generations |
| Cross-runtime compare | `python3 reference/compare/compare_cross_runtime.py old-macos-candidate new-r0-candidate` | PASS; 19,511 exact topology checks; no numerical tolerance failures |
| Upstream tests | `python -m pytest pvfactors/tests -q --junitxml=evidence/g2/upstream-pytest.xml` | 102 passed / 11 warnings; text and XML logs retained |
| Final shared verifier | R0 container: `python3.12 scripts/verify_g2.py --candidate /output/geometry-golden-v0.1` | PASS; source integrity, rebuild, schema, 43 invariants, audit, docs, branch and approved safety |
| Branch safety | verifier uses `origin/master` as authoritative remote ref | PASS; `origin/master` remains `bc0b7ec...` |

The terminal transcript is represented by the generated text/XML/JSON evidence
and exact commands above. R0 and cross-runtime PASS close the runtime condition;
they do not imply owner approval.
