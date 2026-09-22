# 剩余 Owner 集中决策包

日期：2026-09-22。状态：PROPOSED。共 12 个决策对象，2 个合同阻塞发现。所有推荐均未获批准。每项下文给出问题、模块、Reference/独立证据、推荐/替代、兼容/Golden/API/数值影响及验证方式。

| ID | 决策 | Owner 答复 |
|---|---|---|
| OD-01 | IntervalDifference 剩余跨度语义 | PENDING — 批准全文推荐 / 明确替代；附证据 |
| OD-02 | CDR-001 输入、零光照、地平线与夜间 | PENDING — 批准全文推荐 / 明确替代；附证据 |
| OD-03 | CDR-002 无递归半球判定 | PENDING — 批准全文推荐 / 明确替代；附证据 |
| OD-04 | CDR-004 入射求解与吸收 | PENDING — 批准全文推荐 / 明确替代；附证据 |
| OD-05 | CDR-005 Perez 分项修正 | PENDING — 批准全文推荐 / 明确替代；附证据 |
| OD-06 | CDR-007 Fast 透射 | PENDING — 批准全文推荐 / 明确替代；附证据 |
| OD-07 | Native/Python 结果与光学合同 | PENDING — 批准全文推荐 / 明确替代；附证据 |
| OD-08 | 后续 oracle、阈值及批准停点 | PENDING — 批准全文推荐 / 明确替代；附证据 |
| OD-09 | 支持平台与 wheel | PENDING — 批准全文推荐 / 明确替代；附证据 |
| OD-10 | V1 终点与自主执行授权 | PENDING — 批准全文推荐 / 明确替代；附证据 |
| OD-11 | 分支保护与 Agent 权限 | PENDING — 批准全文推荐 / 明确替代；附证据 |
| OD-12 | 资源、Auto 与性能验收 | PENDING — 批准全文推荐 / 明确替代；附证据 |

## OD-01 — IntervalDifference 剩余跨度语义

P3 §5.4 将 Interval 定义为有限闭区间、允许点区间，并公开 IntervalDifference；CDR-006 规定 subtraction，但 Golden 只批准了完整覆盖反例。严格 [0,2]\[1,2]=[0,1) 无法用闭区间准确表示。端点虽然测度为零，却能通过 contains/intersection 观察。因此 BF-01 是公开合同歧义，不是内部实现选择。
推荐：IntervalDifference 定义为扣除正长度重叠后，剩余正长度连通分量的闭包，按位置排序。它是“剩余跨度”，不是严格集合差。无重叠、仅端点接触、减去点区间时，正长度被减区间不变；完整覆盖返回空；点区间作为被减项返回空。math 内不应用 active/snap 阈值，所有数学上正长度片段均返回，再由 Geometry 分类。例如 [0,2] 减 [1,2] -> [0,1]；减 [0.5,1.5] -> [0,0.5],[1.5,2]；减 [1,1] -> [0,2]；[1,1] 减任意区间 -> 空。切分端点可以同时属于两个闭区间表示；边界归属及 touch 分类必须使用独立的相交/predicate 合同，不能用端点重复推导遮挡面积。
替代方案：增加开闭端点标志，保留严格集合差及点残余；这会改变已批准公开值模型，且当前没有正面积消费者需要它。推荐方案保留 Interval 类型及长度行为，但仍须签署补充 P3/CDR-006 语义澄清。旧批准文档保持字节不变；端点、点区间、部分覆盖解析 fixture 另作批准补充，不能刷新 geometry-golden-v0.1。
Owner 答复：批准完整的剩余跨度定义和补充澄清，或选择严格端点拓扑。验证：解析真值表、补集长度、无正长度重叠、反序拒绝、touch 不产生面积。影响 math/geometry 公开 API，不改变原 55 案例数值阈值。

## OD-02 — CDR-001 输入、零光照、地平线与夜间

