# 13｜Pre-Implementation Readiness Review

评审日期：2026-09-21。结论：**CONDITIONALLY READY**。

工程基线足以进入Reference/Golden建设与接口合同落实；**尚未达到无条件开始整套Rust物理核心实现的Gate**。这不是对未完成项目的“通过”声明。下面将开始基础Geometry所需条件与后续Irradiance/Engine的阻塞分开，避免把所有发布要求提前变成开始写第一行Rust的条件。

本评审在规格形成后作为独立检查步骤重新核对source、测试、探针、schema、索引与文档一致性；由同一执行者完成，不声称已经获得外部专家评审或项目批准。

## Evidence-based assessment

| 维度 | 结论 | 实际证据 | 仍需完成 |
|---|---|---|---|
| Reference source冻结 | PASS | v1.6.1 / ecbfc863657e239817603a43898ae173c7ccad9c；main HEAD相同；78文件blob一致 | 后续升级只能新revision；不随main更新 |
| Canonical runtime | PASS（限定R0） | CPython3.12.14、29包hash lock、BLAS/GEOS记录；清洁venv全测102通过 | 跨机器/跨平台采样及可选容器digest属于Golden/Hardening，不能宣称已做 |
| Algorithms完整性 | PASS（行为重建） | 60项Inventory；356源码symbol分组；每项源码/输入输出/规则/tests/边界/Rust映射；直接pvlib10函数/50调用点 | 模型修正的目标行为仍受CDR限制；覆盖索引不等于形式化正确性证明 |
| 数学问题 | PASS（reference定义） | E/F/R/sky、Full/Fast、q0/qinc/qabs、AOI近似、零ρ等价系统均明确 | horizon/背面低日高/经验负分量的目标revision待裁决 |
| Upstream ambiguities | PASS（登记） | 26项DEV，全部41issue/PR有triage；递归、skip、零光、AOI alias/地面吸收、静态difference有证据 | CDR-001…007仍为拟议决策，不能假装已签署 |
| Golden策略可执行性 | CONDITIONAL | 67具体case＋6派生家族；schemas；分层字段/axes/单位/治理；可运行研究generator；封装后重跑探针与原JSON/NPZ数组一致 | 全层capture/comparator尚未实现，完整approved corpus尚未生成；不能用seed trace代替 |
| Rust architecture | PASS（边界） | core/python分离，值类型、独立solver adapter、streaming/active-map、错误合同 | 具体crate/features/MSRV在Solver/Binding阶段实证冻结 |
| Python Binding一级能力 | PASS（设计） | Thin layer、ownership/copy/detach、两套public API、wheel平台、abi3决策Gate | 没有构建wheel，不声称NumPy/PyO3版本兼容已验证 |
| Parallel/Adaptive预留 | PASS（设计） | 同kernel、Serial/Outer/候选Inner、资源预算、确定cost model、ExecutionPlan | 当前无Rust benchmark/calibration；Auto性能目标在后续实测，不虚构阈值 |
| Numerical validation | CONDITIONAL | L1–L6定义、独立invariants与错误前提修正、按量分组tolerance标定程序 | 正式阈值未冻结；跨平台/性质/蜕变的Rust测试未运行 |
| Phase Gate阻断能力 | PASS（设计） | 每阶段输入/范围/产物/tests/entry/exit/禁区明确；bug与model差异不能靠宽容差跳过 | 未来按真实日志执行，文档中的Gate不是自动通过 |

## 开始Rust基础Geometry的最小阻塞集合

**B1｜冻结几何输入域与边界语义。**落实CDR-003及CDR-006涉及的子项：地面extent、离地合法性、axis/azimuth一致性、tilt支持域、共线/active阈值与完全包覆差集。推荐修复已证实difference/index bug；参考数值阈值与新scale-aware判定不能同时以含糊“等价”带过。关闭证据是明确选项、解析反例与对应fixtures，不是再写一份泛泛设计。

**B2｜批准Geometry所需Golden子集。**按06采集normalized input、端点/阴影/分区/keys/遮长/ground cuts，并完成同环境复现与独立长度/集合检查，冻结初版geometry/angle/length验收profile。已有上游tests和nominal trace提供种子，但不覆盖所有上述字段/边界。该子Gate可以先于全模型Corpus完成，不要求等到Python wheels或Auto benchmark后才开始Geometry。

这两项完成后可进入P3。接口类型、fixture capture和schema验证现在可继续；本阶段没有被授权要求实现的Rust算法仍不提前生成。

## 开始Irradiance/Full Engine前追加的真实阻塞

- **CDR-001/002：**夜间、z=90°、零光照/矛盾GHI、非有限输入及近正交AOI判定。确保classifier、Perez、planner共享同一政策，不能各自clip。
- **CDR-004：**接受incident-form solve、零ρ连续极限、F/G独立存储和ground absorption修正，并用独立代数/吸收检查形成corrected expectation。
- **CDR-005/007：**正面horizon缺漏、abs(horizon)、背面circ无85°floor、经验分量非负域、Fast Isotropic透射缺项。分别命名模型语义与修正，不用一个“符合Perez”结论代替；已确认bug不默认保留。
- 相应源项、F/G、system/solution的Golden子集与容差初版通过G2/G4/G5。Anoma/Marion全文访问缺口仅在需要引用它们支持新物理修正时构成证据阻塞；不能借此否认已清楚的基础线性几何。

## 不应误列为开始基础实现的阻塞

无需现在选定所有PyO3/NumPy ABI版本、发布全部wheel、实测WASM、实现inner parallel、获得SIMD收益或冻结最终线程比例。它们分别在Binding/Parallel/Adaptive/Release Gate处理。跨平台最终tol与完整V1 DoD是后续发布条件，不是伪装成当前已完成的事项。

## 本阶段完成与未完成的边界

已完成：参考选择与锁定、实际依赖/源码/测试审计、算法和数学规格、已验证缺陷登记、Rust/Python/执行架构、Golden与验证治理设计、阶段Gate、独立readiness检查，以及可重跑的取证附件。

未宣称完成：Rust实现、完整Golden Corpus、最终tolerance、物理修正的项目批准、跨平台Rust/Python验证、wheel发布、parallel/adaptive性能校准。不会将这些未来产物标成PASS，也不会因为研究投入较大就改判READY。
