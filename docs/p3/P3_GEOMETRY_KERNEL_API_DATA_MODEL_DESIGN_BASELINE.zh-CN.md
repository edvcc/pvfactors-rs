# P3 Geometry Kernel API 与数据模型设计基线

- 状态：**APPROVED**
- 日期：2026-09-22
- 范围：P3 `solarfactors-core` math 与 Geometry API / 数据模型设计
- Approved Golden：`geometry-golden-v0.1`
- 治理决策：CDR-003、CDR-006
- 相关澄清：`CDR-006_IMPLEMENTATION_CLARIFICATION_FRAME_TOPOLOGY.zh-CN.md`
- 实现状态：**本文档未启动实现**

## 1. 目的与权威边界

本文档为下一项需要单独授权的 Rust module/type skeleton 任务冻结设计基线。它是工程规范，
不是实现，也不构成开始 Geometry 算法实现的授权。

本基线整合已批准 Geometry contract、corrected Golden expectation 与 Rust ownership boundary。
如本文档与已批准 CDR 或 immutable Approved Golden 冲突，以已批准证据为准，并将冲突标记为
`P3 DESIGN BLOCKER`；不得通过修改 Golden、放宽 tolerance 或复制偶然的 Python object model
解决冲突。

设计目标是：

```text
Algorithm Reconstruction
+ Independent Rust Domain Model
+ Approved Reference Compatibility
+ Stable Identity
+ Explicit Numerical Semantics
```

优先级为：

```text
Correctness
> Reference Verifiability
> Numerical Stability
> API Clarity
> Maintainability
> Performance
```

P3 使用独立的纯 Rust 模型重建已批准行为；不复刻 Python object graph，不在 runtime 引入
Python、pvlib、Shapely 或 GEOS，也不让 Golden JSON 形状成为 production API。

## 2. 证据基线与解释规则

本基线来源于：

- `docs/05_GEOMETRY_REIMPLEMENTATION_SPEC.md` 至
  `docs/12_PHASE_GATE_IMPLEMENTATION_PLAN.md` 中与 P3 相关的材料；
- 已批准的 CDR-003、CDR-006 及其双语文本、ACTIVE P3 Entry Contract、Geometry Golden
  Contract 与 Geometry Tolerance Profile v0.1；
- immutable `reference/approved/geometry-golden-v0.1` corpus；
- `reference/tools/geometry_golden.py` 中的 policy implementation 与 Owner Review 检查。

各证据层不得混淆：

1. `raw_reference` 记录冻结 upstream 的直接观察，包括缺陷；
2. `normalized_reference` 提供确定性、语言无关的顺序与表示，不修正行为；
3. `corrected_expectation` 只应用已批准的 CDR/DEV 决策；
4. 本 Rust 设计选择可重现已批准语义的 production representation，但不复制 Golden DTO 形状。

Comparison tolerance 不得改变 topology 或 algorithm predicate。Topology、key、ordering、
index mapping、classification 与 nonfinite class 必须精确一致。

## 3. 架构与生命周期

```text
ArrayLayout
    │
    ├── immutable static physical layout
    │
    └── GeometryFrameInput
             │
             ▼
         build_frame
             │
             ├── deterministic validation
             ├── RowGeometry[]
             ├── ProjectionClass
             ├── RowDirectShading[]
             ├── FrameTopology
             ├── SurfaceGeometry[]
             └── ActiveMap
                     │
                     ▼
                FrameGeometry
```

```text
SurfaceKey != ReferenceIndex != ActiveIndex != FrameIndex
```

`ArrayLayout` 针对静态配置构造并校验一次。`GeometryFrameInput` 是 typed raw frame value。
`build_frame` 校验二者组合并返回 owned `FrameGeometry`。结果通过 public API 保持 immutable，
供后续 View Factor 与 irradiance 阶段借用。Builder scratch、cut point、raw projection 与
validation intermediate 不得越过本次 build 生命周期，除非未来另行批准 trace contract。

## 4. 模块边界

第一版公开模块为：

```rust
pub mod math;
pub mod geometry;
```

crate root 初期不大量 re-export public surface。调用方式为：

