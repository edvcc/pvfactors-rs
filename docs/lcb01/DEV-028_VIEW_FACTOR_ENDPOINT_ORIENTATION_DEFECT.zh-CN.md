# DEV-028 — 精确负向水平 PV–Ground View Factor 端点方向缺陷

- 状态：**PROPOSED / UNAPPROVED**
- 日期：2026-09-22
- Owner：Repository Owner
- Reference：`pvlib/solarfactors` v1.6.1，`ecbfc863657e239817603a43898ae173c7ccad9c`
- 相关调查：LCB-01
- Proposed decision record：CDR-008

## 分类

已确认的 Reference behavior defect / endpoint-orientation singularity。

这不是 Geometry 缺陷，也不是一般性的 `tilt > 90°` 限制。

## Trigger 与已观察影响域

确认 trigger 为 Frozen Reference 出现以下状态：

- PV surface 在 `rotation_vec = -180°` 时精确水平；
- 数值 PV surface 两端 y 完全相等；
- `highest_point` 的 tie rule 选择 `b1`，从而反转 180° 左侧单侧极限中的 endpoint ordering；
- PV-ground 计算进入右侧 `_vf_hottel_gnd_surf()` 路径；
- crossed/uncrossed 的带符号表达式未做 orientation-invariant magnitude 归一化而直接返回。

设计扫描中，精确 canonical 180° 的 `N=2/3/11` 出现 bound failure；`N=1`、镜像 +180° 以及其他非端点 >90° case 未出现同类越界。

## 证据

指定 blocker pair：

- receiver ReferenceIndex 3；
- source ReferenceIndex 28；
- Frozen Reference：约 `-0.2038204263767998`；
- 独立 100 位结果：
  `+0.2038204263767998815712607034283142448398871848600639686444912994513033510331848965536530463636382979`。

精确 canonical audit 发现 28 个 negative raw Hottel call；28 个全部由四条 direct、unobstructed string 构成。

Candidate magnitude primitive 将 N=2/3/11 的 14/36/492 个 bound failure 全部消除，并与 `nextafter(180°,0)` 的 Frozen Reference 单侧极限最大相差约 `3.8e-15`。

## Corrected expectation

V1 不得复刻该 Reference singularity 产生的负物理 View Factor。

在 analytic Hottel 路径中，crossed/uncrossed endpoint pairing 只是实现构造；端点方向反转可以交换 pairing label，但不能改变物理 magnitude。Physical side identity 与 visibility 必须独立判定。

Corrected finite-pair expectation 必须非负并满足 CDR-008 合同；只有 finite factors 合法后才计算 sky。

## 禁止的兼容捷径

不得：

- 将 >90° tilt fold 回去；
- 交换 front/back semantic identity；
- 修改 Approved Geometry 来强制端点顺序；
- clamp 非法 Reference entry；
- 对最终 assembled matrix 做 `abs()`；
- 刷新 Approved Geometry Golden 或 tolerance 来掩盖缺陷。

## Raw / corrected evidence 策略

Frozen Reference 输出继续作为 immutable raw evidence。

Corrected oracle 必须独立标记 candidate / approved corrected expectation，不得覆盖 raw Reference capture。

## 批准后的影响

若 DEV-028 被接受，Rust implementation 与 P4 oracle 可以将精确 -180° 的负 Reference VF 视为已登记 incompatibility defect，而不是兼容目标。

单独接受 DEV-028 不等于批准 P4、Full-Project Launch Closure 或 Full Implementation。
