# LCB-01 — View Factor 兼容偏差调查

- 状态：**LCB-01 — READY FOR OWNER DECISION**
- 日期：2026-09-22
- Repository：`edvcc/pvfactors-rs`
- Research branch：`research/vf-lcb01-compatibility`
- Base checkpoint：`d5bc38ebd6ba853c4cec530e4787d1ab6168203d`
- Frozen Reference：`pvlib/solarfactors` v1.6.1，`ecbfc863657e239817603a43898ae173c7ccad9c`
- 范围：仅 Reference deviation investigation；不进行 Rust VF 生产实现。

## 结论

LCB-01 已确认是 Frozen Reference 在**精确负向水平端点**上的 PV-ground Hottel 端点方向缺陷。

当前证据不支持把问题泛化成“所有 `tilt > 90°` 都有问题”，失败也不是由真实 obstruction 导致。在设计扫描域内，只有 Reference 到达精确 `rotation_vec = -180°`、PV row 数量至少为 2，并进入右侧 `_vf_hottel_gnd_surf()` 分支时出现 bound violation。精确水平 PV surface 的两端 y 完全相等；`TsLineCoords.highest_point` 按 tie rule 选择 `b1`，而从 180° 左侧逼近时真正的 higher endpoint 是 `b2`。`_vf_hottel_gnd_surf()` 中带符号的 crossed/uncrossed 分组隐含依赖非退化 high/low 顺序，因此在 tie 点发生 numerator 翻号。

所以，第一个错误数值不是 Geometry，而是：**端点 tie 翻转之后，仍按原 high/low 方向假设返回带符号 Hottel string difference**。

Approved Geometry 坐标、稳定 surface identity、front/back identity 与 Geometry Golden 均保持正确，不应修改。

## Reference 源码证据

Frozen Reference 使用两个语义不同的 primitive：

1. `_vf_surface_to_surface()` 对 Hottel string difference 使用 `abs(...)`，因此 geometric magnitude 对端点方向反转不敏感；
2. `_vf_hottel_gnd_surf()` 返回 `(d1 + d2 - l1 - l2) / (2 * width)`，没有 magnitude 操作，并依赖 `high_pt_pv`、`low_pt_pv`、`shadow_is_left` 与 obstruction-point 分支维持 crossed/uncrossed 的预期方向。

LCB-01 失败 case 进入第二个 primitive。

## 精确端点不连续

Canonical `N=3` case：

| Surface tilt | Rotation | PV b1.y | PV b2.y | high endpoint | PV→ground 目标 VF | PV→sky VF | 越界数 |
|---|---:|---:|---:|---|---:|---:|---:|
| `nextafter(180°, 0)` = `179.99999999999997°` | `-179.99999999999997°` | 0.9999999999999998 | 1.0000000000000002 | b2 | +0.20382042637679965 | ~4.99975e-5 | 0 |
| `180°` | `-180°` | 1.0 | 1.0 | tie rule 选 b1 | −0.20382042637679976 | 1.999950002499975 | 36 |

物理几何只发生浮点端点退化；VF 翻号且 sky 突跳约 2 不可能是合理物理极限。

## 指定 blocker pair 的独立 oracle

指定 pair：

- receiver `ReferenceIndex = 3`（ground shadow 0）
- source `ReferenceIndex = 28`（row 0 front）

使用 Frozen Geometry 输出的**实际二进制浮点坐标**并以 100 位高精度计算：

`F_ground→pv = 0.2038204263767998815712607034283142448398871848600639686444912994513033510331848965536530463636382979`

互易方向 PV→ground：

`F_pv→ground = 0.2038204263767998363140346529403541283845537638530083543871196631595168203537032258281470128079206528`

完全独立的二维 diffuse 数值积分（Gauss order 128）约为：

- PV→ground：`0.2038204263768001`
- ground→PV：`0.20382042637680012`

高精度解析 Hottel 与独立数值积分在浮点精度范围内一致，二者都否定 Reference 的负值。

## Obstruction 审计

对 canonical 精确 `-180°` case 的 raw `_vf_hottel_gnd_surf()` 调用审计：

- raw calls：28
- negative calls：28
- 其中四条 string **均未被 obstruction 改道**：28
- 存在任一 obstruction 的 negative calls：0

因此 LCB-01 的翻号不是 obstruction-point path replacement 导致的。函数处于“obstructed Hottel”调用链中，但此次出错的 string 实际全是 direct path。

## Domain scan

主扫描共 33 个有设计 case，覆盖：

- tilt：0、1e-10、1、45、89.9、90 两侧 near-boundary、90、100、120、150、179、179.9、179.999999、near-180、180；
- row count：1、2、3、11；
- canonical / mirror surface azimuth；
- 通过 assembled matrix 覆盖 front/back、PV-ground、ground-PV、PV-PV、edge/middle、mirror。

Reference bound violation 仅出现于：

- `N=2, tilt=180°, surface_azimuth=270°`：14；
- `N=3, tilt=180°, surface_azimuth=270°`：36；
- `N=11, tilt=180°, surface_azimuth=270°`：492。

扫描中的其他 `tilt > 90°` 非端点 case、`N=1` 精确 180° control，以及 `surface_azimuth=90°` 的精确 180° mirror control 均未出现 bound violation。

因此当前可支持的 affected domain 是**精确负向水平端点 singularity**，不是“tilt > 90° 全域缺陷”。

## Candidate correction 证据

研究用 diagnostic 只在 `_vf_hottel_gnd_surf()` primitive 输出位置，将 signed string difference 转为 geometric magnitude，然后再正常构造 matrix 与 sky closure。

