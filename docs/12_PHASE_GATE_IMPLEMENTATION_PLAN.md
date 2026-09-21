# 12｜Phase & Gate Implementation Plan

各Gate是可审查证据集合，失败禁止把误差带入后续“集成后再说”。阶段可做不依赖未决物理的准备工作，但不能跨Gate宣布数值兼容。Python Binding的配置、轴/错误设计从Specification开始；真正计算入口随Core稳定逐步接入，不等到Release才做包装。

| Phase / Gate | Inputs / Entry criteria | Implementation scope | Artifacts | Tests | Exit criteria | Forbidden premature work |
|---|---|---|---|---|---|---|
| P0 Reference / G0 | 上游仓库/依赖/论文可检索 | 锁source/runtime，核查默认HEAD/tags/issues | 00、source manifests、lock、测试日志 | 上游全测、blob/hash、清洁环境重建 | R0定义完整且可运行，访问缺口登记 | Rust PoC、假定HEAD即最佳 |
| P1 Specification / G1 | G0证据、源码和上游tests | Algorithm Inventory/数学/依赖/边界、architecture/CDR | 01–14，机器索引、case/schema草案 | 源码交叉检查、最小bug probes、独立readiness | 核心算法无隐含项；blocking CDR明确；按模块决定可进入范围 | 批量翻译class、提前最终solver/scheduler |
| P2 Golden / G2 | G0完成，G1合同；blocking CDR关闭或明确模块隔离 | 实现分层capture/normalize/compare、固定case扩展、raw与corrected期望 | approved corpus v1、generator、schemas、reviewdiff | 同环境两次、跨平台抽样、L1/L3独立核对、instrumentation无扰动 | 相关模块有approved fixtures；known failure精确豁免；tolerance初版有依据 | 自动refresh、只留POA、静默修参考源码 |
| P3 Math/Geometry / G3 | G2 geometry子集；CDR002/003/006确定相关边界 | math/values/interval kernel、Ordered/shade/cut/index/active | core geometry模块、API文档、reference映射 | L1/L2/L3长度/阴影、L4、L5mirror/chunk | 受支持域geometry全覆盖，无未解topology/索引差异 | ShapelyAPI克隆、GIS、SIMD |
| P4 View Factor/AOI / G4 | G3；VF golden；CDR004吸收边界/001有效输入 | Hottel/遮挡/互易/sky/Fast组VF、独立F/G与ReferenceMidpoint300 | viewfactor模块、解析benchcases、AOI策略说明 | L1条带/积分、L2矩阵、L3几何界/互易/closure、L5 | F几何与G吸收分别验证，无原位alias；AOI近似误差显式 | 为让G≤F强制clip、未批新积分模型 |
| P5 Irradiance / G5 | primitive/Perez fixtures；CDR001/002/005/007闭合 | minimal pvlib primitives、Isotropic/Hybrid、透射/正背面/源吸收 | irradiance模块、系数及model revision | L1系数/bins/limits、L2分量、L3适用域、L4边界 | source terms无重大未解差异，低太阳/负horizon政策明确 | 重写全pvlib、在binding补算法 |
| P6 Radiosity / G6 | G4/G5接口；已批准零ρ方程 | backend选型小基准、LU adapter、系统装配/solve、分量/qabs | solver实现/锁依赖、残差诊断、native矩阵边界 | L1解析系统、L2、L3residual/energy、ρ0/near1 | solver不泄露vendor types，奇异错误明确，等价与稳健性证实 | 手写大solver、默认inverse、无证据并行backend |
| P7 Simulation Engine / G7 | G3–G6通过；typed输入/输出 | Full/Fast/selection/zero policy/timeseries/weighted aggregation、Serial streaming | Native API、trace/result/status合同 | L6整链、L2逐层、L5cut前提与timechunk | Serial核心全能力可用；shape/index/status稳定 | 任意Python callback、Auto改变模式 |
| P8 Python Binding / G8 | P1边界已定；G7语义稳定；选定PyO3组合 | thin扩展、NumPy ownership、detach、异常、mixed package、wheel CI | Python API/stubs、wheel artifacts、ABI决策记录 | Native/Python同case、并发buffer、非连续输入、平台pip install | 无pvlib/Python算法重复；包可安装；array/GIL安全可证明 | 先冻结abi3、未验证zero-copy、binding重算物理 |
| P9 Correctness Hardening / G9 | G7/G8，完整corpus与CDR集合 | 属性/蜕变/边界、跨平台tol最终冻结、错误诊断 | compatibility report、tolerance v1、regression seeds | L1–L6；Linux/macOS/Windows | 所有Must V1 serial能力通过；无重大未解释数值偏差 | 性能优化掩盖correctness欠债 |
| P10 Explicit Parallel / G10 | G9 serial freeze，worker memory测量 | shared kernel outer parallel、资源预算、索引输出、取消/error传播 | ExplicitParallel与ExecutionPlan基础 | Serial/parallel/chunks/workers等价、memory/error/stress | 数值不变、无oversubscription、资源限制有效 | 未证明双层heavy/全局BLAS改配置 |
| P11 Adaptive Execution / G11 | G10、代表性benchmark workload协议 | deterministic profile/cost model、calibration artifact、Auto/fallback、诊断 | planner、校准数据/版本、plan解释 | 策略选择边界、资源域、equivalence、实测预测误差 | Auto有实测crossover依据，无magic ratio，uncalibrated有保守fallback | LLM规划、未测inner默认开、静默降低精度 |
| P12 Performance / G12 | G9–G11、profile显示瓶颈 | 按09顺序allocation/layout/streaming/chunk优化；必要候选inner实验 | bench reports、memory curves、变更差分 | 原corpus全部回归、稳定bench重复/分位数 | 同模型实测收益，无tolerance越界；memory可预测 | SIMD优先、拿不同cut/FullFast比较当加速 |
| P13 Release / G13 | 所有前置Gate与MustV1 | 版本化API/model/ref/corpus/calibration、文档、平台分发与许可 | crates/wheels、CHANGELOG、SBOM/许可证、release checklist | 干净机器Rust使用与pip安装E2E、平台矩阵 | 下方DoD全部有证据链接；不带未解释重大差异 | benchmark替代correctness、标注未测平台支持 |

