# CDR-006 — Geometry 数值 Predicate 与稳定 Topology 策略

- 状态：**Recommended for Approval**
- 日期：2026-09-21
- Reference：`pvlib/solarfactors` v1.6.1，`ecbfc863657e239817603a43898ae173c7ccad9c`
- 相关偏差：DEV-013、DEV-016、DEV-026

## Reference tolerance 审计

`DISTANCE_TOLERANCE = 1e-8 m` 参与端点 containment/snap、zero/active 分类、surface
过滤与 cleanup；这些分支属于可观察的兼容行为。`TOL_COLLINEAR = 1e-5` 作用于未规范化
的 dot/cross 类量；仅缩放同方向向量也可能改变结果，因此它是 Python/Reference 实现细节，
不是无量纲物理 tolerance。基于 Shapely buffer 的 cleanup 也不是 V1 物理定义。

## 推荐 predicate

- Active numerical surface：严格 `length > 1e-8 m`；等于阈值时 inactive，首版保留
  Reference topology 边界。
- Endpoint snap：距离严格 `< 1e-8 m` 时 snap 到原始 canonical endpoint；等于阈值不 snap。
  Snap 仅能在该命名分支内改变坐标与长度，不得重排 logical key。
- Orientation/parallelism：使用 normalized absolute cross product，阈值为
  `max(1e-12, 64 * f64_epsilon)`；不得用于 distance、activity 或 comparison acceptance。
- 到支撑线的位置偏移使用
  `max(1e-10 m, 64 * f64_epsilon * max(1 m, coordinate_scale))`。
- `geometry-tolerance-v0.1` 的 comparison tolerance 不得替代 algorithm predicate，
  也不得改变 topology。

Scale-aware 项只用于 orientation 与 line-offset predicate，不缩放 active-length 或
endpoint-snap 边界。替代 `TOL_COLLINEAR` 导致的 Reference topology 差异必须登记具体字段
和案例，不得通过放宽 comparator 吞掉。

## 集合运算与 touching 分类

共线 subtraction 以 interval arithmetic 为准。`v` 完全覆盖 `u` 时，`u - v` 为空。
冻结 Reference 在 `PRIM_COMPLETE_COVER_DIFFERENCE` 中返回长度 `1 m`；corrected expectation
为空，并以 DEV-016 / CDR-006 追溯。不得修改 raw evidence。

Point touch 是非端点的单点相交；endpoint touch 是共享 canonical endpoint；
positive-length overlap 的交集长度大于 active threshold；tolerance touch 是距离位于命名
snap 或 line-offset predicate 内的点/端点。point touch 与 endpoint touch 不产生正长度阴影。
Coincident 与 parallel projection 保持为不同类型。

## 稳定身份与顺序

`LogicalSurfaceIdentity` 使用稳定 `SurfaceKey`：

`{kind, source, row, side, segment, illumination, ground_element, cut_interval}`。

即使数值长度为零，该身份也存在。`ReferenceIndex` 单独记录冻结 Reference matrix 顺序。
`ActiveIndex` 是每帧中仅对 `length > 1e-8 m` surface 建立的 optional mapping，不是身份。
临时 `Vec` 位置不得成为外部标识。

外部/重建顺序精确规定为：ground shadow 按投影 row 与 cut interval；ground illumination
按地面顺序与 cut interval；row 从左到右，每排 front 后 back，segment 顺序，illuminated
后 shaded。inactive slot 保留在 logical order。过滤或合并只可生成 active view，且必须保留
完整 key-to-active map；不同 source、side、normal、material 或 visibility 的正长度区域不得合并。

## 批准效果

Owner 批准后，本 predicate 与 topology 语义才对 P3 冻结。此前 G2 保持
`CONDITIONALLY PASS`，Awaiting Repository Owner Approval。

