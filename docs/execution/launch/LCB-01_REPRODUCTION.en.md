# LCB-01 reproduction and verification

Research-only. Candidate verification never closes Owner decisions or accepts P4. Read the investigation, DEV-028 and CDR-008 before interpreting results. No Rust/runtime dependency was added; research uses stdlib plus existing R0 NumPy/SciPy. Preserve upstream attribution and licenses. Capture code calls frozen Reference; `independent.py` is derived from the cosine measure and segment geometry, not a translation of Reference VF helpers.

## Cheap local verification

```sh
python scripts/verify_vf_candidate.py reference/candidate/vf-lcb01-v0.1
python -m unittest discover -s scripts/tests -v
python scripts/verify_project.py assets
python scripts/verify_project.py preflight
```

The first three must pass in the documented tool environment (Python≥3.11, existing jsonschema for project/G2 checks). Preflight must remain NOT_READY/exit2 on a clean checkout until Owner closure and the remaining project launch requirements are satisfied. It is not acceptable to flip statuses to manufacture PASS.

## Fresh independent numerical reconstruction

Use the existing `pvfactors-rs-g2-r0:cp31214` image, Linux/amd64, offline; environment ID must equal `031158a1d1be8cdb9093`. Start from the repository root. Choose a new work directory for a new run; do not overwrite accepted candidate files. This example uses ignored work paths:

```sh
mkdir -p reference/work/lcb01-review/candidate reference/work/lcb01-review/evidence
docker run --rm --pull=never --platform linux/amd64 --network=none --read-only --tmpfs /tmp \
  -v "$PWD:/workspace:ro" -v "$PWD/reference/work/lcb01-review:/review" -w /workspace \
  pvfactors-rs-g2-r0:cp31214 python3.12 reference/launch-closure/lcb01/capture.py --output /review/candidate
docker run --rm --pull=never --platform linux/amd64 --network=none --read-only --tmpfs /tmp \
  -v "$PWD:/workspace:ro" -v "$PWD/reference/work/lcb01-review:/review" -w /workspace \
  pvfactors-rs-g2-r0:cp31214 python3.12 reference/launch-closure/lcb01/analyze.py \
  --candidate /review/candidate --evidence /review/evidence
docker run --rm --pull=never --platform linux/amd64 --network=none --read-only --tmpfs /tmp \
  -v "$PWD:/workspace:ro" -v "$PWD/reference/work/lcb01-review:/review" -w /workspace \
  pvfactors-rs-g2-r0:cp31214 python3.12 reference/launch-closure/lcb01/crosscheck.py \
  --candidate /review/candidate --evidence /review/evidence
```

Compare every raw/normalized/corrected JSON object and the 66-case inventory with the committed candidate; JSON key order is immaterial but field values/types are not. Raw bytes must match. Inspect domain-scan, independent-oracle-verification, minimal-counterexample and the positive Fast counterexample. Full scan currently uses 66 fixed cases, at most 11 rows/cut4, single-thread R0 settings and bounded quadrature (`limit=200` per event cell); do not expand a Cartesian product without a research purpose. Committed candidate/evidence total approximately13 MB; generated working copies are ignored and can be removed after receipts are retained.

`package.py` is a preparation-time packager for this named unapproved candidate, not a launch command. It binds raw/normalized/corrected hashes, code hashes and proposed comparator after independent captures. Never use it to silently refresh an Owner-accepted manifest. `--only-new`/`--resume` are incremental research conveniences and retain earlier numeric results; a full clean reconstruction is the reproducibility check. The archived incremental warning metadata differs from full-capture warnings; raw values are identical and the complete receipt is canonical.

Evidence interpretation: Reference bounds FAIL is the defect under investigation. Corrected candidate invariants PASS and mutation tests PASS do not imply Reference compatibility, complete P4 coverage, approved tolerances, a production test run or permission to launch implementation. Independent quadrature estimates are not certified interval error bounds. The official stop remains **LCB-01 — READY FOR OWNER DECISION**.