CDR-001 / DEV-003、007、018 与 BF-02：已批准 no-direct FrameTopology 没有 PV surface key。若把它用于非零散射 Full 计算，就无法产生承诺的 PV 输出，除非发明另一套 surface universe。Geometry 可表示 zenith [0,180] 不等于辐照模型承诺整个范围。
推荐：先验证全部 geometry、shape、dayofyear 以及有限非负 DNI/DHI/GHI；Simulation 默认 ZeroAtOrBelowHorizon 对 z>=90 返回可用字段的零入射/吸收/反射，并标记 HorizonZero/NightZero。另提供显式 RejectAtOrBelowHorizon；两种 no-direct class 都不运行 Perez/solver。必须承认这有意不计算 twilight 散射，即使 DHI>0 也采用零政策。排级结果身份由 layout 提供；ragged trace 中原本不存在的 geometry surface key 继续缺席，不伪造。Full 的零 q0/qinc/qabs 是零政策结果；Fast q0/qabs 仍 unavailable。
z<90 且 DNI=DHI=0、GHI 未提供或为零，返回 ZeroIrradiance。DNI=DHI=0 而 GHI>0 为 ContradictoryIrradiance，在两个零捷径前拒绝。其他白天输入中的显式 GHI 只影响已有 Fast 环境近似，不替代 Full 源项。负值/非有限值报错，不裁剪。空 T 在静态/shape 验证后返回空类型数组；非法时点使请求失败并保留原索引，不静默丢弃。
替代方案：设计并批准 diffuse-only 地平线/夜间物理拓扑与模型，属于更大设计变更。独立依据：零源线性系统零解；Geometry Golden 明确 N=3 只有 4 个逻辑槽。保留 Reference 的负值/NaN raw trace。请批准具名政策、优先级、状态及 twilight 限制；增加 corrected zero/night/GHI、批次状态与 availability 精确验证。

## OD-03 — CDR-002 无递归半球判定

CDR-002 / DEV-001，影响 AOI、Perez 及源项半球。Reference 递归反转朝向；issue6 探针出现 RecursionError。独立恒等式：法向反转使点积变号，无需递归。
推荐：只计算一次裁剪到 [-1,1] 的 mu；mu>delta 为 front，mu<-delta 为 back，其余为 grazing，delta=64*f64::EPSILON，无量纲；两侧共用同一个带符号值。这个候选舍入带与 geometry orientation、验收 tolerance 分离，批准前须取得独立高精度三角函数边界证据。grazing 时两侧 direct/circumsolar 投影均为零，isotropic/horizon 保留。由系数直接计算 Perez 强度，不用 POA 除零几何因子；DHI=0、DNI>0 定义为 direct-only 极限，diffuse/circumsolar/horizon 为零。不递归，不从舍入后的 acos 反推符号。该有限带会有意改变极近 grazing 输出，必须具名登记。
替代：mu 精确符号分类、无带宽、仍一次判定；避免新增带宽，但正交点会受平台符号舍入影响。推荐独立验证的有限带宽。保留 issue6 原失败；corrected 测试覆盖精确正交、±delta 及邻近 f64、法向反转、DHI=0、有限有界结果。Owner 须结合证据批准数值，不能把此建议视为批准。API trace 公开 grazing 状态；不新增运行时依赖。

## OD-04 — CDR-004 入射求解与吸收

CDR-004 / DEV-008、009、010，影响 F/G、光学、radiosity 与 qabs。Reference 的 inverse-rho 在零值失效，自定义 AOI 原位修改 F 且遗漏地面吸收。独立推导：qinc=E+F R qinc；移除已知 sky 后，(I-Fpp Rp)qinc=E+Fps Lsky；q0=R qinc，零 rho 为连续极限。地面吸收率为 1-albedo。
推荐：用 native backend adapter 进行带部分主元 LU 的 incident-form solve；不显式求逆、正则化或静默 least-squares。F/G 独立存储或不可变独立视图；即使 PV 自定义 AOI，仍有 Gground=(1-albedo)Fground。无自定义 AOI 时 Eabs=(1-rho)E、G=(1-rho_receiver)F。自定义曲线是绝对吸收修正，与单独配置的均匀 rho 区分；不能对任意曲线断言 qabs=(1-rho)qinc，而应验证 source-plus-G 公式及地面常吸收恒等式。保留 ReferenceMidpoint300 整格近似，不用 G<=F 裁剪。
接受 [0,1] 的有限 rho/albedo，包括 0/1；奇异是系统结果。用原 B,b 算残差；分母及残差同为零时 eta=0。验收 trace 必须有条件估计；高条件数系统必须满足批准的条件数相关前向预算，或返回 NumericalFailure，不能仅凭小残差宣告成功。残差/条件阈值由 OD-08 证据批准，不猜 backend 默认值。
替代：具名 reference-only profile 保留缺陷，不推荐作为产品。Golden 要求 AOI 前捕获 raw F，1x1/2x2 解析系统、零 rho 极限、自定义地面吸收、奇异/近奇异案例。Owner 批准方程、吸收边界及诊断失败政策；backend、版本、布局可由实现阶段在许可/MSRV/features 验证后决定。

