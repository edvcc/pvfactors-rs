# Acceptance Harness Contract

Status: PROPOSED acceptance interface for Owner review, implemented preparation tooling. Python >=3.11; new code uses only standard library. Existing G2 jsonschema4.25.1 is reused. No production algorithm or Rust runtime dependency is introduced.

## Commands and result semantics

```sh
python scripts/verify_project.py assets --output /tmp/assets.json
python scripts/verify_project.py preflight --output /tmp/preflight.json
python scripts/verify_project.py milestone geometry --output /tmp/geometry.json
python scripts/verify_project.py final --output /tmp/final.json
python -m unittest discover -s scripts/tests -p 'test_verify_project*.py' -v
```

Exit0=PASS, exit1=FAIL (invalid/mutated/malformed/failed evidence), exit2=NOT_READY (missing implementation/approval/oracle/environment). If both failure and incompleteness occur, FAIL takes precedence; the report preserves individual check statuses. `assets` only verifies current preparation inventory, baseline, tools and G2; it does not authorize launch. `preflight` additionally requires clean named work branch, recorded Owner approval bound to the current contract SHA, environment/governance evidence receipts, actual R0 execution and harness self-tests. It can only mean permitted to start, never project complete. Output reports should normally be outside the tracked worktree or in ignored reference/work; writing inside a tracked evidence directory dirties the next launch check.

Original 491 frozen files are Git-blob checked against c2bc8572a976279abacbcd1d4f9c460233785bdb. The lock inventory itself is re-derived from that commit, so changing source and its local manifest together does not pass. Existing verify_g2.py is called unchanged for approved source/cases/schema/invariants/provenance. The project harness does not duplicate G2 policy math. The approved P3 texts and both languages are among protected files. Rust/Cargo version and locked metadata, workspace Edition/resolver, installed components and Python tooling are probed live.

## Geometry executable adapter

`--scope geometry` is limited to scoped preflight or M3 with explicit Owner authorization. M4-M13 and final require full-project approval; the tool rejects attempts to substitute Geometry-only approval for later decisions.

The milestone expects production math/geometry modules and the future test-only target `crates/solarfactors-core/tests/acceptance_geometry.rs`. It executes:

```sh
cargo test --locked -p solarfactors-core --test acceptance_geometry -- --nocapture --test-threads=1
```

The harness supplies an initially empty PVFACTORS_ACCEPTANCE_OUTPUT directory. The Rust test target must actually invoke public/core code for all55 approved cases plus independent required tests named in acceptance-matrix.json. It writes:

- `run.json`: schema_version1, git_commit (tested clean HEAD), producer=`solarfactors-core`, milestone=`M3`.
- `results/<case_id>.json`: exactly55 case IDs from immutable APPROVAL.json; object keys exactly case_id,input,result,nonfinite_mask. Inputs/metadata may be read from fixtures; computational results must come from Rust. No fixture expected/result copying to actual output.
- Harness writes `test.log`, validates named test records and nonzero matching counts, recomputes artifact hashes, and preserves output under ignored `reference/work/acceptance/M3-*` for review/CI upload. A stale receipt alone is never consumed.

The expected projection is `geometry_payload`: remove only result.warnings, result.reference_length_m, result.ground.reference_extent_m (historical reference-only annotations), and result.errors[*].message (P3 §8 non-protocol diagnostic text). All remaining result fields, input, keys, indices, classifications, ordering, active state and nonfinite mask remain required. The actual exporter produces that projected shape. This projection is an explicit Owner-review object; changing its exclusions is an acceptance-policy change. Golden bytes remain unchanged. Trace-only intermediates belong in a test adapter, not the public production API.

Comparison composes the existing Geometry `Comparison` with exact JSON type checks (False cannot impersonate index0). Numbers use frozen quantity-specific geometry-tolerance-v0.1; alpha radians are converted as in the existing comparator. Exact topology fields get no numeric tolerance. Case omission/addition, changed keys/indices/classes, shape/type/nonfinite mismatches and missing artifacts fail. Zero tests/ignored tests/inconsistent summaries fail even when the subprocess exit code is0. Required independent tests cover interval residuals, validation order, partitions/coverage, identity/active maps, projection states, predicates, mirror and requested frame. Geometry result comparison alone does not substitute for those tests.

## Later milestone/final adapters

M4-M13 deliberately have no approved executable binding or oracle. Their matrix already defines scope/tests/oracles/tolerances/artifacts/CI, but future check execution is NOT_READY. This is an honest extension boundary, not PASS placeholders. Before adoption, bundle concrete expanded IDs, independent expected/derivations, reference capture manifests, profile, test commands and comparator mutation tests under OD-08. Then implement the corresponding adapter and typed evidence validator; Owner approves semantic inventory/profile changes and updates the reviewed contract digest. Plumbing without semantic changes is normal implementation work.

Final currently enumerates all11 milestones, all22 required capabilities and10 exclusions, per-target status, packages/performance evidence (empty while absent), counts, CDR/Golden/tolerance/reference and Git SHA. Release evidence remains NOT_READY until real approved validators exist for package hashes/clean-install tests, platform/interpreter/NumPy Cartesian coverage, provenance/version and OD-12 raw benchmark samples. Do not replace this guard with 'files exist' or user-supplied pass=true. Final must rerun local gates and validate remote evidence against exact tested SHA, CI run URL/conclusion, environment identity and downloaded artifact hashes; different platforms cannot substitute. Package/test adapters must expose individual case outcomes, failed/skipped/waived counts and completeness. No implicit waivers are accepted by the initial harness.

## Trust and independent Owner acceptance

A mutable script cannot prove its own author's trustworthiness. Owner pins the reviewed preparation/approval commit and digest, reviews harness/expected/tolerance diffs separately from implementation, and can run that trusted harness in a separate checkout against candidate output artifacts. Actual CI logs and package digests complement local tests. Protected branches/credential restrictions remain OD-11 controls. Fake pass receipts, expected-output copying, removed tests or modified approval evidence violate the execution contract even if an Agent could edit files to evade a check.

`contract_sha256` pins normative documents, matrix, baseline lock, audit, task and entry point, excluding progress, reports, approval status and verification program bytes. Each run separately records exact `verification_tool_sha256` and `verification_self_tests_sha256` values bound to the Git SHA. Adding adapters or fixing plumbing under approved semantics therefore does not require repeated launch approval; semantic changes still need an Owner decision and updated contract digest. Program hashes provide traceability, not proof of unchanged semantics. Before final acceptance, Owner must review tooling diffs against the reviewed commit and independently rerun a trusted version; a modified program's self-reported PASS is not independent acceptance.

Self-tests use temporary synthetic fixtures and the immutable approved payload roundtrip strictly to verify tooling, never to claim Rust compatibility. Required mutations: omitted case, SurfaceKey/ReferenceIndex/ProjectionClass, tolerance10x, allowed delta, manifest/source byte change, missing/empty artifact, zero/ignored/missing tests, mismatched JSON type, unknown comparator and absent implementation. Run all existing G2 tests too. A self-test FAIL blocks launch. Test counts and logs are archived in evidence/execution after execution.

Independent Owner comparison from the trusted reviewed checkout (comparison only, not proof of Rust execution or milestone acceptance):

```sh
python scripts/verify_project.py compare-geometry --actual /absolute/candidate/results --output /tmp/owner-comparison.json
```
