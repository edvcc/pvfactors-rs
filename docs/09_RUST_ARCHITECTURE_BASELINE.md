# 09｜Rust Architecture Baseline & Solver

本阶段只冻结职责和数据合同方向，不批量生成Rust类型、不给未测库版本虚假背书。默认f64，纯Rust核心，无Python/pvlib/Shapely runtime dependency。

## Workspace 与单向依赖

```
crates/
  solarfactors-core/
    src/{math,geometry,irradiance,viewfactor,radiosity,simulation,execution}/
  solarfactors-python/
reference/       开发用冻结Python环境和fixtures
benches/         Correctness Freeze之后的基准与校准
```

Python PV System → solarfactors-python → solarfactors-core。反向依赖禁止。`solarfactors-cli` 暂不建：研究阶段脚本足够，公开CLI并非V1必须。`solarfactors-reference` 暂不作为Rust发布crate：reference Python工具不应拖入core；如未来fixture parser重复，可建workspace-only test support。禁止把领域设计引入Repository/Aggregate等不相关模式。

## 模块职责与数据流

| module | 拥有的值与职责 | 禁止依赖 |
|---|---|---|
| math | Degree/Radian边界、trig、稳定小原语、数值policy | Python/geometry对象 |
| geometry | Point2/Vec2/Segment2/Interval、ArrayLayout、SurfaceKey、FrameGeometry/ActiveMap、shading | irradiance/solver/threadpool |
| irradiance | ModelConfig、日序、pvlib primitives、SourceTerms/Optics、AOI吸收曲线 | solver/backend矩阵类型 |
| viewfactor | geometric F、absorbed G、Fast组VF、遮挡和积分 | Python callback、solver策略 |
| radiosity | 系统装配、solver adapter、q0/qinc/qabs分解、残差 | simulation对象结构、Python、执行规划 |
| simulation | InputBatch验证、逐步物理pipeline、Mode/TargetSelection、Aggregation、Output/Trace | 特定BLAS类型、进程通信 |
| execution | ProblemProfile、ResourceBudget、Planner、Serial/Outer/候选Inner策略、ExecutionPlan | 改变model、DNI/DHI或Full/Fast语义 |

pipeline：输入规范化/分类 → geometry → irradiance → F → Full solve或Fast estimate → G/qabs（Full）→ aggregation。执行层只为同一纯timestep计算安排资源与结果索引。准备不可变ArrayLayout与ModelConfig，逐worker持有独享Scratch，禁止共享可变矩阵。

## 值与所有权

- `ArrayLayout` 保存排数、尺寸、spacing、extent、每侧cuts；不存随时间变化的Python式surface对象图。
- `SurfaceKey` 使用ground(kind,element,cut_slot)或pv(row,side,segment,illumination)，stable key与临时matrix index分离。active压缩只改映射，不能丢失外部报告的logical身份。
- `InputBatch` 语义为一致长度T的slice/broadcast enum，angle/irradiance单位在API和文档明确。owned/borrowed封装不影响模型；已验证输入可内部安全复用。
- 每timestep `FrameGeometry` 计算可变coords，immutable view供下游；`SourceTerms`区分incident/absorbed，`Optics`区分reflectivity/absorptivity。
- 数组结构以SoA输入、per-frame连续矩阵为首版方向。矩阵owning storage内部统一row-major或column-major，adapter负责转换；最终由实际backend与trace成本选择，外部axes不随backend改变。
- `SimulationResult`按原始时间索引写入typed output；standard summary常驻，full surface/matrix trace按显式TraceLevel输出。一次全量存T×S²不是默认结果。
- 每次simulation拥有自己的ExecutionContext，避免全局可变model、globalBLAS设置与全局threadpool改变其他Python库行为。Rust自定义fAOI函数如开放，合同必须是纯、确定性、Send+Sync且输出有限有界；参数化曲线为首选。不能让有副作用callback破坏执行策略等价。

