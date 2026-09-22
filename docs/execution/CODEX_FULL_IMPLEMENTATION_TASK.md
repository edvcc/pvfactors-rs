# pvfactors-rs — Full V1 Autonomous Implementation Task

任务状态：PREPARED / INACTIVE。此文件只供 Repository Owner 完成 Execution Readiness Review + Remaining Decision Closure 并明确授权启动后使用。看到本文件本身不构成启动指令。

## 项目、输入与权威

仓库：https://github.com/edvcc/pvfactors-rs.git 。项目 edvcc/pvfactors-rs，产品核心 solarfactors-core。已批准 P3 base commit：c2bc8572a976279abacbcd1d4f9c460233785bdb；冻结 Reference v1.6.1：ecbfc863657e239817603a43898ae173c7ccad9c；Geometry Golden manifest SHA256：efd2adf3037740b9788792c9f5be6122fb2e842d72f2ddbe2bb5552abc27141b；geometry-tolerance-v0.1 冻结；R0 environment_id=031158a1d1be8cdb9093。Rust/cargo1.98.1、Edition2024、resolver3。

必要外部输入：Owner 签署的准确剩余决策、启动批准证据、审阅 readiness commit、contract_sha256、implementation branch、允许的 feature push/CI/draft PR 权限、平台/资源合同，以及可用 R0/CI 环境。均在 docs/execution/owner-decisions.json 及其引用的独立审阅记录中绑定。不允许 Agent 自己填 APPROVED。没有这些输入就报告 NOT_READY 并停止，不执行算法。

进入仓库后读取 AGENTS.md，完整 docs/00_REFERENCE_BASELINE.md 至 docs/14_EVIDENCE_AND_TRACEABILITY.md，全部 docs/g2/、docs/p3/，以及以下 docs/execution/ 权威文件（EN/ZH-CN 对照）：V1_COMPLETION_CONTRACT、REMAINING_OWNER_DECISIONS、CONTRACT_EXECUTABILITY_AUDIT、ACCEPTANCE_MATRIX、LONG_TASK_EXECUTION_CONTRACT、ENVIRONMENT_CI_AND_GOVERNANCE、HARNESS_CONTRACT、EXECUTION_PLAN，及 acceptance-matrix.json、contract-audit.json、execution-state.json、baseline-lock.json。推荐方案只有被 Owner 明确采纳后才是决定；冻结文件不被新任务静默覆盖。

## 目标与边界

完成 docs/01_CAPABILITY_MATRIX.md 中全部 CAP01–CAP22，交付 **V1 IMPLEMENTATION COMPLETE + RELEASE CANDIDATE READY FOR OWNER ACCEPTANCE**。Full/Fast、Rust Native/Python binding、timeseries、Serial/ExplicitParallel/Adaptive Auto、finite ground、CDR/Golden 治理均属 V1。CAP23–CAP32 保持原 Out of Scope/Candidate/Future；不把完整 Python API clone、任意2D topology、SIMD/GPU/WASM release 等加入 blocker。

V1 能力完成不等于 SemVer1.0.0。Owner 决定候选版本及最终 merge/tag/release；默认不改0.1.0直至 Owner 选择。不得直接修改或推送 master/develop/release 分支，不自动 merge，不创建正式 tag，不发布 Release/package。终点交付可独立验收的 candidate 及证据。

算法只按批准合同独立重建：Ordered 等高/等宽/等距共轴有限地面；Geometry 遵守批准 P3 public values/build_frame/验证顺序/FrameTopology/SurfaceKey/ReferenceIndex/ActiveIndex 及谓词；IntervalDifference 必须使用 OD-01 批准的完整语义。no-direct 不能私自补 PV slots，Simulation 按 OD-02 处理。View Factor Hottel/sky/reciprocity；独立 F/G 与 ReferenceMidpoint300；Isotropic/HybridPerez 的系数、分箱、abs horizon/背面低日高与正面修正按签署 CDR；incident-form solve/零rho/吸收按 CDR-004；Fast transmission 按 CDR-007，q0/qabs unavailable。Auto 只改变执行方式，不能切 Full/Fast、改 cut/ground/AOI 或降低精度。core 不依赖 Python/pvlib/Shapely/GEOS runtime，binding 不重算物理。

## 启动验证

先 git fetch origin；核对 git status、HEAD、分支和授权 ancestry。工作区必须 clean；在 Owner 指定 implementation branch 开始，该分支应同时包含批准 P3 与审阅准备/决策 commit。保留用户修改，禁止 reset/squash 丢失历史。先运行：

    python scripts/verify_project.py assets --output /tmp/assets.json
    python -m unittest discover -s scripts/tests -v
    python scripts/verify_project.py preflight --output /tmp/preflight.json

使用 Python>=3.11、现有 jsonschema4.25.1。Reference capture 只使用 R0；preflight 必须真实 PASS，不能仅通过 assets。R0 或目标 CI 不可用、批准缺失、合同 hash 不匹配、branch risk 未关闭时停止并报告准确缺口。新版本环境审查必须明确，不修改冻结 expected ID 来通过。

## 自主执行主链

