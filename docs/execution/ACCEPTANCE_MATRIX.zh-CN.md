# 项目验收矩阵

状态 PROPOSED。机器合同 `acceptance-matrix.json`；顶层 CAP 范围见 V1_COMPLETION_CONTRACT。表中的 required test 名是未来必须实现并实际执行的验收义务，不是已有测试。当前只有 Geometry comparator 与治理 tooling 可执行；M4–M13 的 oracle/profile/adapter 缺失明确返回 NOT_READY。

| Layer | Input | Authoritative oracle | Comparator | Tolerance | Applicability | Artifacts | Failure interpretation |
|---|---|---|---|---|---|---|---|
| A0 基线完整性 | source/G2/P3/locks | Owner base commit + approved manifest | Git blob / SHA256 / exact inventory | exact | all modes | integrity.json | Mutation or missing baseline: stop |
| A1 环境与工具链 | toolchain/Python/R0/runner | rust-toolchain + R0 lock + approved platform policy | live versions/metadata/probes | exact version/identity | launch and platform gates | environment.json; command logs | Missing environment: ENVIRONMENT GAP |
| A2 数学单元与解析 | small independently constructed inputs | interval lengths; Hottel analytic; Perez coefficients; rational linear system | fieldwise analytic assertions | exact categories; subsystem profile | each mathematical module | named test results + derivation | Implementation bug or conflicting definition |
| A3 Reference 差分 | expanded cases + full intermediate trace | frozen R0 raw; approved CDR corrected expectation | case/field/axis comparison, first divergence | geometry v0.1; later independently approved profiles | supported reference domain and CDR scope | case inventory, hashes, diff, nonfinite classification | Ordinary mismatch: debug; oracle conflict: stop |
| A4 物理/代数不变量 | geometry/F/G/B/q | conservation, reciprocity, matrix identities | domain-aware assertions | exact structure + approved residual/quantity budget | positive active surfaces; sky/G exceptions | invariant reports with prerequisites | Do not assume positivity outside model domain |
| A5 性质/蜕变 | seeded valid/invalid/boundary families | mirror, fixed-field aggregation, exact input/order laws | shrink, persist seed, relation tests | profile per quantity; exact keys/status | declared valid domains and each relation precondition | seed/run counts, regressions | Failure is feedback; do not assume away hard cases |
| A6 Native 端到端 | public Rust consumer inputs | approved serial outputs + API contract | external consumer tests and layered diff | output/aggregate profile | Full/Fast/targets/batches/errors | consumer build/test logs, traces | API/behavior failure; no Python runtime workaround |
| A7 Python 端到端 | installed wheel, NumPy inputs | same-case Native results + ownership contract | field/availability/error parity; alias/GIL probes | tight approved Native parity | all supported Python/NumPy combinations | wheel hash, clean-install log, parity results | maturin develop alone is insufficient |
| A8 执行等价 | serial/parallel/auto/chunk variants | same kernel Serial baseline | original-index fieldwise comparison | execution-equivalence profile; exact model/status | workers 1/2/max, uneven chunks, mixed statuses | plan metadata, traces, cancellation/thread counts | Feedback; never lower mode/cut to pass |
| A9 性能与资源 | held-out workload, limits, calibration | Owner-approved OD-12 protocol/budgets | isolated repeated release timing, RSS, disk | OD-12 candidate targets; no accuracy relaxation | correctness-frozen workload domain | raw samples, CPU/compiler/backend, fit/holdout error | Slow code is feedback; infeasible contract escalates |
| A10 打包与平台 | crates/wheels, OS/interpreter grid | approved platform floor, clean Native/Python consumers | artifact install/link/dependency audits | exact matrix + platform numeric profiles | Linux/macOS dual arch/Windows | package hashes, OS floor smoke, SBOM/notices | Missing platform cannot be waived by another arch |
| A11 治理与发布候选 | all capability/milestone evidence | Owner-approved completion/execution/CDRs | complete inventory, no unresolved required failures | no implicit waiver | final candidate only | final JSON, review bundle, changelog/provenance | Not master merge or release authority |

## 逐里程碑验收

### M3 / P3 — Geometry

