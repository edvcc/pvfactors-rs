# 全量合同可执行性审计

日期 2026-09-22；对 docs/00–14、全部 G2/P3 双语合同、55 案例批准 corpus、tools/compare/schema/runtime、Cargo/workflows/tests、许可证与实际 GitHub 状态进行交叉核查。`CLOSED` 只表示解释/决策关闭，不代表 Rust 已实现或验收通过。机器清单为 `contract-audit.json`。

| ID | Status | Closure / follow-up |
|---|---|---|
| CDR-001 | OWNER_DECISION_REQUIRED | OD-02; Proposed in doc08, never assumed accepted. |
| CDR-002 | OWNER_DECISION_REQUIRED | OD-03; Proposed in doc08, never assumed accepted. |
| CDR-003 | CLOSED | ; Approved G2 policy. |
| CDR-004 | OWNER_DECISION_REQUIRED | OD-04; Proposed in doc08, never assumed accepted. |
| CDR-005 | OWNER_DECISION_REQUIRED | OD-05; Proposed in doc08, never assumed accepted. |
| CDR-006 | CLOSED | OD-01; CDR-006 approved semantics remain intact; additive public IntervalDifference clarification required. |
| CDR-007 | OWNER_DECISION_REQUIRED | OD-06; Proposed in doc08, never assumed accepted. |

## 阻塞发现

BF-01：P3 public IntervalDifference 未定义剩余跨度与严格开端点集合差的区别。OD-01 提供完整推荐、反例及补充批准对象。它不推翻 G2 完整覆盖修正，不能由 Agent 私自选择。

BF-02：no-direct FrameTopology 没有 PV slots，后续 diffuse 非零计算不能直接消费它并承诺 PV 辐照结果。OD-02 推荐前置具名 zero/reject policy，使 Geometry 表示域与 Simulation 计算域分离；如需 twilight 必须新物理设计。该问题阻塞 P5/P7，不回写 P3/G2。

## 边界核对与历史文本差异

Interval 点/端点成员归属可观察，不能以“长度为零”否认公开语义；正长度 shade 与 topology key/active/index 仍精确。FrameTopology 生命周期已在批准补充文件关闭，不再另开决策。P3 first-error 顺序优先于 generator 对非法复合输入的累积错误列表；当前 Golden 非法案例均单一兼容 code/field，后续多重错误用 P3 顺序独立 fixture。错误 message 是诊断文本，不作为可解析合同。

CDR-003 的方位关系文字提到 angle comparison tolerance，而实现证据使用固定 5e-11 degree。生产 predicate 必须单独命名、冻结相同值，不引用可调整的 acceptance profile；以后比较阈值改变不能改变输入域。这是现有语义的实现分离，不改 5e-11 或边界。

G2 Raw/Corrected 双语历史报告写 45 records，而实际批准 manifest/deviation report 为 47；新审计记录准确数字，不修改冻结历史文件。geometry tolerance JSON 保留推荐状态字样，但独立 APPROVAL.json 与 Owner 记录已批准准确 hash；不能仅凭 JSON 单个状态否定或再批准 G2。doc12 的 P3 CDR-002 提法被后来的 Geometry-only CDR-003/P3 Entry 明确限定；CDR-002 仍阻塞 irradiance，不反向阻塞独立几何。

## 60 项算法覆盖