按 ACCEPTANCE_MATRIX 的入口、范围、测试、evidence、禁区执行：
M3 Geometry -> M4 View Factor/AOI -> M5 Irradiance/Perez -> M6 Radiosity/Solver -> M7 Serial Simulation -> M8 Python Binding -> M9 Correctness Hardening -> M10 Explicit Parallel -> M11 Adaptive Auto -> M12 Performance -> M13 Release Candidate。

每阶段调用统一入口，例如：

    python scripts/verify_project.py milestone geometry --output /tmp/m3.json

后续 slug 为 viewfactor、irradiance、radiosity、serial、python、hardening、parallel、auto、performance、release-candidate。普通 milestone 通过后立即自动推进，不逐模块等待人工确认。需要新 adapter 时依据 HARNESS_CONTRACT 实现真实命令、完整 test/case inventory、comparator、自检和有类型证据校验；缺实现、缺案例、缺 comparator、缺 oracle、0 tests run 不得 PASS。当前准备版本的 M4–M13 adapter 缺失是已知状态，需在获批 oracle 合同内补齐，不能把 NOT_READY guard 改成固定成功。

后续 Golden 如已预批准，则只读消费；若 Owner 选择长任务内 capture-stop 路径，可在冻结 Reference 之外实现 capture/normalize、独立验证、双次复现，输出 candidate 和完整 diff，然后在晋升前停止供 Owner 批准准确 manifest/case/profile。不得将 candidate 自升 approved，不用 Rust 输出造 expected，不修改 frozen upstream，不覆写旧 Golden。修改 comparator semantics、exact field、tolerance 或删 required case 均触发人工 stop。

## 权限、反馈与停止

已授权范围内自主编辑实现/私有布局/测试/必要 dev dependency/内部重构，评估符合许可/MSRV/平台的普通依赖并锁定（P3 normal dependency仍为零），创建中间 commit，维护计划/文档/changelog，按启动权限执行 feature push/CI及最终向develop draft PR。具体 private helper、scratch、temporary struct、iterator、文件组织和实现顺序无需逐项确认。

compile/Clippy、普通 unit/differential/property、numerical bug、性能不足、内部重构、临时CI与首个方案失败均正常反馈：观察 -> 定位最早分歧 -> 修复 -> 重跑 -> regression -> 继续。不得为通过修复同时改 accepted expected/tolerance，不重跑无关大量测试。性能不达标先实测优化，不自动放宽标准。

必须停止：批准数学/CDR/Golden冲突；新物理/输入域/公开输出语义；new deviation；放宽tolerance/改expected/exact fields/required case；candidate批准停点；许可证/provenance风险；必需平台/权限/资源无批准替代路径。保留checkpoint，记录最小反例、最早分歧、已尝试修复、影响、证据与默认推荐、准确Owner action，不自行合理化。允许不依赖未决语义的诊断，不实施未决行为。

## 验证、资源、Provenance 与恢复

遵守 A0–A11：baseline/environment、独立解析/Reference差分、适用域物理与代数不变量、property/metamorphic、Native/Python E2E、执行等价、performance/resource、platform/package、governance。参考相似不是唯一正确性；zero albedo、cut、mirror、G/AOI、Hybrid scaling 各有前提。高条件数不能用小residual代替前向验证；各subsystem使用批准预算，predicate与comparator分离。

按 OD-09 实际批准的平台/interpreter/NumPy/OS-floor矩阵构建并干净安装，保留package hash、native parity、所有权/GIL、错误/cancel、thread cleanup证据。按 OD-12 限额控制磁盘、内存、worker、property seed、Reference artifact expansion和bench隔离；不要建设数据库/队列/Agent平台。所有测试记录具体命令、环境、SHA、passed/failed/skipped/waived；未执行平台不是PASS。

每个重要算法模块记录algorithm provenance/reference behavior source/independent implementation note；禁止逐行翻译、大段复制与移除attribution。软件重写不自动消除许可义务；发布候选包含third-party notices/SBOM。

按 feat/test/fix/docs/ci/perf 创建可恢复中间commit，每个milestone至少稳定checkpoint，不自动squash成巨大commit。先提交实现再在clean SHA验收，报告后续commit引用该被测SHA。持续更新execution-state.json：current milestone、last completed checkpoint、verification status、known failures、approved blockers、next executable action。中断后读仓库状态与receipt恢复，只重跑受影响检查，不记录private reasoning，不把进度笔记当PASS。

## 完成交付与独立验收

最后执行：

    python scripts/verify_project.py final --output /tmp/final.json

Final 必须完整验证所有 CAP01–CAP22/M3–M13、平台/包、性能/资源、provenance与版本，汇总Implemented/Excluded、tests run/passed/failed/skipped/waived、platforms/packages、Golden/tolerance/CDR/reference、Git commit。缺任何Must Have必须非零FAIL/NOT_READY，不能mostly complete成功退出。

交付：完整代码与双语正式文档、可读commit历史、所有已批准manifest/profile/decision追溯、完整最终JSON及原始验证artifact、crates/wheels hash和干净安装证据、benchmark/calibration、license/SBOM/changelog、Owner独立重跑说明、按授权向develop的reviewable candidate/draft PR。Owner应使用审阅过的可信harness/合同commit独立验收，而不是信任Agent可改的pass字符串。

达到候选交付终点后停止。最终Owner决定acceptance、version、master merge、正式tag、release；本任务绝不替代这些决定。
