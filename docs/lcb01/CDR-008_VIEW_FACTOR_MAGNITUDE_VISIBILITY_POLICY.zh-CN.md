**历史 / 已替代。** 这是较早的33-case研究，不是当前批准合同。有效权威为[Owner决定](../execution/launch/LCB-01_OWNER_DECISIONS.zh-CN.md)、[DEV-028](../execution/launch/DEV-028_VIEW_FACTOR_ENDPOINT_ORIENTATION_DEFECT.zh-CN.md)及docs/execution/launch中的DEV-029/CDR-008。下文较窄的“仅exact180”结论由切分敏感的near180证据替代。另一单case候选仍未批准。

# CDR-008 — View Factor 几何 Magnitude、Visibility 与退化端点策略

- 状态：**PROPOSED / UNAPPROVED**
- 日期：2026-09-22
- Owner：Repository Owner
- 相关偏差：DEV-028
- 相关调查：LCB-01

## 决策候选

V1 View Factor 合同将三件事明确分离：

1. semantic surface side 与 outward normal；
2. physical visibility / occlusion；
3. 非负 geometric measure 的 analytic evaluation。

Hottel 实现内部使用的 endpoint ordering 不是 surface identity，也不得决定物理 View Factor 的正负号。

## Normative 物理定义

对 active 二维 diffuse line surface：

[
F_{i\to j}
=
\frac{1}{L_i}
\int_i \int_j
V(s,t)
\frac{
\max(0,n_i\cdot\hat r)
\max(0,-n_j\cdot\hat r)
}{
2r
}
\,dt\,ds
]

因此数学 View Factor 必须满足 `F_ij >= 0`。在本项目支持的 enclosure geometry 中，active pair 还必须满足 `F_ij <= 1`。

## Hottel analytic realization

适用 Hottel crossed-string construction 时：

[
F_{i\to j}
=
\frac{
\left|\Sigma L_{crossed}-\Sigma L_{uncrossed}\right|
}{
2L_i
}
]

存在 blocking 时，相关 path length 可以按所选 visibility construction 使用绕 blocking boundary 的 taut path。端点方向反转可能交换两组 pairing 的标签，但不得改变物理 magnitude。

Rust implementation 可以采用比 Frozen Reference 更清晰的内部构造；必须保持数学结果与已验证兼容行为，而不是复制 Reference 的 high/low endpoint artifact。

## Semantic side 策略

- `SurfaceKey::PvRow.side` 继续作为 front/back authoritative identity；
- `tilt > 90°` 不 fold；
- 90° 或 180° 不交换 front/back；
- visibility 根据 semantic side/normal 与 occlusion geometry 推导，而不是由哪个端点数值上“更高”决定；
- exact horizontal / equal-y endpoint 是普通退化解析 case，不构成改变 surface identity 的理由。

## Matrix assembly 策略

1. 先计算 finite active-pair View Factor；
2. 检查 pair bound 与 visibility invariant；
3. 在适用时检查 reciprocity；
4. finite factors 合法后才通过 closure 派生 sky/enclosure remainder；
5. 如果 finite factors 在 comparison policy 之外导致 closure 物理不可能，应报告 invariant / algorithm failure，不得通过 clamp 或补偿性 sky 值隐藏。

明确禁止对 full matrix 做 `abs()`。

## Invariant

必须检查：

- active entry bound：`0 <= F_ij <= 1`；
- reciprocity：`L_i F_ij ≈ L_j F_ji`；
- completed enclosure closure；
- visibility consistency；
- 定义适用时的 mirror / metamorphic consistency。

Entry bound 是一级 invariant。带符号的物理非法 matrix 仍可能同时通过 reciprocity 与 closure，因此后两者不能单独作为正确性证明。

## LCB-01 接受证据

Proposed analytic magnitude 处理：

- 消除 N=2/3/11 所有已观察精确 -180° bound failure；
- 保持 exact-180 mirror controls 不变；
- 扫描中的非端点 case 未发生实质变化；
- 与 Frozen Reference 180° 左侧单侧极限最大相差约 `3.8e-15`；
- canonical N=3 candidate oracle 恢复为 min 0、max 1、double precision 下 exact closure 与 exact reciprocity。

指定 blocker pair 同时通过 100 位 Hottel 与独立 numerical integration 验证。

## Geometry 边界

CDR-008 **不需要修改** Approved P3 Geometry baseline。

若未来实现为了满足本合同必须修改 Geometry，应登记为新的 decision / blocker 并升级处理。

## 若批准后的验证要求

P4 必须新增：

- closure acceptance 之前的 entry-bound check；
- negative-but-reciprocal mutation；
- closure-pass / invalid-entry mutation；
- `F > 1` mutation；
- exact -180° 与 one-sided-limit case；
- mirrored +180° controls；
- 用于验证同一 magnitude / visibility 分离的 genuinely obstructed case；
- 针对 approved corrected oracle 的 cross-language / tolerance comparison。

## 非决策项

本 CDR 不批准：

- 某个具体 Rust data structure；
- 最终 P4 numerical tolerance profile；
- production implementation；
- Full-Project Launch Closure；
- full autonomous implementation task 激活。
