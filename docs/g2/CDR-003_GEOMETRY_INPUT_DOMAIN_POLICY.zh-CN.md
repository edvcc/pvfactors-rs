# CDR-003 — Geometry 输入与定义域边界策略

- 状态：**Recommended for Approval**
- 修订：**Owner Review Revision 1 incorporated**
- 日期：2026-09-22
- 范围：仅 P2 / G2 Geometry
- Reference：`pvlib/solarfactors` v1.6.1，`ecbfc863657e239817603a43898ae173c7ccad9c`
- 相关偏差：DEV-002、DEV-004、DEV-026、DEV-027

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

V1 支持闭区间 `[0°, 180°]`。精确 `0°`、Reference 的 signed-zero 行为、正负 near-flat
rotation、精确 `90°`、`120°` 与精确 `180°` 分别保留 fixture。大于 `90°` 的 tilt
既不折叠到 `[0°,90°]`，也不得交换 front/back 身份。`TILT_180` 将该边界记录为合法、
有限的完整朝向反转：row segment 保持宽度及稳定 front/back key；实测未产生需要新 CDR
的退化语义。tilt 小于 `0°` 或大于 `180°` 返回 `GEOMETRY_TILT_UNSUPPORTED`。

Geometry Gate 可表示 `[0°, 180°]` 的 solar zenith。小于 `90°` 为
`direct_projection`；精确 `90°` 为 `horizon_no_direct_projection`；大于 `90°` 且不超过
`180°` 为 `below_horizon_no_direct_projection`。两种 no-direct 状态均保留 row geometry；
direct-shadow logical slot 保留但 inactive；不制造伪巨大或 nonfinite shadow；有限 ground
是单一 illuminated direct-projection partition。Geometry 不决定完整 Simulation 是否 skip；
night、light 与 irradiance 政策留给 CDR-001。zenith 小于 `0°` 或大于 `180°` 非法。
parallel non-coincident 与 coincident geometric projection 仍是不同类型。rotation 精确为零
才是 flat；near-flat 不强制归零。

全部标量 geometry 输入、角度及派生值必须有限。row count 至少为 1，width 必须为正，
GCR 必须有限且严格大于 0，cut 必须是至少为 1 的整数。不得以 GCR 大于 1 作为工程常见
范围的代理拒绝；真实 row 相交、clearance 失败或其他 geometry 冲突按其实际规则判断。
`GCR_GT_1`（GCR 1.25、三排、tilt 45°）是 row segment 不相交的合法实例。非法 extent、
shape、nonfinite、cut、azimuth 关系、tilt 或 clearance 返回含 `code`、`field`、`message`
的结构化错误；任何可恢复输入错误都不得 panic。

## 兼容性影响

默认 extent 复现 Reference 数值约定。可配置 extent、构造前拒绝非法输入、扩展后的
tilt/GCR 输入域及三种 solar projection 状态都是 V1 有意决策。DEV-027 是表示层缺口，
不是 upstream bug：DEV-003 针对 Engine skip-mask，不能提供 Geometry 层状态。raw reference
证据保持不变；corrected expectation 以 field-level path、raw value、corrected value、CDR、
DEV 和 explanation 追溯差异，不重写 raw oracle。

## 批准效果

Owner 批准后，本策略才成为 P3 冻结输入。此前它仍是推荐，G2 保持
`CONDITIONALLY PASS`，Awaiting Repository Owner Approval。