```rust
solarfactors_core::math::Point2
solarfactors_core::geometry::ArrayLayout
```

`math` 拥有与领域无关的二维 primitive 和基础代数，不拥有 solarfactors identity、active/snap
policy、Geometry validation 或 differential-comparison tolerance。`geometry` 拥有
solarfactors domain、已批准 numerical predicate、frame construction、stable topology 与
structured Geometry error。

第一版数学 primitive 是 `Point2`、`Vec2`、`Segment2` 与 `Interval`。只有真实消费者证明
`Normal2`、`Direction2` 或 `UnitVec2` 的 invariant 能消除歧义时，才引入这些类型。

## 5. 数学值模型

### 5.1 `Point2`

`Point2` 表示二维欧氏空间中的位置。候选 public representation 为：

```rust
pub struct Point2 {
    pub x: f64,
    pub y: f64,
}
```

它支持 construction、finite inspection、point/vector arithmetic、distance 与 midpoint；
不携带 surface identity、endpoint snap、approximate equality 或任何 Geometry tolerance。

### 5.2 `Vec2`

`Vec2` 支持 dot、cross、norm、norm squared、scalar operation、finite inspection 与 fallible
normalization。预期内的数学退化以 typed outcome 返回；对 zero 或 nonfinite vector 的
normalization 不得用 NaN/Inf sentinel 表示结果。

### 5.3 `Segment2`

`Segment2` 是由两个有序端点定义的有界线段。它保留 caller 顺序，不自动执行
left/right、high/low 或 orientation reorder。`a == b` 是合法的 zero-length 数学线段；
这本身并不使其成为 active Geometry surface。

### 5.4 `Interval`

`Interval` 是字段封装且满足 `lo <= hi` 的有限闭区间；允许 `lo == hi`。普通 constructor
拒绝 NaN、infinity 与 reversed bounds。只有 caller 明确要求时，显式 `from_unordered`
才可 canonicalize bounds。`IntervalError` 表达构造失败，`IntervalDifference` 表达 0、1 或
2 个有序结果区间，不使用 sentinel。

### 5.5 Finite 与退化策略

`Point2`、`Vec2`、`Segment2` 不采用 `FiniteF64` wrapper。它们提供 `is_finite()`，但不承诺
普通代数对任意输入都保持 finite。任何进入持久 Geometry state 的值都必须在 Geometry
validation boundary 检查。`Interval` 是例外，因为其 ordering invariant 依赖 finite value。

Parallel、coincident、point touch、endpoint touch、positive overlap 与 zero length 是数学
outcome，不自动成为 Geometry error。预期退化必须使用 typed outcome，而不是 NaN/Inf。
除 public `IntervalDifference` 外，具体 outcome type 名称与 visibility 由真实消费者在实现时决定。

`math` 中不存在全局通用 `EPS`、`GEOMETRY_EPSILON`、`approx_eq` 或 `almost_equals`。
Active length、endpoint snap、orientation、line-offset 与 differential comparison 必须保持为
不同的具名 policy。

## 6. 静态输入模型

### 6.1 `ArrayLayout`

`ArrayLayout` 描述一个 Geometry batch 或 simulation configuration 中跨 frame 不变的值：

```text
n_pvrows
pvrow_width_m
pvrow_height_m
gcr
axis_azimuth_deg
ground_extent
row_cuts
```

`pitch = pvrow_width_m / gcr` 是派生值，不得成为第二个输入 source of truth。成功构造的
layout 通过 public API 保持 immutable。不存在 `ArrayLayout::default()`，因为没有具有领域意义
的唯一默认 PV array。

静态 invariant 包括：scalar finite；`n_pvrows >= 1`；width 为正；`gcr` finite 且大于 0；
finite extent 合法；每个 row 恰有一个 validated `RowCuts`；axis azimuth 已规范化。不得用
GCR 大于 1 作为代理规则拒绝输入；实际 row intersection 根据构造后的 frame geometry 检查。

### 6.2 `RowCuts`