| Field | Contract |
|---|---|
| Entry conditions | G2 已批准；OD-01 关闭 |
| Implementation scope | math, geometry |
| Required tests | interval_residual, validation_order, row_partition, ground_coverage, identity_active_map, projection_states, predicate_boundaries, mirror, requested_frame |
| Required evidence | ['A2', 'A3', 'A4', 'A5']; oracle=approved-geometry (APPROVED); tolerance=geometry-tolerance-v0.1; artifacts=run.json, results/, test.log |
| Forbidden scope | View Factor, irradiance, solver, binding |
| CI | PR correctness |
| Auto-advance condition | 全部 required tests/cases/artifacts 真实通过、oracle 已批准且无语义冲突后自动进入下一个 Gate。 |
| Human-stop condition | 仅合同冲突、新物理/输入/输出决定、oracle/tolerance 批准、许可证或不可替代环境阻塞。 |
### M4 / P4 — View Factor / AOI

| Field | Contract |
|---|---|
| Entry conditions | M3；OD-02/04/07/08 关闭；VF oracle 已批准 |
| Implementation scope | viewfactor |
| Required tests | hottel_analytic, reciprocity, sky_closure, obstruction, aoi_constant, aoi_bin_edges, f_g_no_alias, ground_absorption, fast_groups |
| Required evidence | ['A2', 'A3', 'A4', 'A5']; oracle=vf-aoi (PENDING_OWNER_APPROVAL); tolerance=view-factor + aoi-quadrature (pending); artifacts=test-results, case-inventory, oracle-digests, comparison, invariants, environment, command-logs |
| Forbidden scope | Unapproved AOI integration, clipping G to F |
| CI | PR correctness |
| Auto-advance condition | 全部 required tests/cases/artifacts 真实通过、oracle 已批准且无语义冲突后自动进入下一个 Gate。 |
| Human-stop condition | 仅合同冲突、新物理/输入/输出决定、oracle/tolerance 批准、许可证或不可替代环境阻塞。 |
### M5 / P5 — Irradiance / Perez

| Field | Contract |
|---|---|
| Entry conditions | M3；OD-02/03/05/06/07/08 关闭；源项 oracle 已批准 |
| Implementation scope | irradiance |
| Required tests | spencer_calendar, airmass, perez_coefficients_bins, zero_dhi_limit, hemisphere_no_recursion, front_back_horizon, low_sun, transmission, absorbed_sources, fast_tau |
| Required evidence | ['A2', 'A3', 'A4', 'A5']; oracle=irradiance (PENDING_OWNER_APPROVAL); tolerance=perez-primitives + perez-components (pending); artifacts=test-results, case-inventory, oracle-digests, comparison, invariants, environment, command-logs |
| Forbidden scope | New physical model, full pvlib clone |
| CI | PR correctness |
| Auto-advance condition | 全部 required tests/cases/artifacts 真实通过、oracle 已批准且无语义冲突后自动进入下一个 Gate。 |
| Human-stop condition | 仅合同冲突、新物理/输入/输出决定、oracle/tolerance 批准、许可证或不可替代环境阻塞。 |
### M6 / P6 — Radiosity / Solver

| Field | Contract |
|---|---|
| Entry conditions | M4/M5；OD-04/08 关闭；solver oracle 已批准 |
| Implementation scope | radiosity |
| Required tests | analytic_systems, zero_rho, near_singular, scaled_residual, incident_identity, absorption_identity, sky_boundary, resource_failure |
| Required evidence | ['A2', 'A3', 'A4']; oracle=radiosity (PENDING_OWNER_APPROVAL); tolerance=solver-residual + surface-output (pending); artifacts=test-results, case-inventory, oracle-digests, comparison, invariants, environment, command-logs |
| Forbidden scope | Explicit inverse, unapproved regularization, inner parallel |
| CI | PR correctness |
| Auto-advance condition | 全部 required tests/cases/artifacts 真实通过、oracle 已批准且无语义冲突后自动进入下一个 Gate。 |
| Human-stop condition | 仅合同冲突、新物理/输入/输出决定、oracle/tolerance 批准、许可证或不可替代环境阻塞。 |
### M7 / P7 — 串行 Simulation

| Field | Contract |
|---|---|
| Entry conditions | M3-M6；OD-02/07/08 关闭 |
| Implementation scope | simulation, execution/serial |
| Required tests | full_hybrid, full_isotropic, fast_targets, fast_availability, broadcast_empty_invalid, zero_night_status, timeseries_order, weighted_fixed_field, ragged_trace, native_consumer |
| Required evidence | ['A3', 'A4', 'A5', 'A6']; oracle=native-e2e (PENDING_OWNER_APPROVAL); tolerance=surface-output + aggregate (pending); artifacts=test-results, case-inventory, oracle-digests, comparison, invariants, environment, command-logs |
| Forbidden scope | Parallel/Auto before serial freeze; hidden Fast fallback |
| CI | PR correctness |
| Auto-advance condition | 全部 required tests/cases/artifacts 真实通过、oracle 已批准且无语义冲突后自动进入下一个 Gate。 |
| Human-stop condition | 仅合同冲突、新物理/输入/输出决定、oracle/tolerance 批准、许可证或不可替代环境阻塞。 |
### M8 / P8 — Python 绑定

