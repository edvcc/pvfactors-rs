# 08｜REFERENCE_DEVIATION_AND_AMBIGUITY_REGISTER

核查日期2026-09-21；上游范围见00。Confirmed 表示源码路径或实测已能确认所述事实，不等于上游作者已接受该缺陷，也不等于修正模型已得到验证。所有 proposed CDR 尚未冒充项目批准。probe 名称对应 evidence/probe-results.json；额外边界实测见 evidence/boundary-probes.json。

| ID | 类别 / 状态 | 证据与影响 | Rust 建议 / Gate |
|---|---|---|---|
| DEV-001 | confirmed bug | [#6](https://github.com/pvlib/solarfactors/issues/6)，utils.perez_diffuse_luminance 背面递归；本次 issue6 探针 RecursionError。接近正交时反转后投影仍微负 | 单次半球判定并明确 near-zero AOI；CDR-002；Perez Gate前解决 |
| DEV-002 | unsupported scenario / 输入验证缺失 | [#9](https://github.com/pvlib/solarfactors/issues/9) 地下排几何可给不合理结果；代码不校验最低点；本次 underground 探针确有负y，但所取 qinc 未重现该 issue 的负值 | 校验所有时点离地 clearance；不要求复制非法几何输出；CDR-003 |
| DEV-003 | confirmed bug | [#10](https://github.com/pvlib/solarfactors/issues/10) skip mask未消费；night z100 探针背面 −19.42755776 W/m²，标记 skip仍计算 | 前置输入/夜间政策；CDR-001，Engine与planner共用分类器 |
| DEV-004 | model/domain limitation | [#12](https://github.com/pvlib/solarfactors/issues/12)，±100m ground硬编码；更大阵列、平移与缩放不能假定不变 | V1显式finite extent；兼容默认值，校验阵列域；infinite/adaptive ground另revision；CDR-003 |
| DEV-005 | confirmed model implementation omission | [#14](https://github.com/pvlib/solarfactors/issues/14)，Hybrid transform只对back施加horizon遮挡；[PR41](https://github.com/pvlib/solarfactors/pull/41) 查询时未合并 | 默认新core不应无说明保留缺漏；两侧遮挡修正需可独立验证Golden；CDR-005阻塞Irradiance冻结 |
| DEV-006 | performance limitation | [#13](https://github.com/pvlib/solarfactors/issues/13)；Sground=(2N+1)(N+1)，名义dense inverse O(S³)，不是“阶乘复杂度” | active压缩/streaming/solve；benchmark后定优化；不影响物理目标 |
| DEV-007 | confirmed bug / zero limit | [#37](https://github.com/pvlib/solarfactors/issues/37)，Hybrid DNI=DHI=0 NaN；本次zero_light_hybrid重现，Isotropic为0 | 显式全零光照短路；保留原始失败Golden，正确期望来自线性系统；CDR-001 |
| DEV-008 | numerical implementation artifact | albedo=0，ρ逆得到inf，ground qinc NaN；zero_albedo探针；PV仍可有限 | 用M08 incident系统，不复制inf；CDR-004，零ρ代数极限测试 |
| DEV-009 | confirmed mutation bug | VFCalculator有fAOI时`vf_aoi_matrix=self.vf_matrix`，原位覆盖F；aoi_constant最大改变0.1714254150；qinc已在覆盖前求出 | 独立F/G缓冲，trace必须在AOI前复制F；不以运行结束后的pvarray.ts_vf_matrix作几何oracle；CDR-004 |
| DEV-010 | confirmed absorption inconsistency | 自定义AOI分支只改PV receiving rows，ground rows保留几何F，缺(1−albedo)；无AOI分支则完整缩放 | Gground=(1−albedo)Fground，检查qabs能量关系；CDR-004；源码确认，本次constant f=.8、albedo=.25时ground qabs超过(1−albedo)qinc最多9.788216915 W/m² |
| DEV-011 | model approximation | AOI质心近似、整格求积有边界多计；G局部可大于F，f=1不严格还原有限面Hottel | V1命名`ReferenceMidpoint300`，不靠clip伪装修正；新积分策略未来单独model revision/CDR |
| DEV-012 | physical/model ambiguity | Perez原文允许负F2；Hybrid取abs(horizon)。背面circ分母cosz而前面有cos85°下限；原文/依赖/模型不同 | CDR-005必须分别决定：保留并标明经验模型，或验证后修正；不得合成一个“Perez兼容”含糊结论 |
| DEV-013 | confirmed indexing bug | TsGround.non_point_shaded_surfaces_at/illum_surfaces_at收到idx，却调用element.non_point_surfaces_at(0) | Rust逐时active映射正确；静态adapter bug不成为Core要求；CDR-006 |
| DEV-014 | dormant capability / implementation artifact | circumsolar_angle/model只用于未进入主链的helper；circ5/circ60输出相同，辅助函数单测不证明主模型使用 | 主模型按M05；圆盘遮挡模型V1.x候选；不暴露无效参数 |
| DEV-015 | suspected bug / Fast approximation | Isotropic front shade环境总量扣D但未补τD；Hybrid补回；Fast里total_perez实际isotropic | 后者作为明确Fast模型语义记录；τ缺项需定向差分CDR-007，不静默改Perez transposition |
| DEV-016 | confirmed static geometry bug | custom difference：u=[0,1]、v=[−1,2]实测返回长度1，正确差集应为空；见boundary-probes | 专用interval subtraction数学正确；已有最小重现；不阻塞Ordered timeseries，CDR-006 |
| DEV-017 | unsupported/ambiguous configuration | 只传一侧fAOI时VF AOI两侧都不启用，而irradiance侧仍可能用回调 | 新API成对配置或显式另一侧常数；拒绝含糊配置；Binding Gate |
| DEV-018 | implementation artifact | scalar DNI驱动广播、Pandas隐式index、NaN/空批缺系统验证；负零/整批is_empty影响路径 | 正式shape/dtype/dayofyear合同；per-timestepactive；C层不机械复制 |
| DEV-019 | model discretization | cut改变horizon质心、有限面均匀radiosity、AOI近似；nominal后背44.4145，指定cut后47.4100 | cut聚合测试分成固定场可加性与重新求解收敛，不能硬判严格相等 |
| DEV-020 | packaging/performance | [#31](https://github.com/pvlib/solarfactors/issues/31) Matplotlib依赖；[PR4](https://github.com/pvlib/solarfactors/pull/4) 去Shapely尝试未合并 | Core均不依赖；不认为该PR已经证明新kernel等价 |
| DEV-021 | resolved upstream compatibility issue | [PR39](https://github.com/pvlib/solarfactors/pull/39) pvlib0.14输出字段；v1.6.1修复 | 选择v1.6.1理由；不能用更早baseline跑新pvlib后叫Rust数值偏差 |
| DEV-022 | evidence gap | Anoma2017全文403、Marion2017全文502；原文未逐式读取 | 几何/VF由源码、官方theory与独立推导交叉验证；涉及新的物理修正前补原文或等强独立证据 |
| DEV-023 | reproducibility gap | 当前只实际跑Linux x86_64 CPython3.12.14；macOS/Windows无实测，container digest未建立 | R0是可执行锁定清单，Golden最终批准前环境复建与跨平台数值采样；不伪称跨平台完成 |
| DEV-024 | physical invariant precondition | Perez F1无上限，可导致Liso负；输入极端而经验模型范围不明 | 不盲目clip分量；把非负检查域与warning/error政策固定进CDR-005 |
| DEV-026 | numerical/predicate artifact | collinearity用未归一normal；同方向差的向量放大100倍，本次判定从true变false；boundary-probes记录 | scale-aware方向与offset分开；CDR-003；不能用常量1e−5当无量纲角阈值 |
| DEV-025 | execution artifact | multiprocessing切空chunk、callback序列化、BLAS嵌套线程、report自定义merge；整批is_empty | Rust确定索引输出；worker≤effective T且统一线程预算；分块等价验证 |

## Compatibility Decision Record 模板

每项放在 `docs/decisions/CDR-NNN.md`（后续阶段创建，不预填假批准）：

```
ID / title / owner / date / status: Proposed | Accepted | Rejected | Superseded
reference SHA + runtime_id + algorithm IDs + affected capabilities
A: physical/model source and exact claim
B: observed reference behavior (case IDs, immutable artifact hashes)
C: incidental implementation detail
issue/deviation IDs and affected valid/invalid input domain
options (preserve named approximation / fix / reject input / defer capability)
selected semantics, formula, boundary and tolerance changes
Rust and Python API effects, result schema/model_revision effects
independent evidence and expected direction/magnitude of changes
required L1/L2/L3/L4/L5/L6 tests; corrected expectation source
reference raw output remains unchanged; diff waiver limited to named fields/cases
migration/versioning note; review identities and approval evidence
```

候选 CDR：001输入/夜间/零光照；002 AOI半球/无递归；003几何有效域/有限地面；004ρ零值与AOI存储/吸收修正；005 horizon/低太阳高度/经验模型非负域；006静态几何适配偏差；007Fast τ缺项。本报告给出方向，但没有为项目虚构审查签字。

**治理原则：**已确认bug无需为了逐位兼容在生产core重演。原始Reference fixture仍记录它；修正后expected来自代数/物理独立证据或明确批准模型，而不是把Rust当前输出写回Golden。严格历史行为如有实际用户需求，可另命名reference-only验证profile，不默认建设一套有bug的产品模式。
