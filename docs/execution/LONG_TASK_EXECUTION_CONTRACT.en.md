# Long-task Execution Contract

Status: PROPOSED; activate only through OD-10 and Owner launch review. Date: 2026-09-22.

## Authority and endpoint

Owner explicit decisions > approved CDR/Golden/model contracts > approved P3 design and additive signed clarifications > approved V1 completion/acceptance/execution contracts > implementation plan > private code choices. Mathematics is an independent correctness constraint: if formal mathematics, approved CDR and approved Golden cannot all be satisfied, stop and expose the conflict; no hierarchy licenses silently picking a convenient answer. Historical research recommendations and candidate data are not approval. EN/ZH-CN must agree; discrepancy affecting behavior is a stop.

The fixed P3 base is c2bc8572a976279abacbcd1d4f9c460233785bdb; frozen Reference is ecbfc863657e239817603a43898ae173c7ccad9c. Geometry Golden manifest is efd2adf3037740b9788792c9f5be6122fb2e842d72f2ddbe2bb5552abc27141b. Preserve all three. The endpoint is V1 IMPLEMENTATION COMPLETE + RELEASE CANDIDATE READY FOR OWNER ACCEPTANCE. It is not master merge, tag, publication or SemVer1.0.0 approval.

## Autonomous execution policy

After explicit launch, Codex may create/modify implementation files, private modules/helpers/iterators/scratch, add unit/property/metamorphic/regression tests, reorder independent work, refactor internal APIs, update implementation docs/changelog/plan, create recoverable commits, run CI and fix failures without asking at every module. Add necessary dev dependencies with consumer/license/MSRV/features rationale and a lock; normal dependencies must stay within approved module/portability/resource boundaries. P3 normal dependencies remain zero. Later solver/binding choices may be evaluated and locked autonomously without exposing vendor types or adding Python/GEOS/BLAS to core. New license/provenance risk or changed supported-platform obligation is not an ordinary dependency choice.

Follow M3->M4->M5->M6->M7->M8->M9->M10->M11->M12->M13, respecting matrix prerequisites. A passed milestone automatically advances. Do not wait for an Owner 'continue' after ordinary success. Reference candidate approval is a named OD-08 stop, not silent promotion. Missing future adapters must be implemented with their acceptance tests; lack of an adapter is never reason to mark a milestone passed. Adapter plumbing may evolve under approved semantics; changed comparator fields/expected/tolerance requires Owner review and a new contract digest.

## Normal feedback, not human stops

Compilation, rustfmt/Clippy, ordinary unit/differential/property failures, numerical implementation defects, internal API refactors, disappointing performance, transient CI failures and failed first approaches are normal work. Observe -> locate first divergence -> fix -> rerun -> add minimal regression -> continue. Diagnose the earliest diverging layer, not merely final POA. Retry transient infrastructure at most three times with bounded backoff, inspect evidence, and use an existing approved equivalent runner when possible. Exhausted permission/platform availability becomes an environment blocker. Do not relabel an unexplained mismatch a contract conflict before investigating the implementation.

## Mandatory stops

1. Correct implementation cannot satisfy approved mathematics/CDR/Golden together.
2. A new deviation, physical behavior, input domain or public result/error contract is required.
3. Accepted expected values, required cases, exact fields, tolerance or comparator semantics would change.
4. Candidate oracle/tolerance approval is due under OD-08; Agent has no approval authority.
5. Potential license/provenance violation, substantial copied source, missing attribution or incompatible dependency obligation is discovered.
6. Required environment/permissions/platform cannot be provided through an approved path, or resource budget cannot accommodate required work.

At a stop: retain safe work in a checkpoint; record affected contract, minimal counterexample, earliest divergent field, current/expected values, attempted implementation fixes, evidence paths, default recommendation, scope and precise Owner action. Update execution-state.json and the plan, stop dependent implementation, and do not self-approve. Unrelated low-risk diagnostic work is allowed while awaiting input; never implement the unresolved semantics. No private reasoning needs to be recorded.

## Trusted acceptance versus development tests

Codex may change development tests to fix mistakes, but must preserve accepted case inventory, expected values and tolerances. It may not change implementation + accepted expected + tolerance in the same repair and declare success. Original baseline files are checked against the Owner-named Git commit, not just a mutable hash list. New approvals are additive, immutable versioned objects. Changes to acceptance policy need explicit Owner evidence, independent comparator mutation tests and a separately reviewed checkpoint. Owner independently checks the review diff and re-runs the trusted harness from the reviewed preparation/approval commit against candidate outputs; a repository script is not a security boundary against its own privileged editor.

## Git, checkpoints and recovery

Never directly modify/push master/develop/release branches, force-push them, merge master, create official tags or publish. Work on the exact Owner-authorized implementation branch containing both P3 and reviewed readiness ancestry. Feature push/CI and draft PR to develop are permitted only if launch approval includes them; never infer merge rights from write credentials. Preserve user changes; do not hard-reset another session.

Use feat/test/fix/docs/ci/perf scoped commits. Each milestone has a stable passing checkpoint, and long milestones have intermediate recoverable commits. No single giant final commit and no automatic squash; pre-PR cleanup must retain intelligible history. Commit implementation before acceptance runs so receipts bind a clean candidate SHA. Reports may be committed afterward and cite that verified ancestor SHA; do not make a report's own hash recursively depend on itself.

Persistent state: current milestone, last stable commit, verification status with commands/artifact hashes, known failures, approved blockers, next executable action. On restart read AGENTS.md, this contract, EXECUTION_PLAN, execution-state.json and Owner decisions; compare HEAD/branch/dirty state, verify frozen baseline, validate checkpoint and receipts. If dirty changes are from the task, inspect/preserve and resume; unexpected concurrent edits require reconciliation. Re-run only stale/affected checks. Never infer PASS from a progress note. Do not restart completed milestones without changed evidence.

## Provenance, resources and completion

Independent Rust reconstruction, not line-by-line frozen Python translation. No large copied reference bodies or removed notices. Each important module records algorithm provenance, frozen behavior source and independent implementation note; per-line citations are unnecessary. Preserve BSD notices and include required third-party notices/SBOM in packages; license doubts stop rather than being decided by 'rewrite'.

Use OD-12 limits, measured memory, bounded property cases, isolated benchmarks and task-owned cache cleanup. No orchestrator service, database, queue or dashboard. Reference Python is development-only and never a Rust runtime dependency.

Final requires all CAP01-CAP22, all milestones, approved platform/package evidence, actual counts (passed/failed/skipped/waived), performance evidence, CDR/Golden/tolerance/reference versions and Git SHA. Missing Must Have means nonzero FAIL/NOT_READY, never 'mostly complete'. Owner performs independent final acceptance and decides release/version. This preparation task must stop after preparing CODEX_FULL_IMPLEMENTATION_TASK.md.