## OD-05 — CDR-005 Perez 分项修正

CDR-005 / DEV-005、012、019、022、024 不能简化为一次二选一。推荐分别批准：(a) 对正背两侧按接收面方向和带符号遮挡仰角修复正面 horizon 遗漏；(b) 在 0<=z<90 保留 abs(P_horizon) 与背面 circumsolar 的 cos(z) 分母，具名为 HybridPerezReference 近似；(c) 保留有限的经验负分量并报告 NegativeEmpiricalComponent，不全面裁剪 F1、sky 或各分量。非负能量检查只在源项/核满足前提时适用。z>=90 由 OD-02 处理，非有限溢出返回 NumericalFailure。
(a) 的完整候选定义：从接收面质心，取该侧法向水平分量所指方向的相邻排；无邻排 h=0。仰角 theta=max(0,atan2(y_neighbor_top-y_centroid,abs(dx)))，单位度；dx=0 仍用 atan2。h=min(1,theta/band)，band 有限且位于 (0,90]，默认 6.5 度。该侧 illuminated/shaded 都应用 H=abs(P_horizon)*(1-h)。精确 flat/180 的水平法向方向无从选择，但 horizon 投影源为零，此 tie 定义 h=0。这是拟议角带软件模型，不宣称论文强制采用该近似。须有独立构造遮挡 fixture、tilt 90/120/180 正背方向检查，并在模型满足对称前提时做同几何 mirror。未合并的 upstream PR 不作为批准真值。
替代：保留正面遗漏（不推荐）；现在改成两侧 cos85 floor 或 signed horizon（需更广验证的新模型 revision）。推荐最小显式修正并命名历史近似，避免未经验证的物理变更扩散。Perez 1990 式(9) 允许带符号 F2，pvlib 使用 cos85；它们证明存在不同选择，不证明经验精度。Anoma/Marion 全文缺口继续保留；独立角度推导可支持本软件合同，不能冒充全面科学验证。Owner 须分别批准 (a)-(c)、model_revision 和正面 corrected 案例，不能用 tolerance 吞掉模型变化。

## OD-06 — CDR-007 Fast 透射

CDR-007 / DEV-015 影响 Isotropic Fast 的邻排 front-shaded 环境辐照。Reference Pps=Piso-Dfront 遗漏透射直射，Hybrid 则补回 tau 项。推荐 Pps=Piso-(1-tau)*Dfront。独立极限：tau=0 与原行为一致，tau=1 恢复 Piso；对 tau 的导数为 Dfront。在非负适用域中，目标增量应为 rho_front*F_target,front_shaded*tau*Dfront>=0。两个 Fast 模型的 Piso 均保留已记录的 isotropic transposition，不因变量名含 Perez 就换模型。Full 仍是另一种多次反射模型。
替代：保留具名 legacy Fast 近似；推荐修复这个局部不一致并版本化偏差。raw 不变；corrected 覆盖 tau=0/0.5/1、rho=0、无邻排、无遮、边/中排及 segment 选择。Owner 批准公式、受影响字段及迁移说明。API availability 仍遵守 CAP13/CAP15；模型修正不归入数值 tolerance。

## OD-07 — Native/Python 结果与光学合同

