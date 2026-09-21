# 06｜Golden Reference & Validation Specification

## 目标与产物状态

Golden 是带 provenance 的分层可观察事实，不是最终 POA 的一列数字。本次交付的是**可执行研究探针、完整数据合同、canonical cases 清单与批准流程**；`evidence/nominal-trace.npz` 是实测 seed trace，22类探针和额外issue6重现不是已批准完整Golden Corpus。`reference/golden` 保留明确未批准状态。正式 generator 的全层采集与跨平台 corpus 审核属于紧接的 Golden 阶段，不能声称本阶段已经完成全部差分验收。

建议目录：

```
reference/
  generator/   reproduce_reference.py; probe_reference.py; 后续 capture/normalize/compare
  cases/       canonical_cases.json; 后续最小问题复现与属性种子
  schemas/     case.schema.json; trace.schema.json; README.md
  golden/      README.md; 后续 r0/<case_id>/manifest.json + arrays.npz
  requirements-linux-cp312.lock
  requirements-canonical.txt
```

Rust测试读取开放NPY数组或生成器导出的二进制f64；不在Core中嵌入Python解释器。Python生成器属于开发验证工具，不是发布runtime dependency。`solarfactors-reference` Rust crate暂无必要；后续若NPY/fixture读取重复，可用独立测试辅助crate。

## 数据合同

每个case包含冻结source SHA、environment ID、依赖lock SHA、generator SHA、schema/model revision、case输入SHA、生成时间、seed、字节序、每个数组dtype/shape/axes/unit/SHA256和nonfinite统计。规范数组little-endian float64；int64用于映射；bool mask；JSON不得写非标准NaN，使用分类码或null+mask，**不得把NaN换0**。NPZ容器zip时间戳会影响整个文件hash，可按未压缩NPY payload逐数组hash；另保存产物文件hash。

| 层 | 必须记录 | 轴/语义 |
|---|---|---|
| 输入 | 原始与normalized DNI/DHI/GHI、角度、albedo、dayofyear、时间标签、配置、skip分类 | [T]；原始与广播结果分开 |
| 几何 | row端点/法向、rotation、太阳截面向量、alpha、raw shadow、裁剪shadow、ground cut点 | [T,N,endpoint,xy]；角单位明确 |
| 分区 | logical SurfaceKey、reference index、active映射、各面coords/length/shaded、PV/ground归属 | [T,S,…]；零长度槽保留 |
| irradiance | I0、airmass、AOI、Perez ε/Δ/bin/F1/F2、三POA/luminance、τ、horizon mask、direct/circ/horizon/absorbed分量 | [T,S]与[T]分开 |
| VF | geometric F的**AOI前copy**、G、sky列、Fast分组VF、AOI quadrature配置 | [T,S+1,S+1]；row=receiver |
| linear system | E/Eabs、ρ、1/ρ、A=diag(1/ρ)−F、b与B等价形式、sky source | inverseρ允许非有限并带标记 |
| solution | q0、qinc、isotropic、reflection、qabs、残差/条件诊断 | Full完整；Fast不存在的字段写unavailable，不写0 |
| 聚合 | 每segment/side/row的length与weighted sum/mean、target selection、validity状态 | stable keys，不依赖对象地址 |
| 异常 | exception type/message摘要、warning类别、发生阶段、timeout | expected failure也可作为raw oracle |

提取顺序必须是 fit输入→geometry→irradiance→F copy→solve→G→结果。因DEV-009，不得在run_full结束后把被覆盖的F当geometric F。不修改冻结源码来“修好”捕获；用外围instrumentation记录原始行为。Instrumentation本身要对nominal聚合值无扰动校验。不要pickle Python对象当跨语言golden。

## Canonical Case Matrix