`RowCuts` 为每排 front 与 back 分别保存正 cut count。Canonical validated layout representation
必须是 per-row，能够自然表达 `CUT_ASYMMETRIC`：row 1 front 为 `3`、back 为 `5`，不能只用
全局统一 cut。校验后的内部表示可采用 `NonZeroUsize`；public constructor 可接受普通 integer
并返回 structured error。具体 collection/container 是 implementation choice。

### 6.3 `GroundExtent`

`GroundExtent` 是 Geometry domain value，不是 `Interval` type alias。其 invariant 是以米为单位的
finite `min_x < max_x`，Approved default 为 `[-100, 100]`。Row endpoint 必须在 approved
position predicate 下位于 extent 内或边界；row 非法时拒绝，不通过 clipping 变成合法。
Projected ground shadow 与 ground partition 可以裁剪到 extent。

只建议 `GroundExtent::default()`。具体 constructor/getter 命名属于 implementation choice；
不得公开可破坏 invariant 的 mutation。

## 7. 动态输入与 validation boundary

`GeometryFrameInput` 只包含：

```text
surface_tilt_deg
surface_azimuth_deg
solar_zenith_deg
solar_azimuth_deg
```

它不包含 DNI、DHI、GHI、albedo、reflectivity、transmissivity、day of year、timestamp、
Perez configuration、solver configuration 或 execution policy。不存在
`GeometryFrameInput::default()`。

`GeometryFrameInput` 是 typed raw frame input，不证明该 frame 相对某个 layout 合法。
完整校验发生在：

```text
ArrayLayout + GeometryFrameInput -> build_frame
```

静态 layout 合法不代表每一个 frame 都合法。

### 7.1 确定性 fail-fast 顺序

Static layout validation 顺序冻结为：

```text
1. finite static scalars
2. row count
3. width
4. gcr
5. extent
6. cuts
7. axis azimuth normalization
```

Frame validation/build 顺序冻结为：

```text
1. finite frame scalars
2. tilt domain
3. solar zenith domain
4. normalize azimuths
5. surface-axis relation
6. row construction
7. clearance
8. extent containment
9. actual row intersection
10. projection / partition
11. numerical + invariant validation
```

校验按此顺序在首个失败处停止。该顺序可通过 `code` 与 `field` 观察；同一输入可能违反多条
规则，因此改变顺序必须经过审查。

## 8. Error contract

Public error type 为 `GeometryError` 与 `GeometryErrorCode`。`GeometryError` 至少包含：

```text
code
field
frame?  (FrameIndex)
row?
message
```

外部程序以 `code` 与 `field` 作为稳定判断依据；`message` 是人类诊断文本，不是可解析协议。
可恢复输入错误不得 panic。`panic=false` 属于 Golden adapter，不是 Rust error 字段。

必须 exact compatible 的 error code 为：

```text
GEOMETRY_CLEARANCE
GEOMETRY_CUT
GEOMETRY_TILT_UNSUPPORTED
GEOMETRY_NONFINITE
GEOMETRY_AZIMUTH_RELATION
GEOMETRY_EXTENT
```

只有出现真实 validation branch 时才可增加：

```text
GEOMETRY_ROW_COUNT
GEOMETRY_WIDTH
GEOMETRY_GCR
GEOMETRY_SOLAR_ZENITH_UNSUPPORTED
GEOMETRY_ROW_INTERSECTION
GEOMETRY_ROW_OUTSIDE_EXTENT
GEOMETRY_NUMERICAL_FAILURE
GEOMETRY_INVARIANT_VIOLATION
```

合法输入意外产生 nonfinite 时使用 `GEOMETRY_NUMERICAL_FAILURE`，不得归因于用户 nonfinite
输入。Topology 或 active-map invariant 被破坏时使用 `GEOMETRY_INVARIANT_VIOLATION`。

第一版自行实现 `Display` 与 `std::error::Error`，不引入 `thiserror`。

## 9. Projection classification 与 no-direct 行为

`ProjectionClass` 是 public closed enum：

```text
DirectProjection
HorizonNoDirectProjection
BelowHorizonNoDirectProjection
```

映射规则精确为 solar zenith 小于 `90°`、等于 `90°`、大于 `90°` 且不超过 `180°`。
构造成功后必须存储 classification；下游不得再次根据 solar zenith 猜测。