| Field | Contract |
|---|---|
| Entry conditions | M7；OD-07/09 关闭；binding 矩阵可用 |
| Implementation scope | solarfactors-python |
| Required tests | native_python_parity, dtype_shape_strides, owned_copy_alias, gil_detach, exceptions, cancel, wheel_clean_install, core_dependency_isolation |
| Required evidence | ['A6', 'A7', 'A10']; oracle=python-e2e (PENDING_OWNER_APPROVAL); tolerance=native-python output (pending); artifacts=test-results, case-inventory, oracle-digests, comparison, invariants, environment, command-logs |
| Forbidden scope | Python physics, callbacks, unverified zero-copy/abi3 |
| CI | PR correctness |
| Auto-advance condition | 全部 required tests/cases/artifacts 真实通过、oracle 已批准且无语义冲突后自动进入下一个 Gate。 |
| Human-stop condition | 仅合同冲突、新物理/输入/输出决定、oracle/tolerance 批准、许可证或不可替代环境阻塞。 |
### M9 / P9 — 正确性强化

| Field | Contract |
|---|---|
| Entry conditions | M7/M8；OD-08 批准与平台采样 |
| Implementation scope | tests, reference candidates |
| Required tests | all_approved_cases, boundary_properties, metamorphic_preconditions, cross_platform_tolerance, regression_seeds, error_contract |
| Required evidence | ['A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A10']; oracle=correctness (PENDING_OWNER_APPROVAL); tolerance=all subsystem profiles (pending); artifacts=test-results, case-inventory, oracle-digests, comparison, invariants, environment, command-logs |
| Forbidden scope | Optimization hiding numerical debt |
| CI | PR correctness |
| Auto-advance condition | 全部 required tests/cases/artifacts 真实通过、oracle 已批准且无语义冲突后自动进入下一个 Gate。 |
| Human-stop condition | 仅合同冲突、新物理/输入/输出决定、oracle/tolerance 批准、许可证或不可替代环境阻塞。 |
### M10 / P10 — 显式并行

| Field | Contract |
|---|---|
| Entry conditions | M9 串行正确性冻结 |
| Implementation scope | execution/outer |
| Required tests | workers_1_2_max, chunks_1_prime_uneven, mixed_status_order, thread_budget, memory_budget, cancel_error_cleanup, concurrent_python_calls |
| Required evidence | ['A5', 'A6', 'A7', 'A8', 'A9']; oracle=parallel (PENDING_OWNER_APPROVAL); tolerance=execution-equivalence (pending); artifacts=test-results, case-inventory, oracle-digests, comparison, invariants, environment, command-logs |
| Forbidden scope | Second kernel, nested heavy pools, global BLAS mutation |
| CI | nightly/deep |
| Auto-advance condition | 全部 required tests/cases/artifacts 真实通过、oracle 已批准且无语义冲突后自动进入下一个 Gate。 |
| Human-stop condition | 仅合同冲突、新物理/输入/输出决定、oracle/tolerance 批准、许可证或不可替代环境阻塞。 |
### M11 / P11 — 自适应 Auto

| Field | Contract |
|---|---|
| Entry conditions | M10；OD-12 协议/目标；校准数据 |
| Implementation scope | execution/planner |
| Required tests | plan_determinism, cost_profile, calibration_holdout, crossover, uncalibrated_fallback, out_of_domain_fallback, resource_caps, auto_equivalence |
| Required evidence | ['A8', 'A9']; oracle=auto (PENDING_OWNER_APPROVAL); tolerance=execution-equivalence; approved perf budget; artifacts=test-results, case-inventory, oracle-digests, comparison, invariants, environment, command-logs |
| Forbidden scope | LLM planner, Full/Fast switch, unmeasured default inner |
| CI | nightly/deep |
| Auto-advance condition | 全部 required tests/cases/artifacts 真实通过、oracle 已批准且无语义冲突后自动进入下一个 Gate。 |
| Human-stop condition | 仅合同冲突、新物理/输入/输出决定、oracle/tolerance 批准、许可证或不可替代环境阻塞。 |
### M12 / P12 — 性能

