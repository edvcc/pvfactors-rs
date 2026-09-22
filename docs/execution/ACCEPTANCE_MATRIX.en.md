# Project Acceptance Matrix

Status PROPOSED. Machine contract: `acceptance-matrix.json`; CAP scope: V1_COMPLETION_CONTRACT. Required test names below are future obligations to implement and execute, not existing tests. Only Geometry comparison and governance tooling are executable now; missing M4-M13 oracle/profile/adapters return NOT_READY.

| Layer | Input | Authoritative oracle | Comparator | Tolerance | Applicability | Artifacts | Failure interpretation |
|---|---|---|---|---|---|---|---|
| A0 Baseline Integrity | source/G2/P3/locks | Owner base commit + approved manifest | Git blob / SHA256 / exact inventory | exact | all modes | integrity.json | Mutation or missing baseline: stop |
| A1 Environment / Toolchain | toolchain/Python/R0/runner | rust-toolchain + R0 lock + approved platform policy | live versions/metadata/probes | exact version/identity | launch and platform gates | environment.json; command logs | Missing environment: ENVIRONMENT GAP |
| A2 Mathematical Unit / Analytic | small independently constructed inputs | interval lengths; Hottel analytic; Perez coefficients; rational linear system | fieldwise analytic assertions | exact categories; subsystem profile | each mathematical module | named test results + derivation | Implementation bug or conflicting definition |
| A3 Reference Differential | expanded cases + full intermediate trace | frozen R0 raw; approved CDR corrected expectation | case/field/axis comparison, first divergence | geometry v0.1; later independently approved profiles | supported reference domain and CDR scope | case inventory, hashes, diff, nonfinite classification | Ordinary mismatch: debug; oracle conflict: stop |
| A4 Physical / Algebraic Invariants | geometry/F/G/B/q | conservation, reciprocity, matrix identities | domain-aware assertions | exact structure + approved residual/quantity budget | positive active surfaces; sky/G exceptions | invariant reports with prerequisites | Do not assume positivity outside model domain |
| A5 Property / Metamorphic | seeded valid/invalid/boundary families | mirror, fixed-field aggregation, exact input/order laws | shrink, persist seed, relation tests | profile per quantity; exact keys/status | declared valid domains and each relation precondition | seed/run counts, regressions | Failure is feedback; do not assume away hard cases |
| A6 Native E2E | public Rust consumer inputs | approved serial outputs + API contract | external consumer tests and layered diff | output/aggregate profile | Full/Fast/targets/batches/errors | consumer build/test logs, traces | API/behavior failure; no Python runtime workaround |
| A7 Python E2E | installed wheel, NumPy inputs | same-case Native results + ownership contract | field/availability/error parity; alias/GIL probes | tight approved Native parity | all supported Python/NumPy combinations | wheel hash, clean-install log, parity results | maturin develop alone is insufficient |
| A8 Execution Equivalence | serial/parallel/auto/chunk variants | same kernel Serial baseline | original-index fieldwise comparison | execution-equivalence profile; exact model/status | workers 1/2/max, uneven chunks, mixed statuses | plan metadata, traces, cancellation/thread counts | Feedback; never lower mode/cut to pass |
| A9 Performance / Resource | held-out workload, limits, calibration | Owner-approved OD-12 protocol/budgets | isolated repeated release timing, RSS, disk | OD-12 candidate targets; no accuracy relaxation | correctness-frozen workload domain | raw samples, CPU/compiler/backend, fit/holdout error | Slow code is feedback; infeasible contract escalates |
| A10 Packaging / Platform | crates/wheels, OS/interpreter grid | approved platform floor, clean Native/Python consumers | artifact install/link/dependency audits | exact matrix + platform numeric profiles | Linux/macOS dual arch/Windows | package hashes, OS floor smoke, SBOM/notices | Missing platform cannot be waived by another arch |
| A11 Governance / RC | all capability/milestone evidence | Owner-approved completion/execution/CDRs | complete inventory, no unresolved required failures | no implicit waiver | final candidate only | final JSON, review bundle, changelog/provenance | Not master merge or release authority |

## Milestone acceptance

### M3 / P3 — Geometry