两种 no-direct class 均满足：

- row entity geometry 继续存在且 finite；
- 每排 front/back direct-shading length 均为 `0`；
- direct-projection PV surface 不 materialize 到所选 `FrameTopology`；
- 存在 `N` 个 inactive ground-shadow logical slot 与 1 个 active full-ground illuminated slot；
- 不制造伪巨大或 nonfinite shadow。

因此，N=3 时 Approved `SUN_90.0` 与 `SUN_BELOW_HORIZON` corrected expectation 均为
`logical_surface_count = 4`、`active_surface_count = 1`。若改成完整 40-slot inactive universe，
必须获得新的 CDR/Golden approval。

Geometry classification 不决定后续 Simulation 是否 skip timestep。

## 10. 稳定身份与索引模型

### 10.1 `SurfaceKey`

`SurfaceKey` 是 logical semantic identity，不包含 coordinate、length、normal、active state、
floating-point value 或 frame index。Production model 是 sum type：

```rust
pub enum SurfaceKey {
    Ground {
        source: GroundSource,
        element: usize,
        cut_interval: usize,
    },
    PvRow {
        row: usize,
        side: PvSide,
        segment: usize,
        illumination: Illumination,
    },
}
```

相关 public closed enum 为：

```text
GroundSource = Shadow | Illumination
PvSide = Front | Back
Illumination = Illuminated | Shaded
```

Golden adapter 将该 enum 映射为扁平 nullable DTO；production type 不增加大量 `Option` 字段
模仿 JSON。

当 logical surface 被 materialize 时，`SurfaceKey` 保持稳定；这不表示每种 projection state
都 materialize 同一个 surface universe。

### 10.2 `ReferenceIndex`

`ReferenceIndex` 是 distinct newtype，表示一个特定 `FrameTopology` 中按 Approved Reference
reconstruction order 排列的 logical surface index。其数值可读取，但外部不得任意构造。
它不是 `usize` 的语义 alias，也不得隐式转换为 `ActiveIndex`。

### 10.3 `ActiveIndex`

`ActiveIndex` 是 distinct newtype，表示某一 frame 中 dense active-compressed ordering，始终
是 frame-local。Inactive logical surface 没有 `ActiveIndex`。

### 10.4 `FrameIndex`

`FrameIndex` 是 distinct newtype，用于 caller 或 internal test 选择 frame，防止 frame integer
与 surface index 混淆，并保护 DEV-013 规则：所有 frame lookup 都实际计算请求的 frame，
包括 nonzero frame。

### 10.5 稳定性规则

完整解释以配套 CDR-006 implementation clarification 为准：

- `SurfaceKey` 是 logical surface materialize 时的稳定 semantic identity；
- `FrameTopology` 是 projection-state-specific logical surface universe；
- `ReferenceIndex` 属于一个 `FrameTopology`；
- logical topology 相同的 frame 必须保持准确的
  `SurfaceKey <-> ReferenceIndex` reconstruction order；
- projection-state transition 可以选择另一个已批准 `FrameTopology`。

## 11. Row 与 shading 模型

### 11.1 `RowGeometry`

`RowGeometry` 表示一个 frame 中某一 PV row 的物理二维几何，只存：

```text
center
ordered segment (b1 -> b2)
rotation_deg
front_normal
back_normal
```

它不重复存 width、height、row ID、highest point 或 lowest point。Width 由 segment 派生；
frame row collection 中的位置提供 row identity；最高/最低端点按 approved tie rule 派生。
Ordered segment 必须准确保留 `b1 -> b2`。

### 11.2 `RowDirectShading`

`RowDirectShading` 与 row entity 分离，存储：

```text
front_length_m
back_length_m
```

它是 row geometry、solar geometry 与 neighbor relationship 共同产生的结果。No-direct 状态
两者均为 0；在 approved predicate 下，长度必须位于 `[0, pvrow_width_m]`。

## 12. Surface、topology 与 active map

### 12.1 `SurfaceGeometry`