| ID | Algorithm | Status | Decision |
|---|---|---|---|
| MATH-01 | Degree trigonometry | CLOSED | G2/P3 |
| MATH-02 | Rotation convention | CLOSED | G2/P3 |
| MATH-03 | Solar vector | CLOSED | G2/P3 |
| MATH-04 | Tolerance predicates | CLOSED | G2/P3 |
| GEO-01 | Point/Vec/Segment | CLOSED | G2/P3 |
| GEO-02 | PVSurface | CLOSED | G2/P3 |
| GEO-03 | PVSegment | CLOSED | G2/P3 |
| GEO-04 | ShadeCollection | CLOSED | G2/P3 |
| GEO-05 | PVRow & normals | CLOSED | G2/P3 |
| GEO-06 | OrderedPVArray | CLOSED | G2/P3 |
| GEO-07 | Timeseries geometry | CLOSED | G2/P3 |
| GEO-08 | Surface indexing | CLOSED | G2/P3 |
| GEO-09 | PV cut/discretization | CLOSED | G2/P3 |
| GEO-10 | Inter-row direct shading | CLOSED | G2/P3 |
| GEO-11 | Ground shadow projection | CLOSED | G2/P3 |
| GEO-12 | Ground cut projection | CLOSED | G2/P3 |
| GEO-13 | Overlap & complement | CLOSED | G2/P3 |
| GEO-14 | Ground per-cut slots | CLOSED | G2/P3 |
| GEO-15 | Containment | CLOSED | G2/P3 |
| GEO-16 | Collinearity | CLOSED | G2/P3 |
| GEO-17 | Line difference | BLOCKING_CONTRACT_CONFLICT | OD-01 |
| GEO-18 | Projection/intersection | CLOSED | G2/P3 |
| GEO-19 | Cast/cut/merge | CLOSED | G2/P3 |
| GEO-20 | Ground snapshot/degeneracy | CLOSED | G2/P3 |
| VF-01 | Hottel crossed-string | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| VF-02 | PV→PV | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| VF-03 | Obstructed strings | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| VF-04 | PV→Ground | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| VF-05 | Reciprocity / ground→PV | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| VF-06 | Sky / VF matrix | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| VF-07 | AOI quadrature basis | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| VF-08 | AOI wedge / obstruction | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| VF-09 | AOI sky | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| VF-10 | AOI matrix | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| VF-11 | Effective reflectivity | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| VF-12 | Fast grouped VF | OWNER_DECISION_REQUIRED | OD-04,OD-07,OD-08 |
| IRR-01 | Input normalization | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| IRR-02 | Extraterrestrial radiation | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| IRR-03 | Relative airmass | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| IRR-04 | AOI / hemisphere | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| IRR-05 | Perez decomposition | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| IRR-06 | Luminance/back conversion | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| IRR-07 | IsotropicOrdered | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| IRR-08 | HybridPerezOrdered | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| IRR-09 | Transmission/albedo/rho | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| IRR-10 | Horizon band shading | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| IRR-11 | Circumsolar disk/Gaussian | FUTURE / OUT OF SCOPE | G2/P3 |
| IRR-12 | Absorbed source/AOI | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| IRR-13 | SAPM convenience | OWNER_DECISION_REQUIRED | OD-02,OD-03,OD-05,OD-06,OD-07,OD-08 |
| ENG-01 | Transform to surfaces | OWNER_DECISION_REQUIRED | OD-02,OD-04,OD-06,OD-07,OD-08 |
| ENG-02 | Irradiance/rho matrices | OWNER_DECISION_REQUIRED | OD-02,OD-04,OD-06,OD-07,OD-08 |
| ENG-03 | Full radiosity solve | OWNER_DECISION_REQUIRED | OD-02,OD-04,OD-06,OD-07,OD-08 |
| ENG-04 | Incident decomposition | OWNER_DECISION_REQUIRED | OD-02,OD-04,OD-06,OD-07,OD-08 |
| ENG-05 | qabs/surface update | OWNER_DECISION_REQUIRED | OD-02,OD-04,OD-06,OD-07,OD-08 |
| ENG-06 | Fast/row/segment selection | OWNER_DECISION_REQUIRED | OD-02,OD-04,OD-06,OD-07,OD-08 |
| ENG-07 | Weighted aggregation | OWNER_DECISION_REQUIRED | OD-02,OD-04,OD-06,OD-07,OD-08 |
| ENG-08 | Skip/input status | OWNER_DECISION_REQUIRED | OD-02,OD-04,OD-06,OD-07,OD-08 |
| EXEC-01 | Serial execution | IMPLEMENTATION_CHOICE | OD-07,OD-12 |
| EXEC-02 | Multiprocessing split | IMPLEMENTATION_CHOICE | OD-07,OD-12 |
| EXEC-03 | Report merge | IMPLEMENTATION_CHOICE | OD-07,OD-12 |

## 27 项 DEV 覆盖

