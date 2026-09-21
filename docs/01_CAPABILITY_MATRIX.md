# 01｜Capability Matrix

本表约束最终 V1，不表示本阶段已经实现。模型 revision、输入域和 CDR 与能力一起版本化。

| ID | 能力 | 级别 | 验收范围/约束 |
|---|---|---|---|
| CAP01 | OrderedPVArray | Must Have V1 | 水平地面、共轴向、等高/等宽/等距直线排，有限排数、无限轴向近似 |
| CAP02 | 专用几何与逐时几何 | Must Have V1 | 点、向量、线段、区间、遮挡分区、确定索引、退化处理 |
| CAP03 | surface cut/discretization | Must Have V1 | 每排正/背面分别配置正整数 cut；加权聚合 |
| CAP04 | ground/direct shading | Must Have V1 | 投影、重叠消除、cut 点、边排行为、零倾角 |
| CAP05 | geometric VF | Must Have V1 | Hottel、邻排、地面、sky、互易性、遮挡 |
| CAP06 | AOI/F_AOI | Must Have V1 | 常数吸收、Rust 原生函数/参数化曲线、NumPy 输入曲线的纯 Rust求值；积分策略命名 |
| CAP07 | IsotropicOrdered | Must Have V1 | Full/Fast 内各自参考语义；总量与分量 |
| CAP08 | HybridPerezOrdered | Must Have V1 | 1990 系数集、direct/isotropic/circumsolar/horizon、正背面 |
| CAP09 | circumsolar shadow | Must Have V1 | 当前主路径的直射分区式遮挡和透光/间隙因子；不伪称已用光盘面积模型 |
| CAP10 | horizon shadow | Must Have V1 | 背面参考行为；正面确认 bug 按 CDR-005 修正并单独验收 |
| CAP11 | albedo / rho / absorption | Must Have V1 | albedo 逐时或标量，rho 正背面；允许零反射率；间隙/透光参数 |
| CAP12 | radiosity | Must Have V1 | 无显式逆、可报告残差、奇异/资源错误；sky 边界 |
| CAP13 | q0/qinc/qabs/分量 | Must Have V1 | Full 全部；Fast 只保证已定义的 qinc/反射分量，q0/qabs 标记 unavailable |
| CAP14 | Full | Must Have V1 | 所有物理表面反射平衡，row/side/segment 聚合 |
| CAP15 | Fast | Must Have V1 | 显式选择某排背面、可选 segment；不是自动降精度档 |
| CAP16 | timeseries | Must Have V1 | 批输入、逐点状态、顺序恢复、可控中间量输出 |
| CAP17 | Rust Native API | Must Have V1 | 纯 Rust；无 Python/pvlib/GEOS runtime |
| CAP18 | Python Binding / wheels | Must Have V1 | PyO3+maturin 候选，thin binding，macOS 双架构/Linux/Windows |
| CAP19 | Serial / Explicit Parallel | Must Have V1 | 同一物理计算；外层 timestep/chunk 并行；可控制资源 |
| CAP20 | Adaptive Auto | Must Have V1 | 确定性 cost model、诊断、benchmark 校准，不切换 Full/Fast |
| CAP21 | finite ground 配置与验证 | Must Have V1 | Reference 范围 [-100,100] 明示；大型阵列显式扩大，禁止静默越界 |
| CAP22 | compatibility/CDR/Golden 管理 | Must Have V1 | 原始 oracle 不修改；修正与 reference 数值分离 |
| CAP23 | Python classes/callback/report API 完整复刻 | Out of Scope V1 | 只提供语义 API；Pandas 用户适配可在外围完成 |
| CAP24 | plotting/GIS/任意二维拓扑 | Out of Scope V1 | 不复制 Matplotlib/Shapely API |
| CAP25 | SAM 数据库、太阳位置/追踪器/天气/电气模型 | Out of Scope V1 | 输入上游 Python 系统提供；支持显式 SAPM B0…B5 即可 |
| CAP26 | 非等高/非等距/坡地/dual tilt/3D 端部效应 | Out of Scope V1 | 必须新模型，不作为普通参数放行 |
| CAP27 | Python 运行时 fAOI callback | Out of Scope V1 | 不在 Rust 并行热路径回调 Python；曲线/系数输入替代 |
| CAP28 | 完整光盘 circumsolar 遮挡 | Candidate V1.x | 原辅助函数不是现行主流程；需独立物理规格与 CDR |
| CAP29 | inner solver parallel | Candidate V1.x | V1 留边界，测得 crossover 后启用 |
| CAP30 | abi3 wheel、free-threaded CPython、PyPy | Candidate V1.x | 逐一核实 NumPy 与 ABI，不预先承诺 |
| CAP31 | 更精确 AOI 积分 / 地面消元 | Candidate V1.x | 用模型 revision/误差对照验证，不静默替换 |
| CAP32 | SIMD/GPU/WASM/稀疏求解/跨机器校准 | Future | WASM 先保持核心依赖可移植，V1 不发包承诺 |

Fast 的 `q0/qabs` 不能通过缺省零值冒充计算结果。若未来增加，需要正式扩展模型，而不是绑定层补算。边界与非有限输入为正式契约，不继承上游“可能能跑”的无验证域。

V1 性能第一目标是内存受控和正确性，不预设固定倍数加速，也不保证每个小任务启用并行。