`SurfaceGeometry` 只存 `Segment2`。Length 始终通过 `segment.length()` 派生；不重复存
active state、`ActiveIndex`、normal、side、source、illumination、`SurfaceKey` 或
`ReferenceIndex`。

PV normal 由 `SurfaceKey` 的 row/side 与 `RowGeometry` 派生。P3 Geometry Golden 层的
ground normal 保持 absent；未来物理模块如需使用，可从 surface kind 派生。

### 12.2 `FrameTopology`

Production representation 是有序 `SurfaceKey` collection，不需要额外公开 `LogicalSurface`
wrapper。Invariant 为：

```text
SurfaceKey values are unique
ReferenceIndex values are dense 0..len-1
position i safely derives ReferenceIndex(i) inside this topology
ordering follows the approved reconstruction order
```

Vec position 是内部 representation invariant，identity 仍然是 `SurfaceKey`。

Direct projection 的准确顺序为：

1. ground shadow element 按 projected row、再按 cut interval；
2. ground illuminated element 按 ground order、再按 cut interval；
3. row 按 row order，每排 front 后 back，segment order，每段 illuminated 后 shaded。

所选 direct-projection topology 中保留 inactive logical slot。

No-direct projection 的顺序准确为：N 个 inactive ground-shadow key，随后一个 active
illuminated full-ground key。该 topology 不 materialize PV projection key。

### 12.3 `ActiveMap`

`ActiveMap` 存储双向映射：

```text
reference_to_active: ReferenceIndex -> Option<ActiveIndex>
active_to_reference: ActiveIndex -> ReferenceIndex
```

它必须满足 dense active index、bidirectional consistency 与 `inactive -> None`。Active
surface 的 endpoint finite，且 length 严格大于 `1e-8 m`。过滤或合并只能生成 active view，
且必须保留完整 logical mapping；不同 source、side、normal、material 或 visibility 的正长度
surface 不得合并。

### 12.4 `FrameGeometry`

逻辑结果为：

```text
FrameGeometry
├── ProjectionClass
├── RowGeometry[]
├── RowDirectShading[]
├── FrameTopology
├── SurfaceGeometry[]
└── ActiveMap
```

核心 invariant 为：

```text
FrameTopology.len
== SurfaceGeometry.len
== ActiveMap.reference_to_active.len
```

Row 与 shading collection 也必须按 row order 各有 `ArrayLayout.n_pvrows` 个条目。
`FrameGeometry` 是 owned output，通过 public API 保持 immutable。

## 13. Stored 与 derived 值

| Concept | Stored | Derived / reason |
|---|---|---|
| `RowGeometry.center` | Yes | Frame entity state |
| `RowGeometry.segment` | Yes | Canonical ordered row coordinates |
| `RowGeometry.rotation_deg` | Yes | Approved orientation result |
| Front/back row normals | Yes | 每排共享一次，不在 cut surface 重复 |
| Row width and height | No | width 从 segment 派生；static height 属于 layout input |
| Highest/lowest endpoint | No | 按 approved tie rule 派生 |
| `RowDirectShading` lengths | Yes | Frame result，不属于 row entity state |
| `ProjectionClass` | Yes | 防止下游重新分类 |
| `FrameTopology` key order | Yes | Exact logical reconstruction contract |
| `ReferenceIndex` | No separate field | 从 topology position 派生 |
| `SurfaceGeometry.segment` | Yes | Minimal numerical surface state |
| Surface length | No | 从 `segment.length()` 派生 |
| Surface active boolean | No separate source | 由 approved active predicate 派生并在 `ActiveMap` 表示 |
| `ActiveMap` | Yes | Dense compression 不能脱离 policy 仅从 geometry 推出 |
| PV surface normal | No | 从 row、side 与 `RowGeometry` 派生 |
| Side/source/illumination | No duplicate | 从 `SurfaceKey` 派生 |
| Golden flat DTO fields | No | Test/reference adapter concern |

目标是每项事实只有一个 source of truth。若未来缓存 derived value，必须有实测消费者与明确
一致性策略。

## 14. Public 与 internal API 矩阵

