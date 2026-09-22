# Environment, CI and Governance

Evidence snapshot: 2026-09-22, preparation branch at approved P3 base. Live API responses: `../../evidence/execution/github-snapshot.json`. This report separates available tools, proposed routes and actual executed checks.

## Actual observations

Rust/cargo 1.98.1, rustfmt/clippy installed; Edition2024/resolver3; cargo locked metadata/build/fmt/Clippy passed. Core contains only crate-level declarations and **zero Rust tests**. No Rust runtime dependencies. Host is macOS arm64; system Python3.14.0 lacked jsonschema. A disposable `/tmp/pvfactors-readiness-venv` installed the existing jsonschema4.25.1 and ran G2/governance checks. It is not R0. No new production dependency was added.

R0 is specified by `reference/runtime/r0/Dockerfile` with pinned Ubuntu OCI digest, CPython3.12.14 archive SHA, 29 wheel hash pins, GEOS3.13.1 and determinism variables. Historical approved environment_id=031158a1d1be8cdb9093 is supported by G2 artifacts. Current Docker CLI exists but daemon socket is absent; current R0 execution is **ENVIRONMENT GAP**. Do not rebuild/refresh Approved Golden. Start an available Docker host and rebuild the existing R0 image if needed, then run the live preflight probe. An alternative CI execution needs dated, reviewed evidence; historical R0 evidence does not prove today's availability. R0's environment ID includes platform/kernel, so equivalent reconstruction with a different ID needs explicit environment review rather than editing the expected ID.

Canonical lock pins packages with hashes; requirements-g2.txt pins jsonschema but its transitive validation dependencies are not hash-locked there. The Dockerfile version-pins validation dependencies. This limits install reproducibility of ordinary PR tooling, not the approved Golden payload integrity. Use a later separately reviewed tooling lock if required; never rewrite the canonical lock to fit this host.

GitHub API: public repository, default master; Actions enabled; self-hosted runner count0 (this does not mean hosted runners unavailable). Existing G2 workflow active; latest queried develop run35654063756 succeeded at fb63a96ef06cc0375fca9dbceb4f59e89e7157a7. Current branch has no new remote readiness run because this preparation has not pushed. master/develop protected=false; both protection APIs return404 'Branch not protected'; parent/repository rulesets=[] and matching branch rules=[]. This is verified absence, not a permission inference.

## Proposed platform contract (OD-09, not yet supported)

| Target | Proposed runner | Package policy / additional evidence |
|---|---|---|
| Linux x86_64 GNU | ubuntu-24.04 | Rust native; wheel manylinux_2_28, clean glibc2.28 container install/audit |
| macOS arm64 | macos-14 | Native arm wheel; deployment11.0; minimum-OS smoke still needed |
| macOS x86_64 | macos-15-intel | Native Intel wheel; deployment10.15; minimum-OS smoke still needed |
| Windows x86_64 MSVC | windows-2022 | Native wheel; proposed Windows10 1809+ floor needs actual smoke |

CPython3.11/3.12/3.13/3.14 ordinary GIL, per-interpreter wheels; NumPy>=2.3.4,<3 candidate support window. Lock lowest/current compatible test versions at adoption. No PyPy/free-threaded/abi3/WASM promise. No local maturin, PyO3 evaluation, wheel, Linux/macOS-Intel/Windows Rust or clean-install evidence exists yet: **ENVIRONMENT GAP**, not PASS. Four hosted labels provide feasible routes but none replaces actual package execution. A disposable binding evaluation may build a non-product probe after launch authority; exact version/features/license and NumPy ownership compatibility are selected from measured results before M8.

