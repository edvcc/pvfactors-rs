# CDR-003 — Geometry 输入与定义域边界策略

- 状态：**Recommended for Approval**
- 日期：2026-09-21
- 范围：仅 P2 / G2 Geometry
- Reference：`pvlib/solarfactors` v1.6.1，`ecbfc863657e239817603a43898ae173c7ccad9c`
- 相关偏差：DEV-002、DEV-004、DEV-026

## 推荐决策

V1 使用以米为单位的有限闭区间 `GroundExtent { min_x, max_x }`。两个边界都必须
有限且满足 `min_x < max_x`。Reference 兼容默认值为 `[-100, 100]`；这是数值约定，
不是物理定义。应用 position predicate 后，所有 row 端点必须位于 extent 内或边界上。
地面投影阴影和地面分区裁剪到 extent；row 位于 extent 外时拒绝输入，不裁剪 row。
精确无限地面留待单独版本化模型。

每个 row 必须严格位于 `y=0` 上方。最小 clearance 必须大于 `1e-10 m`；接触或穿过
ground 均非法。校验在投影和分区构造前执行，返回 `GEOMETRY_CLEARANCE`，不得以 panic
作为可恢复输入错误。

axis azimuth 与 surface azimuth 必须有限，并用 Euclidean modulo 规范化到 `[0, 360)`。
非零 tilt 时，surface azimuth 必须在 angle comparison tolerance 内满足
`axis ± 90° (mod 360)`。tilt 精确为零时，surface azimuth 不会选择不同物理平面，
因此免除该关系检查，但仍记录规范化值。

V1 支持闭区间 `[0°, 90°]`。精确 `0°`、Reference 的 signed-zero 行为、正负 near-flat
rotation、精确 `90°` 与 near-`90°` 分别保留 fixture。大于 `90°` 返回
`GEOMETRY_TILT_UNSUPPORTED`，不得静默折叠，也不得借现有测试宣称已覆盖。

Geometry Gate 接受 `[0°, 90°]` 的 solar zenith。精确 `90°` 时状态为
`horizon_no_direct_projection`：row geometry 仍定义；不以巨大有限阴影代替退化投影；
direct-shadow surface 为 inactive；在 direct-projection 层中有限 ground 为 illuminated。
大于 `90°` 不在本合同内。parallel non-coincident 与 coincident projection 是不同类型。
rotation 精确为零才是 flat；near-flat 不强制归零。

全部标量 geometry 输入、角度及派生值必须有限。row count 至少为 1，width 与 GCR 必须
为正，V1 GCR 不得大于 1，cut 必须是至少为 1 的整数。非法 extent、shape、nonfinite、
cut、azimuth 关系、tilt 或 clearance 返回含 `code`、`field`、`message` 的结构化错误；
任何可恢复输入错误都不得 panic。

## 兼容性影响

默认 extent 复现 Reference 数值约定。可配置 extent、构造前拒绝非法输入与 `z=90°`
分类状态是 V1 有意决策。raw reference 证据保持不变；corrected expectation 通过 CDR / DEV
追溯差异，不重写 raw oracle。

## 批准效果

Owner 批准后，本策略才成为 P3 冻结输入。此前它仍是推荐，G2 保持
`CONDITIONALLY PASS`，Awaiting Repository Owner Approval。