冻结可观察 API，不冻结每个方法名。推荐 Full 的排/侧 q0、qinc、qabs、具名分量及可选 keyed segment/surface trace；Fast 只返回选定背面的 qinc/isotropic/reflection/source 分量，q0/qabs 明确 unavailable。shape、单位、状态、model revision、target key 精确。变长 surface/matrix trace 保存逐帧 key 与 offsets，不用 ReferenceIndex 跨不同 topology join。geometry 遵守 P3 fail-fast 顺序，随后 shape/irradiance/dayofyear/optics；首个非法原始时点返回具名错误。允许标量广播、T=0；全标量调用定义 T=1；重复/非单调 timestamp 保留；当地 dayofyear 1..366 不先转换 UTC。
AOI：正背面成对配置；只给一侧时拒绝，除非另一侧显式常数。f(theta) 是 [0,1] 有限绝对吸收修正，theta 采用 [0,180] 切线角。表格 knot 严格递增、覆盖 0/180，分段线性插值、不外推；拒绝重复、乱序、非有限和越界输入。SAPM 显式 B0..B5，沿用 clamp [0,1]。rho 必须明确选择 Scalar 或 FromAbsorptionCurve；省略 scalar 时默认 .01/.03，不自动覆盖。允许纯确定性 Send+Sync Rust 函数；排除 Python 运行时 callback。取消 token 在 frame/chunk 边界检查；取消返回具名错误，不返回成功的部分结果。binding 在 detach 前复制到 owned 输入，包括 strided 数组；输出独立拥有内存。首版接受 f64/明确可转换数值数组，拒绝 object/complex 和含糊二维广播。
替代：逐时点部分成功或固定 padded surface universe，均改变结果/错误语义，须另选。Owner 批准字段 availability、shape/time/error/cancellation、光学配置。独立验证 shape/order、所有权与 alias 并发、表格端点插值、固定场加权聚合；core 不依赖 Python runtime。方法命名和私有存储仍可自主决定。

## OD-08 — 后续 oracle、阈值及批准停点

当前只有 Geometry 拥有已批准 Golden 与 tolerance。Phase 0–1 的 nominal-trace.npz、22 探针、67 具体案例及 6 个未展开家族都是研究证据，不是验收数据集。推荐现在批准 A0–A11 架构与具体测试义务；每个后续数值阶段开始前，必须整体批准不可变 oracle/case/schema/comparator/tolerance。优先在 full launch 前关闭并采集 VF-AOI、irradiance、radiosity/serial 包。可选路径：明确批准长任务中的 candidate capture 后 Owner stop；它仍是同一个可恢复任务，但不能承诺全程无人中断。
Candidate 由冻结 R0 生成，记录 source/lock/generator hash、两次一致捕获与独立解析/不变量验证。Rust 输出不能作为 expected。每项修正记录 case+field+CDR+raw+corrected+独立依据。Owner 批准准确 manifest 与全部展开 ID。Agent 可实现 capture/adapter，不能晋升 candidate 或改验收语义。复用 Geometry comparator；新 subsystem comparator 采用前必须完成 mutation self-test。schema/key/bin/status 一律精确。
分别冻结 VF、AOI 软件舍入、Perez primitive/component、residual、surface-output、aggregate、execution-equivalence 预算。阈值来自解析误差与独立跨平台测量，不从 Rust 失败值倒推。按条件数分层前向预算及残差诊断，不能只给全局 epsilon。M9 在并行/性能前批准最终平台校准 profile。Owner 答复选择预批准或停点路线，并提供批准对象 hash；未关闭的新 profile 保持 NOT_READY。这是验收授权停点，不是每个普通模块都询问一次。

## OD-09 — 支持平台与 wheel

推荐 Rust 1.98.1 / Edition 2024；Linux x86_64 GNU、macOS arm64/x86_64、Windows x86_64 MSVC。Python：普通 GIL CPython 3.11–3.14，按 interpreter 构建 wheel；初始 NumPy >=2.3.4,<3，各 interpreter 测试最低及当前锁定 NumPy。由于 NumPy 2.3 要求 3.11，此建议收窄 doc10 尚未批准的 3.10–3.14 建议，不删除已批准 CAP。Linux 使用 manylinux_2_28；macOS deployment target 候选为 arm64 11.0 / x86_64 10.15，须审计依赖 wheel；Windows 用户最低候选为 Windows 10 1809+。现代 runner 成功不能证明最低 OS 兼容，必须补最低环境 VM/真机 smoke，或由 Owner 明确调整支持范围。
官方 hosted label 提供 ubuntu-24.04、macos-14（arm64）、macos-15-intel、windows-2022。仓库 API 证明 Actions 启用及历史 Linux G2 成功，不证明四个平台打包路径均已执行。PyO3 当前文档示例为 0.29.2；绑定采用前在隔离打包评估中选择兼容 PyO3/rust-numpy/maturin 准确版本并锁定。本准备任务不创建 binding 生产代码。PyPy、free-threaded、abi3、universal2、musllinux、Linux/Windows ARM、WASM 分发不作为 V1 blocker。
替代：保留 CPython3.10 需要旧 NumPy 支持分支及额外矩阵成本，仅在实际用户需求下选择。Owner 批准平台/interpreter/OS 下限，并接受或解决实际环境缺口；证据见环境报告。不可用平台不能标 PASS。