| Field | Contract |
|---|---|
| Entry conditions | G2 approved; OD-01 closed |
| Implementation scope | math, geometry |
| Required tests | interval_residual, validation_order, row_partition, ground_coverage, identity_active_map, projection_states, predicate_boundaries, mirror, requested_frame |
| Required evidence | ['A2', 'A3', 'A4', 'A5']; oracle=approved-geometry (APPROVED); tolerance=geometry-tolerance-v0.1; artifacts=run.json, results/, test.log |
| Forbidden scope | View Factor, irradiance, solver, binding |
| CI | PR correctness |
| Auto-advance condition | Automatically advance when all required tests/cases/artifacts actually pass, oracles are approved and no semantic conflict remains. |
| Human-stop condition | Only contract conflict, new physical/input/output decision, oracle/tolerance approval, license or irreplaceable environment blocker. |
### M4 / P4 — View Factor / AOI

| Field | Contract |
|---|---|
| Entry conditions | M3; OD-02/04/07/08 closed; VF oracle approved |
| Implementation scope | viewfactor |
| Required tests | hottel_analytic, reciprocity, sky_closure, obstruction, aoi_constant, aoi_bin_edges, f_g_no_alias, ground_absorption, fast_groups |
| Required evidence | ['A2', 'A3', 'A4', 'A5']; oracle=vf-aoi (PENDING_OWNER_APPROVAL); tolerance=view-factor + aoi-quadrature (pending); artifacts=test-results, case-inventory, oracle-digests, comparison, invariants, environment, command-logs |
| Forbidden scope | Unapproved AOI integration, clipping G to F |
| CI | PR correctness |
| Auto-advance condition | Automatically advance when all required tests/cases/artifacts actually pass, oracles are approved and no semantic conflict remains. |
| Human-stop condition | Only contract conflict, new physical/input/output decision, oracle/tolerance approval, license or irreplaceable environment blocker. |
### M5 / P5 — Irradiance / Perez

| Field | Contract |
|---|---|
| Entry conditions | M3; OD-02/03/05/06/07/08 closed; source oracles approved |
| Implementation scope | irradiance |
| Required tests | spencer_calendar, airmass, perez_coefficients_bins, zero_dhi_limit, hemisphere_no_recursion, front_back_horizon, low_sun, transmission, absorbed_sources, fast_tau |
| Required evidence | ['A2', 'A3', 'A4', 'A5']; oracle=irradiance (PENDING_OWNER_APPROVAL); tolerance=perez-primitives + perez-components (pending); artifacts=test-results, case-inventory, oracle-digests, comparison, invariants, environment, command-logs |
| Forbidden scope | New physical model, full pvlib clone |
| CI | PR correctness |
| Auto-advance condition | Automatically advance when all required tests/cases/artifacts actually pass, oracles are approved and no semantic conflict remains. |
| Human-stop condition | Only contract conflict, new physical/input/output decision, oracle/tolerance approval, license or irreplaceable environment blocker. |
### M6 / P6 — Radiosity / Solver

| Field | Contract |
|---|---|
| Entry conditions | M4/M5; OD-04/08 closed; solver oracle approved |
| Implementation scope | radiosity |
| Required tests | analytic_systems, zero_rho, near_singular, scaled_residual, incident_identity, absorption_identity, sky_boundary, resource_failure |
| Required evidence | ['A2', 'A3', 'A4']; oracle=radiosity (PENDING_OWNER_APPROVAL); tolerance=solver-residual + surface-output (pending); artifacts=test-results, case-inventory, oracle-digests, comparison, invariants, environment, command-logs |
| Forbidden scope | Explicit inverse, unapproved regularization, inner parallel |
| CI | PR correctness |
| Auto-advance condition | Automatically advance when all required tests/cases/artifacts actually pass, oracles are approved and no semantic conflict remains. |
| Human-stop condition | Only contract conflict, new physical/input/output decision, oracle/tolerance approval, license or irreplaceable environment blocker. |
### M7 / P7 — Serial Simulation

| Field | Contract |
|---|---|
| Entry conditions | M3-M6; OD-02/07/08 closed |
| Implementation scope | simulation, execution/serial |
| Required tests | full_hybrid, full_isotropic, fast_targets, fast_availability, broadcast_empty_invalid, zero_night_status, timeseries_order, weighted_fixed_field, ragged_trace, native_consumer |
| Required evidence | ['A3', 'A4', 'A5', 'A6']; oracle=native-e2e (PENDING_OWNER_APPROVAL); tolerance=surface-output + aggregate (pending); artifacts=test-results, case-inventory, oracle-digests, comparison, invariants, environment, command-logs |
| Forbidden scope | Parallel/Auto before serial freeze; hidden Fast fallback |
| CI | PR correctness |
| Auto-advance condition | Automatically advance when all required tests/cases/artifacts actually pass, oracles are approved and no semantic conflict remains. |
| Human-stop condition | Only contract conflict, new physical/input/output decision, oracle/tolerance approval, license or irreplaceable environment blocker. |
### M8 / P8 — Python Binding