机器可读cases已随包提供。默认基准：2019-06-01T12:00Z，N=3,w=1,h=1,gcr=.5,axis180,z45,solar az270,tilt45,panel az270,DNI600,DHI100,albedo.25,rho .01/.03，无透射，cut1，Full Hybrid。每个variation继承该基准，不能只保存自然语言描述。

| 家族 | 覆盖与构造 | 必须检查 |
|---|---|---|
| C01–C04 | N=1,2,3,11 | 边排、内排、Slogical与active、mirror映射 |
| GCR | .15,.5,.85,1.0；另gcr≤0/大于声明域 | directshade、距离/交叠、错误合同 |
| orientation | 左/右、flat、±近零、tilt90、azimuth0/360等价 | signed zero、halfspace、法向一致 |
| sun | z5/45/85/89.9/90/100；az对正/背/沿轴 | horizon、grazing、night政策、递归case |
| shading | no/partial/high-shade；N≥3低太阳高度＋独立unit full-shadow端点 | golden记录实得遮长分类，不能凭配置名字断言fully shaded |
| irradiance | DNI0、DHI0、二者0、DHI高/ε bin边界 | NaN、F1/F2、零source与sky、bin归属 |
| optics | albedo0/.02/.25/.9/1；ρ0/接近1；τ0/部分/1 | singularity域、有效吸收、反射耦合 |
| cut | uniform1/2/8；单排front3/back5 | stable索引、固定场加权守恒、独立求解收敛 |
| models/modes | Isotropic/Hybrid × Full/Fast；row0/middle/last；segment0/last | Fast近似、不存在的qabs、选择越界 |
| AOI | constant0/.8/1、SAPM固定系数、非平滑但有界曲线；J=150/300/600 | 原F不可变、absorption、quadrature误差 |
| batch | T=1/2/17/8760，跨flat/tilt变号/日出/年界/闰日 | scalar广播、dayofyear、chunk/serial/parallel等价 |
| invalid | unequal shapes、NaN/Inf、negative inputs、地下排、空T、cut0、非法row | typed errors/空batch约定；不冒充物理oracle |
| geometric boundary | endpoint touch、tol±ULP、完全覆盖difference、平行投影、地面extent触边 | L1及reference static API差异 |

批量“many”不默认跑到数百排完整inverse；先按内存限制评估，否则fixture生成本身不可执行。case expansion需要输出所有已解析参数和seed。catalog是跨语言合同，不是直接对Python构造器的kwargs：GHI映射ghi；JSON cut键转整数；aoi_sections映射VFCalculator.n_aoi_integral_sections；aoi曲线配置生成reference回调且保存曲线数据。ground_extent默认[-100,100]为metadata核对；非默认extent/mirror扩展属于Rust-only不变量或显式模型扩展，不得静默patch参考多处globals后仍称原始oracle。pairwise覆盖为主体，危险交互（near-flat×low-sun×cut、AOI×albedo0、Fast×τ）专门组合，不做失控笛卡尔积。

## 六层验证

| 层 | 必须测试 | 独立性与 Gate |
|---|---|---|
| L1 数学 | trig周期/单位、投影、interval差集、Hottel解析例、Perez bins/系数、LU已知系统 | 手算/解析/高精度输入；先于差分，不只镜像代码 |
| L2 差分 | 按上述层逐层对Frozen Python比较，首先定位最早分歧层 | 有bug的raw oracle与修正expectation并存；waiver按case+field+CDR |
| L3 物理/代数不变量 | 下表 | 不依赖Reference输出；仅适用域内强制 |
| L4 property-based | 合法结构与边界biased输入、失败shrink并持久化seed | Rust proptest；不使用“assume掉所有难例” |
| L5 metamorphic | 镜像、零反照率、无阴影、对称、cut、执行等价 | 每项前提必须满足，不制造错误oracle |
| L6 E2E | Native/Python同输入同结果，Full/Fast/selection，错误合同与wheel安装 | 不在E2E只比一个均值；测试有效性mask与轴顺序 |