## OD-10 — V1 终点与自主执行授权

批准 CAP01–CAP22 完成标准、CAP23–CAP32 排除范围、验收定义、权威/停止规则及终点 V1 IMPLEMENTATION COMPLETE + RELEASE CANDIDATE READY FOR OWNER ACCEPTANCE。这不是 SemVer1.0.0 授权。在 Owner 选择 candidate 版本前保留当前 0.1.0；Rust/Python 版本同步不等于发布。
授权单独命名的 implementation branch，包含已批准 P3 与已审阅 readiness commit；授权中间 commit、该 feature branch push/CI，以及在启动授权包含时最终向 develop 创建 draft PR。不 merge、不修改 master、不 tag、不 publish。实际验证通过后自动推进，允许依赖评估；P3 normal dependency 仍按批准基线保持零。开发测试、重构、私有结构可自主决定，公开合同不可。
Owner 答复必须在 owner-decisions.json 绑定 implementation branch、readiness commit、contract SHA-256 及独立审阅证据；单改 APPROVED 字样不算批准。替代是 OD-01 关闭并单独授权后的限定 P3 任务，不能静默选择。当前不授权执行生成的长任务书。

## OD-11 — 分支保护与 Agent 权限

GitHub 实查 master/develop protected=false，没有 repository/parent ruleset，也没有匹配分支规则。推荐 PR-only、禁止 force push/删除，要求真实 G2 与 Execution Readiness/assets 检查及解决 review thread；master 另要求 Owner 审阅、旧批准失效、最新提交 review、Agent 不可 bypass。develop 必须 PR+CI；合同/基线变更由 Owner 审阅。Agent credential 不应有 administration/release 权限，可用时限制可写分支；普通 write token 不等于技术上禁止 merge。Owner 自己创建 PR 再要求自己批准会死锁：指定另一位人类 reviewer，或明确保留仅 Owner 的紧急 bypass，不能给 Agent。
环境文档提供仓库级精确配置建议；本次未修改仓库或组织治理。替代：Owner 有期限地接受保护缺失风险，配合最小权限凭据、独立验收、人工 merge。接受风险不等于保护已存在。Owner 选择落实规则或记录具体风险、到期及权限。启动前重新查询实际 API；本地 branch check 无法阻止远端特权写入。

## OD-12 — 资源、Auto 与性能验收

推荐长任务初始限额：生成物/build 共 10 GiB；可用磁盘低于 10 GiB 停止新增大分配；测试/build 默认最多 4 worker，若可用 CPU 更少则从低，solver 单线程；可执行限制时单验证进程 2 GiB、任务合计 8 GiB。用户/系统更低限制优先。PR property 每家族 256 seed，deep 2048，持久化缩小后的失败；stress 预估容量，禁止无界笛卡尔积。Reference 逐案例捕获，保留不可变证据，只清理任务自有临时 cache。报告实际峰值 RSS/磁盘增长，无法测量则标缺口。
M11/M12 使用 doc11 固定留出工作负载、release build、隔离机器、3 次 warmup+10 次测量，报告 median/p95/peak RSS。候选目标：每个留出 workload，Auto median<=1.10*可行且已批准的 Serial/Outer 最快 median+2ms，p95<=1.25*最佳+5ms，同时不突破内存，不改 mode/cut/trace。它们是待批验收预算，不是实测结果或固定加速承诺。至少一个代表性 workload 必须证明 Outer crossover；全部回退 Serial 不能算 CAP20 完成。若 median 测量离散超过 5%，应隔离重测，不放宽目标。避免无限优化：两个不同方案都表明目标不可达后，提交实测合同冲突由 Owner 决定；普通性能不佳仍属 Agent 反馈。
替代：Owner 在 M11 前指定基于目标硬件实测的预算。请批准默认协议/预算或替换为准确数值；超限大规模 artifact 或平台费用另需决定。这是资源控制，不建设 orchestration service。

所有决策须在启动前关闭或批准具名 Owner-stop 流程。OD-03 的带宽证据、OD-05 独立遮挡 fixture、OD-08 的实际 manifest/profile 不能靠一封“全部同意”邮件凭空补齐。Owner 可一次批准政策；缺少的实证仍由准备/捕获工作补齐后审阅，未完成部分不会被本任务伪装为 READY。