| Field | Contract |
|---|---|
| Entry conditions | M7; OD-07/09 closed; binding matrix available |
| Implementation scope | solarfactors-python |
| Required tests | native_python_parity, dtype_shape_strides, owned_copy_alias, gil_detach, exceptions, cancel, wheel_clean_install, core_dependency_isolation |
| Required evidence | ['A6', 'A7', 'A10']; oracle=python-e2e (PENDING_OWNER_APPROVAL); tolerance=native-python output (pending); artifacts=test-results, case-inventory, oracle-digests, comparison, invariants, environment, command-logs |
| Forbidden scope | Python physics, callbacks, unverified zero-copy/abi3 |
| CI | PR correctness |
| Auto-advance condition | Automatically advance when all required tests/cases/artifacts actually pass, oracles are approved and no semantic conflict remains. |
| Human-stop condition | Only contract conflict, new physical/input/output decision, oracle/tolerance approval, license or irreplaceable environment blocker. |
### M9 / P9 — Correctness Hardening

| Field | Contract |
|---|---|
| Entry conditions | M7/M8; OD-08 approvals and platform samples |
| Implementation scope | tests, reference candidates |
| Required tests | all_approved_cases, boundary_properties, metamorphic_preconditions, cross_platform_tolerance, regression_seeds, error_contract |
| Required evidence | ['A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A10']; oracle=correctness (PENDING_OWNER_APPROVAL); tolerance=all subsystem profiles (pending); artifacts=test-results, case-inventory, oracle-digests, comparison, invariants, environment, command-logs |
| Forbidden scope | Optimization hiding numerical debt |
| CI | PR correctness |
| Auto-advance condition | Automatically advance when all required tests/cases/artifacts actually pass, oracles are approved and no semantic conflict remains. |
| Human-stop condition | Only contract conflict, new physical/input/output decision, oracle/tolerance approval, license or irreplaceable environment blocker. |
### M10 / P10 — Explicit Parallel

| Field | Contract |
|---|---|
| Entry conditions | M9 serial correctness freeze |
| Implementation scope | execution/outer |
| Required tests | workers_1_2_max, chunks_1_prime_uneven, mixed_status_order, thread_budget, memory_budget, cancel_error_cleanup, concurrent_python_calls |
| Required evidence | ['A5', 'A6', 'A7', 'A8', 'A9']; oracle=parallel (PENDING_OWNER_APPROVAL); tolerance=execution-equivalence (pending); artifacts=test-results, case-inventory, oracle-digests, comparison, invariants, environment, command-logs |
| Forbidden scope | Second kernel, nested heavy pools, global BLAS mutation |
| CI | nightly/deep |
| Auto-advance condition | Automatically advance when all required tests/cases/artifacts actually pass, oracles are approved and no semantic conflict remains. |
| Human-stop condition | Only contract conflict, new physical/input/output decision, oracle/tolerance approval, license or irreplaceable environment blocker. |
### M11 / P11 — Adaptive Auto

| Field | Contract |
|---|---|
| Entry conditions | M10; OD-12 protocol/targets; calibration |
| Implementation scope | execution/planner |
| Required tests | plan_determinism, cost_profile, calibration_holdout, crossover, uncalibrated_fallback, out_of_domain_fallback, resource_caps, auto_equivalence |
| Required evidence | ['A8', 'A9']; oracle=auto (PENDING_OWNER_APPROVAL); tolerance=execution-equivalence; approved perf budget; artifacts=test-results, case-inventory, oracle-digests, comparison, invariants, environment, command-logs |
| Forbidden scope | LLM planner, Full/Fast switch, unmeasured default inner |
| CI | nightly/deep |
| Auto-advance condition | Automatically advance when all required tests/cases/artifacts actually pass, oracles are approved and no semantic conflict remains. |
| Human-stop condition | Only contract conflict, new physical/input/output decision, oracle/tolerance approval, license or irreplaceable environment blocker. |
### M12 / P12 — Performance

