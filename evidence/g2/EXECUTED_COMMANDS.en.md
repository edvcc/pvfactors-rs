# G2 Executed Command Evidence

Date: 2026-09-21. Commands ran on
`research/g2-geometry-acceptance`; no command merged or pushed a branch.

| Purpose | Command (material arguments preserved) | Result / evidence |
|---|---|---|
| Fetch refs | `git fetch --all --prune` | Completed; only `origin/master` was present |
| ZIP identity | `shasum -a 256 Solarfactors_Phase0_1_Baseline.zip` | `2aca31b4...f5729` |
| ZIP internal integrity | `shasum -a 256 -c SHA256SUMS` inside extracted ZIP | 121/121 OK; `zip-integrity.json` |
| Work branch | `git switch -c research/g2-geometry-acceptance` | Created from `bc0b7ec...` |
| Reference environment | isolated `uv pip install -r reference/requirements-canonical.txt`; `jsonschema==4.25.1` | 29/29 pinned packages matched; Python patch mismatch recorded |
| Case construction | `python reference/tools/build_g2_cases.py` | 39 concrete cases; generator-exact rebuild PASS |
| Candidate pipeline | `python reference/tools/geometry_golden.py pipeline --output reference/candidate/geometry-golden-v0.1` | PASS; 39 cases / 117 artifacts |
| Reproducibility | `python reference/compare/reproduce_geometry.py --report evidence/g2/reproducibility.json` | PASS; two byte-identical generations |
| Candidate compare | fresh pipeline plus `compare_geometry.py candidate fresh` | PASS; no differences; `candidate-compare.json` |
| Upstream tests | `python -m pytest pvfactors/tests -q --junitxml=evidence/g2/upstream-pytest.xml` | 102 passed / 11 warnings; text and XML logs retained |
| Final shared verifier | `python scripts/verify_g2.py --output evidence/g2/final-verification.json` | PASS for required checks; runtime mismatch reported separately |
| Branch safety | verifier compares branch and `master` / `origin/master` | PASS; both master refs remain `bc0b7ec...` |

The terminal transcript is represented by the generated text/XML/JSON evidence
and exact commands above. Structural PASS does not erase the unavailable
CPython 3.12.14 condition or imply owner approval.