| Component | Visibility | Reason |
|---|---|---|
| `Point2` | public | 稳定二维数学值 |
| `Vec2` | public | 稳定 vector algebra 值 |
| `Segment2` | public | 有序有界线段值 |
| `Interval` | public | 可复用 finite closed interval |
| `IntervalError` | public | Constructor failure contract |
| `IntervalDifference` | public | Typed set-operation result |
| `ArrayLayout` | public | 主要 static Geometry input |
| `RowCuts` | public | Per-row front/back discretization input |
| `GroundExtent` | public | Validated Geometry domain extent |
| `GeometryFrameInput` | public | Typed raw frame input |
| `SurfaceKey` 与相关 enum | public | Stable semantic identity |
| `ReferenceIndex` | public，restricted constructor | Observable reconstruction index |
| `ActiveIndex` | public，restricted constructor | Observable compressed index |
| `FrameIndex` | public | 防止 frame/surface index 混淆 |
| `ProjectionClass` | public | 成功构造后的显式 classification |
| `RowGeometry` | public | Physical row result |
| `RowDirectShading` | public | Direct-shading result |
| `FrameTopology` | public | Ordered logical surface universe |
| `SurfaceGeometry` | public | Minimal numerical surface geometry |
| `ActiveMap` | public | Exact logical/active mapping |
| `FrameGeometry` | public | 主要 Geometry result |
| `GeometryError`、`GeometryErrorCode` | public | Stable failure contract |
| `build_frame` | public | P3 唯一主要算法入口 |
| Numerical predicate helper | crate-private | Approved algorithm policy，不是独立 API |
| `ValidatedFrameInput`、`SolarSection` | crate-private | Build intermediate |
| Cut/shade/projection builder | private 或 crate-private | Implementation pipeline |
| Partition/topology/active-map builder | private 或 crate-private | 保持单一 public 入口与 invariant |
| `GeometryBuildTrace` | private，除非另行批准 | 尚无 public trace contract |
| Golden DTO/reference adapter | test-only | Development oracle concern |

## 15. 主要 API 与禁止公开的 surface

P3 唯一主要计算入口是：

```rust
pub fn build_frame(
    layout: &ArrayLayout,
    input: &GeometryFrameInput,
) -> Result<FrameGeometry, GeometryError>;
```

P3 不增加 `GeometryEngine`、`GeometryCalculator`、`GeometryContext` 或 `GeometryService`。
当前不设计 `GeometryBatch`、`GeometrySeries` 或 `build_frames`；在后续 Simulation
`InputBatch` contract 设计前，DEV-013 通过 crate-internal/test multi-frame facility 验证。

以下内容不得 public：`ValidatedFrameInput`、`SolarSection`、`CutPoint`、
`GeometryBuildTrace`、predicate/snap helper、row/projection/shade/PV-partition/
ground-partition/topology/active-map builder、Golden DTO 与 reference adapter。

## 16. Serialization、default 与 evolvability

Public domain type 不因读取 Golden JSON 而 derive `serde::Serialize` 或 `Deserialize`。
Serialization 属于 test support；本基线不引入 `serde` dependency。

只建议 `GroundExtent::default()`。`ArrayLayout` 与 `GeometryFrameInput` 没有领域上有意义的
default。

对于很可能扩展的 `GeometryErrorCode` 与 `SurfaceKey`，`#[non_exhaustive]` 是
implementation-time recommendation。它影响 downstream matching 与 construction，必须在
真实 type declaration review 时评估。`PvSide`、`Illumination`、`ProjectionClass` 等稳定
closed enum 不机械添加该属性。本文档不声称任何 attribute 已经实现。

## 17. 数值策略边界

已批准 Geometry predicate 为：

```text
active length:        length > 1e-8 m
endpoint snap:        distance < 1e-8 m
orientation cross:    <= max(1e-12, 64 * f64_epsilon)
line offset:           <= max(1e-10 m,
                              64 * f64_epsilon * max(1 m, coordinate_scale))
```

严格或包含的 operator 属于 contract。Differential profile（`orientation`、`position`、
`length`、`angle`）只判断数值一致性，不能决定 activity、snap、orientation 或 topology。