| ID | Status | Decision / note |
|---|---|---|
| DEV-001 | OWNER_DECISION_REQUIRED | OD-03 |
| DEV-002 | CLOSED | Follow approved G2/P3 and fixed reference; preserve historical observations. |
| DEV-003 | OWNER_DECISION_REQUIRED | OD-02 |
| DEV-004 | CLOSED | Follow approved G2/P3 and fixed reference; preserve historical observations. |
| DEV-005 | OWNER_DECISION_REQUIRED | OD-05 |
| DEV-006 | IMPLEMENTATION_CHOICE | Preserve source evidence and close linked policy before implementing corrected behavior. |
| DEV-007 | OWNER_DECISION_REQUIRED | OD-02 |
| DEV-008 | OWNER_DECISION_REQUIRED | OD-04 |
| DEV-009 | OWNER_DECISION_REQUIRED | OD-04 |
| DEV-010 | OWNER_DECISION_REQUIRED | OD-04 |
| DEV-011 | OWNER_DECISION_REQUIRED | OD-04,OD-08 |
| DEV-012 | OWNER_DECISION_REQUIRED | OD-05 |
| DEV-013 | CLOSED | Follow approved G2/P3 and fixed reference; preserve historical observations. |
| DEV-014 | FUTURE / OUT OF SCOPE | Preserve source evidence and close linked policy before implementing corrected behavior. |
| DEV-015 | OWNER_DECISION_REQUIRED | OD-06 |
| DEV-016 | CLOSED | G2 complete-cover correction closed; public residual endpoint semantics remain BF-01. |
| DEV-017 | OWNER_DECISION_REQUIRED | OD-07 |
| DEV-018 | OWNER_DECISION_REQUIRED | OD-07 |
| DEV-019 | OWNER_DECISION_REQUIRED | OD-05,OD-08 |
| DEV-020 | CLOSED | Follow approved G2/P3 and fixed reference; preserve historical observations. |
| DEV-021 | CLOSED | Follow approved G2/P3 and fixed reference; preserve historical observations. |
| DEV-022 | OWNER_DECISION_REQUIRED | OD-05 |
| DEV-023 | CLOSED | Historical R0/G2 reproducibility closure; current host environment is checked separately. |
| DEV-024 | OWNER_DECISION_REQUIRED | OD-05 |
| DEV-025 | IMPLEMENTATION_CHOICE | Preserve source evidence and close linked policy before implementing corrected behavior. |
| DEV-026 | CLOSED | Follow approved G2/P3 and fixed reference; preserve historical observations. |
| DEV-027 | CLOSED | Follow approved G2/P3 and fixed reference; preserve historical observations. |

## PRE-LONG-TASK DECISIONS

| ID | Required closure |
|---|---|
| OD-01 | IntervalDifference 剩余跨度语义 |
| OD-02 | CDR-001 输入、零光照、地平线与夜间 |
| OD-03 | CDR-002 无递归半球判定 |
| OD-04 | CDR-004 入射求解与吸收 |
| OD-05 | CDR-005 Perez 分项修正 |
| OD-06 | CDR-007 Fast 透射 |
| OD-07 | Native/Python 结果与光学合同 |
| OD-08 | 后续 oracle、阈值及批准停点 |
| OD-09 | 支持平台与 wheel |
| OD-10 | V1 终点与自主执行授权 |
| OD-11 | 分支保护与 Agent 权限 |
| OD-12 | 资源、Auto 与性能验收 |

## AUTHORIZED IMPLEMENTATION CHOICES

| Choice | Boundary |
|---|---|
| 私有 helper、文件拆分、temporary struct | 不改变已批准 public API/错误顺序/计算语义 |
| scratch、allocation、iterator、内部布局 | 内存预算、输出 axes/key、数值合同保持 |
| 测试文件组织、regression case、实现顺序 | 保留全部 required tests/cases，依赖 Gate 不变 |
| 正常依赖评估、solver backend、binding 版本 | 真实消费者、许可/MSRV/features/lock，core 独立；P3 normal dependency 为零 |
| 普通重构、compile/Clippy/测试失败修复 | 不同时改 accepted expected/tolerance 让修复通过 |