| Field | Contract |
|---|---|
| Entry conditions | M9-M11；隔离基准协议 |
| Implementation scope | measured implementation hotspots |
| Required tests | same_model_regression, allocation_memory_curve, benchmark_repetitions, auto_vs_best_feasible, calibration_version |
| Required evidence | ['A3', 'A8', 'A9']; oracle=performance (PENDING_OWNER_APPROVAL); tolerance=unchanged correctness profiles; OD-12 budget; artifacts=test-results, case-inventory, oracle-digests, comparison, invariants, environment, command-logs |
| Forbidden scope | SIMD/GPU/WASM blocker; speedup by lower cut |
| CI | nightly/deep |
| Auto-advance condition | 全部 required tests/cases/artifacts 真实通过、oracle 已批准且无语义冲突后自动进入下一个 Gate。 |
| Human-stop condition | 仅合同冲突、新物理/输入/输出决定、oracle/tolerance 批准、许可证或不可替代环境阻塞。 |
### M13 / P13 — 发布候选

| Field | Contract |
|---|---|
| Entry conditions | M3-M12；全部 CAP01-CAP22；平台矩阵完整 |
| Implementation scope | packages, docs, licensing |
| Required tests | rust_package_consumer, all_wheels_clean_install, native_python_execution_matrix, license_provenance, version_consistency, full_capability_inventory, owner_review_bundle |
| Required evidence | ['A0', 'A1', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11']; oracle=release (PENDING_OWNER_APPROVAL); tolerance=all approved profiles; artifacts=test-results, case-inventory, oracle-digests, comparison, invariants, environment, command-logs |
| Forbidden scope | master merge, official tag, publishing |
| CI | release-candidate/full-matrix |
| Auto-advance condition | 全部 required tests/cases/artifacts 真实通过、oracle 已批准且无语义冲突后自动进入下一个 Gate。 |
| Human-stop condition | 仅合同冲突、新物理/输入/输出决定、oracle/tolerance 批准、许可证或不可替代环境阻塞。 |

## 独立 oracle 与测试具体要求

Geometry：OD-01 全覆盖/左右部分覆盖/内切分/点/接触真值表；两侧长度守恒、ground 完整覆盖、±ULP、四槽 no-direct、逐时 index、完整 mirror。Hottel：两相向平行单位条带间距 1，F=sqrt(2)-1；长度互易 LiFij=LjFji；sky row 全零，不检验 sky 互易。AOI：常数 f 半球积分及整格边界；G 不强加互易或 G<=F。Solver：B=[[1,-0.2],[-0.3,1]]，b=[1,2]，q=[70/47,115/47]；B=I 时 q=b；零 rho、奇异及高条件数单独案例；用原 B,b 算 residual。能量：qinc=E+Fq0、q0=rho*qinc；常吸收 qabs=(1-rho)qinc；自定义 AOI 验证 Eabs+Gq0。

Perez：八个 bin 等号和 ±ULP、冻结系数、闰年 doy366、DHI=0、grazing、负经验分量、低太阳及批准 front horizon fixture。原始 Reference 与 corrected 输出并列，不能把公式候选直接标为批准 expected。

性质：合法抽样 N1..12/cut1..8/T1..17 加定向 tilt90/120/180、gcr>1、rho0/1、near-ground、bin/predicate 边界。Mirror 同时变换 sun/normal/extent/row keys；固定场 cut 加权可加不等于重新离散求解严格相等。Zero albedo 只消除 ground reflection；Hybrid 不普遍满足 irradiance同比缩放。

## Golden 与阈值治理

Geometry 55 个 approved case 全部运行；case ID 从不可变 APPROVAL.json 读取，不用实际输出文件数充当分母。当前 raw/normalized/corrected 各 55，总 165。后续 VF-AOI、irradiance、radiosity/serial、Native/Python/执行矩阵的 expected、derived case expansion、comparator、profile 均需 OD-08 批准。候选生成只写新目录；批准时新版本并存，不覆盖旧 corpus。

algorithm predicate 与 acceptance comparator 分离；topology/key/index/bin/status 精确；每个 subsystem 独立绝对+相对预算；AOI 整格近似误差与软件舍入分开；高条件数分层，不用小 residual 代替前向正确性。禁止从当前 Rust error 反向放宽。waiver 必须有 Owner、case/field/CDR、理由、有效期及独立正确性证据；不能 waive 整个 Must Have。当前没有 waiver。

Final Gate 汇总 CAP→Milestone→Test→Oracle→Tolerance→Artifact→CI 的完整链。每条 CAP 的实现、可观察行为和具体测试表见 V1_COMPLETION_CONTRACT；JSON 提供同 ID 映射。
