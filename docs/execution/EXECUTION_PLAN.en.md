# Persistent Execution Plan

Status: PREPARATION_ONLY, 2026-09-22. Production implementation has not started.

1. Owner reviews REMAINING_OWNER_DECISIONS and signs exact selected semantics; resolve BF-01/BF-02 without editing frozen history.
2. Close OD-08 oracle/profile objects or explicitly approve candidate-capture stop workflow; approve V1 completion, matrix, execution and platform/resource contracts.
3. Resolve current R0/packaging routes and implement or expressly accept branch-protection/permission risks with dated evidence. Refresh GitHub snapshot at launch.
4. Record approval evidence, readiness commit, allowed implementation branch and contract_sha256 in owner-decisions.json. Verify clean checkout; preflight must genuinely PASS. Preparation asset PASS is not launch permission.
5. Only after explicit launch execute M3-M13 in ACCEPTANCE_MATRIX. Each successful milestone automatically advances; remaining approval/contract stops follow the execution contract.
6. At completion run final verification, provide candidate packages/evidence and independent Owner acceptance instructions. No master merge/tag/release.

## Current state and recovery

Machine progress is `execution-state.json`; it is a small human-readable checkpoint, not a product database. Pending decisions are not 'approved blockers'. On resume validate its commit exists and is an ancestor of HEAD; compare actual branch/dirty state. Inspect the last verification receipt's tested SHA and hashes. Re-run changed checks, preserving user changes. Advance only from evidence, not the state file's status string.

At every stable checkpoint write: current milestone; last completed checkpoint; verification status; known failures; approved blockers; next executable action. Include affected commands, report paths and timestamp in an ordinary implementation progress note (paired languages for formal docs). If interrupted mid-edit, preserve files and mark the action unfinished. Commit before testing acceptance; receipt commits can follow and cite the tested parent.

## Canonical commands

```sh
python scripts/verify_project.py assets --output /tmp/readiness-assets.json
python -m unittest discover -s scripts/tests -v
python scripts/verify_project.py preflight --output /tmp/preflight.json
python scripts/verify_project.py milestone geometry --output /tmp/m3.json
python scripts/verify_project.py final --output /tmp/final.json
```

Use Python >=3.11 with the existing jsonschema==4.25.1 tooling dependency; full Reference generation uses R0 only. `assets` may run during editing; launch/milestone/final require clean worktree. `--scope geometry` is only for an explicitly authorized scoped launch and does not bypass OD-01/10/11, environment or approval. Scope does not grant permission.

M3 current result is NOT_READY because no geometry implementation or acceptance exporter exists. M4-M13 likewise lack approved oracles/adapters; future adapter creation must satisfy HARNESS_CONTRACT and OD-08. None is a completed gate.
