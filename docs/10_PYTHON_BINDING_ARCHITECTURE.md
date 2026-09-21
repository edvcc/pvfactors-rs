# 10｜Python Binding Architecture

## 一级能力与边界

正式V1从第一阶段预留Python包、数组合同、错误模型和wheel CI。推荐PyO3 + maturin构建混合包，底层为`solarfactors-python`扩展调用`solarfactors-core`。包导入名暂建议`solarfactors_rs`，发布前确认名称可用性；不要覆盖冻结参照的`pvfactors`命名空间。本阶段不冻结未经构建验证的PyO3/maturin/rust-numpy具体版本与ABI策略。

Thin layer只做：dtype/shape/broadcast验证与转换、时间标签/日序编码、Rust调用、结果包装、异常映射。geometry/shading/VF/Perez/AOI/radiosity/Full/Fast/serial/parallel/Auto全部在Core。Python侧不得为了兼容回调而重算物理。

## Rust API 与 Python API

| 语义 | Rust public API | Python public API建议 |
|---|---|---|
| 阵列配置 | typed ArrayLayout + validated builder | frozen dataclass/typed config对象，经扩展验证 |
| timeseries | typed slices / Broadcast / owned batch | NumPy float64 `(T,)`，允许标量广播；不自动对齐Pandas索引 |
| 日期 | DayOfYear或明确CalendarInput | datetime/DatetimeIndex转dayofyear与原labels，时区规则明确 |
| model/mode | enums + parameter structs | keyword配置/枚举；Full与Fast显式 |
| execution | ExecutionPolicy + ResourceLimits | execution='auto'/'serial'/'parallel'，可选worker/memory limit |
| 输出 | owned arrays + typed metadata | result对象，ndarray字段+metadata+ExecutionPlan |
| 错误 | SimulationError enum | ValueError/TypeError及包专用NumericalError/ResourceLimitError |

二者语义一致，不要求机械同构。Python result可便于分析，core不依赖dict/Pandas/DataFrame。结果常用轴`qinc[T,N,2]`（front,back），Full可含qabs/q0；Fast只含目标背面，采用显式target轴/keys与availability，不能把未求面填0冒充计算结果。surface trace用`[T,S]`和stable keys；矩阵trace `[T,S,S]`＋sky描述。返回模型revision、input validity/status、单位及plan metadata。

## 数组互操作与所有权

1. 输入接受f64 ndarray与明确可转换array-like；维度仅标量或1D一致T，拒绝意外二维广播。非连续/负stride数组先按声明策略copy；dtype downcast必须显式并测试。不把obj dtype穿入Core。
2. 默认low-copy安全路线：GIL持有时验证并复制到Rust owned输入，之后detach执行。批量边界的一次O(T)copy相对Full solver通常可接受，实际bench后再优化。
3. `PyReadonlyArray`只限制Rust借用，不保证其他Python/C线程不能写相同buffer。[rust-numpy官方安全说明](https://docs.rs/numpy/latest/numpy/borrow/index.html)说明该限制；不能在detach后把任意Python ndarray借用当不可变线程安全内存。
4. 可选zero-copy只用于有可证明生命周期/不可写所有权的缓冲协议；需要单独设计，不以`flags.writeable=False`就宣称排除了其他alias写入。首版不承诺输入零拷贝。
5. 输出Rust Vec/owned ndarray转交NumPy持有，释放由合法capsule/所有权机制负责；尽量零额外copy。不能返回引用worker scratch、栈或已释放Rust buffer。
6. 验证array大小、stride、T×N×fields溢出与memory limit；转换失败不启动长计算。可选择返回必要字段，避免总生成T×S²。

## 日期、光学配置与Python对象

Core不需要pandas。Hybrid依赖Spencer日序：由调用者传合法1…366 dayofyear，或由binding按输入日历/本地时区提取；不能先UTC转换造成当地日期跨日。timestamp保留为输出标签，重复/非单调时间允许作为独立样本但按原序返回；是否要求排序由上层PV系统决定。

fAOI支持constant、SAPM coefficients或规定节点/插值策略的table。将用户曲线数组作为数据交给Rust求值，不在parallel worker回调Python。任意Python函数不作为V1物理计算入口；上层可以预计算曲线数据，但插值/AOI评估与积分在Core执行。必须定义吸收修正与IAM差别；两侧配置齐全。

## GIL 与并行

推荐当前PyO3的`Python::detach`调用方式，在验证/复制后运行Core；旧`allow_threads`命名不能不经版本核对照搬。[PyO3并行指南](https://pyo3.rs/main/parallelism)。detach闭包不访问PyObject、Python callback或NumPy共享可写数据，完成后重新attach包装结果。Core自己根据ExecutionPlan使用threadpool；Python进程外层并发与内部线程需由resource limits控制。

取消/KeyboardInterrupt设计为Core可检查的cooperative token，在chunk边界响应；binding按所选PyO3机制处理signal，不在任意Rust线程调用Python C API。首版可定义取消延迟为一个chunk上界并测试，不宣称强制中断LU。Rust panic不得跨FFI；预计错误全部Result，边界防护转为包异常并保留上下文。

## wheel与版本政策

建议先支持CPython3.10–3.14的普通GIL构建，**以逐版本CI成功为发布条件**，不是本次已经支持。canonical reference Python3.12.14与发布用户Python版本是两条不同轴。PyPy/free-threaded构建V1暂不承诺；明确NumPy支持窗口并在最旧/最新受支持版本验证。

| 平台 | 构建/验收要点 |
|---|---|
| Linux x86_64 manylinux | 选择并记录manylinux baseline，auditwheel审计glibc/动态依赖；无系统Python/pvlib/BLAS要求；干净容器pip install |
| macOS arm64 | 原生arm wheel，MACOSX_DEPLOYMENT_TARGET明确；Apple Silicon实际跑数组/线程/数值测试 |
| macOS x86_64 | 独立x86 wheel及实际runner；universal2只在两slice依赖与测试完成后考虑 |
| Windows x86_64 | MSVC工具链，DLL依赖审计，路径/异常/线程回收测试；不要求用户编译Rust |

[maturin distribution](https://www.maturin.rs/distribution.html)作为wheel/manylinux打包官方依据。建议mixed package放类型提示、轻量配置/结果包装与文档，扩展包含唯一计算入口。sdist可作为开发渠道，但V1 DoD要求wheel直接安装；不能把本地`maturin develop`成功视为分发完成。

## stable ABI / abi3决策

PyO3 abi3可减少CPython版本wheel数量，但限制可用CPython API/优化且有minimum Python floor。NumPy C ABI是**另外一层**，选择abi3不能自动保证所有NumPy版本和free-threaded Python兼容。[PyO3 multiple Python versions](https://pyo3.rs/main/building-and-distribution/multiple-python-versions.html)。

首版推荐per-interpreter wheels作为低歧义基线；abi3进入Binding阶段实验Gate：选定PyO3/rust-numpy版本，确认组合支持、实际最老/新Python与NumPy矩阵、数组所有权/GIL路径及性能全部通过，再决定采用。不要本阶段为了减少wheel数量先冻结abi3。新的abi3t等能力要按当时官方版本实证，不能沿用泛化的“abi3覆盖全部Python”说法。

Binding Gate：对每个平台干净环境安装wheel、无pvlib/solarfactors依赖仍可算；与Native同case逐字段等价；NumPy noncontiguous、readonly、alias并发边界、异常/空batch/大batch及Serial/Parallel/Auto验证；core Cargo依赖图中没有PyO3/numpy/Python链接。