| Field | Contract |
|---|---|
| Entry conditions | M9-M11; isolated benchmark protocol |
| Implementation scope | measured implementation hotspots |
| Required tests | same_model_regression, allocation_memory_curve, benchmark_repetitions, auto_vs_best_feasible, calibration_version |
| Required evidence | ['A3', 'A8', 'A9']; oracle=performance (PENDING_OWNER_APPROVAL); tolerance=unchanged correctness profiles; OD-12 budget; artifacts=test-results, case-inventory, oracle-digests, comparison, invariants, environment, command-logs |
| Forbidden scope | SIMD/GPU/WASM blocker; speedup by lower cut |
| CI | nightly/deep |
| Auto-advance condition | Automatically advance when all required tests/cases/artifacts actually pass, oracles are approved and no semantic conflict remains. |
| Human-stop condition | Only contract conflict, new physical/input/output decision, oracle/tolerance approval, license or irreplaceable environment blocker. |
### M13 / P13 — Release Candidate

| Field | Contract |
|---|---|
| Entry conditions | M3-M12; every CAP01-CAP22; matrix complete |
| Implementation scope | packages, docs, licensing |
| Required tests | rust_package_consumer, all_wheels_clean_install, native_python_execution_matrix, license_provenance, version_consistency, full_capability_inventory, owner_review_bundle |
| Required evidence | ['A0', 'A1', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11']; oracle=release (PENDING_OWNER_APPROVAL); tolerance=all approved profiles; artifacts=test-results, case-inventory, oracle-digests, comparison, invariants, environment, command-logs |
| Forbidden scope | master merge, official tag, publishing |
| CI | release-candidate/full-matrix |
| Auto-advance condition | Automatically advance when all required tests/cases/artifacts actually pass, oracles are approved and no semantic conflict remains. |
| Human-stop condition | Only contract conflict, new physical/input/output decision, oracle/tolerance approval, license or irreplaceable environment blocker. |

## Independent oracle and concrete test obligations

Geometry: OD-01 truth table for complete/left/right/interior/point/touch subtraction; side-length/ground coverage, +/-ULP, four-slot no-direct, requested frame and full mirror. Hottel: opposing parallel unit strips separated by 1 have F=sqrt(2)-1; length reciprocity LiFij=LjFji; sky row is zero, no sky reciprocity. AOI: constant-f hemispheric integral and whole-bin edge cases; neither reciprocity nor G<=F is imposed on G. Solver: B=[[1,-0.2],[-0.3,1]], b=[1,2], q=[70/47,115/47]; B=I implies q=b; separate zero-rho, singular and ill-conditioned systems; residual uses original B,b. Energy: qinc=E+Fq0 and q0=rho*qinc; constant absorption gives qabs=(1-rho)qinc; custom AOI checks Eabs+Gq0.

Perez: equality and +/-ULP at all eight bins, frozen coefficients, leap doy366, DHI=0, grazing, negative empirical components, low sun and approved front-horizon fixtures. Raw Reference and corrected outputs coexist; candidate formulas do not automatically become approved expected values.

Properties: valid draws N1..12/cut1..8/T1..17 plus directed tilt90/120/180, gcr>1, rho0/1, near-ground and bin/predicate boundaries. Mirror transforms sun/normal/extent/row keys together; fixed-field cut additivity does not imply exact equality after rediscretization. Zero albedo removes only ground reflection; Hybrid irradiance scaling is not universally linear.

## Golden and tolerance governance

Run all 55 approved Geometry case IDs read from immutable APPROVAL.json, never use observed output count as denominator. Raw/normalized/corrected each contain 55, totaling 165. Later VF-AOI, irradiance, radiosity/serial and Native/Python/execution expectations, expanded families, comparator and profile require OD-08 approval. Candidates use new directories; approved versions coexist without overwriting old corpora.

Algorithm predicates and acceptance comparators are separate. Topology/key/index/bin/status are exact; each subsystem has independent absolute/relative budgets. AOI whole-bin approximation is separate from roundoff; condition-stratified checks prevent small residual from substituting for forward correctness. Never widen tolerances from current Rust errors. Waivers require Owner, case/field/CDR, rationale, expiry and independent correctness evidence; a whole Must Have cannot be waived. No waivers currently exist.

Final Gate resolves CAP->Milestone->Test->Oracle->Tolerance->Artifact->CI. V1_COMPLETION_CONTRACT lists required implementation, behavior and concrete tests for each CAP; JSON uses the same IDs.