### L3 invariants 的准确前提

1. 几何VF：active有限面 `−ε≤F≤1+ε`，`ΣphysicalF+Fsky≈1`，ground-ground和同侧自视为0。零长槽row/column在压缩映射后为0；不检查sky row sum=1。
2. 互易：`L_iF_ij≈L_jF_ji`，只检查有正长度的物理面；sky不具有限面积，G吸收加权不满足此对称。
3. surface-length conservation：每侧lit+shade=w，各segment守恒；ground非交叠覆盖指定extent；每个shade length在[0,w]。
4. qinc=E+Fq0、q0=ρqinc、求解scaled residual满足阈值；sky固定。常数吸收时qabs=(1−ρ)qinc，custom AOI用其独立公式核验。
5. 非负：当E、F、ρ、吸收核非负且系统可逆时qinc/q0/qabs≥−ε。Hybrid极端经验分量可能负；不可不分输入域地断言所有Perez component≥0，也不可事后全clip。
6. symmetry：在整体几何、方向、光学、边界都镜像后按key映射等价。有限阵列不同排有边缘效应，不应直接assert所有row相同。

### L4 合法输入域

首版generators：N∈1…12；w∈[.2,5]m；gcr∈[.1,.9]；tilt∈[0,89.9]°；h≥w|sinβ|/2+正clearance；ground必须包住阵列且边界留量。太阳z∈[0,89.9]、正确轴/面方位；DNI∈[0,1200]、DHI∈[0,800]，全零独立策略；albedo、ρ∈[0,.95]，spacing/transparency∈[0,1]；cut1…8；T1…17。该范围用于测试抽样，不声称就是经验Perez经过实验校准的完整有效域。

另设边界generator集中0、90、εbin阈值、tol±ULP、ρ0/1、flat±小角、最低点近地、接触/包含区间；非法generator验证错误合同。先shrink N/T/cut，再连续参数，保留造成拓扑变更的边界；将最小失败输入加入固定regression。

### L5 metamorphic tests 的限制

- Mirror：关于阵列中心反射x，同时变换sun、tilt、surface normal、row index及ground extent；默认[-100,100]不关于阵列中心对称，必须一起变换或使用对称extent。
- Zero albedo：只令**地面反射贡献**归零，PV↔PV反射仍存在。可用ρground连续趋0核验M08。
- No shading：直射shaded length=0不代表邻排不挡diffuse；隔离面解析比较须满足N1/相应边界假设。
- Row symmetry：镜像输入下对称排对应；不把有限排数系统误作周期系统。
- Cut aggregation：同一固定场/同一partition的ΣLq严格可加；重新离散求解只做收敛与误差界，不要求粗细网格相等。
- Execution：Serial/ExplicitParallel/Auto/不同chunk只重排独立时点，不改变模型、active判定、求和次序定义或原始timestep索引。
- Irradiance scaling：Isotropic在固定光学/几何下对源线性；Hybrid随DHI改变Δ与F1/F2，一般不满足同比缩放，禁止通用此断言。

## Golden update governance

1. 新生成一律写candidate目录，无覆盖权限；manifest记录生成原因及完整diff。
2. 逐层比较max abs/relative、分位数、nonfinite/exception变化、拓扑变化和受影响case计数；总POA相近不能豁免内部差异。
3. 每个超阈值变化关联CDR或reference upgrade记录；审查source/dependency/generator任一变化，禁止把它们混在同一次无解释refresh。
4. Reviewer批准后以immutable corpus version发布，保存旧版本/manifest/hash；分支CI只读approved，不具备失败自动更新开关。
5. Reference bug corrected期望与raw B层并列存储，字段级waiver有expiry/review条件。没有证据的偏差不能通过放宽全局tolerance解决。
6. Golden Gate还需要同环境双次再生成、至少目标平台抽样差分、独立不变量、schema验证通过。样本能运行≠corpus已冻结。