Official evidence checked in this task: [GitHub hosted runner reference](https://docs.github.com/en/actions/reference/runners/github-hosted-runners), [PyO3 guide](https://pyo3.rs/main/), [NumPy2.3.4 Python support](https://numpy.org/devdocs/release/2.3.4-notes.html), [maturin distribution](https://www.maturin.rs/distribution.html). These support the proposed route, not a claim that this project has passed it. PyO3 guide illustrates0.29.2 and supports CPython3.9+; project support is intentionally narrower. NumPy2.3.4 supports3.11-3.14. Manylinux/OS floors must also fit chosen dependency wheels.

## Exact repository rule recommendation (OD-11)

Configure two active branch rulesets, `master` and `develop`, targeting `refs/heads/master` and `refs/heads/develop`. Disable deletion and force pushes; require pull requests; no Agent bypass; require all review conversations resolved; require status checks on current PR head. Current real contexts to select after the new workflow runs: `verify` from G2 Geometry Candidate and `assets` from Execution Readiness. Resolve the exact context/app identity from the checks API rather than typing a guessed workflow-name prefix. Require branch up-to-date; use workflow/job stable names. Do not mark preflight as a PR required check: it deliberately fails until Owner launch and is not a preparation asset test.

Master additionally: required human approval (minimum1), dismiss stale approvals, approval after latest push; Owner is the final merge decision-maker. For Owner-authored PRs choose a second human reviewer or a documented Owner-only emergency bypass, never an Agent bypass. Develop: PR+CI mandatory, review baseline/contract changes by Owner. Rules do not alone ensure Agent cannot merge if its token is an admin/bypass identity; use a non-admin automation identity, restrict push targets where possible, exclude release/package publication and organization management scopes, and retain Owner-only release credentials. If technical no-merge restriction is unavailable, record the residual permission risk explicitly.

No repository or organization rule was changed. Optional prepared configuration is this exact checklist, not an applied rule. Owner can instead explicitly accept a bounded residual risk with expiry, credential scope and manual merge control. Refresh API status at launch; acceptance of risk never changes observed protected=false.

## CI tiers

| Tier | Scope and budget | Evidence |
|---|---|---|
| Current PR fast readiness | existing G2 retained; new assets job: frozen integrity, docs/mapping, harness tests, Rust toolchain/fmt/Clippy; <=15min | uploaded JSON/tests/logs; no production PASS claims |
| Future PR correctness | changed-stage analytic/differential/invariants, 256 property seeds/family, serial smoke, Native/Python subset | complete required case counts and first divergence |
| Future nightly deep | 2048 seeds/family, boundary/cross-platform sets, memory/thread stress; bounded workload | seed/shrink record, platform traces, resource samples |
| Future RC matrix | every supported target/interpreter/NumPy boundary, clean wheels/crates, full correctness+execution, license/SBOM, isolated benchmarks | immutable package hashes and all final evidence |

Only the current readiness asset workflow is added now. No fake jobs for unavailable production functions, no automatic release job, no huge per-commit full matrix. Use read-only contents permission, actions checkout without persisted credentials, bounded timeout/concurrency and avoid secrets on untrusted PRs. Scheduled jobs run from the default branch; with master a formal baseline, Owner must decide a safe develop checkout or manual dispatch when integrating nightly workflows. No schedule is installed now.

## Resource and evidence limits

Current free disk observed about51GiB. Proposed OD-12: 10GiB generated/cache cap, keep10GiB free, 4 workers or lower CPU limit, single solver thread, 2GiB/process and8GiB total where enforceable. Use task-local CARGO_TARGET_DIR/Python venv, avoid hidden global mutation, do not delete user caches. G2 corpus is read-only; derived artifacts outside it. Benchmark host isolated from builds/reference capture; record 3 warmups,10 measurements, CPU/compiler/backend, median/p95/RSS. Network/install/tool failures are recorded; unavailable metrics are gaps.

License/provenance: root BSD-3-Clause, upstream solarfactors/SunPower notices and pvlib notices are present. No legal clearance for future copied code is inferred. Module provenance/independent implementation notes plus package notices/SBOM are A11 obligations;Any doubt follows the mandatory stop rule.