## Gate 交接记录格式

每个Gate记录：commit、输入artifact版本/hash、测试命令/环境、passed/failed/waived数量、CDR关联、未解决风险、责任人/审查者、批准日期、允许进入的下一模块。Waiver必须是字段/输入域级并有独立依据，不接受“upstream本来这样”作为所有解释。P2可按模块先批准geometry corpus，但后续Irradiance仍受自己G2/G5约束；不能将部分G2通过写成整个G2完成。

依赖顺序：Reference→Specification→Golden→Geometry→VF/Irradiance→Radiosity→Engine→Binding集成→Hardening→ExplicitParallel→Adaptive→Performance→Release。VF与Irradiance在共同geometry和输入合同稳定后可以工程上分支推进；这不是要求本阶段启动并行实现。

## 最终项目 Definition of Done

以下全部满足才是V1完成，不因本阶段交付文档而勾选：

- Capability Matrix所有Must Have V1实现；未支持功能明确报错，不接受参数后静默忽略。
- Inventory全部核心条目有实现/明确out-of-scope映射，未进入主链的helper地位清楚；无未解释关键算法。
- 冻结Reference与依赖可重建；source/generator/corpus均可追溯；重复生成经批准。
- Approved Golden Corpus全部通过；CDR修正按限定字段验证，raw oracle不可被覆盖。
- L1–L6全部通过，Physical Invariants、proptest、metamorphic与E2E有真实日志。
- 几何、VF、Perez、solver及outputs独立tolerance已跨平台冻结；无重大未解释数值差异。
- 所有Reference deviations有类型、证据、决策、测试和版本影响；confirmedbug不被无说明复制。
- Linux x86_64、macOS arm64/x86_64、Windows x86_64验证完成；最低支持工具链/依赖明确。
- Core无Python/pvlib/GEOS runtime dependency；Native API独立可用。
- Python wheels可直接安装；Python Binding与Native逐字段等价、无重复计算权威。
- Serial/ExplicitParallel/Auto数值等价，资源/线程预算与错误传播符合合同。
- Adaptive Planner有benchmark校准、可解释ExecutionPlan与未校准fallback；不改变物理模式。
- API/model revision/reference revision、许可证与发布材料完整；新模型或bug修正有迁移说明。

## 本阶段终点

本阶段产物是G0/G1证据及G2设计，不是G3–G13实现。13给出真实readiness结论与阻塞集合；不会为了尽早写Rust降低上述Gate。