Rust API草案仅语义示意：`simulate(&ArrayLayout,&InputBatch,&ModelConfig,&SimulationOptions)->Result<SimulationResult,SimulationError>`。Mode::Full与Mode::Fast{target_row,target_segment}明确；ExecutionPolicy::Auto默认但不改Mode；Result携带model_revision/reference_profile/plan和timestep statuses。错误区分InputShape、InvalidGeometry、NonFiniteInput、UnsupportedConfiguration、SingularSystem、NumericalFailure、ResourceLimit；包含stage、timestep、field、surface key等上下文。

## Solver 边界

内部协议：solver接受本库`DenseMatrixView<f64>`、rhs slice和`SolveOptions{parallelism,budget,diagnostics}`，写入solution/scratch并返回`SolveReport{status,scaled_residual,condition_estimate?,backend_id,pivot_info?}`。库专有matrix types不出adapter，不进入geometry/irradiance/public result；所有权与布局可检查，不依靠隐式转置。

首选问题为M08 `B=I−FR`，去掉sky；还可去除已证明不影响系统的零长slots。避免`inverse(A)*b`。带partial pivot的dense LU为默认候选；QR作诊断/显式fallback。ρ接近1时cond变差要给出状态，不能把QR least-squares结果伪装成同一唯一解。解后残差以原B,b计算；factorization缓冲的原矩阵若已覆盖，保留重建方法或按Trace需求copy。

| 方案 | 优点 | 代价/风险 | 本阶段决策 |
|---|---|---|---|
| faer native dense | 运行时维度、LU/QR、显式并行能力、纯Rust路线 | 默认features可能开rayon；layout/scratch和全局parallelism要控制；小矩阵crossover未知 | **优先评估候选**，先串行feature/config，不冻结版本 |
| nalgebra native | 成熟、dynamic dense、LU/QR、小矩阵便捷、纯Rust | 大矩阵与内部并行策略需实测；public API不可泄露DMatrix | 小系统/可移植基准候选 |
| ndarray + LAPACK/BLAS | 与科学计算生态一致，成熟分解 | 外部native依赖、wheel链接、线程与ABI、WASM限制 | V1默认排除，必要时未来可选backend |
| 手写final solver | 可控 | 主元/稳定性/维护成本高，不必要 | 不采用；只写独立小解析测试 |

[faer官方](https://docs.rs/faer/latest/faer/)明确推荐分解后solve而不是inverse；[nalgebra官方分解说明](https://www.nalgebra.rs/docs/user_guide/decompositions_and_lapack/)区分原生与LAPACK路线。网页“latest”只是研究时能力证据，后续采用时须冻结crate版本、features、MSRV、license和Cargo.lock并验证，不能把动态网页当release lock。

## 可移植性与确定性

V1 Linux/macOS/Windows，不将WASM作为已承诺平台。core避免Python与强制BLAS有利于WASM，但threading、target-feature、allocator和faer backend仍需具体验证；未来可提供串行portable backend。默认无fast-math，不假设FMA一致；输出contract按07 tolerance。多时点顺序与固定长度权重归约有确定顺序；solver内部并行作为另一个被记录且验证的执行策略。

## 性能优化顺序

| 顺序 | 变更 | 阶段 | 前置证据 |
|---|---|---|---|
|1|inverse→solve，去sky、ρ零值安全式|V1基础设计|代数等价、zeroρ与残差 |
|2|workspace复用、避免无用clone/零长solve|V1|active映射差分、无跨时点alias |
|3|连续布局、按timestep/chunk streaming|V1|axes与chunk等价、memory模型 |
|4|outer parallel，solver串行|V1|Serial Correctness Freeze、无共享mutation |
|5|chunk/worker标定、Auto计划|V1|目标工作负载benchmark与memory测量 |
|6|inner solver parallel|V1.x候选|大矩阵低T crossover、线程预算 |
|7|结构化块/Schur或sparse机会|V1.x研究|ground-ground0不等于整体解稀疏；消元fill-in和conditioning证明 |
|8|SIMD、专用trig/批量kernel|Future按profile|准确性/平台收益；先证明瓶颈 |
|9|hardware calibration完善|V1基础+V1.x增强|CPU/solver/compiler keyed模型与可解释回退 |

性能Gate不能用降低cut、切Fast、忽略AOI、改变ground extent来假装同模型加速。