结果：

- `N=2` canonical 180°：14 → 0；
- `N=3`：36 → 0；
- `N=11`：492 → 0；
- exact mirror controls 不变；
- 非端点代表 case 未出现大于 1e-12 的实质变化；
- candidate exact-180 matrix 与 Frozen Reference 在 `nextafter(180°, 0)` 的单侧极限最大差：`3.774758283725532e-15`；
- canonical N=3 candidate oracle：min 0、max 1、closure error 0、reciprocity error 0。

这些证据支持在 Hottel analytic primitive 层使用 orientation-invariant magnitude，但**不等价于允许对任意最终矩阵做 `abs()` 后处理**。

## 为什么 whole-matrix abs 明确错误

如果对已组装好的 Reference matrix 整体 `abs()`：

- row-0 front 的 row sum 变为 `2.99990000499995`；
- 对应 sky 仍为 `1.999950002499975`；
- closure error 约为 `1.99990000499995`；
- 仍有 8 个 active sky entry > 1。

所以修正必须发生在 finite-pair geometric primitive / visibility semantics 层，并在之后重新正常计算 sky closure；不能对最终 matrix 全局取绝对值。

## 统一数学合同候选

Active 二维 diffuse line surface 的主物理定义：

[
F_{i\to j}
=
\frac{1}{L_i}
\int_i \int_j
V(s,t)
\frac{
\max(0, n_i\cdot \hat r)
\max(0, -n_j\cdot \hat r)
}{
2r
}
\, dt\, ds
]

其中 `V(s,t)` 为物理 line-of-sight visibility。该定义天然非负。

Hottel 是同一物理量的解析优化。对合法 Hottel construction，straight 或绕 obstruction 的 taut path 形成两组端点 pairing，其 geometric result 应取 orientation-invariant magnitude：

[
F_{i\to j}
=
\frac{
\left|\Sigma L_{crossed}-\Sigma L_{uncrossed}\right|
}{
2L_i
}
]

端点方向反转可能交换 crossed 与 uncrossed 的命名，但不能改变物理 VF 的符号。

Front/back identity 与 physical visibility 是独立语义输入，不得通过 fold tilt、交换 side 或修改 Approved Geometry 来修补。

## 对调查必答问题的回答

1. **第一个错误 branch/formula：**右侧 branch 中，精确水平 high/low tie 翻转后，`_vf_hottel_gnd_surf()` 仍返回带符号 string difference。
2. **是否只发生 tilt=180？**在本次设计的 valid-domain scan 内，失败隔离在精确 negative-horizontal endpoint；未发现非端点 tilt 失败。
3. **是否覆盖全部 tilt>90？**否。100°、120°、150°、179°、179.9°、179.999999° 以及小于 180° 的最近可表示浮点均正常。
4. **Unobstructed Hottel 是否正确？**未发现 `_vf_surface_to_surface()` 缺陷；在 blocker geometry 上其 magnitude 与解析/数值独立 oracle 一致。
5. **ordering/high-low/visibility/sign？**根因是 endpoint tie ordering + signed crossed/uncrossed return 的组合；本次 negative calls 的 visibility obstruction 不是根因。
6. **global abs 是否有反例？**对 `abs(final_matrix)` 有明确反例，会破坏 closure 且 sky 仍 >1。对更窄的“在 Hottel primitive 内取 geometric magnitude”候选，本次设计域未发现反例，但它是数学语义决定，不是 matrix 后处理许可。
7. **>90° 如何保持 front/back？**保留现有 `SurfaceKey` side 与 normal，以其决定 physical visibility；不 fold tilt，不 swap front/back。Hottel endpoint label 只是局部解析构造，不得成为 surface identity。
8. **统一 VF 合同：**非负 visibility integral 为 normative definition；Hottel 是 orientation-invariant analytic realization；reciprocity 与 closure 是二级 invariant，不能替代 entry bounds。

## 新增 invariant 要求

对每一个 active finite receiver/source pair：

`0 <= F_ij <= 1`

并在适用时同时检查：

- reciprocity；
- closure；
- visibility；
- mirror invariance。

Research harness 的 mutation self-test 已明确覆盖并捕获：

- negative but reciprocal matrix；
- closure-pass but invalid-entry matrix；
- `F > 1`。

三类 mutation 均 PASS。

## Geometry 影响

**无。**

不需要修改 P3 Geometry coordinate、topology、`SurfaceKey`、`ReferenceIndex`、`ActiveIndex`、front/back identity、Golden payload 或 geometry tolerance。

如果后续实现显示必须修改 Geometry，应作为新的 escalation 处理，不得静默并入 DEV-028。

## Environment 说明

原始 blocker 已在 Approved executable R0 evidence 中捕获，环境 ID 为 `031158a1d1be8cdb9093`。

新增 GitHub Actions research run 使用完全冻结的 canonical requirements/runtime 字段，并报告 `canonical_environment_match=true`；但 hosted Linux kernel/platform string 不同，因此 runtime fingerprint 不同。该运行属于跨 host 补充证据，不是重新定义 R0，也没有通过修改 dependency / environment policy 制造兼容。

## 需要 Owner 决策

1. 批准或拒绝 proposed **DEV-028** 分类与 corrected expectation；
2. 批准或拒绝 proposed **CDR-008** VF magnitude / visibility contract；
3. 批准或拒绝 `view-factor-lcb01-oracle-v0.1` 作为 P4 corrected oracle seed；
4. 若批准，授权恢复 Full-Project Launch Closure；此时仍不得激活 Full Implementation。