共线 interval subtraction 以数学正确结果为准；complete cover 返回空 difference，符合
`PRIM_COMPLETE_COVER_DIFFERENCE` 的批准结果。Point touch 与 endpoint touch 不产生正长度
shade。Parallel non-coincident 与 coincident projection 是不同 typed outcome。

## 18. Invariant 与 forbidden state

成功的 `FrameGeometry` 必须满足所有适用 invariant：

- 所有 stored point、vector、coordinate、angle 与 derived scalar finite；
- 每个 row segment 保留 approved endpoint order 与 width；
- 每排严格高于 approved clearance 且位于 extent 内；
- row segment 不实际相交；
- 每个 PV side 的 illuminated length 加 shaded length 等于 width；
- shade length 位于 `[0, width]`；
- finite ground 完整覆盖且无 positive overlap 或 unexplained gap；
- topology key unique，reconstruction index dense；
- 对 active surface，active-map 双向映射准确互逆；
- active endpoint finite 且 active length 严格大于 threshold；
- key、side、coordinate、row geometry 与 derived normal 一致；
- full mirror 同时变换 row geometry、solar vector、normal、extent、row order 与 side
  interpretation。

Forbidden state 包括：持久 Geometry state 中的 nonfinite、同一 topology 内重复
`SurfaceKey`、active surface 无 reverse map、inactive surface 带 `ActiveIndex`、不经显式
remapping 使用另一 topology 的 `ReferenceIndex`、通过 clipping 让 row 合法、或以 numerical
tolerance 隐藏 topology 变化。

## 19. Dependency 与 ownership 策略

第一版实现继续保持 normal dependency 为 0。本设计不要求 `thiserror`、`serde`、
`serde_json`、`proptest`、`approx`、`nalgebra`、`geo`、`ndarray` 或 `ordered-float`。
只有实现中出现真实消费者并审查取舍后，才重新评估 dependency。

`build_frame` 借用输入；output 拥有后续阶段所需的值。Python object、Shapely geometry、
global mutable configuration、solver/execution state 均不得进入 Geometry model。

## 20. Approved evidence anchor

下一阶段实现与测试至少必须保留下列 observable anchor：

- `CUT_ASYMMETRIC`：row 1 front segment 为 `0..2`，back segment 为 `0..4`，每段顺序为
  illuminated 后 shaded；
- `MULTI_TIMESTEP_NONZERO_INDEX`：实际计算请求的 frame 1，同时对相同 topology 保持
  logical/reference identity 稳定；
- `SUN_90.0`：horizon no-direct topology 包含 3 个 inactive shadow slot 与 1 个 active
  full-ground illuminated slot；
- `SUN_BELOW_HORIZON`：topology 形状相同，classification 为 below-horizon；
- `PRIM_COMPLETE_COVER_DIFFERENCE`：complete cover 结果为空；
- active、snap、orientation、line-offset 的 ±ULP case 保持各自准确 predicate boundary
  operator。

## 21. Implementation choice 与 blocker

下列内容是下一任务中的非阻塞 `Implementation Choice`：

- 物理文件数量与 internal module layout；
- constructor/getter 的具体命名；
- validated per-row cuts 的具体 collection；
- 数学退化 private typed outcome 的名称；
- allocation 与 scratch reuse 策略；
- 是否用 cached lookup 加速 `SurfaceKey` 访问，同时仍以 ordered topology 为 source of truth。

本次基线整合未发现新的 `P3 DESIGN BLOCKER`。若后续实现证据与已批准 CDR 或 Golden 字段
冲突，必须在冲突处停止，不得静默选择新语义。

## 22. 审查与变更控制

Repository Owner 已完成批准。本文档现为后续 Math + Geometry Module Skeleton and Public
Type Declaration Bootstrap 独立任务的权威输入；该批准本身不代表算法正确性或 G3 通过。

Projection classification、no-direct topology、stable identity、predicate 数值/operator、
validation order 或 approved error compatibility 的任何变化都需要明确审查；如改变已批准
语义，还需要新建或 supersede CDR/Golden object。上述 implementation detail 只有在改变
observable contract 时才升级为 CDR。
